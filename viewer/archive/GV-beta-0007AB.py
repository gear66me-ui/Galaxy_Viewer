from IPython.display import HTML, Javascript, display

# GV-beta-0007AB
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AB
# USER REQUEST:
# 1. Do not load or modify the splash animation in this release.
# 2. Fix only the current icon defects.
# 3. Center the approved Mollweide icon methodically, not by a guessed offset.
# 4. Preserve the approved Mollweide 0003 geometry and 24x24 size.
# 5. Make the INSIDE of both Projection and Mollweide square tiles visibly glow.
# 6. Make both icon drawings glow with exactly the same timing, easing, intensity and phase.
# 7. Preserve all unrelated viewer behavior and geometry.
# AUTHORIZED CHANGES: viewer/GV-beta-0007AB.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: GV-beta-0007AA baseline except measured post-baseline Mollweide centering and synchronized Web Animations glow.

display(HTML("""
<style id="gv-7ab-placeholder"></style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007AA.py?v=5e71d6ae87e4dfb886f0260f6cbdbc6d63dfd78f";
  const CYCLE=6400;
  const EASING="cubic-bezier(.42,0,.18,1)";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AB STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AA RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AB COULD NOT EXTRACT 7AA BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AB";
  const projection=await waitFor(()=>root.querySelector(".gv-viewer-menu-icon.gv-projection-icon"));

  // Wait until inherited 7AA/7Z/7Y style/script chain has settled before final enforcement.
  await new Promise(resolve=>setTimeout(resolve,350));

  const oldClasses=["gv-7y-sync","gv-7x-sync","gv-7w-sync","gv-pulse-synced","gv-7z-glow","gv-7aa-active"];
  const state=new WeakMap();

  const insetFrames=[
    {offset:0,backgroundColor:"rgba(2,4,8,0.02)",boxShadow:"inset 0 0 0 1px rgba(143,234,255,.12), inset 0 0 4px rgba(98,216,255,.08), inset 0 0 7px rgba(157,124,255,.04)"},
    {offset:.24,backgroundColor:"rgba(24,72,112,.10)",boxShadow:"inset 0 0 0 1.2px rgba(143,234,255,.38), inset 0 0 7px rgba(98,216,255,.28), inset 0 0 11px rgba(157,124,255,.14)"},
    {offset:.52,backgroundColor:"rgba(36,104,160,.22)",boxShadow:"inset 0 0 0 2px rgba(224,252,255,1), inset 0 0 7px rgba(143,234,255,.95), inset 0 0 13px rgba(79,166,255,.78), inset 0 0 17px rgba(157,124,255,.42)"},
    {offset:.76,backgroundColor:"rgba(24,72,112,.11)",boxShadow:"inset 0 0 0 1.2px rgba(143,234,255,.40), inset 0 0 7px rgba(98,216,255,.30), inset 0 0 11px rgba(157,124,255,.15)"},
    {offset:1,backgroundColor:"rgba(2,4,8,0.02)",boxShadow:"inset 0 0 0 1px rgba(143,234,255,.12), inset 0 0 4px rgba(98,216,255,.08), inset 0 0 7px rgba(157,124,255,.04)"}
  ];
  const iconFrames=[
    {offset:0,opacity:.58,filter:"drop-shadow(0 0 1px rgba(143,234,255,.18))"},
    {offset:.24,opacity:.74,filter:"drop-shadow(0 0 2px rgba(143,234,255,.38)) drop-shadow(0 0 4px rgba(157,124,255,.22))"},
    {offset:.52,opacity:1,filter:"drop-shadow(0 0 4px rgba(224,252,255,1)) drop-shadow(0 0 8px rgba(98,216,255,.92)) drop-shadow(0 0 13px rgba(79,166,255,.78)) drop-shadow(0 0 17px rgba(157,124,255,.50))"},
    {offset:.76,opacity:.74,filter:"drop-shadow(0 0 2px rgba(143,234,255,.38)) drop-shadow(0 0 4px rgba(157,124,255,.22))"},
    {offset:1,opacity:.58,filter:"drop-shadow(0 0 1px rgba(143,234,255,.18))"}
  ];

  function clearInherited(el){
    oldClasses.forEach(name=>el.classList.remove(name));
    el.style.setProperty("position","relative","important");
    el.style.setProperty("overflow","hidden","important");
    el.style.setProperty("isolation","isolate","important");
    const old=el.querySelector(":scope > .gv-7aa-inset");
    if(old){old.getAnimations().forEach(a=>a.cancel());old.style.setProperty("display","none","important");}
  }

  function ensureInset(el){
    let layer=el.querySelector(":scope > .gv-7ab-inset");
    if(!layer){
      layer=document.createElement("span");
      layer.className="gv-7ab-inset";
      layer.setAttribute("aria-hidden","true");
      el.insertBefore(layer,el.firstChild);
    }
    const s=layer.style;
    s.setProperty("position","absolute","important");
    s.setProperty("inset","2px","important");
    s.setProperty("border-radius","6px","important");
    s.setProperty("pointer-events","none","important");
    s.setProperty("z-index","0","important");
    s.setProperty("animation","none","important");
    return layer;
  }

  function prepareSvg(svg){
    svg.style.setProperty("position","relative","important");
    svg.style.setProperty("z-index","1","important");
    svg.style.setProperty("animation","none","important");
    svg.getAnimations().forEach(a=>a.cancel());
  }

  function measurePaintedCenter(tile,svg){
    const tileRect=tile.getBoundingClientRect();
    const svgRect=svg.getBoundingClientRect();
    const box=svg.getBBox();
    const vb=svg.viewBox.baseVal;
    const sx=svgRect.width/vb.width,sy=svgRect.height/vb.height;
    return {
      tileX:tileRect.left+tileRect.width/2,
      tileY:tileRect.top+tileRect.height/2,
      paintX:svgRect.left+(box.x+box.width/2-vb.x)*sx,
      paintY:svgRect.top+(box.y+box.height/2-vb.y)*sy,
      box
    };
  }

  function centerMollweide(){
    const tile=root.querySelector(".gv-projection-option-icon");
    const svg=tile?.querySelector("svg");
    if(!tile||!svg)return null;
    tile.style.setProperty("display","grid","important");
    tile.style.setProperty("place-items","center","important");
    svg.style.setProperty("width","24px","important");
    svg.style.setProperty("height","24px","important");
    svg.style.setProperty("margin","0","important");
    svg.style.setProperty("grid-area","1 / 1","important");
    svg.style.setProperty("justify-self","center","important");
    svg.style.setProperty("align-self","center","important");
    svg.style.setProperty("transform-origin","center center","important");
    svg.style.setProperty("transform","none","important");
    void svg.getBoundingClientRect();
    const before=measurePaintedCenter(tile,svg);
    const dx=before.tileX-before.paintX,dy=before.tileY-before.paintY;
    svg.style.setProperty("transform",`translate(${dx.toFixed(3)}px,${dy.toFixed(3)}px)`,`important`);
    void svg.getBoundingClientRect();
    const after=measurePaintedCenter(tile,svg);
    return {dx,dy,errorX:after.tileX-after.paintX,errorY:after.tileY-after.paintY,bbox:{x:after.box.x,y:after.box.y,width:after.box.width,height:after.box.height}};
  }

  function cancelOwned(el){
    const owned=state.get(el)||[];
    owned.forEach(a=>{try{a.cancel()}catch(_){ }});
    state.delete(el);
  }

  function animateControl(el,startTime){
    clearInherited(el);
    const layer=ensureInset(el),svg=el.querySelector("svg");
    if(!svg)return [];
    prepareSvg(svg);
    cancelOwned(el);
    const options={duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"};
    const a=layer.animate(insetFrames,options);
    const b=svg.animate(iconFrames,options);
    a.startTime=startTime;b.startTime=startTime;
    state.set(el,[a,b]);
    return [a,b];
  }

  function startProjection(){
    const t=document.timeline.currentTime||performance.now();
    animateControl(projection,t);
  }

  function synchronizePair(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!mollweide){startProjection();return false;}
    centerMollweide();
    const t=document.timeline.currentTime||performance.now();
    animateControl(projection,t);
    animateControl(mollweide,t);
    return true;
  }

  function validate(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    const pInset=projection.querySelector(":scope > .gv-7ab-inset"),pSvg=projection.querySelector("svg");
    const pAnims=state.get(projection)||[];
    const checks={projectionInsetExists:!!pInset,projectionPairAnimations:pAnims.length===2,projectionAnimationsRunning:pAnims.every(a=>a.playState==="running")};
    let centering=null;
    if(mollweide){
      centering=centerMollweide();
      const mInset=mollweide.querySelector(":scope > .gv-7ab-inset"),mSvg=mollweide.querySelector("svg"),mAnims=state.get(mollweide)||[];
      const pr=projection.getBoundingClientRect(),mr=mollweide.getBoundingClientRect();
      Object.assign(checks,{
        mollweideInsetExists:!!mInset,
        mollweidePairAnimations:mAnims.length===2,
        mollweideAnimationsRunning:mAnims.every(a=>a.playState==="running"),
        exactSharedStart:pAnims.length===2&&mAnims.length===2&&pAnims[0].startTime===mAnims[0].startTime&&pAnims[1].startTime===mAnims[1].startTime,
        mollweideSize:Math.round(mSvg.getBoundingClientRect().width)===24&&Math.round(mSvg.getBoundingClientRect().height)===24,
        measuredCenter:Math.abs(centering.errorX)<0.40&&Math.abs(centering.errorY)<0.40,
        exactApproved0003Geometry:mSvg.innerHTML.includes('rx="25.5" ry="16.5"')&&mSvg.innerHTML.includes('M11 32H53')&&mSvg.innerHTML.includes('M45.5 20.3C50.3 26 50.3 38 45.5 43.7'),
        squareTiles:Math.abs(pr.width-pr.height)<1&&Math.abs(mr.width-mr.height)<1
      });
    }
    const passed=Object.values(checks).every(Boolean);
    window.GV7AB_VALIDATION={passed,checks,centering,cycleMs:CYCLE,easing:EASING,engine:"Web Animations API",splash:"not loaded or modified"};
    if(!passed)throw new Error("GV-BETA-0007AB CONTRACT FAILED "+JSON.stringify(window.GV7AB_VALIDATION));
    return true;
  }

  startProjection();
  requestAnimationFrame(()=>requestAnimationFrame(validate));

  const observer=new MutationObserver(()=>{
    if(root.querySelector(".gv-projection-option-icon"))requestAnimationFrame(()=>{synchronizePair();requestAnimationFrame(()=>requestAnimationFrame(validate));});
  });
  observer.observe(root,{subtree:true,childList:true});
})().catch(error=>console.error("GV-BETA-0007AB STARTUP FAILURE:",error));
"""))

# GV-beta-0007AB staged
