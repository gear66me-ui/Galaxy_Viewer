(function(global){
"use strict";
const VERSION="0006";
const LAYER_NAME="GV AVM NATIVE OVERLAY";
let overlay=null;
let lastContext=null;

function text(v){return String(v??"").trim()}
function clamp01(v){v=Number(v);return Number.isFinite(v)?Math.max(0,Math.min(1,v)):0.55}

function getDestination(randomGalaxy){
  try{
    const state=randomGalaxy?.getState?.();
    if(state?.activeDestination)return state.activeDestination;
  }catch(_){}
  return randomGalaxy?.activeDestination || global.GalaxyRandomGalaxy?.currentDestination || null;
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

function isUsableAvmDestination(d,url){
  if(!d || !url)return false;
  if(text(d.name).match(/^earth\b|milky way/i) && !text(d.screenUrl) && !text(d.avmSourceUrl))return false;
  if(text(d.avmProfile)==="AVM")return true;
  if(text(d.avmStatus).toUpperCase().includes("AVM"))return true;
  if(/\/screen\//i.test(url) && /cdn\.esa(hubble|webb)\.org/i.test(url))return true;
  return false;
}

function panel(){
  let p=document.getElementById("gv-avm-overlay-lab");
  if(p)return p;
  p=document.createElement("div");
  p.id="gv-avm-overlay-lab";
  p.innerHTML=[
    "<button id=\"gv-avm-overlay-load\" type=\"button\">AVM</button>",
    "<label id=\"gv-avm-opacity-label\"><span>OPACITY</span><input id=\"gv-avm-overlay-opacity\" type=\"range\" min=\"0\" max=\"100\" value=\"55\"></label>",
    "<div id=\"gv-avm-overlay-status\">native 0006</div>"
  ].join("");
  document.body.appendChild(p);

  let s=document.getElementById("gv-avm-overlay-lab-style-0006");
  if(!s){
    s=document.createElement("style");
    s.id="gv-avm-overlay-lab-style-0006";
    s.textContent=[
      "#gv-avm-overlay-lab{position:fixed;top:56px;left:50%;transform:translateX(-50%);z-index:2147482000;width:min(360px,calc(100vw - 18px));height:34px;box-sizing:border-box;display:grid;grid-template-columns:72px 1fr 84px;align-items:center;gap:7px;padding:5px 7px;border:1px solid rgba(124,203,255,.92);border-radius:9px;background:rgba(2,7,15,.86);color:#DDF8FF;font:700 9px/1.1 system-ui,sans-serif;box-shadow:0 0 10px rgba(88,191,255,.30)}",
      "#gv-avm-overlay-load{height:24px;border:1px solid #7CCBFF;border-radius:6px;background:#08264d;color:#EAF8FF;font:800 10px/1 system-ui,sans-serif}",
      "#gv-avm-opacity-label{display:grid;grid-template-columns:48px 1fr;align-items:center;gap:5px;min-width:0}",
      "#gv-avm-opacity-label span{white-space:nowrap}",
      "#gv-avm-overlay-opacity{width:100%;height:22px;margin:0}",
      "#gv-avm-overlay-status{justify-self:end;max-width:84px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#9FE5FF;text-align:right}",
      "@media(max-width:430px){#gv-avm-overlay-lab{top:55px;width:calc(100vw - 16px);grid-template-columns:62px 1fr 78px;font-size:8px}}"
    ].join("");
    document.head.appendChild(s);
  }
  return p;
}

function install({A,aladin,viewerRoot,randomGalaxy}={}){
  if(!A)throw new Error("ALADIN A NAMESPACE MISSING");
  if(!aladin)throw new Error("ALADIN INSTANCE MISSING");
  if(!viewerRoot)throw new Error("VIEWER ROOT MISSING");

  const p=panel();
  const button=p.querySelector("#gv-avm-overlay-load");
  const slider=p.querySelector("#gv-avm-overlay-opacity");
  const status=p.querySelector("#gv-avm-overlay-status");
  const setStatus=t=>{status.textContent=String(t||"").slice(0,42)};

  slider.addEventListener("input",()=>{
    const op=clamp01(Number(slider.value)/100);
    try{overlay?.setOpacity?.(op)}catch(_){}
    try{overlay?.setAlpha?.(op)}catch(_){}
    try{overlay?.setOptions?.({opacity:op})}catch(_){}
    setStatus(Math.round(op*100)+"%");
  });

  button.addEventListener("click",async()=>{
    try{
      const d=getDestination(randomGalaxy);
      const url=avmUrlFor(d);
      if(!isUsableAvmDestination(d,url)){
        setStatus("random first");
        console.warn("GV AVM LAB 0006 BLOCKED: no active AVM galaxy", {destination:d,url});
        return;
      }

      setStatus("loading");
      const op=clamp01(Number(slider.value)/100);

      try{aladin.removeOverlayImageLayer?.(LAYER_NAME)}catch(_){}

      overlay=A.image(url,{
        name:LAYER_NAME,
        imgFormat:/\.png(?:[?#]|$)/i.test(url)?"png":"jpeg",
        opacity:op
      });

      if(!overlay)throw new Error("A.image returned empty overlay");
      if(typeof aladin.setOverlayImageLayer!=="function")throw new Error("ALADIN setOverlayImageLayer unavailable");

      aladin.setOverlayImageLayer(overlay,LAYER_NAME);

      lastContext={
        version:VERSION,
        mode:"native-avm-no-manual-wcs-guarded",
        destination:d,
        url,
        opacity:op,
        overlay
      };

      global.GalaxyViewerAvmOverlayLab.lastContext=lastContext;
      setStatus("loaded");
      console.info("GV AVM LAB 0006 LOADED",lastContext);
    }catch(e){
      console.error("GV AVM LAB 0006 FAILED",e);
      setStatus(String(e?.message||e).slice(0,42));
    }
  });

  global.GalaxyViewerAvmOverlayLab.instance={panel:p,button,slider,status,get last(){return lastContext}};
  console.info("GV AVM LAB INSTALLED",VERSION);
}

global.GalaxyViewerAvmOverlayLab={
  VERSION,
  install,
  get last(){return lastContext},
  get overlay(){return overlay}
};
})(window);
