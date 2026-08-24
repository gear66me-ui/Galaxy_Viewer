from IPython.display import HTML, Javascript, display

# Galaxy Viewer 12L analytics diagnostic clone.
# Frozen functional baseline remains viewer/archive/GV-beta-0012F.py.
# 12K behavior is preserved except Diagnostics 0003 is auto-armed and random preparation banners are suppressed.

display(HTML("""
<style>
html,body{background:#000}
#gv-12l-loader{position:fixed;inset:0;background:#000;z-index:1}
#gv-random-preparing-0043,#gv-random-preparing-12k,#gv-random-preparing-12l{display:none!important}
</style>
<div id="gv-12l-loader" aria-hidden="true"></div>
"""))

display(Javascript(r"""
(async()=>{
  'use strict';
  const RAW='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/';
  const SOURCE=RAW+'viewer/archive/GV-beta-0012F.py?v=12L-base';
  const audit=(type,detail={})=>{try{window.__GV_ANALYTICS_AUDIT__?.emit?.(type,detail)}catch(_){}};
  const read=async url=>{
    audit('12L_SOURCE_FETCH_START',{url});
    const started=performance.now();
    const response=await fetch(url,{cache:'no-store'});
    audit('12L_SOURCE_FETCH_END',{url,status:response.status,ok:response.ok,durationMs:Math.round(performance.now()-started)});
    if(!response.ok)throw new Error(`HTTP ${response.status} ${url}`);
    return response.text();
  };
  const extract=source=>{
    const html=[...source.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    const js=[...source.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];
    if(html.length!==1||js.length!==1)throw new Error('12L FROZEN 12F EXTRACTION FAILED');
    return [html[0][1],js[0][1]];
  };
  const once=(text,from,to,label)=>{
    const first=text.indexOf(from);
    if(first<0)throw new Error(`12L PATCH MISSING: ${label}`);
    if(text.indexOf(from,first+from.length)>=0)throw new Error(`12L PATCH NOT UNIQUE: ${label}`);
    return text.slice(0,first)+to+text.slice(first+from.length);
  };
  try{
    audit('12L_PATCH_START');
    const source=await read(SOURCE);
    let [html,js]=extract(source);
    html=html.replace("version.textContent='VERSION 12F'","version.textContent='VERSION 12L'");
    js=once(js,"const DISPLAY_VERSION='12F';","const DISPLAY_VERSION='12L';",'DISPLAY VERSION');
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
      "const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/random-galaxy/gv-random-galaxy-0040.js?v=0040';\n    const RANDOM_PATCH_0042_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/random-galaxy/gv-random-galaxy-0042.js?v=0042';\n    const RANDOM_PATCH_0043_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/random-galaxy/gv-random-galaxy-0043.js?v=0043';\n    const RANDOM_PATCH_0044_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/random-galaxy/gv-random-galaxy-0044.js?v=0044';\n    const RANDOM_PATCH_0045_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/random-galaxy/gv-random-galaxy-0045.js?v=0045';\n    const DIAGNOSTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/diagnostics/gv-diagnostics-0003.js?v=0003';\n    const DOWNLOAD_ANALYTICS_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0002.js?v=0002';\n    const DOWNLOAD_ANALYTICS_PATCH_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/download-analytics/gv-download-analytics-0003.js?v=0003';",
      'RANDOM / DIAGNOSTICS URLS');
    js=once(js,
`    const moduleLoads=Promise.all([
        loadScript(HAMBURGER_URL,'gvHamburger0002'),
        loadScript(COORDINATE_URL,'gvCoordinate0004'),
        loadScript(TARGET_URL,'gvTarget0001'),
        loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0034')
    ]);`,
`    const tracedLoad=(url,id)=>{const started=performance.now();audit('MODULE_LOAD_START',{id,url});return loadScript(url,id).then(value=>{audit('MODULE_LOAD_END',{id,url,durationMs:Math.round(performance.now()-started),ok:true});return value}).catch(error=>{audit('MODULE_LOAD_END',{id,url,durationMs:Math.round(performance.now()-started),ok:false,error:String(error?.stack||error)});throw error})};
    const moduleLoads=Promise.all([
        tracedLoad(HAMBURGER_URL,'gvHamburger0002').then(()=>tracedLoad(HAMBURGER_PATCH_URL,'gvHamburger0003')),
        tracedLoad(COORDINATE_URL,'gvCoordinate0004'),
        tracedLoad(TARGET_URL,'gvTarget0001'),
        tracedLoad(RANDOM_GALAXY_URL,'gvRandomGalaxy0040')
          .then(()=>tracedLoad(RANDOM_PATCH_0042_URL,'gvRandomGalaxy0042'))
          .then(()=>tracedLoad(RANDOM_PATCH_0043_URL,'gvRandomGalaxy0043'))
          .then(()=>tracedLoad(RANDOM_PATCH_0044_URL,'gvRandomGalaxy0044'))
          .then(()=>tracedLoad(RANDOM_PATCH_0045_URL,'gvRandomGalaxy0045')),
        tracedLoad(DIAGNOSTICS_URL,'gvDiagnostics0003'),
        tracedLoad(DOWNLOAD_ANALYTICS_URL,'gvDownloadAnalytics0002').then(()=>tracedLoad(DOWNLOAD_ANALYTICS_PATCH_URL,'gvDownloadAnalytics0003'))
    ]);`,
      'MODULE LOADS');
    js=once(js,`    if(
        window.GalaxyRandomGalaxy?.VERSION!=='0040' ||
        typeof window.GalaxyRandomGalaxy.bootstrapHomePresentation!=='function'
    )throw new Error('RANDOM GALAXY 0040 HOME BOOTSTRAP EXPORT MISSING');`,`    if(
        window.GalaxyRandomGalaxy?.VERSION!=='0045' ||
        typeof window.GalaxyRandomGalaxy.bootstrapHomePresentation!=='function'
    )throw new Error('RANDOM GALAXY 0045 HOME BOOTSTRAP EXPORT MISSING');`,'RANDOM HOME GATE');
    js=once(js,"window.GalaxyViewerHamburgerMenu?.version!=='0002'","window.GalaxyViewerHamburgerMenu?.version!=='0003'",'HAMBURGER GATE');
    js=once(js,"'HAMBURGER MODULE 0002 EXPORT MISSING'","'HAMBURGER MODULE 0003 EXPORT MISSING'",'HAMBURGER ERROR');
    js=once(js,"if(window.GalaxyRandomGalaxy?.VERSION!=='0040')throw new Error('RANDOM GALAXY 0040 EXPORT MISSING OR VERSION MISMATCH');","if(window.GalaxyRandomGalaxy?.VERSION!=='0045')throw new Error('RANDOM GALAXY 0045 EXPORT MISSING OR VERSION MISMATCH');",'RANDOM INSTANCE GATE');
    js=once(js,"if(typeof window.GalaxyRandomNavigationWindow!=='function')throw new Error('RANDOM GALAXY 0040 NAVIGATION WINDOW EXPORT MISSING');","if(typeof window.GalaxyRandomNavigationWindow!=='function')throw new Error('RANDOM GALAXY 0045 NAVIGATION WINDOW EXPORT MISSING');",'RANDOM NAV GATE');
    js=once(js,
`    const launchRandomGalaxy=()=>{
        if(navigationPending||randomGalaxy.getState().busy)return;

        reconcileFutureQueue();

        // Random Galaxy 0036 exclusively owns authoritative FIFO bundle
        // readiness. The viewer must not independently reinterpret HD /
        // Aladin readiness or create a second gate.
        const nextReady=Boolean(
            window.GalaxyRandomGalaxy?.hasReadyNavigation?.()
        );

        if(!nextReady){
            fillPrefetchQueue();
            return;
        }
`,
`    const waitForAuthoritativeRandomReady=async(timeoutMs=10000)=>{
        const started=performance.now();
        while(performance.now()-started<timeoutMs){
            try{window.GalaxyRandomGalaxy0045?.kick?.()}catch(_){}
            try{window.GalaxyRandomGalaxy?.reconcileFutureQueue?.()}catch(_){}
            try{fillPrefetchQueue()}catch(_){}
            if(window.GalaxyRandomGalaxy?.hasReadyNavigation?.())return true;
            await new Promise(resolve=>setTimeout(resolve,120));
        }
        return false;
    };
    const launchRandomGalaxy=async()=>{
        audit('RANDOM_CLICK',{busy:Boolean(randomGalaxy.getState().busy),navigationPending:Boolean(navigationPending)});
        if(navigationPending||randomGalaxy.getState().busy)return;
        const nextReady=await waitForAuthoritativeRandomReady();
        audit('RANDOM_READY_WAIT_END',{ready:Boolean(nextReady),health:window.GalaxyRandomGalaxy0045?.getHealth?.()||null});
        if(!nextReady){
            console.error('GALAXY VIEWER RANDOM GALAXY PREPARATION TIMEOUT',window.GalaxyRandomGalaxy0045?.getHealth?.());
            return;
        }
`,
      'RANDOM CLICK READINESS');

    audit('12L_PATCH_COMPLETE');
    document.getElementById('gv-12l-loader')?.remove();
    document.body.insertAdjacentHTML('beforeend',html);
    const script=document.createElement('script');script.textContent=js;document.body.appendChild(script);
    audit('12L_VIEWER_SCRIPT_MOUNTED');
  }catch(error){
    audit('12L_LOAD_FAILED',{error:String(error?.stack||error)});
    document.getElementById('gv-12l-loader')?.remove();
    const failure=document.createElement('pre');failure.style.cssText='position:fixed;inset:0;z-index:2147483647;margin:0;padding:20px;overflow:auto;background:#000;color:#9BE5FF;font:11px monospace';failure.textContent='GALAXY VIEWER 12L FAILED TO LOAD\n\n'+String(error?.stack||error);document.body.appendChild(failure);
    throw error;
  }
})();
"""))
