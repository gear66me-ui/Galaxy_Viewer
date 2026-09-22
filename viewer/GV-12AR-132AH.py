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
#gv-center-reticle{position:absolute;left:50%;top:50%;z-index:7301;width:270px;height:270px;transform:translate(-50%,-50%);pointer-events:none;user-select:none;-webkit-user-select:none}
#gv-center-reticle img{display:block;width:32px;height:32px}
body.gv-hd-open #gv-center-target{display:none!important}
#gv-galaxy-nav{visibility:hidden;opacity:0;position:absolute;left:50%;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;gap:5px;width:calc(100vw - 24px);height:36px;transform:translateX(-50%);pointer-events:auto}
#gv-version-label{visibility:hidden;opacity:0;position:absolute;left:50%;bottom:51px;z-index:7400;transform:translateX(-50%);height:10px;color:#9BE5FF;font:400 8px/10px "Space Age",sans-serif;letter-spacing:.85px;text-align:center;text-transform:uppercase;text-shadow:0 0 4px rgba(221,248,255,.28),0 0 7px rgba(88,191,255,.58);white-space:nowrap;pointer-events:none}
#gv-apk-cover{flex-direction:column;gap:18px}#gv-apk-cover .gv-viewer-version{visibility:hidden;opacity:0;color:#58BFFF;background:none!important;-webkit-background-clip:initial;background-clip:initial;-webkit-text-fill-color:#58BFFF;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 4px rgba(221,248,255,.42),0 0 9px rgba(88,191,255,.82);filter:none;white-space:nowrap}
</style>
<div id="aladin-cosmic-command-test"></div>
<script>(()=>{const cover=document.getElementById('gv-apk-cover');if(!cover)return;const img=cover.querySelector('img');if(img)img.src='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg';const version=document.createElement('div');version.className='gv-viewer-version';version.textContent='12AR-106';cover.appendChild(version)})();</script>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='12AR-132AH';
    const DISPLAY_VERSION='12AR-132AH';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0005.js';
    const HAMBURGER_EXTENSION_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/target-simbad/gv-target-simbad-0004.js';
    const RANDOM_GALAXY_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/random-galaxy/gv-random-galaxy-0209.js';
    const NAVIGATION_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/navigation/gv-navigation-0020.js';
    const NAVIGATION_VERSION='0020';
    const RANDOM_GALAXY_VERSION='0209';
    const AVM_LAB_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/lab/gv-avm-overlay-lab-0048.js';
    const NAVIGATION_ADMIN_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-navigation-admin-0001.js';
    const DIAGNOSTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0018.js';
    const gvAvmTraceQueue=[];
    function gvAvmTrace(code,detail={}){
        const payload=Object.freeze({code:String(code||'VIEWER_AVM'),detail});
        try{
            const api=window.GalaxyViewerDiagnostics;
            if(api&&typeof api.recordAvm==='function'){
                while(gvAvmTraceQueue.length){
                    const item=gvAvmTraceQueue.shift();
                    try{api.recordAvm(item.code,item.detail)}catch(_){}
                }
                try{api.recordAvm(payload.code,payload.detail)}catch(_){}
                return;
            }
            gvAvmTraceQueue.push(payload);
            if(gvAvmTraceQueue.length>200)gvAvmTraceQueue.shift();
        }catch(_){}
    }
    const BLACK_BOX_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-black-box-0003.js';
    const DOWNLOAD_SERVICE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-service/gv-download-service-0001.js';
    const DOWNLOAD_ANALYTICS_BASE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0002.js';
    const DOWNLOAD_ANALYTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0003.js';
    const MASTER_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/gv-master-catalog.json';
    const RAW_BETA_ROOT='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
    const RETICLE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-reticle.svg';
    const TARGET_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg';
    const HD_LAYOUT=Object.freeze({bannerRatio:403/1536,imageRatio:630/1536,gap:6,edge:6,iconInset:20});
    const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
    const PREFETCH_TARGET=10;
    const startupTiming={
        startedAt:performance.now(),
        aladinPreloadStartedAt:null,
        aladinPreloadReadyAt:null,
        aladinPreloadFailedAt:null,
        aladinPreloadError:null,
        shellReadyAt:null,
        catalogReadyAt:null,
        randomReadyAt:null,
        firstGalaxyReadyAt:null,
        fullReadyAt:null
    };

    function loadScript(url,datasetKey){
        return new Promise((resolve,reject)=>{
            const loaderKey=String(datasetKey||'').trim();
            if(!loaderKey)return reject(new Error(`SCRIPT LOADER KEY MISSING: ${url}`));

            const requestedUrl=new URL(url,window.location.href).href;
            const existing=[...document.scripts].find(
                script=>
                    script.dataset.gvLoaderKey===loaderKey &&
                    new URL(script.src,window.location.href).href===requestedUrl
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

    function loadScriptGithubThenLocal(url,datasetKey){
        const remoteUrl=String(url||'').trim();

        return loadScript(remoteUrl,datasetKey).catch(remoteError=>{
            let fallbackUrl='';

            try{
                const parsed=new URL(remoteUrl);
                fallbackUrl=
                    window.location.origin+
                    parsed.pathname+
                    parsed.search;
            }catch(_){
                throw remoteError;
            }

            if(
                !fallbackUrl ||
                fallbackUrl===remoteUrl ||
                !/^https?:\/\//i.test(fallbackUrl)
            ){
                throw remoteError;
            }

            console.warn(
                'GALAXY VIEWER REMOTE MODULE LOAD FAILED — TRYING LOCAL VIEWER ROOT',
                remoteUrl,
                fallbackUrl,
                remoteError
            );

            return loadScript(
                fallbackUrl,
                datasetKey+'LocalFallback'
            );
        });
    }

    const moduleLoads=Promise.all([
        loadScript(HAMBURGER_URL,'gvHamburger0005').then(()=>loadScript(HAMBURGER_EXTENSION_URL,'gvHamburger0007')),
        loadScript(COORDINATE_URL,'gvCoordinate0006'),
        loadScript(TARGET_URL,'gvTarget0004'),
        loadScript(NAVIGATION_URL,`gvNavigation${NAVIGATION_VERSION}`),
        loadScript(NAVIGATION_ADMIN_URL,'gvNavigationAdmin0001'),
        loadScriptGithubThenLocal(BLACK_BOX_URL,'gvBlackBox0003').then(()=>loadScript(RANDOM_GALAXY_URL,`gvRandomGalaxy${RANDOM_GALAXY_VERSION}`)),
        (()=>{gvAvmTrace('VIEWER_DIAG0012_LOAD_START',{url:DIAGNOSTICS_URL});return loadScript(DIAGNOSTICS_URL,'gvDiagnostics0012').then(v=>{gvAvmTrace('VIEWER_DIAG0012_LOAD_OK',{version:window.GalaxyViewerDiagnostics?.VERSION||''});return v}).catch(error=>{gvAvmTrace('VIEWER_DIAG0012_LOAD_FAIL',{message:String(error?.message||error||'')});throw error})})(),
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
        return normalizeSignedAngle((match[2].toLowerCase()==='left'?1:-1)*angle);
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
        /*
         * 132J — NO CATALOG ADMISSION FILTER.
         *
         * Every object physically present in the provider catalog is
         * retained. Missing optional astronomy metadata remains null/blank.
         * No provider/category/image-type eligibility rejection is applied.
         */
        const record=
            candidate&&typeof candidate==='object'
                ? candidate
                : {};

        const name=String(
            record.name||
            record.title||
            record.objectName||
            record.displayName||
            record.archiveId||
            record.id||
            ''
        ).trim();

        const ra=Number(record.ra);
        const dec=Number(record.dec);

        const distance=parseDistanceMly(
            record.science?.distanceMly ??
            record.distance ??
            record.distanceMly ??
            record.distance_mly
        );

        const constellation=
            String(record.constellation||'').trim();

        const designation=extractDesignation(record);

        const commonName=String(
            record.displayName||
            record.commonName||
            record.common_name||
            record.title||
            record.name||
            ''
        ).trim();

        const age=String(
            record.science?.ageDisplay ??
            record.age ??
            record.ageEstimate ??
            record.age_estimate ??
            ''
        ).trim();

        const ageGyr=Number(record.science?.ageGyr);
        const directAgeYears=
            Number(record.ageYears??record.age_years);

        const ageYears=
            Number.isFinite(ageGyr)&&ageGyr>0
                ? ageGyr*1_000_000_000
                : Number.isFinite(directAgeYears)&&
                  directAgeYears>0
                    ? directAgeYears
                    : null;

        const scienceSize=
            Array.isArray(record.science?.sizeKly)
                ? record.science.sizeKly
                    .map(value=>Number(value)*1000)
                : null;

        const rawSize=
            scienceSize ??
            record.physicalSizeLy ??
            record.physical_size_ly ??
            null;

        const physicalSizeLy=
            Array.isArray(rawSize)
                ? rawSize
                    .map(Number)
                    .filter(
                        value=>
                            Number.isFinite(value)&&
                            value>0
                    )
                : Number.isFinite(Number(rawSize))&&
                  Number(rawSize)>0
                    ? Number(rawSize)
                    : null;

        const fovDegrees=
            Number(record.fovDegrees);

        const aladinRotation=
            Number(record.aladinRotation);

        const rawSourceUrl=
            String(
                record.sourceUrl||
                record.source_url||
                ''
            ).trim();

        const rawHdUrl=
            chooseCatalogImageUrl(record);

        let hdUrl=rawHdUrl;
        let sourceUrl=rawSourceUrl;

        try{
            if(rawHdUrl)
                hdUrl=new URL(rawHdUrl).href;
        }catch(_){}

        try{
            if(rawSourceUrl)
                sourceUrl=new URL(rawSourceUrl).href;
        }catch(_){}

        const imageType=
            String(
                record.imageType||
                record.image_type||
                ''
            ).trim();

        const category=
            String(
                record.category||
                'Galaxies'
            ).trim()||
            'Galaxies';

        const provider=String(
            record.provider ??
            catalogMeta.provider ??
            catalogKey ??
            ''
        ).trim().toUpperCase();

        const telescope=String(
            record.telescope ??
            record.facility ??
            catalogMeta.telescope ??
            catalogMeta.facility ??
            provider
        ).trim();

        const sourceLabel=String(
            record.source ??
            catalogMeta.source ??
            catalogMeta.title ??
            catalogKey ??
            'GALAXY CATALOG'
        ).trim();

        const credit=String(
            record.credit ??
            catalogMeta.credit ??
            ''
        ).trim();

        return Object.freeze({
            source:sourceLabel,
            provider,
            archiveId:String(
                record.archiveId||
                record.id||
                ''
            ).trim(),
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
            hdUrl,
            sourceUrl,
            fovDegrees,
            aladinRotation,
            credit,
            imageType:imageType||'Observation',
            category,
            telescope,
            githubImageUrl:String(
                record.githubImageUrl||
                record.github_image_url||
                ''
            ).trim(),
            sha256:String(
                record.sha256||
                ''
            ).trim(),
            catalogIndex:index
        });
    }

    function catalogDistanceIdentityKeys(record){
        const raw=[record?.designation,record?.commonName,record?.name];
        const out=[];
        for(const value of raw){
            let key=String(value||'').normalize('NFKD').toUpperCase().replace(/[^A-Z0-9]+/g,'');
            if(/^MESSIER[0-9]+$/.test(key))key='M'+key.slice(7);
            if(!key||key.length<2)continue;
            if(/^(?:GALAXY|NEBULA|STAR|OBJECT|IMAGE|FIELD)$/.test(key))continue;
            if(!out.includes(key))out.push(key);
        }
        return out;
    }
    function medianNumber(values){
        const sorted=[...values].filter(value=>Number.isFinite(value)&&value>0).sort((a,b)=>a-b);
        if(!sorted.length)return null;
        const middle=Math.floor(sorted.length/2);
        return sorted.length%2?sorted[middle]:(sorted[middle-1]+sorted[middle])/2;
    }
    function harmonizeCatalogDistances(records){
        const evidence=new Map();
        for(const record of records){
            const distance=Number(record?.distance);
            if(!(Number.isFinite(distance)&&distance>0))continue;
            for(const key of catalogDistanceIdentityKeys(record)){
                if(!evidence.has(key))evidence.set(key,[]);
                evidence.get(key).push(distance);
            }
        }
        const consensus=new Map();
        for(const [key,values] of evidence){
            const clean=values.filter(value=>Number.isFinite(value)&&value>0);
            if(!clean.length)continue;
            const low=Math.min(...clean),high=Math.max(...clean);
            if(!(low>0)||high/low>1.35)continue;
            const value=medianNumber(clean);
            if(value>0)consensus.set(key,value);
        }
        let filled=0;
        const result=records.map(record=>{
            const current=Number(record?.distance);
            if(Number.isFinite(current)&&current>0)return record;
            const candidates=[...new Set(
                catalogDistanceIdentityKeys(record)
                    .map(key=>consensus.get(key))
                    .filter(value=>Number.isFinite(value)&&value>0)
            )];
            if(!candidates.length)return record;
            const low=Math.min(...candidates),high=Math.max(...candidates);
            if(!(low>0)||high/low>1.35)return record;
            const distance=medianNumber(candidates);
            if(!(distance>0))return record;
            filled++;
            return Object.freeze({...record,distance,distanceEstimated:true,distanceMethod:'catalog-peer-identity-consensus'});
        });
        console.info('GALAXY VIEWER DISTANCE CONTINGENCY',{filled,total:records.length});
        return result;
    }

    async function fetchJsonWithFallback(primaryUrl,label){
        const urls=[String(primaryUrl||'').trim()];
        try{
            const parsed=new URL(primaryUrl);
            if(parsed.hostname==='raw.githubusercontent.com' && parsed.pathname.startsWith('/gear66me-ui/Galaxy_Viewer/beta/')){
                const rel=parsed.pathname.replace('/gear66me-ui/Galaxy_Viewer/beta/','');
                urls.push('https://gear66me-ui.github.io/Galaxy_Viewer/'+rel);
            }
        }catch(_){}

        const uniqueUrls=[...new Set(urls.filter(Boolean))];
        const isMaster=String(label||'').trim()==='MASTER CATALOG';
        const cacheMode=isMaster?'no-cache':'force-cache';
        const timeoutMs=8000;
        let lastError=null;

        for(const url of uniqueUrls){
            const controller=new AbortController();
            const timer=setTimeout(()=>controller.abort(),timeoutMs);
            try{
                const response=await fetch(url,{
                    cache:cacheMode,
                    signal:controller.signal
                });
                if(response.ok)return await response.json();
                lastError=new Error(`${label} RETURNED HTTP ${response.status} FROM ${url}`);
            }catch(error){
                lastError=
                    error?.name==='AbortError'
                        ? new Error(`${label} TIMEOUT AFTER ${timeoutMs}ms FROM ${url}`)
                        : error;
            }finally{
                clearTimeout(timer);
            }
        }

        throw lastError||new Error(`${label} LOAD FAILED`);
    }

    async function loadMasterCatalog(){
        const payload=await fetchJsonWithFallback(MASTER_CATALOG_URL,'MASTER CATALOG');
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

        const payload=await fetchJsonWithFallback(url,`GALAXY CATALOG ${key}`);
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);

        if(!Array.isArray(raw)||!raw.length)
            throw new Error(`GALAXY CATALOG ${key} HAS NO ENTRIES`);

        if(Number.isFinite(declared)&&declared!==raw.length)
            console.warn(
                `GALAXY VIEWER CATALOG ${key} DECLARED COUNT ${declared} DOES NOT MATCH ACTUAL ${raw.length}; USING ACTUAL ENTRIES`
            );

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
            .map(
                (candidate,index)=>
                    normalizeCatalogGalaxy(
                        candidate,
                        index,
                        key,
                        catalogMeta
                    )
            );

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

            // AR123 startup contract: Navigation receives the settled catalog.
            // Do not release startup merely because the first ten entries exist.
            if(settled!==catalogSources.length||startupResolved)return;

            startupResolved=true;

            if(combined.length){
                const harmonized=harmonizeCatalogDistances(combined);
                combined.splice(0,combined.length,...harmonized);
                publishCounts();
                resolveStartup(combined);
            }else rejectStartup(new Error('NO TARGETABLE GALAXY CATALOG COULD BE LOADED'));
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
        const COSMIC_BLUE='#58BFFF';
        const COSMIC_BLUE_SOFT='rgba(88,191,255,.64)';
        const NORTH_RED='#FF3B3B';
        const SIZE=270;
        const CENTER=SIZE/2;
        const RING_RADIUS=125;
        // AR58: pointer TIP touches the outside of the 125 px ring.
        // Triangle is 12 px tall, therefore its center is 6 px outside.
        // Label sits farther outward with a protected visual gap.
        const NORTH_POINTER_RADIUS=RING_RADIUS+6;
        const NORTH_LABEL_RADIUS=RING_RADIUS+27;

        const reticle=document.createElement('div');
        reticle.id='gv-center-reticle';
        reticle.setAttribute('aria-hidden','true');

        // AR54: ONE rigid mechanical compass rotor.  The graduated grid,
        // red North pointer, and Space Age N are children of this SAME rotor.
        // Only this parent receives the live North rotation transform.
        const northRotor=document.createElement('div');
        northRotor.id='gv-north-rotor';
        Object.assign(northRotor.style,{
  position:'absolute',left:'0',top:'0',width:`${SIZE}px`,height:`${SIZE}px`,
  transform:'rotate(0deg)',transformOrigin:`${CENTER}px ${CENTER}px`,
  pointerEvents:'none',willChange:'transform'
        });
        reticle.appendChild(northRotor);

        const northGrid=document.createElement('div');
        northGrid.id='gv-north-grid';
        Object.assign(northGrid.style,{
  position:'absolute',left:'0',top:'0',width:`${SIZE}px`,height:`${SIZE}px`,
  pointerEvents:'none'
        });
        northRotor.appendChild(northGrid);

        const ring=document.createElement('div');
        ring.id='gv-direction-ring';
        Object.assign(ring.style,{
  position:'absolute',
  left:'50%',
  top:'50%',
  width:`${RING_RADIUS*2}px`,
  height:`${RING_RADIUS*2}px`,
  transform:'translate(-50%,-50%)',
  border:`0.7px solid ${COSMIC_BLUE_SOFT}`,
  borderRadius:'50%',
  boxShadow:'0 0 4px rgba(88,191,255,.20), inset 0 0 3px rgba(88,191,255,.08)',
  boxSizing:'border-box'
        });
        northGrid.appendChild(ring);

        try{
            const crosshair=document.createElement('div');
            crosshair.id='gv-cardinal-crosshair';
            Object.assign(crosshair.style,{position:'absolute',inset:'0',pointerEvents:'none'});
            for(const angle of [0,90,180,270]){
                const line=document.createElement('div');
                Object.assign(line.style,{
                    position:'absolute',
                    left:`${CENTER}px`,
                    top:`${CENTER}px`,
                    width:'0.5px',
                    height:'27px',
                    background:'#FF3B3B',
                    boxShadow:'0 0 1px rgba(255,59,59,.22)',
                    transform:`translate(-50%,-100%) rotate(${angle}deg) translateY(-57.5px)`,
                    transformOrigin:'50% 100%'
                });
                crosshair.appendChild(line);
            }
            northGrid.appendChild(crosshair);
        }catch(error){
            console.warn('GALAXY VIEWER CARDINAL CROSSHAIR WARNING',error);
        }

        const centerTarget=document.createElement('img');
        centerTarget.id='gv-center-target';
        centerTarget.src=RETICLE_URL;
        centerTarget.alt='';
        centerTarget.setAttribute('aria-hidden','true');
        Object.assign(centerTarget.style,{
  position:'absolute',left:'50%',top:'50%',
  width:'32px',height:'32px',
  transform:'translate(-50%,-50%)'
        });
        reticle.appendChild(centerTarget);

        for(let angle=0;angle<360;angle+=30){
  const major=angle%90===0;
  const length=major?13:7;
  const radians=angle*Math.PI/180;
  const radius=RING_RADIUS-length/2;
  const tick=document.createElement('div');
  tick.className=major?'gv-reticle-tick gv-reticle-tick-major':'gv-reticle-tick gv-reticle-tick-minor';
  Object.assign(tick.style,{
      position:'absolute',
      left:`${CENTER+Math.sin(radians)*radius}px`,
      top:`${CENTER-Math.cos(radians)*radius}px`,
      width:major?'0.8px':'0.55px',
      height:`${length}px`,
      transform:`translate(-50%,-50%) rotate(${angle}deg)`,
      transformOrigin:'50% 50%',
      background:COSMIC_BLUE,
      boxShadow:major?'0 0 3px rgba(88,191,255,.44)':'0 0 2px rgba(88,191,255,.30)',
      borderRadius:'1px'
  });
  northGrid.appendChild(tick);
        }

        const makeTriangle=id=>{
  const marker=document.createElement('div');
  marker.id=id;
  Object.assign(marker.style,{
      position:'absolute',width:'10px',height:'12px',
      background:COSMIC_BLUE,
      clipPath:'polygon(50% 0,100% 100%,0 100%)',
      filter:'drop-shadow(0 0 3px rgba(88,191,255,.78))',
      display:'none'
  });
  return marker;
        };

        try{
            northGrid.dataset.gvAr70MirrorTicks='1';
            for(const tick of northGrid.querySelectorAll('.gv-reticle-tick-major')){
                tick.style.width='1.35px';
                tick.style.height='16px';
                tick.style.borderRadius='0';
                const match=String(tick.style.transform||'').match(/rotate\(([-0-9.]+)deg\)/);
                const angle=match?Number(match[1]):0;
                const normalized=((angle%360)+360)%360;
                const cardinal=Math.abs(normalized%90)<0.001;
                tick.style.background=cardinal?NORTH_RED:COSMIC_BLUE;
                tick.style.boxShadow=cardinal?'0 0 3px rgba(255,59,59,.70),0 0 6px rgba(255,59,59,.24)':'0 0 3px rgba(70,150,255,.78)';
                tick.dataset.gvAr75CardinalMarker=cardinal?'1':'0';
                const radians=angle*Math.PI/180;
                tick.style.left=`${CENTER+Math.sin(radians)*RING_RADIUS}px`;
                tick.style.top=`${CENTER-Math.cos(radians)*RING_RADIUS}px`;
                tick.style.transform=`translate(-50%,-50%) rotate(${angle}deg)`;
                tick.style.transformOrigin='50% 50%';
            }
        }catch(error){
            console.warn('GALAXY VIEWER MIRROR TICKS WARNING',error);
        }

        const northPointer=makeTriangle('gv-north-pointer');
        northPointer.style.display='block';
        northPointer.style.left=`${CENTER}px`;
        northPointer.style.top=`${CENTER-NORTH_POINTER_RADIUS}px`;
        // Triangle is born pointing upward. At bearing zero the marker sits
        // above the ring and its tip points radially OUTWARD.
        northPointer.style.transform='translate(-50%,-50%) rotate(0deg)';
        northPointer.style.background="#FF3B3B";
        northPointer.style.filter='drop-shadow(0 0 3px rgba(255,59,59,.95)) drop-shadow(0 0 7px rgba(255,59,59,.48))';
        northRotor.appendChild(northPointer);

        const northLabel=document.createElement('div');
        northLabel.id='gv-north-label';
        northLabel.textContent='N';
        Object.assign(northLabel.style,{
  position:'absolute',display:'block',left:`${CENTER}px`,top:`${CENTER-NORTH_LABEL_RADIUS}px`,
  transform:'translate(-50%,-50%) rotate(0deg)',color:'#FF3B3B',
  font:'700 15px/1 Arial,sans-serif',letterSpacing:'0px',
  textShadow:'0 0 3px rgba(221,248,255,.92),0 0 7px rgba(88,191,255,.72)',
  whiteSpace:'nowrap',textAlign:'center'
        });
        northRotor.appendChild(northLabel);

        // Dedicated Earth compass presentation.  This does NOT replace the
        // Random Galaxy Earth-return controller; it mirrors that controller's
        reticle.gvDirectional={
  center:CENTER,
  northRotor,
  northGrid,
  northPointerRadius:NORTH_POINTER_RADIUS,
  northLabelRadius:NORTH_LABEL_RADIUS,
  northPointer,
  northLabel,
  lastNorthBearing:null
        };

        root.appendChild(reticle);
        return reticle;
    }

    function createBottomControls(root){
        const version=document.createElement('div');
        version.id='gv-version-label';
        version.textContent=DISPLAY_VERSION;
        version.setAttribute('aria-label',`GALAXY VIEWER ${DISPLAY_VERSION}`);
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
                const value=aladin.pix2world(canvas.clientWidth/2,canvas.clientHeight/2,'ICRSd');
                const ra=Number(value?.[0]),dec=Number(value?.[1]);
                if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
            }
        }catch(error){console.warn('GALAXY VIEWER PIX2WORLD WARNING',error)}
        return null;
    }

    function readCelestialNorthBearing(aladin,root){
        try{
            // AR62: Aladin live viewport rotation is authoritative.
            // North marker uses the same sign convention as setRotation/getRotation.
            // Normalize to 0..360.
            const liveRotation=Number(aladin.getRotation?.());
            if(Number.isFinite(liveRotation)){
                return ((liveRotation%360)+360)%360;
            }
        }catch(error){
            console.warn('GALAXY VIEWER NORTH ROTATION WARNING',error);
        }
        return 0;
    }

    startupTiming.catalogFetchStartedAt=performance.now();
    console.info('GV STARTUP CATALOG FETCH START',{
        elapsedMs:startupTiming.catalogFetchStartedAt-startupTiming.startedAt
    });
    const galaxyCatalogPromise=loadCombinedGalaxyCatalog();
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('GALAXY VIEWER ROOT MISSING');
    document.dispatchEvent(new CustomEvent('gv-viewer-startup-visible',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:performance.now()-startupTiming.startedAt}}));

    const A=await ensureAladin();
    await A.init;

    const aladin=A.aladin('#aladin-cosmic-command-test',{
        target:`${HOME.ra} ${HOME.dec}`,
        survey:'https://alaskybis.unistra.fr/DSS/DSSColor',
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

    if(typeof aladin.setFrame==='function')aladin.setFrame('ICRSd');
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

    function placeDirectionalElement(element,bearing,radius,rotationOffset=0){
        const state=reticle.gvDirectional;
        if(!state||!element||!Number.isFinite(bearing))return;
        const radians=bearing*Math.PI/180;
        element.style.left=`${state.center+Math.sin(radians)*radius}px`;
        element.style.top=`${state.center-Math.cos(radians)*radius}px`;
        element.style.transform=`translate(-50%,-50%) rotate(${bearing+rotationOffset}deg)`;
        element.style.display='block';
    }

    function setNorthMarker(bearing){
        const state=reticle.gvDirectional;
        if(!state||!state.northRotor||!Number.isFinite(bearing))return;
        const northBearing=((bearing%360)+360)%360;
        state.lastNorthBearing=northBearing;

        // AR54 HARD MECHANICAL LOCK: exactly ONE rotation write.
        // Grid + red pointer + N are children of northRotor, therefore they
        // cannot receive different bearings or drift relative to each other.
        state.northRotor.style.transform=`rotate(${northBearing}deg)`;
        state.northRotor.dataset.northBearing=northBearing.toFixed(3);
        state.northGrid.dataset.northBearing=northBearing.toFixed(3);
        state.northPointer.dataset.northBearing=northBearing.toFixed(3);
        state.northLabel.dataset.northBearing=northBearing.toFixed(3);
        state.northPointer.style.display='block';
        state.northLabel.style.display='block';
    }

    // AR58: presentation instrumentation must never compete with Aladin travel.
    // North is cheap. Earth bearing invokes world2pix repeatedly, so update the
    // complete directional presentation at 10 Hz and skip Earth geometry while
    // navigation owns the viewport.
    const updateDirectionalReticle=()=>{
        const state=reticle.gvDirectional;
        if(!state)return;

        const northBearing=readCelestialNorthBearing(aladin,root);
        if(Number.isFinite(northBearing))setNorthMarker(northBearing);
        else if(Number.isFinite(state.lastNorthBearing))setNorthMarker(state.lastNorthBearing);

    };

    const directionalReticleTimer=setInterval(updateDirectionalReticle,100);
    updateDirectionalReticle();
    window.addEventListener(
        'beforeunload',
        ()=>clearInterval(directionalReticleTimer),
        {once:true}
    );

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

    startupTiming.shellReadyAt=performance.now();
    document.dispatchEvent(new CustomEvent('gv-viewer-shell-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:startupTiming.shellReadyAt-startupTiming.startedAt}}));

    await moduleLoads;

    // HOME / observable-universe presentation is owned by Random Galaxy
    if(
        window.GalaxyRandomGalaxy?.VERSION!==RANDOM_GALAXY_VERSION ||
        typeof window.GalaxyRandomGalaxy.bootstrapHomePresentation!=='function'
    )throw new Error(`RANDOM GALAXY ${RANDOM_GALAXY_VERSION} HOME BOOTSTRAP EXPORT MISSING`);

    if(!document.fonts?.load||!document.fonts?.check)throw new Error('SPACE AGE FONT API UNAVAILABLE — STARTUP TEXT REMAINS HIDDEN');
    await document.fonts.load('400 16px "Space Age"');
    if(!document.fonts.check('400 16px "Space Age"'))throw new Error('SPACE AGE FONT NOT READY — STARTUP TEXT REMAINS HIDDEN');
    bottom.version.style.visibility='visible';bottom.version.style.opacity='1';
    const gvCoverVersion=document.querySelector('#gv-apk-cover .gv-viewer-version');if(gvCoverVersion){gvCoverVersion.style.visibility='visible';gvCoverVersion.style.opacity='1';}

    // ==================== HAMBURGER MENU ====================
    if(window.GalaxyViewerHamburgerMenu?.version!=='0007')throw new Error('HAMBURGER MODULE 0007 EXPORT MISSING');
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

            if(action==='TRAVEL SETTINGS'){
                if(typeof window.GalaxyViewerNavigationAdmin?.open==='function'){
                    window.GalaxyViewerNavigationAdmin.open();
                }else{
                    console.warn('GALAXY VIEWER NAVIGATION ADMIN MODULE UNAVAILABLE');
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
                    aladin.setBaseImageLayer('https://alaskybis.unistra.fr/DSS/DSSColor');
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
        coordinate.setFrame('ICRSd');
        coordinate.update(latestRa,latestDec);
    }
    coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(){
        frame='GAL';
        try{if(typeof aladin.setFrame==='function')aladin.setFrame('ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
        coordinate?.setFrame('ICRSd');
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
    console.info('GV STARTUP CATALOG READY',{
        elapsedMs:startupTiming.catalogReadyAt-startupTiming.startedAt,
        fetchMs:startupTiming.catalogReadyAt-startupTiming.catalogFetchStartedAt,
        eligible:galaxyCatalog.length
    });

    // ==================== NAVIGATION ENGINE ====================
    if(window.GalaxyViewerNavigation?.VERSION!==NAVIGATION_VERSION)
        throw new Error(`NAVIGATION ${NAVIGATION_VERSION} EXPORT MISSING OR VERSION MISMATCH`);
    if(window.GalaxyViewerNavigationAdmin?.VERSION!=='0001')
        throw new Error('NAVIGATION ADMIN 0001 EXPORT MISSING OR VERSION MISMATCH');

    // Navigation 0004 is loaded globally; Random Galaxy 0092 owns the planner instance.

    // ==================== RANDOM NAVIGATION ====================
    if(window.GalaxyRandomGalaxy?.VERSION!==RANDOM_GALAXY_VERSION)throw new Error(`RANDOM GALAXY ${RANDOM_GALAXY_VERSION} EXPORT MISSING OR VERSION MISMATCH`);
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
        onArrival(destination){
            showEarthReturnIndicator(destination);
            syncHdProviderPresentation(destination);
        },
        onError(error){
            hideEarthReturnIndicator();console.error('GALAXY VIEWER RANDOM GALAXY FAILURE',error);
        }
    });
    window.GalaxyViewerRandomGalaxy=randomGalaxy;

    // AR53: move the COMPLETE observable-universe callout upward as one unit.
    // The label, leader, and arrow are descendants of #gv-universe-context,
    // therefore this moves all three together. !important defeats the module's
    // original +8px placement without changing its internal geometry.
    const universeContextPositionStyle=document.createElement('style');
    universeContextPositionStyle.id='gv-universe-context-position-12ar55';
    universeContextPositionStyle.textContent=`
#gv-universe-context{
    bottom:calc(50% + min(25vw,50dvh) + 70px) !important;
}
`;
    document.head.appendChild(universeContextPositionStyle);

    randomNavigationWindow=randomGalaxy.installNavigationWindow({
        futureTarget:10,
        historyTarget:10,
        hotTarget:5,
        keyOf:destination=>destinationKey(destination),
        current:HOME
    });

    // Random Galaxy 0084 is the sole preparation owner.
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

    /*
     * AR122 — EARLY AUTHORITATIVE FUTURE QUEUE.
     * Monte Carlo / Navigation owns destination order. Publish only the
     * minimum startup bridge required by Random Galaxy's future-controller,
     * then install that controller NOW so reconcileFutureQueue() creates the
     * authoritative future destinations before HD prefetch is filled.
     */
    window.GalaxyViewerRandomBootstrap=Object.freeze({
        randomGalaxy,
        randomGalaxyButton:bottom.random,
        historyBackButton:bottom.back,
        historyForwardButton:bottom.forward
    });

    if(
        typeof window.GalaxyRandomGalaxy?.installPrefetchRuntime!=='function' ||
        window.GalaxyRandomGalaxy.installPrefetchRuntime()!==true
    )throw new Error('AR123 RANDOM PREFETCH RUNTIME INSTALL FAILED');

    if(
        typeof window.GalaxyRandomGalaxy?.waitForStartupRoute!=='function'
    )throw new Error('AR123 STARTUP ROUTE WAIT API MISSING');

    // AR123 startup contract:
    // catalog settled -> Monte Carlo initialized -> ordered future queue fed.
    startupTiming.monteCarloStartedAt=performance.now();
    console.info('GV STARTUP MONTE CARLO START',{
        elapsedMs:startupTiming.monteCarloStartedAt-startupTiming.startedAt,
        eligible:galaxyCatalog.length
    });

    await window.GalaxyRandomGalaxy.waitForStartupRoute();

    startupTiming.monteCarloReadyAt=performance.now();
    console.info('GV STARTUP MONTE CARLO READY',{
        elapsedMs:startupTiming.monteCarloReadyAt-startupTiming.startedAt,
        solveMs:startupTiming.monteCarloReadyAt-startupTiming.monteCarloStartedAt
    });

    // The route is authoritative before preparation/download is allowed.
    startupTiming.firstPreparationDispatchAt=performance.now();
    console.info('GV STARTUP PREPARATION DISPATCH',{
        elapsedMs:startupTiming.firstPreparationDispatchAt-startupTiming.startedAt
    });
    preparationEngine.fillPrefetchQueue();


    // The physical Random button may become available immediately because
    // travelToRandom() awaits randomGalaxy.ready internally. Viewer readiness,
    // however, is reported only after Random Galaxy initialization succeeds.
    await randomGalaxy.ready;

    const providerIconPreloadUrls=[
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Chandra/Chandra.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/ESO/ESO.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Euclid/Euclid.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/GALEX/GALEX.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Herschel/Herschel.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/JWST/JWST.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NRAO/NRAO.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NoirLabs/NOIRLab.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NuSTAR/NuSTAR.jpg",
        "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Spitzer/Spitzer.jpg"
    ];
    await Promise.all(providerIconPreloadUrls.map(url=>new Promise(resolve=>{
        const image=new Image();
        image.onload=image.onerror=()=>resolve();
        image.src=url;
    })));

    bottom.nav.style.visibility="visible";bottom.nav.style.opacity="1";
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

    // AR84: removed temporary black-box rotation hotdog exporter.


    gvAvmTrace('VIEWER_AVM0048_LOAD_START',{url:AVM_LAB_URL});
    loadScriptGithubThenLocal(AVM_LAB_URL,'gvAvmOverlayLab0048').then(()=>{
        gvAvmTrace('VIEWER_AVM0048_LOAD_OK',{version:window.GalaxyViewerAvmOverlayLab?.VERSION||''});
        const lab=window.GalaxyViewerAvmOverlayLab;
        if(!lab){gvAvmTrace('VIEWER_AVM0048_EXPORT_MISSING',{});return}
        if(lab.VERSION!=='0048')gvAvmTrace('VIEWER_AVM0048_VERSION_MISMATCH',{version:String(lab.VERSION||'')});
        try{
            gvAvmTrace('VIEWER_AVM0048_INSTALL_START',{version:lab.VERSION});
            lab.install?.({A,aladin,viewerRoot:root,randomGalaxy});
            gvAvmTrace('VIEWER_AVM0048_INSTALL_OK',{version:lab.VERSION});
        }catch(error){
            gvAvmTrace('VIEWER_AVM0048_INSTALL_FAIL',{message:String(error?.message||error||'')});
            throw error;
        }
    }).catch(error=>{gvAvmTrace('VIEWER_AVM0048_LOAD_FAIL',{message:String(error?.message||error||'')});console.error('GV AVM LAB LOAD FAILURE',error)});

    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,startupMetrics}}));
})().catch(error=>{console.error('GALAXY VIEWER STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});
"""))

# Galaxy Viewer active implementation staged