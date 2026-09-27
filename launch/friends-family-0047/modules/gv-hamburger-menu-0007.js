/* Galaxy Viewer Hamburger extension 0007. Extends frozen 0005. Temporary DOE controls. */
(() => {
  'use strict';
  const VERSION='0007';
  const base=window.GalaxyViewerHamburgerMenu;
  if(!base||base.version!=='0005')throw new Error('HAMBURGER 0007 REQUIRES FROZEN 0005');
  const leftLabels=['PROJECTION','SAMPLE 20 HZ','SAMPLE 60 HZ','SAMPLE 120 HZ','SURVEY','RETICLE ON/OFF'];
  const DOE_RATES=[20,60,120];

  function ensureDoeStyle(){
    if(document.getElementById('gv-doe-menu-style'))return;
    const style=document.createElement('style');
    style.id='gv-doe-menu-style';
    style.textContent=`
      .gv-hamburger-module-root .gv-viewer-menu-row.gv-doe-selected .gv-viewer-menu-label,
      .gv-hamburger-module-root .gv-viewer-menu-row.gv-doe-selected .gv-viewer-menu-icon,
      .gv-hamburger-module-root .gv-viewer-menu-row.gv-doe-downloaded .gv-viewer-menu-icon{
        background:linear-gradient(145deg,#06371f 0%,#0b7a42 55%,#20c96b 100%)!important;
        border-color:#78ffab!important;
        color:#eafff1!important;
        box-shadow:inset 0 2px 2px rgba(225,255,235,.78),inset 0 -3px 5px rgba(0,0,0,.48),0 0 10px rgba(120,255,171,.68)!important
      }
      .gv-hamburger-module-root .gv-doe-download-glyph{position:relative;z-index:2;font:700 9px/1 "Space Age",sans-serif;letter-spacing:.2px}
    `;
    document.head.appendChild(style);
  }

  function init(options={}){
    ensureDoeStyle();
    const instance=base.init(options);
    const menu=instance.leftMenu;
    let rows=[...menu.querySelectorAll('.gv-viewer-menu-row')];
    const template=rows[2];
    const third=template.cloneNode(true);
    menu.insertBefore(third,rows[3]);
    rows=[...menu.querySelectorAll('.gv-viewer-menu-row')];

    const doeRows=[rows[1],rows[2],rows[3]];
    let selectedRate=20;

    function paint(){
      doeRows.forEach((row,i)=>{
        row.classList.toggle('gv-doe-selected',DOE_RATES[i]===selectedRate);
      });
    }

    doeRows.forEach((row,i)=>{
      const rate=DOE_RATES[i];
      row.style.pointerEvents='auto';
      row.dataset.gvMenuAction='DOE_'+rate;
      row.dataset.gvDoeRate=String(rate);
      const label=row.querySelector('.gv-viewer-menu-label');
      const glyph=label?.querySelector('.gv-space-age-glyph');
      if(glyph)glyph.textContent=`SAMPLE ${rate} HZ`; else if(label)label.textContent=`SAMPLE ${rate} HZ`;
      label?.setAttribute('aria-label',`SELECT ${rate} HZ SAMPLE RATE`);
      const icon=row.querySelector('.gv-viewer-menu-icon');
      if(icon){
        icon.setAttribute('aria-label',`DOWNLOAD ${rate} HZ REPORT`);
        icon.setAttribute('title',`DOWNLOAD ${rate} HZ REPORT`);
        icon.querySelectorAll('svg,.gv-space-age-glyph,.gv-doe-download-glyph').forEach(node=>node.remove());
        const dl=document.createElement('span');dl.className='gv-doe-download-glyph';dl.textContent='DL';icon.appendChild(dl);
      }
      label?.addEventListener('click',event=>{
        event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();
        selectedRate=rate;row.classList.remove('gv-doe-downloaded');paint();
        instance.root.dispatchEvent(new CustomEvent('gv-doe-rate-selected',{bubbles:true,detail:{rate}}));
      },true);
      icon?.addEventListener('click',event=>{
        event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();
        row.classList.add('gv-doe-downloaded');
        setTimeout(()=>row.classList.remove('gv-doe-downloaded'),1200);
        instance.root.dispatchEvent(new CustomEvent('gv-doe-download',{bubbles:true,detail:{rate}}));
      },true);
    });

    rows[4].dataset.gvMenuAction='SURVEY';
    const surveyGlyph=rows[4].querySelector('.gv-viewer-menu-label .gv-space-age-glyph');
    if(surveyGlyph)surveyGlyph.textContent='SURVEY';
    rows[5].dataset.gvMenuAction='RETICLE ON/OFF';
    const reticleGlyph=rows[5].querySelector('.gv-viewer-menu-label .gv-space-age-glyph');
    if(reticleGlyph)reticleGlyph.textContent='RETICLE ON/OFF';

    paint();
    instance.root.dataset.gvHamburgerMenuVersion=VERSION;
    instance.root.dataset.gvDoeRate=String(selectedRate);
    instance.root.addEventListener('gv-doe-rate-selected',e=>{instance.root.dataset.gvDoeRate=String(e.detail?.rate||selectedRate)});
    return instance;
  }

  window.GalaxyViewerHamburgerMenu=Object.freeze({...base,version:VERSION,init,labels:Object.freeze({left:Object.freeze([...leftLabels]),projections:base.labels?.projections||Object.freeze([])})});
})();