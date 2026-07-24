from IPython.display import HTML, display

# viewer-0030
# Standalone Galaxy Viewer release.
# Uses a fixed Galaxy Viewer SIMBAD proxy button while keeping Aladin's native
# SIMBAD control hidden as the command engine.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML(r"""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
#aladin-cosmic-command-test{
    width:100%;height:650px;position:relative!important;
    --text-blue:#62D8FF;--copy-blue:#7DF4FF;--layers-blue:#4F9DFF;
    --world-blue:#8B7CFF;--projection-blue:#6FC7FF;--fullscreen-blue:#BCEEFF;
    --zoom-plus:#55FF88;--zoom-minus:#FF5E78;
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
    flex-flow:row nowrap!important;align-items:stretch!important;gap:0!important;
    margin:0!important;padding:0!important;width:max-content!important;box-sizing:border-box!important;
}
#aladin-cosmic-command-test .gv-native-coordinate-target-row>.aladin-location,
#aladin-cosmic-command-test .gv-native-coordinate-target-row>.aladin-coordinates{
    position:static!important;inset:auto!important;margin:0!important;transform:none!important;
}

/* Native Aladin SIMBAD button remains functional but is never shown. */
#aladin-cosmic-command-test .gv-native-simbad-engine{
    position:absolute!important;left:-10000px!important;top:-10000px!important;
    width:1px!important;height:1px!important;min-width:1px!important;min-height:1px!important;
    max-width:1px!important;max-height:1px!important;padding:0!important;margin:0!important;
    opacity:0!important;visibility:hidden!important;pointer-events:none!important;overflow:hidden!important;
}

/* Visible target is ours and cannot be resized by Aladin. */
#aladin-cosmic-command-test button.gv-simbad-proxy{
    appearance:none!important;-webkit-appearance:none!important;
    position:static!important;inset:auto!important;margin:0!important;padding:0!important;
    transform:none!important;flex:0 0 auto!important;align-self:stretch!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    box-sizing:border-box!important;overflow:hidden!important;background:rgba(0,0,0,.78)!important;
    color:var(--copy-blue)!important;cursor:pointer!important;touch-action:manipulation!important;
    outline:none!important;box-shadow:none!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy:hover,
#aladin-cosmic-command-test button.gv-simbad-proxy:focus,
#aladin-cosmic-command-test button.gv-simbad-proxy:focus-visible,
#aladin-cosmic-command-test button.gv-simbad-proxy:active,
#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active{
    transform:none!important;padding:0!important;margin:0!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy svg{
    display:block!important;width:81%!important;height:81%!important;
    min-width:0!important;min-height:0!important;max-width:81%!important;max-height:81%!important;
    transform:none!important;transform-origin:center center!important;overflow:visible!important;
    color:var(--copy-blue)!important;filter:drop-shadow(0 0 3px rgba(125,244,255,.7))!important;
    pointer-events:none!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy svg *{
    fill:none!important;stroke:currentColor!important;stroke-width:1.8!important;
    stroke-linecap:round!important;stroke-linejoin:round!important;vector-effect:non-scaling-stroke!important;
}

#aladin-cosmic-command-test .gv-simbad-helper-stack{
    display:flex!important;flex-direction:column!important;align-self:center!important;
    margin:0 0 0 9px!important;padding:0!important;
}
#aladin-cosmic-command-test .gv-simbad-helper{
    display:flex!important;align-items:center!important;gap:6px!important;margin:0!important;padding:0!important;
    border:0!important;background:transparent!important;color:#FFD166!important;
    font-family:"Roboto Mono","DejaVu Sans Mono",Consolas,monospace!important;
    font-size:11px!important;font-weight:700!important;line-height:1.12!important;letter-spacing:.15px!important;
    width:238px!important;max-width:238px!important;white-space:normal!important;
    text-shadow:0 0 4px rgba(255,209,102,.45)!important;pointer-events:none!important;
}
#aladin-cosmic-command-test .gv-simbad-helper-text{display:block!important;width:205px!important;max-width:205px!important}
#aladin-cosmic-command-test .gv-simbad-helper-arrow{
    width:19px!important;min-width:19px!important;height:12px!important;display:block!important;
    overflow:visible!important;color:var(--copy-blue)!important;
    filter:drop-shadow(0 0 3px rgba(125,244,255,.72))!important;
}
#aladin-cosmic-command-test .gv-simbad-helper-arrow path{
    fill:none!important;stroke:currentColor!important;stroke-width:2!important;
    stroke-linecap:round!important;stroke-linejoin:round!important;
}
#aladin-cosmic-command-test .gv-simbad-helper.gv-active .gv-simbad-helper-arrow{
    animation:gv-left-arrow-pulse 1.15s ease-in-out infinite;
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
#aladin-cosmic-command-test .gv-plus,
#aladin-cosmic-command-test .gv-plus *{color:#55FF88!important}
#aladin-cosmic-command-test .gv-minus,
#aladin-cosmic-command-test .gv-minus *{color:#FF5E78!important}
#aladin-cosmic-command-test .gv-plus svg,
#aladin-cosmic-command-test .gv-plus svg *{stroke:#55FF88!important;fill:#55FF88!important}
#aladin-cosmic-command-test .gv-minus svg,
#aladin-cosmic-command-test .gv-minus svg *{stroke:#FF5E78!important;fill:#FF5E78!important}
@keyframes gv-left-arrow-pulse{0%,100%{transform:translateX(0);opacity:.82}50%{transform:translateX(-2px);opacity:1}}
</style>
<div id="aladin-cosmic-command-test"></div>
<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js" charset="utf-8"></script>
<script>
A.init.then(() => {
    const root=document.getElementById("aladin-cosmic-command-test");
    const aladin=A.aladin("#aladin-cosmic-command-test",{
        target:"M 31",survey:"P/DSS2/color",fov:1.5,cooFrame:"ICRSd",projection:"TAN",
        reticleColor:"#62D8FF",reticleSize:22,showReticle:true,
        showZoomControl:true,showFullscreenControl:true,showLayersControl:true,
        showGotoControl:true,showCooGridControl:true,showSimbadPointerControl:true,
        showProjectionControl:true
    });
    window.aladin_cosmic_command_test=aladin;

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

    function describe(element){
        return [element.className||"",element.id||"",element.getAttribute?.("title")||"",element.getAttribute?.("aria-label")||"",element.getAttribute?.("data-tooltip")||"",element.textContent||""].join(" ").toLowerCase();
    }
    function controlContainer(element){
        return element.closest("button,[role='button'],[class*='Control'],[class*='control'],[class*='projection'],[class*='fullscreen'],[class*='location']")||element;
    }
    function mark(element,className,filterName){
        const control=controlContainer(element);
        if(!control.classList.contains("gv-command"))control.classList.add("gv-command");
        if(!control.classList.contains(className))control.classList.add(className);
        if(control.style.getPropertyValue("--command-filter")!==filters[filterName]){
            control.style.setProperty("--command-filter",filters[filterName],"important");
        }
    }
    function findCoordinateBox(){
        return root.querySelector(".aladin-location")||root.querySelector(".aladin-coordinates");
    }
    function findNativeSimbadEngine(){
        const claimed=root.querySelector("button.gv-native-simbad-engine");
        if(claimed)return claimed;
        const direct=root.querySelector(
            "button.aladin-simbadPointer-control,"+
            "button.aladin-simbadPointerControl,"+
            "button.aladin-btn[class*='simbadPointer']"
        );
        if(direct)return direct;
        const wrapper=root.querySelector(
            ".aladin-simbadPointer-control,"+
            ".aladin-simbadPointerControl,"+
            "[class*='simbadPointer']"
        );
        if(!wrapper)return null;
        if(wrapper.matches?.("button.aladin-btn"))return wrapper;
        return wrapper.querySelector?.("button.aladin-btn")||null;
    }
    function getProxy(){
        return root.querySelector("button.gv-simbad-proxy");
    }

    function syncProxyGeometry(coordinateBox,proxy){
        const rect=coordinateBox.getBoundingClientRect();
        const height=Math.max(1,Math.round(rect.height));
        const width=Math.max(height,Math.round(height*1.08));
        const style=window.getComputedStyle(coordinateBox);
        const borderColor=style.borderRightColor||"rgb(236,236,236)";
        const borderWidth=parseFloat(style.borderRightWidth)>0?style.borderRightWidth:"1px";
        const borderStyle=style.borderRightStyle!=="none"?style.borderRightStyle:"solid";
        const radius=style.borderTopRightRadius!=="0px"?style.borderTopRightRadius:"6px";
        [["width",width+"px"],["min-width",width+"px"],["max-width",width+"px"],
         ["height",height+"px"],["min-height",height+"px"],["max-height",height+"px"],
         ["border-style",borderStyle],["border-width",borderWidth],
         ["border-color",borderColor],["border-radius",radius]].forEach(([property,value])=>{
            if(proxy.style.getPropertyValue(property)!==value){
                proxy.style.setProperty(property,value,"important");
            }
        });
    }

    function resetHelperAndStatus(){
        const stack=root.querySelector(".gv-simbad-helper-stack");
        const proxy=getProxy();
        if(proxy){
            proxy.classList.remove("gv-active");
            proxy.setAttribute("aria-pressed","false");
            proxy.blur?.();
        }
        if(!stack)return;
        stack.querySelector(".gv-simbad-helper")?.classList.remove("gv-active");
        const text=stack.querySelector(".gv-simbad-helper-text");
        const status=stack.querySelector(".gv-simbad-live-status");
        if(text)text.innerHTML="Click target, then click<br>a galaxy or star to find info";
        if(status){
            status.textContent="";
            status.classList.remove("gv-visible","gv-clear-ready");
            status.setAttribute("aria-label","");
            status.setAttribute("role","status");
            status.removeAttribute("tabindex");
        }
    }

    function clearSimbad(){
        try{aladin.hidePopup()}catch(error){
            root.querySelectorAll(".aladin-popup-container .aladin-closeBtn").forEach(button=>button.click());
        }
        try{aladin.fire("default")}catch(error){
            const engine=findNativeSimbadEngine();
            if(engine&&simbadModeActive)engine.click();
        }
        simbadModeActive=false;
        resultReady=false;
        resetHelperAndStatus();
    }

    function setClearReady(){
        const status=root.querySelector(".gv-simbad-live-status");
        if(!status||resultReady)return;
        resultReady=true;
        status.innerHTML="SIMBAD result displayed<br>TAP HERE TO CLEAR";
        status.classList.add("gv-visible","gv-clear-ready");
        status.setAttribute("role","button");
        status.setAttribute("aria-label","Clear SIMBAD result and restore navigation");
        status.tabIndex=0;
    }

    function ensureHelper(row,proxy){
        let stack=row.querySelector(".gv-simbad-helper-stack");
        if(!stack){
            stack=document.createElement("div");
            stack.className="gv-simbad-helper-stack";
            stack.innerHTML=`<div class="gv-simbad-helper" aria-live="polite"><svg class="gv-simbad-helper-arrow" viewBox="0 0 24 14" aria-hidden="true"><path d="M22 7H6"></path><path d="M11 2L5 7L11 12"></path></svg><span class="gv-simbad-helper-text">Click target, then click<br>a galaxy or star to find info</span></div><div class="gv-simbad-live-status" role="status" aria-live="polite"></div>`;
        }
        if(stack.parentElement!==row||proxy.nextElementSibling!==stack){
            proxy.insertAdjacentElement("afterend",stack);
        }
        const status=stack.querySelector(".gv-simbad-live-status");
        if(!status.dataset.gvClearBound){
            status.dataset.gvClearBound="true";
            status.addEventListener("click",()=>{
                if(status.classList.contains("gv-clear-ready"))clearSimbad();
            });
            status.addEventListener("keydown",event=>{
                if((event.key==="Enter"||event.key===" ")&&status.classList.contains("gv-clear-ready")){
                    event.preventDefault();
                    clearSimbad();
                }
            });
        }
    }

    function bindProxy(proxy){
        if(proxy.dataset.gvProxyBound)return;
        proxy.dataset.gvProxyBound="true";
        proxy.addEventListener("click",()=>{
            const engine=findNativeSimbadEngine();
            if(!engine)return;
            resultReady=false;
            engine.click();
            simbadModeActive=!simbadModeActive;
            const stack=root.querySelector(".gv-simbad-helper-stack");
            const helper=stack?.querySelector(".gv-simbad-helper");
            const text=stack?.querySelector(".gv-simbad-helper-text");
            const status=stack?.querySelector(".gv-simbad-live-status");
            if(simbadModeActive){
                proxy.classList.add("gv-active");
                proxy.setAttribute("aria-pressed","true");
                helper?.classList.add("gv-active");
                if(text)text.innerHTML="Now click a galaxy or star<br>to find information";
                if(status){
                    status.textContent="SIMBAD active — tap one object.";
                    status.classList.add("gv-visible");
                    status.classList.remove("gv-clear-ready");
                    status.setAttribute("role","status");
                }
            }else{
                resetHelperAndStatus();
            }
        });
    }

    function createProxy(){
        let proxy=getProxy();
        if(proxy)return proxy;
        proxy=document.createElement("button");
        proxy.type="button";
        proxy.className="gv-simbad-proxy gv-command gv-copy";
        proxy.setAttribute("title","SIMBAD pointer");
        proxy.setAttribute("aria-label","SIMBAD pointer");
        proxy.setAttribute("aria-pressed","false");
        proxy.style.setProperty("--command-filter",filters.copy,"important");
        proxy.innerHTML=`<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="8.5"></circle><circle cx="16" cy="16" r="2.2"></circle><path d="M16 2.5V8"></path><path d="M16 24V29.5"></path><path d="M2.5 16H8"></path><path d="M24 16H29.5"></path></svg>`;
        bindProxy(proxy);
        return proxy;
    }

    function buildTargetRow(){
        const coordinateBox=findCoordinateBox();
        const engine=findNativeSimbadEngine();
        if(!coordinateBox||!engine)return false;
        engine.classList.add("gv-native-simbad-engine");
        engine.setAttribute("aria-hidden","true");
        engine.tabIndex=-1;

        let row=root.querySelector(".gv-native-coordinate-target-row");
        if(!row){
            const rootRect=root.getBoundingClientRect();
            const coordinateRect=coordinateBox.getBoundingClientRect();
            if(coordinateRect.width<=0||coordinateRect.height<=0)return false;
            row=document.createElement("div");
            row.className="gv-native-coordinate-target-row";
            row.style.setProperty("left",Math.round(coordinateRect.left-rootRect.left)+"px","important");
            row.style.setProperty("top",Math.round(coordinateRect.top-rootRect.top)+"px","important");
            coordinateBox.parentElement.insertBefore(row,coordinateBox);
            row.appendChild(coordinateBox);
        }

        const proxy=createProxy();
        if(proxy.parentElement!==row)row.appendChild(proxy);
        syncProxyGeometry(coordinateBox,proxy);
        ensureHelper(row,proxy);
        return coordinateBox.nextElementSibling===proxy;
    }

    function detectSimbadPopup(){
        const popup=root.querySelector(".aladin-popup-container");
        if(!popup)return;
        const style=window.getComputedStyle(popup);
        const text=normalize(popup.textContent);
        const visible=style.display!=="none"&&popup.getBoundingClientRect().width>0;
        const isSimbad=popup.querySelector(".aladin-sp-title,.aladin-sp-content")||
            text.toLowerCase().includes("query in cds portal")||
            text.toLowerCase().includes("no match was found");
        if(visible&&isSimbad)setClearReady();
    }

    function applyPalette(){
        root.querySelectorAll("*").forEach(element=>{
            const description=describe(element);
            const text=normalize(element.textContent);
            if(description.includes("copy")||description.includes("clipboard"))mark(element,"gv-copy","copy");
            if(description.includes("layer")||description.includes("stack"))mark(element,"gv-layers","layers");
            if(description.includes("world")||description.includes("globe")||description.includes("grid"))mark(element,"gv-world","world");
            if(description.includes("projection")||text==="TAN"||text==="SIN")mark(element,"gv-projection","projection");
            if(description.includes("fullscreen")||description.includes("full screen")||description.includes("maximize"))mark(element,"gv-fullscreen","fullscreen");
            if(description.includes("zoom in")||description.includes("zoomin")||text==="+")mark(element,"gv-plus","plus");
            if(description.includes("zoom out")||description.includes("zoomout")||text==="-"||text==="−")mark(element,"gv-minus","minus");
            if(text==="ICRS"||text==="ICRSd"||/^[-+]?\d+(\.\d+)?\s+[-+]?\d+(\.\d+)?$/.test(text)){
                if(!element.classList.contains("gv-standard-text"))element.classList.add("gv-standard-text");
            }
        });
        buildTargetRow();
        detectSimbadPopup();
    }

    function schedulePalette(){
        if(paletteScheduled)return;
        paletteScheduled=true;
        requestAnimationFrame(()=>{
            paletteScheduled=false;
            applyPalette();
        });
    }

    [250,700,1400,2400].forEach(delay=>setTimeout(schedulePalette,delay));
    const observer=new MutationObserver(()=>schedulePalette());
    observer.observe(root,{childList:true,subtree:true,characterData:true});

    const popupPoll=setInterval(()=>{
        if(!document.body.contains(root)){
            clearInterval(popupPoll);
            observer.disconnect();
            return;
        }
        if(simbadModeActive&&!resultReady)detectSimbadPopup();
    },250);

    window.addEventListener("resize",()=>schedulePalette());
});
</script>
"""))