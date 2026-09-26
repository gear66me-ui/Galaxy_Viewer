/* Galaxy Viewer opt-in ten-slot download analytics 0002. OFF means zero polling. */
(() => {
  'use strict';
  const VERSION='0002',POLL_MS=500,MAX_SNAPSHOTS=200;
  let enabled=false,timer=0,panel=null,statusEl=null,bodyEl=null,crossEl=null,frozenRows=[];
  const snapshots=[];
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const norm=value=>String(value??'').trim().toUpperCase();
  const key=value=>String(value??'').trim().toLowerCase();
  const pad=n=>String(n).padStart(2,'0');
  const stamp=()=>{const d=new Date();return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}_${pad(d.getHours())}-${pad(d.getMinutes())}-${pad(d.getSeconds())}`};
  const core=()=>window.GalaxyViewerCore||window.GalaxyRandomGalaxy?.prefetchRuntime?.core||null;
  const telemetry=()=>window.GalaxyRandomGalaxy?.getPrefetchTelemetry?.()||null;
  const paused=()=>Boolean(core()?.getBackgroundWorkSuspended?.()||telemetry()?.suspended);
  const bottomBannerText=()=>String(document.querySelector('.gvrg-card .gvrg-row:first-child .gvrg-value')?.textContent||'').replace(/\s+/g,' ').trim().toUpperCase();
  function banner(message,kind='info'){
    let el=document.getElementById('gv-download-banner-0002');
    if(!el){el=document.createElement('div');el.id='gv-download-banner-0002';document.body.appendChild(el)}
    el.dataset.kind=kind;el.textContent=String(message||'');el.classList.add('gv-visible');clearTimeout(el.__timer);el.__timer=setTimeout(()=>el.classList.remove('gv-visible'),2600);
  }
  function ensureStyle(){
    if(document.getElementById('gv-download-analytics-0002-style'))return;
    const style=document.createElement('style');style.id='gv-download-analytics-0002-style';style.textContent=`
#gv-download-analytics-0002{position:fixed;left:6px;top:58px;z-index:2147481999;width:calc(100vw - 12px);max-height:36vh;overflow:auto;padding:4px;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,rgba(8,27,58,.94),rgba(11,49,119,.90) 52%,rgba(20,132,219,.60));color:#DDF8FF;font:6.7px/1.12 monospace;box-shadow:inset 0 0 7px rgba(221,248,255,.08),0 0 8px rgba(88,191,255,.28);backdrop-filter:blur(2px)}#gv-download-analytics-0002 *{box-sizing:border-box}#gv-download-analytics-0002 .gvdla-head{display:flex;align-items:center;justify-content:space-between;gap:3px;margin-bottom:2px;color:#9BE5FF;font-weight:700;font-size:7.2px}#gv-download-analytics-0002 .gvdla-controls{display:flex;gap:2px;flex-wrap:wrap;justify-content:flex-end}#gv-download-analytics-0002 button{padding:2px 3px;border:1px solid #7CCBFF;border-radius:3px;background:rgba(8,27,58,.92);color:#EAF8FF;font:6.3px/1 monospace}#gv-download-analytics-0002 .gvdla-status,#gv-download-analytics-0002 .gvdla-cross{margin:2px 0;color:#9BE5FF;font-size:6.4px;white-space:normal}#gv-download-analytics-0002 table{width:100%;border-collapse:collapse;table-layout:auto}#gv-download-analytics-0002 td,#gv-download-analytics-0002 th{padding:1.5px 2px;border:1px solid rgba(124,203,255,.22);vertical-align:top;text-align:left;white-space:nowrap}#gv-download-analytics-0002 th{position:sticky;top:0;background:#081B3A;color:#9BE5FF;font-size:6.2px}#gv-download-analytics-0002 td:nth-child(2){font-weight:700;color:#EAF8FF}#gv-download-analytics-0002 .gvdla-bad td:last-child{color:#FF9B84;font-weight:700}
#gv-download-banner-0002{position:fixed;left:50%;top:12px;z-index:2147483647;transform:translate(-50%,-8px);max-width:calc(100vw - 20px);padding:6px 9px;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,#081B3A,#0B3177 55%,#1484DB);color:#EAF8FF;font:8px/1.25 monospace;text-align:center;white-space:pre-wrap;opacity:0;visibility:hidden;pointer-events:none;transition:.16s ease;box-shadow:0 0 10px rgba(88,191,255,.38)}#gv-download-banner-0002.gv-visible{opacity:1;visibility:visible;transform:translate(-50%,0)}#gv-download-banner-0002[data-kind="error"]{border-color:#FF8A70;color:#FFD5CC}
`;document.head.appendChild(style);
  }
  function readRows(){
    const t=telemetry(),c=core(),rows=(t?.rows||[]).slice(0,10);
    return rows.map((row,index)=>{
      const resource=c?.getHdPreparedResource?.(row.key)||null;
      const resourceKey=key(resource?.key),expectedKey=key(row.key);
      const expectedBanner=String(row.bannerText??row.designation??'').trim().toUpperCase();
      const hdBanner=String(row.hdBannerText??window.GalaxyRandomGalaxy?.bannerIdentity?.(resource?.destination)??'').trim().toUpperCase();
      const expectedProvider=norm(row.provider),hdProvider=norm(resource?.destination?.provider),errors=[];
      if(resource&&resourceKey!==expectedKey)errors.push(`KEY ${resourceKey||'MISSING'} != ${expectedKey}`);
      if(resource&&hdBanner!==expectedBanner)errors.push(`BANNER ${hdBanner||'MISSING'} != ${expectedBanner||'MISSING'}`);
      if(resource&&expectedProvider&&hdProvider&&hdProvider!==expectedProvider)errors.push(`PROVIDER ${hdProvider} != ${expectedProvider}`);
      if(String(row.hd?.state||'').toUpperCase()==='READY'&&!resource)errors.push('READY RESOURCE MISSING');
      return Object.freeze({slot:Number(row.slot||index+1),target:expectedBanner||String(row.name||'').toUpperCase(),provider:expectedProvider,hd:String(row.hd?.state||'QUEUED').toUpperCase(),aladin:String(row.aladin?.state||'QUEUED').toUpperCase(),web:String(row.web?.state||'QUEUED').toUpperCase(),source:String(resource?.sourceKind||row.hd?.detail||'').toUpperCase(),identity:errors.length?`IDENTITY ERROR: ${errors.join('; ')}`:(resource?'MATCH':'WAITING'),key:expectedKey,hdKey:resourceKey,hdTarget:hdBanner});
    });
  }
  function render(rows=frozenRows){
    if(!panel)return;
    const isPaused=paused();
    statusEl.textContent=enabled?(isPaused?'ON — FROZEN DURING TRAVEL':'ON — LIVE 10-SLOT ROSTER'):'OFF — NO POLLING';
    const active=telemetry()?.active;
    crossEl.textContent=`#1 ${rows[0]?.target||'—'}   ACTIVE ${String(active?.bannerText||active?.name||'—').toUpperCase()}   BANNER ${bottomBannerText()||'—'}`;
    bodyEl.innerHTML=rows.map(row=>`<tr class="${row.identity.startsWith('IDENTITY ERROR')?'gvdla-bad':''}"><td>${esc(row.slot)}</td><td>${esc(row.target)}</td><td>${esc(row.provider)}</td><td>${esc(row.hd)}</td><td>${esc(row.aladin)}</td><td>${esc(row.web)}</td><td>${esc(row.source)}</td><td>${esc(row.identity)}</td></tr>`).join('')||'<tr><td colspan="8">WAITING FOR FUTURE ROSTER</td></tr>';
  }
  function collect(){if(!enabled)return;if(paused()){render(frozenRows);return}frozenRows=readRows();snapshots.push(Object.freeze({at:new Date().toISOString(),rows:frozenRows}));if(snapshots.length>MAX_SNAPSHOTS)snapshots.splice(0,snapshots.length-MAX_SNAPSHOTS);render(frozenRows)}
  function setEnabled(next){next=Boolean(next);if(next===enabled){render();return enabled}enabled=next;if(enabled){frozenRows=readRows();collect();timer=setInterval(collect,POLL_MS)}else{if(timer)clearInterval(timer);timer=0}render();return enabled}
  function saveJson(filename,payload){
    const json=JSON.stringify(payload,null,2);ensureStyle();
    if(window.GalaxyViewerDownloads?.saveJson){banner(`DOWNLOADING ANALYTICS\n${filename}\nTO DOWNLOADS/Galaxy Viewer`);window.GalaxyViewerDownloads.saveJson(filename,json);return true}
    banner(`ANALYTICS NOT SAVED\nTHIS APK NEEDS DOWNLOAD SUPPORT\n${filename}`,'error');return false;
  }
  function download(){const filename=`Galaxy-Viewer-Analytics-${stamp()}.json`;const payload={module:'GalaxyViewerDownloadAnalytics',version:VERSION,exportedAt:new Date().toISOString(),enabled,currentRows:[...frozenRows],bottomBanner:bottomBannerText(),snapshots:[...snapshots]};return saveJson(filename,payload)}
  function ensurePanel(){
    ensureStyle();if(panel)return panel;
    panel=document.createElement('section');panel.id='gv-download-analytics-0002';panel.innerHTML=`<div class="gvdla-head"><span>DOWNLOAD ANALYTICS 0002</span><div class="gvdla-controls"><button data-a="on">ON</button><button data-a="off">OFF</button><button data-a="download">DOWNLOAD</button><button data-a="close">X</button></div></div><div class="gvdla-status"></div><div class="gvdla-cross"></div><table><thead><tr><th>#</th><th>TARGET/BANNER</th><th>PROV</th><th>HD</th><th>ALADIN</th><th>WEB</th><th>SRC</th><th>IDENTITY</th></tr></thead><tbody class="gvdla-body"></tbody></table>`;
    statusEl=panel.querySelector('.gvdla-status');crossEl=panel.querySelector('.gvdla-cross');bodyEl=panel.querySelector('.gvdla-body');panel.addEventListener('click',event=>{const a=event.target?.dataset?.a;if(a==='on')setEnabled(true);else if(a==='off')setEnabled(false);else if(a==='download')download();else if(a==='close')panel.style.display='none'});document.body.appendChild(panel);frozenRows=readRows();render();return panel;
  }
  function open(){ensurePanel().style.display='block';if(!enabled)frozenRows=readRows();render()}function close(){if(panel)panel.style.display='none'}
  window.addEventListener('gv-native-download-complete',event=>banner(`SAVED\nDownloads/Galaxy Viewer/${event.detail?.filename||''}`));
  window.addEventListener('gv-native-download-failed',event=>banner(`DOWNLOAD FAILED\n${event.detail?.message||''}`,'error'));
  window.GalaxyViewerDownloadAnalytics=Object.freeze({VERSION,open,close,enable:()=>setEnabled(true),disable:()=>setEnabled(false),setEnabled,getRows:()=>Object.freeze([...readRows()]),getState:()=>Object.freeze({enabled,rows:frozenRows.length,snapshots:snapshots.length}),download});
})();