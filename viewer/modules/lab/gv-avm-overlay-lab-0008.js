(function(global){
"use strict";
const VERSION="0008";
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

function candidatesFromState(randomGalaxy){
  const s=stateOf(randomGalaxy);
  const g=global.GalaxyRandomGalaxy||{};
  const list=[
    s.travelDestination,
    s.pendingDestination,
    s.nextDestination,
    s.preparedDestination,
    s.activeDestination,
    s.destination,
    s.currentDestination,
    randomGalaxy?.travelDestination,
    randomGalaxy?.pendingDestination,
    randomGalaxy?.nextDestination,
    randomGalaxy?.preparedDestination,
    randomGalaxy?.activeDestination,
    randomGalaxy?.currentDestination,
    g.travelDestination,
    g.pendingDestination,
    g.nextDestination,
    g.preparedDestination,
    g.activeDestination,
    g.currentDestination
  ];
  for(const key of ["future","queue","history","route","navigationQueue","preparedQueue"]){
    const arr=s?.[key]||randomGalaxy?.[key]||g?.[key];
    if(Array.isArray(arr)){
      for(const x of arr){
        list.push(x?.destination||x);
      }
    }
  }
  return list.filter(Boolean);
}

function bestDestination(randomGalaxy){
  for(const d of candidatesFromState(randomGalaxy)){
    const url=avmUrlFor(d);
    if(isUsableAvmDestination(d,url))return {d,url,key:destinationKey(d,url)};
  }
  return null;
}

function panel(){
  let p=document.getElementById("gv-avm-overlay-lab");
  if(p)return p;
  p=document.createElement("div");
  p.id="gv-avm-overlay-lab";
  p.innerHTML="<input id=\"gv-avm-overlay-opacity\" aria-label=\"AVM opacity\" type=\"range\" min=\"0\" max=\"100\" value=\"100\">";
  document.body.appendChild(p);

  let s=document.getElementById("gv-avm-overlay-lab-style-0008");
  if(!s){
    s=document.createElement("style");
    s.id="gv-avm-overlay-lab-style-0008";
    s.textContent=[
      "#gv-avm-overlay-lab{position:fixed;right:24px;top:calc(50% + 205px);z-index:2147482000;width:min(220px,42vw);height:20px;background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;pointer-events:auto}",
      "#gv-avm-overlay-opacity{--gv-avm-pct:100%;-webkit-appearance:none;appearance:none;width:100%;height:20px;margin:0;background:transparent!important;outline:none;display:block}",
      "#gv-avm-overlay-opacity::-webkit-slider-runnable-track{height:6px;border-radius:999px;background:linear-gradient(90deg,#78FFAB 0 var(--gv-avm-pct),rgba(255,255,255,.30) var(--gv-avm-pct) 100%);box-shadow:0 0 7px rgba(120,255,171,.70)}",
      "#gv-avm-overlay-opacity::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:16px;height:16px;border-radius:50%;background:#78FFAB;border:1px solid rgba(230,255,242,.95);margin-top:-5px;box-shadow:0 0 9px rgba(120,255,171,.95)}",
      "#gv-avm-overlay-opacity::-moz-range-track{height:6px;border-radius:999px;background:#78FFAB;box-shadow:0 0 7px rgba(120,255,171,.70)}",
      "#gv-avm-overlay-opacity::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:#78FFAB;border:1px solid rgba(230,255,242,.95);box-shadow:0 0 9px rgba(120,255,171,.95)}",
      "#gv-avm-overlay-vignette{position:absolute;inset:0;z-index:6900;pointer-events:none;display:none;opacity:.86;background:radial-gradient(ellipse var(--gv-vig-x,74%) var(--gv-vig-y,74%) at center,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 54%,rgba(5,18,42,.16) 70%,rgba(2,8,25,.58) 100%)}",
      "#gv-avm-overlay-vignette[data-on=\"1\"]{display:block}",
      "@media(max-height:720px){#gv-avm-overlay-lab{top:auto;bottom:170px}}",
      "@media(max-width:430px){#gv-avm-overlay-lab{right:18px;top:calc(50% + 190px);width:min(205px,44vw)}}"
    ].join("");
    document.head.appendChild(s);
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

function applyOpacity(){
  const op=opacityNow();
  paintSlider();
  try{overlay?.setOpacity?.(op)}catch(_){}
  try{overlay?.setAlpha?.(op)}catch(_){}
  try{overlay?.setOptions?.({opacity:op})}catch(_){}
}

function setExactImageFov(ra,dec,fov,destination){
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
function loadForBestDestination(reason){
  const candidate=bestDestination(randomRef);
  if(!candidate)return false;

  const {d,url,key}=candidate;
  if(!key || key===lastKey || key===loadingKey)return true;

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
        lastContext={version:VERSION,mode:"auto-native-avm-image-fov",reason,destination:d,url,opacity:opacityNow(),ra,dec,fov,image,overlay};
        global.GalaxyViewerAvmOverlayLab.lastContext=lastContext;
        console.info("GV AVM LAB 0008 AUTO LOADED",lastContext);
      },
      errorCallback:(error)=>{
        loadingKey="";
        console.warn("GV AVM LAB 0008 IMAGE LOAD FAILED",{reason,key,url,error});
      }
    });

    if(!overlay)throw new Error("A.image returned empty overlay");
    if(typeof aladinRef.setOverlayImageLayer!=="function")throw new Error("ALADIN setOverlayImageLayer unavailable");

    aladinRef.setOverlayImageLayer(overlay,LAYER_NAME);
    applyOpacity();

    return true;
  }catch(e){
    loadingKey="";
    console.error("GV AVM LAB 0008 FAILED",e);
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

  const sl=slider();
  paintSlider();
  sl.addEventListener("input",applyOpacity);
  sl.addEventListener("change",applyOpacity);

  if(watchTimer)clearInterval(watchTimer);
  watchTimer=setInterval(()=>loadForBestDestination("watch"),WATCH_MS);

  // Try immediately, then shortly after boot/random state settles.
  loadForBestDestination("install");
  setTimeout(()=>loadForBestDestination("install-delay-1"),250);
  setTimeout(()=>loadForBestDestination("install-delay-2"),900);

  global.GalaxyViewerAvmOverlayLab.instance={panel:panel(),slider:sl,load:()=>loadForBestDestination("manual-api"),get last(){return lastContext}};
  console.info("GV AVM LAB INSTALLED",VERSION);
}

global.GalaxyViewerAvmOverlayLab={
  VERSION,
  install,
  load:()=>loadForBestDestination("public-api"),
  get last(){return lastContext},
  get overlay(){return overlay}
};
})(window);
