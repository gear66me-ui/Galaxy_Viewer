/* Galaxy Viewer Random Galaxy extension 0043. Extends frozen 0042. */
(() => {
  'use strict';
  const VERSION='0043',DISPLAY_VERSION='12I';
  const base=window.GalaxyRandomGalaxy;
  if(!base||base.VERSION!=='0042')throw new Error('RANDOM GALAXY 0043 REQUIRES 0042');

  if(!document.getElementById('gv-random-galaxy-0043-style')){
    const style=document.createElement('style');
    style.id='gv-random-galaxy-0043-style';
    style.textContent=`
#gv-we-are-here .gv-earth-icon,#gv-earth-return-indicator .gv-earth-return-icon{filter:saturate(.92) brightness(.96) drop-shadow(0 0 1px rgba(120,255,171,.22))!important;text-shadow:none!important}
#gv-we-are-here .gv-earth-icon{opacity:.96!important}
`;
    document.head.appendChild(style);
  }

  const originalGetState=base.prototype.getState;
  if(typeof originalGetState==='function'&&!base.prototype.__gv0043StateWrapped){
    Object.defineProperty(base.prototype,'__gv0043StateWrapped',{value:true});
    base.prototype.getState=function(){return {...originalGetState.call(this),version:VERSION}};
  }
  base.VERSION=VERSION;

  function setViewerVersion(){
    const core=window.GalaxyViewerCore||base.prefetchRuntime?.core;
    const label=core?.versionLabel;
    if(label){label.textContent=`VERSION ${DISPLAY_VERSION}`;label.setAttribute('aria-label',`GALAXY VIEWER VERSION ${DISPLAY_VERSION}`)}
    if(core?.randomGalaxy?.root)core.randomGalaxy.root.dataset.gvrgVersion=VERSION;
  }

  function kickPreparation(){
    const core=window.GalaxyViewerCore||base.prefetchRuntime?.core;
    try{core?.fillPrefetchQueue?.()}catch(error){console.warn('RANDOM 0043 VIEWER PREFETCH KICK WARNING',error)}
    try{base.reconcileFutureQueue?.()}catch(error){console.warn('RANDOM 0043 FUTURE RECONCILE WARNING',error)}
    try{
      const telemetry=base.getPrefetchTelemetry?.();
      const count=Number(telemetry?.rows?.length||0);
      if(core?.randomGalaxyButton&&count>0&&!core.getBackgroundWorkSuspended?.()&&!core.randomGalaxy?.getState?.().busy)
        core.randomGalaxyButton.disabled=!Boolean(base.hasReadyNavigation?.());
      return count;
    }catch(error){console.warn('RANDOM 0043 PREPARATION HEALTH WARNING',error);return 0}
  }

  function installClickFeedback(){
    const core=window.GalaxyViewerCore||base.prefetchRuntime?.core;
    const button=core?.randomGalaxyButton;
    if(!button||button.__gv0043Feedback)return;
    button.__gv0043Feedback=true;
    button.addEventListener('click',()=>{
      if(base.hasReadyNavigation?.())return;
      kickPreparation();
      const existing=document.getElementById('gv-random-preparing-0043');
      if(existing){clearTimeout(existing.__timer);existing.__timer=setTimeout(()=>existing.remove(),1600);return}
      const note=document.createElement('div');note.id='gv-random-preparing-0043';note.textContent='PREPARING RANDOM GALAXY';note.style.cssText='position:fixed;left:50%;bottom:62px;z-index:2147483000;transform:translateX(-50%);padding:5px 8px;border:1px solid #7CCBFF;border-radius:5px;background:rgba(8,27,58,.92);color:#9BE5FF;font:7px monospace;letter-spacing:.4px;pointer-events:none;white-space:nowrap';document.body.appendChild(note);note.__timer=setTimeout(()=>note.remove(),1600);
    },true);
  }

  function finalize(){setViewerVersion();kickPreparation();installClickFeedback()}
  document.addEventListener('gv-prefetch-ready',finalize);
  document.addEventListener('gv-viewer-ready',()=>{
    setTimeout(finalize,0);
    setTimeout(finalize,150);
    setTimeout(finalize,500);
    setTimeout(finalize,1200);
  });
  setTimeout(finalize,0);
  window.GalaxyRandomGalaxy0043=Object.freeze({VERSION,DISPLAY_VERSION,finalize,kickPreparation,getHealth:()=>Object.freeze({telemetry:Boolean(base.getPrefetchTelemetry),future:Number(base.getPrefetchTelemetry?.()?.rows?.length||0),ready:Boolean(base.hasReadyNavigation?.())})});
})();