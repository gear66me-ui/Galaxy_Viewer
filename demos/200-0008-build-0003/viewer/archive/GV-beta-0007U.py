from IPython.display import HTML, Javascript, display

# GV-beta-0007U
# Mollweide UI refinement based on verified 7T behavior.
# Authorized change: square Mollweide tile, symmetric Mollweide preview geometry,
# Projection-sized Mollweide text, and synchronized Projection/Mollweide neon pulse.

display(HTML("""
<style>
#aladin-cosmic-command-test .gv-projection-submenu{width:158px!important}
#aladin-cosmic-command-test .gv-projection-option-row{grid-template-columns:120px 36px!important;width:158px!important;height:36px!important;column-gap:2px!important}
#aladin-cosmic-command-test .gv-projection-option-label{width:120px!important;min-width:120px!important;max-width:120px!important;font:400 12px/1.15 "Space Age",sans-serif!important;letter-spacing:.55px!important;padding:0 8px!important;overflow:hidden!important}
#aladin-cosmic-command-test .gv-projection-option-label .gv-space-age-glyph{display:inline-block!important;transform:scaleY(1.5)!important;transform-origin:center!important}
#aladin-cosmic-command-test .gv-projection-option-icon{width:36px!important;min-width:36px!important;max-width:36px!important;height:36px!important;min-height:36px!important;max-height:36px!important;aspect-ratio:1/1!important;padding:0!important;overflow:hidden!important}
#aladin-cosmic-command-test .gv-projection-option-icon svg{width:30px!important;height:30px!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon,
#aladin-cosmic-command-test .gv-projection-option-row.gv-active .gv-projection-option-icon{animation:gv-shared-projection-tile-pulse 2.6s ease-in-out infinite!important}
#aladin-cosmic-command-test .gv-viewer-menu-icon.gv-projection-icon svg,
#aladin-cosmic-command-test .gv-projection-option-icon svg{animation:gv-shared-projection-icon-pulse 2.6s ease-in-out infinite!important}
@keyframes gv-shared-projection-tile-pulse{
  0%,12%,100%{background:rgba(0,0,0,.88)!important;box-shadow:0 0 8px rgba(98,216,255,.24)!important}
  18%{background:radial-gradient(circle at 50% 50%,rgba(73,153,255,.28),rgba(20,17,49,.96) 74%)!important;box-shadow:0 0 5px rgba(255,255,255,.95),0 0 14px rgba(98,216,255,.95),inset 0 0 10px rgba(157,124,255,.34)!important}
  32%,88%{background:rgba(7,12,22,.92)!important;box-shadow:0 0 10px rgba(98,216,255,.42)!important}
}
@keyframes gv-shared-projection-icon-pulse{
  0%,12%,100%{opacity:.62;filter:drop-shadow(0 0 1px rgba(143,234,255,.22))}
  18%{opacity:1;filter:drop-shadow(0 0 4px rgba(143,234,255,1)) drop-shadow(0 0 9px rgba(79,166,255,.84)) drop-shadow(0 0 13px rgba(157,124,255,.50))}
  32%,88%{opacity:.77;filter:drop-shadow(0 0 2px rgba(143,234,255,.42))}
}
</style>
"""))

display(Javascript(r"""
(async()=>{
  const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007T.py?v=b32b7b6d253b12c44263f669d5cd498e615baa65";
  const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const end=performance.now()+timeout;const tick=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>end){reject(new Error("GV-BETA-0007U STARTUP TIMEOUT"));return}setTimeout(tick,50)};tick()});
  const response=await fetch(BASE_URL,{cache:"no-store"});
  if(!response.ok)throw new Error("GV-BETA-0007T RETURNED HTTP "+response.status);
  const source=await response.text();
  const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
  const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
  if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007U COULD NOT EXTRACT 7T BASELINE");
  htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
  jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});
  const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
  const versionLabel=await waitFor(()=>root.querySelector("#gv-version-label"));
  versionLabel.textContent="V-7U";
  const symmetricMol=`<svg viewBox="0 0 64 64" aria-hidden="true"><ellipse class="gv-mol-outline" cx="32" cy="32" rx="25" ry="15"/><path class="gv-mol-grid" d="M7 32H57"/><path class="gv-mol-grid" d="M10 25C20 28 44 28 54 25M10 39C20 36 44 36 54 39"/><path class="gv-mol-grid" d="M32 17V47"/><path class="gv-mol-grid" d="M32 17C24 21 24 43 32 47M32 17C40 21 40 43 32 47"/></svg>`;
  const refresh=()=>{
    const row=root.querySelector(".gv-projection-option-row");if(!row)return false;
    const label=row.querySelector(".gv-projection-option-label"),icon=row.querySelector(".gv-projection-option-icon");if(!label||!icon)return false;
    if(label.dataset.gv7u!=="true"){label.dataset.gv7u="true";label.innerHTML='<span class="gv-space-age-glyph">MOLLWEIDE</span>'}
    if(icon.dataset.gv7u!=="true"){icon.dataset.gv7u="true";icon.innerHTML=symmetricMol}
    const projectionIcon=root.querySelector(".gv-viewer-menu-icon.gv-projection-icon");
    if(projectionIcon){projectionIcon.style.animationDelay="0ms";projectionIcon.querySelector("svg")?.style.setProperty("animation-delay","0ms","important")}
    icon.style.animationDelay="0ms";icon.querySelector("svg")?.style.setProperty("animation-delay","0ms","important");
    return true
  };
  const observer=new MutationObserver(()=>refresh());observer.observe(root,{subtree:true,childList:true});refresh();
})().catch(error=>console.error("GV-BETA-0007U STARTUP FAILURE:",error));
"""))

# GV-beta-0007U staged
