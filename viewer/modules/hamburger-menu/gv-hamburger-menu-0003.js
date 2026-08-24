/* Galaxy Viewer Hamburger extension 0003. Extends frozen 0002. */
(() => {
  'use strict';
  const VERSION='0003';
  const base=window.GalaxyViewerHamburgerMenu;
  if(!base||base.version!=='0002')throw new Error('HAMBURGER 0003 REQUIRES FROZEN 0002');
  const leftLabels=['PROJECTION','DIAGNOSTICS','DOWNLOAD ANALYTICS','SURVEY','RETICLE ON/OFF'];
  function relabelRow(row,name){
    if(!row)return;
    row.dataset.gvMenuAction=name;
    const label=row.querySelector('.gv-viewer-menu-label');
    const glyph=label?.querySelector('.gv-space-age-glyph');
    if(glyph)glyph.textContent=name;else if(label)label.textContent=name;
    label?.setAttribute('aria-label',name);
    const icon=row.querySelector('.gv-viewer-menu-icon');
    icon?.setAttribute('aria-label',name);icon?.setAttribute('title',name);
  }
  function init(options={}){
    const originalAction=options.onMenuAction;
    let instance=null;
    const wrapped={...options,onMenuAction(action,context){
      if(action==='DIAGNOSTICS'){
        window.GalaxyViewerDiagnostics?.open?.();
        setTimeout(()=>instance?.close?.(),0);
        return;
      }
      if(action==='DOWNLOAD ANALYTICS'){
        window.GalaxyViewerDownloadAnalytics?.open?.();
        setTimeout(()=>instance?.close?.(),0);
        return;
      }
      originalAction?.(action,context);
    }};
    instance=base.init(wrapped);
    const rows=[...instance.leftMenu.querySelectorAll('.gv-viewer-menu-row')];
    relabelRow(rows[1],'DIAGNOSTICS');
    relabelRow(rows[2],'DOWNLOAD ANALYTICS');
    instance.root.dataset.gvHamburgerMenuVersion=VERSION;
    return instance;
  }
  window.GalaxyViewerHamburgerMenu=Object.freeze({...base,version:VERSION,init,labels:Object.freeze({left:Object.freeze([...leftLabels]),projections:base.labels?.projections||Object.freeze([])})});
})();
