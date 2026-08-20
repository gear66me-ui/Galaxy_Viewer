import { chromium } from 'playwright';
import fs from 'node:fs/promises';

const CATALOGS = [
  {
    provider: 'HUBBLE',
    url: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0018.json'
  },
  {
    provider: 'JWST',
    url: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0002.json'
  }
];

const RUNS = Math.max(1, Number(process.env.RUNS || 3));
const CONCURRENCY = Math.max(1, Number(process.env.CONCURRENCY || 4));
const NAV_TIMEOUT_MS = Math.max(5000, Number(process.env.NAV_TIMEOUT_MS || 45000));
const SETTLE_TIMEOUT_MS = Math.max(1000, Number(process.env.SETTLE_TIMEOUT_MS || 10000));
const OUT_CSV = 'test/ESA-LINK-HEALTH-LATEST.csv';
const OUT_MD = 'test/ESA-LINK-HEALTH-LATEST.md';
const OUT_HTML = 'test/ESA-LINK-HEALTH-LATEST.html';

function escCsv(v){
  const s = String(v ?? '');
  return /[",\n]/.test(s) ? `"${s.replaceAll('"','""')}"` : s;
}
function escHtml(v){
  return String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function median(values){
  const a = values.filter(Number.isFinite).sort((a,b)=>a-b);
  if(!a.length) return null;
  const m = Math.floor(a.length/2);
  return a.length % 2 ? a[m] : Math.round((a[m-1]+a[m])/2);
}
function p95(values){
  const a = values.filter(Number.isFinite).sort((a,b)=>a-b);
  if(!a.length) return null;
  return a[Math.min(a.length-1, Math.ceil(a.length*0.95)-1)];
}
function providerFromUrl(url, fallback='UNKNOWN'){
  try{
    const h = new URL(url).hostname.toLowerCase();
    if(h.includes('esahubble.org')) return 'HUBBLE';
    if(h.includes('esawebb.org')) return 'JWST';
  }catch{}
  return fallback;
}
function collectEntries(root, providerHint){
  const out=[];
  const seen=new Set();
  function walk(node){
    if(!node) return;
    if(Array.isArray(node)){ for(const x of node) walk(x); return; }
    if(typeof node !== 'object') return;
    const sourceUrl = typeof node.sourceUrl === 'string' ? node.sourceUrl.trim() : typeof node.officialUrl === 'string' ? node.officialUrl.trim() : '';
    if(sourceUrl && /^https:\/\//i.test(sourceUrl)){
      let host='';
      try{ host = new URL(sourceUrl).hostname.toLowerCase(); }catch{}
      if(host.includes('esahubble.org') || host.includes('esawebb.org')){
        if(!seen.has(sourceUrl)){
          seen.add(sourceUrl);
          out.push({
            provider: providerFromUrl(sourceUrl, providerHint),
            archiveId: String(node.archiveId || node.id || '').trim(),
            name: String(node.displayName || node.commonName || node.name || node.title || '').trim(),
            sourceUrl
          });
        }
      }
    }
    for(const [k,v] of Object.entries(node)){
      if(k === 'sourceUrl' || k === 'officialUrl') continue;
      if(v && typeof v === 'object') walk(v);
    }
  }
  walk(root);
  return out;
}
async function fetchCatalogs(){
  const all=[];
  for(const cat of CATALOGS){
    console.log(`Fetching ${cat.provider}: ${cat.url}`);
    const r = await fetch(cat.url, {cache:'no-store', headers:{'cache-control':'no-cache'}});
    if(!r.ok) throw new Error(`${cat.provider} catalog HTTP ${r.status}`);
    const data = await r.json();
    const entries = collectEntries(data, cat.provider);
    console.log(`${cat.provider}: ${entries.length} unique ESA source URLs`);
    all.push(...entries);
  }
  const dedup=new Map();
  for(const e of all) dedup.set(e.sourceUrl,e);
  return [...dedup.values()];
}
function classifyEmbed(headers){
  const xfo = String(headers['x-frame-options'] || '').trim();
  const csp = String(headers['content-security-policy'] || '').trim();
  const frameAncestors = /(?:^|;)\s*frame-ancestors\s+([^;]+)/i.exec(csp)?.[1]?.trim() || '';
  let blocked=false;
  const reasons=[];
  if(/DENY|SAMEORIGIN/i.test(xfo)){ blocked=true; reasons.push(`X-Frame-Options: ${xfo}`); }
  if(frameAncestors){
    if(/'none'/i.test(frameAncestors)){ blocked=true; reasons.push(`CSP frame-ancestors ${frameAncestors}`); }
    else if(/'self'/i.test(frameAncestors) && !/gear66me-ui\.github\.io/i.test(frameAncestors)){ blocked=true; reasons.push(`CSP frame-ancestors ${frameAncestors}`); }
  }
  return {xfo,frameAncestors,blocked,reasons:reasons.join(' | ')};
}
async function coldRun(browser, entry, run){
  const context = await browser.newContext({serviceWorkers:'block'});
  const page = await context.newPage();
  const cdp = await context.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
  let requests=0, failedRequests=0;
  page.on('request',()=>requests++);
  page.on('requestfailed',()=>failedRequests++);
  const started=performance.now();
  let response=null, domMs=null, loadMs=null, settledMs=null, error='';
  try{
    response=await page.goto(entry.sourceUrl,{waitUntil:'domcontentloaded',timeout:NAV_TIMEOUT_MS});
    domMs=Math.round(performance.now()-started);
    try{ await page.waitForLoadState('load',{timeout:NAV_TIMEOUT_MS}); loadMs=Math.round(performance.now()-started); }catch(e){ error+=`load:${e.message}; `; }
    try{ await page.waitForLoadState('networkidle',{timeout:SETTLE_TIMEOUT_MS}); }catch{}
    settledMs=Math.round(performance.now()-started);
  }catch(e){ error+=`goto:${e.message}; `; }
  let timing={};
  try{
    timing=await page.evaluate(()=>{
      const n=performance.getEntriesByType('navigation')[0];
      if(!n) return {};
      return {
        dnsMs:Math.max(0,n.domainLookupEnd-n.domainLookupStart),
        connectMs:Math.max(0,n.connectEnd-n.connectStart),
        tlsMs:n.secureConnectionStart>0?Math.max(0,n.connectEnd-n.secureConnectionStart):0,
        ttfbMs:Math.max(0,n.responseStart-n.requestStart),
        responseDownloadMs:Math.max(0,n.responseEnd-n.responseStart),
        transferSize:n.transferSize,
        redirectCount:n.redirectCount
      };
    });
  }catch{}
  const headers=response?await response.allHeaders().catch(()=>({})):{};
  const embed=classifyEmbed(headers);
  const status=response?response.status():null;
  const stale = status===404 || status===410 || !response || /ERR_NAME_NOT_RESOLVED/i.test(error);
  const result={...entry,run,status,ok:!!response&&response.ok(),finalUrl:page.url(),domMs,loadMs,settledMs,requests,failedRequests,stale,embedBlocked:embed.blocked,embedReasons:embed.reasons,xFrameOptions:embed.xfo,frameAncestors:embed.frameAncestors,...timing,error:error.trim()};
  await context.close();
  return result;
}
async function mapLimit(items,limit,fn){
  const results=new Array(items.length);
  let next=0;
  async function worker(){
    while(true){
      const i=next++;
      if(i>=items.length) return;
      results[i]=await fn(items[i],i);
    }
  }
  await Promise.all(Array.from({length:limit},worker));
  return results;
}
function summarize(entries,runs){
  const byUrl=new Map();
  for(const r of runs){ if(!byUrl.has(r.sourceUrl)) byUrl.set(r.sourceUrl,[]); byUrl.get(r.sourceUrl).push(r); }
  return entries.map(e=>{
    const rr=byUrl.get(e.sourceUrl)||[];
    const loads=rr.map(x=>x.loadMs);
    const settled=rr.map(x=>x.settledMs);
    const dom=rr.map(x=>x.domMs);
    const statusCodes=[...new Set(rr.map(x=>x.status).filter(x=>x!==null))];
    const medLoad=median(loads);
    const medSettled=median(settled);
    let classification='FAST';
    if(rr.some(x=>x.stale)) classification='STALE/FAILED';
    else if(medLoad===null) classification='FAILED';
    else if(medLoad>=15000) classification='VERY SLOW';
    else if(medLoad>=10000) classification='SLOW';
    else if(medLoad>=5000) classification='MODERATE';
    if(rr.some(x=>x.embedBlocked) && classification==='FAST') classification='FAST / EMBED BLOCKED';
    return {
      ...e,
      classification,
      runs:rr.length,
      statusCodes:statusCodes.join(','),
      allOk:rr.length===RUNS && rr.every(x=>x.ok),
      stale:rr.some(x=>x.stale),
      embedBlocked:rr.some(x=>x.embedBlocked),
      embedReasons:[...new Set(rr.map(x=>x.embedReasons).filter(Boolean))].join(' | '),
      medianDomMs:median(dom),
      medianLoadMs:medLoad,
      p95LoadMs:p95(loads),
      medianSettledMs:medSettled,
      p95SettledMs:p95(settled),
      maxFailedRequests:Math.max(0,...rr.map(x=>x.failedRequests||0)),
      errors:rr.map(x=>x.error).filter(Boolean).join(' | ')
    };
  }).sort((a,b)=>(b.medianLoadMs??-1)-(a.medianLoadMs??-1));
}
function fmtMs(v){ return Number.isFinite(v)?`${(v/1000).toFixed(2)} s`:'—'; }
function buildMarkdown(summary,counts){
  const lines=[];
  lines.push('# ESA/Hubble + ESA/Webb Link Health Report','');
  lines.push(`Generated: ${new Date().toISOString()}`,'');
  lines.push(`Catalogs tested: Hubble full-0018 and JWST full-0002. Cold-cache runs per URL: ${RUNS}.`,'');
  lines.push(`- Unique URLs: ${counts.unique}`);
  lines.push(`- Hubble URLs: ${counts.hubble}`);
  lines.push(`- JWST URLs: ${counts.jwst}`);
  lines.push(`- Stale/failed: ${counts.stale}`);
  lines.push(`- Slow (>=10 s median load): ${counts.slow}`);
  lines.push(`- Very slow (>=15 s median load): ${counts.verySlow}`);
  lines.push(`- Likely iframe/embed blocked: ${counts.embedBlocked}`,'');
  lines.push('| Class | Provider | Archive ID | Name | HTTP | Median DOM | Median Load | P95 Load | Median Settled | Embed blocked | URL |');
  lines.push('|---|---|---|---|---:|---:|---:|---:|---:|---|---|');
  for(const r of summary){
    lines.push(`| ${r.classification} | ${r.provider} | ${r.archiveId||''} | ${(r.name||'').replaceAll('|','\\|')} | ${r.statusCodes||'—'} | ${fmtMs(r.medianDomMs)} | ${fmtMs(r.medianLoadMs)} | ${fmtMs(r.p95LoadMs)} | ${fmtMs(r.medianSettledMs)} | ${r.embedBlocked?'YES':'NO'} | ${r.sourceUrl} |`);
  }
  lines.push('','## Notes','');
  lines.push('- STALE/FAILED means HTTP 404/410, DNS failure, or no main-document response.');
  lines.push('- SLOW means median full load >= 10 seconds; VERY SLOW means >= 15 seconds.');
  lines.push('- Embed blocked means response headers indicate iframe/WebView embedding may be refused even if the page opens directly in a browser.');
  lines.push('- This report is regenerated each time the test workflow is run.');
  return lines.join('\n');
}
function buildHtml(summary,counts){
  const rows=summary.map(r=>`<tr class="${r.stale?'bad':r.medianLoadMs>=10000?'slow':r.embedBlocked?'warn':'ok'}"><td>${escHtml(r.classification)}</td><td>${escHtml(r.provider)}</td><td>${escHtml(r.archiveId)}</td><td>${escHtml(r.name)}</td><td>${escHtml(r.statusCodes||'—')}</td><td>${escHtml(fmtMs(r.medianDomMs))}</td><td>${escHtml(fmtMs(r.medianLoadMs))}</td><td>${escHtml(fmtMs(r.p95LoadMs))}</td><td>${escHtml(fmtMs(r.medianSettledMs))}</td><td>${r.embedBlocked?'YES':'NO'}</td><td><a href="${escHtml(r.sourceUrl)}" target="_blank" rel="noopener">OPEN</a></td><td>${escHtml(r.errors)}</td></tr>`).join('');
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ESA Link Health Report</title><style>body{font-family:system-ui;background:#07111f;color:#edf7ff;margin:0}header{position:sticky;top:0;background:#0d2138;padding:14px;border-bottom:1px solid #3478b5}main{padding:12px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px}.card{background:#102a45;border:1px solid #2f6796;border-radius:8px;padding:10px}.card b{display:block;font-size:22px}table{width:100%;border-collapse:collapse;font-size:12px;margin-top:14px}th,td{padding:7px;border-bottom:1px solid #1d405f;text-align:left;vertical-align:top}th{position:sticky;top:86px;background:#0d2138}.bad{background:#431d25}.slow{background:#4a3816}.warn{background:#31331a}.ok{background:#0c281f}a{color:#74c8ff}</style></head><body><header><h2>ESA/Hubble + ESA/Webb Link Health Report</h2><div>Generated ${escHtml(new Date().toISOString())} — ${RUNS} cold-cache runs per URL</div></header><main><div class="cards"><div class="card">Unique URLs<b>${counts.unique}</b></div><div class="card">Hubble<b>${counts.hubble}</b></div><div class="card">JWST<b>${counts.jwst}</b></div><div class="card">Stale/failed<b>${counts.stale}</b></div><div class="card">Slow >=10s<b>${counts.slow}</b></div><div class="card">Very slow >=15s<b>${counts.verySlow}</b></div><div class="card">Embed blocked<b>${counts.embedBlocked}</b></div></div><table><thead><tr><th>Class</th><th>Provider</th><th>ID</th><th>Name</th><th>HTTP</th><th>DOM</th><th>Load</th><th>P95 Load</th><th>Settled</th><th>Embed</th><th>Link</th><th>Errors</th></tr></thead><tbody>${rows}</tbody></table></main></body></html>`;
}

const entries=await fetchCatalogs();
const work=[];
for(const entry of entries) for(let run=1;run<=RUNS;run++) work.push({entry,run});
console.log(`Testing ${entries.length} unique URLs, ${work.length} cold-cache page loads, concurrency ${CONCURRENCY}.`);
const browser=await chromium.launch({headless:true});
let done=0;
let runs=[];
try{
  runs=await mapLimit(work,CONCURRENCY,async ({entry,run})=>{
    const result=await coldRun(browser,entry,run);
    done++;
    console.log(`[${done}/${work.length}] ${entry.provider} ${entry.archiveId||entry.name} run ${run}/${RUNS}: HTTP ${result.status} load=${result.loadMs}ms settled=${result.settledMs}ms stale=${result.stale} embedBlocked=${result.embedBlocked}`);
    return result;
  });
} finally { await browser.close(); }
const summary=summarize(entries,runs);
const counts={
  unique:summary.length,
  hubble:summary.filter(x=>x.provider==='HUBBLE').length,
  jwst:summary.filter(x=>x.provider==='JWST').length,
  stale:summary.filter(x=>x.stale).length,
  slow:summary.filter(x=>Number.isFinite(x.medianLoadMs)&&x.medianLoadMs>=10000).length,
  verySlow:summary.filter(x=>Number.isFinite(x.medianLoadMs)&&x.medianLoadMs>=15000).length,
  embedBlocked:summary.filter(x=>x.embedBlocked).length
};
const csvCols=['classification','provider','archiveId','name','sourceUrl','runs','statusCodes','allOk','stale','embedBlocked','embedReasons','medianDomMs','medianLoadMs','p95LoadMs','medianSettledMs','p95SettledMs','maxFailedRequests','errors'];
const csv=[csvCols.join(','),...summary.map(r=>csvCols.map(c=>escCsv(r[c])).join(','))].join('\n');
await fs.writeFile(OUT_CSV,csv,'utf8');
await fs.writeFile(OUT_MD,buildMarkdown(summary,counts),'utf8');
await fs.writeFile(OUT_HTML,buildHtml(summary,counts),'utf8');
console.log('Reports written:');
console.log(`- ${OUT_MD}`);
console.log(`- ${OUT_CSV}`);
console.log(`- ${OUT_HTML}`);
