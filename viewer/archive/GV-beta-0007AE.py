from IPython.display import HTML, Javascript, display

# GV-beta-0007AE
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AE
# PURPOSE: Restore the inherited Space Age glyph wrapper on all five Projection submenu labels and shorten ORTHOGRAPHIC to ORTHO.
# USER REQUEST: Preserve GV-beta-0007AD exactly except the approved right-side label contents, V-7AE version label, and runtime validation.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AE.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: 7AD geometry, icons, glow, dimming, coordinates, hamburger, target/SIMBAD, Aladin, navigation, controls, splash absence, fonts, colors, and all unrelated behavior.

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/19f5a381314e1ebb336f7d25c4df9fdb54163301/viewer/GV-beta-0007AD.py";
  const LABELS=["MOLLWEIDE","SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"];
  const TOL=.50;
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AE STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AD RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AE COULD NOT EXTRACT 7AD BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AE";
  window.GV7AE_VALIDATION={passed:false,pending:true,status:"AWAITING PROJECTION SUBMENU"};

  const rect=e=>{const r=e.getBoundingClientRect();return {left:r.left,top:r.top,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
  const style=e=>{const s=getComputedStyle(e);return {fontSize:s.fontSize,fontFamily:s.fontFamily,fontWeight:s.fontWeight,lineHeight:s.lineHeight,letterSpacing:s.letterSpacing,color:s.color,textShadow:s.textShadow}};
  const sameNumber=(a,b)=>Math.abs(a-b)<=TOL;
  const sameRect=(a,b)=>["left","top","width","height","right","bottom"].every(k=>sameNumber(a[k],b[k]));
  const sameStyle=(a,b)=>Object.keys(a).every(k=>a[k]===b[k]);
  const scaleY15=value=>{if(!value||value==="none")return false;try{const m=new DOMMatrixReadOnly(value);return Math.abs(m.a-1)<.01&&Math.abs(m.b)<.01&&Math.abs(m.c)<.01&&Math.abs(m.d-1.5)<.01}catch(_){return false}};

  let observer=null;
  let patched=false;

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
      mollweideSvg:c.rightIcons[0].querySelector("svg")?.outerHTML||""
    };

    c.rightLabels.forEach((label,index)=>ensureGlyph(label,LABELS[index]));
    patched=true;
    observer?.disconnect();
    requestAnimationFrame(()=>requestAnimationFrame(()=>validate(baseline)));
    return true;
  }

  function validate(baseline){
    const c=collect();
    const labelNames=c.rightLabels.map(e=>(e?.textContent||"").trim().toUpperCase());
    const wrapperCounts=c.rightLabels.map(e=>e?.querySelectorAll("span.gv-space-age-glyph").length||0);
    const spans=c.rightLabels.map(e=>e?.querySelector(":scope > span.gv-space-age-glyph"));
    const fontSizes=c.rightLabels.map(e=>e?getComputedStyle(e).fontSize:"");
    const transforms=spans.map(e=>e?getComputedStyle(e).transform:"");
    const fontFamilies=c.rightLabels.map(e=>e?getComputedStyle(e).fontFamily:"");
    const letterSpacing=c.rightLabels.map(e=>e?getComputedStyle(e).letterSpacing:"");
    const iconEmptyStates=c.rightIcons.map((e,i)=>i===0?false:!!e&&e.innerHTML.trim()==="");
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
    const checks={
      versionLabel:versionLabel.textContent==="V-7AE",
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
      mollweideSvgPresent:!!mollweide?.querySelector("svg"),
      mollweideSvgUnchanged:(mollweide?.querySelector("svg")?.outerHTML||"")===baseline.mollweideSvg,
      fourGeneratedIconTilesEmpty:iconEmptyStates.slice(1).every(Boolean),
      labelButtonElementsPreserved:c.rightLabels.every((e,i)=>e===baseline.labelButtons[i]),
      iconButtonElementsPreserved:c.rightIcons.every((e,i)=>e===baseline.iconButtons[i]),
      rowElementsPreserved:c.rightRows.every((e,i)=>e===baseline.rowNodes[i]),
      noNewProjectionActions:noInlineNewActions,
      splashUnloaded:!document.querySelector('[src*="Singularity"],[href*="Singularity"]'),
      noDuplicateProjectionLabels:new Set(labelNames).size===5
    };
    const failedChecks=Object.entries(checks).filter(([,value])=>!value).map(([name])=>name);
    const passed=failedChecks.length===0;
    window.GV7AE_VALIDATION={
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
      iconEmptyStates,
      projectionModeOpen:open,
      baseline:"GV-beta-0007AD.py@19f5a381314e1ebb336f7d25c4df9fdb54163301",
      fontSizeContract:"12px unchanged",
      glyphTransformContract:"scaleY(1.5)",
      splash:"not loaded",
      newProjectionActions:"not wired"
    };
    if(!passed)throw new Error("GV-BETA-0007AE CONTRACT FAILED "+JSON.stringify(window.GV7AE_VALIDATION));
    return true;
  }

  observer=new MutationObserver(()=>{if(patched)return;const c=collect();if(c.rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch))});
  observer.observe(root,{subtree:true,childList:true});
  if(collect().rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch));
})().catch(error=>console.error("GV-BETA-0007AE STARTUP FAILURE:",error));
"""))

# GV-beta-0007AE staged
