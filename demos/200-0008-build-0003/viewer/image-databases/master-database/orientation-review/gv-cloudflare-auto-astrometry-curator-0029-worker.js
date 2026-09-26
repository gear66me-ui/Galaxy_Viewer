import {htmlResponse} from './gv0029-ui.js';
import {REV,json,catalog,predictionsDisabled,predictionDiagnostics,image,solve,status,gaia} from './gv0029-api.js';

const HOTFIX=String.raw`<style>
#gv29Sync{margin:0 6px 6px;padding:6px 8px;border:1px solid #42566f;border-radius:8px;background:#09121f;font:800 10px/1.35 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap;word-break:break-word}
#gv29Sync.good{border-color:#2f8b60;color:#57e39b}#gv29Sync.warn{border-color:#9b8130;color:#ffd166}#gv29Sync.bad{border-color:#a94750;color:#ff7575}
#gv29ControlsHotfix{scroll-margin-top:56px}
@media(max-width:700px){#gv29Sync{font-size:9px;margin:0 4px 4px;padding:5px 6px}#gv29ControlsHotfix{padding:5px;margin-bottom:5px}#gv29ControlsHotfix .controls{gap:3px}#gv29ControlsHotfix button{padding:6px 7px;font-size:10px}#gv29ControlsHotfix .deg{width:60px;padding:4px}#gv29ControlsHotfix .controls input[type=range]{min-width:90px}}
</style>
<script>(()=>{'use strict';
let gv29LastKey='',gv29PendingImageKey='',gv29LoadedImageKey='',gv29AladinKey='',gv29Queued=false,gv29Retry=0;
const q=s=>document.querySelector(s);
function safeCurrent(){try{return typeof current==='function'?current():null}catch{return null}}
function key(){const x=safeCurrent();return String(x?.key||'')}
function nm(x){try{return typeof nameOf==='function'?nameOf(x.r):String(x?.r?.displayName||x?.r?.name||x?.r?.title||'')}catch{return''}}
function expectedImage(x){try{return typeof imageOf==='function'?String(imageOf(x.r)||''):''}catch{return''}}
function live(){let c=null,f=null,r=null;try{c=typeof currentCenter==='function'?currentCenter():null}catch{}try{f=typeof currentFov==='function'?currentFov():null}catch{}try{r=typeof currentRot==='function'?currentRot():null}catch{}return{c,f,r}}
function fmt(v,d=6){return Number.isFinite(Number(v))?Number(v).toFixed(d):'—'}
function setMessage(text,bad=false){const s=q('#status');if(s){s.textContent=text;s.className='status '+(bad?'error':'analyzing')}const g=q('#gv29Gate');if(g){g.textContent=text;g.className=bad?'bad':'warn'}}
function installLayout(){const read=q('.readouts'),controls=q('#analyzeBtn')?.closest('.panel');if(!read||!controls)return;controls.id='gv29ControlsHotfix';let box=q('#gv29Sync');if(!box){box=document.createElement('div');box.id='gv29Sync';read.insertAdjacentElement('afterend',box)}if(box.nextElementSibling!==controls)box.insertAdjacentElement('afterend',controls);const img=q('#published');if(img&&!img.dataset.gv29Bound){img.dataset.gv29Bound='1';const markPending=()=>{gv29PendingImageKey=key();gv29LoadedImageKey='';updateSync()};new MutationObserver(markPending).observe(img,{attributes:true,attributeFilter:['src']});img.addEventListener('load',()=>{gv29LoadedImageKey=gv29PendingImageKey||key();updateSync()});img.addEventListener('error',()=>{gv29LoadedImageKey='';updateSync()});if(img.getAttribute('src')){gv29PendingImageKey=key();if(img.complete&&img.naturalWidth>0)gv29LoadedImageKey=gv29PendingImageKey}}
}
function updateSync(){installLayout();const box=q('#gv29Sync'),x=safeCurrent();if(!box||!x)return;const k=String(x.key||'');if(k!==gv29LastKey){gv29LastKey=k;gv29PendingImageKey=k;gv29LoadedImageKey='';gv29AladinKey=''}let verified=false;try{verified=typeof targetVerified!=='undefined'&&!!targetVerified}catch{}if(verified)gv29AladinKey=k;const img=q('#published'),leftReady=gv29LoadedImageKey===k&&!!img?.complete&&Number(img?.naturalWidth||0)>0,aladinReady=gv29AladinKey===k&&verified,L=live(),catalog=String(x?.c?.name||''),archive=String(x?.r?.archiveId||x?.r?.id||x?.r?.designation||'—'),name=nm(x),actual=String(img?.currentSrc||img?.src||''),expected=expectedImage(x);let state='MISMATCHED / SYNCING',klass='bad';if(leftReady&&aladinReady){state='MATCHED — LEFT IMAGE + ALADIN ARE THE SAME RECORD';klass='good'}else if(leftReady){state='SYNCING — LEFT IMAGE LOADED; ALADIN STILL POSITIONING';klass='warn'}else if(aladinReady){state='SYNCING — ALADIN READY; LEFT IMAGE STILL LOADING';klass='warn'}box.className=klass;box.textContent='LEFT IMAGE: '+catalog+' · '+archive+' · '+name+'\nLEFT KEY: '+(gv29LoadedImageKey||'LOADING')+'\nLEFT URL: '+(actual||expected||'—')+'\nALADIN: '+k+' · RA '+fmt(L.c?.[0])+' · DEC '+fmt(L.c?.[1])+' · FOV '+fmt(L.f)+'° · ROT '+fmt(L.r,2)+'°\nSTATUS: '+state}
function isBusy(){try{return typeof busy!=='undefined'&&!!busy}catch{return false}}
function runGaia(){const btn=q('#analyzeBtn');if(!btn)return;installLayout();if(isBusy()){gv29Queued=true;gv29Retry++;setMessage('GAIA BUTTON RECEIVED — WAITING FOR CURRENT RECORD');if(gv29Retry<=40)setTimeout(runGaia,250);else{gv29Queued=false;gv29Retry=0;setMessage('0029 BUTTON ERROR — CURATOR REMAINED BUSY',true)}return}gv29Queued=false;gv29Retry=0;btn.disabled=false;try{if(typeof analyzeCurrent!=='function')throw Error('analyzeCurrent unavailable');setMessage('GAIA BUTTON RECEIVED — STARTING STELLAR SOLVE');const p=analyzeCurrent();if(p&&typeof p.catch==='function')p.catch(e=>setMessage('GAIA SOLVE ERROR — '+String(e?.message||e),true))}catch(e){setMessage('0029 BUTTON BRIDGE ERROR — '+String(e?.message||e),true)}}
document.addEventListener('click',e=>{const b=e.target?.closest?.('#analyzeBtn');if(!b)return;if(!q('#gv29Gate')&&!/GAIA/i.test(b.textContent||''))return;e.preventDefault();e.stopImmediatePropagation();runGaia()},true);
setInterval(()=>{installLayout();updateSync();const b=q('#analyzeBtn');if(b&&!isBusy()){b.disabled=false;if(!/GAIA/i.test(b.textContent||''))b.textContent='GAIA STELLAR ALIGN'}},300);
window.addEventListener('error',e=>{if(String(e?.message||'').includes('0029')||q('#gv29Gate'))setMessage('0029 UI ERROR — '+String(e?.message||'unknown error'),true)});
setTimeout(()=>{installLayout();updateSync();console.log('[GV0029][HOTFIX] button capture + identity sync + compact controls installed')},100);
})();</script>`;

async function page(){
  const r=await htmlResponse();
  let h=await r.text();
  const i=h.lastIndexOf('</body>');
  if(i<0)return new Response('0029 STARTUP ERROR: hotfix body anchor missing',{status:500});
  h=h.slice(0,i)+HOTFIX+h.slice(i);
  const headers=new Headers(r.headers);
  headers.set('content-type','text/html; charset=utf-8');
  headers.set('cache-control','no-store');
  return new Response(h,{status:r.status,headers});
}

export default {async fetch(request,env){
  const u=new URL(request.url);
  if(u.pathname==='/'||u.pathname==='/index.html') return page();
  if(u.pathname==='/api/health') return json({
    ok:true,
    revision:REV,
    service:'gv-cloudflare-auto-astrometry-curator-0029',
    key_source:'server-secret',
    key_configured:Boolean(String(env?.ASTROMETRY_API_KEY||'').trim()),
    architecture:'gaia-stellar-gated',
    fail_closed:true,
    thresholds:{min_stellar_inliers:15,min_inlier_ratio:.60,max_rms_px:2.5,max_centroid_residual_px:2.0,max_rotation_disagreement_deg:5,max_fov_relative_disagreement:.15,max_center_disagreement_fraction_of_fov:.10},
    features:['standalone-0029','catalog-navigation','source-and-live-data','manual-rotation','legacy-sift-automation-disabled','point-source-detection','gaia-dr3-vizier','triangle-asterism-ransac','mandatory-stellar-validation-gate','astrometry-independent-cross-check','fail-closed-disagreement','match-circles-and-ids-no-lines','human-gold-curation','button-capture-hotfix','left-right-identity-sync','compact-controls-under-readouts','diagnostics']
  });
  if(u.pathname==='/api/catalog') return catalog(u);
  if(u.pathname==='/api/predictions') return predictionsDisabled();
  if(u.pathname==='/api/predictions-diagnostic') return predictionDiagnostics();
  if(u.pathname==='/api/image') return image(u,request);
  if(u.pathname==='/api/solve') return solve(request,env);
  if(u.pathname==='/api/status') return status(u);
  if(u.pathname==='/api/gaia') return gaia(u);
  return new Response('Not found',{status:404});
}};
