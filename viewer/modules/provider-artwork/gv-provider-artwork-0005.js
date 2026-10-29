(()=>{'use strict';
const VERSION='0010';
const ART='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/artwork/';
const CDN_ART='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/artwork/';
const PAGES_ART='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/';
const PROVIDER_ARTWORK=Object.freeze({
  HUBBLE:'Hubble/Hubble.jpg',
  JWST:'JWST/JWST.jpeg',
  CHANDRA:'Chandra/Chandra.jpg',
  ESO:'ESO/ESO.jpg',
  NOIRLAB:'NoirLabs/NOIRLab.jpg',
  SPITZER:'Spitzer/Spitzer.jpg',
  EUCLID:'Euclid/Euclid.jpg',
  HERSCHEL:'Herschel/Herschel.jpg',
  GALEX:'GALEX/GALEX.jpg',
  NUSTAR:'NuSTAR/NuSTAR.jpg',
  NRAO:'NRAO/NRAO.jpg'
});
const ALIASES=Object.freeze({
  'HUBBLE SPACE TELESCOPE':'HUBBLE',
  'JAMES WEBB SPACE TELESCOPE':'JWST',
  'CHANDRA X-RAY OBSERVATORY':'CHANDRA',
  'NSF NOIRLAB':'NOIRLAB',
  'SPITZER SPACE TELESCOPE':'SPITZER'
});
function key(provider){
  const raw=String(provider??'').trim().toUpperCase();
  return ALIASES[raw]||raw;
}
function path(provider){
  const k=key(provider);
  return Object.prototype.hasOwnProperty.call(PROVIDER_ARTWORK,k)?PROVIDER_ARTWORK[k]:'';
}
function icon(provider){
  const p=path(provider);
  return p?CDN_ART+p:'';
}
function iconSources(provider){
  const p=path(provider);
  return p?[CDN_ART+p,ART+p,PAGES_ART+p]:[];
}
const CONSTELLATION_ALIASES=Object.freeze({
AND:'ANDROMEDA',ANT:'ANTLIA',APS:'APUS',AQR:'AQUARIUS',AQL:'AQUILA',ARA:'ARA',ARI:'ARIES',AUR:'AURIGA',BOO:'BOOTES',CAE:'CAELUM',CAM:'CAMELOPARDALIS',CNC:'CANCER',CVN:'CANES_VENATICI',CMA:'CANIS_MAJOR',CMI:'CANIS_MINOR',CAP:'CAPRICORNUS',CAR:'CARINA',CAS:'CASSIOPEIA',CEN:'CENTAURUS',CEP:'CEPHEUS',CET:'CETUS',CHA:'CHAMAELEON',CIR:'CIRCINUS',COL:'COLUMBA',COM:'COMA_BERENICES',CRA:'CORONA_AUSTRALIS',CRB:'CORONA_BOREALIS',CRV:'CORVUS',CRT:'CRATER',CRU:'CRUX',CYG:'CYGNUS',DEL:'DELPHINUS',DOR:'DORADO',DRA:'DRACO',EQU:'EQUULEUS',ERI:'ERIDANUS',FOR:'FORNAX',GEM:'GEMINI',GRU:'GRUS',HER:'HERCULES',HOR:'HOROLOGIUM',HYA:'HYDRA',HYI:'HYDRUS',IND:'INDUS',LAC:'LACERTA',LEO:'LEO',LMI:'LEO_MINOR',LEP:'LEPUS',LIB:'LIBRA',LUP:'LUPUS',LYN:'LYNX',LYR:'LYRA',MEN:'MENSA',MIC:'MICROSCOPIUM',MON:'MONOCEROS',MUS:'MUSCA',NOR:'NORMA',OCT:'OCTANS',OPH:'OPHIUCHUS',OPHICUS:'OPHIUCHUS',OPHIUCUS:'OPHIUCHUS',ORI:'ORION',PAV:'PAVO',PEG:'PEGASUS',PER:'PERSEUS',PHE:'PHOENIX',PIC:'PICTOR',PSC:'PISCES',PSA:'PISCIS_AUSTRINUS',PUP:'PUPPIS',PYX:'PYXIS',RET:'RETICULUM',SGE:'SAGITTA',SGR:'SAGITTARIUS',SCO:'SCORPIUS',SCL:'SCULPTOR',SCT:'SCUTUM',SER:'SERPENS',SEX:'SEXTANS',TAU:'TAURUS',TEL:'TELESCOPIUM',TRI:'TRIANGULUM',TRA:'TRIANGULUM_AUSTRALE',TUC:'TUCANA',UMA:'URSA_MAJOR',UMI:'URSA_MINOR',VEL:'VELA',VIR:'VIRGO',VOL:'VOLANS',VUL:'VULPECULA'
});
function constellationSources(name){
  const raw=String(name??'').trim().toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^A-Z0-9]+/g,'_').replace(/^_+|_+$/g,'');
  if(!raw)return[];
  const k=CONSTELLATION_ALIASES[raw]||raw;
  const p='Constellations/'+encodeURIComponent(k)+'.SVG';
  // Raw GitHub first avoids a stale or stalled per-file CDN response; CDN and Pages remain fallbacks.
  return [...new Set([
    'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/artwork/'+p,
    CDN_ART+p,
    'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/'+p
  ])];
}
// Bounded LRU cache for successful and in-flight artwork image probes.
const IMAGE_CACHE_LIMIT=96;
const imageCache=new Map();
function trimImageCache(){while(imageCache.size>IMAGE_CACHE_LIMIT)imageCache.delete(imageCache.keys().next().value)}
function loadSource(url){
  if(imageCache.has(url)){const cached=imageCache.get(url);imageCache.delete(url);imageCache.set(url,cached);return cached;}
  const promise=new Promise((resolve,reject)=>{
    const probe=new Image();
    let settled=false;
    // Bound stalled CDN requests so a dead primary source cannot hold up the
    // constellation fallback chain indefinitely.
    const timeout=setTimeout(()=>{
      if(settled)return;
      settled=true;
      if(imageCache.get(url)===promise)imageCache.delete(url);
      reject(new Error('GV ARTWORK LOAD TIMEOUT '+url));
    },3500);
    probe.onload=()=>{
      if(settled)return;
      settled=true;clearTimeout(timeout);resolve(url);
    };
    probe.onerror=()=>{
      if(settled)return;
      settled=true;clearTimeout(timeout);if(imageCache.get(url)===promise)imageCache.delete(url);
      reject(new Error('GV ARTWORK LOAD FAILED '+url));
    };
    probe.src=url;
    if(probe.complete&&probe.naturalWidth>0){
      settled=true;clearTimeout(timeout);resolve(url);
    }
  });
  imageCache.set(url,promise);trimImageCache();
  return promise;
}
const imageRequestTokens=new WeakMap();
// Promise.any is not available in every Android WebView used by Galaxy Viewer.
function firstSuccessful(promises){
  return new Promise((resolve,reject)=>{
    let pending=promises.length;
    const errors=[];
    if(!pending){reject(new Error('GV ARTWORK HAS NO SOURCES'));return}
    promises.forEach(promise=>Promise.resolve(promise).then(resolve,error=>{
      errors.push(error);
      if(--pending===0)reject(new Error('GV ARTWORK SOURCES ALL FAILED: '+errors.map(e=>String(e?.message||e)).join(' | ')));
    }));
  });
}
function loadImage(img,sources,onReady,onFail){
  const urls=[...new Set((sources||[]).filter(Boolean))];
  const token=(imageRequestTokens.get(img)||0)+1;
  imageRequestTokens.set(img,token);
  const active=()=>imageRequestTokens.get(img)===token;
  let index=0,finished=false,sourceTimer=0;
  img.onload=null;
  img.onerror=null;
  const clearSourceTimer=()=>{if(sourceTimer){clearTimeout(sourceTimer);sourceTimer=0}};
  const finish=(url)=>{
    if(!active()||finished)return;
    finished=true;clearSourceTimer();onReady?.(url);
  };
  const fail=()=>{
    if(!active()||finished)return;
    clearSourceTimer();
    if(index>=urls.length){
      finished=true;
      img.removeAttribute('src');
      console.error('GV ARTWORK ALL SOURCES FAILED',{alt:img.alt||'',sources:urls});
      onFail?.();
      return;
    }
    const url=urls[index++];
    img.onload=()=>finish(url);
    img.onerror=()=>{
      if(!active()||finished)return;
      clearSourceTimer();
      console.warn('GV ARTWORK IMAGE REQUEST FAILED',{alt:img.alt||'',url,remaining:urls.length-index});
      fail();
    };
    // Some Android WebViews leave image requests pending without firing either
    // load or error. Time out each source so the fallback chain always advances.
    sourceTimer=setTimeout(()=>{
      if(!active()||finished)return;
      console.warn('GV ARTWORK IMAGE REQUEST TIMEOUT',{alt:img.alt||'',url,remaining:urls.length-index});
      fail();
    },3500);
    img.src=url;
    if(img.complete&&img.naturalWidth>0)finish(url);
  };
  if(!urls.length){onFail?.();return}
  fail();
}
const CONSTELLATION_NAMES=Object.freeze([...new Set(Object.values(CONSTELLATION_ALIASES))]);
const constellationPreloadJobs=new Map();
function preloadConstellation(name){
  const urls=constellationSources(name);
  if(!urls.length)return Promise.reject(new Error('GV CONSTELLATION NAME MISSING: '+String(name??'')));
  const jobKey=urls[0];
  if(constellationPreloadJobs.has(jobKey))return constellationPreloadJobs.get(jobKey);
  const job=(async()=>{
    const errors=[];
    // One request at a time per icon: use the raw source first, then CDN and Pages. Never fan out three requests for every constellation.
    for(const url of urls){try{return await loadSource(url);}catch(error){errors.push(error);}}
    throw new Error('GV CONSTELLATION ALL SOURCES FAILED '+String(name)+': '+errors.map(e=>String(e?.message||e)).join(' | '));
  })();
  constellationPreloadJobs.set(jobKey,job);
  job.catch(()=>{if(constellationPreloadJobs.get(jobKey)===job)constellationPreloadJobs.delete(jobKey);});
  return job;
}
function preloadConstellations(limit=88){
  const parsed=Number(limit);
  const count=Math.max(0,Math.min(88,Number.isFinite(parsed)?Math.floor(parsed):88));
  const names=CONSTELLATION_NAMES.slice(0,count);
  let cursor=0,loaded=0,failed=0;
  const worker=async()=>{while(cursor<names.length){const name=names[cursor++];try{await preloadConstellation(name);loaded++;}catch(error){failed++;console.warn('GV CONSTELLATION PRELOAD FAILED',{name,error:String(error?.message||error)});}}};
  return Promise.all(Array.from({length:Math.min(4,names.length)},worker)).then(()=>Object.freeze({started:true,queued:names.length,loaded,failed}));
}
function preloadAllConstellations(){return preloadConstellations(88)}
globalThis.GVProviderArtwork=Object.freeze({VERSION,ART,CDN_ART,PAGES_ART,PROVIDER_ARTWORK,key,path,icon,iconSources,constellationSources,loadImage,preloadConstellation,preloadConstellations,preloadAllConstellations,constellationNames:CONSTELLATION_NAMES,cacheDiagnostics:()=>Object.freeze({entries:imageCache.size,limit:IMAGE_CACHE_LIMIT})});
})();
