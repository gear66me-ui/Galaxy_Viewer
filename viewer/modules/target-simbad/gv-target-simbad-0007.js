/*
 * Galaxy Viewer Survey Selector 0007
 * Replaces dormant SIMBAD target interaction with provider-sequential Survey mode.
 * Owns only Target-button presentation, provider menu, selected-provider state, and callbacks.
 * Navigation/camera/catalog authority remains in RC-V1.0.0 viewer + Galaxy Route Engine.
 */
(function(global){
'use strict';

const VERSION='0007';
const STYLE_ID='gv-target-survey-0007-style';
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
.gv-target-survey-button{appearance:none;-webkit-appearance:none;position:relative;display:flex;align-items:center;justify-content:center;width:36px;height:36px;margin:0;padding:0;overflow:hidden;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,#081B3A 0%,#0B3177 42%,#1484DB 76%,#296DBD 100%);box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 3px #DDF8FF,0 0 9px rgba(50,190,255,.72),0 0 18px rgba(20,116,219,.35);cursor:pointer;touch-action:none;-webkit-touch-callout:none;user-select:none;outline:none}
.gv-target-survey-button::after{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(255,255,255,.38) 0%,rgba(118,225,255,.08) 25%,transparent 43%);pointer-events:none}
.gv-target-survey-button img{position:relative;z-index:2;width:34px;height:34px;display:block;object-fit:contain;pointer-events:none}
.gv-target-survey-button.gv-open,.gv-target-survey-button.gv-selected{border-color:#78FFAB;background:linear-gradient(145deg,#062B1D 0%,#08783F 42%,#13B968 76%,#38E69A 100%);box-shadow:inset 0 0 8px rgba(120,255,171,.25),0 0 5px #78FFAB,0 0 13px rgba(56,230,154,.78)}
.gv-target-survey-button.gv-press-green,.gv-target-survey-tile.gv-press-green{border-color:#78FFAB!important;background:linear-gradient(145deg,#062B1D 0%,#08783F 42%,#13B968 76%,#38E69A 100%)!important;color:#DFFFF0!important;box-shadow:inset 0 0 8px rgba(120,255,171,.28),0 0 6px #78FFAB,0 0 15px rgba(56,230,154,.92)!important}
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
.gv-target-survey-all-icon{box-sizing:border-box;object-fit:contain;padding:2px;background:linear-gradient(180deg,#174E86 0%,#082C59 15%,#041B3E 56%,#0D5A98 100%);border:1px solid rgba(221,248,255,.56);box-shadow:inset 0 1px 2px rgba(225,251,255,.42),inset 0 -2px 4px rgba(0,0,0,.46),0 0 5px rgba(88,191,255,.52)}
.gv-target-survey-index{position:absolute;right:46px;top:50%;z-index:3;transform:translateY(-50%);font:400 7px/1 "GV Survey Space Age",sans-serif;letter-spacing:.45px;color:#DFFFF0;text-shadow:0 0 4px rgba(120,255,171,.8);pointer-events:none}

.gv-target-calculator{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2147483000;width:min(66vw,420px);max-width:66vw;max-height:76dvh;overflow:auto;padding:12px;border:1px solid #7CCBFF;border-radius:14px;background:radial-gradient(ellipse at 50% 0%,rgba(20,78,134,.98),rgba(3,17,38,.99) 58%,rgba(2,9,24,.99));box-shadow:inset 0 1px 2px rgba(225,251,255,.3),0 0 20px rgba(50,190,255,.65),0 0 48px rgba(0,0,0,.85);display:none;pointer-events:auto;color:#EAFBFF;font-family:"GV Survey Space Age","Space Age",sans-serif;overscroll-behavior:contain}
.gv-target-calculator.gv-open{display:block}
.gv-target-calculator *{box-sizing:border-box}
.gv-target-calculator-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;color:#DDF8FF;font-size:10px;letter-spacing:1px;text-shadow:0 0 5px rgba(88,191,255,.82)}
.gv-target-calculator-close{width:25px;height:25px;border:1px solid #43CFFF;border-radius:6px;background:linear-gradient(180deg,#174E86,#041B3E);color:#EAFBFF;font:16px/1 sans-serif}
.gv-target-calculator-display{width:100%;min-height:48px;margin-bottom:8px;padding:9px 8px;overflow:hidden;border:1px solid #43CFFF;border-radius:7px;background:linear-gradient(180deg,#010914,#071C33);color:#9DFFDF;text-align:right;font:16px/1.4 "GV Survey Space Age","Space Age",sans-serif;overflow-wrap:anywhere;box-shadow:inset 0 0 9px #000,0 0 6px #008bce55}
.gv-target-calculator-keys{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px}
.gv-target-calculator-key{min-height:39px;border:1px solid #43CFFF;border-radius:7px;background:linear-gradient(180deg,#174E86 0%,#082C59 18%,#041B3E 62%,#0D5A98 100%);color:#F4FDFF;font:10px/1 "GV Survey Space Age","Space Age",sans-serif;box-shadow:inset 0 1px 2px #ffffff45,0 0 5px #32beff44;touch-action:manipulation}
.gv-target-calculator-key.gv-op{color:#9DFFDF;border-color:#78FFAB}
.gv-target-calculator-key.gv-equals{background:linear-gradient(145deg,#08783F,#13B968 76%,#38E69A);border-color:#78FFAB;color:#031b10}
.gv-target-calculator-key:active{filter:brightness(1.35);transform:translateY(1px)}
.gv-target-cosmo-data{margin-top:10px;padding:9px;border:1px solid rgba(67,207,255,.62);border-radius:9px;background:linear-gradient(180deg,rgba(1,9,20,.92),rgba(5,28,53,.96));box-shadow:inset 0 0 12px rgba(0,0,0,.5)}.gv-target-cosmo-title{margin-bottom:5px;color:#7CCBFF;font-size:9px;letter-spacing:1.2px;text-align:center}.gv-target-cosmo-row{display:flex;justify-content:space-between;align-items:flex-start;gap:7px;padding:5px 0;border-top:1px solid rgba(124,203,255,.18);font-size:8px;line-height:1.35}.gv-target-cosmo-row span{flex:1;color:#B8DDF4}.gv-target-cosmo-row b{max-width:56%;color:#9DFFDF;text-align:right;overflow-wrap:anywhere;font-size:8px}.gv-target-cosmo-note{margin-top:6px;color:#8FB8D5;font-size:7px;line-height:1.4;text-align:center}
@media(max-width:390px){.gv-target-calculator{width:66vw;max-width:66vw;padding:9px}.gv-target-calculator-key{min-height:35px}}

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

  const calculator=document.createElement('section');
  calculator.className='gv-target-calculator';
  calculator.setAttribute('aria-label','Simple calculator');
  calculator.innerHTML='<div class="gv-target-calculator-head"><span>GALAXY CALCULATOR</span><button type="button" class="gv-target-calculator-close" aria-label="Close calculator">×</button></div><div class="gv-target-calculator-display" aria-live="polite">0</div><div class="gv-target-calculator-keys">'+
  '<button class="gv-target-calculator-key" data-action="clear">AC</button><button class="gv-target-calculator-key" data-action="back">⌫</button><button class="gv-target-calculator-key gv-op" data-action="operator" data-value="%">%</button><button class="gv-target-calculator-key gv-op" data-action="operator" data-value="/">÷</button>'+
  '<button class="gv-target-calculator-key" data-action="digit" data-value="7">7</button><button class="gv-target-calculator-key" data-action="digit" data-value="8">8</button><button class="gv-target-calculator-key" data-action="digit" data-value="9">9</button><button class="gv-target-calculator-key gv-op" data-action="operator" data-value="*">×</button>'+
  '<button class="gv-target-calculator-key" data-action="digit" data-value="4">4</button><button class="gv-target-calculator-key" data-action="digit" data-value="5">5</button><button class="gv-target-calculator-key" data-action="digit" data-value="6">6</button><button class="gv-target-calculator-key gv-op" data-action="operator" data-value="-">−</button>'+
  '<button class="gv-target-calculator-key" data-action="digit" data-value="1">1</button><button class="gv-target-calculator-key" data-action="digit" data-value="2">2</button><button class="gv-target-calculator-key" data-action="digit" data-value="3">3</button><button class="gv-target-calculator-key gv-op" data-action="operator" data-value="+">+</button>'+
  '<button class="gv-target-calculator-key" data-action="sign">±</button><button class="gv-target-calculator-key" data-action="digit" data-value="0">0</button><button class="gv-target-calculator-key" data-action="decimal">.</button><button class="gv-target-calculator-key gv-equals" data-action="equals">=</button></div>'+
  '<section class="gv-target-cosmo-data" aria-label="Live cosmology data"><div class="gv-target-cosmo-title">LIVE COSMOLOGY</div><div class="gv-target-cosmo-row"><span>REDSHIFT Z</span><b data-cosmo="z">LOADING…</b></div><div class="gv-target-cosmo-row"><span>FOV X × Y</span><b data-cosmo="fov">LOADING…</b></div><div class="gv-target-cosmo-row"><span>PRESENT-DAY COMOVING</span><b data-cosmo="dc">LOADING…</b></div><div class="gv-target-cosmo-row"><span>DISTANCE AT EMISSION</span><b data-cosmo="dem">LOADING…</b></div><div class="gv-target-cosmo-note">FLAT ΛCDM · H₀ 67.6 · Ωₘ 0.315 · DISTANCES IN MLY</div></section>';
  calculator.addEventListener('gv-cosmo-data',event=>{const d=event.detail||{};const put=(key,value)=>{const el=calculator.querySelector('[data-cosmo="'+key+'"]');if(el)el.textContent=value??'UNAVAILABLE'};put('z',d.z??'UNAVAILABLE');put('fov',d.fov??'UNAVAILABLE');put('dc',d.dc??'UNAVAILABLE');put('dem',d.dem??'UNAVAILABLE')});
   const calculatorDisplay=calculator.querySelector('.gv-target-calculator-display');
  const calculatorClose=calculator.querySelector('.gv-target-calculator-close');
  const calculatorKeys=calculator.querySelector('.gv-target-calculator-keys');
  const list=panel.querySelector('.gv-target-survey-list');

  root.append(button,panel);
  host.replaceChildren(root);
  document.body.appendChild(calculator);

  let destroyed=false,open=false,providers=[],activeProvider='',activeIndex=0,activeTotal=0,pressTimer=0;
  let calculatorOpen=false,calculatorHoldTimer=0,calculatorLongPressed=false,calculatorDownPoint=null;
  let calcCurrent='0',calcStored=null,calcOperator=null,calcFresh=false;
  const calcRender=()=>{calculatorDisplay.textContent=calcCurrent;};
  const calcClose=()=>{calculatorOpen=false;calculator.classList.remove('gv-open');};
  const calcOpen=()=>{close();calculatorOpen=true;calculator.classList.add('gv-open');calcRender();calculator.querySelectorAll('[data-cosmo]').forEach(e=>e.textContent='LOADING…');window.dispatchEvent(new CustomEvent('gv-request-cosmo-calculator'));};
  const calcReset=()=>{calcCurrent='0';calcStored=null;calcOperator=null;calcFresh=false;calcRender();};
  const calcNumber=value=>{if(calcFresh){calcCurrent='0';calcFresh=false;}if(value==='.' ){if(!calcCurrent.includes('.'))calcCurrent+='.';}else if(calcCurrent==='0')calcCurrent=value;else if(calcCurrent.length<16)calcCurrent+=value;calcRender();};
  const calcOperate=op=>{const v=Number(calcCurrent);if(!Number.isFinite(v))return;if(calcStored!==null&&calcOperator&&!calcFresh){const result=calcApply(calcStored,v,calcOperator);if(result===null){calcCurrent='ERROR';calcStored=null;calcOperator=null;calcFresh=true;calcRender();return;}calcCurrent=calcFormat(result);}calcStored=Number(calcCurrent);calcOperator=op;calcFresh=true;calcRender();};
  const calcApply=(a,b,op)=>{let r;switch(op){case '+':r=a+b;break;case '-':r=a-b;break;case '*':r=a*b;break;case '/':if(b===0)return null;r=a/b;break;case '%':r=a%b;break;default:return b;}return Number.isFinite(r)?r:null;};
  const calcFormat=n=>{if(!Number.isFinite(n))return 'ERROR';return String(Number(n.toPrecision(12)));};
  const calcEquals=()=>{if(calcStored===null||!calcOperator||calcCurrent==='ERROR')return;const result=calcApply(calcStored,Number(calcCurrent),calcOperator);calcCurrent=result===null?'ERROR':calcFormat(result);calcStored=null;calcOperator=null;calcFresh=true;calcRender();};
  calculatorClose.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();calcClose();});
  calculatorKeys.addEventListener('click',event=>{const key=event.target.closest('button[data-action]');if(!key)return;event.preventDefault();event.stopPropagation();const action=key.dataset.action,value=key.dataset.value;if(action==='digit')calcNumber(value);else if(action==='decimal')calcNumber('.');else if(action==='operator')calcOperate(value);else if(action==='equals')calcEquals();else if(action==='clear')calcReset();else if(action==='back'){if(calcFresh){calcCurrent='0';calcFresh=false;}else calcCurrent=calcCurrent.length>1?calcCurrent.slice(0,-1):'0';calcRender();}else if(action==='sign'&&calcCurrent!=='0'&&calcCurrent!=='ERROR'){calcCurrent=calcCurrent.startsWith('-')?calcCurrent.slice(1):'-'+calcCurrent;calcRender();}});

  const flashGreen=element=>{if(!element)return;element.classList.add('gv-press-green');clearTimeout(element._gvPressGreenTimer);element._gvPressGreenTimer=setTimeout(()=>{if(element.isConnected)element.classList.remove('gv-press-green')},900)};

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
    all.addEventListener('pointerdown',event=>{if(event.button!==undefined&&event.button!==0)return;flashGreen(all)},true);
    all.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();flashGreen(all);close();options.onExitSurvey?.();});
    list.appendChild(all);

    for(const provider of providers){
      const tile=document.createElement('button');
      tile.type='button';
      tile.className='gv-target-survey-tile'+(provider.key===activeProvider?' gv-active':'');
      tile.dataset.provider=provider.key;
      const position=provider.key===activeProvider&&activeTotal>0?`<span class="gv-target-survey-index">${activeIndex}/${activeTotal}</span>`:'';
      tile.innerHTML=`<span class="gv-target-survey-copy"><span class="gv-target-survey-name">${provider.label}</span><span class="gv-target-survey-count">${provider.count} IMAGE${provider.count===1?'':'S'}</span></span>${position}<img class="gv-target-survey-icon" src="${provider.icon}" alt="" aria-hidden="true">`;
      tile.addEventListener('pointerdown',event=>{if(event.button!==undefined&&event.button!==0)return;flashGreen(tile)},true);
      tile.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();flashGreen(tile);close();options.onSelectProvider?.(provider.key,provider);});
      list.appendChild(tile);
    }
    button.classList.toggle('gv-selected',Boolean(activeProvider));
  }

  const startCalculatorHold=(x,y)=>{flashGreen(button);calculatorLongPressed=false;calculatorDownPoint={x:Number(x)||0,y:Number(y)||0};clearTimeout(calculatorHoldTimer);calculatorHoldTimer=setTimeout(()=>{calculatorLongPressed=true;calcOpen();},650);};
  const cancelCalculatorHold=()=>{clearTimeout(calculatorHoldTimer);calculatorHoldTimer=0;calculatorDownPoint=null;};
  button.addEventListener('pointerdown',event=>{if(event.button!==undefined&&event.button!==0)return;startCalculatorHold(event.clientX,event.clientY);},true);
  button.addEventListener('touchstart',event=>{const t=event.changedTouches&&event.changedTouches[0];if(t)startCalculatorHold(t.clientX,t.clientY);},{capture:true,passive:true});
  for(const eventName of ['pointerup','pointercancel','touchend','touchcancel','mouseleave'])button.addEventListener(eventName,cancelCalculatorHold,true);
  button.addEventListener('pointermove',event=>{if(calculatorDownPoint&&Math.hypot(event.clientX-calculatorDownPoint.x,event.clientY-calculatorDownPoint.y)>24)cancelCalculatorHold()},true);
  button.addEventListener('touchmove',event=>{const t=event.changedTouches&&event.changedTouches[0];if(t&&calculatorDownPoint&&Math.hypot(t.clientX-calculatorDownPoint.x,t.clientY-calculatorDownPoint.y)>24)cancelCalculatorHold()},{capture:true,passive:true});
  // Android may emit contextmenu or pointercancel during a long touch; neither should open the survey menu.
  button.addEventListener('contextmenu',event=>{event.preventDefault();event.stopPropagation();if(calculatorOpen)calcClose()},true);
  button.addEventListener('click',event=>{event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();flashGreen(button);if(calculatorLongPressed){calculatorLongPressed=false;return;}if(calculatorOpen){calcClose();return;}toggle()});

  const api={
    version:VERSION,root,button,panel,
    get open(){return open},
    get calculatorOpen(){return calculatorOpen},
    openCalculator:calcOpen,closeCalculator:calcClose,
    get activeProvider(){return activeProvider},
    setProviders(next){
      providers=Array.isArray(next)?next.map(x=>({key:String(x?.key||'').toUpperCase(),label:String(x?.label||x?.key||'').toUpperCase(),count:Number(x?.count)||0,icon:String(x?.icon||TARGET_ICON_URL)})).filter(x=>x.key&&x.count>0):[];
      render();return providers.length;
    },
    setActiveProvider(provider,{index=0,total=0}={}){
      activeProvider=String(provider||'').toUpperCase();activeIndex=Number(index)||0;activeTotal=Number(total)||0;render();
    },
    open:openPanel,close,toggle,
    destroy(){if(destroyed)return;destroyed=true;calculator.remove();host.replaceChildren()}
  };
  root.__gvTargetSimbad=api;
  render();
  return api;
}

global.GalaxyViewerTargetSimbad=Object.freeze({version:VERSION,init:createInstance});
})(window);
