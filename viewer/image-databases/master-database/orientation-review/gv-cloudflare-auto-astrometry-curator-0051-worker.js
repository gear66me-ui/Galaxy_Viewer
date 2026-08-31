import base0050 from './gv-cloudflare-auto-astrometry-curator-0050-worker.js';

const COORDINATE_CLIENT=String.raw`<script>(()=>{'use strict';
const q=s=>document.querySelector(s);

function num51(v){
  const n=Number(v);
  return Number.isFinite(n)?n:null;
}
function fmt51(v,d=6){
  const n=num51(v);
  return n===null?'UNAVAILABLE':n.toFixed(d);
}
function norm51(v){
  let n=num51(v);
  if(n===null)return null;
  while(n>180)n-=360;
  while(n<=-180)n+=360;
  return n;
}
function current51(){
  try{return typeof current==='function'?current():null}catch{return null}
}
function sourceState51(){
  const x=current51();
  if(!x)return null;
  try{
    if(typeof baseOf==='function'){
      const b=baseOf(x);
      return{ra:num51(b?.ra),dec:num51(b?.dec),fov:num51(b?.fov),rot:norm51(b?.rot)};
    }
  }catch{}
  const r=x.r||{};
  const first=(keys)=>{
    for(const k of keys){const n=num51(r[k]);if(n!==null)return n}
    return null;
  };
  return{
    ra:first(['ra','RA','raDeg','raDegrees']),
    dec:first(['dec','Dec','DEC','decDeg','decDegrees']),
    fov:first(['fieldOfView','fov','FOV','field_of_view']),
    rot:norm51(first(['aladinRotationDeg','rotationDeg','orientationDeg','orientation','positionAngle','pa']))
  };
}
function liveCenter51(){
  try{
    if(typeof aladin==='undefined'||!aladin)return null;
    for(const method of ['getRaDec','getCenter','getViewCenter']){
      try{
        const v=aladin?.[method]?.();
        if(Array.isArray(v)&&v.length>=2){
          const ra=num51(v[0]),dec=num51(v[1]);
          if(ra!==null&&dec!==null)return[ra,dec];
        }
        if(v&&typeof v==='object'){
          const ra=num51(v.ra??v.lon??v[0]),dec=num51(v.dec??v.lat??v[1]);
          if(ra!==null&&dec!==null)return[ra,dec];
        }
      }catch{}
    }
  }catch{}
  return null;
}
function liveFov51(){
  try{
    if(typeof aladin==='undefined'||!aladin)return null;
    for(const method of ['getFov','getFoV','getFieldOfView']){
      try{
        const v=aladin?.[method]?.();
        if(Array.isArray(v)){
          const a=v.map(Number).filter(Number.isFinite);
          if(a.length)return Math.max(...a);
        }
        if(v&&typeof v==='object'){
          const n=num51(v.fov??v.x??v.width);
          if(n!==null)return n;
        }
        const n=num51(v);if(n!==null)return n;
      }catch{}
    }
  }catch{}
  return null;
}
function liveRot51(){
  try{
    if(typeof aladin==='undefined'||!aladin)return null;
    for(const method of ['getRotation','getViewRotation','getRoll']){
      try{
        const n=norm51(aladin?.[method]?.());
        if(n!==null)return n;
      }catch{}
    }
  }catch{}
  return null;
}
function put51(id,value){
  const e=q('#'+id);
  if(e)e.textContent=value;
}
function refreshSource51(){
  const s=sourceState51();
  put51('catRa',s?.ra===null||!s?'MISSING':fmt51(s.ra));
  put51('catDec',s?.dec===null||!s?'MISSING':fmt51(s.dec));
  put51('catFov',s?.fov===null||!s?'MISSING':fmt51(s.fov)+'°');
  put51('catRot',s?.rot===null||!s?'MISSING':fmt51(s.rot,2)+'°');
}
function refreshLive51(){
  const c=liveCenter51(),f=liveFov51(),r=liveRot51();
  const ra=c?fmt51(c[0]):'UNAVAILABLE';
  const dec=c?fmt51(c[1]):'UNAVAILABLE';
  const fov=f===null?'UNAVAILABLE':fmt51(f)+'°';
  const rot=r===null?'UNAVAILABLE':fmt51(r,2)+'°';
  for(const id of ['liveRa','dockRa','gv48ra'])put51(id,ra);
  for(const id of ['liveDec','dockDec','gv48dec'])put51(id,dec);
  for(const id of ['liveFov','dockFov','gv48fov'])put51(id,fov);
  for(const id of ['liveRot','dockRot','gv48rot'])put51(id,rot);
  const compact=q('#gv26coords');
  if(compact)compact.textContent='RA '+ra+' · DEC '+dec+' · FOV '+fov+' · ROT '+rot;
}
function sync51(){
  refreshSource51();
  refreshLive51();
}
sync51();
setInterval(sync51,200);
console.log('[GV0051] independent source/live coordinate readback installed');
})();</script>`;

function injectBodyEnd(html,addition){
  const i=html.lastIndexOf('</body>');
  return i<0?null:html.slice(0,i)+addition+html.slice(i);
}

export default {
  async fetch(request,env){
    const url=new URL(request.url);
    if(url.pathname!=='/'&&url.pathname!=='/index.html')return base0050.fetch(request,env);
    const response=await base0050.fetch(request,env);
    const type=(response.headers.get('content-type')||'').toLowerCase();
    if(!response.ok||!type.includes('text/html'))return response;
    const html=await response.text();
    const patched=injectBodyEnd(html,COORDINATE_CLIENT);
    if(!patched)return new Response('0051 STARTUP ERROR: body close missing',{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
    return new Response(patched,{status:response.status,headers:response.headers});
  }
};
