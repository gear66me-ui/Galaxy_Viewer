/*
AVM 0050 — CANVAS-SAFE FILTER SOURCE PREFERENCE
BASELINE: AVM 0049
- Keeps vignette filtering mandatory; raw/unfiltered substitution remains forbidden.
- Prefers githubImageUrl as the filter raster when available, while provider AVM/WCS stays authoritative.
- Falls back to the prepared provider image only when no mirror is available.
- Random navigation does not wait on this hidden preparation.
*/
/*
AVM 0049 — VIGNETTE FILTER HARD REQUIREMENT
BASELINE: AVM 0048
- Removes both silent raw-image fallbacks.
- If vignette preparation fails, the AVM layer fails/retries instead of showing an unfiltered image.
- Keeps 0048 cooperative bounded-row processing and exact vignette math.
*/
/*
AVM 0047 — COOPERATIVE VIGNETTE PREPARATION
- Preserves 0046's full resolution and exact vignette math.
- Processes image pixels in bounded row strips and yields between strips.
- Prevents FUTURE[0] preparation from monopolizing Android WebView's UI thread.
*/
/*
AVM 0051 — VIGNETTE FAILURE BACKOFF + UI YIELD
BASELINE: AVM 0050
- Prevents pretravel and arrival vignette failures from entering 80/250 ms retry storms.
- Records one failure state per destination and backs off automatic restaging for 30 seconds.
- Removes immediate 250 ms filtered-image retry timers; the normal watcher may retry only after backoff.
- Restores explicit event-loop yields around canvas draw/mask/PNG encode work so Android WebView remains touch-responsive.
- Keeps vignette filtering mandatory; no raw/unfiltered image fallback is introduced.
*/
(()=>{
'use strict';
/* AVM 0043 — FUTURE[0] may stage its prepared blob/WCS layer before click; prepareForTravel reuses that ready layer. */
const VERSION="0051";const trace=(code,detail={})=>{try{globalThis.GalaxyViewerDiagnostics?.recordAvm?.(code,detail)}catch(_){}};trace("AVM_LAB_BOOT",{version:VERSION});
const WATCH_MS=260;
const ARRIVAL_SETTLE_MS=650;
const MAX_BLEND_DIMENSION=2048;
const VIGNETTE_FAILURE_BACKOFF_MS=30000;
const LAYER_NAMES=["Galaxy Viewer AVM Overlay A","Galaxy Viewer AVM Overlay B"];
let activeLayerName=LAYER_NAMES[0],pendingLayerName=LAYER_NAMES[1];
const PANEL_ID="gv-avm-overlay-lab";
const STYLE_ID="gv-avm-overlay-lab-style-0035";
const DEFAULT_SLIDER="0";
let ARef=null,aladinRef=null,randomRef=null,rootRef=null,overlay=null,watchTimer=null,arrivalTimer=0,panelRecoveryTimer=0,lastKey="",loadingKey="",scheduledKey="",lastContext=null,navigationSeen=false;
let pendingOverlay=null,pendingKey="",pendingReady=false,pendingContext=null,pendingPreparePromise=null;
const vignetteFailureState=new Map();
const GLOBAL_BLEND=Object.freeze({
  hdOpacity:1.00,
  crossblend:1.00,
  diameter:1.04,
  blend:0.24,
  decay:1.75,
  core:0.72,
  feather:0.58,
  curve:1.20,
  dissolve:0.38,
  dark:0.72,
  block:1,
  hardMode:false
});
const layerBlendUrls=new Map();
function releaseBlendUrl(url){if(!url)return;try{URL.revokeObjectURL(url)}catch(_){}}
function releaseLayerBlend(layerName){const url=layerBlendUrls.get(layerName)||'';if(url)releaseBlendUrl(url);layerBlendUrls.delete(layerName)}
function bindLayerBlend(layerName,url){releaseLayerBlend(layerName);if(url)layerBlendUrls.set(layerName,url)}
function globalBlendHash(x,y){let n=(x*374761393+y*668265263)>>>0;n=(n^(n>>>13))*1274126177>>>0;n^=n>>>16;return(n>>>0)/4294967295}
function yieldGlobalBlendWork(){
  return new Promise(resolve=>{
    if(
      typeof requestAnimationFrame==='function' &&
      document.visibilityState!=='hidden'
    )requestAnimationFrame(()=>resolve());
    else setTimeout(resolve,0);
  });
}
function markVignetteFailure(key,error,phase){
  const k=String(key||'');
  if(!k)return null;

  const previous=vignetteFailureState.get(k)||{};
  const next={
    count:Number(previous.count||0)+1,
    until:Date.now()+VIGNETTE_FAILURE_BACKOFF_MS,
    message:String(error?.message||error||''),
    phase:String(phase||''),
    suppressionTraced:false
  };

  vignetteFailureState.set(k,next);

  trace('AVM_0051_VIGNETTE_BACKOFF_ARMED',{
    key:k,
    count:next.count,
    delayMs:VIGNETTE_FAILURE_BACKOFF_MS,
    phase:next.phase,
    message:next.message
  });

  return next;
}
function clearVignetteFailure(key,phase){
  const k=String(key||'');
  if(!k||!vignetteFailureState.has(k))return false;

  vignetteFailureState.delete(k);
  trace('AVM_0051_VIGNETTE_BACKOFF_CLEARED',{
    key:k,
    phase:String(phase||'')
  });
  return true;
}
function vignetteBackoffActive(key,phase){
  const k=String(key||'');
  const state=vignetteFailureState.get(k);

  if(!state)return false;

  if(Date.now()>=Number(state.until||0)){
    vignetteFailureState.delete(k);
    trace('AVM_0051_VIGNETTE_BACKOFF_EXPIRED',{
      key:k,
      phase:String(phase||'')
    });
    return false;
  }

  if(!state.suppressionTraced){
    state.suppressionTraced=true;
    trace('AVM_0051_VIGNETTE_RETRY_SUPPRESSED',{
      key:k,
      remainingMs:Math.max(0,Number(state.until||0)-Date.now()),
      phase:String(phase||''),
      count:Number(state.count||0),
      message:String(state.message||'')
    });
  }

  return true;
}
async function makeGlobalBlendSource(
  sourceUrl,
  key,
  preparedImage=null,
  formatHint=''
){
  const raw=String(sourceUrl||'').trim();
  if(!raw)throw new Error('GLOBAL BLEND SOURCE URL MISSING');

  let bmp=null,canvas=null,source=null,sourceKind='prepared-image';
  const started=performance.now();

  try{
    const preparedReady=Boolean(
      preparedImage instanceof HTMLImageElement &&
      preparedImage.complete &&
      Number(preparedImage.naturalWidth)>0 &&
      Number(preparedImage.naturalHeight)>0
    );

    if(preparedReady){
      source=preparedImage;
    }else{
      sourceKind='blob-decode';
      try{
        const response=await fetch(raw,{cache:'force-cache'});
        if(!response.ok)
          throw new Error('GLOBAL BLEND IMAGE FETCH '+response.status);
        const blob=await response.blob();
        if(typeof createImageBitmap!=='function')
          throw new Error('createImageBitmap unavailable');
        bmp=await createImageBitmap(blob);
        source=bmp;
      }catch(fetchError){
        trace('AVM_0049_BLEND_FETCH_REQUIRED_FAILURE',{
          key,
          sourceUrl:raw,
          message:String(fetchError?.message||fetchError||'')
        });
        throw fetchError;
      }
    }

    const w=Number(
      source?.naturalWidth ??
      source?.videoWidth ??
      source?.width
    )||0;
    const h=Number(
      source?.naturalHeight ??
      source?.videoHeight ??
      source?.height
    )||0;

    if(w<1||h<1)
      throw new Error('GLOBAL BLEND IMAGE DIMENSIONS INVALID');

    const scale=Math.min(
      1,
      MAX_BLEND_DIMENSION/Math.max(w,h)
    );
    const outW=Math.max(1,Math.round(w*scale));
    const outH=Math.max(1,Math.round(h*scale));

    canvas=document.createElement('canvas');
    canvas.width=outW;
    canvas.height=outH;

    const ctx=canvas.getContext('2d');
    if(!ctx)throw new Error('GLOBAL BLEND 2D CONTEXT UNAVAILABLE');

    await yieldGlobalBlendWork();
    ctx.drawImage(source,0,0,outW,outH);
    await yieldGlobalBlendWork();

    const p=GLOBAL_BLEND;
    const cx=outW/2,cy=outH/2;
    const rx=outW*.5*p.diameter;
    const ry=outH*.5*p.diameter;
    const core=Math.max(0,Math.min(.98,Number(p.core)||0));
    const opacity=Math.max(
      0,
      Math.min(1,Number(p.hdOpacity||1)*Number(p.crossblend||1))
    );

    ctx.save();
    ctx.globalCompositeOperation='destination-in';
    ctx.translate(cx,cy);
    ctx.scale(rx,ry);

    const mask=ctx.createRadialGradient(0,0,0,0,0,1);
    const mid1=core+(1-core)*.42;
    const mid2=core+(1-core)*.72;
    const mid3=core+(1-core)*.90;
    mask.addColorStop(0,`rgba(0,0,0,${opacity})`);
    mask.addColorStop(core,`rgba(0,0,0,${opacity})`);
    mask.addColorStop(mid1,`rgba(0,0,0,${opacity*.90})`);
    mask.addColorStop(mid2,`rgba(0,0,0,${opacity*.52})`);
    mask.addColorStop(mid3,`rgba(0,0,0,${opacity*.16})`);
    mask.addColorStop(1,'rgba(0,0,0,0)');

    ctx.fillStyle=mask;
    ctx.beginPath();
    ctx.arc(0,0,1,0,Math.PI*2);
    ctx.fill();
    ctx.restore();

    await yieldGlobalBlendWork();

    const png=await new Promise((resolve,reject)=>{
      try{
        canvas.toBlob(
          value=>value
            ? resolve(value)
            : reject(new Error('GLOBAL BLEND PNG ENCODE FAILED')),
          'image/png'
        );
      }catch(error){
        reject(error);
      }
    });

    await yieldGlobalBlendWork();

    const objectUrl=URL.createObjectURL(png);

    trace('AVM_GLOBAL_BLEND_READY',{
      key,
      width:w,height:h,
      outputWidth:outW,outputHeight:outH,
      sourceKind,
      pipeline:'native-gradient-0048',
      elapsedMs:Math.round(performance.now()-started),
      settings:GLOBAL_BLEND
    });

    return {
      url:objectUrl,
      imgFormat:'png',
      filtered:true,
      objectUrl,
      sourceKind,
      sourceWidth:w,sourceHeight:h,
      outputWidth:outW,outputHeight:outH
    };
  }catch(error){
    trace('AVM_0049_VIGNETTE_REQUIRED_FAILURE',{
      key,
      sourceUrl:raw,
      sourceKind,
      message:String(error?.message||error||'')
    });
    throw error;
  }finally{
    try{bmp?.close?.()}catch(_){}
    if(canvas){
      try{canvas.width=1;canvas.height=1}catch(_){}
    }
  }
}
function clamp(n,min,max){n=Number(n);if(!Number.isFinite(n))n=min;return Math.max(min,Math.min(max,n))}
function panel(){return document.getElementById(PANEL_ID)}
function hdOpen(){return document.body?.classList?.contains('gv-hd-open')||document.documentElement?.classList?.contains('gv-hd-open')}
function stateOf(){try{return randomRef?.getState?.()||{}}catch(_){return {}}}
function isArrivedStable(){const st=stateOf(),open=hdOpen(),result=!open&&navigationSeen===true&&st.arrived===true&&st.busy!==true;trace("AVM_ARRIVAL_STATE",{arrived:st.arrived,busy:st.busy,hdOpen:open,navigationSeen,result});if(!result)trace("AVM_ARRIVAL_GATE_FALSE",{arrived:st.arrived,busy:st.busy,hdOpen:open,navigationSeen});return result}
function randomInTransit(){const st=stateOf();return Boolean(st.busy||st.arrived===false)}
function slider(){return panel()?.querySelector('input[type="range"]')||null}
function rail(){return panel()?.querySelector('.gv-avm-rail')||null}
function thumb(){return panel()?.querySelector('.gv-avm-thumb')||null}
function opacityNow(){const sl=slider();const raw=sl?sl.value:DEFAULT_SLIDER;const v=clamp(raw,0,100);return clamp(Math.max(0.01,1-(v/100)),0,1)}
function activeOverlay(){return overlay||lastContext?.overlay||null}
function applyOpacity(){trace("AVM_APPLY_OPACITY_ENTER",{});const op=opacityNow();const target=activeOverlay();try{if(target&&typeof target.setOpacity==="function")target.setOpacity(op)}catch(_){}try{if(target&&typeof target.setAlpha==="function")target.setAlpha(op)}catch(_){}try{if(target?.options)target.options.opacity=op}catch(_){}updateThumb();return op}
function setPanelVisible(on){trace("AVM_PANEL_VISIBILITY_REQUEST",{on});const p=panel();if(!p)return;if(hdOpen()||randomInTransit())on=false;p.dataset.on=on?'1':'0';p.style.display=on?'block':'none';if(on)updateThumb()}
function cancelPanelRecovery(){
  if(panelRecoveryTimer){
    clearTimeout(panelRecoveryTimer);
    panelRecoveryTimer=0;
  }
}
function schedulePanelRecovery(key){
  cancelPanelRecovery();
  let attempts=0;

  const tick=()=>{
    panelRecoveryTimer=0;
    if(!key||key!==lastKey)return;

    if(activeOverlay()&&!hdOpen()&&!randomInTransit()){
      ensurePanel();
      applyOpacity();
      setPanelVisible(true);
      trace('AVM_0046_PANEL_RECOVERED',{key,attempts});
      return;
    }

    attempts++;
    if(attempts<24)
      panelRecoveryTimer=setTimeout(tick,125);
  };

  panelRecoveryTimer=setTimeout(tick,0);
}
function ensureStyle(){if(document.getElementById(STYLE_ID))return;const st=document.createElement('style');st.id=STYLE_ID;st.textContent=`
#${PANEL_ID}{position:fixed;left:-4px;top:calc(50% - 79px);width:57px;height:158px;z-index:7312;display:none;pointer-events:none;font-family:"Space Age",sans-serif;color:#9eefff;filter:drop-shadow(0 0 10px rgba(76,205,255,.82))}
#${PANEL_ID}[data-on="1"]{display:block}
body.gv-hd-open #${PANEL_ID},html.gv-hd-open #${PANEL_ID}{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
#${PANEL_ID} .gv-avm-touch-shield{position:absolute;left:0;top:0;width:57px;height:158px;border-radius:18px;background:rgba(0,22,54,.12);pointer-events:auto;touch-action:none;overscroll-behavior:contain}
#${PANEL_ID} .gv-avm-title{position:absolute;left:11px;top:50%;transform:translateY(-50%);height:108px;display:flex;align-items:center;justify-content:center;writing-mode:vertical-rl;text-orientation:mixed;font:400 6px/1 "Space Age",sans-serif;letter-spacing:1.5px;color:#6feaff;text-shadow:0 0 4px rgba(190,250,255,.96),0 0 10px rgba(35,190,255,.9);user-select:none;pointer-events:none;white-space:nowrap}
#${PANEL_ID} .gv-avm-rail{position:absolute;left:27px;top:14px;width:10px;height:131px;border-radius:999px;background:linear-gradient(180deg,rgba(18,187,255,.95),rgba(4,18,58,.82));box-shadow:0 0 8px rgba(100,226,255,.88),0 0 18px rgba(18,157,255,.72);pointer-events:none}
#${PANEL_ID} .gv-avm-thumb{position:absolute;left:32px;top:145px;width:18px;height:18px;border-radius:50%;transform:translate(-50%,-50%);background:#72e8ff;border:2px solid rgba(224,255,255,.98);box-shadow:0 0 12px rgba(185,250,255,.98),0 0 28px rgba(20,176,255,.82);pointer-events:none}
#${PANEL_ID} input[type="range"]{position:absolute;left:9px;top:14px;width:39px;height:131px;opacity:.001;appearance:none;-webkit-appearance:none;pointer-events:auto;touch-action:none}
@media(max-height:740px){#${PANEL_ID}{top:calc(50% - 69px);height:138px}#${PANEL_ID} .gv-avm-touch-shield{height:138px}#${PANEL_ID} .gv-avm-rail{height:113px}#${PANEL_ID} .gv-avm-thumb{top:126px}#${PANEL_ID} input[type="range"]{height:113px}}
`;document.head.appendChild(st)}
function valueFromY(y){const r=rail()?.getBoundingClientRect?.()||panel()?.getBoundingClientRect?.();if(!r||!r.height)return Number(slider()?.value||DEFAULT_SLIDER);return clamp(Math.round(((r.bottom-y)/r.height)*100),0,100)}
function setSliderValue(v){const sl=slider();if(!sl)return;sl.value=String(clamp(v,0,100));applyOpacity()}
function resetSliderOpaque(){const sl=slider();if(!sl)return Number(DEFAULT_SLIDER);sl.value=DEFAULT_SLIDER;updateThumb();return opacityNow()}
function updateThumb(){const sl=slider(),r=rail(),t=thumb();if(!sl||!r||!t)return;const v=clamp(sl.value,0,100);const top=r.offsetTop+((100-v)/100)*r.offsetHeight;t.style.top=`${top}px`}
function handlePanelPoint(e){if(!panel()?.dataset?.on||panel().dataset.on!=='1')return;if(e.cancelable)e.preventDefault();e.stopPropagation();const touch=e.touches?.[0]||e.changedTouches?.[0]||e;setSliderValue(valueFromY(touch.clientY))}
function ensurePanel(){ensureStyle();let p=panel();if(p)return p;p=document.createElement('div');p.id=PANEL_ID;p.dataset.on='0';p.innerHTML='<div class="gv-avm-touch-shield" aria-hidden="true"></div><div class="gv-avm-title">CROSS FADE</div><div class="gv-avm-rail" aria-hidden="true"></div><div class="gv-avm-thumb" aria-hidden="true"></div><input aria-label="CROSS FADE" type="range" min="0" max="100" step="1" value="'+DEFAULT_SLIDER+'">';document.body.appendChild(p);const shield=p.querySelector('.gv-avm-touch-shield');for(const el of [shield,p.querySelector('input')]){if(!el)continue;for(const ev of ['pointerdown','pointermove','touchstart','touchmove','mousedown','mousemove'])el.addEventListener(ev,handlePanelPoint,{capture:true,passive:false});for(const ev of ['pointerup','touchend','mouseup','click'])el.addEventListener(ev,e=>{e.stopPropagation();},{capture:true,passive:true})}const sl=slider();if(sl){sl.addEventListener('input',()=>{applyOpacity();setPanelVisible(!!lastKey)},{passive:true});sl.addEventListener('change',()=>{applyOpacity();setPanelVisible(!!lastKey)},{passive:true})}updateThumb();return p}
function avmUrlFor(d){if(!d)return '';return d.avmAuthorityUrl||d.avmSourceUrl||d.selectedImageUrl||d.imageUrl||d.screenUrl||d.hdUrl||d.largeUrl||d.url||d.thumbnailUrl||''}
function destinationKey(d,url){if(!d&&!url)return '';return String(d?.id||d?.archiveId||d?.sourceId||d?.designation||d?.name||url||'').trim()+'|'+String(url||avmUrlFor(d)||'').trim()}
function addCandidate(out,d){const url=avmUrlFor(d);if(!url)return;const key=destinationKey(d,url);if(!key)return;if(out.some(x=>x.key===key))return;out.push({d,url,key})}
function liveCandidates(){const s=stateOf();const g=globalThis.GalaxyRandomGalaxy||{};const out=[];for(const d of [s.activeDestination,s.currentDestination,randomRef?.activeDestination,randomRef?.currentDestination,g.activeDestination,g.currentDestination])addCandidate(out,d);return out}
function bestDestination(){return liveCandidates()[0]||null}
function currentKey(){return bestDestination()?.key||''}
function destinationStillCurrent(key){return !!key&&key===currentKey()}
function clearArrivalTimer(){if(arrivalTimer){clearTimeout(arrivalTimer);arrivalTimer=0}scheduledKey=''}

function clearPendingOverlay(){
  try{
    if(aladinRef&&typeof aladinRef.removeOverlayImageLayer==='function'&&pendingOverlay)
      aladinRef.removeOverlayImageLayer(pendingLayerName);
  }catch(_){}
  releaseLayerBlend(pendingLayerName);
  pendingOverlay=null;
  pendingKey='';
  pendingReady=false;
  pendingContext=null;
  if(loadingKey&&loadingKey!==lastKey)loadingKey='';
}

function clearOverlay(){
  clearArrivalTimer();
  cancelPanelRecovery();
  try{
    if(aladinRef&&typeof aladinRef.removeOverlayImageLayer==='function'){
      aladinRef.removeOverlayImageLayer(activeLayerName);
      aladinRef.removeOverlayImageLayer(pendingLayerName);
    }
  }catch(_){}
  releaseLayerBlend(activeLayerName);
  releaseLayerBlend(pendingLayerName);
  overlay=null;
  lastKey='';
  loadingKey='';
  pendingOverlay=null;
  pendingKey='';
  pendingReady=false;
  pendingContext=null;
  activeLayerName=LAYER_NAMES[0];
  pendingLayerName=LAYER_NAMES[1];
  setPanelVisible(false);
}

/* 0036: travel never removes the currently visible AVM. */
function hideOverlayForTravel(){
  navigationSeen=true;
  clearArrivalTimer();
  setPanelVisible(false);
}

function installTravelButtonGuard(){
  const buttons=document.querySelectorAll('#gv-random-galaxy,.gv-galaxy-history');
  for(const b of buttons){
    if(!b||b.dataset.gvAvmGuard0036)continue;
    b.dataset.gvAvmGuard0036='1';
    for(const ev of ['pointerdown','touchstart','click'])
      b.addEventListener(ev,hideOverlayForTravel,{capture:true,passive:true});
  }
}

function setOverlayOpacity(target,value){
  if(!target)return;
  try{if(typeof target.setOpacity==='function')target.setOpacity(value)}catch(_){}
  try{if(typeof target.setAlpha==='function')target.setAlpha(value)}catch(_){}
  try{if(target.options)target.options.opacity=value}catch(_){}
}

function promotePending(d,key,reason){
  if(!pendingOverlay||!pendingReady||pendingKey!==key)return false;

  const oldOverlay=overlay;
  const oldLayerName=activeLayerName;
  const newOverlay=pendingOverlay;
  const newLayerName=pendingLayerName;
  const context=pendingContext;

  resetSliderOpaque();
  setOverlayOpacity(newOverlay,1);

  overlay=newOverlay;
  lastKey=key;
  lastContext={
    ...(context||{}),
    version:VERSION,
    mode:'double-buffer-active',
    reason,
    destination:d,
    overlay:newOverlay,
    opacity:1
  };

  activeLayerName=newLayerName;
  pendingLayerName=oldLayerName;

  pendingOverlay=null;
  pendingKey='';
  pendingReady=false;
  pendingContext=null;
  loadingKey='';

  /* 0041: Navigation owns camera rotation during travel/arrival. */

  try{
    if(oldOverlay&&aladinRef&&typeof aladinRef.removeOverlayImageLayer==='function')
      aladinRef.removeOverlayImageLayer(oldLayerName);
  }catch(_){}
  releaseLayerBlend(oldLayerName);

  applyOpacity();
  setPanelVisible(true);
  schedulePanelRecovery(key);
  trace('AVM_DOUBLE_BUFFER_PROMOTE',{key,reason,oldLayerName,newLayerName});
  return true;
}


/*
 * 0041 — TWO-IMAGE NAVIGATION BUFFER
 *
 * ACTIVE  = galaxy we are departing from.
 * PENDING = already-loaded destination galaxy.
 *
 * Zoom-out / cruise:
 *     ACTIVE  opacity 0
 *     PENDING opacity 0
 *
 * Final destination zoom-in:
 *     ACTIVE  opacity 0
 *     PENDING opacity 1
 *
 * Arrival:
 *     PENDING becomes ACTIVE.
 *     Old ACTIVE is then released.
 */
function hideForCruise(d){
  const url=String(d?.avmAuthorityUrl||avmUrlFor(d)||'').trim();
  const key=destinationKey(d,url);

  setPanelVisible(false);

  setOverlayOpacity(overlay,0);
  setOverlayOpacity(pendingOverlay,0);

  trace('AVM_0041_PHASE_CRUISE_HIDE',{
    key,
    lastKey,
    pendingKey,
    pendingReady
  });

  return true;
}

function showPendingForZoomIn(d){
  const url=String(d?.avmAuthorityUrl||avmUrlFor(d)||'').trim();
  const key=destinationKey(d,url);

  setPanelVisible(false);

  if(
    !pendingOverlay ||
    !pendingReady ||
    pendingKey!==key
  ){
    trace('AVM_0041_ZOOM_IN_PENDING_NOT_READY',{
      key,
      pendingKey,
      pendingReady,
      hasPendingOverlay:!!pendingOverlay
    });

    return false;
  }

  // Old image remains retained but invisible as rollback insurance.
  setOverlayOpacity(overlay,0);

  // Destination photograph materializes DURING final zoom-in.
  setOverlayOpacity(pendingOverlay,1);

  trace('AVM_0041_ZOOM_IN_DESTINATION_VISIBLE',{
    key,
    pendingKey
  });

  return true;
}

function commitPreparedArrival(d){
  const url=String(d?.avmAuthorityUrl||avmUrlFor(d)||'').trim();
  const key=destinationKey(d,url);

  if(!key)return false;

  // Already committed by fallback watcher.
  if(key===lastKey){
    setOverlayOpacity(overlay,1);
    applyOpacity();
    setPanelVisible(true);
    schedulePanelRecovery(key);

    trace('AVM_0046_ARRIVAL_ALREADY_ACTIVE',{key});
    return true;
  }

  if(
    pendingOverlay &&
    pendingReady &&
    pendingKey===key
  ){
    const committed=
      promotePending(
        d,
        key,
        'navigation-phase-arrival'
      );

    trace('AVM_0041_ARRIVAL_COMMIT',{
      key,
      committed
    });

    return committed;
  }

  if(pendingKey===key&&pendingPreparePromise){
    trace('AVM_0046_ARRIVAL_AWAIT_PENDING',{key,pendingReady,hasPendingOverlay:!!pendingOverlay});
    void Promise.resolve(pendingPreparePromise)
      .then(()=>{
        if(pendingOverlay&&pendingReady&&pendingKey===key&&destinationStillCurrent(key))
          promotePending(d,key,'arrival-await-pending');
        else
          maybeLoadAfterArrival('arrival-await-pending-fallback');
      })
      .catch(error=>{
        trace('AVM_0046_ARRIVAL_AWAIT_PENDING_ERROR',{key,message:String(error?.message||error||'')});
        maybeLoadAfterArrival('arrival-await-pending-error');
      });
    return true;
  }

  trace('AVM_0046_ARRIVAL_COMMIT_REJECT',{
    key,
    lastKey,
    pendingKey,
    pendingReady,
    hasPendingOverlay:!!pendingOverlay
  });

  maybeLoadAfterArrival('arrival-commit-recovery');
  return false;
}

function imageFormatFor(url){return /\.png(?:[?#]|$)/i.test(url)?'png':'jpeg'}
function canCommandAladin(key){return isArrivedStable()&&destinationStillCurrent(key)}
function finiteValue(v){const n=Number(v);return Number.isFinite(n)?n:null}function normalize180(deg){let n=Number(deg);if(!Number.isFinite(n))return null;n=((n+180)%360+360)%360-180;return n}function cameraFromAvmRotation(deg){let camera=normalize180(deg);if(camera===null)return null;if(camera>90)camera-=180;if(camera<=-90)camera+=180;return camera}function ownValue(o,k){return o&&Object.prototype.hasOwnProperty.call(o,k)?o[k]:undefined}function avmRotationSource(d){if(!d)return {source:'missing-destination',value:null,camera:null};const candidates=[['avmRotation',d.avmRotation],['wcs_rotation',d.wcs_rotation],['wcsRotation',d.wcsRotation],['spatialRotation',d.spatialRotation],['spatial_rotation',d.spatial_rotation],['Spatial_Rotation',d.Spatial_Rotation],['SpatialRotation',d.SpatialRotation],['Spatial.Rotation',ownValue(d,'Spatial.Rotation')],['Spatial.Rotation.nested',d.Spatial&&d.Spatial.Rotation],['spatial.Rotation.nested',d.spatial&&d.spatial.Rotation],['avm.Spatial.Rotation',d.avm&&ownValue(d.avm,'Spatial.Rotation')],['avm.spatialRotation',d.avm&&d.avm.spatialRotation],['metadata.Spatial.Rotation',d.metadata&&ownValue(d.metadata,'Spatial.Rotation')],['metadata.wcs_rotation',d.metadata&&d.metadata.wcs_rotation],['wcs.rotation',d.wcs&&d.wcs.rotation]];for(const [source,value] of candidates){const n=finiteValue(value);if(n!==null)return {source,value:n,camera:cameraFromAvmRotation(n)}}return {source:'none',value:null,camera:null}}function applyPreparedAuthorityCamera(d,key){const camera=finiteValue(d?.avmCameraRotation);const before=cameraSnapshot('before-prepared-authority-camera',d);let applied=false;if(camera!==null&&typeof aladinRef.setRotation==='function'){aladinRef.setRotation(camera);applied=true}const after=cameraSnapshot('after-prepared-authority-camera',d);trace('AVM_PREPARED_AUTHORITY_CAMERA_APPLIED',{key,camera,applied,before,after,catalog:catalogSummary(d)});return {source:'avmCameraRotation',camera,applied,before,after}}function catalogSummary(d){return {name:String(d?.name||''),archiveId:String(d?.archiveId||''),sourceUrl:String(d?.sourceUrl||''),selectedImageUrl:String(d?.selectedImageUrl||''),ra:finiteValue(d?.ra),dec:finiteValue(d?.dec),fovDegrees:finiteValue(d?.fovDegrees),imageFovDeg:finiteValue(d?.imageFovDeg??d?.imageFovDegrees??d?.image_fov_degrees),imageFovXDeg:finiteValue(d?.imageFovXDeg??d?.imageFovXDegrees??d?.image_fov_x_degrees),imageFovYDeg:finiteValue(d?.imageFovYDeg??d?.imageFovYDegrees??d?.image_fov_y_degrees),aladinRotation:finiteValue(d?.aladinRotation),avmRotation:avmRotationSource(d)}}function cameraSnapshot(label,d){let fov=null,rotation=null,center=null;try{const raw=aladinRef?.getFov?.();fov=Array.isArray(raw)?Number(raw[0]):Number(raw)}catch(_){}try{rotation=Number(aladinRef?.getRotation?.())}catch(_){}try{const c=aladinRef?.getRaDec?.();if(Array.isArray(c))center={ra:Number(c[0]),dec:Number(c[1])}}catch(_){}const detail={label,fov:Number.isFinite(fov)?fov:null,rotation:Number.isFinite(rotation)?rotation:null,center,catalog:catalogSummary(d)};trace('AVM_CAMERA_SNAPSHOT',detail);return detail}function applyAvmCallbackCamera(ra,dec,fov,d,key){const before=cameraSnapshot('before-callback-camera',d);const callbackFov=finiteValue(fov);let didCenter=false,didFov=false;if(Number.isFinite(Number(ra))&&Number.isFinite(Number(dec))&&typeof aladinRef.gotoRaDec==='function'){aladinRef.gotoRaDec(Number(ra),Number(dec));didCenter=true}const after=cameraSnapshot('after-callback-ra-dec-fov',d);trace('AVM_CALLBACK_CAMERA_APPLIED',{key,ra:Number(ra),dec:Number(dec),fov:callbackFov,didCenter,didFov,before,after,catalog:catalogSummary(d)});return {didCenter,didFov,callbackFov,before,after}}function applyAvmCameraRoll(d,key){const rot=avmRotationSource(d);const before=cameraSnapshot('before-avm-camera-roll',d);let applied=false;if(rot.camera!==null&&typeof aladinRef.setRotation==='function'){aladinRef.setRotation(rot.camera);applied=true}const after=cameraSnapshot('after-avm-camera-roll',d);trace('AVM_CAMERA_ROLL_APPLIED',{key,source:rot.source,avmRotation:rot.value,camera:rot.camera,applied,before,after,catalog:catalogSummary(d)});return {source:rot.source,avmRotation:rot.value,camera:rot.camera,applied,before,after}}let interactionDiagnosticInstalled=false;function installInteractionDiagnostics(){if(interactionDiagnosticInstalled)return;const host=rootRef||document.body;if(!host||!host.addEventListener)return;interactionDiagnosticInstalled=true;let last=0;function snap(kind,phase){const now=Date.now();if(phase==='before'&&now-last<140)return;last=now;const d=bestDestination()?.d||stateOf()?.activeDestination||null;trace('AVM_INTERACTION_CAMERA',{kind,phase,camera:cameraSnapshot(kind+'-'+phase,d),catalog:catalogSummary(d)})}for(const ev of ['wheel','pointerdown','touchstart'])host.addEventListener(ev,()=>snap(ev,'before'),{capture:true,passive:true});for(const ev of ['wheel','pointerup','touchend'])host.addEventListener(ev,()=>setTimeout(()=>snap(ev,'after'),80),{capture:true,passive:true})}
function cloneWcsForVisible(d){
  const source=d?.avmAuthorityWcs;
  if(!source||typeof source!=='object')return null;
  const wcs={};
  for(const [key,value] of Object.entries(source)){
    if(
      value!==undefined&&
      value!==null&&
      (
        typeof value==='string'||
        typeof value==='number'||
        typeof value==='boolean'
      )
    )wcs[key]=value;
  }
  for(const required of ['CRVAL1','CRVAL2','CRPIX1','CRPIX2']){
    if(!Number.isFinite(Number(wcs[required])))return null;
  }

  const ctype1=String(wcs.CTYPE1||'').trim().toUpperCase();
  const ctype2=String(wcs.CTYPE2||'').trim().toUpperCase();
  const cdKeys=['CD1_1','CD1_2','CD2_1','CD2_2'];
  const hasCd=cdKeys.every(key=>Number.isFinite(Number(wcs[key])));
  const xScale=Number(wcs.CDELT1);
  const yScale=Number(wcs.CDELT2);

  if(
    ctype1.startsWith('RA---') &&
    ctype2.startsWith('DEC--') &&
    !hasCd &&
    Number.isFinite(xScale) &&
    Number.isFinite(yScale) &&
    xScale>0 &&
    yScale>0
  ){
    wcs.CDELT1=-xScale;
    trace('AVM_VISIBLE_WCS_HANDEDNESS_NORMALIZED',{
      archiveId:String(d?.archiveId||''),
      before:{CDELT1:xScale,CDELT2:yScale,CROTA2:finiteValue(wcs.CROTA2)},
      after:{CDELT1:wcs.CDELT1,CDELT2:wcs.CDELT2,CROTA2:finiteValue(wcs.CROTA2)}
    });
  }

  return wcs;
}
function scaledWcsForBlend(baseWcs,blendSource){
  if(!baseWcs||!blendSource)return baseWcs;

  const sw=Number(blendSource.sourceWidth)||0;
  const sh=Number(blendSource.sourceHeight)||0;
  const ow=Number(blendSource.outputWidth)||0;
  const oh=Number(blendSource.outputHeight)||0;

  if(sw<1||sh<1||ow<1||oh<1||(sw===ow&&sh===oh))
    return baseWcs;

  const sx=sw/ow,sy=sh/oh,wcs={...baseWcs};

  if(Number.isFinite(Number(wcs.CRPIX1)))
    wcs.CRPIX1=(Number(wcs.CRPIX1)-.5)/sx+.5;
  if(Number.isFinite(Number(wcs.CRPIX2)))
    wcs.CRPIX2=(Number(wcs.CRPIX2)-.5)/sy+.5;

  const hasCd=
    ['CD1_1','CD1_2','CD2_1','CD2_2']
      .every(key=>Number.isFinite(Number(wcs[key])));

  if(hasCd){
    wcs.CD1_1=Number(wcs.CD1_1)*sx;
    wcs.CD2_1=Number(wcs.CD2_1)*sx;
    wcs.CD1_2=Number(wcs.CD1_2)*sy;
    wcs.CD2_2=Number(wcs.CD2_2)*sy;
  }else{
    if(Number.isFinite(Number(wcs.CDELT1)))
      wcs.CDELT1=Number(wcs.CDELT1)*sx;
    if(Number.isFinite(Number(wcs.CDELT2)))
      wcs.CDELT2=Number(wcs.CDELT2)*sy;
  }

  wcs.NAXIS1=ow;
  wcs.NAXIS2=oh;

  trace('AVM_0048_WCS_SCALED_FOR_BLEND',{
    sourceWidth:sw,sourceHeight:sh,
    outputWidth:ow,outputHeight:oh,
    sx,sy
  });

  return wcs;
}
function travelIdentity(d){
  const authorityUrl=String(d?.avmAuthorityUrl||avmUrlFor(d)||'').trim();
  const key=destinationKey(d,authorityUrl);
  return {authorityUrl,key};
}
function isPreparedForTravel(d){
  const {key}=travelIdentity(d);
  return Boolean(
    key &&
    pendingReady===true &&
    pendingKey===key &&
    pendingOverlay
  );
}
async function stageForTravel(d,{hidePanel=false}={}){
  trace('AVM_PRETRAVEL_REQUEST',{name:String(d?.name||''),archiveId:String(d?.archiveId||''),hidePanel:Boolean(hidePanel)});
  if(!ARef||!aladinRef)throw new Error('AVM PRETRAVEL VIEWER NOT INSTALLED');

  const {authorityUrl,key}=travelIdentity(d);

  if(vignetteBackoffActive(key,'pretravel-auto')){
    if(hidePanel)setPanelVisible(false);
    return false;
  }

  const preparedUrl=String(d?.preparedHdUrl||'').trim();
  const sourceUrl=preparedUrl||authorityUrl;
  const mirrorUrl=String(d?.githubImageUrl||'').trim();
  const filterSourceUrl=mirrorUrl||sourceUrl;
  const baseWcs=cloneWcsForVisible(d);
  if(!authorityUrl||!sourceUrl||!key||!baseWcs)
    throw new Error('AVM PRETRAVEL DESTINATION/WCS INVALID');

  if(isPreparedForTravel(d)){
    if(hidePanel)setPanelVisible(false);
    trace('AVM_PRETRAVEL_REUSE_READY',{key,authorityUrl,sourceUrl,prepared:Boolean(preparedUrl)});
    return true;
  }

  if(loadingKey===key&&pendingPreparePromise){
    if(hidePanel)setPanelVisible(false);
    trace('AVM_PRETRAVEL_REUSE_PENDING',{key,authorityUrl,sourceUrl,prepared:Boolean(preparedUrl)});
    return pendingPreparePromise;
  }

  clearArrivalTimer();
  clearPendingOverlay();

  loadingKey=key;
  pendingKey=key;
  pendingReady=false;
  scheduledKey='';
  if(hidePanel)setPanelVisible(false);

  const stagedLayerName=pendingLayerName;

  const promise=(async()=>{
    const blendSource=await makeGlobalBlendSource(
      filterSourceUrl,
      key,
      mirrorUrl ? null : (d?.preparedHdImage||null),
      authorityUrl
    );

    clearVignetteFailure(key,'pretravel-blend-ready');

    if(blendSource?.filtered!==true)
      throw new Error('AVM 0049 VIGNETTE FILTER REQUIRED');
    const wcs=scaledWcsForBlend(baseWcs,blendSource);
    if(loadingKey!==key||pendingKey!==key){
      releaseBlendUrl(blendSource.objectUrl);
      throw new Error('AVM PRETRAVEL BLEND SUPERSEDED');
    }
    return new Promise((resolve,reject)=>{
      let settled=false;
      const finish=(error,value)=>{
        if(settled)return;
        settled=true;
        if(error){
          if(loadingKey===key)loadingKey='';
          trace('AVM_PRETRAVEL_ERROR',{key,authorityUrl,sourceUrl,filtered:blendSource.filtered,prepared:Boolean(preparedUrl),message:String(error?.message||error||'')});
          reject(error);
        }else resolve(value);
      };

      try{
        bindLayerBlend(stagedLayerName,blendSource.objectUrl);
        const imageLayer=ARef.image(blendSource.url,{
          name:stagedLayerName,
          imgFormat:blendSource.imgFormat,
          wcs,
          opacity:0,
          successCallback:(ra,dec,fov,image)=>{
            if(key!==loadingKey||pendingOverlay!==imageLayer||pendingLayerName!==stagedLayerName){
              finish(new Error('AVM PRETRAVEL LOAD SUPERSEDED'));
              return;
            }

            pendingReady=true;
            loadingKey='';
            pendingContext={
              version:VERSION,
              mode:'double-buffer-pending',
              reason:'random-pretravel',
              destination:d,
              url:authorityUrl,
              sourceUrl,
              layerUrl:blendSource.url,
              filtered:blendSource.filtered,
              prepared:Boolean(preparedUrl),
              opacity:0,
              ra,dec,fov,image,
              overlay:imageLayer
            };

            trace('AVM_PRETRAVEL_READY',{
              key,authorityUrl,sourceUrl,filtered:blendSource.filtered,prepared:Boolean(preparedUrl),ra,dec,fov,
              activeLayerName,
              pendingLayerName:stagedLayerName,
              camera:cameraSnapshot('pretravel-pending-ready',d),
              catalog:catalogSummary(d)
            });
            finish(null,true);
          },
          errorCallback:error=>{
            if(pendingOverlay===imageLayer)clearPendingOverlay();
            finish(error instanceof Error?error:new Error(String(error||'AVM PRETRAVEL IMAGE LOAD FAILED')));
          }
        });

        pendingOverlay=imageLayer;
        trace('AVM_PRETRAVEL_SET_PENDING_LAYER',{key,authorityUrl,sourceUrl,filtered:blendSource.filtered,prepared:Boolean(preparedUrl),activeLayerName,pendingLayerName:stagedLayerName});
        aladinRef.setOverlayImageLayer(imageLayer,stagedLayerName);
      }catch(error){
        clearPendingOverlay();
        finish(error);
      }
    });
  })();

  let wrapped;
  wrapped=promise.catch(error=>{
    markVignetteFailure(key,error,'pretravel');
    throw error;
  }).finally(()=>{
    if(pendingPreparePromise===wrapped)pendingPreparePromise=null;
  });
  pendingPreparePromise=wrapped;
  return wrapped;
}
function prepareForTravel(d){
  return stageForTravel(d,{hidePanel:true});
}

function loadArrivedCandidate(candidate,reason){
  trace('AVM_LOAD_CANDIDATE_ENTER',{reason,key:candidate?.key});

  if(
    !candidate ||
    !canCommandAladin(candidate.key) ||
    candidate.key===loadingKey
  ){
    trace('AVM_LOAD_CANDIDATE_REJECT',{
      reason,
      key:candidate?.key,
      loadingKey
    });
    return false;
  }

  clearPendingOverlay();

  const key=candidate.key;

  if(vignetteBackoffActive(key,'arrival-load'))
    return false;

  const authorityUrl=candidate.url;
  const preparedUrl=String(candidate.d?.preparedHdUrl||'').trim();
  const sourceUrl=preparedUrl||authorityUrl;
  const mirrorUrl=String(candidate.d?.githubImageUrl||'').trim();
  const filterSourceUrl=mirrorUrl||sourceUrl;
  const preparedImage=mirrorUrl ? null : (candidate.d?.preparedHdImage||null);
  const stagedLayerName=pendingLayerName;

  loadingKey=key;
  pendingKey=key;
  pendingReady=false;

  void (async()=>{
    let blendSource=null;

    try{
      blendSource=await makeGlobalBlendSource(
        filterSourceUrl,
        key,
        preparedImage,
        authorityUrl
      );

      clearVignetteFailure(key,'arrival-blend-ready');

      if(blendSource?.filtered!==true)
        throw new Error('AVM 0049 VIGNETTE FILTER REQUIRED');

      if(
        !canCommandAladin(key) ||
        loadingKey!==key ||
        pendingKey!==key
      ){
        releaseBlendUrl(blendSource.objectUrl);
        if(loadingKey===key)loadingKey='';
        return;
      }

      bindLayerBlend(stagedLayerName,blendSource.objectUrl);

      const imageLayer=ARef.image(
        blendSource.url,
        {
          name:stagedLayerName,
          imgFormat:blendSource.imgFormat,
          wcs:scaledWcsForBlend(
            cloneWcsForVisible(candidate.d),
            blendSource
          ),
          opacity:0,
          successCallback:(ra,dec,fov,image)=>{
            if(
              !canCommandAladin(key) ||
              pendingOverlay!==imageLayer ||
              pendingLayerName!==stagedLayerName
            ){
              if(loadingKey===key)loadingKey='';
              return;
            }

            pendingReady=true;
            loadingKey='';
            pendingContext={
              version:VERSION,
              mode:'double-buffer-arrival-pending',
              reason,
              destination:candidate.d,
              url:authorityUrl,
              sourceUrl,
              prepared:Boolean(preparedUrl),
              layerUrl:blendSource.url,
              filtered:true,
              opacity:0,
              ra,dec,fov,image,
              overlay:imageLayer
            };

            promotePending(
              candidate.d,
              key,
              'arrival-loaded-'+reason
            );
          },
          errorCallback:error=>{
            trace('AVM_AREF_IMAGE_ERROR',{
              reason,
              key,
              url:authorityUrl,
              sourceUrl,
              filtered:true,
              message:String(error?.message||error||'')
            });

            if(pendingOverlay===imageLayer)
              clearPendingOverlay();

            if(loadingKey===key)
              loadingKey='';

            markVignetteFailure(
              key,
              error,
              'arrival-image-layer'
            );
          }
        }
      );

      pendingOverlay=imageLayer;
      aladinRef.setOverlayImageLayer(
        imageLayer,
        stagedLayerName
      );

      trace('AVM_PENDING_LAYER_INSTALLED',{
        key,
        reason,
        filtered:true,
        prepared:Boolean(preparedUrl),
        sourceKind:blendSource.sourceKind,
        activeLayerName,
        pendingLayerName:stagedLayerName
      });
    }catch(error){
      if(blendSource?.objectUrl)
        releaseBlendUrl(blendSource.objectUrl);

      if(pendingKey===key)
        clearPendingOverlay();

      if(loadingKey===key)
        loadingKey='';

      trace('AVM_FILTERED_LOAD_RETRY',{
        reason,
        key,
        authorityUrl,
        sourceUrl,
        prepared:Boolean(preparedUrl),
        message:String(error?.message||error||'')
      });

      markVignetteFailure(
        key,
        error,
        'arrival-filter'
      );
    }
  })();

  return true;
}

function maybeLoadAfterArrival(reason){
  trace('AVM_LOAD_REQUEST',{reason});
  installTravelButtonGuard();
  ensurePanel();

  if(hdOpen()){
    trace('AVM_HD_OPEN_SKIP',{reason});
    clearOverlay();
    return false;
  }

  if(!isArrivedStable()){
    trace('AVM_NOT_ARRIVED_STABLE',{reason});
    setPanelVisible(false);
    return false;
  }

  const candidate=bestDestination();
  trace('AVM_CANDIDATE_RESULT',{reason,key:candidate?.key,url:candidate?.url});
  if(!candidate||!canCommandAladin(candidate.key)){
    trace('AVM_CANDIDATE_REJECT',{reason,key:candidate?.key});
    return false;
  }

  if(vignetteBackoffActive(candidate.key,'arrival-watch'))
    return false;

  if(candidate.key===lastKey){
    applyOpacity();
    setPanelVisible(true);
    schedulePanelRecovery(candidate.key);
    return true;
  }

  if(candidate.key===pendingKey&&pendingReady)
    return promotePending(candidate.d,candidate.key,'arrival-promote-'+reason);

  if(candidate.key===pendingKey||candidate.key===loadingKey||candidate.key===scheduledKey)
    return true;

  clearPendingOverlay();
  scheduledKey=candidate.key;
  trace('AVM_SCHEDULE_SETTLE',{reason,key:candidate.key,delayMs:ARRIVAL_SETTLE_MS});

  arrivalTimer=setTimeout(()=>{
    arrivalTimer=0;
    const fresh=bestDestination();

    if(!fresh||fresh.key!==scheduledKey||!canCommandAladin(fresh.key)){
      trace('AVM_SETTLE_REJECT',{reason,key:fresh?.key,scheduledKey});
      scheduledKey='';
      return;
    }

    scheduledKey='';
    loadArrivedCandidate(fresh,'arrival-settle-'+reason);
  },ARRIVAL_SETTLE_MS);

  return true;
}

function install({A,aladin,viewerRoot,randomGalaxy}={}){trace('AVM_INSTALL_ENTER',{hasA:!!A,hasAladin:!!aladin});if(!A)throw new Error('ALADIN A NAMESPACE MISSING');if(!aladin)throw new Error('ALADIN INSTANCE MISSING');ARef=A;aladinRef=aladin;randomRef=randomGalaxy;rootRef=viewerRoot||document.body;ensurePanel();installTravelButtonGuard();installInteractionDiagnostics();setPanelVisible(false);if(!watchTimer)watchTimer=setInterval(()=>{maybeLoadAfterArrival('watch')},WATCH_MS);try{console.info('GV AVM LAB 0046 INSTALLED navigation-phase two-image buffer')}catch(_){}trace('AVM_INSTALL_EXIT',{version:VERSION});return {version:VERSION,panel:panel(),loadForBestDestination:maybeLoadAfterArrival}}
function uninstall(){clearArrivalTimer();cancelPanelRecovery();if(watchTimer){clearInterval(watchTimer);watchTimer=null}clearOverlay();try{panel()?.remove()}catch(_){}try{document.getElementById(STYLE_ID)?.remove()}catch(_){}}
globalThis.GalaxyViewerAvmOverlayLab={
  VERSION,
  install,
  uninstall,
  prepareForTravel,
  stageForTravel,
  isPreparedForTravel,
  hideForCruise,
  showPendingForZoomIn,
  commitPreparedArrival,
  loadForBestDestination:maybeLoadAfterArrival,
  get lastContext(){return lastContext}
};
})();
