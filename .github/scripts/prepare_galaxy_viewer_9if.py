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
    blob = subprocess.check_output(['git', 'hash-object', str(VIEWER)], cwd=ROOT, text=True).strip()
    expected = 'b3be3d94fbeeea16dd13384cf2b51a7a218f0ddf'
    if blob != expected:
        raise SystemExit(f'REFUSING PATCH: beta Viewer blob {blob} != expected {expected}')

    old = "    const DISPLAY_VERSION='9I-A';"
    if text.count(old) != 1:
        raise SystemExit('REFUSING PATCH: expected exactly one 9I-A DISPLAY_VERSION')
    text = text.replace(old, "    const DISPLAY_VERSION='9I-F';", 1)

    anchor = "    await randomGalaxy.ready;\n"
    if text.count(anchor) != 1:
        raise SystemExit('REFUSING PATCH: expected exactly one randomGalaxy.ready anchor')

    patch = r'''    const hdScience=randomGalaxy.hdScience;
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
'''
    text = text.replace(anchor, anchor + patch, 1)
    VIEWER.write_text(text, encoding='utf-8')

    if "const DISPLAY_VERSION='9I-F';" not in text:
        raise SystemExit('9I-F identity missing after patch')
    if text.count("key.textContent='CONST';") != 1:
        raise SystemExit('Expected exactly one source-level CONST creation')


def build_local_shell():
    viewer = VIEWER.read_text(encoding='utf-8')
    shell = (ROOT / 'mobile/beta/9I-app.html').read_text(encoding='utf-8')
    modules = {
        'hamburger': (ROOT / 'viewer/modules/gv-hamburger-menu-0002.js').read_text(encoding='utf-8'),
        'coordinate': (ROOT / 'viewer/modules/gv-coordinate-overlay-0004.js').read_text(encoding='utf-8'),
        'target': (ROOT / 'viewer/modules/gv-target-simbad-0001.js').read_text(encoding='utf-8'),
        'random': (ROOT / 'viewer/modules/gv-random-galaxy-0028.js').read_text(encoding='utf-8'),
    }

    asset_dir = ANDROID / 'app/src/main/assets'
    if asset_dir.exists():
        shutil.rmtree(asset_dir)
    asset_dir.mkdir(parents=True)
    shutil.copytree(ROOT / 'viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL', asset_dir / 'splash')

    shell = shell.replace('../../viewer/artwork/App%20Icons/GV-app-icon-512.png', 'app-icon.png')
    shell = shell.replace("const SPLASH_BASE='../../viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/';", "const SPLASH_BASE='splash/';")
    shell = shell.replace("versionLabel.textContent='VERSION 9D'", "versionLabel.textContent='VERSION 9I-F'")
    shell = shell.replace("GALAXY VIEWER VERSION 9D", "GALAXY VIEWER VERSION 9I-F")

    fetch_line = "  const viewerDownloadPromise=fetch(VIEWER_URL,{cache:'force-cache'}).then(async response=>{if(!response.ok)throw new Error('GV-BETA-0009I.PY RETURNED HTTP '+response.status);return response.blob()});"
    replacement = "  const viewerDownloadPromise=Promise.resolve(new Blob([" + json.dumps(viewer) + "],{type:'text/plain'}));"
    if fetch_line not in shell:
        raise SystemExit('Viewer download line not found in app shell')
    shell = shell.replace(fetch_line, replacement, 1)

    inject_anchor = "    let source=await viewerBlob.text();\n"
    inject = f"""    const embeddedModules={json.dumps(modules)};
    const moduleUrls={{}};
    for(const [name,moduleSource] of Object.entries(embeddedModules))moduleUrls[name]=URL.createObjectURL(new Blob([moduleSource],{{type:'text/javascript'}}));
    source=source.replace(/const HAMBURGER_URL='[^']+';/,`const HAMBURGER_URL='${{moduleUrls.hamburger}}';`);
    source=source.replace(/const COORDINATE_URL='[^']+';/,`const COORDINATE_URL='${{moduleUrls.coordinate}}';`);
    source=source.replace(/const TARGET_URL='[^']+';/,`const TARGET_URL='${{moduleUrls.target}}';`);
    source=source.replace(/const RANDOM_GALAXY_URL='[^']+';/,`const RANDOM_GALAXY_URL='${{moduleUrls.random}}';`);
"""
    if inject_anchor not in shell:
        raise SystemExit('Viewer source anchor not found in app shell')
    shell = shell.replace(inject_anchor, inject_anchor + inject, 1)
    (asset_dir / 'index.html').write_text(shell, encoding='utf-8')


def patch_android():
    manifest = ANDROID / 'app/src/main/AndroidManifest.xml'
    text = manifest.read_text(encoding='utf-8')
    text = re.sub(r'android:icon="@drawable/[^"]+"', 'android:icon="@drawable/gv_app_icon_9if"', text, count=1)
    text = re.sub(r'android:label="[^"]+"', 'android:label="GALAXY VIEWER 9I-F"', text, count=1)
    manifest.write_text(text, encoding='utf-8')

    gradle = ANDROID / 'app/build.gradle'
    text = gradle.read_text(encoding='utf-8')
    text = re.sub(r'versionCode\s+\d+', 'versionCode 12', text, count=1)
    text = re.sub(r"versionName\s+'[^']+'", "versionName '9I-F'", text, count=1)
    gradle.write_text(text, encoding='utf-8')

    main = ANDROID / 'app/src/main/java/com/gear66me/galaxyviewer9i/MainActivity.java'
    text = main.read_text(encoding='utf-8')
    text = re.sub(r'private static final String APP_URL = "[^"]+";', 'private static final String APP_URL = "file:///android_asset/index.html";', text, count=1)
    text = text.replace('settings.setAllowFileAccess(false);', 'settings.setAllowFileAccess(true);')
    text = text.replace('settings.setAllowContentAccess(false);', 'settings.setAllowContentAccess(true);')
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
    main.write_text(text.replace(old, new, 1), encoding='utf-8')


def main():
    patch_viewer()
    if '--viewer-only' in __import__('sys').argv:
        return
    build_local_shell()
    patch_android()


if __name__ == '__main__':
    main()
