/*
AVM 0053 ROLLBACK SHIM — CRPIX / VIGNETTE RESCALE INVESTIGATION
BASELINE REQUEST: use the known-good 130H AVM behavior without touching Random Galaxy.

This shim intentionally replaces the AVM 0053 implementation with the AVM 0038
runtime module. It removes the later 0048+ filtered-raster / scaledWcsForBlend
path where CRPIX1/CRPIX2 were rewritten after downscaling/vignette processing.

No Random Galaxy, Navigation, catalog, or Aladin source files are changed here.
*/
(()=>{
  'use strict';

  const SHIM_VERSION='0053-ROLLBACK-TO-0038';
  const SOURCE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/lab/gv-avm-overlay-lab-0038.js?v=0053-rollback-to-0038-20260922';

  let readyPromise=null;
  let realApi=null;

  function trace(code,detail={}){
    try{globalThis.GalaxyViewerDiagnostics?.recordAvm?.(code,detail)}catch(_){}
  }

  function load0038(){
    if(realApi)return Promise.resolve(realApi);
    if(readyPromise)return readyPromise;

    trace('AVM_0053_ROLLBACK_SHIM_LOAD_START',{sourceUrl:SOURCE_URL});

    readyPromise=new Promise((resolve,reject)=>{
      const script=document.createElement('script');
      script.src=SOURCE_URL;
      script.async=true;
      script.dataset.gvAvm0053RollbackShim='1';

      script.addEventListener('load',()=>{
        const api=globalThis.GalaxyViewerAvmOverlayLab;
        if(!api||api.VERSION===SHIM_VERSION){
          reject(new Error('AVM 0038 ROLLBACK API DID NOT INSTALL'));
          return;
        }
        realApi=api;
        trace('AVM_0053_ROLLBACK_SHIM_LOAD_OK',{
          shimVersion:SHIM_VERSION,
          realVersion:String(api.VERSION||'')
        });
        resolve(api);
      },{once:true});

      script.addEventListener('error',()=>{
        const error=new Error('AVM 0038 ROLLBACK SCRIPT LOAD FAILED');
        trace('AVM_0053_ROLLBACK_SHIM_LOAD_FAIL',{message:error.message,sourceUrl:SOURCE_URL});
        reject(error);
      },{once:true});

      document.head.appendChild(script);
    });

    return readyPromise;
  }

  async function call(method,args){
    const api=await load0038();
    const fn=api&&api[method];
    if(typeof fn!=='function')
      throw new Error('AVM 0038 METHOD MISSING: '+method);
    return fn.apply(api,args);
  }

  const proxy={
    VERSION:SHIM_VERSION,
    install(...args){return call('install',args)},
    uninstall(...args){return realApi?.uninstall?.(...args)},
    prepareForTravel(...args){return call('prepareForTravel',args)},
    stageForTravel(...args){
      return realApi?.stageForTravel
        ? realApi.stageForTravel(...args)
        : call('prepareForTravel',args);
    },
    isPreparedForTravel(...args){return realApi?.isPreparedForTravel?.(...args)??false},
    hideForCruise(...args){return realApi?.hideForCruise?.(...args)??false},
    showPendingForZoomIn(...args){return realApi?.showPendingForZoomIn?.(...args)??false},
    commitPreparedArrival(...args){return realApi?.commitPreparedArrival?.(...args)??false},
    loadForBestDestination(...args){return realApi?.loadForBestDestination?.(...args)??false},
    get lastContext(){return realApi?.lastContext??null}
  };

  globalThis.GalaxyViewerAvmOverlayLab=proxy;
  load0038().catch(error=>{
    console.error('AVM 0053 rollback shim failed',error);
  });
})();
