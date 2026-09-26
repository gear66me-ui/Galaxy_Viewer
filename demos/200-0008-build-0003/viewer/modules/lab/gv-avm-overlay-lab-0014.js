"use strict";
(function(global){
const VERSION="0014";
const LAYER_NAME="Galaxy Viewer AVM Overlay";
const WATCH_MS=140;
const FOV_PAD=1.0;
const PRELOAD_LIMIT=12;
const CACHE_LIMIT=36;

let aladinRef=null;
let ARef=null;
let randomRef=null;
let rootRef=null;
let overlay=null;
let watchTimer=null;
let lastKey="";
let loadingKey="";
let lastContext=null;
let panelEverEnabled=false;
let travelOldKey="";
let travelMinUntil=0;
let suppressUntil=0;
let preloadTimer=0;

const processedReady=new Map();
const processing=new Set();
const keepAlive=[];

function finite(v){v=Number(v);return Number.isFinite(v)?v:null}
function stateOf(r){try{return r?.getState?.()||{}}catch(_){return {}}}
function destinationKey(d,url){return String(d?.archiveId||d?.id||d?.name||d?.title||url||"").trim()}
function avmUrlFor(d){
  if(!d)return "";
  return String(
    d.avmImageUrl||d.aladinImageUrl||d.selectedImageUrl||d.screenUrl||d.imageUrl||d.url||d.hdUrl||d.largeUrl||""
  ).trim();
}
function isUsableAvmDestination(d,url){
  url=String(url||avmUrlFor(d)||"").trim();
  return !!(d&&url&&/^https?:\/\//i.test(url)&&/\.(?:jpg|jpeg|png)(?:[?#]|$)/i.test(url));
}
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
  if(src.x!==null&&src.y!==null&&va>0)f=Math.max(src.x,src.y*va,f||0);
  return finite(f);
}

function injectStyle(){
  if(document.getElementById("gv-avm-overlay-lab-style-0014"))return;
  const style=document.createElement("style");
  style.id="gv-avm-overlay-lab-style-0014";
  style.textContent=[
    "#gv-avm-overlay-lab{position:fixed;left:0;top:172px;z-index:7200;width:96px;height:164px;transform:none;background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;pointer-events:none;display:none}",
    "#gv-avm-touch-shield{position:absolute;left:0;top:0;width:96px;height:164px;border-radius:18px;background:rgba(0,18,60,.09);pointer-events:auto;touch-action:none;user-select:none;-webkit-user-select:none;overscroll-behavior:contain}",
    "#gv-avm-fader-label{position:absolute;left:4px;top:50%;height:118px;transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;text-orientation:mixed;font:400 7px/1 \"Space Age\",sans-serif;letter-spacing:.75px;color:#6DE2FF;text-shadow:0 0 7px rgba(109,226,255,.88),0 0 12px rgba(0,146,255,.52);pointer-events:none}",
    "#gv-avm-overlay-opacity{--gv-avm-pct:100%;-webkit-appearance:none;appearance:none;position:absolute;left:-33px;top:70px;width:130px;height:24px;margin:0;background:transparent!important;outline:none;display:block;transform:rotate(-90deg);transform-origin:center;direction:rtl;touch-action:none;pointer-events:auto}",
    "#gv-avm-overlay-opacity::-webkit-slider-runnable-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#0050B8 0%,#007BE8 48%,#32C7FF 80%,#9AF0FF 100%);box-shadow:0 0 8px rgba(109,226,255,.75),0 0 14px rgba(0,146,255,.48),inset 0 0 5px rgba(221,248,255,.30)}",
    "#gv-avm-overlay-opacity::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:18px;height:18px;border-radius:50%;background:#6DE2FF;border:1px solid rgba(221,248,255,.98);margin-top:-5px;box-shadow:0 0 10px rgba(109,226,255,.95),0 0 19px rgba(0,146,255,.64)}",
    "#gv-avm-overlay-opacity::-moz-range-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#0050B8 0%,#007BE8 48%,#32C7FF 80%,#9AF0FF 100%);box-shadow:0 0 8px rgba(109,226,255,.75),0 0 14px rgba(0,146,255,.48),inset 0 0 5px rgba(221,248,255,.30)}",
    "#gv-avm-overlay-opacity::-moz-range-thumb{width:18px;height:18px;border-radius:50%;background:#6DE2FF;border:1px solid rgba(221,248,255,.98);box-shadow:0 0 10px rgba(109,226,255,.95),0 0 19px rgba(0,146,255,.64)}",
    "#gv-avm-overlay-lab[data-on=\"1\"]{display:block}",
    "@media(max-height:720px){#gv-avm-overlay-lab{top:158px;width:92px;height:150px}#gv-avm-touch-shield{width:92px;height:150px}#gv-avm-fader-label{height:106px}#gv-avm-overlay-opacity{left:-30px;top:63px;width:118px}}",
    "@media(max-width:430px){#gv-avm-overlay-lab{left:0;top:164px;width:94px;height:156px}#gv-avm-touch-shield{width:94px;height:156px}#gv-avm-overlay-opacity{left:-31px;top:66px;width:124px}}"
  ].join("");
  document.head.appendChild(style);
}
function panel(){
  injectStyle();
  let p=document.getElementById("gv-avm-overlay-lab");
  if(p)return p;
  p=document.createElement("div");
  p.id="gv-avm-overlay-lab";
  p.innerHTML="<div id=\"gv-avm-touch-shield\"><div id=\"gv-avm-fader-label\">CROSS FADE</div><input id=\"gv-avm-overlay-opacity\" aria-label=\"AVM cross fade\" type=\"range\" min=\"0\" max=\"100\" value=\"100\" dir=\"rtl\"></div>";
  document.body.appendChild(p);
  return p;
}
function slider(){
  const p=panel();
  let sl=p.querySelector("#gv-avm-overlay-opacity");
  if(!sl)throw new Error("AVM opacity slider missing");
  return sl;
}
function opacityNow(){return Math.max(0,Math.min(1,(Number(slider().value)||0)/100))}
function paintSlider(){
  const sl=slider();
  const val=Math.max(0,Math.min(100,Number(sl.value)||0));
  sl.style.setProperty("--gv-avm-pct",val+"%");
}
function setPanelVisible(on){
  try{
    const p=panel();
    if(on)panelEverEnabled=true;
    p.dataset.on=panelEverEnabled?"1":"0";
  }catch(_){}
}
function swallowPanelTouches(){
  const p=panel();
  if(p.dataset.gvTouchShield0014)return;
  p.dataset.gvTouchShield0014="1";
  const stop=e=>{
    try{e.stopPropagation()}catch(_){}
    try{if((e.target&&e.target.id)!=="gv-avm-overlay-opacity")e.preventDefault()}catch(_){}
  };
  for(const ev of ["pointerdown","pointermove","pointerup","pointercancel","touchstart","touchmove","touchend","touchcancel","mousedown","mousemove","mouseup","wheel","click"]){
    p.addEventListener(ev,stop,{capture:true,passive:false});
  }
}
function applyOpacity(){
  let op=opacityNow();
  paintSlider();
  try{overlay?.setOpacity?.(op)}catch(_){}
  try{overlay?.setAlpha?.(op)}catch(_){}
  try{overlay?.setOptions?.({opacity:op})}catch(_){}
}

function addCandidate(out,item){
  if(!item)return;
  const d=item.destination||item.record||item;
  const url=avmUrlFor(d);
  if(isUsableAvmDestination(d,url))out.push(d);
}
function collectCandidatesFrom(root,out,seen,depth){
  if(!root||depth>5||typeof root!=="object")return;
  if(seen.has(root))return;
  seen.add(root);
  addCandidate(out,root);
  if(Array.isArray(root)){
    for(const x of root)collectCandidatesFrom(x,out,seen,depth+1);
    return;
  }
  for(const key of ["future","queue","route","navigationQueue","preparedQueue","prefetchReady","prefetchQueued","activePreparedItem","historyPreparedItems","destination","record"]){
    if(root[key])collectCandidatesFrom(root[key],out,seen,depth+1);
  }
}
function liveCandidates(randomGalaxy){
  const s=stateOf(randomGalaxy);
  const g=global.GalaxyRandomGalaxy||{};
  const out=[];
  for(const d of [
    s.activeDestination,
    s.currentDestination,
    randomGalaxy?.activeDestination,
    randomGalaxy?.currentDestination,
    g.activeDestination,
    g.currentDestination
  ])addCandidate(out,d);
  return out;
}
function upcomingCandidates(randomGalaxy){
  const s=stateOf(randomGalaxy);
  const g=global.GalaxyRandomGalaxy||{};
  const out=[];
  const seen=new WeakSet();
  collectCandidatesFrom(s,out,seen,0);
  collectCandidatesFrom(g,out,seen,0);
  for(const key of ["future","queue","route","navigationQueue","preparedQueue","prefetchReady","prefetchQueued","activePreparedItem","historyPreparedItems"]){
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
function bestDestination(randomGalaxy){
  for(const d of liveCandidates(randomGalaxy)){
    const url=avmUrlFor(d);
    if(isUsableAvmDestination(d,url))return {d,url,key:destinationKey(d,url)};
  }
  return null;
}
function suppressed(){return Date.now()<suppressUntil}

async function fetchImageBlob(url){
  const res=await fetch(url,{mode:"cors",cache:"force-cache",credentials:"omit"});
  if(!res.ok)throw new Error("fetch image failed "+res.status);
  return await res.blob();
}
function loadHtmlImage(src){
  return new Promise((resolve,reject)=>{
    const img=new Image();
    img.crossOrigin="anonymous";
    img.decoding="async";
    img.onload=()=>resolve(img);
    img.onerror=()=>reject(new Error("image decode failed"));
    img.src=src;
  });
}
async function createVignettedUrl(url,key,reason){
  const blob=await fetchImageBlob(url);
  const rawUrl=URL.createObjectURL(blob);
  let img=null;
  try{img=await loadHtmlImage(rawUrl)}finally{try{URL.revokeObjectURL(rawUrl)}catch(_){}}
  const w=img.naturalWidth||img.width;
  const h=img.naturalHeight||img.height;
  if(!(w>0&&h>0))throw new Error("invalid image size");
  const canvas=document.createElement("canvas");
  canvas.width=w;
  canvas.height=h;
  const ctx=canvas.getContext("2d");
  ctx.drawImage(img,0,0,w,h);
  const g=ctx.createRadialGradient(w/2,h/2,Math.min(w,h)*0.12,w/2,h/2,Math.max(w,h)*0.68);
  g.addColorStop(0,"rgba(0,0,0,0)");
  g.addColorStop(0.55,"rgba(0,0,0,0)");
  g.addColorStop(0.78,"rgba(3,14,36,0.18)");
  g.addColorStop(1,"rgba(0,3,14,0.58)");
  ctx.globalCompositeOperation="source-over";
  ctx.fillStyle=g;
  ctx.fillRect(0,0,w,h);
  const outBlob=await new Promise(resolve=>canvas.toBlob(resolve,"image/jpeg",0.92));
  if(!outBlob)throw new Error("canvas toBlob failed");
  const processedUrl=URL.createObjectURL(outBlob);
  return {url:processedUrl,originalUrl:url,key,width:w,height:h,reason,createdAt:Date.now()};
}
function browserPreloadUrl(url){
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
  if(keepAlive.length>90)keepAlive.splice(0,keepAlive.length-90);
}
function trimProcessedCache(){
  while(processedReady.size>CACHE_LIMIT){
    const first=processedReady.keys().next().value;
    const item=processedReady.get(first);
    try{if(item?.url?.startsWith("blob:"))URL.revokeObjectURL(item.url)}catch(_){}
    processedReady.delete(first);
  }
}
function preloadProcessedImage(d,reason){
  const url=avmUrlFor(d);
  const key=destinationKey(d,url);
  if(!key||!isUsableAvmDestination(d,url))return false;
  browserPreloadUrl(url);
  if(processedReady.has(key)||processing.has(key))return false;
  processing.add(key);
  createVignettedUrl(url,key,reason).then(item=>{
    processing.delete(key);
    processedReady.set(key,item);
    trimProcessedCache();
    try{console.info("GV AVM LAB 0014 IMAGE VIGNETTE PRELOAD READY",{reason,key,name:d?.name,archiveId:d?.archiveId,url,width:item.width,height:item.height})}catch(_){}
  }).catch(error=>{
    processing.delete(key);
    try{console.warn("GV AVM LAB 0014 IMAGE VIGNETTE PRELOAD FAILED",{reason,key,url,error})}catch(_){}
  });
  return true;
}
function preloadUpcoming(reason){
  let count=0;
  for(const d of upcomingCandidates(randomRef)){
    if(preloadProcessedImage(d,reason))count++;
    if(count>=PRELOAD_LIMIT)break;
  }
  if(count){try{console.info("GV AVM LAB 0014 PRELOAD STARTED",{reason,count})}catch(_){}}
}

function hideOverlayForTravel(){
  preloadUpcoming("travel-button");
  travelOldKey=lastKey||loadingKey||"";
  travelMinUntil=Date.now()+350;
  suppressUntil=Math.max(suppressUntil,Date.now()+26000);
  loadingKey="";
  lastKey="";
  setPanelVisible(false);
  try{overlay?.setOpacity?.(0)}catch(_){}
  try{overlay?.setAlpha?.(0)}catch(_){}
  try{overlay?.setOptions?.({opacity:0})}catch(_){}
  for(const ms of [250,500,850,1200,1700,2400,3400,4800,6600,8800,11200,14000,17200,20800,24400]){
    setTimeout(()=>loadForBestDestination("travel-poll-"+ms),ms);
  }
}
function installTravelButtonGuard(){
  const buttons=document.querySelectorAll("#gv-random-galaxy,.gv-galaxy-history");
  for(const b of buttons){
    if(!b||b.dataset.gvAvmGuard0014)continue;
    b.dataset.gvAvmGuard0014="1";
    for(const ev of ["pointerdown","touchstart","click"]){
      b.addEventListener(ev,hideOverlayForTravel,{capture:true,passive:true});
    }
  }
}
function applyExactImageFov(ra,dec,fov,destination,tag){
  const r=finite(ra), decv=finite(dec), sourceFov=finite(fov);
  if(r!==null&&decv!==null){try{aladinRef.gotoRaDec?.(r,decv)}catch(_){}}
  const fit=fitFovFor(destination,sourceFov);
  if(fit!==null&&fit>0){
    try{
      if(typeof aladinRef.setFoV==="function")aladinRef.setFoV(fit*FOV_PAD);
      else aladinRef.setFov?.(fit*FOV_PAD);
    }catch(_){}
    try{console.info("GV AVM LAB 0014 FOV FIT",{tag,fit,sourceFov,imageFovDeg:destination?.imageFovDeg,imageFovXDeg:destination?.imageFovXDeg,imageFovYDeg:destination?.imageFovYDeg,name:destination?.name,archiveId:destination?.archiveId})}catch(_){}
  }
}
function destinationStillCurrent(destination){
  const current=bestDestination(randomRef);
  if(!current)return false;
  const url=avmUrlFor(destination);
  return current.key===destinationKey(destination,url);
}
function setExactImageFov(ra,dec,fov,destination){
  applyExactImageFov(ra,dec,fov,destination,"immediate");
  for(const ms of [160,420,900,1500,2600]){
    setTimeout(()=>{if(destinationStillCurrent(destination))applyExactImageFov(ra,dec,fov,destination,"delayed-"+ms)},ms);
  }
}
function chooseDisplayUrl(candidate){
  const ready=processedReady.get(candidate.key);
  if(ready?.url)return {url:ready.url,source:"processed-vignette",ready};
  return {url:candidate.url,source:"original",ready:null};
}
function loadForBestDestination(reason){
  installTravelButtonGuard();
  swallowPanelTouches();
  preloadUpcoming(reason);
  const candidate=bestDestination(randomRef);
  if(!candidate)return false;
  const {d,key}=candidate;
  if(suppressed()){
    if(Date.now()<travelMinUntil)return false;
    if(travelOldKey&&key===travelOldKey)return false;
    suppressUntil=0;
    travelOldKey="";
    travelMinUntil=0;
  }
  if(!key)return false;
  if(key===lastKey){setPanelVisible(true);return true}
  if(key===loadingKey)return true;

  const chosen=chooseDisplayUrl(candidate);
  const url=chosen.url;
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
        lastContext={version:VERSION,mode:chosen.source,reason,destination:d,url,originalUrl:candidate.url,opacity:opacityNow(),ra,dec,fov,image,overlay};
        global.GalaxyViewerAvmOverlayLab.lastContext=lastContext;
        console.info("GV AVM LAB 0014 AUTO LOADED",lastContext);
      },
      errorCallback:(error)=>{
        loadingKey="";
        console.warn("GV AVM LAB 0014 IMAGE LOAD FAILED",{reason,key,url,source:chosen.source,error});
        if(chosen.source!=="original"){
          processedReady.delete(key);
          setTimeout(()=>loadForBestDestination("fallback-original"),30);
        }
      }
    });
    if(!overlay)throw new Error("A.image returned empty overlay");
    if(typeof aladinRef.setOverlayImageLayer!=="function")throw new Error("ALADIN setOverlayImageLayer unavailable");
    aladinRef.setOverlayImageLayer(overlay,LAYER_NAME);
    applyOpacity();
    return true;
  }catch(e){
    loadingKey="";
    console.error("GV AVM LAB 0014 FAILED",e);
    return false;
  }
}
function install({aladin,A,randomGalaxy,viewerRoot}={}){
  aladinRef=aladin||global.aladin||global.Aladin;
  ARef=A||global.A;
  randomRef=randomGalaxy||global.GalaxyRandomGalaxy;
  rootRef=viewerRoot||document.body;
  if(!aladinRef||!ARef)return false;
  panel();
  setPanelVisible(false);
  swallowPanelTouches();
  installTravelButtonGuard();
  slider().addEventListener("input",applyOpacity,{passive:true});
  applyOpacity();
  preloadUpcoming("install");
  if(!preloadTimer)preloadTimer=setInterval(()=>preloadUpcoming("background"),700);
  if(!watchTimer)watchTimer=setInterval(()=>loadForBestDestination("watch"),WATCH_MS);
  loadForBestDestination("install");
  console.info("GV AVM LAB 0014 INSTALLED",{version:VERSION});
  return true;
}
function uninstall(){
  if(watchTimer){clearInterval(watchTimer);watchTimer=null}
  if(preloadTimer){clearInterval(preloadTimer);preloadTimer=0}
  for(const item of processedReady.values()){try{if(item?.url?.startsWith("blob:"))URL.revokeObjectURL(item.url)}catch(_){}}
  processedReady.clear();
}

global.GalaxyViewerAvmOverlayLab={VERSION,install,uninstall,loadForBestDestination,preloadUpcoming,get lastContext(){return lastContext},get cacheSize(){return processedReady.size}};
})(window);
