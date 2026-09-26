from IPython.display import HTML, Javascript, display

# Galaxy Viewer 12H repair loader.
# Frozen source baseline remains viewer/archive/GV-beta-0012F.py.
# This revision fixes 12G gate matching, rewires organized modules, and adds opt-in diagnostics surfaces.

display(HTML("""
<style>html,body{background:#000}#gv-12h-loader{position:fixed;inset:0;background:#000;z-index:1}</style>
<div id="gv-12h-loader" aria-hidden="true"></div>
"""))

display(Javascript(r"""
(async()=>{
  'use strict';
  const RAW='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
  const SOURCE=RAW+'viewer/archive/GV-beta-0012F.py?v=12H-base';
  const read=async url=>{const response=await fetch(url,{cache:'no-store'});if(!response.ok)throw new Error(`HTTP ${response.status} ${url}`);return response.text()};
  const extract=source=>{
    const html=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    const js=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(html.length!==1||js.length!==1)throw new Error('12H FROZEN 12F EXTRACTION FAILED');
    return [html[0][1],js[0][1]];
  };
  const once=(text,from,to,label)=>{
    const first=text.indexOf(from);
    if(first<0)throw new Error(`12H PATCH MISSING: ${label}`);
    if(text.indexOf(from,first+from.length)>=0)throw new Error(`12H PATCH NOT UNIQUE: ${label}`);
    return text.slice(0,first)+to+text.slice(first+from.length);
  };
  try{
    const source=await read(SOURCE);
    let [html,js]=extract(source);
    html=html.replace("version.textContent='VERSION 12F'","version.textContent='VERSION 12H'");
    js=once(js,"const DISPLAY_VERSION='12F';","const DISPLAY_VERSION='12H';",'DISPLAY VERSION');
    js=once(js,
      "const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-hamburger-menu-0002.js?v=9ed18798f4c7010b76782d0ff2bf0c8ec5eb4cba';",
      "const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0002.js?v=9ed18798f4c7010b76782d0ff2bf0c8ec5eb4cba';\n    const HAMBURGER_PATCH_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/hamburger-menu/gv-hamburger-menu-0003.js?v=0003';",
      'HAMBURGER URL');
    js=once(js,
      "const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0004.js?v=4c9a595860ed69d800d4c1a038c4e0402c69bba0';",
      "const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/coordinate-overlay/gv-coordinate-overlay-0004.js?v=4c9a595860ed69d800d4c1a038c4e0402c69bba0';",
      'COORDINATE URL');
    js=once(js,
      "const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-target-simbad-0001.js?v=9f50e6c8e199b64b82ee49267250157c35997662';",
      "const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/target-simbad/gv-target-simbad-0001.js?v=9f50e6c8e199b64b82ee49267250157c35997662';",
      'TARGET URL');
    js=once(js,
      "const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/gv-random-galaxy-0040.js?v=0040';",
      "const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/random-galaxy/gv-random-galaxy-0040.js?v=0040';\n    const RANDOM_PATCH_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/random-galaxy/gv-random-galaxy-0042.js?v=0042';\n    const DIAGNOSTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0001.js?v=0001';\n    const DOWNLOAD_ANALYTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0001.js?v=0001';",
      'RANDOM / DIAGNOSTICS URLS');
    js=once(js,
`    const moduleLoads=Promise.all([
        loadScript(HAMBURGER_URL,'gvHamburger0002'),
        loadScript(COORDINATE_URL,'gvCoordinate0004'),
        loadScript(TARGET_URL,'gvTarget0001'),
        loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0034')
    ]);`,
`    const moduleLoads=Promise.all([
        loadScript(HAMBURGER_URL,'gvHamburger0002').then(()=>loadScript(HAMBURGER_PATCH_URL,'gvHamburger0003')),
        loadScript(COORDINATE_URL,'gvCoordinate0004'),
        loadScript(TARGET_URL,'gvTarget0001'),
        loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0040').then(()=>loadScript(RANDOM_PATCH_URL,'gvRandomGalaxy0042')),
        loadScript(DIAGNOSTICS_URL,'gvDiagnostics0001'),
        loadScript(DOWNLOAD_ANALYTICS_URL,'gvDownloadAnalytics0001')
    ]);`,
      'MODULE LOADS');
    js=once(js,`    if(
        window.GalaxyRandomGalaxy?.VERSION!=='0040' ||
        typeof window.GalaxyRandomGalaxy.bootstrapHomePresentation!=='function'
    )throw new Error('RANDOM GALAXY 0040 HOME BOOTSTRAP EXPORT MISSING');`,`    if(
        window.GalaxyRandomGalaxy?.VERSION!=='0042' ||
        typeof window.GalaxyRandomGalaxy.bootstrapHomePresentation!=='function'
    )throw new Error('RANDOM GALAXY 0042 HOME BOOTSTRAP EXPORT MISSING');`,'RANDOM HOME GATE');
    js=once(js,"window.GalaxyViewerHamburgerMenu?.version!=='0002'","window.GalaxyViewerHamburgerMenu?.version!=='0003'",'HAMBURGER GATE');
    js=once(js,"'HAMBURGER MODULE 0002 EXPORT MISSING'","'HAMBURGER MODULE 0003 EXPORT MISSING'",'HAMBURGER ERROR');
    js=once(js,"if(window.GalaxyRandomGalaxy?.VERSION!=='0040')throw new Error('RANDOM GALAXY 0040 EXPORT MISSING OR VERSION MISMATCH');","if(window.GalaxyRandomGalaxy?.VERSION!=='0042')throw new Error('RANDOM GALAXY 0042 EXPORT MISSING OR VERSION MISMATCH');",'RANDOM INSTANCE GATE');
    js=once(js,"if(typeof window.GalaxyRandomNavigationWindow!=='function')throw new Error('RANDOM GALAXY 0040 NAVIGATION WINDOW EXPORT MISSING');","if(typeof window.GalaxyRandomNavigationWindow!=='function')throw new Error('RANDOM GALAXY 0042 NAVIGATION WINDOW EXPORT MISSING');",'RANDOM NAV GATE');
    document.getElementById('gv-12h-loader')?.remove();
    document.body.insertAdjacentHTML('beforeend',html);
    const script=document.createElement('script');script.textContent=js;document.body.appendChild(script);
  }catch(error){
    document.getElementById('gv-12h-loader')?.remove();
    const failure=document.createElement('pre');failure.style.cssText='position:fixed;inset:0;z-index:2147483647;margin:0;padding:20px;overflow:auto;background:#000;color:#FFD84D;font:13px monospace';failure.textContent='GALAXY VIEWER 12H FAILED TO LOAD\n\n'+String(error?.stack||error);document.body.appendChild(failure);
    throw error;
  }
})();
"""))
