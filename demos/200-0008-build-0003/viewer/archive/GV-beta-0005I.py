from IPython.display import HTML, Javascript, display

# GV-beta-0005I
# Standalone Galaxy Viewer release based only on the final GV-beta-0005H.
# Preserves the 1,000-record catalog, Spectacular Mode, centered reticle, safe FOV floor, and navigation.
# Adds only the compact native coordinate-frame/coordinate/Target row derived from GV-beta-0004O.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{width:100%;height:100vh;height:100dvh;position:relative!important}
#aladin-cosmic-command-test button,
#aladin-cosmic-command-test input,
#aladin-cosmic-command-test .aladin-location,
#aladin-cosmic-command-test .aladin-coordinates,
#aladin-cosmic-command-test .aladin-logo,
#aladin-cosmic-command-test .aladin-copyright,
#aladin-cosmic-command-test .aladin-fov,
#aladin-cosmic-command-test .aladin-status-bar,
#aladin-cosmic-command-test [class*="Control"],
#aladin-cosmic-command-test [class*="control"],
#aladin-cosmic-command-test [class*="reticle"]{
    display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important;
}
#aladin-cosmic-command-test #gv-center-reticle{
    position:absolute!important;left:50%!important;top:50%!important;z-index:7050!important;
    width:32px!important;height:32px!important;display:block!important;visibility:visible!important;
    opacity:1!important;pointer-events:none!important;user-select:none!important;-webkit-user-drag:none!important;
    transform:translate(-50%,-50%)!important;
}
#aladin-cosmic-command-test .gv-coordinate-target-row{
    position:absolute!important;left:12px!important;top:12px!important;z-index:7120!important;
    display:flex!important;visibility:visible!important;opacity:1!important;align-items:center!important;
    flex-flow:row nowrap!important;gap:0!important;max-width:calc(100% - 24px)!important;
    margin:0!important;padding:0!important;box-sizing:border-box!important;pointer-events:auto!important;
}
#aladin-cosmic-command-test .gv-coordinate-target-row>.aladin-cooFrame{
    position:static!important;inset:auto!important;display:block!important;visibility:visible!important;opacity:1!important;
    width:92px!important;min-width:92px!important;max-width:92px!important;height:32px!important;
    margin:0 7px 0 0!important;padding:0 25px 0 9px!important;box-sizing:border-box!important;
    border:1px solid #7575FF!important;border-radius:6px!important;
    background-color:rgba(0,0,0,.86)!important;color:#BCEEFF!important;
    font:700 12px/1.15 "Roboto Mono",Consolas,monospace!important;
    box-shadow:0 0 10px rgba(117,117,255,.42)!important;pointer-events:auto!important;
}
#aladin-cosmic-command-test .gv-coordinate-target-row>.aladin-location,
#aladin-cosmic-command-test .gv-coordinate-target-row>.aladin-coordinates{
    position:static!important;inset:auto!important;display:flex!important;visibility:visible!important;opacity:1!important;
    align-items:center!important;width:min(52vw,360px)!important;min-width:170px!important;max-width:360px!important;
    height:32px!important;min-height:32px!important;max-height:32px!important;margin:0!important;padding:0 10px!important;
    box-sizing:border-box!important;overflow:hidden!important;border:1px solid #7575FF!important;border-radius:6px!important;
    background:rgba(0,0,0,.86)!important;color:#FFD166!important;
    font:700 12px/1.15 "Roboto Mono",Consolas,monospace!important;
    text-shadow:0 0 6px rgba(255,209,102,.42)!important;box-shadow:0 0 10px rgba(117,117,255,.42)!important;
    pointer-events:auto!important;
}
#aladin-cosmic-command-test .gv-coordinate-target-row>.aladin-location input,
#aladin-cosmic-command-test .gv-coordinate-target-row>.aladin-coordinates input{
    display:block!important;visibility:visible!important;opacity:1!important;width:100%!important;height:100%!important;
    margin:0!important;padding:0!important;border:0!important;background:transparent!important;color:#FFD166!important;
    font:700 12px/1.15 "Roboto Mono",Consolas,monospace!important;text-align:center!important;pointer-events:auto!important;
}
#aladin-cosmic-command-test button.gv-target-proxy,
#aladin-cosmic-command-test button.gv-target-proxy:hover,
#aladin-cosmic-command-test button.gv-target-proxy:focus,
#aladin-cosmic-command-test button.gv-target-proxy:active{
    appearance:none!important;-webkit-appearance:none!important;position:static!important;inset:auto!important;
    display:flex!important;visibility:visible!important;opacity:1!important;align-items:center!important;justify-content:center!important;
    width:34px!important;min-width:34px!important;max-width:34px!important;height:34px!important;min-height:34px!important;max-height:34px!important;
    flex:0 0 34px!important;margin:0 0 0 7px!important;padding:0!important;box-sizing:border-box!important;overflow:hidden!important;
    background:rgba(0,0,0,.82)!important;border:1px solid #FFFFFF!important;border-radius:6px!important;
    cursor:pointer!important;touch-action:manipulation!important;outline:none!important;box-shadow:none!important;pointer-events:auto!important;
}
#aladin-cosmic-command-test button.gv-target-proxy img{
    display:block!important;width:30px!important;height:30px!important;object-fit:contain!important;
    filter:none!important;pointer-events:none!important;user-select:none!important;-webkit-user-drag:none!important;
}
#aladin-cosmic-command-test .gv-native-simbad-engine{
    position:absolute!important;left:-10000px!important;top:-10000px!important;width:1px!important;height:1px!important;
    min-width:1px!important;min-height:1px!important;max-width:1px!important;max-height:1px!important;
    padding:0!important;margin:0!important;opacity:0!important;visibility:hidden!important;pointer-events:none!important;overflow:hidden!important;
}
#aladin-cosmic-command-test #gv-version-label{
    position:absolute!important;left:12px!important;bottom:12px!important;z-index:7100!important;
    display:block!important;visibility:visible!important;opacity:1!important;pointer-events:none!important;
    padding:6px 9px!important;border:1px solid var(--gv-version-color,#FFD166)!important;border-radius:5px!important;
    background:rgba(0,0,0,.84)!important;color:var(--gv-version-color,#FFD166)!important;
    font:700 12px/1.15 "Roboto Mono",Consolas,monospace!important;
    letter-spacing:.2px!important;text-shadow:0 0 7px var(--gv-version-glow,rgba(255,209,102,.65))!important;
    box-shadow:0 0 9px var(--gv-version-glow,rgba(255,209,102,.35))!important;
}
#aladin-cosmic-command-test #gv-random-galaxy-panel{
    position:absolute!important;right:12px!important;bottom:12px!important;z-index:7000!important;
    display:flex!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;
    flex-direction:column!important;align-items:flex-end!important;gap:6px!important;font-family:"Roboto Mono",Consolas,monospace!important;
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
    const reticleUrl="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/GV-reticle-0001.svg";
    const targetIconUrl="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/icon_transparent.png";
    const SPECTACULAR_WEIGHT=0.65;
    const CURATED_WEIGHT=0.30;
    const DISCOVERY_WEIGHT=0.05;
    const MAX_NON_SPECTACULAR_RUN=6;

    async function fetchCuratedRecords(){
        const response=await fetch(curatedCatalogUrl+"?v="+Date.now(),{cache:"no-store"});
        if(!response.ok)throw new Error("Curated catalog returned HTTP "+response.status);
        const payload=await response.json();
        return Array.isArray(payload.targets)?payload.targets.filter(target=>target&&target.name).map((target,index)=>({
            primary_name:String(target.name),target_name:String(target.name),ra_deg:Number(target.ra_deg),dec_deg:Number(target.dec_deg),
            preferred_fov_deg:Number(target.fov)||0.18,morphology:String(target.object_type||"Galaxy"),source:"CURATED",
            source_id:"CURATED:"+String(index+1).padStart(4,"0"),spectacular:target.spectacular===true
        })):[];
    }

    async function fetchDiscoveryRecords(){
        const response=await fetch(discoveryCatalogUrl+"?v="+Date.now(),{cache:"no-store"});
        if(!response.ok)throw new Error("Discovery catalog returned HTTP "+response.status);
        const payload=await response.json();
        return Array.isArray(payload.records)?payload.records.filter(record=>record&&record.source==="SIMBAD").map(record=>({...record,spectacular:false})):[];
    }

    function recordKey(record){return String(record?.source||"")+"|"+String(record?.source_id||record?.primary_name||"");}
    function chooseFromPool(pool,currentRecord){
        if(!pool.length)return null;
        const candidates=pool.filter(record=>recordKey(record)!==recordKey(currentRecord));
        const usable=candidates.length?candidates:pool;
        return usable[Math.floor(Math.random()*usable.length)];
    }
    function chooseRecord(curatedRecords,discoveryRecords,currentRecord,nonSpectacularRun){
        const spectacularRecords=curatedRecords.filter(record=>record.spectacular);
        const otherCuratedRecords=curatedRecords.filter(record=>!record.spectacular);
        if(nonSpectacularRun>=MAX_NON_SPECTACULAR_RUN&&spectacularRecords.length)return chooseFromPool(spectacularRecords,currentRecord);
        const roll=Math.random();
        if(roll<SPECTACULAR_WEIGHT&&spectacularRecords.length)return chooseFromPool(spectacularRecords,currentRecord);
        if(roll<SPECTACULAR_WEIGHT+CURATED_WEIGHT&&otherCuratedRecords.length)return chooseFromPool(otherCuratedRecords,currentRecord);
        if(discoveryRecords.length)return chooseFromPool(discoveryRecords,currentRecord);
        return chooseFromPool(spectacularRecords.length?spectacularRecords:otherCuratedRecords,currentRecord);
    }
    function targetFor(record){
        const ra=Number(record?.ra_deg),dec=Number(record?.dec_deg);
        if(Number.isFinite(ra)&&Number.isFinite(dec))return ra+" "+dec;
        return String(record?.target_name||record?.primary_name||"0 0").trim();
    }
    function fovFor(record){return Math.min(1.5,Math.max(0.18,Number(record?.preferred_fov_deg)||0.18));}

    function startGalaxyViewer(){
        if(!window.A||!window.A.init){console.error("GV-beta-0005I STARTUP FAILURE: window.A was not created");return;}
        window.A.init.then(async() => {
            const A=window.A;
            const root=document.getElementById("aladin-cosmic-command-test");
            let curatedRecords=[],discoveryRecords=[];
            try{[curatedRecords,discoveryRecords]=await Promise.all([fetchCuratedRecords(),fetchDiscoveryRecords()]);}
            catch(error){console.error("GV-beta-0005I CATALOG FAILURE:",error);}

            let nonSpectacularRun=0;
            const firstRecord=chooseRecord(curatedRecords,discoveryRecords,null,nonSpectacularRun);
            const initialTarget=firstRecord?targetFor(firstRecord):"0 0";
            const initialFov=firstRecord?fovFor(firstRecord):0.18;
            const aladin=A.aladin("#aladin-cosmic-command-test",{
                target:initialTarget,survey:"P/DSS2/color",fov:initialFov,cooFrame:"ICRSd",projection:"TAN",
                showReticle:false,showZoomControl:false,showFullscreenControl:false,showLayersControl:false,
                showGotoControl:false,showCooGridControl:false,showSettingsControl:false,
                showSelectionModeControl:false,showColorPickerControl:false,showShareControl:false,
                showSimbadPointerControl:true,showProjectionControl:false,showStatusBar:false,
                showFrame:true,showFov:false,showCooLocation:true,showContextMenu:false,
                showCatalog:false,showCooGrid:false
            });
            window.aladin_cosmic_command_test=aladin;

            const centerReticle=document.createElement("img");
            centerReticle.id="gv-center-reticle";
            centerReticle.src=reticleUrl+"?v=5I-coordinate-row-001";
            centerReticle.alt="";
            centerReticle.setAttribute("aria-hidden","true");
            root.appendChild(centerReticle);

            function findCoordinateBox(){return root.querySelector(".aladin-location")||root.querySelector(".aladin-coordinates");}
            function findNativeSimbadEngine(){
                const claimed=root.querySelector("button.gv-native-simbad-engine");
                if(claimed)return claimed;
                const direct=root.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");
                if(direct)return direct;
                const wrapper=root.querySelector(".aladin-simbadPointer-control,.aladin-simbadPointerControl,[class*='simbadPointer']");
                return wrapper?.matches?.("button.aladin-btn")?wrapper:wrapper?.querySelector?.("button.aladin-btn")||null;
            }
            function createTargetProxy(){
                let proxy=root.querySelector("button.gv-target-proxy");
                if(proxy)return proxy;
                proxy=document.createElement("button");
                proxy.type="button";
                proxy.className="gv-target-proxy";
                proxy.title="SIMBAD target";
                proxy.setAttribute("aria-label","SIMBAD target");
                proxy.setAttribute("aria-pressed","false");
                proxy.innerHTML=`<img src="${targetIconUrl}?v=5I-coordinate-row-001" alt="" aria-hidden="true" draggable="false">`;
                proxy.addEventListener("click",event=>{
                    event.preventDefault();event.stopPropagation();
                    const active=proxy.getAttribute("aria-pressed")!=="true";
                    proxy.setAttribute("aria-pressed",active?"true":"false");
                    if(typeof aladin.useSimbadPointer==="function")aladin.useSimbadPointer(active);
                    else findNativeSimbadEngine()?.click();
                });
                return proxy;
            }
            function buildCoordinateTargetRow(){
                const frame=root.querySelector(".aladin-cooFrame");
                const coordinateBox=findCoordinateBox();
                const engine=findNativeSimbadEngine();
                if(!frame||!coordinateBox||!engine)return false;
                engine.classList.add("gv-native-simbad-engine");
                engine.setAttribute("aria-hidden","true");
                engine.tabIndex=-1;
                let row=root.querySelector(".gv-coordinate-target-row");
                if(!row){row=document.createElement("div");row.className="gv-coordinate-target-row";root.appendChild(row);}
                if(frame.parentElement!==row)row.appendChild(frame);
                if(coordinateBox.parentElement!==row)row.appendChild(coordinateBox);
                const proxy=createTargetProxy();
                if(proxy.parentElement!==row)row.appendChild(proxy);
                return row.children.length>=3;
            }
            [150,350,700,1200,2200].forEach(delay=>setTimeout(buildCoordinateTargetRow,delay));
            const rowObserver=new MutationObserver(()=>buildCoordinateTargetRow());
            rowObserver.observe(root,{childList:true,subtree:true});

            const versionLabel=document.createElement("div");
            versionLabel.id="gv-version-label";
            versionLabel.textContent="Galaxy Viewer 5I";
            const versionPalette=[["#FFD166","rgba(255,209,102,.58)"],["#FF7B8B","rgba(255,123,139,.58)"],["#55FF88","rgba(85,255,136,.52)"],["#45E7FF","rgba(69,231,255,.56)"],["#C98BFF","rgba(201,139,255,.58)"]];
            const versionColor=versionPalette[Math.floor(Math.random()*versionPalette.length)];
            versionLabel.style.setProperty("--gv-version-color",versionColor[0]);
            versionLabel.style.setProperty("--gv-version-glow",versionColor[1]);
            root.appendChild(versionLabel);

            const panel=document.createElement("div");
            panel.id="gv-random-galaxy-panel";
            panel.innerHTML='<div id="gv-random-galaxy-name" role="status" aria-live="polite">1,000 galaxies · 250 spectacular</div><div id="gv-galaxy-navigation"><button id="gv-back-galaxy" type="button" disabled>Back</button><button id="gv-next-galaxy" type="button" disabled>Next Galaxy</button></div>';
            root.appendChild(panel);
            const nameLabel=panel.querySelector("#gv-random-galaxy-name");
            const backButton=panel.querySelector("#gv-back-galaxy");
            const nextButton=panel.querySelector("#gv-next-galaxy");
            let history=[],historyPosition=-1,navigating=false;

            async function openGalaxy(record){
                if(!record||navigating)return;
                navigating=true;backButton.disabled=true;nextButton.disabled=true;
                try{
                    const ra=Number(record?.ra_deg),dec=Number(record?.dec_deg),fov=fovFor(record);
                    if(Number.isFinite(ra)&&Number.isFinite(dec))aladin.gotoRaDec(ra,dec);
                    else await Promise.resolve(aladin.gotoObject(targetFor(record)));
                    aladin.setFoV(fov);
                    const category=record.spectacular?"Spectacular":(record.source==="CURATED"?"Beautiful":"Discovery");
                    const type=String(record.morphology||"Galaxy").trim();
                    nameLabel.textContent=String(record.primary_name||"Unnamed galaxy").trim()+" · "+category+" · "+type+" · FOV "+fov.toFixed(2)+"°";
                }catch(error){nameLabel.textContent="Could not resolve "+String(record.primary_name||"galaxy");console.error("GV-beta-0005I TARGET FAILURE:",error);}
                finally{navigating=false;backButton.disabled=historyPosition<=0;nextButton.disabled=!(curatedRecords.length||discoveryRecords.length);}
            }
            async function openNextGalaxy(){
                if(navigating)return;
                const current=historyPosition>=0?history[historyPosition]:null;
                const nextRecord=chooseRecord(curatedRecords,discoveryRecords,current,nonSpectacularRun);
                if(!nextRecord)return;
                if(historyPosition<history.length-1)history=history.slice(0,historyPosition+1);
                history.push(nextRecord);historyPosition=history.length-1;
                nonSpectacularRun=nextRecord.spectacular?0:nonSpectacularRun+1;
                await openGalaxy(nextRecord);
            }
            async function openPreviousGalaxy(){if(navigating||historyPosition<=0)return;historyPosition-=1;await openGalaxy(history[historyPosition]);}
            backButton.addEventListener("click",openPreviousGalaxy);
            nextButton.addEventListener("click",openNextGalaxy);
            if(firstRecord){history=[firstRecord];historyPosition=0;nonSpectacularRun=firstRecord.spectacular?0:1;await openGalaxy(firstRecord);}
            else nameLabel.textContent="Galaxy catalogs unavailable";
        }).catch(error=>console.error("GV-beta-0005I STARTUP FAILURE:",error));
    }

    if(window.A&&window.A.init){startGalaxyViewer();return;}
    let loader=document.querySelector('script[data-gv-aladin="3.8.2"]');
    if(loader){
        loader.addEventListener("load",startGalaxyViewer,{once:true});
        loader.addEventListener("error",()=>console.error("GV-beta-0005I STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
        return;
    }
    loader=document.createElement("script");
    loader.src=aladinBundleUrl;loader.charset="utf-8";loader.dataset.gvAladin="3.8.2";
    loader.addEventListener("load",startGalaxyViewer,{once:true});
    loader.addEventListener("error",()=>console.error("GV-beta-0005I STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
    document.head.appendChild(loader);
})();
"""))

# GV-beta-0005I released
