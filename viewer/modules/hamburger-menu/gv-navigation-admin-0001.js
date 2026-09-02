/* Galaxy Viewer Navigation Admin 0001 — ECO-20260902-12AR01-NAVIGATION-ADMIN-001C */
(function(global){
  'use strict';
  const VERSION='0001';
  let planner=null;
  let overlay=null;
  let status=null;

  function bind(nextPlanner){
    planner=nextPlanner||null;
    return Boolean(planner);
  }

  function ensureUi(){
    if(overlay)return overlay;
    const style=document.createElement('style');
    style.textContent=`
      .gv-nav-admin-0001{position:fixed;inset:0;z-index:2147483600;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.74);font-family:system-ui,sans-serif}
      .gv-nav-admin-0001.gv-open{display:flex}.gv-nav-admin-panel{width:min(92vw,430px);background:#080b10;color:#eaf8ff;border:1px solid #58bfff;border-radius:12px;padding:16px;box-shadow:0 0 28px rgba(88,191,255,.25)}
      .gv-nav-admin-title{font-weight:800;letter-spacing:.08em;margin-bottom:12px}.gv-nav-admin-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}.gv-nav-admin-grid button,.gv-nav-admin-actions button{background:#111923;color:#dff6ff;border:1px solid #58bfff;border-radius:8px;padding:10px 4px;font-weight:800}.gv-nav-admin-grid button.gv-active{background:#123a54;color:#fff}.gv-nav-admin-actions{display:flex;gap:8px;margin-top:12px}.gv-nav-admin-actions button{flex:1}.gv-nav-admin-status{margin-top:12px;white-space:pre-wrap;font:700 11px/1.4 monospace;color:#aee9ff}.gv-nav-admin-note{margin-top:10px;font-size:11px;line-height:1.35;color:#b8c9d4}`;
    document.head.appendChild(style);

    overlay=document.createElement('div');
    overlay.className='gv-nav-admin-0001';
    overlay.innerHTML=`<div class="gv-nav-admin-panel" role="dialog" aria-modal="true" aria-label="Travel Settings">
      <div class="gv-nav-admin-title">TRAVEL SETTINGS</div>
      <div class="gv-nav-admin-grid"></div>
      <div class="gv-nav-admin-actions"><button data-action="download">DOWNLOAD DATA</button><button data-action="close">CLOSE</button></div>
      <div class="gv-nav-admin-status"></div>
      <div class="gv-nav-admin-note">Engineering control only. Selecting a duration changes total navigation time T only. Route constraints and normalized S7 motion geometry remain fixed.</div>
    </div>`;
    document.body.appendChild(overlay);
    status=overlay.querySelector('.gv-nav-admin-status');
    const grid=overlay.querySelector('.gv-nav-admin-grid');
    for(const seconds of [17,15,12,9,6]){
      const button=document.createElement('button');
      button.textContent=`${seconds}s`;
      button.dataset.seconds=String(seconds);
      button.addEventListener('click',()=>{
        if(!planner)return renderStatus('NAVIGATION MODULE NOT BOUND');
        planner.setTravelSeconds(seconds);
        renderStatus();renderButtons();
      });
      grid.appendChild(button);
    }
    overlay.querySelector('[data-action="close"]').addEventListener('click',close);
    overlay.querySelector('[data-action="download"]').addEventListener('click',downloadData);
    return overlay;
  }

  function renderButtons(){
    if(!overlay)return;
    const selected=Number(planner?.getState?.().selectedTravelSeconds||17);
    for(const button of overlay.querySelectorAll('[data-seconds]'))
      button.classList.toggle('gv-active',Number(button.dataset.seconds)===selected);
  }

  function renderStatus(message=''){
    if(!status)return;
    if(message){status.textContent=message;return}
    const state=planner?.getState?.()||{};
    status.textContent=
      `NORMAL TRAVEL: ${Number(state.selectedTravelSeconds||0).toFixed(1)} s\n`+
      `FIRST TRAVEL:  ${Number(state.firstTravelSeconds||0).toFixed(1)} s\n`+
      `ROUTE REMAINING: ${Number(state.remaining||0)}\n`+
      `NEXT BATCH: ${state.nextBatchReady?'READY':state.nextBatchPlanning?'PLANNING':'IDLE'}`;
  }

  function open(){
    ensureUi();renderButtons();renderStatus();overlay.classList.add('gv-open');
  }

  function close(){overlay?.classList.remove('gv-open')}

  function downloadData(){
    if(!planner)return renderStatus('NAVIGATION MODULE NOT BOUND');
    const payload={
      schema:'GV-NAVIGATION-ADMIN-SNAPSHOT-0001',
      generatedAt:new Date().toISOString(),
      navigationVersion:global.GalaxyViewerNavigation?.VERSION||'',
      state:planner.getState?.()||null,
      routePlannerTelemetry:[...(planner.telemetry||[])]
    };
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url;a.download=`gv-navigation-${payload.state?.selectedTravelSeconds||'x'}s-${Date.now()}.json`;
    document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }

  global.GalaxyViewerNavigationAdmin=Object.freeze({VERSION,bind,open,close});
})(window);
