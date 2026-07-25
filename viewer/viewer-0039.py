from IPython.display import HTML, display

# viewer-0039 — Custom SIMBAD pointer isolated (inline) so external fetch isn\'t required

HTML_TEMPLATE = """
<link rel=\"stylesheet\" href=\"https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css\" />
<style>
#aladin-gv { width:100%; height:650px; position:relative; }
button.gv-simbad-proxy { appearance:none; width:34px; height:34px; }
.gv-simbad-live-status.gv-visible { display:block; }
</style>
<div id=\"aladin-gv\"></div>
<script src=\"https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js\" charset=\"utf-8\"></script>
<!-- inline custom SIMBAD pointer helper to avoid external fetch issues -->
<script>
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
    function activate(){ if(active) return; active=true; btn.classList.add('gv-active'); showBanner(); }
    function deactivate(){ if(!active) return; active=false; btn.classList.remove('gv-active'); hideBanner(); }
    btn.addEventListener('click', ev => { ev.preventDefault(); (active?deactivate:activate)(); });
    root.addEventListener('click', ev => {
      if(!active) return;
      const rect = root.getBoundingClientRect();
      const x = ev.clientX - rect.left;
      const y = ev.clientY - rect.top;
      const world = view.pix2world(x, y);
      if(!world) return;
      const ra = world[0];
      const dec = world[1];
      A.catalogFromSimbad({name:'SIMBAD',onClick:'showTable',color:'cyan'}, cat => {
        cat.addSources([A.marker(ra, dec)]);
      });
      deactivate();
    });
    return {activate, deactivate, isActive:()=>active};
  }
  global.initGVSimbadPointer = initGVSimbadPointer;
})(window);
</script>
<script>
A.init.then(()=>{
  const root = document.getElementById('aladin-gv');
  const aladin = A.aladin('#aladin-gv', {
      target:'M 31', survey:'P/DSS2/color', fov:1.5,
      showZoomControl:true, showFullscreenControl:true,
      showLayersControl:true, showSimbadPointerControl:false // hide native
  });
  const btn = document.createElement('button');
  btn.className = 'gv-simbad-proxy';
  btn.title = 'SIMBAD query';
  btn.textContent = '★';
  root.appendChild(btn);
  const banner = document.createElement('div');
  banner.className = 'gv-simbad-live-status';
  banner.textContent = 'SELECT A TARGET';
  root.appendChild(banner);
  initGVSimbadPointer({aladin:aladin, targetButton:btn, bannerElement:banner});
});
</script>
"""

display(HTML(HTML_TEMPLATE))
