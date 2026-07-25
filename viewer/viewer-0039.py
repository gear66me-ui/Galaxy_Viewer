from IPython.display import HTML, display

# viewer-0039 — Custom SIMBAD pointer isolated in external JS
# Requires gvSimbadPointer.js (added in viewer/js/)

RAW_BASE = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta"
JS_POINTER = f"{RAW_BASE}/viewer/js/gvSimbadPointer.js"

HTML_TEMPLATE = f"""
<link rel=\"stylesheet\" href=\"https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css\" />
<style>
/* keep same cosmic style as 38A (abbrev) */
#aladin-gv {{ width:100%; height:650px; position:relative; }}
button.gv-simbad-proxy {{ appearance:none; width:34px; height:34px; }}
.gv-simbad-live-status.gv-visible {{ display:block; }}
</style>
<div id=\"aladin-gv\"></div>
<script src=\"https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js\" charset=\"utf-8\"></script>
<script src=\"{JS_POINTER}\"></script>
<script>
A.init.then(()=>{{
  const root = document.getElementById('aladin-gv');
  const aladin = A.aladin('#aladin-gv', {{
      target:'M 31', survey:'P/DSS2/color', fov:1.5,
      showZoomControl:true, showFullscreenControl:true,
      showLayersControl:true, showSimbadPointerControl:false // hide native
  }});

  // Insert custom Target button next to coordinate box
  const btn = document.createElement('button');
  btn.className = 'gv-simbad-proxy';
  btn.title = 'SIMBAD query';
  btn.textContent = '★';
  root.appendChild(btn);

  // Optional banner for locked state
  const banner = document.createElement('div');
  banner.className = 'gv-simbad-live-status';
  banner.textContent = 'SELECT A TARGET';
  root.appendChild(banner);

  // Wire custom pointer (pan/zoom stay active)
  initGVSimbadPointer({{aladin:aladin, targetButton:btn, bannerElement:banner}});
}});
</script>
"""

display(HTML(HTML_TEMPLATE))
