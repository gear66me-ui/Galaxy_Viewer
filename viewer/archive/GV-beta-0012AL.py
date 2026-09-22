from IPython.display import HTML, Javascript, display

# ECO: https://github.com/gear66me-ui/Galaxy_Viewer/blob/beta/docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md#gv-eco-0012n

display(HTML("""
<link rel="stylesheet" href="https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/src/css/aladin.css" />
<style>
@font-face{
    font-family:"Space Age";
    src:url("https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf") format("opentype");
    font-style:normal;font-weight:400;font-display:block
}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{position:relative!important;width:100%!important;height:100vh!important;height:100svh!important;height:100dvh!important;min-height:100vh!important;min-height:100svh!important;min-height:100dvh!important;overflow:hidden!important;background:#000!important}
#gv-startup-wait{position:absolute;inset:0;z-index:7085;display:flex;align-items:center;justify-content:center;background:#000;pointer-events:none}
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
#gv-target-info-host{position:absolute;inset:0;z-index:7350;width:100%;height:100%;margin:0;padding:0;overflow:hidden;pointer-events:none}
#gv-random-galaxy-host{position:absolute;inset:0;z-index:7300;pointer-events:none}
#gv-center-reticle{position:absolute;left:50%;top:50%;z-index:7050;width:32px;height:32px;transform:translate(-50%,-50%);pointer-events:none;user-select:none;-webkit-user-select:none}
#gv-center-reticle img{display:block;width:32px;height:32px}
#gv-galaxy-nav{position:absolute;left:50%;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;gap:5px;width:calc(100vw - 24px);height:36px;transform:translateX(-50%);pointer-events:auto}
#gv-version-label{position:absolute;left:50%;bottom:51px;z-index:7400;transform:translateX(-50%);height:10px;color:#9BE5FF;font:400 8px/10px "Space Age",sans-serif;letter-spacing:.85px;text-align:center;text-transform:uppercase;text-shadow:0 0 4px rgba(221,248,255,.28),0 0 7px rgba(88,191,255,.58);white-space:nowrap;pointer-events:none}
#gv-apk-cover{flex-direction:column;gap:18px}#gv-apk-cover .gv-viewer-version{color:#58BFFF;background:none!important;-webkit-background-clip:initial;background-clip:initial;-webkit-text-fill-color:#58BFFF;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 4px rgba(221,248,255,.42),0 0 9px rgba(88,191,255,.82);filter:none;white-space:nowrap}
</style>
<div id="aladin-cosmic-command-test"><div id="gv-startup-wait" aria-hidden="true"></div></div>
<script>(()=>{const cover=document.getElementById('gv-apk-cover');if(!cover)return;const img=cover.querySelector('img');if(img)img.src='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg';const version=document.createElement('div');version.className='gv-viewer-version';version.textContent='VERSION 12AL';cover.appendChild(version)})();</script>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='12AL';
    const DISPLAY_VERSION='12AL';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0005.js';
    const HAMBURGER_EXTENSION_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0006.js';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/target-simbad/gv-target-simbad-0004.js';
    const RANDOM_GALAXY_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/random-galaxy/gv-random-galaxy-0066.js';
    const DIAGNOSTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0005.js?v=20213375C52DF374';
    const DOWNLOAD_SERVICE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-service/gv-download-service-0001.js';
    const DOWNLOAD_ANALYTICS_BASE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0002.js';
    const DOWNLOAD_ANALYTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0003.js';
    const MASTER_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/gv-master-catalog.json';
    const RAW_BETA_ROOT='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
    const RETICLE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/runtime/navigation/galaxy-viewer-reticle.svg?v=fd0f8aa1d5d1f5746e373577c06ae6c81d1f9cc0';
    const TARGET_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg';
    const HD_LAYOUT=Object.freeze({bannerRatio:403/1536,imageRatio:630/1536,gap:6,edge:6,iconInset:20});
    const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
    const PREFETCH_TARGET=10;
    const TRAVEL_SECONDS=17.0;
    const FIRST_HOME_TRAVEL_SECONDS=7.5;
    const startupTiming={
        startedAt:performance.now(),
        aladinPreloadStartedAt:null,
        aladinPreloadReadyAt:null,
        aladinPreloadFailedAt:null,
        aladinPreloadError:null,
        shellReadyAt:null,
        catalogReadyAt:null,
        randomReadyAt:null,
        fullReadyAt:null
    };

    function loadScript(url,datasetKey){
        return new Promise((resolve,reject)=>{
            const loaderKey=String(datasetKey||'').trim();
            if(!loaderKey)return reject(new Error(`SCRIPT LOADER KEY MISSING: ${url}`));

            const existing=[...document.scripts].find(
                script=>script.dataset.gvLoaderKey===loaderKey
            );

            if(existing){
                if(existing.dataset.ready==='1')return resolve(existing);
                existing.addEventListener('load',()=>resolve(existing),{once:true});
                existing.addEventListener('error',()=>reject(new Error(`SCRIPT LOAD FAILED: ${url}`)),{once:true});
                return;
            }

            const script=document.createElement('script');
            script.src=url;
            script.async=true;
            script.dataset.gvLoaderKey=loaderKey;

            script.addEventListener('load',()=>{
                script.dataset.ready='1';
                resolve(script);
            },{once:true});

            script.addEventListener('error',()=>{
                reject(new Error(`SCRIPT LOAD FAILED: ${url}`));
            },{once:true});

            document.head.appendChild(script);
        });
    }

    let aladinPreloadPromise=null;

    function startAladinPreload(){
        if(aladinPreloadPromise)return aladinPreloadPromise;

        startupTiming.aladinPreloadStartedAt=performance.now();

        aladinPreloadPromise=(async()=>{
            try{
                if(!window.A?.init){
                    await loadScript(ALADIN_URL,'gvAladin382');
                }

                if(!window.A?.init){
                    throw new Error('GALAXY VIEWER LOCAL ALADIN EXPORT MISSING');
                }

                startupTiming.aladinPreloadReadyAt=performance.now();

                return Object.freeze({
                    ok:true,
                    A:window.A
                });
            }catch(error){
                startupTiming.aladinPreloadFailedAt=performance.now();
                startupTiming.aladinPreloadError=String(error?.message||error);

                return Object.freeze({
                    ok:false,
                    error
                });
            }
        })();

        return aladinPreloadPromise;
    }

    const aladinPreload=startAladinPreload();

    async function ensureAladin(){
        if(window.A?.init)return window.A;

        const outcome=await aladinPreload;

        if(!outcome?.ok){
            throw outcome?.error || new Error('GALAXY VIEWER LOCAL ALADIN PRELOAD FAILED');
        }

        if(!outcome.A?.init){
            throw new Error('GALAXY VIEWER LOCAL ALADIN EXPORT MISSING');
        }

        return outcome.A;
    }

    const moduleLoads=Promise.all([
        loadScript(HAMBURGER_URL,'gvHamburger0005').then(()=>loadScript(HAMBURGER_EXTENSION_URL,'gvHamburger0006')),
        loadScript(COORDINATE_URL,'gvCoordinate0006'),
        loadScript(TARGET_URL,'gvTarget0004'),
        loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0066'),
        loadScript(DIAGNOSTICS_URL,'gvDiagnostics0005'),
        loadScript(DOWNLOAD_SERVICE_URL,'gvDownloadService0001').then(()=>loadScript(DOWNLOAD_ANALYTICS_BASE_URL,'gvDownloadAnalytics0002')).then(()=>loadScript(DOWNLOAD_ANALYTICS_URL,'gvDownloadAnalytics0003'))
    ]);

    let galaxyCatalog=[];
    let catalogRecordCount=0;
    let catalogDatabaseCounts=Object.freeze({databases:Object.freeze({}),total:0,eligibleTotal:0});
    let activeTargetKey='';
    let ensureArchivePreloadQueue=()=>{};
    let suspendArchivePreloads=()=>{};
    let resumeArchivePreloads=()=>{};
    let releaseActiveArchivePreload=()=>{};
    let syncHdProviderPresentation=()=>{};
    let hdArchiveIntegration=null;




    function clamp(value,min,max){return Math.max(min,Math.min(max,Number(value)))}
    function clamp01(value){return clamp(value,0,1)}
    function smootherstep(value){const t=clamp01(value);return t*t*t*(t*(t*6-15)+10)}

    function parseDistanceMly(value){
        if(typeof value==='number'&&Number.isFinite(value)&&value>0)return value;
        const text=String(value??'').trim().toLowerCase().replace(/,/g,'');
        if(!text)return null;
        let match=text.match(/([0-9]+(?:\.[0-9]+)?)\s*(billion|million|thousand)\s+light\s*-?\s*years?/i);
        if(match){
            const number=Number(match[1]);
            if(!Number.isFinite(number)||number<=0)return null;
            if(match[2]==='billion')return number*1000;
            if(match[2]==='million')return number;
            return number/1000;
        }
        match=text.match(/([0-9][0-9\s]*(?:\.[0-9]+)?)\s+light\s*-?\s*years?/i);
        if(!match)return null;
        const lightYears=Number(match[1].replace(/\s+/g,''));
        return Number.isFinite(lightYears)&&lightYears>0?lightYears/1_000_000:null;
    }

    function parseFieldOfViewDegrees(value){
        const text=String(value??'').trim().toLowerCase();
        if(!text)return null;
        const numbers=[...text.matchAll(/[0-9]+(?:\.[0-9]+)?/g)].slice(0,2).map(match=>Number(match[0])).filter(Number.isFinite);
        if(!numbers.length)return null;
        let span=Math.max(...numbers);
        if(/arcsec/.test(text))span/=3600;
        else if(/arcmin/.test(text))span/=60;
        else if(!/(?:degree|\bdeg\b)/.test(text))return null;
        return span>0?span:null;
    }

    function parseArchiveOrientation(value){
        const text=String(value??'').trim();
        if(/^[+-]?[0-9]+([.][0-9]+)?$/.test(text)){const numeric=Number(text);return Number.isFinite(numeric)?normalizeSignedAngle(numeric):null;}
        if(!text)return null;
        const match=text.match(/North\s+is\s+([0-9]+(?:\.[0-9]+)?)\s*°?\s*(right|left)\s+of\s+vertical/i);
        if(!match)return null;
        const angle=Number(match[1]);
        if(!Number.isFinite(angle))return null;
        return normalizeSignedAngle((match[2].toLowerCase()==='left'?-1:1)*angle);
    }

    function extractDesignation(candidate){
        const explicit=String(candidate?.designation||'').trim();
        const texts=[explicit,candidate?.name,candidate?.title,candidate?.displayName,candidate?.imageType,candidate?.category]
            .map(value=>String(value||'').trim()).filter(Boolean);
        const joined=texts.join(' | ');
        if(/stephan(?:'|’)?s\s+quintet/i.test(joined))return 'HCG 92';
        for(const text of texts){
            let match=text.match(/\bHCG\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bHICKSON(?:\s+COMPACT\s+GROUP)?\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bABELL\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `ABELL ${match[1].toUpperCase()}`;
        }
        if(explicit)return explicit.toUpperCase();
        for(const text of texts){
            const match=text.match(/\b(?:M|NGC|IC|UGC|PGC|ARP|ESO)\s*[- ]?\s*\d+[A-Z]?(?:[- ]?\d+)?\b/i);
            if(match)return match[0].replace(/\s+/g,' ').toUpperCase();
        }
        if(/\b(?:galaxy\s+cluster|cluster\s+of\s+galaxies|galaxies\s+cluster)\b/i.test(joined))return 'GALAXY CLUSTER';
        if(/\b(?:compact\s+group|galaxy\s+group|group\s+of\s+galaxies|quintet|quartet|triplet)\b/i.test(joined))return 'GALAXY GROUP';
        if(/\b(?:galaxy\s+pair|pair\s+of\s+galaxies|interacting\s+galaxies)\b/i.test(joined))return 'GALAXY PAIR';
        if(/\b(?:star\s+cluster|stellar\s+cluster)\b/i.test(joined))return 'STAR CLUSTER';
        if(/\b(?:star\s+field|stellar\s+field)\b/i.test(joined))return 'STAR FIELD';
        if(/\bnebula\b/i.test(joined))return 'NEBULA';
        if(/\bstar\b/i.test(joined)&&!/\bgalax/i.test(joined))return 'STAR';
        return 'GALAXY';
    }

    function chooseCatalogImageUrl(candidate){
        const candidates=[
            ...(Array.isArray(candidate?.jpegCandidates)?candidate.jpegCandidates:[]),
            candidate?.selectedImageUrl,
            candidate?.hdUrl,
            candidate?.hd_url
        ].map(value=>String(value||'').trim()).filter(Boolean);
        return candidates.find(url=>/\/screen\//i.test(url))||candidates[0]||'';
    }

    function normalizeCatalogGalaxy(candidate,index,catalogKey,catalogMeta={}){
        if(!candidate||typeof candidate!=='object')return null;

        const name=String(candidate.name||candidate.title||candidate.objectName||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.science?.distanceMly??candidate.distance??candidate.distanceMly??candidate.distance_mly);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.displayName||candidate.commonName||candidate.common_name||candidate.title||candidate.name||'').trim();
        const age=String(candidate.science?.ageDisplay??candidate.age??candidate.ageEstimate??candidate.age_estimate??'').trim();

        const ageGyr=Number(candidate.science?.ageGyr);
        const directAgeYears=Number(candidate.ageYears??candidate.age_years);
        const ageYears=
            Number.isFinite(ageGyr)&&ageGyr>0
                ? ageGyr*1_000_000_000
                : Number.isFinite(directAgeYears)&&directAgeYears>0
                    ? directAgeYears
                    : null;

        const scienceSize=Array.isArray(candidate.science?.sizeKly)
            ? candidate.science.sizeKly.map(value=>Number(value)*1000)
            : null;

        const rawSize=scienceSize??candidate.physicalSizeLy??candidate.physical_size_ly??null;
        const physicalSizeLy=Array.isArray(rawSize)
            ? rawSize.map(Number).filter(value=>Number.isFinite(value)&&value>0)
            : Number.isFinite(Number(rawSize))&&Number(rawSize)>0
                ? Number(rawSize)
                : null;

        const fieldDegrees=parseFieldOfViewDegrees(
            candidate.fieldOfView ??
            candidate.imageFovDegrees ??
            candidate.image_fov_degrees ??
            candidate.fieldOfViewDegrees ??
            candidate.field_of_view_degrees
        );

        const fov=Number.isFinite(fieldDegrees)&&fieldDegrees>0
            ? fieldDegrees
            : Number.isFinite(Number(candidate.fov))&&Number(candidate.fov)>0
                ? Number(candidate.fov)
                : null;

        const sourceUrl=String(candidate.sourceUrl||candidate.source_url||'').trim();
        const hdUrl=chooseCatalogImageUrl(candidate);

        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)return null;
        if(!Number.isFinite(distance)||distance<=0||!constellation)return null;
        if(!Number.isFinite(fov)||fov<=0)return null;

        let hd,source;
        try{
            hd=new URL(hdUrl);
            source=new URL(sourceUrl);
        }catch(_){
            return null;
        }

        if(hd.protocol!=='https:'||source.protocol!=='https:')return null;

        const imageType=String(candidate.imageType||candidate.image_type||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;

        const category=String(candidate.category||'Galaxies').trim()||'Galaxies';
        if(category&&!/galax/i.test(category))return null;

        const orientation=String(candidate.orientation||'').trim();
        const archiveRotation=parseArchiveOrientation(orientation);

        const provider=String(
            candidate.provider ??
            catalogMeta.provider ??
            catalogKey ??
            ''
        ).trim().toUpperCase();

        const telescope=String(
            candidate.telescope ??
            candidate.facility ??
            catalogMeta.telescope ??
            catalogMeta.facility ??
            provider
        ).trim();

        const sourceLabel=String(
            candidate.source ??
            catalogMeta.source ??
            catalogMeta.title ??
            catalogKey ??
            'GALAXY CATALOG'
        ).trim();

        const credit=String(
            candidate.credit ??
            catalogMeta.credit ??
            ''
        ).trim();

        return Object.freeze({
            source:sourceLabel,
            provider,
            archiveId:String(candidate.archiveId||candidate.id||'').trim(),
            name,
            ra,
            dec,
            distance,
            constellation,
            designation,
            commonName,
            age,
            ageYears,
            physicalSizeLy,
            fov,
            imageFovDegrees:Number.isFinite(fieldDegrees)&&fieldDegrees>0?fieldDegrees:null,
            hdUrl:hd.href,
            sourceUrl:source.href,
            orientation,
            aladinRotation:Number.isFinite(archiveRotation)?archiveRotation:null,
            credit,
            imageType:imageType||'Observation',
            category,
            telescope,
            githubImageUrl:String(candidate.githubImageUrl||candidate.github_image_url||'').trim(),
            sha256:String(candidate.sha256||'').trim(),
            catalogIndex:index
        });
    }

    async function loadMasterCatalog(){
        const response=await fetch(MASTER_CATALOG_URL,{cache:'no-store'});
        if(!response.ok)throw new Error('MASTER CATALOG RETURNED HTTP '+response.status);

        const payload=await response.json();
        const catalogs=payload?.catalogs;

        if(!catalogs||typeof catalogs!=='object'||Array.isArray(catalogs))
            throw new Error('MASTER CATALOG POINTER MAP MISSING');

        const sources=Object.entries(catalogs)
            .map(([key,value])=>[
                String(key||'').trim(),
                String(value||'').trim()
            ])
            .filter(([key,value])=>key&&value)
            .map(([key,value])=>Object.freeze({
                key,
                url:new URL(value,RAW_BETA_ROOT).href
            }));

        if(!sources.length)
            throw new Error('MASTER CATALOG CONTAINS NO DATABASE POINTERS');

        return Object.freeze(sources);
    }

    async function loadGalaxyCatalog(catalogSource){
        const key=String(catalogSource?.key||'').trim();
        const url=String(catalogSource?.url||'').trim();

        if(!key||!url)throw new Error('CATALOG SOURCE DESCRIPTOR INVALID');

        const response=await fetch(url,{cache:'no-store'});
        if(!response.ok)
            throw new Error(`GALAXY CATALOG ${key} RETURNED HTTP ${response.status}`);

        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);

        if(!Array.isArray(raw)||!raw.length)
            throw new Error(`GALAXY CATALOG ${key} HAS NO ENTRIES`);

        if(Number.isFinite(declared)&&declared!==raw.length)
            throw new Error(`GALAXY CATALOG ${key} COUNT MISMATCH`);

        const catalogMeta=Object.freeze({
            provider:String(payload?.provider||'').trim(),
            telescope:String(payload?.telescope||'').trim(),
            facility:String(payload?.facility||'').trim(),
            source:String(payload?.source||'').trim(),
            title:String(payload?.title||'').trim(),
            credit:String(payload?.credit||'').trim(),
            version:String(payload?.version||'').trim()
        });

        const eligible=raw
            .map((candidate,index)=>normalizeCatalogGalaxy(candidate,index,key,catalogMeta))
            .filter(Boolean);

        if(!eligible.length)
            throw new Error(`GALAXY CATALOG ${key} HAS NO TARGETABLE GALAXIES`);

        return Object.freeze({
            key,
            rawCount:raw.length,
            eligible:Object.freeze(eligible)
        });
    }

    function shuffledCopy(items){
        const copy=[...items];
        for(let i=copy.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]]}
        return copy;
    }

    async function loadCombinedGalaxyCatalog(){
        const catalogSources=await loadMasterCatalog();
        const combined=[];
        const state=new Map(
            catalogSources.map(source=>[
                source.key,
                {rawCount:0,eligibleCount:0,done:false}
            ])
        );

        let settled=0;
        let startupResolved=false;
        let resolveStartup,rejectStartup;

        const startup=new Promise((resolve,reject)=>{
            resolveStartup=resolve;
            rejectStartup=reject;
        });

        const publishCounts=()=>{
            const databases={};
            let total=0;

            for(const [key,value] of state.entries()){
                databases[key]=Object.freeze({
                    rawCount:value.rawCount,
                    eligibleCount:value.eligibleCount,
                    done:value.done
                });
                total+=value.rawCount;
            }

            catalogRecordCount=combined.length;
            catalogDatabaseCounts=Object.freeze({
                databases:Object.freeze(databases),
                total,
                eligibleTotal:combined.length
            });

            console.info('GALAXY VIEWER CATALOG COUNTS',catalogDatabaseCounts);
        };

        const maybeReleaseStartup=()=>{
            publishCounts();

            if(!startupResolved&&combined.length>=PREFETCH_TARGET){
                startupResolved=true;
                resolveStartup(combined);
                return;
            }

            if(settled===catalogSources.length&&!startupResolved){
                startupResolved=true;
                if(combined.length)resolveStartup(combined);
                else rejectStartup(new Error('NO TARGETABLE GALAXY CATALOG COULD BE LOADED'));
            }
        };

        const attach=source=>{
            loadGalaxyCatalog(source).then(data=>{
                const current=state.get(source.key);
                if(current){
                    current.rawCount=data.rawCount;
                    current.eligibleCount=data.eligible.length;
                    current.done=true;
                }
                combined.push(...data.eligible);
            }).catch(error=>{
                const current=state.get(source.key);
                if(current)current.done=true;
                console.warn(`GALAXY VIEWER CATALOG ${source.key} STARTUP WARNING`,error);
            }).finally(()=>{
                settled++;
                maybeReleaseStartup();
            });
        };

        for(const source of catalogSources)
            attach(source);

        return startup;
    }

    function destinationKey(destination){return String(destination?.archiveId||destination?.name||'').trim().toLowerCase()}















    function normalizeSignedAngle(value){
        let angle=Number(value)||0;
        while(angle>90)angle-=180;
        while(angle<-90)angle+=180;
        return angle;
    }























    // ==================== VIEWER STARTUP / SCRIPT LOADING ====================
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
        version.textContent=`VERSION ${DISPLAY_VERSION}`;
        version.setAttribute('aria-label',`GALAXY VIEWER VERSION ${DISPLAY_VERSION}`);
        root.appendChild(version);

        const nav=document.createElement('div');
        nav.id='gv-galaxy-nav';
        const back=document.createElement('button');
        back.type='button';back.className='gv-galaxy-history gv-galaxy-history-back';back.textContent='';back.setAttribute('aria-label','PREVIOUS GALAXY');back.disabled=true;
        const random=document.createElement('button');
        random.id='gv-random-galaxy';random.type='button';random.innerHTML='<span class="gvrg-random-layout"><span class="gvrg-random-star-wrap gvrg-random-star-wrap-left" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet gvrg-random-comet-left"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span><span class="gvrg-random-label">RANDOM GALAXY</span><span class="gvrg-random-star-wrap gvrg-random-star-wrap-right" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span></span>';random.setAttribute('aria-label','RANDOM GALAXY');
        const forward=document.createElement('button');
        forward.type='button';forward.className='gv-galaxy-history gv-galaxy-history-forward';forward.textContent='';forward.setAttribute('aria-label','NEXT GALAXY');forward.disabled=true;
        nav.append(back,random,forward);root.appendChild(nav);

        const hud=document.createElement('div');
        hud.id='gv-travel-hud';hud.setAttribute('role','status');hud.setAttribute('aria-live','polite');
        hud.innerHTML='<div id="gv-travel-distance"><span id="gv-travel-distance-value"><span id="gv-travel-distance-integer">0</span><span id="gv-travel-distance-decimal">.</span><span id="gv-travel-distance-fraction">00</span></span><span id="gv-travel-distance-unit">MILLION LIGHT-YEARS</span></div><div id="gv-travel-primary"><div id="gv-travel-course">COURSE LOCKED</div><div id="gv-travel-heading">HEADING TO</div><div id="gv-travel-destination"></div></div>';
        root.appendChild(hud);
        return {version,nav,back,random,forward,hud};
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
        }catch(error){console.warn('GALAXY VIEWER GETRADEC WARNING',error)}
        try{
            const canvas=root.querySelector('canvas');
            if(canvas&&typeof aladin.pix2world==='function'){
                const value=aladin.pix2world(canvas.clientWidth/2,canvas.clientHeight/2);
                const ra=Number(value?.[0]),dec=Number(value?.[1]);
                if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
            }
        }catch(error){console.warn('GALAXY VIEWER PIX2WORLD WARNING',error)}
        return null;
    }

    const galaxyCatalogPromise=loadCombinedGalaxyCatalog();
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('GALAXY VIEWER ROOT MISSING');
    const startupWait=document.getElementById('gv-startup-wait');
    document.dispatchEvent(new CustomEvent('gv-viewer-startup-visible',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:performance.now()-startupTiming.startedAt}}));

    const A=await ensureAladin();
    await A.init;

    const aladin=A.aladin('#aladin-cosmic-command-test',{
        target:`${HOME.ra} ${HOME.dec}`,
        survey:'P/DSS2/color',
        fov:360,
        projection:'MOL',
        cooFrame:'ICRSd',
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
    if(typeof aladin.setFrame==='function')aladin.setFrame('galactic');
    if(typeof aladin.setRotation==='function')aladin.setRotation(0);
    if(typeof aladin.gotoRaDec==='function')aladin.gotoRaDec(HOME.ra,HOME.dec);
    if(typeof aladin.setFov==='function')aladin.setFov(360);
    window.aladin_cosmic_command_test=aladin;

    const hamburgerHost=createHost(root,'gv-hamburger-host');
    const coordinateHost=createHost(root,'gv-coordinate-host');
    const targetHost=createHost(root,'gv-target-host');
    const randomGalaxyHost=createHost(root,'gv-random-galaxy-host');
    const reticle=createCenterReticle(root);
    const bottom=createBottomControls(root);

    // Generic Aladin physical field scale.  Random Galaxy supplies the
    // current destination distance, but the ruler belongs to viewer
    // presentation because it follows the live Aladin FOV.
    const skyPhysicalScale=document.createElement('div');
    skyPhysicalScale.id='gv-sky-physical-scale';
    skyPhysicalScale.setAttribute('aria-hidden','true');

    const skyPhysicalScaleLabel=document.createElement('div');
    skyPhysicalScaleLabel.className='gv-sky-scale-label';

    const skyPhysicalScaleLine=document.createElement('div');
    skyPhysicalScaleLine.className='gv-sky-scale-line';

    skyPhysicalScale.append(skyPhysicalScaleLabel,skyPhysicalScaleLine);
    root.appendChild(skyPhysicalScale);

    const skyPhysicalScaleStyle=document.createElement('style');
    skyPhysicalScaleStyle.textContent=
        '#gv-sky-physical-scale{position:absolute;left:50%;z-index:28;transform:translateX(-50%);display:none;flex-direction:column;align-items:center;gap:4px;pointer-events:none;color:#78FFAB;font:400 9px/1.05 "Space Age",sans-serif;letter-spacing:.7px;text-align:center;text-shadow:0 0 3px rgba(229,255,239,.72),0 0 7px rgba(87,255,147,.28);white-space:nowrap}' +
        '#gv-sky-physical-scale .gv-sky-scale-label{font:400 9px/1.05 "Space Age",sans-serif;color:#78FFAB;letter-spacing:.7px;text-shadow:0 0 3px rgba(229,255,239,.72),0 0 7px rgba(87,255,147,.28)}' +
        '#gv-sky-physical-scale .gv-sky-scale-line{position:relative;height:10px;border-top:1px solid #78FFAB;filter:drop-shadow(0 0 2px rgba(120,255,171,.52))}' +
        '#gv-sky-physical-scale .gv-sky-scale-line::before,#gv-sky-physical-scale .gv-sky-scale-line::after{content:"";position:absolute;top:-5px;width:1px;height:9px;background:#78FFAB;box-shadow:0 0 2px rgba(120,255,171,.48)}' +
        '#gv-sky-physical-scale .gv-sky-scale-line::before{left:0}' +
        '#gv-sky-physical-scale .gv-sky-scale-line::after{right:0}';
    document.head.appendChild(skyPhysicalScaleStyle);

    startupWait?.remove();
    startupTiming.shellReadyAt=performance.now();
    document.dispatchEvent(new CustomEvent('gv-viewer-shell-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:startupTiming.shellReadyAt-startupTiming.startedAt}}));

    await moduleLoads;

    // HOME / observable-universe presentation is owned by Random Galaxy
    if(
        window.GalaxyRandomGalaxy?.VERSION!=='0066' ||
        typeof window.GalaxyRandomGalaxy.bootstrapHomePresentation!=='function'
    )throw new Error('RANDOM GALAXY 0066 HOME BOOTSTRAP EXPORT MISSING');

    window.GalaxyRandomGalaxy.bootstrapHomePresentation(root);

    // ==================== HAMBURGER MENU ====================
    if(window.GalaxyViewerHamburgerMenu?.version!=='0006')throw new Error('HAMBURGER MODULE 0006 EXPORT MISSING');
    const hamburger=window.GalaxyViewerHamburgerMenu.init({
        host:hamburgerHost,
        onMenuAction(action){
            if(action==='DIAGNOSTICS'){
                if(typeof window.GalaxyViewerDiagnostics?.open==='function'){
                    window.GalaxyViewerDiagnostics.open();
                }else{
                    console.warn('GALAXY VIEWER DIAGNOSTICS MODULE UNAVAILABLE');
                }
                return;
            }

            if(action==='DOWNLOAD ANALYTICS'){
                if(typeof window.GalaxyViewerDownloadAnalytics?.open==='function'){
                    window.GalaxyViewerDownloadAnalytics.open();
                }else{
                    console.warn('GALAXY VIEWER DOWNLOAD ANALYTICS MODULE UNAVAILABLE');
                }
                return;
            }

            if(action==='RETICLE ON/OFF'){
                reticle.style.display=reticle.style.display==='none'?'':'none';
                return;
            }

            if(action==='SURVEY'){
                try{
                    if(typeof aladin.setBaseImageLayer!=='function'){
                        throw new Error('ALADIN setBaseImageLayer IS UNAVAILABLE');
                    }
                    aladin.setBaseImageLayer('P/DSS2/color');
                }catch(error){
                    console.error('GALAXY VIEWER SURVEY FAILURE',error);
                }
                return;
            }
        },
        onProjectionSelected(name,detail){
            try{
                if(typeof aladin.setProjection!=='function')throw new Error('ALADIN setProjection IS UNAVAILABLE');
                aladin.setProjection(detail.code);
            }catch(error){console.error('GALAXY VIEWER PROJECTION FAILURE',name,detail?.code,error)}
        }
    });
    hamburger.root.style.position='absolute';
    hamburger.root.style.inset='0';
    hamburger.root.style.width='100%';
    hamburger.root.style.height='100%';
    hamburger.root.style.pointerEvents='none';
    hamburger.menuButton.style.pointerEvents='auto';

    // ==================== COORDINATE BOX / NAVIGATION INSTRUMENTS ====================
    if(window.GalaxyCoordinateOverlay?.VERSION!=='0006')throw new Error('COORDINATE MODULE 0006 EXPORT MISSING OR VERSION MISMATCH');
    let frame='GAL',latestRa=HOME.ra,latestDec=HOME.dec;
    let coordinate=null;
    function renderCoordinates(){
        if(!coordinate)return;
        const shown=frame==='GAL'?equatorialToGalactic(latestRa,latestDec):[latestRa,latestDec];
        coordinate.setFrame(frame);
        coordinate.update(shown[0],shown[1]);
    }
    coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(nextFrame){
        frame=nextFrame;
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
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

    // ==================== TARGET / SIMBAD ====================
    if(window.GalaxyViewerTargetSimbad?.version!=='0004')throw new Error('TARGET / SIMBAD MODULE 0004 EXPORT MISSING');
    const target=await window.GalaxyViewerTargetSimbad.init({host:targetHost,aladin});

    galaxyCatalog=await galaxyCatalogPromise;
    startupTiming.catalogReadyAt=performance.now();

    // ==================== RANDOM NAVIGATION ====================
    if(window.GalaxyRandomGalaxy?.VERSION!=='0066')throw new Error('RANDOM GALAXY 0066 EXPORT MISSING OR VERSION MISMATCH');
    let randomNavigationWindow=null;

    let earthReturnApi=Object.freeze({
        hide(){},
        show(_destination){}
    });

    const hideEarthReturnIndicator=()=>earthReturnApi.hide();
    const showEarthReturnIndicator=destination=>earthReturnApi.show(destination);

    let skyPhysicalScaleValue=null;
    let skyPhysicalScaleFrame=0;
    let skyPhysicalScaleLastUpdate=0;

    const formatPhysicalScale=valueLy=>{
        const ly=Number(valueLy);
        if(!Number.isFinite(ly)||ly<=0)return '';

        let divisor=1000,unit='KLY';
        if(ly>=1_000_000_000){divisor=1_000_000_000;unit='BLY'}
        else if(ly>=1_000_000){divisor=1_000_000;unit='MLY'}

        const value=ly/divisor;
        let digits;
        if(value>=100)digits=Math.round(value).toString();
        else if(value>=10)digits=(Math.round(value*10)/10).toString();
        else if(value>=1)digits=(Math.round(value*10)/10).toString();
        else if(value>=0.1)digits=(Math.round(value*100)/100).toString();
        else digits=(Math.round(value*1000)/1000).toString();

        return `${digits} ${unit}`;
    };

    const choosePhysicalScaleValue=(lyPerPx,usableWidth)=>{
        const targetFraction=.40;
        const targetLy=Number(lyPerPx)*Number(usableWidth)*targetFraction;
        if(!(targetLy>0))return null;

        const exponent=Math.floor(Math.log10(targetLy));
        const candidates=[];
        for(let e=exponent-2;e<=exponent+2;e++)
            for(const m of [1,2,5])
                candidates.push(m*Math.pow(10,e));

        const scored=candidates.map(value=>{
            const fraction=(value/lyPerPx)/usableWidth;
            const inBand=fraction>=.30&&fraction<=.50;
            return {
                value,
                score:Math.abs(fraction-targetFraction)+(inBand?0:10)
            };
        }).sort((a,b)=>a.score-b.score);

        return scored.length?scored[0].value:null;
    };

    const hideSkyPhysicalScale=()=>{
        skyPhysicalScale.style.display='none';
        skyPhysicalScale.setAttribute('aria-hidden','true');
        skyPhysicalScaleValue=null;
    };

    const updateSkyPhysicalScale=now=>{
        skyPhysicalScaleFrame=requestAnimationFrame(updateSkyPhysicalScale);

        // Ten updates per second is plenty for a scale ruler and prevents
        // unnecessary layout churn while Aladin is animating.
        if(Number(now)-skyPhysicalScaleLastUpdate<100)return;
        skyPhysicalScaleLastUpdate=Number(now);

        if(window.GalaxyRandomGalaxy?.isNavigationPending?.()){
            hideSkyPhysicalScale();
            return;
        }

        const state=randomNavigationWindow?.getState?.()||{};
        const destination=state.current||null;
        const distanceMly=Number(destination?.distance);

        const card=document.querySelector('#gv-random-galaxy .gvrg-card');
        const cardVisible=Boolean(card?.classList?.contains('gvrg-card-visible'));
        if(!cardVisible||!Number.isFinite(distanceMly)||distanceMly<=0){
            hideSkyPhysicalScale();
            return;
        }

        const rootRect=root.getBoundingClientRect();
        const cardRect=card.getBoundingClientRect();
        const usableWidth=Math.min(680,Math.max(40,rootRect.width-20));

        let fovDegrees=NaN;
        try{
            const fov=aladin.getFov?.();
            fovDegrees=Number(Array.isArray(fov)?fov[0]:fov);
        }catch(_){}

        if(!Number.isFinite(fovDegrees)||fovDegrees<=0){
            hideSkyPhysicalScale();
            return;
        }

        // Approximate transverse physical width of the live Aladin field.
        // Arrival/normal galaxy views are well inside the useful range;
        // clamp only pathological ultra-wide manual zoom-outs.
        const boundedFov=Math.min(170,Math.max(.000001,fovDegrees));
        const angleRadians=boundedFov*Math.PI/180;
        const distanceLy=distanceMly*1_000_000;
        const physicalViewportLy=2*distanceLy*Math.tan(angleRadians/2);

        if(!Number.isFinite(physicalViewportLy)||physicalViewportLy<=0){
            hideSkyPhysicalScale();
            return;
        }

        const lyPerPx=physicalViewportLy/usableWidth;
        if(!Number.isFinite(lyPerPx)||lyPerPx<=0){
            hideSkyPhysicalScale();
            return;
        }

        let widthPx=skyPhysicalScaleValue>0
            ? skyPhysicalScaleValue/lyPerPx
            : 0;
        let fraction=widthPx/usableWidth;

        // Wider hysteresis than the normal target band prevents rapid
        // label switching near a pinch-zoom threshold.
        if(!(skyPhysicalScaleValue>0)||fraction<.27||fraction>.53){
            skyPhysicalScaleValue=choosePhysicalScaleValue(lyPerPx,usableWidth);
            widthPx=skyPhysicalScaleValue>0
                ? skyPhysicalScaleValue/lyPerPx
                : 0;
        }

        if(!(skyPhysicalScaleValue>0)||!(widthPx>0)){
            hideSkyPhysicalScale();
            return;
        }

        // Hard 50% ruler maximum regardless of transient zoom geometry.
        const hardMaxPx=usableWidth*.50;
        skyPhysicalScaleLine.style.width=
            `${Math.max(4,Math.min(hardMaxPx,widthPx))}px`;

        skyPhysicalScaleLabel.textContent=
            formatPhysicalScale(skyPhysicalScaleValue);

        if(!skyPhysicalScaleLabel.textContent){
            hideSkyPhysicalScale();
            return;
        }

        skyPhysicalScale.style.display='flex';
        skyPhysicalScale.setAttribute('aria-hidden','false');

        // Entire ruler sits above the Random Galaxy / View-HD card.
        const bottomGap=Math.max(6,rootRect.bottom-cardRect.top+6);
        skyPhysicalScale.style.bottom=`${bottomGap}px`;
    };

    skyPhysicalScaleFrame=requestAnimationFrame(updateSkyPhysicalScale);


    let preparationEngine=null;

    const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomGalaxyHost,{
        aladin,
        viewerRoot:root,
        earthReturnOptions:Object.freeze({
            home:HOME,
            hamburgerHost,
            coordinateHost,
            targetHost,
            nav:bottom.nav,
            skyPhysicalScale,
            isNavigationPending:()=>Boolean(window.GalaxyRandomGalaxy?.isNavigationPending?.())
        }),
        randomButton:bottom.random,
        bindClick:false,
        prefetch:false,
        provider:null,
        currentGalaxy:HOME,
        catalogCount:catalogRecordCount,
        getCatalogCount:()=>catalogRecordCount,
        travelSeconds:TRAVEL_SECONDS,
        firstHomeTravelSeconds:FIRST_HOME_TRAVEL_SECONDS,
        maxFov:237.6,
        turnPoint:0.4705882353,
        onArrival(destination){
            showEarthReturnIndicator(destination);
            syncHdProviderPresentation(destination);
        },
        onError(error){
            hideEarthReturnIndicator();console.error('GALAXY VIEWER RANDOM GALAXY FAILURE',error);
        }
    });
    window.GalaxyViewerRandomGalaxy=randomGalaxy;

    randomNavigationWindow=randomGalaxy.installNavigationWindow({
        futureTarget:10,
        historyTarget:10,
        hotTarget:5,
        keyOf:destination=>destinationKey(destination),
        current:HOME
    });

    // Random Galaxy 0066 is the sole preparation owner.
    // Galaxy Viewer supplies only generic host infrastructure.
    preparationEngine=randomGalaxy.installPreparationEngine({
        aladinUrl:ALADIN_URL,
        home:HOME,
        galaxyCatalog,
        aladin,
        A,
        ensureArchivePreloadQueue:
            ()=>hdArchiveIntegration?.ensureArchivePreloadQueue?.(),
        releaseActiveArchivePreload:
            ()=>hdArchiveIntegration?.releaseActiveArchivePreload?.()
    });

    randomGalaxy.provider=
        preparationEngine.randomGalaxyProvider;

    earthReturnApi=Object.freeze({
        hide:()=>randomGalaxy.hideEarthReturn(),
        show:destination=>randomGalaxy.showEarthReturn(destination)
    });


    hdArchiveIntegration=randomGalaxy.installHdArchiveIntegration({
        bottom,
        targetIconUrl:TARGET_ICON_URL,
        hdLayout:HD_LAYOUT,
        getPrefetchReady:()=>preparationEngine.getPrefetchReady(),
        isBackgroundWorkSuspended:()=>preparationEngine.getBackgroundWorkSuspended(),
        isNavigationPending:()=>Boolean(window.GalaxyRandomGalaxy?.isNavigationPending?.()),
        getActiveTargetKey:()=>preparationEngine.getActiveTargetKey(),
        onHideEarthReturn:()=>hideEarthReturnIndicator()
    });

    ensureArchivePreloadQueue=
        ()=>hdArchiveIntegration.ensureArchivePreloadQueue();

    suspendArchivePreloads=
        ()=>hdArchiveIntegration.suspendArchivePreloads();

    resumeArchivePreloads=
        ()=>hdArchiveIntegration.resumeArchivePreloads();

    releaseActiveArchivePreload=
        ()=>hdArchiveIntegration.releaseActiveArchivePreload();

    syncHdProviderPresentation=
        destination=>hdArchiveIntegration.syncHdProviderPresentation(destination);

    // The physical Random button may become available immediately because
    // travelToRandom() awaits randomGalaxy.ready internally.  Viewer readiness,
    // however, is reported only after Random Galaxy initialization succeeds.
    preparationEngine.fillPrefetchQueue();
    await randomGalaxy.ready;
    startupTiming.randomReadyAt=performance.now();


    window.addEventListener('beforeunload',()=>{
        try{preparationEngine?.destroy?.()}catch(_){}
        try{hdArchiveIntegration?.destroy?.()}catch(_){}
    },{once:true});
    startupTiming.fullReadyAt=performance.now();
    const aladinPreloadEndAt=
        startupTiming.aladinPreloadReadyAt ??
        startupTiming.aladinPreloadFailedAt;

    const aladinPreloadMs=
        Number.isFinite(startupTiming.aladinPreloadStartedAt) &&
        Number.isFinite(aladinPreloadEndAt)
            ? aladinPreloadEndAt-startupTiming.aladinPreloadStartedAt
            : null;

    const startupMetrics=Object.freeze({
        ...startupTiming,
        aladinPreloadMs,
        shellMs:startupTiming.shellReadyAt-startupTiming.startedAt,
        catalogMs:startupTiming.catalogReadyAt-startupTiming.startedAt,
        randomMs:startupTiming.randomReadyAt-startupTiming.startedAt,
        fullMs:startupTiming.fullReadyAt-startupTiming.startedAt
    });
    window.GalaxyViewerCore=Object.freeze({
        version:VERSION,
        displayVersion:DISPLAY_VERSION,
        aladin,
        hamburger,
        coordinate,
        target,
        randomGalaxy,
        randomNavigationWindow,
        randomGalaxyButton:bottom.random,
        historyBackButton:bottom.back,
        historyForwardButton:bottom.forward,
        reticle,
        versionLabel:bottom.version,
        get catalogCount(){return catalogRecordCount},
        get eligibleCatalogCount(){return galaxyCatalog.length},
        get catalogDatabaseCounts(){return catalogDatabaseCounts},
        startupMetrics,

        getGalaxyCatalog:()=>Object.freeze([...galaxyCatalog]),

        getRandomNavigationState:
            ()=>preparationEngine.getRandomNavigationState(),

        getPrefetchState:
            ()=>preparationEngine.getPrefetchState(),

        getDownloadStatus:
            ()=>preparationEngine.getDownloadStatus(),

        getAladinPrewarmState:
            ()=>preparationEngine.getAladinPrewarmState(),

        fillPrefetchQueue:
            ()=>preparationEngine.fillPrefetchQueue(),

        activateQueuedDestination:
            (destination,excludeName='')=>
                preparationEngine.activateQueuedDestination(destination,excludeName),

        requestHdPrefetch:
            destination=>preparationEngine.requestHdPrefetch(destination),

        getHdPreparedResource:
            key=>preparationEngine.getHdPreparedResource(key),

        isHdPrepared:
            key=>preparationEngine.isHdPrepared(key),

        getAladinPreparedReceipt:
            key=>preparationEngine.getAladinPreparedReceipt(key),

        isAladinPrepared:
            key=>preparationEngine.isAladinPrepared(key),

        ensureAladinPreparedForNavigation:
            destination=>preparationEngine.ensureAladinPreparedForNavigation(destination),

        getBackgroundWorkSuspended:
            ()=>preparationEngine.getBackgroundWorkSuspended(),

        suspendBackgroundWork:
            ()=>preparationEngine.suspendBackgroundWork(),

        resumeBackgroundWork:
            ()=>preparationEngine.resumeBackgroundWork(),

        suspendArchivePreloads:
            ()=>hdArchiveIntegration?.suspendArchivePreloads?.(),

        resumeArchivePreloads:
            ()=>hdArchiveIntegration?.resumeArchivePreloads?.()
    });
    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,startupMetrics}}));
})().catch(error=>{console.error('GALAXY VIEWER STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});
"""))

# Galaxy Viewer active implementation staged
