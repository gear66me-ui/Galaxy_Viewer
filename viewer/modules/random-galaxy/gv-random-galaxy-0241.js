/*
RANDOM GALAXY PRESENTATION 0241 — GV 200-008 BLD0004
Presentation-only restoration from the late 0239/0240 family.
Owns travel/arrival banners, provider artwork, VIEW HD viewport and source website link.
Does NOT own navigation, camera, Aladin, AVM/WCS registration, vignette, route state or image preparation.
*/
(function(global){
'use strict';
const VERSION='0241';
const FONT_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf';
const ICONS=Object.freeze({
 chandra:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Chandra/Chandra.jpg',
 eso:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/ESO/ESO.jpg',
 euclid:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Euclid/Euclid.jpg',
 galex:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/GALEX/GALEX.jpg',
 herschel:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Herschel/Herschel.jpg',
 hubble:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble.jpg',
 jwst:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/JWST/JWST.jpeg',
 nrao:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NRAO/NRAO.jpg',
 noirlab:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NoirLabs/NOIRLab.jpg',
 nustar:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NuSTAR/NuSTAR.jpg',
 spitzer:'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Spitzer/Spitzer.jpg'
});
const clean=v=>String(v??'').replace(/\s+/g,' ').trim();
function providerKey(d){
 const t=[d?.provider,d?.telescope,d?.source,d?.hdUrl,d?.sourceUrl].map(clean).join(' ').toLowerCase();
 if(/noir|gemini|noao/.test(t))return'noirlab';if(/hubble|hst/.test(t))return'hubble';if(/james webb|webb|jwst/.test(t))return'jwst';
 for(const k of Object.keys(ICONS))if(t.includes(k))return k;return'';
}
function distanceText(d){
 const n=Number(d?.distance??d?.distanceMly??d?.science?.distanceMly);
 if(!(n>0))return'DISTANCE —';
 if(n>=1000)return `${(n/1000).toFixed(n>=10000?1:2)} BILLION LIGHT-YEARS`;
 if(n>=1)return `${n.toFixed(n>=100?0:n>=10?1:2)} MILLION LIGHT-YEARS`;
 return `${Math.round(n*1000).toLocaleString()} THOUSAND LIGHT-YEARS`;
}
function imageUrl(d){return clean(d?.hdUrl||d?.selectedImageUrl||d?.githubImageUrl||d?.imageUrl)}
function sourceUrl(d){const u=clean(d?.sourceUrl||d?.source_url);return /^https:\/\//i.test(u)?u:''}
function label(d){return clean(d?.commonName||d?.designation||d?.name||'GALAXY').toUpperCase()}
function info(d){return [clean(d?.designation),clean(d?.constellation),clean(d?.provider||d?.telescope)].filter(Boolean).join(' · ').toUpperCase()}
function installStyle(){
 if(document.getElementById('gvrg0241-style'))return;
 const s=document.createElement('style');s.id='gvrg0241-style';s.textContent=`
@font-face{font-family:"GVRG Space";src:url("${FONT_URL}") format("opentype");font-display:swap}
.gvrg0241{position:absolute;inset:0;z-index:7290;pointer-events:none;font-family:"GVRG Space",sans-serif;color:#eefaff}
.gvrg0241-banner{position:absolute;left:50%;bottom:56px;transform:translateX(-50%);width:min(94vw,620px);min-height:48px;padding:5px 62px 5px 9px;border:1px solid rgba(124,203,255,.82);border-radius:7px;background:linear-gradient(145deg,rgba(4,17,43,.94),rgba(8,39,74,.94));box-shadow:0 0 14px rgba(64,165,255,.3);opacity:0;visibility:hidden;transition:opacity .15s ease;pointer-events:auto}
.gvrg0241-banner.on{opacity:1;visibility:visible}.gvrg0241-banner.travel{border-color:rgba(255,183,71,.9);box-shadow:0 0 14px rgba(255,135,45,.32)}
.gvrg0241-state{font-size:7px;letter-spacing:1px;color:#78ffab}.gvrg0241-banner.travel .gvrg0241-state{color:#ffb347}
.gvrg0241-title{margin-top:2px;font-size:11px;letter-spacing:.8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gvrg0241-distance,.gvrg0241-info{margin-top:2px;font:9px/1.15 system-ui,sans-serif;color:#cfeeff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gvrg0241-provider{position:absolute;right:7px;top:50%;width:48px;height:48px;transform:translateY(-50%);padding:2px;border:1px solid rgba(124,203,255,.8);border-radius:7px;background:#06162e}
.gvrg0241-provider img{width:100%;height:100%;display:block;border-radius:5px;object-fit:cover}
.gvrg0241-actions{display:flex;gap:6px;margin-top:4px}.gvrg0241-btn{padding:3px 7px;border:1px solid rgba(124,203,255,.78);border-radius:5px;background:linear-gradient(145deg,#0a2a55,#12457d);color:#eefaff;font:7px/1.2 "GVRG Space",sans-serif;letter-spacing:.5px}
.gvrg0241-hd{position:absolute;inset:0;z-index:10020;display:none;flex-direction:column;background:#020711;pointer-events:auto}.gvrg0241-hd.on{display:flex}
.gvrg0241-hd-head{flex:0 0 auto;padding:9px 58px 8px 10px;min-height:72px;border-bottom:1px solid rgba(124,203,255,.5);background:linear-gradient(145deg,#06162e,#0a315b);position:relative}
.gvrg0241-hd-title{font-size:14px;letter-spacing:1px;text-align:center}.gvrg0241-hd-info,.gvrg0241-hd-distance{margin-top:4px;text-align:center;font:9px/1.2 system-ui,sans-serif;color:#d9f1ff}
.gvrg0241-hd-provider{position:absolute;right:7px;top:50%;width:48px;height:48px;transform:translateY(-50%);border-radius:7px;object-fit:cover}
.gvrg0241-image{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;overflow:hidden;background:#000}.gvrg0241-image img{display:block;max-width:100%;max-height:100%;object-fit:contain}
.gvrg0241-foot{display:flex;justify-content:center;gap:8px;padding:8px;background:linear-gradient(145deg,#06162e,#0a315b)}
`;document.head.appendChild(s);
}
function mount(host){
 if(!(host instanceof Element))throw new TypeError('RANDOM PRESENTATION HOST MISSING');installStyle();
 const root=document.createElement('div');root.className='gvrg0241';root.innerHTML=`
 <section class="gvrg0241-banner"><div class="gvrg0241-state"></div><div class="gvrg0241-title"></div><div class="gvrg0241-distance"></div><div class="gvrg0241-info"></div><div class="gvrg0241-actions"><button class="gvrg0241-btn view" type="button">VIEW HD IMAGE</button><button class="gvrg0241-btn web" type="button">WEBSITE</button></div><button class="gvrg0241-provider" type="button" aria-label="VIEW HD IMAGE"><img alt=""></button></section>
 <section class="gvrg0241-hd"><div class="gvrg0241-hd-head"><div class="gvrg0241-hd-title"></div><div class="gvrg0241-hd-distance"></div><div class="gvrg0241-hd-info"></div><img class="gvrg0241-hd-provider" alt=""></div><div class="gvrg0241-image"><img alt=""></div><div class="gvrg0241-foot"><button class="gvrg0241-btn back" type="button">BACK TO SKY</button><button class="gvrg0241-btn source" type="button">SOURCE WEBSITE</button></div></section>`;
 host.appendChild(root);
 const q=x=>root.querySelector(x),banner=q('.gvrg0241-banner'),state=q('.gvrg0241-state'),title=q('.gvrg0241-title'),dist=q('.gvrg0241-distance'),meta=q('.gvrg0241-info'),provider=q('.gvrg0241-provider img'),hd=q('.gvrg0241-hd'),hdTitle=q('.gvrg0241-hd-title'),hdDist=q('.gvrg0241-hd-distance'),hdInfo=q('.gvrg0241-hd-info'),hdProvider=q('.gvrg0241-hd-provider'),hdImage=q('.gvrg0241-image img');
 let current=null;
 function sync(d){current=d;const k=providerKey(d),icon=ICONS[k]||'',name=label(d),dt=distanceText(d),it=info(d);title.textContent=name;dist.textContent=dt;meta.textContent=it;hdTitle.textContent=name;hdDist.textContent=dt;hdInfo.textContent=it;provider.src=icon;provider.hidden=!icon;hdProvider.src=icon;hdProvider.hidden=!icon;const im=imageUrl(d);if(im)hdImage.src=im;else hdImage.removeAttribute('src')}
 function openSource(){const u=sourceUrl(current);if(u)global.open(u,'_blank','noopener,noreferrer')}
 function showHD(){if(!current)return;hd.classList.add('on');document.body.classList.add('gv-hd-open')}
 function hideHD(){hd.classList.remove('on');document.body.classList.remove('gv-hd-open')}
 q('.view').onclick=showHD;q('.gvrg0241-provider').onclick=showHD;q('.web').onclick=openSource;q('.source').onclick=openSource;q('.back').onclick=hideHD;
 return Object.freeze({
  beginTravel(d){sync(d);state.textContent='TRAVELING';banner.classList.add('on','travel');q('.gvrg0241-actions').style.display='none';return d},
  arrive(d){sync(d);state.textContent='ARRIVAL';banner.classList.remove('travel');banner.classList.add('on');q('.gvrg0241-actions').style.display='flex';return d},
  showHD,hideHD,
  destroy(){hideHD();root.remove()}
 });
}
global.GalaxyRandomGalaxyPresentation=Object.freeze({VERSION,mount,ICONS});
})(typeof window!=='undefined'?window:globalThis);
