from pathlib import Path
import base64
import re
import subprocess
import prepare_galaxy_viewer_9ij as base

ROOT=Path(__file__).resolve().parents[2]
VIEWER=ROOT/'viewer/GV-beta-0009I.py'
ANDROID=ROOT/'android/galaxy-viewer-9i'
ASSETS=ANDROID/'app/src/main/assets'
EXPECTED_VIEWER='d2a0b57e0aad3c47bfd6b224ea5da24a5632f35d'
ICON_SHA='47b3e714053bfd64f835d3f1a2510e13618dbede'
MODULES=[
    'gv-hamburger-menu-0002.js',
    'gv-coordinate-overlay-0004.js',
    'gv-target-simbad-0001.js',
    'gv-random-galaxy-0028.js',
]


def hash_object(path):
    return subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip()


def patch_viewer():
    if hash_object(VIEWER)!=EXPECTED_VIEWER:
        raise SystemExit('REFUSING 9I-L: active beta Viewer blob is not verified 9I-K')
    text=VIEWER.read_text(encoding='utf-8')
    old="    const DISPLAY_VERSION='9I-K';"
    if text.count(old)!=1:
        raise SystemExit('REFUSING 9I-L: expected exactly one 9I-K DISPLAY_VERSION')
    if "document.dispatchEvent(new CustomEvent('gv-viewer-ready'" not in text:
        raise SystemExit('REFUSING 9I-L: Viewer READY event missing')
    if "document.dispatchEvent(new CustomEvent('gv-viewer-failed'" not in text:
        raise SystemExit('REFUSING 9I-L: Viewer FAILED event missing')
    VIEWER.write_text(text.replace(old,"    const DISPLAY_VERSION='9I-L';",1),encoding='utf-8')


def add_packaged_splash_bridge():
    p=ASSETS/'splash/index.html'
    s=p.read_text(encoding='utf-8')
    needle="window.dispatchEvent(new CustomEvent('galaxy-splash-complete'))"
    if s.count(needle)!=2:
        raise SystemExit('REFUSING 9I-L: expected exactly two splash completion exits')
    bridge=needle+";try{parent.postMessage('galaxy-splash-complete','*')}catch(_){}"
    s=s.replace(needle,bridge)
    p.write_text(s,encoding='utf-8')


def embed_modules_as_data_urls():
    p=ASSETS/'index.html'
    s=p.read_text(encoding='utf-8')
    replacements={
        'gv-hamburger-menu-0002.js':'HAMBURGER_URL',
        'gv-coordinate-overlay-0004.js':'COORDINATE_URL',
        'gv-target-simbad-0001.js':'TARGET_URL',
        'gv-random-galaxy-0028.js':'RANDOM_GALAXY_URL',
    }
    for name,const_name in replacements.items():
        source=(ROOT/'viewer/modules'/name).read_bytes()
        payload=base64.b64encode(source).decode('ascii')
        data_url=f"data:text/javascript;base64,{payload}"
        old=f"const {const_name}='modules/{name}';"
        new=f"const {const_name}='{data_url}';"
        if s.count(old)!=1:
            raise SystemExit(f'REFUSING 9I-L: expected one generated local-module replacement for {name}')
        s=s.replace(old,new,1)
        s=s.replace(f"modules/{name}",data_url)
    p.write_text(s,encoding='utf-8')


def patch_generated_identity():
    index=ASSETS/'index.html'
    s=index.read_text(encoding='utf-8').replace('9I-J','9I-L')
    index.write_text(s,encoding='utf-8')

    gradle=ANDROID/'app/build.gradle'
    g=gradle.read_text(encoding='utf-8')
    g=re.sub(r'versionCode\s+\d+','versionCode 18',g,count=1)
    g=re.sub(r"versionName\s+'[^']+'","versionName '9I-L'",g,count=1)
    gradle.write_text(g,encoding='utf-8')

    manifest=ANDROID/'app/src/main/AndroidManifest.xml'
    m=manifest.read_text(encoding='utf-8')
    m=re.sub(r'android:label="[^"]+"','android:label="GALAXY VIEWER 9I-L"',m,count=1)
    manifest.write_text(m,encoding='utf-8')


def verify():
    if hash_object(ANDROID/'app/src/main/res/drawable/gv_app_icon.png')!=ICON_SHA:
        raise SystemExit('REFUSING 9I-L: existing Android icon changed')
    index=(ASSETS/'index.html').read_text(encoding='utf-8')
    if 'gv-viewer-ready' not in index or 'gv-viewer-failed' not in index:
        raise SystemExit('REFUSING 9I-L: deterministic Viewer gate missing')
    if 'homeReady' in index or 'root&&aladin&&canvas' in index:
        raise SystemExit('REFUSING 9I-L: obsolete readiness heuristic survived')
    for name in MODULES:
        if f"modules/{name}" in index:
            raise SystemExit(f'REFUSING 9I-L: runtime local-module path survived: {name}')
    if index.count('data:text/javascript;base64,')<4:
        raise SystemExit('REFUSING 9I-L: fewer than four embedded module payloads')
    splash=(ASSETS/'splash/index.html').read_text(encoding='utf-8')
    if splash.count("parent.postMessage('galaxy-splash-complete','*')")!=2:
        raise SystemExit('REFUSING 9I-L: splash completion bridge missing')
    catalog=ASSETS/'data/gv-hubble-galaxies-full-0002.json'
    if not catalog.exists() or '"categoryEntryCount": 1879' not in catalog.read_text(encoding='utf-8'):
        raise SystemExit('REFUSING 9I-L: bundled 1879-entry catalog invariant failed')


def main():
    base.patch_viewer=patch_viewer
    base.main()
    add_packaged_splash_bridge()
    embed_modules_as_data_urls()
    patch_generated_identity()
    verify()


if __name__=='__main__':
    main()
