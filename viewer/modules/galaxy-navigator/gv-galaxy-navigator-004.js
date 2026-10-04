/* Galaxy Viewer Galaxy Navigator 004
 * Presentation and user-intent module only.
 * Visual baseline restored from Random Galaxy 0166.
 * Owns: Back / Random Galaxy / Forward UI, stars, wait comets, enabled/busy state.
 * Does NOT own: route planning, catalog selection, RA/Dec/FOV, Aladin camera, AVM.
 */
(function(global){
'use strict';
const VERSION='004';
const FONT_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf';

function installStyle(){
 if(document.getElementById('gv-galaxy-navigator-004-style'))return;
 const style=document.createElement('style');
 style.id='gv-galaxy-navigator-004-style';
 style.textContent=`
@font-face{font-family:"GV Space Age";src:url("${FONT_URL}") format("opentype");font-display:swap}
.gv-galaxy-navigator{display:flex;align-items:center;justify-content:center;gap:7px;width:min(100%,430px);margin:0 auto}
#gv-random-galaxy,.gv-galaxy-history{appearance:none;-webkit-appearance:none;position:relative;height:42px;margin:0;border:1px solid #43CFFF;border-radius:10px;background:linear-gradient(180deg,#174E86 0%,#082C59 13%,#041B3E 54%,#07366A 88%,#0D5A98 100%) padding-box;color:#F4FDFF;box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 2px rgba(221,248,255,.88),0 0 7px rgba(50,190,255,.58);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto;transition:transform .08s ease,filter .12s ease,box-shadow .12s ease}
#gv-random-galaxy::after,.gv-galaxy-history::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.46) 0%,rgba(118,225,255,.08) 24%,transparent 42%);pointer-events:none}
#gv-random-galaxy{position:relative;display:flex;flex:1 1 auto;min-width:0;align-items:center;justify-content:center;padding:0 12px;overflow:hidden;font:400 15.5px/1 "GV Space Age",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 5px #fff,0 0 11px rgba(88,191,255,.85)}
.gv-galaxy-history{display:flex;flex:0 0 42px;align-items:center;justify-content:center;width:42px;padding:0;color:transparent;overflow:hidden}
.gv-galaxy-history::before{content:"";position:absolute;left:50%;top:50%;width:16px;height:16px;border:solid #F4FDFF;border-width:0 5px 5px 0;filter:drop-shadow(0 0 4px #8DDAFF) drop-shadow(0 0 8px #58BFFF);transform:translate(-62%,-50%) rotate(-45deg);box-sizing:border-box}
.gv-galaxy-history-back::before{transform:translate(-38%,-50%) rotate(135deg)}
#gv-random-galaxy:active,.gv-galaxy-history:active{transform:translateY(2px) scale(.985);filter:brightness(1.14);box-shadow:inset 0 3px 7px rgba(0,0,0,.52),inset 0 0 10px rgba(88,191,255,.36),0 0 5px rgba(88,191,255,.62)}
.gv-galaxy-history:disabled{opacity:1;cursor:default;filter:saturate(.72) brightness(.72);background:linear-gradient(180deg,#123E6C 0%,#07284F 14%,#03162F 54%,#062B52 88%,#0A4779 100%);box-shadow:inset 0 2px 2px rgba(205,245,255,.52),inset 0 -3px 5px rgba(0,0,0,.58),inset 0 0 10px rgba(41,153,255,.22),0 0 2px rgba(221,248,255,.58),0 0 5px rgba(50,190,255,.32)}
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
#gv-random-galaxy.gvrg-random-traveling,#gv-random-galaxy.gvrg-random-start{background:linear-gradient(145deg,#062B1D 0%,#08783F 42%,#13B968 76%,#38E69A 100%) padding-box,linear-gradient(135deg,#38E69A 0%,#78FFAB 48%,#D9FFE9 100%) border-box;color:#DFFFF0;text-shadow:0 0 5px rgba(120,255,171,.9);box-shadow:inset 0 0 8px rgba(120,255,171,.22),0 0 12px rgba(56,230,154,.62)}#gv-random-galaxy.gvrg-press-green{border-color:#78FFAB!important;background:linear-gradient(145deg,#062B1D 0%,#08783F 42%,#13B968 76%,#38E69A 100%)!important;color:#DFFFF0!important;text-shadow:0 0 5px rgba(120,255,171,.95)!important;box-shadow:inset 0 0 8px rgba(120,255,171,.28),0 0 5px #78FFAB,0 0 14px rgba(56,230,154,.92)!important}
#gv-random-galaxy .gvrg-random-comet-left{animation-delay:-1.4s}
#gv-random-galaxy.gvrg-survey-mode .gvrg-random-star-wrap{display:none}
#gv-random-galaxy.gvrg-survey-mode .gvrg-random-layout{display:flex;align-items:center;justify-content:center;grid-template-columns:none;column-gap:0}
#gv-random-galaxy.gvrg-survey-mode .gvrg-random-label{grid-column:auto;white-space:nowrap;font-size:14px;letter-spacing:.28px;transition:opacity .28s ease}
#gv-random-galaxy.gvrg-survey-mode.gvrg-survey-end{filter:saturate(.72) brightness(.82)}
.gv-survey-selector-backdrop{position:fixed;inset:0;z-index:9800;display:none;align-items:center;justify-content:center;background:rgba(0,4,14,.60);backdrop-filter:blur(1.5px);-webkit-backdrop-filter:blur(1.5px)}
.gv-survey-selector-backdrop.gv-open{display:flex}
.gv-survey-selector{position:relative;width:60vw;height:60vh;display:flex;flex-direction:column;overflow:hidden;border:1px solid #43CFFF;border-radius:15px;background:linear-gradient(155deg,rgba(3,18,43,.992),rgba(5,43,91,.992) 58%,rgba(2,16,38,.996));box-shadow:inset 0 2px 2px rgba(225,251,255,.30),inset 0 -4px 10px rgba(0,0,0,.58),0 0 8px rgba(221,248,255,.74),0 0 24px rgba(50,190,255,.52)}
.gv-survey-selector::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.14) 0%,rgba(118,225,255,.04) 17%,transparent 32%);pointer-events:none;z-index:0}
.gv-survey-selector-head{position:relative;z-index:2;flex:0 0 42px;display:grid;grid-template-columns:1fr 28px;align-items:center;gap:5px;padding:5px 6px 5px 10px;border-bottom:1px solid rgba(67,207,255,.52);background:linear-gradient(180deg,rgba(23,78,134,.78),rgba(4,27,62,.48))}
.gv-survey-selector-title{min-width:0;display:flex;flex-direction:column;gap:3px}
.gv-survey-selector-provider{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#F4FDFF;font:400 10px/1 "GV Space Age",sans-serif;letter-spacing:.65px;text-shadow:0 0 5px #fff,0 0 9px rgba(88,191,255,.72)}
.gv-survey-selector-hint{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#9EDCFF;font:400 6.8px/1 "GV Space Age",sans-serif;letter-spacing:.45px}
.gv-survey-selector-close{appearance:none;-webkit-appearance:none;width:28px;height:28px;margin:0;padding:0;border:1px solid #43CFFF;border-radius:8px;background:linear-gradient(180deg,#174E86,#041B3E 58%,#0D5A98);color:#F4FDFF;font:700 16px/1 system-ui,sans-serif;text-shadow:0 0 5px #fff;box-shadow:inset 0 1px 2px rgba(225,251,255,.62),0 0 5px rgba(50,190,255,.5)}
.gv-survey-selector-list{position:relative;z-index:2;flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:5px;scrollbar-width:thin;scrollbar-color:#43CFFF rgba(4,27,62,.74);touch-action:pan-y}
.gv-survey-selector-row{appearance:none;-webkit-appearance:none;position:relative;width:100%;height:40px;margin:0 0 4px 0;padding:3px 7px 3px 3px;display:grid;grid-template-columns:32px minmax(0,1fr);align-items:center;gap:7px;border:1px solid rgba(67,207,255,.72);border-radius:9px;background:linear-gradient(180deg,rgba(23,78,134,.86),rgba(4,27,62,.96) 58%,rgba(13,90,152,.78));color:#F4FDFF;box-shadow:inset 0 1px 2px rgba(225,251,255,.32),inset 0 -2px 4px rgba(0,0,0,.42),0 0 4px rgba(50,190,255,.26);text-align:left;overflow:hidden}
.gv-survey-selector-row.gv-current{border-color:#78FFAB;background:linear-gradient(145deg,rgba(6,43,29,.96),rgba(8,120,63,.94) 44%,rgba(19,185,104,.88));box-shadow:inset 0 0 6px rgba(120,255,171,.20),0 0 5px rgba(120,255,171,.64)}
.gv-survey-selector-thumb{width:32px;height:32px;display:flex;align-items:center;justify-content:center;overflow:hidden;border:1px solid rgba(158,220,255,.66);border-radius:8px;background:radial-gradient(circle at 50% 45%,#0B2749 0%,#02070F 72%);box-shadow:inset 0 0 5px rgba(0,0,0,.52),0 0 4px rgba(88,191,255,.32)}
.gv-survey-selector-thumb img{display:block;width:100%;height:100%;object-fit:contain;object-position:center center;background:#000}
.gv-survey-selector-copy{min-width:0;display:flex;flex-direction:column;justify-content:center;gap:3px}
.gv-survey-selector-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#F4FDFF;font:400 9.2px/1 "GV Space Age",sans-serif;letter-spacing:.22px;text-shadow:0 0 4px rgba(255,255,255,.76),0 0 7px rgba(88,191,255,.54)}
.gv-survey-selector-meta{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#9EDCFF;font:400 6.7px/1 "GV Space Age",sans-serif;letter-spacing:.24px}
.gv-survey-selector-row.gv-current .gv-survey-selector-meta{color:#DFFFF0}
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
 let randomPressTimer=0;
 let surveyState=null,surveyTimer=0,surveyMessageIndex=0,surveyTraveling=false,surveyItems=[];
 const label=random.querySelector('.gvrg-random-label');
 const stopSurveyCycle=()=>{clearInterval(surveyTimer);surveyTimer=0};
 const surveyCounterText=()=>surveyState?`${surveyState.provider} ${surveyState.current} OF ${surveyState.total}`:'';
 const surveyMessages=()=>{
   if(!surveyState)return [];
   const base=[surveyCounterText()];
   if(surveyState.current<surveyState.total)base.push('PRESS FOR NEXT');
   return base
 };
 const renderSurveyLabel=()=>{
   if(!surveyState||surveyTraveling)return;
   const atEnd=surveyState.current>=surveyState.total;
   random.classList.toggle('gvrg-survey-end',atEnd);
   const messages=surveyMessages();
   if(!messages.length)return;
   surveyMessageIndex%=messages.length;
   const text=messages[surveyMessageIndex];
   if(label){label.style.opacity='0';setTimeout(()=>{if(label&&!surveyTraveling){label.textContent=text;label.style.opacity='1'}},120)}
   random.setAttribute('aria-label',text);
 };
 const startSurveyCycle=()=>{
   stopSurveyCycle();surveyMessageIndex=0;renderSurveyLabel();
   if(!surveyState||surveyTraveling)return;
   surveyTimer=setInterval(()=>{const messages=surveyMessages();if(!messages.length)return;surveyMessageIndex=(surveyMessageIndex+1)%messages.length;renderSurveyLabel()},1200);
 };
 const flashRandom=()=>{if(random.disabled)return;random.classList.add('gvrg-press-green');clearTimeout(randomPressTimer);randomPressTimer=setTimeout(()=>random.classList.remove('gvrg-press-green'),520)};

 let selectorBackdrop=null,selectorScrollRaf=0;
 const thumbnailCache=new Map(),thumbnailQueue=[];let thumbnailActive=0;
 const destroySelector=()=>{
   if(selectorScrollRaf)cancelAnimationFrame(selectorScrollRaf);
   selectorScrollRaf=0;
   selectorBackdrop?.remove?.();selectorBackdrop=null
 };
 const closeSelector=()=>destroySelector();
 const pumpThumbnailQueue=()=>{
   while(thumbnailActive<4&&thumbnailQueue.length){
     const job=thumbnailQueue.shift();
     if(!job?.img?.isConnected)continue;
     const candidates=job.candidates||[];
     let attempt=0;thumbnailActive++;
     const tryNext=()=>{
       const src=candidates[attempt++];
       if(!src){thumbnailActive--;pumpThumbnailQueue();return}
       const cached=thumbnailCache.get(src);
       if(cached==='loaded'){job.img.src=src;job.img.style.display='block';thumbnailActive--;pumpThumbnailQueue();return}
       if(cached==='failed'){tryNext();return}
       const pre=new Image();pre.decoding='async';
       pre.onload=async()=>{
         thumbnailCache.set(src,'loaded');
         try{await pre.decode?.()}catch(_){}
         if(job.img.isConnected){job.img.src=src;job.img.style.display='block'}
         thumbnailActive--;pumpThumbnailQueue()
       };
       pre.onerror=()=>{thumbnailCache.set(src,'failed');tryNext()};
       pre.src=src;
     };
     tryNext();
   }
 };
 const queueThumbnail=(img,candidates)=>{
   if(!img||img.dataset.gvQueued==='1'||!Array.isArray(candidates)||!candidates.length)return;
   img.dataset.gvQueued='1';
   for(const src of candidates){
     if(thumbnailCache.get(src)==='loaded'){img.src=src;img.style.display='block';return}
   }
   thumbnailQueue.push({img,candidates});pumpThumbnailQueue()
 };
 const loadThumbnailWindow=(list)=>{
   if(!list?.isConnected)return;
   const rows=[...list.querySelectorAll('.gv-survey-selector-row')];
   if(!rows.length)return;
   const stride=44;
   const first=Math.max(0,Math.floor(list.scrollTop/stride)-4);
   const visible=Math.ceil(list.clientHeight/stride)+8;
   const last=Math.min(rows.length,first+visible);
   for(let i=first;i<last;i++){
     const img=rows[i].querySelector('.gv-survey-selector-thumb img');
     if(!img)continue;
     let candidates=[];
     try{candidates=JSON.parse(img.dataset.candidates||'[]')}catch(_){}
     queueThumbnail(img,candidates)
   }
 };
 const scheduleThumbnailWindow=(list)=>{
   if(selectorScrollRaf)cancelAnimationFrame(selectorScrollRaf);
   selectorScrollRaf=requestAnimationFrame(()=>{selectorScrollRaf=0;loadThumbnailWindow(list)})
 };
 const openSelector=()=>{
   if(!surveyState||surveyTraveling||!surveyItems.length)return;
   destroySelector();
   const backdrop=document.createElement('div');
   backdrop.className='gv-survey-selector-backdrop gv-open';
   backdrop.setAttribute('role','dialog');
   backdrop.setAttribute('aria-modal','true');
   backdrop.setAttribute('aria-label',`${surveyState.provider} galaxy selector`);
   const panel=document.createElement('div');
   panel.className='gv-survey-selector';
   const head=document.createElement('div');
   head.className='gv-survey-selector-head';
   head.innerHTML=`<div class="gv-survey-selector-title"><div class="gv-survey-selector-provider">${surveyState.provider} CATALOG</div><div class="gv-survey-selector-hint">${surveyState.current} OF ${surveyState.total} · TAP A GALAXY</div></div><button type="button" class="gv-survey-selector-close" aria-label="Close">×</button>`;
   const list=document.createElement('div');
   list.className='gv-survey-selector-list';
   const frag=document.createDocumentFragment();
   surveyItems.forEach((item,index)=>{
     const row=document.createElement('button');
     row.type='button';
     row.className='gv-survey-selector-row'+(index===surveyState.current-1?' gv-current':'');
     row.dataset.index=String(index);
     const thumb=document.createElement('span');
     thumb.className='gv-survey-selector-thumb';
     const img=document.createElement('img');
     img.alt='';
     img.decoding='async';
     img.loading='eager';
     img.fetchPriority='low';
     img.style.display='none';
     img.dataset.candidates=JSON.stringify(Array.isArray(item.thumbnails)?item.thumbnails:[]);
     img.addEventListener('error',()=>{img.removeAttribute('src');img.style.display='none'});
     thumb.appendChild(img);
     const copy=document.createElement('span');
     copy.className='gv-survey-selector-copy';
     const number=String(index+1).padStart(String(surveyState.total).length,'0');
     const name=String(item.name||item.designation||('IMAGE '+(index+1))).toUpperCase();
     const meta=[item.designation,item.constellation,item.imageType].map(v=>String(v||'').trim().toUpperCase()).filter((v,i,a)=>v&&v!==name&&a.indexOf(v)===i).slice(0,2).join(' · ');
     copy.innerHTML=`<span class="gv-survey-selector-name">${number} — ${name.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</span><span class="gv-survey-selector-meta">${(meta||surveyState.provider).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</span>`;
     row.append(thumb,copy);
     row.addEventListener('click',()=>{closeSelector();handlers.onSelectSurveyIndex?.(index)});
     frag.appendChild(row);
   });
   list.appendChild(frag);
   panel.append(head,list);
   backdrop.appendChild(panel);
   document.body.appendChild(backdrop);
   selectorBackdrop=backdrop;
   head.querySelector('.gv-survey-selector-close')?.addEventListener('click',closeSelector);
   backdrop.addEventListener('click',event=>{if(event.target===backdrop)closeSelector()});
   list.addEventListener('scroll',()=>scheduleThumbnailWindow(list),{passive:true});
   requestAnimationFrame(()=>{
     const current=list.querySelector('.gv-survey-selector-row.gv-current');
     current?.scrollIntoView?.({block:'center',inline:'nearest'});
     scheduleThumbnailWindow(list);
   });
 };

 back.addEventListener('click',()=>{if(!back.disabled)handlers.onBack?.()});
 random.addEventListener('pointerdown',event=>{
   if(event.button!==undefined&&event.button!==0)return;
   if(random.disabled||surveyTraveling)return;
   flashRandom()
 });
 random.addEventListener('click',()=>{
   if(random.disabled)return;
   flashRandom();
   handlers.onRandom?.()
 });
 forward.addEventListener('click',()=>{if(!forward.disabled)handlers.onForward?.()});

 return Object.freeze({VERSION,host,back,random,forward,
  setBusy(busy){
   random.classList.toggle('gvrg-random-busy',Boolean(busy));
   if(!surveyState)random.disabled=Boolean(busy)
  },
  setStart(start){
   if(surveyState)return;
   const on=Boolean(start);random.classList.toggle('gvrg-random-start',on);
   if(on)random.classList.remove('gvrg-random-traveling');
   if(label)label.textContent=on?'START':'RANDOM GALAXY';
   random.setAttribute('aria-label',on?'START':'RANDOM GALAXY')
  },
  setTraveling(traveling){
   const on=Boolean(traveling);surveyTraveling=on;
   random.classList.remove('gvrg-random-start');
   random.classList.toggle('gvrg-random-traveling',on);
   if(surveyState){
     if(on){
       stopSurveyCycle();closeSelector();
       if(label){label.style.opacity='1';label.textContent='TRAVELING'}
       random.setAttribute('aria-label','TRAVELING')
     }else startSurveyCycle();
     return
   }
   if(label)label.textContent=on?'TRAVELING':'RANDOM GALAXY';
   random.setAttribute('aria-label',on?'TRAVELING':'RANDOM GALAXY')
  },
  setSurvey({provider,current,total,items}={}){
   const p=String(provider||'').toUpperCase(),c=Math.max(1,Number(current)||1),t=Math.max(1,Number(total)||1);
   surveyState={provider:p,current:Math.min(c,t),total:t};
   if(Array.isArray(items))surveyItems=items.map(x=>Object.freeze({
     name:String(x?.name||''),
     designation:String(x?.designation||''),
     constellation:String(x?.constellation||''),
     imageType:String(x?.imageType||''),
     thumbnails:Object.freeze(Array.isArray(x?.thumbnails)?x.thumbnails.map(v=>String(v||'').trim()).filter(Boolean):[])
   }));
   random.classList.add('gvrg-survey-mode');
   random.classList.remove('gvrg-random-start','gvrg-random-traveling');
   surveyTraveling=false;startSurveyCycle()
  },
  clearSurvey(){
   stopSurveyCycle();closeSelector();surveyState=null;surveyItems=[];surveyMessageIndex=0;surveyTraveling=false;
   random.classList.remove('gvrg-survey-mode','gvrg-survey-end','gvrg-random-traveling');
   if(label){label.style.opacity='1';label.textContent='RANDOM GALAXY'}
   random.setAttribute('aria-label','RANDOM GALAXY')
  },
  openSurveySelector(){openSelector()},
  closeSurveySelector(){closeSelector()},
  setEnabled({back:be=true,random:re=true,forward:fe=true}={}){back.disabled=!be;random.disabled=!re;forward.disabled=!fe}
 });
}
global.GalaxyNavigator=Object.freeze({VERSION,mount});
})(typeof window!=='undefined'?window:globalThis);
