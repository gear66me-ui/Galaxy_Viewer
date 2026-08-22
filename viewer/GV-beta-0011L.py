from IPython.display import HTML, Javascript, display

# Galaxy Viewer active implementation
# Standalone Galaxy Viewer implementation.
# 10V authorized changes only: preserve 10U behavior while repairing the HD control row
# (matched BACK TO SKY / DOWNLOAD IMAGE geometry plus a measured no-write zone) and
# expose the already-rendered Earth/Milky Way shell immediately after splash while catalogs,
# modules and HD prefetch finish outside the first-viewer-frame critical path.

display(HTML("""
<link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css" />
<style>
@font-face{
    font-family:"Space Age";
    src:url("https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001") format("opentype");
    font-style:normal;font-weight:400;font-display:block
}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#aladin-cosmic-command-test{position:relative!important;width:100%!important;height:100vh!important;height:100svh!important;height:100dvh!important;min-height:100vh!important;min-height:100svh!important;min-height:100dvh!important;overflow:hidden!important;background:#000!important}
#gv-startup-wait{position:absolute;inset:0;z-index:7085;display:flex;align-items:center;justify-content:center;background:#000;pointer-events:none}
#aladin-cosmic-command-test .aladin-logo,
#aladin-cosmic-command-test .aladin-copyright,
#aladin-cosmic-command-test .aladin-fov,
#aladin-cosmic-command-test .aladin-status-bar{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important}
#aladin-cosmic-command-test [class*="simbadPointer"]{position:absolute!important;left:-10000px!important;top:-10000px!important;width:1px!important;height:1px!important;min-width:1px!important;min-height:1px!important;max-width:1px!important;max-height:1px!important;margin:0!important;padding:0!important;opacity:0!important;visibility:hidden!important;pointer-events:none!important;overflow:hidden!important}
#gv-hamburger-host{position:absolute;inset:0;z-index:7200;pointer-events:none}
#gv-hamburger-host>.gv-hamburger-module-root{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;min-height:0!important;pointer-events:none!important}
#gv-hamburger-host .gv-menu-proxy{pointer-events:auto!important}
#gv-hamburger-host .gv-viewer-menu.gv-open,#gv-hamburger-host .gv-projection-submenu.gv-open{pointer-events:auto!important}
#gv-coordinate-host{position:absolute;left:50px;top:12px;z-index:7210;width:290px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}
#gv-target-host{position:absolute;left:342px;top:12px;z-index:7210;width:36px;height:36px;margin:0;padding:0;overflow:visible;pointer-events:auto}
#gv-coordinate-north-pulse{position:absolute;left:50px;top:12px;z-index:7211;width:290px;height:36px;border-radius:6px;pointer-events:none;overflow:visible}
#gv-coordinate-north-pulse::before{content:"";position:absolute;left:var(--gv-north-pulse-x,50%);top:var(--gv-north-pulse-y,0%);width:34px;height:3px;transform:translate(-50%,-50%) rotate(var(--gv-north-pulse-angle,0deg));transform-origin:50% 50%;border-radius:999px;background:#78FFAB;box-shadow:0 0 4px #78FFAB,0 0 9px rgba(87,255,147,.72),0 0 15px rgba(87,255,147,.34);opacity:.28;animation:gvCoordinateNorthPulse 1.8s ease-in-out infinite}
@keyframes gvCoordinateNorthPulse{0%,100%{opacity:.18;filter:brightness(.82)}50%{opacity:.72;filter:brightness(1.28)}}
#gv-nav-instrument-toggles{position:absolute;left:50px;top:52px;z-index:7210;display:flex;gap:5px;height:28px;pointer-events:auto}
.gv-nav-instrument-toggle{appearance:none;-webkit-appearance:none;width:28px;height:28px;margin:0;padding:0;border:1px solid rgba(183,255,208,.72);border-radius:5px;background:rgba(0,16,10,.72);color:#78FFAB;font:400 10px/1 "Space Age",sans-serif;letter-spacing:.2px;box-shadow:0 0 6px rgba(87,255,147,.20);cursor:pointer;touch-action:manipulation}
.gv-nav-instrument-toggle[aria-pressed="false"]{opacity:.42;box-shadow:none}
#gv-nav-instruments{position:absolute;inset:0;z-index:7060;pointer-events:none;overflow:hidden}
.gv-nav-marker{position:absolute;left:50%;top:50%;width:0;height:0;display:none;pointer-events:none}
.gv-nav-marker.gv-visible{display:block}
.gv-nav-marker-pointer{position:absolute;left:-9px;top:-15px;width:18px;height:15px;border:0;transform-origin:9px 15px;filter:drop-shadow(0 0 4px currentColor)}
.gv-nav-marker-pointer::before,.gv-nav-marker-pointer::after{content:"";position:absolute;top:0;width:2px;height:18px;background:currentColor;border-radius:2px;transform-origin:50% 0}
.gv-nav-marker-pointer::before{left:1px;transform:rotate(-30deg)}
.gv-nav-marker-pointer::after{right:1px;transform:rotate(30deg)}
.gv-nav-marker-label{position:absolute;left:50%;top:14px;transform:translateX(-50%);text-align:center;white-space:nowrap;text-transform:uppercase;font-family:"Space Age",sans-serif;font-weight:400;line-height:1.05;text-shadow:0 0 5px currentColor}
#gv-earth-marker{color:#FFD85A}
#gv-earth-marker .gv-nav-marker-label{font-size:12px}
#gv-earth-distance{display:block;margin-top:2px;font-size:11px;letter-spacing:.25px}
#gv-north-marker{color:#78FFAB}
#gv-north-marker .gv-nav-marker-label{font-size:12px}
#gv-north-marker::before,#gv-north-marker::after{content:"";position:absolute;left:-12px;top:2px;width:24px;height:8px;border-top:1px solid currentColor;border-radius:50%;opacity:.35}
#gv-north-marker::after{transform:rotate(90deg)}
#gv-random-galaxy-host{position:absolute;inset:0;z-index:7300;pointer-events:none}
#gv-center-reticle{position:absolute;left:50%;top:50%;z-index:7050;width:32px;height:32px;transform:translate(-50%,-50%);pointer-events:none;user-select:none;-webkit-user-select:none}
#gv-center-reticle img{display:block;width:32px;height:32px}
#gv-galaxy-nav{position:absolute;left:50%;bottom:12px;z-index:7100;display:flex;align-items:center;justify-content:center;gap:5px;width:calc(100vw - 24px);height:36px;transform:translateX(-50%);pointer-events:auto}
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:static;display:flex;flex:1 1 auto;min-width:0;align-items:center;justify-content:center;height:36px;margin:0;padding:0 12px;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:#E8FFF0;font:400 15.5px/1 "Space Age",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 4px rgba(229,255,239,.76);box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
#gv-random-galaxy:active{filter:brightness(1.08)}
.gv-galaxy-history{appearance:none;-webkit-appearance:none;position:relative;display:flex;flex:0 0 36px;align-items:center;justify-content:center;width:36px;height:36px;margin:0;padding:0;border:1px solid #B7FFD0;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94));color:transparent;box-shadow:inset 0 0 7px rgba(167,255,203,.28),0 0 8px rgba(77,255,143,.34);cursor:pointer;touch-action:manipulation;outline:none;overflow:hidden;pointer-events:auto}
.gv-galaxy-history::before,.gv-galaxy-history::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;pointer-events:none;box-sizing:border-box}
.gv-galaxy-history::before{border-width:6px;border-color:#78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.90));transform:translate(-62%,-50%) rotate(45deg)}
.gv-galaxy-history::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-66%,-50%) rotate(45deg)}
.gv-galaxy-history-back::before{transform:translate(-38%,-50%) rotate(-135deg)}
.gv-galaxy-history-back::after{transform:translate(-34%,-50%) rotate(-135deg)}
.gv-galaxy-history:disabled{opacity:.62;cursor:default;box-shadow:inset 0 0 7px rgba(167,255,203,.18),0 0 6px rgba(77,255,143,.24)}
#gv-travel-hud{position:absolute;left:50%;top:auto;bottom:64px;z-index:7350;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:4px;width:min(214px,68vw);padding:0;border:0;background:transparent;box-shadow:none;text-align:center;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-travel-hud.gv-visible{opacity:1;visibility:visible}
#gv-travel-primary{box-sizing:border-box;width:calc(100vw - 24px);padding:4px 7px 5px;border:1px solid rgba(131,255,176,.76);border-radius:6px;background:rgba(0,16,10,.72);box-shadow:0 0 8px rgba(65,255,133,.14);text-align:center}
#gv-travel-course,#gv-travel-heading{font:400 13px/1.05 "Space Age",sans-serif;letter-spacing:.55px;color:#E1FFEC;text-align:center;text-shadow:0 0 4px rgba(87,255,147,.20)}
#gv-travel-course{font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#78FFAB;text-shadow:0 0 7px rgba(87,255,147,.58)}
#gv-travel-heading{margin-top:1px;color:#AEEFC5}
#gv-travel-destination{margin-top:2px;font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#78FFAB;text-shadow:0 0 7px rgba(87,255,147,.58);text-align:center;white-space:normal;overflow-wrap:anywhere}
#gv-travel-distance{box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;width:172px;height:34px;padding:2px 6px 1px;border:1px solid rgba(131,255,176,.78);border-radius:5px;background:rgba(0,12,8,.76);color:#FFD85A;text-align:center;text-shadow:0 0 4px rgba(255,242,168,.82),0 0 9px rgba(255,180,45,.34);white-space:nowrap}
#gv-travel-distance-value{position:relative;display:block;width:100%;height:18px;font:400 17px/18px "Space Age",sans-serif;letter-spacing:.32px;text-align:center;font-variant-numeric:tabular-nums}
#gv-travel-distance-integer{position:absolute;right:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:right;white-space:nowrap}
#gv-travel-distance-decimal{position:absolute;left:50%;top:0;width:6px;height:18px;transform:translateX(-50%);font:inherit;letter-spacing:0;text-align:center;white-space:nowrap}
#gv-travel-distance-fraction{position:absolute;left:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:left;white-space:nowrap}
#gv-travel-distance-unit{display:block;width:100%;height:12px;font:400 10.5px/12px "Space Age",sans-serif;letter-spacing:.45px;text-align:center;white-space:nowrap}
#gv-version-label{position:absolute;left:50%;bottom:51px;z-index:7400;transform:translateX(-50%);height:10px;color:rgba(183,255,208,.86);font:400 8px/10px "Space Age",sans-serif;letter-spacing:.85px;text-align:center;text-transform:uppercase;text-shadow:0 0 5px rgba(87,255,147,.40);white-space:nowrap;pointer-events:none}
#gv-universe-context{position:absolute;left:50%;top:auto;bottom:calc(50% + min(25vw,50dvh) + 8px);z-index:7095;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;width:min(310px,76vw);pointer-events:none;transition:opacity .2s ease}
#gv-universe-context .gv-universe-label{padding:5px 8px 6px;border:1px solid rgba(120,255,171,.78);border-radius:6px;background:rgba(0,12,8,.68);box-shadow:0 0 9px rgba(87,255,147,.18);color:#DFFFEA;text-align:center;text-transform:uppercase;text-shadow:0 0 6px rgba(87,255,147,.42);font:400 9px/1.25 "Space Age",sans-serif;letter-spacing:.65px}
#gv-universe-context .gv-universe-count{display:block;margin-top:2px;color:#78FFAB;font-size:10px;letter-spacing:.8px}
#gv-universe-context .gv-universe-leader{position:relative;width:1px;height:18px;background:rgba(120,255,171,.86);box-shadow:0 0 7px rgba(87,255,147,.48)}
#gv-universe-context .gv-universe-leader::after{content:"";position:absolute;left:50%;bottom:-1px;width:0;height:0;transform:translateX(-50%);border-left:5px solid transparent;border-right:5px solid transparent;border-top:8px solid #78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.68))}
#gv-universe-context.gv-hidden{opacity:0;visibility:hidden}
#gv-we-are-here{position:absolute;inset:0;z-index:7090;pointer-events:none;transition:opacity .2s ease}
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 16px);bottom:34%;width:1px;min-height:36px;transform:translateX(-50%);background:rgba(120,255,171,.88);box-shadow:0 0 8px rgba(87,255,147,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.75))}
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:66%;transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(120,255,171,.88);border-radius:6px;background:rgba(0,12,8,.74);color:#E8FFF0;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(87,255,147,.58);box-shadow:0 0 10px rgba(87,255,147,.24)}
#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:8px;color:#78FFAB;font:400 15px/1.2 "Space Age",sans-serif;letter-spacing:1.25px}
#gv-we-are-here .gv-earth-icon{display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:drop-shadow(0 0 5px rgba(87,255,147,.55))}
#gv-we-are-here .gv-home-sub{margin-top:4px;color:#CFFFE0;font:400 10px/1.3 "Space Age",sans-serif;letter-spacing:1px}
#gv-we-are-here .gv-home-hint{margin-top:5px;color:#A7DDBA;font:400 9px/1.3 "Space Age",sans-serif;letter-spacing:.8px}
#gv-we-are-here.gv-hidden{opacity:0;visibility:hidden}
#gv-apk-cover{flex-direction:column;gap:18px}#gv-apk-cover .gv-viewer-version{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}
</style>
<div id="aladin-cosmic-command-test"><div id="gv-startup-wait" aria-hidden="true"></div></div>
<script>(()=>{const cover=document.getElementById('gv-apk-cover');if(!cover)return;const img=cover.querySelector('img');if(img)img.src='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/icon_target_vector.svg';const version=document.createElement('div');version.className='gv-viewer-version';version.textContent='VERSION 10AE2';cover.appendChild(version)})();</script>
"""))

display(Javascript(r"""
(async()=>{
    'use strict';
    const VERSION='10AE2';
    const DISPLAY_VERSION='10AE2';
    const ALADIN_URL='https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js';
    const HAMBURGER_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-hamburger-menu-0002.js?v=28d4acb0b724e2c9ec9764f4f3ce92ee1e3210a5';
    const COORDINATE_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-coordinate-overlay-0004.js?v=5c323a13b92f146426b45c047fc716b599494f3a';
    const TARGET_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/modules/gv-target-simbad-0001.js?v=7b877f841f091f214d844bdc8ae2f933530f4592';
    const RANDOM_GALAXY_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/559dfd10c0c3dafa7f7a5c3f7fe2c76337f26066/viewer/modules/gv-random-galaxy-0031.js?v=4abd2d76e717c0f4abbb61777154b7db14f49cf8';
    const HUBBLE_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0018.json';
    const JWST_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/948867116a8f35e5265c4cecf887c60c1df0cd77/viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0002.json?v=bcc37a66bc5bb697b57530d07daee5886c63338a';
    const CHANDRA_CATALOG_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0001.json';
    const RETICLE_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/5274c366f42bb1e764c4b2c4827df0bbba41b4cd/viewer/artwork/GV-reticle-0001.svg?v=fd0f8aa1d5d1f5746e373577c06ae6c81d1f9cc0';
    const TARGET_ICON_URL='data:image/svg+xml;charset=UTF-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%20role%3D%22img%22%20aria-label%3D%22Galaxy%20Viewer%20target%20icon%22%3E%0A%20%20%3Cdefs%3E%0A%20%20%20%20%3ClinearGradient%20id%3D%22ring%22%20x1%3D%224.5%22%20y1%3D%2210%22%20x2%3D%2227.5%22%20y2%3D%2222%22%20gradientUnits%3D%22userSpaceOnUse%22%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%220%22%20stop-color%3D%22%2345E7FF%22%2F%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%220.52%22%20stop-color%3D%22%234F9DFF%22%2F%3E%0A%20%20%20%20%20%20%3Cstop%20offset%3D%221%22%20stop-color%3D%22%237575FF%22%2F%3E%0A%20%20%20%20%3C%2FlinearGradient%3E%0A%20%20%3C%2Fdefs%3E%0A%20%20%3Ccircle%20cx%3D%2216%22%20cy%3D%2216%22%20r%3D%229.5%22%20fill%3D%22%23000000%22%20stroke%3D%22%23FF6B2D%22%20stroke-width%3D%221.8%22%2F%3E%0A%20%20%3Cellipse%20cx%3D%2216%22%20cy%3D%2216%22%20rx%3D%2211.5%22%20ry%3D%224.2%22%20fill%3D%22none%22%20stroke%3D%22url%28%23ring%29%22%20stroke-width%3D%222.2%22%20transform%3D%22rotate%28-18%2016%2016%29%22%2F%3E%0A%20%20%3Cellipse%20cx%3D%2216%22%20cy%3D%2216%22%20rx%3D%225.7%22%20ry%3D%222.2%22%20fill%3D%22none%22%20stroke%3D%22%2345E7FF%22%20stroke-width%3D%221.6%22%20transform%3D%22rotate%28-18%2016%2016%29%22%2F%3E%0A%20%20%3Ccircle%20cx%3D%2216%22%20cy%3D%2216%22%20r%3D%221.6%22%20fill%3D%22%237575FF%22%2F%3E%0A%20%20%3Cpath%20d%3D%22M16%202.5V7%20M16%2025V29.5%20M2.5%2016H7%20M25%2016H29.5%22%20fill%3D%22none%22%20stroke%3D%22%23FFFFFF%22%20stroke-width%3D%221.6%22%20stroke-linecap%3D%22round%22%2F%3E%0A%3C%2Fsvg%3E';
    const HUBBLE_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble-NASA-ESA-logo.png?v=9283e83cfbacd230551e9fc005794138be59709b';
    const JWST_ICON_URL='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/JWST/esa-jwst-logo.png?v=7169a77e4b56dc582f9b0b76bf389bcf337ce';
    const CHANDRA_ICON_URL='https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Chandra/images.png';
    const HD_LAYOUT=Object.freeze({bannerRatio:366/1536,imageRatio:630/1536,gap:6,edge:6,iconInset:20});
    const HOME=Object.freeze({name:'EARTH — MILKY WAY',ra:266.41683,dec:-29.00781,distance:null});
    const ARRIVAL_OCCUPANCY=Object.freeze({target:0.35,max:0.40,minFov:0.05,maxFov:8});
    const HUBBLE_PREFETCH_TARGET=10;
    const PREFETCH_MAX_WORKERS=3;
    const PREFETCH_PROBE_CONCURRENCY=3;
    const PREFETCH_HEALTH_INTERVAL_MS=30000;
    const ALADIN_PREWARM_DWELL_MS=1400;
    const PREFETCH_RETRY_MS=5000;
    const HD_PREFERRED_MAX_BYTES=1024*1024;
    const FRAMING_SAMPLE_SIZE=96;
    const FRAMING_MAX_SHIFT_FRACTION=0.18;
    const TRAVEL_SECONDS=14.4;
    const ARCHIVE_PRELOAD_TARGET=3;
    const startupTiming={startedAt:performance.now(),shellReadyAt:null,catalogReadyAt:null,randomReadyAt:null,fullReadyAt:null};

    let galaxyCatalog=[];
    let catalogRecordCount=0;
    let catalogDatabaseCounts=Object.freeze({hubble:0,jwst:0,chandra:0,total:0,eligibleHubble:0,eligibleJwst:0,eligibleChandra:0,eligibleTotal:0});
    let chandraTestQueue=[];
    let chandraTestTotal=0;
    let chandraTestOverrideActive=false;
    const prefetchReady=[];
    const prefetchQueued=[];
    const prefetchLoading=new Map();
    const prefetchControllers=new Map();
    const prefetchRetryAfter=new Map();
    const hdDownloadStatus=new Map();
    let prefetchFailedCount=0;
    let prefetchRetryTimer=0;
    let prefetchHealthTimer=0;
    let lastPrefetchHealth=Object.freeze({ready:0,loading:0,queued:0,total:0,activeKeys:Object.freeze([]),retryWait:Object.freeze([]),workers:Object.freeze([]),checkedAt:0});
    let priorityPrefetchDestination=null;
    let aladinPrefetchSerial=Promise.resolve();
    let activePreparedItem=null;
    let historyPreparedItem=null;
    let activeTargetKey='';
    let forcedDestination=null;
    let pendingHistoryIndex=null;
    let navigationPending=false;
    let backgroundWorkSuspended=false;
    let ensureArchivePreloadQueue=()=>{};
    const galaxyHistory=[];
    let galaxyHistoryIndex=-1;
    let travelHudFrame=0;
    let aladinPrewarm=null;
    let aladinPrewarmHost=null;
    let aladinPrewarmReady=null;
    let aladinPrewarmTimer=0;
    let aladinPrewarmWaitResolve=null;
    let aladinPrewarmActiveKey='';
    let aladinPrewarmLastKey='';
    const aladinPrewarmedKeys=new Set();

    function setHdStatus(destination,state,sourceKind=''){
        const key=destinationKey(destination);
        if(!key)return;
        const old=hdDownloadStatus.get(key)||{};
        hdDownloadStatus.set(key,{key,name:String(destination?.name||old.name||''),state,sourceKind:sourceKind||old.sourceKind||'',updatedAt:Date.now()});
    }

    function getHubbleDownloadStatus(){
        return Object.freeze([...hdDownloadStatus.values()].map(item=>Object.freeze({...item})));
    }

    function suspendBackgroundWork(){
        if(backgroundWorkSuspended)return;
        backgroundWorkSuspended=true;
        if(aladinPrewarmTimer){clearTimeout(aladinPrewarmTimer);aladinPrewarmTimer=0}
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
        aladinPrewarmActiveKey='';
        aladinPrewarm=null;
        aladinPrewarmReady=null;
        try{aladinPrewarmHost?.remove()}catch(_){}
        aladinPrewarmHost=null;
        for(const controller of prefetchControllers.values())try{controller.abort()}catch(_){}
    }

    function resumeBackgroundWork(){
        if(!backgroundWorkSuspended)return;
        backgroundWorkSuspended=false;
        const active=galaxyCatalog.find(item=>destinationKey(item)===activeTargetKey);
        const alreadyReady=Boolean(activePreparedItem?.key===activeTargetKey||prefetchReady.some(item=>item.key===activeTargetKey));
        if(active&&!alreadyReady)priorityPrefetchDestination=active;
        queueMicrotask(fillPrefetchQueue);
    }

    function clamp(value,min,max){return Math.max(min,Math.min(max,Number(value)))}
    function clamp01(value){return clamp(value,0,1)}
    function smootherstep(value){const t=clamp01(value);return t*t*t*(t*(t*6-15)+10)}

    function parseDistanceMly(value){
        if(typeof value==='number'&&Number.isFinite(value)&&value>0)return value;
        const text=String(value??'').trim().toLowerCase().replace(/,/g,'');
        if(!text)return null;
        let match=text.match(/([0-9]+(?:\.[0-9]+)?)\s*(billion|million|thousand)\s+light\s*-?\s*years?/i);
        if(match){
            const number=Number(match[1]);
            if(!Number.isFinite(number)||number<=0)return null;
            if(match[2]==='billion')return number*1000;
            if(match[2]==='million')return number;
            return number/1000;
        }
        match=text.match(/([0-9][0-9\s]*(?:\.[0-9]+)?)\s+light\s*-?\s*years?/i);
        if(!match)return null;
        const lightYears=Number(match[1].replace(/\s+/g,''));
        return Number.isFinite(lightYears)&&lightYears>0?lightYears/1_000_000:null;
    }

    function parseFieldOfViewDegrees(value){
        const text=String(value??'').trim().toLowerCase();
        if(!text)return null;
        const numbers=[...text.matchAll(/[0-9]+(?:\.[0-9]+)?/g)].slice(0,2).map(match=>Number(match[0])).filter(Number.isFinite);
        if(!numbers.length)return null;
        let span=Math.max(...numbers);
        if(/arcsec/.test(text))span/=3600;
        else if(/arcmin/.test(text))span/=60;
        else if(!/(?:degree|\bdeg\b)/.test(text))return null;
        return span>0?span:null;
    }

    function parseArchiveOrientation(value){
        const text=String(value??'').trim();
        if(!text)return null;
        const match=text.match(/North\s+is\s+([0-9]+(?:\.[0-9]+)?)\s*°?\s*(right|left)\s+of\s+vertical/i);
        if(!match)return null;
        const angle=Number(match[1]);
        if(!Number.isFinite(angle))return null;
        return normalizeSignedAngle((match[2].toLowerCase()==='left'?-1:1)*angle);
    }

    function extractDesignation(candidate){
        const explicit=String(candidate?.designation||'').trim();
        const texts=[explicit,candidate?.name,candidate?.title,candidate?.displayName,candidate?.imageType,candidate?.category]
            .map(value=>String(value||'').trim()).filter(Boolean);
        const joined=texts.join(' | ');
        if(/stephan(?:'|’)?s\s+quintet/i.test(joined))return 'HCG 92';
        for(const text of texts){
            let match=text.match(/\bHCG\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bHICKSON(?:\s+COMPACT\s+GROUP)?\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `HCG ${match[1].toUpperCase()}`;
            match=text.match(/\bABELL\s*[- ]?\s*(\d+[A-Z]?)\b/i);
            if(match)return `ABELL ${match[1].toUpperCase()}`;
        }
        if(explicit)return explicit.toUpperCase();
        for(const text of texts){
            const match=text.match(/\b(?:M|NGC|IC|UGC|PGC|ARP|ESO)\s*[- ]?\s*\d+[A-Z]?(?:[- ]?\d+)?\b/i);
            if(match)return match[0].replace(/\s+/g,' ').toUpperCase();
        }
        if(/\b(?:galaxy\s+cluster|cluster\s+of\s+galaxies|galaxies\s+cluster)\b/i.test(joined))return 'GALAXY CLUSTER';
        if(/\b(?:compact\s+group|galaxy\s+group|group\s+of\s+galaxies|quintet|quartet|triplet)\b/i.test(joined))return 'GALAXY GROUP';
        if(/\b(?:galaxy\s+pair|pair\s+of\s+galaxies|interacting\s+galaxies)\b/i.test(joined))return 'GALAXY PAIR';
        if(/\b(?:star\s+cluster|stellar\s+cluster)\b/i.test(joined))return 'STAR CLUSTER';
        if(/\b(?:star\s+field|stellar\s+field)\b/i.test(joined))return 'STAR FIELD';
        if(/\bnebula\b/i.test(joined))return 'NEBULA';
        if(/\bstar\b/i.test(joined)&&!/\bgalax/i.test(joined))return 'STAR';
        return 'GALAXY';
    }

    function normalizeCatalogGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')return null;
        const name=String(candidate.name||candidate.title||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.science?.distanceMly??candidate.distance);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.displayName||candidate.title||candidate.name||'').trim();
        const age=String(candidate.science?.ageDisplay??candidate.age??candidate.ageEstimate??candidate.age_estimate??'').trim();
        const ageGyr=Number(candidate.science?.ageGyr);
        const ageYears=Number.isFinite(ageGyr)&&ageGyr>0?ageGyr*1_000_000_000:Number(candidate.ageYears??candidate.age_years);
        const scienceSize=Array.isArray(candidate.science?.sizeKly)?candidate.science.sizeKly.map(value=>Number(value)*1000):null;
        const sizeRaw=scienceSize??candidate.physicalSizeLy??candidate.physical_size_ly??null;
        const physicalSizeLy=Array.isArray(sizeRaw)?sizeRaw.map(Number):Number(sizeRaw);
        const fieldDegrees=parseFieldOfViewDegrees(candidate.fieldOfView);
        const sourceUrl=String(candidate.sourceUrl||'').trim();
        const hdUrl=String(candidate.selectedImageUrl||'').trim();
        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)return null;
        if(!Number.isFinite(distance)||distance<=0||!constellation||!Number.isFinite(fieldDegrees)||fieldDegrees<=0)return null;
        let hd,source;
        try{hd=new URL(hdUrl);source=new URL(sourceUrl)}catch(_){return null}
        const approvedHost=host=>host==='esahubble.org'||host.endsWith('.esahubble.org');
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        const fov=clamp(fieldDegrees/ARRIVAL_OCCUPANCY.target,ARRIVAL_OCCUPANCY.minFov,ARRIVAL_OCCUPANCY.maxFov);
        return Object.freeze({
            source:'ESA/HUBBLE GALAXIES CATALOG FULL-0002',provider:'HUBBLE',hubble:true,
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy:Array.isArray(physicalSizeLy)?physicalSizeLy.filter(value=>Number.isFinite(value)&&value>0):Number.isFinite(physicalSizeLy)&&physicalSizeLy>0?physicalSizeLy:null,
            fov,imageFovDegrees:fieldDegrees,hdUrl:hd.href,sourceUrl:source.href,orientation:String(candidate.orientation||'').trim(),
            credit:String(candidate.credit||'ESA/Hubble').trim()||'ESA/Hubble',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'Hubble Space Telescope',
            githubImageUrl:String(candidate.githubImageUrl||'').trim(),sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }

    function chooseJwstImageUrl(candidate){
        const candidates=[...(Array.isArray(candidate?.jpegCandidates)?candidate.jpegCandidates:[]),candidate?.selectedImageUrl].map(value=>String(value||'').trim()).filter(Boolean);
        return candidates.find(url=>/\/screen\//i.test(url))||String(candidate?.selectedImageUrl||candidates[0]||'').trim();
    }

    function normalizeJwstGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')return null;
        const name=String(candidate.name||candidate.title||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.science?.distanceMly??candidate.distance);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.displayName||candidate.title||candidate.name||'').trim();
        const age=String(candidate.science?.ageDisplay??candidate.age??'').trim();
        const ageGyr=Number(candidate.science?.ageGyr);
        const ageYears=Number.isFinite(ageGyr)&&ageGyr>0?ageGyr*1_000_000_000:null;
        const scienceSize=Array.isArray(candidate.science?.sizeKly)?candidate.science.sizeKly.map(value=>Number(value)*1000):null;
        const physicalSizeLy=Array.isArray(scienceSize)?scienceSize.filter(value=>Number.isFinite(value)&&value>0):null;
        const fieldDegrees=parseFieldOfViewDegrees(candidate.fieldOfView);
        const sourceUrl=String(candidate.sourceUrl||'').trim();
        const hdUrl=chooseJwstImageUrl(candidate);
        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)return null;
        if(!Number.isFinite(distance)||distance<=0||!constellation||!Number.isFinite(fieldDegrees)||fieldDegrees<=0)return null;
        let hd,source;
        try{hd=new URL(hdUrl);source=new URL(sourceUrl)}catch(_){return null}
        const approvedHost=host=>host==='esawebb.org'||host.endsWith('.esawebb.org');
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        const fov=clamp(fieldDegrees/ARRIVAL_OCCUPANCY.target,ARRIVAL_OCCUPANCY.minFov,ARRIVAL_OCCUPANCY.maxFov);
        const orientation=String(candidate.orientation||'').trim();
        const archiveRotation=parseArchiveOrientation(orientation);
        return Object.freeze({
            source:'ESA/WEBB GALAXIES CATALOG FULL-0002',provider:'JWST',hubble:true,
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy, fov,imageFovDegrees:fieldDegrees,hdUrl:hd.href,sourceUrl:source.href,orientation,
            aladinRotation:Number.isFinite(archiveRotation)?archiveRotation:null,
            credit:String(candidate.credit||'ESA/Webb, NASA & CSA').trim()||'ESA/Webb, NASA & CSA',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'James Webb Space Telescope',
            githubImageUrl:'',sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }

    function normalizeChandraGalaxy(candidate,index){
        if(!candidate||typeof candidate!=='object')return null;
        const name=String(candidate.name||candidate.title||'').trim();
        const ra=Number(candidate.ra),dec=Number(candidate.dec);
        const distance=parseDistanceMly(candidate.science?.distanceMly??candidate.distance);
        const constellation=String(candidate.constellation||'').trim();
        const designation=extractDesignation(candidate);
        const commonName=String(candidate.displayName||candidate.title||candidate.name||'').trim();
        const age=String(candidate.science?.ageDisplay??candidate.age??'').trim();
        const ageGyr=Number(candidate.science?.ageGyr);
        const ageYears=Number.isFinite(ageGyr)&&ageGyr>0?ageGyr*1_000_000_000:null;
        const scienceSize=Array.isArray(candidate.science?.sizeKly)?candidate.science.sizeKly.map(value=>Number(value)*1000):null;
        const physicalSizeLy=Array.isArray(scienceSize)?scienceSize.filter(value=>Number.isFinite(value)&&value>0):null;
        const fieldDegrees=parseFieldOfViewDegrees(candidate.fieldOfView);
        const fov=Number.isFinite(fieldDegrees)&&fieldDegrees>0?clamp(fieldDegrees/ARRIVAL_OCCUPANCY.target,ARRIVAL_OCCUPANCY.minFov,ARRIVAL_OCCUPANCY.maxFov):0.25;
        const sourceUrl=String(candidate.sourceUrl||'').trim();
        const hdUrl=String(candidate.selectedImageUrl||'').trim();
        if(!name||!Number.isFinite(ra)||ra<0||ra>=360||!Number.isFinite(dec)||dec<-90||dec>90)return null;
        if(!Number.isFinite(distance)||distance<=0||!constellation)return null;
        let hd,source;
        try{hd=new URL(hdUrl);source=new URL(sourceUrl)}catch(_){return null}
        const approvedHost=host=>host==='chandra.harvard.edu'||host.endsWith('.chandra.harvard.edu');
        if(hd.protocol!=='https:'||source.protocol!=='https:'||!approvedHost(hd.hostname)||!approvedHost(source.hostname))return null;
        const imageType=String(candidate.imageType||'').trim();
        if(imageType&&/\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(imageType))return null;
        return Object.freeze({
            source:'NASA CHANDRA X-RAY CENTER CATALOG FULL-0001',provider:'CHANDRA',hubble:true,
            archiveId:String(candidate.archiveId||'').trim(),
            name,ra,dec,distance,constellation,designation,commonName,age,
            ageYears:Number.isFinite(ageYears)&&ageYears>0?ageYears:null,
            physicalSizeLy,fov,imageFovDegrees:Number.isFinite(fieldDegrees)&&fieldDegrees>0?fieldDegrees:null,hdUrl:hd.href,sourceUrl:source.href,orientation:String(candidate.orientation||'').trim(),
            credit:String(candidate.credit||'NASA/CXC').trim()||'NASA/CXC',
            imageType:imageType||'Observation',category:'Galaxies',telescope:'Chandra X-ray Observatory',
            githubImageUrl:'',sha256:String(candidate.sha256||'').trim(),catalogIndex:index
        });
    }

    async function loadGalaxyCatalog(){
        const response=await fetch(HUBBLE_CATALOG_URL,{cache:'no-store'});
        if(!response.ok)throw new Error('FULL HUBBLE CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);
        if(!Array.isArray(raw)||!raw.length||!Number.isFinite(declared)||declared!==raw.length)throw new Error('FULL HUBBLE CATALOG COUNT MISMATCH');
        const eligible=raw.map(normalizeCatalogGalaxy).filter(Boolean);
        if(eligible.length<HUBBLE_PREFETCH_TARGET)throw new Error('FULL HUBBLE CATALOG HAS FEWER THAN TEN TRUTHFULLY TARGETABLE GALAXIES');
        return Object.freeze({rawCount:raw.length,eligible:Object.freeze(eligible)});
    }

    async function loadJwstCatalog(){
        const response=await fetch(JWST_CATALOG_URL,{cache:'no-store'});
        if(!response.ok)throw new Error('FULL JWST CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);
        if(payload?.version!=='full-0002')throw new Error('JWST CATALOG MUST BE FULL-0002');
        if(!Array.isArray(raw)||!raw.length||!Number.isFinite(declared)||declared!==raw.length)throw new Error('FULL JWST CATALOG COUNT MISMATCH');
        const eligible=raw.map(normalizeJwstGalaxy).filter(Boolean);
        if(!eligible.length)throw new Error('FULL JWST CATALOG HAS NO TARGETABLE GALAXIES');
        return Object.freeze({rawCount:raw.length,eligible:Object.freeze(eligible)});
    }

    async function loadChandraCatalog(){
        const response=await fetch(CHANDRA_CATALOG_URL,{cache:'no-store'});
        if(!response.ok)throw new Error('FULL CHANDRA CATALOG RETURNED HTTP '+response.status);
        const payload=await response.json();
        const raw=payload?.entries;
        const declared=Number(payload?.categoryEntryCount);
        if(payload?.version!=='full-0001')throw new Error('CHANDRA CATALOG MUST BE FULL-0001');
        if(!Array.isArray(raw)||!raw.length||!Number.isFinite(declared)||declared!==raw.length)throw new Error('FULL CHANDRA CATALOG COUNT MISMATCH');
        const eligible=raw.map(normalizeChandraGalaxy).filter(Boolean);
        if(!eligible.length)throw new Error('FULL CHANDRA CATALOG HAS NO TARGETABLE GALAXIES');
        return Object.freeze({rawCount:raw.length,eligible:Object.freeze(eligible)});
    }

    function shuffledCopy(items){
        const copy=[...items];
        for(let i=copy.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]]}
        return copy;
    }

    async function loadCombinedGalaxyCatalog(){
        const [hubbleData,jwstData,chandraData]=await Promise.all([loadGalaxyCatalog(),loadJwstCatalog(),loadChandraCatalog()]);
        const hubble=hubbleData.eligible,jwst=jwstData.eligible,chandra=chandraData.eligible;
        const combined=Object.freeze([...hubble,...jwst,...chandra]);
        chandraTestQueue=shuffledCopy(chandra);
        chandraTestTotal=chandraTestQueue.length;
        chandraTestOverrideActive=false;
        catalogRecordCount=combined.length;
        catalogDatabaseCounts=Object.freeze({hubble:hubbleData.rawCount,jwst:jwstData.rawCount,chandra:chandraData.rawCount,total:hubbleData.rawCount+jwstData.rawCount+chandraData.rawCount,eligibleHubble:hubble.length,eligibleJwst:jwst.length,eligibleChandra:chandra.length,eligibleTotal:combined.length});
        console.info('GALAXY VIEWER CATALOG COUNTS',catalogDatabaseCounts);
        return combined;
    }

    function destinationKey(destination){return String(destination?.archiveId||destination?.name||'').trim().toLowerCase()}
    function chooseGalaxy(catalog,excludeName=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        const available=catalog.filter(item=>item.name.toLowerCase()!==excluded&&destinationKey(item)!==activeTargetKey);
        const pool=available.length?available:catalog;
        return pool[Math.floor(Math.random()*pool.length)];
    }

    function releasePreparedItem(item){
        if(!item)return;
        try{if(item.image)item.image.src=''}catch(_){}
        try{if(item.objectUrl)URL.revokeObjectURL(item.objectUrl)}catch(_){}
    }

    async function decodePreparedBlob(blob){
        const objectUrl=URL.createObjectURL(blob);
        const image=new Image();
        image.decoding='async';
        image.loading='eager';
        image.src=objectUrl;
        try{
            if(image.decode){
                try{await image.decode()}catch(_){
                    if(!(image.complete&&image.naturalWidth))await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HD PRELOAD FAILED')),{once:true})});
                }
            }else if(!(image.complete&&image.naturalWidth)){
                await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HD PRELOAD FAILED')),{once:true})});
            }
            if(!image.naturalWidth||!image.naturalHeight)throw new Error('HD PRELOAD DECODED WITHOUT IMAGE DIMENSIONS');
            return {image,objectUrl};
        }catch(error){
            image.src='';
            URL.revokeObjectURL(objectUrl);
            throw error;
        }
    }

    function hdVariantRank(url){
        const value=String(url||'').toLowerCase();
        if(value.includes('/publicationjpg/'))return 60;
        if(value.includes('/large/'))return 50;
        if(value.includes('/screen/'))return 40;
        if(value.includes('/wallpaper'))return 30;
        if(value.includes('/thumb700'))return 20;
        if(value.includes('/thumb300'))return 10;
        return 45;
    }

    function buildHdSourceCandidates(destination){
        const sources=[];
        const seen=new Set();
        const add=(url,kind,rank=hdVariantRank(url))=>{
            const value=String(url||'').trim();
            if(!/^https:\/\//i.test(value)||seen.has(value))return;
            seen.add(value);sources.push({url:value,kind,rank});
        };
        const github=String(destination.githubImageUrl||'').trim();
        const archive=String(destination.hdUrl||'').trim();
        if(github)add(github,'GITHUB',55);
        if(archive){
            const provider=destination.provider||'ARCHIVE';
            const match=archive.match(/^(https:\/\/[^/]+\/archives\/images\/)([^/]+)(\/[^?#]+(?:\?[^#]*)?)$/i);
            if(match){
                for(const variant of ['publicationjpg','large','screen','wallpaper1','thumb700x','thumb300y'])add(match[1]+variant+match[3],provider,hdVariantRank('/'+variant+'/'));
            }
            add(archive,provider);
        }
        return sources.sort((a,b)=>b.rank-a.rank);
    }

    async function probeHdSourceBytes(source,signal=null){
        try{
            const head=await fetch(source.url,{method:'HEAD',cache:'force-cache',signal});
            if(head.ok){
                const length=Number(head.headers.get('content-length'));
                if(Number.isFinite(length)&&length>0)return length;
            }
        }catch(error){if(error?.name==='AbortError')throw error}
        try{
            const probe=await fetch(source.url,{method:'GET',headers:{Range:'bytes=0-0'},cache:'force-cache',signal});
            if(!probe.ok&&probe.status!==206)return null;
            const range=String(probe.headers.get('content-range')||'');
            const total=Number(range.match(/\/(\d+)$/)?.[1]);
            const length=Number(probe.headers.get('content-length'));
            try{await probe.body?.cancel()}catch(_){}
            if(Number.isFinite(total)&&total>0)return total;
            if(probe.status===200&&Number.isFinite(length)&&length>0)return length;
        }catch(error){if(error?.name==='AbortError')throw error}
        return null;
    }

    async function mapWithConcurrency(items,limit,worker){
        const results=new Array(items.length);
        let next=0;
        const count=Math.max(1,Math.min(Number(limit)||1,items.length));
        await Promise.all(Array.from({length:count},async()=>{
            for(;;){
                const index=next++;
                if(index>=items.length)return;
                results[index]=await worker(items[index],index);
            }
        }));
        return results;
    }

    async function orderHdSourcesBySize(destination,signal=null){
        const sources=buildHdSourceCandidates(destination);
        if(sources.length<2)return sources;
        const probed=await mapWithConcurrency(sources,PREFETCH_PROBE_CONCURRENCY,async source=>({...source,bytes:await probeHdSourceBytes(source,signal)}));
        const preferred=[];
        const oversized=[];
        const unknown=[];
        for(const source of probed){
            const bytes=source.bytes;
            if(Number.isFinite(bytes)&&bytes>0&&bytes<=HD_PREFERRED_MAX_BYTES)preferred.push(source);
            else if(Number.isFinite(bytes)&&bytes>HD_PREFERRED_MAX_BYTES)oversized.push(source);
            else unknown.push(source);
        }
        preferred.sort((a,b)=>b.rank-a.rank||b.bytes-a.bytes);
        oversized.sort((a,b)=>a.bytes-b.bytes||a.rank-b.rank);
        unknown.sort((a,b)=>a.rank-b.rank);
        return [...preferred,...oversized,...unknown];
    }

    async function prepareHdDestination(destination,signal=null){
        const sources=await orderHdSourcesBySize(destination,signal);
        let lastError=null;
        for(const source of sources){
            try{
                setHdStatus(destination,'DOWNLOADING',source.kind);
                const response=await fetch(source.url,{cache:'force-cache',signal});
                if(!response.ok)throw new Error('HD PRELOAD RETURNED HTTP '+response.status);
                const blob=await response.blob();
                if(signal?.aborted)throw new DOMException('HD PRELOAD SUSPENDED','AbortError');
                setHdStatus(destination,'DECODING',source.kind);
                const prepared=await decodePreparedBlob(blob);
                setHdStatus(destination,'READY',source.kind);
                return {key:destinationKey(destination),destination,image:prepared.image,objectUrl:prepared.objectUrl,sourceUrl:source.url,sourceKind:source.kind};
            }catch(error){
                if(error?.name==='AbortError'){setHdStatus(destination,'SUSPENDED',source.kind);throw error}
                lastError=error;
            }
        }
        setHdStatus(destination,'RETRY-WAIT');
        throw lastError||new Error('HD PRELOAD HAS NO USABLE SOURCE');
    }

    function ensureAladinPrewarm(){
        if(backgroundWorkSuspended)return Promise.resolve(null);
        if(aladinPrewarmReady)return aladinPrewarmReady;
        aladinPrewarmReady=new Promise((resolve,reject)=>{
            const frame=document.createElement('iframe');
            aladinPrewarmHost=frame;
            frame.id='gv-aladin-prewarm-frame';
            frame.setAttribute('aria-hidden','true');
            frame.tabIndex=-1;
            Object.assign(frame.style,{position:'fixed',left:'-10000px',top:'0',width:'512px',height:'512px',border:'0',opacity:'0',pointerEvents:'none',overflow:'hidden'});
            frame.srcdoc=`<!doctype html><html><head><link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css"><style>html,body,#gv-prewarm{margin:0;width:512px;height:512px;overflow:hidden;background:#000}</style></head><body><div id="gv-prewarm"></div><script src="${ALADIN_URL}"><\/script></body></html>`;
            frame.addEventListener('load',async()=>{
                try{
                    if(backgroundWorkSuspended){resolve(null);return}
                    const win=frame.contentWindow;
                    if(!win?.A?.init)throw new Error('ISOLATED ALADIN PREWARM EXPORT MISSING');
                    await win.A.init;
                    if(backgroundWorkSuspended){resolve(null);return}
                    aladinPrewarm=win.A.aladin('#gv-prewarm',{
                        target:`${HOME.ra} ${HOME.dec}`,
                        survey:'P/DSS2/color',
                        fov:1,
                        projection:'SIN',
                        cooFrame:'ICRSd',
                        showReticle:false,
                        showZoomControl:false,
                        showFullscreenControl:false,
                        showLayersControl:false,
                        showGotoControl:false,
                        showCooGridControl:false,
                        showSettingsControl:false,
                        showSelectionModeControl:false,
                        showColorPickerControl:false,
                        showShareControl:false,
                        showSimbadPointerControl:false,
                        showProjectionControl:false,
                        showStatusBar:false,
                        showFrame:false,
                        showFov:false,
                        showCooLocation:false,
                        showContextMenu:false,
                        showCatalog:false,
                        showCooGrid:false
                    });
                    if(typeof aladinPrewarm.setFrame==='function')aladinPrewarm.setFrame('ICRSd');
                    if(typeof aladinPrewarm.setProjection==='function')aladinPrewarm.setProjection('SIN');
                    resolve(aladinPrewarm);
                }catch(error){reject(error)}
            },{once:true});
            frame.addEventListener('error',()=>reject(new Error('ISOLATED ALADIN PREWARM FRAME FAILED TO LOAD')),{once:true});
            document.body.appendChild(frame);
        }).catch(error=>{
            console.warn('GALAXY VIEWER ISOLATED ALADIN PREWARM WARNING',error);
            aladinPrewarmReady=null;
            aladinPrewarm=null;
            try{aladinPrewarmHost?.remove()}catch(_){}
            aladinPrewarmHost=null;
            return null;
        });
        return aladinPrewarmReady;
    }

    function abortError(message='BACKGROUND PREPARATION SUSPENDED'){return new DOMException(message,'AbortError')}

    async function prepareAladinDestination(destination,force=false){
        if(backgroundWorkSuspended)throw abortError();
        const key=destinationKey(destination);
        if(!key)return false;
        if(aladinPrewarmedKeys.has(key)&&!force)return true;
        aladinPrewarmActiveKey=key;
        const isolated=await ensureAladinPrewarm();
        if(backgroundWorkSuspended||!isolated){aladinPrewarmActiveKey='';throw abortError()}
        try{
            if(typeof isolated.setFrame==='function')isolated.setFrame('ICRSd');
            if(typeof isolated.setProjection==='function')isolated.setProjection('SIN');
            if(typeof isolated.setRotation==='function'&&Number.isFinite(Number(destination.aladinRotation)))isolated.setRotation(Number(destination.aladinRotation));
            if(typeof isolated.gotoRaDec==='function')isolated.gotoRaDec(destination.ra,destination.dec);
            if(typeof isolated.setFov==='function')isolated.setFov(destination.fov);
        }catch(error){
            aladinPrewarmActiveKey='';
            throw error;
        }
        const completed=await new Promise(resolve=>{
            aladinPrewarmWaitResolve=resolve;
            aladinPrewarmTimer=setTimeout(()=>{
                aladinPrewarmTimer=0;
                if(aladinPrewarmWaitResolve===resolve)aladinPrewarmWaitResolve=null;
                resolve(true);
            },ALADIN_PREWARM_DWELL_MS);
        });
        aladinPrewarmActiveKey='';
        if(!completed||backgroundWorkSuspended)throw abortError();
        aladinPrewarmedKeys.add(key);
        aladinPrewarmLastKey=key;
        return true;
    }

    function imageLightProfile(source){
        if(!source)return null;
        try{
            const canvas=document.createElement('canvas');
            canvas.width=FRAMING_SAMPLE_SIZE;canvas.height=FRAMING_SAMPLE_SIZE;
            const ctx=canvas.getContext('2d',{willReadFrequently:true});
            if(!ctx)return null;
            ctx.filter='blur(2px)';
            ctx.drawImage(source,0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE);
            const data=ctx.getImageData(0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE).data;
            const lum=[];
            for(let i=0;i<data.length;i+=4)lum.push(.2126*data[i]+.7152*data[i+1]+.0722*data[i+2]);
            const sorted=[...lum].sort((a,b)=>a-b);
            const background=sorted[Math.floor(sorted.length*.45)]||0;
            const threshold=sorted[Math.floor(sorted.length*.78)]||background;
            let sum=0,sx=0,sy=0;
            const weights=new Float64Array(lum.length);
            for(let y=0;y<FRAMING_SAMPLE_SIZE;y++)for(let x=0;x<FRAMING_SAMPLE_SIZE;x++){
                const index=y*FRAMING_SAMPLE_SIZE+x;
                const edge=Math.min(x,y,FRAMING_SAMPLE_SIZE-1-x,FRAMING_SAMPLE_SIZE-1-y);
                const edgeFactor=clamp(edge/(FRAMING_SAMPLE_SIZE*.08),0,1);
                const weight=Math.max(0,lum[index]-Math.max(background,threshold*.82))*edgeFactor;
                weights[index]=weight;sum+=weight;sx+=weight*x;sy+=weight*y;
            }
            if(!(sum>1))return null;
            const cx=sx/sum,cy=sy/sum;
            let xx=0,yy=0,xy=0;
            for(let y=0;y<FRAMING_SAMPLE_SIZE;y++)for(let x=0;x<FRAMING_SAMPLE_SIZE;x++){
                const weight=weights[y*FRAMING_SAMPLE_SIZE+x];if(!weight)continue;
                const dx=x-cx,dy=y-cy;xx+=weight*dx*dx;yy+=weight*dy*dy;xy+=weight*dx*dy;
            }
            xx/=sum;yy/=sum;xy/=sum;
            const trace=xx+yy,disc=Math.sqrt(Math.max(0,(xx-yy)*(xx-yy)+4*xy*xy));
            const major=(trace+disc)/2,minor=(trace-disc)/2;
            const eccentricity=major>0?clamp(1-Math.max(0,minor)/major,0,1):0;
            const angle=.5*Math.atan2(2*xy,xx-yy)*180/Math.PI;
            return {x:cx,y:cy,angle,eccentricity,weight:sum};
        }catch(_){return null}
    }

    function normalizeSignedAngle(value){
        let angle=Number(value)||0;
        while(angle>90)angle-=180;
        while(angle<-90)angle+=180;
        return angle;
    }

    function angularSeparationDegrees(ra1,dec1,ra2,dec2){
        const d=Math.PI/180;
        const a1=ra1*d,a2=ra2*d,b1=dec1*d,b2=dec2*d;
        const cosine=Math.sin(b1)*Math.sin(b2)+Math.cos(b1)*Math.cos(b2)*Math.cos(a1-a2);
        return Math.acos(clamp(cosine,-1,1))/d;
    }

    function deriveHubbleFraming(destination,hubbleImage){
        if(!hubbleImage?.naturalWidth||!hubbleImage?.naturalHeight||!aladinPrewarm||!aladinPrewarmHost)return destination;
        try{
            const skyCanvas=aladinPrewarmHost.contentDocument?.querySelector('canvas');
            if(!skyCanvas)return destination;
            const hubble=imageLightProfile(hubbleImage),sky=imageLightProfile(skyCanvas);
            if(!hubble||!sky)return destination;
            const width=skyCanvas.clientWidth||skyCanvas.width||512,height=skyCanvas.clientHeight||skyCanvas.height||512;
            const desiredX=hubble.x/FRAMING_SAMPLE_SIZE*width;
            const desiredY=hubble.y/FRAMING_SAMPLE_SIZE*height;
            const currentX=sky.x/FRAMING_SAMPLE_SIZE*width;
            const currentY=sky.y/FRAMING_SAMPLE_SIZE*height;
            const maxDx=width*FRAMING_MAX_SHIFT_FRACTION,maxDy=height*FRAMING_MAX_SHIFT_FRACTION;
            const sampleX=width/2+clamp(currentX-desiredX,-maxDx,maxDx);
            const sampleY=height/2+clamp(currentY-desiredY,-maxDy,maxDy);
            if(typeof aladinPrewarm.pix2world!=='function')return destination;
            const world=aladinPrewarm.pix2world(sampleX,sampleY);
            const ra=Number(world?.[0]),dec=Number(world?.[1]);
            if(!Number.isFinite(ra)||!Number.isFinite(dec))return destination;
            const maxAngularShift=Math.max(.02,Number(destination.fov)*.30);
            if(angularSeparationDegrees(destination.ra,destination.dec,ra,dec)>maxAngularShift)return destination;
            let rotation=Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):null;
            if(rotation===null&&hubble.eccentricity>.22&&sky.eccentricity>.22){
                const delta=normalizeSignedAngle(hubble.angle-sky.angle);
                if(Number.isFinite(delta)&&Math.abs(delta)<=90)rotation=delta;
            }
            return Object.freeze({...destination,ra,dec,aladinRotation:rotation,framingCorrected:true});
        }catch(error){
            console.warn('GALAXY VIEWER OPTIONAL ARCHIVE FRAMING SKIPPED',error);
            return destination;
        }
    }

    function blockedPrefetchKeys(){
        const keys=new Set(prefetchReady.map(item=>item.key));
        for(const destination of prefetchQueued)keys.add(destinationKey(destination));
        for(const key of prefetchLoading.keys())keys.add(key);
        if(priorityPrefetchDestination)keys.add(destinationKey(priorityPrefetchDestination));
        if(activePreparedItem?.key)keys.add(activePreparedItem.key);
        if(historyPreparedItem?.key)keys.add(historyPreparedItem.key);
        if(activeTargetKey)keys.add(activeTargetKey);
        return keys;
    }

    function choosePrefetchCandidate(){
        const blocked=blockedPrefetchKeys(),now=Date.now();
        const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&now>=Number(prefetchRetryAfter.get(key)||0)});
        if(!pool.length)return null;
        const warmed=pool.filter(item=>aladinPrewarmedKeys.has(destinationKey(item)));
        const preferred=warmed.length?warmed:pool;
        return preferred[Math.floor(Math.random()*preferred.length)];
    }

    function chooseAladinAheadCandidates(destination,count=2){
        const blocked=blockedPrefetchKeys();
        blocked.add(destinationKey(destination));
        const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&!aladinPrewarmedKeys.has(key)});
        const chosen=[];
        while(pool.length&&chosen.length<count){const index=Math.floor(Math.random()*pool.length);chosen.push(pool.splice(index,1)[0])}
        return chosen;
    }

    function inFlightDestination(excludeName=''){
        const excluded=String(excludeName||'').trim().toLowerCase();
        for(const key of prefetchLoading.keys()){
            const destination=galaxyCatalog.find(item=>destinationKey(item)===key&&item.name.toLowerCase()!==excluded);
            if(destination)return destination;
        }
        return null;
    }

    function scheduleRetryFill(){
        if(prefetchRetryTimer)return;
        const now=Date.now();
        const waits=[...prefetchRetryAfter.values()].map(value=>Number(value)-now).filter(value=>value>0);
        if(!waits.length)return;
        prefetchRetryTimer=setTimeout(()=>{prefetchRetryTimer=0;fillPrefetchQueue()},Math.max(100,Math.min(...waits)));
    }

    function queueHasKey(key){return prefetchQueued.some(destination=>destinationKey(destination)===key)}

    function enqueuePrefetch(destination,priority=false){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItem?.key===key)return false;
        const queuedIndex=prefetchQueued.findIndex(item=>destinationKey(item)===key);
        if(queuedIndex>=0){
            if(priority&&queuedIndex>0){const [queued]=prefetchQueued.splice(queuedIndex,1);prefetchQueued.unshift(queued)}
            return false;
        }
        if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return false}
        setHdStatus(destination,'QUEUED');
        if(priority)prefetchQueued.unshift(destination);else prefetchQueued.push(destination);
        return true;
    }

    function scheduleAladinEnhancement(item,destination,priority=false){
        const key=destinationKey(destination);
        const task=async()=>{
            if(backgroundWorkSuspended||!item?.image)return;
            try{
                const ahead=chooseAladinAheadCandidates(destination,2);
                for(const candidate of [destination,...ahead]){
                    if(backgroundWorkSuspended)return;
                    try{await prepareAladinDestination(candidate,priority&&candidate===destination)}catch(error){
                        if(error?.name==='AbortError')return;
                        console.warn('GALAXY VIEWER ALADIN AHEAD PREWARM WARNING',error);
                    }
                }
                if(backgroundWorkSuspended||aladinPrewarmLastKey!==key)return;
                let preparedDestination=deriveHubbleFraming(destination,item.image);
                if(preparedDestination!==destination&&preparedDestination.framingCorrected){
                    try{await prepareAladinDestination(preparedDestination,true)}catch(error){
                        if(error?.name==='AbortError')return;
                        preparedDestination=destination;
                    }
                }
                item.destination=preparedDestination;
            }catch(error){
                if(error?.name!=='AbortError')console.warn('GALAXY VIEWER SERIAL ALADIN PREWARM WARNING',error);
            }
        };
        const run=aladinPrefetchSerial.then(task,task);
        aladinPrefetchSerial=run.catch(()=>null);
    }

    function startPrefetch(destination,priority=false){
        const key=destinationKey(destination);
        if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItem?.key===key)return;
        if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return}
        if(prefetchLoading.size>=PREFETCH_MAX_WORKERS){enqueuePrefetch(destination,priority);return}
        const controller=new AbortController();
        prefetchControllers.set(key,controller);
        const promise=(async()=>{
            try{
                const item=await prepareHdDestination(destination,controller.signal);
                item.destination=destination;
                prefetchRetryAfter.delete(key);
                if(key===activeTargetKey&&!activePreparedItem){
                    activePreparedItem=item;
                    window.GalaxyViewerRandomGalaxy?.setPreparedHdResource?.(key,item.objectUrl,item.sourceKind,item.image);
                }else if(prefetchReady.length<HUBBLE_PREFETCH_TARGET){
                    prefetchReady.push(item);
                }else{
                    releasePreparedItem(item);
                    return;
                }
                scheduleAladinEnhancement(item,destination,priority);
            }catch(error){
                if(error?.name==='AbortError'){
                    setHdStatus(destination,'SUSPENDED');
                    if(key===activeTargetKey)priorityPrefetchDestination=destination;
                    return;
                }
                prefetchFailedCount++;
                setHdStatus(destination,'RETRY-WAIT');
                prefetchRetryAfter.set(key,Date.now()+PREFETCH_RETRY_MS);
            }
        })().finally(()=>{
            prefetchLoading.delete(key);
            prefetchControllers.delete(key);
            queueMicrotask(fillPrefetchQueue);
            queueMicrotask(ensureArchivePreloadQueue);
        });
        prefetchLoading.set(key,promise);
    }

    function fillPrefetchQueue(){
        if(backgroundWorkSuspended)return;
        if(priorityPrefetchDestination){
            const destination=priorityPrefetchDestination;
            priorityPrefetchDestination=null;
            enqueuePrefetch(destination,true);
        }
        while(prefetchReady.length+prefetchLoading.size+prefetchQueued.length<HUBBLE_PREFETCH_TARGET){
            const candidate=choosePrefetchCandidate();
            if(!candidate||!enqueuePrefetch(candidate))break;
        }
        while(prefetchLoading.size<PREFETCH_MAX_WORKERS&&prefetchQueued.length){
            const destination=prefetchQueued.shift();
            startPrefetch(destination,destinationKey(destination)===activeTargetKey);
        }
        if(prefetchReady.length+prefetchLoading.size+prefetchQueued.length<HUBBLE_PREFETCH_TARGET)scheduleRetryFill();
    }

    function prefetchHealthCheck(){
        const ready=prefetchReady.length;
        const loading=prefetchLoading.size;
        const queued=prefetchQueued.length;
        const activeKeys=[...prefetchLoading.keys()];
        const retryWait=[...prefetchRetryAfter.entries()].filter(([,time])=>Date.now()<Number(time)).map(([key])=>key);
        const workers=activeKeys.map(key=>Object.freeze({...hdDownloadStatus.get(key)}));
        lastPrefetchHealth=Object.freeze({ready,loading,queued,total:ready+loading+queued,activeKeys:Object.freeze(activeKeys),retryWait:Object.freeze(retryWait),workers:Object.freeze(workers),checkedAt:Date.now()});
        if(!backgroundWorkSuspended&&lastPrefetchHealth.total<HUBBLE_PREFETCH_TARGET)fillPrefetchQueue();
        return lastPrefetchHealth;
    }

    prefetchHealthTimer=setInterval(prefetchHealthCheck,PREFETCH_HEALTH_INTERVAL_MS);

    function destinationWithPrepared(item){
        return {...item.destination,preparedHdUrl:item.objectUrl,preparedSource:item.sourceKind,preparedHdImage:item.image};
    }

    function setPreparedActive(item){
        if(activePreparedItem&&activePreparedItem!==item&&activePreparedItem.key!==item.key){
            releasePreparedItem(historyPreparedItem);
            historyPreparedItem=activePreparedItem;
        }
        activePreparedItem=item;
        activeTargetKey=item.key;
    }

    function setUnpreparedActive(destination){
        const key=destinationKey(destination);
        if(activePreparedItem&&activePreparedItem.key!==key){
            releasePreparedItem(historyPreparedItem);
            historyPreparedItem=activePreparedItem;
        }
        activePreparedItem=null;
        activeTargetKey=key;
        priorityPrefetchDestination=destination;
        if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
        return {...destination,preparedHdUrl:'',preparedSource:'',preparedHdImage:null};
    }

    function consumeReady(destination=null,excludeName=''){
        const requestedKey=destination?destinationKey(destination):'';
        if(requestedKey&&activePreparedItem?.key===requestedKey)return destinationWithPrepared(activePreparedItem);
        if(requestedKey&&historyPreparedItem?.key===requestedKey){
            const item=historyPreparedItem;
            historyPreparedItem=activePreparedItem;
            activePreparedItem=item;
            activeTargetKey=item.key;
            if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
            return destinationWithPrepared(item);
        }
        let index=-1;
        if(destination)index=prefetchReady.findIndex(item=>item.key===requestedKey);
        else{
            const excluded=String(excludeName||'').trim().toLowerCase();
            index=prefetchReady.findIndex(item=>item.destination.name.toLowerCase()!==excluded);
        }
        if(index<0)return null;
        const [item]=prefetchReady.splice(index,1);
        setPreparedActive(item);
        if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
        return destinationWithPrepared(item);
    }

    async function waitForPreparedKey(key){
        for(;;){
            if(activePreparedItem?.key===key)return true;
            const loading=prefetchLoading.get(key);
            if(loading){
                try{await loading}catch(_){}
                return activePreparedItem?.key===key;
            }
            if(priorityPrefetchDestination&&destinationKey(priorityPrefetchDestination)===key){
                await new Promise(resolve=>setTimeout(resolve,25));
                continue;
            }
            return false;
        }
    }

    function distanceProgress(t){
        const turn=0.46,ninety=0.58,complete=0.68;
        if(t<=turn)return 0.20*smootherstep(t/turn);
        if(t<=ninety)return 0.20+0.70*smootherstep((t-turn)/(ninety-turn));
        if(t<=complete)return 0.90+0.08*smootherstep((t-ninety)/(complete-ninety));
        return 0.98+0.02*smootherstep((t-complete)/(1-complete));
    }

    function routeDistanceMillionLy(source,destination){
        const dA=Number(source?.distance),dB=Number(destination?.distance);
        if(Number.isFinite(dA)&&dA>0&&Number.isFinite(dB)&&dB>0){
            const toVector=(ra,dec)=>{const r=Number(ra)*Math.PI/180,d=Number(dec)*Math.PI/180;return [Math.cos(d)*Math.cos(r),Math.cos(d)*Math.sin(r),Math.sin(d)]};
            const a=toVector(source.ra,source.dec),b=toVector(destination.ra,destination.dec);
            const theta=Math.acos(clamp(a[0]*b[0]+a[1]*b[1]+a[2]*b[2],-1,1));
            return Math.sqrt(Math.max(0,dA*dA+dB*dB-2*dA*dB*Math.cos(theta)));
        }
        return Number.isFinite(dB)&&dB>0?dB:0;
    }

    function formatTravelDistance(millionLy){
        const value=Number.isFinite(Number(millionLy))&&Number(millionLy)>0?Number(millionLy):0;
        const scaled=value>=1000?value/1000:value;
        const [integer,fraction='00']=scaled.toFixed(2).split('.');
        return {integer,fraction:fraction.padEnd(2,'0').slice(0,2),unit:value>=1000?'BILLION LIGHT-YEARS':'MILLION LIGHT-YEARS'};
    }

    function beginTravelHud(destination){
        const hud=document.getElementById('gv-travel-hud');
        const destinationEl=document.getElementById('gv-travel-destination');
        const distanceIntegerEl=document.getElementById('gv-travel-distance-integer');
        const distanceFractionEl=document.getElementById('gv-travel-distance-fraction');
        const distanceUnitEl=document.getElementById('gv-travel-distance-unit');
        if(!hud||!destinationEl||!distanceIntegerEl||!distanceFractionEl||!distanceUnitEl)return;
        cancelAnimationFrame(travelHudFrame);
        const state=window.GalaxyViewerCore?.randomGalaxy?.getState?.()||window.GalaxyViewerRandomGalaxy?.getState?.()||{};
        const coords=window.aladin_cosmic_command_test?.getRaDec?.()||[HOME.ra,HOME.dec];
        const source={...(state.currentGalaxy||HOME),ra:Number(coords[0]),dec:Number(coords[1])};
        const fov=window.aladin_cosmic_command_test?.getFov?.()||[0,0];
        const firstHomeTrip=!(Number(source?.distance)>0)&&Number(fov[0])>=300;
        const hudSeconds=firstHomeTrip?8:TRAVEL_SECONDS;
        const total=routeDistanceMillionLy(source,destination);
        destinationEl.textContent=destination.name.toUpperCase();
        const initialDistance=formatTravelDistance(0);
        distanceIntegerEl.textContent=initialDistance.integer;
        distanceFractionEl.textContent=initialDistance.fraction;
        distanceUnitEl.textContent=initialDistance.unit;
        hud.classList.add('gv-visible');
        const started=performance.now();
        const frame=now=>{
            const t=Math.min(1,(now-started)/(hudSeconds*1000));
            const shown=formatTravelDistance(total*(firstHomeTrip?t:distanceProgress(t)));
            distanceIntegerEl.textContent=shown.integer;
            distanceFractionEl.textContent=shown.fraction;
            distanceUnitEl.textContent=shown.unit;
            if(t<1)travelHudFrame=requestAnimationFrame(frame);
        };
        travelHudFrame=requestAnimationFrame(frame);
    }

    function endTravelHud(){
        cancelAnimationFrame(travelHudFrame);
        const hud=document.getElementById('gv-travel-hud');
        if(hud)hud.classList.remove('gv-visible');
    }

    function takeNextChandraTestDestination(excludeName=''){
        if(!chandraTestOverrideActive||!chandraTestQueue.length){chandraTestOverrideActive=false;return null}
        const excluded=String(excludeName||'').trim().toLowerCase();
        let index=chandraTestQueue.findIndex(item=>String(item?.name||'').trim().toLowerCase()!==excluded);
        if(index<0)index=0;
        const [destination]=chandraTestQueue.splice(index,1);
        if(!chandraTestQueue.length)chandraTestOverrideActive=false;
        return destination||null;
    }

    function randomHubbleProvider({excludeName}={}){
        let destination=null;
        if(forcedDestination){
            releaseActiveArchivePreload();
            const requested=forcedDestination;
            forcedDestination=null;
            destination=consumeReady(requested,excludeName);
            if(!destination)destination=setUnpreparedActive(requested);
        }else{
            if(!galaxyCatalog.length)throw new Error('COMBINED GALAXY CATALOG IS EMPTY');
            releaseActiveArchivePreload();
            const chandraRequested=takeNextChandraTestDestination(excludeName);
            if(chandraRequested){
                destination=consumeReady(chandraRequested,excludeName);
                if(!destination)destination=setUnpreparedActive(chandraRequested);
            }else{
                const archiveItem=consumeArchivePreloadedDestination(excludeName);
                if(archiveItem){
                    const requested=archiveItem.destination;
                    destination=consumeReady(requested,excludeName);
                    if(!destination)destination=setUnpreparedActive(requested);
                    bindActiveArchivePreload(archiveItem,destination);
                }else{
                    destination=consumeReady(null,excludeName);
                    if(!destination){
                        const requested=galaxyCatalog[Math.floor(Math.random()*galaxyCatalog.length)];
                        destination=setUnpreparedActive(requested);
                    }
                }
            }
        }
        activeTargetKey=destinationKey(destination);
        if(Number.isFinite(Number(destination.aladinRotation))&&typeof window.aladin_cosmic_command_test?.setRotation==='function'){
            try{window.aladin_cosmic_command_test.setRotation(Number(destination.aladinRotation))}catch(error){console.warn('GALAXY VIEWER OPTIONAL ARRIVAL ROTATION SKIPPED',error)}
        }else if(typeof window.aladin_cosmic_command_test?.setRotation==='function'){
            try{window.aladin_cosmic_command_test.setRotation(0)}catch(_){}
        }
        beginTravelHud(destination);
        return destination;
    }

    function getHubblePrefetchState(){
        return Object.freeze({
            targetReady:HUBBLE_PREFETCH_TARGET,
            maxWorkers:PREFETCH_MAX_WORKERS,
            readyCount:prefetchReady.length,
            loadingCount:prefetchLoading.size,
            queuedCount:prefetchQueued.length,
            pipelineCount:prefetchReady.length+prefetchLoading.size+prefetchQueued.length,
            failedCount:prefetchFailedCount,
            activeDownloadKeys:Object.freeze([...prefetchLoading.keys()]),
            activePreparedGalaxy:activePreparedItem?.destination?.name||'',
            activePreparedSource:activePreparedItem?.sourceKind||'',
            readyDestinations:prefetchReady.map(item=>item.destination.name),
            queuedDestinations:prefetchQueued.map(item=>item.name),
            health:lastPrefetchHealth,
            downloads:getHubbleDownloadStatus()
        });
    }

    function getAladinPrewarmState(){
        return Object.freeze({
            targetReady:HUBBLE_PREFETCH_TARGET,
            cachedCount:aladinPrewarmedKeys.size,
            activeKey:aladinPrewarmActiveKey,
            queuedDestinations:[]
        });
    }

    function loadScript(url,datasetKey){
        return new Promise((resolve,reject)=>{
            const existing=[...document.scripts].find(script=>script.src===url||script.dataset[datasetKey]==='true');
            if(existing){
                if(existing.dataset.gvLoaded==='true'){resolve(existing);return}
                existing.addEventListener('load',()=>resolve(existing),{once:true});
                existing.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
                return;
            }
            const script=document.createElement('script');
            script.charset='utf-8';
            script.dataset[datasetKey]='true';
            if(url.startsWith('https://raw.githubusercontent.com/')){
                fetch(url,{cache:'no-store'}).then(response=>{
                    if(!response.ok)throw new Error('SCRIPT FETCH RETURNED HTTP '+response.status+': '+url);
                    return response.text();
                }).then(source=>{
                    if(datasetKey==='gvRandomGalaxy0031'){
                        source=source.replace("return host === 'esahubble.org' || host.endsWith('.esahubble.org');","return host === 'esahubble.org' || host.endsWith('.esahubble.org') || host === 'esawebb.org' || host.endsWith('.esawebb.org') || host === 'chandra.harvard.edu' || host.endsWith('.chandra.harvard.edu');");
                        source=source.replace("if (telescope && !/hubble/i.test(telescope)) throw new Error('Rejected entry without Hubble telescope data.');","if (telescope && !/(hubble|webb|chandra)/i.test(telescope)) throw new Error('Rejected entry without Hubble/Webb/Chandra telescope data.');");
                        source=source.replace("source: cleanText(candidate.source || 'ESA/HUBBLE GALAXIES CATALOG'),\n        hubble: true,","source: cleanText(candidate.source || 'ESA/HUBBLE GALAXIES CATALOG'),\n        provider: cleanText(candidate.provider || (/chandra/i.test(telescope) ? 'CHANDRA' : /webb/i.test(telescope) ? 'JWST' : 'HUBBLE')).toUpperCase(),\n        hubble: true,");
                        if(!source.includes("host === 'chandra.harvard.edu'")||!source.includes("/(hubble|webb|chandra)/i")||!source.includes("provider: cleanText(candidate.provider"))throw new Error('RANDOM GALAXY 0031 10AE2 COMPATIBILITY PATCH FAILED');
                    }
                    script.textContent=source;
                    document.head.appendChild(script);
                    script.dataset.gvLoaded='true';
                    resolve(script);
                }).catch(error=>reject(new Error('SCRIPT FAILED TO LOAD: '+url+' — '+String(error?.message||error))));
                return;
            }
            script.src=url;
            script.addEventListener('load',()=>{script.dataset.gvLoaded='true';resolve(script)},{once:true});
            script.addEventListener('error',()=>reject(new Error('SCRIPT FAILED TO LOAD: '+url)),{once:true});
            document.head.appendChild(script);
        });
    }

    async function ensureAladin(){
        if(window.A?.init)return window.A;
        await loadScript(ALADIN_URL,'gvAladin382');
        if(!window.A?.init)throw new Error('ALADIN LITE 3.8.2 EXPORT MISSING');
        return window.A;
    }

    function createHost(root,id){
        let host=root.querySelector('#'+id);
        if(!host){host=document.createElement('div');host.id=id;root.appendChild(host)}
        return host;
    }

    function createCenterReticle(root){
        const reticle=document.createElement('div');
        reticle.id='gv-center-reticle';
        reticle.setAttribute('aria-hidden','true');
        const image=document.createElement('img');
        image.src=RETICLE_URL;
        image.alt='';
        image.width=32;
        image.height=32;
        reticle.appendChild(image);
        root.appendChild(reticle);
        return reticle;
    }

    function createBottomControls(root){
        const version=document.createElement('div');
        version.id='gv-version-label';
        version.textContent=`VERSION ${DISPLAY_VERSION}`;
        version.setAttribute('aria-label',`GALAXY VIEWER VERSION ${DISPLAY_VERSION}`);
        root.appendChild(version);

        const nav=document.createElement('div');
        nav.id='gv-galaxy-nav';
        const back=document.createElement('button');
        back.type='button';back.className='gv-galaxy-history gv-galaxy-history-back';back.textContent='';back.setAttribute('aria-label','PREVIOUS GALAXY');back.disabled=true;
        const random=document.createElement('button');
        random.id='gv-random-galaxy';random.type='button';random.innerHTML='<span class="gvrg-random-layout"><span class="gvrg-random-star-wrap gvrg-random-star-wrap-left" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet gvrg-random-comet-left"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span><span class="gvrg-random-label">RANDOM GALAXY</span><span class="gvrg-random-star-wrap gvrg-random-star-wrap-right" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span></span>';random.setAttribute('aria-label','RANDOM GALAXY');
        const forward=document.createElement('button');
        forward.type='button';forward.className='gv-galaxy-history gv-galaxy-history-forward';forward.textContent='';forward.setAttribute('aria-label','NEXT GALAXY');forward.disabled=true;
        nav.append(back,random,forward);root.appendChild(nav);

        const hud=document.createElement('div');
        hud.id='gv-travel-hud';hud.setAttribute('role','status');hud.setAttribute('aria-live','polite');
        hud.innerHTML='<div id="gv-travel-distance"><span id="gv-travel-distance-value"><span id="gv-travel-distance-integer">0</span><span id="gv-travel-distance-decimal">.</span><span id="gv-travel-distance-fraction">00</span></span><span id="gv-travel-distance-unit">MILLION LIGHT-YEARS</span></div><div id="gv-travel-primary"><div id="gv-travel-course">COURSE LOCKED</div><div id="gv-travel-heading">HEADING TO</div><div id="gv-travel-destination"></div></div>';
        root.appendChild(hud);
        return {version,nav,back,random,forward,hud};
    }

    function createUniverseContext(root){
        const context=document.createElement('div');
        context.id='gv-universe-context';
        context.setAttribute('aria-live','polite');
        context.innerHTML='<div class="gv-universe-label">THIS IS OUR MAP OF THE OBSERVABLE UNIVERSE<span class="gv-universe-count">EST. ~2 TRILLION GALAXIES</span></div><div class="gv-universe-leader" aria-hidden="true"></div>';
        root.appendChild(context);
        return context;
    }

    function createHomeOverlay(root){
        const overlay=document.createElement('div');
        overlay.id='gv-we-are-here';
        overlay.setAttribute('aria-live','polite');
        overlay.innerHTML='<div class="gv-home-leader" aria-hidden="true"></div><div class="gv-home-label"><div class="gv-home-origin"><span class="gv-earth-icon" aria-hidden="true">🌎</span><strong>WE ARE HERE</strong></div><div class="gv-home-sub">EARTH — MILKY WAY</div><div class="gv-home-hint">TAP RANDOM GALAXY TO BEGIN</div></div>';
        root.appendChild(overlay);
        return overlay;
    }

    function equatorialToGalactic(raDeg,decDeg){
        const d=Math.PI/180,ra=raDeg*d,dec=decDeg*d;
        const raNGP=192.85948*d,decNGP=27.12825*d,lOmega=32.93192*d;
        const b=Math.asin(Math.sin(dec)*Math.sin(decNGP)+Math.cos(dec)*Math.cos(decNGP)*Math.cos(ra-raNGP));
        const y=Math.sin(dec)*Math.cos(decNGP)-Math.cos(dec)*Math.sin(decNGP)*Math.cos(ra-raNGP);
        const x=Math.cos(dec)*Math.sin(ra-raNGP);
        let l=(Math.atan2(y,x)+lOmega)/d;
        l=((l%360)+360)%360;
        return [l,b/d];
    }

    function readCurrentRaDec(aladin,root){
        try{
            const value=aladin.getRaDec?.();
            const ra=Number(value?.[0]),dec=Number(value?.[1]);
            if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
        }catch(error){console.warn('GALAXY VIEWER GETRADEC WARNING',error)}
        try{
            const canvas=root.querySelector('canvas');
            if(canvas&&typeof aladin.pix2world==='function'){
                const value=aladin.pix2world(canvas.clientWidth/2,canvas.clientHeight/2);
                const ra=Number(value?.[0]),dec=Number(value?.[1]);
                if(Number.isFinite(ra)&&Number.isFinite(dec))return [ra,dec];
            }
        }catch(error){console.warn('GALAXY VIEWER PIX2WORLD WARNING',error)}
        return null;
    }

    const galaxyCatalogPromise=loadCombinedGalaxyCatalog();
    const moduleLoads=Promise.all([
        loadScript(HAMBURGER_URL,'gvHamburger0002'),
        loadScript(COORDINATE_URL,'gvCoordinate0004'),
        loadScript(TARGET_URL,'gvTarget0001'),
        loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0031')
    ]);
    const root=document.getElementById('aladin-cosmic-command-test');
    if(!root)throw new Error('GALAXY VIEWER ROOT MISSING');
    const startupWait=document.getElementById('gv-startup-wait');
    document.dispatchEvent(new CustomEvent('gv-viewer-startup-visible',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:performance.now()-startupTiming.startedAt}}));

    const A=await ensureAladin();
    await A.init;

    const aladin=A.aladin('#aladin-cosmic-command-test',{
        target:`${HOME.ra} ${HOME.dec}`,
        survey:'P/DSS2/color',
        fov:360,
        projection:'MOL',
        cooFrame:'galactic',
        showReticle:false,
        showZoomControl:false,
        showFullscreenControl:false,
        showLayersControl:false,
        showGotoControl:false,
        showCooGridControl:false,
        showSettingsControl:false,
        showSelectionModeControl:false,
        showColorPickerControl:false,
        showShareControl:false,
        showSimbadPointerControl:true,
        showProjectionControl:false,
        showStatusBar:false,
        showFrame:false,
        showFov:false,
        showCooLocation:false,
        showContextMenu:false,
        showCatalog:false,
        showCooGrid:false
    });
    if(typeof aladin.setFrame==='function')aladin.setFrame('galactic');
    if(typeof aladin.setRotation==='function')aladin.setRotation(0);
    if(typeof aladin.gotoRaDec==='function')aladin.gotoRaDec(HOME.ra,HOME.dec);
    if(typeof aladin.setFov==='function')aladin.setFov(360);
    window.aladin_cosmic_command_test=aladin;

    const hamburgerHost=createHost(root,'gv-hamburger-host');
    const coordinateHost=createHost(root,'gv-coordinate-host');
    const targetHost=createHost(root,'gv-target-host');
    const randomGalaxyHost=createHost(root,'gv-random-galaxy-host');
    const reticle=createCenterReticle(root);
    const bottom=createBottomControls(root);
    const universeContext=createUniverseContext(root);
    const homeOverlay=createHomeOverlay(root);
    startupWait?.remove();
    startupTiming.shellReadyAt=performance.now();
    document.dispatchEvent(new CustomEvent('gv-viewer-shell-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,elapsedMs:startupTiming.shellReadyAt-startupTiming.startedAt}}));

    galaxyCatalog=await galaxyCatalogPromise;
    startupTiming.catalogReadyAt=performance.now();
    await moduleLoads;

    if(window.GalaxyViewerHamburgerMenu?.version!=='0002')throw new Error('HAMBURGER MODULE 0002 EXPORT MISSING');
    const hamburger=window.GalaxyViewerHamburgerMenu.init({
        host:hamburgerHost,
        onProjectionSelected(name,detail){
            try{
                if(typeof aladin.setProjection!=='function')throw new Error('ALADIN setProjection IS UNAVAILABLE');
                aladin.setProjection(detail.code);
            }catch(error){console.error('GALAXY VIEWER PROJECTION FAILURE',name,detail?.code,error)}
        }
    });
    hamburger.root.style.position='absolute';
    hamburger.root.style.inset='0';
    hamburger.root.style.width='100%';
    hamburger.root.style.height='100%';
    hamburger.root.style.pointerEvents='none';
    hamburger.menuButton.style.pointerEvents='auto';

    if(window.GalaxyCoordinateOverlay?.VERSION!=='0003')throw new Error('COORDINATE MODULE 0004 PATH / 0003 VERIFIED CORE EXPORT MISSING');
    let frame='GAL',latestRa=HOME.ra,latestDec=HOME.dec;
    let coordinate=null;
    function renderCoordinates(){
        if(!coordinate)return;
        const shown=frame==='GAL'?equatorialToGalactic(latestRa,latestDec):[latestRa,latestDec];
        coordinate.setFrame(frame);
        coordinate.update(shown[0],shown[1]);
    }
    coordinate=window.GalaxyCoordinateOverlay.mount(coordinateHost,{onFrameChange(nextFrame){
        frame=nextFrame;
        try{if(typeof aladin.setFrame==='function')aladin.setFrame(frame==='GAL'?'galactic':'ICRSd')}catch(error){console.warn('GALAXY VIEWER FRAME CHANGE WARNING',error)}
        renderCoordinates();
    }});
    await coordinate.ready;

    const navInstrumentToggles=document.createElement('div');
    navInstrumentToggles.id='gv-nav-instrument-toggles';

    const northToggle=document.createElement('button');
    northToggle.type='button';
    northToggle.className='gv-nav-instrument-toggle';
    northToggle.textContent='N';
    northToggle.setAttribute('aria-label','TOGGLE NORTH POINTER');
    northToggle.setAttribute('aria-pressed','true');

    const earthToggle=document.createElement('button');
    earthToggle.type='button';
    earthToggle.className='gv-nav-instrument-toggle';
    earthToggle.textContent='E';
    earthToggle.setAttribute('aria-label','TOGGLE EARTH POINTER');
    earthToggle.setAttribute('aria-pressed','true');

    navInstrumentToggles.append(northToggle,earthToggle);
    root.appendChild(navInstrumentToggles);

    const navInstruments=document.createElement('div');
    navInstruments.id='gv-nav-instruments';

    const northMarker=document.createElement('div');
    northMarker.id='gv-north-marker';
    northMarker.className='gv-nav-marker';
    northMarker.innerHTML='<span class="gv-nav-marker-pointer"></span><span class="gv-nav-marker-label">N</span>';

    const earthMarker=document.createElement('div');
    earthMarker.id='gv-earth-marker';
    earthMarker.className='gv-nav-marker';
    earthMarker.innerHTML='<span class="gv-nav-marker-pointer"></span><span class="gv-nav-marker-label">EARTH<span id="gv-earth-distance">0 LY</span></span>';

    navInstruments.append(northMarker,earthMarker);
    root.appendChild(navInstruments);

    const coordinateNorthPulse=document.createElement('div');
    coordinateNorthPulse.id='gv-coordinate-north-pulse';
    root.appendChild(coordinateNorthPulse);

    let northPointerEnabled=true;
    let earthPointerEnabled=true;

    function compactEarthDistance(millionLy){
        const value=Number(millionLy);
        if(!Number.isFinite(value)||value<=0)return '0 LY';
        if(value>=1000)return `${(value/1000).toFixed(1)} BLY`;
        if(value>=1)return `${value.toFixed(value>=100?0:1)} MLY`;
        const thousand=value*1000;
        return `${thousand.toFixed(thousand>=100?0:1)} KLY`;
    }

    function projectSkyPoint(ra,dec){
        if(typeof aladin.world2pix!=='function')return null;
        try{
            const value=aladin.world2pix(Number(ra),Number(dec));
            const x=Number(value?.[0]),y=Number(value?.[1]);
            return Number.isFinite(x)&&Number.isFinite(y)?[x,y]:null;
        }catch(_){return null}
    }

    function screenDirectionTo(ra,dec){
        const canvas=root.querySelector('canvas');
        if(!canvas)return null;
        const center=projectSkyPoint(latestRa,latestDec);
        const target=projectSkyPoint(ra,dec);
        if(!center||!target)return null;
        const dx=target[0]-center[0],dy=target[1]-center[1];
        const length=Math.hypot(dx,dy);
        if(!(length>0.0001))return null;
        return {x:dx/length,y:dy/length};
    }

    function northScreenDirection(){
        const step=Math.max(.05,Math.min(1,Math.abs(89.8-latestDec)));
        const northDec=Math.min(89.8,latestDec+step);
        return screenDirectionTo(latestRa,northDec);
    }

    function placeNavigationMarker(marker,direction,radiusFraction,labelInset){
        if(!marker||!direction)return false;
        const rect=root.getBoundingClientRect();
        if(!rect.width||!rect.height)return false;
        const radius=Math.min(rect.width,rect.height)*radiusFraction;
        const x=rect.width/2+direction.x*radius;
        const y=rect.height/2+direction.y*radius;
        const angle=Math.atan2(direction.y,direction.x)*180/Math.PI+90;
        marker.style.left=`${x}px`;
        marker.style.top=`${y}px`;
        const pointer=marker.querySelector('.gv-nav-marker-pointer');
        if(pointer)pointer.style.transform=`rotate(${angle}deg)`;
        const label=marker.querySelector('.gv-nav-marker-label');
        if(label){
            label.style.left=`${-direction.x*labelInset}px`;
            label.style.top=`${-direction.y*labelInset}px`;
            label.style.transform='translate(-50%,-50%)';
        }
        return true;
    }

    function positionCoordinateNorthPulse(direction){
        if(!direction||!coordinateNorthPulse)return;
        const width=290,height=36;
        const cx=width/2,cy=height/2;
        const tx=Math.abs(direction.x)>0.0001?cx/Math.abs(direction.x):Infinity;
        const ty=Math.abs(direction.y)>0.0001?cy/Math.abs(direction.y):Infinity;
        const t=Math.min(tx,ty);
        const x=cx+direction.x*t;
        const y=cy+direction.y*t;
        const edgeHorizontal=Math.abs(y)<=1||Math.abs(y-height)<=1;
        coordinateNorthPulse.style.setProperty('--gv-north-pulse-x',`${x}px`);
        coordinateNorthPulse.style.setProperty('--gv-north-pulse-y',`${y}px`);
        coordinateNorthPulse.style.setProperty('--gv-north-pulse-angle',edgeHorizontal?'0deg':'90deg');
    }

    function updateNavigationInstruments(){
        const hdOpen=Boolean(window.GalaxyViewerRandomGalaxy?.getState?.().hdOpen);
        if(hdOpen){
            northMarker.classList.remove('gv-visible');
            earthMarker.classList.remove('gv-visible');
            coordinateNorthPulse.style.display='none';
            return;
        }

        const northDirection=northScreenDirection();
        if(northDirection){
            positionCoordinateNorthPulse(northDirection);
            coordinateNorthPulse.style.display=northPointerEnabled?'block':'none';
            if(northPointerEnabled&&placeNavigationMarker(northMarker,northDirection,.30,30))northMarker.classList.add('gv-visible');
            else northMarker.classList.remove('gv-visible');
        }else{
            northMarker.classList.remove('gv-visible');
            coordinateNorthPulse.style.display='none';
        }

        const earthDirection=screenDirectionTo(HOME.ra,HOME.dec);
        const state=window.GalaxyViewerRandomGalaxy?.getState?.()||{};
        const current=state.activeDestination||state.currentGalaxy||null;
        const earthDistance=document.getElementById('gv-earth-distance');
        if(earthDistance)earthDistance.textContent=compactEarthDistance(current?.distance);
        if(earthPointerEnabled&&earthDirection&&placeNavigationMarker(earthMarker,earthDirection,.40,42))earthMarker.classList.add('gv-visible');
        else earthMarker.classList.remove('gv-visible');
    }

    northToggle.addEventListener('click',()=>{
        northPointerEnabled=!northPointerEnabled;
        northToggle.setAttribute('aria-pressed',String(northPointerEnabled));
        updateNavigationInstruments();
    });

    earthToggle.addEventListener('click',()=>{
        earthPointerEnabled=!earthPointerEnabled;
        earthToggle.setAttribute('aria-pressed',String(earthPointerEnabled));
        updateNavigationInstruments();
    });

    const initialCoordinates=readCurrentRaDec(aladin,root);
    if(initialCoordinates){latestRa=initialCoordinates[0];latestDec=initialCoordinates[1];renderCoordinates();updateNavigationInstruments()}
    let lastRa=NaN,lastDec=NaN;
    const coordinateTimer=setInterval(()=>{
        const value=readCurrentRaDec(aladin,root);
        if(!value)return;
        const ra=value[0],dec=value[1];
        if(ra===lastRa&&dec===lastDec)return;
        lastRa=ra;lastDec=dec;latestRa=ra;latestDec=dec;renderCoordinates();updateNavigationInstruments();
    },100);
    window.addEventListener('beforeunload',()=>clearInterval(coordinateTimer),{once:true});

    if(window.GalaxyViewerTargetSimbad?.version!=='0001')throw new Error('TARGET / SIMBAD MODULE 0001 EXPORT MISSING');
    const target=window.GalaxyViewerTargetSimbad.init({host:targetHost,aladin,viewerRoot:root});
    const targetButtonIcon=target.button?.querySelector('img');
    if(targetButtonIcon)targetButtonIcon.src=TARGET_ICON_URL;

    if(window.GalaxyRandomGalaxy?.VERSION!=='0031')throw new Error('RANDOM GALAXY 0031 EXPORT MISSING OR VERSION MISMATCH');
    function historySnapshot(destination){
        const {preparedHdUrl,preparedSource,preparedHdImage,...snapshot}=destination||{};
        return Object.freeze({...snapshot});
    }
    function setHistoryControls(){
        const busy=navigationPending||Boolean(window.GalaxyViewerRandomGalaxy?.getState?.().busy);
        bottom.back.disabled=busy||galaxyHistoryIndex<=0;
        bottom.forward.disabled=busy||galaxyHistoryIndex<0||galaxyHistoryIndex>=galaxyHistory.length-1;
    }
    function recordArrival(destination){
        if(Number.isInteger(pendingHistoryIndex)){
            galaxyHistoryIndex=pendingHistoryIndex;
            pendingHistoryIndex=null;
        }else{
            if(galaxyHistoryIndex<galaxyHistory.length-1)galaxyHistory.splice(galaxyHistoryIndex+1);
            galaxyHistory.push(historySnapshot(destination));
            galaxyHistoryIndex=galaxyHistory.length-1;
        }
    }
    function navigateHistory(index){
        if(index<0||index>=galaxyHistory.length||navigationPending||randomGalaxy.getState().busy)return;
        suspendBackgroundWork();
        suspendArchivePreloads();
        releaseActiveArchivePreload();
        forcedDestination=galaxyHistory[index];
        pendingHistoryIndex=index;
        navigationPending=true;
        homeOverlay.classList.add('gv-hidden');universeContext.classList.add('gv-hidden');setHistoryControls();
        randomGalaxy.travelToRandom().catch(error=>{
            forcedDestination=null;pendingHistoryIndex=null;navigationPending=false;resumeBackgroundWork();resumeArchivePreloads();endTravelHud();setHistoryControls();console.error('GALAXY VIEWER HISTORY NAVIGATION FAILURE',error);
        });
    }

    const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomGalaxyHost,{
        aladin,
        randomButton:bottom.random,
        bindClick:false,
        prefetch:false,
        hubbleProvider:randomHubbleProvider,
        currentGalaxy:HOME,
        catalogCount:catalogRecordCount,
        travelSeconds:TRAVEL_SECONDS,
        onArrival(destination){
            navigationPending=false;
            endTravelHud();
            recordArrival(destination);
            syncHdProviderPresentation(destination);
            setHistoryControls();
            resumeBackgroundWork();
            preloadArchiveSource(destination);
            resumeArchivePreloads();
            requestAnimationFrame(()=>checkAndRecoverStaleAladin('random-arrival'));
        },
        onError(error){
            navigationPending=false;pendingHistoryIndex=null;forcedDestination=null;endTravelHud();setHistoryControls();resumeBackgroundWork();resumeArchivePreloads();console.error('GALAXY VIEWER RANDOM GALAXY FAILURE',error);
        }
    });
    window.GalaxyViewerRandomGalaxy=randomGalaxy;
    await randomGalaxy.ready;
    startupTiming.randomReadyAt=performance.now();
    bottom.random.disabled=false;
    fillPrefetchQueue();
    const launchRandomGalaxy=()=>{
        if(navigationPending||randomGalaxy.getState().busy)return;
        suspendBackgroundWork();
        suspendArchivePreloads();
        navigationPending=true;
        setHistoryControls();

        randomGalaxy.travelToRandom().then(destination=>{
            if(destination){
                const hud=document.getElementById('gv-travel-hud');
                if(!hud)console.error('GALAXY VIEWER TRAVEL HUD MISSING');
            }
        }).catch(error=>{
            navigationPending=false;
            pendingHistoryIndex=null;
            forcedDestination=null;
            endTravelHud();
            setHistoryControls();
            resumeBackgroundWork();
            resumeArchivePreloads();
            console.error('GALAXY VIEWER RANDOM GALAXY CLICK FAILURE',error);
        });
    };
    bottom.random.addEventListener('click',launchRandomGalaxy);


    // 10N HD presentation: exact scope is archive/source controls + Galaxy Info + BACK TO SKY.
    const presentationStyle=document.createElement('style');
    presentationStyle.textContent='#gv-random-galaxy{border:2px solid #ABB3AA!important;box-shadow:none!important;filter:brightness(1.10)}.gv-galaxy-history{border:2px solid #ABB3AA!important;box-shadow:none!important;filter:brightness(1.10);opacity:1!important}.gvrg-hd-science,.gvrg-hd-viewport,#gv-hd-info-panel{box-sizing:border-box!important;width:min(680px,calc(100vw - 20px))!important;border:1px solid #78FFAB!important;border-radius:8px!important}.gvrg-hd-science,#gv-hd-info-panel{background:transparent!important;box-shadow:none!important}.gvrg-hd-science{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;overflow:hidden!important;pointer-events:none!important}.gvrg-hd-science .gvrg-hd-science-value{font-size:10.5px!important}.gvrg-hd-viewport{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;aspect-ratio:auto!important;overflow:hidden!important;background:#020B07!important;box-shadow:inset 0 0 6px rgba(120,255,171,.10),0 0 8px rgba(87,255,147,.22)!important;pointer-events:auto!important}.gvrg-hd-viewport>img:not(#gv-hd-archive-button img){width:100%!important;height:100%!important;max-width:none!important;max-height:none!important;object-fit:contain!important;object-position:50% 50%;scale:1!important}.gvrg-hd-scale,.gvrg-hd-scale-label{font-size:13.5px!important}#gv-hd-info-panel{position:absolute;left:50%;z-index:4;transform:translateX(-50%);padding:9px 11px 10px;color:#DFFFEA;font:400 10.5px/1.45 "Space Age",sans-serif;letter-spacing:.42px;text-align:left;text-shadow:0 0 4px rgba(87,255,147,.22);display:flex;flex-direction:column;overflow:hidden;pointer-events:none}#gv-hd-info-title{flex:0 0 auto;margin-bottom:6px;color:#78FFAB;font-size:12px;letter-spacing:.75px;text-align:center}#gv-hd-info-body{flex:1 1 auto;min-height:0;overflow:hidden;overflow-wrap:anywhere}.gvrg-credit{display:none!important}#gv-hd-control-row{position:absolute!important;left:11px!important;right:11px!important;bottom:10px!important;z-index:30!important;height:40px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;box-sizing:border-box!important;pointer-events:none!important}#gv-hd-control-row>.gvrg-back-button,#gv-hd-control-row>#gv-hd-download-button{position:static!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;flex:1 1 0!important;width:0!important;min-width:0!important;max-width:none!important;height:40px!important;min-height:40px!important;margin:0!important;padding:0 8px!important;gap:7px!important;box-sizing:border-box!important;align-items:center!important;justify-content:center!important;white-space:nowrap!important;overflow:hidden!important;font-size:10.5px!important;line-height:1!important;pointer-events:auto!important;touch-action:manipulation!important}#gv-hd-control-row>.gvrg-back-button>span:last-child,#gv-hd-control-row>#gv-hd-download-button>span:last-child{min-width:0!important;white-space:nowrap!important;overflow:visible!important;line-height:1!important}#gv-hd-control-row .gvrg-back-chevron,#gv-hd-control-row .gvrg-download-icon{width:18px!important;height:18px!important;flex:0 0 18px!important}#gv-hd-archive-button{position:absolute!important;right:14px!important;bottom:14px!important;z-index:40!important;width:36px!important;height:36px!important;margin:0!important;padding:2px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;box-sizing:content-box!important;border:2px solid #78FFAB!important;border-radius:5px!important;background:linear-gradient(145deg,rgba(18,105,65,.96),rgba(31,176,96,.94))!important;box-shadow:none!important;filter:none!important;overflow:visible!important;pointer-events:auto!important;touch-action:manipulation!important}#gv-hd-archive-button img{display:block!important;width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;margin:0!important;padding:0!important;border:0!important;border-radius:3px!important;background:transparent!important;box-shadow:none!important}#gv-hd-archive-button .gv-hd-archive-comet{position:absolute;inset:4px;border-radius:50%;opacity:0;pointer-events:none;transform-origin:50% 50%}#gv-hd-archive-button .gv-hd-archive-comet::before{content:"";position:absolute;left:50%;top:-1px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#F8FFFF;box-shadow:0 0 4px #FFFFFF,0 0 8px #8FE5FF,0 0 12px #296DBD}#gv-hd-archive-button .gv-hd-archive-comet::after{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 250deg,rgba(15,54,122,0) 0deg,rgba(91,184,255,.22) 42deg,rgba(143,229,255,.56) 82deg,rgba(248,255,255,.92) 110deg,transparent 111deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));filter:drop-shadow(0 0 2px rgba(143,229,255,.72))}#gv-hd-archive-button.gv-archive-loading .gv-hd-archive-comet{opacity:1;animation:gvHdArchiveOrbit 1s linear infinite}@keyframes gvHdArchiveOrbit{to{transform:rotate(360deg)}}#gv-hd-download-button{border:2px solid #7CCBFF!important;border-radius:6px!important;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98))!important;color:#EAF8FF!important;box-shadow:none!important;filter:none!important}#gv-hd-download-button *{color:#EAF8FF!important;fill:#EAF8FF!important;stroke:#EAF8FF!important}#gv-hd-download-button .gvrg-download-icon{filter:drop-shadow(0 0 3px rgba(225,248,255,.92))!important}#gv-hd-download-button .gvrg-download-arrow{top:1px!important;width:3px!important;height:10px!important;background:#F7FDFF!important;border-radius:1px!important;box-shadow:0 0 3px rgba(225,248,255,.88)!important}#gv-hd-download-button .gvrg-download-arrow::after{bottom:-1px!important;width:8px!important;height:8px!important;border-right:3px solid #EAF8FF!important;border-bottom:3px solid #EAF8FF!important}#gv-hd-download-button .gvrg-download-bar{width:14px!important;height:3px!important;background:#F7FDFF!important;box-shadow:0 0 4px rgba(225,248,255,.92)!important}#gv-archive-overlay{position:fixed;inset:0;z-index:2147483000;background:#000;display:block;visibility:hidden;opacity:0;pointer-events:none}#gv-archive-overlay.gv-open{visibility:visible;opacity:1;pointer-events:auto}#gv-archive-frame{position:absolute;inset:0;width:100%;height:100%;border:0;background:#000}#gv-archive-back{position:fixed;left:50%;bottom:max(18px,env(safe-area-inset-bottom));z-index:2147483647;transform:translateX(-50%);display:inline-flex;align-items:center;justify-content:center;gap:10px;height:48px;padding:0 12px;border:2px solid #ABB3AA;border-radius:7px;background:linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98));color:#E8FFF0;font:400 13px/1 "Space Age",sans-serif;letter-spacing:.55px;text-transform:uppercase;white-space:nowrap;box-shadow:0 0 12px rgba(0,0,0,.75);pointer-events:auto;touch-action:manipulation;cursor:pointer}#gv-archive-arrow{position:relative;display:inline-flex;width:36px;height:36px;flex:0 0 36px;align-items:center;justify-content:center}#gv-archive-arrow::before,#gv-archive-arrow::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;box-sizing:border-box;pointer-events:none}#gv-archive-arrow::before{border-width:6px;border-color:#78FFAB;filter:drop-shadow(0 0 4px rgba(87,255,147,.90));transform:translate(-38%,-50%) rotate(-135deg)}#gv-archive-arrow::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-34%,-50%) rotate(-135deg)}#gv-archive-target-tile{box-sizing:border-box;width:36px;height:36px;flex:0 0 36px;display:inline-flex;align-items:center;justify-content:center;border:2px solid #ABB3AA;border-radius:6px;background:linear-gradient(145deg,rgba(18,105,65,.98),rgba(31,176,96,.98));overflow:hidden}#gv-archive-target-tile img{display:block;width:28px;height:28px;object-fit:contain;flex:0 0 28px;margin:0;padding:0;border:0}';
    document.head.appendChild(presentationStyle);

    const hdScience=randomGalaxy.hdScience;
    if(hdScience){
        const scienceItems=[...hdScience.querySelectorAll('.gvrg-hd-science-item')];
        const constellationItems=scienceItems.filter(item=>String(item.querySelector('.gvrg-hd-science-label')?.textContent||'').trim().toUpperCase()==='CONST');
        let constellationItem=constellationItems.shift()||null;
        constellationItems.forEach(item=>item.remove());
        let constellationValue=null;
        if(!constellationItem){
            constellationItem=document.createElement('div');
            constellationItem.className='gvrg-hd-science-item';
            const key=document.createElement('div');
            key.className='gvrg-hd-science-label';
            key.textContent='CONST';
            constellationValue=document.createElement('div');
            constellationValue.className='gvrg-hd-science-value';
            constellationItem.append(key,constellationValue);
            const ageItem=scienceItems.find(item=>String(item.querySelector('.gvrg-hd-science-label')?.textContent||'').trim().toUpperCase()==='AGE');
            hdScience.insertBefore(constellationItem,ageItem||null);
        }else{
            constellationValue=constellationItem.querySelector('.gvrg-hd-science-value');
        }
        const syncHdConst=()=>{
            if(constellationValue)constellationValue.textContent=String(randomGalaxy.activeDestination?.constellation||randomGalaxy.constellationValueEl?.textContent||'').trim().toUpperCase();
        };
        if(randomGalaxy.constellationValueEl)new MutationObserver(syncHdConst).observe(randomGalaxy.constellationValueEl,{childList:true,subtree:true,characterData:true});
        randomGalaxy.viewHdButton?.addEventListener('click',syncHdConst,true);
        randomGalaxy.hubbleIconButton?.addEventListener('click',syncHdConst,true);
        syncHdConst();
    }

    const hdDownloadButton=randomGalaxy.downloadButton||null;

    const hdInfoPanel=document.createElement('div');
    hdInfoPanel.id='gv-hd-info-panel';
    hdInfoPanel.innerHTML='<div id="gv-hd-info-title">GALAXY INFO</div><div id="gv-hd-info-body"></div><div id="gv-hd-control-row"></div>';
    randomGalaxy.hdOverlay?.appendChild(hdInfoPanel);
    const hdInfoBody=hdInfoPanel.querySelector('#gv-hd-info-body');
    const hdControlRow=hdInfoPanel.querySelector('#gv-hd-control-row');
    const hdBackToSky=randomGalaxy.backButton;
    if(hdBackToSky){
        // Preserve the established denomination exactly: BACK TO SKY.
        const backLabel=hdBackToSky.lastElementChild;
        if(backLabel)backLabel.textContent='BACK TO SKY';
        else hdBackToSky.textContent='BACK TO SKY';
        hdBackToSky.setAttribute('aria-label','BACK TO SKY');
        hdControlRow.appendChild(hdBackToSky);
    }
    function restoreAfterHdClose(attempt=0){
        if(isHdPresentationActive()){
            if(attempt<60)requestAnimationFrame(()=>restoreAfterHdClose(attempt+1));
            return;
        }
        restoreNormalViewerPresentation();
        requestAnimationFrame(()=>checkAndRecoverStaleAladin('back-to-sky'));
    }
    if(hdBackToSky)hdBackToSky.addEventListener('click',()=>requestAnimationFrame(()=>restoreAfterHdClose()),true);
    if(hdDownloadButton){
        hdDownloadButton.id='gv-hd-download-button';
        hdDownloadButton.setAttribute('aria-label','DOWNLOAD HD IMAGE');
        hdDownloadButton.setAttribute('title','DOWNLOAD HD IMAGE');
        hdControlRow.appendChild(hdDownloadButton);
    }
    if(randomGalaxy.creditEl)randomGalaxy.creditEl.remove();

    const hdArchiveButton=document.createElement('button');
    hdArchiveButton.id='gv-hd-archive-button';
    hdArchiveButton.type='button';
    hdArchiveButton.setAttribute('aria-label','OPEN ARCHIVE SOURCE');
    const hdArchiveIcon=document.createElement('img');
    hdArchiveIcon.alt='ARCHIVE SOURCE';
    const hdArchiveComet=document.createElement('span');
    hdArchiveComet.className='gv-hd-archive-comet';
    hdArchiveComet.setAttribute('aria-hidden','true');
    hdArchiveButton.append(hdArchiveIcon,hdArchiveComet);
    randomGalaxy.hdViewport?.appendChild(hdArchiveButton);
    hdArchiveButton.addEventListener('pointerdown',event=>event.stopPropagation(),true);
    hdArchiveButton.addEventListener('pointerup',event=>event.stopPropagation(),true);

    const archiveOverlay=document.createElement('div');
    archiveOverlay.id='gv-archive-overlay';
    let archiveFrame=document.createElement('iframe');
    archiveFrame.id='gv-archive-frame';
    archiveFrame.title='GALAXY ARCHIVE SOURCE';
    const archiveBack=document.createElement('button');
    archiveBack.id='gv-archive-back';
    archiveBack.type='button';
    const archiveArrow=document.createElement('span');
    archiveArrow.id='gv-archive-arrow';
    archiveArrow.setAttribute('aria-hidden','true');
    const archiveTargetTile=document.createElement('span');
    archiveTargetTile.id='gv-archive-target-tile';
    archiveTargetTile.setAttribute('aria-hidden','true');
    const archiveTarget=document.createElement('img');
    archiveTarget.src=TARGET_ICON_URL;
    archiveTarget.alt='';
    archiveTarget.setAttribute('aria-hidden','true');
    archiveTargetTile.appendChild(archiveTarget);
    const archiveBackLabel=document.createElement('span');
    archiveBackLabel.textContent='BACK TO GALAXY VIEWER';
    archiveBack.append(archiveArrow,archiveBackLabel,archiveTargetTile);
    archiveBack.setAttribute('aria-label','BACK TO GALAXY VIEWER');
    archiveOverlay.append(archiveFrame,archiveBack);
    document.body.appendChild(archiveOverlay);
    let archiveSourceUrl='';
    let archiveLoadedUrl='';
    let archiveOpenRequested=false;
    let archiveClosing=false;
    let archiveLaunchReadyAt=0;
    let archiveRevealTimer=0;
    const archivePreloadQueue=[];
    let archivePreloadSuspended=false;
    let archivePreloadLoadingItem=null;
    let archivePreloadController=null;
    let activeArchivePreloadItem=null;
    const archivePreloadFailedKeys=new Set();
    const setArchiveLoading=loading=>{
        hdArchiveButton.classList.toggle('gv-archive-loading',loading);
    };
    const loadArchiveFrameSource=sourceUrl=>{
        archiveFrame.src=sourceUrl;
    };
    const releaseActiveArchivePreload=()=>{
        activeArchivePreloadItem=null;
        archiveSourceUrl='';
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        try{archiveFrame.src='about:blank'}catch(_){}
    };
    const revealArchiveWhenReady=()=>{
        if(!archiveOpenRequested||archiveClosing||!archiveSourceUrl)return;
        const remaining=Math.max(0,archiveLaunchReadyAt-performance.now());
        if(remaining>0){
            clearTimeout(archiveRevealTimer);
            archiveRevealTimer=setTimeout(revealArchiveWhenReady,remaining);
            return;
        }
        archiveRevealTimer=0;
        setArchiveLoading(false);
        archiveOverlay.removeAttribute('aria-hidden');
        archiveOverlay.style.pointerEvents='auto';
        archiveOverlay.classList.add('gv-open');
        archiveFrame.style.pointerEvents='auto';
    };
    const archiveQueueKey=destination=>destinationKey(destination);
    const chooseArchivePreloadDestination=()=>{
        const excluded=new Set([activeTargetKey,...archivePreloadQueue.map(item=>item.key),activeArchivePreloadItem?.key,...archivePreloadFailedKeys].filter(Boolean));
        const prepared=prefetchReady.find(item=>{
            const destination=item?.destination;
            const key=item?.key||archiveQueueKey(destination);
            const sourceUrl=String(destination?.sourceUrl||'').trim();
            return key&&!excluded.has(key)&&/^https:\/\//i.test(sourceUrl);
        });
        return prepared?.destination||null;
    };
    const startNextArchivePreload=()=>{
        if(archivePreloadSuspended||backgroundWorkSuspended||navigationPending||archivePreloadLoadingItem)return;
        if(archivePreloadQueue.filter(item=>item.state==='ready').length>=ARCHIVE_PRELOAD_TARGET)return;
        let item=archivePreloadQueue.find(candidate=>candidate.state==='pending');
        if(!item){
            const destination=chooseArchivePreloadDestination();
            if(!destination)return;
            item={key:archiveQueueKey(destination),destination,sourceUrl:String(destination.sourceUrl||'').trim(),state:'pending'};
            archivePreloadQueue.push(item);
        }
        archivePreloadLoadingItem=item;
        item.state='loading';
        const controller=new AbortController();
        archivePreloadController=controller;
        fetch(item.sourceUrl,{mode:'no-cors',cache:'force-cache',credentials:'omit',signal:controller.signal,priority:'low'})
            .then(()=>{
                if(archivePreloadLoadingItem!==item)return;
                item.state='ready';
                item.loadedAt=performance.now();
            })
            .catch(error=>{
                if(error?.name==='AbortError'){
                    if(archivePreloadQueue.includes(item))item.state='pending';
                    return;
                }
                archivePreloadFailedKeys.add(item.key);
                const index=archivePreloadQueue.indexOf(item);
                if(index>=0)archivePreloadQueue.splice(index,1);
            })
            .finally(()=>{
                if(archivePreloadLoadingItem===item)archivePreloadLoadingItem=null;
                if(archivePreloadController===controller)archivePreloadController=null;
                if(!archivePreloadSuspended&&!backgroundWorkSuspended&&!navigationPending)queueMicrotask(ensureArchivePreloadQueue);
            });
    };
    ensureArchivePreloadQueue=()=>{
        if(archivePreloadSuspended||backgroundWorkSuspended||navigationPending)return;
        while(archivePreloadQueue.length<ARCHIVE_PRELOAD_TARGET){
            const destination=chooseArchivePreloadDestination();
            if(!destination)break;
            archivePreloadQueue.push({key:archiveQueueKey(destination),destination,sourceUrl:String(destination.sourceUrl||'').trim(),state:'pending'});
        }
        startNextArchivePreload();
    };
    const suspendArchivePreloads=()=>{
        archivePreloadSuspended=true;
        const item=archivePreloadLoadingItem;
        archivePreloadLoadingItem=null;
        if(item&&archivePreloadQueue.includes(item)&&item.state==='loading')item.state='pending';
        if(archivePreloadController){try{archivePreloadController.abort()}catch(_){};archivePreloadController=null}
    };
    const resumeArchivePreloads=()=>{
        if(navigationPending)return;
        archivePreloadSuspended=false;
        queueMicrotask(ensureArchivePreloadQueue);
    };
    const consumeArchivePreloadedDestination=excludeName=>{
        const excluded=String(excludeName||'').trim().toLowerCase();
        const index=archivePreloadQueue.findIndex(item=>item.state==='ready'&&String(item.destination?.name||'').trim().toLowerCase()!==excluded);
        if(index<0)return null;
        return archivePreloadQueue.splice(index,1)[0];
    };
    const bindActiveArchivePreload=(item,destination)=>{
        if(!item)return;
        activeArchivePreloadItem=item;
        activeArchivePreloadItem.destination=destination;
        archiveSourceUrl='';
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        archiveClosing=false;
    };
    const preloadArchiveSource=destination=>{
        if(navigationPending||backgroundWorkSuspended)return;
        const sourceUrl=String(destination?.sourceUrl||'').trim();
        if(!/^https:\/\//i.test(sourceUrl)||archiveSourceUrl===sourceUrl)return;
        archiveSourceUrl=sourceUrl;
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        archiveClosing=false;
        archiveOverlay.classList.remove('gv-open');
        archiveOverlay.style.pointerEvents='none';
        archiveOverlay.setAttribute('aria-hidden','true');
        archiveFrame.style.pointerEvents='none';
        loadArchiveFrameSource(sourceUrl);
    };
    const consumeArchiveBackEvent=event=>{
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
    };
    const closeArchiveOverlay=()=>{
        if(archiveClosing)return;
        archiveClosing=true;
        setArchiveLoading(false);
        archiveOverlay.classList.remove('gv-open');
        archiveOverlay.style.pointerEvents='none';
        archiveOverlay.setAttribute('aria-hidden','true');
        archiveFrame.style.pointerEvents='none';
        archiveFrame.blur();
        archiveOpenRequested=false;
        archiveLaunchReadyAt=0;
        clearTimeout(archiveRevealTimer);
        archiveRevealTimer=0;
        archiveClosing=false;
        requestAnimationFrame(()=>{if(isHdPresentationActive())try{hdArchiveButton.focus({preventScroll:true})}catch(_){}});
    };
    archiveBack.addEventListener('pointerdown',consumeArchiveBackEvent,true);
    archiveBack.addEventListener('pointerup',consumeArchiveBackEvent,true);
    archiveBack.addEventListener('click',event=>{
        consumeArchiveBackEvent(event);
        closeArchiveOverlay();
        requestAnimationFrame(()=>{
            if(isHdPresentationActive()){
                settleHdPresentation();
            }else{
                restoreNormalViewerPresentation();
            }
            requestAnimationFrame(()=>checkAndRecoverStaleAladin('archive-return'));
        });
    },true);
    archiveFrame.addEventListener('load',()=>{
        if(!archiveSourceUrl||archiveClosing)return;
        archiveLoadedUrl=archiveSourceUrl;
        revealArchiveWhenReady();
    });
    archiveFrame.addEventListener('error',()=>{
        const sourceUrl=archiveSourceUrl;
        const requested=archiveOpenRequested;
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        archiveLaunchReadyAt=0;
        clearTimeout(archiveRevealTimer);
        archiveRevealTimer=0;
        setArchiveLoading(false);
        if(requested&&sourceUrl)window.open(sourceUrl,'_blank','noopener,noreferrer');
    });
    function currentArchiveDestination(){return randomGalaxy.getState?.().activeDestination||randomGalaxy.activeDestination||null}
    function providerFor(destination){return destination?.provider==='CHANDRA'?'CHANDRA':destination?.provider==='JWST'?'JWST':'HUBBLE'}
    hdArchiveButton.addEventListener('click',event=>{
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        const destination=currentArchiveDestination();
        const sourceUrl=String(destination?.sourceUrl||'').trim();
        if(!/^https:\/\//i.test(sourceUrl))return;
        archiveOpenRequested=true;
        archiveClosing=false;
        archiveLaunchReadyAt=performance.now()+1000;
        setArchiveLoading(true);
        if(archiveSourceUrl!==sourceUrl){
            preloadArchiveSource(destination);
            archiveOpenRequested=true;
        }
        revealArchiveWhenReady();
    },true);


    function galaxyInfoText(destination){
        if(!destination)return '';
        const provider=providerFor(destination);
        const telescope=provider==='CHANDRA'?'CHANDRA X-RAY OBSERVATORY':provider==='JWST'?'JAMES WEBB SPACE TELESCOPE':'HUBBLE SPACE TELESCOPE';
        const identity=String(destination.commonName||destination.designation||destination.name||'THIS GALAXY').trim().toUpperCase();
        const parts=[`${identity} — ${telescope} IMAGERY.`];
        if(destination.constellation)parts.push(`CONSTELLATION ${String(destination.constellation).trim().toUpperCase()}.`);
        const distance=Number(destination.distance);
        if(Number.isFinite(distance)&&distance>0)parts.push(`DISTANCE ${distance>=1000?(distance/1000).toFixed(2)+' BILLION':distance.toFixed(distance>=100?0:1)+' MILLION'} LIGHT-YEARS.`);
        if(destination.age)parts.push(`AGE ${String(destination.age).trim().toUpperCase()}.`);
        if(destination.imageType)parts.push(`${String(destination.imageType).trim().toUpperCase()} IMAGE.`);
        return parts.join(' ');
    }

    function renderHdInfoCandidate(words,count){
        hdInfoBody.replaceChildren();
        const bodyRect=hdInfoBody.getBoundingClientRect();
        const style=getComputedStyle(hdInfoBody);
        const font=style.font||`${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
        const measuredLineHeight=parseFloat(style.lineHeight);
        const fontSize=parseFloat(style.fontSize)||10.5;
        const lineHeight=Number.isFinite(measuredLineHeight)?measuredLineHeight:fontSize*1.45;
        const canvas=renderHdInfoCandidate._canvas||(renderHdInfoCandidate._canvas=document.createElement('canvas'));
        const context=canvas.getContext('2d');
        context.font=font;
        const controlRect=hdControlRow.getBoundingClientRect();
        const noWriteGap=14;
        const textBottom=Math.min(bodyRect.bottom,controlRect.top-noWriteGap);
        const sourceWords=count?words.slice(0,count):[];
        const lines=[];
        let index=0;
        const maxLines=Math.max(0,Math.floor((Math.max(0,textBottom-bodyRect.top)+.5)/lineHeight));
        const letterSpacing=parseFloat(style.letterSpacing)||0;
        const measure=value=>context.measureText(value).width+Math.max(0,value.length-1)*letterSpacing;
        for(let lineIndex=0;lineIndex<maxLines&&index<sourceWords.length;lineIndex++){
            const lineTop=bodyRect.top+lineIndex*lineHeight;
            const lineBottom=lineTop+lineHeight;
            if(lineBottom>textBottom+.5)break;
            const leftOffset=0;
            const availableWidth=bodyRect.width;
            if(availableWidth<24)break;
            let text='';
            while(index<sourceWords.length){
                const proposed=text?`${text} ${sourceWords[index]}`:sourceWords[index];
                if(text&&measure(proposed)>availableWidth)break;
                if(!text&&measure(proposed)>availableWidth){
                    text=proposed;
                    index++;
                    break;
                }
                text=proposed;
                index++;
            }
            if(!text)break;
            lines.push({text,width:availableWidth,left:leftOffset});
        }
        const truncated=index<sourceWords.length||count<words.length;
        if(truncated&&lines.length){
            let line=lines[lines.length-1];
            let text=line.text.replace(/\s*…$/,'');
            while(text&&measure(`${text} …`)>line.width)text=text.replace(/\s+\S+$/,'');
            line.text=text?`${text} …`:'…';
        }
        const fragment=document.createDocumentFragment();
        for(const line of lines){
            const row=document.createElement('div');
            row.textContent=line.text;
            Object.assign(row.style,{display:'block',marginLeft:`${line.left}px`,width:`${line.width}px`,height:`${lineHeight}px`,lineHeight:`${lineHeight}px`,whiteSpace:'nowrap',overflow:'hidden'});
            fragment.appendChild(row);
        }
        hdInfoBody.appendChild(fragment);
        return {renderedWords:index,lineCount:lines.length,truncated};
    }

    function fitHdInfoText(destination=currentArchiveDestination()){
        if(!hdInfoBody||!destination)return;
        const words=galaxyInfoText(destination).split(/\s+/).filter(Boolean);
        const metrics=renderHdInfoCandidate(words,words.length);
        hdInfoBody.dataset.fittedCharacters=String(hdInfoBody.textContent.length);
        hdInfoBody.dataset.fittedWords=String(metrics.renderedWords);
    }

    function syncHdProviderPresentation(destination=currentArchiveDestination()){
        if(!destination)return;
        const provider=providerFor(destination);
        const iconUrl=provider==='CHANDRA'?CHANDRA_ICON_URL:provider==='JWST'?JWST_ICON_URL:HUBBLE_ICON_URL;
        if(randomGalaxy.viewHdButton){randomGalaxy.viewHdButton.textContent=`VIEW ${provider} IN HD`;randomGalaxy.viewHdButton.setAttribute('aria-label',`VIEW ${provider} IN HD`)}
        const buttonIcon=randomGalaxy.hubbleIconButton?.querySelector('img');
        if(buttonIcon){buttonIcon.src=iconUrl;buttonIcon.alt=`${provider} ARCHIVE`}
        hdArchiveIcon.src=iconUrl;
        hdArchiveIcon.alt=`${provider} ARCHIVE`;
        hdArchiveButton.setAttribute('aria-label',`OPEN ${provider} ARCHIVE SOURCE`);
        if(randomGalaxy.hdLoading&&provider!=='HUBBLE'&&/HUBBLE/i.test(randomGalaxy.hdLoading.textContent||''))randomGalaxy.hdLoading.textContent=String(randomGalaxy.hdLoading.textContent||'').replace(/HUBBLE/gi,provider);
        fitHdInfoText(destination);
    }

    resumeArchivePreloads();

    function applySmartHdCrop(){
        const image=randomGalaxy.hdImage;
        if(!(image instanceof HTMLImageElement)||!image.complete||!image.naturalWidth)return;
        image.style.objectFit='contain';
        image.style.objectPosition='50% 50%';
    }

    function isHdPresentationActive(){return Boolean(randomGalaxy.getState?.().hdOpen)}

    let viewerHiddenAt=0;
    let lastRenderRecoveryAt=0;
    let renderRecoveryBusy=false;

    function aladinCanvasLooksStale(){
        const canvas=root.querySelector('canvas');
        if(!canvas)return true;
        const rect=canvas.getBoundingClientRect();
        if(!(rect.width>1&&rect.height>1&&canvas.width>1&&canvas.height>1))return true;

        try{
            const sample=document.createElement('canvas');
            sample.width=16;
            sample.height=16;
            const context=sample.getContext('2d',{willReadFrequently:true});
            if(!context)return false;
            context.drawImage(canvas,0,0,16,16);
            const pixels=context.getImageData(0,0,16,16).data;

            let nearWhite=0;
            let sum=0;
            let sumSquares=0;
            let count=0;

            for(let i=0;i<pixels.length;i+=4){
                const r=pixels[i],g=pixels[i+1],b=pixels[i+2],a=pixels[i+3];
                if(a<16)continue;
                const luminance=.2126*r+.7152*g+.0722*b;
                if(r>248&&g>248&&b>248)nearWhite++;
                sum+=luminance;
                sumSquares+=luminance*luminance;
                count++;
            }

            if(count<32)return false;
            const mean=sum/count;
            const variance=Math.max(0,sumSquares/count-mean*mean);
            const whiteFraction=nearWhite/count;

            return whiteFraction>.96&&variance<18;
        }catch(_){
            return false;
        }
    }

    function forceAladinRepaint(){
        const coordinates=readCurrentRaDec(aladin,root);
        const fov=aladin.getFov?.();

        try{window.dispatchEvent(new Event('resize'))}catch(_){}

        requestAnimationFrame(()=>{
            try{
                if(coordinates&&typeof aladin.gotoRaDec==='function')
                    aladin.gotoRaDec(coordinates[0],coordinates[1]);
            }catch(_){}

            try{
                const value=Number(fov?.[0]);
                if(Number.isFinite(value)&&value>0&&typeof aladin.setFov==='function')
                    aladin.setFov(value);
            }catch(_){}

            requestAnimationFrame(()=>{
                reconcileViewerPresentation();
                updateNavigationInstruments();
            });
        });
    }

    function checkAndRecoverStaleAladin(reason=''){
        if(renderRecoveryBusy||isHdPresentationActive())return;
        const now=performance.now();
        if(now-lastRenderRecoveryAt<5000)return;

        if(!aladinCanvasLooksStale())return;

        renderRecoveryBusy=true;

        setTimeout(()=>{
            if(!aladinCanvasLooksStale()){
                renderRecoveryBusy=false;
                return;
            }

            lastRenderRecoveryAt=performance.now();
            console.warn('GALAXY VIEWER ALADIN STALE CANVAS RECOVERY',reason);
            forceAladinRepaint();

            setTimeout(()=>{
                renderRecoveryBusy=false;
            },1200);
        },300);
    }

    function restoreNormalViewerPresentation(){
        bottom.version.style.top='';
        bottom.version.style.bottom='51px';
        if(!archiveOverlay.classList.contains('gv-open')){
            archiveOverlay.style.pointerEvents='none';
            archiveOverlay.setAttribute('aria-hidden','true');
            archiveFrame.style.pointerEvents='none';
        }
        bottom.nav.style.display='flex';
        bottom.random.style.display='flex';
        bottom.back.style.display='flex';
        bottom.forward.style.display='flex';
        bottom.version.style.display='block';
        if(!navigationPending&&!randomGalaxy.getState().busy)
            bottom.random.disabled=false;
        setHistoryControls();
    }

    function positionHdInfoPanel(){
        if(!isHdPresentationActive())return;
        if(!randomGalaxy.hdOverlay||!randomGalaxy.hdViewport||!randomGalaxy.hdScience)return;
        const overlayRect=randomGalaxy.hdOverlay.getBoundingClientRect();
        const navRect=bottom.nav.getBoundingClientRect();
        if(!overlayRect.height||!overlayRect.width)return;
        const safeBottom=Math.min(overlayRect.bottom-HD_LAYOUT.edge,navRect.top-24);
        const available=Math.max(1,safeBottom-overlayRect.top-HD_LAYOUT.edge-HD_LAYOUT.gap*2);
        const bannerTarget=overlayRect.height*HD_LAYOUT.bannerRatio;
        const viewportWidth=Math.min(680,Math.max(1,randomGalaxy.hdViewport.getBoundingClientRect().width||overlayRect.width-20));
        const layoutScale=Math.min(1,available/Math.max(1,bannerTarget+viewportWidth+150));
        const bannerHeight=Math.max(1,Math.floor(bannerTarget*layoutScale));
        const imageHeight=Math.max(1,Math.floor(viewportWidth*layoutScale));
        const scienceTop=HD_LAYOUT.edge;
        const imageTop=scienceTop+bannerHeight+HD_LAYOUT.gap;
        const infoTop=imageTop+imageHeight+HD_LAYOUT.gap;
        const infoHeight=Math.max(150,Math.floor(safeBottom-(overlayRect.top+infoTop)));
        const set=(element,name,value)=>element.style.setProperty(name,value,'important');
        set(randomGalaxy.hdScience,'top',`${scienceTop}px`);set(randomGalaxy.hdScience,'height',`${bannerHeight}px`);set(randomGalaxy.hdScience,'max-height',`${bannerHeight}px`);
        set(randomGalaxy.hdViewport,'top',`${imageTop}px`);set(randomGalaxy.hdViewport,'bottom','auto');set(randomGalaxy.hdViewport,'height',`${imageHeight}px`);set(randomGalaxy.hdViewport,'max-height',`${imageHeight}px`);
        set(hdInfoPanel,'top',`${infoTop}px`);set(hdInfoPanel,'height',`${infoHeight}px`);set(hdInfoPanel,'max-height',`${infoHeight}px`);
        randomGalaxy.hdOverlay.style.pointerEvents='none';
        randomGalaxy.hdViewport.style.pointerEvents='auto';
        hdInfoPanel.style.pointerEvents='none';
        hdControlRow.style.pointerEvents='none';
        hdControlRow.style.display='flex';
        hdControlRow.style.visibility='visible';
        hdControlRow.style.opacity='1';
        hdControlRow.style.zIndex='30';
        if(hdBackToSky){
            hdBackToSky.style.display='flex';
            hdBackToSky.style.visibility='visible';
            hdBackToSky.style.opacity='1';
            hdBackToSky.style.pointerEvents='auto';
            hdBackToSky.disabled=false;
        }
        if(hdDownloadButton){
            hdDownloadButton.style.display='flex';
            hdDownloadButton.style.visibility='visible';
            hdDownloadButton.style.opacity='1';
            hdDownloadButton.style.pointerEvents='auto';
        }
        hdArchiveButton.style.pointerEvents='auto';
        const rootRect=root.getBoundingClientRect();
        const versionTop=Math.ceil(overlayRect.top+infoTop+infoHeight+5-rootRect.top);
        bottom.version.style.bottom='auto';
        bottom.version.style.top=`${versionTop}px`;
        randomGalaxy.hdOverlay.querySelectorAll('button,a').forEach(element=>{element.style.pointerEvents='auto'});
        fitHdInfoText();
    }

    function settleHdPresentation(){
        if(!isHdPresentationActive())return;
        syncHdProviderPresentation();
        applySmartHdCrop();
        positionHdInfoPanel();
        const row=document.getElementById('gv-hd-control-row');
        if(row)row.style.display='flex';
        const image=randomGalaxy.hdImage;
        if(image instanceof HTMLImageElement&&!image.complete)
            image.addEventListener('load',()=>{
                if(!isHdPresentationActive())return;
                applySmartHdCrop();
                positionHdInfoPanel();
                syncHdProviderPresentation();
                if(row)row.style.display='flex';
            },{once:true});
    }

    function reconcileViewerPresentation(){
        if(isHdPresentationActive())settleHdPresentation();
        else restoreNormalViewerPresentation();
    }

    const originalShowHubbleHD=randomGalaxy.showHubbleHD.bind(randomGalaxy);
    randomGalaxy.showHubbleHD=function(){
        const result=originalShowHubbleHD();
        requestAnimationFrame(()=>requestAnimationFrame(settleHdPresentation));
        return result;
    };
    randomGalaxy.viewHdButton?.addEventListener('click',()=>requestAnimationFrame(settleHdPresentation),true);
    randomGalaxy.hubbleIconButton?.addEventListener('click',()=>requestAnimationFrame(settleHdPresentation),true);
    const handleViewerResize=()=>requestAnimationFrame(reconcileViewerPresentation);
    const handleViewerPageShow=()=>requestAnimationFrame(()=>{
        reconcileViewerPresentation();
        checkAndRecoverStaleAladin('pageshow');
    });
    const handleViewerVisibility=()=>{
        if(document.hidden){
            viewerHiddenAt=performance.now();
            return;
        }
        requestAnimationFrame(()=>{
            reconcileViewerPresentation();
            if(!viewerHiddenAt||performance.now()-viewerHiddenAt>=30000)
                checkAndRecoverStaleAladin('visibility-return');
            viewerHiddenAt=0;
        });
    };
    window.addEventListener('resize',handleViewerResize);
    window.addEventListener('pageshow',handleViewerPageShow);
    document.addEventListener('visibilitychange',handleViewerVisibility);
    syncHdProviderPresentation();

    const deferHdUntilPrepared=async event=>{
        const destination=randomGalaxy.getState?.().activeDestination;
        syncHdProviderPresentation(destination);
        const key=destinationKey(destination);
        const pending=Boolean(key&&(prefetchLoading.has(key)||queueHasKey(key)||(priorityPrefetchDestination&&destinationKey(priorityPrefetchDestination)===key)));
        if(!pending)return;
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        try{
            await waitForPreparedKey(key);
            randomGalaxy.showHubbleHD();
        }catch(error){
            console.error('GALAXY VIEWER ARCHIVE PREPARATION WAIT FAILURE',error);
            try{randomGalaxy.showHubbleHD()}catch(fallbackError){console.error('GALAXY VIEWER ARCHIVE FALLBACK FAILURE',fallbackError)}
        }
    };

    window.addEventListener('beforeunload',()=>{
        for(const controller of prefetchControllers.values())controller.abort();
        prefetchControllers.clear();
        if(prefetchRetryTimer)clearTimeout(prefetchRetryTimer);
        if(prefetchHealthTimer)clearInterval(prefetchHealthTimer);
        if(aladinPrewarmTimer)clearTimeout(aladinPrewarmTimer);
        if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
        randomGalaxy.viewHdButton?.removeEventListener('click',deferHdUntilPrepared,true);
        randomGalaxy.hubbleIconButton?.removeEventListener('click',deferHdUntilPrepared,true);
        window.removeEventListener('resize',handleViewerResize);
        window.removeEventListener('pageshow',handleViewerPageShow);
        document.removeEventListener('visibilitychange',handleViewerVisibility);
        releasePreparedItem(activePreparedItem);releasePreparedItem(historyPreparedItem);prefetchReady.splice(0).forEach(releasePreparedItem);
        prefetchQueued.splice(0);
        try{aladinPrewarmHost?.remove()}catch(_){}
    },{once:true});
    bottom.random.addEventListener('click',suspendBackgroundWork,true);
    bottom.random.addEventListener('click',()=>{pendingHistoryIndex=null;navigationPending=true;homeOverlay.classList.add('gv-hidden');universeContext.classList.add('gv-hidden');setHistoryControls()});
    bottom.back.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex-1));
    bottom.forward.addEventListener('click',()=>navigateHistory(galaxyHistoryIndex+1));
    setHistoryControls();
    startupTiming.fullReadyAt=performance.now();
    const startupMetrics=Object.freeze({...startupTiming,shellMs:startupTiming.shellReadyAt-startupTiming.startedAt,catalogMs:startupTiming.catalogReadyAt-startupTiming.startedAt,randomMs:startupTiming.randomReadyAt-startupTiming.startedAt,fullMs:startupTiming.fullReadyAt-startupTiming.startedAt});
    window.GalaxyViewerCore=Object.freeze({version:VERSION,displayVersion:DISPLAY_VERSION,aladin,hamburger,coordinate,target,randomGalaxy,randomGalaxyButton:bottom.random,historyBackButton:bottom.back,historyForwardButton:bottom.forward,reticle,versionLabel:bottom.version,universeContext,homeOverlay,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,catalogDatabaseCounts,startupMetrics,getHubblePrefetchState,getHubbleDownloadStatus,getAladinPrewarmState,startHubblePrefetch:fillPrefetchQueue,getGalaxyCatalog:()=>Object.freeze([...galaxyCatalog]),activateQueuedDestination:(destination,excludeName='')=>consumeReady(destination,excludeName)||setUnpreparedActive(destination),requestHdPrefetch:destination=>{if(!destination)return '';enqueuePrefetch(destination,true);fillPrefetchQueue();return destinationKey(destination)},isAladinPrepared:key=>aladinPrewarmedKeys.has(String(key||'').trim().toLowerCase()),getBackgroundWorkSuspended:()=>backgroundWorkSuspended,getChandraTestOverrideState:()=>Object.freeze({chandraTestOverrideActive,chandraTestRemaining:chandraTestQueue.length,chandraTestTotal}),getGalaxyHistory:()=>({index:galaxyHistoryIndex,items:galaxyHistory.map(item=>({name:item.name,archiveId:item.archiveId,provider:item.provider||'HUBBLE'}))})});
    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length,startupMetrics}}));
})().catch(error=>{console.error('GALAXY VIEWER 10AE2 STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});
"""))

# Galaxy Viewer active implementation staged

# Galaxy Viewer Prefetch — unified future-ten prefetch integration layer.
display(Javascript(r"""
(()=>{
'use strict';
const VERSION='11F';
const FUTURE_TARGET=10;
const WEB_MAX=10;
const WEB_RETRY_MS=5000;
const POLL_MS=80;
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const keyOf=destination=>String(destination?.archiveId||destination?.name||'').trim().toLowerCase();
let core=null;
let randomGalaxy=null;
let originalProvider=null;
let catalog=[];
let catalogByKey=new Map();
let catalogByName=new Map();
let future=[];
let activeRecord=null;
let nextSequence=0;
let historyBypass=false;
let installed=false;
let suspended=false;
let hdFeedbackBusy=false;
const webStatus=new Map();
const webControllers=new Map();

function makeRecord(destination){
  return {sequence:++nextSequence,key:keyOf(destination),destination};
}
function uniqueRecords(records){
  const seen=new Set();
  return records.filter(record=>record?.key&&!seen.has(record.key)&&(seen.add(record.key),true));
}
function findDestinationByName(name){return catalogByName.get(String(name||'').trim().toLowerCase())||null}
function findDestinationByKey(key){return catalogByKey.get(String(key||'').trim().toLowerCase())||null}
function currentBlockedKeys(){
  const blocked=new Set(future.map(record=>record.key));
  if(activeRecord?.key)blocked.add(activeRecord.key);
  const activeKey=keyOf(randomGalaxy?.getState?.().activeDestination);
  if(activeKey)blocked.add(activeKey);
  return blocked;
}
function chooseUniqueDestination(){
  const blocked=currentBlockedKeys();
  const pool=catalog.filter(destination=>{const key=keyOf(destination);return key&&!blocked.has(key)});
  return pool.length?pool[Math.floor(Math.random()*pool.length)]:null;
}
function pipelineDestinations(){
  const state=core?.getHubblePrefetchState?.()||{};
  const downloads=Array.isArray(state.downloads)?state.downloads:[];
  const byDownloadKey=new Map(downloads.map(item=>[String(item?.key||'').toLowerCase(),item]));
  const out=[];
  const add=destination=>{if(destination)out.push(destination)};
  for(const name of state.readyDestinations||[])add(findDestinationByName(name));
  for(const key of state.activeDownloadKeys||[]){
    const normalized=String(key||'').toLowerCase();
    add(findDestinationByKey(normalized)||findDestinationByName(byDownloadKey.get(normalized)?.name));
  }
  for(const name of state.queuedDestinations||[])add(findDestinationByName(name));
  return uniqueRecords(out.map(makeRecord)).map(record=>record.destination);
}
function setWebState(record,state,detail=''){
  if(!record?.key)return;
  webStatus.set(record.key,{state,detail,updatedAt:Date.now(),nextRetryAt:state==='RETRY'?Date.now()+WEB_RETRY_MS:0});
}
function webStateFor(record){return webStatus.get(record?.key)||{state:'QUEUED',detail:'',updatedAt:0,nextRetryAt:0}}
function suspendWeb(){
  suspended=true;
  for(const [key,controller] of webControllers){try{controller.abort()}catch(_){};const record=activeRecord?.key===key?activeRecord:future.find(item=>item.key===key);if(record)setWebState(record,'SUSPENDED')}
  webControllers.clear();
}
function resumeWeb(){
  suspended=false;
  for(const record of [activeRecord,...future].filter(Boolean)){const state=webStateFor(record);if(state.state==='SUSPENDED')setWebState(record,'QUEUED')}
  pumpWeb();
}
function startWeb(record){
  if(!record?.key||suspended||webControllers.size>=WEB_MAX||webControllers.has(record.key))return;
  const state=webStateFor(record);
  if(state.state==='READY'||state.state==='DOWNLOADING')return;
  if(state.state==='RETRY'&&Date.now()<Number(state.nextRetryAt||0))return;
  const sourceUrl=String(record.destination?.sourceUrl||'').trim();
  if(!/^https:\/\//i.test(sourceUrl)){setWebState(record,'FAILED','NO SOURCE URL');return}
  const controller=new AbortController();
  webControllers.set(record.key,controller);
  setWebState(record,'DOWNLOADING');
  fetch(sourceUrl,{mode:'no-cors',cache:'force-cache',credentials:'omit',signal:controller.signal,priority:'low'})
    .then(()=>setWebState(record,'READY'))
    .catch(error=>{if(error?.name==='AbortError'){setWebState(record,'SUSPENDED');return}setWebState(record,'RETRY',String(error?.message||error))})
    .finally(()=>{webControllers.delete(record.key);setTimeout(pumpWeb,0)});
}
function pumpWeb(){
  if(suspended)return;
  const candidates=[activeRecord,...future].filter(Boolean);
  for(const record of candidates){if(webControllers.size>=WEB_MAX)break;startWeb(record)}
function prepareRecord(record){
  if(!record)return;
  core?.requestHdPrefetch?.(record.destination);
  if(!webStatus.has(record.key))setWebState(record,'QUEUED');
  pumpWeb();
}
function addFuture(destination){
  if(!destination)return false;
  const key=keyOf(destination);
  if(!key||currentBlockedKeys().has(key))return false;
  const record=makeRecord(destination);
  future.push(record);
  prepareRecord(record);
  return true;
}
function reconcileFutureQueue(){
  future=uniqueRecords(future).slice(0,FUTURE_TARGET);
  const pipeline=pipelineDestinations();
  for(const destination of pipeline){if(future.length>=FUTURE_TARGET)break;addFuture(destination)}
  while(future.length<FUTURE_TARGET){const candidate=chooseUniqueDestination();if(!candidate||!addFuture(candidate))break}
  pumpWeb();
}
function consumeNext(excludeName=''){
  reconcileFutureQueue();
  const excluded=String(excludeName||'').trim().toLowerCase();
  let index=future.findIndex(record=>String(record.destination?.name||'').trim().toLowerCase()!==excluded&&record.key!==activeRecord?.key);
  if(index<0)index=0;
  const record=future.splice(index,1)[0]||null;
  if(!record)return null;
  activeRecord=record;
  const destination=core.activateQueuedDestination(record.destination,excludeName);
  activeRecord.destination=destination;
  setTimeout(reconcileFutureQueue,100);
  pumpWeb();
  return destination;
}
function normalizeHdState(state){
  const value=String(state||'').toUpperCase();
  if(value==='READY')return 'READY';
  if(value==='DOWNLOADING'||value==='DECODING')return value;
  if(value==='SUSPENDED')return 'SUSPENDED';
  if(value.includes('RETRY'))return 'RETRY';
  if(value==='QUEUED')return 'QUEUED';
  return value||'QUEUED';
}
function hdStateFor(record){
  const status=(core.getHubbleDownloadStatus?.()||[]).find(item=>String(item?.key||'').toLowerCase()===record.key);
  const state=normalizeHdState(status?.state);
  return {state,progress:state==='READY'?100:null,detail:String(status?.sourceKind||'')};
}
function aladinStateFor(record){
  if(core.isAladinPrepared?.(record.key))return {state:'READY',progress:100};
  if(core.getBackgroundWorkSuspended?.())return {state:'SUSPENDED',progress:null};
  const state=core.getAladinPrewarmState?.()||{};
  if(String(state.activeKey||'').toLowerCase()===record.key)return {state:'PREPARING',progress:null};
  return {state:'QUEUED',progress:null};
}
function webTelemetry(record){
  const state=webStateFor(record);
  return {state:state.state,progress:state.state==='READY'?100:null,detail:state.detail||''};
}
function telemetry(){
  return Object.freeze({
    version:VERSION,
    suspended:Boolean(core?.getBackgroundWorkSuspended?.()),
    active:activeRecord?Object.freeze({sequence:activeRecord.sequence,key:activeRecord.key,name:String(activeRecord.destination?.name||''),provider:String(activeRecord.destination?.provider||'')}):null,
    rows:Object.freeze(future.slice(0,FUTURE_TARGET).map(record=>Object.freeze({sequence:record.sequence,key:record.key,name:String(record.destination?.name||''),provider:String(record.destination?.provider||''),hd:Object.freeze(hdStateFor(record)),aladin:Object.freeze(aladinStateFor(record)),web:Object.freeze(webTelemetry(record))})))
  });
}
function installHdFeedback(){
  if(!randomGalaxy?.hubbleIconButton)return;
  const style=document.createElement('style');
  style.id='gv-prefetch-hd-feedback-style';
  style.textContent='.gvrg-hd-icon-button{position:relative!important}.gv-prefetch-hd-feedback{position:absolute;inset:5px;border-radius:50%;opacity:0;pointer-events:none;transform-origin:50% 50%}.gv-prefetch-hd-feedback::before{content:"";position:absolute;left:50%;top:-1px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#F8FFFF;box-shadow:0 0 4px #fff,0 0 8px #8FE5FF,0 0 11px #296DBD}.gv-prefetch-hd-feedback::after{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 250deg,transparent 0deg,rgba(91,184,255,.25) 42deg,rgba(143,229,255,.58) 82deg,rgba(248,255,255,.92) 110deg,transparent 111deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px))}.gvrg-hd-icon-button.gv-prefetch-hd-wait .gv-prefetch-hd-feedback{opacity:1;animation:gvPrefetchHdOrbit 1s linear infinite}@keyframes gvPrefetchHdOrbit{to{transform:rotate(360deg)}}';
  document.head.appendChild(style);
  const feedback=document.createElement('span');
  feedback.className='gv-prefetch-hd-feedback';feedback.setAttribute('aria-hidden','true');
  randomGalaxy.hubbleIconButton.appendChild(feedback);
  const waitForHd=async(key,timeout=2500)=>{const started=performance.now();for(;;){const state=hdStateFor({key});if(state.state==='READY')return true;if(performance.now()-started>=timeout)return false;await sleep(80)}};
  const handle=async event=>{
    const destination=randomGalaxy.getState?.().activeDestination;
    if(!destination||hdFeedbackBusy)return;
    event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();
    hdFeedbackBusy=true;
    randomGalaxy.hubbleIconButton.classList.add('gv-prefetch-hd-wait');
    const key=keyOf(destination);
    core.requestHdPrefetch?.(destination);
    try{await Promise.all([sleep(1000),waitForHd(key,2500)]);randomGalaxy.showHubbleHD()}catch(error){console.error('GALAXY VIEWER PREFETCH HD ENTRY FAILURE',error);try{randomGalaxy.showHubbleHD()}catch(_){} }finally{randomGalaxy.hubbleIconButton.classList.remove('gv-prefetch-hd-wait');hdFeedbackBusy=false}
  };
  randomGalaxy.viewHdButton?.addEventListener('click',handle,true);
  randomGalaxy.hubbleIconButton?.addEventListener('click',handle,true);
}
function install(){
  if(installed)return true;
  core=window.GalaxyViewerCore;
  if(!core?.randomGalaxy||typeof core.getGalaxyCatalog!=='function'||typeof core.activateQueuedDestination!=='function')return false;
  randomGalaxy=core.randomGalaxy;
  originalProvider=randomGalaxy.hubbleProvider;
  catalog=core.getGalaxyCatalog();
  catalogByKey=new Map(catalog.map(destination=>[keyOf(destination),destination]));
  catalogByName=new Map(catalog.map(destination=>[String(destination?.name||'').trim().toLowerCase(),destination]));
  reconcileFutureQueue();
  randomGalaxy.hubbleProvider=async args=>{
    if(historyBypass){historyBypass=false;return originalProvider(args)}
    const destination=consumeNext(args?.excludeName||'');
    return destination||originalProvider(args);
  };
  core.historyBackButton?.addEventListener('click',()=>{if(!core.historyBackButton.disabled)historyBypass=true},true);
  core.historyForwardButton?.addEventListener('click',()=>{if(!core.historyForwardButton.disabled)historyBypass=true},true);
  core.randomGalaxyButton?.addEventListener('click',()=>{setTimeout(()=>{if(core.getBackgroundWorkSuspended?.())suspendWeb()},0)},true);
  const monitor=setInterval(()=>{
    const nextSuspended=Boolean(core.getBackgroundWorkSuspended?.());
    if(nextSuspended!==suspended){if(nextSuspended)suspendWeb();else resumeWeb()}
    if(!nextSuspended)reconcileFutureQueue();
  },POLL_MS);
  window.addEventListener('beforeunload',()=>{clearInterval(monitor);for(const controller of webControllers.values())try{controller.abort()}catch(_){};webControllers.clear()},{once:true});
  installHdFeedback();
  if(core.versionLabel){core.versionLabel.textContent='VERSION 11F';core.versionLabel.setAttribute('aria-label','GALAXY VIEWER VERSION 11F')}
  window.GalaxyViewerPrefetch=Object.freeze({version:VERSION,displayVersion:VERSION,core,randomGalaxy,getPrefetchTelemetry:telemetry,reconcileFutureQueue});
  installed=true;
  document.dispatchEvent(new CustomEvent('gv-prefetch-ready',{detail:{version:VERSION,rows:future.length}}));
  return true;
}
if(!install()){
  const onReady=()=>setTimeout(install,0);
  document.addEventListener('gv-viewer-ready',onReady,{once:true});
  const timer=setInterval(()=>{if(install())clearInterval(timer)},100);
  setTimeout(()=>clearInterval(timer),30000);
}
})();
"""))

# Galaxy Viewer Prefetch staged
