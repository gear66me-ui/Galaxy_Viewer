from IPython.display import HTML, display

# GV-beta-0002E
# Standalone Galaxy Viewer release.
# ONLY CHANGE: SIMBAD proxy click handler FIXED
# EVERYTHING ELSE IDENTICAL TO 0002A

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

#aladin-cosmic-command-test .gv-native-coordinate-target-row{
    position:absolute!important;z-index:5000!important;display:flex!important;
    flex-flow:row nowrap!important;align-items:center!important;gap:0!important;
}

#aladin-cosmic-command-test button.gv-simbad-proxy{
    width:34px!important;height:34px!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    background:rgba(0,0,0,.78)!important;color:var(--copy-blue)!important;
    cursor:pointer!important;
}
</style>

<div id="aladin-cosmic-command-test"></div>

<script src="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js"></script>

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

        // ✅ ONLY CHANGE IN ENTIRE FILE
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
        proxy.innerHTML=`<svg viewBox="0 0 32 32">
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
