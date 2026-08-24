/* Galaxy Viewer Random Galaxy extension 0044. Extends 0043. */
(() => {
  'use strict';
  const VERSION='0044',DISPLAY_VERSION='12I';
  const base=window.GalaxyRandomGalaxy;
  if(!base||base.VERSION!=='0043')throw new Error('RANDOM GALAXY 0044 REQUIRES 0043');
  const previous=window.GalaxyRandomGalaxy0043;
  let assistTimer=0,assistStarted=0;

  const originalGetState=base.prototype.getState;
  if(typeof originalGetState==='function'&&!base.prototype.__gv0044StateWrapped){
    Object.defineProperty(base.prototype,'__gv0044StateWrapped',{value:true});
    base.prototype.getState=function(){return {...originalGetState.call(this),version:VERSION}};
  }
  base.VERSION=VERSION;

  function core(){return window.GalaxyViewerCore||base.prefetchRuntime?.core||null}
  function stampVersion(){
    const c=core(),label=c?.versionLabel;
    if(label){label.textContent=`VERSION ${DISPLAY_VERSION}`;label.setAttribute('aria-label',`GALAXY VIEWER VERSION ${DISPLAY_VERSION}`)}
    if(c?.randomGalaxy?.root)c.randomGalaxy.root.dataset.gvrgVersion=VERSION;
  }
  function ready(){try{return Boolean(base.hasReadyNavigation?.())}catch(_){return false}}
  function kick(){
    try{previous?.kickPreparation?.()}catch(_){}
    try{base.reconcileFutureQueue?.()}catch(_){}
    try{core()?.fillPrefetchQueue?.()}catch(_){}
  }
  function stopAssist(){if(assistTimer){clearInterval(assistTimer);assistTimer=0}}
  function assistTick(){
    const c=core(),button=c?.randomGalaxyButton,random=c?.randomGalaxy;
    if(!button||!random)return;
    const busy=Boolean(random.getState?.().busy),suspended=Boolean(c.getBackgroundWorkSuspended?.());
    if(!busy&&!suspended)button.disabled=false;
    kick();
    if(ready()){
      if(!busy&&!suspended)button.disabled=false;
      stopAssist();
      return;
    }
    if(performance.now()-assistStarted>15000){
      if(!busy&&!suspended)button.disabled=false;
      stopAssist();
    }
  }
  function startAssist(){
    stampVersion();kick();
    if(assistTimer)return;
    assistStarted=performance.now();
    assistTimer=setInterval(assistTick,100);
    assistTick();
  }
  document.addEventListener('gv-prefetch-ready',startAssist);
  document.addEventListener('gv-viewer-ready',()=>setTimeout(startAssist,0));
  window.addEventListener('beforeunload',stopAssist,{once:true});
  setTimeout(startAssist,0);
  window.GalaxyRandomGalaxy0044=Object.freeze({VERSION,DISPLAY_VERSION,startAssist,stopAssist,kick,ready,getHealth:()=>Object.freeze({future:Number(base.getPrefetchTelemetry?.()?.rows?.length||0),ready:ready(),assisting:Boolean(assistTimer)})});
})();