import base0023 from './gv-cloudflare-auto-astrometry-curator-0023-worker.js';

const REV='0024';

function jsonResponse(obj,status=200,headers={}){
  return new Response(JSON.stringify(obj),{
    status,
    headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff',...headers}
  });
}

const CLIENT_PATCH=String.raw`<style id="gv0024-top-controls-style">
#gv0024TopSurvey{margin-top:6px;padding-top:6px;border-top:1px solid #2b3544}
#gv0024TopSurvey .gv0024Label{font-size:10px;font-weight:950;color:#9cabbf}
#gv0024TopSurvey select{flex:1;min-width:260px;max-width:100%;background:#090d13;color:#edf4ff;border:1px solid #2b3544;border-radius:7px;padding:7px}
#gv0024Recenter{background:#183e69;border-color:#4f83ba;white-space:nowrap}
@media(max-width:760px){
 #gv0024TopSurvey{display:grid;grid-template-columns:1fr 1fr;gap:5px}
 #gv0024TopSurvey .gv0024Label,#gv0024TopSurvey select{grid-column:1/-1;width:100%}
 #gv0024TopSurvey button{width:100%}
}
</style>
<script>
(()=>{
'use strict';
const s=document.getElementById('survey');
const mission=document.getElementById('missionDefault');
const all=document.getElementById('allSurveys');
const header=document.querySelector('header');
if(!s||!mission||!all||!header){window.gv0023Diag?.('0024-UI-FAIL','survey controls/header missing');return}
const oldPanel=s.closest('section.panel');
const oldControls=s.closest('.controls');
const oldLabel=oldControls?.querySelector('label');
const bar=document.createElement('div');
bar.id='gv0024TopSurvey';
bar.className='bar';
const label=document.createElement('span');
label.className='gv0024Label';
label.textContent='SURVEY';
bar.appendChild(label);
bar.appendChild(s);
bar.appendChild(mission);
bar.appendChild(all);
const recenter=document.createElement('button');
recenter.id='gv0024Recenter';
recenter.type='button';
recenter.textContent='◎ RE-CENTER ALADIN';
bar.appendChild(recenter);
header.appendChild(bar);
if(oldLabel)oldLabel.remove();
if(oldPanel)oldPanel.remove();

function diag(stage,msg,data){
  try{window.gv0023Diag?.(stage,msg,data)}catch{}
}
function getFallback(){
  try{
    const x=(typeof current==='function')?current():null;
    if(!x?.r)return null;
    const ra=(typeof raOf==='function')?raOf(x.r):null;
    const dec=(typeof decOf==='function')?decOf(x.r):null;
    const fov=(typeof fovOf==='function')?fovOf(x.r):null;
    const rot=(typeof rotOf==='function')?rotOf(x.r):0;
    if(Number.isFinite(Number(ra))&&Number.isFinite(Number(dec))){
      return {ra:Number(ra),dec:Number(dec),fov:Number(fov)||1.5,rot:Number(rot)||0,source:'catalog'};
    }
  }catch(e){diag('RECENTER-FALLBACK-FAIL',e.message)}
  return null;
}
function getSolved(){
  try{
    if(typeof solution!=='undefined'&&solution&&Number.isFinite(Number(solution.ra))&&Number.isFinite(Number(solution.dec))){
      return {
        ra:Number(solution.ra),
        dec:Number(solution.dec),
        fov:Number(solution.fov_x_deg||solution.fov||0)||null,
        rot:Number(solution.aladin_rotation_deg||0),
        mirror:Boolean(solution.mirror_x||solution.mirror_required||solution.longitude_reversed),
        source:'plate-solution'
      };
    }
  }catch(e){diag('RECENTER-SOLUTION-FAIL',e.message)}
  return null;
}
recenter.addEventListener('click',()=>{
  const st=getSolved()||getFallback();
  if(!st){diag('RECENTER-FAIL','no solved/catalog center available');return}
  let ok=true;
  try{
    ok=(typeof setCenter==='function'?setCenter(st.ra,st.dec):false)&&ok;
    if(st.fov&&typeof setFov==='function')ok=setFov(st.fov)&&ok;
    if(Number.isFinite(st.rot)&&typeof setRot==='function')ok=setRot(st.rot)&&ok;
    if(st.source==='plate-solution'&&typeof setMirror==='function')setMirror(Boolean(st.mirror));
    if(typeof updateLive==='function')updateLive();
    diag('RECENTER',st.source+' restored',{ra:st.ra,dec:st.dec,fov:st.fov,rot:st.rot,mirror:st.mirror??null,ok});
  }catch(e){diag('RECENTER-FAIL',e.message,{state:st})}
});
diag('0024-UI','survey selector moved to sticky header; recenter installed',{
  surveys:[...s.options].map(o=>({label:o.textContent,id:o.value}))
});
})();
</script>`;

async function html0024(request){
  const r=await base0023.fetch(request);
  let h=await r.text();
  h=h.replaceAll('0023','0024');
  const pos=h.lastIndexOf('</body>');
  if(pos<0)return new Response('0024 STARTUP ERROR: body anchor missing',{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
  h=h.slice(0,pos)+CLIENT_PATCH+h.slice(pos);
  return new Response(h,{status:200,headers:{'content-type':'text/html; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff','referrer-policy':'no-referrer','permissions-policy':'camera=(), microphone=(), geolocation=()'}});
}

async function reviseJson(request){
  const r=await base0023.fetch(request);
  const ct=(r.headers.get('content-type')||'').toLowerCase();
  if(!ct.includes('application/json'))return r;
  let j;try{j=await r.json()}catch{return r}
  if(j&&typeof j==='object'){
    if(j.revision==='0023')j.revision=REV;
    if(j.service==='gv-cloudflare-astrometry-bridge-0023')j.service='gv-cloudflare-astrometry-bridge-0024';
    if(j.diagnostics&&j.diagnostics.revision==='0023')j.diagnostics.revision=REV;
    if(j.result&&j.result.revision==='0023')j.result.revision=REV;
  }
  const headers=new Headers(r.headers);
  headers.set('content-type','application/json; charset=utf-8');
  headers.set('cache-control','no-store');
  return new Response(JSON.stringify(j),{status:r.status,headers});
}

export default {
  async fetch(request){
    const url=new URL(request.url);
    if(url.pathname==='/api/health')return jsonResponse({
      ok:true,
      service:'gv-cloudflare-astrometry-bridge-0024',
      revision:REV,
      stable_worker_name:'gv-cloudflare-auto-astrometry-curator-0015',
      features:['refresh-lock','image-proxy-cache','diagnostics','top-survey-selector','recenter-aladin']
    });
    if(url.pathname==='/'||url.pathname==='/index.html')return html0024(request);
    if(url.pathname==='/api/solve'||url.pathname==='/api/status')return reviseJson(request);
    return base0023.fetch(request);
  }
};