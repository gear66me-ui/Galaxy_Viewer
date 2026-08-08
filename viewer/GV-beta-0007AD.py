from IPython.display import HTML, Javascript, display

# GV-beta-0007AD
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AD
# PURPOSE: Make the left main menu and right Projection submenu mathematically symmetric and dim inactive left rows while Projection mode is open.
# USER REQUEST:
# 1. Use the exact same calculated long-tile width on the left and right columns.
# 2. Use the exact same square icon size, text-to-icon gap, vertical row gap, and disciplined inter-column gap on both sides.
# 3. Calculate widths from measured runtime geometry; do not eyeball or hard-code the long-tile width.
# 4. Align the full two-column menu from the existing left-menu edge to the measured right edge of the top target button without overlap.
# 5. Preserve the existing Space Age font family and use the added width so labels no longer look squeezed; no font files may change.
# 6. While Projection mode is open, visually gray/dim LAYERS, GRID, SURVEY, and RETICLE ON/OFF; those inactive rows must not glow or pulse.
# 7. Keep the Projection main row visually active and preserve the inherited Projection/Mollweide synchronized glow exactly.
# 8. Preserve the five right-side projection rows/order and keep the four new right icon tiles empty and unwired.
# 9. Preserve coordinates, hamburger, target/SIMBAD, Aladin, galaxy navigation, bottom controls, splash absence, artwork, fonts, workflows, modules, and all unrelated behavior.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AD.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: GV-beta-0007AC baseline except the authorized symmetric menu geometry, label sizing/spacing, Projection-mode dimming, and V-7AD version label.

display(HTML("""
<style>
#aladin-cosmic-command-test.gv-7ad-projection-mode .gv-viewer-menu > .gv-viewer-menu-row:not(:first-child) .gv-viewer-menu-label,
#aladin-cosmic-command-test.gv-7ad-projection-mode .gv-viewer-menu > .gv-viewer-menu-row:not(:first-child) .gv-viewer-menu-icon{
  opacity:.42!important;
  filter:grayscale(1) saturate(.12) brightness(.58)!important;
  box-shadow:0 0 4px rgba(120,150,165,.10)!important;
  animation:none!important;
}
#aladin-cosmic-command-test.gv-7ad-projection-mode .gv-viewer-menu > .gv-viewer-menu-row:not(:first-child) .gv-viewer-menu-icon *,
#aladin-cosmic-command-test.gv-7ad-projection-mode .gv-viewer-menu > .gv-viewer-menu-row:not(:first-child) .gv-viewer-menu-label *{
  animation:none!important;
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007AC.py?v=3c74f216768dd6c8cede63fc51e76b71d8da40d2";
  const LABELS=["MOLLWEIDE","SPHERICAL","ORTHOGRAPHIC","TANGENTIAL","SINUSOIDAL"];
  const TOL=.50;
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AD STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AC RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AD COULD NOT EXTRACT 7AC BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AD";

  const px=v=>`${Number(v).toFixed(3)}px`;
  function collect(){
    const leftMenu=root.querySelector(".gv-viewer-menu");
    const leftRows=[...leftMenu?.querySelectorAll(":scope > .gv-viewer-menu-row")||[]];
    const rightMenu=root.querySelector(".gv-projection-submenu");
    const rightRows=[...rightMenu?.querySelectorAll(":scope > .gv-projection-option-row")||[]];
    const target=root.querySelector("button.gv-target-proxy");
    return {leftMenu,leftRows,rightMenu,rightRows,target};
  }

  function applySymmetry(){
    const {leftMenu,leftRows,rightMenu,rightRows,target}=collect();
    if(!leftMenu||leftRows.length!==5||!rightMenu||rightRows.length!==5||!target)return null;
    const leftLabels=leftRows.map(r=>r.querySelector(".gv-viewer-menu-label"));
    const leftIcons=leftRows.map(r=>r.querySelector(".gv-viewer-menu-icon"));
    const rightLabels=rightRows.map(r=>r.querySelector(".gv-projection-option-label"));
    const rightIcons=rightRows.map(r=>r.querySelector(".gv-projection-option-icon"));
    if([...leftLabels,...leftIcons,...rightLabels,...rightIcons].some(v=>!v))return null;

    const rootRect=root.getBoundingClientRect();
    const leftRect=leftMenu.getBoundingClientRect();
    const firstLabelRect=leftLabels[0].getBoundingClientRect();
    const firstIconRect=leftIcons[0].getBoundingClientRect();
    const targetRect=target.getBoundingClientRect();
    const leftStart=leftRect.left-rootRect.left;
    const rightBoundary=Math.min(rootRect.width,targetRect.right-rootRect.left);
    const A=rightBoundary-leftStart;
    const S=firstIconRect.width;
    const G=firstIconRect.left-firstLabelRect.right;
    const C=G;
    const W=(A-(2*S)-(2*G)-C)/2;
    if(!(A>0&&S>0&&G>=0&&W>0))throw new Error("GV-BETA-0007AD INVALID GEOMETRY "+JSON.stringify({A,S,G,C,W}));
    const groupWidth=W+G+S;
    const rightLeft=leftStart+groupWidth+C;

    leftMenu.style.setProperty("width",px(groupWidth),"important");
    leftRows.forEach(row=>{
      row.style.setProperty("grid-template-columns",`${px(W)} ${px(S)}`,"important");
      row.style.setProperty("column-gap",px(G),"important");
      row.style.setProperty("width",px(groupWidth),"important");
      row.style.setProperty("height",px(S),"important");
    });
    leftLabels.forEach(label=>{
      ["width","min-width","max-width"].forEach(p=>label.style.setProperty(p,px(W),"important"));
      ["height","min-height","max-height"].forEach(p=>label.style.setProperty(p,px(S),"important"));
      label.style.setProperty("font-size","12px","important");
      label.style.setProperty("letter-spacing",".55px","important");
    });
    leftIcons.forEach(icon=>{
      ["width","min-width","max-width","height","min-height","max-height"].forEach(p=>icon.style.setProperty(p,px(S),"important"));
    });

    rightMenu.style.setProperty("left",px(rightLeft),"important");
    rightMenu.style.setProperty("width",px(groupWidth),"important");
    rightMenu.style.setProperty("gap",px(G),"important");
    rightRows.forEach(row=>{
      row.style.setProperty("grid-template-columns",`${px(W)} ${px(S)}`,"important");
      row.style.setProperty("column-gap",px(G),"important");
      row.style.setProperty("width",px(groupWidth),"important");
      row.style.setProperty("height",px(S),"important");
      row.style.setProperty("flex-basis",px(S),"important");
    });
    rightLabels.forEach(label=>{
      ["width","min-width","max-width"].forEach(p=>label.style.setProperty(p,px(W),"important"));
      ["height","min-height","max-height"].forEach(p=>label.style.setProperty(p,px(S),"important"));
      label.style.setProperty("font-size","12px","important");
      label.style.setProperty("letter-spacing",".55px","important");
    });
    rightIcons.forEach(icon=>{
      ["width","min-width","max-width","height","min-height","max-height"].forEach(p=>icon.style.setProperty(p,px(S),"important"));
    });
    return {A,S,G,C,W,groupWidth,leftStart,rightBoundary,rightLeft};
  }

  function setProjectionMode(){
    const {rightMenu}=collect();
    const open=!!rightMenu?.classList.contains("gv-open");
    root.classList.toggle("gv-7ad-projection-mode",open);
    return open;
  }

  function validate(){
    const geometry=applySymmetry();
    const {leftMenu,leftRows,rightMenu,rightRows,target}=collect();
    if(!geometry||leftRows.length!==5||rightRows.length!==5)return false;
    const leftLabels=leftRows.map(r=>r.querySelector(".gv-viewer-menu-label"));
    const leftIcons=leftRows.map(r=>r.querySelector(".gv-viewer-menu-icon"));
    const rightLabels=rightRows.map(r=>r.querySelector(".gv-projection-option-label"));
    const rightIcons=rightRows.map(r=>r.querySelector(".gv-projection-option-icon"));
    const lLabelRects=leftLabels.map(e=>e.getBoundingClientRect());
    const rLabelRects=rightLabels.map(e=>e.getBoundingClientRect());
    const lIconRects=leftIcons.map(e=>e.getBoundingClientRect());
    const rIconRects=rightIcons.map(e=>e.getBoundingClientRect());
    const labelNames=rightLabels.map(e=>(e.textContent||"").trim().toUpperCase());
    const leftRowRects=leftRows.map(e=>e.getBoundingClientRect());
    const rightRowRects=rightRows.map(e=>e.getBoundingClientRect());
    const leftGaps=leftRowRects.slice(1).map((r,i)=>r.top-leftRowRects[i].bottom);
    const rightGaps=rightRowRects.slice(1).map((r,i)=>r.top-rightRowRects[i].bottom);
    const leftTextIconGaps=lIconRects.map((r,i)=>r.left-lLabelRects[i].right);
    const rightTextIconGaps=rIconRects.map((r,i)=>r.left-rLabelRects[i].right);
    const maxLabelDelta=Math.max(...lLabelRects.flatMap(l=>rLabelRects.map(r=>Math.abs(l.width-r.width))));
    const allIconRects=[...lIconRects,...rIconRects];
    const maxIconDelta=Math.max(...allIconRects.flatMap(a=>allIconRects.map(b=>Math.max(Math.abs(a.width-b.width),Math.abs(a.height-b.height)))));
    const equationResidual=Math.abs((2*geometry.W+2*geometry.S+2*geometry.G+geometry.C)-geometry.A);
    const rightEdge=rIconRects[0].right;
    const targetRect=target.getBoundingClientRect();
    const boundaryError=Math.abs(rightEdge-targetRect.right);
    const open=setProjectionMode();
    const inactive=leftRows.slice(1);
    const inactiveDimmed=inactive.every(row=>Number(getComputedStyle(row.querySelector(".gv-viewer-menu-label")).opacity)<=.43&&Number(getComputedStyle(row.querySelector(".gv-viewer-menu-icon")).opacity)<=.43);
    const inactiveNoPulse=inactive.every(row=>row.getAnimations({subtree:true}).filter(a=>a.playState==="running").length===0);
    const projection=leftIcons[0];
    const mollweide=rightIcons[0];
    const projectionAnimations=projection.getAnimations({subtree:true}).filter(a=>a.playState==="running");
    const mollweideAnimations=mollweide.getAnimations({subtree:true}).filter(a=>a.playState==="running");
    const checks={
      versionLabel:versionLabel.textContent==="V-7AD",
      exactlyFiveLeftRows:leftRows.length===5,
      exactlyFiveRightRows:rightRows.length===5,
      projectionLabelOrder:JSON.stringify(labelNames)===JSON.stringify(LABELS),
      fourNewRightIconsEmpty:rightIcons.slice(1).every(i=>i.innerHTML.trim()===""),
      mollweideSvgPresent:!!mollweide.querySelector("svg"),
      equalLongTileWidths:maxLabelDelta<=TOL,
      equalSquareDimensions:maxIconDelta<=TOL&&allIconRects.every(r=>Math.abs(r.width-r.height)<=TOL),
      matchingTextIconGaps:[...leftTextIconGaps,...rightTextIconGaps].every(g=>Math.abs(g-geometry.G)<=TOL),
      matchingVerticalGaps:[...leftGaps,...rightGaps].every(g=>Math.abs(g-geometry.G)<=TOL),
      equationReconciles:equationResidual<=.01,
      labelTolerance:maxLabelDelta<=TOL,
      squareTolerance:maxIconDelta<=TOL,
      rightBoundaryAligned:boundaryError<=TOL,
      menuBelowTargetNoOverlap:rightRowRects[0].top>=targetRect.bottom-1,
      inactiveRowsDimmed:!open||inactiveDimmed,
      inactiveRowsNoGlow:!open||inactiveNoPulse,
      projectionMainActive:!open||leftRows[0].classList.contains("gv-selected"),
      projectionGlowRunning:projectionAnimations.length>=2,
      mollweideGlowRunning:mollweideAnimations.length>=2,
      noNewProjectionActions:rightRows.slice(1).every(r=>!r.querySelector("[onclick]")),
      splashNotLoaded:!document.querySelector('[src*="Singularity"],[href*="Singularity"]'),
      noDuplicateRightRows:new Set(labelNames).size===5
    };
    const passed=Object.values(checks).every(Boolean);
    window.GV7AD_VALIDATION={passed,checks,geometry:{...geometry,equationResidual,boundaryError,maxLabelDelta,maxIconDelta,leftTextIconGaps,rightTextIconGaps,leftGaps,rightGaps},projectionModeOpen:open,tolerancePx:TOL,splash:"not loaded",newProjectionActions:"not wired"};
    if(!passed)throw new Error("GV-BETA-0007AD CONTRACT FAILED "+JSON.stringify(window.GV7AD_VALIDATION));
    return true;
  }

  function apply(){
    const geometry=applySymmetry();
    if(!geometry)return false;
    setProjectionMode();
    requestAnimationFrame(()=>requestAnimationFrame(validate));
    return true;
  }

  const observer=new MutationObserver(()=>requestAnimationFrame(apply));
  observer.observe(root,{subtree:true,childList:true,attributes:true,attributeFilter:["class"]});
  window.addEventListener("resize",()=>requestAnimationFrame(apply),{passive:true});
  apply();
})().catch(error=>console.error("GV-BETA-0007AD STARTUP FAILURE:",error));
"""))

# GV-beta-0007AD staged
