import gv0029 from './gv-cloudflare-auto-astrometry-curator-0029-worker.js';

const REV='0040';
const BUILD_STAMP_COLOMBIA='2026-08-29 20:19:00 COT';
const BUILD_STAMP_ISO='2026-08-29T20:19:00-05:00';

const BINDING=String.raw`
function gv0040EnsureLayout(){
  const compare=document.querySelector('main > section.compare')||document.querySelector('.compare');
  const readouts=document.querySelector('main > section.readouts')||document.querySelector('.readouts');
  const rot=document.getElementById('rotRange'),row=rot?.closest?.('.controls');
  if(!compare||!readouts||!row)return false;
  let panel=document.getElementById('gv40OrientationPanel');
  if(!panel){panel=document.createElement('section');panel.id='gv40OrientationPanel';panel.className='panel';const t=document.createElement('div');t.id='gv40OrientationTitle';t.textContent='ORIENTATION / ANGLE ADJUSTMENT';panel.appendChild(t)}
  if(row.parentElement!==panel)panel.appendChild(row);
  if(compare.nextElementSibling!==panel)compare.insertAdjacentElement('afterend',panel);
  if(panel.nextElementSibling!==readouts)panel.insertAdjacentElement('afterend',readouts);
  return true;
}
function gv0040MachineCandidate(){
  return [...document.querySelectorAll('button')].find(b=>/APPLY MACHINE PREDICTION|LEGACY SIFT DISABLED|APPLY MACHINE ASTROMETRY|MACHINE APPLIED|MACHINE SOLVING/i.test((b.textContent||'').trim()))||document.querySelector('button[data-gv0040-machine="1"]')||null;
}
function gv0040InstallMachineButton(){
  let b=gv0040MachineCandidate();if(!b)return false;
  if(b.dataset.gv0040Machine!=='1'){
    const c=b.cloneNode(true);b.replaceWith(c);b=c;b.dataset.gv0040Machine='1';
    console.log('[GV0040][BUTTON] legacy machine button listeners stripped by clone');
  }
  if(!busy&&!/MACHINE SOLVING/i.test(b.textContent||'')){b.disabled=false;b.textContent='★ APPLY MACHINE ASTROMETRY'}
  return true;
}
function gv0040StartView(){
  const c=currentCenter(),f=currentFov(),r=currentRot();
  return {ra:c?.[0]??null,dec:c?.[1]??null,fov:Number.isFinite(Number(f))?Number(f):null,rot:Number.isFinite(Number(r))?Number(r):null,capturedAt:new Date().toISOString()};
}
window.addEventListener('click',e=>{
  const b=e.target?.closest?.('button[data-gv0040-machine="1"]');
  if(!b||busy)return;
  e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();
  const start=gv0040StartView();window.__gv0040ManualStart=start;
  console.log('[GV0040][BUTTON] direct same-scope Gaia solve start; live view preserved until gate',start);
  b.textContent='★ MACHINE SOLVING…';b.disabled=true;
  const al=Q('#analysisLog');if(al)al.textContent='[0040] MACHINE START ACCEPTED · CURRENT ALADIN HELD · RA '+(start.ra??'—')+' · DEC '+(start.dec??'—')+' · FOV '+(start.fov??'—')+'° · ROT '+(start.rot??'—')+'°\nGAIA stellar solve is running. No legacy prediction handler is allowed to reposition Aladin.';
  gateBox('GAIA SOLVING · CURRENT CENTER / FOV / ROTATION PRESERVED UNTIL STELLAR GATE','warn');
  Promise.resolve(analyze0029()).then(()=>{
    const verified=/GAIA VERIFIED/i.test(Q('#predConfidence')?.textContent||'');
    b.disabled=false;b.textContent=verified?'★ MACHINE APPLIED · GAIA VERIFIED':'★ APPLY MACHINE ASTROMETRY';
    console.log('[GV0040][BUTTON] Gaia solve returned',{verified,start,live:{center:currentCenter(),fov:currentFov(),rot:currentRot()}});
  }).catch(err=>{
    b.disabled=false;b.textContent='★ APPLY MACHINE ASTROMETRY';
    gateBox('MACHINE START FAILED · '+String(err?.message||err),'bad');
    console.error('[GV0040][BUTTON] Gaia solve rejected',err);
  });
},true);

gv0040EnsureLayout();gv0040InstallMachineButton();
setInterval(()=>{gv0040EnsureLayout();gv0040InstallMachineButton()},250);
console.log('[GV0040] direct same-script Gaia binding installed; final solution contract = RA/DEC/FOV/ROTATION');
`;

const STYLE=String.raw`<style id="gv40-style">
#gv40OrientationPanel{margin:0 0 6px!important;border-color:#9b8130!important;background:#161207!important}
#gv40OrientationTitle{margin:0 0 5px;color:#ffd166;font:900 10px/1.2 ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:.5px}
</style>`;
const BANNER=String.raw`<div id="gv40DeployStamp" style="position:relative;z-index:9999;padding:5px 8px;background:#08251a;border-bottom:1px solid #2f8b60;color:#8fffc0;font:900 10px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace">GV 0040 LIVE · BUILD 2026-08-29 20:19:00 COT · DIRECT SAME-SCRIPT GAIA · SOLVES RA/DEC/FOV/ROTATION</div>`;

function extractScriptContaining(html,needle){
  const n=html.indexOf(needle);if(n<0)return{html,found:false,code:''};
  const s=html.lastIndexOf('<script',n),open=html.indexOf('>',s),e=html.indexOf('</script>',n);
  if(s<0||open<0||e<0)return{html,found:false,code:''};
  return{html:html.slice(0,s)+html.slice(e+9),found:true,code:html.slice(open+1,e)};
}
function stripScriptContaining(html,needle){
  const x=extractScriptContaining(html,needle);return{html:x.html,removed:x.found};
}
function findCoreScript(html){
  let pos=0;
  while(true){
    const s=html.indexOf('<script',pos);if(s<0)return null;
    const open=html.indexOf('>',s),e=html.indexOf('</script>',open);if(open<0||e<0)return null;
    const code=html.slice(open+1,e);
    if(code.includes('showCurrent')&&code.includes('currentRot')&&code.includes('hardAim'))return{s,open,e,code};
    pos=e+9;
  }
}
function augmentSolver(code){
  const end=code.lastIndexOf('})();');
  if(end<0)return null;
  return code.slice(0,end)+BINDING+'\n'+code.slice(end);
}
function injectIntoCore(html,code){
  const core=findCoreScript(html);if(!core)return null;
  return html.slice(0,core.e)+'\n'+code+'\n'+html.slice(core.e);
}
function injectPresentation(html){
  let h=html;
  const hs=h.indexOf('</head>');if(hs>=0)h=h.slice(0,hs)+STYLE+h.slice(hs);
  const m=h.match(/<body(?:\s[^>]*)?>/i);if(m){const i=m.index+m[0].length;h=h.slice(0,i)+BANNER+h.slice(i)}
  return h.replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0029','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0040');
}

async function page(request,env){
  const r=await gv0029.fetch(request,env);let h=await r.text();
  const solver=extractScriptContaining(h,'const oldShow29=showCurrent;');
  if(!solver.found)return new Response('0040 STARTUP ERROR: 0029 Gaia solver script not found',{status:500});
  h=solver.html;
  const hotfix=stripScriptContaining(h,'let gv29LastKey=');h=hotfix.html;
  const augmented=augmentSolver(solver.code);
  if(!augmented)return new Response('0040 STARTUP ERROR: Gaia solver IIFE end not found',{status:500});
  const injected=injectIntoCore(h,augmented);
  if(!injected)return new Response('0040 STARTUP ERROR: core curator script containing showCurrent/currentRot/hardAim not found',{status:500});
  h=injectPresentation(injected);
  const headers=new Headers(r.headers);
  headers.set('content-type','text/html; charset=utf-8');
  headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('pragma','no-cache');headers.set('expires','0');
  headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);
  headers.set('x-gv-machine-scope','0029-gaia-rehomed-inside-core-script');
  headers.set('x-gv-machine-button','legacy-button-cloned-and-direct-same-scope-bound');
  headers.set('x-gv-pre-solve-movement','none-from-machine-button');
  headers.set('x-gv-machine-solution-contract','ra-dec-fov-rotation-from-stellar-transform');
  headers.set('x-gv-0029-hotfix-removed',hotfix.removed?'yes':'no');
  return new Response(h,{status:r.status,headers});
}
async function health(request,env){
  const r=await gv0029.fetch(request,env);let data={};try{data=await r.json()}catch{}
  data={...data,ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0040',direct_from:'0029',bypasses:['0030','0031','0032','0033','0034','0035','0036','0037','0038','0039'],build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',architecture:'0029-gaia-solver-rehomed-into-core-curator-script',scope_anchor:'script-containing-showCurrent-currentRot-hardAim',machine_button:'legacy-machine-button-cloned-listeners-stripped-window-capture-direct-analyze0029',pre_solve_movement:'none-from-machine-button',manual_start_view:['ra','dec','fov','rotation'],manual_start_role:'preserved-human-starting-view-not-acceptance-proof',machine_solution_contract:['ra','dec','fov','rotation'],fov_source:'gaia-stellar-transform-of-left-source-image',astrometry_cross_check:true,fail_closed:true,thresholds:{min_stellar_inliers:15,min_inlier_ratio:0.60,max_rms_px:2.5,max_centroid_residual_px:2.0},layout_order:['images','orientation-angle-controls','source-image-data','live-validation-data']};
  return new Response(JSON.stringify(data,null,2),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-gv-revision':REV,'x-gv-build-colombia':BUILD_STAMP_COLOMBIA}});
}
export default{async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(request,env);return gv0029.fetch(request,env)}};
