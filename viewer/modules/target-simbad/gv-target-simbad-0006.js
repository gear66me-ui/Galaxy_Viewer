/*
 * Galaxy Viewer Survey Selector 0006
 * Replaces dormant SIMBAD target interaction with provider-sequential Survey mode.
 * Owns only Target-button presentation, provider menu, selected-provider state, and callbacks.
 * Navigation/camera/catalog authority remains in RC-V1.0.0 viewer + Galaxy Route Engine.
 */
(function(global){
'use strict';

const VERSION='0006';
const STYLE_ID='gv-target-survey-0006-style';
const FONT_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf';
const TARGET_ICON_URL='https://cdn.jsdelivr.net/gh/gear66me-ui/Galaxy_Viewer@release/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg';

function installStyles(){
  if(document.getElementById(STYLE_ID))return;
  const style=document.createElement('style');
  style.id=STYLE_ID;
  style.textContent=`
@font-face{font-family:"GV Survey Space Age";src:url("${FONT_URL}") format("opentype");font-style:normal;font-weight:400;font-display:block}
.gv-target-survey-root{position:relative;width:36px;height:36px;overflow:visible;font-family:"GV Survey Space Age","Space Age",sans-serif;text-transform:uppercase}
.gv-target-survey-root *{box-sizing:border-box}
.gv-target-survey-button{appearance:none;-webkit-appearance:none;position:relative;display:flex;align-items:center;justify-content:center;width:36px;height:36px;margin:0;padding:0;overflow:hidden;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,#081B3A 0%,#0B3177 42%,#1484DB 76%,#296DBD 100%);box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 3px #DDF8FF,0 0 9px rgba(50,190,255,.72),0 0 18px rgba(20,116,219,.35);cursor:pointer;touch-action:manipulation;outline:none}
.gv-target-survey-button::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.38) 0%,rgba(118,225,255,.08) 25%,transparent 43%);pointer-events:none}
.gv-target-survey-button img{position:relative;z-index:2;width:34px;height:34px;display:block;object-fit:contain;pointer-events:none}
.gv-target-survey-button.gv-open,.gv-target-survey-button.gv-selected{border-color:#78FFAB;background:linear-gradient(145deg,#062B1D 0%,#08783F 42%,#13B968 76%,#38E69A 100%);box-shadow:inset 0 0 8px rgba(120,255,171,.25),0 0 5px #78FFAB,0 0 13px rgba(56,230,154,.78)}
.gv-target-survey-panel{position:absolute;right:0;top:44px;z-index:9500;width:226px;padding:8px;border:1px solid #7CCBFF;border-radius:12px;background:linear-gradient(145deg,rgba(3,17,38,.985),rgba(7,43,93,.985) 58%,rgba(4,21,47,.985));box-shadow:inset 0 1px 2px rgba(225,251,255,.30),0 0 18px rgba(50,190,255,.48);display:none;pointer-events:auto}
.gv-target-survey-panel.gv-open{display:block}
.gv-target-survey-title{height:22px;display:flex;align-items:center;justify-content:center;color:#DDF8FF;font:400 11px/1 "GV Survey Space Age",sans-serif;letter-spacing:1.1px;text-shadow:0 0 5px rgba(88,191,255,.82)}
.gv-target-survey-list{display:flex;flex-direction:column;gap:5px}
.gv-target-survey-tile{appearance:none;-webkit-appearance:none;position:relative;width:100%;height:44px;margin:0;padding:0 5px 0 12px;display:grid;grid-template-columns:minmax(0,1fr) 39px;align-items:center;gap:8px;border:1px solid #43CFFF;border-radius:10px;background:linear-gradient(180deg,#174E86 0%,#082C59 13%,#041B3E 54%,#07366A 88%,#0D5A98 100%);color:#F4FDFF;box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 2px rgba(221,248,255,.85),0 0 7px rgba(50,190,255,.56);cursor:pointer;overflow:hidden;text-align:left}
.gv-target-survey-tile::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.42) 0%,rgba(118,225,255,.07) 24%,transparent 42%);pointer-events:none}
.gv-target-survey-tile.gv-active{border-color:#78FFAB;background:linear-gradient(145deg,#062B1D 0%,#08783F 42%,#13B968 76%,#38E69A 100%);box-shadow:inset 0 0 8px rgba(120,255,171,.25),0 0 4px #78FFAB,0 0 12px rgba(56,230,154,.72)}
.gv-target-survey-copy{position:relative;z-index:2;min-width:0;display:flex;flex-direction:column;gap:4px}
.gv-target-survey-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font:400 12px/1 "GV Survey Space Age",sans-serif;letter-spacing:.55px;text-shadow:0 0 5px #fff,0 0 10px rgba(88,191,255,.82)}
.gv-target-survey-count{font:400 7px/1 "GV Survey Space Age",sans-serif;letter-spacing:.7px;color:#9EDCFF;text-shadow:0 0 4px rgba(88,191,255,.58)}
.gv-target-survey-tile.gv-active .gv-target-survey-count{color:#DFFFF0}
.gv-target-survey-icon{position:relative;z-index:2;justify-self:end;width:34px;height:34px;border-radius:7px;object-fit:cover;border:1px solid rgba(221,248,255,.56);box-shadow:0 0 5px rgba(88,191,255,.52)}
.gv-target-survey-all-icon{object-fit:contain;border:0;box-shadow:none}
.gv-target-survey-index{position:absolute;right:46px;top:50%;z-index:3;transform:translateY(-50%);font:400 7px/1 "GV Survey Space Age",sans-serif;letter-spacing:.45px;color:#DFFFF0;text-shadow:0 0 4px rgba(120,255,171,.8);pointer-events:none}
@media(max-width:390px){.gv-target-survey-panel{width:214px}}
`;
  document.head.appendChild(style);
}

function createInstance(options={}){
  installStyles();
  const host=options.host;
  if(!(host instanceof Element))throw new TypeError('GalaxyViewerTargetSimbad.init requires an Element host');

  const root=document.createElement('div');
  root.className='gv-target-survey-root';
  root.dataset.gvTargetSimbadVersion=VERSION;

  const button=document.createElement('button');
  button.type='button';
  button.className='gv-target-survey-button';
  button.title='SURVEY';
  button.setAttribute('aria-label','SURVEY');
  button.setAttribute('aria-expanded','false');
  button.innerHTML=`<img src="${TARGET_ICON_URL}" alt="" aria-hidden="true" draggable="false">`;

  const panel=document.createElement('div');
  panel.className='gv-target-survey-panel';
  panel.innerHTML='<div class="gv-target-survey-title">SURVEY</div><div class="gv-target-survey-list"></div>';
  const list=panel.querySelector('.gv-target-survey-list');

  root.append(button,panel);
  host.replaceChildren(root);

  let destroyed=false,open=false,providers=[],activeProvider='',activeIndex=0,activeTotal=0;

  function close(){
    open=false;panel.classList.remove('gv-open');button.classList.remove('gv-open');button.setAttribute('aria-expanded','false');
  }
  function openPanel(){
    if(destroyed||!providers.length)return;
    open=true;panel.classList.add('gv-open');button.classList.add('gv-open');button.setAttribute('aria-expanded','true');
  }
  function toggle(){open?close():openPanel()}

  function render(){
    list.replaceChildren();
    const all=document.createElement('button');
    all.type='button';
    all.className='gv-target-survey-tile'+(!activeProvider?' gv-active':'');
    all.dataset.provider='';
    all.innerHTML=`<span class="gv-target-survey-copy"><span class="gv-target-survey-name">ALL PROVIDERS</span><span class="gv-target-survey-count">RANDOM GALAXY MODE</span></span><img class="gv-target-survey-icon gv-target-survey-all-icon" src="${TARGET_ICON_URL}" alt="" aria-hidden="true">`;
    all.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();close();options.onExitSurvey?.();});
    list.appendChild(all);

    for(const provider of providers){
      const tile=document.createElement('button');
      tile.type='button';
      tile.className='gv-target-survey-tile'+(provider.key===activeProvider?' gv-active':'');
      tile.dataset.provider=provider.key;
      const position=provider.key===activeProvider&&activeTotal>0?`<span class="gv-target-survey-index">${activeIndex}/${activeTotal}</span>`:'';
      tile.innerHTML=`<span class="gv-target-survey-copy"><span class="gv-target-survey-name">${provider.label}</span><span class="gv-target-survey-count">${provider.count} IMAGE${provider.count===1?'':'S'}</span></span>${position}<img class="gv-target-survey-icon" src="${provider.icon}" alt="" aria-hidden="true">`;
      tile.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();close();options.onSelectProvider?.(provider.key,provider);});
      list.appendChild(tile);
    }
    button.classList.toggle('gv-selected',Boolean(activeProvider));
  }

  button.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();toggle()});

  const api={
    version:VERSION,root,button,panel,
    get open(){return open},
    get activeProvider(){return activeProvider},
    setProviders(next){
      providers=Array.isArray(next)?next.map(x=>({key:String(x?.key||'').toUpperCase(),label:String(x?.label||x?.key||'').toUpperCase(),count:Number(x?.count)||0,icon:String(x?.icon||TARGET_ICON_URL)})).filter(x=>x.key&&x.count>0):[];
      render();return providers.length;
    },
    setActiveProvider(provider,{index=0,total=0}={}){
      activeProvider=String(provider||'').toUpperCase();activeIndex=Number(index)||0;activeTotal=Number(total)||0;render();
    },
    open:openPanel,close,toggle,
    destroy(){if(destroyed)return;destroyed=true;host.replaceChildren()}
  };
  root.__gvTargetSimbad=api;
  render();
  return api;
}

global.GalaxyViewerTargetSimbad=Object.freeze({version:VERSION,init:createInstance});
})(window);
