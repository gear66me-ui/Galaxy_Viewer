from pathlib import Path
import re
import subprocess
import prepare_galaxy_viewer_9ij as base

ROOT=Path(__file__).resolve().parents[2]
VIEWER=ROOT/'viewer/GV-beta-0009I.py'
ANDROID=ROOT/'android/galaxy-viewer-9i'
ASSETS=ANDROID/'app/src/main/assets'
EXPECTED_VIEWER='e5d768aee94f12b4d15e22d08443a6a1fbb796e4'
ICON_SHA='47b3e714053bfd64f835d3f1a2510e13618dbede'


def hash_object(path):
    return subprocess.check_output(['git','hash-object',str(path)],cwd=ROOT,text=True).strip()


def patch_viewer():
    if hash_object(VIEWER)!=EXPECTED_VIEWER:
        raise SystemExit('REFUSING 9I-K: active beta Viewer blob is not verified 9I-J')
    text=VIEWER.read_text(encoding='utf-8')
    old="    const DISPLAY_VERSION='9I-J';"
    if text.count(old)!=1:
        raise SystemExit('REFUSING 9I-K: expected exactly one 9I-J DISPLAY_VERSION')
    if "document.dispatchEvent(new CustomEvent('gv-viewer-ready'" not in text:
        raise SystemExit('REFUSING 9I-K: Viewer READY event missing')
    if "document.dispatchEvent(new CustomEvent('gv-viewer-failed'" not in text:
        raise SystemExit('REFUSING 9I-K: Viewer FAILED event missing')
    VIEWER.write_text(text.replace(old,"    const DISPLAY_VERSION='9I-K';",1),encoding='utf-8')


def patch_packaged_splash():
    p=ASSETS/'splash/index.html'
    s=p.read_text(encoding='utf-8')
    needle="window.dispatchEvent(new CustomEvent('galaxy-splash-complete'))"
    count=s.count(needle)
    if count!=2:
        raise SystemExit(f'REFUSING 9I-K: expected 2 splash completion exits, found {count}')
    bridge=needle+";try{parent.postMessage('galaxy-splash-complete','*')}catch(_){}"
    s=s.replace(needle,bridge)
    p.write_text(s,encoding='utf-8')
    if s.count("parent.postMessage('galaxy-splash-complete','*')")!=2:
        raise SystemExit('REFUSING 9I-K: packaged splash bridge verification failed')


def patch_generated_identity():
    index=ASSETS/'index.html'
    s=index.read_text(encoding='utf-8').replace('9I-J','9I-K')
    index.write_text(s,encoding='utf-8')

    gradle=ANDROID/'app/build.gradle'
    g=gradle.read_text(encoding='utf-8')
    g=re.sub(r'versionCode\s+\d+','versionCode 17',g,count=1)
    g=re.sub(r"versionName\s+'[^']+'","versionName '9I-K'",g,count=1)
    gradle.write_text(g,encoding='utf-8')

    manifest=ANDROID/'app/src/main/AndroidManifest.xml'
    m=manifest.read_text(encoding='utf-8')
    m=re.sub(r'android:label="[^"]+"','android:label="GALAXY VIEWER 9I-K"',m,count=1)
    manifest.write_text(m,encoding='utf-8')


def verify():
    if hash_object(ANDROID/'app/src/main/res/drawable/gv_app_icon.png')!=ICON_SHA:
        raise SystemExit('REFUSING 9I-K: existing Android icon changed')
    index=(ASSETS/'index.html').read_text(encoding='utf-8')
    if 'gv-viewer-ready' not in index or 'gv-viewer-failed' not in index:
        raise SystemExit('REFUSING 9I-K: deterministic Viewer gate missing')
    if 'homeReady' in index or 'root&&aladin&&canvas' in index:
        raise SystemExit('REFUSING 9I-K: obsolete readiness heuristic survived')
    splash=(ASSETS/'splash/index.html').read_text(encoding='utf-8')
    if splash.count("parent.postMessage('galaxy-splash-complete','*')")!=2:
        raise SystemExit('REFUSING 9I-K: splash bridge missing after packaging')


def main():
    base.patch_viewer=patch_viewer
    base.main()
    patch_packaged_splash()
    patch_generated_identity()
    verify()


if __name__=='__main__':
    main()
