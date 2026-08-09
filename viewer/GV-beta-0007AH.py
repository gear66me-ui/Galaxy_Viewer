from IPython.display import HTML, Javascript, display

# GV-beta-0007AH
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AH
# PURPOSE: Reduce the synchronized interaction-glow cycle from 6400 ms to 4480 ms, synchronize Projection/hamburger/menu/coordinate attention glows on one clock, and add ICRSD/GAL neon underglow.
# USER REQUEST: Preserve GV-beta-0007AG exactly except V-7AH identity, the authorized 30% shorter glow cycle, synchronized hamburger/menu attention glow, ICRSD/GAL neon underglow, and corresponding runtime validation.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AH.py and its dedicated launcher only.
# PRESERVED BEHAVIOR: 7AG geometry, icon centering/SVG geometry, labels, typography, Projection-mode dimming, coordinate calculations/switching, hamburger actions, target/SIMBAD, Aladin, navigation, controls, splash absence, fonts, projection actions, and all unrelated behavior.

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
  const CYCLE=4480;
  const EASING="cubic-bezier(.42,0,.18,1)";
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
  const coordinateFrames=[
    {offset:0,color:"#72A7E8",textShadow:"0 0 1px rgba(143,234,255,.18)"},
    {offset:.24,color:"#82BDF2",textShadow:"0 0 2px rgba(143,234,255,.40),0 0 4px rgba(79,166,255,.20)"},
    {offset:.52,color:"#D7F4FF",textShadow:"0 0 4px rgba(224,252,255,.92),0 0 7px rgba(98,216,255,.72),0 0 10px rgba(157,124,255,.28)"},
    {offset:.76,color:"#82BDF2",textShadow:"0 0 2px rgba(143,234,255,.40),0 0 4px rgba(79,166,255,.20)"},
    {offset:1,color:"#72A7E8",textShadow:"0 0 1px rgba(143,234,255,.18)"}
  ];
  const hamburgerStackFrames=[
    {offset:0,filter:"brightness(.88) drop-shadow(0 0 2px rgba(98,216,255,.22))"},
    {offset:.24,filter:"brightness(.98) drop-shadow(0 0 3px rgba(98,216,255,.38)) drop-shadow(0 0 4px rgba(157,124,255,.10))"},
    {offset:.52,filter:"brightness(1.18) drop-shadow(0 0 4px rgba(98,216,255,.64)) drop-shadow(0 0 7px rgba(157,124,255,.20))"},
    {offset:.76,filter:"brightness(.98) drop-shadow(0 0 3px rgba(98,216,255,.38)) drop-shadow(0 0 4px rgba(157,124,255,.10))"},
    {offset:1,filter:"brightness(.88) drop-shadow(0 0 2px rgba(98,216,255,.22))"}
  ];
  const hamburgerButtonFrames=[
    {offset:0,opacity:.18,boxShadow:"inset 0 0 3px rgba(98,216,255,.10), inset 0 0 6px rgba(157,124,255,.04)"},
    {offset:.24,opacity:.38,boxShadow:"inset 0 0 5px rgba(98,216,255,.22), inset 0 0 8px rgba(157,124,255,.08)"},
    {offset:.52,opacity:1,boxShadow:"inset 0 0 6px rgba(215,244,255,.62), inset 0 0 11px rgba(98,216,255,.42), inset 0 0 14px rgba(157,124,255,.16)"},
    {offset:.76,opacity:.38,boxShadow:"inset 0 0 5px rgba(98,216,255,.22), inset 0 0 8px rgba(157,124,255,.08)"},
    {offset:1,opacity:.18,boxShadow:"inset 0 0 3px rgba(98,216,255,.10), inset 0 0 6px rgba(157,124,255,.04)"}
  ];
  const menuContentFrames=[
    {offset:0,filter:"brightness(.92) drop-shadow(0 0 1px rgba(143,234,255,.12))"},
    {offset:.24,filter:"brightness(1.00) drop-shadow(0 0 2px rgba(143,234,255,.24)) drop-shadow(0 0 3px rgba(157,124,255,.08))"},
    {offset:.52,filter:"brightness(1.12) drop-shadow(0 0 3px rgba(215,244,255,.52)) drop-shadow(0 0 6px rgba(98,216,255,.38)) drop-shadow(0 0 8px rgba(157,124,255,.14))"},
    {offset:.76,filter:"brightness(1.00) drop-shadow(0 0 2px rgba(143,234,255,.24)) drop-shadow(0 0 3px rgba(157,124,255,.08))"},
    {offset:1,filter:"brightness(.92) drop-shadow(0 0 1px rgba(143,234,255,.12))"}
  ];
  const coordinateUnderglowFrames=[
    {offset:0,opacity:.18,boxShadow:"0 0 3px rgba(143,234,255,.10),0 0 7px rgba(79,166,255,.07),0 0 10px rgba(157,124,255,.03)"},
    {offset:.24,opacity:.42,boxShadow:"0 0 5px rgba(143,234,255,.24),0 0 10px rgba(79,166,255,.16),0 0 14px rgba(157,124,255,.07)"},
    {offset:.52,opacity:.82,boxShadow:"0 0 7px rgba(224,252,255,.42),0 0 13px rgba(98,216,255,.34),0 0 18px rgba(79,166,255,.22),0 0 22px rgba(157,124,255,.12)"},
    {offset:.76,opacity:.42,boxShadow:"0 0 5px rgba(143,234,255,.24),0 0 10px rgba(79,166,255,.16),0 0 14px rgba(157,124,255,.07)"},
    {offset:1,opacity:.18,boxShadow:"0 0 3px rgba(143,234,255,.10),0 0 7px rgba(79,166,255,.07),0 0 10px rgba(157,124,255,.03)"}
  ];
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AH STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AD RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AH COULD NOT EXTRACT 7AD BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AH";
  window.GV7AH_VALIDATION={passed:false,pending:true,status:"AWAITING PROJECTION SUBMENU"};

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
  let globalPulseStart=document.timeline.currentTime??performance.now();
  let projectionAnimations=[];
  let hamburgerAnimations=[];
  let hamburgerExpectedCount=0;
  let coordinateFrameEl=null;
  let coordinateAnimation=null;
  let coordinateUnderglowEl=null;
  let coordinateUnderglowAnimation=null;
  let coordinateInitialFrame=null;
  let coordinateFrameObserver=null;

  function collect(){
    const leftMenu=root.querySelector(".gv-viewer-menu");
    const leftRows=[...leftMenu?.querySelectorAll(":scope > .gv-viewer-menu-row")||[]];
    const rightMenu=root.querySelector(".gv-projection-submenu");
    const rightRows=[...rightMenu?.querySelectorAll(":scope > .gv-projection-option-row")||[]];
    const leftLabels=leftRows.map(r=>r.querySelector(".gv-viewer-menu-label"));
    const leftIcons=leftRows.map(r=>r.querySelector(".gv-viewer-menu-icon"));
    const rightLabels=rightRows.map(r=>r.querySelector(".gv-projection-option-label"));
    const rightIcons=rightRows.map(r=>r.querySelector(".gv-projection-option-icon"));
    const menuButton=root.querySelector("button.gv-menu-proxy");
    const menuStack=menuButton?.querySelector(".gv-menu-stack")||null;
    return {leftMenu,leftRows,rightMenu,rightRows,leftLabels,leftIcons,rightLabels,rightIcons,menuButton,menuStack};
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

  function ensureHamburgerButtonLayer(button){
    let layer=button?.querySelector(":scope > .gv-7ah-hamburger-glow");
    if(!button)return null;
    if(!layer){
      layer=document.createElement("span");
      layer.className="gv-7ah-hamburger-glow";
      layer.setAttribute("aria-hidden","true");
      button.insertBefore(layer,button.firstChild);
    }
    const s=layer.style;
    s.setProperty("position","absolute","important");
    s.setProperty("inset","2px","important");
    s.setProperty("border-radius","5px","important");
    s.setProperty("pointer-events","none","important");
    s.setProperty("z-index","0","important");
    s.setProperty("opacity","0");
    s.setProperty("box-shadow","none");
    s.setProperty("background","transparent","important");
    button.style.setProperty("isolation","isolate","important");
    return layer;
  }

  function cancelOwned(list){
    list.forEach(a=>{try{a.cancel()}catch(_){ }});
  }

  function menuLabelTarget(label){
    return label?.querySelector(":scope > .gv-space-age-glyph")||label?.querySelector(".gv-space-age-glyph")||null;
  }

  function menuIconTarget(icon){
    return icon?.querySelector("svg,img")||icon?.firstElementChild||null;
  }

  function enforceProjectionPulse(c=collect()){
    if(!c.leftLabels[0]||!c.leftIcons[0])return false;
    const tileTargets=[c.leftLabels[0],c.leftIcons[0],...c.rightLabels,...c.rightIcons].filter(Boolean);
    const svgTargets=[c.leftIcons[0].querySelector("svg"),...c.rightIcons.map(icon=>icon?.querySelector("svg"))].filter(Boolean);
    tileTargets.forEach(cancelAnimations);
    svgTargets.forEach(svg=>{svg.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});svg.style.setProperty("animation","none","important")});
    const options={duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"};
    const next=[];
    tileTargets.forEach(el=>{const a=el.animate(insetFrames,options);a.startTime=globalPulseStart;next.push(a)});
    svgTargets.forEach(svg=>{const a=svg.animate(iconFrames,options);a.startTime=globalPulseStart;next.push(a)});
    projectionAnimations=next;
    return true;
  }

  function enforceHamburgerPulse(c=collect()){
    if(!c.menuButton||!c.menuStack)return false;
    cancelOwned(hamburgerAnimations);
    hamburgerAnimations=[];
    c.menuStack.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});
    c.menuStack.style.setProperty("animation","none","important");
    c.menuStack.style.setProperty("z-index","1","important");
    const layer=ensureHamburgerButtonLayer(c.menuButton);
    const options={duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"};
    const buttonGlow=layer.animate(hamburgerButtonFrames,options);
    const stackGlow=c.menuStack.animate(hamburgerStackFrames,options);
    buttonGlow.startTime=globalPulseStart;
    stackGlow.startTime=globalPulseStart;
    hamburgerAnimations.push(buttonGlow,stackGlow);
    const projectionModeOpen=root.classList.contains("gv-7ad-projection-mode");
    const labels=c.leftLabels.slice(1);
    const icons=c.leftIcons.slice(1);
    if(!projectionModeOpen){
      labels.forEach(label=>{
        const target=menuLabelTarget(label);
        if(!target)return;
        const a=target.animate(menuContentFrames,options);
        a.startTime=globalPulseStart;
        hamburgerAnimations.push(a);
      });
      icons.forEach(icon=>{
        const target=menuIconTarget(icon);
        if(!target)return;
        const a=target.animate(menuContentFrames,options);
        a.startTime=globalPulseStart;
        hamburgerAnimations.push(a);
      });
    }
    hamburgerExpectedCount=projectionModeOpen?2:10;
    return true;
  }

  function enforceGlobalPulse(c=collect()){
    const projectionReady=enforceProjectionPulse(c);
    const hamburgerReady=enforceHamburgerPulse(c);
    return projectionReady&&hamburgerReady;
  }

  function ensurePulseObserver(){
    if(pulseObserver)return;
    pulseObserver=new MutationObserver(()=>{
      if(pulseEnforceScheduled)return;
      pulseEnforceScheduled=true;
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        pulseEnforceScheduled=false;
        enforceGlobalPulse();
      }));
    });
    pulseObserver.observe(root,{subtree:true,childList:true,attributes:true,attributeFilter:["class"]});
  }

  async function initializeProjectionPulse(){
    await new Promise(resolve=>setTimeout(resolve,450));
    await waitFor(()=>{const c=collect();return c.leftLabels[0]&&c.leftIcons[0]&&c.menuButton&&c.menuStack});
    enforceGlobalPulse();
    ensurePulseObserver();
    return true;
  }

  function ensureCoordinateUnderglow(frame){
    const shadow=frame?.getRootNode();
    const coordinateRoot=shadow?.querySelector?.(".gvco-root");
    if(!frame||!coordinateRoot)return null;
    let layer=coordinateRoot.querySelector(":scope > .gv-7ah-coordinate-underglow");
    if(!layer){
      layer=document.createElement("span");
      layer.className="gv-7ah-coordinate-underglow";
      layer.setAttribute("aria-hidden","true");
      coordinateRoot.insertBefore(layer,frame);
    }
    const s=layer.style;
    s.setProperty("position","absolute","important");
    s.setProperty("pointer-events","none","important");
    s.setProperty("z-index","0","important");
    s.setProperty("border-radius","50%","important");
    s.setProperty("background","radial-gradient(ellipse at center, rgba(224,252,255,.34) 0%, rgba(143,234,255,.28) 24%, rgba(98,216,255,.20) 44%, rgba(79,166,255,.12) 62%, rgba(157,124,255,.08) 76%, rgba(0,0,0,0) 100%)","important");
    s.setProperty("opacity","0");
    s.setProperty("box-shadow","none");
    frame.style.setProperty("z-index","1","important");
    return layer;
  }

  function syncCoordinateUnderglowGeometry(){
    const frame=coordinateFrameEl,layer=coordinateUnderglowEl;
    const shadow=frame?.getRootNode();
    const coordinateRoot=shadow?.querySelector?.(".gvco-root");
    if(!frame||!layer||!coordinateRoot)return null;
    const rootRect=coordinateRoot.getBoundingClientRect();
    const frameRect=frame.getBoundingClientRect();
    const padX=6,padY=5;
    layer.style.setProperty("left",`${(frameRect.left-rootRect.left-padX).toFixed(3)}px`,"important");
    layer.style.setProperty("top",`${(frameRect.top-rootRect.top-padY).toFixed(3)}px`,"important");
    layer.style.setProperty("width",`${(frameRect.width+2*padX).toFixed(3)}px`,"important");
    layer.style.setProperty("height",`${(frameRect.height+2*padY).toFixed(3)}px`,"important");
    return {rootRect,frameRect,layerRect:layer.getBoundingClientRect()};
  }

  async function startCoordinateGlow(){
    const frame=await waitFor(()=>root.querySelector(".gv-coordinate-module-host")?.shadowRoot?.querySelector(".gvco-frame"));
    coordinateFrameEl=frame;
    coordinateInitialFrame=(frame.textContent||"").trim().toUpperCase();
    frame.getAnimations().forEach(a=>{try{a.cancel()}catch(_){ }});
    coordinateUnderglowEl=ensureCoordinateUnderglow(frame);
    if(!coordinateUnderglowEl)throw new Error("GV-BETA-0007AH COORDINATE UNDERGLOW LAYER UNAVAILABLE");
    syncCoordinateUnderglowGeometry();
    const options={duration:CYCLE,iterations:Infinity,easing:EASING,fill:"both"};
    coordinateAnimation=frame.animate(coordinateFrames,options);
    coordinateUnderglowAnimation=coordinateUnderglowEl.animate(coordinateUnderglowFrames,options);
    coordinateAnimation.startTime=globalPulseStart;
    coordinateUnderglowAnimation.startTime=globalPulseStart;
    coordinateFrameObserver=new MutationObserver(()=>requestAnimationFrame(syncCoordinateUnderglowGeometry));
    coordinateFrameObserver.observe(frame,{childList:true,subtree:true});
    window.GV7AH_COORDINATE_GLOW={
      passed:coordinateInitialFrame==="ICRSD",
      initialFrame:coordinateInitialFrame,
      cycleMs:CYCLE,
      easing:EASING,
      startTime:globalPulseStart,
      textPlayState:coordinateAnimation.playState,
      underglowPlayState:coordinateUnderglowAnimation.playState
    };
    return frame;
  }

  const nextPaint=()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));

  async function validateCoordinateGlow(){
    const frame=await coordinateGlowPromise;
    if(!frame||!coordinateAnimation||!coordinateUnderglowEl||!coordinateUnderglowAnimation)return {passed:false,error:String(coordinateGlowError||"coordinate frame unavailable")};
    const host=root.querySelector(".gv-coordinate-module-host");
    const shadow=host?.shadowRoot;
    const coordinateRoot=shadow?.querySelector(".gvco-root");
    syncCoordinateUnderglowGeometry();
    const beforeFrame=(frame.textContent||"").trim().toUpperCase();
    const beforeRootRect=coordinateRoot?.getBoundingClientRect();
    const beforeFrameRect=frame.getBoundingClientRect();
    const beforeLayerRect=coordinateUnderglowEl.getBoundingClientRect();
    const beforeX=shadow?.querySelector(".gvco-x")?.textContent||"";
    const beforeY=shadow?.querySelector(".gvco-y")?.textContent||"";
    const textAnimationRef=coordinateAnimation;
    const underglowAnimationRef=coordinateUnderglowAnimation;
    const underglowNodeRef=coordinateUnderglowEl;
    const expectedFirst=beforeFrame==="GAL"?"ICRSD":"GAL";
    frame.click();
    await nextPaint();
    syncCoordinateUnderglowGeometry();
    const firstFrame=(frame.textContent||"").trim().toUpperCase();
    const firstFrameRect=frame.getBoundingClientRect();
    const firstLayerRect=coordinateUnderglowEl.getBoundingClientRect();
    const sameNodeAfterFirst=shadow?.querySelector(".gvco-frame")===frame;
    const sameTextAnimationAfterFirst=coordinateAnimation===textAnimationRef&&frame.getAnimations().includes(textAnimationRef)&&textAnimationRef.playState==="running";
    const sameUnderglowAfterFirst=coordinateUnderglowEl===underglowNodeRef&&coordinateUnderglowAnimation===underglowAnimationRef&&coordinateUnderglowEl.getAnimations().includes(underglowAnimationRef)&&underglowAnimationRef.playState==="running";
    frame.click();
    await nextPaint();
    syncCoordinateUnderglowGeometry();
    const restoredFrame=(frame.textContent||"").trim().toUpperCase();
    const afterRootRect=coordinateRoot?.getBoundingClientRect();
    const afterFrameRect=frame.getBoundingClientRect();
    const afterLayerRect=coordinateUnderglowEl.getBoundingClientRect();
    const afterX=shadow?.querySelector(".gvco-x")?.textContent||"";
    const afterY=shadow?.querySelector(".gvco-y")?.textContent||"";
    const textRunning=frame.getAnimations().filter(a=>a.playState==="running");
    const layerRunning=coordinateUnderglowEl.getAnimations().filter(a=>a.playState==="running");
    const textTiming=textAnimationRef.effect.getTiming();
    const underglowTiming=underglowAnimationRef.effect.getTiming();
    const phaseSpread=Math.abs(Number(textAnimationRef.currentTime)-Number(underglowAnimationRef.currentTime));
    const rootChildren=[...coordinateRoot.children];
    const frameIndex=rootChildren.indexOf(frame),layerIndex=rootChildren.indexOf(underglowNodeRef),dividerIndex=rootChildren.findIndex(el=>el.classList?.contains("gvco-divider"));
    const effectProperties=[...new Set(textAnimationRef.effect.getKeyframes().flatMap(k=>Object.keys(k))),...new Set(underglowAnimationRef.effect.getKeyframes().flatMap(k=>Object.keys(k)))];
    const geometryKeys=["transform","left","top","width","height","padding","margin"];
    const result={
      initialStartupFrame:coordinateInitialFrame,
      beforeFrame,firstFrame,restoredFrame,
      expectedFirst,
      sameNodeAfterFirst,
      sameTextAnimationAfterFirst,
      sameUnderglowAfterFirst,
      sameNodeAfterRestore:shadow?.querySelector(".gvco-frame")===frame,
      sameTextAnimationAfterRestore:coordinateAnimation===textAnimationRef&&frame.getAnimations().includes(textAnimationRef)&&textAnimationRef.playState==="running",
      sameUnderglowAfterRestore:coordinateUnderglowEl===underglowNodeRef&&coordinateUnderglowAnimation===underglowAnimationRef&&coordinateUnderglowEl.getAnimations().includes(underglowAnimationRef)&&underglowAnimationRef.playState==="running",
      exactlyOneRunningTextGlow:textRunning.length===1&&textRunning[0]===textAnimationRef,
      exactlyOneRunningUnderglow:layerRunning.length===1&&layerRunning[0]===underglowAnimationRef,
      textCycleMs:textTiming.duration,
      underglowCycleMs:underglowTiming.duration,
      textEasing:textTiming.easing,
      underglowEasing:underglowTiming.easing,
      textStartTime:textAnimationRef.startTime,
      underglowStartTime:underglowAnimationRef.startTime,
      sharedGlobalStart:textAnimationRef.startTime===globalPulseStart&&underglowAnimationRef.startTime===globalPulseStart,
      phaseSpreadMs:phaseSpread,
      rootGeometryStable:!!beforeRootRect&&!!afterRootRect&&sameNumber(beforeRootRect.width,afterRootRect.width)&&sameNumber(beforeRootRect.height,afterRootRect.height),
      frameGeometryRestored:sameNumber(beforeFrameRect.left,afterFrameRect.left)&&sameNumber(beforeFrameRect.top,afterFrameRect.top)&&sameNumber(beforeFrameRect.width,afterFrameRect.width)&&sameNumber(beforeFrameRect.height,afterFrameRect.height),
      coordinateTextRestored:beforeX===afterX&&beforeY===afterY,
      frameXChangedForGAL:Math.abs(firstFrameRect.left-beforeFrameRect.left)>1,
      underglowTracksFrameGAL:sameNumber((firstLayerRect.left+firstLayerRect.width/2),(firstFrameRect.left+firstFrameRect.width/2)),
      underglowRestored:sameNumber(beforeLayerRect.left,afterLayerRect.left)&&sameNumber(beforeLayerRect.top,afterLayerRect.top)&&sameNumber(beforeLayerRect.width,afterLayerRect.width)&&sameNumber(beforeLayerRect.height,afterLayerRect.height),
      underglowPointerSafe:getComputedStyle(coordinateUnderglowEl).pointerEvents==="none",
      underglowBehind:Number(getComputedStyle(coordinateUnderglowEl).zIndex||0)<Number(getComputedStyle(frame).zIndex||1),
      underglowBeforeDivider:layerIndex>=0&&dividerIndex>=0&&layerIndex<frameIndex&&layerIndex<dividerIndex,
      noGeometryAnimationKeys:geometryKeys.every(key=>!effectProperties.includes(key))
    };
    result.passed=
      result.initialStartupFrame==="ICRSD"&&
      result.firstFrame===expectedFirst&&
      result.restoredFrame===beforeFrame&&
      result.sameNodeAfterFirst&&result.sameTextAnimationAfterFirst&&result.sameUnderglowAfterFirst&&
      result.sameNodeAfterRestore&&result.sameTextAnimationAfterRestore&&result.sameUnderglowAfterRestore&&
      result.exactlyOneRunningTextGlow&&result.exactlyOneRunningUnderglow&&
      result.textCycleMs===CYCLE&&result.underglowCycleMs===CYCLE&&
      normalizeEasing(result.textEasing)===normalizeEasing(EASING)&&normalizeEasing(result.underglowEasing)===normalizeEasing(EASING)&&
      result.sharedGlobalStart&&result.phaseSpreadMs<=5&&
      result.rootGeometryStable&&result.frameGeometryRestored&&result.coordinateTextRestored&&
      result.frameXChangedForGAL&&result.underglowTracksFrameGAL&&result.underglowRestored&&
      result.underglowPointerSafe&&result.underglowBehind&&result.underglowBeforeDivider&&result.noGeometryAnimationKeys;
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
      expectedCount:18,
      sharedStart:projectionAnimations.length===18&&projectionAnimations.every(a=>a.startTime===globalPulseStart),
      allRunning:projectionAnimations.length===18&&projectionAnimations.every(a=>a.playState==="running"),
      durationMatch:timings.length===18&&timings.every(t=>t.duration===CYCLE),
      easingMatch:timings.length===18&&timings.every(t=>normalizeEasing(t.easing)===normalizeEasing(EASING)),
      phaseSpreadMs:phaseSpread,
      phaseMatch:phaseSpread<=5,
      foreignRunningCount:foreign.length,
      noForeignRunning:foreign.length===0,
      startTime:globalPulseStart,
      cycleMs:CYCLE,
      easing:EASING
    };
  }

  function hamburgerPulseDiagnostics(c){
    const timings=hamburgerAnimations.map(a=>a.effect.getTiming());
    const currentTimes=hamburgerAnimations.map(a=>Number(a.currentTime)).filter(Number.isFinite);
    const phaseSpread=currentTimes.length?Math.max(...currentTimes)-Math.min(...currentTimes):Infinity;
    const menuTargets=[...c.leftLabels.slice(1).map(menuLabelTarget),...c.leftIcons.slice(1).map(menuIconTarget)].filter(Boolean);
    const allFourLabelTargets=c.leftLabels.slice(1).every(label=>!!menuLabelTarget(label));
    const allFourIconTargets=c.leftIcons.slice(1).every(icon=>!!menuIconTarget(icon));
    const legacyCssAnimations=c.menuStack?.getAnimations().filter(a=>typeof CSSAnimation!=="undefined"&&a instanceof CSSAnimation&&a.animationName==="gv-menu-stack-pulse")||[];
    return {
      count:hamburgerAnimations.length,
      expectedCount:hamburgerExpectedCount,
      allFourLabelTargets,
      allFourIconTargets,
      menuContentTargetCount:menuTargets.length,
      sharedStart:hamburgerAnimations.length===hamburgerExpectedCount&&hamburgerAnimations.every(a=>a.startTime===globalPulseStart),
      allRunning:hamburgerAnimations.length===hamburgerExpectedCount&&hamburgerAnimations.every(a=>a.playState==="running"),
      durationMatch:timings.length===hamburgerExpectedCount&&timings.every(t=>t.duration===CYCLE),
      easingMatch:timings.length===hamburgerExpectedCount&&timings.every(t=>normalizeEasing(t.easing)===normalizeEasing(EASING)),
      phaseSpreadMs:phaseSpread,
      phaseMatch:phaseSpread<=5,
      inheritedCssSuppressed:legacyCssAnimations.length===0&&getComputedStyle(c.menuStack).animationName==="none",
      startTime:globalPulseStart,
      cycleMs:CYCLE,
      easing:EASING,
      projectionModeOpen:root.classList.contains("gv-7ad-projection-mode")
    };
  }

  function globalPulseDiagnostics(){
    const animations=[...projectionAnimations,...hamburgerAnimations,coordinateAnimation,coordinateUnderglowAnimation].filter(Boolean);
    const timings=animations.map(a=>a.effect.getTiming());
    const currentTimes=animations.map(a=>Number(a.currentTime)).filter(Number.isFinite);
    const phaseSpread=currentTimes.length?Math.max(...currentTimes)-Math.min(...currentTimes):Infinity;
    return {
      count:animations.length,
      sharedStart:animations.length>0&&animations.every(a=>a.startTime===globalPulseStart),
      durationMatch:timings.length===animations.length&&timings.every(t=>t.duration===CYCLE),
      easingMatch:timings.length===animations.length&&timings.every(t=>normalizeEasing(t.easing)===normalizeEasing(EASING)),
      allRunning:animations.length>0&&animations.every(a=>a.playState==="running"),
      phaseSpreadMs:phaseSpread,
      phaseMatch:phaseSpread<=5,
      startTime:globalPulseStart,
      cycleMs:CYCLE,
      easing:EASING
    };
  }

  async function finalizeAndValidate(baseline){
    const c=collect();
    const centering=centerProjectionIcons(c);
    await projectionPulseReady;
    enforceGlobalPulse(c);
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
      mollweideSvg:c.rightIcons[0].querySelector("svg")?.outerHTML||"",
      generatedIconHtml:c.rightIcons.slice(1).map(e=>e.innerHTML),
      menuButton:c.menuButton,
      menuStack:c.menuStack,
      menuButtonRect:rect(c.menuButton),
      menuStackRect:rect(c.menuStack)
    };

    c.rightLabels.forEach((label,index)=>ensureGlyph(label,LABELS[index]));
    populateProjectionIcons(c);
    patched=true;
    observer?.disconnect();
    finalizeAndValidate(baseline).catch(error=>console.error("GV-BETA-0007AH FINALIZATION FAILURE:",error));
    return true;
  }

  async function validate(baseline,centering){
    const c=collect();
    const labelNames=c.rightLabels.map(e=>(e?.textContent||"").trim().toUpperCase());
    const wrapperCounts=c.rightLabels.map(e=>e?.querySelectorAll("span.gv-space-age-glyph").length||0);
    const spans=c.rightLabels.map(e=>e?.querySelector(":scope > span.gv-space-age-glyph"));
    const fontSizes=c.rightLabels.map(e=>e?getComputedStyle(e).fontSize:"");
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
      if(!label||!span||label.children.length!==1||label.firstElementChild!==span)return false;
      return [...label.childNodes].every(node=>node.nodeType!==Node.TEXT_NODE||(node.nodeValue||"").trim()==="");
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
    const hamburger=hamburgerPulseDiagnostics(c);
    const coordinate=await validateCoordinateGlow();
    const globalPulse=globalPulseDiagnostics();
    const newCenterNames=["SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
    const newCentersPass=newCenterNames.every(name=>centering?.[name]&&Math.abs(centering[name].errorX)<CENTER_TOL&&Math.abs(centering[name].errorY)<CENTER_TOL);
    const checks={
      versionLabel:versionLabel.textContent==="V-7AH",
      exactlyFiveProjectionRows:c.rightRows.length===5,
      exactLabelOrder:JSON.stringify(labelNames)===JSON.stringify(LABELS),
      orthographicAbsent:!(c.rightMenu?.textContent||"").toUpperCase().includes("ORTHOGRAPHIC"),
      exactlyOneGlyphWrapper:wrapperCounts.length===5&&wrapperCounts.every(n=>n===1),
      noPlainTextOutsideGlyph:noPlainOutside,
      allGlyphTransformsScaleY15:transforms.length===5&&transforms.every(scaleY15),
      allButtonFontSizes12px:fontSizes.length===5&&fontSizes.every(v=>v==="12px"),
      allButtonsSpaceAge:fontFamilies.length===5&&fontFamilies.every(v=>v.toLowerCase().includes("space age")),
      allButtonsLetterSpacing055px:letterSpacing.length===5&&letterSpacing.every(v=>Math.abs(parseFloat(v)-.55)<.01),
      rightTypographyStylesPreserved:currentRightStyles.every((s,i)=>sameStyle(s,baseline.rightLabelStyles[i])),
      leftTypographyUntouched:c.leftLabels.every((e,i)=>e.innerHTML===baseline.leftLabelHtml[i]&&sameStyle(currentLeftStyles[i],baseline.leftLabelStyles[i])),
      longTileGeometryUnchanged:geometryUnchanged,
      squareTileDimensionsUnchanged:[...currentLeftIconRects,...currentRightIconRects].every((r,i)=>{const before=[...baseline.leftIconRects,...baseline.rightIconRects][i];return sameNumber(r.width,before.width)&&sameNumber(r.height,before.height)&&sameNumber(r.width,r.height)}),
      projectionModeDimmingFunctional:open?(inactiveDimmed&&inactiveNoPulse):dimRulePresent,
      projectionActiveStateRetained:!open||c.leftRows[0].classList.contains("gv-selected"),
      projectionGlowRunning:projectionAnimations.length>=2,
      mollweideGlowRunning:mollweideAnimations.length>=2,
      projectionSvgUnchanged:(projection?.querySelector("svg")?.outerHTML||"")===baseline.projectionSvg,
      mollweideSvgPresent:!!mollweide?.querySelector("svg"),
      mollweideSvgUnchanged:(mollweide?.querySelector("svg")?.outerHTML||"")===baseline.mollweideSvg,
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
      exactAuthorizedCycle:CYCLE===4480,
      hamburgerButtonNodePreserved:c.menuButton===baseline.menuButton,
      hamburgerStackNodePreserved:c.menuStack===baseline.menuStack,
      hamburgerGeometryUnchanged:sameRect(rect(c.menuButton),baseline.menuButtonRect)&&sameRect(rect(c.menuStack),baseline.menuStackRect),
      hamburgerAllFourLabelTargets:hamburger.allFourLabelTargets,
      hamburgerAllFourIconTargets:hamburger.allFourIconTargets,
      hamburgerPulseCount:hamburger.count===hamburger.expectedCount,
      hamburgerPulseSharedStart:hamburger.sharedStart,
      hamburgerPulseAllRunning:hamburger.allRunning,
      hamburgerPulseDuration:hamburger.durationMatch,
      hamburgerPulseEasing:hamburger.easingMatch,
      hamburgerPulsePhase:hamburger.phaseMatch,
      hamburgerLegacyCssSuppressed:hamburger.inheritedCssSuppressed,
      coordinateStartupICRSD:coordinate.initialStartupFrame==="ICRSD",
      coordinateGlowPersistent:coordinate.passed,
      coordinateNeonUnderglow:coordinate.exactlyOneRunningUnderglow&&coordinate.underglowPointerSafe&&coordinate.underglowBehind&&coordinate.underglowBeforeDivider,
      coordinateGlobalStart:coordinate.sharedGlobalStart,
      globalPulseSharedStart:globalPulse.sharedStart,
      globalPulseDuration:globalPulse.durationMatch,
      globalPulseEasing:globalPulse.easingMatch,
      globalPulseAllRunning:globalPulse.allRunning,
      globalPulsePhase:globalPulse.phaseMatch,
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
    window.GV7AH_VALIDATION={
      passed,
      pending:false,
      checks,
      failedChecks,
      labelNames,
      wrapperCounts,
      computedFontSizes:fontSizes,
      computedTransforms:transforms,
      fontFamilies,
      letterSpacing,
      iconPopulatedStates,
      iconGeometryChecks,
      newSvgRects,
      centering,
      centerTolerancePx:CENTER_TOL,
      authorizedCycleMs:CYCLE,
      globalPulse,
      projectionPulse:pulse,
      hamburgerPulse:hamburger,
      coordinateGlow:coordinate,
      projectionModeOpen:open,
      baseline:"GV-beta-0007AD.py@19f5a381314e1ebb336f7d25c4df9fdb54163301",
      fontSizeContract:"12px unchanged",
      glyphTransformContract:"scaleY(1.5)",
      splash:"not loaded",
      newProjectionActions:"not wired",
      populatedIcons:["SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"]
    };
    if(!passed)throw new Error("GV-BETA-0007AH CONTRACT FAILED "+JSON.stringify(window.GV7AH_VALIDATION));
    return true;
  }

  let coordinateGlowError=null;
  const coordinateGlowPromise=startCoordinateGlow().catch(error=>{coordinateGlowError=error;window.GV7AH_COORDINATE_GLOW={passed:false,error:String(error)};return null});
  const projectionPulseReady=initializeProjectionPulse().catch(error=>{console.error("GV-BETA-0007AH PROJECTION PULSE INITIALIZATION FAILURE:",error);return false});

  observer=new MutationObserver(()=>{if(patched)return;const c=collect();if(c.rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch))});
  observer.observe(root,{subtree:true,childList:true});
  if(collect().rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch));
})().catch(error=>console.error("GV-BETA-0007AH STARTUP FAILURE:",error));
"""))

# GV-beta-0007AH staged
