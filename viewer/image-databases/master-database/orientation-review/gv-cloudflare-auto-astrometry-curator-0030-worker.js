import gv0029 from './gv-cloudflare-auto-astrometry-curator-0029-worker.js';

const REV='0030';
const BUILD_STAMP_COLOMBIA='2026-08-29 19:11:14 COT';
const BUILD_STAMP_ISO='2026-08-29T19:11:14-05:00';

const STATUS_BANNER=String.raw`<style>
#gv30DeployStamp{position:sticky;top:0;z-index:2147483647;box-sizing:border-box;width:100%;padding:5px 8px;background:#07131f;border-bottom:1px solid #2f8b60;color:#7dffb5;font:800 10px/1.25 ui-monospace,SFMono-Regular,Consolas,monospace;text-align:center;letter-spacing:.2px}
#gv30DeployStamp strong{color:#fff}#gv30DeployStamp .now{color:#ffd166}
@media(max-width:700px){#gv30DeployStamp{font-size:9px;padding:4px 5px;line-height:1.2}}
</style>
<div id="gv30DeployStamp" role="status" aria-live="polite"><strong>GV 0030 LIVE</strong> · BUILD 2026-08-29 19:11:14 COT · <span class="now" id="gv30ColombiaClock">COLOMBIA NOW —</span></div>
<script>(()=>{'use strict';
const el=document.getElementById('gv30ColombiaClock');
const f=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Bogota',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false});
function tick(){if(el)el.textContent='COLOMBIA NOW '+f.format(new Date())+' COT'}
tick();setInterval(tick,1000);
console.log('[GV0030][DEPLOY] build '+${JSON.stringify(BUILD_STAMP_COLOMBIA)}+'; inherited solver/UI from 0029');
})();</script>`;

function injectAfterBody(html){
  const m=html.match(/<body(?:\s[^>]*)?>/i);
  if(!m)return null;
  const i=m.index+m[0].length;
  return html.slice(0,i)+STATUS_BANNER+html.slice(i);
}

async function page(request,env){
  const r=await gv0029.fetch(request,env);
  const h=await r.text();
  const out=injectAfterBody(h);
  if(out==null)return new Response('0030 STARTUP ERROR: body anchor missing',{status:500});
  const headers=new Headers(r.headers);
  headers.set('content-type','text/html; charset=utf-8');
  headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');
  headers.set('pragma','no-cache');
  headers.set('expires','0');
  headers.set('x-gv-revision',REV);
  headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);
  return new Response(out,{status:r.status,headers});
}

async function health(request,env){
  const r=await gv0029.fetch(request,env);
  let data={};
  try{data=await r.json()}catch{}
  data={...data,
    ok:true,
    revision:REV,
    service:'gv-cloudflare-auto-astrometry-curator-0030',
    inherited_from:'0029',
    build_stamp_colombia:BUILD_STAMP_COLOMBIA,
    build_stamp_iso:BUILD_STAMP_ISO,
    timezone:'America/Bogota',
    deployment_visibility:'visible-banner-and-live-colombia-clock',
    features:[...new Set([...(Array.isArray(data.features)?data.features:[]),'visible-deployment-stamp','live-colombia-clock','no-store-root'])]
  };
  return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store, no-cache, must-revalidate, max-age=0','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA}});
}

export default {async fetch(request,env){
  const u=new URL(request.url);
  if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);
  if(u.pathname==='/api/health')return health(request,env);
  return gv0029.fetch(request,env);
}};
