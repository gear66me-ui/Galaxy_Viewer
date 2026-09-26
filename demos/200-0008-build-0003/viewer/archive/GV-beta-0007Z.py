from IPython.display import HTML, Javascript, display

# GV-beta-0007Z
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007Z
# USER REQUEST:
# 1. Restore the Mollweide glow behavior to match the approved standalone mollweide-icon-glow-0003.html pattern.
# 2. Make the left Projection icon tile actually glow using the same approved glow treatment.
# 3. Projection and Mollweide must use one identical disciplined glow system: same colors, intensity, inset depth, SVG bloom, 6.4s timing, easing, start/end and phase.
# 4. Projection must glow even before the Mollweide submenu exists; when Mollweide appears, both restart together in phase.
# 5. Do not change Projection geometry, Mollweide geometry, Mollweide size/centering, submenu layout, text, coordinates, target/SIMBAD, navigation or unrelated behavior.
# AUTHORIZED CHANGES: viewer/GV-beta-0007Z.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: GV-beta-0007Y baseline behavior except the two authorized glow corrections above.

display(HTML("""
<style>
:root{--gv-7z-cycle:6.4s}

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
  animation:none!important;
}

/* One identical glow definition for BOTH tiles. Values are the approved prototype pattern scaled from 96px prototype tile to the 36px viewer tile. */
#aladin-cosmic-command-test .gv-7z-glow::before{
  animation:gv-7z-innerPulse var(--gv-7z-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
#aladin-cosmic-command-test .gv-7z-glow svg{
  animation:gv-7z-iconPulse var(--gv-7z-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}

@keyframes gv-7z-innerPulse{
  0%,100%{
    background:rgba(0,0,0,0);
    box-shadow:inset 0 0 0 1px rgba(143,234,255,.08),inset 0 0 2.6px rgba(98,216,255,.05),inset 0 0 4.5px rgba(157,124,255,.03);
  }
  24%{
    background:rgba(79,166,255,.025);
    box-shadow:inset 0 0 0 1px rgba(143,234,255,.24),inset 0 0 3.75px rgba(98,216,255,.16),inset 0 0 6px rgba(157,124,255,.09);
  }
  52%{
    background:rgba(79,166,255,.055);
    box-shadow:inset 0 0 0 1px rgba(214,249,255,.95),inset 0 0 3.75px rgba(143,234,255,.82),inset 0 0 7.1px rgba(79,166,255,.58),inset 0 0 10.5px rgba(157,124,255,.30);
  }
  76%{
    background:rgba(79,166,255,.03);
    box-shadow:inset 0 0 0 1px rgba(143,234,255,.26),inset 0 0 3.75px rgba(98,216,255,.17),inset 0 0 6px rgba(157,124,255,.10);
  }
}

@keyframes gv-7z-iconPulse{
  0%,100%{opacity:.56;filter:drop-shadow(0 0 1px rgba(143,234,255,.16))}
  24%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
  52%{opacity:1;filter:drop-shadow(0 0 4px rgba(214,249,255,1)) drop-shadow(0 0 8px rgba(98,216,255,.90)) drop-shadow(0 0 13px rgba(79,166,255,.76)) drop-shadow(0 0 17px rgba(157,124,255,.48))}
  76%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007Y.py?v=d5360e9c12783810d1da8a1b27a5084e1221b57e";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007Z STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007Y RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007Z COULD NOT EXTRACT 7Y BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7Z";

  const projection=await waitFor(()=>root.querySelector(".gv-viewer-menu-icon.gv-projection-icon"));

  function clearOld(el){
    if(!el)return;
    el.classList.remove("gv-7y-sync","gv-7x-sync","gv-7w-sync","gv-pulse-synced","gv-7z-glow");
  }

  function startProjectionStandalone(){
    clearOld(projection);
    void root.offsetWidth;
    projection.classList.add("gv-7z-glow");
  }

  function synchronizePair(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!mollweide){startProjectionStandalone();return false;}
    clearOld(projection);clearOld(mollweide);
    void root.offsetWidth;
    projection.classList.add("gv-7z-glow");
    mollweide.classList.add("gv-7z-glow");
    return true;
  }

  function validate(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    const pSvg=projection.querySelector("svg");
    if(!pSvg)return false;
    const pBefore=getComputedStyle(projection,"::before"),ps=getComputedStyle(pSvg);
    const checks={
      projectionInterior:pBefore.animationName.includes("gv-7z-innerPulse"),
      projectionInteriorDuration:pBefore.animationDuration==="6.4s",
      projectionIcon:ps.animationName.includes("gv-7z-iconPulse"),
      projectionIconDuration:ps.animationDuration==="6.4s"
    };
    if(mollweide){
      const mSvg=mollweide.querySelector("svg"),mBefore=getComputedStyle(mollweide,"::before"),ms=getComputedStyle(mSvg);
      Object.assign(checks,{
        mollweideInterior:mBefore.animationName.includes("gv-7z-innerPulse"),
        mollweideInteriorDuration:mBefore.animationDuration==="6.4s",
        mollweideIcon:ms.animationName.includes("gv-7z-iconPulse"),
        mollweideIconDuration:ms.animationDuration==="6.4s",
        sameInteriorAnimation:pBefore.animationName===mBefore.animationName,
        sameInteriorDuration:pBefore.animationDuration===mBefore.animationDuration,
        sameIconAnimation:ps.animationName===ms.animationName,
        sameIconDuration:ps.animationDuration===ms.animationDuration
      });
    }
    const passed=Object.values(checks).every(Boolean);
    window.GV7Z_VALIDATION={passed,checks,cycle:"6.4s",phase:mollweide?"simultaneous-pair-restart":"projection-standalone"};
    if(!passed)throw new Error("GV-BETA-0007Z CONTRACT FAILED "+JSON.stringify(window.GV7Z_VALIDATION));
    return true;
  }

  startProjectionStandalone();
  requestAnimationFrame(()=>requestAnimationFrame(validate));

  const observer=new MutationObserver(()=>{
    if(root.querySelector(".gv-projection-option-icon")){
      requestAnimationFrame(()=>{synchronizePair();requestAnimationFrame(()=>requestAnimationFrame(validate));});
    }
  });
  observer.observe(root,{subtree:true,childList:true});
})().catch(error=>console.error("GV-BETA-0007Z STARTUP FAILURE:",error));
"""))

# GV-beta-0007Z staged
