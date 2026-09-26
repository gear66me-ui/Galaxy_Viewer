from IPython.display import HTML, Javascript, display

# GV-beta-0007AF
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AF
# PURPOSE: Populate only the four previously empty Projection submenu icon tiles with the approved Galaxy Viewer SVG artwork.
# USER REQUEST: Preserve GV-beta-0007AE behavior exactly except V-7AF identity, four approved icon insertions, and corresponding runtime validation.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AF.py and its dedicated launcher only.
# PRESERVED BEHAVIOR: 7AE geometry, Projection/Mollweide artwork and glow, labels, typography, dimming, coordinates, hamburger, target/SIMBAD, Aladin, navigation, controls, splash absence, fonts, colors, actions, and all unrelated behavior.

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
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AF STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AD RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AF COULD NOT EXTRACT 7AD BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AF";
  window.GV7AF_VALIDATION={passed:false,pending:true,status:"AWAITING PROJECTION SUBMENU"};

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

  function populateProjectionIcons(c){
    c.rightIcons.slice(1).forEach((icon,index)=>{icon.innerHTML=PROJECTION_ICONS[index]});
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
      generatedIconHtml:c.rightIcons.slice(1).map(e=>e.innerHTML)
    };

    c.rightLabels.forEach((label,index)=>ensureGlyph(label,LABELS[index]));
    populateProjectionIcons(c);
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
    const checks={
      versionLabel:versionLabel.textContent==="V-7AF",
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
    window.GV7AF_VALIDATION={
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
      projectionModeOpen:open,
      baseline:"GV-beta-0007AD.py@19f5a381314e1ebb336f7d25c4df9fdb54163301",
      fontSizeContract:"12px unchanged",
      glyphTransformContract:"scaleY(1.5)",
      splash:"not loaded",
      newProjectionActions:"not wired",
      populatedIcons:["SPHERICAL","ORTHO","TANGENTIAL","SINUSOIDAL"]
    };
    if(!passed)throw new Error("GV-BETA-0007AF CONTRACT FAILED "+JSON.stringify(window.GV7AF_VALIDATION));
    return true;
  }

  observer=new MutationObserver(()=>{if(patched)return;const c=collect();if(c.rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch))});
  observer.observe(root,{subtree:true,childList:true});
  if(collect().rightRows.length===5)requestAnimationFrame(()=>requestAnimationFrame(prepareAndPatch));
})().catch(error=>console.error("GV-BETA-0007AF STARTUP FAILURE:",error));
"""))

# GV-beta-0007AF staged
