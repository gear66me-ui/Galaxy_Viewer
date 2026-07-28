from IPython.display import HTML, Javascript, display

# GV-beta-0005A
# Standalone Galaxy Viewer release based on the complete GV-beta-0004O baseline.
# Replaces the inherited native coordinate/SIMBAD proxy architecture with a
# Galaxy Viewer-owned coordinate-frame, live-coordinate, and Target module.
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

#aladin-cosmic-command-test .gv-coordinate-control-module{
    position:absolute!important;left:8px!important;bottom:8px!important;z-index:5000!important;
    display:flex!important;flex-flow:row nowrap!important;align-items:center!important;gap:0!important;
    margin:0!important;padding:0!important;width:max-content!important;max-width:calc(100% - 16px)!important;
    box-sizing:border-box!important;font-family:"Roboto Mono",Consolas,monospace!important;
}
#aladin-cosmic-command-test .gv-frame-select,
#aladin-cosmic-command-test .gv-live-coordinate,
#aladin-cosmic-command-test .gv-target-button{
    height:34px!important;min-height:34px!important;max-height:34px!important;
    box-sizing:border-box!important;background:rgba(0,0,0,.78)!important;
    border:1px solid #FFFFFF!important;border-radius:0!important;
    font-family:"Roboto Mono",Consolas,monospace!important;font-weight:700!important;
    outline:none!important;box-shadow:none!important;
}
#aladin-cosmic-command-test .gv-frame-select{
    width:86px!important;min-width:86px!important;padding:0 22px 0 8px!important;
    color:#62D8FF!important;font-size:12px!important;cursor:pointer!important;
    border-radius:6px 0 0 6px!important;
}
#aladin-cosmic-command-test .gv-live-coordinate{
    display:flex!important;align-items:center!important;justify-content:center!important;
    min-width:226px!important;padding:0 10px!important;margin-left:-1px!important;
    color:#7575FF!important;font-size:12px!important;white-space:nowrap!important;
    text-shadow:0 0 5px rgba(117,117,255,.55)!important;
}
#aladin-cosmic-command-test .gv-target-button,
#aladin-cosmic-command-test .gv-target-button:hover,
#aladin-cosmic-command-test .gv-target-button:focus,
#aladin-cosmic-command-test .gv-target-button:focus-visible,
#aladin-cosmic-command-test .gv-target-button:active{
    appearance:none!important;-webkit-appearance:none!important;
    width:74px!important;min-width:74px!important;max-width:74px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;gap:5px!important;
    margin-left:-1px!important;padding:0 7px!important;border-radius:0 6px 6px 0!important;
    color:var(--copy-blue)!important;font-size:12px!important;cursor:pointer!important;
    touch-action:manipulation!important;
}
#aladin-cosmic-command-test .gv-target-button img{
    display:block!important;width:24px!important;height:24px!important;object-fit:contain!important;
    pointer-events:none!important;user-select:none!important;filter:none!important;
}
#aladin-cosmic-command-test .gv-target-button.gv-active{
    color:var(--gv-active-blue)!important;
    text-shadow:0 0 8px color-mix(in srgb,var(--gv-active-blue) 70%,transparent)!important;
}
#aladin-cosmic-command-test .gv-coordinate-helper{
    position:absolute!important;left:8px!important;bottom:47px!important;z-index:5000!important;
    display:none!important;padding:5px 9px!important;max-width:290px!important;
    box-sizing:border-box!important;background:rgba(0,0,0,.78)!important;
    border:1px solid #FFFFFF!important;border-radius:6px!important;color:#FFD166!important;
    font-family:"Roboto Mono",Consolas,monospace!important;font-size:12px!important;font-weight:700!important;
    line-height:1.25!important;text-align:center!important;white-space:normal!important;
}
#aladin-cosmic-command-test .gv-coordinate-helper.gv-visible{display:block!important}
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

            function createCoordinateControlModule(aladinInstance,viewerRoot){
                let module=viewerRoot.querySelector(".gv-coordinate-control-module");
                if(module)return module;

                module=document.createElement("div");
                module.className="gv-coordinate-control-module";
                module.setAttribute("role","group");
                module.setAttribute("aria-label","Galaxy Viewer coordinate controls");
                module.innerHTML=`
                    <select class="gv-frame-select" aria-label="Coordinate frame">
                        <option value="ICRS">ICRS</option>
                        <option value="ICRSd" selected>ICRSd</option>
                        <option value="GAL">Galactic</option>
                    </select>
                    <div class="gv-live-coordinate" aria-live="polite">10.6847083&nbsp;&nbsp;+41.2687500</div>
                    <button class="gv-target-button" type="button" aria-label="SIMBAD Target" aria-pressed="false">
                        <img src="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/icon_target_vector.svg?v=608828c6835dd2d892969475469937f0a6956552" alt="" aria-hidden="true" draggable="false">
                        <span>Target</span>
                    </button>`;
                viewerRoot.appendChild(module);

                const helper=document.createElement("div");
                helper.className="gv-coordinate-helper";
                helper.textContent="Tap a galaxy or star to find SIMBAD information. Tap Target again to exit.";
                viewerRoot.appendChild(helper);

                const frameSelect=module.querySelector(".gv-frame-select");
                const coordinateDisplay=module.querySelector(".gv-live-coordinate");
                const targetButton=module.querySelector(".gv-target-button");
                let simbadActive=false;
                let blueTimer=null;
                let blueIndex=0;
                const blueSequence=["#45E7FF","#4F9DFF","#7575FF"];

                function setBlue(){viewerRoot.style.setProperty("--gv-active-blue",blueSequence[blueIndex]);}
                function startBlue(){if(blueTimer)return;blueIndex=0;setBlue();blueTimer=setInterval(()=>{blueIndex=(blueIndex+1)%blueSequence.length;setBlue();},500);}
                function stopBlue(){if(blueTimer){clearInterval(blueTimer);blueTimer=null;}blueIndex=0;setBlue();}
                function setTargetState(active){
                    simbadActive=active;
                    targetButton.classList.toggle("gv-active",active);
                    targetButton.setAttribute("aria-pressed",active?"true":"false");
                    helper.classList.toggle("gv-visible",active);
                    if(active)startBlue();else stopBlue();
                }

                frameSelect.addEventListener("change",event=>{
                    if(typeof aladinInstance.setFrame==="function")aladinInstance.setFrame(event.target.value);
                });

                targetButton.addEventListener("click",event=>{
                    event.preventDefault();
                    event.stopPropagation();
                    const next=!simbadActive;
                    if(typeof aladinInstance.useSimbadPointer==="function")aladinInstance.useSimbadPointer(next);
                    setTargetState(next);
                });

                function updateCoordinates(){
                    try{
                        const coordinates=typeof aladinInstance.getRaDec==="function"?aladinInstance.getRaDec():null;
                        if(Array.isArray(coordinates)&&coordinates.length>=2&&Number.isFinite(Number(coordinates[0]))&&Number.isFinite(Number(coordinates[1]))){
                            const ra=Number(coordinates[0]).toFixed(7);
                            const decNumber=Number(coordinates[1]);
                            const dec=(decNumber>=0?"+":"")+decNumber.toFixed(7);
                            coordinateDisplay.textContent=`${ra}  ${dec}`;
                        }
                    }catch(error){console.debug("GV-beta-0005A coordinate update skipped",error);}
                }

                updateCoordinates();
                const coordinateTimer=setInterval(updateCoordinates,150);
                module.dataset.gvCoordinateTimer=String(coordinateTimer);
                return module;
            }

            createCoordinateControlModule(aladin,root);

            function applyPalette(){root.querySelectorAll("*").forEach(element=>{const description=describe(element),text=normalize(element.textContent);if(element.closest(".gv-coordinate-control-module,.gv-coordinate-helper"))return;if(description.includes("copy")||description.includes("clipboard"))mark(element,"gv-copy","copy");if(description.includes("layer")||description.includes("stack"))mark(element,"gv-layers","layers");if(description.includes("world")||description.includes("globe")||description.includes("grid"))mark(element,"gv-world","world");if(description.includes("projection")||text==="TAN"||text==="SIN")mark(element,"gv-projection","projection");if(description.includes("fullscreen")||description.includes("full screen")||description.includes("maximize"))mark(element,"gv-fullscreen","fullscreen");if(description.includes("zoom in")||description.includes("zoomin")||text==="+")mark(element,"gv-plus","plus");if(description.includes("zoom out")||description.includes("zoomout")||text==="-"||text==="−")mark(element,"gv-minus","minus");});}
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
