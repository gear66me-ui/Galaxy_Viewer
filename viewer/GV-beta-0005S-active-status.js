/* Galaxy Viewer 5S — active Target status control only.
   Keeps the Target and status boxes visually independent.
   Adds matching active neon glow and allows the active status box to deactivate Target mode. */
(() => {
  const ROOT_ID='aladin-cosmic-command-test';

  function install(){
    const root=document.getElementById(ROOT_ID);
    if(!root)return false;

    if(!document.getElementById('gv-5s-active-status-style')){
      const style=document.createElement('style');
      style.id='gv-5s-active-status-style';
      style.textContent=`
#${ROOT_ID} .gv-target-status.gv-active{
  pointer-events:auto!important;
  cursor:pointer!important;
  box-shadow:0 0 5px #FFFFFF,0 0 13px 4px rgba(98,216,255,.82)!important;
}
`;
      document.head.appendChild(style);
    }

    const proxy=root.querySelector('button.gv-target-proxy');
    const status=root.querySelector('.gv-target-status');
    if(!proxy||!status)return false;

    if(status.dataset.gv5sBound!=='true'){
      status.dataset.gv5sBound='true';
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
