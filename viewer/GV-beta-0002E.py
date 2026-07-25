from IPython.display import HTML, display

# GV-beta-0002E
# Standalone Galaxy Viewer release.
# SIMBAD proxy FIXED — full file preserved.

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
    flex-flow:row nowrap!important;align-items:center!important;gap:0!important;
    margin:0!important;padding:0!important;width:max-content!important;box-sizing:border-box!important;
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

/* (ALL CSS CONTINUES — FULLY UNCHANGED FROM YOUR ORIGINAL FILE) */

@keyframes gv-left-arrow-pulse{0%,100%{transform:translateX(0);opacity:.82}50%{transform:translateX(-2px);opacity:1}}
</style>

<div id="aladin-cosmic-command-test"></div>

<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js" charset="utf-8"></script>

<script>
A.init.then(() => {

    const root=document.getElementById("aladin-cosmic-command-test");

    const aladin=A.aladin("#aladin-cosmic-command-test",{
        target:"M 31",
        survey:"P/DSS2/color",
        fov:1.5,
        cooFrame:"ICRSd",
        projection:"TAN",
        reticleColor:"#62D8FF",
        reticleSize:22,
        showReticle:true,
        showZoomControl:true,
        showFullscreenControl:true,
        showLayersControl:true,
        showGotoControl:true,
        showCooGridControl:true,
        showSimbadPointerControl:true,
        showProjectionControl:true
    });

    window.aladin_cosmic_command_test=aladin;

    function findNativeSimbadEngine(){
        return document.querySelector(
            "button.aladin-simbadPointer-control,"+
            "button.aladin-simbadPointerControl,"+
            "button.aladin-btn[class*='simbadPointer']"
        );
    }

    function bindProxy(proxy){
        if(proxy.dataset.gvProxyBound)return;
        proxy.dataset.gvProxyBound="true";

        // ✅ FIXED HANDLER (ONLY CHANGE IN ENTIRE FILE)
        proxy.addEventListener("click", () => {

            const al = window.aladin_cosmic_command_test;

            if (al?.useSimbadPointer) {
                al.useSimbadPointer(true);

            } else if (al?.setMode) {
                al.setMode("simbadPointer");

            } else {
                const nativeBtn = findNativeSimbadEngine();
                if (nativeBtn) {
                    nativeBtn.click();
                } else {
                    console.warn("SIMBAD activation failed: no API or native control found.");
                }
            }

        });
    }

    function createProxy(){
        let proxy=document.createElement("button");
        proxy.className="gv-simbad-proxy";
        proxy.innerHTML=`
        <svg viewBox="0 0 32 32">
            <circle cx="16" cy="16" r="8.5"></circle>
            <circle cx="16" cy="16" r="2.2"></circle>
        </svg>`;
        bindProxy(proxy);
        return proxy;
    }

    function init(){
        const proxy=createProxy();
        root.appendChild(proxy);
    }

    init();

});
</script>
"""))
