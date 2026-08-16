from pathlib import Path
import json
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
VIEWER = ROOT / 'viewer/GV-beta-0009I.py'
ANDROID = ROOT / 'android/galaxy-viewer-9i'


def patch_viewer():
    text = VIEWER.read_text(encoding='utf-8')
    blob = subprocess.check_output(['git','hash-object',str(VIEWER)], cwd=ROOT, text=True).strip()
    expected = '883fdb8e1b6cb795a8d1a8b695b2ad8e40e66052'
    if blob != expected:
        raise SystemExit(f'REFUSING PATCH: beta Viewer blob {blob} != expected {expected}')
    old = "    const DISPLAY_VERSION='9I-F';"
    if text.count(old) != 1:
        raise SystemExit('REFUSING PATCH: expected exactly one 9I-F DISPLAY_VERSION')
    text = text.replace(old, "    const DISPLAY_VERSION='9I-G';", 1)
    VIEWER.write_text(text, encoding='utf-8')
    if "const DISPLAY_VERSION='9I-G';" not in text:
        raise SystemExit('9I-G identity missing after patch')


def build_local_shell():
    viewer = VIEWER.read_text(encoding='utf-8')
    shell = (ROOT / 'mobile/beta/9I-app.html').read_text(encoding='utf-8')
    asset_dir = ANDROID / 'app/src/main/assets'
    if asset_dir.exists():
        shutil.rmtree(asset_dir)
    asset_dir.mkdir(parents=True)
    shutil.copytree(ROOT / 'viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL', asset_dir / 'splash')
    modules_dir = asset_dir / 'modules'
    modules_dir.mkdir()
    for name in ['gv-hamburger-menu-0002.js','gv-coordinate-overlay-0004.js','gv-target-simbad-0001.js','gv-random-galaxy-0028.js']:
        shutil.copy2(ROOT / 'viewer/modules' / name, modules_dir / name)
    shutil.copy2(ROOT / 'android/galaxy-viewer-9i/app/src/main/res/drawable/gv_app_icon.png', asset_dir / 'app-icon.png')

    splash_path = asset_dir / 'splash/index.html'
    splash = splash_path.read_text(encoding='utf-8')
    needle = "window.dispatchEvent(new CustomEvent('galaxy-splash-complete'))"
    if splash.count(needle) < 1:
        raise SystemExit('Splash completion dispatch not found')
    splash = splash.replace(needle, "try{parent.postMessage('galaxy-splash-complete','*')}catch(_){};" + needle)
    splash_path.write_text(splash, encoding='utf-8')

    shell = shell.replace('../../viewer/artwork/App%20Icons/GV-app-icon-512.png', 'app-icon.png')
    shell = shell.replace("const SPLASH_BASE='../../viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/';", "const SPLASH_BASE='splash/';")
    shell = shell.replace("versionLabel.textContent='VERSION 9D'", "versionLabel.textContent='VERSION 9I-G'")
    shell = shell.replace("GALAXY VIEWER VERSION 9D", "GALAXY VIEWER VERSION 9I-G")

    fetch_line = "  const viewerDownloadPromise=fetch(VIEWER_URL,{cache:'force-cache'}).then(async response=>{if(!response.ok)throw new Error('GV-BETA-0009I.PY RETURNED HTTP '+response.status);return response.blob()});"
    replacement = "  const viewerDownloadPromise=Promise.resolve(new Blob([" + json.dumps(viewer) + "],{type:'text/plain'}));"
    if fetch_line not in shell:
        raise SystemExit('Viewer download line not found in app shell')
    shell = shell.replace(fetch_line, replacement, 1)

    inject_anchor = "    let source=await viewerBlob.text();\n"
    inject = """    source=source.replace(/const HAMBURGER_URL='[^']+';/,\"const HAMBURGER_URL='modules/gv-hamburger-menu-0002.js';\");
    source=source.replace(/const COORDINATE_URL='[^']+';/,\"const COORDINATE_URL='modules/gv-coordinate-overlay-0004.js';\");
    source=source.replace(/const TARGET_URL='[^']+';/,\"const TARGET_URL='modules/gv-target-simbad-0001.js';\");
    source=source.replace(/const RANDOM_GALAXY_URL='[^']+';/,\"const RANDOM_GALAXY_URL='modules/gv-random-galaxy-0028.js';\");
"""
    if inject_anchor not in shell:
        raise SystemExit('Viewer source anchor not found in app shell')
    shell = shell.replace(inject_anchor, inject_anchor + inject, 1)

    start = shell.index('  const startVisibleSplash=async()=>{')
    end = shell.index('  const waitForViewer=()=>', start)
    new_start = '''  const startVisibleSplash=async()=>{\n    await waitForIconMinimum();\n    if(splashPreloadFrame.isConnected)splashPreloadFrame.remove();\n    return new Promise((resolve,reject)=>{\n      let settled=false;\n      let timeout=0;\n      const cleanup=()=>{window.removeEventListener('message',onMessage);if(timeout)clearTimeout(timeout)};\n      const fail=error=>{if(settled)return;settled=true;cleanup();reject(error)};\n      const onMessage=event=>{\n        if(event.data!=='galaxy-splash-complete'||settled)return;\n        settled=true;cleanup();resolve();\n      };\n      window.addEventListener('message',onMessage);\n      splashFrame.addEventListener('load',()=>{\n        requestAnimationFrame(()=>requestAnimationFrame(()=>{if(launchCover.isConnected)launchCover.remove()}));\n      },{once:true});\n      splashFrame.addEventListener('error',()=>fail(new Error('FINAL SPLASH FAILED TO LOAD')),{once:true});\n      timeout=setTimeout(()=>fail(new Error('FINAL SPLASH COMPLETION TIMEOUT')),18000);\n      splashFrame.src=SPLASH_URL;\n    });\n  };\n'''
    shell = shell[:start] + new_start + shell[end:]
    if 'splashWindow.addEventListener' in shell or 'splashWindow.document' in shell:
        raise SystemExit('Cross-frame splash listener/DOM access still present')
    (asset_dir / 'index.html').write_text(shell, encoding='utf-8')


def patch_android():
    manifest = ANDROID / 'app/src/main/AndroidManifest.xml'
    text = manifest.read_text(encoding='utf-8')
    text = re.sub(r'android:icon="@drawable/[^"]+"', 'android:icon="@drawable/gv_app_icon"', text, count=1)
    text = re.sub(r'android:label="[^"]+"', 'android:label="GALAXY VIEWER 9I-G"', text, count=1)
    manifest.write_text(text, encoding='utf-8')

    gradle = ANDROID / 'app/build.gradle'
    text = gradle.read_text(encoding='utf-8')
    text = re.sub(r'versionCode\s+\d+', 'versionCode 13', text, count=1)
    text = re.sub(r"versionName\s+'[^']+'", "versionName '9I-G'", text, count=1)
    gradle.write_text(text, encoding='utf-8')

    main = ANDROID / 'app/src/main/java/com/gear66me/galaxyviewer9i/MainActivity.java'
    text = main.read_text(encoding='utf-8')
    text = re.sub(r'private static final String APP_URL = "[^"]+";', 'private static final String APP_URL = "file:///android_asset/index.html";', text, count=1)
    text = text.replace('settings.setAllowFileAccess(false);','settings.setAllowFileAccess(true);')
    text = text.replace('settings.setAllowContentAccess(false);','settings.setAllowContentAccess(true);')
    old = '''                return uri != null
                        && "https".equalsIgnoreCase(uri.getScheme())
                        && APP_HOST.equalsIgnoreCase(uri.getHost())
                        && uri.getPath() != null
                        && uri.getPath().startsWith(APP_PATH);'''
    new = '''                if (uri == null) return false;
                if ("file".equalsIgnoreCase(uri.getScheme())) return true;
                return "https".equalsIgnoreCase(uri.getScheme())
                        && APP_HOST.equalsIgnoreCase(uri.getHost())
                        && uri.getPath() != null
                        && uri.getPath().startsWith(APP_PATH);'''
    if old not in text:
        raise SystemExit('Android URL guard block not found')
    main.write_text(text.replace(old,new,1), encoding='utf-8')


def main():
    patch_viewer()
    if '--viewer-only' in __import__('sys').argv:
        return
    build_local_shell()
    patch_android()

if __name__ == '__main__':
    main()
