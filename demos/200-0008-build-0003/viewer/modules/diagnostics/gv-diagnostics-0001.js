/* Galaxy Viewer opt-in diagnostics 0001. OFF means zero background activity. */
(() => {
  'use strict';
  const VERSION='0001',MAX_ERRORS=100,MAX_SNAPSHOTS=200,POLL_MS=500;
  let enabled=false,timer=0,panel=null,statusEl=null,bodyEl=null,errorsEl=null;
  const errors=[],snapshots=[];
  const nowIso=()=>new Date().toISOString();
  const boundedPush=(array,value,max)=>{array.push(value);if(array.length>max)array.splice(0,array.length-max)};
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const telemetry=()=>window.GalaxyRandomGalaxy?.getPrefetchTelemetry?.()||null;
  const core=()=>window.GalaxyViewerCore||window.GalaxyRandomGalaxy?.prefetchRuntime?.core||null;
  const paused=()=>Boolean(core()?.getBackgroundWorkSuspended?.()||telemetry()?.suspended);
  function summary(){
    const t=telemetry(),c=core(),rows=t?.rows||[],random=c?.randomGalaxy?.getState?.()||{};
    const count=selector=>rows.filter(row=>String(selector(row)||'').toUpperCase()==='READY').length;
    return Object.freeze({at:nowIso(),viewer:String(c?.displayVersion||''),randomVersion:String(window.GalaxyRandomGalaxy?.VERSION||''),mode:random.busy?'TRAVELING':random.hdOpen?'HD OPEN':'READY',background:paused()?'SUSPENDED':'RUNNING',future:rows.length,next:String(rows[0]?.bannerText||rows[0]?.name||''),hdReady:count(row=>row.hd?.state),aladinReady:count(row=>row.aladin?.state),webReady:count(row=>row.web?.state),active:String(t?.active?.bannerText||t?.active?.name||'')});
  }
  function render(snapshot=snapshots.at(-1)||summary()){
    if(!panel)return;
    statusEl.textContent=enabled?(paused()?'ON — PAUSED DURING RANDOM GALAXY TRAVEL':'ON — COLLECTING'):'OFF — NO COLLECTION';
    const rows=[['VIEWER',snapshot.viewer||'—',`RANDOM ${snapshot.randomVersion||'—'}`],['MODE',snapshot.mode||'—',snapshot.background||'—'],['FUTURE',snapshot.future??0,`NEXT ${snapshot.next||'—'}`],['HD READY',snapshot.hdReady??0,`OF ${snapshot.future??0}`],['ALADIN READY',snapshot.aladinReady??0,`OF ${snapshot.future??0}`],['WEB READY',snapshot.webReady??0,`OF ${snapshot.future??0}`],['ACTIVE',snapshot.active||'—','']];
    bodyEl.innerHTML=rows.map(row=>`<tr><td>${esc(row[0])}</td><td>${esc(row[1])}</td><td>${esc(row[2])}</td></tr>`).join('');
    errorsEl.innerHTML=errors.slice(-10).reverse().map(error=>`<tr><td>${esc(error.at.slice(11,19))}</td><td>${esc(error.type)}</td><td>${esc(error.message)}</td></tr>`).join('')||'<tr><td colspan="3">NO CAPTURED ERRORS</td></tr>';
  }
  function collect(){if(!enabled||paused()){if(panel)render();return}const snap=summary();boundedPush(snapshots,snap,MAX_SNAPSHOTS);render(snap)}
  function capture(type,value){if(!enabled||paused())return;const message=value?.error?.stack||value?.reason?.stack||value?.message||value?.reason||value?.error||value;boundedPush(errors,Object.freeze({at:nowIso(),type,message:String(message||'UNKNOWN ERROR')}),MAX_ERRORS);render()}
  const onError=event=>capture('ERROR',event),onRejection=event=>capture('PROMISE',event);
  function setEnabled(next){next=Boolean(next);if(next===enabled){render();return enabled}enabled=next;if(enabled){window.addEventListener('error',onError);window.addEventListener('unhandledrejection',onRejection);collect();timer=setInterval(collect,POLL_MS)}else{if(timer)clearInterval(timer);timer=0;window.removeEventListener('error',onError);window.removeEventListener('unhandledrejection',onRejection)}render();return enabled}
  function download(){const payload={module:'GalaxyViewerDiagnostics',version:VERSION,exportedAt:nowIso(),enabled,errors:[...errors],snapshots:[...snapshots]};const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`galaxy-viewer-diagnostics-${Date.now()}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}
  function ensurePanel(){
    if(panel)return panel;
    const style=document.createElement('style');style.id='gv-diagnostics-0001-style';style.textContent=`#gv-diagnostics-0001{position:fixed;right:8px;top:54px;z-index:2147482000;width:min(430px,calc(100vw - 16px));max-height:58vh;overflow:auto;padding:8px;border:1px solid rgba(255,216,77,.85);border-radius:6px;background:rgba(0,0,0,.38);backdrop-filter:blur(2px);color:#FFD84D;font:11px/1.25 monospace;box-shadow:0 0 10px rgba(255,216,77,.18)}#gv-diagnostics-0001 *{box-sizing:border-box}#gv-diagnostics-0001 .gvdiag-head{display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:6px;font-weight:700}#gv-diagnostics-0001 .gvdiag-controls{display:flex;gap:4px;flex-wrap:wrap}#gv-diagnostics-0001 button{padding:4px 6px;border:1px solid #FFD84D;border-radius:4px;background:rgba(0,0,0,.28);color:#FFD84D;font:10px monospace}#gv-diagnostics-0001 .gvdiag-status{margin:4px 0 6px;color:#FFE98A}#gv-diagnostics-0001 table{width:100%;border-collapse:collapse;table-layout:fixed}#gv-diagnostics-0001 td,#gv-diagnostics-0001 th{padding:3px 4px;border:1px solid rgba(255,216,77,.26);vertical-align:top;overflow-wrap:anywhere;text-align:left}#gv-diagnostics-0001 th{color:#FFF1A8}#gv-diagnostics-0001 .gvdiag-section{margin:8px 0 3px;font-weight:700;color:#FFF1A8}`;document.head.appendChild(style);
    panel=document.createElement('section');panel.id='gv-diagnostics-0001';panel.innerHTML=`<div class="gvdiag-head"><span>DIAGNOSTICS 0001</span><div class="gvdiag-controls"><button data-a="on">TURN ON</button><button data-a="off">TURN OFF</button><button data-a="download">DOWNLOAD</button><button data-a="close">CLOSE</button></div></div><div class="gvdiag-status"></div><table><tbody class="gvdiag-body"></tbody></table><div class="gvdiag-section">LAST 10 ERRORS</div><table><thead><tr><th>TIME</th><th>TYPE</th><th>MESSAGE</th></tr></thead><tbody class="gvdiag-errors"></tbody></table>`;
    statusEl=panel.querySelector('.gvdiag-status');bodyEl=panel.querySelector('.gvdiag-body');errorsEl=panel.querySelector('.gvdiag-errors');panel.addEventListener('click',event=>{const a=event.target?.dataset?.a;if(a==='on')setEnabled(true);else if(a==='off')setEnabled(false);else if(a==='download')download();else if(a==='close')panel.style.display='none'});document.body.appendChild(panel);render();return panel;
  }
  function open(){ensurePanel().style.display='block';render()}function close(){if(panel)panel.style.display='none'}
  window.GalaxyViewerDiagnostics=Object.freeze({VERSION,open,close,enable:()=>setEnabled(true),disable:()=>setEnabled(false),setEnabled,getState:()=>Object.freeze({enabled,errors:errors.length,snapshots:snapshots.length}),exportData:()=>({errors:[...errors],snapshots:[...snapshots]}),download});
})();
