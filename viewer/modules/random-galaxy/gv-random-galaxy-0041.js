/* Galaxy Viewer Random Galaxy extension 0041. Extends frozen 0040. */
(() => {
  'use strict';
  const VERSION='0041', DISPLAY_VERSION='12G';
  const base=window.GalaxyRandomGalaxy;
  if(!base||base.VERSION!=='0040')throw new Error('RANDOM GALAXY 0041 REQUIRES FROZEN 0040');
  const clean=value=>String(value==null?'':value).replace(/\s+/g,' ').trim();
  const keyOf=item=>String(item?.key||item?.destination?.archiveId||item?.destination?.name||item?.archiveId||item?.name||'').trim().toLowerCase();
  const bannerIdentity=destination=>clean(destination?.designation).toUpperCase();
  const originalGetState=base.prototype.getState;
  if(typeof originalGetState==='function'&&!base.prototype.__gv0041StateWrapped){
    Object.defineProperty(base.prototype,'__gv0041StateWrapped',{value:true});
    base.prototype.getState=function(){return {...originalGetState.call(this),version:VERSION}};
  }
  base.VERSION=VERSION;
  base.bannerIdentity=bannerIdentity;
  let telemetryWrapped=false;
  function setViewerVersion(){
    const core=window.GalaxyViewerCore||base.prefetchRuntime?.core;
    const label=core?.versionLabel;
    if(label){label.textContent=`VERSION ${DISPLAY_VERSION}`;label.setAttribute('aria-label',`GALAXY VIEWER VERSION ${DISPLAY_VERSION}`)}
    const randomGalaxy=core?.randomGalaxy;
    if(randomGalaxy?.root)randomGalaxy.root.dataset.gvrgVersion=VERSION;
  }
  function wrapTelemetry(){
    if(telemetryWrapped||typeof base.getPrefetchTelemetry!=='function')return false;
    const originalTelemetry=base.getPrefetchTelemetry;
    base.getPrefetchTelemetry=function(){
      const telemetry=originalTelemetry.call(base)||{};
      const core=window.GalaxyViewerCore||base.prefetchRuntime?.core;
      const future=core?.randomNavigationWindow?.getFuture?.()||[];
      const byKey=new Map(future.map(record=>[keyOf(record),record]));
      const rows=(telemetry.rows||[]).map((row,index)=>{
        const record=byKey.get(String(row?.key||'').trim().toLowerCase())||null;
        const destination=record?.destination||null;
        const resource=core?.getHdPreparedResource?.(row?.key)||null;
        return Object.freeze({...row,slot:index+1,bannerText:bannerIdentity(destination),hdBannerText:bannerIdentity(resource?.destination),designation:clean(destination?.designation).toUpperCase()});
      });
      const activeDestination=telemetry.active?.key?(core?.randomNavigationWindow?.getState?.()?.pending?.destination||core?.randomGalaxy?.getState?.()?.activeDestination||null):null;
      const active=telemetry.active?Object.freeze({...telemetry.active,bannerText:bannerIdentity(activeDestination)}):null;
      return Object.freeze({...telemetry,version:VERSION,active,rows:Object.freeze(rows)});
    };
    telemetryWrapped=true;
    return true;
  }
  function finalize(){wrapTelemetry();setViewerVersion()}
  document.addEventListener('gv-prefetch-ready',finalize);
  document.addEventListener('gv-viewer-ready',()=>setTimeout(finalize,0));
  setTimeout(finalize,0);
  window.GalaxyRandomGalaxy0041=Object.freeze({VERSION,DISPLAY_VERSION,bannerIdentity,finalize});
})();
