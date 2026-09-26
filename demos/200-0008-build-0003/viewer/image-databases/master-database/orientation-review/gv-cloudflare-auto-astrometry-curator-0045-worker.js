import base0026 from './gv-cloudflare-auto-astrometry-curator-0026-worker.js';

const REV='0045';
const BUILD_STAMP_COLOMBIA='2026-08-29 21:19:00 COT';
const BUILD_STAMP_ISO='2026-08-29T21:19:00-05:00';

const CLIENT=String.raw`<style id="gv45-style">
#gv45Recovery{margin:6px 8px;padding:7px 9px;border:1px solid #2f8b60;border-radius:8px;background:#0d2c20;color:#8fffc0;font:900 10px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap}
#gv26apply:disabled{opacity:.72!important;cursor:not-allowed!important}
.compare{grid-template-columns:1fr 1fr!important}
</style>
<script>(()=>{
'use strict';
function install0045(){
  const compare=document.querySelector('main > section.compare')||document.querySelector('.compare');
  const readouts=document.querySelector('main > section.readouts')||document.querySelector('.readouts');
  const rot=document.getElementById('rotRange');
  const rotRow=rot?.closest?.('.controls');
  const applyRot=[...document.querySelectorAll('button')].find(b=>/^APPLY\s+ROT(?:ATION)?$/i.test((b.textContent||'').trim()));
  const applyRow=applyRot?.closest?.('.controls');
  if(compare&&readouts&&rotRow){
    if(compare.nextElementSibling!==rotRow)compare.insertAdjacentElement('afterend',rotRow);
    if(applyRow&&applyRow!==rotRow&&rotRow.nextElementSibling!==applyRow)rotRow.insertAdjacentElement('afterend',applyRow);
    const lastOrientationRow=applyRow&&applyRow!==rotRow?applyRow:rotRow;
    if(lastOrientationRow.nextElementSibling!==readouts)lastOrientationRow.insertAdjacentElement('afterend',readouts);
  }
  const published=document.getElementById('published');
  if(published&&!published.dataset.gv45DimsBound){
    published.dataset.gv45DimsBound='1';
    published.addEventListener('load',()=>{
      const d=document.getElementById('catDims');
      if(d&&published.naturalWidth&&published.naturalHeight)d.textContent=published.naturalWidth+' × '+published.naturalHeight+' px';
    });
  }
  const survey=document.getElementById('survey');
  if(survey&&!survey.dataset.gv45SurveyBound){
    survey.dataset.gv45SurveyBound='1';
    survey.addEventListener('change',()=>{
      const id=String(survey.value||'').trim();
      if(!id)return;
      if(typeof aladin?.setBaseImageLayer==='function')aladin.setBaseImageLayer(id);
      else if(typeof aladin?.setImageSurvey==='function')aladin.setImageSurvey(id);
    });
  }
  const missionDefault=document.getElementById('missionDefault');
  if(missionDefault&&!missionDefault.dataset.gv45MissionDefaultBound){
    missionDefault.dataset.gv45MissionDefaultBound='1';
    missionDefault.addEventListener('click',()=>{
      setTimeout(()=>{
        survey?.dispatchEvent(new Event('change',{bubbles:true}));
      },0);
    });
  }
  const b=document.querySelector('#gv26apply');
  if(b){b.disabled=true;b.textContent='★ MACHINE ASTROMETRY · SAFE RECOVERY — DISABLED';b.title='Legacy SIFT movement is disabled. Gaia machine solve will be restored only after catalog/image/Aladin baseline is healthy.'}
  if(!document.querySelector('#gv45Recovery')){
    const e=document.createElement('div');e.id='gv45Recovery';e.textContent='0045 SAFE RECOVERY · LEGACY SIFT MOVEMENT DISABLED · CATALOG / SOURCE IMAGE / ALADIN RESTORED THROUGH 0026 BASELINE';
    const host=document.querySelector('#gv26bar')||document.querySelector('main');host?.insertAdjacentElement('afterend',e);
  }
}
install0045();setInterval(install0045,500);console.log('[GV0045] safe recovery client installed');
})();</script>`;

function count(h,s){return h.split(s).length-1}
function patchLegacy(h){
  const a="q('#gv26apply').onclick=()=>apply(true,'manual');";
  const b="timer=setTimeout(()=>apply(false,'record-load'),900)";
  const c="setTimeout(()=>apply(false,'boot'),700)";
  const counts={manual:count(h,a),record:count(h,b),boot:count(h,c)};
  if(counts.manual!==1||counts.record!==1||counts.boot!==1)return{ok:false,counts};
  h=h.replace(a,"q('#gv26apply').onclick=()=>{};")
     .replace(b,"timer=setTimeout(()=>state(),900)")
     .replace(c,"setTimeout(()=>state(),700)")
     .replaceAll('★ APPLY MACHINE PREDICTION','★ MACHINE ASTROMETRY · SAFE RECOVERY — DISABLED')
     .replaceAll('AUTO APPLIED','LEGACY SIFT DISPLAY ONLY');
  return{ok:true,h,counts};
}
function patchHdSourcePriority(h){
  const imageOfOld="function imageOf(r){return r.selectedImageUrl||r.githubImageUrl||r.esaPublicationJpeg||r.publicationJpeg||r.imageUrl||r.jpegUrl||r.image||(Array.isArray(r.jpegCandidates)?r.jpegCandidates[0]:'')||''}";
  const imageOfNew="function imageOf(r){return r.hdUrl||r.hd_url||r.selectedImageUrl||r.githubImageUrl||r.esaPublicationJpeg||r.publicationJpeg||r.imageUrl||r.jpegUrl||r.image||(Array.isArray(r.jpegCandidates)?r.jpegCandidates[0]:'')||''}";
  const candidatesOld="const raw=[r.selectedImageUrl,r.githubImageUrl,r.esaPublicationJpeg,r.publicationJpeg,r.imageUrl,r.jpegUrl,r.image,...(Array.isArray(r.jpegCandidates)?r.jpegCandidates:[])];";
  const candidatesNew="const raw=[r.hdUrl,r.hd_url,r.selectedImageUrl,r.githubImageUrl,r.esaPublicationJpeg,r.publicationJpeg,r.imageUrl,r.jpegUrl,r.image,...(Array.isArray(r.jpegCandidates)?r.jpegCandidates:[])];";
  const counts={imageOf:count(h,imageOfOld),fallbackCandidates:count(h,candidatesOld)};
  if(counts.imageOf!==1||counts.fallbackCandidates!==1)return{ok:false,counts};
  return{ok:true,h:h.replace(imageOfOld,imageOfNew).replace(candidatesOld,candidatesNew),counts};
}
function patchAladinEarlyInit(h){
  const boot="async function boot(){";
  const init="await A.init;";
  const ctor="aladin=A.aladin('#aladin'";
  const counts={boot:count(h,boot),init:count(h,init),constructor:count(h,ctor)};
  if(counts.boot!==1||counts.init!==1||counts.constructor!==1)return{ok:false,counts};
  const bootAt=h.indexOf(boot),initAt=h.indexOf(init,bootAt),ctorAt=h.indexOf(ctor,initAt);
  if(!(bootAt>=0&&bootAt<initAt&&initAt<ctorAt))return{ok:false,counts:{...counts,order:false}};
  const openAt=h.indexOf('(',ctorAt);
  if(openAt<0)return{ok:false,counts:{...counts,constructorBoundary:false}};
  let depth=0,quote='',escape=false,closeAt=-1;
  for(let i=openAt;i<h.length;i++){
    const ch=h[i];
    if(quote){
      if(escape){escape=false;continue}
      if(ch==='\\'){escape=true;continue}
      if(ch===quote){quote='';continue}
      continue;
    }
    if(ch==="'"||ch==='"'||ch==='`'){quote=ch;continue}
    if(ch==='('){depth++;continue}
    if(ch===')'){
      depth--;
      if(depth===0){closeAt=i;break}
      if(depth<0)break;
    }
  }
  if(closeAt<0)return{ok:false,counts:{...counts,constructorBoundary:false}};
  let endAt=closeAt+1;if(h[endAt]===';')endAt++;
  const neutral="aladin=A.aladin('#aladin',{survey:'P/DSS2/color',target:'0 0',fov:1.5,projection:'TAN',cooFrame:'ICRSd',lockNorthUp:false,northPoleOrientation:0,showReticle:true,showCooGrid:true,showZoomControl:true,showLayersControl:false,showFullscreenControl:false,inertia:false});";
  h=h.slice(0,ctorAt)+"applyState(init);"+h.slice(endAt);
  const insertAt=h.indexOf(init,bootAt)+init.length;
  h=h.slice(0,insertAt)+neutral+h.slice(insertAt);
  return{ok:true,h,counts};
}
function patchCatalogRevision(h){
  const objectPattern=/\{[^{}]*name\s*:\s*['"]Hubble['"][^{}]*\}/g;
  const hubblePath='viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-';
  const matches=[...h.matchAll(objectPattern)].filter(m=>m[0].includes(hubblePath));
  const counts={hubbleObjects:matches.length};
  if(matches.length!==1)return{ok:false,counts};
  const old=matches[0][0];
  const revisionMatches=old.match(/\brevision\s*:\s*['"][^'"]+['"]/g)||[];
  const urlCount=(old.match(/viewer\/image-databases\/Hubble\/databases\/gv-hubble-galaxies-full-[^'"}]+\.json/g)||[]).length;
  if(revisionMatches.length>1||urlCount!==1)return{ok:false,counts:{...counts,revision:revisionMatches.length,url:urlCount}};
  let good=old.replace(/gv-hubble-galaxies-full-[^'"}]+\.json/,'gv-hubble-galaxies-full-0025.json');
  if(revisionMatches.length===1){
    good=good.replace(/(\brevision\s*:\s*['"])[^'"]+(['"])/,(_,a,b)=>a+'0025'+b);
  }
  return{ok:true,h:h.slice(0,matches[0].index)+good+h.slice(matches[0].index+old.length),counts:{...counts,revision:revisionMatches.length,url:1}};
}
function patchSourceMetadata(h){
  const publishedPattern=/<img\b[^>]*\bid=['"]published['"][^>]*>/g;
  const matches=[...h.matchAll(publishedPattern)];
  const dimsCount=(h.match(/\bid=['"]catDims['"]/g)||[]).length;
  const counts={published:matches.length,catDims:dimsCount};
  if(matches.length!==1||dimsCount!==0)return{ok:false,counts};
  const old=matches[0][0];
  const good=old+'<span id="gv45SourceDims" style="position:absolute;left:5px;bottom:5px;z-index:30;background:#000d;border-radius:5px;padding:3px 5px;font-size:10px;pointer-events:none">DIM <b id="catDims">—</b></span>';
  return{ok:true,h:h.slice(0,matches[0].index)+good+h.slice(matches[0].index+old.length),counts};
}
function patchLiveMetadata(h){
  const rotationReadout='id="gv26arot"';
  const coordinateReadout='id="gv26coords"';
  const rotationUpdate="if(q('#gv26arot'))q('#gv26arot').textContent=";
  const coordinateUpdate="if(q('#gv26coords'))q('#gv26coords').textContent=";
  const counts={
    rotationReadout:count(h,rotationReadout),
    coordinateReadout:count(h,coordinateReadout),
    rotationUpdate:count(h,rotationUpdate),
    coordinateUpdate:count(h,coordinateUpdate)
  };
  if(counts.rotationReadout!==1||counts.coordinateReadout!==1||counts.rotationUpdate!==1||counts.coordinateUpdate!==1)return{ok:false,counts};
  return{ok:true,h,counts};
}
function json(o,status=200){return new Response(JSON.stringify(o),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}})}
async function page(request,env){
  const r=await base0026.fetch(request,env);let h=await r.text();
  const p=patchLegacy(h);if(!p.ok)return new Response('0045 STARTUP ERROR: legacy movement anchor counts '+JSON.stringify(p.counts),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  const hd=patchHdSourcePriority(p.h);if(!hd.ok)return new Response('0045 STARTUP ERROR: HD source anchor counts '+JSON.stringify(hd.counts),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  const ai=patchAladinEarlyInit(hd.h);if(!ai.ok)return new Response('0045 STARTUP ERROR: Aladin init anchor counts '+JSON.stringify(ai.counts),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  const cat=patchCatalogRevision(ai.h);if(!cat.ok)return new Response('0045 STARTUP ERROR: Hubble catalog anchor counts '+JSON.stringify(cat.counts),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  const sm=patchSourceMetadata(cat.h);if(!sm.ok)return new Response('0045 STARTUP ERROR: source metadata anchor counts '+JSON.stringify(sm.counts),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  const lm=patchLiveMetadata(sm.h);if(!lm.ok)return new Response('0045 STARTUP ERROR: live metadata anchor counts '+JSON.stringify(lm.counts),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  h=lm.h;const i=h.lastIndexOf('</body>');if(i<0)return new Response('0045 STARTUP ERROR: body anchor missing',{status:500});
  h=h.slice(0,i)+CLIENT+h.slice(i);
  h=h.replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0026','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0045');
  const headers=new Headers(r.headers);headers.set('content-type','text/html; charset=utf-8');headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-recovery-baseline','0026');headers.set('x-gv-legacy-sift-movement','disabled');headers.set('x-gv-source-image-priority','hdUrl-hd_url-then-existing');
  return new Response(h,{status:200,headers});
}
async function health(env){
  const keyConfigured=Boolean(String(env?.ASTROMETRY_API_KEY||'').trim());
  return json({ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0045',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,key_source:'server-secret',key_configured:keyConfigured,mode:'safe-recovery',base_page:'0026',catalog_route:'0026 baseline passthrough',image_route:'0026 baseline passthrough',aladin:'0026 baseline',source_image_priority:['hdUrl','hd_url','selectedImageUrl','githubImageUrl','esaPublicationJpeg','publicationJpeg','imageUrl','jpegUrl','image','jpegCandidates[0]'],legacy_sift_movement:false,machine_astrometry:'disabled-until-baseline-proven'});
}
export default{async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(env);return base0026.fetch(request,env)}};
