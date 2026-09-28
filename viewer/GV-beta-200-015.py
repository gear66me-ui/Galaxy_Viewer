from IPython.display import HTML, Javascript, display

VIEWER_VERSION = "GV-beta-200-015"

display(HTML(r"""
<div id="gv015-app" class="gv015-root">
  <div class="gv015-stage" id="gv015-stage">
    <section class="gv015-launch" id="gv015-launch">
      <div class="gv015-launch-bg"></div>
      <div class="gv015-launch-card">
        <div class="gv015-launch-title">VIEW HD PROVIDER TEST</div>
        <div class="gv015-launch-sub">Tap provider icon to open Galaxy Web Browser</div>
        <button class="gv015-provider-hit" id="gv015-open-browser" aria-label="Open Spitzer provider browser">
          <img src="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Spitzer/Spitzer.jpg" alt="Spitzer">
          <span>SPITZER</span>
        </button>
      </div>
    </section>
    <section class="gv015-browser" id="gv015-browser" aria-hidden="true">
      <div class="gv015-toprow">
        <div class="gv015-titlebox">GALAXY WEB BROWSER</div>
        <div class="gv015-provider-box"><img src="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Spitzer/Spitzer.jpg" alt="Spitzer"></div>
      </div>
      <div class="gv015-navrow">
        <button class="gv015-navbtn" id="gv015-web-back" aria-label="Back">‹</button>
        <button class="gv015-navbtn" id="gv015-web-forward" aria-label="Forward">›</button>
        <div class="gv015-address" aria-label="Locked address"><span class="gv015-lock">🔒</span><span id="gv015-url-text">https://www.spitzer.caltech.edu</span></div>
        <button class="gv015-navbtn gv015-refresh" id="gv015-refresh" aria-label="Refresh">⟳</button>
      </div>
      <div class="gv015-frame-wrap">
        <iframe id="gv015-frame" title="Spitzer source page" referrerpolicy="no-referrer" src="about:blank"></iframe>
      </div>
      <button class="gv015-back-viewer" id="gv015-close-browser" aria-label="Back to Galaxy Viewer">
        <span class="gv015-bottom-arrow">‹</span>
        <span class="gv015-bottom-text">BACK TO GALAXY VIEWER</span>
        <img class="gv015-gv-icon" src="https://gear66me-ui.github.io/Galaxy_Viewer/mobile/icon.svg" alt="Galaxy Viewer">
      </button>
    </section>
  </div>
</div>
<style>
@font-face{font-family:'SpaceAgeGV015';src:url('https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf') format('opentype');font-weight:400;font-style:normal;font-display:block}
:root{--gv015-cyan:#86ecff;--gv015-cyan2:#21d4ff;--gv015-deep:#020817;--gv015-blue:#0d53b7;--gv015-green:#78ffab}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000!important}.gv015-root{position:fixed;inset:0;z-index:2147483000;background:radial-gradient(circle at 50% 12%,rgba(33,150,255,.34),transparent 35%),linear-gradient(180deg,#020817,#000 80%);overflow:hidden;color:#eaffff;font-family:Arial,sans-serif}.gv015-root *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}.gv015-root:before{content:"";position:absolute;inset:0;background-image:radial-gradient(#fff 0.75px,transparent 1px),radial-gradient(#64dfff 0.65px,transparent 1px);background-size:51px 51px,89px 89px;background-position:6px 9px,25px 35px;opacity:.26;pointer-events:none}.gv015-stage{position:absolute;left:50%;top:50%;width:min(100vw,calc(100dvh * 0.5625));height:min(100dvh,calc(100vw * 1.777777));transform:translate(-50%,-50%);overflow:hidden}.gv015-launch,.gv015-browser{position:absolute;inset:0;padding:2.8% 3%;display:flex;flex-direction:column;gap:1.45%;}.gv015-launch{justify-content:center}.gv015-launch-bg{position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,rgba(255,100,30,.25),transparent 24%),radial-gradient(circle at 70% 30%,rgba(64,215,255,.28),transparent 36%),#020817}.gv015-launch-card{position:relative;margin:auto;width:92%;border:2px solid var(--gv015-cyan);border-radius:22px;background:linear-gradient(145deg,rgba(2,12,32,.96),rgba(10,58,130,.70));box-shadow:0 0 9px var(--gv015-cyan),0 0 28px rgba(33,212,255,.55),inset 0 2px 3px rgba(255,255,255,.35),inset 0 -5px 12px rgba(0,0,0,.60);padding:8% 6%;text-align:center}.gv015-launch-title{font:400 clamp(18px,5.4vw,34px)/1 SpaceAgeGV015,Arial,sans-serif;letter-spacing:.08em;text-shadow:0 0 8px var(--gv015-cyan),0 0 18px rgba(33,212,255,.8);white-space:nowrap}.gv015-launch-sub{margin-top:4%;font:700 clamp(11px,3vw,17px)/1.35 Arial,sans-serif;color:#c8efff;text-transform:uppercase}.gv015-provider-hit{margin:8% auto 0;width:38%;aspect-ratio:1;border:2px solid var(--gv015-cyan);border-radius:22px;background:linear-gradient(145deg,#061431,#0d53b7);box-shadow:0 0 10px var(--gv015-cyan),0 0 24px rgba(33,212,255,.45),inset 0 2px 3px rgba(255,255,255,.35);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6%;color:white}.gv015-provider-hit img{width:72%;height:72%;object-fit:contain;border-radius:14px}.gv015-provider-hit span{font:900 clamp(10px,2.6vw,15px)/1 Arial,sans-serif;letter-spacing:.16em}.gv015-browser{display:none}.gv015-browser.gv015-open{display:flex}.gv015-toprow{height:5.8%;display:grid;grid-template-columns:1fr 10.5%;gap:1.5%}.gv015-titlebox,.gv015-provider-box,.gv015-navrow,.gv015-frame-wrap,.gv015-back-viewer{border:2px solid var(--gv015-cyan);background:linear-gradient(145deg,rgba(4,23,61,.97),rgba(12,74,160,.80) 58%,rgba(31,145,220,.50));box-shadow:0 0 6px var(--gv015-cyan),0 0 19px rgba(33,212,255,.58),inset 0 2px 2px rgba(255,255,255,.35),inset 0 -4px 10px rgba(0,0,0,.58)}.gv015-titlebox{border-radius:13px;display:flex;align-items:center;justify-content:center;font:400 clamp(14px,4.4vw,27px)/1 SpaceAgeGV015,Arial,sans-serif;letter-spacing:.085em;text-shadow:0 0 7px var(--gv015-cyan),0 0 17px rgba(33,212,255,.90);white-space:nowrap;overflow:hidden}.gv015-provider-box{border-radius:13px;display:flex;align-items:center;justify-content:center;overflow:hidden}.gv015-provider-box img{width:82%;height:82%;object-fit:contain;border-radius:9px;filter:drop-shadow(0 0 6px rgba(134,236,255,.9))}.gv015-navrow{height:6.2%;border-radius:14px;display:grid;grid-template-columns:10.5% 10.5% 1fr 10.5%;gap:1.45%;align-items:center;padding:1.25%}.gv015-navbtn{height:100%;border:2px solid rgba(134,236,255,.85);border-radius:11px;background:linear-gradient(145deg,#061636,#0b3886,#0b8ee0);color:#eaffff;font:900 clamp(28px,7vw,46px)/.8 Arial,sans-serif;box-shadow:inset 0 2px 2px rgba(255,255,255,.38),inset 0 -4px 8px rgba(0,0,0,.55),0 0 9px rgba(134,236,255,.7);display:flex;align-items:center;justify-content:center}.gv015-refresh{font-size:clamp(22px,5.4vw,34px)}.gv015-address{height:100%;min-width:0;border:2px solid rgba(134,236,255,.54);border-radius:12px;background:linear-gradient(180deg,rgba(2,8,27,.96),rgba(2,6,18,.98));box-shadow:inset 0 1px 8px rgba(0,0,0,.75),0 0 8px rgba(33,212,255,.28);display:flex;align-items:center;padding:0 4%;pointer-events:none}.gv015-lock{font-size:clamp(18px,4.4vw,26px);margin-right:4%;filter:drop-shadow(0 0 6px rgba(134,236,255,.9))}.gv015-address span:last-child{font:800 clamp(12px,3.4vw,20px)/1 Arial,sans-serif;text-transform:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#f5fcff}.gv015-frame-wrap{flex:1;min-height:0;border-radius:18px;background:#01040b;padding:.8%;overflow:hidden}.gv015-frame-wrap iframe{width:100%;height:100%;border:0;border-radius:13px;background:#fff}.gv015-back-viewer{height:7.8%;border-radius:16px;display:grid;grid-template-columns:13% 1fr 13%;gap:1%;align-items:center;padding:0 1.4%;color:#eaffff;transition:.12s ease}.gv015-back-viewer.gv015-green{background:linear-gradient(145deg,rgba(6,55,31,.96),rgba(11,122,66,.86),rgba(32,201,107,.64));box-shadow:0 0 8px var(--gv015-green),0 0 24px rgba(120,255,171,.62),inset 0 2px 2px rgba(235,255,240,.54),inset 0 -4px 8px rgba(0,0,0,.44)}.gv015-bottom-arrow{height:78%;border:2px solid rgba(134,236,255,.82);border-radius:13px;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,#061636,#0b3886,#0b8ee0);font:900 clamp(34px,9vw,54px)/.8 Arial,sans-serif;box-shadow:inset 0 2px 2px rgba(255,255,255,.38),0 0 10px rgba(134,236,255,.65)}.gv015-bottom-text{font:400 clamp(12px,3.7vw,24px)/1 SpaceAgeGV015,Arial,sans-serif;letter-spacing:.09em;text-shadow:0 0 7px var(--gv015-cyan),0 0 17px rgba(33,212,255,.90);white-space:nowrap;text-align:center}.gv015-gv-icon{height:76%;width:76%;justify-self:center;object-fit:contain;border-radius:13px;filter:drop-shadow(0 0 7px rgba(134,236,255,.9))}@media (orientation:landscape){.gv015-stage{width:min(100vw,calc(100dvh * 0.5625));height:100dvh}.gv015-root:after{content:'PORTRAIT APP VIEW';position:fixed;right:1rem;bottom:1rem;color:#78ffab;font:800 12px/1 Arial,sans-serif;opacity:.72}}
</style>
"""))

display(Javascript(r"""
(()=>{
'use strict';
const VERSION='GV-beta-200-015';
const GV200001_BUILD='0001';
const MASTER='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/gv-master-catalog.json';
const FALLBACK='https://www.spitzer.caltech.edu';
const browser=document.getElementById('gv015-browser');
const launch=document.getElementById('gv015-launch');
const frame=document.getElementById('gv015-frame');
const urlText=document.getElementById('gv015-url-text');
const backViewer=document.getElementById('gv015-close-browser');
let activeUrl=FALLBACK;
function pickUrlFromRecord(r){
  const keys=['sourceUrl','source_url','providerUrl','provider_url','webUrl','web_url','referenceUrl','reference_url','pageUrl','page_url','imageUrl','image_url','selectedImageUrl','hdUrl','url'];
  for(const k of keys){const v=r&&r[k]; if(typeof v==='string'&&/^https?:\/\//i.test(v)&&/(spitzer|caltech|ipac)/i.test(v)) return v;}
  for(const [k,v] of Object.entries(r||{})){if(typeof v==='string'&&/^https?:\/\//i.test(v)&&/(spitzer|caltech|ipac)/i.test(v)) return v;}
  return '';
}
async function resolveSpitzerUrl(){
  try{
    const res=await fetch(MASTER+'?v='+Date.now(),{cache:'no-store'});
    if(!res.ok) throw new Error('master '+res.status);
    const data=await res.json();
    const arr=Array.isArray(data)?data:(Array.isArray(data.records)?data.records:Array.isArray(data.galaxies)?data.galaxies:[]);
    for(const r of arr){
      const blob=JSON.stringify(r||{});
      if(/spitzer|caltech|ipac/i.test(blob)){const u=pickUrlFromRecord(r); if(u) return u;}
    }
  }catch(e){console.warn('GV015 master URL fallback',e);}
  return FALLBACK;
}
function loadUrl(u){activeUrl=u||FALLBACK;urlText.textContent=activeUrl;frame.src=activeUrl;}
document.getElementById('gv015-open-browser').addEventListener('click',async()=>{
  launch.style.display='none'; browser.classList.add('gv015-open'); browser.setAttribute('aria-hidden','false');
  loadUrl(await resolveSpitzerUrl());
});
document.getElementById('gv015-refresh').addEventListener('click',()=>{try{frame.src=activeUrl;}catch(_){}});
document.getElementById('gv015-web-back').addEventListener('click',()=>{try{frame.contentWindow.history.back();}catch(_){}});
document.getElementById('gv015-web-forward').addEventListener('click',()=>{try{frame.contentWindow.history.forward();}catch(_){}});
backViewer.addEventListener('click',()=>{backViewer.classList.add('gv015-green');setTimeout(()=>backViewer.classList.remove('gv015-green'),220);browser.classList.remove('gv015-open');browser.setAttribute('aria-hidden','true');launch.style.display='flex';});
})();
"""))
