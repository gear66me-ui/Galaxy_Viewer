from IPython.display import HTML, Javascript, display

# GV-beta-0005Y
# Standalone Galaxy Viewer release based only on final GV-beta-0005X.
# Protects the complete central Target artwork while applying a bright cloudy green field only outside the target circle, with the original comet head locked at the exact center.
# Preserves the four-decimal coordinate display, 1,000-record catalog, Spectacular Mode, centered reticle, safe FOV floor, navigation, artwork, compact controls, circular comet orbit, active status pulse, and #B8B1F0 color.

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
    width:68px!important;min-width:68px!important;max-width:68px!important;height:32px!important;
    margin:0 6px 0 0!important;padding:0 19px 0 7px!important;box-sizing:border-box!important;
    border:1px solid #B8B1F0!important;border-radius:6px!important;
    background-color:rgba(0,0,0,.86)!important;color:#D7F3FF!important;
    font:700 12px/1.15 "Roboto Mono",Consolas,monospace!important;
    box-shadow:0 0 10px rgba(184,177,240,.44)!important;pointer-events:auto!important;
}
#aladin-cosmic-command-test .gv-coordinate-target-row>.aladin-location,
#aladin-cosmic-command-test .gv-coordinate-target-row>.aladin-coordinates{
    position:static!important;inset:auto!important;display:flex!important;visibility:visible!important;opacity:1!important;
    align-items:center!important;width:min(38vw,300px)!important;min-width:132px!important;max-width:300px!important;
    height:32px!important;min-height:32px!important;max-height:32px!important;margin:0!important;padding:0 8px!important;
    box-sizing:border-box!important;overflow:hidden!important;border:1px solid #B8B1F0!important;border-radius:6px!important;
    background:rgba(0,0,0,.86)!important;color:#FFD166!important;
    font:700 12px/1.15 "Roboto Mono",Consolas,monospace!important;
    text-shadow:0 0 6px rgba(255,209,102,.42)!important;box-shadow:0 0 10px rgba(184,177,240,.44)!important;
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
    appearance:none!important;-webkit-appearance:none!important;position:relative!important;inset:auto!important;
    display:flex!important;visibility:visible!important;opacity:1!important;align-items:center!important;justify-content:center!important;
    width:32px!important;min-width:32px!important;max-width:32px!important;height:32px!important;min-height:32px!important;max-height:32px!important;
    flex:0 0 32px!important;margin:0 0 0 -1px!important;padding:0!important;box-sizing:border-box!important;overflow:hidden!important;
    background:rgba(0,0,0,.82)!important;border:1px solid #B8B1F0!important;border-radius:6px!important;
    cursor:pointer!important;touch-action:manipulation!important;outline:none!important;box-shadow:0 0 10px rgba(184,177,240,.38)!important;pointer-events:auto!important;
}
#aladin-cosmic-command-test button.gv-target-proxy::before{
    content:"";position:absolute;inset:1px;z-index:0;border-radius:5px;pointer-events:none;opacity:0;
}
#aladin-cosmic-command-test button.gv-target-proxy img{
    position:relative!important;z-index:1!important;display:block!important;width:34px!important;height:34px!important;object-fit:contain!important;
    filter:none!important;pointer-events:none!important;user-select:none!important;-webkit-user-drag:none!important;
}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet{
    position:absolute!important;left:16px!important;top:16px!important;width:0!important;height:0!important;
    animation:gv-target-comet-orbit 2.8s linear infinite!important;pointer-events:none!important;z-index:3!important;
}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i{
    position:absolute!important;left:-2px!important;top:-2px!important;width:4px!important;height:4px!important;border-radius:50%!important;
    background:#62D8FF!important;transform:rotate(var(--gv-angle)) translateY(-13px) scale(var(--gv-scale))!important;
    opacity:var(--gv-opacity)!important;box-shadow:0 0 4px rgba(98,216,255,.85)!important;
}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(1){--gv-angle:0deg;--gv-scale:1;--gv-opacity:1;background:#FFFFFF!important;box-shadow:0 0 3px 1px #FFFFFF,0 0 7px 2px #62D8FF!important}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(2){--gv-angle:-15deg;--gv-scale:.88;--gv-opacity:.84}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(3){--gv-angle:-30deg;--gv-scale:.76;--gv-opacity:.68}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(4){--gv-angle:-45deg;--gv-scale:.64;--gv-opacity:.52}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(5){--gv-angle:-60deg;--gv-scale:.52;--gv-opacity:.38}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(6){--gv-angle:-75deg;--gv-scale:.42;--gv-opacity:.26}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(7){--gv-angle:-90deg;--gv-scale:.32;--gv-opacity:.16}
#aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet i:nth-child(8){--gv-angle:-105deg;--gv-scale:.24;--gv-opacity:.08}
#aladin-cosmic-command-test button.gv-target-proxy[aria-pressed="true"]{
    box-shadow:0 0 10px rgba(184,177,240,.38)!important;
}
#aladin-cosmic-command-test button.gv-target-proxy[aria-pressed="true"]::before{
    opacity:1;
    background:
      radial-gradient(circle at 18% 20%,rgba(218,255,231,.72) 0 2px,rgba(92,255,157,.46) 5px,transparent 11px),
      radial-gradient(circle at 82% 22%,rgba(183,255,210,.64) 0 2px,rgba(50,244,137,.42) 6px,transparent 12px),
      radial-gradient(circle at 20% 82%,rgba(146,255,190,.58) 0 2px,rgba(37,226,126,.42) 7px,transparent 13px),
      radial-gradient(circle at 82% 80%,rgba(199,255,220,.60) 0 2px,rgba(64,249,148,.42) 7px,transparent 13px),
      linear-gradient(145deg,rgba(30,197,110,.97),rgba(65,246,143,.95) 48%,rgba(19,158,88,.98));
    -webkit-mask:radial-gradient(circle at center,transparent 0 10px,#000 10.5px 100%);
    mask:radial-gradient(circle at center,transparent 0 10px,#000 10.5px 100%);
    box-shadow:inset 0 0 8px rgba(164,255,202,.62),inset 0 0 3px rgba(239,255,245,.70);
}
#aladin-cosmic-command-test button.gv-target-proxy[aria-pressed="true"] .gv-target-comet{
    animation:none!important;opacity:1!important;transform:none!important;
}
#aladin-cosmic-command-test button.gv-target-proxy[aria-pressed="true"] .gv-target-comet i{
    opacity:0!important;transform:none!important;
}
#aladin-cosmic-command-test button.gv-target-proxy[aria-pressed="true"] .gv-target-comet i:nth-child(1){
    opacity:1!important;transform:none!important;background:#FFFFFF!important;
    box-shadow:0 0 3px 1px #FFFFFF,0 0 7px 2px #62D8FF!important;
}
@keyframes gv-target-comet-orbit{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes gv-target-status-pulse{
    0%{filter:drop-shadow(0 0 4px rgba(255,255,255,.98)) drop-shadow(0 0 10px rgba(98,216,255,.96))}
    10%{filter:drop-shadow(0 0 2.8px rgba(214,247,255,.76)) drop-shadow(0 0 8px rgba(98,216,255,.82))}
    32%{filter:drop-shadow(0 0 2px rgba(188,239,255,.56)) drop-shadow(0 0 6px rgba(98,216,255,.64))}
    58%{filter:drop-shadow(0 0 1px rgba(172,232,255,.34)) drop-shadow(0 0 3.5px rgba(98,216,255,.38))}
    86%{filter:drop-shadow(0 0 .5px rgba(160,225,255,.18)) drop-shadow(0 0 2px rgba(98,216,255,.22))}
    94%{filter:drop-shadow(0 0 2px rgba(255,255,255,.82)) drop-shadow(0 0 7px rgba(160,236,255,.76))}
    100%{filter:drop-shadow(0 0 5px #fff) drop-shadow(0 0 12px rgba(98,216,255,1))}
}
@media (prefers-reduced-motion:reduce){
    #aladin-cosmic-command-test button.gv-target-proxy .gv-target-comet{animation:none!important;transform:rotate(35deg)!important}
    #aladin-cosmic-command-test .gv-target-status.gv-active{animation:none!important;filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 8px rgba(98,216,255,.9))!important}
}
#aladin-cosmic-command-test .gv-target-status{
    display:none!important;visibility:hidden!important;opacity:0!important;align-items:center!important;justify-content:center!important;
    flex-direction:column!important;width:128px!important;min-width:128px!important;max-width:128px!important;min-height:32px!important;margin-left:4px!important;padding:3px 7px!important;
    box-sizing:border-box!important;border:1px solid #B8B1F0!important;border-radius:6px!important;background:rgba(0,0,0,.88)!important;
    color:#D7F3FF!important;font:700 9px/1.12 "Roboto Mono",Consolas,monospace!important;text-align:center!important;
    box-shadow:0 0 9px rgba(184,177,240,.34)!important;pointer-events:none!important;
}
#aladin-cosmic-command-test .gv-target-status>span{display:block!important;width:100%!important;text-align:center!important}
#aladin-cosmic-command-test .gv-target-status.gv-active{
    display:flex!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;cursor:pointer!important;
    animation:gv-target-status-pulse 3s cubic-bezier(.35,.02,.18,1) infinite!important;will-change:filter;
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
        })) : [];
    }

    async function fetchDiscoveryRecords(){
        const response=await fetch(discoveryCatalogUrl+"?v="+Date.now(),{cache:"no-store"});
        if(!response.ok)throw new Error("Discovery catalog returned HTTP "+response.status);
        const payload=await response.json();
        return Array.isArray(payload.records)?payload.records.filter(record=>record&&record.source==="SIMBAD").map(record=>({...record,spectacular:false})) : [];
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
        if(!window.A||!window.A.init){console.error("GV-beta-0005Y STARTUP FAILURE: window.A was not created");return;}
        window.A.init.then(async() => {
            const A=window.A;
            const root=document.getElementById("aladin-cosmic-command-test");
            let curatedRecords=[],discoveryRecords=[];
            try{[curatedRecords,discoveryRecords]=await Promise.all([fetchCuratedRecords(),fetchDiscoveryRecords()]);}
            catch(error){console.error("GV-beta-0005Y CATALOG FAILURE:",error);}

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
            centerReticle.src=reticleUrl+"?v=5Y-protected-green-001";
            centerReticle.alt="";
            centerReticle.setAttribute("aria-hidden","true");
            root.appendChild(centerReticle);

            function findCoordinateBox(){return root.querySelector(".aladin-location")||root.querySelector(".aladin-coordinates");}
            function formatCoordinateText(raw){
                let count=0;
                return String(raw??"").replace(/[-+]?\d+(?:\.\d+)?/g,token=>{
                    if(count>=2)return token;
                    const value=Number(token);count+=1;
                    return Number.isFinite(value)?value.toFixed(4):token;
                });
            }
            function formatCoordinatesFourDecimals(){
                const coordinateBox=findCoordinateBox();
                if(!coordinateBox)return;
                const input=coordinateBox.matches?.("input")?coordinateBox:coordinateBox.querySelector?.("input");
                if(input){
                    const formatted=formatCoordinateText(input.value);
                    if(formatted!==input.value)input.value=formatted;
                    return;
                }
                const formatted=formatCoordinateText(coordinateBox.textContent);
                if(formatted!==coordinateBox.textContent)coordinateBox.textContent=formatted;
            }
            function findNativeSimbadEngine(){
                const claimed=root.querySelector("button.gv-native-simbad-engine");
                if(claimed)return claimed;
                const direct=root.querySelector("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");
                if(direct)return direct;
                const wrapper=root.querySelector(".aladin-simbadPointer-control,.aladin-simbadPointerControl,[class*='simbadPointer']");
                return wrapper?.matches?.("button.aladin-btn")?wrapper:wrapper?.querySelector?.("button.aladin-btn")||null;
            }
            function getTargetStatus(){
                let status=root.querySelector(".gv-target-status");
                if(status)return status;
                status=document.createElement("div");
                status.className="gv-target-status";
                status.setAttribute("role","button");
                status.setAttribute("tabindex","0");
                status.setAttribute("aria-live","polite");
                status.setAttribute("aria-label","Deactivate Target mode and resume navigation");
                status.setAttribute("title","Tap to exit Target mode and resume navigation");
                status.innerHTML="<span>Tap target/galaxy</span><span>Pan locked</span><span>Tap to exit</span>";
                return status;
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
                proxy.innerHTML=`<img src="${targetIconUrl}?v=5Y-protected-green-001" alt="" aria-hidden="true" draggable="false"><span class="gv-target-comet" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>`;
                proxy.addEventListener("click",event=>{
                    event.preventDefault();event.stopPropagation();
                    const active=proxy.getAttribute("aria-pressed")!=="true";
                    proxy.setAttribute("aria-pressed",active?"true":"false");
                    getTargetStatus().classList.toggle("gv-active",active);
                    if(typeof aladin.useSimbadPointer==="function")aladin.useSimbadPointer(active);
                    else findNativeSimbadEngine()?.click();
                });
                return proxy;
            }
            function bindTargetStatus(proxy,status){
                if(status.dataset.gv5yBound==="true")return;
                status.dataset.gv5yBound="true";
                const deactivate=event=>{
                    event.preventDefault();event.stopPropagation();
                    if(proxy.getAttribute("aria-pressed")==="true")proxy.click();
                };
                status.addEventListener("click",deactivate);
                status.addEventListener("keydown",event=>{
                    if(event.key==="Enter"||event.key===" "||event.key==="Spacebar")deactivate(event);
                });
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
                const status=getTargetStatus();
                if(status.parentElement!==row)row.appendChild(status);
                bindTargetStatus(proxy,status);
                formatCoordinatesFourDecimals();
                return row.children.length>=4;
            }
            [150,350,700,1200,2200].forEach(delay=>setTimeout(buildCoordinateTargetRow,delay));
            const rowObserver=new MutationObserver(()=>buildCoordinateTargetRow());
            rowObserver.observe(root,{childList:true,subtree:true});
            setInterval(formatCoordinatesFourDecimals,120);

            const versionLabel=document.createElement("div");
            versionLabel.id="gv-version-label";
            versionLabel.textContent="Galaxy Viewer 5Y";
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

            function deactivateTarget(){
                const proxy=root.querySelector("button.gv-target-proxy");
                if(proxy?.getAttribute("aria-pressed")==="true")proxy.click();
            }
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
                }catch(error){nameLabel.textContent="Could not resolve "+String(record.primary_name||"galaxy");console.error("GV-beta-0005Y TARGET FAILURE:",error);}
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
            backButton.addEventListener("click",()=>{deactivateTarget();openPreviousGalaxy();});
            nextButton.addEventListener("click",()=>{deactivateTarget();openNextGalaxy();});
            if(firstRecord){history=[firstRecord];historyPosition=0;nonSpectacularRun=firstRecord.spectacular?0:1;await openGalaxy(firstRecord);}
            else nameLabel.textContent="Galaxy catalogs unavailable";
        }).catch(error=>console.error("GV-beta-0005Y STARTUP FAILURE:",error));
    }

    if(window.A&&window.A.init){startGalaxyViewer();return;}
    let loader=document.querySelector('script[data-gv-aladin="3.8.2"]');
    if(loader){
        loader.addEventListener("load",startGalaxyViewer,{once:true});
        loader.addEventListener("error",()=>console.error("GV-beta-0005Y STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
        return;
    }
    loader=document.createElement("script");
    loader.src=aladinBundleUrl;loader.charset="utf-8";loader.dataset.gvAladin="3.8.2";
    loader.addEventListener("load",startGalaxyViewer,{once:true});
    loader.addEventListener("error",()=>console.error("GV-beta-0005Y STARTUP FAILURE: official Aladin 3.8.2 bundle failed to load"),{once:true});
    document.head.appendChild(loader);
})();
"""))

# GV-beta-0005Y released