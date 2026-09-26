/* Galaxy Viewer Download Analytics 0003 — layering-only repair over frozen 0002. */
(() => {
  'use strict';
  const VERSION='0003';
  const base=window.GalaxyViewerDownloadAnalytics;
  if(!base||base.VERSION!=='0002')throw new Error('DOWNLOAD ANALYTICS 0003 REQUIRES FROZEN 0002');

  const STYLE_ID='gv-download-analytics-0003-layer-style';
  function ensureLayer(){
    if(document.getElementById(STYLE_ID))return;
    const style=document.createElement('style');
    style.id=STYLE_ID;
    style.textContent='#gv-download-analytics-0002{z-index:2147482001!important}';
    document.head.appendChild(style);
  }

  const open=()=>{ensureLayer();return base.open?.()};
  ensureLayer();

  window.GalaxyViewerDownloadAnalytics=Object.freeze({
    ...base,
    VERSION,
    open
  });
})();