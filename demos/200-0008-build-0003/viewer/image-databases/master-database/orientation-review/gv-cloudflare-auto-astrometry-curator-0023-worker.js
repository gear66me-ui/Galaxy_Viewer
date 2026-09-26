import base0019 from './gv-cloudflare-auto-astrometry-curator-0019-worker.js';

const NOVA='https://nova.astrometry.net';
const REV='0023';
const IMAGE_TIMEOUT_MS=12000;
const IMAGE_CACHE_SECONDS=604800;

function jsonResponse(obj,status=200,extra={}){
  return new Response(JSON.stringify(obj),{status,headers:{
    'content-type':'application/json; charset=utf-8',
    'cache-control':'no-store',
    'x-content-type-options':'nosniff',
    ...extra
  }});
}
function finiteOptional(v){if(v===null||v===undefined||v==='')return null;const n=Number(v);return Number.isFinite(n)?n:null}
function requiredFinite(v,name){const n=Number(v);if(!Number.isFinite(n))throw Error(name+' must be finite');return n}
function clamp(v,lo,hi){return Math.max(lo,Math.min(hi,v))}
function safeRemoteUrl(raw){
  const u=new URL(String(raw||''));
  if(!/^https?:$/.test(u.protocol))throw Error('image URL must use http(s)');
  const h=u.hostname.toLowerCase();
  if(h==='localhost'||h.endsWith('.localhost')||h==='0.0.0.0'||h==='127.0.0.1'||h==='::1')throw Error('local image host blocked');
  if(/^(10\.|192\.168\.|169\.254\.|172\.(1[6-9]|2\d|3[01])\.)/.test(h))throw Error('private image host blocked');
  return u;
}
async function timedFetch(url,init={},timeoutMs=IMAGE_TIMEOUT_MS){
  const controller=new AbortController();
  const timer=setTimeout(()=>controller.abort('timeout'),timeoutMs);
  const started=Date.now();
  try{
    const r=await fetch(url,{...init,signal:controller.signal});
    return {response:r,ms:Date.now()-started};
  }finally{clearTimeout(timer)}
}
async function novaPost(path,payload){
  const body=new URLSearchParams();body.set('request-json',JSON.stringify(payload));
  const {response:r,ms}=await timedFetch(NOVA+path,{method:'POST',headers:{'content-type':'application/x-www-form-urlencoded;charset=UTF-8'},body:body.toString(),redirect:'follow'},30000);
  const text=await r.text();let j={};try{j=JSON.parse(text)}catch{}
  if(!r.ok){const e=Error('Astrometry.net '+path+' HTTP '+r.status);e.httpStatus=r.status;e.body=text.slice(0,500);e.ms=ms;throw e}
  return {json:j,ms,httpStatus:r.status};
}

async function handleImage(request){
  const url=new URL(request.url);let remote;
  try{remote=safeRemoteUrl(url.searchParams.get('url'))}catch(e){return jsonResponse({ok:false,revision:REV,stage:'image-url',error:String(e.message||e)},400)}
  const cache=caches.default;
  const cacheKey=new Request(new URL('/__gv_image_cache__?url='+encodeURIComponent(remote.href),request.url).href,{method:'GET'});
  const cached=await cache.match(cacheKey);
  if(cached){const h=new Headers(cached.headers);h.set('x-gv-image-cache','HIT');h.set('access-control-allow-origin','*');return new Response(cached.body,{status:cached.status,headers:h})}
  try{
    const {response:r,ms}=await timedFetch(remote.href,{headers:{'accept':'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8','user-agent':'GalaxyViewerAstrometryCurator/0023'},redirect:'follow'},IMAGE_TIMEOUT_MS);
    if(!r.ok)return jsonResponse({ok:false,revision:REV,stage:'image-fetch',source:remote.href,http_status:r.status,elapsed_ms:ms,error:'source image HTTP '+r.status},502,{'access-control-allow-origin':'*'});
    const ct=(r.headers.get('content-type')||'').toLowerCase();
    if(ct&&!ct.startsWith('image/'))return jsonResponse({ok:false,revision:REV,stage:'image-content-type',source:remote.href,content_type:ct,elapsed_ms:ms,error:'source did not return an image'},502,{'access-control-allow-origin':'*'});
    const h=new Headers(r.headers);h.set('cache-control','public, max-age='+IMAGE_CACHE_SECONDS);h.set('access-control-allow-origin','*');h.set('x-gv-image-cache','MISS');h.set('x-gv-image-source',remote.hostname);h.set('x-gv-image-fetch-ms',String(ms));h.delete('set-cookie');
    const out=new Response(r.body,{status:200,headers:h});
    try{await cache.put(cacheKey,out.clone())}catch{}
    return out;
  }catch(e){
    return jsonResponse({ok:false,revision:REV,stage:e?.name==='AbortError'?'image-timeout':'image-fetch',source:remote.href,timeout_ms:IMAGE_TIMEOUT_MS,error:String(e?.message||e)},504,{'access-control-allow-origin':'*'});
  }
}

async function handleSolve(request){
  if(request.method!=='POST')return jsonResponse({error:'POST required',revision:REV,stage:'request'},405);
  let b;try{b=await request.json()}catch{return jsonResponse({error:'invalid JSON',revision:REV,stage:'request-json'},400)}
  const diag={revision:REV,stage:'init',strategy:null,login_ms:null,upload_ms:null,image_url_kind:null};
  try{
    const apikey=String(b.apikey||'').trim(),imageUrl=String(b.image_url||'').trim(),strategy=String(b.strategy||'seeded-scale').trim();diag.strategy=strategy;
    if(!apikey)throw Object.assign(Error('Astrometry.net API key is required'),{stage:'apikey'});
    if(!/^https?:\/\//i.test(imageUrl))throw Object.assign(Error('source image must be an http(s) URL'),{stage:'image-url'});
    if(!['seeded-scale','seeded-relaxed','blind'].includes(strategy))throw Object.assign(Error('invalid solve strategy'),{stage:'strategy'});
    diag.image_url_kind=imageUrl.includes('/api/image?url=')?'cloudflare-proxy':'direct';
    const width=Math.max(1,Math.round(requiredFinite(b.width,'width'))),height=Math.max(1,Math.round(requiredFinite(b.height,'height'))),ra=finiteOptional(b.ra),dec=finiteOptional(b.dec),fov=finiteOptional(b.fov);
    diag.stage='login';
    const login=await novaPost('/api/login',{apikey});diag.login_ms=login.ms;
    if(login.json.status!=='success'||!login.json.session)throw Object.assign(Error('Astrometry.net login failed'),{stage:'login-response'});
    const upload={session:login.json.session,url:imageUrl,allow_commercial_use:'d',allow_modifications:'d',publicly_visible:'n'};
    if(strategy==='seeded-scale'){
      upload.downsample_factor=2;
      if(fov!==null&&fov>0){upload.scale_units='degwidth';upload.scale_type='ul';upload.scale_lower=Math.max(fov*.20,.0001);upload.scale_upper=Math.min(Math.max(fov*5,upload.scale_lower*2),180)}
      if(ra!==null&&dec!==null){upload.center_ra=ra;upload.center_dec=dec;upload.radius=fov!==null&&fov>0?clamp(fov*4,.05,30):10}
    }else if(strategy==='seeded-relaxed'){
      upload.downsample_factor=1;upload.positional_error=2;
      if(ra!==null&&dec!==null){upload.center_ra=ra;upload.center_dec=dec;upload.radius=fov!==null&&fov>0?clamp(Math.max(fov*12,2),2,90):30}
    }else{upload.downsample_factor=1;upload.positional_error=2}
    diag.stage='url-upload';
    const sub=await novaPost('/api/url_upload',upload);diag.upload_ms=sub.ms;
    if(sub.json.status!=='success'||!sub.json.subid)throw Object.assign(Error('Astrometry.net submission failed: '+JSON.stringify(sub.json)),{stage:'url-upload-response'});
    diag.stage='submitted';
    return jsonResponse({ok:true,subid:sub.json.subid,width,height,strategy,seeded:strategy!=='blind'&&ra!==null&&dec!==null,scaleConstrained:strategy==='seeded-scale'&&fov!==null&&fov>0,diagnostics:diag});
  }catch(e){
    diag.stage=e?.stage||diag.stage||'solve';
    diag.error=String(e?.message||e);if(e?.httpStatus)diag.http_status=e.httpStatus;if(e?.ms!=null)diag.elapsed_ms=e.ms;
    return jsonResponse({error:diag.error,revision:REV,stage:diag.stage,diagnostics:diag},400);
  }
}

const CLIENT_PATCH=String.raw`<style id="gv0023-lock-style">
html,body{overscroll-behavior-y:none!important;overscroll-behavior-x:none!important}
#gv0023Lock{position:fixed;right:8px;top:8px;z-index:2147483646;background:#123d2a;border:1px solid #57e39b;color:#eafff4;padding:5px 8px;border-radius:999px;font:800 10px system-ui;box-shadow:0 0 10px #57e39b55;pointer-events:none}
#gv0023Diag{margin:8px;border:1px solid #44546a;border-radius:8px;background:#07101b;color:#d9e8ff;font:11px ui-monospace,SFMono-Regular,Consolas,monospace;padding:7px}
#gv0023Diag summary{cursor:pointer;font-family:system-ui;font-weight:900;color:#8ab4ff}
#gv0023Diag pre{white-space:pre-wrap;word-break:break-word;max-height:36vh;overflow:auto;margin:7px 0}
#gv0023Diag button{font:800 10px system-ui;padding:5px 7px}
</style>
<div id="gv0023Lock">🔒 REFRESH LOCKED · 0023</div>
<details id="gv0023Diag" open><summary>0023 DIAGNOSTICS — LIVE FAILURE TRACE</summary><pre id="gv0023DiagLog">BOOT 0023</pre><button type="button" id="gv0023CopyDiag">COPY DIAGNOSTICS</button></details>
<script>
(()=>{
'use strict';
const REV='0023',D=document.getElementById('gv0023DiagLog'),P=document.getElementById('published');
const lines=[];function d(stage,msg,data){const t=new Date().toISOString();let tail='';if(data!==undefined){try{tail=' '+JSON.stringify(data)}catch{tail=' '+String(data)}}const s=t+' ['+stage+'] '+msg+tail;lines.push(s);if(lines.length>180)lines.splice(0,lines.length-180);if(D)D.textContent=lines.join('\n');console.log('[GV0023]',stage,msg,data??'')}
window.gv0023Diag=d;d('BOOT','revision '+REV,{ua:navigator.userAgent,viewport:[innerWidth,innerHeight],href:location.href});
let sy=0;document.addEventListener('touchstart',e=>{if(e.touches&&e.touches[0])sy=e.touches[0].clientY},{passive:true});
document.addEventListener('touchmove',e=>{if(!e.touches||!e.touches[0])return;const dy=e.touches[0].clientY-sy;if(scrollY<=0&&dy>0){e.preventDefault()}},{passive:false});
window.addEventListener('error',e=>d('JS-ERROR',e.message||'error',{file:e.filename,line:e.lineno,col:e.colno}));window.addEventListener('unhandledrejection',e=>d('PROMISE-ERROR',String(e.reason?.message||e.reason||'unhandled rejection')));
function candidates(r){if(!r)return[];const raw=[r.selectedImageUrl,r.githubImageUrl,r.esaPublicationJpeg,r.publicationJpeg,r.imageUrl,r.jpegUrl,r.image,...(Array.isArray(r.jpegCandidates)?r.jpegCandidates:[])];return [...new Set(raw.filter(x=>typeof x==='string'&&/^https?:\/\//i.test(x.trim())).map(x=>x.trim()))]}
function proxy(u){return u?location.origin+'/api/image?url='+encodeURIComponent(u):''}
function rec(){try{return typeof current==='function'?current()?.r:null}catch{return null}}
function setSource(original,idx=0){if(!P||!original)return;P.dataset.gvOriginalUrl=original;P.dataset.gvCandidateIndex=String(idx);const pu=proxy(original);if(P.src!==pu){d('IMAGE','proxy request',{candidate:idx,source:original});P.src=pu}}
if(P){
 const mo=new MutationObserver(()=>{const s=P.getAttribute('src')||'';if(/^https?:\/\//i.test(s)&&!s.includes('/api/image?url=')){const rr=rec(),cs=candidates(rr),idx=Math.max(0,cs.indexOf(s));setSource(s,idx)}});mo.observe(P,{attributes:true,attributeFilter:['src']});
 P.addEventListener('load',()=>{d('IMAGE','loaded',{w:P.naturalWidth,h:P.naturalHeight,source:P.dataset.gvOriginalUrl||null,proxy:P.currentSrc});const rr=rec(),cs=candidates(rr);if(cs.length){const idx=Number(P.dataset.gvCandidateIndex||0),next=cs[idx+1]||(()=>{try{const q=queue?.[qpos+1];return candidates(q?.r)[0]}catch{return null}})();if(next)fetch(proxy(next),{cache:'force-cache'}).then(r=>d('PRELOAD','next image '+r.status,{source:next})).catch(e=>d('PRELOAD-FAIL',e.message,{source:next}))}});
 P.addEventListener('error',()=>{const rr=rec(),cs=candidates(rr),idx=Number(P.dataset.gvCandidateIndex||0),next=cs[idx+1];d('IMAGE-FAIL','candidate failed',{candidate:idx,source:P.dataset.gvOriginalUrl||P.src,next:next||null});if(next)setSource(next,idx+1)});
}
const nativeFetch=window.fetch.bind(window);window.fetch=async function(input,init){let url=typeof input==='string'?input:input?.url||String(input),cfg=init?{...init}:{};const started=performance.now();
 try{
  if(url.includes('/api/solve')&&cfg.body){try{const b=JSON.parse(cfg.body);const original=P?.dataset.gvOriginalUrl||(()=>{const rr=rec();return candidates(rr)[0]||b.image_url})();if(original){b.image_url=proxy(original);cfg.body=JSON.stringify(b);d('SOLVE-SUBMIT','forcing displayed image through proxy',{strategy:b.strategy,image:original,width:b.width,height:b.height,ra:b.ra,dec:b.dec,fov:b.fov})}}catch(e){d('SOLVE-PATCH-FAIL',e.message)}}
  const r=await nativeFetch(input instanceof Request?new Request(input,cfg):url,cfg);const ms=Math.round(performance.now()-started);
  if(url.includes('/api/solve')||url.includes('/api/status')||url.includes('/api/health')){let body=null;try{body=await r.clone().json()}catch{}d(r.ok?'API':'API-FAIL',url+' -> '+r.status+' in '+ms+'ms',body)}
  return r;
 }catch(e){d('FETCH-FAIL',url+' in '+Math.round(performance.now()-started)+'ms',String(e?.message||e));throw e}
};
const cb=document.getElementById('gv0023CopyDiag');if(cb)cb.addEventListener('click',async()=>{const text=lines.join('\n');try{await navigator.clipboard.writeText(text);d('DIAG','copied')}catch{const ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();d('DIAG','copied fallback')}});
nativeFetch('/api/health',{cache:'no-store'}).then(async r=>d('HEALTH','HTTP '+r.status,await r.json().catch(()=>null))).catch(e=>d('HEALTH-FAIL',e.message));
})();
</script>`;

async function html0023(request){
  const r=await base0019.fetch(request);let h=await r.text();
  h=h.replaceAll('0019','0023');
  const pos=h.lastIndexOf('</body>');
  if(pos<0)return new Response('0023 STARTUP ERROR: body anchor missing',{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  h=h.slice(0,pos)+CLIENT_PATCH+h.slice(pos);
  return new Response(h,{status:200,headers:{'content-type':'text/html; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff','referrer-policy':'no-referrer','permissions-policy':'camera=(), microphone=(), geolocation=()'}});
}

async function wrapStatus(request){
  const started=Date.now();
  try{
    const r=await base0019.fetch(request);const text=await r.text();let j;try{j=JSON.parse(text)}catch{return new Response(text,{status:r.status,headers:r.headers})}
    j.revision=REV;j.diagnostics={...(j.diagnostics||{}),revision:REV,stage:'status',elapsed_ms:Date.now()-started};
    if(!r.ok||j.status==='error')j.diagnostics.failure=j.message||j.error||'status failure';
    return jsonResponse(j,r.status);
  }catch(e){return jsonResponse({status:'error',revision:REV,stage:'status',message:String(e?.message||e),diagnostics:{revision:REV,stage:'status-exception',elapsed_ms:Date.now()-started}},502)}
}

export default {async fetch(request){
  const url=new URL(request.url);
  if(url.pathname==='/api/health')return jsonResponse({ok:true,service:'gv-cloudflare-astrometry-bridge-0023',revision:REV,refresh_lock:true,image_proxy:true,image_timeout_ms:IMAGE_TIMEOUT_MS,image_cache_seconds:IMAGE_CACHE_SECONDS,image_fallback:true,diagnostics:true,retryLadder:['seeded-scale','seeded-relaxed','blind'],parity:'unconstrained'});
  if(url.pathname==='/api/image')return handleImage(request);
  if(url.pathname==='/api/solve')return handleSolve(request);
  if(url.pathname==='/api/status')return wrapStatus(request);
  if(url.pathname==='/'||url.pathname==='/index.html')return html0023(request);
  return base0019.fetch(request);
}};
