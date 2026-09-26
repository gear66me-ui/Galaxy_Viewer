/* Galaxy Viewer Hamburger extension 0007. Extends frozen 0006. ECO-20260902-12AR01-NAVIGATION-ADMIN-001C */
(() => {
  'use strict';
  const VERSION='0007';
  const base=window.GalaxyViewerHamburgerMenu;
  if(!base||base.version!=='0005')throw new Error('HAMBURGER 0007 REQUIRES FROZEN 0005');
  const leftLabels=['PROJECTION','','','SURVEY','RETICLE ON/OFF'];
  function init(options={}){
    const instance=base.init(options);
    const rows=[...instance.leftMenu.querySelectorAll('.gv-viewer-menu-row')];
    for(const index of [1,2]){
      const row=rows[index];
      if(!row)continue;
      row.dataset.gvMenuAction='';
      const label=row.querySelector('.gv-viewer-menu-label');
      const glyph=label?.querySelector('.gv-space-age-glyph');
      if(glyph)glyph.textContent='';else if(label)label.textContent='';
      label?.removeAttribute('aria-label');
      const icon=row.querySelector('.gv-viewer-menu-icon');
      icon?.removeAttribute('aria-label');icon?.removeAttribute('title');
      row.style.pointerEvents='none';
    }
    instance.root.dataset.gvHamburgerMenuVersion=VERSION;
    return instance;
  }
  window.GalaxyViewerHamburgerMenu=Object.freeze({...base,version:VERSION,init,labels:Object.freeze({left:Object.freeze([...leftLabels]),projections:base.labels?.projections||Object.freeze([])})});
})();
