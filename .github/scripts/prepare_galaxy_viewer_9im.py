from pathlib import Path
import re, shutil, subprocess
import prepare_galaxy_viewer_9ij as base

ROOT=Path(__file__).resolve().parents[2]
VIEWER=ROOT/'viewer/GV-beta-0009I.py'
ANDROID=ROOT/'android/galaxy-viewer-9i'
ASSETS=ANDROID/'app/src/main/assets'
EXPECTED_VIEWER='cdab230d7f4f7a9862508579563fdc316a0b3a72'
ICON_SHA='47b3e714053bfd64f835d3f1a2510e13618dbede'
MODULES=[
 ('gv-hamburger-menu-0002.js','HAMBURGER_URL','gvHamburger0002'),
 ('gv-coordinate-overlay-0004.js','COORDINATE_URL','gvCoordinate0004'),
 ('gv-target-simbad-0001.js','TARGET_URL','gvTarget0001'),
 ('gv-random-galaxy-0028.js','RANDOM_GALAXY_URL','gvRandomGalaxy0028'),
]

def hash_object(path):
    return subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip()

def patch_viewer():
    if hash_object(VIEWER)!=EXPECTED_VIEWER:
        raise SystemExit('REFUSING 9I-M: active beta Viewer is not verified 9I-L')
    text=VIEWER.read_text(encoding='utf-8')
    old="    const DISPLAY_VERSION='9I-L';"
    if text.count(old)!=1:
        raise SystemExit('REFUSING 9I-M: expected exactly one 9I-L DISPLAY_VERSION')
    VIEWER.write_text(text.replace(old,"    const DISPLAY_VERSION='9I-M';",1),encoding='utf-8')

def copy_assets():
    if ASSETS.exists(): shutil.rmtree(ASSETS)
    ASSETS.mkdir(parents=True)
    shutil.copytree(ROOT/'viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL',ASSETS/'splash')
    (ASSETS/'data').mkdir()
    shutil.copy2(ROOT/'viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0002.json',ASSETS/'data/gv-hubble-galaxies-full-0002.json')
    (ASSETS/'artwork').mkdir()
    shutil.copy2(ROOT/'viewer/artwork/GV-reticle-0001.svg',ASSETS/'artwork/GV-reticle-0001.svg')
    shutil.copy2(ANDROID/'app/src/main/res/drawable/gv_app_icon.png',ASSETS/'app-icon.png')
    if hash_object(ANDROID/'app/src/main/res/drawable/gv_app_icon.png')!=ICON_SHA:
        raise SystemExit('REFUSING 9I-M: Android icon changed')

def patch_packaged_splash():
    p=ASSETS/'splash/index.html'
    s=p.read_text(encoding='utf-8')
    s=s.replace(' crossorigin="anonymous"','')
    needle="window.dispatchEvent(new CustomEvent('galaxy-splash-complete'))"
    if s.count(needle)!=2:
        raise SystemExit('REFUSING 9I-M: splash must have exactly two completion exits')
    bridge=needle+";try{parent.postMessage('galaxy-splash-complete','*')}catch(_){}"
    s=s.replace(needle,bridge)
    p.write_text(s,encoding='utf-8')

def safe_script(text):
    return re.sub(r'</script',r'<\\/script',text,flags=re.I)

def build_standalone():
    source=VIEWER.read_text(encoding='utf-8')
    html=re.findall(r'display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)',source)
    js=re.findall(r'display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)',source)
    if len(html)!=1 or len(js)!=1:
        raise SystemExit(f'REFUSING 9I-M: expected exactly one Viewer HTML and one Viewer JS block, got {len(html)} / {len(js)}')
    viewer_js=js[0]
    viewer_js=re.sub(r"const HUBBLE_CATALOG_URL='[^']+';","const HUBBLE_CATALOG_URL='data/gv-hubble-galaxies-full-0002.json';",viewer_js,count=1)
    viewer_js=re.sub(r"const RETICLE_URL='[^']+';","const RETICLE_URL='artwork/GV-reticle-0001.svg';",viewer_js,count=1)
    module_scripts=[]
    for name,const_name,script_id in MODULES:
        exact=f"    await loadScript({const_name},'{script_id}');"
        if viewer_js.count(exact)!=1:
            raise SystemExit(f'REFUSING 9I-M: expected one module load call for {name}')
        viewer_js=viewer_js.replace(exact,f"    /* 9I-M {name} embedded before Viewer startup */",1)
        module_scripts.append(safe_script((ROOT/'viewer/modules'/name).read_text(encoding='utf-8')))
    if 'await loadScript(HAMBURGER_URL' in viewer_js or 'await loadScript(COORDINATE_URL' in viewer_js or 'await loadScript(TARGET_URL' in viewer_js or 'await loadScript(RANDOM_GALAXY_URL' in viewer_js:
        raise SystemExit('REFUSING 9I-M: dynamic Galaxy Viewer module loader survived')

    control=r'''<script>
(()=>{
'use strict';
const root=document.documentElement,cover=document.getElementById('gv-apk-cover'),splash=document.getElementById('gv-apk-splash'),errorBox=document.getElementById('gv-apk-error');
let viewerReady=false,splashDone=false;
root.dataset.viewerStatus='booting';root.dataset.splashStatus='waiting';
const showError=error=>{root.dataset.viewerStatus='failed';errorBox.style.display='block';errorBox.textContent='APP FAILED TO LOAD\n\n'+String(error?.stack||error)};
const reveal=()=>{if(viewerReady&&splashDone){root.dataset.gvStatus='ready';requestAnimationFrame(()=>{splash.remove();cover.remove()})}};
document.addEventListener('gv-viewer-ready',event=>{viewerReady=true;root.dataset.viewerStatus='ready';root.dataset.viewerVersion=String(event.detail?.displayVersion||'');reveal()},{once:true});
document.addEventListener('gv-viewer-failed',event=>showError(new Error(event.detail?.message||'GALAXY VIEWER INITIALIZATION FAILED')),{once:true});
window.addEventListener('message',event=>{if(event.source===splash.contentWindow&&event.data==='galaxy-splash-complete'){splashDone=true;root.dataset.splashStatus='ready';reveal()}});
setTimeout(()=>{splash.addEventListener('load',()=>requestAnimationFrame(()=>cover.remove()),{once:true});splash.addEventListener('error',()=>showError(new Error('FINAL SPLASH FAILED TO LOAD')),{once:true});splash.src='splash/index.html'},3500);
setTimeout(()=>{if(!viewerReady)showError(new Error('GALAXY VIEWER READY EVENT TIMEOUT'))},60000);
setTimeout(()=>{if(!splashDone)showError(new Error('FINAL SPLASH COMPLETION TIMEOUT'))},30000);
})();
</script>'''
    shell='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 9I-M</title><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(42vw,240px);height:auto;max-height:42vh;object-fit:contain}#gv-apk-splash{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000}#gv-apk-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;box-sizing:border-box;background:#000;color:#FFD166;white-space:pre-wrap;font:14px/1.5 monospace}</style></head><body><div id="gv-apk-cover"><img src="app-icon.png" alt="GALAXY VIEWER"></div><iframe id="gv-apk-splash" title="GALAXY VIEWER SPLASH"></iframe><div id="gv-apk-error"></div>'''
    shell+=html[0]+control
    for module in module_scripts:
        shell+='<script>'+module+'</script>'
    shell+='<script>'+safe_script(viewer_js)+'</script></body></html>'
    (ASSETS/'index.html').write_text(shell,encoding='utf-8')

def patch_android_identity():
    base.patch_android()
    gradle=ANDROID/'app/build.gradle'
    g=gradle.read_text(encoding='utf-8')
    g=re.sub(r'versionCode\s+\d+','versionCode 19',g,count=1)
    g=re.sub(r"versionName\s+'[^']+'","versionName '9I-M'",g,count=1)
    gradle.write_text(g,encoding='utf-8')
    manifest=ANDROID/'app/src/main/AndroidManifest.xml'
    m=manifest.read_text(encoding='utf-8')
    m=re.sub(r'android:label="[^"]+"','android:label="GALAXY VIEWER 9I-M"',m,count=1)
    manifest.write_text(m,encoding='utf-8')

def verify():
    index=(ASSETS/'index.html').read_text(encoding='utf-8')
    if "DISPLAY_VERSION='9I-M'" not in index: raise SystemExit('REFUSING 9I-M: standalone Viewer identity missing')
    for name,const_name,script_id in MODULES:
        if f"await loadScript({const_name},'{script_id}')" in index: raise SystemExit('REFUSING 9I-M: runtime module load survived: '+name)
    for marker in ['GalaxyViewerHamburgerMenu','GalaxyCoordinateOverlay','GalaxyViewerTargetSimbad','GalaxyRandomGalaxy']:
        if marker not in index: raise SystemExit('REFUSING 9I-M: embedded module export marker missing: '+marker)
    for marker in ['gv-viewer-ready','gv-viewer-failed','data/gv-hubble-galaxies-full-0002.json','artwork/GV-reticle-0001.svg']:
        if marker not in index: raise SystemExit('REFUSING 9I-M: standalone invariant missing: '+marker)
    splash=(ASSETS/'splash/index.html').read_text(encoding='utf-8')
    if splash.count("parent.postMessage('galaxy-splash-complete','*')")!=2: raise SystemExit('REFUSING 9I-M: packaged splash bridge missing')
    catalog=(ASSETS/'data/gv-hubble-galaxies-full-0002.json').read_text(encoding='utf-8')
    if '"categoryEntryCount": 1879' not in catalog: raise SystemExit('REFUSING 9I-M: catalog invariant failed')
    if hash_object(ANDROID/'app/src/main/res/drawable/gv_app_icon.png')!=ICON_SHA: raise SystemExit('REFUSING 9I-M: icon changed')

def main():
    patch_viewer();copy_assets();patch_packaged_splash();build_standalone();patch_android_identity();verify()

if __name__=='__main__': main()
