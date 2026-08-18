from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
SOURCE_PROJECT = ROOT / 'android/galaxy-viewer-10e'
BUILD_PROJECT = Path('/tmp/galaxy-viewer-10g-build')
TEN_G = ROOT / 'viewer/GV-beta-0010G.py'

# GALAXY VIEWER 10G APK PACKAGER
#
# CONTROL RULE:
#   10G already exists before packaging begins.
#   This script is a CONSUMER of 10G, never a CREATOR of 10G.
#   It must never write viewer/GV-beta-0010G.py or read an earlier Viewer
#   release as a source baseline.

assert TEN_G.is_file(), 'authoritative standalone 10G source is missing'
standalone = TEN_G.read_text(encoding='utf-8')

# Release-boundary gate: reject active prior-release Viewer dependencies.
for forbidden in (
    'GV-beta-0010F.py',
    'GV-beta-0010E.py',
    'BASELINE_URL=',
    'could not extract frozen 10F baseline',
    'could not extract frozen 10E baseline',
):
    assert forbidden not in standalone, f'forbidden prior-release dependency in 10G: {forbidden}'

# Any explicit Viewer .py URL in the standalone release is a release-boundary
# violation. Ordinary module/service URLs remain allowed.
viewer_py_urls = re.findall(r'https?://[^\s\"\']*GV-beta-[^\s\"\']+\.py[^\s\"\']*', standalone, flags=re.I)
assert not viewer_py_urls, f'forbidden runtime Viewer .py URL(s): {viewer_py_urls}'

assert "const VERSION='10G';" in standalone
assert "const DISPLAY_VERSION='10G';" in standalone
assert 'VERSION 10G' in standalone
assert 'GalaxyViewerInfo10G' in standalone

# Extract the already-complete 10G payload. No source reconstruction occurs.
html_blocks = re.findall(r'display\(HTML\("""([\s\S]*?)"""\)\)', standalone)
js_blocks = re.findall(r'display\(Javascript\(r"""([\s\S]*?)"""\)\)', standalone)
assert html_blocks, '10G HTML extraction failed'
assert js_blocks, '10G JavaScript extraction failed'
viewer_html = ''.join(html_blocks)
viewer_js = js_blocks

# Build in a disposable copy. Existing repository Android projects remain
# byte-for-byte untouched by packaging.
if BUILD_PROJECT.exists():
    shutil.rmtree(BUILD_PROJECT)
shutil.copytree(SOURCE_PROJECT, BUILD_PROJECT)
A = BUILD_PROJECT / 'app/src/main/assets'

# Dedicated 10G Android package identity in the disposable build tree.
p = BUILD_PROJECT / 'app/build.gradle'
s = p.read_text(encoding='utf-8')
s = re.sub(r"namespace\s+'[^']+'", "namespace 'com.gear66me.galaxyviewer10g'", s, count=1)
s = re.sub(r"applicationId\s+'[^']+'", "applicationId 'com.gear66me.galaxyviewer10g'", s, count=1)
s = re.sub(r'versionCode\s+\d+', 'versionCode 1015', s, count=1)
s = re.sub(r"versionName\s+'[^']+'", "versionName '10G-standalone-apk-2'", s, count=1)
assert "namespace 'com.gear66me.galaxyviewer10g'" in s
assert "applicationId 'com.gear66me.galaxyviewer10g'" in s
p.write_text(s, encoding='utf-8')

p = BUILD_PROJECT / 'app/src/main/AndroidManifest.xml'
s = p.read_text(encoding='utf-8').replace('android:label="Galaxy Viewer 10E"', 'android:label="Galaxy Viewer 10G"')
p.write_text(s, encoding='utf-8')

old_java = BUILD_PROJECT / 'app/src/main/java/com/gear66me/galaxyviewer10e/MainActivity.java'
new_java = BUILD_PROJECT / 'app/src/main/java/com/gear66me/galaxyviewer10g/MainActivity.java'
new_java.parent.mkdir(parents=True, exist_ok=True)
s = old_java.read_text(encoding='utf-8')
s = s.replace('package com.gear66me.galaxyviewer10e;', 'package com.gear66me.galaxyviewer10g;')
s = s.replace('GalaxyViewer10E/10E-generic', 'GalaxyViewer10G/10G-standalone-apk-2')
s = s.replace('GALAXY VIEWER 10E\\n\\n', 'GALAXY VIEWER 10G\\n\\n')
new_java.write_text(s, encoding='utf-8')
old_java.unlink()

# Remove now-empty legacy Java package directories from the disposable copy.
legacy_dir = old_java.parent
while legacy_dir != BUILD_PROJECT / 'app/src/main/java' and legacy_dir.exists():
    try:
        legacy_dir.rmdir()
    except OSError:
        break
    legacy_dir = legacy_dir.parent

vh = json.dumps(viewer_html)
vj = json.dumps(viewer_js)

# APK startup deliberately mirrors the approved dedicated 10G launcher:
# Viewer initialization begins immediately in parallel with the icon/splash
# sequence. This packaging repair does not redesign splash choreography.
bootstrap = f'''(async()=>{{'use strict';
const VIEWER_HTML={vh};
const VIEWER_JS={vj};
const VIEWER_TIMEOUT_MS=45000,SPLASH_FIRST_FRAME_TIMEOUT_MS=5000,ICON_MIN_HOLD_MS=3500,launchStartedAt=performance.now();
const launchCover=document.getElementById('gv-apk-cover');
const splashFrame=document.getElementById('gv-splash-frame');
const errorBox=document.getElementById('gv-launch-error');
const showError=e=>{{errorBox.style.display='block';errorBox.textContent='GALAXY VIEWER 10G FAILED TO LOAD\\n\\n'+String(e?.stack||e)}};
const run=s=>{{const x=document.createElement('script');x.textContent=s;document.body.appendChild(x)}};
const mountViewerHtml=()=>{{
  const t=document.createElement('template');t.innerHTML=VIEWER_HTML;
  for(const old of [...t.content.querySelectorAll('script')]){{
    const fresh=document.createElement('script');
    for(const a of [...old.attributes])fresh.setAttribute(a.name,a.value);
    fresh.textContent=old.textContent;
    old.replaceWith(fresh);
  }}
  document.body.appendChild(t.content);
}};
const waitForIconMinimum=()=>new Promise(resolve=>setTimeout(resolve,Math.max(0,ICON_MIN_HOLD_MS-(performance.now()-launchStartedAt))));
const waitForViewer=()=>new Promise((resolve,reject)=>{{
  const deadline=performance.now()+VIEWER_TIMEOUT_MS;let settled=false;
  const fail=err=>{{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);reject(err)}};
  const pass=()=>{{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);requestAnimationFrame(()=>requestAnimationFrame(resolve))}};
  const viewerFailed=event=>fail(new Error(String(event?.detail?.message||'10G Viewer startup failed')));
  document.addEventListener('gv-viewer-failed',viewerFailed,{{once:true}});
  const check=()=>{{
    if(settled)return;
    try{{
      const root=document.getElementById('aladin-cosmic-command-test');
      if(root?.querySelector('canvas')&&window.aladin_cosmic_command_test&&window.GalaxyViewerInfo10G)return pass();
      if(performance.now()>=deadline)return fail(new Error('GALAXY VIEWER 10G STARTUP TIMEOUT'));
      setTimeout(check,100);
    }}catch(e){{fail(e)}}
  }};
  check();
}});
const initializeViewer=async()=>{{
  mountViewerHtml();
  for(const source of VIEWER_JS)run(source);
  await waitForViewer();
}};
const startSplash=async()=>{{
  await waitForIconMinimum();
  return new Promise((resolve,reject)=>{{
    let done=false;
    const fail=e=>{{if(done)return;done=true;reject(e)}};
    splashFrame.addEventListener('load',()=>{{
      try{{
        const w=splashFrame.contentWindow;if(!w)throw new Error('SPLASH WINDOW UNAVAILABLE');
        w.addEventListener('galaxy-splash-complete',()=>{{if(done)return;done=true;resolve()}},{{once:true}});
        const deadline=performance.now()+SPLASH_FIRST_FRAME_TIMEOUT_MS;
        const reveal=()=>{{
          try{{
            const d=w.document,scene=d.getElementById('scene'),poster=d.getElementById('poster');
            if(scene?.style.opacity==='1'||poster?.style.visibility==='visible'){{if(launchCover?.isConnected)launchCover.remove();return}}
            if(performance.now()>=deadline)return fail(new Error('SPLASH FIRST FRAME TIMEOUT'));
            requestAnimationFrame(reveal);
          }}catch(e){{fail(e)}}
        }};
        requestAnimationFrame(reveal);
      }}catch(e){{fail(e)}}
    }},{{once:true}});
    splashFrame.addEventListener('error',()=>fail(new Error('SPLASH FAILED TO LOAD')),{{once:true}});
    splashFrame.src='viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html';
  }});
}};
try{{
  await Promise.all([initializeViewer(),startSplash()]);
  requestAnimationFrame(()=>{{if(splashFrame?.isConnected)splashFrame.remove();if(launchCover?.isConnected)launchCover.remove()}});
}}catch(e){{console.error('GALAXY VIEWER 10G APK FAILURE',e);showError(e)}}
}})();'''

head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 10G</title><style>@font-face{font-family:"Space Age";src:url("artwork/Space-Age.otf") format("opentype");font-style:normal;font-weight:400;font-display:block}*{box-sizing:border-box;font-family:"Space Age",sans-serif!important}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(58vw,280px);height:min(58vw,280px);max-width:280px;max-height:280px;object-fit:contain;object-position:center;background:transparent}.v{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}#gv-splash-frame{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000;visibility:visible}#gv-launch-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;background:#000;color:#FFD85A;white-space:pre-wrap;font:400 14px/1.45 "Space Age",sans-serif}</style></head><body><div id="gv-apk-cover"><img src="artwork/icon.svg" alt="GALAXY VIEWER"><div class="v">VERSION 10G</div></div><iframe id="gv-splash-frame" title="GALAXY VIEWER SPLASH"></iframe><div id="gv-launch-error" role="alert"></div>'''
out = head + '<script>' + bootstrap + '</script></body></html>'
(A / 'index.html').write_text(out, encoding='utf-8')

# Packaging assertions: positive 10G identity, negative prior-release boundary.
text_out = (A / 'index.html').read_text(encoding='utf-8')
assert 'VERSION 10G' in text_out
assert 'GalaxyViewerInfo10G' in text_out
assert 'font-family:"Space Age",sans-serif!important' in text_out
assert 'GV-beta-0010F.py' not in text_out
assert 'GV-beta-0010E.py' not in text_out
assert 'BASELINE_URL=' not in text_out
assert not re.search(r'GV-beta-[0-9A-Z-]+\.py', text_out, flags=re.I)
assert 'Promise.all([initializeViewer(),startSplash()])' in text_out

print('AUTHORITATIVE 10G SOURCE READ-ONLY:', TEN_G)
print('10G source bytes:', TEN_G.stat().st_size)
print('Disposable Android build:', BUILD_PROJECT)
print('Embedded APK index bytes:', len(text_out.encode('utf-8')))
