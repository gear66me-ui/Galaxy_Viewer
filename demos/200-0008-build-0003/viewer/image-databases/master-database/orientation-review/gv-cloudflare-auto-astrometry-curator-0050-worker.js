import base0049 from './gv-cloudflare-auto-astrometry-curator-0049-worker.js';

const SURVEY_CLIENT=String.raw`<style id="gv50-survey-style">
#gv50SurveyGuide{margin:6px 8px;padding:7px 9px;border:1px solid #4f83ba;border-radius:8px;background:#091a2d;color:#d9e8ff;font:850 10px/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap}
#gv50SurveyGuide b{color:#8ab4ff}
#gv50SurveyHelp{color:#ffd166}
</style>
<script>(()=>{'use strict';
const q=s=>document.querySelector(s);
const runtime={key:'',manual:false,applying:false,expanding:false,timer:0};

function diag50(stage,msg,data){
  try{window.gv0023Diag?.('0050-'+stage,msg,data)}catch{}
  try{console.log('[GV0050]['+stage+']',msg,data||'')}catch{}
}
function current50(){try{return typeof current==='function'?current():null}catch{return null}}
function text50(v){return String(v??'').trim()}
function source50(){
  const x=current50(),r=x?.r||{};
  return {
    mission:text50(x?.c?.name||x?.catalog||r.mission||r.telescope||r.observatory||r.catalog||'UNKNOWN'),
    r
  };
}
function regime50(mission,r){
  const raw=[
    r.obs_regime,r.obsRegime,r.observationRegime,r.regime,r.wavelength,r.wavelengthBand,
    r.band,r.filter,r.filters,r.instrument,r.detector,r.channel,r.waveband
  ].flatMap(v=>Array.isArray(v)?v:[v]).map(text50).filter(Boolean).join(' ').toLowerCase();
  const m=mission.toLowerCase();
  if(/x[\s-]?ray|kev|chandra|xmm|rosat/.test(raw)||/chandra/.test(m))return'X-RAY';
  if(/ultraviolet|\buv\b|far-uv|near-uv|fuv|nuv|galex/.test(raw))return'ULTRAVIOLET';
  if(/infrared|\bir\b|nir|mir|miri|nircam|micron|µm|spitzer|wise|2mass/.test(raw)||/spitzer|jwst/.test(m))return'INFRARED';
  if(/radio|millimeter|millimetre|submillimeter|submillimetre|alma|vla|mhz|ghz/.test(raw))return'RADIO';
  if(/optical|visible|acs|wfc3|wfpc|sdss|pan[\s-]?starr|dss/.test(raw))return'OPTICAL';
  return'UNKNOWN';
}
function optionText50(o){return (text50(o?.textContent)+' '+text50(o?.value)).toLowerCase()}
function score50(o,mission,regime){
  const s=optionText50(o),m=mission.toLowerCase();
  let score=0;
  const missionTokens={
    chandra:['chandra'],
    spitzer:['spitzer'],
    jwst:['jwst','webb'],
    hubble:['hubble','hst']
  };
  for(const[k,tokens]of Object.entries(missionTokens))if(m.includes(k)&&tokens.some(t=>s.includes(t)))score+=120;
  const regimeTokens={
    'X-RAY':['x-ray','xray','chandra','xmm','rosat','swift'],
    'INFRARED':['infrared','spitzer','wise','2mass','irsa','nir','mir'],
    'ULTRAVIOLET':['ultraviolet','galex',' fuv',' nuv',' uv'],
    'OPTICAL':['optical','panstarr','pan-starr','sdss','dss','gaia','hubble','hst'],
    'RADIO':['radio','nvss','first','alma','vla']
  };
  for(const t of regimeTokens[regime]||[])if(s.includes(t))score+=35;
  if(/color|colour|rgb/.test(s))score+=4;
  if(/dss2/.test(s))score+=regime==='OPTICAL'?12:1;
  if(/hips/.test(s))score+=1;
  return score;
}
function currentLabel50(){
  const s=q('#survey');
  if(!s)return'UNAVAILABLE';
  return text50(s.selectedOptions?.[0]?.textContent||s.value||'UNSELECTED');
}
function ensureGuide50(){
  let e=q('#gv50SurveyGuide');
  if(e)return e;
  e=document.createElement('div');e.id='gv50SurveyGuide';
  const host=q('#gv0024TopSurvey')||q('header')||q('main');
  host?.insertAdjacentElement('afterend',e);
  return e;
}
function render50(recommendation='WAITING'){
  const e=ensureGuide50();if(!e)return;
  const {mission,r}=source50(),regime=regime50(mission,r);
  e.innerHTML=
    '<b>SOURCE:</b> '+mission+' · '+regime+'\\n'+
    '<b>RECOMMENDED ALADIN:</b> '+recommendation+'\\n'+
    '<b>CURRENT ALADIN SURVEY:</b> '+currentLabel50()+'\\n'+
    '<b>SURVEY MODE:</b> '+(runtime.manual?'MANUAL OVERRIDE':'AUTOMATIC RECOMMENDATION')+'\\n'+
    '<span id="gv50SurveyHelp">ALL AVAILABLE loads the full Aladin survey list. Press it to browse/select surveys beyond Mission Default.</span>';
}
function choose50(){
  const s=q('#survey'),x=current50();if(!s||!x)return null;
  const {mission,r}=source50(),regime=regime50(mission,r),opts=[...s.options].filter(o=>text50(o.value));
  if(!opts.length)return null;
  let ranked=opts.map(o=>({o,score:score50(o,mission,regime)})).sort((a,b)=>b.score-a.score);
  let best=ranked[0];
  if(!best||best.score<=0){
    best=ranked.find(z=>/P\/DSS2\/color|DSS2.*color/i.test(z.o.value+' '+z.o.textContent))||ranked[0];
  }
  return best?{option:best.o,label:text50(best.o.textContent||best.o.value),score:best.score,mission,regime}:null;
}
function apply50(){
  if(runtime.manual)return;
  const s=q('#survey'),pick=choose50();if(!s||!pick){render50('NO COMPATIBLE SURVEY FOUND');return}
  render50(pick.label);
  if(s.value===pick.option.value)return;
  runtime.applying=true;
  s.value=pick.option.value;
  s.dispatchEvent(new Event('change',{bubbles:true}));
  runtime.applying=false;
  render50(pick.label);
  diag50('SURVEY','automatic recommendation applied',{mission:pick.mission,regime:pick.regime,label:pick.label,value:pick.option.value,score:pick.score});
}
function expandAndRecommend50(){
  if(runtime.manual)return;
  const all=q('#allSurveys');
  if(all&&!runtime.expanding){
    runtime.expanding=true;
    try{all.click()}catch(e){diag50('ALL-AVAILABLE-FAIL',String(e?.message||e))}
    setTimeout(()=>{runtime.expanding=false;apply50()},450);
    setTimeout(()=>{if(!runtime.manual)apply50()},1000);
  }else apply50();
}
function bind50(){
  const s=q('#survey'),mission=q('#missionDefault'),all=q('#allSurveys');
  if(s&&s.dataset.gv50Bound!=='1'){
    s.dataset.gv50Bound='1';
    s.addEventListener('change',()=>{
      if(!runtime.applying){
        runtime.manual=true;
        diag50('SURVEY','manual override',{value:s.value,label:currentLabel50()});
      }
      render50(choose50()?.label||'NO COMPATIBLE SURVEY FOUND');
    });
  }
  if(mission&&mission.dataset.gv50Bound!=='1'){
    mission.dataset.gv50Bound='1';
    mission.addEventListener('click',()=>{
      if(!runtime.expanding){runtime.manual=true;setTimeout(()=>render50(choose50()?.label||'NO COMPATIBLE SURVEY FOUND'),0)}
    });
  }
  if(all&&all.dataset.gv50Bound!=='1'){
    all.dataset.gv50Bound='1';
    all.title='Loads the full Aladin survey list so you can browse beyond Mission Default.';
  }
  ensureGuide50();
}
function sync50(){
  bind50();
  const x=current50(),key=text50(x?.key);
  if(key&&key!==runtime.key){
    runtime.key=key;runtime.manual=false;clearTimeout(runtime.timer);
    render50('SCANNING AVAILABLE SURVEYS…');
    runtime.timer=setTimeout(expandAndRecommend50,250);
  }else render50(choose50()?.label||'WAITING');
}
sync50();setInterval(sync50,300);
console.log('[GV0050] survey recommendation client installed');
})();</script>`;

function injectBodyEnd(html,addition){
  const i=html.lastIndexOf('</body>');
  return i<0?null:html.slice(0,i)+addition+html.slice(i);
}

export default {
  async fetch(request,env){
    const url=new URL(request.url);
    if(url.pathname!=='/'&&url.pathname!=='/index.html')return base0049.fetch(request,env);
    const response=await base0049.fetch(request,env);
    const type=(response.headers.get('content-type')||'').toLowerCase();
    if(!response.ok||!type.includes('text/html'))return response;
    const html=await response.text();
    const patched=injectBodyEnd(html,SURVEY_CLIENT);
    if(!patched)return new Response('0050 STARTUP ERROR: body close missing',{status:500,headers:{'content-type':'text/plain; charset=utf-8'}});
    return new Response(patched,{status:response.status,headers:response.headers});
  }
};
