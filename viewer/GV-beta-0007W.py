from IPython.display import HTML, Javascript, display

# GV-beta-0007W
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007W
# USER REQUEST:
# 1. Place the Mollweide 36x36 icon tile directly beside the Mollweide text tile with the same 2px gap used by the main Projection row.
# 2. Projection icon drawing edges and Mollweide icon drawing edges must glow in exact unison.
# 3. The inside edge/interior of both square icon tiles must glow in that same pulse.
# 4. Both controls must share the same start, end, 6.4s cycle, easing and phase.
# 5. Tile borders remain stable; no animated exterior halo.
# 6. Keep the current Mollweide geometry and center it precisely inside its square tile.
# AUTHORIZED CHANGES: viewer/GV-beta-0007W.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: Hamburger, target/SIMBAD, Aladin initialization, coordinate overlay/font, galaxy navigation, all unrelated menu rows, previous releases.

display(HTML("""
<style>
:root{--gv-7w-cycle:6.4s}

/* Lock the Mollweide submenu row into the same label + square-tile geometry as the main menu. */
#aladin-cosmic-command-test .gv-projection-submenu{
  width:158px!important;
}
#aladin-cosmic-command-test .gv-projection-submenu .gv-projection-option-row{
  display:grid!important;
  grid-template-columns:120px 36px!important;
  column-gap:2px!important;
  width:158px!important;
  min-width:158px!important;
  max-width:158px!important;
  height:36px!important;
  margin:0!important;
  padding:0!important;
  align-items:center!important;
}
#aladin-cosmic-command-test .gv-projection-submenu .gv-projection-option-row > button.gv-projection-option-label{
  width:120px!important;
  min-width:120px!important;
  max-width:120px!important;
  height:36px!important;
  min-height:36px!important;
  max-height:36px!important;
  margin:0!important;
  padding:0 8px!important;
}
#aladin-cosmic-command-test .gv-projection-submenu .gv-projection-option-row > button.gv-projection-option-icon{
  width:36px!important;
  min-width:36px!important;
  max-width:36px!important;
  height:36px!important;
  min-height:36px!important;
  max-height:36px!important;
  margin:0!important;
  padding:0!important;
  justify-self:start!important;
  align-self:center!important;
  display:grid!important;
  place-items:center!important;
}

/* Stable tile shell. Only the inside layer and SVG drawing animate. */
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon,
#aladin-cosmic-command-test .gv-projection-option-icon{
  position:relative!important;
  overflow:hidden!important;
  background:#020408!important;
  animation:none!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon::before,
#aladin-cosmic-command-test .gv-projection-option-icon::before{
  content:""!important;
  position:absolute!important;
  inset:1px!important;
  z-index:0!important;
  border-radius:5px!important;
  pointer-events:none!important;
  animation:none!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg,
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  position:relative!important;
  z-index:1!important;
  width:30px!important;
  height:30px!important;
  margin:0!important;
  transform:none!important;
  transform-origin:center!important;
  animation:none!important;
}

/* One shared clock for both square-tile interiors. */
#aladin-cosmic-command-test .gv-7w-sync::before{
  animation:gv-7w-inner-tile-pulse var(--gv-7w-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
/* One shared clock for both actual icon drawings. */
#aladin-cosmic-command-test .gv-7w-sync svg{
  animation:gv-7w-icon-edge-pulse var(--gv-7w-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}

@keyframes gv-7w-inner-tile-pulse{
  0%,100%{
    opacity:.42;
    background:radial-gradient(circle at 50% 50%,rgba(79,166,255,.025) 0%,rgba(0,0,0,0) 70%);
    box-shadow:inset 0 0 5px rgba(98,216,255,.025),inset 0 0 2px rgba(157,124,255,.02);
  }
  24%{
    opacity:.64;
    background:radial-gradient(circle at 50% 50%,rgba(79,166,255,.075) 0%,rgba(38,48,78,.05) 42%,rgba(0,0,0,0) 72%);
    box-shadow:inset 0 0 9px rgba(98,216,255,.08),inset 0 0 5px rgba(157,124,255,.05);
  }
  52%{
    opacity:1;
    background:radial-gradient(circle at 50% 50%,rgba(96,191,255,.24) 0%,rgba(58,72,128,.16) 38%,rgba(38,25,78,.10) 58%,rgba(0,0,0,0) 78%);
    box-shadow:inset 0 0 17px rgba(98,216,255,.34),inset 0 0 9px rgba(157,124,255,.24),inset 0 0 3px rgba(255,255,255,.15);
  }
  76%{
    opacity:.66;
    background:radial-gradient(circle at 50% 50%,rgba(79,166,255,.085) 0%,rgba(38,48,78,.055) 42%,rgba(0,0,0,0) 72%);
    box-shadow:inset 0 0 9px rgba(98,216,255,.085),inset 0 0 5px rgba(157,124,255,.055);
  }
}
@keyframes gv-7w-icon-edge-pulse{
  0%,100%{opacity:.54;filter:drop-shadow(0 0 1px rgba(143,234,255,.16))}
  24%{opacity:.70;filter:drop-shadow(0 0 2px rgba(143,234,255,.30)) drop-shadow(0 0 4px rgba(157,124,255,.18))}
  52%{opacity:1;filter:drop-shadow(0 0 4px rgba(143,234,255,1)) drop-shadow(0 0 9px rgba(79,166,255,.82)) drop-shadow(0 0 14px rgba(157,124,255,.60))}
  76%{opacity:.70;filter:drop-shadow(0 0 2px rgba(143,234,255,.30)) drop-shadow(0 0 4px rgba(157,124,255,.18))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007V.py?v=f04b2ce1a1b49b5703689ba355ee2ad04fbdb401";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007W STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007V RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007W COULD NOT EXTRACT 7V BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7W";

  function synchronize(){
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!projection||!mollweide)return false;
    [projection,mollweide].forEach(el=>el.classList.remove("gv-7w-sync","gv-pulse-synced"));
    void root.offsetWidth;
    [projection,mollweide].forEach(el=>el.classList.add("gv-7w-sync"));
    return true;
  }

  function validate(){
    const row=root.querySelector(".gv-projection-option-row");
    const label=row?.querySelector(".gv-projection-option-label");
    const mollweide=row?.querySelector(".gv-projection-option-icon");
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const pSvg=projection?.querySelector("svg"),mSvg=mollweide?.querySelector("svg");
    if(!row||!label||!mollweide||!projection||!pSvg||!mSvg)return false;

    const r=getComputedStyle(row),l=getComputedStyle(label),m=getComputedStyle(mollweide),p=getComputedStyle(projection);
    const pBefore=getComputedStyle(projection,"::before"),mBefore=getComputedStyle(mollweide,"::before");
    const ps=getComputedStyle(pSvg),ms=getComputedStyle(mSvg);
    const gap=Math.round(mollweide.getBoundingClientRect().left-label.getBoundingClientRect().right);
    const checks={
      rowWidth:Math.round(row.getBoundingClientRect().width)===158,
      labelWidth:Math.round(label.getBoundingClientRect().width)===120,
      mollweideTileSquare:Math.round(mollweide.getBoundingClientRect().width)===36&&Math.round(mollweide.getBoundingClientRect().height)===36,
      sideBySideGap:gap===2,
      projectionTileAnimation:p.animationName==="none",
      mollweideTileAnimation:m.animationName==="none",
      projectionInterior:pBefore.animationName.includes("gv-7w-inner-tile-pulse"),
      mollweideInterior:mBefore.animationName.includes("gv-7w-inner-tile-pulse"),
      sameInteriorDuration:pBefore.animationDuration===mBefore.animationDuration&&pBefore.animationDuration==="6.4s",
      projectionIcon:ps.animationName.includes("gv-7w-icon-edge-pulse"),
      mollweideIcon:ms.animationName.includes("gv-7w-icon-edge-pulse"),
      sameIconDuration:ps.animationDuration===ms.animationDuration&&ps.animationDuration==="6.4s",
      iconCentered:Math.abs((mollweide.getBoundingClientRect().left+mollweide.getBoundingClientRect().width/2)-(mSvg.getBoundingClientRect().left+mSvg.getBoundingClientRect().width/2))<1.1
    };
    const passed=Object.values(checks).every(Boolean);
    window.GV7W_VALIDATION={passed,checks,gap,cycle:"6.4s",phase:"simultaneous-class-activation"};
    if(!passed)throw new Error("GV-BETA-0007W CONTRACT FAILED "+JSON.stringify(window.GV7W_VALIDATION));
    return true;
  }

  function apply(){if(!synchronize())return false;requestAnimationFrame(()=>requestAnimationFrame(validate));return true}
  const observer=new MutationObserver(()=>{if(root.querySelector(".gv-projection-option-icon"))requestAnimationFrame(apply)});
  observer.observe(root,{subtree:true,childList:true});
  apply();
})().catch(error=>console.error("GV-BETA-0007W STARTUP FAILURE:",error));
"""))

# GV-beta-0007W staged
