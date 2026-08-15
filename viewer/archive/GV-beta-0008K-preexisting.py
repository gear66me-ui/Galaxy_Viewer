from IPython.display import HTML, Javascript, display

# GV-beta-0008K
# Derived from exact GV-beta-0008J baseline blob 29655d5a1259bdc5b53c039549d8006b31161d15.
# Authorized 8K changes: Random Galaxy 0008 identity, polished navigation/arrival presentation,
# conservative arrival framing, and one-shot local luminance-region centering with safe catalog fallback.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
@font-face{
    font-family:"Space Age";
    src:url("https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001") format("opentype");
    font-style:normal;font-weight:400;font-display:block;
}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{position:relative!important;width:100%!important;height:100vh!important;height:100svh!important;height:100dvh!important;min-height:100vh!important;min-height:100svh!important;min-height:100dvh!important;overflow:hidden!important;background:#000!important}
#aladin-cosmic-command-test .aladin-logo,
#aladin-cosmic-command-test .aladin-copyright,
#aladin-cosmic-command-test .aladin-fov,
#aladin-cosmic-command-test .aladin-status-bar{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
#aladin-cosmic-command-test [class*="simbadPointer"]{position:absolute!important;left:-10000px!important;top:-10000px!important;width:1px!important;height:1px!important;min-width:1px!important;min-height:1px!important;max-width:1px!important;max-height:1px!important;margin:0!important;padding:0!important;opacity:0!important;visibility:hidden!important;pointer-events:none!important;overflow:hidden!important}
#gv-hamburger-host{position:absolute;inset:0;z-index:7200;pointer-events:none}
#gv-hamburger-host>.gv-hamburger-module-root{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;min-height:0!important;pointer-events:none!important}
#gv-hamburger-host .gv-menu-proxy{pointer-events:auto!important}
#gv-hamburger-host .gv-viewer-menu.gv-open,#gv-hamburger-host .gv-projection-submenu.gv-open{pointer-events:auto!important}
#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}
#gv-target-host{position:absolute;left:342px;top:12px;z-index:7210;width:36px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}
#gv-random-galaxy-host{position:absolute;inset:0;z-index:7300;pointer-events:none}
#gv-center-reticle{position:absolute;left:50%;top:50%;z-index:7050;width:32px;height:32px;transform:translate(-50%,-50%);pointer-events:none;user-select:none;-webkit-user-select:none}
#gv-center-reticle img{display:block;width:32px;height:32px}
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:absolute;right:12px;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;height:36px;margin:0;padding:0 14px;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:#E8FFF0;font:400 12px/1 "Space Age",sans-serif;letter-spacing:.45px;text-transform:uppercase;text-shadow:0 0 4px rgba(229,255,239,.76);box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
#gv-random-galaxy:active{filter:brightness(1.08)}
#gv-version-label{position:absolute;left:12px;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;min-width:36px;height:30px;margin:0;padding:0 8px;border:1px solid #D7F4FF;border-radius:5px;background:rgba(0,0,0,.84);color:#62D8FF;font:400 12px/1 "Space Age",sans-serif;letter-spacing:.2px;text-transform:uppercase;text-shadow:0 0 7px rgba(98,216,255,.65);box-shadow:0 0 9px rgba(98,216,255,.35);pointer-events:none}
#gv-we-are-here{position:absolute;inset:0;z-index:7090;pointer-events:none;transition:opacity .2s ease}
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 20px);bottom:40%;width:1px;min-height:28px;transform:translateX(-50%);background:rgba(120,255,171,.88);box-shadow:0 0 8px rgba(87,255,147,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.75))}
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:61%;transform:translateX(-50%);width:min(260px,76vw);padding:0;border:0;background:transparent;color:#E8FFF0;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(87,255,147,.58);box-shadow:none}
#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:7px;color:#78FFAB;font:400 15px/1.2 "Space Age",sans-serif;letter-spacing:1.35px}
#gv-we-are-here .gv-earth-icon{display:inline-flex;align-items:center;justify-content:center;font:21px/1 system-ui,sans-serif;filter:drop-shadow(0 0 5px rgba(87,255,147,.55))}
#gv-we-are-here .gv-home-sub{margin-top:3px;color:#CFFFE0;font:400 9px/1.3 "Space Age",sans-serif;letter-spacing:1.2px}
#gv-we-are-here .gv-home-hint{margin-top:5px;color:#96CFAA;font:400 8px/1.3 "Space Age",sans-serif;letter-spacing:1px}
#gv-we-are-here.gv-hidden{opacity:0;visibility:hidden}
</style>
<div id="aladin-cosmic-command-test"></div>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='8K';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-hamburger-menu-0002.js?v=28d4acb0b724e2c9ec9764f4f3ce92ee1e3210a5';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0003.js?v=34e599fe4e8d3881105b6491c2d9eda9b5c1c17a';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-target-simbad-0001.js?v=7b877f841f091f214d844bdc8ae2f933530f4592';
    const RANDOM_GALAXY_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-random-galaxy-0008.js?v=aa001831a0e84633b10e528bca1b3d2c5ce551bf';
    const HUBBLE_CATALOG_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/data/gv-hubble-galaxies-0002.json?v=9f886f354f33b91e193c4f9e8f185701bb8fe663';
    const RETICLE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/5274c366f42bb1e764c4b2c4827df0bbba41b4cd/viewer/artwork/GV-reticle-0001.svg?v=fd0f8aa1d5d1f5746e373577c06ae6c81d1f9cc0';
    const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
    const ARRIVAL_OCCUPANCY=Object.freeze({target:0.35,max:0.40,minFov:0.30,scale:2.5,maxFov:8});

    let galaxyCatalog=[];
    let arrivalSerial=0;
    let refinedArrivalView=null;

    function clamp(value,min,max){return Math.max(min,Math.min(max,Number(value)))}

    function validateCatalogGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')throw new Error('HUBBLE CATALOG ENTRY '+index+' IS INVALID');
        const name=String(candidate.name||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec),distance=Number(candidate.distance),fov=Number(candidate.fov);
        const constellation=String(candidate.constellation||'').trim();
        const age=String(candidate.age??candidate.ageEstimate??candidate.age_estimate??'UNKNOWN').trim()||'UNKNOWN';
        const hdUrl=String(candidate.hdUrl||'').trim();
        const sourceUrl=String(candidate.sourceUrl||'').trim();
        const imageType=String(candidate.imageType||'').trim();
        const category=String(candidate.category||'').trim();
        const telescope=String(candidate.telescope||'').trim();
        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)throw new Error('HUBBLE CATALOG ENTRY '+index+' HAS INVALID IDENTITY OR COORDINATES');
        if(!Number.isFinite(distance)||distance<=0||!constellation||!Number.isFinite(fov)||fov<=0)throw new Error('HUBBLE CATALOG ENTRY '+index+' HAS INVALID DISTANCE / CONSTELLATION / FOV');
        let hd,source;
        try{hd=new URL(hdUrl);source=new URL(sourceUrl)}catch(_){throw new Error('HUBBLE CATALOG ENTRY '+index+' HAS INVALID URLS')}
        const approvedHost=host=>host==='esahubble.org'||host.endsWith('.esahubble.org');
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))throw new Error('HUBBLE CATALOG ENTRY '+index+' IS NOT ESA/HUBBLE BACKED');
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))throw new Error('HUBBLE CATALOG ENTRY '+index+' IS NOT AN OBSERVATION');
        if(category&&!/galax/i.test(category))throw new Error('HUBBLE CATALOG ENTRY '+index+' IS NOT A GALAXY');
        if(telescope&&!/hubble/i.test(telescope))throw new Error('HUBBLE CATALOG ENTRY '+index+' IS NOT HUBBLE DATA');
        return Object.freeze({...candidate,name,ra,dec,distance,constellation,age,fov,hdUrl:hd.href,sourceUrl:source.href,imageType:imageType||'Observation',category:category||'Galaxies',telescope:telescope||'Hubble Space Telescope'});
    }

    async function loadGalaxyCatalog(){
        const response=await fetch(HUBBLE_CATALOG_URL,{cache:'no-store'});
        if(!response.ok)throw new Error('HUBBLE CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=Array.isArray(payload)?payload:payload?.galaxies;
        if(!Array.isArray(raw)||raw.length<2)throw new Error('HUBBLE CATALOG REQUIRES AT LEAST TWO GALAXIES');
        return Object.freeze(raw.map(validateCatalogGalaxy));
    }

    function chooseGalaxy(catalog,excludeName=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        const available=catalog.filter(item=>item.name.toLowerCase()!==excluded);
        const pool=available.length?available:catalog;
        return pool[Math.floor(Math.random()*pool.length)];
    }

    function randomHubbleProvider({excludeName}={}){
        return {...chooseGalaxy(galaxyCatalog,excludeName)};
    }

    function loadScript(url,datasetKey){
        return new Promise((resolve,reject)=>{
            const existing=[...document.scripts].find(script=>script.src===url||script.dataset[datasetKey]==='true');
            if(existing){
                if(existing.dataset.gvLoaded==='true'){resolve(existing);return}
                existing.addEventListener('load',()=>resolve(existing),{once:true});
                existing.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
                return;
            }
            const script=document.createElement('script');
            script.src=url;
            script.charset='utf-8';
            script.dataset[datasetKey]='true';
            script.addEventListener('load',()=>{script.dataset.gvLoaded='true';resolve(script)},{once:true});
            script.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
            document.head.appendChild(script);
        });
    }

    async function ensureAladin(){
        if(window.A?.init)return window.A;
        await loadScript(ALADIN_URL,'gvAladin382');
        if(!window.A?.init)throw new Error('ALADIN LITE 3.8.2 EXPORT MISSING');
        return window.A;
    }

    function createHost(root,id){
        let host=root.querySelector('#'+id);
        if(!host){host=document.createElement('div');host.id=id;root.appendChild(host)}
        return host;
    }

    function createCenterReticle(root){
        const reticle=document.createElement('div');
        reticle.id='gv-center-reticle';
        reticle.setAttribute('aria-hidden','true');
        const image=document.createElement('img');
        image.src=RETICLE_URL;
        image.alt='';
        image.width=32;
        image.height=32;
        reticle.appendChild(image);
        root.appendChild(reticle);
        return reticle;
    }

    function createBottomControls(root){
        const version=document.createElement('div');
        version.id='gv-version-label';
        version.textContent=VERSION;
        version.setAttribute('aria-label','GALAXY VIEWER VERSION 8K');
        root.appendChild(version);

        const random=document.createElement('button');
        random.id='gv-random-galaxy';
        random.type='button';
        random.textContent='RANDOM GALAXY';
        random.setAttribute('aria-label','RANDOM GALAXY');
        root.appendChild(random);
        return {version,random};
    }

    function createHomeOverlay(root){
        const overlay=document.createElement('div');
        overlay.id='gv-we-are-here';
        overlay.setAttribute('aria-live','polite');
        overlay.innerHTML='<div class="gv-home-leader" aria-hidden="true"></div><div class="gv-home-label"><div class="gv-home-origin"><span class="gv-earth-icon" aria-hidden="true">🌎</span><strong>WE ARE HERE</strong></div><div class="gv-home-sub">EARTH — MILKY WAY</div><div class="gv-home-hint">TAP RANDOM GALAXY TO BEGIN</div></div>';
        root.appendChild(overlay);
        return overlay;
    }

    function installRandomGalaxyPolish(){
        if(document.getElementById('gv-8k-random-polish'))return;
        const style=document.createElement('style');
        style.id='gv-8k-random-polish';
        style.textContent=`
#gv-random-galaxy-host .gvrg-status{top:68px;width:min(252px,76vw);padding:8px 12px 9px;border:1px solid rgba(131,255,176,.82);border-radius:7px 7px 4px 4px;background:linear-gradient(180deg,rgba(1,22,13,.82),rgba(0,10,7,.70));box-shadow:0 0 11px rgba(65,255,133,.20),inset 0 1px 0 rgba(206,255,224,.08);text-align:left}
#gv-random-galaxy-host .gvrg-status::before{content:"";position:absolute;left:9px;right:9px;top:4px;height:1px;background:linear-gradient(90deg,transparent,#75ffab,transparent);opacity:.65}
#gv-random-galaxy-host .gvrg-status-kicker{font-size:8px;line-height:1.2;letter-spacing:2px;color:#9de4b8}
#gv-random-galaxy-host .gvrg-status-heading{margin-top:4px;font-size:8px;line-height:1.2;letter-spacing:1.35px;color:#9ebbad}
#gv-random-galaxy-host .gvrg-status-destination{margin-top:2px;font-size:16px;line-height:1.13;letter-spacing:.8px;color:#74ffab;text-shadow:0 0 8px rgba(87,255,147,.48)}
#gv-random-galaxy-host .gvrg-distance{top:138px;width:min(252px,76vw);padding:6px 9px 8px;border:1px solid rgba(131,255,176,.58);border-radius:4px 4px 7px 7px;background:linear-gradient(180deg,rgba(0,13,8,.68),rgba(0,7,5,.76));box-shadow:0 0 10px rgba(65,255,133,.12);text-align:left}
#gv-random-galaxy-host .gvrg-distance-label{height:11px;font-size:7px;line-height:11px;letter-spacing:1.7px;color:#79b790}
#gv-random-galaxy-host .gvrg-distance-number{justify-content:flex-start;gap:5px;height:23px}
#gv-random-galaxy-host .gvrg-digit-cell,#gv-random-galaxy-host .gvrg-decimal-cell{height:21px;font-size:17px;line-height:21px;color:#edfff4}
#gv-random-galaxy-host .gvrg-distance-unit{width:120px;height:21px;font-size:7px;line-height:21px;letter-spacing:.55px;color:#a9cfb7}
#gv-random-galaxy-host .gvrg-route{height:12px;font-size:7px;line-height:12px;letter-spacing:.75px;color:#81b995}
#gv-random-galaxy-host .gvrg-progress{height:2px;margin-top:5px;border-radius:0;background:rgba(119,255,169,.12)}
#gv-random-galaxy-host .gvrg-progress-fill{background:#70ffab;box-shadow:0 0 6px rgba(112,255,171,.62)}
#gv-random-galaxy-host .gvrg-card{top:73%;width:min(350px,88vw);padding:18px 14px 13px;border:1px solid rgba(129,213,255,.62);border-radius:8px;background:linear-gradient(155deg,rgba(2,13,24,.94),rgba(0,7,14,.91) 58%,rgba(0,18,20,.90));box-shadow:0 14px 34px rgba(0,0,0,.42),0 0 15px rgba(71,194,255,.16),inset 0 1px 0 rgba(214,244,255,.08);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
#gv-random-galaxy-host .gvrg-card::before{content:"HUBBLE FIELD ACQUIRED";display:block;margin:-5px 0 8px;padding-bottom:7px;border-bottom:1px solid rgba(105,216,255,.24);font:400 7px/1.2 "Space Age",sans-serif;letter-spacing:1.8px;color:#62d8ff;text-shadow:0 0 7px rgba(98,216,255,.34)}
#gv-random-galaxy-host .gvrg-card::after{content:"";position:absolute;left:12px;top:9px;width:18px;height:1px;background:#67e4ff;box-shadow:23px 0 0 rgba(103,228,255,.34)}
#gv-random-galaxy-host .gvrg-name{margin:0 0 10px;font-size:18px;line-height:1.15;letter-spacing:1px;color:#f5fdff;text-shadow:0 0 8px rgba(111,221,255,.38)}
#gv-random-galaxy-host .gvrg-row{grid-template-columns:108px minmax(0,1fr);gap:10px;margin-top:0;padding:6px 0;border-bottom:1px solid rgba(120,195,220,.12)}
#gv-random-galaxy-host .gvrg-label{font-size:7px;line-height:1.25;letter-spacing:1.25px;color:#72a9bf}
#gv-random-galaxy-host .gvrg-value{font-size:11px;line-height:1.25;letter-spacing:.45px;color:#e7f8ff;text-align:right}
#gv-random-galaxy-host .gvrg-card-distance{justify-content:flex-end;gap:5px}
#gv-random-galaxy-host .gvrg-value-number{font-size:14px;line-height:1.2;color:#fff}
#gv-random-galaxy-host .gvrg-value-unit{font-size:8px;line-height:1.2;color:#b9d7e2}
#gv-random-galaxy-host .gvrg-actions{grid-template-columns:minmax(0,1fr) 64px;gap:7px;margin-top:11px}
#gv-random-galaxy-host .gvrg-hd-primary{height:64px;border-color:rgba(112,222,255,.72);background:linear-gradient(145deg,rgba(5,31,48,.96),rgba(5,21,33,.98));font-size:16px;letter-spacing:.9px;box-shadow:inset 0 0 12px rgba(98,216,255,.08),0 0 8px rgba(98,216,255,.12)}
#gv-random-galaxy-host .gvrg-hd-icon-button{border-color:rgba(112,222,255,.72);background:rgba(4,18,29,.96)}
@media(max-width:380px){#gv-random-galaxy-host .gvrg-card{width:min(334px,90vw);padding-left:12px;padding-right:12px}#gv-random-galaxy-host .gvrg-row{grid-template-columns:99px minmax(0,1fr)}#gv-random-galaxy-host .gvrg-status,#gv-random-galaxy-host .gvrg-distance{width:min(240px,74vw)}}`;
        document.head.appendChild(style);
    }

    function equatorialToGalactic(raDeg,decDeg){
        const d=Math.PI/180,ra=raDeg*d,dec=decDeg*d;
        const raNGP=192.85948*d,decNGP=27.12825*d,lOmega=32.93192*d;
        const b=Math.asin(Math.sin(dec)*Math.sin(decNGP)+Math.cos(dec)*Math.cos(decNGP)*Math.cos(ra-raNGP));
        const y=Math.sin(dec)*Math.cos(decNGP)-Math.cos(dec)*Math.sin(decNGP)*Math.cos(ra-raNGP);
        const x=Math.cos(dec)*Math.sin(ra-raNGP);
        let l=(Math.atan2(y,x)+lOmega)/d;
        l=((l%360)+360)%360;
        return [l,b/d];
    }

    function readCurrentRaDec(aladin,root){
        try{
            const value=aladin.getRaDec?.();
            const ra=Number(value?.[0]),dec=Number(value?.[1]);
            if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
        }catch(error){console.warn('GV-8K GETRADEC WARNING',error)}
        try{
            const canvas=root.querySelector('canvas');
            if(canvas&&typeof aladin.pix2world==='function'){
                const value=aladin.pix2world(canvas.clientWidth/2,canvas.clientHeight/2);
                const ra=Number(value?.[0]),dec=Number(value?.[1]);
                if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
            }
        }catch(error){console.warn('GV-8K PIX2WORLD WARNING',error)}
        return null;
    }

    function waitFrames(count=2){
        return new Promise(resolve=>{
            const next=()=>{if(count--<=0){resolve();return}requestAnimationFrame(next)};
            requestAnimationFrame(next);
        });
    }

    function findSkyCanvas(aladin){
        const host=aladin?.aladinDiv;
        if(!host)return null;
        return [...host.querySelectorAll('canvas')]
            .filter(canvas=>canvas.clientWidth>100&&canvas.clientHeight>100)
            .sort((a,b)=>(b.clientWidth*b.clientHeight)-(a.clientWidth*a.clientHeight))[0]||null;
    }

    function analyzeRenderedGalaxy(aladin){
        const canvas=findSkyCanvas(aladin);
        if(!canvas)return null;
        const cw=canvas.clientWidth,ch=canvas.clientHeight;
        if(cw<100||ch<100)return null;
        const sw=96,sh=Math.max(54,Math.min(128,Math.round(sw*ch/cw)));
        const sample=document.createElement('canvas');
        sample.width=sw;sample.height=sh;
        const ctx=sample.getContext('2d',{willReadFrequently:true});
        if(!ctx)return null;
        ctx.drawImage(canvas,0,0,sw,sh);
        const rgba=ctx.getImageData(0,0,sw,sh).data;
        const lum=new Float32Array(sw*sh);
        for(let i=0;i<lum.length;i++){
            const p=i*4;
            lum[i]=0.2126*rgba[p]+0.7152*rgba[p+1]+0.0722*rgba[p+2];
        }
        const smooth=new Float32Array(lum.length);
        for(let y=1;y<sh-1;y++)for(let x=1;x<sw-1;x++){
            let sum=0;
            for(let yy=-1;yy<=1;yy++)for(let xx=-1;xx<=1;xx++)sum+=lum[(y+yy)*sw+x+xx];
            smooth[y*sw+x]=sum/9;
        }
        const margin=Math.max(3,Math.round(Math.min(sw,sh)*.05));
        const values=[];
        for(let y=margin;y<sh-margin;y++)for(let x=margin;x<sw-margin;x++)values.push(smooth[y*sw+x]);
        if(values.length<50)return null;
        values.sort((a,b)=>a-b);
        const mean=values.reduce((a,b)=>a+b,0)/values.length;
        let variance=0;
        for(const value of values){const d=value-mean;variance+=d*d}
        variance/=values.length;
        const p82=values[Math.floor((values.length-1)*.82)];
        const threshold=Math.max(p82,mean+Math.sqrt(variance)*.28);
        const mask=new Uint8Array(sw*sh),seen=new Uint8Array(sw*sh);
        for(let y=margin;y<sh-margin;y++)for(let x=margin;x<sw-margin;x++){
            const i=y*sw+x;
            if(smooth[i]>=threshold)mask[i]=1;
        }
        let best=null;
        const directions=[[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]];
        for(let y=margin;y<sh-margin;y++)for(let x=margin;x<sw-margin;x++){
            const start=y*sw+x;
            if(!mask[start]||seen[start])continue;
            const queue=[start];seen[start]=1;
            let head=0,area=0,weight=0,wx=0,wy=0,minX=x,maxX=x,minY=y,maxY=y;
            while(head<queue.length){
                const i=queue[head++],px=i%sw,py=Math.floor(i/sw);
                const w=Math.max(1,smooth[i]-threshold+1);
                area++;weight+=w;wx+=px*w;wy+=py*w;
                minX=Math.min(minX,px);maxX=Math.max(maxX,px);minY=Math.min(minY,py);maxY=Math.max(maxY,py);
                for(const [dx,dy] of directions){
                    const nx=px+dx,ny=py+dy;
                    if(nx<margin||nx>=sw-margin||ny<margin||ny>=sh-margin)continue;
                    const ni=ny*sw+nx;
                    if(mask[ni]&&!seen[ni]){seen[ni]=1;queue.push(ni)}
                }
            }
            if(area<6||area>values.length*.45)continue;
            const score=weight*Math.sqrt(area);
            if(!best||score>best.score)best={score,area,weight,wx,wy,minX,maxX,minY,maxY};
        }
        if(!best||best.weight<=0)return null;
        const sx=best.wx/best.weight,sy=best.wy/best.weight;
        const x=sx/sw*cw,y=sy/sh*ch;
        const spanPx=Math.max((best.maxX-best.minX+1)/sw*cw,(best.maxY-best.minY+1)/sh*ch);
        return {x,y,spanRatio:spanPx/Math.min(cw,ch),canvasWidth:cw,canvasHeight:ch};
    }

    async function refineArrivalView(destination,aladin,token){
        const baseFov=clamp(Math.max(ARRIVAL_OCCUPANCY.minFov,Number(destination.fov)*ARRIVAL_OCCUPANCY.scale),ARRIVAL_OCCUPANCY.minFov,ARRIVAL_OCCUPANCY.maxFov);
        aladin.gotoRaDec(destination.ra,destination.dec);
        aladin.setFov(baseFov);
        refinedArrivalView={name:destination.name,ra:destination.ra,dec:destination.dec,fov:baseFov};
        await waitFrames(3);
        await new Promise(resolve=>setTimeout(resolve,180));
        if(token!==arrivalSerial)return;
        let analysis=null;
        try{analysis=analyzeRenderedGalaxy(aladin)}catch(error){console.warn('GV-8K ARRIVAL IMAGE ANALYSIS FALLBACK',error)}
        if(token!==arrivalSerial||!analysis)return;
        let finalFov=baseFov;
        if(Number.isFinite(analysis.spanRatio)&&analysis.spanRatio>ARRIVAL_OCCUPANCY.max){
            finalFov=clamp(baseFov*(analysis.spanRatio/ARRIVAL_OCCUPANCY.target),baseFov,ARRIVAL_OCCUPANCY.maxFov);
        }
        let finalRa=destination.ra,finalDec=destination.dec;
        if(typeof aladin.pix2world==='function'){
            try{
                const cx=analysis.canvasWidth/2,cy=analysis.canvasHeight/2;
                const px=cx+clamp(analysis.x-cx,-analysis.canvasWidth*.18,analysis.canvasWidth*.18);
                const py=cy+clamp(analysis.y-cy,-analysis.canvasHeight*.18,analysis.canvasHeight*.18);
                const sky=aladin.pix2world(px,py,'ICRS');
                const ra=Number(sky?.[0]),dec=Number(sky?.[1]);
                if(Number.isFinite(ra)&&Number.isFinite(dec)){finalRa=ra;finalDec=dec}
            }catch(error){console.warn('GV-8K HOTSPOT RECENTER FALLBACK',error)}
        }
        if(token!==arrivalSerial)return;
        aladin.gotoRaDec(finalRa,finalDec);
        aladin.setFov(finalFov);
        refinedArrivalView={name:destination.name,ra:finalRa,dec:finalDec,fov:finalFov};
    }

    function reapplyRefinedArrival(aladin){
        const view=refinedArrivalView;
        if(!view)return;
        aladin.gotoRaDec(view.ra,view.dec);
        aladin.setFov(view.fov);
    }

    galaxyCatalog=await loadGalaxyCatalog();

    const A=await ensureAladin();
    await A.init;
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('GALAXY VIEWER ROOT MISSING');

    const aladin=A.aladin('#aladin-cosmic-command-test',{
        target:`${HOME.ra} ${HOME.dec}`,
        survey:'P/DSS2/color',
        fov:1.5,
        projection:'MOL',
        showReticle:false,
        showZoomControl:false,
        showFullscreenControl:false,
        showLayersControl:false,
        showGotoControl:false,
        showCooGridControl:false,
        showSettingsControl:false,
        showSelectionModeControl:false,
        showColorPickerControl:false,
        showShareControl:false,
        showSimbadPointerControl:true,
        showProjectionControl:false,
        showStatusBar:false,
        showFrame:false,
        showFov:false,
        showCooLocation:false,
        showContextMenu:false,
        showCatalog:false,
        showCooGrid:false
    });
    window.aladin_cosmic_command_test=aladin;

    const hamburgerHost=createHost(root,'gv-hamburger-host');
    const coordinateHost=createHost(root,'gv-coordinate-host');
    const targetHost=createHost(root,'gv-target-host');
    const randomGalaxyHost=createHost(root,'gv-random-galaxy-host');
    const reticle=createCenterReticle(root);
    const bottom=createBottomControls(root);
    const homeOverlay=createHomeOverlay(root);

    await loadScript(HAMBURGER_URL,'gvHamburger0002');
    if(window.GalaxyViewerHamburgerMenu?.version!=='0002')throw new Error('HAMBURGER MODULE 0002 EXPORT MISSING');
    const hamburger=window.GalaxyViewerHamburgerMenu.init({
        host:hamburgerHost,
        onProjectionSelected(name,detail){
            try{
                if(typeof aladin.setProjection!=='function')throw new Error('ALADIN setProjection IS UNAVAILABLE');
                aladin.setProjection(detail.code);
            }catch(error){console.error('GV-8K PROJECTION FAILURE',name,detail?.code,error)}
        }
    });
    hamburger.root.style.position='absolute';
    hamburger.root.style.inset='0';
    hamburger.root.style.width='100%';
    hamburger.root.style.height='100%';
    hamburger.root.style.pointerEvents='none';
    hamburger.menuButton.style.pointerEvents='auto';

    await loadScript(COORDINATE_URL,'gvCoordinate0003');
    if(window.GalaxyCoordinateOverlay?.VERSION!=='0003')throw new Error('COORDINATE MODULE 0003 EXPORT MISSING');
    let frame='ICRSD',latestRa=0,latestDec=0;
    let coordinate=null;
    function renderCoordinates(){
        if(!coordinate)return;
        const shown=frame==='GAL'?equatorialToGalactic(latestRa,latestDec):[latestRa,latestDec];
        coordinate.setFrame(frame);
        coordinate.update(shown[0],shown[1]);
    }
    coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(nextFrame){
        frame=nextFrame;
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GV-8K FRAME CHANGE WARNING',error)}
        renderCoordinates();
    }});
    await coordinate.ready;
    const initialCoordinates=readCurrentRaDec(aladin,root);
    if(initialCoordinates){latestRa=initialCoordinates[0];latestDec=initialCoordinates[1];renderCoordinates()}
    let lastRa=NaN,lastDec=NaN;
    const coordinateTimer=setInterval(()=>{
        const value=readCurrentRaDec(aladin,root);
        if(!value)return;
        const ra=value[0],dec=value[1];
        if(ra===lastRa&&dec===lastDec)return;
        lastRa=ra;lastDec=dec;latestRa=ra;latestDec=dec;renderCoordinates();
    },100);
    window.addEventListener('beforeunload',()=>clearInterval(coordinateTimer),{once:true});

    await loadScript(TARGET_URL,'gvTarget0001');
    if(window.GalaxyViewerTargetSimbad?.version!=='0001')throw new Error('TARGET / SIMBAD MODULE 0001 EXPORT MISSING');
    const target=window.GalaxyViewerTargetSimbad.init({host:targetHost,aladin,viewerRoot:root});

    installRandomGalaxyPolish();
    await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0008');
    if(window.GalaxyRandomGalaxy?.VERSION!=='0008')throw new Error('RANDOM GALAXY MODULE 0008 EXPORT MISSING');
    const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomGalaxyHost,{
        aladin,
        randomButton:bottom.random,
        bindClick:true,
        hubbleProvider:randomHubbleProvider,
        currentGalaxy:HOME,
        catalogCount:galaxyCatalog.length,
        onArrival(destination){
            const token=++arrivalSerial;
            refineArrivalView(destination,aladin,token).catch(error=>console.warn('GV-8K ARRIVAL REFINEMENT FALLBACK',error));
        }
    });
    await randomGalaxy.ready;
    bottom.random.addEventListener('click',()=>{arrivalSerial++;refinedArrivalView=null;homeOverlay.classList.add('gv-hidden')},{once:true});
    bottom.random.addEventListener('click',()=>{arrivalSerial++;refinedArrivalView=null});
    const backButton=[...randomGalaxy.root.querySelectorAll('button')].find(button=>button.textContent.trim()==='BACK TO SKY');
    if(backButton)backButton.addEventListener('click',()=>requestAnimationFrame(()=>reapplyRefinedArrival(aladin)));

    window.GV8K=Object.freeze({version:VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomGalaxyButton:bottom.random,reticle,versionLabel:bottom.version,homeOverlay,catalogCount:galaxyCatalog.length,getRefinedArrivalView:()=>refinedArrivalView?{...refinedArrivalView}:null});
    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,catalogCount:galaxyCatalog.length}}));
})().catch(error=>console.error('GALAXY VIEWER 8K STARTUP FAILURE:',error));
"""))

# GV-beta-0008K staged
