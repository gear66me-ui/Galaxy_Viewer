(function(global){
'use strict';
const VERSION='0001';
const REV='d85d91201ea52aa6524a62394fc81b450b15ac23';
const ROOT='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@'+REV+'/viewer/artwork/Fonts/';
const FACES=Object.freeze({
  coordinateFrame:{family:'GV Space Age 0003',url:ROOT+'Space%20Age%20Regular/Space%20Age%20Regular.otf',fallbackUrl:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/'+REV+'/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf',size:12.5,sample:'ICRSD'},
  coordinateDigits:{family:'GV Coordinate Digits 0003',url:ROOT+'Space%20Age%20Regular%20GV-9/GV-Coordinate-Digits-0005.otf',fallbackUrl:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/'+REV+'/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/GV-Coordinate-Digits-0005.otf',size:20,sample:'359.9999 -90.0000'},
  destination:{family:'GV Destination Space Age',url:ROOT+'Space%20Age%20Regular/Space%20Age%20Regular.otf',fallbackUrl:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/'+REV+'/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf',size:10,sample:'DESIGNATION DISTANCE'},
  travel:{family:'Space Age',url:ROOT+'Space%20Age%20Regular/Space%20Age%20Regular.otf',fallbackUrl:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/'+REV+'/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf',size:16,sample:'HEADING TO'},
  navigator:{family:'GV Space Age',url:ROOT+'Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf',fallbackUrl:'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/'+REV+'/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf',size:15.5,sample:'RANDOM GALAXY'}
});
const jobs=new Map(),loaded=new Map();
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function loadFace(key){
 const spec=FACES[key];
 if(!spec)throw new Error('GV FONT FACE UNKNOWN: '+key);
 if(loaded.has(key))return loaded.get(key);
 if(jobs.has(key))return jobs.get(key);
 const job=(async()=>{
  let lastError=null;
  for(let attempt=1;attempt<=4;attempt++){
   const candidates=[spec.url,spec.fallbackUrl].filter(Boolean);
   const sourceUrl=candidates[(attempt-1)%candidates.length];
   try{
    const face=new FontFace(spec.family,'url("'+sourceUrl+'")',{style:'normal',weight:'400'});
    const result=await face.load();
    if(result.status!=='loaded')throw new Error('FontFace status='+result.status);
    document.fonts.add(result);
    await document.fonts.load('400 '+spec.size+'px "'+spec.family+'"',spec.sample);
    await document.fonts.ready;
    if(result.status!=='loaded'||!document.fonts.check('400 '+spec.size+'px "'+spec.family+'"',spec.sample)){
      document.fonts.delete(result);
      throw new Error('document.fonts verification failed');
    }
    loaded.set(key,result);
    console.info('GV FONT READY',{key,family:spec.family,url:spec.url,attempt,status:result.status});
    return result;
   }catch(error){
    lastError=error;
    console.warn('GV FONT LOAD RETRY',{key,attempt,sourceUrl,error:String(error?.message||error)});
    if(attempt<4)await delay(250*attempt);
   }
  }
  throw new Error('GV FONT FAILED AFTER 4 ATTEMPTS ['+key+'] across primary CDN and raw GitHub fallback: '+String(lastError?.message||lastError));
 })().catch(error=>{jobs.delete(key);throw error});
 jobs.set(key,job);
 try{return await job}finally{if(jobs.get(key)===job)jobs.delete(key)}
}
const GROUPS=Object.freeze({
 coordinate:Object.freeze(['coordinateFrame','coordinateDigits']),
 destination:Object.freeze(['destination']),
 travel:Object.freeze(['travel']),
 navigator:Object.freeze(['navigator'])
});
function ensure(group){
 const keys=GROUPS[group];
 if(!keys) return Promise.reject(new Error('GV FONT GROUP UNKNOWN: '+group));
 return Promise.allSettled(keys.map(loadFace)).then(results=>{const failures=results.filter(result=>result.status==='rejected');if(failures.length)console.error('GV FONT DEGRADED MODE — continuing with browser fallback fonts',{group,failures:failures.map(result=>String(result.reason?.message||result.reason))});return true;});
}
function diagnostics(){
 return Object.freeze({
  version:VERSION,
  loaded:[...loaded.keys()],
  pending:[...jobs.keys()],
  faces:[...document.fonts].filter(face=>Object.values(FACES).some(spec=>face.family===spec.family)).map(face=>({family:face.family,status:face.status,weight:face.weight,style:face.style}))
 });
}
global.GVFontsReady=Object.freeze({VERSION,ensure,diagnostics});
console.info('GV FONTS READY SERVICE REGISTERED',VERSION);
})(typeof window!=='undefined'?window:globalThis);
