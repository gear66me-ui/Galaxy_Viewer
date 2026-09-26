from IPython.display import HTML, Javascript, display

# Galaxy Viewer 12J layering-only repair loader.
# Frozen baseline: viewer/GV-beta-0012I.py.
# Only functional change: Download Analytics 0003 sits above Diagnostics.

display(HTML("""
<style>html,body{background:#000}#gv-12j-loader{position:fixed;inset:0;background:#000;z-index:1}</style>
<div id="gv-12j-loader" aria-hidden="true"></div>
"""))

display(Javascript(r"""
(async()=>{
  'use strict';
  const RAW='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
  const SOURCE=RAW+'viewer/GV-beta-0012I.py?v=12J-base';
  const read=async url=>{const response=await fetch(url,{cache:'no-store'});if(!response.ok)throw new Error(`HTTP ${response.status} ${url}`);return response.text()};
  const extract=source=>{
    const html=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    const js=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(html.length!==1||js.length!==1)throw new Error('12J FROZEN 12I EXTRACTION FAILED');
    return [html[0][1],js[0][1]];
  };
  const once=(text,from,to,label)=>{
    const first=text.indexOf(from);
    if(first<0)throw new Error(`12J PATCH MISSING: ${label}`);
    if(text.indexOf(from,first+from.length)>=0)throw new Error(`12J PATCH NOT UNIQUE: ${label}`);
    return text.slice(0,first)+to+text.slice(first+from.length);
  };
  try{
    let source=await read(SOURCE);
    source=source.replaceAll('12I','12J').replaceAll('12i','12j');
    let [html,js]=extract(source);
    js=once(js,
      "const DOWNLOAD_ANALYTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0002.js?v=0002';",
      "const DOWNLOAD_ANALYTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0002.js?v=0002';\n    const DOWNLOAD_ANALYTICS_PATCH_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0003.js?v=0003';",
      'DOWNLOAD ANALYTICS URL');
    js=once(js,
      "loadScript(DOWNLOAD_ANALYTICS_URL,'gvDownloadAnalytics0002')",
      "loadScript(DOWNLOAD_ANALYTICS_URL,'gvDownloadAnalytics0002').then(()=>loadScript(DOWNLOAD_ANALYTICS_PATCH_URL,'gvDownloadAnalytics0003'))",
      'DOWNLOAD ANALYTICS LOAD');
    document.getElementById('gv-12j-loader')?.remove();
    document.body.insertAdjacentHTML('beforeend',html);
    const script=document.createElement('script');script.textContent=js;document.body.appendChild(script);
  }catch(error){
    document.getElementById('gv-12j-loader')?.remove();
    const failure=document.createElement('pre');failure.style.cssText='position:fixed;inset:0;z-index:2147483647;margin:0;padding:20px;overflow:auto;background:#000;color:#9BE5FF;font:11px monospace';failure.textContent='GALAXY VIEWER 12J FAILED TO LOAD\n\n'+String(error?.stack||error);document.body.appendChild(failure);
    throw error;
  }
})();
"""))
