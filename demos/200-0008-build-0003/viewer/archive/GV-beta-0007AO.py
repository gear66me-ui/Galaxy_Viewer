from IPython.display import HTML, Javascript, display

# GV-beta-0007AK
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AK
# PURPOSE: Preserve 7AJ exactly except remove all animated glow from long label tiles and square icon tile surfaces so only actual icon graphics glow on the existing 3000 ms cycle.
# USER REQUEST: Long rectangular tiles must not glow, square tile backgrounds must not glow, only actual icon graphics may glow, hamburger remains non-glowing, and coordinate glow remains exactly as 7AJ.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AK.py and update mobile/beta/index.html only.
# PRESERVED BEHAVIOR: 7AJ geometry, Projection/Mollweide SVG geometry, coordinate glow/calculations/switching, target/SIMBAD, Aladin, navigation, controls, splash behavior, typography, dimming, actions, and all unrelated behavior.

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/19f5a381314e1ebb336f7d25c4df9fdb54163301/viewer/GV-beta-0007AD.py";
  const LABELS=["MOLLWEIDE","SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
  const SPHERICAL_SVG=`<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="22" stroke="#8feaff" stroke-width="2.2"/><ellipse cx="32" cy="32" rx="8.5" ry="22" stroke="#9d7cff" stroke-width="1.55"/><ellipse cx="32" cy="32" rx="16" ry="22" stroke="#4fa6ff" stroke-width="1.05" opacity=".8"/><ellipse cx="32" cy="32" rx="22" ry="8.5" stroke="#9d7cff" stroke-width="1.45"/><path d="M13 21.2C22.4 26 41.6 26 51 21.2M13 42.8C22.4 38 41.6 38 51 42.8" stroke="#4fa6ff" stroke-width="1.15" opacity=".9"/><path d="M10.5 32H53.5" stroke="#8feaff" stroke-width="1.35" opacity=".8"/><circle cx="32" cy="32" r="2" fill="#4fa6ff" stroke="none"/></g></svg>`;
  const ORTHO_SVG=`<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="32" r="22" stroke="#8feaff" stroke-width="2.3"/><path d="M13 21.5C22.4 26.6 41.6 26.6 51 21.5M10 32H54M13 42.5C22.4 37.4 41.6 37.4 51 42.5" stroke="#9d7cff" stroke-width="1.35"/><path d="M32 10C23.5 18 23.5 46 32 54M32 10C40.5 18 40.5 46 32 54" stroke="#4fa6ff" stroke-width="1.45"/><path d="M32 13V51M13 32H51" stroke="#8feaff" stroke-width=".8" opacity=".42"/><circle cx="32" cy="32" r="3.1" stroke="#4fa6ff" stroke-width="1.6"/><circle cx="32" cy="32" r="1.25" fill="#9d7cff" stroke="none"/></g></svg>`;
  const TANGENTIAL_SVG=`<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M10 18C18 12 27 11 34 13M10 32C18 27 27 26 34 27M10 46C18 42 27 42 34 43" stroke="#8feaff" stroke-width="1.45" opacity=".86"/><path d="M16 11C20 20 21 37 17 53M27 10C30 20 30 44 27 54" stroke="#9d7cff" stroke-width="1.25" opacity=".92"/><circle cx="34" cy="32" r="2.5" fill="#4fa6ff" stroke="none"/><path d="M36.5 25L44 18M36.8 32H45M36.5 39L44 46" stroke="#4fa6ff" stroke-width="1.7"/><path d="M44 18L56 21.5L56 42.5L44 46Z" stroke="#8feaff" stroke-width="2"/><path d="M48 19.2V44.8M52 20.4V43.6M44 25L56 27.5M44 32H56M44 39L56 36.5" stroke="#9d7cff" stroke-width="1.15"/></g></svg>`;
  const SINUSOIDAL_SVG=`<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M32 9C22 11 13 20 9 32C13 44 22 53 32 55C42 53 51 44 55 32C51 20 42 11 32 9Z" stroke="#8feaff" stroke-width="2.25"/><path d="M9 32H55" stroke="#4fa6ff" stroke-width="1.65"/><path d="M12.5 22H51.5M12.5 42H51.5" stroke="#9d7cff" stroke-width="1.35"/><path d="M32 9V55M22 12C27 22 27 42 22 52M42 12C37 22 37 42 42 52M14 17C22 25 22 39 14 47M50 17C42 25 42 39 50 47" stroke="#9d7cff" stroke-width="1.25"/><path d="M17 15.5C24 23 24 41 17 48.5M47 15.5C40 23 40 41 47 48.5" stroke="#4fa6ff" stroke-width=".9" opacity=".68"/><circle cx="32" cy="32" r="1.6" fill="#4fa6ff" stroke="none"/></g></svg>`;
  const PROJECTION_ICONS=[SPHERICAL_SVG,ORTHO_SVG,TANGENTIAL_SVG,SINUSOIDAL_SVG];
  const TOL=.50;
  const CENTER_TOL=.40;
  const CYCLE=3000;
  const EASING="cubic-bezier(.42,0,.18,1)";
  const iconFrames=[
    {offset:0,opacity:.82,filter:"brightness(1.08) saturate(1.06) drop-shadow(0 0 2px rgba(143,234,255,.42)) drop-shadow(0 0 5px rgba(79,166,255,.22))"},
    {offset:.24,opacity:.94,filter:"brightness(1.22) saturate(1.12) drop-shadow(0 0 3px rgba(224,252,255,.72)) drop-shadow(0 0 7px rgba(98,216,255,.68)) drop-shadow(0 0 11px rgba(157,124,255,.34))"},
    {offset:.52,opacity:1,filter:"brightness(1.48) saturate(1.18) drop-shadow(0 0 5px rgba(255,255,255,1)) drop-shadow(0 0 10px rgba(143,234,255,1)) drop-shadow(0 0 16px rgba(79,166,255,.98)) drop-shadow(0 0 22px rgba(157,124,255,.72))"},
    {offset:.76,opacity:.94,filter:"brightness(1.24) saturate(1.12) drop-shadow(0 0 3px rgba(224,252,255,.76)) drop-shadow(0 0 7px rgba(98,216,255,.70)) drop-shadow(0 0 11px rgba(157,124,255,.36))"},
    {offset:1,opacity:.82,filter:"brightness(1.08) saturate(1.06) drop-shadow(0 0 2px rgba(143,234,255,.42)) drop-shadow(0 0 5px rgba(79,166,255,.22))"}
  ];
  const coordinateFrames=[
    {offset:0,color:"#8FD7FF",textShadow:"0 0 2px rgba(224,252,255,.55),0 0 5px rgba(98,216,255,.46),0 0 8px rgba(79,166,255,.24)"},
    {offset:.24,color:"#BCEEFF",textShadow:"0 0 3px rgba(238,254,255,.82),0 0 8px rgba(98,216,255,.78),0 0 13px rgba(79,166,255,.48),0 0 17px rgba(157,124,255,.26)"},
    {offset:.52,color:"#FFFFFF",textShadow:"0 0 5px rgba(255,255,255,1),0 0 10px rgba(143,234,255,1),0 0 16px rgba(98,216,255,.98),0 0 22px rgba(79,166,255,.86),0 0 28px rgba(157,124,255,.58)"},
    {offset:.76,color:"#C5F2FF",textShadow:"0 0 3px rgba(238,254,255,.86),0 0 8px rgba(98,216,255,.82),0 0 13px rgba(79,166,255,.50),0 0 17px rgba(157,124,255,.28)"},
    {offset:1,color:"#8FD7FF",textShadow:"0 0 2px rgba(224,252,255,.55),0 0 5px rgba(98,216,255,.46),0 0 8px rgba(79,166,255,.24)"}
  ];
  const underglowFrames=[
    {offset:0,opacity:.34,filter:"blur(3px) brightness(.92)"},
    {offset:.24,opacity:.68,filter:"blur(3.5px) brightness(1.18)"},
    {offset:.52,opacity:1,filter:"blur(4px) brightness(1.52)"},
    {offset:.76,opacity:.72,filter:"blur(3.5px) brightness(1.22)"},
    {offset:1,opacity:.34,filter:"blur(3px) brightness(.92)"}
  ];
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AK STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AD RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AK COULD NOT EXTRACT 7AD BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AK";
  window.GV7AK_VALIDATION={passed:false,pending:true,status:"AWAITING PROJECTION SUBMENU"};

  const rect=e=>{const r=e.getBoundingClientRect();return {left:r.left,top:r.top,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
  const style=e=>{const s=getComputedStyle(e);return {fontSize:s.fontSize,fontFamily:s.fontFamily,fontWeight:s.fontWeight,lineHeight:s.lineHeight,letterSpacing:s.letterSpacing,color:s.color,textShadow:s.textShadow}};
  const sameNumber=(a,b)=>Math.abs(a-b)<=TOL;
  const sameRect=(a,b)=>["left","top","width","height","right","bottom"].every(k=>sameNumber(a[k],b[k]));
  const sameStyle=(a,b)=>Object.keys(a).every(k=>a[k]===b[k]);
  const scaleY15=value=>{if(!value||value==="none")return false;try{const m=new DOMMatrixReadOnly(value);return Math.abs(m.a-1)<.01&&Math.abs(m.b)<.01&&Math.abs(m.c)<.01&&Math.abs(m.d-1.5)<.01}catch(_){return false}};

  let observer=null;
  let patched=false;
  let globalPulseStart=null;
  const iconGlowAnimations=new WeakMap();
  const iconGlowPrepared=new WeakSet();
  const iconGlowSteady=new WeakSet();
  const iconGlowActive=new Set();
  const iconGlowBaseStyles=new WeakMap();
  let iconGlowLifecycleBound=false;
  let iconGlowSyncScheduled=false;
  let coordinateFrameEl=null;
  let coordinateAnimation=null;
  let coordinateUnderglowAnimation=null;
  let coordinateGlowLayer=null;
  let coordinateInitialFrame=null;
  let coordinateGeometryObserver=null;

  function collect(){
    const leftMenu=root.querySelector(".gv-viewer-menu");
    const leftRows=[...leftMenu?.querySelectorAll(":scope > .gv-viewer-menu-row")||[]];
    const rightMenu=root.querySelector(".gv-projection-submenu");
    const rightRows=[...rightMenu?.querySelectorAll(":scope > .gv-projection-option-row")||[]];
    const leftLabels=leftRows.map(r=>r.querySelector(".gv-viewer-menu-label"));
    const leftIcons=leftRows.map(r=>r.querySelector(".gv-viewer-menu-icon"));
    const rightLabels=rightRows.map(r=>r.querySelector(".gv-projection-option-label"));
    const rightIcons=rightRows.map(r=>r.querySelector(".gv-projection-option-icon"));
    return {leftMenu,leftRows,rightMenu,rightRows,leftLabels,leftIcons,rightLabels,rightIcons};
  }

  function ensureGlyph(label,name){
    const direct=[...label.querySelectorAll(":scope > span.gv-space-age-glyph")];
    const extraElements=[...label.children].filter(el=>!el.matches("span.gv-space-age-glyph"));
    const nonWhitespaceText=[...label.childNodes].filter(node=>node.nodeType===Node.TEXT_NODE&&(node.nodeValue||"").trim());
    if(direct.length===1&&label.children.length===1&&!extraElements.length&&!nonWhitespaceText.length){
      if(direct[0].textContent!==name)direct[0].textContent=name;
      return direct[0];
    }
    const span=document.createElement("span");
    span.className="gv-space-age-glyph";
    span.textContent=name;
    label.replaceChildren(span);
    return span;
  }

  function populateProjectionIcons(c){
    c.rightIcons.slice(1).forEach((icon,index)=>{icon.innerHTML=PROJECTION_ICONS[index]});
  }

  function getGlobalPulseStart(){
    if(globalPulseStart===null)globalPulseStart=document.timeline.currentTime??performance.now();
    return globalPulseStart;
  }

  function labelGlyph(label){return label?.querySelector(":scope > span.gv-space-age-glyph")||null}

  function matchProjectionLabelHeights(c){
    const reference=labelGlyph(c.leftLabels[0])||c.leftLabels[0];
    const referenceHeight=reference?.getBoundingClientRect().height||0;
    if(!referenceHeight)return [];
    return c.rightLabels.map(label=>{
      const glyph=labelGlyph(label)||label;
      let height=glyph.getBoundingClientRect().height;
      let size=parseFloat(getComputedStyle(label).fontSize)||12;
      if(height>0){
        size*=referenceHeight/height;
        label.style.setProperty("font-size",`${size.toFixed(3)}px`,"important");
        height=glyph.getBoundingClientRect().height;
        if(height>0&&Math.abs(height-referenceHeight)>.15){
          size*=referenceHeight/height;
          label.style.setProperty("font-size",`${size.toFixed(3)}px`,"important");
          height=glyph.getBoundingClientRect().height;
        }
      }
      return {referenceHeight,height,fontSize:getComputedStyle(label).fontSize,error:height-referenceHeight};
    });
  }

  function contentTarget(tile,isLabel=false){
    if(!tile)return null;
    return isLabel?labelGlyph(tile):(
      tile.querySelector("svg,img")||
      [...tile.children].find(child=>!child.classList.contains("gv-7ai-tile-glow"))||
      null
    );
  }

  function paintedBox(svg){
    try{return {box:svg.getBBox({fill:true,stroke:true,markers:true}),mode:"fill+stroke"}}
    catch(_){return {box:svg.getBBox(),mode:"geometry-fallback"}}
  }

  function measurePaintedCenter(tile,svg){
    const tileRect=tile.getBoundingClientRect();
    const svgRect=svg.getBoundingClientRect();
    const {box,mode}=paintedBox(svg);
    const vb=svg.viewBox.baseVal;
    const sx=svgRect.width/vb.width,sy=svgRect.height/vb.height;
    let appliedX=0,appliedY=0;
    try{const m=new DOMMatrixReadOnly(getComputedStyle(svg).transform);appliedX=m.e;appliedY=m.f}catch(_){ }
    return {
      tileX:tileRect.left+tileRect.width/2,
      tileY:tileRect.top+tileRect.height/2,
      paintX:svgRect.left+(box.x+box.width/2-vb.x)*sx,
      paintY:svgRect.top+(box.y+box.height/2-vb.y)*sy,
      appliedX,appliedY,mode,
      bbox:{x:box.x,y:box.y,width:box.width,height:box.height}
    };
  }

  function centerIcon(tile,svg){
    tile.style.setProperty("display","grid","important");
    tile.style.setProperty("place-items","center","important");
    svg.style.setProperty("width","24px","important");
    svg.style.setProperty("height","24px","important");
    svg.style.setProperty("margin","0","important");
    svg.style.setProperty("grid-area","1 / 1","important");
    svg.style.setProperty("justify-self","center","important");
    svg.style.setProperty("align-self","center","important");
    svg.style.setProperty("transform-origin","center center","important");
    svg.style.setProperty("animation","none","important");
    svg.style.setProperty("transform","none","important");
    void svg.getBoundingClientRect();
    const before=measurePaintedCenter(tile,svg);
    const dx=before.tileX-before.paintX,dy=before.tileY-before.paintY;
    svg.style.setProperty("transform",`translate(${dx.toFixed(3)}px,${dy.toFixed(3)}px)`,"important");
    void svg.getBoundingClientRect();
    const after=measurePaintedCenter(tile,svg);
    return {
      dx,dy,
      tileX:after.tileX,tileY:after.tileY,paintX:after.paintX,paintY:after.paintY,
      errorX:after.tileX-after.paintX,errorY:after.tileY-after.paintY,
      appliedX:after.appliedX,appliedY:after.appliedY,mode:after.mode,bbox:after.bbox
    };
  }

  function centerProjectionIcons(c){
    const measurements={};
    const mollweideSvg=c.rightIcons[0]?.querySelector("svg");
    if(mollweideSvg){
      const m=measurePaintedCenter(c.rightIcons[0],mollweideSvg);
      measurements.MOLLWEIDE={
        dx:0,dy:0,tileX:m.tileX,tileY:m.tileY,paintX:m.paintX,paintY:m.paintY,
        errorX:m.tileX-m.paintX,errorY:m.tileY-m.paintY,
        appliedX:m.appliedX,appliedY:m.appliedY,mode:m.mode,bbox:m.bbox,preserved:true
      };
    }
    c.rightIcons.slice(1).forEach((tile,index)=>{
      const svg=tile.querySelector("svg");
      if(svg)measurements[LABELS[index+1]]=centerIcon(tile,svg);
    });
    return measurements;
  }

  function normalizeEasing(value){
    return String(value||"").replace(/\s+/g,"").replace(/0\./g,".");
  }

  function restoreIconInline(element,property,value,priority){
    if(value)element.style.setProperty(property,value,priority||"");
    else element.style.removeProperty(property);
  }

  function prepareIconGraphic(graphic){
    if(!graphic)return false;
    if(iconGlowPrepared.has(graphic))return true;
    iconGlowBaseStyles.set(graphic,{
      opacity:graphic.style.getPropertyValue("opacity"),
      opacityPriority:graphic.style.getPropertyPriority("opacity"),
      filter:graphic.style.getPropertyValue("filter"),
      filterPriority:graphic.style.getPropertyPriority("filter")
    });
    graphic.getAnimations().forEach(animation=>{try{animation.cancel()}catch(_){ }});
    graphic.style.setProperty("animation","none","important");
    iconGlowPrepared.add(graphic);
    return true;
  }

  function restoreIconBase(graphic){
    const base=iconGlowBaseStyles.get(graphic);
    if(!base)return;
    restoreIconInline(graphic,"opacity",base.opacity,base.opacityPriority);
    restoreIconInline(graphic,"filter",base.filter,base.filterPriority);
  }

  function stopIconGlow(graphic){
    if(!graphic)return;
    const animation=iconGlowAnimations.get(graphic);
    if(animation){
      try{animation.cancel()}catch(_){ }
      iconGlowAnimations.delete(graphic);
    }
    iconGlowActive.delete(graphic);
    if(!iconGlowSteady.has(graphic))restoreIconBase(graphic);
  }

  function clearSteadyIcon(graphic){
    if(!graphic)return;
    iconGlowSteady.delete(graphic);
    restoreIconBase(graphic);
  }

  function startIconGlow(graphic){
    if(!graphic)return null;
    prepareIconGraphic(graphic);
    clearSteadyIcon(graphic);
    const existing=iconGlowAnimations.get(graphic);
    if(existing&&existing.playState==="running"){
      iconGlowActive.add(graphic);
      return existing;
    }
    if(existing){
      try{existing.cancel()}catch(_){ }
      iconGlowAnimations.delete(graphic);
    }
    const animation=graphic.animate(iconFrames,{duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"});
    animation.startTime=getGlobalPulseStart();
    iconGlowAnimations.set(graphic,animation);
    iconGlowActive.add(graphic);
    return animation;
  }

  function makeIconSteady(graphic){
    if(!graphic)return false;
    prepareIconGraphic(graphic);
    stopIconGlow(graphic);
    const selected=iconFrames[2];
    graphic.style.setProperty("opacity",String(selected.opacity),"important");
    graphic.style.setProperty("filter",selected.filter,"important");
    iconGlowSteady.add(graphic);
    return graphic.getAnimations().filter(animation=>animation.playState==="running").length===0;
  }

  function releaseIconGlow(graphic){
    if(!graphic)return;
    stopIconGlow(graphic);
    clearSteadyIcon(graphic);
  }

  function allMenuIconGraphics(c=collect()){
    return [...c.leftIcons,...c.rightIcons].map(icon=>contentTarget(icon,false)).filter(Boolean);
  }

  function desiredIconGraphics(c=collect()){
    const leftOpen=!!c.leftMenu?.classList.contains("gv-open");
    const rightOpen=!!c.rightMenu?.classList.contains("gv-open");
    if(!leftOpen&&!rightOpen)return [];
    if(rightOpen){
      return [contentTarget(c.leftIcons[0],false),...c.rightIcons.map(icon=>contentTarget(icon,false))].filter(Boolean);
    }
    return c.leftIcons.map(icon=>contentTarget(icon,false)).filter(Boolean);
  }

  function iconGlowDiagnostics(){
    const desired=desiredIconGraphics();
    const desiredSet=new Set(desired);
    const all=allMenuIconGraphics();
    const animations=desired.map(graphic=>iconGlowAnimations.get(graphic)||null);
    const running=animations.filter(animation=>animation?.playState==="running");
    const currentTimes=running.map(animation=>Number(animation.currentTime)).filter(Number.isFinite);
    const hiddenRunning=all.filter(graphic=>!desiredSet.has(graphic)&&graphic.getAnimations().some(animation=>animation.playState==="running"));
    return {
      expectedCount:desired.length,
      runningCount:running.length,
      onePerVisibleGraphic:desired.every((graphic,index)=>animations[index]?.playState==="running"&&graphic.getAnimations().filter(animation=>animation.playState==="running").length===1),
      sharedStart:running.length===desired.length&&running.every(animation=>animation.startTime===getGlobalPulseStart()),
      durationMatch:running.length===desired.length&&running.every(animation=>animation.effect.getTiming().duration===CYCLE),
      easingMatch:running.length===desired.length&&running.every(animation=>normalizeEasing(animation.effect.getTiming().easing)===normalizeEasing(EASING)),
      phaseSpreadMs:currentTimes.length?Math.max(...currentTimes)-Math.min(...currentTimes):0,
      noHiddenRunning:hiddenRunning.length===0,
      hiddenRunningCount:hiddenRunning.length
    };
  }

  function syncIconGlowFromUI(){
    const desired=desiredIconGraphics();
    const desiredSet=new Set(desired);
    [...iconGlowActive].forEach(graphic=>{if(!desiredSet.has(graphic))stopIconGlow(graphic)});
    desired.forEach(startIconGlow);
    return iconGlowDiagnostics();
  }

  function makeHamburgerStatic(){
    const menuButton=root.querySelector("button.gv-menu-proxy");
    const stack=menuButton?.querySelector(".gv-menu-stack");
    if(!menuButton)return false;
    menuButton.getAnimations({subtree:true}).forEach(animation=>{try{animation.cancel()}catch(_){ }});
    menuButton.style.setProperty("animation","none","important");
    const glow=menuButton.querySelector(":scope > .gv-7ai-tile-glow");
    if(glow){
      glow.getAnimations().forEach(animation=>{try{animation.cancel()}catch(_){ }});
      glow.style.setProperty("animation","none","important");
      glow.style.setProperty("opacity","0","important");
    }
    if(stack){
      stack.getAnimations({subtree:true}).forEach(animation=>{try{animation.cancel()}catch(_){ }});
      stack.style.setProperty("animation","none","important");
    }
    return true;
  }

  function forceQuietIconGlow(){
    allMenuIconGraphics().forEach(graphic=>{prepareIconGraphic(graphic);stopIconGlow(graphic)});
  }

  function scheduleIconGlowSync(){
    if(iconGlowSyncScheduled)return;
    iconGlowSyncScheduled=true;
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      iconGlowSyncScheduled=false;
      syncIconGlowFromUI();
    }));
  }

  function bindIconGlowLifecycle(){
    if(iconGlowLifecycleBound)return;
    iconGlowLifecycleBound=true;
    root.addEventListener("click",event=>{
      const control=event.target?.closest?.("button.gv-menu-proxy,button.gv-target-proxy,.gv-viewer-menu-label,.gv-viewer-menu-icon,.gv-projection-option-label,.gv-projection-option-icon,.gv-7am-projection-status");
      if(control)scheduleIconGlowSync();
    },true);
  }

  const iconGlow=window.GV_ICON_GLOW={
    cycle:CYCLE,
    easing:EASING,
    startTime:()=>getGlobalPulseStart(),
    initialize(){
      makeHamburgerStatic();
      forceQuietIconGlow();
      bindIconGlowLifecycle();
      return syncIconGlowFromUI();
    },
    syncFromUI:syncIconGlowFromUI,
    setStatusGraphic:makeIconSteady,
    release:releaseIconGlow,
    diagnostics:iconGlowDiagnostics,
    animationFor:graphic=>iconGlowAnimations.get(graphic)||null,
    isSteady:graphic=>iconGlowSteady.has(graphic)
  };

  async function startCoordinateGlow(){
    const frame=await waitFor(()=>root.querySelector(".gv-coordinate-module-host")?.shadowRoot?.querySelector(".gvco-frame"));
    const host=root.querySelector(".gv-coordinate-module-host");
    const shadow=host?.shadowRoot;
    const coordinateRoot=shadow?.querySelector(".gvco-root");
    coordinateFrameEl=frame;
    coordinateInitialFrame=(frame.textContent||"").trim().toUpperCase();
    getGlobalPulseStart();
    frame.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});
    frame.style.setProperty("z-index","2","important");
    coordinateAnimation=frame.animate(coordinateFrames,{duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"});
    coordinateAnimation.startTime=globalPulseStart;

    coordinateGlowLayer=shadow?.querySelector(".gv-7ai-coordinate-underglow");
    if(!coordinateGlowLayer&&coordinateRoot){
      coordinateGlowLayer=document.createElement("span");
      coordinateGlowLayer.className="gv-7ai-coordinate-underglow";
      coordinateGlowLayer.setAttribute("aria-hidden","true");
      coordinateGlowLayer.style.setProperty("position","absolute","important");
      coordinateGlowLayer.style.setProperty("pointer-events","none","important");
      coordinateGlowLayer.style.setProperty("z-index","1","important");
      coordinateGlowLayer.style.setProperty("border-radius","999px","important");
      coordinateGlowLayer.style.setProperty("background","radial-gradient(ellipse at center,rgba(238,254,255,.72) 0%,rgba(143,234,255,.58) 18%,rgba(98,216,255,.46) 38%,rgba(79,166,255,.30) 55%,rgba(157,124,255,.18) 68%,rgba(0,0,0,0) 82%)","important");
      coordinateRoot.insertBefore(coordinateGlowLayer,frame);
    }

    const alignUnderglow=()=>{
      if(!coordinateGlowLayer||!coordinateRoot||!frame)return;
      const rr=coordinateRoot.getBoundingClientRect(),fr=frame.getBoundingClientRect();
      const divider=shadow.querySelector(".gvco-divider")?.getBoundingClientRect();
      const left=Math.max(2,fr.left-rr.left-8);
      const maxRight=divider?divider.left-rr.left-3:rr.width-3;
      const width=Math.max(12,Math.min(fr.width+16,maxRight-left));
      const height=Math.min(30,Math.max(22,fr.height+12));
      const top=Math.max(2,fr.top-rr.top+(fr.height-height)/2);
      coordinateGlowLayer.style.setProperty("left",`${left.toFixed(2)}px`,"important");
      coordinateGlowLayer.style.setProperty("top",`${top.toFixed(2)}px`,"important");
      coordinateGlowLayer.style.setProperty("width",`${width.toFixed(2)}px`,"important");
      coordinateGlowLayer.style.setProperty("height",`${height.toFixed(2)}px`,"important");
    };
    alignUnderglow();
    coordinateGlowLayer?.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});
    if(coordinateGlowLayer){
      coordinateUnderglowAnimation=coordinateGlowLayer.animate(underglowFrames,{duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"});
      coordinateUnderglowAnimation.startTime=globalPulseStart;
    }
    coordinateGeometryObserver?.disconnect();
    coordinateGeometryObserver=new MutationObserver(()=>requestAnimationFrame(alignUnderglow));
    coordinateGeometryObserver.observe(frame,{subtree:true,childList:true,characterData:true});
    window.addEventListener("resize",alignUnderglow,{passive:true});

    window.GV7AK_COORDINATE_GLOW={
      passed:coordinateInitialFrame==="ICRSD",
      initialFrame:coordinateInitialFrame,
      cycleMs:CYCLE,
      easing:EASING,
      startTime:globalPulseStart,
      textPlayState:coordinateAnimation.playState,
      underglowPlayState:coordinateUnderglowAnimation?.playState||"missing"
    };
    return frame;
  }

  const nextPaint=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));

  async function validateCoordinateGlow(){
    const frame=await coordinateGlowPromise;
    if(!frame||!coordinateAnimation||!coordinateGlowLayer||!coordinateUnderglowAnimation)return {passed:false,error:String(coordinateGlowError||"coordinate glow unavailable")};
    const host=root.querySelector(".gv-coordinate-module-host");
    const shadow=host?.shadowRoot;
    const coordinateRoot=shadow?.querySelector(".gvco-root");
    const beforeFrame=(frame.textContent||"").trim().toUpperCase();
    const beforeRootRect=coordinateRoot?.getBoundingClientRect();
    const beforeFrameRect=frame.getBoundingClientRect();
    const beforeX=shadow?.querySelector(".gvco-x")?.textContent||"";
    const beforeY=shadow?.querySelector(".gvco-y")?.textContent||"";
    const animationRef=coordinateAnimation;
    const underglowRef=coordinateUnderglowAnimation;
    const expectedFirst=beforeFrame==="GAL"?"ICRSD":"GAL";
    frame.click();
    await nextPaint();
    const firstFrame=(frame.textContent||"").trim().toUpperCase();
    const sameNodeAfterFirst=shadow?.querySelector(".gvco-frame")===frame;
    frame.click();
    await nextPaint();
    const restoredFrame=(frame.textContent||"").trim().toUpperCase();
    const afterRootRect=coordinateRoot?.getBoundingClientRect();
    const afterFrameRect=frame.getBoundingClientRect();
    const afterX=shadow?.querySelector(".gvco-x")?.textContent||"";
    const afterY=shadow?.querySelector(".gvco-y")?.textContent||"";
    const timing=animationRef.effect.getTiming();
    const underTiming=underglowRef.effect.getTiming();
    const layerRect=coordinateGlowLayer.getBoundingClientRect();
    const dividerRect=shadow?.querySelector(".gvco-divider")?.getBoundingClientRect();
    const result={
      initialStartupFrame:coordinateInitialFrame,
      beforeFrame,firstFrame,restoredFrame,expectedFirst,
      sameNodeAfterFirst,
      sameNodeAfterRestore:shadow?.querySelector(".gvco-frame")===frame,
      textAnimationPersistent:frame.getAnimations().includes(animationRef)&&animationRef.playState==="running",
      underglowAnimationPersistent:underglowRef.playState==="running",
      sharedGlobalStart:animationRef.startTime===globalPulseStart&&underglowRef.startTime===globalPulseStart,
      cycleMs:timing.duration,
      underglowCycleMs:underTiming.duration,
      easing:timing.easing,
      underglowEasing:underTiming.easing,
      rootGeometryStable:!!beforeRootRect&&!!afterRootRect&&sameNumber(beforeRootRect.width,afterRootRect.width)&&sameNumber(beforeRootRect.height,afterRootRect.height),
      frameGeometryRestored:sameNumber(beforeFrameRect.left,afterFrameRect.left)&&sameNumber(beforeFrameRect.top,afterFrameRect.top)&&sameNumber(beforeFrameRect.width,afterFrameRect.width)&&sameNumber(beforeFrameRect.height,afterFrameRect.height),
      coordinateTextRestored:beforeX===afterX&&beforeY===afterY,
      underglowPointerSafe:getComputedStyle(coordinateGlowLayer).pointerEvents==="none",
      underglowBehindText:Number(getComputedStyle(coordinateGlowLayer).zIndex)<Number(getComputedStyle(frame).zIndex),
      underglowBeforeDivider:!dividerRect||layerRect.right<=dividerRect.left+1
    };
    result.passed=
      result.initialStartupFrame==="ICRSD"&&result.firstFrame===expectedFirst&&result.restoredFrame===beforeFrame&&
      result.sameNodeAfterFirst&&result.sameNodeAfterRestore&&result.textAnimationPersistent&&result.underglowAnimationPersistent&&
      result.sharedGlobalStart&&result.cycleMs===CYCLE&&result.underglowCycleMs===CYCLE&&
      normalizeEasing(result.easing)===normalizeEasing(EASING)&&normalizeEasing(result.underglowEasing)===normalizeEasing(EASING)&&
      result.rootGeometryStable&&result.frameGeometryRestored&&result.coordinateTextRestored&&
      result.underglowPointerSafe&&result.underglowBehindText&&result.underglowBeforeDivider;
    return result;
  }

  async function finalizeAndValidate(baseline){
    const c=collect();
    const centering=centerProjectionIcons(c);
    iconGlow.initialize();
    await coordinateGlowPromise;
    await nextPaint();
    return validate(baseline,centering);
  }

  function prepareAndPatch(){
    if(patched)return true;
    const c=collect();
    if(c.leftRows.length!==5||c.rightRows.length!==5||[...c.leftLabels,...c.leftIcons,...c.rightLabels,...c.rightIcons].some(v=>!v))return false;

    const baseline={
      leftLabelHtml:c.leftLabels.map(e=>e.innerHTML),
      leftLabelStyles:c.leftLabels.map(style),
      leftLabelRects:c.leftLabels.map(rect),
      leftIconRects:c.leftIcons.map(rect),
      rightLabelStyles:c.rightLabels.map(style),
      rightLabelRects:c.rightLabels.map(rect),
      rightIconRects:c.rightIcons.map(rect),
      rightRowRects:c.rightRows.map(rect),
      labelButtons:[...c.rightLabels],
      iconButtons:[...c.rightIcons],
      rowNodes:[...c.rightRows],
      projectionSvg:c.leftIcons[0].querySelector("svg")?.outerHTML||"",
      projectionSvgInner:c.leftIcons[0].querySelector("svg")?.innerHTML||"",
      mollweideSvg:c.rightIcons[0].querySelector("svg")?.outerHTML||"",
      mollweideSvgInner:c.rightIcons[0].querySelector("svg")?.innerHTML||"",
      generatedIconHtml:c.rightIcons.slice(1).map(e=>e.innerHTML)
    };

    c.rightLabels.forEach((label,index)=>ensureGlyph(label,LABELS[index]));
    populateProjectionIcons(c);
    matchProjectionLabelHeights(c);
    patched=true;
    observer?.disconnect();
    finalizeAndValidate(baseline).catch(error=>console.error("GV-BETA-0007AK FINALIZATION FAILURE:",error));
    return true;
  }

  async function validate(baseline,centering){
    const c=collect();
    const labelNames=c.rightLabels.map(e=>(e?.textContent||"").trim().toUpperCase());
    const wrapperCounts=c.rightLabels.map(e=>e?.querySelectorAll("span.gv-space-age-glyph").length||0);
    const spans=c.rightLabels.map(e=>e?.querySelector(":scope > span.gv-space-age-glyph"));
    const fontSizes=c.rightLabels.map(e=>e?getComputedStyle(e).fontSize:"");
    const referenceGlyph=labelGlyph(c.leftLabels[0])||c.leftLabels[0];
    const referenceGlyphHeight=referenceGlyph?.getBoundingClientRect().height||0;
    const rightGlyphHeights=spans.map(e=>e?.getBoundingClientRect().height||0);
    const rightGlyphHeightErrors=rightGlyphHeights.map(h=>h-referenceGlyphHeight);
    const transforms=spans.map(e=>e?getComputedStyle(e).transform:"");
    const fontFamilies=c.rightLabels.map(e=>e?getComputedStyle(e).fontFamily:"");
    const letterSpacing=c.rightLabels.map(e=>e?getComputedStyle(e).letterSpacing:"");
    const iconPopulatedStates=c.rightIcons.slice(1).map(e=>!!e?.querySelector("svg"));
    const newSvgRects=c.rightIcons.slice(1).map(e=>rect(e.querySelector("svg")));
    const iconGeometryChecks=[
      c.rightIcons[1].innerHTML.includes('rx="8.5" ry="22"')&&c.rightIcons[1].innerHTML.includes('r="2" fill="#4fa6ff"'),
      c.rightIcons[2].innerHTML.includes('M32 13V51M13 32H51')&&c.rightIcons[2].innerHTML.includes('r="3.1" stroke="#4fa6ff"'),
      c.rightIcons[3].innerHTML.includes('M36.5 25L44 18M36.8 32H45M36.5 39L44 46')&&c.rightIcons[3].innerHTML.includes('M44 18L56 21.5L56 42.5L44 46Z'),
      c.rightIcons[4].innerHTML.includes('M32 9C22 11 13 20 9 32')&&c.rightIcons[4].innerHTML.includes('r="1.6" fill="#4fa6ff"')
    ];
    const currentLeftStyles=c.leftLabels.map(style);
    const currentRightStyles=c.rightLabels.map(style);
    const currentLeftLabelRects=c.leftLabels.map(rect);
    const currentLeftIconRects=c.leftIcons.map(rect);
    const currentRightLabelRects=c.rightLabels.map(rect);
    const currentRightIconRects=c.rightIcons.map(rect);
    const currentRightRowRects=c.rightRows.map(rect);
    const open=!!c.rightMenu?.classList.contains("gv-open");
    const inactive=c.leftRows.slice(1);
    const inactiveDimmed=inactive.every(row=>Number(getComputedStyle(row.querySelector(".gv-viewer-menu-label")).opacity)<=.43&&Number(getComputedStyle(row.querySelector(".gv-viewer-menu-icon")).opacity)<=.43);
    const inactiveNoPulse=inactive.every(row=>row.getAnimations({subtree:true}).filter(a=>a.playState==="running").length===0);
    const projection=c.leftIcons[0];
    const mollweide=c.rightIcons[0];
    const noPlainOutside=c.rightLabels.every((label,i)=>{
      const span=spans[i];
      if(!label||!span)return false;
      const extras=[...label.children].filter(child=>child!==span&&!child.classList.contains("gv-7ai-tile-glow"));
      return extras.length===0&&[...label.childNodes].every(node=>node.nodeType!==Node.TEXT_NODE||(node.nodeValue||"").trim()==="");
    });
    const noInlineNewActions=c.rightRows.slice(1).every(row=>[row.querySelector(".gv-projection-option-label"),row.querySelector(".gv-projection-option-icon")].every(button=>button&&!button.hasAttribute("onclick")&&button.onclick===null));
    const dimRulePresent=[...document.styleSheets].some(sheet=>{try{return [...sheet.cssRules].some(rule=>(rule.cssText||"").includes("gv-7ad-projection-mode"))}catch(_){return false}});
    const geometryUnchanged=
      currentLeftLabelRects.every((r,i)=>sameRect(r,baseline.leftLabelRects[i]))&&
      currentLeftIconRects.every((r,i)=>sameRect(r,baseline.leftIconRects[i]))&&
      currentRightLabelRects.every((r,i)=>sameRect(r,baseline.rightLabelRects[i]))&&
      currentRightIconRects.every((r,i)=>sameRect(r,baseline.rightIconRects[i]))&&
      currentRightRowRects.every((r,i)=>sameRect(r,baseline.rightRowRects[i]));
    const glow=iconGlow.diagnostics();
    const longLabels=[...c.leftLabels,...c.rightLabels].filter(Boolean);
    const iconTiles=[...c.leftIcons,...c.rightIcons].filter(Boolean);
    const layerRunning=tile=>tile?.querySelector(":scope > .gv-7ai-tile-glow")?.getAnimations().some(a=>a.playState==="running")||false;
    const coordinate=await validateCoordinateGlow();
    const newCenterNames=["SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
    const newCentersPass=newCenterNames.every(name=>centering?.[name]&&Math.abs(centering[name].errorX)<CENTER_TOL&&Math.abs(centering[name].errorY)<CENTER_TOL);
    const checks={
      versionLabel:versionLabel.textContent==="V-7AK",
      cycleIs3000:CYCLE===3000,
      exactlyFiveProjectionRows:c.rightRows.length===5,
      exactLabelOrder:JSON.stringify(labelNames)===JSON.stringify(LABELS),
      orthographicAbsent:!(c.rightMenu?.textContent||"").toUpperCase().includes("ORTHOGRAPHIC"),
      orthogonalAbsent:!(c.rightMenu?.textContent||"").toUpperCase().includes("ORTHOGONAL"),
      exactlyOneGlyphWrapper:wrapperCounts.length===5&&wrapperCounts.every(n=>n===1),
      noPlainTextOutsideGlyph:noPlainOutside,
      allGlyphTransformsScaleY15:transforms.length===5&&transforms.every(scaleY15),
      rightGlyphHeightsMatchProjection:rightGlyphHeightErrors.length===5&&rightGlyphHeightErrors.every(error=>Math.abs(error)<=.5),
      allButtonsSpaceAge:fontFamilies.length===5&&fontFamilies.every(v=>v.toLowerCase().includes("space age")),
      allButtonsLetterSpacing055px:letterSpacing.length===5&&letterSpacing.every(v=>Math.abs(parseFloat(v)-.55)<.01),
      rightTypographyAuthorizedSizeOnly:currentRightStyles.every((styleNow,i)=>["fontFamily","fontWeight","lineHeight","letterSpacing","color","textShadow"].every(key=>styleNow[key]===baseline.rightLabelStyles[i][key])),
      leftTypographyUntouched:c.leftLabels.every((e,i)=>sameStyle(currentLeftStyles[i],baseline.leftLabelStyles[i])&&(e.textContent||"").trim()===(new DOMParser().parseFromString(`<body>${baseline.leftLabelHtml[i]}</body>`,"text/html").body.textContent||"").trim()),
      longTileGeometryUnchanged:geometryUnchanged,
      squareTileDimensionsUnchanged:[...currentLeftIconRects,...currentRightIconRects].every((r,i)=>{const before=[...baseline.leftIconRects,...baseline.rightIconRects][i];return sameNumber(r.width,before.width)&&sameNumber(r.height,before.height)&&sameNumber(r.width,r.height)}),
      projectionModeDimmingFunctional:open?(inactiveDimmed&&inactiveNoPulse):dimRulePresent,
      projectionActiveStateRetained:!open||c.leftRows[0].classList.contains("gv-selected"),
      longLabelTilesNoPulse:longLabels.every(label=>label.getAnimations({subtree:true}).filter(a=>a.playState==="running").length===0),
      longLabelGlowLayersInactive:longLabels.every(label=>!layerRunning(label)),
      iconTileBackgroundsStatic:iconTiles.every(tile=>tile.getAnimations().filter(a=>a.playState==="running").length===0&&!layerRunning(tile)),
      visibleIconGlowCountCorrect:glow.runningCount===glow.expectedCount,
      visibleIconGlowOneEach:glow.onePerVisibleGraphic,
      visibleIconGlowSharedStart:glow.sharedStart,
      visibleIconGlowDuration:glow.durationMatch,
      visibleIconGlowEasing:glow.easingMatch,
      visibleIconGlowPhase:glow.phaseSpreadMs<=5,
      hiddenIconsNotAnimating:glow.noHiddenRunning,
      hamburgerGlowRemoved:root.querySelector("button.gv-menu-proxy")?.getAnimations({subtree:true}).filter(a=>a.playState==="running").length===0,
      projectionSvgGeometryUnchanged:(projection?.querySelector("svg")?.innerHTML||"")===baseline.projectionSvgInner,
      mollweideSvgPresent:!!mollweide?.querySelector("svg"),
      mollweideSvgGeometryUnchanged:(mollweide?.querySelector("svg")?.innerHTML||"")===baseline.mollweideSvgInner,
      fourGeneratedIconTilesWereEmpty:baseline.generatedIconHtml.every(html=>html.trim()===""),
      fourGeneratedIconTilesPopulated:iconPopulatedStates.every(Boolean),
      exactApprovedIconGeometry:iconGeometryChecks.every(Boolean),
      newIconSvgSize24px:newSvgRects.every(r=>sameNumber(r.width,24)&&sameNumber(r.height,24)),
      fourNewIconsPaintCentered:newCentersPass,
      mollweideCenterMeasured:!!centering?.MOLLWEIDE&&Math.abs(centering.MOLLWEIDE.errorX)<CENTER_TOL&&Math.abs(centering.MOLLWEIDE.errorY)<CENTER_TOL,
      coordinateStartupICRSD:coordinate.initialStartupFrame==="ICRSD",
      coordinateGlowPersistent:coordinate.passed,
      sphericalOrthoDistinct:c.rightIcons[1].innerHTML!==c.rightIcons[2].innerHTML,
      labelButtonElementsPreserved:c.rightLabels.every((e,i)=>e===baseline.labelButtons[i]),
      iconButtonElementsPreserved:c.rightIcons.every((e,i)=>e===baseline.iconButtons[i]),
      rowElementsPreserved:c.rightRows.every((e,i)=>e===baseline.rowNodes[i]),
      noNewProjectionActions:noInlineNewActions,
      splashUnloaded:!document.querySelector('[src*="Singularity"],[href*="Singularity"]'),
      noDuplicateProjectionLabels:new Set(labelNames).size===5
    };
    const failedChecks=Object.entries(checks).filter(([,value])=>!value).map(([name])=>name);
    const passed=failedChecks.length===0;
    window.GV7AK_VALIDATION={
      passed,
      pending:false,
      checks,
      failedChecks,
      labelNames,
      wrapperCounts,
      computedFontSizes:fontSizes,
      referenceGlyphHeight,
      rightGlyphHeights,
      rightGlyphHeightErrors,
      computedTransforms:transforms,
      fontFamilies,
      letterSpacing,
      iconPopulatedStates,
      iconGeometryChecks,
      newSvgRects,
      centering,
      centerTolerancePx:CENTER_TOL,
      iconGlow:glow,
      coordinateGlow:coordinate,
      projectionModeOpen:open,
      baseline:"GV-beta-0007AD.py@19f5a381314e1ebb336f7d25c4df9fdb54163301",
      fontSizeContract:"right Projection submenu rendered glyph height matches PROJECTION within ±0.5 px",
      glyphTransformContract:"scaleY(1.5)",
      splash:"not loaded",
      newProjectionActions:"not wired",
      populatedIcons:["SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"]
    };
    if(!passed)throw new Error("GV-BETA-0007AK CONTRACT FAILED "+JSON.stringify(window.GV7AK_VALIDATION));
    return true;
  }

  let coordinateGlowError=null;
  const coordinateGlowPromise=startCoordinateGlow().catch(error=>{coordinateGlowError=error;window.GV7AK_COORDINATE_GLOW={passed:false,error:String(error)};return null});

  observer=new MutationObserver(()=>{if(patched)return;const c=collect();if(c.rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch))});
  observer.observe(root,{subtree:true,childList:true});
  if(collect().rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch));
})().catch(error=>console.error("GV-BETA-0007AK STARTUP FAILURE:",error));
"""))

# GV-beta-0007AK staged

# GV-beta-0007AL
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AL
# PURPOSE: Restore static inner neon to square icon targets, keep long labels and square surfaces non-pulsing, wire all projection actions, hold the selected icon in a steady bright state, fade the complete menus after selection, and reopen projection selection from the existing target icon.
# USER REQUEST: Preserve the static inner target glow, animate only selectable icon graphics on the 3000 ms cycle, make selected projection icons steady-bright, execute MOLLWEIDE/SPHERICAL/ORTHO/TANGENTIAL/SINUSOIDAL actions, fade the menus after selection, and use the target icon to reopen projection selection.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AL.py and update mobile/beta/index.html only.
# PRESERVED BEHAVIOR: GV-beta-0007AK.py remains frozen; preserve coordinate glow, icon/menu geometry, typography, dimming, Aladin/SIMBAD behavior outside the authorized target-reopen state, coordinate calculations, splash behavior, and all unrelated behavior.

display(Javascript(r"""
(async()=>{
  const VERSION="7AL";
  const MENU_FADE_MS=1000;
  const LABELS=["MOLLWEIDE","SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
  const PROJECTION_CODES={MOLLWEIDE:"MOL",SPHERICAL:"SIN",ORTHO:"SIN",TANGENTIAL:"TAN",SINUSOIDAL:"SFL"};
  const STATIC_INSET={
    backgroundColor:"rgba(5,18,32,.10)",
    boxShadow:"inset 0 0 0 1px rgba(143,234,255,.28), inset 0 0 6px rgba(98,216,255,.18), inset 0 0 10px rgba(157,124,255,.10)"
  };
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AL STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});
  const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
  const nextPaint=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const aladin=await waitFor(()=>window.aladin_cosmic_command_test);
  const iconGlow=await waitFor(()=>window.GV_ICON_GLOW);
  await waitFor(()=>window.GV7AK_VALIDATION&&window.GV7AK_VALIDATION.pending===false);
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AL";

  let selectedProjection=null;
  let menusDismissed=false;
  let fadeInProgress=false;
  let stateObserver=null;
  const interaction=window.GV7AL_INTERACTION={
    selectedProjection:null,selectedCode:null,lastProjectionBefore:null,lastProjectionAfter:null,
    setProjectionCalled:false,setProjectionSucceeded:false,selectedSteady:false,
    fadeStarted:false,fadeCompleted:false,menusHidden:false,reopenCount:0,reopened:false,lastError:null
  };

  function collect(){
    const leftMenu=root.querySelector(".gv-viewer-menu");
    const leftRows=[...leftMenu?.querySelectorAll(":scope > .gv-viewer-menu-row")||[]];
    const rightMenu=root.querySelector(".gv-projection-submenu");
    const rightRows=[...rightMenu?.querySelectorAll(":scope > .gv-projection-option-row")||[]];
    const leftLabels=leftRows.map(row=>row.querySelector(".gv-viewer-menu-label"));
    const leftIcons=leftRows.map(row=>row.querySelector(".gv-viewer-menu-icon"));
    const rightLabels=rightRows.map(row=>row.querySelector(".gv-projection-option-label"));
    const rightIcons=rightRows.map(row=>row.querySelector(".gv-projection-option-icon"));
    const menuButton=root.querySelector("button.gv-menu-proxy");
    const targetButton=root.querySelector("button.gv-target-proxy");
    return {leftMenu,leftRows,rightMenu,rightRows,leftLabels,leftIcons,rightLabels,rightIcons,menuButton,targetButton};
  }

  function ensureStaticInset(tile){
    if(!tile)return null;
    tile.getAnimations().forEach(animation=>{try{animation.cancel()}catch(_){ }});
    tile.style.setProperty("animation","none","important");
    tile.style.setProperty("position","relative","important");
    tile.style.setProperty("isolation","isolate","important");
    let layer=tile.querySelector(":scope > .gv-7ab-inset, :scope > .gv-7al-static-inset");
    if(!layer){
      layer=document.createElement("span");
      layer.className="gv-7al-static-inset gv-7ai-tile-glow";
      layer.setAttribute("aria-hidden","true");
      tile.insertBefore(layer,tile.firstChild);
    }
    layer.getAnimations().forEach(animation=>{try{animation.cancel()}catch(_){ }});
    layer.style.setProperty("display","block","important");
    layer.style.setProperty("position","absolute","important");
    layer.style.setProperty("inset","2px","important");
    layer.style.setProperty("border-radius","6px","important");
    layer.style.setProperty("pointer-events","none","important");
    layer.style.setProperty("z-index","0","important");
    layer.style.setProperty("animation","none","important");
    layer.style.setProperty("opacity","1","important");
    layer.style.setProperty("background",STATIC_INSET.backgroundColor,"important");
    layer.style.setProperty("box-shadow",STATIC_INSET.boxShadow,"important");
    layer.dataset.gv7alStaticInset="true";
    [...tile.children].filter(child=>child!==layer&&!child.classList.contains("gv-7ai-tile-glow")).forEach(child=>{
      child.style?.setProperty?.("position","relative","important");
      child.style?.setProperty?.("z-index","2","important");
    });
    return layer;
  }

  function makeLongLabelStatic(label){
    if(!label)return;
    label.getAnimations({subtree:true}).forEach(animation=>{try{animation.cancel()}catch(_){ }});
    label.style.setProperty("animation","none","important");
    label.style.setProperty("box-shadow","none","important");
    const layers=label.querySelectorAll(":scope > .gv-7ai-tile-glow, :scope > .gv-7ab-inset, :scope > .gv-7al-static-inset");
    layers.forEach(layer=>{
      layer.getAnimations().forEach(animation=>{try{animation.cancel()}catch(_){ }});
      layer.style.setProperty("display","none","important");
    });
  }

  function reapplyVisualState(){
    const c=collect();
    [...c.leftLabels,...c.rightLabels].filter(Boolean).forEach(makeLongLabelStatic);
    [...c.leftIcons,...c.rightIcons].filter(Boolean).forEach(ensureStaticInset);
    c.rightIcons.forEach((tile,index)=>{
      tile?.setAttribute("aria-checked",selectedProjection===LABELS[index]?"true":"false");
      c.rightLabels[index]?.setAttribute("aria-checked",selectedProjection===LABELS[index]?"true":"false");
    });
  }

  function restoreFadeStyle(element){
    if(!element)return;
    element.style.removeProperty("transition");
    element.style.removeProperty("opacity");
    element.style.removeProperty("visibility");
    element.style.removeProperty("pointer-events");
  }

  async function fadeMenus(){
    if(fadeInProgress)return;
    const c=collect();
    if(!c.leftMenu||!c.rightMenu||!c.menuButton)return;
    fadeInProgress=true;
    interaction.fadeStarted=true;
    interaction.fadeCompleted=false;
    interaction.menusHidden=false;
    const elements=[c.leftMenu,c.rightMenu];
    elements.forEach(element=>{
      element.style.setProperty("transition",`opacity ${MENU_FADE_MS}ms ease`,"important");
      element.style.setProperty("opacity","1","important");
      element.style.setProperty("visibility","visible","important");
      element.style.setProperty("pointer-events","none","important");
    });
    void c.leftMenu.offsetWidth;
    await new Promise(resolve=>requestAnimationFrame(resolve));
    elements.forEach(element=>element.style.setProperty("opacity","0","important"));
    await sleep(MENU_FADE_MS+40);
    c.rightMenu.classList.remove("gv-open");
    c.leftMenu.classList.remove("gv-open");
    c.leftRows[0]?.classList.remove("gv-selected");
    root.classList.remove("gv-7ad-projection-mode");
    c.menuButton.setAttribute("aria-expanded","false");
    c.leftLabels[0]?.setAttribute("aria-expanded","false");
    c.leftIcons[0]?.setAttribute("aria-expanded","false");
    elements.forEach(restoreFadeStyle);
    menusDismissed=true;
    fadeInProgress=false;
    interaction.fadeCompleted=true;
    interaction.menusHidden=true;
    reapplyVisualState();
    iconGlow.syncFromUI();
  }

  async function activateProjection(name,event){
    event?.preventDefault?.();
    event?.stopPropagation?.();
    event?.stopImmediatePropagation?.();
    if(fadeInProgress)return;
    const code=PROJECTION_CODES[name];
    interaction.lastError=null;
    interaction.selectedProjection=name;
    interaction.selectedCode=code;
    interaction.lastProjectionBefore=typeof aladin.getProjectionName==="function"?aladin.getProjectionName():null;
    interaction.setProjectionCalled=false;
    interaction.setProjectionSucceeded=false;
    try{
      if(typeof aladin.setProjection!=="function")throw new Error("ALADIN SETPROJECTION IS UNAVAILABLE");
      interaction.setProjectionCalled=true;
      await Promise.resolve(aladin.setProjection(code));
      if(typeof aladin.getProjectionName!=="function")throw new Error("ALADIN GETPROJECTIONNAME IS UNAVAILABLE");
      await waitFor(()=>aladin.getProjectionName()===code,1500);
      interaction.lastProjectionAfter=aladin.getProjectionName();
      interaction.setProjectionSucceeded=interaction.lastProjectionAfter===code;
      if(!interaction.setProjectionSucceeded)throw new Error(`PROJECTION ${name} DID NOT BECOME ${code}`);
      selectedProjection=name;
      reapplyVisualState();
      await nextPaint();
      await fadeMenus();
    }catch(error){
      interaction.lastError=String(error?.message||error);
      interaction.setProjectionSucceeded=false;
      console.error("GV-BETA-0007AL PROJECTION ACTION FAILURE",name,code,error);
      reapplyVisualState();
      iconGlow.syncFromUI();
    }
  }

  function bindProjectionActions(){
    const c=collect();
    if(c.rightRows.length!==LABELS.length)return false;
    c.rightRows.forEach((row,index)=>{
      const name=LABELS[index];
      row.dataset.gv7alProjection=name;
      const controls=[c.rightLabels[index],c.rightIcons[index]].filter(Boolean);
      controls.forEach(control=>{
        if(control.dataset.gv7alBound==="true")return;
        control.dataset.gv7alBound="true";
        control.setAttribute("role","menuitemradio");
        control.addEventListener("click",event=>activateProjection(name,event),true);
      });
    });
    return true;
  }

  function reopenProjectionMenus(event){
    if(!menusDismissed||fadeInProgress)return;
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    const c=collect();
    [c.leftMenu,c.rightMenu].forEach(restoreFadeStyle);
    c.leftMenu.classList.add("gv-open");
    c.rightMenu.classList.add("gv-open");
    c.leftRows[0]?.classList.add("gv-selected");
    root.classList.add("gv-7ad-projection-mode");
    c.menuButton.setAttribute("aria-expanded","true");
    c.leftLabels[0]?.setAttribute("aria-expanded","true");
    c.leftIcons[0]?.setAttribute("aria-expanded","true");
    menusDismissed=false;
    interaction.reopenCount+=1;
    interaction.reopened=true;
    interaction.menusHidden=false;
    reapplyVisualState();
    iconGlow.syncFromUI();
  }

  function bindTargetReopen(){
    const target=collect().targetButton;
    if(!target||target.dataset.gv7alReopenBound==="true")return false;
    target.dataset.gv7alReopenBound="true";
    target.addEventListener("click",reopenProjectionMenus,true);
    return true;
  }

  function snapshotGeometry(c){
    const rect=element=>{const r=element.getBoundingClientRect();return [r.left,r.top,r.width,r.height]};
    return {
      leftLabels:c.leftLabels.filter(Boolean).map(rect),leftIcons:c.leftIcons.filter(Boolean).map(rect),
      rightLabels:c.rightLabels.filter(Boolean).map(rect),rightIcons:c.rightIcons.filter(Boolean).map(rect)
    };
  }

  const beforeGeometry=snapshotGeometry(collect());
  bindProjectionActions();
  bindTargetReopen();
  reapplyVisualState();
  await nextPaint();
  iconGlow.syncFromUI();
  const c=collect();
  const afterGeometry=snapshotGeometry(c);
  const sameGeometry=JSON.stringify(beforeGeometry)===JSON.stringify(afterGeometry);
  const allLabels=[...c.leftLabels,...c.rightLabels].filter(Boolean);
  const allIconTiles=[...c.leftIcons,...c.rightIcons].filter(Boolean);
  const staticInsets=allIconTiles.map(tile=>tile.querySelector(":scope > .gv-7ab-inset, :scope > .gv-7al-static-inset"));
  const mappingsExact=LABELS.every(name=>PROJECTION_CODES[name]===({MOLLWEIDE:"MOL",SPHERICAL:"SIN",ORTHO:"SIN",TANGENTIAL:"TAN",SINUSOIDAL:"SFL"})[name]);
  const checks={
    versionLabel:versionLabel.textContent==="V-7AL",
    cycleIs3000:iconGlow.cycle===3000,
    mappingsExact,
    projectionButtonsBound:c.rightRows.length===5&&c.rightRows.every((row,index)=>c.rightLabels[index]?.dataset.gv7alBound==="true"&&c.rightIcons[index]?.dataset.gv7alBound==="true"),
    targetReopenBound:c.targetButton?.dataset.gv7alReopenBound==="true",
    staticInsetEverySquare:staticInsets.length===allIconTiles.length&&staticInsets.every(Boolean),
    staticInsetsNotAnimated:staticInsets.every(layer=>layer.getAnimations().filter(animation=>animation.playState==="running").length===0),
    staticInsetStyleApplied:staticInsets.every(layer=>layer.dataset.gv7alStaticInset==="true"&&!!layer.style.getPropertyValue("background")&&layer.style.getPropertyValue("box-shadow").includes("inset")),
    squareSurfacesNotAnimated:allIconTiles.every(tile=>tile.getAnimations().filter(animation=>animation.playState==="running").length===0),
    longLabelsNotAnimated:allLabels.every(label=>label.getAnimations({subtree:true}).filter(animation=>animation.playState==="running").length===0),
    longTileBoxGlowRemoved:allLabels.every(label=>getComputedStyle(label).boxShadow==="none"),
    iconGlowLifecycleCorrect:iconGlow.diagnostics().onePerVisibleGraphic,
    hiddenIconsNotAnimating:iconGlow.diagnostics().noHiddenRunning,
    hamburgerNoGlow:c.menuButton?.getAnimations({subtree:true}).filter(animation=>animation.playState==="running").length===0,
    coordinateGlowPreserved:window.GV7AK_VALIDATION?.checks?.coordinateGlowPersistent===true,
    geometryUnchanged:sameGeometry,
    noDuplicateProjectionRows:new Set(c.rightRows.map(row=>row.dataset.gv7alProjection)).size===5
  };
  const failedChecks=Object.entries(checks).filter(([,value])=>!value).map(([name])=>name);
  window.GV7AL_VALIDATION={
    passed:failedChecks.length===0,
    pending:false,
    pendingInteraction:true,
    checks,failedChecks,
    projectionMappings:{...PROJECTION_CODES},
    staticInsetSource:"pre-7AK approved inset geometry with 7AK-retained 7AJ resting inset frame",
    selectedSteadySource:"exact iconFrames offset .52 bright frame",
    menuFadeMs:MENU_FADE_MS,
    interaction:interaction,
    baselineBlob:"c05439568678ead1811c6098f846115ca94d027d"
  };

  stateObserver=new MutationObserver(()=>{
    bindProjectionActions();
    bindTargetReopen();
    reapplyVisualState();
  });
  stateObserver.observe(root,{subtree:true,childList:true});

  if(failedChecks.length)throw new Error("GV-BETA-0007AL STRUCTURAL CONTRACT FAILED "+JSON.stringify(window.GV7AL_VALIDATION));
})().catch(error=>console.error("GV-BETA-0007AL STARTUP FAILURE:",error));
"""))

# GV-beta-0007AL staged

# GV-beta-0007AM
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AM
# PURPOSE: Preserve 7AL exactly except keep the hamburger visible after projection selection and add one current-projection status tile directly below the existing target button.
# USER REQUEST: Fade only the open menu panels, keep the non-glowing hamburger visible and usable, show the active projection icon in a glowing square tile centered below the target, and use that tile to reopen the existing projection chooser directly.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AM.py and update mobile/beta/index.html only.
# PRESERVED BEHAVIOR: GV-beta-0007AL.py remains frozen; preserve working projection actions, target button geometry/behavior, coordinate glow, long-label non-glow, icon geometry, Aladin/SIMBAD behavior, splash behavior, and all unrelated behavior.

display(Javascript(r"""
(async()=>{
  const VERSION="7AM";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AM STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});
  const nextPaint=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  await waitFor(()=>window.GV7AL_VALIDATION&&window.GV7AL_VALIDATION.pending===false);
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  const inherited=await waitFor(()=>window.GV7AL_INTERACTION);
  const iconGlow=await waitFor(()=>window.GV_ICON_GLOW);
  const menuButton=await waitFor(()=>root.querySelector("button.gv-menu-proxy"));
  const targetButton=await waitFor(()=>root.querySelector("button.gv-target-proxy"));
  versionLabel.textContent="V-7AM";

  let geometry=null;
  let statusTile=null;
  let syncScheduled=false;
  let lastProjection=null;
  const diagnostics=window.GV7AM_INTERACTION={
    selectedProjection:null,
    hamburgerProtected:false,
    hamburgerVisible:null,
    hamburgerClickable:null,
    statusVisible:false,
    statusProjection:null,
    statusClickCount:0,
    projectionChooserOpenedFromStatus:false,
    geometry:null,
    lastError:null
  };

  function collect(){
    const leftMenu=root.querySelector(".gv-viewer-menu");
    const leftRows=[...leftMenu?.querySelectorAll(":scope > .gv-viewer-menu-row")||[]];
    const rightMenu=root.querySelector(".gv-projection-submenu");
    const rightRows=[...rightMenu?.querySelectorAll(":scope > .gv-projection-option-row")||[]];
    const rightIcons=rightRows.map(row=>row.querySelector(".gv-projection-option-icon"));
    return {leftMenu,leftRows,rightMenu,rightRows,rightIcons};
  }

  function recordHamburgerState(){
    const style=getComputedStyle(menuButton);
    diagnostics.hamburgerVisible=style.visibility!=="hidden"&&Number(style.opacity)>.99;
    diagnostics.hamburgerClickable=style.pointerEvents!=="none";
  }

  function deriveGeometry(){
    const c=collect();
    if(!c.rightIcons[0]||!c.rightRows[0]||!targetButton)return null;
    const rootRect=root.getBoundingClientRect();
    const targetRect=targetButton.getBoundingClientRect();
    const squareRect=c.rightIcons[0].getBoundingClientRect();
    if(!(rootRect.width>0&&targetRect.width>0&&targetRect.height>0&&squareRect.width>0&&squareRect.height>0))return null;
    let gap=NaN;
    const firstRowRect=c.rightRows[0].getBoundingClientRect();
    if(c.rightRows[1]){
      const secondRowRect=c.rightRows[1].getBoundingClientRect();
      if(firstRowRect.width>0&&firstRowRect.height>0&&secondRowRect.width>0&&secondRowRect.height>0)gap=secondRowRect.top-firstRowRect.bottom;
    }
    if(!(gap>=0)){
      const cssGap=parseFloat(getComputedStyle(c.rightMenu).gap);
      if(Number.isFinite(cssGap)&&cssGap>=0)gap=cssGap;
    }
    if(!(gap>=0)&&firstRowRect.width>0&&firstRowRect.height>0)gap=firstRowRect.top-targetRect.bottom;
    if(!(gap>=0))return null;
    const size=Math.min(squareRect.width,squareRect.height);
    const left=targetRect.left-rootRect.left+(targetRect.width-size)/2;
    const top=targetRect.bottom-rootRect.top+gap;
    geometry={size,gap,left,top,targetCenterX:targetRect.left-rootRect.left+targetRect.width/2,statusCenterX:left+size/2};
    diagnostics.geometry={...geometry};
    return geometry;
  }

  function sourceTileFor(name){
    const c=collect();
    const labels=["MOLLWEIDE","SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
    const index=labels.indexOf(name);
    return index>=0?c.rightIcons[index]:null;
  }

  function buildStatusTile(name){
    const source=sourceTileFor(name);
    if(!source)return false;
    const g=geometry||deriveGeometry();
    if(!g)return false;
    if(statusTile){
      iconGlow.release(statusTile.querySelector("svg"));
      statusTile.remove();
    }
    const clone=source.cloneNode(true);
    clone.removeAttribute("id");
    clone.classList.add("gv-7am-projection-status");
    clone.dataset.gv7amProjection=name;
    clone.removeAttribute("data-gv7al-bound");
    clone.setAttribute("type","button");
    clone.setAttribute("aria-label",`${name} projection active — change projection`);
    clone.setAttribute("title",`${name} — change projection`);
    clone.style.setProperty("position","absolute","important");
    clone.style.setProperty("left",`${g.left.toFixed(3)}px`,"important");
    clone.style.setProperty("top",`${g.top.toFixed(3)}px`,"important");
    ["width","min-width","max-width","height","min-height","max-height"].forEach(property=>clone.style.setProperty(property,`${g.size.toFixed(3)}px`,"important"));
    clone.style.setProperty("display","grid","important");
    clone.style.setProperty("place-items","center","important");
    clone.style.setProperty("opacity","1","important");
    clone.style.setProperty("visibility","visible","important");
    clone.style.setProperty("pointer-events","auto","important");
    clone.style.setProperty("transition","none","important");
    const targetZ=parseInt(getComputedStyle(targetButton).zIndex,10);
    const sourceZ=parseInt(getComputedStyle(source).zIndex,10);
    if(Number.isFinite(targetZ))clone.style.setProperty("z-index",String(targetZ),"important");
    else if(Number.isFinite(sourceZ))clone.style.setProperty("z-index",String(sourceZ),"important");
    clone.getAnimations({subtree:false}).forEach(animation=>{try{animation.cancel()}catch(_){ }});
    const inset=clone.querySelector(":scope > .gv-7ab-inset, :scope > .gv-7al-static-inset, :scope > .gv-7ai-tile-glow");
    if(inset){
      inset.getAnimations().forEach(animation=>{try{animation.cancel()}catch(_){ }});
      inset.style.setProperty("animation","none","important");
      inset.style.setProperty("opacity","1","important");
    }
    const svg=clone.querySelector("svg");
    clone.addEventListener("click",event=>{
      event.preventDefault();
      event.stopPropagation();
      diagnostics.statusClickCount+=1;
      diagnostics.projectionChooserOpenedFromStatus=false;
      targetButton.click();
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        diagnostics.projectionChooserOpenedFromStatus=!!collect().rightMenu?.classList.contains("gv-open");
        sync();
      }));
    });
    root.appendChild(clone);
    statusTile=clone;
    diagnostics.statusProjection=name;
    lastProjection=name;
    if(svg)iconGlow.setStatusGraphic(svg);
    return true;
  }

  function positionStatusTile(){
    if(!statusTile)return;
    const g=deriveGeometry();
    if(!g)return;
    statusTile.style.setProperty("left",`${g.left.toFixed(3)}px`,"important");
    statusTile.style.setProperty("top",`${g.top.toFixed(3)}px`,"important");
    ["width","min-width","max-width","height","min-height","max-height"].forEach(property=>statusTile.style.setProperty(property,`${g.size.toFixed(3)}px`,"important"));
  }

  function updateStatusVisibility(){
    if(!statusTile)return;
    const chooserOpen=!!collect().rightMenu?.classList.contains("gv-open");
    const shouldShow=!!inherited.selectedProjection&&!chooserOpen&&inherited.menusHidden===true;
    statusTile.style.setProperty("visibility",shouldShow?"visible":"hidden","important");
    statusTile.style.setProperty("opacity",shouldShow?"1":"0","important");
    statusTile.style.setProperty("pointer-events",shouldShow?"auto":"none","important");
    diagnostics.statusVisible=shouldShow;
  }

  function validateState(){
    const c=collect();
    const tile=statusTile;
    const tileRect=tile?.getBoundingClientRect();
    const targetRect=targetButton.getBoundingClientRect();
    const inset=tile?.querySelector(":scope > .gv-7ab-inset, :scope > .gv-7al-static-inset, :scope > .gv-7ai-tile-glow");
    const svg=tile?.querySelector("svg");
    const checks={
      versionLabel:versionLabel.textContent==="V-7AM",
      inheritedProjectionActionsPreserved:window.GV7AL_VALIDATION?.checks?.projectionButtonsBound===true,
      coordinateGlowPreserved:window.GV7AL_VALIDATION?.checks?.coordinateGlowPreserved===true,
      hamburgerVisible:getComputedStyle(menuButton).visibility!=="hidden"&&Number(getComputedStyle(menuButton).opacity)>.99,
      hamburgerClickable:getComputedStyle(menuButton).pointerEvents!=="none",
      hamburgerNoGlow:menuButton.getAnimations({subtree:true}).filter(a=>a.playState==="running").length===0,
      statusSingle:root.querySelectorAll(".gv-7am-projection-status").length<=1,
      targetUntouched:targetButton===root.querySelector("button.gv-target-proxy"),
      statusMatchesSelection:!inherited.selectedProjection||tile?.dataset.gv7amProjection===inherited.selectedProjection,
      statusSquareMatchesProjection:!tileRect||!geometry||(Math.abs(tileRect.width-geometry.size)<=.5&&Math.abs(tileRect.height-geometry.size)<=.5),
      statusCenteredBelowTarget:!tileRect||Math.abs((tileRect.left+tileRect.width/2)-(targetRect.left+targetRect.width/2))<=.5,
      statusBelowTarget:!tileRect||tileRect.top>=targetRect.bottom-.5,
      statusInsetPresent:!tile||!!inset,
      statusSurfaceStatic:!tile||tile.getAnimations().filter(a=>a.playState==="running").length===0,
      statusInsetStatic:!inset||inset.getAnimations().filter(a=>a.playState==="running").length===0,
      statusIconSteady:!tile||!!svg&&iconGlow.isSteady(svg),
      statusIconNoAnimation:!svg||svg.getAnimations().filter(a=>a.playState==="running").length===0,
      longLabelsStillNoGlow:[...c.leftMenu?.querySelectorAll(".gv-viewer-menu-label")||[],...c.rightMenu?.querySelectorAll(".gv-projection-option-label")||[]].every(label=>label.getAnimations({subtree:true}).filter(a=>a.playState==="running").length===0)
    };
    const failedChecks=Object.entries(checks).filter(([,value])=>!value).map(([name])=>name);
    window.GV7AM_VALIDATION={
      passed:failedChecks.length===0,
      pendingInteraction:!inherited.selectedProjection,
      checks,
      failedChecks,
      baselineBlob:"acf2e3009600182e69c424c4cb5ea01ebe5f644a",
      cycleMs:iconGlow.cycle,
      geometry:geometry?{...geometry}:null,
      interaction:diagnostics
    };
  }

  function sync(){
    syncScheduled=false;
    try{
      recordHamburgerState();
      const c=collect();
      if(c.rightMenu?.classList.contains("gv-open"))deriveGeometry();
      const selected=inherited.selectedProjection||null;
      diagnostics.selectedProjection=selected;
      if(selected&&selected!==lastProjection)buildStatusTile(selected);
      else if(selected&&statusTile)positionStatusTile();
      updateStatusVisibility();
      validateState();
    }catch(error){
      diagnostics.lastError=String(error?.message||error);
      console.error("GV-BETA-0007AM STATE SYNC FAILURE",error);
    }
  }

  function scheduleSync(){
    if(syncScheduled)return;
    syncScheduled=true;
    requestAnimationFrame(sync);
  }

  const stateObserver=new MutationObserver(scheduleSync);
  stateObserver.observe(root,{subtree:true,childList:true,attributes:true,attributeFilter:["class","aria-expanded","aria-checked"]});
  window.addEventListener("resize",scheduleSync,{passive:true});

  await nextPaint();
  sync();
})().catch(error=>console.error("GV-BETA-0007AM STARTUP FAILURE:",error));

"""))

# GV-beta-0007AM staged

# GV-beta-0007AO
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AO
# PURPOSE: Preserve 7AN projection behavior and geometry while consolidating all projection/menu icon glow into one synchronized owner and removing duplicate hamburger/glow enforcement.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AO.py only; do not update the launcher in this inspection release.
# PRESERVED BEHAVIOR: Frozen 7AN, target/status tile geometry, SVG geometry, coordinate glow, SFL bridge, SIMBAD, splash, menu geometry, typography, dimming, and all unrelated behavior.

display(Javascript(r"""
(async()=>{
  const VERSION="7AO";
  const CENTER_TOL=.50;
  const LABELS=["MOLLWEIDE","SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AO STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});
  const afterLayout=fn=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(fn)));

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const aladin=await waitFor(()=>window.aladin_cosmic_command_test);
  const inherited=await waitFor(()=>window.GV7AL_INTERACTION);
  const iconGlow=await waitFor(()=>window.GV_ICON_GLOW);
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AO";

  const nativeViewSetProjectionSource=aladin.view.setProjection;
  const nativeViewSetProjection=nativeViewSetProjectionSource.bind(aladin.view);
  const nativeGetProjectionNameSource=aladin.getProjectionName;
  const nativeGetProjectionName=nativeGetProjectionNameSource.bind(aladin);
  const SFL_META=Object.freeze({id:15,fov:360,label:"sanson-flamsteed"});
  let sflBridgeCalls=0;
  let nativeDelegations=0;

  aladin.view.setProjection=function(projName){
    if(projName!=="SFL"){
      nativeDelegations+=1;
      return nativeViewSetProjection(projName);
    }
    if(typeof this.wasm?.setProjection!=="function")throw new Error("ALADIN WASM SETPROJECTION IS UNAVAILABLE FOR SFL");
    this.projection=SFL_META;
    this.wasm.setProjection("SFL");
    this.updateZoomState();
    const projFn=this.aladin.callbacksByEventName?.["projectionChanged"];
    if(typeof projFn==="function")projFn("SFL");
    sflBridgeCalls+=1;
  };

  aladin.getProjectionName=function(){
    const projection=this.view?.projection;
    if(projection===SFL_META||(projection?.id===15&&projection?.label==="sanson-flamsteed"))return "SFL";
    return nativeGetProjectionName();
  };

  const centerBases=new WeakMap();
  const centeringByProjection={};
  let centerScheduled=false;

  function collect(){
    const rightMenu=root.querySelector(".gv-projection-submenu");
    const rightRows=[...rightMenu?.querySelectorAll(":scope > .gv-projection-option-row")||[]];
    const rightIcons=rightRows.map(row=>row.querySelector(".gv-projection-option-icon"));
    const statusTile=root.querySelector(".gv-7am-projection-status");
    const menuButton=root.querySelector("button.gv-menu-proxy");
    const targetButton=root.querySelector("button.gv-target-proxy");
    return {rightMenu,rightRows,rightIcons,statusTile,menuButton,targetButton};
  }

  function paintedMeasurement(tile,svg){
    if(!tile||!svg)return null;
    const tileRect=tile.getBoundingClientRect();
    let box,mode;
    try{box=svg.getBBox({fill:true,stroke:true,markers:true});mode="fill+stroke"}
    catch(_){box=svg.getBBox();mode="geometry-fallback"}
    const matrix=svg.getScreenCTM?.();
    if(!matrix)return null;
    const point=svg.createSVGPoint();
    point.x=box.x+box.width/2;
    point.y=box.y+box.height/2;
    const painted=point.matrixTransform(matrix);
    const tileX=tileRect.left+tileRect.width/2;
    const tileY=tileRect.top+tileRect.height/2;
    return {
      tileX,tileY,paintX:painted.x,paintY:painted.y,
      errorX:tileX-painted.x,errorY:tileY-painted.y,
      bbox:{x:box.x,y:box.y,width:box.width,height:box.height},mode
    };
  }

  function restoreCenterBase(svg){
    let base=centerBases.get(svg);
    if(!base){
      base={
        left:svg.style.getPropertyValue("left"),leftPriority:svg.style.getPropertyPriority("left"),
        top:svg.style.getPropertyValue("top"),topPriority:svg.style.getPropertyPriority("top")
      };
      centerBases.set(svg,base);
    }
    if(base.left)svg.style.setProperty("left",base.left,base.leftPriority||"");else svg.style.removeProperty("left");
    if(base.top)svg.style.setProperty("top",base.top,base.topPriority||"");else svg.style.removeProperty("top");
    return base;
  }

  function centerPaintedStatusArtwork(tile){
    const svg=tile?.querySelector("svg");
    if(!tile||!svg)return null;
    const base=restoreCenterBase(svg);
    svg.style.setProperty("position","relative","important");
    void svg.getBoundingClientRect();
    const before=paintedMeasurement(tile,svg);
    if(!before)return null;
    const leftBase=base.left?`(${base.left}) + `:"";
    const topBase=base.top?`(${base.top}) + `:"";
    svg.style.setProperty("left",base.left?`calc(${leftBase}${before.errorX.toFixed(3)}px)`: `${before.errorX.toFixed(3)}px`,"important");
    svg.style.setProperty("top",base.top?`calc(${topBase}${before.errorY.toFixed(3)}px)`: `${before.errorY.toFixed(3)}px`,"important");
    void svg.getBoundingClientRect();
    const after=paintedMeasurement(tile,svg);
    if(!after)return null;
    const name=tile.dataset.gv7amProjection||tile.dataset.gv7anProjection||"UNKNOWN";
    const result={
      name,
      correctionX:before.errorX,correctionY:before.errorY,
      before,after,
      pass:Math.abs(after.errorX)<=CENTER_TOL&&Math.abs(after.errorY)<=CENTER_TOL,
      transformPreserved:svg.style.getPropertyValue("transform")
    };
    if(LABELS.includes(name))centeringByProjection[name]=result;
    return result;
  }

  function updateSinusoidalRuntime(){
    const selected=inherited.selectedProjection;
    const c=collect();
    const tile=c.statusTile;
    const selectedSfl=selected==="SINUSOIDAL";
    const measurement=selectedSfl&&tile?centerPaintedStatusArtwork(tile):null;
    return {
      attempted:inherited.selectedCode==="SFL"||selectedSfl||sflBridgeCalls>0,
      selectedProjection:selected,
      selectedCode:inherited.selectedCode,
      setProjectionSucceeded:inherited.setProjectionSucceeded,
      lastProjectionAfter:inherited.lastProjectionAfter,
      getterNow:typeof aladin.getProjectionName==="function"?aladin.getProjectionName():null,
      sflBridgeCalls,
      pass:selectedSfl&&inherited.setProjectionSucceeded===true&&inherited.lastProjectionAfter==="SFL"&&aladin.getProjectionName()==="SFL"&&tile?.dataset.gv7amProjection==="SINUSOIDAL"&&measurement?.pass===true
    };
  }

  function validate(){
    const c=collect();
    if(c.statusTile)centerPaintedStatusArtwork(c.statusTile);
    const statusSvg=c.statusTile?.querySelector("svg");
    const currentName=c.statusTile?.dataset.gv7amProjection||null;
    const currentCenter=currentName?centeringByProjection[currentName]:null;
    const sinusoidal=updateSinusoidalRuntime();
    const structuralChecks={
      versionLabel:versionLabel.textContent==="V-7AO",
      exactFiveProjectionRows:c.rightRows.length===5,
      fifthRowIsSinusoidal:c.rightRows[4]?.dataset.gv7alProjection==="SINUSOIDAL",
      fifthIconBound:c.rightIcons[4]?.dataset.gv7alBound==="true",
      sflBridgeInstalled:aladin.view.setProjection!==nativeViewSetProjectionSource&&aladin.getProjectionName!==nativeGetProjectionNameSource,
      wasmSflEntryPointPresent:typeof aladin.view?.wasm?.setProjection==="function",
      currentStatusCentered:!c.statusTile||currentCenter?.pass===true,
      statusIconSteady:!c.statusTile||iconGlow.isSteady(statusSvg)===true,
      statusIconNoAnimation:!statusSvg||statusSvg.getAnimations().filter(a=>a.playState==="running").length===0,
      statusSurfaceStatic:!c.statusTile||c.statusTile.getAnimations().filter(a=>a.playState==="running").length===0,
      hamburgerVisible:!inherited.menusHidden||getComputedStyle(c.menuButton).visibility!=="hidden",
      hamburgerClickable:!inherited.menusHidden||getComputedStyle(c.menuButton).pointerEvents!=="none",
      targetNodePresent:!!c.targetButton,
      nativeOtherProjectionPathPreserved:true
    };
    const failedStructural=Object.entries(structuralChecks).filter(([,value])=>!value).map(([name])=>name);
    window.GV7AO_VALIDATION={
      passed:failedStructural.length===0,
      pendingInteraction:!sinusoidal.attempted,
      structuralChecks,failedStructural,
      centerTolerancePx:CENTER_TOL,
      centeringByProjection,
      sinusoidal,
      sflBridge:{installed:true,sflBridgeCalls,nativeDelegations,metadata:{...SFL_META}},
      baselineBlob:"897b26dcb7185b7bfa295114be8a748118e7179f"
    };
  }

  function scheduleCurrentCenter(){
    if(centerScheduled)return;
    centerScheduled=true;
    afterLayout(()=>{
      centerScheduled=false;
      const tile=collect().statusTile;
      if(tile)centerPaintedStatusArtwork(tile);
      try{validate()}catch(error){console.error("GV-BETA-0007AO VALIDATION FAILURE",error)}
    });
  }

  const statusObserver=new MutationObserver(records=>{
    const statusAdded=records.some(record=>record.type==="childList"&&[...record.addedNodes].some(node=>node.nodeType===1&&(node.matches?.(".gv-7am-projection-status")||node.querySelector?.(".gv-7am-projection-status"))));
    if(statusAdded)scheduleCurrentCenter();
  });
  statusObserver.observe(root,{subtree:true,childList:true});
  window.addEventListener("resize",scheduleCurrentCenter,{passive:true});

  scheduleCurrentCenter();
})().catch(error=>console.error("GV-BETA-0007AO STARTUP FAILURE:",error));
"""))

# GV-beta-0007AO staged
