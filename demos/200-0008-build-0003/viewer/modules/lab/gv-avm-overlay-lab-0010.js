(function(global){
"use strict";
const VERSION="0010";
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
const preloadCache=new Set();
const preloadImages=[];

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

function upcomingCandidates(randomGalaxy){
  const s=stateOf(randomGalaxy);
  const g=global.GalaxyRandomGalaxy||{};
  const list=[
    s.travelDestination,
    s.pendingDestination,
    s.nextDestination,
    s.preparedDestination,
    randomGalaxy?.travelDestination,
    randomGalaxy?.pendingDestination,
    randomGalaxy?.nextDestination,
    randomGalaxy?.preparedDestination,
    g.travelDestination,
    g.pendingDestination,
    g.nextDestination,
    g.preparedDestination
  ];
  for(const key of ["future","queue","route","navigationQueue","preparedQueue"]){
    const arr=s?.[key]||randomGalaxy?.[key]||g?.[key];
    if(Array.isArray(arr)){
      for(const x of arr)list.push(x?.destination||x);
    }
  }
  return list.filter(Boolean);
}

function preloadUpcoming(reason){
  let count=0;
  for(const d of upcomingCandidates(randomRef)){
    const url=avmUrlFor(d);
    if(!isUsableAvmDestination(d,url))continue;
    if(preloadCache.has(url))continue;
    preloadCache.add(url);
    const img=new Image();
    img.decoding="async";
    img.loading="eager";
    img.src=url;
    preloadImages.push(img);
    if(preloadImages.length>24)preloadImages.splice(0,preloadImages.length-24);
    count++;
    if(count>=4)break;
  }
  if(count){
    try{console.info("GV AVM LAB 0010 PRELOADED",{reason,count})}catch(_){}
  }
}

function candidatesFromState(randomGalaxy){
  const s=stateOf(randomGalaxy);
  const g=global.GalaxyRandomGalaxy||{};
  const list=[
    s.activeDestination,
    s.currentDestination,
    randomGalaxy?.activeDestination,
    randomGalaxy?.currentDestination,
    g.activeDestination,
    g.currentDestination
  ];
  return list.filter(Boolean);
}

function suppressed(){
  return Date.now()<suppressUntil;
}

function hideVignette(){
  try{
    if(vignette)vignette.dataset.on="0";
    setPanelVisible(false);
  }catch(_){}
}

function hideOverlayForTravel(){
  preloadUpcoming("travel-button");
  suppressUntil=Math.max(suppressUntil,Date.now()+19000);
  loadingKey="";
  lastKey="";
  hideVignette();
  try{overlay?.setOpacity?.(0)}catch(_){}
  try{overlay?.setAlpha?.(0)}catch(_){}
  try{overlay?.setOptions?.({opacity:0})}catch(_){}
  setTimeout(()=>{
    suppressUntil=0;
    loadForBestDestination("post-travel-release");
  },19050);
}

function installTravelButtonGuard(){
  const buttons=document.querySelectorAll("#gv-random-galaxy,.gv-galaxy-history");
  for(const b of buttons){
    if(!b||b.dataset.gvAvmGuard0010)continue;
    b.dataset.gvAvmGuard0010="1";
    for(const ev of ["pointerdown","touchstart","click"]){
      b.addEventListener(ev,hideOverlayForTravel,{capture:true,passive:true});
    }
  }
}

function bestDestination(randomGalaxy){
  if(suppressed())return null;
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
  p.innerHTML="<div id=\"gv-avm-touch-shield\"><div id=\"gv-avm-fader-label\">CROSS FADE</div><input id=\"gv-avm-overlay-opacity\" aria-label=\"AVM cross fade\" type=\"range\" min=\"0\" max=\"100\" value=\"100\" dir=\"rtl\"></div>";
  document.body.appendChild(p);

  let s=document.getElementById("gv-avm-overlay-lab-style-0010");
  if(!s){
    s=document.createElement("style");
    s.id="gv-avm-overlay-lab-style-0010";
    s.textContent=[
      "#gv-avm-overlay-lab{position:fixed;left:50%;right:auto;top:auto;bottom:clamp(220px,32vh,430px);z-index:2147482000;width:min(260px,58vw);height:22px;transform:translateX(-50%);background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;pointer-events:auto}",
      "#gv-avm-overlay-opacity{--gv-avm-pct:100%;-webkit-appearance:none;appearance:none;width:100%;height:20px;margin:0;background:transparent!important;outline:none;display:block}",
      "#gv-avm-overlay-opacity::-webkit-slider-runnable-track{height:6px;border-radius:999px;background:linear-gradient(90deg,#DDF8FF 0%,#9BE5FF var(--gv-avm-pct),rgba(104,198,255,.25) var(--gv-avm-pct),rgba(255,255,255,.18) 100%);box-shadow:0 0 8px rgba(155,229,255,.74),0 0 14px rgba(88,191,255,.42)}",
      "#gv-avm-overlay-opacity::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:16px;height:16px;border-radius:50%;background:#DDF8FF;border:1px solid rgba(235,251,255,.98);margin-top:-5px;box-shadow:0 0 10px rgba(155,229,255,.95),0 0 18px rgba(88,191,255,.62)}",
      "#gv-avm-overlay-opacity::-moz-range-track{height:6px;border-radius:999px;background:#9BE5FF;box-shadow:0 0 8px rgba(155,229,255,.74),0 0 14px rgba(88,191,255,.42)}",
      "#gv-avm-overlay-opacity::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:#DDF8FF;border:1px solid rgba(235,251,255,.98);box-shadow:0 0 10px rgba(155,229,255,.95),0 0 18px rgba(88,191,255,.62)}",
      "#gv-avm-overlay-vignette{position:fixed;inset:0;z-index:6900;pointer-events:none;display:none;opacity:.92;background:radial-gradient(ellipse var(--gv-vig-x,76%) var(--gv-vig-y,76%) at center,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 48%,rgba(19,95,145,.12) 64%,rgba(5,18,42,.52) 100%)}",
      "#gv-avm-overlay-vignette[data-on=\"1\"]{display:block}",
      "@media(max-height:720px){#gv-avm-overlay-lab{bottom:235px;width:min(250px,62vw)}}",
      "@media(max-width:430px){#gv-avm-overlay-lab{left:50%;right:auto;top:auto;bottom:235px;width:min(250px,62vw)}}",
      "#gv-avm-overlay-lab{position:fixed;left:2px;top:50%;z-index:2147482000;width:118px;height:340px;transform:translateY(-50%);background:transparent!important;border:0!important;box-shadow:none!important;padding:0!important;margin:0!important;pointer-events:none;display:none}",
      "#gv-avm-touch-shield{position:absolute;left:0;top:0;width:118px;height:340px;border-radius:24px;background:rgba(0,35,96,.13);pointer-events:auto;touch-action:none;user-select:none;-webkit-user-select:none;overscroll-behavior:contain}",
      "#gv-avm-fader-label{position:absolute;left:7px;top:50%;height:210px;transform:translateY(-50%) rotate(180deg);writing-mode:vertical-rl;text-orientation:mixed;font:400 8px/1 \"Space Age\",sans-serif;letter-spacing:.95px;color:#32C7FF;text-shadow:0 0 7px rgba(50,199,255,.95),0 0 14px rgba(0,120,232,.68);pointer-events:none}",
      "#gv-avm-overlay-opacity{--gv-avm-pct:100%;-webkit-appearance:none;appearance:none;position:absolute;left:-29px;top:158px;width:250px;height:24px;margin:0;background:transparent!important;outline:none;display:block;transform:rotate(-90deg);transform-origin:center;direction:rtl;touch-action:none;pointer-events:auto}",
      "#gv-avm-overlay-opacity::-webkit-slider-runnable-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#002C78 0%,#004DAD 38%,#0078E8 68%,#32C7FF 100%);box-shadow:0 0 8px rgba(50,199,255,.82),0 0 17px rgba(0,120,232,.58),inset 0 0 5px rgba(221,248,255,.34)}",
      "#gv-avm-overlay-opacity::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:20px;height:20px;border-radius:50%;background:#32C7FF;border:1px solid rgba(221,248,255,.98);margin-top:-6px;box-shadow:0 0 11px rgba(50,199,255,.98),0 0 22px rgba(0,120,232,.72)}",
      "#gv-avm-overlay-opacity::-moz-range-track{height:8px;border-radius:999px;background:linear-gradient(90deg,#002C78 0%,#004DAD 38%,#0078E8 68%,#32C7FF 100%);box-shadow:0 0 8px rgba(50,199,255,.82),0 0 17px rgba(0,120,232,.58),inset 0 0 5px rgba(221,248,255,.34)}",
      "#gv-avm-overlay-opacity::-moz-range-thumb{width:20px;height:20px;border-radius:50%;background:#32C7FF;border:1px solid rgba(221,248,255,.98);box-shadow:0 0 11px rgba(50,199,255,.98),0 0 22px rgba(0,120,232,.72)}",
      "#gv-avm-overlay-lab[data-on=\"1\"]{display:block}",
      "@media(max-height:720px){#gv-avm-overlay-lab{height:295px}#gv-avm-touch-shield{height:295px}#gv-avm-overlay-opacity{left:-15px;top:136px;width:220px}}",
      "@media(max-width:430px){#gv-avm-overlay-lab{left:1px;width:112px;height:318px}#gv-avm-touch-shield{width:112px;height:318px}#gv-avm-overlay-opacity{left:-23px;top:148px;width:238px}}",
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
function setPanelVisible(on){
  try{
    const p=panel();
    if(on)panelEverEnabled=true;
    const show=panelEverEnabled?true:!!on;
    p.dataset.on=show?"1":"0";
  }catch(_){}
}

function swallowPanelTouches(){
  const p=panel();
  if(p.dataset.gvTouchShield0010)return;
  p.dataset.gvTouchShield0010="1";
  const stop=e=>{
    try{e.stopPropagation()}catch(_){}
    try{
      const id=e.target&&e.target.id;
      const hard=id!=="gv-avm-overlay-opacity";
      if(hard)e.preventDefault();
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
    try{
      console.info("GV AVM LAB 0010 FOV FIT",{tag,fit,sourceFov,imageFovDeg:destination?.imageFovDeg,imageFovXDeg:destination?.imageFovXDeg,imageFovYDeg:destination?.imageFovYDeg,name:destination?.name,archiveId:destination?.archiveId});
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
function loadForBestDestination(reason){
  installTravelButtonGuard();
  swallowPanelTouches();
  preloadUpcoming(reason);
  if(suppressed())return false;
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
        console.info("GV AVM LAB 0010 AUTO LOADED",lastContext);
      },
      errorCallback:(error)=>{
        loadingKey="";
        console.warn("GV AVM LAB 0010 IMAGE LOAD FAILED",{reason,key,url,error});
      }
    });

    if(!overlay)throw new Error("A.image returned empty overlay");
    if(typeof aladinRef.setOverlayImageLayer!=="function")throw new Error("ALADIN setOverlayImageLayer unavailable");

    aladinRef.setOverlayImageLayer(overlay,LAYER_NAME);
    applyOpacity();

    return true;
  }catch(e){
    loadingKey="";
    console.error("GV AVM LAB 0010 FAILED",e);
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
  installTravelButtonGuard();
  swallowPanelTouches();

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
