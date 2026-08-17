from pathlib import Path
import re, shutil, subprocess, json

ROOT=Path(__file__).resolve().parents[2]
VIEWER=ROOT/'viewer/GV-beta-0009I.py'
ANDROID=ROOT/'android/galaxy-viewer-9i'
ASSETS=ANDROID/'app/src/main/assets'
EXPECTED_VIEWER='be558dfbdcb4e0d44cfcb1afaae775071a8bc0a0'
ICON_SHA='47b3e714053bfd64f835d3f1a2510e13618dbede'


def hash_object(path):
    return subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip()


def patch_viewer():
    if hash_object(VIEWER)!=EXPECTED_VIEWER:
        raise SystemExit('REFUSING 9I-J: active beta Viewer blob is not verified 9I-I')
    text=VIEWER.read_text(encoding='utf-8')
    old="    const DISPLAY_VERSION='9I-I';"
    if text.count(old)!=1:
        raise SystemExit('REFUSING 9I-J: expected one 9I-I DISPLAY_VERSION')
    text=text.replace(old,"    const DISPLAY_VERSION='9I-J';",1)
    old_catch="})().catch(error=>console.error('GALAXY VIEWER 9I STARTUP FAILURE:',error));"
    new_catch="})().catch(error=>{console.error('GALAXY VIEWER 9I STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});"
    if text.count(old_catch)!=1:
        raise SystemExit('REFUSING 9I-J: Viewer terminal catch anchor changed')
    text=text.replace(old_catch,new_catch,1)
    VIEWER.write_text(text,encoding='utf-8')


def build_assets():
    if ASSETS.exists(): shutil.rmtree(ASSETS)
    ASSETS.mkdir(parents=True)
    shutil.copytree(ROOT/'viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL',ASSETS/'splash')
    (ASSETS/'modules').mkdir()
    for name in ['gv-hamburger-menu-0002.js','gv-coordinate-overlay-0004.js','gv-target-simbad-0001.js','gv-random-galaxy-0028.js']:
        shutil.copy2(ROOT/'viewer/modules'/name,ASSETS/'modules'/name)
    (ASSETS/'data').mkdir()
    shutil.copy2(ROOT/'viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0002.json',ASSETS/'data/gv-hubble-galaxies-full-0002.json')
    (ASSETS/'artwork').mkdir()
    shutil.copy2(ROOT/'viewer/artwork/GV-reticle-0001.svg',ASSETS/'artwork/GV-reticle-0001.svg')
    shutil.copy2(ANDROID/'app/src/main/res/drawable/gv_app_icon.png',ASSETS/'app-icon.png')
    if hash_object(ANDROID/'app/src/main/res/drawable/gv_app_icon.png')!=ICON_SHA:
        raise SystemExit('REFUSING 9I-J: existing Android icon changed')


def make_shell():
    shell=(ROOT/'mobile/beta/9I-app.html').read_text(encoding='utf-8')
    viewer=VIEWER.read_text(encoding='utf-8')
    shell=shell.replace('../../viewer/artwork/App%20Icons/GV-app-icon-512.png','app-icon.png')
    shell=shell.replace("const SPLASH_BASE='../../viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/';","const SPLASH_BASE='splash/';")
    shell=shell.replace("versionLabel.textContent='VERSION 9D'","versionLabel.textContent='VERSION 9I-J'")
    shell=shell.replace('GALAXY VIEWER VERSION 9D','GALAXY VIEWER VERSION 9I-J')
    fetch_line="  const viewerDownloadPromise=fetch(VIEWER_URL,{cache:'force-cache'}).then(async response=>{if(!response.ok)throw new Error('GV-BETA-0009I.PY RETURNED HTTP '+response.status);return response.blob()});"
    if fetch_line not in shell: raise SystemExit('Launcher Viewer fetch anchor missing')
    shell=shell.replace(fetch_line,"  const viewerDownloadPromise=Promise.resolve(new Blob(["+json.dumps(viewer)+"],{type:'text/plain'}));",1)

    # Preserve postMessage splash completion; never inspect child-frame DOM.
    start=shell.index('  const startVisibleSplash=async()=>{')
    end=shell.index('  const waitForViewer=()=>',start)
    splash_fn='''  const startVisibleSplash=async()=>{\n    await waitForIconMinimum();\n    if(splashPreloadFrame.isConnected)splashPreloadFrame.remove();\n    return new Promise((resolve,reject)=>{\n      let settled=false;let timeout=0;\n      const cleanup=()=>{window.removeEventListener('message',onMessage);if(timeout)clearTimeout(timeout)};\n      const done=()=>{if(settled)return;settled=true;cleanup();resolve()};\n      const fail=error=>{if(settled)return;settled=true;cleanup();reject(error)};\n      const onMessage=event=>{if(event.data==='galaxy-splash-complete')done()};\n      window.addEventListener('message',onMessage);\n      splashFrame.addEventListener('load',()=>requestAnimationFrame(()=>requestAnimationFrame(()=>{if(launchCover.isConnected)launchCover.remove()})),{once:true});\n      splashFrame.addEventListener('error',()=>fail(new Error('FINAL SPLASH FAILED TO LOAD')),{once:true});\n      timeout=setTimeout(()=>fail(new Error('FINAL SPLASH COMPLETION TIMEOUT')),25000);\n      splashFrame.src=SPLASH_URL;\n    });\n  };\n'''
    shell=shell[:start]+splash_fn+shell[end:]

    # Replace heuristic waitForViewer with the Viewer's own terminal READY/FAILED events.
    start=shell.index('  const waitForViewer=()=>')
    end=shell.index('  const initializeViewer=async()=>',start)
    ready_fn='''  const waitForViewer=()=>new Promise((resolve,reject)=>{\n    let settled=false;let timeout=0;\n    const cleanup=()=>{document.removeEventListener('gv-viewer-ready',onReady);document.removeEventListener('gv-viewer-failed',onFailed);if(timeout)clearTimeout(timeout)};\n    const onReady=event=>{if(settled)return;settled=true;cleanup();requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(event.detail||{})))};\n    const onFailed=event=>{if(settled)return;settled=true;cleanup();reject(new Error(event.detail?.message||'GALAXY VIEWER INITIALIZATION FAILED'))};\n    document.addEventListener('gv-viewer-ready',onReady,{once:true});\n    document.addEventListener('gv-viewer-failed',onFailed,{once:true});\n    timeout=setTimeout(()=>{if(settled)return;settled=true;cleanup();reject(new Error('GALAXY VIEWER READY EVENT TIMEOUT'))},60000);\n  });\n'''
    shell=shell[:start]+ready_fn+shell[end:]

    # Patch embedded Viewer URLs to same-origin APK assets before executing it.
    anchor="    let source=await viewerBlob.text();\n"
    patch="""    source=source.replace(/const HAMBURGER_URL='[^']+';/,\"const HAMBURGER_URL='modules/gv-hamburger-menu-0002.js';\");
    source=source.replace(/const COORDINATE_URL='[^']+';/,\"const COORDINATE_URL='modules/gv-coordinate-overlay-0004.js';\");
    source=source.replace(/const TARGET_URL='[^']+';/,\"const TARGET_URL='modules/gv-target-simbad-0001.js';\");
    source=source.replace(/const RANDOM_GALAXY_URL='[^']+';/,\"const RANDOM_GALAXY_URL='modules/gv-random-galaxy-0028.js';\");
    source=source.replace(/const HUBBLE_CATALOG_URL='[^']+';/,\"const HUBBLE_CATALOG_URL='data/gv-hubble-galaxies-full-0002.json';\");
    source=source.replace(/const RETICLE_URL='[^']+';/,\"const RETICLE_URL='artwork/GV-reticle-0001.svg';\");
"""
    if anchor not in shell: raise SystemExit('Launcher source anchor missing')
    shell=shell.replace(anchor,anchor+patch,1)

    # Attach READY listener before executing Viewer scripts so the event cannot be missed.
    old="  const initializeViewer=async()=>{\n    const viewerBlob=await viewerDownloadPromise;"
    new="  const initializeViewer=async()=>{\n    const readyPromise=waitForViewer();\n    const viewerBlob=await viewerDownloadPromise;"
    if old not in shell: raise SystemExit('initializeViewer anchor missing')
    shell=shell.replace(old,new,1)
    shell=shell.replace('    await waitForViewer();\n  };','    await readyPromise;\n  };',1)
    (ASSETS/'index.html').write_text(shell,encoding='utf-8')


def patch_android():
    gradle=ANDROID/'app/build.gradle'
    g=gradle.read_text(encoding='utf-8')
    g=re.sub(r'versionCode\s+\d+','versionCode 16',g,count=1)
    g=re.sub(r"versionName\s+'[^']+'","versionName '9I-J'",g,count=1)
    if 'androidx.webkit:webkit:' not in g:
        g += "\n\ndependencies {\n    implementation 'androidx.webkit:webkit:1.12.1'\n}\n"
    gradle.write_text(g,encoding='utf-8')

    manifest=ANDROID/'app/src/main/AndroidManifest.xml'
    m=manifest.read_text(encoding='utf-8')
    m=re.sub(r'android:label="[^"]+"','android:label="GALAXY VIEWER 9I-J"',m,count=1)
    m=re.sub(r'android:icon="@drawable/[^"]+"','android:icon="@drawable/gv_app_icon"',m,count=1)
    manifest.write_text(m,encoding='utf-8')

    main=ANDROID/'app/src/main/java/com/gear66me/galaxyviewer9i/MainActivity.java'
    s=main.read_text(encoding='utf-8')
    # imports
    if 'android.webkit.WebResourceResponse;' not in s:
        s=s.replace('import android.webkit.WebResourceRequest;','import android.webkit.WebResourceRequest;\nimport android.webkit.WebResourceResponse;')
    if 'androidx.webkit.WebViewAssetLoader;' not in s:
        s=s.replace('import org.json.JSONObject;','import org.json.JSONObject;\n\nimport androidx.webkit.WebViewAssetLoader;')
    s=re.sub(r'private static final String APP_URL = "[^"]+";','private static final String APP_URL = "https://appassets.androidplatform.net/assets/index.html";',s,count=1)
    # Replace settings with secure asset-loader compatible settings.
    s=s.replace('settings.setAllowFileAccess(false);','settings.setAllowFileAccess(false);')
    s=s.replace('settings.setAllowContentAccess(false);','settings.setAllowContentAccess(false);')
    marker='        webView.addJavascriptInterface(new DownloadBridge(this), "GalaxyViewerAndroid");\n        webView.setWebChromeClient(new WebChromeClient());\n'
    if marker not in s: raise SystemExit('MainActivity WebChrome marker missing')
    insert=marker+'        final WebViewAssetLoader assetLoader = new WebViewAssetLoader.Builder()\n                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))\n                .build();\n'
    s=s.replace(marker,insert,1)
    # Replace allowed() and add shouldInterceptRequest.
    old='''            private boolean allowed(Uri uri) {
                return uri != null
                        && "https".equalsIgnoreCase(uri.getScheme())
                        && APP_HOST.equalsIgnoreCase(uri.getHost())
                        && uri.getPath() != null
                        && uri.getPath().startsWith(APP_PATH);
            }
'''
    new='''            private boolean allowed(Uri uri) {
                return uri != null
                        && "https".equalsIgnoreCase(uri.getScheme())
                        && "appassets.androidplatform.net".equalsIgnoreCase(uri.getHost());
            }

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return assetLoader.shouldInterceptRequest(request.getUrl());
            }

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, String url) {
                return assetLoader.shouldInterceptRequest(Uri.parse(url));
            }
'''
    if old not in s: raise SystemExit('MainActivity allowed() block missing')
    s=s.replace(old,new,1)
    main.write_text(s,encoding='utf-8')


def verify_assets():
    index=(ASSETS/'index.html').read_text(encoding='utf-8')
    required=['gv-viewer-ready','gv-viewer-failed','data/gv-hubble-galaxies-full-0002.json','modules/gv-random-galaxy-0028.js','artwork/GV-reticle-0001.svg']
    for x in required:
        if x not in index: raise SystemExit('Missing packaged launcher invariant: '+x)
    if 'homeReady' in index or "root&&aladin&&canvas" in index:
        raise SystemExit('Old heuristic readiness logic survived')


def main():
    patch_viewer(); build_assets(); make_shell(); patch_android(); verify_assets()

if __name__=='__main__': main()
