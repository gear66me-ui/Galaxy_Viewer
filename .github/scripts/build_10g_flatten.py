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
viewer_js = list(js_blocks)

# FORENSIC-ONLY instrumentation. This modifies only the disposable APK copy;
# viewer/GV-beta-0010G.py remains byte-for-byte untouched. No timing, state,
# geometry, splash, Random Galaxy, or Viewer behavior is intentionally changed.
def replace_once(source, old, new, label):
    assert old in source, f'forensic marker target missing: {label}'
    return source.replace(old, new, 1)

main = viewer_js[0]
main = replace_once(main, "    'use strict';", "    'use strict';\n    const __gvTrace=(name,data='')=>console.info('[GV10G_TRACE]',Math.round(performance.now()),name,data);\n    __gvTrace('VIEWER_MAIN_JS_START');", 'viewer main start')
main = replace_once(main, "    const A=await ensureAladin();", "    __gvTrace('ALADIN_SCRIPT_LOAD_START');\n    const A=await ensureAladin();\n    __gvTrace('ALADIN_SCRIPT_LOAD_COMPLETE');", 'Aladin load')
main = replace_once(main, "    window.aladin_cosmic_command_test=aladin;", "    window.aladin_cosmic_command_test=aladin;\n    __gvTrace('ALADIN_INSTANCE_CREATED');", 'Aladin instance')
main = replace_once(main, "    await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0031');", "    __gvTrace('RANDOM_MODULE_LOAD_START');\n    await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0031');\n    __gvTrace('RANDOM_MODULE_LOAD_COMPLETE',{version:window.GalaxyRandomGalaxy?.VERSION||null});", 'Random module load')
main = replace_once(main, "    const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomGalaxyHost,{", "    __gvTrace('RANDOM_MOUNT_START');\n    const randomGalaxy=window.GalaxyRandomGalaxy.mount(randomGalaxyHost,{", 'Random mount')
main = replace_once(main, "    window.__gv10eRandomGalaxy=randomGalaxy;\n    await randomGalaxy.ready;\n    bottom.random.disabled=false;", "    window.__gv10eRandomGalaxy=randomGalaxy;\n    __gvTrace('RANDOM_CONSTRUCTED',{hasReady:!!randomGalaxy?.ready});\n    __gvTrace('RANDOM_READY_START');\n    try{await randomGalaxy.ready;__gvTrace('RANDOM_READY_RESOLVED',randomGalaxy.getState?.()||null)}catch(error){__gvTrace('RANDOM_READY_REJECTED',String(error?.stack||error));throw error}\n    bottom.random.disabled=false;\n    __gvTrace('RANDOM_BUTTON_ENABLED',{disabled:bottom.random.disabled});", 'Random ready')
main = replace_once(main, "    const launchRandomGalaxy=()=>{\n        if(navigationPending||randomGalaxy.getState().busy)return;\n        randomGalaxy.travelToRandom().catch(error=>{", "    const launchRandomGalaxy=()=>{\n        const __state=randomGalaxy.getState?.()||{};\n        __gvTrace('RANDOM_CLICK_HANDLER_ENTER',{navigationPending,busy:!!__state.busy,disabled:bottom.random.disabled});\n        if(navigationPending||__state.busy){__gvTrace('RANDOM_CLICK_BLOCKED',{navigationPending,busy:!!__state.busy});return;}\n        __gvTrace('TRAVEL_TO_RANDOM_START');\n        randomGalaxy.travelToRandom().then(()=>__gvTrace('TRAVEL_TO_RANDOM_RESOLVED')).catch(error=>{\n            __gvTrace('TRAVEL_TO_RANDOM_REJECTED',String(error?.stack||error));", 'Random click path')
main = replace_once(main, "    bottom.random.addEventListener('click',launchRandomGalaxy);", "    bottom.random.addEventListener('pointerdown',()=>__gvTrace('POINTER_EVENT_RECEIVED'),{capture:true});\n    bottom.random.addEventListener('click',launchRandomGalaxy);\n    __gvTrace('RANDOM_CLICK_LISTENER_ATTACHED');", 'Random listener')
main = replace_once(main, "    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length}}));", "    __gvTrace('AUTHORITATIVE_VIEWER_READY',{randomReady:true,randomDisabled:bottom.random.disabled,state:randomGalaxy.getState?.()||null});\n    document.dispatchEvent(new CustomEvent('gv-viewer-ready',{detail:{version:VERSION,displayVersion:DISPLAY_VERSION,catalogCount:catalogRecordCount,eligibleCatalogCount:galaxyCatalog.length}}));", 'Authoritative Viewer ready')
main = replace_once(main, "})().catch(error=>{console.error('GALAXY VIEWER 10E STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});", "})().catch(error=>{console.info('[GV10G_TRACE]',Math.round(performance.now()),'VIEWER_MAIN_REJECTED',String(error?.stack||error));console.error('GALAXY VIEWER 10E STARTUP FAILURE:',error);document.dispatchEvent(new CustomEvent('gv-viewer-failed',{detail:{message:String(error?.stack||error)}}));});", 'Viewer failure')
viewer_js[0] = main

if len(viewer_js) > 1:
    info = viewer_js[1]
    info = "console.info('[GV10G_TRACE]',Math.round(performance.now()),'INFO_JS_START');\n" + info
    info = replace_once(info, "global.GalaxyViewerInfo10G=Object.freeze({", "console.info('[GV10G_TRACE]',Math.round(performance.now()),'INFO_MODULE_READY');\nglobal.GalaxyViewerInfo10G=Object.freeze({", 'Info ready')
    viewer_js[1] = info

# Build in a disposable copy. Existing repository Android projects remain
# byte-for-byte untouched by packaging.
if BUILD_PROJECT.exists():
    shutil.rmtree(BUILD_PROJECT)
shutil.copytree(SOURCE_PROJECT, BUILD_PROJECT)
A = BUILD_PROJECT / 'app/src/main/assets'

for legacy in (
    A / 'bootstrap-fallback.js',
    A / 'viewer/gv-current-viewer.json',
    A / 'viewer/GV-beta-0010E.py',
):
    if legacy.exists():
        legacy.unlink()
assert not list((A / 'viewer').glob('GV-beta-*.py')), 'prior-release Viewer .py asset remains in disposable APK tree'
assert not (A / 'bootstrap-fallback.js').exists()
assert not (A / 'viewer/gv-current-viewer.json').exists()

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

legacy_dir = old_java.parent
while legacy_dir != BUILD_PROJECT / 'app/src/main/java' and legacy_dir.exists():
    try:
        legacy_dir.rmdir()
    except OSError:
        break
    legacy_dir = legacy_dir.parent

# HTML parses raw script text before JavaScript parses string literals. Escape
# only that parser sentinel; JavaScript restores the runtime value.
vh = json.dumps(viewer_html).replace('</script', '<\\/script')
vj = json.dumps(viewer_js).replace('</script', '<\\/script')

# Forensic baseline: preserve the pre-timeout startup behavior exactly. No
# splash deadlock workaround is active while the shared initialization race is
# being measured.
bootstrap = f'''(async()=>{{'use strict';
const VIEWER_HTML={vh};
const VIEWER_JS={vj};
const VIEWER_TIMEOUT_MS=45000,SPLASH_FIRST_FRAME_TIMEOUT_MS=5000,ICON_MIN_HOLD_MS=3500,launchStartedAt=performance.now();
const trace=(name,data='')=>console.info('[GV10G_TRACE]',Math.round(performance.now()),name,data);
trace('APK_BOOTSTRAP_START');
const launchCover=document.getElementById('gv-apk-cover');
const splashFrame=document.getElementById('gv-splash-frame');
const errorBox=document.getElementById('gv-launch-error');
const showError=e=>{{trace('APK_FAILURE',String(e?.stack||e));errorBox.style.display='block';errorBox.textContent='GALAXY VIEWER 10G FAILED TO LOAD\\n\\n'+String(e?.stack||e)}};
const run=(s,index)=>{{trace('EMBEDDED_JS_EXECUTE',index);const x=document.createElement('script');x.textContent=s;document.body.appendChild(x)}};
const mountViewerHtml=()=>{{
  trace('VIEWER_HTML_MOUNT_START');
  const t=document.createElement('template');t.innerHTML=VIEWER_HTML;
  let embeddedIndex=0;
  for(const old of [...t.content.querySelectorAll('script')]){{
    const fresh=document.createElement('script');
    for(const a of [...old.attributes])fresh.setAttribute(a.name,a.value);
    fresh.textContent=old.textContent;
    old.replaceWith(fresh);
    trace('EMBEDDED_HTML_SCRIPT_PREPARED',embeddedIndex++);
  }}
  document.body.appendChild(t.content);
  trace('VIEWER_HTML_MOUNT_COMPLETE',{scripts:embeddedIndex});
}};
const waitForIconMinimum=()=>new Promise(resolve=>setTimeout(resolve,Math.max(0,ICON_MIN_HOLD_MS-(performance.now()-launchStartedAt))));
const waitForViewer=()=>new Promise((resolve,reject)=>{{
  const deadline=performance.now()+VIEWER_TIMEOUT_MS;let settled=false;
  const fail=err=>{{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);reject(err)}};
  const pass=()=>{{if(settled)return;settled=true;trace('APK_WEAK_READY_CONDITION_PASS',{hasGV10E:!!window.GV10E,randomReady:!!window.__gv10eRandomGalaxy,randomDisabled:document.getElementById('gv-random-galaxy')?.disabled});document.removeEventListener('gv-viewer-failed',viewerFailed);requestAnimationFrame(()=>requestAnimationFrame(resolve))}};
  const viewerFailed=event=>{{trace('GV_VIEWER_FAILED_EVENT',event?.detail||'');fail(new Error(String(event?.detail?.message||'10G Viewer startup failed')))}};
  document.addEventListener('gv-viewer-failed',viewerFailed,{{once:true}});
  document.addEventListener('gv-viewer-ready',event=>trace('GV_VIEWER_READY_EVENT',event?.detail||''),{{once:true}});
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
  trace('VIEWER_INIT_START');
  mountViewerHtml();
  VIEWER_JS.forEach((source,index)=>run(source,index));
  await waitForViewer();
  trace('VIEWER_INIT_WEAK_READY_RETURNED');
}};
const startSplash=async()=>{{
  trace('SPLASH_WAIT_ICON_START');
  await waitForIconMinimum();
  trace('SPLASH_START');
  return new Promise((resolve,reject)=>{{
    let done=false;
    const fail=e=>{{if(done)return;done=true;trace('SPLASH_FAILED',String(e?.stack||e));reject(e)}};
    splashFrame.addEventListener('load',()=>{{
      trace('SPLASH_IFRAME_LOAD');
      try{{
        const w=splashFrame.contentWindow;if(!w)throw new Error('SPLASH WINDOW UNAVAILABLE');
        w.addEventListener('galaxy-splash-complete',()=>{{if(done)return;done=true;trace('SPLASH_COMPLETE_EVENT');resolve()}},{{once:true}});
        const deadline=performance.now()+SPLASH_FIRST_FRAME_TIMEOUT_MS;
        const reveal=()=>{{
          try{{
            const d=w.document,scene=d.getElementById('scene'),poster=d.getElementById('poster');
            if(scene?.style.opacity==='1'||poster?.style.visibility==='visible'){{trace('SPLASH_FIRST_FRAME',{sceneOpacity:scene?.style.opacity||'',posterVisibility:poster?.style.visibility||''});if(launchCover?.isConnected)launchCover.remove();return}}
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
  trace('PROMISE_ALL_RESOLVED');
  requestAnimationFrame(()=>{{if(splashFrame?.isConnected)splashFrame.remove();if(launchCover?.isConnected)launchCover.remove();trace('HOME_REVEALED')}});
}}catch(e){{console.error('GALAXY VIEWER 10G APK FAILURE',e);showError(e)}}
}})();'''

head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 10G</title><style>@font-face{font-family:"Space Age";src:url("artwork/Space-Age.otf") format("opentype");font-style:normal;font-weight:400;font-display:block}*{box-sizing:border-box;font-family:"Space Age",sans-serif!important}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(58vw,280px);height:min(58vw,280px);max-width:280px;max-height:280px;object-fit:contain;object-position:center;background:transparent}.v{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}#gv-splash-frame{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000;visibility:visible}#gv-launch-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;background:#000;color:#FFD85A;white-space:pre-wrap;font:400 14px/1.45 "Space Age",sans-serif}</style></head><body><div id="gv-apk-cover"><img src="artwork/icon.svg" alt="GALAXY VIEWER"><div class="v">VERSION 10G</div></div><iframe id="gv-splash-frame" title="GALAXY VIEWER SPLASH"></iframe><div id="gv-launch-error" role="alert"></div>'''
out = head + '<script>' + bootstrap + '</script></body></html>'
(A / 'index.html').write_text(out, encoding='utf-8')

# Packaging assertions: positive identity, negative release boundary, and
# forensic-only instrumentation. The functional splash workaround is
# deliberately absent during this audit.
text_out = (A / 'index.html').read_text(encoding='utf-8')
assert 'VERSION 10G' in text_out
assert 'GalaxyViewerInfo10G' in text_out
assert 'font-family:"Space Age",sans-serif!important' in text_out
assert 'GV-beta-0010F.py' not in text_out
assert 'GV-beta-0010E.py' not in text_out
assert 'BASELINE_URL=' not in text_out
assert not re.search(r'GV-beta-[0-9A-Z-]+\.py', text_out, flags=re.I)
assert 'Promise.all([initializeViewer(),startSplash()])' in text_out
assert '[GV10G_TRACE]' in text_out
assert 'AUTHORITATIVE_VIEWER_READY' in text_out
assert 'APK_WEAK_READY_CONDITION_PASS' in text_out
assert 'SPLASH_COMPLETION_TIMEOUT_MS' not in text_out
assert text_out.lower().count('</script>') == 1

print('AUTHORITATIVE 10G SOURCE READ-ONLY:', TEN_G)
print('10G source bytes:', TEN_G.stat().st_size)
print('Disposable Android build:', BUILD_PROJECT)
print('Embedded APK index bytes:', len(text_out.encode('utf-8')))
print('FORENSIC TRACE MODE: initialization ordering only; no functional workaround')
