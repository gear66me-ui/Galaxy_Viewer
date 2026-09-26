/* Galaxy Viewer Hamburger extension 0007. Extends frozen 0006. ECO-20260902-12AR01-NAVIGATION-ADMIN-001C */
(() => {
  'use strict';
  const VERSION='0007';
  const base=window.GalaxyViewerHamburgerMenu;
  if(!base||base.version!=='0005')throw new Error('HAMBURGER 0007 REQUIRES FROZEN 0005');
  const leftLabels=['PROJECTION','SURVEY','RETICLE ON/OFF'];
  function init(options={}){
    const instance=base.init(options);
    const rows=[...instance.leftMenu.querySelectorAll('.gv-viewer-menu-row')];
    rows[2]?.remove();
    rows[1]?.remove();
    instance.root.dataset.gvHamburgerMenuVersion=VERSION;
    return instance;
  }
  window.GalaxyViewerHamburgerMenu=Object.freeze({...base,version:VERSION,init,labels:Object.freeze({left:Object.freeze([...leftLabels]),projections:base.labels?.projections||Object.freeze([])})});
})();
