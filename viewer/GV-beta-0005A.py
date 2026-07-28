from IPython.display import HTML, Javascript, display

# GV-beta-0005A
# Standalone Galaxy Viewer release based on GV-beta-0004O.
# Restores the standard Aladin viewer controls and reticle.
# Contains no custom coordinate module, Target control, SIMBAD proxy, helper, or overlay.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{width:100%;height:100vh;height:100dvh;position:relative!important}
#aladin-cosmic-command-test .aladin-location,
#aladin-cosmic-command-test .aladin-coordinates,
#aladin-cosmic-command-test .aladin-logo,
#aladin-cosmic-command-test .aladin-copyright,
#aladin-cosmic-command-test .aladin-fov,
#aladin-cosmic-command-test .aladin-status-bar,
#aladin-cosmic-command-test .aladin-cooFrame{
    display:none!important;
    visibility:hidden!important;
    opacity:0!important;
    pointer-events:none!important;
}
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
            const aladin=A.aladin("#aladin-cosmic-command-test",{
                target:"M 31",survey:"P/DSS2/color",fov:1.5,cooFrame:"ICRSd",projection:"TAN",
                reticleColor:"#62D8FF",reticleSize:22,showReticle:true,
                showZoomControl:true,
                showFullscreenControl:false,
                showLayersControl:true,
                showGotoControl:false,
                showCooGridControl:true,
                showSettingsControl:false,
                showSelectionModeControl:false,
                showColorPickerControl:false,
                showShareControl:false,
                showSimbadPointerControl:false,
                showProjectionControl:true,
                showStatusBar:false,
                showFrame:false,
                showFov:false,
                showCooLocation:false,
                showContextMenu:false,
                showCatalog:false,
                showCooGrid:false
            });
            window.aladin_cosmic_command_test=aladin;
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
