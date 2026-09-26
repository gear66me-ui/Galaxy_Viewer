/* Galaxy Viewer opt-in diagnostics 0002. OFF means zero background activity. */
(() => {
  'use strict';
  const VERSION='0002',MAX_ERRORS=100,MAX_SNAPSHOTS=200,POLL_MS=500;
  let enabled=false,timer=0,panel=null,statusEl=null,bodyEl=null,errorsEl=null;
  const errors=[],snapshots=[];
  const nowIso=()=>new Date().toISOString();
  const pad=n=>String(n).padStart(2,'0');
  const stamp=()=>{const d=new Date();return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}_${pad(d.getHours())}-${pad(d.getMinutes())}-${pad(d.getSeconds())}`};
  const boundedPush=(array,value,max)=>{array.push(value);if(array.length>max)array.splice(0,array.length-max)};
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const telemetry=()=>window.GalaxyRandomGalaxy?.getPrefetchTelemetry?.()||null;
  const core=()=>window.GalaxyViewerCore||window.GalaxyRandomGalaxy?.prefetchRuntime?.core||null;
  const paused=()=>Boolean(core()?.getBackgroundWorkSuspended?.()||telemetry()?.suspended);
  function banner(message,kind='info'){
    let el=document.getElementById('gv-download-banner-0002');
    if(!el){el=document.createElement('div');el.id='gv-download-banner-0002';document.body.appendChild(el)}
    el.dataset.kind=kind;el.textContent=String(message||'');el.classList.add('gv-visible');clearTimeout(el.__timer);el.__timer=setTimeout(()=>el.classList.remove('gv-visible'),2600);
  }
  function ensureSharedStyle(){
    if(document.getElementById('gv-diagnostics-0002-style'))return;
    const style=document.createElement('style');style.id='gv-diagnostics-0002-style';style.textContent=`
#gv-diagnostics-0002{position:fixed;right:6px;top:58px;z-index:2147482000;width:min(300px,calc(100vw - 12px));max-height:34vh;overflow:auto;padding:5px;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,rgba(8,27,58,.92),rgba(11,49,119,.88) 52%,rgba(20,132,219,.62));color:#DDF8FF;font:7.3px/1.15 monospace;box-shadow:inset 0 0 7px rgba(221,248,255,.08),0 0 8px rgba(88,191,255,.28);backdrop-filter:blur(2px)}
#gv-diagnostics-0002 *{box-sizing:border-box}#gv-diagnostics-0002 .gvdiag-head{display:flex;align-items:center;justify-content:space-between;gap:4px;margin-bottom:3px;color:#9BE5FF;font-weight:700;font-size:7.5px}#gv-diagnostics-0002 .gvdiag-controls{display:flex;gap:2px;flex-wrap:wrap;justify-content:flex-end}#gv-diagnostics-0002 button{padding:2px 3px;border:1px solid #7CCBFF;border-radius:3px;background:rgba(8,27,58,.92);color:#EAF8FF;font:6.6px/1 monospace}#gv-diagnostics-0002 .gvdiag-status{margin:2px 0 3px;color:#9BE5FF;font-size:6.8px}#gv-diagnostics-0002 table{width:100%;border-collapse:collapse;table-layout:fixed}#gv-diagnostics-0002 td,#gv-diagnostics-0002 th{padding:1.5px 2px;border:1px solid rgba(124,203,255,.24);vertical-align:top;overflow-wrap:anywhere;text-align:left}#gv-diagnostics-0002 td:first-child{width:27%;color:#9BE5FF}#gv-diagnostics-0002 th{color:#9BE5FF;background:rgba(8,27,58,.78)}#gv-diagnostics-0002 .gvdiag-section{margin:4px 0 2px;color:#9BE5FF;font-weight:700;font-size:6.8px}
#gv-download-banner-0002{position:fixed;left:50%;top:12px;z-index:2147483647;transform:translate(-50%,-8px);max-width:calc(100vw - 20px);padding:6px 9px;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,#081B3A,#0B3177 55%,#1484DB);color:#EAF8FF;font:8px/1.25 monospace;text-align:center;white-space:pre-wrap;opacity:0;visibility:hidden;pointer-events:none;transition:.16s ease;box-shadow:0 0 10px rgba(88,191,255,.38)}#gv-download-banner-0002.gv-visible{opacity:1;visibility:visible;transform:translate(-50%,0)}#gv-download-banner-0002[data-kind="error"]{border-color:#FF8A70;color:#FFD5CC}
`;document.head.appendChild(style);
  }
  function summary(){
    const t=telemetry(),c=core(),rows=t?.rows||[],random=c?.randomGalaxy?.getState?.()||{};
    const count=selector=>rows.filter(row=>String(selector(row)||'').toUpperCase()==='READY').length;
    return Object.freeze({at:nowIso(),viewer:String(c?.displayVersion||''),randomVersion:String(window.GalaxyRandomGalaxy?.VERSION||''),telemetryApi:typeof window.GalaxyRandomGalaxy?.getPrefetchTelemetry==='function'?'READY':'MISSING',mode:random.busy?'TRAVELING':random.hdOpen?'HD OPEN':'READY',background:paused()?'SUSPENDED':'RUNNING',future:rows.length,next:String(rows[0]?.bannerText||rows[0]?.name||''),hdReady:count(row=>row.hd?.state),aladinReady:count(row=>row.aladin?.state),webReady:count(row=>row.web?.state),active:String(t?.active?.bannerText||t?.active?.name||''),catalog:Number(c?.eligibleCatalogCount||0)});
  }
  function render(snapshot=snapshots.at(-1)||summary()){
    if(!panel)return;
    statusEl.textContent=enabled?(paused()?'ON — PAUSED DURING TRAVEL':'ON — COLLECTING'):'OFF — NO COLLECTION';
    const rows=[['VIEWER',snapshot.viewer||'—',`RANDOM ${snapshot.randomVersion||'—'}`],['TELEMETRY',snapshot.telemetryApi||'—',`CAT ${snapshot.catalog||0}`],['MODE',snapshot.mode||'—',snapshot.background||'—'],['FUTURE',snapshot.future??0,`NEXT ${snapshot.next||'—'}`],['HD',snapshot.hdReady??0,`/ ${snapshot.future??0}`],['ALADIN',snapshot.aladinReady??0,`/ ${snapshot.future??0}`],['WEB',snapshot.webReady??0,`/ ${snapshot.future??0}`],['ACTIVE',snapshot.active||'—','']];
    bodyEl.innerHTML=rows.map(row=>`<tr><td>${esc(row[0])}</td><td>${esc(row[1])}</td><td>${esc(row[2])}</td></tr>`).join('');
    errorsEl.innerHTML=errors.slice(-10).reverse().map(error=>`<tr><td>${esc(error.at.slice(11,19))}</td><td>${esc(error.type)}</td><td>${esc(error.message)}</td></tr>`).join('')||'<tr><td colspan="3">NO CAPTURED ERRORS</td></tr>';
  }
  function collect(){if(!enabled||paused()){if(panel)render();return}const snap=summary();boundedPush(snapshots,snap,MAX_SNAPSHOTS);render(snap)}
  function capture(type,value){if(!enabled||paused())return;const message=value?.error?.stack||value?.reason?.stack||value?.message||value?.reason||value?.error||value;boundedPush(errors,Object.freeze({at:nowIso(),type,message:String(message||'UNKNOWN ERROR')}),MAX_ERRORS);render()}
  const onError=event=>capture('ERROR',event),onRejection=event=>capture('PROMISE',event);
  function setEnabled(next){next=Boolean(next);if(next===enabled){render();return enabled}enabled=next;if(enabled){window.addEventListener('error',onError);window.addEventListener('unhandledrejection',onRejection);collect();timer=setInterval(collect,POLL_MS)}else{if(timer)clearInterval(timer);timer=0;window.removeEventListener('error',onError);window.removeEventListener('unhandledrejection',onRejection)}render();return enabled}
  function saveJson(filename,payload){
    const json=JSON.stringify(payload,null,2);ensureSharedStyle();
    if(window.GalaxyViewerDownloads?.saveJson){banner(`DOWNLOADING\n${filename}\nTO DOWNLOADS/Galaxy Viewer`);window.GalaxyViewerDownloads.saveJson(filename,json);return true}
    banner(`DOWNLOAD NOT SAVED\nTHIS APK NEEDS DOWNLOAD SUPPORT\n${filename}`,'error');return false;
  }
  function download(){const filename=`Galaxy-Viewer-Diagnostics-${stamp()}.json`;const payload={module:'GalaxyViewerDiagnostics',version:VERSION,exportedAt:nowIso(),enabled,errors:[...errors],snapshots:[...snapshots]};return saveJson(filename,payload)}
  function ensurePanel(){
    ensureSharedStyle();if(panel)return panel;
    panel=document.createElement('section');panel.id='gv-diagnostics-0002';panel.innerHTML=`<div class="gvdiag-head"><span>DIAGNOSTICS 0002</span><div class="gvdiag-controls"><button data-a="on">ON</button><button data-a="off">OFF</button><button data-a="download">DOWNLOAD</button><button data-a="close">X</button></div></div><div class="gvdiag-status"></div><table><tbody class="gvdiag-body"></tbody></table><div class="gvdiag-section">LAST 10 ERRORS</div><table><thead><tr><th>TIME</th><th>TYPE</th><th>MESSAGE</th></tr></thead><tbody class="gvdiag-errors"></tbody></table>`;
    statusEl=panel.querySelector('.gvdiag-status');bodyEl=panel.querySelector('.gvdiag-body');errorsEl=panel.querySelector('.gvdiag-errors');panel.addEventListener('click',event=>{const a=event.target?.dataset?.a;if(a==='on')setEnabled(true);else if(a==='off')setEnabled(false);else if(a==='download')download();else if(a==='close')panel.style.display='none'});document.body.appendChild(panel);render();return panel;
  }
  function open(){ensurePanel().style.display='block';render()}function close(){if(panel)panel.style.display='none'}
  window.addEventListener('gv-native-download-complete',event=>banner(`SAVED\nDownloads/Galaxy Viewer/${event.detail?.filename||''}`));
  window.addEventListener('gv-native-download-failed',event=>banner(`DOWNLOAD FAILED\n${event.detail?.message||''}`,'error'));
  window.GalaxyViewerDiagnostics=Object.freeze({VERSION,open,close,enable:()=>setEnabled(true),disable:()=>setEnabled(false),setEnabled,getState:()=>Object.freeze({enabled,errors:errors.length,snapshots:snapshots.length}),exportData:()=>({errors:[...errors],snapshots:[...snapshots]}),download});
})();