from IPython.display import HTML, Javascript, display

# GV-beta-0005C
# Standalone filtered-catalog Galaxy Viewer release based only on GV-beta-0005B.
# Preserves the empty canvas and adds navigation history with Back and Next Galaxy.
# The beta launcher remains on 5B until this revision is tested and approved.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{width:100%;height:100vh;height:100dvh;position:relative!important}
#aladin-cosmic-command-test button,
#aladin-cosmic-command-test select,
#aladin-cosmic-command-test input,
#aladin-cosmic-command-test .aladin-location,
#aladin-cosmic-command-test .aladin-coordinates,
#aladin-cosmic-command-test .aladin-logo,
#aladin-cosmic-command-test .aladin-copyright,
#aladin-cosmic-command-test .aladin-fov,
#aladin-cosmic-command-test .aladin-status-bar,
#aladin-cosmic-command-test .aladin-cooFrame,
#aladin-cosmic-command-test [class*="Control"],
#aladin-cosmic-command-test [class*="control"],
#aladin-cosmic-command-test [class*="reticle"]{
    display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important;
}
#aladin-cosmic-command-test #gv-random-galaxy-panel{
    position:absolute!important;right:12px!important;bottom:12px!important;z-index:7000!important;
    display:flex!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;
    flex-direction:column!important;align-items:flex-end!important;gap:6px!important;
    font-family:"Roboto Mono",Consolas,monospace!important;
}
#aladin-cosmic-command-test #gv-random-galaxy-name{
    max-width:300px!important;padding:5px 9px!important;border:1px solid rgba(98,216,255,.75)!important;
    border-radius:5px!important;background:rgba(0,0,0,.78)!important;color:#62D8FF!important;
    font-size:12px!important;font-weight:700!important;line-height:1.25!important;text-align:right!important;
    text-shadow:0 0 6px rgba(98,216,255,.55)!important;
}
#aladin-cosmic-command-test #gv-galaxy-navigation{display:flex!important;gap:7px!important;pointer-events:auto!important}
#aladin-cosmic-command-test #gv-galaxy-navigation button{
    display:block!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;
    appearance:none!important;-webkit-appearance:none!important;padding:8px 12px!important;
    border:1px solid #FFFFFF!important;border-radius:6px!important;background:rgba(0,0,0,.82)!important;
    color:#7DF4FF!important;font:700 13px/1.1 "Roboto Mono",Consolas,monospace!important;
    cursor:pointer!important;touch-action:manipulation!important;box-shadow:0 0 8px rgba(125,244,255,.35)!important;
}
#aladin-cosmic-command-test #gv-galaxy-navigation button:disabled{opacity:.45!important;cursor:default!important}
</style>
<div id="aladin-cosmic-command-test"></div>
"""))

display(Javascript(r"""
(() => {
    const aladinBundleUrl="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js";
    const catalogUrl="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/discovery/galaxy-catalog-beta.json";

    function startGalaxyViewer(){
        if(!window.A||!window.A.init){console.error("GV-beta-0005C STARTUP FAILURE: window.A was not created");return;}

        window.A.init.then(() => {
            const A=window.A;
            const root=document.getElementById("aladin-cosmic-command-test");
            const aladin=A.aladin("#aladin-cosmic-command-test",{
                target:"M 31",survey:"P/DSS2/color",fov:1.5,cooFrame:"ICRSd",projection:"TAN",
                showReticle:false,showZoomControl:false,showFullscreenControl:false,showLayersControl:false,
                showGotoControl:false,showCooGridControl:false,showSettingsControl:false,
                showSelectionModeControl:false,showColorPickerControl:false,showShareControl:false,
                showSimbadPointerControl:false,showProjectionControl:false,showStatusBar:false,
                showFrame:false,showFov:false,showCooLocation:false,showContextMenu:false,
                showCatalog:false,showCooGrid:false
            });
            window.aladin_cosmic_command_test=aladin;

            const panel=document.createElement("div");
            panel.id="gv-random-galaxy-panel";
            panel.innerHTML='<div id="gv-random-galaxy-name" role="status" aria-live="polite">Loading filtered galaxy catalog…</div><div id="gv-galaxy-navigation"><button id="gv-back-galaxy" type="button" disabled>Back</button><button id="gv-next-galaxy" type="button" disabled>Next Galaxy</button></div>';
            root.appendChild(panel);

            const nameLabel=panel.querySelector("#gv-random-galaxy-name");
            const backButton=panel.querySelector("#gv-back-galaxy");
            const nextButton=panel.querySelector("#gv-next-galaxy");
            let records=[];
            let history=[];
            let historyPosition=-1;

            function openGalaxy(record){
                const ra=Number(record?.ra_deg),dec=Number(record?.dec_deg);
                const fov=Math.min(1,Math.max(0.04,Number(record?.preferred_fov_deg)||0.10));
                if(!Number.isFinite(ra)||!Number.isFinite(dec))return;
                aladin.gotoRaDec(ra,dec);aladin.setFoV(fov);
                const type=String(record.morphology||"Galaxy").trim();
                nameLabel.textContent=String(record.primary_name||"Unnamed galaxy").trim()+" · "+type+" · FOV "+fov.toFixed(2)+"°";
                backButton.disabled=historyPosition<=0;
            }

            function chooseRandomIndex(){
                if(!records.length)return -1;
                const current=historyPosition>=0?history[historyPosition]:-1;
                let next=Math.floor(Math.random()*records.length);
                if(records.length>1&&next===current)next=(next+1)%records.length;
                return next;
            }

            function openNextGalaxy(){
                const nextIndex=chooseRandomIndex();if(nextIndex<0)return;
                if(historyPosition<history.length-1)history=history.slice(0,historyPosition+1);
                history.push(nextIndex);historyPosition=history.length-1;openGalaxy(records[nextIndex]);
            }

            function openPreviousGalaxy(){
                if(historyPosition<=0)return;
                historyPosition-=1;openGalaxy(records[history[historyPosition]]);
            }

            backButton.addEventListener("click",openPreviousGalaxy);
            nextButton.addEventListener("click",openNextGalaxy);

            fetch(catalogUrl+"?v="+Date.now(),{cache:"no-store"})
                .then(response=>{if(!response.ok)throw new Error("HTTP "+response.status);return response.json();})
                .then(payload=>{
                    records=Array.isArray(payload.records)?payload.records.filter(record=>record&&record.source==="SIMBAD"):[];
                    if(!records.length)throw new Error("Catalog contains no SIMBAD galaxy records");
                    nextButton.disabled=false;openNextGalaxy();
                })
                .catch(error=>{nameLabel.textContent="Filtered galaxy catalog unavailable";console.error("GV-beta-0005C CATALOG FAILURE:",error);});
        }).catch(error=>console.error("GV-beta-0005C STARTUP FAILURE:",error));
    }

    if(window.A&&window.A.init){startGalaxyViewer();return;}
    let loader=document.querySelector('script[data-gv-aladin="3.8.2"]');
    if(loader){
        loader.addEventListener("load",startGalaxyViewer,{once:true});
        loader.addEventListener("error",()=>console.error("GV-beta-0005C STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
        return;
    }
    loader=document.createElement("script");loader.src=aladinBundleUrl;loader.charset="utf-8";loader.dataset.gvAladin="3.8.2";
    loader.addEventListener("load",startGalaxyViewer,{once:true});
    loader.addEventListener("error",()=>console.error("GV-beta-0005C STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
    document.head.appendChild(loader);
})();
"""))

# GV-beta-0005C released
