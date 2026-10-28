(()=>{'use strict';
const VERSION='0007';
const ART='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/release/viewer/artwork/';
const CDN_ART='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@c44cb47cf506724cbc034e8afe6ffde85cd7b9a3/viewer/artwork/';
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
AND:'ANDROMEDA',ANT:'ANTLIA',APS:'APUS',AQR:'AQUARIUS',AQL:'AQUILA',ARA:'ARA',ARI:'ARIES',AUR:'AURIGA',BOO:'BOOTES',CAE:'CAELUM',CAM:'CAMELOPARDALIS',CNC:'CANCER',CVN:'CANES_VENATICI',CMA:'CANIS_MAJOR',CMI:'CANIS_MINOR',CAP:'CAPRICORNUS',CAR:'CARINA',CAS:'CASSIOPEIA',CEN:'CENTAURUS',CEP:'CEPHEUS',CET:'CETUS',CHA:'CHAMAELEON',CIR:'CIRCINUS',COL:'COLUMBA',COM:'COMA_BERENICES',CRA:'CORONA_AUSTRALIS',CRB:'CORONA_BOREALIS',CRV:'CORVUS',CRT:'CRATER',CRU:'CRUX',CYG:'CYGNUS',DEL:'DELPHINUS',DOR:'DORADO',DRA:'DRACO',EQU:'EQUULEUS',ERI:'ERIDANUS',FOR:'FORNAX',GEM:'GEMINI',GRU:'GRUS',HER:'HERCULES',HOR:'HOROLOGIUM',HYA:'HYDRA',HYI:'HYDRUS',IND:'INDUS',LAC:'LACERTA',LEO:'LEO',LMI:'LEO_MINOR',LEP:'LEPUS',LIB:'LIBRA',LUP:'LUPUS',LYN:'LYNX',LYR:'LYRA',MEN:'MENSA',MIC:'MICROSCOPIUM',MON:'MONOCEROS',MUS:'MUSCA',NOR:'NORMA',OCT:'OCTANS',OPH:'OPHIUCHUS',ORI:'ORION',PAV:'PAVO',PEG:'PEGASUS',PER:'PERSEUS',PHE:'PHOENIX',PIC:'PICTOR',PSC:'PISCES',PSA:'PISCIS_AUSTRINUS',PUP:'PUPPIS',PYX:'PYXIS',RET:'RETICULUM',SGE:'SAGITTA',SGR:'SAGITTARIUS',SCO:'SCORPIUS',SCL:'SCULPTOR',SCT:'SCUTUM',SER:'SERPENS',SEX:'SEXTANS',TAU:'TAURUS',TEL:'TELESCOPIUM',TRI:'TRIANGULUM',TRA:'TRIANGULUM_AUSTRALIS',TUC:'TUCANA',UMA:'URSA_MAJOR',UMI:'URSA_MINOR',VEL:'VELA',VIR:'VIRGO',VOL:'VOLANS',VUL:'VULPECULA'
});
function constellationSources(name){
  const raw=String(name??'').trim().toUpperCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^A-Z0-9]+/g,'_').replace(/^_+|_+$/g,'');
  if(!raw)return[];
  const k=CONSTELLATION_ALIASES[raw]||raw;
  const p='Constellations%202/'+encodeURIComponent(k)+'.SVG';
  return [CDN_ART+p,PAGES_ART+p,ART+p];
}
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
    },900);
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
function loadImage(img,sources,onReady,onFail){
  const urls=[...new Set((sources||[]).filter(Boolean))];
  const token=(imageRequestTokens.get(img)||0)+1;
  imageRequestTokens.set(img,token);
  const active=()=>imageRequestTokens.get(img)===token;
  img.onload=null;
  img.onerror=null;
  let round=0;
  const next=()=>{
    if(!active())return;
    if(round>=3){onFail?.();return}
    const currentRound=round++;
    // Race the CDN, Pages, and raw GitHub copies together. Serial fallback
    // made one slow host delay an icon even when another copy was available.
    const candidates=urls.map((base,index)=>{
      const sep=base.includes('?')?'&':'?';
      const url=currentRound?base+sep+'gv_art_retry='+(currentRound*urls.length+index+1)+'&t='+Date.now():base;
      return loadSource(url).then(readyUrl=>({readyUrl}));
    });
    Promise.any(candidates).then(({readyUrl})=>{
      if(!active())return;
      let fired=false;
      const ready=()=>{if(!active()||fired)return;fired=true;onReady?.()};
      img.onload=ready;
      img.onerror=()=>{if(active())setTimeout(next,120*round)};
      img.src=readyUrl;
      if(active()&&img.complete&&img.naturalWidth>0)Promise.resolve().then(ready);
    }).catch(()=>{
      if(active())setTimeout(next,120*round);
    });
  };
  next();
}
globalThis.GVProviderArtwork=Object.freeze({VERSION,ART,CDN_ART,PAGES_ART,PROVIDER_ARTWORK,key,path,icon,iconSources,constellationSources,loadImage,cacheDiagnostics:()=>Object.freeze({entries:imageCache.size,limit:IMAGE_CACHE_LIMIT})});
})();
