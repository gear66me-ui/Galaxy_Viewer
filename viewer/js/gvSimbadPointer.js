// gvSimbadPointer.js  (Galaxy Viewer custom SIMBAD selector)
// Lightweight replacement for AladinLite's simbadPointerControl so we can
// keep normal pan/zoom enabled while selecting an object.
//
// Usage:
//   initGVSimbadPointer({
//       aladin,           // Aladin instance
//       targetButton,     // HTMLButtonElement that toggles pointer on/off
//       bannerElement     // Optional element shown while pointer is active
//   });

(function(global){
  function initGVSimbadPointer(opts){
    if(!opts||!opts.aladin||!opts.targetButton) return;
    const aladin = opts.aladin;
    const view   = aladin.view || aladin;
    const root   = aladin.getParentDiv ? aladin.getParentDiv() : document;
    const btn    = opts.targetButton;
    const banner = opts.bannerElement || null;

    let active = false;

    function showBanner(){ if(banner){ banner.classList.add('gv-visible'); } }
    function hideBanner(){ if(banner){ banner.classList.remove('gv-visible'); } }

    function activate(){
      if(active) return;
      active = true;
      btn.classList.add('gv-active');
      showBanner();
    }
    function deactivate(){
      if(!active) return;
      active = false;
      btn.classList.remove('gv-active');
      hideBanner();
    }

    btn.addEventListener('click', ev => {
      ev.preventDefault();
      (active ? deactivate : activate)();
    });

    root.addEventListener('click', ev => {
      if(!active) return;
      // Convert pixel → world coordinates (returns [ra, dec] in deg)
      const rect = root.getBoundingClientRect();
      const x = ev.clientX - rect.left;
      const y = ev.clientY - rect.top;
      const world = view.pix2world(x, y);
      if(!world) return;
      const ra  = world[0];
      const dec = world[1];
      // Query SIMBAD via AladinLite helper (catalogFromSimbad) and show marker
      A.catalogFromSimbad({name:'SIMBAD',onClick:'showTable',color:'cyan'}, (cat)=>{
        cat.addSources([A.marker(ra, dec)]);
      });
      // Finish
      deactivate();
    });

    // Export controls (optional)
    return {activate,deactivate,isActive:()=>active};
  }
  global.initGVSimbadPointer = initGVSimbadPointer;
})(window);