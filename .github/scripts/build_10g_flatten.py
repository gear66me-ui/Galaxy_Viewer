from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'android/galaxy-viewer-10e'
A = P / 'app/src/main/assets'
BASE = ROOT / 'viewer/GV-beta-0010F.py'
TEN_G = ROOT / 'viewer/GV-beta-0010G.py'
INFO = ROOT / 'viewer/modules/gv-info-module-0001.js'

# -----------------------------------------------------------------------------
# 1) MATERIALIZE 10G AS A TRUE STANDALONE RELEASE.
#    10F is used only as a one-time source baseline during build generation.
#    The resulting GV-beta-0010G.py contains the implementation itself and has
#    ZERO runtime dependency on GV-beta-0010F.py or any prior Viewer .py file.
# -----------------------------------------------------------------------------
base = BASE.read_text(encoding='utf-8')
info = INFO.read_text(encoding='utf-8')

# Promote the frozen baseline identity to 10G without changing Viewer behavior.
standalone = base.replace('10F', '10G')
standalone = standalone.replace(
    '# GV-beta-0010G\n',
    '# GV-beta-0010G\n# STANDALONE RELEASE: contains its own Viewer implementation; no prior-release .py is loaded at runtime.\n',
    1,
)

# Inline the authorized 10G INFO feature into the release itself.  This removes
# the extra runtime fetch for the INFO module and makes the 10G release payload
# self-contained with respect to its 10G-specific feature.
info = info.replace(
    'const inst=global.galaxyRandomGalaxy||global.randomGalaxy||null;',
    'const inst=global.GV10G?.randomGalaxy||global.GV10E?.randomGalaxy||global.__gv10eRandomGalaxy||global.galaxyRandomGalaxy||global.randomGalaxy||null;'
)
inline_info = '\n\ndisplay(Javascript(r"""\n' + info.rstrip() + '\n"""))\n'
standalone = standalone.rstrip() + inline_info + '\n# GV-beta-0010G standalone\n'

# Hard release-boundary assertions.
for forbidden in (
    'GV-beta-0010F.py',
    'BASELINE_URL=',
    'could not extract frozen 10F baseline',
):
    assert forbidden not in standalone, f'forbidden prior-release dependency remains: {forbidden}'
assert "const VERSION='10G';" in standalone
assert "const DISPLAY_VERSION='10G';" in standalone
assert "VERSION 10G" in standalone
assert 'GalaxyViewerInfo10G' in standalone
TEN_G.write_text(standalone, encoding='utf-8')

# -----------------------------------------------------------------------------
# 2) PACKAGE THE STANDALONE 10G RELEASE DIRECTLY INTO THE APK.
#    No runtime .py fetch. No runtime 10F composition.
# -----------------------------------------------------------------------------
html_blocks = re.findall(r'display\(HTML\("""([\s\S]*?)"""\)\)', standalone)
js_blocks = re.findall(r'display\(Javascript\(r"""([\s\S]*?)"""\)\)', standalone)
assert len(html_blocks) >= 1, 'standalone 10G HTML extraction failed'
assert len(js_blocks) >= 2, 'standalone 10G JavaScript extraction failed'
viewer_html = ''.join(html_blocks)
viewer_js = js_blocks

# Android package identity.
p = P / 'app/build.gradle'
s = p.read_text(encoding='utf-8')
s = s.replace("applicationId 'com.gear66me.galaxyviewer10e.generic'", "applicationId 'com.gear66me.galaxyviewer10g'")
s = s.replace("versionCode 1010", "versionCode 1014")
s = s.replace("versionName '10E-generic-permanent-1'", "versionName '10G-standalone-1'")
s = s.replace("versionCode 1013", "versionCode 1014")
s = s.replace("versionName '10G-flattened-3'", "versionName '10G-standalone-1'")
p.write_text(s, encoding='utf-8')

p = P / 'app/src/main/AndroidManifest.xml'
s = p.read_text(encoding='utf-8').replace('android:label="Galaxy Viewer 10E"', 'android:label="Galaxy Viewer 10G"')
p.write_text(s, encoding='utf-8')

p = P / 'app/src/main/java/com/gear66me/galaxyviewer10e/MainActivity.java'
s = p.read_text(encoding='utf-8')
s = s.replace('GalaxyViewer10E/10E-generic', 'GalaxyViewer10G/10G-standalone')
s = s.replace('GalaxyViewer10G/10G-proven-shell', 'GalaxyViewer10G/10G-standalone')
s = s.replace('GALAXY VIEWER 10E\\n\\n', 'GALAXY VIEWER 10G\\n\\n')
p.write_text(s, encoding='utf-8')

vh = json.dumps(viewer_html)
vj = json.dumps(viewer_js)

bootstrap = f'''(async()=>{{'use strict';
const VIEWER_HTML={vh};
const VIEWER_JS={vj};
const c=document.getElementById('gv-apk-cover');
const p=document.getElementById('gv-splash-frame');
const e=document.getElementById('gv-launch-error');
const run=s=>{{const x=document.createElement('script');x.textContent=s;document.body.appendChild(x)}};
const waitViewer=()=>new Promise((ok,no)=>{{const d=performance.now()+45000;let settled=false;const fail=err=>{{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);no(err)}};const pass=()=>{{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);ok()}};const viewerFailed=event=>fail(new Error(String(event?.detail?.message||'10G Viewer startup failed')));document.addEventListener('gv-viewer-failed',viewerFailed,{{once:true}});const q=()=>{{if(settled)return;try{{const root=document.getElementById('aladin-cosmic-command-test');if(root?.querySelector('canvas')&&window.aladin_cosmic_command_test)return pass();if(performance.now()>d)return fail(new Error('10G Viewer readiness timeout'));setTimeout(q,50)}}catch(z){{fail(z)}}}};q()}});
const startViewer=async()=>{{document.body.insertAdjacentHTML('beforeend',VIEWER_HTML);for(const source of VIEWER_JS)run(source);await waitViewer();const v=document.getElementById('gv-version-label');if(v)v.textContent='VERSION 10G';return true}};
const runSplash=()=>new Promise((ok,no)=>{{let timer=0,done=false;const finish=()=>{{if(done)return;done=true;if(timer)clearTimeout(timer);ok()}};p.addEventListener('load',()=>{{try{{p.contentWindow.addEventListener('galaxy-splash-complete',finish,{{once:true}});p.style.visibility='visible';c?.remove();timer=setTimeout(()=>no(new Error('10G splash completion timeout')),22000)}}catch(z){{no(z)}}}},{{once:true}});p.addEventListener('error',()=>no(new Error('10G splash failed to load')),{{once:true}});p.src='viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html'}});
try{{
  /* GPU-safe startup: splash completes and its WebGL surface is removed before Aladin starts. */
  await runSplash();
  p.remove();
  await new Promise(requestAnimationFrame);
  await startViewer();
  c?.remove();
}}catch(z){{e.style.display='block';e.textContent='GALAXY VIEWER 10G FAILED TO LOAD\\n\\n'+String(z?.stack||z)}}}})();'''

head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 10G</title><style>@font-face{font-family:"Space Age";src:url("artwork/Space-Age.otf") format("opentype");font-style:normal;font-weight:400;font-display:block}*{box-sizing:border-box;font-family:"Space Age",sans-serif!important}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(58vw,280px);height:min(58vw,280px);max-width:280px;max-height:280px;object-fit:contain;object-position:center;background:transparent}.v{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}#gv-splash-frame{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000;visibility:hidden}#gv-launch-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;background:#000;color:#FFD85A;white-space:pre-wrap;font:400 14px/1.45 "Space Age",sans-serif}</style></head><body><div id="gv-apk-cover"><img src="artwork/icon.svg" alt="GALAXY VIEWER"><div class="v">VERSION 10G</div></div><iframe id="gv-splash-frame"></iframe><div id="gv-launch-error"></div>'''
out = head + '<script>' + bootstrap + '</script></body></html>'
(A / 'index.html').write_text(out, encoding='utf-8')

text_out = (A / 'index.html').read_text(encoding='utf-8')
assert 'VERSION 10G' in text_out
assert 'GalaxyViewerInfo10G' in text_out
assert 'font-family:"Space Age",sans-serif!important' in text_out
assert 'GV-beta-0010F.py' not in text_out
assert 'GV-beta-0010G.py' not in text_out
assert 'BASELINE_URL=' not in text_out
assert 'await runSplash();' in text_out and 'await startViewer();' in text_out
assert text_out.index('await runSplash();') < text_out.index('await startViewer();')
print('Standalone 10G source bytes:', TEN_G.stat().st_size)
print('Embedded 10G APK index bytes:', len(text_out.encode('utf-8')))
