from IPython.display import HTML, Javascript, display

# GV-beta-0005A
# Standalone stripped-down Galaxy Viewer release based on GV-beta-0004O.
# Contains no coordinate module, Target control, SIMBAD control, helper, or viewer control icons.
# No earlier Galaxy Viewer file is imported, downloaded, patched, or executed.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{width:100%;height:100vh;height:100dvh;position:relative!important}
#aladin-cosmic-command-test #gv-version-label{
    position:absolute!important;left:50%!important;bottom:4px!important;transform:translateX(-50%)!important;
    z-index:6000!important;padding:2px 7px!important;border:1px solid rgba(255,255,255,.65)!important;
    border-radius:4px!important;background:rgba(0,0,0,.70)!important;color:#BCEEFF!important;
    font-family:"Roboto Mono",Consolas,monospace!important;font-size:11px!important;font-weight:700!important;
    line-height:1.2!important;letter-spacing:.2px!important;white-space:nowrap!important;pointer-events:none!important;
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
            const root=document.getElementById("aladin-cosmic-command-test");
            const aladin=A.aladin("#aladin-cosmic-command-test",{
                target:"M 31",survey:"P/DSS2/color",fov:1.5,cooFrame:"ICRSd",projection:"TAN",
                reticleColor:"#62D8FF",reticleSize:22,showReticle:true,
                showZoomControl:false,showFullscreenControl:false,showLayersControl:false,
                showGotoControl:false,showCooGridControl:false,showSimbadPointerControl:false,
                showProjectionControl:false
            });
            window.aladin_cosmic_command_test=aladin;

            const versionLabel=document.createElement("div");
            versionLabel.id="gv-version-label";
            versionLabel.textContent="Galaxy Viewer 5A";
            root.appendChild(versionLabel);
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
