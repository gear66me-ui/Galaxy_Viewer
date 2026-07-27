from IPython.display import HTML, display

# GV-beta-0003C
# Standalone Galaxy Viewer release based on the known-good GV-beta-0003B state.
# Keeps the synchronized diagonal rainbow across the active Target icon and
# the "or Tap Target Again / to Exit" text, but slows the motion and removes
# the glow/bloom so the icon and lettering retain sharp, readable edges.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
#aladin-cosmic-command-test{
    width:100%;height:650px;position:relative!important;
    --text-blue:#62D8FF;--copy-blue:#7DF4FF;--layers-blue:#4F9DFF;
    --world-blue:#8B7CFF;--projection-blue:#6FC7FF;--fullscreen-blue:#BCEEFF;
    --zoom-plus:#55FF88;--zoom-minus:#FF5E78;
    --gv-rainbow:linear-gradient(135deg,#ff315d 0%,#ff9d2e 16%,#ffe45c 32%,#62ff8c 48%,#45e7ff 64%,#7575ff 80%,#ff55df 100%);
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
    cursor:pointer!important;touch-action:manipulation!important;outline:none!important;box-shadow:none!important;
    pointer-events:auto!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy svg{
    display:block!important;width:27px!important;height:27px!important;
    min-width:27px!important;min-height:27px!important;max-width:27px!important;max-height:27px!important;
    transform:none!important;transform-origin:center center!important;overflow:visible!important;
    color:var(--copy-blue)!important;filter:drop-shadow(0 0 3px rgba(125,244,255,.7))!important;
    pointer-events:none!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy svg *{
    fill:none!important;stroke:currentColor!important;stroke-width:1.8!important;
    stroke-linecap:round!important;stroke-linejoin:round!important;vector-effect:non-scaling-stroke!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active svg *{
    stroke:url(#gv-0003c-rainbow)!important;
}
#aladin-cosmic-command-test button.gv-simbad-proxy.gv-active svg{
    filter:none!important;
    animation:none!important;
    opacity:1!important;
    transform:none!important;
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
    width:200px!important;max-width:200px!important;height:56px!important;min-height:56px!important;
    padding:3px 10px!important;flex-direction:column!important;align-items:center!important;
    justify-content:center!important;text-align:center!important;color:#FFD166!important;
    line-height:1.12!important;text-shadow:0 0 10px rgba(255,209,102,.75)!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line{
    display:block!important;width:100%!important;text-align:center!important;color:#FFD166!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line:nth-child(1){
    color:#FFD166!important;text-shadow:0 0 10px rgba(255,209,102,.75)!important;
}
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line:nth-child(2),
#aladin-cosmic-command-test .gv-helper-row.gv-active .gv-helper-active-line:nth-child(3){
    color:transparent!important;
    background-image:var(--gv-rainbow)!important;
    background-size:260% 260%!important;
    background-position:var(--gv-rainbow-x,0%) var(--gv-rainbow-y,100%)!important;
    -webkit-background-clip:text!important;background-clip:text!important;
    -webkit-text-fill-color:transparent!important;
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

    const normalize=value=>String(value||"").trim().split(/\\s+/).join(" ");
    let simbadModeActive=false;
    let resultReady=false;
    let paletteScheduled=false;
    let rainbowFrame=null;
    let rainbowStart=0;
    let speed=0.072;
    let speedTarget=0.072;
    let nextSpeedChange=0;
    const hueOffsets=[0,48,103,161,219,278,332];

    function hsl(h,s=100,l=66){return `hsl(${((h%360)+360)%360} ${s}% ${l}%)`}
    function ensureGradient(svg){
        if(svg.querySelector("#gv-0003c-rainbow"))return;
        svg.insertAdjacentHTML("afterbegin",`<defs><linearGradient id="gv-0003c-rainbow" x1="0" y1="1" x2="1" y2="0"><stop offset="0%"></stop><stop offset="16%"></stop><stop offset="33%"></stop><stop offset="50%"></stop><stop offset="67%"></stop><stop offset="84%"></stop><stop offset="100%"></stop></linearGradient></defs>`);
    }
    function rainbowTick(now){
        if(!rainbowStart)rainbowStart=now;
        if(now>=nextSpeedChange){speedTarget=.055+Math.random()*.035;nextSpeedChange=now+1800+Math.random()*1400}
        speed+=(speedTarget-speed)*.004;
        const t=(now-rainbowStart)*speed;
        const wobble=Math.sin(now*.00055)*7+Math.sin(now*.00023)*4;
        const colors=hueOffsets.map((offset,i)=>hsl(t+offset+wobble+Math.sin(now*.00042+i)*5,96,64+Math.round(Math.sin(now*.00048+i)*3)));
        const gradient=`linear-gradient(135deg,${colors[0]} 0%,${colors[1]} 16%,${colors[2]} 33%,${colors[3]} 50%,${colors[4]} 67%,${colors[5]} 84%,${colors[6]} 100%)`;
        root.style.setProperty("--gv-rainbow",gradient);
        const phase=((now-rainbowStart)*.035)%260;
        root.style.setProperty("--gv-rainbow-x",`${phase}%`);
        root.style.setProperty("--gv-rainbow-y",`${260-phase}%`);
        const svg=root.querySelector("button.gv-simbad-proxy.gv-active svg");
        if(svg){
            ensureGradient(svg);
            const stops=svg.querySelectorAll("#gv-0003c-rainbow stop");
            stops.forEach((stop,i)=>stop.setAttribute("stop-color",colors[i]));
            const grad=svg.querySelector("#gv-0003c-rainbow");
            if(grad)grad.setAttribute("gradientTransform",`translate(${Math.sin(now*.00045)*.08} ${Math.cos(now*.00039)*.08}) rotate(${(now*.018)%360} .5 .5)`);
        }
        rainbowFrame=requestAnimationFrame(rainbowTick);
    }
    function startRainbow(){if(rainbowFrame)return;rainbowStart=0;rainbowFrame=requestAnimationFrame(rainbowTick)}
    function stopRainbow(){if(rainbowFrame){cancelAnimationFrame(rainbowFrame);rainbowFrame=null}rainbowStart=0}
    function syncRainbowState(){
        const target=root.querySelector("button.gv-simbad-proxy");
        const helperRow=root.querySelector(".gv-helper-row");
        const active=!!helperRow&&helperRow.classList.contains("gv-active");
        if(target){target.classList.toggle("gv-active",active);target.setAttribute("aria-pressed",active?"true":"false");const svg=target.querySelector("svg");if(svg)ensureGradient(svg)}
        if(active)startRainbow();else stopRainbow();
    }

    function describe(element){return [element.className||"",element.id||"",element.getAttribute?.("title")||"",element.getAttribute?.("aria-label")||"",element.getAttribute?.("data-tooltip")||"",element.textContent||""].join(" ").toLowerCase()}
    function controlContainer(element){return element.closest("button,[role='button'],[class*='Control'],[class*='control'],[class*='projection'],[class*='fullscreen'],[class*='location']")||element}
    function mark(element,className,filterName){const control=controlContainer(element);control.classList.add("gv-command",className);control.style.setProperty("--command-filter",filters[filterName],"important")}
    function findCoordinateBox(){return root.querySelector(".aladin-location")||root.querySelector(".aladin-coordinates")}
    function findNativeSimbadEngine(){
        const claimed=root.querySelector("button.gv-native-simbad-engine");if(claimed)return claimed;
        const direct=root.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");if(direct)return direct;
        const wrapper=root.querySelector(".aladin-simbadPointer-control,.aladin-simbadPointerControl,[class*='simbadPointer']");
        if(!wrapper)return null;if(wrapper.matches?.("button.aladin-btn"))return wrapper;return wrapper.querySelector?.("button.aladin-btn")||null;
    }
    function getProxy(){return root.querySelector("button.gv-simbad-proxy")}
    function syncProxyBorder(coordinateBox,proxy){
        const style=window.getComputedStyle(coordinateBox);
        const borderColor=style.borderRightColor||"rgb(236,236,236)";
        const borderWidth=parseFloat(style.borderRightWidth)>0?style.borderRightWidth:"1px";
        const borderStyle=style.borderRightStyle!=="none"?style.borderRightStyle:"solid";
        const radius=style.borderTopRightRadius!=="0px"?style.borderTopRightRadius:"6px";
        [["border-style",borderStyle],["border-width",borderWidth],["border-color",borderColor],["border-radius",radius]].forEach(([property,value])=>proxy.style.setProperty(property,value,"important"));
    }
    function setHelperIdle(){
        const stack=root.querySelector(".gv-simbad-helper-stack");if(!stack)return;
        const row=stack.querySelector(".gv-helper-row"),arrow=stack.querySelector(".gv-arrow"),box=stack.querySelector(".gv-helper-box");
        row?.classList.remove("gv-active");
        if(arrow){arrow.style.color="var(--copy-blue)";arrow.style.animation="none"}
        if(box){box.innerHTML="Tap Target to Find Info";box.style.color="var(--copy-blue)";box.style.setProperty("border-color","#FFFFFF","important");box.style.animation="";box.style.textShadow="0 0 6px rgba(125,244,255,.60)"}
        syncRainbowState();
    }
    function setHelperActive(){
        const stack=root.querySelector(".gv-simbad-helper-stack");if(!stack)return;
        const row=stack.querySelector(".gv-helper-row"),arrow=stack.querySelector(".gv-arrow"),box=stack.querySelector(".gv-helper-box");
        row?.classList.add("gv-active");
        if(arrow){arrow.style.color="var(--copy-blue)";arrow.style.animation="none"}
        if(box){box.innerHTML='<span class="gv-helper-active-line">✨ Tap Galaxy / Star</span><span class="gv-helper-active-line">or Tap Target Again</span><span class="gv-helper-active-line">to Exit</span>';box.style.setProperty("color","#FFD166","important");box.style.setProperty("border-color","#FFFFFF","important");box.style.animation="none"}
        syncRainbowState();
    }
    function resetHelperAndStatus(){
        setHelperIdle();const stack=root.querySelector(".gv-simbad-helper-stack"),proxy=getProxy();
        if(proxy){proxy.classList.remove("gv-active");proxy.setAttribute("aria-pressed","false");proxy.blur?.()}
        if(!stack)return;
        const status=stack.querySelector(".gv-simbad-live-status");
        if(status){status.textContent="";status.classList.remove("gv-visible","gv-clear-ready");status.setAttribute("aria-label","");status.setAttribute("role","status");status.removeAttribute("tabindex")}
        syncRainbowState();
    }
    function clearSimbad(){
        const al=window.aladin_cosmic_command_test;
        if(al&&typeof al.useSimbadPointer==="function")al.useSimbadPointer(false);
        simbadModeActive=false;resultReady=false;resetHelperAndStatus();
    }
    function ensureHelper(row,proxy){
        let stack=row.querySelector(".gv-simbad-helper-stack");
        if(!stack){stack=document.createElement("div");stack.className="gv-simbad-helper-stack";stack.innerHTML=`<div class="gv-helper-row"><div class="gv-arrow">◀</div><div class="gv-helper-box">Tap Target to Find Info</div></div><div class="gv-simbad-live-status" role="status" aria-live="polite"></div>`}
        if(stack.parentElement!==row||proxy.nextElementSibling!==stack)proxy.insertAdjacentElement("afterend",stack);
        const status=stack.querySelector(".gv-simbad-live-status");
        if(!status.dataset.gvClearBound){status.dataset.gvClearBound="true";status.addEventListener("click",()=>{if(status.classList.contains("gv-clear-ready"))clearSimbad()});status.addEventListener("keydown",event=>{if((event.key==="Enter"||event.key===" ")&&status.classList.contains("gv-clear-ready")){event.preventDefault();clearSimbad()}})}
    }
    function bindProxy(proxy){
        if(proxy.dataset.gvProxyBound)return;proxy.dataset.gvProxyBound="true";
        proxy.addEventListener("click",e=>{
            e.stopPropagation();e.preventDefault();const al=window.aladin_cosmic_command_test;
            if(simbadModeActive){if(al&&typeof al.useSimbadPointer==="function")al.useSimbadPointer(false);else{const btn=document.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");if(btn)btn.click()}simbadModeActive=false;resetHelperAndStatus();return}
            setHelperActive();simbadModeActive=true;
            if(al&&typeof al.useSimbadPointer==="function"){al.useSimbadPointer(true);return}
            const btn=document.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");if(btn)btn.click();
        });
    }
    function createProxy(){
        let proxy=getProxy();if(proxy)return proxy;
        proxy=document.createElement("button");proxy.type="button";proxy.className="gv-simbad-proxy gv-command gv-copy";
        proxy.setAttribute("title","SIMBAD pointer");proxy.setAttribute("aria-label","SIMBAD pointer");proxy.setAttribute("aria-pressed","false");
        proxy.style.setProperty("--command-filter",filters.copy,"important");
        proxy.innerHTML=`<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="8.5"></circle><circle cx="16" cy="16" r="2.2"></circle><path d="M16 2.5V8"></path><path d="M16 24V29.5"></path><path d="M2.5 16H8"></path><path d="M24 16H29.5"></path></svg>`;
        ensureGradient(proxy.querySelector("svg"));bindProxy(proxy);return proxy;
    }
    function buildTargetRow(){
        const coordinateBox=findCoordinateBox(),engine=findNativeSimbadEngine();if(!coordinateBox||!engine)return false;
        engine.classList.add("gv-native-simbad-engine");engine.setAttribute("aria-hidden","true");engine.tabIndex=-1;
        let row=root.querySelector(".gv-native-coordinate-target-row");
        if(!row){const rootRect=root.getBoundingClientRect(),coordinateRect=coordinateBox.getBoundingClientRect();if(coordinateRect.width<=0||coordinateRect.height<=0)return false;row=document.createElement("div");row.className="gv-native-coordinate-target-row";row.style.setProperty("left",Math.round(coordinateRect.left-rootRect.left)+"px","important");row.style.setProperty("top",Math.round(coordinateRect.top-rootRect.top)+"px","important");coordinateBox.parentElement.insertBefore(row,coordinateBox);row.appendChild(coordinateBox)}
        const proxy=createProxy();if(proxy.parentElement!==row)row.appendChild(proxy);syncProxyBorder(coordinateBox,proxy);ensureHelper(row,proxy);syncRainbowState();return coordinateBox.nextElementSibling===proxy;
    }
    function applyPalette(){
        root.querySelectorAll("*").forEach(element=>{
            const description=describe(element),text=normalize(element.textContent);
            if(description.includes("copy")||description.includes("clipboard"))mark(element,"gv-copy","copy");
            if(description.includes("layer")||description.includes("stack"))mark(element,"gv-layers","layers");
            if(description.includes("world")||description.includes("globe")||description.includes("grid"))mark(element,"gv-world","world");
            if(description.includes("projection")||text==="TAN"||text==="SIN")mark(element,"gv-projection","projection");
            if(description.includes("fullscreen")||description.includes("full screen")||description.includes("maximize"))mark(element,"gv-fullscreen","fullscreen");
            if(description.includes("zoom in")||description.includes("zoomin")||text==="+")mark(element,"gv-plus","plus");
            if(description.includes("zoom out")||description.includes("zoomout")||text==="-"||text==="−")mark(element,"gv-minus","minus");
            if(text==="ICRS"||text==="ICRSd"||/^[-+]?\\d+(\\.\\d+)?\\s+[-+]?\\d+(\\.\\d+)?$/.test(text))element.classList.add("gv-standard-text");
        });
        buildTargetRow();syncRainbowState();
    }
    function schedulePalette(){if(paletteScheduled)return;paletteScheduled=true;requestAnimationFrame(()=>{paletteScheduled=false;applyPalette()})}
    [250,700,1400,2400].forEach(delay=>setTimeout(schedulePalette,delay));
    const observer=new MutationObserver(()=>{schedulePalette();syncRainbowState()});
    observer.observe(root,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:["class"]});
    window.addEventListener("resize",schedulePalette);
    [100,300,700,1400,2400].forEach(delay=>setTimeout(syncRainbowState,delay));
});
</script>
"""))

# GV-beta-0003C released
