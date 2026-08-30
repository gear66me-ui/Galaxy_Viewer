import gv0033 from './gv-cloudflare-auto-astrometry-curator-0033-worker.js';

const REV='0034';
const BUILD_STAMP_COLOMBIA='2026-08-29 19:39:04 COT';
const BUILD_STAMP_ISO='2026-08-29T19:39:04-05:00';

const LAYOUT_PATCH=String.raw`<style id="gv34-orientation-layout-style">
#gv34OrientationPanel{margin:0 0 6px!important;border-color:#9b8130!important;background:#161207!important}
#gv34OrientationTitle{margin:0 0 5px;color:#ffd166;font:900 10px/1.2 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:.5px}
#gv34OrientationPanel .controls{margin-top:0!important}
@media(max-width:700px){#gv34OrientationPanel{margin:0 0 4px!important;padding:5px!important}#gv34OrientationTitle{font-size:9px;margin-bottom:3px}}
</style>
<script>(()=>{'use strict';
function installOrientationBelowImages(){
  const compare=document.querySelector('main > section.compare')||document.querySelector('.compare');
  const readouts=document.querySelector('main > section.readouts')||document.querySelector('.readouts');
  const rot=document.getElementById('rotRange');
  const rotRow=rot?.closest?.('.controls');
  if(!compare||!readouts||!rotRow)return false;
  let panel=document.getElementById('gv34OrientationPanel');
  if(!panel){
    panel=document.createElement('section');
    panel.id='gv34OrientationPanel';
    panel.className='panel';
    const title=document.createElement('div');
    title.id='gv34OrientationTitle';
    title.textContent='ORIENTATION / ANGLE ADJUSTMENT';
    panel.appendChild(title);
  }
  if(rotRow.parentElement!==panel)panel.appendChild(rotRow);
  const applyRot=[...document.querySelectorAll('button')].find(b=>/^APPLY\s+ROT(?:ATION)?$/i.test((b.textContent||'').trim()));
  const applyRow=applyRot?.closest?.('.controls');
  if(applyRow&&applyRow!==rotRow&&applyRow.parentElement!==panel)panel.appendChild(applyRow);
  if(compare.nextElementSibling!==panel)compare.insertAdjacentElement('afterend',panel);
  if(panel.nextElementSibling!==readouts)panel.insertAdjacentElement('afterend',readouts);
  panel.dataset.gvLayout='images-then-orientation-then-readouts';
  console.log('[GV0034][LAYOUT] images -> orientation controls -> source/live readouts');
  return true;
}
let tries=0;
function enforce(){tries++;if(installOrientationBelowImages()||tries>=20)return;setTimeout(enforce,250)}
enforce();
setTimeout(installOrientationBelowImages,1000);
setTimeout(installOrientationBelowImages,3000);
})();</script>`;

function normalizeIdentity(html){
  return html
    .replaceAll('GV 0033 LIVE','GV 0034 LIVE')
    .replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0033','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0034')
    .replaceAll('2026-08-29 19:38:03 COT',BUILD_STAMP_COLOMBIA);
}
function injectBeforeBodyEnd(html){const i=html.lastIndexOf('</body>');if(i<0)return null;return html.slice(0,i)+LAYOUT_PATCH+html.slice(i)}

async function page(request,env){
  const r=await gv0033.fetch(request,env);
  let h=normalizeIdentity(await r.text());
  const out=injectBeforeBodyEnd(h);
  if(out==null)return new Response('0034 STARTUP ERROR: body anchor missing',{status:500});
  const headers=new Headers(r.headers);
  headers.set('content-type','text/html; charset=utf-8');
  headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');
  headers.set('pragma','no-cache');
  headers.set('expires','0');
  headers.set('x-gv-revision',REV);
  headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);
  headers.set('x-gv-layout-order','images-orientation-source-live');
  return new Response(out,{status:r.status,headers});
}
async function health(request,env){
  const r=await gv0033.fetch(request,env);let data={};try{data=await r.json()}catch{}
  data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0034',inherited_from:'0033',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',layout_order:['images','orientation-angle-controls','source-image-data','live-validation-data'],layout_rule:'rotRange row physically moved immediately after .compare and before .readouts'};
  return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA,'x-gv-layout-order':'images-orientation-source-live'}});
}
export default {async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(request,env);return gv0033.fetch(request,env)}};
