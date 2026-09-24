from IPython.display import HTML, Javascript, display

# 12AR-132BF cache-bypass wrapper.
# Loads GV-12AR-132BD.py, injects its HTML, then runs its Javascript with only:
#   VERSION/DISPLAY_VERSION 12AR-132BD -> 12AR-132BF
#   AVM_LAB_URL gv-avm-overlay-lab-0053.js -> gv-avm-overlay-lab-0054.js

display(HTML("""
<div id="gv-132bf-loader" style="position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;background:#000;color:#9BE5FF;font:12px monospace;letter-spacing:.08em;text-align:center">
  GALAXY VIEWER 12AR-132BF<br/>LOADING BD CORE WITH AVM 0054 CACHE BYPASS
</div>
"""))

display(Javascript(r"""
(async()=>{
  'use strict';
  const BD_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/GV-12AR-132BD.py?bf=132BF-AVM0054-20260923';
  const log=(code,detail={})=>{try{console.info(code,detail)}catch(_){}};
  const fail=error=>{
    const box=document.getElementById('gv-132bf-loader');
    if(box){
      box.style.color='#ff7070';
      box.innerHTML='GALAXY VIEWER 12AR-132BF FAILED<br/><pre style="white-space:pre-wrap;max-width:92vw;text-align:left">'+String(error?.stack||error||'')+'</pre>';
    }
    throw error;
  };

  function extractTriple(source,kind){
    const marker=kind==='html'?'display(HTML("""':'display(Javascript(r"""';
    const start=source.indexOf(marker);
    if(start<0)throw new Error('132BF wrapper could not find '+kind+' block');
    const bodyStart=start+marker.length;
    const end=source.indexOf('\n"""))',bodyStart);
    if(end<0)throw new Error('132BF wrapper could not close '+kind+' block');
    return source.slice(bodyStart,end);
  }

  try{
    log('GV_132BF_WRAPPER_FETCH_START',{url:BD_URL});
    const response=await fetch(BD_URL,{cache:'no-store'});
    if(!response.ok)throw new Error('BD CORE FETCH HTTP '+response.status);
    const source=await response.text();

    let html=extractTriple(source,'html');
    let js=extractTriple(source,'js');

    html=html.replaceAll('12AR-132BD','12AR-132BF');
    js=js
      .replaceAll("const VERSION='12AR-132BD';","const VERSION='12AR-132BF';")
      .replaceAll("const DISPLAY_VERSION='12AR-132BD';","const DISPLAY_VERSION='12AR-132BF';")
      .replaceAll('gv-avm-overlay-lab-0053.js','gv-avm-overlay-lab-0054.js')
      .replaceAll('VIEWER_AVM0053_','VIEWER_AVM0054_')
      .replaceAll('gvAvmOverlayLab0053','gvAvmOverlayLab0054')
      .replaceAll('GV AVM LAB LOAD FAILURE','GV AVM LAB 0054 LOAD FAILURE');

    const loader=document.getElementById('gv-132bf-loader');
    const host=document.createElement('div');
    host.innerHTML=html;
    while(host.firstChild)document.body.appendChild(host.firstChild);
    try{loader?.remove?.()}catch(_){}

    log('GV_132BF_WRAPPER_EVAL_START',{bdBytes:source.length,jsBytes:js.length});
    (0,eval)(js);
    log('GV_132BF_WRAPPER_EVAL_DISPATCHED',{});
  }catch(error){
    fail(error);
  }
})();
"""))
