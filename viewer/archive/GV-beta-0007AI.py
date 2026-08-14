from IPython.display import HTML, Javascript, display

# GV-beta-0007AI
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AI
# PURPOSE: Preserve 7AG geometry while synchronizing brighter tile/icon/hamburger/coordinate neon on one 1000 ms clock and matching Projection submenu title height.
# USER REQUEST: Preserve GV-beta-0007AG exactly except V-7AI identity, 1000 ms synchronized glow, stronger authorized tile/icon/neon intensity, right-title visual size matching, and ORTHO validation.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AI.py and its dedicated launcher/PWA release chain only.
# PRESERVED BEHAVIOR: 7AG geometry, Projection/Mollweide SVG geometry, coordinate calculations/switching, target/SIMBAD, Aladin, navigation, controls, splash behavior, fonts except authorized launcher typography, actions, and all unrelated behavior.

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
  const CYCLE=1000;
  const EASING="cubic-bezier(.42,0,.18,1)";
  const insetFrames=[
    {offset:0,backgroundColor:"rgba(5,18,32,.10)",boxShadow:"inset 0 0 0 1px rgba(143,234,255,.28), inset 0 0 6px rgba(98,216,255,.18), inset 0 0 10px rgba(157,124,255,.10)"},
    {offset:.24,backgroundColor:"rgba(18,82,135,.26)",boxShadow:"inset 0 0 0 1.4px rgba(184,244,255,.70), inset 0 0 9px rgba(98,216,255,.62), inset 0 0 15px rgba(79,166,255,.44), inset 0 0 19px rgba(157,124,255,.26)"},
    {offset:.52,backgroundColor:"rgba(30,132,208,.48)",boxShadow:"inset 0 0 0 2px rgba(238,254,255,1), inset 0 0 10px rgba(143,234,255,1), inset 0 0 17px rgba(79,166,255,.98), inset 0 0 24px rgba(157,124,255,.68)"},
    {offset:.76,backgroundColor:"rgba(18,88,145,.29)",boxShadow:"inset 0 0 0 1.5px rgba(184,244,255,.76), inset 0 0 10px rgba(98,216,255,.66), inset 0 0 16px rgba(79,166,255,.48), inset 0 0 20px rgba(157,124,255,.28)"},
    {offset:1,backgroundColor:"rgba(5,18,32,.10)",boxShadow:"inset 0 0 0 1px rgba(143,234,255,.28), inset 0 0 6px rgba(98,216,255,.18), inset 0 0 10px rgba(157,124,255,.10)"}
  ];
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
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AI STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AD RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AI COULD NOT EXTRACT 7AD BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AI";
  window.GV7AI_VALIDATION={passed:false,pending:true,status:"AWAITING PROJECTION SUBMENU"};

  const rect=e=>{const r=e.getBoundingClientRect();return {left:r.left,top:r.top,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
  const style=e=>{const s=getComputedStyle(e);return {fontSize:s.fontSize,fontFamily:s.fontFamily,fontWeight:s.fontWeight,lineHeight:s.lineHeight,letterSpacing:s.letterSpacing,color:s.color,textShadow:s.textShadow}};
  const sameNumber=(a,b)=>Math.abs(a-b)<=TOL;
  const sameRect=(a,b)=>["left","top","width","height","right","bottom"].every(k=>sameNumber(a[k],b[k]));
  const sameStyle=(a,b)=>Object.keys(a).every(k=>a[k]===b[k]);
  const scaleY15=value=>{if(!value||value==="none")return false;try{const m=new DOMMatrixReadOnly(value);return Math.abs(m.a-1)<.01&&Math.abs(m.b)<.01&&Math.abs(m.c)<.01&&Math.abs(m.d-1.5)<.01}catch(_){return false}};

  let observer=null;
  let patched=false;
  let pulseObserver=null;
  let pulseEnforceScheduled=false;
  let globalPulseStart=null;
  let projectionAnimations=[];
  let menuAnimations=[];
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

  function ensureTileGlowLayer(tile){
    let layer=tile.querySelector(":scope > .gv-7ai-tile-glow");
    if(!layer){
      layer=document.createElement("span");
      layer.className="gv-7ai-tile-glow";
      layer.setAttribute("aria-hidden","true");
      layer.style.setProperty("position","absolute","important");
      layer.style.setProperty("inset","1px","important");
      layer.style.setProperty("border-radius","4px","important");
      layer.style.setProperty("pointer-events","none","important");
      layer.style.setProperty("z-index","0","important");
      layer.style.background="transparent";
      tile.appendChild(layer);
    }
    [...tile.children].filter(child=>child!==layer).forEach(child=>{
      child.style?.setProperty?.("position","relative","important");
      child.style?.setProperty?.("z-index","2","important");
    });
    return layer;
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

  function cancelAnimations(el){
    if(!el)return;
    el.getAnimations({subtree:true}).forEach(a=>{try{a.cancel()}catch(_){ }});
    el.style.setProperty("animation","none","important");
  }

  function normalizeEasing(value){
    return String(value||"").replace(/\s+/g,"").replace(/0\./g,".");
  }

  function animateOwned(el,frames,options,list){
    if(!el)return null;
    const a=el.animate(frames,options);
    a.startTime=getGlobalPulseStart();
    list.push(a);
    return a;
  }

  function animateTile(tile,options,list){
    if(!tile)return;
    cancelAnimations(tile);
    const layer=ensureTileGlowLayer(tile);
    animateOwned(tile,insetFrames,options,list);
    animateOwned(layer,insetFrames,options,list);
  }

  function enforceProjectionPulse(c=collect()){
    if(!c.leftLabels[0]||!c.leftIcons[0])return false;
    getGlobalPulseStart();
    const tileTargets=[c.leftLabels[0],c.leftIcons[0],...c.rightLabels,...c.rightIcons].filter(Boolean);
    const svgTargets=[c.leftIcons[0].querySelector("svg"),...c.rightIcons.map(icon=>icon?.querySelector("svg"))].filter(Boolean);
    const options={duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"};
    const next=[];
    tileTargets.forEach(el=>animateTile(el,options,next));
    svgTargets.forEach(svg=>{
      svg.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});
      svg.style.setProperty("animation","none","important");
      svg.style.setProperty("position","relative","important");
      svg.style.setProperty("z-index","2","important");
      animateOwned(svg,iconFrames,options,next);
    });
    projectionAnimations=next;
    return true;
  }

  function enforceMenuPulse(c=collect()){
    const menuButton=root.querySelector("button.gv-menu-proxy");
    const menuStack=menuButton?.querySelector(".gv-menu-stack");
    if(!menuButton||!menuStack)return false;
    getGlobalPulseStart();
    const options={duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"};
    const next=[];
    animateTile(menuButton,options,next);
    menuStack.getAnimations({subtree:true}).forEach(a=>{try{a.cancel()}catch(_){ }});
    menuStack.style.setProperty("animation","none","important");
    menuStack.style.setProperty("position","absolute","important");
    menuStack.style.setProperty("z-index","2","important");
    animateOwned(menuStack,iconFrames,options,next);

    const projectionOpen=!!c.rightMenu?.classList.contains("gv-open");
    c.leftRows.slice(1).forEach(row=>{
      const label=row.querySelector(".gv-viewer-menu-label");
      const icon=row.querySelector(".gv-viewer-menu-icon");
      if(projectionOpen){
        [label,icon].filter(Boolean).forEach(tile=>{
          cancelAnimations(tile);
          const layer=ensureTileGlowLayer(tile);
          layer.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});
          layer.style.opacity="0";
        });
        return;
      }
      [label,icon].filter(Boolean).forEach(tile=>animateTile(tile,options,next));
      const labelContent=contentTarget(label,true);
      const iconContent=contentTarget(icon,false);
      [labelContent,iconContent].filter(Boolean).forEach(content=>{
        content.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});
        content.style?.setProperty?.("position","relative","important");
        content.style?.setProperty?.("z-index","2","important");
        animateOwned(content,iconFrames,options,next);
      });
    });
    menuAnimations=next;
    return true;
  }

  function enforceAllPulses(){
    const c=collect();
    enforceProjectionPulse(c);
    enforceMenuPulse(c);
    return true;
  }

  function ensurePulseObserver(){
    if(pulseObserver)return;
    pulseObserver=new MutationObserver(()=>{
      if(pulseEnforceScheduled)return;
      pulseEnforceScheduled=true;
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        pulseEnforceScheduled=false;
        enforceAllPulses();
      }));
    });
    pulseObserver.observe(root,{subtree:true,childList:true,attributes:true,attributeFilter:["class"]});
  }

  async function initializeProjectionPulse(){
    await new Promise(resolve=>setTimeout(resolve,450));
    await waitFor(()=>collect().leftLabels[0]&&collect().leftIcons[0]&&root.querySelector("button.gv-menu-proxy"));
    getGlobalPulseStart();
    enforceAllPulses();
    ensurePulseObserver();
    return true;
  }

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

    window.GV7AI_COORDINATE_GLOW={
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

  function projectionPulseDiagnostics(c){
    const tileTargets=[c.leftLabels[0],c.leftIcons[0],...c.rightLabels,...c.rightIcons].filter(Boolean);
    const foreign=[];
    const owned=new Set(projectionAnimations);
    tileTargets.forEach(el=>el.getAnimations({subtree:true}).forEach(a=>{if(a.playState==="running"&&!owned.has(a)&&!foreign.includes(a))foreign.push(a)}));
    const timings=projectionAnimations.map(a=>a.effect.getTiming());
    const currentTimes=projectionAnimations.map(a=>Number(a.currentTime)).filter(Number.isFinite);
    const phaseSpread=currentTimes.length?Math.max(...currentTimes)-Math.min(...currentTimes):Infinity;
    return {
      count:projectionAnimations.length,
      expectedCount:30,
      sharedStart:projectionAnimations.length===30&&projectionAnimations.every(a=>a.startTime===globalPulseStart),
      allRunning:projectionAnimations.length===30&&projectionAnimations.every(a=>a.playState==="running"),
      durationMatch:timings.length===30&&timings.every(t=>t.duration===CYCLE),
      easingMatch:timings.length===30&&timings.every(t=>normalizeEasing(t.easing)===normalizeEasing(EASING)),
      phaseSpreadMs:phaseSpread,
      phaseMatch:phaseSpread<=5,
      foreignRunningCount:foreign.length,
      noForeignRunning:foreign.length===0,
      startTime:globalPulseStart,
      cycleMs:CYCLE,
      easing:EASING
    };
  }

  function menuPulseDiagnostics(c){
    const projectionOpen=!!c.rightMenu?.classList.contains("gv-open");
    const hamburger=root.querySelector("button.gv-menu-proxy");
    const stack=hamburger?.querySelector(".gv-menu-stack");
    const timings=menuAnimations.map(a=>a.effect.getTiming());
    const inactive=c.leftRows.slice(1);
    const inactiveNoPulse=inactive.every(row=>row.getAnimations({subtree:true}).filter(a=>a.playState==="running").length===0);
    return {
      projectionOpen,
      count:menuAnimations.length,
      allRunning:menuAnimations.length>0&&menuAnimations.every(a=>a.playState==="running"),
      sharedStart:menuAnimations.length>0&&menuAnimations.every(a=>a.startTime===globalPulseStart),
      durationMatch:timings.length>0&&timings.every(t=>t.duration===CYCLE),
      easingMatch:timings.length>0&&timings.every(t=>normalizeEasing(t.easing)===normalizeEasing(EASING)),
      hamburgerTileHasOwnedGlow:!!hamburger?.querySelector(":scope > .gv-7ai-tile-glow"),
      hamburgerStackAnimationSuppressed:getComputedStyle(stack).animationName==="none",
      inactiveNoPulseWhenProjectionOpen:!projectionOpen||inactiveNoPulse
    };
  }

  async function finalizeAndValidate(baseline){
    const c=collect();
    const centering=centerProjectionIcons(c);
    await projectionPulseReady;
    enforceProjectionPulse(c);
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
    finalizeAndValidate(baseline).catch(error=>console.error("GV-BETA-0007AI FINALIZATION FAILURE:",error));
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
    const projectionAnimations=projection?.getAnimations({subtree:true}).filter(a=>a.playState==="running")||[];
    const mollweideAnimations=mollweide?.getAnimations({subtree:true}).filter(a=>a.playState==="running")||[];
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
    const pulse=projectionPulseDiagnostics(c);
    const menuPulse=menuPulseDiagnostics(c);
    const coordinate=await validateCoordinateGlow();
    const newCenterNames=["SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
    const newCentersPass=newCenterNames.every(name=>centering?.[name]&&Math.abs(centering[name].errorX)<CENTER_TOL&&Math.abs(centering[name].errorY)<CENTER_TOL);
    const checks={
      versionLabel:versionLabel.textContent==="V-7AI",
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
      projectionGlowRunning:projectionAnimations.length>=2,
      projectionTilesOwnGlow:[c.leftLabels[0],c.leftIcons[0],...c.rightLabels,...c.rightIcons].every(tile=>!!tile?.querySelector(":scope > .gv-7ai-tile-glow")),
      hamburgerTileGlow:menuPulse.hamburgerTileHasOwnedGlow,
      hamburgerLegacyPulseSuppressed:menuPulse.hamburgerStackAnimationSuppressed,
      menuPulseSharedStart:menuPulse.sharedStart,
      menuPulseDuration:menuPulse.durationMatch,
      menuPulseEasing:menuPulse.easingMatch,
      menuProjectionDimmingPreserved:menuPulse.inactiveNoPulseWhenProjectionOpen,
      mollweideGlowRunning:mollweideAnimations.length>=2,
      projectionSvgGeometryUnchanged:(projection?.querySelector("svg")?.innerHTML||"")===baseline.projectionSvgInner,
      mollweideSvgPresent:!!mollweide?.querySelector("svg"),
      mollweideSvgGeometryUnchanged:(mollweide?.querySelector("svg")?.innerHTML||"")===baseline.mollweideSvgInner,
      fourGeneratedIconTilesWereEmpty:baseline.generatedIconHtml.every(html=>html.trim()===""),
      fourGeneratedIconTilesPopulated:iconPopulatedStates.every(Boolean),
      exactApprovedIconGeometry:iconGeometryChecks.every(Boolean),
      newIconSvgSize24px:newSvgRects.every(r=>sameNumber(r.width,24)&&sameNumber(r.height,24)),
      fourNewIconsPaintCentered:newCentersPass,
      mollweideCenterMeasured:!!centering?.MOLLWEIDE&&Math.abs(centering.MOLLWEIDE.errorX)<CENTER_TOL&&Math.abs(centering.MOLLWEIDE.errorY)<CENTER_TOL,
      projectionPulseCount:pulse.count===pulse.expectedCount,
      projectionPulseSharedStart:pulse.sharedStart,
      projectionPulseAllRunning:pulse.allRunning,
      projectionPulseDuration:pulse.durationMatch,
      projectionPulseEasing:pulse.easingMatch,
      projectionPulsePhase:pulse.phaseMatch,
      projectionPulseNoForeignClocks:pulse.noForeignRunning,
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
    window.GV7AI_VALIDATION={
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
      projectionPulse:pulse,
      menuPulse,
      coordinateGlow:coordinate,
      projectionModeOpen:open,
      baseline:"GV-beta-0007AD.py@19f5a381314e1ebb336f7d25c4df9fdb54163301",
      fontSizeContract:"right Projection submenu rendered glyph height matches PROJECTION within ±0.5 px",
      glyphTransformContract:"scaleY(1.5)",
      splash:"not loaded",
      newProjectionActions:"not wired",
      populatedIcons:["SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"]
    };
    if(!passed)throw new Error("GV-BETA-0007AI CONTRACT FAILED "+JSON.stringify(window.GV7AI_VALIDATION));
    return true;
  }

  let coordinateGlowError=null;
  const coordinateGlowPromise=startCoordinateGlow().catch(error=>{coordinateGlowError=error;window.GV7AI_COORDINATE_GLOW={passed:false,error:String(error)};return null});
  const projectionPulseReady=initializeProjectionPulse().catch(error=>{console.error("GV-BETA-0007AI PROJECTION PULSE INITIALIZATION FAILURE:",error);return false});

  observer=new MutationObserver(()=>{if(patched)return;const c=collect();if(c.rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch))});
  observer.observe(root,{subtree:true,childList:true});
  if(collect().rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch));
})().catch(error=>console.error("GV-BETA-0007AI STARTUP FAILURE:",error));
"""))

# GV-beta-0007AI staged
