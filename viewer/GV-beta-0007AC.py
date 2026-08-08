from IPython.display import HTML, Javascript, display

# GV-beta-0007AC
# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AC
# PURPOSE: Expand only the Projection submenu from one Mollweide row to five labeled projection rows while preserving 7AB behavior.
# USER REQUEST:
# 1. Keep MOLLWEIDE first, then add SPHERICAL, ORTHOGRAPHIC, TANGENTIAL, SINUSOIDAL.
# 2. Each projection row must contain one long text tile and one matching square icon tile immediately to its right.
# 3. Preserve the approved Mollweide row, 0003 SVG, 24x24 size, measured centering, and synchronized 7AB glow exactly.
# 4. Leave the four new square icon tiles intentionally empty; do not add placeholder icons and do not wire the new projections to Aladin yet.
# 5. Preserve the main Projection row/icon/glow, coordinate strip, hamburger, target/SIMBAD, Aladin, galaxy navigation, bottom controls, fonts, colors, and all unrelated behavior.
# 6. Splash animation remains absent from this release.
# AUTHORIZED CHANGES: Create viewer/GV-beta-0007AC.py and its dedicated launcher/ECO record only.
# PRESERVED BEHAVIOR: GV-beta-0007AB baseline except the authorized Projection submenu expansion and V-7AC version label.

display(HTML("""
<style>
#aladin-cosmic-command-test .gv-projection-submenu{
  display:flex!important;
  flex-direction:column!important;
  gap:2px!important;
  width:158px!important;
  height:auto!important;
}
#aladin-cosmic-command-test .gv-projection-submenu > .gv-projection-option-row{
  flex:0 0 36px!important;
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007AB.py?v=68d892fde62240d284a71263a2ab796d7e71f758";
  const LABELS=["MOLLWEIDE","SPHERICAL","ORTHOGRAPHIC","TANGENTIAL","SINUSOIDAL"];
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007AC STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007AB RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007AC COULD NOT EXTRACT 7AB BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7AC";

  function stripCloneIdentity(node){
    [node,...node.querySelectorAll("*")].forEach(el=>{
      el.removeAttribute("id");
      [...el.attributes].forEach(attr=>{
        if(attr.name.startsWith("on")||attr.name.startsWith("data-"))el.removeAttribute(attr.name);
      });
    });
  }

  function buildRows(){
    const submenu=root.querySelector(".gv-projection-submenu");
    const firstRow=submenu?.querySelector(":scope > .gv-projection-option-row");
    if(!submenu||!firstRow)return false;

    [...submenu.querySelectorAll(":scope > .gv-projection-option-row.gv-7ac-generated")].forEach(row=>row.remove());
    firstRow.dataset.gv7acProjection="MOLLWEIDE";

    LABELS.slice(1).forEach(name=>{
      const row=firstRow.cloneNode(true);
      stripCloneIdentity(row);
      row.classList.add("gv-7ac-generated");
      row.dataset.gv7acProjection=name;
      const label=row.querySelector(".gv-projection-option-label");
      const icon=row.querySelector(".gv-projection-option-icon");
      if(!label||!icon)throw new Error("GV-BETA-0007AC ROW TEMPLATE INCOMPLETE");
      label.textContent=name;
      label.type="button";
      icon.innerHTML="";
      icon.type="button";
      icon.setAttribute("aria-label",name+" icon placeholder");
      submenu.appendChild(row);
    });
    return true;
  }

  function validate(){
    const submenu=root.querySelector(".gv-projection-submenu");
    const rows=[...submenu?.querySelectorAll(":scope > .gv-projection-option-row")||[]];
    if(rows.length!==5)return false;
    const labels=rows.map(row=>row.querySelector(".gv-projection-option-label"));
    const icons=rows.map(row=>row.querySelector(".gv-projection-option-icon"));
    const labelNames=labels.map(el=>(el?.textContent||"").trim().toUpperCase());
    const firstSvg=icons[0]?.querySelector("svg");
    const newIconsEmpty=icons.slice(1).every(icon=>icon&&icon.innerHTML.trim()==="");
    const labelRects=labels.map(el=>el.getBoundingClientRect());
    const iconRects=icons.map(el=>el.getBoundingClientRect());
    const rowRects=rows.map(el=>el.getBoundingClientRect());
    const sameLabelSize=labelRects.every(r=>Math.abs(r.width-labelRects[0].width)<0.6&&Math.abs(r.height-labelRects[0].height)<0.6);
    const sameIconSize=iconRects.every(r=>Math.abs(r.width-iconRects[0].width)<0.6&&Math.abs(r.height-iconRects[0].height)<0.6);
    const rowGaps=rowRects.slice(1).map((r,i)=>r.top-rowRects[i].bottom);
    const sameRowGap=rowGaps.every(g=>Math.abs(g-rowGaps[0])<0.6)&&Math.abs(rowGaps[0]-2)<0.6;
    const projection=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    const projectionAnimations=projection?.getAnimations({subtree:true})||[];
    const mollweideAnimations=icons[0]?.getAnimations({subtree:true})||[];
    const checks={
      exactlyFiveRows:rows.length===5,
      labelOrder:JSON.stringify(labelNames)===JSON.stringify(LABELS),
      exactlyFiveLabels:labels.every(Boolean)&&labels.length===5,
      exactlyFiveIcons:icons.every(Boolean)&&icons.length===5,
      mollweideRetainsSvg:!!firstSvg,
      fourNewIconsEmpty:newIconsEmpty,
      matchingLabelDimensions:sameLabelSize,
      matchingSquareDimensions:sameIconSize&&iconRects.every(r=>Math.abs(r.width-r.height)<0.6),
      matchingTwoPixelRowGaps:sameRowGap,
      mollweideGlowActive:mollweideAnimations.filter(a=>a.playState==="running").length>=2,
      projectionGlowActive:projectionAnimations.filter(a=>a.playState==="running").length>=2,
      noDuplicateRows:new Set(labelNames).size===5,
      versionLabel:versionLabel.textContent==="V-7AC"
    };
    const passed=Object.values(checks).every(Boolean);
    window.GV7AC_VALIDATION={passed,checks,labels:labelNames,rowGaps:rowGaps.map(v=>Number(v.toFixed(2))),splash:"not loaded by 7AC",newProjectionActions:"not wired"};
    if(!passed)throw new Error("GV-BETA-0007AC CONTRACT FAILED "+JSON.stringify(window.GV7AC_VALIDATION));
    return true;
  }

  function apply(){
    if(!buildRows())return false;
    requestAnimationFrame(()=>requestAnimationFrame(validate));
    return true;
  }

  const observer=new MutationObserver(()=>{
    const submenu=root.querySelector(".gv-projection-submenu");
    if(submenu&&submenu.querySelector(".gv-projection-option-row")&&!submenu.querySelector(".gv-7ac-generated"))requestAnimationFrame(apply);
  });
  observer.observe(root,{subtree:true,childList:true});
  apply();
})().catch(error=>console.error("GV-BETA-0007AC STARTUP FAILURE:",error));
"""))

# GV-beta-0007AC staged
