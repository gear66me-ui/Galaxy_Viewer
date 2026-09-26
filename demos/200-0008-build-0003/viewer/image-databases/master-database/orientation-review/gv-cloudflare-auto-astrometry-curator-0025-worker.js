import base0024 from './gv-cloudflare-auto-astrometry-curator-0024-worker.js';

const REV='0025';
const SERVER_KEY_MARKER='__GV_SERVER_KEY__';

function jsonResponse(obj,status=200,headers={}){
  return new Response(JSON.stringify(obj),{
    status,
    headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff',...headers}
  });
}

async function reviseJsonResponse(r,extras={}){
  const ct=(r.headers.get('content-type')||'').toLowerCase();
  if(!ct.includes('application/json'))return r;
  let j;try{j=await r.json()}catch{return r}
  if(j&&typeof j==='object'){
    if(j.revision==='0024')j.revision=REV;
    if(j.service==='gv-cloudflare-astrometry-bridge-0024')j.service='gv-cloudflare-astrometry-bridge-0025';
    if(j.diagnostics&&j.diagnostics.revision==='0024')j.diagnostics.revision=REV;
    if(j.result&&j.result.revision==='0024')j.result.revision=REV;
    Object.assign(j,extras);
  }
  const headers=new Headers(r.headers);
  headers.set('content-type','application/json; charset=utf-8');
  headers.set('cache-control','no-store');
  return new Response(JSON.stringify(j),{status:r.status,headers});
}

async function handleSolve0025(request,env){
  let body;
  try{body=await request.json()}catch{
    return jsonResponse({ok:false,revision:REV,stage:'request-json',error:'invalid JSON'},400);
  }
  const serverKey=String(env?.ASTROMETRY_API_KEY||'').trim();
  if(!serverKey){
    return jsonResponse({
      ok:false,
      revision:REV,
      stage:'server-key-missing',
      error:'Cloudflare secret ASTROMETRY_API_KEY is not configured',
      diagnostics:{revision:REV,key_source:'server-secret',key_configured:false}
    },503);
  }
  body.apikey=serverKey;
  const headers=new Headers(request.headers);
  headers.set('content-type','application/json');
  headers.delete('content-length');
  const forwarded=new Request(request.url,{
    method:'POST',
    headers,
    body:JSON.stringify(body),
    redirect:request.redirect
  });
  const r=await base0024.fetch(forwarded);
  let priorDiagnostics={};
  try{
    const j=await r.clone().json();
    if(j?.diagnostics&&typeof j.diagnostics==='object')priorDiagnostics=j.diagnostics;
  }catch{}
  return reviseJsonResponse(r,{
    revision:REV,
    diagnostics:{...priorDiagnostics,revision:REV,key_source:'server-secret',key_configured:true}
  });
}

const CLIENT_PATCH=String.raw`<style id="gv0025-key-style">
#gv0025KeyState{display:inline-flex;align-items:center;gap:5px;border:1px solid #2f8b60;border-radius:999px;padding:4px 7px;color:#57e39b;background:#0d2c20;font:850 10px system-ui}
</style>
<script>
(()=>{
'use strict';
function diag(stage,msg,data){try{window.gv0025Diag?.(stage,msg,data);window.gv0024Diag?.(stage,msg,data);window.gv0023Diag?.(stage,msg,data)}catch{}}
const key=document.getElementById('apikey');
if(key){
  key.value='${SERVER_KEY_MARKER}';
  key.setAttribute('value','${SERVER_KEY_MARKER}');
  key.type='hidden';
  key.autocomplete='off';
  key.tabIndex=-1;
  key.setAttribute('aria-hidden','true');
  const labels=[...document.querySelectorAll('label')].filter(l=>l.htmlFor==='apikey'||/astrometry.*api.*key|api.*key/i.test(l.textContent||''));
  for(const l of labels)l.style.display='none';
  try{localStorage.removeItem('gv-astrometry-api-key');localStorage.removeItem('astrometry-api-key')}catch{}
  const host=document.querySelector('header .bar')||document.querySelector('header');
  if(host){
    const pill=document.createElement('span');
    pill.id='gv0025KeyState';
    pill.textContent='🔑 ASTROMETRY KEY · SERVER';
    host.appendChild(pill);
  }
  diag('0025-KEY','client API-key entry disabled; server secret mode active');
}
const nativeFetch=window.fetch.bind(window);
window.fetch=async function(input,init){
  let url=typeof input==='string'?input:input?.url||String(input);
  let cfg=init?{...init}:{};
  if(url.includes('/api/solve')&&cfg.body){
    try{
      const b=JSON.parse(cfg.body);
      b.apikey='${SERVER_KEY_MARKER}';
      cfg.body=JSON.stringify(b);
    }catch(e){diag('0025-KEY-PATCH-FAIL',e.message)}
  }
  return nativeFetch(input instanceof Request?new Request(input,cfg):url,cfg);
};
nativeFetch('/api/health',{cache:'no-store'}).then(async r=>{
  const j=await r.json().catch(()=>null);
  diag('0025-HEALTH','server key '+(j?.key_configured?'configured':'missing'),j);
  const pill=document.getElementById('gv0025KeyState');
  if(pill&&!j?.key_configured){
    pill.textContent='🔑 ASTROMETRY KEY · SERVER MISSING';
    pill.style.color='#ff7575';
    pill.style.borderColor='#a94750';
    pill.style.background='#4b171b';
  }
}).catch(e=>diag('0025-HEALTH-FAIL',e.message));
})();
</script>`;

async function html0025(request){
  const r=await base0024.fetch(request);
  let h=await r.text();
  h=h.replaceAll('0024','0025');
  const pos=h.lastIndexOf('</body>');
  if(pos<0)return new Response('0025 STARTUP ERROR: body anchor missing',{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  h=h.slice(0,pos)+CLIENT_PATCH+h.slice(pos);
  return new Response(h,{status:200,headers:{
    'content-type':'text/html; charset=utf-8',
    'cache-control':'no-store',
    'x-content-type-options':'nosniff',
    'referrer-policy':'no-referrer',
    'permissions-policy':'camera=(), microphone=(), geolocation=()'
  }});
}

export default {
  async fetch(request,env){
    const url=new URL(request.url);
    if(url.pathname==='/api/health')return jsonResponse({
      ok:true,
      service:'gv-cloudflare-astrometry-bridge-0025',
      revision:REV,
      stable_worker_name:'gv-cloudflare-auto-astrometry-curator-0015',
      key_source:'server-secret',
      key_configured:Boolean(String(env?.ASTROMETRY_API_KEY||'').trim()),
      features:['refresh-lock','image-proxy-cache','diagnostics','top-survey-selector','recenter-aladin','server-side-astrometry-key']
    });
    if(url.pathname==='/'||url.pathname==='/index.html')return html0025(request);
    if(url.pathname==='/api/solve')return handleSolve0025(request,env);
    if(url.pathname==='/api/status')return reviseJsonResponse(await base0024.fetch(request),{revision:REV});
    return base0024.fetch(request);
  }
};
