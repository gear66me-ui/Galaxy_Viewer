from IPython.display import HTML, Javascript, display

# GV-beta-0004N
# Standalone Galaxy Viewer release based on the known-good GV-beta-0004A state.
# Preserves the GV-beta-0004A visuals and behavior while separating notebook HTML
# from executable JavaScript and loading the official Aladin Lite 3.8.2 browser bundle.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
#aladin-cosmic-command-test{
    width:100%;height:100vh;height:100dvh;position:relative!important;
    --text-blue:#62D8FF;--copy-blue:#7DF4FF;--layers-blue:#4F9DFF;
    --world-blue:#8B7CFF;--projection-blue:#6FC7FF;--fullscreen-blue:#BCEEFF;
    --zoom-plus:#55FF88;--zoom-minus:#FF5E78;
    --gv-active-blue:#45E7FF;
}
#aladin-cosmic-command-test .gv-standard-text,
#aladin-cosmic-command-test .gv-standard-text *{
    color:var(--text-blue)!important;fill:var(--text-blue)!important;
    text-shadow:0 0 5px rgba(98,216,255,.55)!important;
}
#aladin-cosmic-command-test .gv-copy{--command-color:var(--copy-blue)}
#aladin-cosmic-command-test .gv-layers{--command-color:var(--layers-blue)}
#aladin-cosmic-command-test .gv-world{--command-color:var(--world-blue)}
#aladin-cosmic-command-test .gv-projection{--command-color:var(--projection-blue)}
#aladin-cosmic-command-test .gv-fullscreen{--command-color:var(--fullscreen-blue)}
#aladin-cosmic-command-test .gv-plus{--command-color:var(--zoom-plus)}
#aladin-cosmic-command-test .gv-minus{--command-color:var(--zoom-minus)}
#aladin-cosmic-command-test .gv-command,
#aladin-cosmic-command-test .gv-command *{color:var(--command-color)!important}
#aladin-cosmic-command-test .gv-command svg,
#aladin-cosmic-command-test .gv-command svg *{color:var(--command-color)!important}
#aladin-cosmic-command-test .gv-command svg path,
#aladin-cosmic-command-test .gv-command svg line,
#aladin-cosmic-command-test .gv-command svg polyline,
#aladin-cosmic-command-test .gv-command svg polygon,
#aladin-cosmic-command-test .gv-command svg circle,
#aladin-cosmic-command-test .gv-command svg ellipse,
#aladin-cosmic-command-test .gv-command svg rect{stroke:var(--command-color)!important}
#aladin-cosmic-command-test .gv-command svg path[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg polygon[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg circle[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg rect[fill]:not([fill="none"]),
#aladin-cosmic-command-test .gv-command svg text,
#aladin-cosmic-command-test .gv-command svg tspan{fill:var(--command-color)!important}
#aladin-cosmic-command-test .gv-command img,
#aladin-cosmic-command-test .gv-command canvas{filter:var(--command-filter)!important}

#aladin-cosmic-command-test .gv-native-coordinate-target-row{
    position:absolute!important;z-index:5000!important;display:flex!important;
    flex-flow:row nowrap!important;align-items:center!important;gap:0!important;
    margin:0!important;padding:0!important;width:max-content!important;box-sizing:border-box!important;
    pointer-events:none!important;
}
#aladin-cosmic-command-test .gv-native-coordinate-target-row>.aladin-location,
#aladin-cosmic-command-test .gv-native-coordinate-target-row>.aladin-coordinates{
    position:static!important;inset:auto!important;margin:0!important;transform:none!important;
    height:34px!important;min-height:34px!important;max-height:34px!important;
    box-sizing:border-box!important;color:#7575FF!important;
}
#aladin-cosmic-command-test .gv-native-simbad-engine{
    position:absolute!important;left:-10000px!important;top:-10000px!important;
    width:1px!important;height:1px!important;min-width:1px!important;min-height:1px!important;
    max-width:1px!important;max-height:1px!important;padding:0!important;margin:0!important;
    opacity:0!important;visibility:hidden!important;pointer-events:none!important;overflow:hidden!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy,
#aladin-cosmic-command-test button.gv-simbad-proxy:hover,
#aladin-cosmic-command-test button.gv-simbad-proxy:focus,
#aladin-cosmic-command-test button.gv-simbad-proxy:focus-visible,
#aladin-cosmic-command-test button.gv-simbad-proxy:active,
#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active{
    appearance:none!important;-webkit-appearance:none!important;
    position:static!important;inset:auto!important;margin:0!important;padding:0!important;
    width:34px!important;min-width:34px!important;max-width:34px!important;
    height:34px!important;min-height:34px!important;max-height:34px!important;
    flex:0 0 34px!important;align-self:center!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    box-sizing:border-box!important;overflow:hidden!important;transform:none!important;
    background:rgba(0,0,0,.78)!important;color:var(--copy-blue)!important;
    border:1px solid #FFFFFF!important;border-radius:6px!important;
    cursor:pointer!important;touch-action:manipulation!important;outline:none!important;box-shadow:none!important;
    pointer-events:auto!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy img.gv-target-trademark{
    display:block!important;
    width:32px!important;height:32px!important;
    min-width:32px!important;min-height:32px!important;max-width:32px!important;max-height:32px!important;
    object-fit:contain!important;
    pointer-events:none!important;user-select:none!important;
    filter:none!important;
}
#aladin-cosmic-command-test #gv-version-label{
    position:absolute!important;left:50%!important;bottom:4px!important;transform:translateX(-50%)!important;
    z-index:6000!important;padding:2px 7px!important;border:1px solid rgba(255,255,255,.65)!important;
    border-radius:4px!important;background:rgba(0,0,0,.70)!important;color:#BCEEFF!important;
    font-family:"Roboto Mono",Consolas,monospace!important;font-size:11px!important;font-weight:700!important;
    line-height:1.2!important;letter-spacing:.2px!important;white-space:nowrap!important;pointer-events:none!important;
}

#aladin-cosmic-command-test .gv-helper-row{display:flex!important;align-items:center!important;margin-left:-15px!important}
#aladin-cosmic-command-test .gv-arrow{
    color:var(--copy-blue)!important;font-size:22px!important;font-weight:bold!important;
    margin-right:6px!important;position:relative!important;left:5px!important;top:0!important;
    text-shadow:0 0 6px rgba(125,244,255,.70)!important;
}
#aladin-cosmic-command-test .gv-helper-box{
    display:flex!important;align-items:center!important;justify-content:center!important;
    height:34px!important;padding:0 16px!important;position:relative!important;top:2px!important;
    background:transparent!important;border:1px solid #FFFFFF!important;border-radius:6px!important;
    color:var(--copy-blue)!important;font-family:"Roboto Mono",Consolas,monospace!important;
    font-size:13px!important;font-weight:600!important;line-height:1.3!important;
    white-space:nowrap!important;box-sizing:border-box!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-box{
    width:200px!important;max-width:200px!important;height:72px!important;min-height:72px!important;
    padding:3px 10px!important;flex-direction:column!important;align-items:center!important;
    justify-content:center!important;text-align:center!important;color:#FFD166!important;
    line-height:1.08!important;text-shadow:0 0 10px rgba(255,209,102,.75)!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line{
    display:block!important;width:100%!important;text-align:center!important;color:#FFD166!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line:nth-child(1){
    color:#FFD166!important;text-shadow:0 0 10px rgba(255,209,102,.75)!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-pan-line{
    display:flex!important;align-items:center!important;justify-content:center!important;gap:5px!important;
    color:#45E7FF!important;-webkit-text-fill-color:#45E7FF!important;
    text-shadow:0 0 6px rgba(69,231,255,.55)!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-lock{
    display:block!important;width:13px!important;height:13px!important;flex:0 0 13px!important;
    overflow:visible!important;color:#45E7FF!important;filter:none!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-lock *{
    fill:none!important;stroke:#45E7FF!important;stroke-width:1.8!important;
    stroke-linecap:round!important;stroke-linejoin:round!important;vector-effect:non-scaling-stroke!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line:nth-child(3),
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line:nth-child(4){
    color:var(--gv-active-blue)!important;
    -webkit-text-fill-color:var(--gv-active-blue)!important;
    filter:none!important;
    text-shadow:0 1px 1px rgba(0,0,0,.95)!important;
}
#aladin-cosmic-command-test .gv-simbad-helper-stack{
    display:flex!important;flex-direction:column!important;align-self:center!important;
    margin:0 0 0 9px!important;padding:0!important;
}
#aladin-cosmic-command-test .gv-simbad-live-status{
    display:none!important;margin:4px 0 0 25px!important;padding:3px 8px!important;
    width:max-content!important;max-width:294px!important;box-sizing:border-box!important;
    color:#FFD166!important;background:rgba(0,0,0,.78)!important;
    border:1px solid rgba(255,209,102,.65)!important;border-radius:4px!important;
    font-family:"Roboto Mono","DejaVu Sans Mono",Consolas,monospace!important;
    font-size:14px!important;font-weight:700!important;line-height:1.25!important;
    white-space:normal!important;pointer-events:none!important;
}
#aladin-cosmic-command-test .gv-simbad-live-status.gv-visible{display:block!important}
#aladin-cosmic-command-test .gv-simbad-live-status.gv-clear-ready{
    pointer-events:auto!important;cursor:pointer!important;touch-action:manipulation!important;
    user-select:none!important;border-color:#7DF4FF!important;box-shadow:0 0 8px rgba(125,244,255,.55)!important;
}
#aladin-cosmic-command-test .gv-plus,#aladin-cosmic-command-test .gv-plus *{color:#55FF88!important}
#aladin-cosmic-command-test .gv-minus,#aladin-cosmic-command-test .gv-minus *{color:#FF5E78!important}
#aladin-cosmic-command-test .gv-plus svg,#aladin-cosmic-command-test .gv-plus svg *{stroke:#55FF88!important;fill:#55FF88!important}
#aladin-cosmic-command-test .gv-minus svg,#aladin-cosmic-command-test .gv-minus svg *{stroke:#FF5E78!important;fill:#FF5E78!important}
</style>
<div id="aladin-cosmic-command-test"></div>
"""))

display(Javascript(r"""
(() => {
    const aladinBundleUrl="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js";

    function startGalaxyViewer(){
        if(!window.A||!window.A.init){
            console.error("GV-beta-0004N STARTUP FAILURE: window.A was not created");
            return;
        }

        window.A.init.then(() => {
            const A=window.A;
            const root=document.getElementById("aladin-cosmic-command-test");
            const aladin=A.aladin("#aladin-cosmic-command-test",{
                target:"M 31",survey:"P/DSS2/color",fov:1.5,cooFrame:"ICRSd",projection:"TAN",
                reticleColor:"#62D8FF",reticleSize:22,showReticle:true,
                showZoomControl:true,showFullscreenControl:false,showLayersControl:true,
                showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true,
                showProjectionControl:true
            });
            window.aladin_cosmic_command_test=aladin;
            let versionLabel=root.querySelector("#gv-version-label");
            if(!versionLabel){
                versionLabel=document.createElement("div");
                versionLabel.id="gv-version-label";
                versionLabel.textContent="Galaxy Viewer 4N";
                root.appendChild(versionLabel);
            }

            const filters={
                copy:"brightness(0) saturate(100%) invert(94%) sepia(44%) saturate(1415%) hue-rotate(160deg) brightness(103%) contrast(103%)",
                layers:"brightness(0) saturate(100%) invert(58%) sepia(99%) saturate(1819%) hue-rotate(190deg) brightness(102%) contrast(101%)",
                world:"brightness(0) saturate(100%) invert(55%) sepia(94%) saturate(1690%) hue-rotate(219deg) brightness(101%) contrast(101%)",
                projection:"brightness(0) saturate(100%) invert(79%) sepia(38%) saturate(1260%) hue-rotate(172deg) brightness(101%) contrast(102%)",
                fullscreen:"brightness(0) saturate(100%) invert(94%) sepia(21%) saturate(996%) hue-rotate(171deg) brightness(104%) contrast(102%)",
                plus:"brightness(0) saturate(100%) invert(84%) sepia(66%) saturate(654%) hue-rotate(77deg) brightness(105%) contrast(104%)",
                minus:"brightness(0) saturate(100%) invert(53%) sepia(84%) saturate(3287%) hue-rotate(319deg) brightness(105%) contrast(101%)"
            };

            const normalize=value=>String(value||"").trim().split(/\s+/).join(" ");
            let simbadModeActive=false;
            let resultReady=false;
            let paletteScheduled=false;
            let blueSequenceTimer=null;
            let blueSequenceIndex=0;
            const blueSequence=["#45E7FF","#4F9DFF","#7575FF"];

            function applyBlueSequenceColor(){root.style.setProperty("--gv-active-blue",blueSequence[blueSequenceIndex]);}
            function advanceBlueSequence(){blueSequenceIndex=(blueSequenceIndex+1)%blueSequence.length;applyBlueSequenceColor();}
            function startBlueSequence(){if(blueSequenceTimer)return;blueSequenceIndex=0;applyBlueSequenceColor();blueSequenceTimer=setInterval(advanceBlueSequence,500);}
            function stopBlueSequence(){if(blueSequenceTimer){clearInterval(blueSequenceTimer);blueSequenceTimer=null}blueSequenceIndex=0;applyBlueSequenceColor();}
            function syncBlueSequenceState(){const target=root.querySelector("button.gv-simbad-proxy");const helperRow=root.querySelector(".gv-helper-row");const active=!!helperRow&&helperRow.classList.contains("gv-active");if(target){target.classList.toggle("gv-active",active);target.setAttribute("aria-pressed",active?"true":"false")}if(active)startBlueSequence();else stopBlueSequence();}

            function describe(element){return [element.className||"",element.id||"",element.getAttribute?.("title")||"",element.getAttribute?.("aria-label")||"",element.getAttribute?.("data-tooltip")||"",element.textContent||""].join(" ").toLowerCase()}
            function controlContainer(element){return element.closest("button,[role='button'],[class*='Control'],[class*='control'],[class*='projection'],[class*='fullscreen'],[class*='location']")||element}
            function mark(element,className,filterName){const control=controlContainer(element);control.classList.add("gv-command",className);control.style.setProperty("--command-filter",filters[filterName],"important")}
            function findCoordinateBox(){return root.querySelector(".aladin-location")||root.querySelector(".aladin-coordinates")}
            function findNativeSimbadEngine(){const claimed=root.querySelector("button.gv-native-simbad-engine");if(claimed)return claimed;const direct=root.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");if(direct)return direct;const wrapper=root.querySelector(".aladin-simbadPointer-control,.aladin-simbadPointerControl,[class*='simbadPointer']");if(!wrapper)return null;if(wrapper.matches?.("button.aladin-btn"))return wrapper;return wrapper.querySelector?.("button.aladin-btn")||null;}
            function getProxy(){return root.querySelector("button.gv-simbad-proxy")}
            function syncProxyBorder(coordinateBox,proxy){proxy.style.setProperty("height","34px","important");proxy.style.setProperty("min-height","34px","important");proxy.style.setProperty("max-height","34px","important");proxy.style.setProperty("border","1px solid #FFFFFF","important");proxy.style.setProperty("border-radius","6px","important");}
            function setHelperIdle(){const stack=root.querySelector(".gv-simbad-helper-stack");if(!stack)return;const row=stack.querySelector(".gv-helper-row"),arrow=stack.querySelector(".gv-arrow"),box=stack.querySelector(".gv-helper-box");row?.classList.remove("gv-active");if(arrow){arrow.style.color="var(--copy-blue)";arrow.style.animation="none"}if(box){box.innerHTML="Tap Target to Find Info";box.style.color="var(--copy-blue)";box.style.setProperty("border-color","#FFFFFF","important");box.style.animation="";box.style.textShadow="0 0 6px rgba(125,244,255,.60)"}syncBlueSequenceState();}
            function setHelperActive(){const stack=root.querySelector(".gv-simbad-helper-stack");if(!stack)return;const row=stack.querySelector(".gv-helper-row"),arrow=stack.querySelector(".gv-arrow"),box=stack.querySelector(".gv-helper-box");row?.classList.add("gv-active");if(arrow){arrow.style.color="var(--copy-blue)";arrow.style.animation="none"}if(box){box.innerHTML='<span class="gv-helper-active-line">✨ Tap Galaxy / Star</span><span class="gv-helper-active-line gv-helper-pan-line"><svg class="gv-helper-lock" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="4.5" y="10" width="15" height="10" rx="2"></rect><path d="M8 10V7.5a4 4 0 0 1 8 0V10"></path><circle cx="12" cy="14.5" r="1.2"></circle><path d="M12 15.7V18"></path></svg><span>Pan Disabled</span></span><span class="gv-helper-active-line">or Tap Target Again</span><span class="gv-helper-active-line">to Exit</span>';box.style.setProperty("color","#FFD166","important");box.style.setProperty("border-color","#FFFFFF","important");box.style.animation="none"}syncBlueSequenceState();}
            function resetHelperAndStatus(){setHelperIdle();const stack=root.querySelector(".gv-simbad-helper-stack"),proxy=getProxy();if(proxy){proxy.classList.remove("gv-active");proxy.setAttribute("aria-pressed","false");proxy.blur?.()}if(!stack)return;const status=stack.querySelector(".gv-simbad-live-status");if(status){status.textContent="";status.classList.remove("gv-visible","gv-clear-ready");status.setAttribute("aria-label","");status.setAttribute("role","status");status.removeAttribute("tabindex")}syncBlueSequenceState();}
            function clearSimbad(){const al=window.aladin_cosmic_command_test;if(al&&typeof al.useSimbadPointer==="function")al.useSimbadPointer(false);simbadModeActive=false;resultReady=false;resetHelperAndStatus();}
            function ensureHelper(row,proxy){let stack=row.querySelector(".gv-simbad-helper-stack");if(!stack){stack=document.createElement("div");stack.className="gv-simbad-helper-stack";stack.innerHTML=`<div class="gv-helper-row"><div class="gv-arrow">◀</div><div class="gv-helper-box">Tap Target to Find Info</div></div><div class="gv-simbad-live-status" role="status" aria-live="polite"></div>`}if(stack.parentElement!==row||proxy.nextElementSibling!==stack)proxy.insertAdjacentElement("afterend",stack);const status=stack.querySelector(".gv-simbad-live-status");if(!status.dataset.gvClearBound){status.dataset.gvClearBound="true";status.addEventListener("click",()=>{if(status.classList.contains("gv-clear-ready"))clearSimbad()});status.addEventListener("keydown",event=>{if((event.key==="Enter"||event.key===" ")&&status.classList.contains("gv-clear-ready")){event.preventDefault();clearSimbad()}})}}
            function bindProxy(proxy){if(proxy.dataset.gvProxyBound)return;proxy.dataset.gvProxyBound="true";proxy.addEventListener("click",e=>{e.stopPropagation();e.preventDefault();const al=window.aladin_cosmic_command_test;if(simbadModeActive){if(al&&typeof al.useSimbadPointer==="function")al.useSimbadPointer(false);else{const btn=document.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");if(btn)btn.click()}simbadModeActive=false;resetHelperAndStatus();return}setHelperActive();simbadModeActive=true;if(al&&typeof al.useSimbadPointer==="function"){al.useSimbadPointer(true);return}const btn=document.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");if(btn)btn.click();});}
            function createProxy(){let proxy=getProxy();if(proxy)return proxy;proxy=document.createElement("button");proxy.type="button";proxy.className="gv-simbad-proxy gv-command gv-copy";proxy.setAttribute("title","SIMBAD pointer");proxy.setAttribute("aria-label","SIMBAD pointer");proxy.setAttribute("aria-pressed","false");proxy.style.setProperty("--command-filter",filters.copy,"important");proxy.innerHTML=`<img class="gv-target-trademark" src="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/icon_target_vector.svg?v=608828c6835dd2d892969475469937f0a6956552" alt="" aria-hidden="true" draggable="false">`;bindProxy(proxy);return proxy;}
            function buildTargetRow(){const coordinateBox=findCoordinateBox(),engine=findNativeSimbadEngine();if(!coordinateBox||!engine)return false;engine.classList.add("gv-native-simbad-engine");engine.setAttribute("aria-hidden","true");engine.tabIndex=-1;let row=root.querySelector(".gv-native-coordinate-target-row");if(!row){const rootRect=root.getBoundingClientRect(),coordinateRect=coordinateBox.getBoundingClientRect();if(coordinateRect.width<=0||coordinateRect.height<=0)return false;row=document.createElement("div");row.className="gv-native-coordinate-target-row";row.style.setProperty("left",Math.round(coordinateRect.left-rootRect.left)+"px","important");row.style.setProperty("top",Math.round(coordinateRect.top-rootRect.top)+"px","important");coordinateBox.parentElement.insertBefore(row,coordinateBox);row.appendChild(coordinateBox)}const proxy=createProxy();if(proxy.parentElement!==row)row.appendChild(proxy);syncProxyBorder(coordinateBox,proxy);ensureHelper(row,proxy);syncBlueSequenceState();return coordinateBox.nextElementSibling===proxy;}
            function applyPalette(){root.querySelectorAll("*").forEach(element=>{const description=describe(element),text=normalize(element.textContent);if(description.includes("copy")||description.includes("clipboard"))mark(element,"gv-copy","copy");if(description.includes("layer")||description.includes("stack"))mark(element,"gv-layers","layers");if(description.includes("world")||description.includes("globe")||description.includes("grid"))mark(element,"gv-world","world");if(description.includes("projection")||text==="TAN"||text==="SIN")mark(element,"gv-projection","projection");if(description.includes("fullscreen")||description.includes("full screen")||description.includes("maximize"))mark(element,"gv-fullscreen","fullscreen");if(description.includes("zoom in")||description.includes("zoomin")||text==="+")mark(element,"gv-plus","plus");if(description.includes("zoom out")||description.includes("zoomout")||text==="-"||text==="−")mark(element,"gv-minus","minus");if(text==="ICRS"||text==="ICRSd"||/^[-+]?\d+(\.\d+)?\s+[-+]?\d+(\.\d+)?$/.test(text))element.classList.add("gv-standard-text");});buildTargetRow();syncBlueSequenceState();}
            function schedulePalette(){if(paletteScheduled)return;paletteScheduled=true;requestAnimationFrame(()=>{paletteScheduled=false;applyPalette()})}
            [250,700,1400,2400].forEach(delay=>setTimeout(schedulePalette,delay));
            const observer=new MutationObserver(()=>{schedulePalette();syncBlueSequenceState()});
            observer.observe(root,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:["class"]});
            window.addEventListener("resize",schedulePalette);
            [100,300,700,1400,2400].forEach(delay=>setTimeout(syncBlueSequenceState,delay));
        }).catch(error=>console.error("GV-beta-0004N STARTUP FAILURE:",error));
    }

    if(window.A&&window.A.init){
        startGalaxyViewer();
        return;
    }

    let loader=document.querySelector('script[data-gv-aladin="3.8.2"]');
    if(loader){
        loader.addEventListener("load",startGalaxyViewer,{once:true});
        loader.addEventListener("error",()=>console.error("GV-beta-0004N STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
        return;
    }

    loader=document.createElement("script");
    loader.src=aladinBundleUrl;
    loader.charset="utf-8";
    loader.dataset.gvAladin="3.8.2";
    loader.addEventListener("load",startGalaxyViewer,{once:true});
    loader.addEventListener("error",()=>console.error("GV-beta-0004N STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
    document.head.appendChild(loader);
})();
"""))

# GV-beta-0004N released