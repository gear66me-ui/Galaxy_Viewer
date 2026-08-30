import base0046 from './gv-cloudflare-auto-astrometry-curator-0046-worker.js';

const REV='0048';
const BUILD_STAMP_COLOMBIA='2026-08-30 17:53:00 COT';
const BUILD_STAMP_ISO='2026-08-30T17:53:00-05:00';

const STYLE=String.raw`<style id="gv48-client-recovery-style">
#gv48BuildStamp{position:relative;z-index:10000;padding:5px 8px;background:#08251a;border-bottom:1px solid #2f8b60;color:#8fffc0;font:900 10px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace}
#published{width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;object-position:center center!important}
#gv48LiveStats{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:5px;margin:0 8px 8px;padding:6px;border:1px solid #384d67;border-radius:8px;background:#09121f;font:800 10px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace}
#gv48LiveStats span{border:1px solid #2f3e52;border-radius:6px;padding:5px;color:#9cabbf;min-width:0}
#gv48LiveStats b{display:block;color:#57e39b;font-size:12px;overflow:hidden;text-overflow:ellipsis}
#gv26refresh,#gv0024Recenter{display:inline-flex!important;visibility:visible!important;opacity:1!important}
#gv48FallbackControls{display:none;gap:5px;margin:0 8px 8px}
#gv48FallbackControls.show{display:flex}
@media(max-width:700px){.compare{grid-template-columns:1fr!important}.viewbox{max-height:none!important}#gv48LiveStats{grid-template-columns:1fr 1fr}}
</style>`;

const BANNER='<div id="gv48BuildStamp">GV 0048 LIVE · BUILD '+BUILD_STAMP_COLOMBIA+'</div>';

const CLIENT=String.raw`<script>(()=>{'use strict';
const q=s=>document.querySelector(s);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const runtime={key:'',imageFailures:[],nativeLoadImage:null,loadImageWrapped:false};

function status48(text,kind='analyzing'){
  const e=q('#status');if(e){e.textContent=text;e.className='status '+kind}
}
function diag48(stage,msg,data){
  try{window.gv0023Diag?.('0048-'+stage,msg,data)}catch{}
  try{console.log('[GV0048]['+stage+']',msg,data||'')}catch{}
}
function current48(){try{return typeof current==='function'?current():null}catch{return null}}
function candidates48(r){
  if(!r)return[];
  const a=[r.hdUrl,r.hd_url,r.selectedImageUrl,r.githubImageUrl,r.esaPublicationJpeg,r.publicationJpeg,r.imageUrl,r.jpegUrl,r.image,...(Array.isArray(r.jpegCandidates)?r.jpegCandidates:[])];
  return [...new Set(a.filter(x=>typeof x==='string'&&/^https?:\/\//i.test(x.trim())).map(x=>x.trim()))];
}
function proxy48(u){return u?location.origin+'/api/image?url='+encodeURIComponent(u):''}
function setCandidate48(x,index=0){
  const p=q('#published');if(!p||!x?.r)return false;
  const a=candidates48(x.r),u=a[index]||'';
  p.dataset.gv48Key=String(x.key||'');
  p.dataset.gv48Index=String(index);
  p.dataset.gv48Candidates=JSON.stringify(a);
  p.dataset.gv48OriginalUrl=u;
  p.dataset.gvOriginalUrl=u;
  if(!u){p.removeAttribute('src');status48('SOURCE IMAGE MISSING · NO USABLE URL','error');return false}
  const pu=proxy48(u);if(p.getAttribute('src')!==pu)p.src=pu;
  return true;
}
function displayedOriginal48(){
  const p=q('#published');if(!p)return'';
  const x=current48(),key=String(x?.key||'');
  if(key&&p.dataset.gv48Key===key&&p.dataset.gv48OriginalUrl)return p.dataset.gv48OriginalUrl;
  return candidates48(x?.r)[0]||'';
}
function bindImage48(){
  const p=q('#published');if(!p)return false;
  p.style.objectFit='contain';p.style.objectPosition='center center';
  if(p.dataset.gv48Bound==='1')return true;
  p.dataset.gv48Bound='1';
  p.addEventListener('load',()=>{
    const d=q('#catDims');if(d&&p.naturalWidth&&p.naturalHeight)d.textContent=p.naturalWidth+' × '+p.naturalHeight+' px';
    diag48('IMAGE','loaded',{key:p.dataset.gv48Key,source:p.dataset.gv48OriginalUrl,w:p.naturalWidth,h:p.naturalHeight});
  });
  p.addEventListener('error',()=>{
    let a=[];try{a=JSON.parse(p.dataset.gv48Candidates||'[]')}catch{}
    const i=Number(p.dataset.gv48Index||0),next=a[i+1];
    runtime.imageFailures.push({key:p.dataset.gv48Key,index:i,source:p.dataset.gv48OriginalUrl||''});
    if(next){
      p.dataset.gv48Index=String(i+1);p.dataset.gv48OriginalUrl=next;p.dataset.gvOriginalUrl=next;p.src=proxy48(next);
      status48('SOURCE IMAGE FALLBACK '+String(i+2)+' / '+String(a.length),'analyzing');
    }else status48('SOURCE IMAGE FAILED · ALL CANDIDATES EXHAUSTED','error');
  });
  new MutationObserver(()=>{
    const src=p.getAttribute('src')||'';
    if(!/^https?:\/\//i.test(src)||src.includes('/api/image?url='))return;
    const x=current48(),a=candidates48(x?.r),idx=Math.max(0,a.indexOf(src));
    if(x)setCandidate48(x,idx);
  }).observe(p,{attributes:true,attributeFilter:['src']});
  return true;
}
function wrapLoadImage48(){
  if(runtime.loadImageWrapped)return true;
  try{
    if(typeof loadImage!=='function')return false;
    runtime.nativeLoadImage=loadImage;
    const wrapped=function(url){
      const original=displayedOriginal48();
      const target=original?proxy48(original):(/^https?:\/\//i.test(String(url||''))&&!String(url).includes('/api/image?url=')?proxy48(String(url)):url);
      diag48('ANALYSIS-IMAGE','load through displayed proxy',{original:original||url,target});
      return runtime.nativeLoadImage(target);
    };
    loadImage=wrapped;
    runtime.loadImageWrapped=true;
    return true;
  }catch(e){diag48('ANALYSIS-WRAP-FAIL',String(e?.message||e));return false}
}
function live48(){
  let c=null,f=null,r=null;
  try{c=typeof currentCenter==='function'?currentCenter():null}catch{}
  try{f=typeof currentFov==='function'?currentFov():null}catch{}
  try{r=typeof currentRot==='function'?currentRot():null}catch{}
  let mirror=false;
  try{mirror=/mirror\s*ON/i.test(String(q('#gv26arot')?.textContent||''))}catch{}
  try{if(typeof solution!=='undefined'&&solution)mirror=mirror||Boolean(solution.mirror_x||solution.mirror_required||solution.longitude_reversed)}catch{}
  return{ra:c?.[0]??null,dec:c?.[1]??null,fov:Number.isFinite(Number(f))?Number(f):null,rot:Number.isFinite(Number(r))?Number(r):null,mirror,survey:String(q('#survey')?.value||'').trim()};
}
function fmt48(v,d=6){return Number.isFinite(Number(v))?Number(v).toFixed(d):'—'}
function stats48(){
  let e=q('#gv48LiveStats');
  if(!e){
    e=document.createElement('div');e.id='gv48LiveStats';
    e.innerHTML='<span>RA<b id="gv48ra">—</b></span><span>DEC<b id="gv48dec">—</b></span><span>FOV<b id="gv48fov">—</b></span><span>ROTATION<b id="gv48rot">—</b></span><span>MIRROR<b id="gv48mirror">OFF</b></span>';
    const h=q('#gv26rot')||q('.readouts')||q('main');h?.insertAdjacentElement('afterend',e);
  }
  const s=live48(),m={gv48ra:fmt48(s.ra),gv48dec:fmt48(s.dec),gv48fov:s.fov!==null?fmt48(s.fov)+'°':'—',gv48rot:s.rot!==null?s.rot.toFixed(2)+'°':'—',gv48mirror:s.mirror?'ON':'OFF'};
  for(const[k,v]of Object.entries(m)){const n=q('#'+k);if(n)n.textContent=v}
  const c=q('#gv26coords');if(c)c.textContent='RA '+m.gv48ra+' · DEC '+m.gv48dec+' · FOV '+m.gv48fov+' · ROT '+m.gv48rot+' · MIRROR '+m.gv48mirror;
}
function machineTarget48(){
  const vals=['machRa','machDec','machFov','machRot'].map(id=>Number(q('#'+id)?.textContent?.replace('°','')));
  if(vals.every(Number.isFinite)&&/GAIA VERIFIED|MACHINE APPLIED/i.test(String(q('#predConfidence')?.textContent||'')))return{ra:vals[0],dec:vals[1],fov:vals[2],rot:vals[3],source:'solved'};
  const x=current48();try{if(x&&typeof baseOf==='function'){const b=baseOf(x);if(Number.isFinite(Number(b?.ra))&&Number.isFinite(Number(b?.dec)))return{ra:Number(b.ra),dec:Number(b.dec),fov:Number(b.fov)||1.5,rot:Number(b.rot)||0,source:'catalog'}}}catch{}
  return null;
}
function recenter48(){
  const s=machineTarget48();if(!s){status48('RE-CENTER FAILED · NO SOLVED/CATALOG POSITION','error');return false}
  try{
    if(typeof applyState!=='function')throw Error('applyState unavailable');
    applyState(s);setTimeout(()=>{applyState(s);try{updateLive?.()}catch{}stats48()},180);
    status48('ALADIN RE-CENTERED · '+s.source.toUpperCase()+' POSITION','ready');return true;
  }catch(e){status48('RE-CENTER FAILED · '+String(e?.message||e),'error');return false}
}
async function refresh48(){
  const s=live48();
  if(!Number.isFinite(Number(s.ra))||!Number.isFinite(Number(s.dec))||!Number.isFinite(Number(s.fov))||s.fov<=0){status48('REFRESH FAILED · LIVE ALADIN STATE UNREADABLE','error');return false}
  if(s.mirror){status48('REFRESH FAILED · MIRROR ON CANNOT BE SAFELY REBUILT','error');return false}
  status48('REFRESHING ALADIN · REBUILDING RENDERER','analyzing');
  try{
    await A.init;
    const old=q('#aladin');if(!old)throw Error('Aladin host missing');
    const fresh=old.cloneNode(false);old.replaceWith(fresh);
    aladin=A.aladin('#aladin',{survey:s.survey||'P/DSS2/color',target:String(s.ra)+' '+String(s.dec),fov:s.fov,projection:'TAN',cooFrame:'ICRSd',lockNorthUp:false,northPoleOrientation:0,showReticle:true,showCooGrid:true,showZoomControl:true,showLayersControl:false,showFullscreenControl:false,inertia:false});
    if(s.survey){if(typeof aladin?.setBaseImageLayer==='function')aladin.setBaseImageLayer(s.survey);else if(typeof aladin?.setImageSurvey==='function')aladin.setImageSurvey(s.survey)}
    await sleep(350);applyState(s);await sleep(350);applyState(s);await sleep(180);
    const z=live48(),t=Math.max(.000001,s.fov*.0001);
    if(!Number.isFinite(Number(z.ra))||!Number.isFinite(Number(z.dec))||!Number.isFinite(Number(z.fov))||Math.abs(z.ra-s.ra)>t||Math.abs(z.dec-s.dec)>t||Math.abs(z.fov-s.fov)>t)throw Error('restored state verification failed');
    status48('ALADIN REFRESHED · LIVE VIEW RESTORED','ready');stats48();return true;
  }catch(e){status48('ALADIN REFRESH FAILED · '+String(e?.message||e),'error');return false}
}
function bindButton48(id,label,fn){
  let b=q('#'+id);if(!b)return false;
  if(b.dataset.gv48Bound!=='1'){
    const c=b.cloneNode(true);b.replaceWith(c);b=c;b.dataset.gv48Bound='1';
    b.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();Promise.resolve(fn()).finally(()=>{b.disabled=false;b.textContent=label})},true);
  }
  b.textContent=label;b.disabled=false;return true;
}
function controls48(){
  const r=bindButton48('gv26refresh','↻ REFRESH ALADIN',refresh48);
  const c=bindButton48('gv0024Recenter','◎ RE-CENTER ALADIN',recenter48);
  let f=q('#gv48FallbackControls');
  if(!f){
    f=document.createElement('div');f.id='gv48FallbackControls';
    f.innerHTML='<button id="gv48FallbackRecenter">◎ RE-CENTER ALADIN</button><button id="gv48FallbackRefresh">↻ REFRESH ALADIN</button>';
    const h=q('#gv26bar')||q('header')||q('main');h?.insertAdjacentElement('afterend',f);
    q('#gv48FallbackRecenter')?.addEventListener('click',recenter48);
    q('#gv48FallbackRefresh')?.addEventListener('click',refresh48);
  }
  f.classList.toggle('show',!(r&&c));
}
function sync48(){
  bindImage48();wrapLoadImage48();controls48();stats48();
  const x=current48(),key=String(x?.key||'');
  if(key&&key!==runtime.key){
    runtime.key=key;setCandidate48(x,0);window.gv46ClearAstro?.();diag48('RECORD','synchronized',{key});
  }
}
sync48();setInterval(sync48,250);
console.log('[GV0048] client-only recovery installed; 0046 core untouched');
})();</script>`;

function injectHead(h,x){const i=h.indexOf('</head>');return i<0?null:h.slice(0,i)+x+h.slice(i)}
function injectTop(h,x){const m=h.match(/<body(?:\s[^>]*)?>/i);if(!m)return null;const i=m.index+m[0].length;return h.slice(0,i)+x+h.slice(i)}
function injectBodyEnd(h,x){const i=h.lastIndexOf('</body>');return i<0?null:h.slice(0,i)+x+h.slice(i)}
function json(o,s=200){return new Response(JSON.stringify(o,null,2),{status:s,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}})}

async function page(request,env){
  const r=await base0046.fetch(request,env);
  const ct=(r.headers.get('content-type')||'').toLowerCase();
  if(!r.ok||!ct.includes('text/html'))return r;
  let h=await r.text();
  h=injectHead(h,STYLE);if(!h)return new Response('0048 STARTUP ERROR: head missing',{status:500});
  h=injectTop(h,BANNER);if(!h)return new Response('0048 STARTUP ERROR: body missing',{status:500});
  h=injectBodyEnd(h,CLIENT);if(!h)return new Response('0048 STARTUP ERROR: body close missing',{status:500});
  h=h.replaceAll('GV 0046 LIVE','GV 0048 LIVE').replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0046','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0048');
  const hd=new Headers(r.headers);
  hd.set('content-type','text/html; charset=utf-8');hd.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');
  hd.set('x-gv-revision',REV);hd.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);
  hd.set('x-gv-base-runtime','0046-untouched');hd.set('x-gv-recovery-layer','client-only');
  return new Response(h,{status:200,headers:hd});
}
async function health(env){
  return json({ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0048',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,base_runtime:'0046-untouched',server_core_rewrite:false,client_recovery:true,source_image_fallback:true,source_image_fit:'contain',analysis_image:'displayed-cloudflare-proxy',controls:['recenter-aladin','refresh-aladin'],live_stats:['ra','dec','fov','rotation','mirror'],record_sync:true,gaia_runtime:'0046-preserved',star_overlays:'0046-preserved',legacy_sift_movement:false,astrometry_cross_check:'mandatory',key_configured:Boolean(String(env?.ASTROMETRY_API_KEY||'').trim())});
}
export default{async fetch(request,env){
  const u=new URL(request.url);
  if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);
  if(u.pathname==='/api/health')return health(env);
  return base0046.fetch(request,env);
}};
