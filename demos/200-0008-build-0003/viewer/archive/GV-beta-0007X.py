from IPython.display import HTML, Javascript, display

# GV-beta-0007X
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007X
# USER REQUEST:
# 1. Make the inside edge of both Projection and Mollweide square icon tiles visibly glow as an inset neon ring/bloom, not an exterior halo and not merely a center haze.
# 2. Projection icon strokes and Mollweide icon strokes must glow in exact unison with those tile-interior glows.
# 3. Both controls share the same 6.4s cycle, easing, start, peak, fade and phase.
# 4. Move the Mollweide drawing visually to the right inside its 36x36 tile so it no longer reads left-flushed.
# 5. Preserve Mollweide text tile, menu geometry, coordinate strip, target/SIMBAD, galaxy navigation and all unrelated behavior.
# AUTHORIZED CHANGES: viewer/GV-beta-0007X.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: GV-beta-0007W baseline behavior except the authorized tile-inner-glow strength and Mollweide icon horizontal alignment.

display(HTML("""
<style>
:root{--gv-7x-cycle:6.4s}

/* Stable square shells: no animated exterior halo. */
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon,
#aladin-cosmic-command-test .gv-projection-option-icon{
  position:relative!important;
  overflow:hidden!important;
  background:#020408!important;
  animation:none!important;
}

/* The glow is an inner-edge ring plus inward bloom, entirely inside the tile. */
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon::before,
#aladin-cosmic-command-test .gv-projection-option-icon::before{
  content:""!important;
  position:absolute!important;
  inset:1px!important;
  z-index:0!important;
  border-radius:5px!important;
  pointer-events:none!important;
  background:rgba(0,0,0,0)!important;
  box-shadow:
    inset 0 0 0 1px rgba(143,234,255,.08),
    inset 0 0 5px rgba(98,216,255,.04),
    inset 0 0 9px rgba(157,124,255,.025)!important;
  animation:none!important;
}

#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg,
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  position:relative!important;
  z-index:1!important;
  width:30px!important;
  height:30px!important;
  margin:0!important;
  animation:none!important;
}

/* Optical correction requested: shift only Mollweide artwork to the right. */
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  transform:translateX(2.5px)!important;
  transform-origin:center!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg{
  transform:none!important;
}

/* One synchronized clock drives both inner rings. */
#aladin-cosmic-command-test .gv-7x-sync::before{
  animation:gv-7x-inner-edge-pulse var(--gv-7x-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
/* Same synchronized clock drives both SVG drawings. */
#aladin-cosmic-command-test .gv-7x-sync svg{
  animation:gv-7x-icon-stroke-pulse var(--gv-7x-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}

@keyframes gv-7x-inner-edge-pulse{
  0%,100%{
    opacity:.48;
    background:rgba(0,0,0,0);
    box-shadow:
      inset 0 0 0 1px rgba(143,234,255,.08),
      inset 0 0 5px rgba(98,216,255,.04),
      inset 0 0 9px rgba(157,124,255,.025);
  }
  24%{
    opacity:.70;
    background:radial-gradient(circle at 50% 50%,rgba(79,166,255,.035) 0%,rgba(0,0,0,0) 66%);
    box-shadow:
      inset 0 0 0 1px rgba(143,234,255,.22),
      inset 0 0 8px rgba(98,216,255,.13),
      inset 0 0 13px rgba(157,124,255,.08);
  }
  52%{
    opacity:1;
    background:radial-gradient(circle at 50% 50%,rgba(79,166,255,.08) 0%,rgba(0,0,0,0) 64%);
    box-shadow:
      inset 0 0 0 1.35px rgba(214,249,255,.92),
      inset 0 0 7px rgba(143,234,255,.76),
      inset 0 0 14px rgba(79,166,255,.52),
      inset 0 0 20px rgba(157,124,255,.25);
  }
  76%{
    opacity:.72;
    background:radial-gradient(circle at 50% 50%,rgba(79,166,255,.04) 0%,rgba(0,0,0,0) 66%);
    box-shadow:
      inset 0 0 0 1px rgba(143,234,255,.24),
      inset 0 0 8px rgba(98,216,255,.14),
      inset 0 0 13px rgba(157,124,255,.09);
  }
}

@keyframes gv-7x-icon-stroke-pulse{
  0%,100%{opacity:.56;filter:drop-shadow(0 0 1px rgba(143,234,255,.16))}
  24%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
  52%{opacity:1;filter:drop-shadow(0 0 4px rgba(214,249,255,1)) drop-shadow(0 0 8px rgba(98,216,255,.90)) drop-shadow(0 0 13px rgba(79,166,255,.76)) drop-shadow(0 0 17px rgba(157,124,255,.48))}
  76%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007W.py?v=387cdbbe311361c7e9861cf6bc3d3ea9edaf9d1b";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007X STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007W RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007X COULD NOT EXTRACT 7W BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7X";

  function synchronize(){
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!projection||!mollweide)return false;
    [projection,mollweide].forEach(el=>el.classList.remove("gv-7x-sync","gv-7w-sync","gv-pulse-synced"));
    void root.offsetWidth;
    [projection,mollweide].forEach(el=>el.classList.add("gv-7x-sync"));
    return true;
  }

  function validate(){
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const mollweide=root.querySelector(".gv-projection-option-icon");
    const pSvg=projection?.querySelector("svg"),mSvg=mollweide?.querySelector("svg");
    if(!projection||!mollweide||!pSvg||!mSvg)return false;

    const p=getComputedStyle(projection),m=getComputedStyle(mollweide);
    const pBefore=getComputedStyle(projection,"::before"),mBefore=getComputedStyle(mollweide,"::before");
    const ps=getComputedStyle(pSvg),ms=getComputedStyle(mSvg);
    const tile=mollweide.getBoundingClientRect(),svg=mSvg.getBoundingClientRect();
    const tileCenter=tile.left+tile.width/2,svgCenter=svg.left+svg.width/2;
    const offset=svgCenter-tileCenter;
    const checks={
      projectionTileAnimation:p.animationName==="none",
      mollweideTileAnimation:m.animationName==="none",
      projectionInnerGlow:pBefore.animationName.includes("gv-7x-inner-edge-pulse"),
      mollweideInnerGlow:mBefore.animationName.includes("gv-7x-inner-edge-pulse"),
      sameInnerDuration:pBefore.animationDuration===mBefore.animationDuration&&pBefore.animationDuration==="6.4s",
      projectionStrokeGlow:ps.animationName.includes("gv-7x-icon-stroke-pulse"),
      mollweideStrokeGlow:ms.animationName.includes("gv-7x-icon-stroke-pulse"),
      sameStrokeDuration:ps.animationDuration===ms.animationDuration&&ps.animationDuration==="6.4s",
      mollweideShiftedRight:offset>=2&&offset<=3.2
    };
    const passed=Object.values(checks).every(Boolean);
    window.GV7X_VALIDATION={passed,checks,cycle:"6.4s",phase:"simultaneous-class-activation",mollweideVisualOffsetPx:Number(offset.toFixed(2))};
    if(!passed)throw new Error("GV-BETA-0007X CONTRACT FAILED "+JSON.stringify(window.GV7X_VALIDATION));
    return true;
  }

  function apply(){if(!synchronize())return false;requestAnimationFrame(()=>requestAnimationFrame(validate));return true}
  const observer=new MutationObserver(()=>{if(root.querySelector(".gv-projection-option-icon"))requestAnimationFrame(apply)});
  observer.observe(root,{subtree:true,childList:true});
  apply();
})().catch(error=>console.error("GV-BETA-0007X STARTUP FAILURE:",error));
"""))

# GV-beta-0007X staged
