from IPython.display import HTML, Javascript, display

# GV-beta-0005A
# Standalone stripped-down Galaxy Viewer release based on the complete GV-beta-0004O baseline.
# Removes the inherited native coordinate/Target/SIMBAD proxy architecture.
# No replacement coordinate or Target module is included in this release.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
#aladin-cosmic-command-test{
    width:100%;height:100vh;height:100dvh;position:relative!important;
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
#aladin-cosmic-command-test #gv-version-label{
    position:absolute!important;left:50%!important;bottom:4px!important;transform:translateX(-50%)!important;
    z-index:6000!important;padding:2px 7px!important;border:1px solid rgba(255,255,255,.65)!important;
    border-radius:4px!important;background:rgba(0,0,0,.70)!important;color:#BCEEFF!important;
    font-family:"Roboto Mono",Consolas,monospace!important;font-size:11px!important;font-weight:700!important;
    line-height:1.2!important;letter-spacing:.2px!important;white-space:nowrap!important;pointer-events:none!important;
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
            console.error("GV-beta-0005A STARTUP FAILURE: window.A was not created");
            return;
        }

        window.A.init.then(() => {
            const A=window.A;
            const root=document.getElementById("aladin-cosmic-command-test");
            const aladin=A.aladin("#aladin-cosmic-command-test",{
                target:"M 31",survey:"P/DSS2/color",fov:1.5,cooFrame:"ICRSd",projection:"TAN",
                reticleColor:"#62D8FF",reticleSize:22,showReticle:true,
                showZoomControl:true,showFullscreenControl:false,showLayersControl:true,
                showGotoControl:false,showCooGridControl:true,showSimbadPointerControl:false,
                showProjectionControl:true
            });
            window.aladin_cosmic_command_test=aladin;
            let versionLabel=root.querySelector("#gv-version-label");
            if(!versionLabel){
                versionLabel=document.createElement("div");
                versionLabel.id="gv-version-label";
                versionLabel.textContent="Galaxy Viewer 5A";
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
            let paletteScheduled=false;

            function describe(element){return [element.className||"",element.id||"",element.getAttribute?.("title")||"",element.getAttribute?.("aria-label")||"",element.getAttribute?.("data-tooltip")||"",element.textContent||""].join(" ").toLowerCase()}
            function controlContainer(element){return element.closest("button,[role='button'],[class*='Control'],[class*='control'],[class*='projection'],[class*='fullscreen']")||element}
            function mark(element,className,filterName){const control=controlContainer(element);control.classList.add("gv-command",className);control.style.setProperty("--command-filter",filters[filterName],"important")}

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
                });
            }
            function schedulePalette(){if(paletteScheduled)return;paletteScheduled=true;requestAnimationFrame(()=>{paletteScheduled=false;applyPalette()})}
            [250,700,1400,2400].forEach(delay=>setTimeout(schedulePalette,delay));
            const observer=new MutationObserver(schedulePalette);
            observer.observe(root,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:["class"]});
            window.addEventListener("resize",schedulePalette);
        }).catch(error=>console.error("GV-beta-0005A STARTUP FAILURE:",error));
    }

    if(window.A&&window.A.init){
        startGalaxyViewer();
        return;
    }

    let loader=document.querySelector('script[data-gv-aladin="3.8.2"]');
    if(loader){
        loader.addEventListener("load",startGalaxyViewer,{once:true});
        loader.addEventListener("error",()=>console.error("GV-beta-0005A STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
        return;
    }

    loader=document.createElement("script");
    loader.src=aladinBundleUrl;
    loader.charset="utf-8";
    loader.dataset.gvAladin="3.8.2";
    loader.addEventListener("load",startGalaxyViewer,{once:true});
    loader.addEventListener("error",()=>console.error("GV-beta-0005A STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
    document.head.appendChild(loader);
})();
"""))

# GV-beta-0005A released
