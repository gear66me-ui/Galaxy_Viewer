from IPython.display import HTML, Javascript, display

# GV-beta-0007AA
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AA
# USER REQUEST:
# 1. Do not load or modify the splash animation in this release.
# 2. Center the approved Mollweide icon methodically, not by a guessed offset.
# 3. Keep the approved Mollweide 0003 geometry and 24x24 size.
# 4. Make the inside of both Projection and Mollweide square icon tiles visibly glow.
# 5. Make both SVG drawings glow with exactly the same timing, easing, intensity pattern and phase.
# 6. Preserve Projection geometry, Mollweide geometry, menu layout, text, coordinates, target/SIMBAD, navigation and all unrelated behavior.
# AUTHORIZED CHANGES: viewer/GV-beta-0007AA.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: GV-beta-0007Z baseline behavior except the two authorized corrections: measured Mollweide centering and explicit synchronized interior glow.

display(HTML("""
<style>
:root{--gv-7aa-cycle:6.4s}

#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon,
#aladin-cosmic-command-test .gv-projection-option-icon{
  position:relative!important;
  overflow:hidden!important;
  isolation:isolate!important;
  background:#020408!important;
  animation:none!important;
}

/* Disable inherited pseudo-element animation. 7AA uses a real DOM inset layer so the glow is guaranteed to render inside the tile. */
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon::before,
#aladin-cosmic-command-test .gv-projection-option-icon::before{
  animation:none!important;
  box-shadow:none!important;
  background:transparent!important;
}

#aladin-cosmic-command-test .gv-7aa-inset{
  position:absolute!important;
  inset:1px!important;
  z-index:0!important;
  border-radius:5px!important;
  pointer-events:none!important;
  background:rgba(0,0,0,0);
  box-shadow:inset 0 0 0 1px rgba(143,234,255,.08),inset 0 0 2.6px rgba(98,216,255,.05),inset 0 0 4.5px rgba(157,124,255,.03);
  animation:none!important;
}

#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg,
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  position:relative!important;
  z-index:1!important;
  animation:none!important;
}

#aladin-cosmic-command-test .gv-projection-option-icon{
  display:grid!important;
  place-items:center!important;
}

#aladin-cosmic-command-test .gv-projection-option-icon svg{
  width:24px!important;
  height:24px!important;
  margin:0!important;
  transform:var(--gv-7aa-center-transform,none)!important;
  transform-origin:center center!important;
}

#aladin-cosmic-command-test .gv-7aa-active > .gv-7aa-inset{
  animation:gv-7aa-innerPulse var(--gv-7aa-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}
#aladin-cosmic-command-test .gv-7aa-active > svg{
  animation:gv-7aa-iconPulse var(--gv-7aa-cycle) cubic-bezier(.42,0,.18,1) infinite!important;
}

@keyframes gv-7aa-innerPulse{
  0%,100%{background:rgba(0,0,0,0);box-shadow:inset 0 0 0 1px rgba(143,234,255,.08),inset 0 0 2.6px rgba(98,216,255,.05),inset 0 0 4.5px rgba(157,124,255,.03)}
  24%{background:rgba(79,166,255,.025);box-shadow:inset 0 0 0 1px rgba(143,234,255,.24),inset 0 0 3.75px rgba(98,216,255,.16),inset 0 0 6px rgba(157,124,255,.09)}
  52%{background:rgba(79,166,255,.055);box-shadow:inset 0 0 0 1px rgba(214,249,255,.95),inset 0 0 3.75px rgba(143,234,255,.82),inset 0 0 7.1px rgba(79,166,255,.58),inset 0 0 10.5px rgba(157,124,255,.30)}
  76%{background:rgba(79,166,255,.03);box-shadow:inset 0 0 0 1px rgba(143,234,255,.26),inset 0 0 3.75px rgba(98,216,255,.17),inset 0 0 6px rgba(157,124,255,.10)}
}

@keyframes gv-7aa-iconPulse{
  0%,100%{opacity:.56;filter:drop-shadow(0 0 1px rgba(143,234,255,.16))}
  24%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
  52%{opacity:1;filter:drop-shadow(0 0 4px rgba(214,249,255,1)) drop-shadow(0 0 8px rgba(98,216,255,.90)) drop-shadow(0 0 13px rgba(79,166,255,.76)) drop-shadow(0 0 17px rgba(157,124,255,.48))}
  76%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.34)) drop-shadow(0 0 4px rgba(157,124,255,.20))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007Z.py?v=e5536e55880ef765a3631d0ca3a543baedb12c4f";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AA STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007Z RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AA COULD NOT EXTRACT 7Z BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AA";
  const projection=await waitFor(()=>root.querySelector(".gv-viewer-menu-icon.gv-projection-icon"));

  const oldClasses=["gv-7y-sync","gv-7x-sync","gv-7w-sync","gv-pulse-synced","gv-7z-glow","gv-7aa-active"];

  function clearOld(el){if(!el)return;oldClasses.forEach(name=>el.classList.remove(name));}

  function ensureInset(el){
    if(!el)return null;
    let layer=el.querySelector(":scope > .gv-7aa-inset");
    if(!layer){layer=document.createElement("span");layer.className="gv-7aa-inset";layer.setAttribute("aria-hidden","true");el.insertBefore(layer,el.firstChild);}
    return layer;
  }

  function paintedCenter(svg){
    const tile=svg.parentElement;
    const tileRect=tile.getBoundingClientRect();
    const svgRect=svg.getBoundingClientRect();
    const box=svg.getBBox();
    const vb=svg.viewBox.baseVal;
    const sx=svgRect.width/vb.width, sy=svgRect.height/vb.height;
    return {
      tileX:tileRect.left+tileRect.width/2,
      tileY:tileRect.top+tileRect.height/2,
      paintX:svgRect.left+(box.x+box.width/2-vb.x)*sx,
      paintY:svgRect.top+(box.y+box.height/2-vb.y)*sy,
      tileRect,svgRect,box,vb,sx,sy
    };
  }

  function centerMollweide(){
    const tile=root.querySelector(".gv-projection-option-icon");
    const svg=tile?.querySelector("svg");
    if(!tile||!svg)return null;
    svg.style.setProperty("--gv-7aa-center-transform","none");
    void svg.getBoundingClientRect();
    const before=paintedCenter(svg);
    const dx=before.tileX-before.paintX;
    const dy=before.tileY-before.paintY;
    svg.style.setProperty("--gv-7aa-center-transform",`translate(${dx.toFixed(3)}px,${dy.toFixed(3)}px)`);
    void svg.getBoundingClientRect();
    const after=paintedCenter(svg);
    return {dx,dy,errorX:after.tileX-after.paintX,errorY:after.tileY-after.paintY};
  }

  function startProjection(){
    clearOld(projection);ensureInset(projection);void root.offsetWidth;projection.classList.add("gv-7aa-active");
  }

  function synchronizePair(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    if(!mollweide){startProjection();return false;}
    ensureInset(projection);ensureInset(mollweide);
    clearOld(projection);clearOld(mollweide);
    centerMollweide();
    void root.offsetWidth;
    projection.classList.add("gv-7aa-active");
    mollweide.classList.add("gv-7aa-active");
    return true;
  }

  function validate(){
    const mollweide=root.querySelector(".gv-projection-option-icon");
    const pInset=projection.querySelector(":scope > .gv-7aa-inset");
    const pSvg=projection.querySelector("svg");
    if(!pInset||!pSvg)return false;
    const pi=getComputedStyle(pInset),ps=getComputedStyle(pSvg);
    const checks={
      projectionExplicitInset:!!pInset,
      projectionInteriorAnimation:pi.animationName.includes("gv-7aa-innerPulse"),
      projectionInteriorDuration:pi.animationDuration==="6.4s",
      projectionIconAnimation:ps.animationName.includes("gv-7aa-iconPulse"),
      projectionIconDuration:ps.animationDuration==="6.4s"
    };
    let centering=null;
    if(mollweide){
      const mInset=mollweide.querySelector(":scope > .gv-7aa-inset"),mSvg=mollweide.querySelector("svg");
      const mi=getComputedStyle(mInset),ms=getComputedStyle(mSvg);
      centering=centerMollweide();
      Object.assign(checks,{
        mollweideExplicitInset:!!mInset,
        mollweideInteriorAnimation:mi.animationName.includes("gv-7aa-innerPulse"),
        mollweideInteriorDuration:mi.animationDuration==="6.4s",
        mollweideIconAnimation:ms.animationName.includes("gv-7aa-iconPulse"),
        mollweideIconDuration:ms.animationDuration==="6.4s",
        identicalInteriorAnimation:pi.animationName===mi.animationName,
        identicalInteriorDuration:pi.animationDuration===mi.animationDuration,
        identicalIconAnimation:ps.animationName===ms.animationName,
        identicalIconDuration:ps.animationDuration===ms.animationDuration,
        mollweideWidth:Math.round(mSvg.getBoundingClientRect().width)===24,
        mollweideHeight:Math.round(mSvg.getBoundingClientRect().height)===24,
        mollweideMeasuredCenter:Math.abs(centering.errorX)<0.40&&Math.abs(centering.errorY)<0.40,
        exactApproved0003Geometry:mSvg.innerHTML.includes('rx="25.5" ry="16.5"')&&mSvg.innerHTML.includes('M11 32H53')&&mSvg.innerHTML.includes('M45.5 20.3C50.3 26 50.3 38 45.5 43.7')
      });
    }
    const passed=Object.values(checks).every(Boolean);
    window.GV7AA_VALIDATION={passed,checks,centering,cycle:"6.4s",phase:mollweide?"simultaneous-pair-restart":"projection-standalone",splash:"unchanged-not-loaded-by-7AA"};
    if(!passed)throw new Error("GV-BETA-0007AA CONTRACT FAILED "+JSON.stringify(window.GV7AA_VALIDATION));
    return true;
  }

  startProjection();
  requestAnimationFrame(()=>requestAnimationFrame(validate));

  const observer=new MutationObserver(()=>{
    if(root.querySelector(".gv-projection-option-icon")){
      requestAnimationFrame(()=>{synchronizePair();requestAnimationFrame(()=>requestAnimationFrame(validate));});
    }
  });
  observer.observe(root,{subtree:true,childList:true});
})().catch(error=>console.error("GV-BETA-0007AA STARTUP FAILURE:",error));
"""))

# GV-beta-0007AA staged
