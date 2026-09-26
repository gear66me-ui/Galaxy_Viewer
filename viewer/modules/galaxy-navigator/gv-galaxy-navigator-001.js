/* Galaxy Viewer Galaxy Navigator 001
 * Presentation and user-intent module only.
 * Visual baseline restored from Random Galaxy 0166.
 * Owns: Back / Random Galaxy / Forward UI, stars, wait comets, enabled/busy state.
 * Does NOT own: route planning, catalog selection, RA/Dec/FOV, Aladin camera, AVM.
 */
(function(global){
'use strict';
const VERSION='001';
const FONT_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf';

function installStyle(){
 if(document.getElementById('gv-galaxy-navigator-001-style'))return;
 const style=document.createElement('style');
 style.id='gv-galaxy-navigator-001-style';
 style.textContent=`
@font-face{font-family:"GV Space Age";src:url("${FONT_URL}") format("opentype");font-display:swap}
.gv-galaxy-navigator{display:flex;align-items:center;justify-content:center;gap:5px;width:min(100%,430px);margin:0 auto}
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:static;display:flex;flex:1 1 auto;min-width:0;align-items:center;justify-content:center;height:36px;margin:0;padding:0 12px;border:2px solid transparent;border-radius:6px;background:linear-gradient(145deg,#081B3A 0%,#0B3177 40%,#1484DB 74%,#296DBD 100%) padding-box,linear-gradient(135deg,#296DBD 0%,#58BFFF 38%,#8DDAFF 70%,#F4FDFF 100%) border-box;color:#EAF8FF;font:400 15.5px/1 "GV Space Age",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 5px rgba(221,248,255,.54);box-shadow:inset 0 0 8px rgba(221,248,255,.14),0 0 9px rgba(88,191,255,.34);filter:brightness(1.04);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
.gv-galaxy-history{appearance:none;-webkit-appearance:none;position:relative;display:flex;flex:0 0 36px;align-items:center;justify-content:center;width:36px;height:36px;margin:0;padding:0;border:2px solid transparent;border-radius:6px;background:linear-gradient(145deg,#081B3A 0%,#0B3177 40%,#1484DB 74%,#296DBD 100%) padding-box,linear-gradient(135deg,#296DBD 0%,#58BFFF 38%,#8DDAFF 70%,#F4FDFF 100%) border-box;color:transparent;box-shadow:inset 0 0 8px rgba(221,248,255,.14),0 0 9px rgba(88,191,255,.34);filter:brightness(1.04);cursor:pointer;touch-action:manipulation;outline:none;overflow:hidden;pointer-events:auto}
.gv-galaxy-history::before,.gv-galaxy-history::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;pointer-events:none;box-sizing:border-box}
.gv-galaxy-history::before{border-width:6px;border-color:#7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.90));transform:translate(-62%,-50%) rotate(45deg)}
.gv-galaxy-history::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-66%,-50%) rotate(45deg)}
.gv-galaxy-history-back::before{transform:translate(-38%,-50%) rotate(-135deg)}
.gv-galaxy-history-back::after{transform:translate(-34%,-50%) rotate(-135deg)}
.gv-galaxy-history:disabled{opacity:.62;cursor:default;box-shadow:inset 0 0 7px rgba(143,229,255,.18),0 0 6px rgba(41,109,189,.24)}
#gv-random-galaxy .gvrg-random-layout{display:grid;grid-template-columns:20px auto 20px;align-items:center;justify-content:center;column-gap:13px}
#gv-random-galaxy .gvrg-random-label{display:block;grid-column:2;text-align:center}
#gv-random-galaxy .gvrg-random-star-wrap{position:relative;display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;margin:0;flex:0 0 20px;line-height:20px;transform:none}
#gv-random-galaxy .gvrg-random-star-wrap-left{grid-column:1}
#gv-random-galaxy .gvrg-random-star-wrap-right{grid-column:3;transform:translateX(-2px)}
#gv-random-galaxy .gvrg-random-star{display:block;font:16px/20px system-ui,sans-serif;transform:translateY(-.5px)}
#gv-random-galaxy .gvrg-random-comet{position:absolute;left:50%;top:50%;width:0;height:0;opacity:1;pointer-events:none;z-index:2;animation:gvrg-random-comet-orbit-0031 2.8s linear infinite;animation-play-state:running}
#gv-random-galaxy .gvrg-random-comet i{position:absolute;left:-1.5px;top:-1.5px;width:3px;height:3px;border-radius:50%;background:#FF8420;transform:rotate(var(--a)) translateY(-8px) scale(var(--s));opacity:var(--o);box-shadow:0 0 3px rgba(255,132,32,.85)}
#gv-random-galaxy .gvrg-random-comet i:nth-child(1){--a:0deg;--s:1;--o:1;background:#FF4414;box-shadow:0 0 2px 1px #FF4414,0 0 5px 1px #FF8420}
#gv-random-galaxy .gvrg-random-comet i:nth-child(2){--a:-15deg;--s:.88;--o:.84}#gv-random-galaxy .gvrg-random-comet i:nth-child(3){--a:-30deg;--s:.76;--o:.68}#gv-random-galaxy .gvrg-random-comet i:nth-child(4){--a:-45deg;--s:.64;--o:.52}#gv-random-galaxy .gvrg-random-comet i:nth-child(5){--a:-60deg;--s:.52;--o:.38}#gv-random-galaxy .gvrg-random-comet i:nth-child(6){--a:-75deg;--s:.42;--o:.26}#gv-random-galaxy .gvrg-random-comet i:nth-child(7){--a:-90deg;--s:.32;--o:.16}#gv-random-galaxy .gvrg-random-comet i:nth-child(8){--a:-105deg;--s:.24;--o:.08}
#gv-random-galaxy.gvrg-random-busy .gvrg-random-comet{opacity:1;animation-play-state:running}
#gv-random-galaxy.gvrg-random-traveling{background:linear-gradient(145deg,#062B1D 0%,#08783F 42%,#13B968 76%,#38E69A 100%) padding-box,linear-gradient(135deg,#38E69A 0%,#78FFAB 48%,#D9FFE9 100%) border-box;color:#DFFFF0;text-shadow:0 0 5px rgba(120,255,171,.9);box-shadow:inset 0 0 8px rgba(120,255,171,.22),0 0 12px rgba(56,230,154,.62)}
#gv-random-galaxy .gvrg-random-comet-left{animation-delay:-1.4s}
@keyframes gvrg-random-comet-orbit-0031{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
`;
 document.head.appendChild(style);
}
const comet='<span class="gvrg-random-comet"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>';
function mount(host,handlers={}){
 if(!(host instanceof Element))throw new Error('GALAXY NAVIGATOR HOST REQUIRED');
 installStyle();host.classList.add('gv-galaxy-navigator');
 host.innerHTML='<button class="gv-galaxy-history gv-galaxy-history-back" data-gv-nav="back" type="button" aria-label="Back"></button>'+
 '<button id="gv-random-galaxy" data-gv-nav="random" type="button" aria-label="RANDOM GALAXY"><span class="gvrg-random-layout"><span class="gvrg-random-star-wrap gvrg-random-star-wrap-left" aria-hidden="true"><span class="gvrg-random-star">✨</span>'+comet.replace('gvrg-random-comet','gvrg-random-comet gvrg-random-comet-left')+'</span><span class="gvrg-random-label">RANDOM GALAXY</span><span class="gvrg-random-star-wrap gvrg-random-star-wrap-right" aria-hidden="true"><span class="gvrg-random-star">✨</span>'+comet+'</span></span></button>'+
 '<button class="gv-galaxy-history" data-gv-nav="forward" type="button" aria-label="Forward"></button>';
 const back=host.querySelector('[data-gv-nav="back"]'),random=host.querySelector('[data-gv-nav="random"]'),forward=host.querySelector('[data-gv-nav="forward"]');
 back.addEventListener('click',()=>{if(!back.disabled)handlers.onBack?.()});
 random.addEventListener('click',()=>{if(!random.disabled)handlers.onRandom?.()});
 forward.addEventListener('click',()=>{if(!forward.disabled)handlers.onForward?.()});
 return Object.freeze({VERSION,host,back,random,forward,
  setBusy(busy){random.classList.toggle('gvrg-random-busy',Boolean(busy));random.disabled=Boolean(busy)},
  setTraveling(traveling){const on=Boolean(traveling);random.classList.toggle('gvrg-random-traveling',on);const label=random.querySelector('.gvrg-random-label');if(label)label.textContent=on?'TRAVELING':'RANDOM GALAXY';random.setAttribute('aria-label',on?'TRAVELING':'RANDOM GALAXY')},
  setEnabled({back:be=true,random:re=true,forward:fe=true}={}){back.disabled=!be;random.disabled=!re;forward.disabled=!fe}
 });
}
global.GalaxyNavigator=Object.freeze({VERSION,mount});
})(typeof window!=='undefined'?window:globalThis);
