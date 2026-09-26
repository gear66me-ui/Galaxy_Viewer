import gv0032 from './gv-cloudflare-auto-astrometry-curator-0032-worker.js';

const REV='0033';
const BUILD_STAMP_COLOMBIA='2026-08-29 19:38:03 COT';
const BUILD_STAMP_ISO='2026-08-29T19:38:03-05:00';
const OLD_VISIBLE_STAMPS=[
  '2026-08-29 19:22:14 COT',
  '2026-08-29 19:33:28 COT'
];

function normalizeVisibleBuildIdentity(html){
  let h=html;
  h=h.replaceAll('GV 0032 LIVE','GV 0033 LIVE');
  h=h.replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0032','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0033');
  for(const stamp of OLD_VISIBLE_STAMPS)h=h.replaceAll(stamp,BUILD_STAMP_COLOMBIA);
  return h;
}

async function page(request,env){
  const r=await gv0032.fetch(request,env);
  const h=normalizeVisibleBuildIdentity(await r.text());
  const headers=new Headers(r.headers);
  headers.set('content-type','text/html; charset=utf-8');
  headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');
  headers.set('pragma','no-cache');
  headers.set('expires','0');
  headers.set('x-gv-revision',REV);
  headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);
  headers.set('x-gv-visible-stamps','normalized-to-current-build');
  return new Response(h,{status:r.status,headers});
}

async function health(request,env){
  const r=await gv0032.fetch(request,env);
  let data={};try{data=await r.json()}catch{}
  data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0033',inherited_from:'0032',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',visible_build_stamps:'normalized',stale_visible_build_stamps_removed:OLD_VISIBLE_STAMPS};
  return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA}});
}

export default {async fetch(request,env){
  const u=new URL(request.url);
  if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);
  if(u.pathname==='/api/health')return health(request,env);
  return gv0032.fetch(request,env);
}};
