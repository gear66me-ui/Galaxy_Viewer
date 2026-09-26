(function(global){
"use strict";
const VERSION="0013";
const LAYER_NAME="GV AVM NATIVE OVERLAY";
const WATCH_MS=140;
const FOV_PAD=1.0;
let overlay=null;
let lastContext=null;
let lastKey="";
let loadingKey="";
let randomRef=null;
let aladinRef=null;
let rootRef=null;
let vignette=null;
let ARef=null;
let watchTimer=null;
let suppressUntil=0;
let panelEverEnabled=false;
let travelOldKey="";
let travelMinUntil=0;
const browserPreloaded=new Set();
const nativePreloadReady=new Map();
const nativePreloadLoading=new Set();
const keepAlive=[];

function text(v){return String(v??"").trim()}
function finite(v){v=Number(v);return Number.isFinite(v)?v:null}
function clamp01(v){v=Number(v);return Number.isFinite(v)?Math.max(0,Math.min(1,v)):0.55}

function arcminToDeg(v){v=finite(v);return v!==null&&v>0?v/60:null}

function sourceImageFov(d,fallback){
  const x=finite(d?.imageFovXDeg)??arcminToDeg(d?.imageFovXArcmin);
  const y=finite(d?.imageFovYDeg)??arcminToDeg(d?.imageFovYArcmin);
  const s=finite(d?.imageFovDeg)??finite(d?.imageFovDegrees)??finite(d?.fieldOfViewDegrees)??finite(d?.fovDegrees)??finite(fallback);
  return {x,y,scalar:s??((x!==null&&y!==null)?Math.max(x,y):null)};
}

function viewportAspect(){
  try{
    const r=(rootRef||document.body).getBoundingClientRect();
    if(r.width>0&&r.height>0)return r.width/r.height;
  }catch(_){}
  return window.innerWidth>0&&window.innerHeight>0?window.innerWidth/window.innerHeight:1;
}

function fitFovFor(d,fallback){
  const src=sourceImageFov(d,fallback);
  let f=src.scalar;
  const va=viewportAspect();
  if(src.x!==null&&src.y!==null&&va>0){
    f=Math.max(src.x,src.y*va,f||0);
  }
  return finite(f);
}

function ensureVignette(){
  if(vignette&&vignette.isConnected)return vignette;
  vignette=document.getElementById("gv-avm-overlay-vignette")||document.createElement("div");
  vignette.id="gv-avm-overlay-vignette";
  vignette.setAttribute("aria-hidden","true");
  const host=rootRef||document.body;
  try{
    if(host&&host!==document.body&&getComputedStyle(host).position==="static")host.style.position="relative";
  }catch(_){}
  if(!vignette.parentNode)host.appendChild(vignette);
  return vignette;
}

function applyVignetteFor(d,fallback){
  const v=ensureVignette();
  const src=sourceImageFov(d,fallback);
  const va=viewportAspect();
  let rx=74,ry=74;
  if(src.x!==null&&src.y!==null&&src.y>0&&va>0){
    const ratio=Math.max(0.25,Math.min(4,(src.x/src.y)/va));
    if(ratio>=1){
      rx=78;
      ry=Math.max(42,Math.min(78,78/ratio));
    }else{
      ry=78;
      rx=Math.max(42,Math.min(78,78*ratio));
    }
  }
  v.style.setProperty("--gv-vig-x",rx.toFixed(1)+"%");
  v.style.setProperty("--gv-vig-y",ry.toFixed(1)+"%");
  v.dataset.on="1";
  setPanelVisible(true);
}


function collectUrls(d){
  const fields=["avmSourceUrl","screenUrl","hdUrl","selectedImageUrl","esaPublicationJpeg","githubImageUrl","imageUrl","imageURL","sourceUrl"];
  const urls=[];
  for(const k of fields){
    const v=text(d?.[k]);
    if(/^https:\/\//i.test(v))urls.push(v);
  }
  const variants=d?.imageVariants||d?.variants||[];
  if(Array.isArray(variants)){
    for(const v of variants){
      if(typeof v==="string" && /^https:\/\//i.test(v.trim()))urls.push(v.trim());
      else if(v&&typeof v==="object"){
        for(const x of Object.values(v)){
          if(typeof x==="string" && /^https:\/\//i.test(x.trim()))urls.push(x.trim());
        }
      }
    }
  }
  return [...new Set(urls)];
}

function avmUrlFor(d){
  const urls=collectUrls(d);
  return urls.find(u=>/\/screen\//i.test(u)) ||
         urls.find(u=>/\.(jpg|jpeg)(?:[?#]|$)/i.test(u)) ||
         urls[0] ||
         "";
}

function destinationKey(d,url){
  return text(d?.archiveId) ||
         text(d?.designation) ||
         text(d?.name)+"|"+text(d?.ra)+"|"+text(d?.dec)+"|"+url ||
         url;
}

function isUsableAvmDestination(d,url){
  if(!d || !url)return false;
  if(text(d.name).match(/^earth\b|milky way/i) && !text(d.screenUrl) && !text(d.avmSourceUrl))return false;
  if(text(d.avmProfile)==="AVM")return true;
  if(text(d.avmStatus).toUpperCase().includes("AVM"))return true;
  if(/\/screen\//i.test(url) && /cdn\.esa(hubble|webb)\.org/i.test(url))return true;
  return false;
}

function stateOf(randomGalaxy){
  try{return randomGalaxy?.getState?.()||{}}catch(_){return{}}
}

function addCandidate(out,item){
  if(!item)return;
  const d=item.destination||item.record||item;
  const url=avmUrlFor(d);
  if(isUsableAvmDestination(d,url))out.push(d);
}

function collectCandidatesFrom(root,out,seen,depth){
  if(!root||depth>5)return;
  if(typeof root!=="object")return;
  if(seen.has(root))return;
  seen.add(root);
  addCandidate(out,root);
  if(Array.isArray(root)){
    for(const x of root)collectCandidatesFrom(x,out,seen,depth+1);
    return;
  }
  for(const key of ["future","queue","route","navigationQueue","preparedQueue","prefetchReady","prefetchQueued","activePreparedItem","historyPreparedItems","queuedDestinations","destination","record"]){
    if(root[key])collectCandidatesFrom(root[key],out,seen,depth+1);
  }
}

function candidatesFromState(randomGalaxy){
  const s=stateOf(randomGalaxy);
  const g=global.GalaxyRandomGalaxy||{};
  const out=[];
  for(const d of [
    s.activeDestination,
    s.currentDestination,
    s.destination,
    s.travelDestination,
    randomGalaxy?.activeDestination,
    randomGalaxy?.currentDestination,
    randomGalaxy?.destination,
    randomGalaxy?.travelDestination,
    g.activeDestination,
    g.currentDestination,
    g.destination,
    g.travelDestination
  ])addCandidate(out,d);
  const unique=[];
  const keys=new Set();
  for(const d of out){
    const url=avmUrlFor(d);
    const key=destinationKey(d,url);
    if(!key||keys.has(key))continue;
    keys.add(key);
    unique.push(d);
  }
  return unique;
}

function upcomingCandidates(randomGalaxy){
  const s=stateOf(randomGalaxy);
  const g=global.GalaxyRandomGalaxy||{};
  const out=[];
  const seen=new WeakSet();
  for(const d of candidatesFromState(randomGalaxy))addCandidate(out,d);
  collectCandidatesFrom(s,out,seen,0);
  collectCandidatesFrom(g,out,seen,0);
  for(const key of ["future","queue","route","navigationQueue","preparedQueue","prefetchReady","prefetchQueued","activePreparedItem","historyPreparedItems","queuedDestinations"]){
    collectCandidatesFrom(randomGalaxy?.[key],out,seen,0);
  }
  const unique=[];
  const keys=new Set();
  for(const d of out){
    const url=avmUrlFor(d);
    const key=destinationKey(d,url);
    if(!key||keys.has(key))continue;
    keys.add(key);
    unique.push(d);
  }
  return unique;
}

function suppressed(){return Date.now()<suppressUntil}

function setPanelVisible(on){
  try{
    const p=panel();
    if(on)panelEverEnabled=true;
    p.dataset.on=panelEverEnabled?"1":"0";
  }catch(_){}
}

function hideVignette(){
  try{
    if(vignette)vignette.dataset.on="0";
    setPanelVisible(false);
  }catch(_){}
}

function hideOverlayForTravel(){
  preloadUpcoming("travel-button");
  travelOldKey=lastKey||loadingKey||"";
  travelMinUntil=Date.now()+350;
  suppressUntil=Math.max(suppressUntil,Date.now()+26000);
  loadingKey="";
  lastKey="";
  hideVignette();
  try{overlay?.setOpacity?.(0)}catch(_){}
  try{overlay?.setAlpha?.(0)}catch(_){}
  try{overlay?.setOptions?.({opacity:0})}catch(_){}
  for(const ms of [180,350,600,900,1250,1700,2400,3400,4800,6600,8800,11200,14000,17200,20800,24400]){
    setTimeout(()=>{preloadUpcoming("travel-preload-"+ms);loadForBestDestination("travel-poll-"+ms)},ms);
  }
}

function installTravelButtonGuard(){
  const buttons=document.querySelectorAll("#gv-random-galaxy,.gv-galaxy-history");
  for(const b of buttons){
    if(!b||b.dataset.gvAvmGuard0013)continue;
    b.dataset.gvAvmGuard0013="1";
    for(const ev of ["pointerdown","touchstart","click"]){
      b.addEventListener(ev,hideOverlayForTravel,{capture:true,passive:true});
    }
  }
}

function bestDestination(randomGalaxy){
  for(const d of candidatesFromState(randomGalaxy)){
    const url=avmUrlFor(d);
    if(isUsableAvmDestination(d,url))return {d,url,key:destinationKey(d,url)};
  }
  return null;
}

function browserPreloadUrl(url){
  if(browserPreloaded.has(url))return false;
  browserPreloaded.add(url);
  try{
    const link=document.createElement("link");
    link.rel="preload";
    link.as="image";
    link.href=url;
    document.head.appendChild(link);
    keepAlive.push(link);
  }catch(_){}
  try{
    const img=new Image();
    img.decoding="async";
    img.loading="eager";
    img.src=url;
    keepAlive.push(img);
  }catch(_){}
  try{
    if(global.fetch)global.fetch(url,{mode:"no-cors",cache:"force-cache",credentials:"omit"}).catch(()=>{});
  }catch(_){}
  if(keepAlive.length>120)keepAlive.splice(0,keepAlive.length-120);
  return true;
}

function preloadNativeOverlay(d,reason){
  if(!ARef)return false;
  const url=avmUrlFor(d);
  if(!isUsableAvmDestination(d,url))return false;
  const key=destinationKey(d,url);
  if(!key)return false;
  browserPreloadUrl(url);
  if(nativePreloadReady.has(key)||nativePreloadLoading.has(key))return false;
  nativePreloadLoading.add(key);
  let pre=null;
  try{
    pre=ARef.image(url,{
      name:LAYER_NAME+" PRELOAD",
      imgFormat:/\.png(?:[?#]|$)/i.test(url)?"png":"jpeg",
      opacity:0,
      successCallback:(ra,dec,fov,image)=>{
        nativePreloadLoading.delete(key);
        nativePreloadReady.set(key,{d,url,key,overlay:pre,ra,dec,fov,image,readyAt:Date.now()});
        keepAlive.push(pre);
        if(keepAlive.length>120)keepAlive.splice(0,keepAlive.length-120);
        try{console.info("GV AVM LAB 0013 NATIVE PRELOAD READY",{reason,key,name:d?.name,archiveId:d?.archiveId,url})}catch(_){}
      },
      errorCallback:(error)=>{
        nativePreloadLoading.delete(key);
        try{console.warn("GV AVM LAB 0013 NATIVE PRELOAD FAILED",{reason,key,url,error})}catch(_){}
      }
    });
    if(!pre){nativePreloadLoading.delete(key);return false}
    return true;
  }catch(error){
    nativePreloadLoading.delete(key);
    try{console.warn("GV AVM LAB 0013 NATIVE PRELOAD ERROR",{reason,key,url,error})}catch(_){}
    return false;
  }
}

function preloadUpcoming(reason){
  let count=0;
  for(const d of upcomingCandidates(randomRef)){
    if(preloadNativeOverlay(d,reason))count++;
    if(count>=10)break;
  }
  if(count){
    try{console.info("GV AVM LAB 0013 PRELOAD STARTED",{reason,count})}catch(_){}
  }
}
function panel(){
  let p=document.getElementById("gv-avm-overlay-lab");
  if(p)return p;
  p=document.createElement("div");
  p.id="gv-avm-overlay-lab";
  p.innerHTML="<div id=\"gv-avm-touch-shield\"><div id=\"gv-avm-fader-label\">CROSS FADE</div><input id=\"gv-avm-overlay-opacity\" aria-label=\"AVM cross fade\" type=\"range\" min=\"0\" max=\"100\" value=\"100\" dir=\"rtl\"></div>";
  document.body.appendChild(p);
  let style=document.getElementById("gv-avm-overlay-lab-style-0013");
  if(!style){
    style=document.createElement("style");
    style.id="gv-avm-overlay-lab-style-0013";
    style.textContent=[
      "#gv-avm-overlay-lab{position:fixed;left:0;top:102px;z-index:2147482000;width:102px;height:184px;transform:none;background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;pointer-events:none;display:none}",
      "#gv-avm-touch-shield{position:absolute;left:0;top:0;width:102px;height:184px;border-radius:21px;background:rgba(0,18,60,.10);pointer-events:auto;touch-action:none;user-select:none;-webkit-user-select:none;overscroll-behavior:contain}",
      "#gv-avm-fader-label{position:absolute;left:4px;top:50%;height:132px;transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;text-orientation:mixed;font:400 7px/1 \"Space Age\",sans-serif;letter-spacing:.85px;color:#68E0FF;text-shadow:0 0 7px rgba(104,224,255,.92),0 0 13px rgba(0,140,255,.58);pointer-events:none}",
      "#gv-avm-overlay-opacity{--gv-avm-pct:100%;-webkit-appearance:none;appearance:none;position:absolute;left:-34px;top:77px;width:148px;height:24px;margin:0;background:transparent!important;outline:none;display:block;transform:rotate(-90deg);transform-origin:center;direction:rtl;touch-action:none;pointer-events:auto}",
      "#gv-avm-overlay-opacity::-webkit-slider-runnable-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#0050B8 0%,#007BE8 50%,#32C7FF 80%,#9AF0FF 100%);box-shadow:0 0 8px rgba(104,224,255,.78),0 0 15px rgba(0,140,255,.52),inset 0 0 5px rgba(221,248,255,.34)}",
      "#gv-avm-overlay-opacity::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:19px;height:19px;border-radius:50%;background:#68E0FF;border:1px solid rgba(221,248,255,.98);margin-top:-5.5px;box-shadow:0 0 11px rgba(104,224,255,.96),0 0 21px rgba(0,140,255,.68)}",
      "#gv-avm-overlay-opacity::-moz-range-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#0050B8 0%,#007BE8 50%,#32C7FF 80%,#9AF0FF 100%);box-shadow:0 0 8px rgba(104,224,255,.78),0 0 15px rgba(0,140,255,.52),inset 0 0 5px rgba(221,248,255,.34)}",
      "#gv-avm-overlay-opacity::-moz-range-thumb{width:19px;height:19px;border-radius:50%;background:#68E0FF;border:1px solid rgba(221,248,255,.98);box-shadow:0 0 11px rgba(104,224,255,.96),0 0 21px rgba(0,140,255,.68)}",
      "#gv-avm-overlay-vignette{position:fixed;inset:0;z-index:6900;pointer-events:none;display:none;opacity:.92;background:radial-gradient(ellipse var(--gv-vig-x,76%) var(--gv-vig-y,76%) at center,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 48%,rgba(19,95,145,.12) 64%,rgba(5,18,42,.52) 100%)}",
      "#gv-avm-overlay-vignette[data-on=\"1\"]{display:block}",
      "#gv-avm-overlay-lab[data-on=\"1\"]{display:block}",
      "@media(max-height:720px){#gv-avm-overlay-lab{top:98px;width:98px;height:176px}#gv-avm-touch-shield{width:98px;height:176px}#gv-avm-fader-label{height:124px}#gv-avm-overlay-opacity{left:-32px;top:73px;width:142px}}",
      "@media(max-width:430px){#gv-avm-overlay-lab{left:0;top:102px;width:100px;height:182px}#gv-avm-touch-shield{width:100px;height:182px}#gv-avm-overlay-opacity{left:-33px;top:76px;width:146px}}"
    ].join("");
    document.head.appendChild(style);
  }
  return p;
}
function slider(){
  const p=panel();
  return p.querySelector("#gv-avm-overlay-opacity");
}

function opacityNow(){
  return clamp01(Number(slider().value)/100);
}

function paintSlider(){
  const sl=slider();
  const val=Math.max(0,Math.min(100,Number(sl.value)||0));
  sl.style.setProperty("--gv-avm-pct",val+"%");
}
function swallowPanelTouches(){
  const p=panel();
  if(p.dataset.gvTouchShield0013)return;
  p.dataset.gvTouchShield0013="1";
  const stop=e=>{
    try{e.stopPropagation()}catch(_){}
    try{
      const id=e.target&&e.target.id;
      if(id!=="gv-avm-overlay-opacity")e.preventDefault();
    }catch(_){}
  };
  for(const ev of ["pointerdown","pointermove","pointerup","pointercancel","touchstart","touchmove","touchend","touchcancel","mousedown","mousemove","mouseup","wheel","click"]){
    p.addEventListener(ev,stop,{capture:true,passive:false});
  }
}


function applyOpacity(){
  const op=opacityNow();
  paintSlider();
  try{overlay?.setOpacity?.(op)}catch(_){}
  try{overlay?.setAlpha?.(op)}catch(_){}
  try{overlay?.setOptions?.({opacity:op})}catch(_){}
}

function destinationStillCurrent(destination){
  const current=bestDestination(randomRef);
  if(!current)return false;
  const url=avmUrlFor(destination);
  return current.key===destinationKey(destination,url);
}

function applyExactImageFov(ra,dec,fov,destination,tag){
  const r=finite(ra), decv=finite(dec), sourceFov=finite(fov);
  if(r!==null && decv!==null){
    try{aladinRef.gotoRaDec?.(r,decv)}catch(_){}
  }
  const fit=fitFovFor(destination,sourceFov);
  applyVignetteFor(destination,fit);
  if(fit!==null && fit>0){
    try{
      if(typeof aladinRef.setFoV==="function")aladinRef.setFoV(fit*FOV_PAD);
      else aladinRef.setFov?.(fit*FOV_PAD);
    }catch(_){}
  }
}

function setExactImageFov(ra,dec,fov,destination){
  applyExactImageFov(ra,dec,fov,destination,"immediate");
  for(const ms of [160,420,900,1500,2600]){
    setTimeout(()=>{
      if(destinationStillCurrent(destination))applyExactImageFov(ra,dec,fov,destination,"delayed-"+ms);
    },ms);
  }
}

function useNativePreload(candidate,reason){
  const {d,url,key}=candidate;
  const ready=nativePreloadReady.get(key);
  if(!ready)return false;
  try{
    overlay=ready.overlay;
    if(!overlay)return false;
    if(typeof aladinRef.setOverlayImageLayer!=="function")return false;
    aladinRef.setOverlayImageLayer(overlay,LAYER_NAME);
    applyOpacity();
    setExactImageFov(ready.ra,ready.dec,ready.fov,d);
    lastKey=key;
    loadingKey="";
    setPanelVisible(true);
    lastContext={version:VERSION,mode:"native-avm-preload-hit",reason,destination:d,url,opacity:opacityNow(),ra:ready.ra,dec:ready.dec,fov:ready.fov,image:ready.image,overlay};
    global.GalaxyViewerAvmOverlayLab.lastContext=lastContext;
    console.info("GV AVM LAB 0013 NATIVE PRELOAD HIT",lastContext);
    return true;
  }catch(error){
    console.warn("GV AVM LAB 0013 NATIVE PRELOAD USE FAILED",{reason,key,url,error});
    return false;
  }
}

function loadForBestDestination(reason){
  installTravelButtonGuard();
  swallowPanelTouches();
  preloadUpcoming(reason);

  const candidate=bestDestination(randomRef);
  if(!candidate)return false;

  const {d,url,key}=candidate;
  if(suppressed()){
    if(Date.now()<travelMinUntil)return false;
    if(travelOldKey && key===travelOldKey)return false;
    suppressUntil=0;
    travelOldKey="";
    travelMinUntil=0;
  }

  if(!key)return false;
  if(key===lastKey){
    setPanelVisible(true);
    applyOpacity();
    return true;
  }
  if(key===loadingKey)return true;

  if(useNativePreload(candidate,reason))return true;

  loadingKey=key;

  try{
    const op=opacityNow();

    overlay=ARef.image(url,{
      name:LAYER_NAME,
      imgFormat:/\.png(?:[?#]|$)/i.test(url)?"png":"jpeg",
      opacity:op,
      successCallback:(ra,dec,fov,image)=>{
        setExactImageFov(ra,dec,fov,d);
        lastKey=key;
        loadingKey="";
        setPanelVisible(true);
        lastContext={version:VERSION,mode:"native-avm-direct-load",reason,destination:d,url,opacity:opacityNow(),ra,dec,fov,image,overlay};
        global.GalaxyViewerAvmOverlayLab.lastContext=lastContext;
        console.info("GV AVM LAB 0013 AUTO LOADED",lastContext);
      },
      errorCallback:(error)=>{
        loadingKey="";
        console.warn("GV AVM LAB 0013 IMAGE LOAD FAILED",{reason,key,url,error});
      }
    });

    if(!overlay)throw new Error("A.image returned empty overlay");
    if(typeof aladinRef.setOverlayImageLayer!=="function")throw new Error("ALADIN setOverlayImageLayer unavailable");

    aladinRef.setOverlayImageLayer(overlay,LAYER_NAME);
    applyOpacity();

    return true;
  }catch(e){
    loadingKey="";
    console.error("GV AVM LAB 0013 FAILED",e);
    return false;
  }
}
function install({A,aladin,viewerRoot,randomGalaxy}={}){
  if(!A)throw new Error("ALADIN A NAMESPACE MISSING");
  if(!aladin)throw new Error("ALADIN INSTANCE MISSING");
  if(!viewerRoot)throw new Error("VIEWER ROOT MISSING");

  ARef=A;
  aladinRef=aladin;
  randomRef=randomGalaxy;
  rootRef=viewerRoot;

  ensureVignette();
  setPanelVisible(false);
  swallowPanelTouches();
  installTravelButtonGuard();
  preloadUpcoming("install");

  if(!global.__gvAvmNativePreloadInterval0013){
    global.__gvAvmNativePreloadInterval0013=setInterval(()=>preloadUpcoming("background"),700);
  }

  const sl=slider();
  paintSlider();
  sl.addEventListener("input",applyOpacity);
  sl.addEventListener("change",applyOpacity);
  if(watchTimer)clearInterval(watchTimer);
  watchTimer=setInterval(()=>loadForBestDestination("watch"),WATCH_MS);

  loadForBestDestination("install");
  setTimeout(()=>loadForBestDestination("install-delay-1"),180);
  setTimeout(()=>loadForBestDestination("install-delay-2"),450);
  setTimeout(()=>loadForBestDestination("install-delay-3"),900);

  global.GalaxyViewerAvmOverlayLab.instance={
    panel:panel(),
    slider:sl,
    load:()=>loadForBestDestination("manual-api"),
    preload:()=>preloadUpcoming("manual-api"),
    get last(){return lastContext},
    get preloadReady(){return nativePreloadReady.size},
    get preloadLoading(){return nativePreloadLoading.size}
  };
  console.info("GV AVM LAB INSTALLED",VERSION);
}

global.GalaxyViewerAvmOverlayLab={
  VERSION,
  install,
  load:()=>loadForBestDestination("public-api"),
  preload:()=>preloadUpcoming("public-api"),
  get last(){return lastContext},
  get overlay(){return overlay},
  get preloadReady(){return nativePreloadReady.size},
  get preloadLoading(){return nativePreloadLoading.size}
};
})(window);
