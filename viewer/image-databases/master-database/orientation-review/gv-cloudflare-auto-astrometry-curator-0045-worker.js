import base0026 from './gv-cloudflare-auto-astrometry-curator-0026-worker.js';

const REV='0045';
const BUILD_STAMP_COLOMBIA='2026-08-29 21:19:00 COT';
const BUILD_STAMP_ISO='2026-08-29T21:19:00-05:00';

const CLIENT=String.raw`<style id="gv45-style">
#gv45Recovery{margin:6px 8px;padding:7px 9px;border:1px solid #2f8b60;border-radius:8px;background:#0d2c20;color:#8fffc0;font:900 10px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap}
#gv26apply:disabled{opacity:.72!important;cursor:not-allowed!important}
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
function json(o,status=200){return new Response(JSON.stringify(o),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}})}
async function page(request,env){
  const r=await base0026.fetch(request,env);let h=await r.text();
  const p=patchLegacy(h);if(!p.ok)return new Response('0045 STARTUP ERROR: legacy movement anchor counts '+JSON.stringify(p.counts),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  h=p.h;const i=h.lastIndexOf('</body>');if(i<0)return new Response('0045 STARTUP ERROR: body anchor missing',{status:500});
  h=h.slice(0,i)+CLIENT+h.slice(i);
  h=h.replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0026','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0045');
  const headers=new Headers(r.headers);headers.set('content-type','text/html; charset=utf-8');headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-recovery-baseline','0026');headers.set('x-gv-legacy-sift-movement','disabled');
  return new Response(h,{status:200,headers});
}
async function health(env){
  const keyConfigured=Boolean(String(env?.ASTROMETRY_API_KEY||'').trim());
  return json({ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0045',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,key_source:'server-secret',key_configured:keyConfigured,mode:'safe-recovery',base_page:'0026',catalog_route:'0026 baseline passthrough',image_route:'0026 baseline passthrough',aladin:'0026 baseline',legacy_sift_movement:false,machine_astrometry:'disabled-until-baseline-proven'});
}
export default{async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(env);return base0026.fetch(request,env)}};
