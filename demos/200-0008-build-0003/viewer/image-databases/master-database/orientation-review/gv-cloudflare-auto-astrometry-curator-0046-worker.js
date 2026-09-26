import base0045 from './gv-cloudflare-auto-astrometry-curator-0045-worker.js';
import gaia0029 from './gv-cloudflare-auto-astrometry-curator-0029-worker.js';

const REV='0046';
const BUILD_STAMP_COLOMBIA='2026-08-30 15:39:00 COT';
const BUILD_STAMP_ISO='2026-08-30T15:39:00-05:00';
const LEGACY_PREDICTIONS_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/orientation-review/gv-registration-predictions-0001.json';

const STYLE=String.raw`<style id="gv46-style">
#gv46BuildStamp{position:relative;z-index:9999;padding:5px 8px;background:#08251a;border-bottom:1px solid #2f8b60;color:#8fffc0;font:900 10px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace}
#gv46Recovery{margin:6px 8px;padding:7px 9px;border:1px solid #2f8b60;border-radius:8px;background:#0d2c20;color:#8fffc0;font:900 10px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap}
#gv46AstroProgress{margin:6px 8px;padding:7px 9px;border:1px solid #384d67;border-radius:8px;background:#09121f;color:#d9e8ff;font:800 11px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap;min-height:34px}
#gv46MatchInfo{margin:0 8px 8px;padding:6px 8px;border:1px solid #384d67;border-radius:8px;background:#09121f;color:#d9e8ff;font:800 10px/1.35 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap}
#gv46SourceStars,#gv46AladinStars{position:absolute;inset:0;width:100%;height:100%;z-index:31;pointer-events:none}
.compare>.gv46RotRow{grid-column:2;align-self:start;margin:0!important}
.compare>#gv26rot.gv46RotReadout{grid-column:1/-1;margin:0!important}
@media(max-width:700px){.compare{grid-template-columns:1fr!important}.compare>.gv46RotRow,.compare>#gv26rot.gv46RotReadout{grid-column:1}}
</style>`;

const BANNER='<div id="gv46BuildStamp">GV 0046 LIVE · BUILD '+BUILD_STAMP_COLOMBIA+'</div>';

const CLIENT=String.raw`<script>(()=>{'use strict';
const q=s=>document.querySelector(s);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let gv46MatchState=null,gv46LastKey='';

function status46(text,kind='analyzing'){
  const s=q('#status');
  if(s){s.textContent=text;s.className='status '+kind}
}
function diag46(stage,msg,data){
  try{window.gv0023Diag?.(stage,msg,data)}catch{}
  try{console.log('[GV0046]['+stage+']',msg,data||'')}catch{}
}
function install0045PreservedClient(){
  const published=q('#published');
  if(published&&!published.dataset.gv46DimsBound){
    published.dataset.gv46DimsBound='1';
    published.addEventListener('load',()=>{
      const d=q('#catDims');
      if(d&&published.naturalWidth&&published.naturalHeight)d.textContent=published.naturalWidth+' × '+published.naturalHeight+' px';
    });
  }
  const survey=q('#survey');
  if(survey&&!survey.dataset.gv46SurveyBound){
    survey.dataset.gv46SurveyBound='1';
    survey.addEventListener('change',()=>{
      const id=String(survey.value||'').trim();
      if(!id)return;
      if(typeof aladin?.setBaseImageLayer==='function')aladin.setBaseImageLayer(id);
      else if(typeof aladin?.setImageSurvey==='function')aladin.setImageSurvey(id);
    });
  }
  const missionDefault=q('#missionDefault');
  if(missionDefault&&!missionDefault.dataset.gv46MissionDefaultBound){
    missionDefault.dataset.gv46MissionDefaultBound='1';
    missionDefault.addEventListener('click',()=>setTimeout(()=>survey?.dispatchEvent(new Event('change',{bubbles:true})),0));
  }
}

function ensureRecovery46(){
  let e=q('#gv46Recovery');if(e)return e;e=document.createElement('div');e.id='gv46Recovery';e.textContent='0046 RECOVERY BASELINE · LEGACY SIFT MOVEMENT DISABLED · 0045 CATALOG / SOURCE IMAGE / ALADIN REPAIRS PRESERVED · GAIA STELLAR MACHINE SOLVE ENABLED';const host=q('#gv26bar')||q('main');host?.insertAdjacentElement('afterend',e);return e;
}

function ensureProgress46(){
  let box=q('#gv46AstroProgress');
  if(box)return box;
  box=document.createElement('div');box.id='gv46AstroProgress';box.setAttribute('role','status');box.setAttribute('aria-live','polite');
  const host=q('#gv26bar')||q('main');host?.insertAdjacentElement('afterend',box);return box;
}
const progress46={lines:[]};
window.gv46Progress=function(stage,detail='',kind='analyzing'){
  const label=String(stage||'').trim();if(!label)return;
  const text=detail?label+' · '+detail:label;
  progress46.lines.push(text);if(progress46.lines.length>18)progress46.lines.splice(0,progress46.lines.length-18);
  const box=ensureProgress46();if(box){box.dataset.stage=label;box.textContent=progress46.lines.join('\n')}
  status46(text,kind);
  const log=q('#analysisLog');if(log)log.textContent=progress46.lines.join('\n');
};
function resetProgress46(){progress46.lines=[];const b=ensureProgress46();if(b)b.textContent='MACHINE ASTROMETRY READY'}

function sourceRect46(img){
  const W=img.clientWidth,H=img.clientHeight,nw=img.naturalWidth||W,nh=img.naturalHeight||H;
  const scale=Math.min(W/nw,H/nh),w=nw*scale,h=nh*scale;return{x:(W-w)/2,y:(H-h)/2,w,h};
}
function ensureCanvas46(id,host){
  let c=q('#'+id);if(!c){c=document.createElement('canvas');c.id=id;host.style.position='relative';host.appendChild(c)}
  c.width=Math.max(1,host.clientWidth);c.height=Math.max(1,host.clientHeight);return c;
}
function matchPairs46(ev){
  return (ev?.pairs||[]).map((p,i)=>({id:'M'+String(i+1).padStart(2,'0'),source:p.s,gaia:p.g,residual:Number(p.d)}));
}
function world46(ra,dec){
  try{const p=aladin?.world2pix?.(ra,dec);return Array.isArray(p)&&Number.isFinite(Number(p[0]))&&Number.isFinite(Number(p[1]))?{x:Number(p[0]),y:Number(p[1])}:null}catch{return null}
}
function info46(pair){
  let e=q('#gv46MatchInfo');if(!e){e=document.createElement('div');e.id='gv46MatchInfo';const host=q('#gv26rot')||q('#gv46AstroProgress')||q('main');host?.insertAdjacentElement('afterend',e)}
  if(!pair){e.textContent='MATCH DETAILS · select M01/M02/etc. on either image';return}
  e.textContent='MATCH '+pair.id+' · Gaia DR3 '+String(pair.gaia?.id||'—')+'\nsource '+Number(pair.source?.x).toFixed(1)+','+Number(pair.source?.y).toFixed(1)+' px · Gaia RA '+Number(pair.gaia?.ra).toFixed(7)+' DEC '+Number(pair.gaia?.dec).toFixed(7)+' · residual '+Number(pair.residual).toFixed(2)+' px';
}
function drawSource46(){
  const st=gv46MatchState,img=q('#published'),host=img?.parentElement;if(!st||!img||!host)return;
  const c=ensureCanvas46('gv46SourceStars',host),g=c.getContext('2d'),r=sourceRect46(img),sx=r.w/st.w,sy=r.h/st.h;
  g.clearRect(0,0,c.width,c.height);g.font='10px ui-monospace,monospace';g.lineWidth=1.2;
  const confirmed=new Map(st.pairs.map(p=>[p.source,p]));
  for(const s of st.det){const x=r.x+s.x*sx,y=r.y+s.y*sy,p=confirmed.get(s);g.beginPath();g.arc(x,y,p?(st.selected===p.id?8:6):3,0,Math.PI*2);g.strokeStyle=p?(st.selected===p.id?'#ffd166':'#42dcff'):'rgba(210,220,235,.45)';g.stroke();if(!p){g.beginPath();g.moveTo(x-2,y-2);g.lineTo(x+2,y+2);g.moveTo(x+2,y-2);g.lineTo(x-2,y+2);g.stroke()}else{g.fillStyle=st.selected===p.id?'#ffd166':'#eef4ff';g.fillText(p.id,x+7,y-5)}}
  st.sourcePixels=st.pairs.map(p=>({p,x:r.x+p.source.x*sx,y:r.y+p.source.y*sy}));
}
function drawAladin46(){
  const st=gv46MatchState,al=q('#aladin'),host=al?.parentElement;if(!st||!al||!host)return;
  const c=ensureCanvas46('gv46AladinStars',host),g=c.getContext('2d');g.clearRect(0,0,c.width,c.height);g.font='10px ui-monospace,monospace';g.lineWidth=1.2;
  const confirmed=new Map(st.pairs.map(p=>[p.gaia,p]));
  for(const s of st.G){const z=world46(s.ra,s.dec);if(!z)continue;const p=confirmed.get(s);g.beginPath();g.arc(z.x,z.y,p?(st.selected===p.id?8:6):3,0,Math.PI*2);g.strokeStyle=p?(st.selected===p.id?'#ffd166':'#42dcff'):'rgba(112,184,255,.35)';g.stroke();if(!p){g.beginPath();g.moveTo(z.x-2,z.y-2);g.lineTo(z.x+2,z.y+2);g.moveTo(z.x+2,z.y-2);g.lineTo(z.x-2,z.y+2);g.stroke()}else{g.fillStyle=st.selected===p.id?'#ffd166':'#eef4ff';g.fillText(p.id,z.x+7,z.y-5)}}
  const center=world46(st.base.ra,st.base.dec),cd=Math.max(.05,Math.cos(st.base.dec*Math.PI/180)),edge=world46(st.base.ra+st.radius/cd,st.base.dec);
  if(center&&edge){g.beginPath();g.arc(center.x,center.y,Math.hypot(edge.x-center.x,edge.y-center.y),0,Math.PI*2);g.setLineDash([4,4]);g.strokeStyle='rgba(138,180,255,.7)';g.stroke();g.setLineDash([])}
  const solved=world46(st.sol.ra,st.sol.dec);if(solved){g.strokeStyle='#57e39b';g.beginPath();g.moveTo(solved.x-8,solved.y);g.lineTo(solved.x+8,solved.y);g.moveTo(solved.x,solved.y-8);g.lineTo(solved.x,solved.y+8);g.stroke()}
  st.aladinPixels=st.pairs.map(p=>{const z=world46(p.gaia.ra,p.gaia.dec);return z?{p,x:z.x,y:z.y}:null}).filter(Boolean);
}
function redraw46(){drawSource46();drawAladin46()}
window.gv46ClearAstro=function(){gv46MatchState=null;for(const id of ['gv46SourceStars','gv46AladinStars']){const c=q('#'+id);if(c)c.getContext('2d').clearRect(0,0,c.width,c.height)}info46(null)};
window.gv46RenderMatches=function(data){
  gv46MatchState={pairs:matchPairs46(data.ev),det:data.det?.points||[],G:data.G||[],w:data.w,h:data.h,base:data.base,radius:data.radius,sol:data.sol,selected:''};redraw46();info46(null);
};
function selectNear46(list,x,y){let best=null,bd=14;for(const z of list||[]){const d=Math.hypot(z.x-x,z.y-y);if(d<bd){bd=d;best=z.p}}if(best&&gv46MatchState){gv46MatchState.selected=best.id;info46(best);redraw46()}}
function bindPairClicks46(){
  const imgHost=q('#published')?.parentElement,alHost=q('#aladin')?.parentElement;
  if(imgHost&&!imgHost.dataset.gv46PairClick){imgHost.dataset.gv46PairClick='1';imgHost.addEventListener('click',e=>{if(!gv46MatchState)return;const r=imgHost.getBoundingClientRect();selectNear46(gv46MatchState.sourcePixels,e.clientX-r.left,e.clientY-r.top)},true)}
  if(alHost&&!alHost.dataset.gv46PairClick){alHost.dataset.gv46PairClick='1';alHost.addEventListener('click',e=>{if(!gv46MatchState)return;const r=alHost.getBoundingClientRect();selectNear46(gv46MatchState.aladinPixels,e.clientX-r.left,e.clientY-r.top)},true)}
}

function sourceRotation46(){try{const x=typeof current==='function'?current():null,r=x?.r||x||null,v=r&&typeof rotOf==='function'?Number(rotOf(r)):NaN;return Number.isFinite(v)?v:null}catch{return null}}
function liveRotation46(){try{if(typeof currentRot==='function'){const v=Number(currentRot());if(Number.isFinite(v))return v}}catch{}for(const m of ['getRotation','getViewRotation','getRoll'])try{const v=Number(aladin?.[m]?.());if(Number.isFinite(v))return v}catch{}return null}
function mirror46(){const e=q('#mirrorState,#mirror,#mirrorX');return !!e&&/ON|TRUE|MIRROR/i.test(String(e.textContent||e.value||''))}
function rotText46(v){return Number.isFinite(v)?v.toFixed(2)+'°':'—'}
function updateRotation46(){const s=q('#gv26srot'),a=q('#gv26arot');if(s)s.textContent=rotText46(sourceRotation46());if(a)a.textContent=rotText46(liveRotation46())+' · mirror '+(mirror46()?'ON':'OFF')}
function installLayout46(){
  const compare=q('main > section.compare')||q('.compare'),aladinView=q('#aladin')?.closest?.('.viewbox'),rot=q('#rotRange'),rotRow=rot?.closest?.('.controls'),read=q('#gv26rot');
  if(compare&&aladinView&&rotRow){rotRow.classList.add('gv46RotRow');if(aladinView.nextElementSibling!==rotRow)aladinView.insertAdjacentElement('afterend',rotRow)}
  if(rotRow&&read){read.classList.add('gv46RotReadout');if(rotRow.nextElementSibling!==read)rotRow.insertAdjacentElement('afterend',read);const cells=read.querySelectorAll('.gv26cell');if(cells.length>=2){const l=cells[0].childNodes[0],r=cells[1].childNodes[0];if(l?.nodeType===Node.TEXT_NODE)l.nodeValue='SOURCE IMAGE ROTATION';if(r?.nodeType===Node.TEXT_NODE)r.nodeValue='ALADIN LIVE ROTATION'}}
  if(rot&&rot.dataset.gv46Live!=='1'){rot.dataset.gv46Live='1';rot.addEventListener('input',()=>requestAnimationFrame(updateRotation46));q('#rotDeg')?.addEventListener('change',()=>requestAnimationFrame(updateRotation46));for(const b of document.querySelectorAll('[data-r]'))b.addEventListener('click',()=>requestAnimationFrame(updateRotation46))}
  updateRotation46();
}

function saveToast46(text,good=true){let t=q('#gv46SaveAck');if(!t){t=document.createElement('div');t.id='gv46SaveAck';t.style.cssText='position:fixed;left:50%;top:64px;transform:translateX(-50%);z-index:2147483647;padding:8px 12px;border-radius:8px;background:#09121ff2;border:1px solid #57e39b;color:#eafff4;font:900 11px/1.3 ui-monospace,SFMono-Regular,Consolas,monospace;pointer-events:none';document.body.appendChild(t)}t.style.borderColor=good?'#57e39b':'#ff7575';t.textContent=text;t.hidden=false;clearTimeout(saveToast46.timer);saveToast46.timer=setTimeout(()=>{t.hidden=true},1600)}
function installSave46(){
  const b=q('#yesBtn');if(!b||b.dataset.gv46Save==='1'||typeof b.onclick!=='function')return;
  const nativeYes=b.onclick;b.dataset.gv46Save='1';b.onclick=function(ev){const x=typeof current==='function'?current():null,key=String(x?.key||''),m=mirror46();b.disabled=true;b.textContent='YES — SAVING…';try{nativeYes.call(this,ev);if(!key||typeof state==='undefined'||!state.saved?.[key])throw Error('accepted record not written');const rec=state.saved[key];rec.mirrorX=m;rec.confirmedMirrorX=m;if(typeof persist==='function')persist();saveToast46('SAVED LIVE ALADIN · RA '+Number(rec.confirmedRaDeg).toFixed(6)+' · DEC '+Number(rec.confirmedDecDeg).toFixed(6)+' · FOV '+Number(rec.confirmedFovDeg).toFixed(6)+'° · ROT '+Number(rec.aladinRotationDeg).toFixed(2)+'° · MIRROR '+(m?'ON':'OFF'),true)}catch(err){saveToast46('SAVE FAILED · '+String(err?.message||err),false)}finally{setTimeout(()=>{b.disabled=false;b.textContent='YES — SAVE + NEXT'},450)}};
}

function captureLive46(){
  let c=null,f=null,r=null;try{c=typeof currentCenter==='function'?currentCenter():null}catch{}try{f=typeof currentFov==='function'?currentFov():null}catch{}try{r=typeof currentRot==='function'?currentRot():null}catch{}
  return{ra:Number(c?.[0]),dec:Number(c?.[1]),fov:Number(f),rot:Number(r),mirror:mirror46(),survey:String(q('#survey')?.value||'').trim()};
}
function setCenter46(ra,dec){try{if(typeof setCenter==='function'){setCenter(ra,dec);return true}}catch{}try{if(typeof aladin?.gotoRaDec==='function'){aladin.gotoRaDec(ra,dec);return true}if(typeof aladin?.gotoObject==='function'){aladin.gotoObject(String(ra)+' '+String(dec));return true}}catch{}return false}
function setFov46(v){try{if(typeof setFov==='function'){setFov(v);return true}}catch{}try{if(typeof aladin?.setFoV==='function'){aladin.setFoV(v);return true}if(typeof aladin?.setFov==='function'){aladin.setFov(v);return true}}catch{}return false}
function setRot46(v){try{if(typeof setRot==='function'){setRot(v);return true}}catch{}for(const m of ['setRotation','setViewRotation','setRoll'])try{if(typeof aladin?.[m]==='function'){aladin[m](v);return true}}catch{}return false}
function setMirror46(v){try{if(typeof setMirror==='function'){setMirror(Boolean(v));return true}}catch{}if(!v)return true;return false}
function restoreLive46(s){return setCenter46(s.ra,s.dec)&&setFov46(s.fov)&&setRot46(s.rot)&&setMirror46(s.mirror)}
function rotDiff46(a,b){let d=Math.abs(Number(a)-Number(b));while(d>360)d-=360;if(d>180)d=360-d;return d}
function verifyLive46(s){const z=captureLive46(),ct=Math.max(.000001,s.fov*.00001),ft=Math.max(.000001,s.fov*.0001);return Math.abs(z.ra-s.ra)<=ct&&Math.abs(z.dec-s.dec)<=ct&&Math.abs(z.fov-s.fov)<=ft&&rotDiff46(z.rot,s.rot)<=.05&&z.mirror===s.mirror&&z.survey===s.survey}
async function refreshAladin46(){
  const b=q('#gv26refresh'),s=captureLive46();if(!b)return false;
  if(!Number.isFinite(s.ra)||!Number.isFinite(s.dec)||!Number.isFinite(s.fov)||s.fov<=0){status46('ALADIN REFRESH FAILED · LIVE VIEW UNREADABLE','error');return false}
  if(s.mirror&&typeof setMirror!=='function'){status46('ALADIN REFRESH FAILED · MIRROR STATE CANNOT BE SAFELY RESTORED','error');return false}
  b.disabled=true;b.textContent='↻ REFRESHING ALADIN…';status46('REFRESHING ALADIN · REBUILDING CANVAS','analyzing');diag46('REFRESH-ALADIN','rebuild begin',s);
  try{
    await A.init;const old=q('#aladin');if(!old)throw Error('Aladin host missing');const fresh=old.cloneNode(false);old.replaceWith(fresh);
    aladin=A.aladin('#aladin',{survey:s.survey||'P/DSS2/color',target:String(s.ra)+' '+String(s.dec),fov:s.fov,projection:'TAN',cooFrame:'ICRSd',lockNorthUp:false,northPoleOrientation:0,showReticle:true,showCooGrid:true,showZoomControl:true,showLayersControl:false,showFullscreenControl:false,inertia:false});
    if(s.survey){if(typeof aladin?.setBaseImageLayer==='function')aladin.setBaseImageLayer(s.survey);else if(typeof aladin?.setImageSurvey==='function')aladin.setImageSurvey(s.survey)}
    await sleep(350);if(!restoreLive46(s))throw Error('live state restore failed');await sleep(350);if(!restoreLive46(s))throw Error('live state second restore failed');await sleep(150);if(!verifyLive46(s))throw Error('live state verification failed');
    bindPairClicks46();redraw46();if(typeof updateLive==='function')updateLive();status46('ALADIN REFRESHED · LIVE VIEW RESTORED','ready');b.textContent='↻ ALADIN REFRESHED';diag46('REFRESH-ALADIN','rebuild verified',s);return true;
  }catch(err){status46('ALADIN REFRESH FAILED · '+String(err?.message||err),'error');diag46('REFRESH-FAIL',String(err?.message||err),s);return false}
  finally{setTimeout(()=>{b.disabled=false;b.textContent='↻ REFRESH ALADIN'},700)}
}
function installRefresh46(){const r=q('#gv26refresh'),c=q('#gv0024Recenter');if(r&&r.dataset.gv46Refresh!=='1'){r.dataset.gv46Refresh='1';r.textContent='↻ REFRESH ALADIN';r.onclick=refreshAladin46}if(c)c.textContent='◎ RE-CENTER ALADIN'}

function installMachine46(){
  let b=q('#gv26apply');if(!b)return;
  if(b.dataset.gv46Machine!=='1'){const c=b.cloneNode(true);b.replaceWith(c);b=c;b.dataset.gv46Machine='1';b.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();if(b.dataset.gv46Busy==='1')return;if(!window.__gv46GaiaSolverBound||typeof window.gv46RunGaia!=='function'){status46('MACHINE ASTROMETRY FAILED · GAIA SOLVER NOT BOUND','error');return}b.dataset.gv46Busy='1';b.disabled=true;b.textContent='★ MACHINE ASTROMETRY · SOLVING…';resetProgress46();status46('MACHINE ASTROMETRY STARTED','analyzing');Promise.resolve(window.gv46RunGaia()).catch(err=>window.gv46Progress('MACHINE ASTROMETRY FAILED',String(err?.message||err),'error')).finally(()=>{b.dataset.gv46Busy='0';b.disabled=false;const verified=/GAIA VERIFIED/i.test(q('#predConfidence')?.textContent||'');b.textContent=verified?'★ MACHINE ASTROMETRY · GAIA VERIFIED':'★ APPLY MACHINE ASTROMETRY';if(verified)setTimeout(()=>{if(b.dataset.gv46Busy!=='1')b.textContent='★ APPLY MACHINE ASTROMETRY'},1200)})},true)}
  if(b.dataset.gv46Busy!=='1'){b.disabled=false;if(!/SOLVING|GAIA VERIFIED/.test(b.textContent||''))b.textContent='★ APPLY MACHINE ASTROMETRY'}
}

function clearRecordDiagnostics46(){try{const k=String((typeof current==='function'?current():null)?.key||'');if(k&&k!==gv46LastKey){gv46LastKey=k;window.gv46ClearAstro?.();resetProgress46()}}catch{}}
function install46(){install0045PreservedClient();installLayout46();installSave46();installRefresh46();installMachine46();bindPairClicks46();ensureRecovery46();ensureProgress46();clearRecordDiagnostics46();updateRotation46()}
resetProgress46();install46();setInterval(()=>{install46();if(gv46MatchState)redraw46()},250);
console.log('[GV0046] interactive Gaia astrometry client installed');
})();</script>`;

function count(h,s){return h.split(s).length-1}
function replaceRequired(code,needle,replacement,label,report){
  const n=count(code,needle);report[label]=n;if(n!==1)return{ok:false,code};return{ok:true,code:code.replace(needle,replacement)};
}
function extractScriptContaining(html,needle){
  const n=html.indexOf(needle);if(n<0)return{html,found:false,code:''};const s=html.lastIndexOf('<script',n),open=html.indexOf('>',s),e=html.indexOf('</script>',n);if(s<0||open<0||e<0)return{html,found:false,code:''};return{html:html.slice(0,s)+html.slice(e+9),found:true,code:html.slice(open+1,e)};
}
function patchGaiaSolver(input){
  let code=input;const report={};let r;
  const patches=[
    ['progress-start',"const lines=[];try{const b=baseOf(x);","const lines=[];window.gv46ClearAstro?.();window.gv46Progress?.('MACHINE ASTROMETRY STARTED');try{const b=baseOf(x);"],
    ['source-loaded',"const im=await loadImage(imageOf(x.r));","const im=await loadImage(imageOf(x.r));window.gv46Progress?.('SOURCE IMAGE LOADED',im.naturalWidth+' × '+im.naturalHeight+' px');"],
    ['stars-detected',"const px=imageData29(im),det=detectPointSources29(px.data);","const px=imageData29(im),det=detectPointSources29(px.data);window.gv46Progress?.('DETECTING STARS',det.points.length+' FOUND');"],
    ['gaia-query',"const gj=await gaia29(x,b),G=gaiaPlane29(gj.stars||[],b.ra,b.dec);","window.gv46Progress?.('QUERYING GAIA DR3');const gj=await gaia29(x,b),G=gaiaPlane29(gj.stars||[],b.ra,b.dec);window.gv46Progress?.('GAIA CANDIDATES',String(G.length));"],
    ['stellar-matching',"const ev=stellarRansac29(G,det.points,px.w,px.h);","window.gv46Progress?.('MATCHING STELLAR PATTERNS');const ev=stellarRansac29(G,det.points,px.w,px.h);"],
    ['stellar-result',"const stellarPass=ev.inliers>=CFG.minInliers&&ev.ratio>=CFG.minRatio&&ev.rms<=CFG.maxRms&&ev.centroid<=CFG.maxCentroid;","window.gv46Progress?.('MATCHING STELLAR PATTERNS',ev.inliers+' STARS MATCHED · RMS '+ev.rms.toFixed(2)+' PX');const stellarPass=ev.inliers>=CFG.minInliers&&ev.ratio>=CFG.minRatio&&ev.rms<=CFG.maxRms&&ev.centroid<=CFG.maxCentroid;"],
    ['stellar-gate',"const sol=solutionFromTransform29(ev,b.ra,b.dec,px.w,px.h);","window.gv46Progress?.('STELLAR GATE','PASS · '+ev.inliers+' INLIERS','ready');const sol=solutionFromTransform29(ev,b.ra,b.dec,px.w,px.h);"],
    ['match-render',"drawMatches29(ev,px.w,px.h);","window.gv46RenderMatches?.({ev,det,G,w:px.w,h:px.h,base:b,radius:clamp(Math.max(.03,(b.fov||1.5)*.85),.01,2),sol});"],
    ['cross-start',"const astro=await astrometry29(x,b,im);","window.gv46Progress?.('ASTROMETRY.NET CROSS-CHECK');const astro=await astrometry29(x,b,im);"],
    ['cross-result',"const cross=compareAstrometry29(sol,astro);","const cross=compareAstrometry29(sol,astro);window.gv46Progress?.('ASTROMETRY.NET CROSS-CHECK',cross.available?('CENTER Δ '+cross.sep_deg.toFixed(6)+'° · ROT Δ '+cross.rotation_diff_deg.toFixed(2)+'°'):('UNAVAILABLE · '+cross.error),cross.available&&cross.ok?'ready':'analyzing');"],
    ['cross-fail-closed',"else lines.push('6. ASTROMETRY.NET unavailable: '+cross.error+' · Gaia gate remains authoritative.');","else throw Error('FAIL CLOSED — Astrometry.net cross-check unavailable: '+cross.error);"],
    ['apply-stage',"const pg=await hardAim(machineSolution0029,'0029 Gaia stellar solution');","window.gv46Progress?.('APPLYING RA / DEC / FOV / ROTATION');const pg=await hardAim(machineSolution0029,'0029 Gaia stellar solution');"],
    ['ready-stage',"Q('#score').textContent='STELLAR PASS';","window.gv46Progress?.('READY FOR HUMAN CONFIRMATION',ev.inliers+' STARS MATCHED · RMS '+ev.rms.toFixed(2)+' PX','ready');Q('#score').textContent='STELLAR PASS';"],
    ['failure-stage',"machineSolution0029=null;setGate(false,'MACHINE FAILED CLOSED');","machineSolution0029=null;window.gv46Progress?.('MACHINE ASTROMETRY FAILED',String(e.message||e),'error');setGate(false,'MACHINE FAILED CLOSED');"],
    ['gaia-entrypoint',"analyzeCurrent=analyze0029;Q('#analyzeBtn').onclick=analyze0029;","analyzeCurrent=analyze0029;Q('#analyzeBtn').onclick=analyze0029;window.gv46RunGaia=analyze0029;window.__gv46GaiaSolverBound=true;"]
  ];
  for(const [label,needle,replacement] of patches){r=replaceRequired(code,needle,replacement,label,report);if(!r.ok)return{ok:false,code,report};code=r.code}
  return{ok:true,code,report};
}
function injectHead(html,addition){const i=html.indexOf('</head>');return i<0?null:html.slice(0,i)+addition+html.slice(i)}
function injectBodyTop(html,addition){const m=html.match(/<body(?:\s[^>]*)?>/i);if(!m)return null;const i=m.index+m[0].length;return html.slice(0,i)+addition+html.slice(i)}
function json(o,status=200){return new Response(JSON.stringify(o,null,2),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}})}

async function page(request,env){
  const br=await base0045.fetch(request,env);let h=await br.text();
  const old45=extractScriptContaining(h,'[GV0045] safe recovery client installed');if(!old45.found)return new Response('0046 STARTUP ERROR: 0045 client anchor missing',{status:500});h=old45.html;
  h=h.replaceAll(LEGACY_PREDICTIONS_URL,'/api/predictions');
  const gr=await gaia0029.fetch(request,env);const gh=await gr.text();const solver=extractScriptContaining(gh,'const oldShow29=showCurrent;');if(!solver.found)return new Response('0046 STARTUP ERROR: 0029 Gaia solver script missing',{status:500});
  const patched=patchGaiaSolver(solver.code);if(!patched.ok)return new Response('0046 STARTUP ERROR: Gaia patch anchor counts '+JSON.stringify(patched.report),{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  const head=injectHead(h,STYLE);if(!head)return new Response('0046 STARTUP ERROR: head anchor missing',{status:500});h=head;
  const top=injectBodyTop(h,BANNER);if(!top)return new Response('0046 STARTUP ERROR: body-open anchor missing',{status:500});h=top;
  const i=h.lastIndexOf('</body>');if(i<0)return new Response('0046 STARTUP ERROR: body-close anchor missing',{status:500});
  h=h.slice(0,i)+'<script>'+patched.code+'</script>'+CLIENT+h.slice(i);
  h=h.replaceAll('GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0045','GV CLOUDFLARE AUTO ASTROMETRY CURATOR 0046');
  const headers=new Headers(br.headers);headers.set('content-type','text/html; charset=utf-8');headers.set('cache-control','no-store, no-cache, must-revalidate, max-age=0');headers.set('pragma','no-cache');headers.set('expires','0');headers.set('x-gv-revision',REV);headers.set('x-gv-build-colombia',BUILD_STAMP_COLOMBIA);headers.set('x-gv-machine','gaia-dr3-stellar-gated-plus-mandatory-astrometry-cross-check');headers.set('x-gv-legacy-sift-movement','disabled');headers.set('x-gv-aladin-refresh','rebuild-and-restore-live-state');
  return new Response(h,{status:200,headers});
}
async function health(env){return json({ok:true,revision:REV,service:'gv-cloudflare-auto-astrometry-curator-0046',build_stamp_colombia:BUILD_STAMP_COLOMBIA,build_stamp_iso:BUILD_STAMP_ISO,timezone:'America/Bogota',base_page:'0045',gaia_solver_source:'0029',machine_button:'direct-gaia-stellar-entrypoint',legacy_sift_movement:false,fail_closed:true,astrometry_cross_check:'mandatory',requirements:['REQ-093','REQ-094','REQ-095','REQ-096','REQ-097','REQ-098','REQ-099','REQ-100','REQ-101','REQ-103'],refresh_and_recenter_separate:true,key_configured:Boolean(String(env?.ASTROMETRY_API_KEY||'').trim())})}
export default{async fetch(request,env){const u=new URL(request.url);if(u.pathname==='/'||u.pathname==='/index.html')return page(request,env);if(u.pathname==='/api/health')return health(env);if(['/api/gaia','/api/solve','/api/status','/api/predictions','/api/predictions-diagnostic'].includes(u.pathname))return gaia0029.fetch(request,env);return base0045.fetch(request,env)}};
