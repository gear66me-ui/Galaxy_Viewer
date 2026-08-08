from IPython.display import HTML, Javascript, display

# GV-beta-0007T
# Projection menu refinement based on verified 7S behavior.
# Authorized change: synchronize Projection tile glow and add one Mollweide preview row only.

display(HTML("""
<style>
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon{
  animation:gv-projection-tile-wake 2.6s ease-in-out infinite!important;
}
@keyframes gv-projection-tile-wake{
  0%,12%,100%{background:rgba(0,0,0,.86)!important;box-shadow:0 0 10px rgba(98,216,255,.28)!important}
  18%{background:radial-gradient(circle at 50% 48%,rgba(79,166,255,.25),rgba(26,20,58,.94) 72%)!important;box-shadow:0 0 5px rgba(240,237,255,.95),0 0 14px rgba(98,216,255,.92),inset 0 0 11px rgba(157,124,255,.30)!important}
  32%,88%{background:rgba(7,12,22,.90)!important;box-shadow:0 0 10px rgba(98,216,255,.42)!important}
}
#aladin-cosmic-command-test .gv-projection-submenu{
  width:184px!important;
}
#aladin-cosmic-command-test .gv-projection-submenu.gv-open{
  display:flex!important;flex-direction:column!important;gap:2px!important;
}
#aladin-cosmic-command-test .gv-projection-option-row{
  display:grid!important;grid-template-columns:146px 36px!important;column-gap:2px!important;
  width:184px!important;height:36px!important;
}
#aladin-cosmic-command-test .gv-projection-option-label,
#aladin-cosmic-command-test .gv-projection-option-icon{
  appearance:none!important;-webkit-appearance:none!important;position:relative!important;
  display:flex!important;align-items:center!important;height:36px!important;margin:0!important;
  box-sizing:border-box!important;border:1px solid #D7F4FF!important;border-radius:6px!important;
  background:rgba(0,0,0,.90)!important;color:#D7F3FF!important;
  box-shadow:0 0 10px rgba(98,216,255,.38)!important;cursor:pointer!important;pointer-events:auto!important;
}
#aladin-cosmic-command-test .gv-projection-option-label{
  width:146px!important;justify-content:flex-start!important;padding:0 10px!important;
  font:400 12px/1.15 "Space Age",sans-serif!important;letter-spacing:.55px!important;
  text-shadow:0 0 2px rgba(234,248,255,.58)!important;white-space:nowrap!important;
}
#aladin-cosmic-command-test .gv-projection-option-icon{
  width:36px!important;justify-content:center!important;padding:0!important;overflow:hidden!important;
}
#aladin-cosmic-command-test .gv-projection-option-icon svg{
  width:29px!important;height:29px!important;overflow:visible!important;pointer-events:none!important;
  animation:gv-mollweide-icon-wake 2.6s ease-in-out infinite!important;
}
#aladin-cosmic-command-test .gv-projection-option-icon .gv-mol-outline,
#aladin-cosmic-command-test .gv-projection-option-icon .gv-mol-grid{
  fill:none!important;stroke-linecap:round!important;stroke-linejoin:round!important;
}
#aladin-cosmic-command-test .gv-projection-option-icon .gv-mol-outline{stroke:#8FEAFF!important;stroke-width:1.8!important}
#aladin-cosmic-command-test .gv-projection-option-icon .gv-mol-grid{stroke:#9D7CFF!important;stroke-width:1.15!important;opacity:.96!important}
#aladin-cosmic-command-test .gv-projection-option-row.gv-active .gv-projection-option-icon{
  animation:gv-mollweide-tile-wake 2.6s ease-in-out infinite!important;
}
#aladin-cosmic-command-test .gv-projection-option-row.gv-active .gv-projection-option-label{
  box-shadow:0 0 5px rgba(240,237,255,.70),0 0 11px rgba(98,216,255,.62),inset 0 0 7px rgba(215,243,255,.14)!important;
}
@keyframes gv-mollweide-tile-wake{
  0%,12%,100%{background:rgba(0,0,0,.90)!important;box-shadow:0 0 9px rgba(98,216,255,.25)!important}
  18%{background:radial-gradient(ellipse at center,rgba(79,166,255,.26),rgba(28,20,64,.96) 72%)!important;box-shadow:0 0 5px rgba(255,255,255,.92),0 0 14px rgba(98,216,255,.92),inset 0 0 10px rgba(157,124,255,.30)!important}
  32%,88%{background:rgba(7,12,22,.92)!important;box-shadow:0 0 10px rgba(98,216,255,.42)!important}
}
@keyframes gv-mollweide-icon-wake{
  0%,12%,100%{opacity:.62;filter:drop-shadow(0 0 1px rgba(143,234,255,.22))}
  18%{opacity:1;filter:drop-shadow(0 0 4px rgba(143,234,255,.98)) drop-shadow(0 0 9px rgba(79,166,255,.80)) drop-shadow(0 0 13px rgba(157,124,255,.50))}
  32%,88%{opacity:.76;filter:drop-shadow(0 0 2px rgba(143,234,255,.40))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007S.py?v=4dd69daf46f2c73113f7323dc5e720bd9f51eaa5";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007T STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007S RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007T COULD NOT EXTRACT 7S BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const aladin=await waitFor(()=>window.aladin_cosmic_command_test);
  const menuButton=await waitFor(()=>root.querySelector("button.gv-menu-proxy"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7T";

  const mollweideSvg=`<svg viewBox="0 0 64 64" aria-hidden="true"><ellipse class="gv-mol-outline" cx="32" cy="32" rx="25" ry="15"/><ellipse class="gv-mol-grid" cx="32" cy="32" rx="12" ry="15"/><path class="gv-mol-grid" d="M7 32h50M10 25c13 5 31 5 44 0M10 39c13-5 31-5 44 0M18 19c5 7 5 19 0 26M46 19c-5 7-5 19 0 26"/></svg>`;

  function rebuildMollweide(){
    const panel=root.querySelector(".gv-projection-submenu");if(!panel)return false;
    if(panel.dataset.gv7tBuilt==="true")return true;
    panel.dataset.gv7tBuilt="true";panel.replaceChildren();
    const row=document.createElement("div");row.className="gv-projection-option-row gv-active";row.setAttribute("role","none");
    const label=document.createElement("button");label.type="button";label.className="gv-projection-option-label";label.textContent="MOLLWEIDE";label.setAttribute("role","menuitemradio");label.setAttribute("aria-checked","true");
    const icon=document.createElement("button");icon.type="button";icon.className="gv-projection-option-icon";icon.innerHTML=mollweideSvg;icon.setAttribute("role","menuitemradio");icon.setAttribute("aria-label","MOLLWEIDE PROJECTION");icon.setAttribute("aria-checked","true");
    const choose=event=>{event.preventDefault();event.stopPropagation();try{if(typeof aladin.setProjection==="function")aladin.setProjection("MOL")}catch(error){console.warn("GV-BETA-0007T MOLLWEIDE WARNING",error)}};
    label.addEventListener("click",choose);icon.addEventListener("click",choose);row.append(label,icon);panel.appendChild(row);return true
  }

  menuButton.addEventListener("click",()=>setTimeout(()=>{const viewerMenu=root.querySelector(".gv-viewer-menu");if(viewerMenu?.classList.contains("gv-open")){const projectionRow=viewerMenu.querySelector(".gv-viewer-menu-row");const projectionIcon=projectionRow?.querySelector(".gv-viewer-menu-icon.gv-projection-icon");if(projectionIcon)projectionIcon.style.animationDelay="0ms"}},20));

  root.addEventListener("click",event=>{
    if(event.target.closest(".gv-viewer-menu-row:first-child"))setTimeout(()=>rebuildMollweide(),20)
  },true);
})().catch(error=>console.error("GV-BETA-0007T STARTUP FAILURE:",error));
"""))

# GV-beta-0007T staged
