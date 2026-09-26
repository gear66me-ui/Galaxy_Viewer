from IPython.display import HTML, Javascript, display

# GV-beta-0007Q
# Independent coordinate-overlay inspection release based on the verified GV-beta-0007P viewer.
# USER INSTRUCTION: Add the approved coordinate box without restoring the removed native-coordinate machinery.

display(HTML("""
<style>
#aladin-cosmic-command-test .gv-coordinate-target-row{position:absolute!important;left:12px!important;top:12px!important;z-index:7120!important;display:grid!important;visibility:visible!important;opacity:1!important;align-items:center!important;grid-template-columns:36px 290px 36px!important;column-gap:2px!important;width:366px!important;height:36px!important;margin:0!important;padding:0!important;box-sizing:border-box!important;pointer-events:auto!important}
#aladin-cosmic-command-test .gv-coordinate-module-host{position:relative!important;width:290px!important;min-width:290px!important;max-width:290px!important;height:36px!important;min-height:36px!important;max-height:36px!important;margin:0!important;padding:0!important;box-sizing:border-box!important;overflow:visible!important;pointer-events:auto!important}
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-menu-proxy,
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-menu-proxy:hover,
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-menu-proxy:focus,
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-menu-proxy:active,
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-target-proxy,
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-target-proxy:hover,
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-target-proxy:focus,
#aladin-cosmic-command-test .gv-coordinate-target-row button.gv-target-proxy:active{position:relative!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;inset:auto!important;z-index:1!important}
#aladin-cosmic-command-test .gv-target-status{right:12px!important;top:56px!important}
</style>
"""))

display(Javascript(r"""
(async()=>{
    const BASE_URL="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/GV-beta-0007P.py?v=835b651bb2c41aa56bec992426ea822a50695d81";
    const MODULE_URL="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0002.js?v=24c7e3f105bae400d5e16bc15184a15ef6ffa3c2";
    const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
    const waitFor=(test,timeout=20000)=>new Promise((resolve,reject)=>{const deadline=performance.now()+timeout;const check=()=>{let value=null;try{value=test()}catch(_){ }if(value){resolve(value);return}if(performance.now()>=deadline){reject(new Error("GV-BETA-0007Q COMPONENT STARTUP TIMEOUT"));return}setTimeout(check,50)};check()});

    const response=await fetch(BASE_URL,{cache:"no-store"});
    if(!response.ok)throw new Error("GV-BETA-0007P RETURNED HTTP "+response.status);
    const source=await response.text();
    const htmlMatches=[...source.matchAll(/display\(HTML\("""([\s\S]*?)"""\)\)/g)];
    const jsMatches=[...source.matchAll(/display\(Javascript\(r"""([\s\S]*?)"""\)\)/g)];
    if(!htmlMatches.length||!jsMatches.length)throw new Error("GV-BETA-0007Q COULD NOT EXTRACT 7P BASELINE");
    htmlMatches.forEach(match=>document.body.insertAdjacentHTML("beforeend",match[1]));
    jsMatches.forEach(match=>{const script=document.createElement("script");script.textContent=match[1];document.body.appendChild(script)});

    const root=await waitFor(()=>document.getElementById("aladin-cosmic-command-test"));
    const aladin=await waitFor(()=>window.aladin_cosmic_command_test);
    const menu=await waitFor(()=>root.querySelector("button.gv-menu-proxy"));
    const target=await waitFor(()=>root.querySelector("button.gv-target-proxy"));

    let row=root.querySelector(".gv-coordinate-target-row");
    if(!row){row=document.createElement("div");row.className="gv-coordinate-target-row";root.appendChild(row)}
    let host=row.querySelector(".gv-coordinate-module-host");
    if(!host){host=document.createElement("div");host.className="gv-coordinate-module-host"}
    row.append(menu,host,target);

    const versionLabel=root.querySelector("#gv-version-label");
    if(versionLabel)versionLabel.textContent="V-7Q";

    await new Promise((resolve,reject)=>{
        if(window.GalaxyCoordinateOverlay?.VERSION==="0002"){resolve();return}
        const script=document.createElement("script");script.src=MODULE_URL;script.charset="utf-8";script.dataset.gvCoordinateOverlay="0002";
        script.addEventListener("load",resolve,{once:true});script.addEventListener("error",()=>reject(new Error("GV-BETA-0007Q COORDINATE MODULE FAILED TO LOAD")),{once:true});document.head.appendChild(script)
    });
    if(window.GalaxyCoordinateOverlay?.VERSION!=="0002")throw new Error("GV-BETA-0007Q COORDINATE MODULE EXPORT MISSING");

    let frame="ICRSD";
    const overlay=window.GalaxyCoordinateOverlay.mount(host,{onFrameChange(nextFrame){frame=nextFrame;try{if(typeof aladin.setFrame==="function")aladin.setFrame(frame==="GAL"?"galactic":"ICRSd")}catch(error){console.warn("GV-BETA-0007Q FRAME CHANGE WARNING",error)}updateCoordinates()}});
    await overlay.ready;

    function equatorialToGalactic(raDeg,decDeg){
        const d=Math.PI/180,ra=raDeg*d,dec=decDeg*d;
        const raNGP=192.85948*d,decNGP=27.12825*d,lOmega=32.93192*d;
        const b=Math.asin(Math.sin(dec)*Math.sin(decNGP)+Math.cos(dec)*Math.cos(decNGP)*Math.cos(ra-raNGP));
        const y=Math.sin(dec)*Math.cos(decNGP)-Math.cos(dec)*Math.sin(decNGP)*Math.cos(ra-raNGP);
        const x=Math.cos(dec)*Math.sin(ra-raNGP);
        let l=(Math.atan2(y,x)+lOmega)/d;l=((l%360)+360)%360;
        return [l,b/d]
    }
    function currentRaDec(){
        try{const value=aladin.getRaDec?.();if(Array.isArray(value)&&Number.isFinite(Number(value[0]))&&Number.isFinite(Number(value[1])))return [Number(value[0]),Number(value[1])]}
        catch(_){ }
        return null
    }
    function updateCoordinates(){const value=currentRaDec();if(!value)return;const shown=frame==="GAL"?equatorialToGalactic(value[0],value[1]):value;overlay.setFrame(frame);overlay.update(shown[0],shown[1])}
    updateCoordinates();
    const coordinateTimer=setInterval(updateCoordinates,200);
    window.addEventListener("beforeunload",()=>clearInterval(coordinateTimer),{once:true});

    const measurements=overlay.getMeasurements();
    if(!host.shadowRoot||measurements.renderedWidth!==290||measurements.renderedHeight!==36)throw new Error("GV-BETA-0007Q COORDINATE MODULE RUNTIME CONTRACT FAILED");
})().catch(error=>console.error("GV-BETA-0007Q STARTUP FAILURE:",error));
"""))

# GV-beta-0007Q staged