from IPython.display import HTML, Javascript, display

# GV-beta-0007S
# Projection activation inspection release based on verified 7R behavior.
# Authorized change: install approved Projection icon 0002 and activate Projection submenu shell only.

display(HTML("""
<style>
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon{overflow:hidden!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg{display:block!important;width:31px!important;height:31px!important;overflow:visible!important;filter:drop-shadow(0 0 2px rgba(143,234,255,.30))!important;animation:gv-projection-wake 2.6s ease-in-out infinite!important;pointer-events:none!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon .gv-proj-sphere,
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon .gv-proj-grid,
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon .gv-proj-bridge{fill:none!important;stroke-linecap:round!important;stroke-linejoin:round!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon .gv-proj-sphere{stroke:#8FEAFF!important;stroke-width:1.55!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon .gv-proj-grid{stroke:#9D7CFF!important;stroke-width:1.45!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon .gv-proj-bridge{stroke:#4FA6FF!important;stroke-width:1.3!important;opacity:.9!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon .gv-proj-node{fill:#4FA6FF!important}
@keyframes gv-projection-wake{0%,12%,100%{opacity:.58;filter:drop-shadow(0 0 1px rgba(143,234,255,.20))}18%{opacity:1;filter:drop-shadow(0 0 4px rgba(143,234,255,.95)) drop-shadow(0 0 10px rgba(79,166,255,.72)) drop-shadow(0 0 14px rgba(157,124,255,.38))}32%,88%{opacity:.72;filter:drop-shadow(0 0 2px rgba(143,234,255,.38))}}
#aladin-cosmic-command-test .gv-projection-submenu{position:absolute!important;left:198px!important;top:50px!important;z-index:7116!important;display:none!important;visibility:hidden!important;opacity:0!important;width:146px!important;margin:0!important;padding:0!important;box-sizing:border-box!important;pointer-events:none!important}
#aladin-cosmic-command-test .gv-projection-submenu.gv-open{display:flex!important;visibility:visible!important;opacity:1!important;flex-direction:column!important;gap:2px!important;pointer-events:auto!important}
#aladin-cosmic-command-test .gv-projection-submenu button{appearance:none!important;-webkit-appearance:none!important;display:flex!important;visibility:visible!important;opacity:1!important;align-items:center!important;justify-content:flex-start!important;width:146px!important;height:36px!important;margin:0!important;padding:0 10px!important;box-sizing:border-box!important;border:1px solid #D7F4FF!important;border-radius:6px!important;background:rgba(0,0,0,.90)!important;color:#D7F3FF!important;box-shadow:0 0 10px rgba(98,216,255,.38)!important;font:400 11px/1.15 "Space Age",sans-serif!important;letter-spacing:.45px!important;cursor:pointer!important;pointer-events:auto!important}
#aladin-cosmic-command-test .gv-projection-submenu button.gv-active{background:rgba(35,31,70,.96)!important;box-shadow:0 0 5px rgba(240,237,255,.96),0 0 13px rgba(98,216,255,.90),inset 0 0 8px rgba(215,243,255,.24)!important}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007R.py?v=e716e6c1a680fb31c95680a391a5db98e71e3f3f";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007S STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});

  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007R RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007S COULD NOT EXTRACT 7R BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const aladin=await waitFor(()=>window.aladin_cosmic_command_test);
  const menuButton=await waitFor(()=>root.querySelector("button.gv-menu-proxy"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7S";

  const projectionSvg=`<svg viewBox="0 0 64 64" aria-hidden="true"><g><circle class="gv-proj-sphere" cx="23" cy="31" r="14.5"/><ellipse class="gv-proj-sphere" cx="23" cy="31" rx="6" ry="14.5"/><ellipse class="gv-proj-sphere" cx="23" cy="31" rx="14.5" ry="6"/><path class="gv-proj-sphere" d="M10.5 24.5c7.7 3.9 17.3 3.9 25 0M10.5 37.5c7.7-3.9 17.3-3.9 25 0"/><path class="gv-proj-bridge" d="M35.5 23.5L43 18M37.5 31L47 31M35.5 38.5L43 44"/><path class="gv-proj-grid" d="M43 18L57 22L57 40L43 44Z"/><path class="gv-proj-grid" d="M47.7 19.35V42.65M52.4 20.7V41.3M43 24.5L57 27M43 31L57 31M43 37.5L57 35"/><circle class="gv-proj-node" cx="47" cy="31" r="1.5"/></g></svg>`;

  function getProjectionSubmenu(){
    let panel=root.querySelector(".gv-projection-submenu");
    if(panel)return panel;
    panel=document.createElement("div");panel.className="gv-projection-submenu";panel.setAttribute("role","menu");panel.setAttribute("aria-label","PROJECTION OPTIONS");
    const mol=document.createElement("button");mol.type="button";mol.className="gv-active";mol.textContent="MOLLWEIDE";mol.setAttribute("role","menuitemradio");mol.setAttribute("aria-checked","true");
    mol.addEventListener("click",event=>{event.preventDefault();event.stopPropagation();try{if(typeof aladin.setProjection==="function")aladin.setProjection("MOL")}catch(error){console.warn("GV-BETA-0007S PROJECTION WARNING",error)}});
    panel.appendChild(mol);root.appendChild(panel);return panel
  }

  function decorateProjection(){
    const panel=root.querySelector(".gv-viewer-menu");if(!panel)return false;
    const row=panel.querySelector(".gv-viewer-menu-row");if(!row||row.dataset.gvProjectionActivated==="true")return !!row;
    row.dataset.gvProjectionActivated="true";
    const label=row.querySelector(".gv-viewer-menu-label");
    const icon=row.querySelector(".gv-viewer-menu-icon");
    if(!label||!icon)return false;
    icon.classList.add("gv-projection-icon");icon.innerHTML=projectionSvg;icon.setAttribute("aria-label","PROJECTION");
    const toggle=event=>{event.preventDefault();event.stopPropagation();const submenu=getProjectionSubmenu();const open=!submenu.classList.contains("gv-open");submenu.classList.toggle("gv-open",open);row.classList.toggle("gv-selected",open);label.setAttribute("aria-expanded",open?"true":"false");icon.setAttribute("aria-expanded",open?"true":"false")};
    label.setAttribute("aria-haspopup","menu");icon.setAttribute("aria-haspopup","menu");
    label.addEventListener("click",toggle);icon.addEventListener("click",toggle);
    return true
  }

  menuButton.addEventListener("click",()=>setTimeout(()=>{const viewerMenu=root.querySelector(".gv-viewer-menu");if(viewerMenu?.classList.contains("gv-open")){decorateProjection()}else{root.querySelector(".gv-projection-submenu")?.classList.remove("gv-open")}},0));
})().catch(error=>console.error("GV-BETA-0007S STARTUP FAILURE:",error));
"""))

# GV-beta-0007S staged
