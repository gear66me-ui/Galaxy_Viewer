/* Galaxy Viewer 5T — active Target pulse correction only.
   Keeps the Target and status boxes visually independent.
   Preserves their existing shadows and adds a synchronized three-second
   blue-dimming pulse with a brief white/cyan flash.
   Keeps the active status box able to deactivate Target mode. */
(() => {
  const ROOT_ID='aladin-cosmic-command-test';

  function install(){
    const root=document.getElementById(ROOT_ID);
    if(!root)return false;

    if(!document.getElementById('gv-5t-active-pulse-style')){
      const style=document.createElement('style');
      style.id='gv-5t-active-pulse-style';
      style.textContent=`
@keyframes gv-5t-cosmic-pulse{
  0%{
    filter:drop-shadow(0 0 4px rgba(255,255,255,.98)) drop-shadow(0 0 10px rgba(98,216,255,.96));
  }
  10%{
    filter:drop-shadow(0 0 2.8px rgba(214,247,255,.76)) drop-shadow(0 0 8px rgba(98,216,255,.82));
  }
  32%{
    filter:drop-shadow(0 0 2px rgba(188,239,255,.56)) drop-shadow(0 0 6px rgba(98,216,255,.64));
  }
  58%{
    filter:drop-shadow(0 0 1px rgba(172,232,255,.34)) drop-shadow(0 0 3.5px rgba(98,216,255,.38));
  }
  86%{
    filter:drop-shadow(0 0 .5px rgba(160,225,255,.18)) drop-shadow(0 0 2px rgba(98,216,255,.22));
  }
  94%{
    filter:drop-shadow(0 0 2px rgba(255,255,255,.82)) drop-shadow(0 0 7px rgba(160,236,255,.76));
  }
  100%{
    filter:drop-shadow(0 0 5px #FFFFFF) drop-shadow(0 0 12px rgba(98,216,255,1));
  }
}
#${ROOT_ID} button.gv-target-proxy[aria-pressed="true"],
#${ROOT_ID} .gv-target-status.gv-active{
  animation:gv-5t-cosmic-pulse 3s cubic-bezier(.35,.02,.18,1) infinite!important;
  will-change:filter;
}
#${ROOT_ID} .gv-target-status.gv-active{
  pointer-events:auto!important;
  cursor:pointer!important;
}
@media (prefers-reduced-motion:reduce){
  #${ROOT_ID} button.gv-target-proxy[aria-pressed="true"],
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

    if(status.dataset.gv5tBound!=='true'){
      status.dataset.gv5tBound='true';
      status.setAttribute('aria-label','Deactivate Target mode');
      status.setAttribute('title','Tap to deactivate Target mode');
      status.addEventListener('click',event=>{
        event.preventDefault();
        event.stopPropagation();
        if(proxy.getAttribute('aria-pressed')==='true')proxy.click();
      });
    }
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
