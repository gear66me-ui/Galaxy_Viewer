from IPython.display import HTML, Javascript, display

# GV-beta-0005E
# Standalone curated-first Galaxy Viewer release based only on GV-beta-0005D.
# Preserves the 5D UI, random startup, Back/Next history, and version label.
# Selects approximately 90% curated outreach galaxies and 10% discovery galaxies.

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
#aladin-cosmic-command-test #gv-version-label{
    position:absolute!important;left:12px!important;bottom:12px!important;z-index:7100!important;
    display:block!important;visibility:visible!important;opacity:1!important;pointer-events:none!important;
    padding:6px 9px!important;border:1px solid rgba(188,238,255,.85)!important;border-radius:5px!important;
    background:rgba(0,0,0,.82)!important;color:#BCEEFF!important;
    font:700 12px/1.15 "Roboto Mono",Consolas,monospace!important;
    letter-spacing:.2px!important;text-shadow:0 0 6px rgba(188,238,255,.45)!important;
}
#aladin-cosmic-command-test #gv-random-galaxy-panel{
    position:absolute!important;right:12px!important;bottom:12px!important;z-index:7000!important;
    display:flex!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;
    flex-direction:column!important;align-items:flex-end!important;gap:6px!important;
    font-family:"Roboto Mono",Consolas,monospace!important;
}
#aladin-cosmic-command-test #gv-random-galaxy-name{
    max-width:320px!important;padding:5px 9px!important;border:1px solid rgba(98,216,255,.75)!important;
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
    const curatedCatalogUrl="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/discovery/beautiful-galaxy-catalog-beta.json";
    const discoveryCatalogUrl="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/discovery/galaxy-catalog-beta.json";
    const CURATED_WEIGHT=0.90;

    async function fetchCuratedRecords(){
        const response=await fetch(curatedCatalogUrl+"?v="+Date.now(),{cache:"no-store"});
        if(!response.ok)throw new Error("Curated catalog returned HTTP "+response.status);
        const payload=await response.json();
        return Array.isArray(payload.targets)
            ? payload.targets.filter(target=>target&&target.name).map((target,index)=>({
                primary_name:String(target.name),
                target_name:String(target.name),
                preferred_fov_deg:Number(target.fov)||0.18,
                source:"OUTREACH",
                source_id:"OUTREACH:"+String(index+1).padStart(4,"0")
            }))
            : [];
    }

    async function fetchDiscoveryRecords(){
        const response=await fetch(discoveryCatalogUrl+"?v="+Date.now(),{cache:"no-store"});
        if(!response.ok)throw new Error("Discovery catalog returned HTTP "+response.status);
        const payload=await response.json();
        return Array.isArray(payload.records)
            ? payload.records.filter(record=>record&&record.source==="SIMBAD")
            : [];
    }

    function recordKey(record){
        return String(record?.source||"")+"|"+String(record?.source_id||record?.primary_name||"");
    }

    function chooseRecord(curatedRecords,discoveryRecords,currentRecord){
        const preferCurated=curatedRecords.length&&(!discoveryRecords.length||Math.random()<CURATED_WEIGHT);
        const pool=preferCurated?curatedRecords:discoveryRecords;
        if(!pool.length)return null;
        let next=pool[Math.floor(Math.random()*pool.length)];
        if(pool.length>1&&recordKey(next)===recordKey(currentRecord)){
            const index=pool.indexOf(next);
            next=pool[(index+1)%pool.length];
        }
        return next;
    }

    function targetFor(record){
        const ra=Number(record?.ra_deg),dec=Number(record?.dec_deg);
        if(Number.isFinite(ra)&&Number.isFinite(dec))return ra+" "+dec;
        return String(record?.target_name||record?.primary_name||"0 0").trim();
    }

    function fovFor(record){
        return Math.min(1.5,Math.max(0.04,Number(record?.preferred_fov_deg)||0.18));
    }

    function startGalaxyViewer(){
        if(!window.A||!window.A.init){console.error("GV-beta-0005E STARTUP FAILURE: window.A was not created");return;}

        window.A.init.then(async() => {
            const A=window.A;
            const root=document.getElementById("aladin-cosmic-command-test");

            let curatedRecords=[],discoveryRecords=[];
            try{
                [curatedRecords,discoveryRecords]=await Promise.all([
                    fetchCuratedRecords(),
                    fetchDiscoveryRecords(),
                ]);
            }catch(error){
                console.error("GV-beta-0005E CATALOG FAILURE:",error);
            }

            const firstRecord=chooseRecord(curatedRecords,discoveryRecords,null);
            const initialTarget=firstRecord?targetFor(firstRecord):"0 0";
            const initialFov=firstRecord?fovFor(firstRecord):0.18;

            const aladin=A.aladin("#aladin-cosmic-command-test",{
                target:initialTarget,survey:"P/DSS2/color",fov:initialFov,cooFrame:"ICRSd",projection:"TAN",
                showReticle:false,showZoomControl:false,showFullscreenControl:false,showLayersControl:false,
                showGotoControl:false,showCooGridControl:false,showSettingsControl:false,
                showSelectionModeControl:false,showColorPickerControl:false,showShareControl:false,
                showSimbadPointerControl:false,showProjectionControl:false,showStatusBar:false,
                showFrame:false,showFov:false,showCooLocation:false,showContextMenu:false,
                showCatalog:false,showCooGrid:false
            });
            window.aladin_cosmic_command_test=aladin;

            const versionLabel=document.createElement("div");
            versionLabel.id="gv-version-label";
            versionLabel.textContent="Galaxy Viewer 5E";
            root.appendChild(versionLabel);

            const panel=document.createElement("div");
            panel.id="gv-random-galaxy-panel";
            panel.innerHTML='<div id="gv-random-galaxy-name" role="status" aria-live="polite">Loading beautiful galaxy catalog…</div><div id="gv-galaxy-navigation"><button id="gv-back-galaxy" type="button" disabled>Back</button><button id="gv-next-galaxy" type="button" disabled>Next Galaxy</button></div>';
            root.appendChild(panel);

            const nameLabel=panel.querySelector("#gv-random-galaxy-name");
            const backButton=panel.querySelector("#gv-back-galaxy");
            const nextButton=panel.querySelector("#gv-next-galaxy");
            let history=[];
            let historyPosition=-1;
            let navigating=false;

            async function openGalaxy(record){
                if(!record||navigating)return;
                navigating=true;
                backButton.disabled=true;
                nextButton.disabled=true;
                try{
                    const ra=Number(record?.ra_deg),dec=Number(record?.dec_deg);
                    const fov=fovFor(record);
                    if(Number.isFinite(ra)&&Number.isFinite(dec)){
                        aladin.gotoRaDec(ra,dec);
                    }else{
                        await Promise.resolve(aladin.gotoObject(targetFor(record)));
                    }
                    aladin.setFoV(fov);
                    const category=record.source==="OUTREACH"?"Beautiful":"Discovery";
                    const type=String(record.morphology||"Galaxy").trim();
                    nameLabel.textContent=String(record.primary_name||"Unnamed galaxy").trim()+" · "+category+" · "+type+" · FOV "+fov.toFixed(2)+"°";
                }catch(error){
                    nameLabel.textContent="Could not resolve "+String(record.primary_name||"galaxy");
                    console.error("GV-beta-0005E TARGET FAILURE:",error);
                }finally{
                    navigating=false;
                    backButton.disabled=historyPosition<=0;
                    nextButton.disabled=!(curatedRecords.length||discoveryRecords.length);
                }
            }

            async function openNextGalaxy(){
                if(navigating)return;
                const current=historyPosition>=0?history[historyPosition]:null;
                const nextRecord=chooseRecord(curatedRecords,discoveryRecords,current);
                if(!nextRecord)return;
                if(historyPosition<history.length-1)history=history.slice(0,historyPosition+1);
                history.push(nextRecord);
                historyPosition=history.length-1;
                await openGalaxy(nextRecord);
            }

            async function openPreviousGalaxy(){
                if(navigating||historyPosition<=0)return;
                historyPosition-=1;
                await openGalaxy(history[historyPosition]);
            }

            backButton.addEventListener("click",openPreviousGalaxy);
            nextButton.addEventListener("click",openNextGalaxy);

            if(firstRecord){
                history=[firstRecord];
                historyPosition=0;
                await openGalaxy(firstRecord);
            }else{
                nameLabel.textContent="Galaxy catalogs unavailable";
            }
        }).catch(error=>console.error("GV-beta-0005E STARTUP FAILURE:",error));
    }

    if(window.A&&window.A.init){startGalaxyViewer();return;}
    let loader=document.querySelector('script[data-gv-aladin="3.8.2"]');
    if(loader){
        loader.addEventListener("load",startGalaxyViewer,{once:true});
        loader.addEventListener("error",()=>console.error("GV-beta-0005E STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
        return;
    }
    loader=document.createElement("script");
    loader.src=aladinBundleUrl;
    loader.charset="utf-8";
    loader.dataset.gvAladin="3.8.2";
    loader.addEventListener("load",startGalaxyViewer,{once:true});
    loader.addEventListener("error",()=>console.error("GV-beta-0005E STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
    document.head.appendChild(loader);
})();
"""))

# GV-beta-0005E released
