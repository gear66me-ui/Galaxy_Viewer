from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'android/galaxy-viewer-10e'
A = P / 'app/src/main/assets'

# Keep the existing R3 metadata because the proven completed workflow validates it.
p = P / 'app/build.gradle'
s = p.read_text()
s = s.replace("applicationId 'com.gear66me.galaxyviewer10e.generic'", "applicationId 'com.gear66me.galaxyviewer10g'")
s = s.replace("versionCode 1010", "versionCode 1013")
s = s.replace("versionName '10E-generic-permanent-1'", "versionName '10G-flattened-3'")
p.write_text(s)

p = P / 'app/src/main/AndroidManifest.xml'
p.write_text(p.read_text().replace('android:label="Galaxy Viewer 10E"', 'android:label="Galaxy Viewer 10G"'))

# Preserve the proven 10E WebView behavior; only change visible identity/user agent.
p = P / 'app/src/main/java/com/gear66me/galaxyviewer10e/MainActivity.java'
s = p.read_text()
s = s.replace('GalaxyViewer10E/10E-generic', 'GalaxyViewer10G/10G-proven-shell')
s = s.replace('GALAXY VIEWER 10E\\n\\n', 'GALAXY VIEWER 10G\\n\\n')
p.write_text(s)

# Dedicated bootstrap: exact proven generic-shell pattern, fixed to frozen 10F + 10G INFO.
# IMPORTANT: splash and Viewer are deliberately SERIALIZED.  The previous launcher started
# Aladin/WebGL behind the animated splash, causing competing GPU/WebGL startup workloads.
bootstrap = r'''(async()=>{'use strict';
const BASELINE='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/a88b56749bd73efe166e0a849749f15d03fed47d/viewer/GV-beta-0010F.py';
const INFO='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/modules/gv-info-module-0001.js';
const c=document.getElementById('gv-apk-cover');
const p=document.getElementById('gv-splash-frame');
const e=document.getElementById('gv-launch-error');
const text=async u=>{const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status+' '+u);return r.text()};
const run=s=>{const x=document.createElement('script');x.textContent=s;document.body.appendChild(x)};
const set10G=()=>{const nodes=[...document.querySelectorAll('#gv-apk-cover .v,#gv-apk-cover .gv-10e-version')];if(nodes.length){nodes[0].textContent='VERSION 10G';nodes.slice(1).forEach(n=>n.remove())}const v=document.getElementById('gv-version-label');if(v){v.textContent='VERSION 10G';v.setAttribute('aria-label','GALAXY VIEWER VERSION 10G')}if(window.GalaxyViewerInfo10G)window.GalaxyViewerInfo10G.refresh()};
const extract=s=>{const h=[...s.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)],j=[...s.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];if(h.length!==1||j.length!==1)throw new Error('Viewer extraction failed');return[h[0][1],j[0][1]]};
const waitViewer=()=>new Promise((ok,no)=>{const d=performance.now()+45000;let settled=false;const fail=err=>{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);no(err)};const pass=()=>{if(settled)return;settled=true;document.removeEventListener('gv-viewer-failed',viewerFailed);ok()};const viewerFailed=event=>fail(new Error(String(event?.detail?.message||'10F Viewer startup failed')));document.addEventListener('gv-viewer-failed',viewerFailed,{once:true});const q=()=>{if(settled)return;try{const root=document.getElementById('aladin-cosmic-command-test');if(root?.querySelector('canvas')&&window.aladin_cosmic_command_test)return pass();if(performance.now()>d)return fail(new Error('10G Viewer readiness timeout'));setTimeout(q,50)}catch(z){fail(z)}};q()});
const startViewer=async()=>{const source=await text(BASELINE);const[h,j]=extract(source);document.body.insertAdjacentHTML('beforeend',h);set10G();run(j);set10G();await waitViewer();run(await text(INFO));set10G();setTimeout(set10G,500);setTimeout(set10G,1800);return true};
const runSplash=()=>new Promise((ok,no)=>{let timer=0,done=false;const finish=()=>{if(done)return;done=true;if(timer)clearTimeout(timer);ok()};p.addEventListener('load',()=>{try{p.contentWindow.addEventListener('galaxy-splash-complete',finish,{once:true});p.style.visibility='visible';c?.remove();timer=setTimeout(()=>no(new Error('10G splash completion timeout')),22000)}catch(z){no(z)}},{once:true});p.addEventListener('error',()=>no(new Error('10G splash failed to load')),{once:true});p.src='viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html'});
try{
  /* Surgical GPU fix: never initialize Aladin/WebGL concurrently with the animated splash. */
  await runSplash();
  p.remove();
  await new Promise(requestAnimationFrame);
  await startViewer();
  c?.remove();
  set10G();
}catch(z){e.style.display='block';e.textContent='GALAXY VIEWER 10G FAILED TO LOAD\n\n'+String(z?.stack||z)}})();'''

head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 10G</title><style>@font-face{font-family:"Space Age";src:url("artwork/Space-Age.otf") format("opentype");font-style:normal;font-weight:400;font-display:block}*{box-sizing:border-box;font-family:"Space Age",sans-serif!important}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(58vw,280px);height:min(58vw,280px);max-width:280px;max-height:280px;object-fit:contain;object-position:center;background:transparent}.v{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}#gv-splash-frame{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000;visibility:hidden}#gv-launch-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;background:#000;color:#FFD85A;white-space:pre-wrap;font:400 14px/1.45 "Space Age",sans-serif}</style></head><body><div id="gv-apk-cover"><img src="artwork/icon.svg" alt="GALAXY VIEWER"><div class="v">VERSION 10G</div></div><iframe id="gv-splash-frame"></iframe><div id="gv-launch-error"></div>'''
out = head + '<script>' + bootstrap + '</script></body></html>'
(A / 'index.html').write_text(out)

text_out = (A / 'index.html').read_text()
assert 'VERSION 10G' in text_out
assert 'GalaxyViewerInfo10G' in text_out
assert 'GV-beta-0010G.py' not in text_out
assert 'fetch(VIEWER_URL' not in text_out
assert 'font-family:"Space Age",sans-serif!important' in text_out
assert 'GV-beta-0010F.py' in text_out
assert 'gv-info-module-0001.js' in text_out
assert 'await runSplash();' in text_out
assert text_out.index('await runSplash();') < text_out.index('await startViewer();')
print('10G serialized-startup index bytes:', len(text_out.encode()))
