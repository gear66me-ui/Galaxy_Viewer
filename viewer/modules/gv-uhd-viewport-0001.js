(()=>{
'use strict';
if(window.GVUHDViewport)return;
const ID='gv-uhd-viewport-0001';
let root=null,img=null,loading=null,current=null,scale=1,x=0,y=0,start=null,lastTap=0,uhdToken=0;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function css(){if(document.getElementById(ID+'-style'))return;const s=document.createElement('style');s.id=ID+'-style';s.textContent=`
#${ID}{position:fixed;inset:0;z-index:9800;display:none;box-sizing:border-box;padding:10px;background:#000;font-family:"Space Age",system-ui,sans-serif;color:#eaffff;touch-action:none}
#${ID}.open{display:flex;flex-direction:column}
#${ID} .gvuhd-frame{position:relative;flex:1 1 auto;min-height:0;padding:2px;border-radius:22px;background:linear-gradient(120deg,#05265d,#168cff,#7fdcff,#42f5df,#eefcff,#1779d8,#05265d);background-size:300% 300%;animation:gvuhdGradient 10s ease infinite;box-shadow:0 0 14px rgba(69,190,255,.48)}
@keyframes gvuhdGradient{0%{background-position:0 50%}50%{background-position:100% 50%}100%{background-position:0 50%}}
#${ID} .gvuhd-stage{position:absolute;inset:2px;border-radius:20px;overflow:hidden;background:#000;touch-action:none}
#${ID} .gvuhd-image{position:absolute;left:50%;top:50%;max-width:none;max-height:none;transform-origin:center center;user-select:none;-webkit-user-select:none;pointer-events:none;will-change:transform}
#${ID} .gvuhd-loading{position:absolute;right:14px;top:14px;width:34px;height:34px;border-radius:50%;display:none;animation:gvuhdOrbit .8s linear infinite}
#${ID} .gvuhd-loading.on{display:block}
#${ID} .gvuhd-loading:before{content:"";position:absolute;left:50%;top:-1px;width:8px;height:8px;margin-left:-4px;border-radius:50%;background:#eefdff;box-shadow:0 0 6px #fff,0 0 12px #58cfff}
#${ID} .gvuhd-loading:after{content:"";position:absolute;left:50%;top:2px;width:20px;height:4px;background:linear-gradient(90deg,#fff,rgba(72,190,255,.65),transparent);border-radius:4px;transform:rotate(30deg);transform-origin:left center}
@keyframes gvuhdOrbit{to{transform:rotate(360deg)}}
#${ID} .gvuhd-controls{flex:0 0 auto;display:grid;grid-template-columns:1fr .62fr 1.35fr;gap:8px;padding:9px 2px 1px;align-items:stretch}
#${ID} button{appearance:none;-webkit-appearance:none;min-width:0;height:48px;margin:0;padding:4px 7px;border-radius:8px;color:#eaffff;font:400 9px/1.15 "Space Age",system-ui,sans-serif;letter-spacing:.25px;text-transform:uppercase;touch-action:manipulation}
#${ID} .gvuhd-back{border:1px solid #8bdcff;background:linear-gradient(145deg,rgba(5,42,82,.98),rgba(8,92,140,.96));box-shadow:inset 0 0 6px rgba(132,225,255,.22),0 0 7px rgba(50,171,255,.28)}
#${ID} .gvuhd-uhd{border:1px solid #8bdcff;background:linear-gradient(145deg,rgba(5,55,110,.98),rgba(0,121,206,.96));box-shadow:inset 0 0 6px rgba(132,225,255,.24),0 0 7px rgba(50,171,255,.32)}
#${ID} .gvuhd-info{border:1px solid #b7ffd0;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34)}
#${ID} .gvuhd-btnrow{height:100%;display:flex;align-items:center;justify-content:center;gap:5px;overflow:hidden}
#${ID} .gvuhd-back .gvuhd-btnrow{justify-content:flex-start}#${ID} .gvuhd-info .gvuhd-btnrow{justify-content:flex-end}
#${ID} .gvuhd-provider{width:25px;height:25px;object-fit:contain;flex:0 0 25px}
#${ID} .gvuhd-arrow{font:700 22px/1 system-ui,sans-serif;flex:0 0 auto}
#${ID} .gvuhd-copy{display:flex;flex-direction:column;gap:2px;min-width:0;text-align:center}
#${ID} .gvuhd-copy strong{font:inherit;font-size:11px;color:#fff;white-space:nowrap}#${ID} .gvuhd-copy span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (orientation:landscape){#${ID}{padding:7px}#${ID} .gvuhd-controls{padding-top:6px}#${ID} button{height:42px}}
`;document.head.appendChild(s)}
function build(){if(root)return;css();root=document.createElement('div');root.id=ID;root.setAttribute('aria-hidden','true');root.innerHTML=`<div class="gvuhd-frame"><div class="gvuhd-stage"><img class="gvuhd-image" alt=""><div class="gvuhd-loading" aria-hidden="true"></div></div></div><div class="gvuhd-controls"><button class="gvuhd-back" type="button"><div class="gvuhd-btnrow"><span class="gvuhd-arrow">‹</span><span class="gvuhd-copy"><strong>BACK TO</strong><span>GALAXY VIEWER</span></span></div></button><button class="gvuhd-uhd" type="button"><div class="gvuhd-btnrow"><img class="gvuhd-provider" alt=""><span class="gvuhd-copy"><strong>UHD</strong></span></div></button><button class="gvuhd-info" type="button"><div class="gvuhd-btnrow"><img class="gvuhd-provider" alt=""><span class="gvuhd-copy"><strong>MORE IMAGES / INFO</strong><span class="gvuhd-visit">VISIT PROVIDER</span></span><span class="gvuhd-arrow">›</span></div></button></div>`;document.body.appendChild(root);img=root.querySelector('.gvuhd-image');loading=root.querySelector('.gvuhd-loading');root.querySelector('.gvuhd-back').onclick=close;root.querySelector('.gvuhd-uhd').onclick=loadUHD;root.querySelector('.gvuhd-info').onclick=()=>{if(current&&current.officialUrl)window.open(current.officialUrl,'_blank','noopener,noreferrer')};const stage=root.querySelector('.gvuhd-stage');stage.addEventListener('pointerdown',down);stage.addEventListener('pointermove',move);stage.addEventListener('pointerup',up);stage.addEventListener('pointercancel',up);stage.addEventListener('wheel',wheel,{passive:false});stage.addEventListener('dblclick',()=>zoomAt(2));}
const pointers=new Map();
function apply(){if(!img)return;img.style.transform=`translate(calc(-50% + ${x}px),calc(-50% + ${y}px)) scale(${scale})`}
function reset(){scale=1;x=0;y=0;apply()}
function down(e){e.currentTarget.setPointerCapture?.(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===1)start={x:e.clientX,y:e.clientY,ox:x,oy:y};if(pointers.size===2){const a=[...pointers.values()];start={dist:Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y),scale,ox:x,oy:y,cx:(a[0].x+a[1].x)/2,cy:(a[0].y+a[1].y)/2}};
function move(e){if(!pointers.has(e.pointerId))return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});const a=[...pointers.values()];if(a.length===1&&start){x=start.ox+(a[0].x-start.x);y=start.oy+(a[0].y-start.y);apply()}else if(a.length===2&&start&&start.dist){const d=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);scale=clamp(start.scale*d/start.dist,1,12);x=start.ox+((a[0].x+a[1].x)/2-start.cx);y=start.oy+((a[0].y+a[1].y)/2-start.cy);apply()}}
function up(e){pointers.delete(e.pointerId);if(!pointers.size){const now=performance.now();if(now-lastTap<300)zoomAt(scale<2?2:1);lastTap=now;start=null}else if(pointers.size===1){const a=[...pointers.values()][0];start={x:a.x,y:a.y,ox:x,oy:y}}}
function wheel(e){e.preventDefault();scale=clamp(scale*(e.deltaY<0?1.15:.87),1,12);apply()}
function zoomAt(v){scale=clamp(v,1,12);if(scale===1){x=0;y=0}apply()}
function fit(){if(!img||!img.naturalWidth)return;const stage=root.querySelector('.gvuhd-stage'),r=stage.getBoundingClientRect();const s=Math.min(r.width/img.naturalWidth,r.height/img.naturalHeight);img.style.width=(img.naturalWidth*s)+'px';img.style.height=(img.naturalHeight*s)+'px';reset()}
function open(opts){build();current=Object.assign({provider:'Provider',providerIcon:'',previewUrl:'',uhdUrl:'',officialUrl:'',title:''},opts||{});uhdToken++;loading.classList.remove('on');root.querySelectorAll('.gvuhd-provider').forEach(el=>{el.src=current.providerIcon||'';el.style.visibility=current.providerIcon?'visible':'hidden'});root.querySelector('.gvuhd-visit').textContent='VISIT '+String(current.provider||'PROVIDER').toUpperCase();img.onload=fit;img.src=current.previewUrl||'';img.alt=current.title||'Galaxy image';root.classList.add('open');root.setAttribute('aria-hidden','false');requestAnimationFrame(fit)}
function close(){if(!root)return;uhdToken++;loading.classList.remove('on');root.classList.remove('open');root.setAttribute('aria-hidden','true');current=null;pointers.clear();reset()}
function loadUHD(){if(!current||!current.uhdUrl||current.uhdUrl===img.src)return;const token=++uhdToken;loading.classList.add('on');const hi=new Image();hi.decoding='async';hi.onload=()=>{if(token!==uhdToken||!current)return;const oldScale=scale,oldX=x,oldY=y;img.onload=()=>{fit();scale=oldScale;x=oldX;y=oldY;apply();loading.classList.remove('on')};img.src=hi.src};hi.onerror=()=>{if(token===uhdToken)loading.classList.remove('on')};hi.src=current.uhdUrl}
window.addEventListener('resize',()=>{if(root&&root.classList.contains('open'))fit()});
window.GVUHDViewport={open,close,version:'0001'};
})();