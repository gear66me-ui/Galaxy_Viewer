/* Galaxy Viewer Random Galaxy extension 0045. Extends 0044. */
(() => {
  'use strict';
  const VERSION='0045',DISPLAY_VERSION='12I';
  const base=window.GalaxyRandomGalaxy;
  if(!base||base.VERSION!=='0044')throw new Error('RANDOM GALAXY 0045 REQUIRES 0044');
  const prior=window.GalaxyRandomGalaxy0044;
  prior?.stopAssist?.();
  let observer=null;

  const originalGetState=base.prototype.getState;
  if(typeof originalGetState==='function'&&!base.prototype.__gv0045StateWrapped){
    Object.defineProperty(base.prototype,'__gv0045StateWrapped',{value:true});
    base.prototype.getState=function(){return {...originalGetState.call(this),version:VERSION}};
  }
  base.VERSION=VERSION;

  const core=()=>window.GalaxyViewerCore||base.prefetchRuntime?.core||null;
  const isBusy=()=>Boolean(core()?.randomGalaxy?.getState?.().busy||core()?.getBackgroundWorkSuspended?.());
  function stampVersion(){
    const c=core(),label=c?.versionLabel;
    if(label){label.textContent=`VERSION ${DISPLAY_VERSION}`;label.setAttribute('aria-label',`GALAXY VIEWER VERSION ${DISPLAY_VERSION}`)}
    if(c?.randomGalaxy?.root)c.randomGalaxy.root.dataset.gvrgVersion=VERSION;
  }
  function kick(){
    try{prior?.kick?.()}catch(_){}
    try{window.GalaxyRandomGalaxy0043?.kickPreparation?.()}catch(_){}
    try{base.reconcileFutureQueue?.()}catch(_){}
    try{core()?.fillPrefetchQueue?.()}catch(_){}
  }
  function keepButtonUsable(){
    const button=core()?.randomGalaxyButton;
    if(!button)return false;
    if(!isBusy()&&button.disabled)button.disabled=false;
    if(observer)return true;
    observer=new MutationObserver(()=>{
      if(!isBusy()&&button.disabled)button.disabled=false;
    });
    observer.observe(button,{attributes:true,attributeFilter:['disabled']});
    button.addEventListener('pointerdown',()=>{if(!isBusy()){button.disabled=false;kick()}},true);
    return true;
  }
  function finalize(){stampVersion();kick();keepButtonUsable()}
  document.addEventListener('gv-prefetch-ready',finalize);
  document.addEventListener('gv-viewer-ready',()=>{setTimeout(finalize,0);setTimeout(finalize,200);setTimeout(finalize,700)});
  window.addEventListener('beforeunload',()=>observer?.disconnect(),{once:true});
  setTimeout(finalize,0);
  window.GalaxyRandomGalaxy0045=Object.freeze({VERSION,DISPLAY_VERSION,finalize,kick,keepButtonUsable,getHealth:()=>Object.freeze({future:Number(base.getPrefetchTelemetry?.()?.rows?.length||0),ready:Boolean(base.hasReadyNavigation?.()),buttonDisabled:Boolean(core()?.randomGalaxyButton?.disabled)})});
})();