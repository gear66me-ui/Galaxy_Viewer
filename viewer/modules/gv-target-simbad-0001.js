/*
 * Galaxy Viewer Target / SIMBAD Module 0001
 * Standalone target control extracted from the approved Galaxy Viewer 7P target lineage.
 * Owns only target DOM, visual state, SIMBAD pointer activation, status interaction, and callbacks.
 */
(function(global){
  'use strict';

  const VERSION='0001';
  const STYLE_ID='gv-target-simbad-0001-style';
  const FONT_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001';
  const TARGET_ICON_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/icon_target_vector.svg?v=92b223268c18c7ed67c69c56374fc0bd968b8236';

  function installStyles(){
    if(document.getElementById(STYLE_ID))return;
    const style=document.createElement('style');
    style.id=STYLE_ID;
    style.textContent=`
@font-face{font-family:"Space Age";src:url("${FONT_URL}") format("opentype");font-style:normal;font-weight:400;font-display:block}
.gv-target-simbad-root{position:relative;width:36px;height:36px;overflow:visible;font-family:"Space Age",sans-serif;text-transform:uppercase}
.gv-target-simbad-root *{box-sizing:border-box}
.gv-target-simbad-button,.gv-target-simbad-button:hover,.gv-target-simbad-button:focus,.gv-target-simbad-button:active{appearance:none;-webkit-appearance:none;position:relative;display:flex;visibility:visible;opacity:1;align-items:center;justify-content:center;width:36px;min-width:36px;max-width:36px;height:36px;min-height:36px;max-height:36px;margin:0;padding:0;overflow:hidden;background:linear-gradient(145deg,#081B3A 0%,#0B3177 42%,#1484DB 76%,#296DBD 100%);border:1px solid #7CCBFF;border-radius:6px;cursor:pointer;touch-action:manipulation;outline:none;box-shadow:inset 0 0 7px rgba(221,248,255,.16),0 0 10px rgba(88,191,255,.38);pointer-events:auto}
.gv-target-simbad-button::before{content:"";position:absolute;inset:0;z-index:0;border-radius:5px;pointer-events:none;opacity:0}
.gv-target-simbad-button img{position:relative;z-index:2;display:block;width:34px;height:34px;object-fit:contain;filter:none;pointer-events:none;user-select:none;-webkit-user-drag:none}
.gv-target-simbad-comet{position:absolute;left:50%;top:50%;width:0;height:0;animation:gv-target-simbad-comet-orbit 2.8s linear infinite;pointer-events:none;z-index:3}
.gv-target-simbad-comet i{position:absolute;left:-2px;top:-2px;width:4px;height:4px;border-radius:50%;background:#62D8FF;transform:rotate(var(--gv-angle)) translateY(-13px) scale(var(--gv-scale));opacity:var(--gv-opacity);box-shadow:0 0 4px rgba(98,216,255,.85)}
.gv-target-simbad-comet i:nth-child(1){--gv-angle:0deg;--gv-scale:1;--gv-opacity:1;background:#FFFFFF;box-shadow:0 0 3px 1px #FFFFFF,0 0 7px 2px #62D8FF}
.gv-target-simbad-comet i:nth-child(2){--gv-angle:-15deg;--gv-scale:.88;--gv-opacity:.84}
.gv-target-simbad-comet i:nth-child(3){--gv-angle:-30deg;--gv-scale:.76;--gv-opacity:.68}
.gv-target-simbad-comet i:nth-child(4){--gv-angle:-45deg;--gv-scale:.64;--gv-opacity:.52}
.gv-target-simbad-comet i:nth-child(5){--gv-angle:-60deg;--gv-scale:.52;--gv-opacity:.38}
.gv-target-simbad-comet i:nth-child(6){--gv-angle:-75deg;--gv-scale:.42;--gv-opacity:.26}
.gv-target-simbad-comet i:nth-child(7){--gv-angle:-90deg;--gv-scale:.32;--gv-opacity:.16}
.gv-target-simbad-comet i:nth-child(8){--gv-angle:-105deg;--gv-scale:.24;--gv-opacity:.08}
.gv-target-simbad-button[aria-pressed="true"]::before{opacity:1;background:radial-gradient(circle at 18% 20%,rgba(221,248,255,.92) 0 2px,rgba(124,203,255,.58) 5px,transparent 11px),radial-gradient(circle at 82% 22%,rgba(183,235,255,.82) 0 2px,rgba(88,191,255,.54) 6px,transparent 12px),radial-gradient(circle at 20% 82%,rgba(143,229,255,.78) 0 2px,rgba(49,125,212,.52) 7px,transparent 13px),radial-gradient(circle at 82% 80%,rgba(221,248,255,.72) 0 2px,rgba(20,132,219,.54) 7px,transparent 13px),linear-gradient(145deg,#0B3177 0%,#1484DB 48%,#296DBD 100%);box-shadow:inset 0 0 9px rgba(221,248,255,.48),inset 0 0 4px rgba(247,253,255,.58),0 0 10px rgba(88,191,255,.58)}
.gv-target-simbad-button[aria-pressed="true"] .gv-target-simbad-comet{animation:none;opacity:1;transform:translate(-50%,-50%)}
.gv-target-simbad-button[aria-pressed="true"] .gv-target-simbad-comet i{opacity:0;transform:none}
.gv-target-simbad-button[aria-pressed="true"] .gv-target-simbad-comet i:nth-child(1){left:-1px;top:-1px;width:2px;height:2px;border-radius:50%;opacity:1;transform:none;background:#FFFFFF;box-shadow:0 0 2px 1px #FFFFFF,0 0 6px 2px #62D8FF}
.gv-target-simbad-status{position:absolute;right:0;top:44px;z-index:2;display:none;visibility:hidden;opacity:0;align-items:center;justify-content:center;flex-direction:column;width:140px;min-width:140px;max-width:140px;height:72px;min-height:72px;max-height:72px;margin:0;padding:6px;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,#081B3A 0%,#0B3177 56%,#296DBD 100%);color:#DDF8FF;font:400 8px/1.35 "Space Age",sans-serif;text-align:center;white-space:nowrap;box-shadow:0 0 9px rgba(98,216,255,.34);pointer-events:none}
.gv-target-simbad-status>span{display:block;width:100%;text-align:center;white-space:nowrap}
.gv-target-simbad-status.gv-active{display:flex;visibility:visible;opacity:1;pointer-events:auto;cursor:pointer;animation:gv-target-simbad-status-pulse 3s cubic-bezier(.35,.02,.18,1) infinite;will-change:filter}
@keyframes gv-target-simbad-comet-orbit{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes gv-target-simbad-status-pulse{0%{filter:drop-shadow(0 0 4px rgba(255,255,255,.98)) drop-shadow(0 0 10px rgba(98,216,255,.96))}10%{filter:drop-shadow(0 0 2.8px rgba(214,247,255,.76)) drop-shadow(0 0 8px rgba(98,216,255,.82))}32%{filter:drop-shadow(0 0 2px rgba(188,239,255,.56)) drop-shadow(0 0 6px rgba(98,216,255,.64))}58%{filter:drop-shadow(0 0 1px rgba(172,232,255,.34)) drop-shadow(0 0 3.5px rgba(98,216,255,.38))}86%{filter:drop-shadow(0 0 .5px rgba(160,225,255,.18)) drop-shadow(0 0 2px rgba(98,216,255,.22))}94%{filter:drop-shadow(0 0 2px rgba(255,255,255,.82)) drop-shadow(0 0 7px rgba(160,236,255,.76))}100%{filter:drop-shadow(0 0 5px #fff) drop-shadow(0 0 12px rgba(98,216,255,1))}}
@media (prefers-reduced-motion:reduce){.gv-target-simbad-comet{animation:none;transform:rotate(35deg)}.gv-target-simbad-button[aria-pressed="true"] .gv-target-simbad-comet{transform:translate(-50%,-50%)}.gv-target-simbad-status.gv-active{animation:none;filter:none}}
`;
    document.head.appendChild(style);
  }

  function createInstance(options={}){
    installStyles();
    const host=options.host;
    const aladin=options.aladin;
    const viewerRoot=options.viewerRoot||document;
    if(!(host instanceof Element))throw new TypeError('GalaxyViewerTargetSimbad.init requires an Element host');
    if(!aladin)throw new TypeError('GalaxyViewerTargetSimbad.init requires an Aladin instance');

    const root=document.createElement('div');
    root.className='gv-target-simbad-root';
    root.dataset.gvTargetSimbadVersion=VERSION;

    const button=document.createElement('button');
    button.type='button';
    button.className='gv-target-simbad-button';
    button.title='SIMBAD TARGET';
    button.setAttribute('aria-label','SIMBAD TARGET');
    button.setAttribute('aria-pressed','false');
    button.innerHTML=`<img src="${TARGET_ICON_URL}" alt="" aria-hidden="true" draggable="false"><span class="gv-target-simbad-comet" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>`;

    const status=document.createElement('div');
    status.className='gv-target-simbad-status';
    status.setAttribute('role','button');
    status.setAttribute('tabindex','0');
    status.setAttribute('aria-live','polite');
    status.setAttribute('aria-label','DEACTIVATE TARGET MODE AND RESUME NAVIGATION');
    status.setAttribute('title','TAP TO EXIT TARGET MODE AND RESUME NAVIGATION');
    status.innerHTML='<span>SELECT A GALAXY</span><span>OR A STAR</span><span>TAP HERE AGAIN</span><span>TO EXIT TARGET MODE</span>';

    root.append(button,status);
    host.replaceChildren(root);

    let destroyed=false;
    let active=false;

    function findNativeSimbadEngine(){
      const scope=viewerRoot instanceof Element?viewerRoot:document;
      const claimed=scope.querySelector?.('button.gv-native-simbad-engine');
      if(claimed)return claimed;
      const direct=scope.querySelector?.("button.aladin-simbadPointer-control,button.aladin-simbadPointerControl,button.aladin-btn[class*='simbadPointer']");
      if(direct)return direct;
      const wrapper=scope.querySelector?.(".aladin-simbadPointer-control,.aladin-simbadPointerControl,[class*='simbadPointer']");
      return wrapper?.matches?.('button.aladin-btn')?wrapper:wrapper?.querySelector?.('button.aladin-btn')||null;
    }

    function applySimbadPointer(next){
      if(typeof aladin.useSimbadPointer==='function'){
        aladin.useSimbadPointer(next);
        return true;
      }
      const nativeButton=findNativeSimbadEngine();
      if(nativeButton){nativeButton.click();return true}
      return false;
    }

    function emit(){
      const detail={active,version:VERSION};
      root.dispatchEvent(new CustomEvent('gv-target-simbad-toggle',{bubbles:true,detail}));
      options.onToggle?.(active,detail);
    }

    function setActive(next,{notify=true}={}){
      if(destroyed)return false;
      next=Boolean(next);
      if(next===active)return active;
      applySimbadPointer(next);
      active=next;
      button.setAttribute('aria-pressed',active?'true':'false');
      status.classList.toggle('gv-active',active);
      if(notify)emit();
      return active;
    }

    function toggle(event){
      event?.preventDefault?.();
      event?.stopPropagation?.();
      setActive(!active);
    }
    function deactivate(event){
      event?.preventDefault?.();
      event?.stopPropagation?.();
      if(active)setActive(false);
    }

    button.addEventListener('click',toggle);
    status.addEventListener('click',deactivate);
    status.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '||event.key==='Spacebar')deactivate(event)});

    const api={
      version:VERSION,
      root,
      button,
      status,
      get active(){return active},
      setActive,
      toggle(){return setActive(!active)},
      destroy(){
        if(destroyed)return;
        if(active){try{applySimbadPointer(false)}catch(_){}}
        destroyed=true;
        button.removeEventListener('click',toggle);
        status.removeEventListener('click',deactivate);
        host.replaceChildren();
      }
    };
    root.__gvTargetSimbad=api;
    return api;
  }

  global.GalaxyViewerTargetSimbad=Object.freeze({version:VERSION,init:createInstance});
})(window);
