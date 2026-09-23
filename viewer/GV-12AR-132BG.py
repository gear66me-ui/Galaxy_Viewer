from IPython.display import HTML, Javascript, display

# 12AR-132BG — extractor-compatible authorized BG wrapper.
# The Android launcher extracts these display(HTML/Javascript) blocks from source text.
# Loads GV-12AR-132BD.py in the browser, then applies only:
#   12AR-132BD -> 12AR-132BG
#   GV-12AR-132BD.py -> GV-12AR-132BG.py
#   gv-avm-overlay-lab-0053.js -> gv-avm-overlay-lab-0055.js


display(HTML("""
<div id="gv-132bg-loader" style="position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;background:#000;color:#9BE5FF;font:12px monospace;letter-spacing:.08em;text-align:center">
  GALAXY VIEWER 12AR-132BG<br/>LOADING BD CORE WITH AVM 0055
</div>
"""))


display(Javascript(r"""
(async()=>{
  'use strict';
  const BD_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/GV-12AR-132BD.py?bg=132BG-avm0055-20260923-extractor-compatible';
  const log=(code,detail={})=>{try{console.info(code,detail)}catch(_){}};
  const fail=error=>{
    const box=document.getElementById('gv-132bg-loader');
    if(box){
      box.style.color='#ff7b7b';
      box.innerHTML='GALAXY VIEWER 12AR-132BG<br/>LOAD FAILED<br/><br/>'+String(error&&error.message||error||'UNKNOWN');
    }
    throw error;
  };
  const extractBlock=(src,kind)=>{
    const token=kind==='html'?'display(HTML("""':'display(Javascript(r"""';
    let start=src.indexOf(token);
    if(start<0&&kind==='js')start=src.indexOf('display(Javascript("""');
    if(start<0)throw new Error('BD '+kind.toUpperCase()+' BLOCK NOT FOUND');
    const bodyStart=src.indexOf('"""',start)+3;
    const end=src.indexOf('"""))',bodyStart);
    if(bodyStart<3||end<0)throw new Error('BD '+kind.toUpperCase()+' BLOCK MALFORMED');
    return src.slice(bodyStart,end);
  };
  try{
    log('GV_132BG_BD_FETCH_START',{url:BD_URL});
    const response=await fetch(BD_URL,{cache:'no-store'});
    if(!response.ok)throw new Error('BD VIEWER HTTP '+response.status);
    const src=await response.text();
    let html=extractBlock(src,'html');
    let js=extractBlock(src,'js');
    html=html
      .replaceAll('12AR-132BD','12AR-132BG')
      .replaceAll('GV-12AR-132BD.py','GV-12AR-132BG.py')
      .replaceAll('gv-avm-overlay-lab-0053.js','gv-avm-overlay-lab-0055.js')
      .replaceAll('AVM0053','AVM0055')
      .replaceAll('AVM 0053','AVM 0055');
    js=js
      .replaceAll('12AR-132BD','12AR-132BG')
      .replaceAll('GV-12AR-132BD.py','GV-12AR-132BG.py')
      .replaceAll('gv-avm-overlay-lab-0053.js','gv-avm-overlay-lab-0055.js')
      .replaceAll('AVM0053','AVM0055')
      .replaceAll('AVM 0053','AVM 0055');
    document.body.insertAdjacentHTML('beforeend',html);
    const loader=document.getElementById('gv-132bg-loader');
    if(loader)loader.remove();
    log('GV_132BG_EVAL_START',{htmlBytes:html.length,jsBytes:js.length});
    (0,eval)(js+'\n//# sourceURL=GV-12AR-132BG-from-BD.js');
    log('GV_132BG_EVAL_OK',{});
  }catch(error){
    log('GV_132BG_FAIL',{message:String(error&&error.message||error||'')});
    fail(error);
  }
})();
"""))
