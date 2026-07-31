/* Galaxy Viewer 5U — active Target hierarchy refinement only.
   Inactive: preserves the original circular comet orbit.
   Active: keeps a smaller centered comet, gives the Target artwork a steady
   cyan neon glow, and pulses only the separate status box.
   Target, status, Back, and Next all deactivate Target mode and restore orbit. */
(() => {
  const ROOT_ID='aladin-cosmic-command-test';
  const STATUS_TEXT='Target active · Pan locked · Tap to exit';

  function install(){
    const root=document.getElementById(ROOT_ID);
    if(!root)return false;

    if(!document.getElementById('gv-5u-active-state-style')){
      const style=document.createElement('style');
      style.id='gv-5u-active-state-style';
      style.textContent=`
@keyframes gv-5u-status-pulse{
  0%{filter:drop-shadow(0 0 4px rgba(255,255,255,.98)) drop-shadow(0 0 10px rgba(98,216,255,.96))}
  10%{filter:drop-shadow(0 0 2.8px rgba(214,247,255,.76)) drop-shadow(0 0 8px rgba(98,216,255,.82))}
  32%{filter:drop-shadow(0 0 2px rgba(188,239,255,.56)) drop-shadow(0 0 6px rgba(98,216,255,.64))}
  58%{filter:drop-shadow(0 0 1px rgba(172,232,255,.34)) drop-shadow(0 0 3.5px rgba(98,216,255,.38))}
  86%{filter:drop-shadow(0 0 .5px rgba(160,225,255,.18)) drop-shadow(0 0 2px rgba(98,216,255,.22))}
  94%{filter:drop-shadow(0 0 2px rgba(255,255,255,.82)) drop-shadow(0 0 7px rgba(160,236,255,.76))}
  100%{filter:drop-shadow(0 0 5px #fff) drop-shadow(0 0 12px rgba(98,216,255,1))}
}
#${ROOT_ID} button.gv-target-proxy[aria-pressed="true"]{
  box-shadow:0 0 10px rgba(184,177,240,.38)!important;
}
#${ROOT_ID} button.gv-target-proxy[aria-pressed="true"] img{
  filter:drop-shadow(0 0 2px rgba(255,255,255,.78)) drop-shadow(0 0 7px rgba(98,216,255,.92))!important;
}
#${ROOT_ID} button.gv-target-proxy[aria-pressed="true"] .gv-target-comet{
  animation:none!important;
  opacity:1!important;
  transform:rotate(0deg) scale(.70)!important;
  transform-origin:0 0!important;
}
#${ROOT_ID} .gv-target-status.gv-active{
  animation:gv-5u-status-pulse 3s cubic-bezier(.35,.02,.18,1) infinite!important;
  pointer-events:auto!important;
  cursor:pointer!important;
  will-change:filter;
}
@media (prefers-reduced-motion:reduce){
  #${ROOT_ID} .gv-target-status.gv-active{
    animation:none!important;
    filter:drop-shadow(0 0 3px rgba(255,255,255,.9)) drop-shadow(0 0 8px rgba(98,216,255,.9))!important;
  }
}
`;
      document.head.appendChild(style);
    }

    const proxy=root.querySelector('button.gv-target-proxy');
    const status=root.querySelector('.gv-target-status');
    if(!proxy||!status)return false;

    const deactivateTarget=()=>{
      if(proxy.getAttribute('aria-pressed')==='true')proxy.click();
    };

    if(status.textContent!==STATUS_TEXT)status.textContent=STATUS_TEXT;
    status.setAttribute('role','button');
    status.setAttribute('tabindex','0');
    status.setAttribute('aria-label','Deactivate Target mode and resume navigation');
    status.setAttribute('title','Tap to exit Target mode and resume navigation');

    if(status.dataset.gv5uBound!=='true'){
      status.dataset.gv5uBound='true';
      const deactivate=event=>{
        event.preventDefault();
        event.stopPropagation();
        deactivateTarget();
      };
      status.addEventListener('click',deactivate);
      status.addEventListener('keydown',event=>{
        if(event.key==='Enter'||event.key===' '||event.key==='Spacebar')deactivate(event);
      });
    }

    ['gv-back-galaxy','gv-next-galaxy'].forEach(id=>{
      const button=root.querySelector(`#${id}`);
      if(!button||button.dataset.gv5uTargetReset==='true')return;
      button.dataset.gv5uTargetReset='true';
      button.addEventListener('click',deactivateTarget,{capture:true});
    });
    return true;
  }

  [0,150,350,700,1200,2200].forEach(delay=>setTimeout(install,delay));
  const observer=new MutationObserver(()=>install());
  const begin=()=>{
    const root=document.getElementById(ROOT_ID);
    if(root)observer.observe(root,{childList:true,subtree:true});
    install();
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',begin,{once:true});
  else begin();
})();
