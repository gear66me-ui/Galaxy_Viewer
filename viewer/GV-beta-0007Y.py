from IPython.display import HTML, Javascript, display

# GV-beta-0007Y
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007Y
# USER REQUEST:
# 1. Install the approved standalone Projection glow prototype and approved Mollweide glow 0003 prototype into the viewer.
# 2. Keep Projection icon geometry unchanged.
# 3. Replace viewer Mollweide icon geometry with the exact approved rounded-ellipse 0003 geometry: denser wireframe, purple grid stopping short of cyan boundary, 20% smaller, centered.
# 4. Both Projection and Mollweide square tiles use the same visible inside-edge inset glow; both SVG drawings glow on the same synchronized 6.4s cycle.
# 5. Preserve the current Projection/Mollweide submenu layout and every unrelated viewer behavior.
# AUTHORIZED CHANGES: viewer/GV-beta-0007Y.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: Hamburger, target/SIMBAD, Aladin initialization, coordinate overlay/font, galaxy navigation, all unrelated menu rows, previous releases.

display(HTML("""
<style>
:root{--gv-7y-cycle:6.4s}
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
  background:rgba(0,0,0,0)!important;
  box-shadow:inset 0 0 0 1px rgba(143,234,255,.08),inset 0 0 5px rgba(98,216,255,.04),inset 0 0 9px rgba(157,124,255,.025)!important;
  animation:none!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg,
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  position:relative!important;
  z-index:1!important;
  margin:0!important;
  animation:none!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg{
  width:30px!important;
  height:30px!important;
  transform:none!important;
}
#aladin-cosmic-command-test .gv-projection-option-icon{
  display:grid!important;
  place-items:center!important;
}
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  width:24px!important;
  height:24px!important;
  transform:none!important;
  transform-origin:center!important;
}
#aladin-cosmic-command-test .gv-7y-sync::before{
  animation:gv-7y-inner-edge-pulse var(--gv-7y-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
#aladin-cosmic-command-test .gv-7y-sync svg{
  animation:gv-7y-icon-stroke-pulse var(--gv-7y-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
@keyframes gv-7y-inner-edge-pulse{
  0%,100%{opacity:.48;background:rgba(0,0,0,0);box-shadow:inset 0 0 0 1px rgba(143,234,255,.08),inset 0 0 5px rgba(98,216,255,.04),inset 0 0 9px rgba(157,124,255,.025)}
  24%{opacity:.70;background:rgba(79,166,255,.025);box-shadow:inset 0 0 0 1px rgba(143,234,255,.22),inset 0 0 8px rgba(98,216,255,.13),inset 0 0 13px rgba(157,124,255,.08)}
  52%{opacity:1;background:rgba(79,166,255,.055);box-shadow:inset 0 0 0 1.35px rgba(214,249,255,.92),inset 0 0 7px rgba(143,234,255,.76),inset 0 0 14px rgba(79,166,255,.52),inset 0 0 20px rgba(157,124,255,.25)}
  76%{opacity:.72;background:rgba(79,166,255,.03);box-shadow:inset 0 0 0 1px rgba(143,234,255,.24),inset 0 0 8px rgba(98,216,255,.14),inset 0 0 13px rgba(157,124,255,.09)}
}
@keyframes gv-7y-icon-stroke-pulse{
  0%,100%{opacity:.56;filter:drop-shadow(0 0 1px rgba(143,234,255,.16))}
  24%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
  52%{opacity:1;filter:drop-shadow(0 0 4px rgba(214,249,255,1)) drop-shadow(0 0 8px rgba(98,216,255,.90)) drop-shadow(0 0 13px rgba(79,166,255,.76)) drop-shadow(0 0 17px rgba(157,124,255,.48))}
  76%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007X.py?v=aaefffb9a03e4bdc87e9735e3c00c1ebe7421941";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007Y STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});
  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007X RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007Y COULD NOT EXTRACT 7X BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7Y";

  const approvedMollweide=`<svg viewBox="0 0 64 64" aria-hidden="true"><ellipse class="gv-mol-outline" cx="32" cy="32" rx="25.5" ry="16.5"/><path class="gv-mol-grid" d="M11 32H53"/><path class="gv-mol-grid" d="M12.5 25.2C21.5 21.8 42.5 21.8 51.5 25.2"/><path class="gv-mol-grid" d="M12.5 38.8C21.5 42.2 42.5 42.2 51.5 38.8"/><path class="gv-mol-grid" d="M32 17.5V46.5"/><path class="gv-mol-grid" d="M25 18.4C20.5 23.8 20.5 40.2 25 45.6"/><path class="gv-mol-grid" d="M39 18.4C43.5 23.8 43.5 40.2 39 45.6"/><path class="gv-mol-grid" d="M18.5 20.3C13.7 26 13.7 38 18.5 43.7"/><path class="gv-mol-grid" d="M45.5 20.3C50.3 26 50.3 38 45.5 43.7"/></svg>`;

  function synchronize(){
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!projection||!mollweide)return false;
    [projection,mollweide].forEach(el=>el.classList.remove("gv-7y-sync","gv-7x-sync","gv-7w-sync","gv-pulse-synced"));
    void root.offsetWidth;
    [projection,mollweide].forEach(el=>el.classList.add("gv-7y-sync"));
    return true;
  }

  function apply(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!mollweide)return false;
    if(mollweide.dataset.gv7y!=="true"){
      mollweide.dataset.gv7y="true";
      mollweide.innerHTML=approvedMollweide;
    }
    return synchronize();
  }

  function validate(){
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const mollweide=root.querySelector(".gv-projection-option-icon");
    const pSvg=projection?.querySelector("svg"),mSvg=mollweide?.querySelector("svg");
    if(!projection||!mollweide||!pSvg||!mSvg)return false;
    const p=getComputedStyle(projection),m=getComputedStyle(mollweide),pBefore=getComputedStyle(projection,"::before"),mBefore=getComputedStyle(mollweide,"::before"),ps=getComputedStyle(pSvg),ms=getComputedStyle(mSvg);
    const tile=mollweide.getBoundingClientRect(),svg=mSvg.getBoundingClientRect();
    const exactGeometry=mSvg.innerHTML.includes('rx="25.5" ry="16.5"')&&mSvg.innerHTML.includes('M11 32H53')&&mSvg.innerHTML.includes('M45.5 20.3C50.3 26 50.3 38 45.5 43.7');
    const checks={
      projectionTileAnimation:p.animationName==="none",
      mollweideTileAnimation:m.animationName==="none",
      projectionInnerGlow:pBefore.animationName.includes("gv-7y-inner-edge-pulse"),
      mollweideInnerGlow:mBefore.animationName.includes("gv-7y-inner-edge-pulse"),
      sameInnerDuration:pBefore.animationDuration===mBefore.animationDuration&&pBefore.animationDuration==="6.4s",
      projectionStrokeGlow:ps.animationName.includes("gv-7y-icon-stroke-pulse"),
      mollweideStrokeGlow:ms.animationName.includes("gv-7y-icon-stroke-pulse"),
      sameStrokeDuration:ps.animationDuration===ms.animationDuration&&ps.animationDuration==="6.4s",
      mollweideWidth:Math.round(svg.width)===24,
      mollweideHeight:Math.round(svg.height)===24,
      mollweideCentered:Math.abs((tile.left+tile.width/2)-(svg.left+svg.width/2))<1.1&&Math.abs((tile.top+tile.height/2)-(svg.top+svg.height/2))<1.1,
      exactApproved0003Geometry:exactGeometry
    };
    const passed=Object.values(checks).every(Boolean);
    window.GV7Y_VALIDATION={passed,checks,cycle:"6.4s",phase:"simultaneous-class-activation",mollweidePrototype:"0003-exact"};
    if(!passed)throw new Error("GV-BETA-0007Y CONTRACT FAILED "+JSON.stringify(window.GV7Y_VALIDATION));
    return true;
  }

  function run(){if(!apply())return false;requestAnimationFrame(()=>requestAnimationFrame(validate));return true}
  const observer=new MutationObserver(()=>{if(root.querySelector(".gv-projection-option-icon"))requestAnimationFrame(run)});
  observer.observe(root,{subtree:true,childList:true});
  run();
})().catch(error=>console.error("GV-BETA-0007Y STARTUP FAILURE:",error));
"""))

# GV-beta-0007Y staged
