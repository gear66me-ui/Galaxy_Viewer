import fs from 'node:fs/promises';

const CATALOGS = [
  ['HUBBLE','https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0018.json'],
  ['JWST','https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0002.json'],
  ['CHANDRA','https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0001.json']
];

const RUNS = Math.max(1, Number(process.env.RUNS || 2));
const CONCURRENCY = Math.max(1, Number(process.env.CONCURRENCY || 10));
const TIMEOUT_MS = Math.max(5000, Number(process.env.TIMEOUT_MS || 30000));
const RETRIES = Math.max(0, Number(process.env.RETRIES || 2));
const MAX_BYTES = Math.max(65536, Number(process.env.MAX_BYTES || 262144));
const OUT_MD='test/ESA-LINK-HEALTH-LATEST.md';
const OUT_CSV='test/ESA-LINK-HEALTH-LATEST.csv';
const OUT_HTML='test/ESA-LINK-HEALTH-LATEST.html';
const OUT_JSON='test/ESA-LINK-HEALTH-LATEST.json';

const IMAGE_KEYS = new Set([
  'selectedImageUrl','esaPublicationJpeg','imageUrl','imageURL','hdImageUrl','fullImageUrl',
  'fullResUrl','downloadUrl','downloadURL','jpegUrl','jpgUrl','pngUrl','assetUrl','githubImageUrl'
]);
const IMAGE_ARRAY_KEYS = new Set(['jpegCandidates','imageCandidates','downloadCandidates','assetCandidates']);

const sleep = ms => new Promise(r=>setTimeout(r,ms));
const fmtMs=v=>Number.isFinite(v)?`${(v/1000).toFixed(2)} s`:'—';
const escHtml=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const escCsv=v=>{const s=String(v??'');return /[",\n]/.test(s)?`"${s.replaceAll('"','""')}"`:s;};
function median(a){const b=a.filter(Number.isFinite).sort((x,y)=>x-y); if(!b.length)return null; const m=Math.floor(b.length/2); return b.length%2?b[m]:Math.round((b[m-1]+b[m])/2);}
function p95(a){const b=a.filter(Number.isFinite).sort((x,y)=>x-y); if(!b.length)return null; return b[Math.min(b.length-1,Math.ceil(b.length*.95)-1)];}
function looksImageUrl(v){
  if(typeof v!=='string' || !/^https:\/\//i.test(v.trim())) return false;
  const s=v.toLowerCase();
  return /\.(jpe?g|png|webp|gif|tiff?)(?:[?#]|$)/i.test(s) || /image|photo|media|asset|download/.test(s);
}
function extractEntries(root,provider){
  const out=[]; const seen=new Set();
  function add(node,key,url){
    url=String(url||'').trim(); if(!looksImageUrl(url) || seen.has(url)) return;
    seen.add(url);
    out.push({provider,archiveId:String(node.archiveId||node.id||'').trim(),name:String(node.displayName||node.commonName||node.name||node.title||'').trim(),field:key,url,sourceUrl:String(node.sourceUrl||node.officialUrl||'').trim()});
  }
  function walk(node){
    if(!node) return;
    if(Array.isArray(node)){for(const v of node) walk(v); return;}
    if(typeof node!=='object') return;
    for(const [k,v] of Object.entries(node)){
      if(IMAGE_KEYS.has(k) && typeof v==='string') add(node,k,v);
      else if(IMAGE_ARRAY_KEYS.has(k) && Array.isArray(v)) for(const x of v) if(typeof x==='string') add(node,k,x);
    }
    for(const [k,v] of Object.entries(node)) if(v && typeof v==='object' && !IMAGE_ARRAY_KEYS.has(k)) walk(v);
  }
  walk(root); return out;
}
async function fetchCatalog(provider,url){
  const ctl=new AbortController(); const t=setTimeout(()=>ctl.abort(),TIMEOUT_MS);
  try{
    const r=await fetch(url,{signal:ctl.signal,headers:{'cache-control':'no-cache','user-agent':'GalaxyViewer-LinkAudit/2'}});
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    const data=await r.json();
    return {entries:extractEntries(data,provider),error:null};
  }catch(e){return {entries:[],error:`${provider}: ${e.name==='AbortError'?'catalog timeout':e.message}`};}
  finally{clearTimeout(t);}
}
async function probeOnce(entry,run){
  let last={status:null,error:'not attempted'};
  for(let attempt=0;attempt<=RETRIES;attempt++){
    const ctl=new AbortController(); const timer=setTimeout(()=>ctl.abort(),TIMEOUT_MS); const started=performance.now();
    try{
      const r=await fetch(entry.url,{signal:ctl.signal,redirect:'follow',headers:{'cache-control':'no-cache','pragma':'no-cache','range':`bytes=0-${MAX_BYTES-1}`,'user-agent':'GalaxyViewer-LinkAudit/2'}});
      const ttfb=Math.round(performance.now()-started);
      let bytes=0;
      if(r.body){const reader=r.body.getReader(); while(bytes<MAX_BYTES){const {done,value}=await reader.read(); if(done)break; bytes+=value?.byteLength||0;} try{await reader.cancel();}catch{}}
      const elapsed=Math.round(performance.now()-started);
      const ct=r.headers.get('content-type')||'';
      const ok=r.ok || r.status===206;
      last={...entry,run,attempt:attempt+1,status:r.status,ok,elapsedMs:elapsed,ttfbMs:ttfb,bytesSampled:bytes,contentType:ct,finalUrl:r.url,error:'',stale:r.status===404||r.status===410,notImage:!!ct&&!/^image\//i.test(ct)};
      if(ok) return last;
    }catch(e){
      last={...entry,run,attempt:attempt+1,status:null,ok:false,elapsedMs:Math.round(performance.now()-started),ttfbMs:null,bytesSampled:0,contentType:'',finalUrl:'',error:e.name==='AbortError'?`timeout>${TIMEOUT_MS}ms`:e.message,stale:false,notImage:false};
    } finally {clearTimeout(timer);}
    if(attempt<RETRIES) await sleep(400*(attempt+1));
  }
  return last;
}
async function mapLimit(items,limit,fn){
  const result=new Array(items.length); let next=0;
  async function worker(){while(true){const i=next++; if(i>=items.length)return; try{result[i]=await fn(items[i],i);}catch(e){result[i]={...items[i],ok:false,error:`worker:${e.message}`};}}}
  await Promise.all(Array.from({length:Math.min(limit,items.length||1)},worker)); return result;
}
function summarize(entries,runs){
  const by=new Map(); for(const r of runs){if(!by.has(r.url))by.set(r.url,[]);by.get(r.url).push(r);}
  return entries.map(e=>{
    const rr=by.get(e.url)||[]; const med=median(rr.map(x=>x.elapsedMs)); const ttfb=median(rr.map(x=>x.ttfbMs));
    const statuses=[...new Set(rr.map(x=>x.status).filter(x=>x!==null))].join(',');
    const stale=rr.some(x=>x.stale); const failed=rr.length<RUNS||rr.some(x=>!x.ok); const notImage=rr.some(x=>x.notImage);
    let classification='FAST';
    if(stale) classification='STALE'; else if(failed) classification='FAILED/FLAKY'; else if(notImage) classification='NOT IMAGE';
    else if(med>=15000) classification='VERY SLOW'; else if(med>=10000) classification='SLOW'; else if(med>=5000) classification='MODERATE';
    return {...e,classification,statuses,runs:rr.length,medianMs:med,p95Ms:p95(rr.map(x=>x.elapsedMs)),medianTtfbMs:ttfb,maxBytesSampled:Math.max(0,...rr.map(x=>x.bytesSampled||0)),contentTypes:[...new Set(rr.map(x=>x.contentType).filter(Boolean))].join(' | '),errors:[...new Set(rr.map(x=>x.error).filter(Boolean))].join(' | ')};
  }).sort((a,b)=>{
    const rank={'STALE':6,'FAILED/FLAKY':5,'NOT IMAGE':4,'VERY SLOW':3,'SLOW':2,'MODERATE':1,'FAST':0};
    return (rank[b.classification]-rank[a.classification]) || ((b.medianMs??-1)-(a.medianMs??-1));
  });
}
function counts(summary){
  const c={unique:summary.length,HUBBLE:0,JWST:0,CHANDRA:0,stale:0,failed:0,notImage:0,moderate:0,slow:0,verySlow:0,fast:0};
  for(const r of summary){c[r.provider]=(c[r.provider]||0)+1; if(r.classification==='STALE')c.stale++; else if(r.classification==='FAILED/FLAKY')c.failed++; else if(r.classification==='NOT IMAGE')c.notImage++; else if(r.classification==='VERY SLOW')c.verySlow++; else if(r.classification==='SLOW')c.slow++; else if(r.classification==='MODERATE')c.moderate++; else c.fast++;}
  return c;
}
function markdown(summary,c,catalogErrors){
  const l=['# Galaxy Viewer Image Download Link Health Report','',`Generated: ${new Date().toISOString()}`,'',`Actual image/download URLs tested. Runs per URL: ${RUNS}; retries per failed run: ${RETRIES}; timeout: ${TIMEOUT_MS/1000}s; concurrency: ${CONCURRENCY}.`,'',`- Unique image URLs: ${c.unique}`,`- Hubble: ${c.HUBBLE}`,`- JWST: ${c.JWST}`,`- Chandra: ${c.CHANDRA}`,`- Stale (404/410): ${c.stale}`,`- Failed/flaky: ${c.failed}`,`- Not image content: ${c.notImage}`,`- Moderate (>=5s): ${c.moderate}`,`- Slow (>=10s): ${c.slow}`,`- Very slow (>=15s): ${c.verySlow}`,`- Fast: ${c.fast}`,''];
  if(catalogErrors.length) l.push('## Catalog errors','',...catalogErrors.map(x=>`- ${x}`),'');
  l.push('## Problem links','', '| Class | Provider | Archive ID | Name | Field | HTTP | Median | P95 | TTFB | URL |','|---|---|---|---|---|---:|---:|---:|---:|---|');
  const problems=summary.filter(r=>r.classification!=='FAST');
  for(const r of problems) l.push(`| ${r.classification} | ${r.provider} | ${r.archiveId||''} | ${(r.name||'').replaceAll('|','\\|')} | ${r.field} | ${r.statuses||'—'} | ${fmtMs(r.medianMs)} | ${fmtMs(r.p95Ms)} | ${fmtMs(r.medianTtfbMs)} | ${r.url} |`);
  if(!problems.length) l.push('| FAST | ALL | — | No problem links detected | — | — | — | — | — | — |');
  l.push('','## Method','', '- Uses Node built-in fetch only; no browser or Playwright dependency.',`- Downloads only the first ${MAX_BYTES} bytes of each image URL using HTTP Range where supported, enough to verify reachability and measure response speed without pulling every full-resolution asset.`, '- Every URL is isolated with its own timeout and retries; one bad server cannot abort the whole scan.', '- Reports are written even when individual links or an individual catalog fail.');
  return l.join('\n');
}
function csv(summary){
  const cols=['classification','provider','archiveId','name','field','statuses','runs','medianMs','p95Ms','medianTtfbMs','maxBytesSampled','contentTypes','url','sourceUrl','errors'];
  return [cols.join(','),...summary.map(r=>cols.map(k=>escCsv(r[k])).join(','))].join('\n');
}
function html(summary,c,catalogErrors){
  const rows=summary.map(r=>`<tr><td>${escHtml(r.classification)}</td><td>${escHtml(r.provider)}</td><td>${escHtml(r.archiveId)}</td><td>${escHtml(r.name)}</td><td>${escHtml(r.field)}</td><td>${escHtml(r.statuses||'—')}</td><td>${escHtml(fmtMs(r.medianMs))}</td><td>${escHtml(fmtMs(r.p95Ms))}</td><td><a href="${escHtml(r.url)}">OPEN</a></td><td>${escHtml(r.errors)}</td></tr>`).join('');
  return `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Galaxy Viewer Link Health</title><style>body{font-family:system-ui;background:#08111f;color:#eef7ff;margin:18px}table{border-collapse:collapse;width:100%;font-size:12px}td,th{border-bottom:1px solid #29435d;padding:6px;text-align:left}a{color:#75c8ff}.cards{display:flex;flex-wrap:wrap;gap:8px}.card{padding:10px 14px;background:#10263d;border-radius:8px}.card b{display:block;font-size:22px}</style><h1>Galaxy Viewer Image Download Link Health</h1><p>Generated ${new Date().toISOString()}</p><div class="cards"><div class="card">URLs<b>${c.unique}</b></div><div class="card">Stale<b>${c.stale}</b></div><div class="card">Failed/flaky<b>${c.failed}</b></div><div class="card">Slow+Very slow<b>${c.slow+c.verySlow}</b></div><div class="card">Hubble<b>${c.HUBBLE}</b></div><div class="card">JWST<b>${c.JWST}</b></div><div class="card">Chandra<b>${c.CHANDRA}</b></div></div>${catalogErrors.length?`<h2>Catalog errors</h2><pre>${escHtml(catalogErrors.join('\n'))}</pre>`:''}<h2>All links</h2><table><thead><tr><th>Class</th><th>Provider</th><th>ID</th><th>Name</th><th>Field</th><th>HTTP</th><th>Median</th><th>P95</th><th>Link</th><th>Error</th></tr></thead><tbody>${rows}</tbody></table>`;
}

const catalogErrors=[]; let entries=[];
for(const [provider,url] of CATALOGS){
  const r=await fetchCatalog(provider,url); if(r.error) catalogErrors.push(r.error); entries.push(...r.entries); console.log(`${provider}: ${r.entries.length} image URLs${r.error?` (${r.error})`:''}`);
}
const dedup=new Map(); for(const e of entries) if(!dedup.has(e.url)) dedup.set(e.url,e); entries=[...dedup.values()];
console.log(`Testing ${entries.length} unique actual image URLs; ${RUNS} run(s) each.`);
const work=[]; for(const e of entries) for(let run=1;run<=RUNS;run++) work.push({...e,run});
let completed=0;
const raw=await mapLimit(work,CONCURRENCY,async w=>{const r=await probeOnce(w,w.run); completed++; if(completed%50===0||completed===work.length) console.log(`Progress ${completed}/${work.length}`); return r;});
const summary=summarize(entries,raw); const c=counts(summary);
await fs.writeFile(OUT_MD,markdown(summary,c,catalogErrors));
await fs.writeFile(OUT_CSV,csv(summary));
await fs.writeFile(OUT_HTML,html(summary,c,catalogErrors));
await fs.writeFile(OUT_JSON,JSON.stringify({generatedAt:new Date().toISOString(),settings:{RUNS,CONCURRENCY,TIMEOUT_MS,RETRIES,MAX_BYTES},catalogErrors,counts:c,results:summary},null,2));
console.log(JSON.stringify(c,null,2));
if(process.env.GITHUB_STEP_SUMMARY){await fs.appendFile(process.env.GITHUB_STEP_SUMMARY,markdown(summary,c,catalogErrors).split('\n## Problem links')[0]+'\n');}
if(entries.length===0){console.error('FATAL: zero image URLs discovered. Reports were still written.'); process.exitCode=2;}
