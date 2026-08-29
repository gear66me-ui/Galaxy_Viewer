/*
GALAXY VIEWER — RANDOM NAVIGATION 0064
AUTHORIZED BASELINE: Random Galaxy 0063.
AUTHORIZED CHANGE: diagnostic restoration of the direct Random navigation handoff only.
0063 remains the owner of catalog selection, ten-slot prefetch, HD resources, archive/source integration,
history storage, presentation, and the existing travelToRandom() zoom-out / translate / zoom-in choreography.
0064 intercepts only the physical RANDOM GALAXY click, hands the already-ready future[0] destination
directly to travelToRandom(), and performs 0063 queue/history bookkeeping only after visible travel succeeds.
*/
(function(global){
  'use strict';

  const VERSION='0064';
  const BASE_VERSION='0063';
  const INSTALL_POLL_MS=25;
  const INSTALL_TIMEOUT_MS=30000;

  let installed=false;
  let directPending=false;
  let installedAt=0;

  const keyOf=value=>String(
    value?.key ||
    value?.destination?.archiveId ||
    value?.destination?.name ||
    value?.archiveId ||
    value?.name ||
    ''
  ).trim().toLowerCase();

  function syncHistoryControls(core,nav,randomGalaxy){
    const busy=Boolean(directPending||randomGalaxy?.getState?.().busy);
    if(core?.historyBackButton)
      core.historyBackButton.disabled=busy||!nav?.canBack?.();
    if(core?.historyForwardButton)
      core.historyForwardButton.disabled=busy||!nav?.canForward?.();
  }

  function patchRuntimeIdentity(G,core){
    G.VERSION=VERSION;

    const runtime=G.prefetchRuntime;
    if(runtime&&runtime.version!==VERSION){
      G.prefetchRuntime=Object.freeze({
        ...runtime,
        version:VERSION,
        displayVersion:VERSION
      });
    }

    if(typeof G.getPrefetchTelemetry==='function'&&!G.__gv0064TelemetryBase){
      const base=G.getPrefetchTelemetry.bind(G);
      G.__gv0064TelemetryBase=base;
      G.getPrefetchTelemetry=()=>{
        const value=base();
        if(!value||typeof value!=='object')return value;
        return Object.freeze({...value,version:VERSION});
      };
    }

    if(!G.__gv0064PendingBase){
      const basePending=typeof G.isNavigationPending==='function'
        ? G.isNavigationPending.bind(G)
        : ()=>false;
      G.__gv0064PendingBase=basePending;
      G.isNavigationPending=()=>Boolean(directPending||basePending());
    }

    G.prefetchRuntime=Object.freeze({
      ...(G.prefetchRuntime||{}),
      version:VERSION,
      displayVersion:VERSION,
      core,
      randomGalaxy:core.randomGalaxy
    });
  }

  async function directRandomNavigation(core){
    const G=global.GalaxyRandomGalaxy;
    const randomGalaxy=core?.randomGalaxy;
    const nav=core?.randomNavigationWindow;

    if(!G||!randomGalaxy||!nav)return null;
    if(directPending||randomGalaxy?.getState?.().busy)return null;

    const expectedHead=nav.peekNext?.()||nav.getState?.().next||null;
    if(!expectedHead)return null;

    const expectedKey=keyOf(expectedHead);
    const sourceDestination=expectedHead?.destination||expectedHead;

    if(!expectedKey||!sourceDestination)
      throw new Error('RANDOM 0064 FUTURE0 DESTINATION MISSING');

    directPending=true;
    syncHistoryControls(core,nav,randomGalaxy);

    let bookkeepingStarted=false;

    try{
      /*
       * The queue supplies a destination; it does not gate travel.
       * Reuse the already-prepared HD destination when available, but do not
       * lock, claim, wait for a receipt, suspend work, or create a pending
       * transaction before the visible Aladin movement starts.
       */
      const destination=
        core.activateQueuedDestination?.(
          sourceDestination,
          randomGalaxy?.currentGalaxy?.name||''
        ) || sourceDestination;

      if(!destination||keyOf(destination)!==expectedKey)
        throw new Error('RANDOM 0064 DIRECT DESTINATION HANDOFF MISMATCH');

      randomGalaxy.prefetchedDestination=destination;
      randomGalaxy.prefetchPromise=null;

      const arrived=await randomGalaxy.travelToRandom();

      if(!arrived||keyOf(arrived)!==expectedKey)
        throw new Error('RANDOM 0064 DIRECT TRAVEL ARRIVAL MISMATCH');

      /*
       * Visible travel succeeded. Now let 0063 perform its existing FIFO
       * consume/active-record bookkeeping. Passing an empty exclusion is
       * intentional because currentGalaxy is already the arrived destination.
       */
      bookkeepingStarted=true;
      const consumed=await randomGalaxy.provider?.({excludeName:''});

      if(!consumed||keyOf(consumed)!==expectedKey)
        throw new Error('RANDOM 0064 POST-ARRIVAL FIFO BOOKKEEPING MISMATCH');

      const pending=nav.getState?.().pending;
      if(pending?.kind!=='random')
        throw new Error('RANDOM 0064 POST-ARRIVAL PENDING STATE MISSING');

      nav.commitPending(arrived);

      core.resumeBackgroundWork?.();
      core.resumeArchivePreloads?.();
      G.reconcileFutureQueue?.();
      core.fillPrefetchQueue?.();
      syncHistoryControls(core,nav,randomGalaxy);

      return arrived;
    }catch(error){
      const state=nav.getState?.()||{};
      if(state.locked)nav.rollbackLocked?.();
      if(state.pending)nav.rollbackPending?.();

      if(bookkeepingStarted){
        core.resumeBackgroundWork?.();
        core.resumeArchivePreloads?.();
      }

      syncHistoryControls(core,nav,randomGalaxy);
      throw error;
    }finally{
      directPending=false;
      randomGalaxy.prefetchPromise=null;
      syncHistoryControls(core,nav,randomGalaxy);
    }
  }

  function install(){
    if(installed)return true;

    const G=global.GalaxyRandomGalaxy;
    const core=global.GalaxyViewerCore;

    if(!G||!core?.randomGalaxy||!core?.randomNavigationWindow||!core?.randomGalaxyButton)
      return false;

    /* Wait until 0063 has completed its normal integration and future queue setup. */
    if(!G.prefetchRuntime?.core)return false;

    if(G.prefetchRuntime.core!==core)
      throw new Error('RANDOM 0064 BASE RUNTIME / VIEWER CORE MISMATCH');

    if(G.VERSION!==BASE_VERSION&&G.VERSION!==VERSION)
      throw new Error(`RANDOM 0064 REQUIRES BASE ${BASE_VERSION}; FOUND ${G.VERSION}`);

    const button=core.randomGalaxyButton;
    const nav=core.randomNavigationWindow;
    const randomGalaxy=core.randomGalaxy;

    patchRuntimeIdentity(G,core);

    const clickHandler=event=>{
      const target=event.target;
      if(!target||!(target===button||button.contains(target)))return;

      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();

      if(button.disabled)return;

      directRandomNavigation(core).catch(error=>
        console.error('GALAXY VIEWER RANDOM NAVIGATION 0064 FAILURE',error)
      );
    };

    /* Window capture runs before 0063's target-capture transaction handler. */
    global.addEventListener('click',clickHandler,true);
    global.addEventListener('beforeunload',()=>{
      try{global.removeEventListener('click',clickHandler,true)}catch(_){}
    },{once:true});

    G.requestRandomNavigation=()=>directRandomNavigation(core);

    global.GalaxyRandomNavigation0064=Object.freeze({
      VERSION,
      BASE_VERSION,
      directRandomNavigation:()=>directRandomNavigation(core),
      getState:()=>Object.freeze({
        version:VERSION,
        baseVersion:BASE_VERSION,
        installed,
        directPending,
        installedAt
      })
    });

    installed=true;
    installedAt=Date.now();
    syncHistoryControls(core,nav,randomGalaxy);

    document.dispatchEvent(new CustomEvent(
      'gv-random-navigation-0064-ready',
      {detail:{version:VERSION,baseVersion:BASE_VERSION}}
    ));

    return true;
  }

  const started=performance.now();
  const timer=setInterval(()=>{
    try{
      if(install()){
        clearInterval(timer);
        return;
      }
      if(performance.now()-started>=INSTALL_TIMEOUT_MS){
        clearInterval(timer);
        console.error('GALAXY VIEWER RANDOM NAVIGATION 0064 INSTALL TIMEOUT');
      }
    }catch(error){
      clearInterval(timer);
      console.error('GALAXY VIEWER RANDOM NAVIGATION 0064 INSTALL FAILURE',error);
    }
  },INSTALL_POLL_MS);

  try{install()}catch(error){
    clearInterval(timer);
    console.error('GALAXY VIEWER RANDOM NAVIGATION 0064 INSTALL FAILURE',error);
  }
})(window);
