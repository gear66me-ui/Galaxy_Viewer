/*
AVM 0054 — CACHE-BYPASS LOADER FOR RESTORED AVM 0053
- Avoids the stale GitHub Pages gv-avm-overlay-lab-0053.js edge object.
- Fetches the restored beta 0053 source from raw.githubusercontent.com and evaluates it.
- The evaluated module must still publish GalaxyViewerAvmOverlayLab.VERSION === "0053".
*/
(()=>{
  'use strict';
  const RAW_0053_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/lab/gv-avm-overlay-lab-0053.js?cb=0054-cache-bypass-20260923';
  const trace=(code,detail={})=>{try{globalThis.GalaxyViewerDiagnostics?.recordAvm?.(code,detail)}catch(_){}};
  trace('AVM_0054_RAW0053_FETCH_START',{url:RAW_0053_URL});
  fetch(RAW_0053_URL,{cache:'no-store'})
    .then(response=>{
      if(!response.ok)throw new Error('RAW AVM 0053 HTTP '+response.status);
      return response.text();
    })
    .then(source=>{
      if(!/const VERSION=\"0053\"/.test(source)&&!/const VERSION='0053'/.test(source))
        throw new Error('RAW AVM 0053 VERSION MARKER MISSING');
      trace('AVM_0054_RAW0053_FETCH_OK',{bytes:source.length});
      (0,eval)(source);
      trace('AVM_0054_RAW0053_EVAL_OK',{version:String(globalThis.GalaxyViewerAvmOverlayLab?.VERSION||'')});
    })
    .catch(error=>{
      trace('AVM_0054_RAW0053_LOAD_FAIL',{message:String(error?.message||error||'')});
      console.error('AVM 0054 raw 0053 cache-bypass failed',error);
    });
})();
