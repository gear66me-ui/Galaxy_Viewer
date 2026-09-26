from IPython.display import HTML, Javascript, display

# GV-beta-0007V
# GALAXY VIEWER CHANGE ORDER
# USER INSTRUCTION: Projection tile and Mollweide tile must glow INSIDE only, never by an animated outer halo. Both tile interiors and both icons must pulse in exact unison: same start, same end, same cycle, same phase. Mollweide preview must use a more authentic pointed all-sky ellipse instead of a rounded watermelon shape.
# AUTHORIZED CHANGES: Create standalone viewer/GV-beta-0007V.py from GV-beta-0007U.py behavior. Projection/Mollweide pulse and Mollweide preview geometry only.
# PRESERVED BEHAVIOR: Hamburger, target/SIMBAD, Aladin initialization, coordinate overlay/font, galaxy navigation, all unrelated menu rows and behavior.

display(HTML("""
<style>
:root{--gv-projection-cycle:6.4s}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon,
#aladin-cosmic-command-test .gv-projection-option-icon{
  position:relative!important;
  overflow:hidden!important;
  background:#020408!important;
  box-shadow:0 0 10px rgba(98,216,255,.38)!important;
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
  opacity:.48!important;
  background:radial-gradient(ellipse at 50% 50%,rgba(79,166,255,.035) 0%,rgba(26,34,54,.025) 42%,rgba(0,0,0,0) 76%)!important;
  box-shadow:inset 0 0 7px rgba(98,216,255,.02),inset 0 0 2px rgba(157,124,255,.015)!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg,
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  position:relative!important;
  z-index:1!important;
  animation:none!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon.gv-pulse-synced::before,
#aladin-cosmic-command-test .gv-projection-option-icon.gv-pulse-synced::before{
  animation:gv-projection-interior-pulse var(--gv-projection-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon.gv-pulse-synced svg,
#aladin-cosmic-command-test .gv-projection-option-icon.gv-pulse-synced svg{
  animation:gv-projection-icon-pulse var(--gv-projection-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
@keyframes gv-projection-interior-pulse{
  0%,100%{
    opacity:.48;
    background:radial-gradient(ellipse at 50% 50%,rgba(79,166,255,.035) 0%,rgba(26,34,54,.025) 42%,rgba(0,0,0,0) 76%);
    box-shadow:inset 0 0 7px rgba(98,216,255,.02),inset 0 0 2px rgba(157,124,255,.015);
  }
  24%{
    opacity:.68;
    background:radial-gradient(ellipse at 50% 50%,rgba(79,166,255,.09) 0%,rgba(42,58,92,.055) 46%,rgba(0,0,0,0) 77%);
    box-shadow:inset 0 0 10px rgba(98,216,255,.07),inset 0 0 5px rgba(157,124,255,.045);
  }
  52%{
    opacity:1;
    background:radial-gradient(ellipse at 50% 50%,rgba(96,191,255,.28) 0%,rgba(61,76,138,.18) 36%,rgba(38,25,78,.12) 58%,rgba(0,0,0,0) 80%);
    box-shadow:inset 0 0 18px rgba(98,216,255,.30),inset 0 0 9px rgba(157,124,255,.22),inset 0 0 3px rgba(255,255,255,.13);
  }
  76%{
    opacity:.70;
    background:radial-gradient(ellipse at 50% 50%,rgba(79,166,255,.10) 0%,rgba(42,58,92,.06) 46%,rgba(0,0,0,0) 77%);
    box-shadow:inset 0 0 10px rgba(98,216,255,.075),inset 0 0 5px rgba(157,124,255,.05);
  }
}
@keyframes gv-projection-icon-pulse{
  0%,100%{opacity:.54;filter:drop-shadow(0 0 1px rgba(143,234,255,.16))}
  24%{opacity:.68;filter:drop-shadow(0 0 2px rgba(143,234,255,.28))}
  52%{opacity:1;filter:drop-shadow(0 0 4px rgba(143,234,255,.98)) drop-shadow(0 0 9px rgba(79,166,255,.76)) drop-shadow(0 0 14px rgba(157,124,255,.58))}
  76%{opacity:.68;filter:drop-shadow(0 0 2px rgba(143,234,255,.30))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007U.py?v=5ae7d2eba296b5fb5f04cf237c0e21766bb13d8e";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007V STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});
  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007U RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007V COULD NOT EXTRACT 7U BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7V";

  const pointedMollweide=`<svg viewBox="0 0 64 64" aria-hidden="true"><path class="gv-mol-outline" d="M6 32C10 19 19.5 13.5 32 13.5C44.5 13.5 54 19 58 32C54 45 44.5 50.5 32 50.5C19.5 50.5 10 45 6 32Z"/><path class="gv-mol-grid" d="M6 32H58"/><path class="gv-mol-grid" d="M8.5 25.5C20 21.2 44 21.2 55.5 25.5M8.5 38.5C20 42.8 44 42.8 55.5 38.5"/><path class="gv-mol-grid" d="M32 13.5V50.5"/><path class="gv-mol-grid" d="M32 13.5C23.5 20 22 44 32 50.5M32 13.5C40.5 20 42 44 32 50.5"/><path class="gv-mol-grid" d="M32 13.5C16.5 21 14 43 32 50.5M32 13.5C47.5 21 50 43 32 50.5"/></svg>`;

  function validatePulseContract(projection,mollweide){
    const projectionTile=getComputedStyle(projection),mollweideTile=getComputedStyle(mollweide);
    const projectionInterior=getComputedStyle(projection,"::before"),mollweideInterior=getComputedStyle(mollweide,"::before");
    const projectionSvg=getComputedStyle(projection.querySelector("svg")),mollweideSvg=getComputedStyle(mollweide.querySelector("svg"));
    const failures=[];
    if(projectionTile.animationName!=="none"||mollweideTile.animationName!=="none")failures.push("tile element animation must be none");
    if(projectionInterior.animationName!=="gv-projection-interior-pulse"||mollweideInterior.animationName!=="gv-projection-interior-pulse")failures.push("interior animation name mismatch");
    if(projectionInterior.animationDuration!==mollweideInterior.animationDuration||projectionInterior.animationDuration!=="6.4s")failures.push("interior duration mismatch");
    if(projectionSvg.animationName!=="gv-projection-icon-pulse"||mollweideSvg.animationName!=="gv-projection-icon-pulse")failures.push("icon animation name mismatch");
    if(projectionSvg.animationDuration!==mollweideSvg.animationDuration||projectionSvg.animationDuration!=="6.4s")failures.push("icon duration mismatch");
    if(failures.length)throw new Error("GV-BETA-0007V PULSE CONTRACT FAILED: "+failures.join("; "));
    window.GV7V_VALIDATION={passed:true,cycle:"6.4s",tileAnimation:"none",interiorAnimation:"gv-projection-interior-pulse",iconAnimation:"gv-projection-icon-pulse",phaseReset:"simultaneous-class-activation",mollweideGeometry:"pointed-all-sky"};
    console.info("GV-BETA-0007V PULSE CONTRACT PASS",window.GV7V_VALIDATION);
    return true;
  }

  function synchronizePulse(){
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!projection||!mollweide)return false;
    [projection,mollweide].forEach(el=>el.classList.remove("gv-pulse-synced"));
    void root.offsetWidth;
    [projection,mollweide].forEach(el=>el.classList.add("gv-pulse-synced"));
    requestAnimationFrame(()=>validatePulseContract(projection,mollweide));
    return true;
  }

  function apply(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!mollweide)return false;
    if(mollweide.dataset.gv7v!=="true"){
      mollweide.dataset.gv7v="true";
      mollweide.innerHTML=pointedMollweide;
    }
    return synchronizePulse();
  }

  const observer=new MutationObserver(()=>{if(root.querySelector(".gv-projection-option-icon"))requestAnimationFrame(apply)});
  observer.observe(root,{subtree:true,childList:true});
  apply();
})().catch(error=>console.error("GV-BETA-0007V STARTUP FAILURE:",error));
"""))

# GV-beta-0007V staged
