(function(global){
  "use strict";
  const VERSION="0001";
  const LAB_ID="gv-avm-overlay-lab";
  const LAYER_NAME="GV AVM LAB OVERLAY";

  function finite(value){const n=Number(value);return Number.isFinite(n)?n:null}
  function firstText(){for(const value of arguments){const text=String(value||"").trim();if(text)return text}return ""}

  function getDestination(randomGalaxy){
    const state=randomGalaxy?.getState?.()||{};
    return state.activeDestination||randomGalaxy?.activeDestination||global.GalaxyRandomGalaxy?.currentDestination||global.GalaxyRandomGalaxy?.activeDestination||null;
  }

  function imageUrlFor(destination){
    return firstText(destination?.preparedHdUrl,destination?.githubImageUrl,destination?.hdUrl,destination?.imageUrl,destination?.imageURL,destination?.url);
  }

  function loadPixelDimensions(url){
    return new Promise((resolve,reject)=>{
      const img=new Image();
      img.decoding="async";
      img.onload=()=>resolve({width:img.naturalWidth||img.width||0,height:img.naturalHeight||img.height||0});
      img.onerror=()=>reject(new Error("AVM LAB IMAGE DIMENSION LOAD FAILED"));
      img.src=url;
    });
  }

  function buildManualWcs(destination,width,height){
    const ra=finite(destination?.ra);
    const dec=finite(destination?.dec);
    const fov=finite(destination?.fovDegrees??destination?.fov??destination?.fieldOfView);
    const rotation=finite(destination?.aladinRotation??destination?.rotation)??0;
    const scale=fov/Math.max(width,height);
    const theta=rotation*Math.PI/180;
    const cos=Math.cos(theta);
    const sin=Math.sin(theta);
    return {NAXIS:2,NAXIS1:width,NAXIS2:height,CTYPE1:"RA---TAN",CTYPE2:"DEC--TAN",CUNIT1:"deg",CUNIT2:"deg",CRVAL1:ra,CRVAL2:dec,CRPIX1:width/2,CRPIX2:height/2,CD1_1:-scale*cos,CD1_2:scale*sin,CD2_1:scale*sin,CD2_2:scale*cos};
  }

  function forceJsonView(aladin,destination){
    const ra=finite(destination?.ra);
    const dec=finite(destination?.dec);
    const fov=finite(destination?.fovDegrees??destination?.fov??destination?.fieldOfView);
    const rotation=finite(destination?.aladinRotation??destination?.rotation)??0;
    try{aladin.setFrame?.("ICRSd")}catch(error){console.warn("AVM LAB setFrame warning",error)}
    try{aladin.setProjection?.("TAN")}catch(error){console.warn("AVM LAB setProjection warning",error)}
    try{if(ra!==null&&dec!==null)aladin.gotoRaDec?.(ra,dec)}catch(error){console.warn("AVM LAB goto warning",error)}
    try{if(fov!==null){if(typeof aladin.setFoV==="function")aladin.setFoV(fov);else aladin.setFov?.(fov)}}catch(error){console.warn("AVM LAB fov warning",error)}
    try{aladin.setRotation?.(rotation)}catch(error){console.warn("AVM LAB rotation warning",error)}
  }

  function makePanel(root){
    let panel=root.querySelector("#"+LAB_ID);
    if(panel)return panel;
    panel=document.createElement("div");
    panel.id=LAB_ID;
    panel.innerHTML="<button id=\"gv-avm-overlay-load\" type=\"button\">AVM LAB OVERLAY</button><label> OPACITY <input id=\"gv-avm-overlay-opacity\" type=\"range\" min=\"0\" max=\"100\" value=\"55\"></label><div id=\"gv-avm-overlay-status\">idle</div>";
    const style=document.createElement("style");
    style.id="gv-avm-overlay-lab-style";
    style.textContent="#gv-avm-overlay-lab{position:absolute;left:50%;top:max(8px,env(safe-area-inset-top));z-index:7700;transform:translateX(-50%);display:flex;align-items:center;gap:8px;padding:5px 7px;border:1px solid rgba(124,203,255,.78);border-radius:7px;background:rgba(4,15,32,.78);color:#DDF8FF;font:400 9px/1.2 \"Space Age\",sans-serif;letter-spacing:.45px;pointer-events:auto}#gv-avm-overlay-lab button{height:28px;padding:0 8px;border:1px solid #7CCBFF;border-radius:5px;background:rgba(11,49,119,.94);color:#EAF8FF;font:inherit;letter-spacing:.45px}#gv-avm-overlay-lab input{width:92px;vertical-align:middle}#gv-avm-overlay-status{max-width:150px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#9BE5FF}";
    document.head.appendChild(style);
    root.appendChild(panel);
    return panel;
  }

  function install({A,aladin,viewerRoot,randomGalaxy}={}){
    if(viewerRoot.dataset.gvAvmLabInstalled==="1")return;
    viewerRoot.dataset.gvAvmLabInstalled="1";
    const panel=makePanel(viewerRoot);
    const button=panel.querySelector("#gv-avm-overlay-load");
    const slider=panel.querySelector("#gv-avm-overlay-opacity");
    const status=panel.querySelector("#gv-avm-overlay-status");
    let overlay=null;
    const setStatus=text=>{status.textContent=String(text||"")};

    slider.addEventListener("input",()=>{
      const opacity=Math.max(0,Math.min(1,Number(slider.value)/100));
      try{overlay?.setOpacity?.(opacity)}catch(_){}
      try{overlay?.setAlpha?.(opacity)}catch(_){}
      try{overlay?.setOptions?.({opacity})}catch(_){}
      setStatus("opacity "+Math.round(opacity*100)+"%");
    });

    button.addEventListener("click",async()=>{
      try{
        setStatus("loading");
        const destination=getDestination(randomGalaxy);
        const url=imageUrlFor(destination);
        const dims=await loadPixelDimensions(url);
        const wcs=buildManualWcs(destination,dims.width,dims.height);
        const opacity=Math.max(0,Math.min(1,Number(slider.value)/100));
        overlay=A.image(url,{name:LAYER_NAME,imgFormat:/\.png(?:[?#]|$)/i.test(url)?"png":"jpeg",opacity,wcs});
        if(typeof aladin.setOverlayImageLayer!=="function")throw new Error("ALADIN setOverlayImageLayer unavailable");
        aladin.setOverlayImageLayer(overlay,LAYER_NAME);
        forceJsonView(aladin,destination);
        global.GalaxyViewerAvmOverlayLab.last={version:VERSION,destination,url,dimensions:dims,wcs,opacity};
        setStatus("loaded "+dims.width+"x"+dims.height);
        console.info("GV AVM LAB OVERLAY LOADED",global.GalaxyViewerAvmOverlayLab.last);
      }catch(error){
        console.error("GV AVM LAB OVERLAY FAILED",error);
        setStatus(String(error?.message||error).slice(0,80));
      }
    });
    global.GalaxyViewerAvmOverlayLab.instance={panel,button,slider};
    console.info("GV AVM LAB INSTALLED",VERSION);
  }

  global.GalaxyViewerAvmOverlayLab=Object.freeze({VERSION,install});
})(window);
