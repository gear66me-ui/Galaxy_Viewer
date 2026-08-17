from pathlib import Path
import re
import shutil
import subprocess


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected one match, found {n}')
    return text.replace(old, new, 1)


old = Path('viewer/modules/gv-random-galaxy-0028.js')
new = Path('viewer/modules/gv-random-galaxy-0029.js')
if new.exists():
    raise SystemExit('0029 already exists')
if subprocess.check_output(['git', 'hash-object', str(old)], text=True).strip() != '625b8d889f67652fa19a39b8689e306ea1c1fb91':
    raise SystemExit('Active Random Galaxy baseline changed; aborting')

text = old.read_text(encoding='utf-8').replace('0011', '0012')
text = once(text, "    hdMaxScale: 8\n  });", "    hdMaxScale: 8,\n    hdScaleSettleMs: 200\n  });", 'defaults')
text = once(text, "      this.hdGesture = null;\n      this.currentGalaxy = this.#initialCurrent(options.currentGalaxy);", "      this.hdGesture = null;\n      this.hdScaleBarValue = null;\n      this.hdScaleBarTimer = 0;\n      this.currentGalaxy = this.#initialCurrent(options.currentGalaxy);", 'scale state')
text = once(text, '.gvrg-hd-loading{', '.gvrg-hd-scale{position:absolute;left:50%;bottom:12px;z-index:6;transform:translateX(-50%);display:none;flex-direction:column;align-items:center;gap:4px;pointer-events:none;color:#FFD85A;font:400 10px/1.05 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.45px;text-align:center;text-shadow:0 0 4px rgba(255,242,168,.82),0 0 9px rgba(255,180,45,.34);white-space:nowrap}\n.gvrg-hd-scale-line{position:relative;height:12px;border-top:2px solid #FFD85A;filter:drop-shadow(0 0 4px rgba(255,216,90,.60))}\n.gvrg-hd-scale-line::before,.gvrg-hd-scale-line::after{content:"";position:absolute;top:-6px;width:2px;height:11px;background:#FFD85A;box-shadow:0 0 4px rgba(255,216,90,.55)}\n.gvrg-hd-scale-line::before{left:0}.gvrg-hd-scale-line::after{right:0}\n.gvrg-hd-scale-label{font:400 10px/1.05 "${FONT_NAMES.spaceAge}",sans-serif;color:#FFD85A;letter-spacing:.45px;text-shadow:0 0 4px rgba(255,242,168,.82),0 0 9px rgba(255,180,45,.34)}\n.gvrg-hd-loading{', 'scale css')
text = once(text, "      viewport.appendChild(hdImage);", "      const scaleBar = document.createElement('div');\n      scaleBar.className = 'gvrg-hd-scale';\n      this.hdScaleBar = scaleBar;\n      const scaleLine = document.createElement('div');\n      scaleLine.className = 'gvrg-hd-scale-line';\n      this.hdScaleLine = scaleLine;\n      const scaleLabel = document.createElement('div');\n      scaleLabel.className = 'gvrg-hd-scale-label';\n      this.hdScaleLabel = scaleLabel;\n      scaleBar.append(scaleLine, scaleLabel);\n      viewport.append(hdImage, scaleBar);", 'scale dom')
text = once(text, "      const fov = finiteNumber(candidate.fov) ?? 0.25;", "      const imageFovDegrees = finiteNumber(candidate.imageFovDegrees ?? candidate.image_fov_degrees ?? candidate.fieldOfViewDegrees ?? candidate.field_of_view_degrees);\n      const fov = finiteNumber(candidate.fov) ?? 0.25;", 'image fov read')
text = once(text, "        name, ra, dec, distance, constellation, age, ageYears, physicalSizeLy, designation, commonName, preparedHdUrl, preparedSource, preparedHdImage,", "        name, ra, dec, distance, constellation, age, ageYears, physicalSizeLy, designation, commonName, preparedHdUrl, preparedSource, preparedHdImage, imageFovDegrees,", 'image fov return')
methods = r'''    #hdScaleGeometry() {
      const destination = this.activeDestination;
      const distanceMly = finiteNumber(destination && destination.distance);
      const fovDegrees = finiteNumber(destination && destination.imageFovDegrees);
      const imageWidth = Number(this.hdImage && this.hdImage.offsetWidth);
      const viewportWidth = Number(this.hdViewport && this.hdViewport.clientWidth);
      const zoom = finiteNumber(this.hdScale);
      if (!(distanceMly > 0) || !(fovDegrees > 0) || !(imageWidth > 0) || !(viewportWidth > 0) || !(zoom > 0)) return null;
      const theta = fovDegrees * Math.PI / 180;
      const physicalWidthLy = 2 * distanceMly * 1_000_000 * Math.tan(theta / 2);
      if (!(physicalWidthLy > 0) || !Number.isFinite(physicalWidthLy)) return null;
      return { lyPerPx: physicalWidthLy / (imageWidth * zoom), viewportWidth };
    }
    #chooseHdScaleValue(geometry) {
      const targetPx = geometry.viewportWidth * 0.275;
      const targetLy = geometry.lyPerPx * targetPx;
      if (!(targetLy > 0)) return null;
      const exponent = Math.floor(Math.log10(targetLy));
      const candidates = [];
      for (let e = exponent - 2; e <= exponent + 2; e += 1) for (const m of [1, 2, 5]) candidates.push(m * Math.pow(10, e));
      const scored = candidates.map(value => {
        const px = value / geometry.lyPerPx;
        const fraction = px / geometry.viewportWidth;
        const inBand = fraction >= 0.20 && fraction <= 0.35;
        return { value, score: Math.abs(fraction - 0.275) + (inBand ? 0 : 10) };
      }).sort((a,b) => a.score - b.score);
      return scored.length ? scored[0].value : null;
    }
    #resetHdScaleBar() {
      if (this.hdScaleBarTimer) clearTimeout(this.hdScaleBarTimer);
      this.hdScaleBarTimer = 0;
      this.hdScaleBarValue = null;
      if (this.hdScaleBar) this.hdScaleBar.style.display = 'none';
    }
    #scheduleHdScaleBar() {
      if (this.hdScaleBarTimer) clearTimeout(this.hdScaleBarTimer);
      this.hdScaleBarTimer = setTimeout(() => {
        this.hdScaleBarTimer = 0;
        this.#updateHdScaleBar(true);
      }, Number(this.options.hdScaleSettleMs) || 200);
    }
    #updateHdScaleBar(selectNew = false) {
      if (!this.hdOpen || !this.hdScaleBar || !this.hdScaleLine || !this.hdScaleLabel) return;
      const geometry = this.#hdScaleGeometry();
      if (!geometry) { this.hdScaleBar.style.display = 'none'; return; }
      if (selectNew || !(this.hdScaleBarValue > 0)) this.hdScaleBarValue = this.#chooseHdScaleValue(geometry);
      if (!(this.hdScaleBarValue > 0)) { this.hdScaleBar.style.display = 'none'; return; }
      const widthPx = this.hdScaleBarValue / geometry.lyPerPx;
      const fraction = widthPx / geometry.viewportWidth;
      if (!selectNew && (fraction < 0.18 || fraction > 0.38)) this.#scheduleHdScaleBar();
      this.hdScaleLine.style.width = `${Math.max(4, widthPx)}px`;
      this.hdScaleLabel.textContent = formatWholeAstronomyScale(this.hdScaleBarValue);
      this.hdScaleBar.setAttribute('aria-label', `IMAGE SCALE ${this.hdScaleLabel.textContent}`);
      this.hdScaleBar.style.display = 'flex';
    }
'''
text = once(text, '    #applyHdTransform() {', methods + '    #applyHdTransform() {', 'scale methods')
text = once(text, "      this.hdGesture = null;\n      this.#applyHdTransform();\n    }\n    #pointerPair()", "      this.hdGesture = null;\n      this.#applyHdTransform();\n      this.#resetHdScaleBar();\n    }\n    #pointerPair()", 'reset scale')
text = once(text, "      this.#clampHdTranslation();\n      this.#applyHdTransform();\n    }\n    #onHdPointerUp(event)", "      this.#clampHdTranslation();\n      this.#applyHdTransform();\n      if (this.hdPointers.size >= 2) { this.#updateHdScaleBar(false); this.#scheduleHdScaleBar(); }\n    }\n    #onHdPointerUp(event)", 'pinch update')
text = once(text, "      } else if (this.hdPointers.size === 0) this.hdGesture = null;", "      } else if (this.hdPointers.size === 0) { this.hdGesture = null; this.#scheduleHdScaleBar(); }", 'pinch settle')
text = once(text, "        this.#positionHdPresentation();\n        this.#resetHdTransform();\n        return destination.preparedHdUrl", "        this.#positionHdPresentation();\n        this.#resetHdTransform();\n        this.#updateHdScaleBar(true);\n        return destination.preparedHdUrl", 'prepared scale init')
text = once(text, "        this.#positionHdPresentation();\n        this.#resetHdTransform();\n      };", "        this.#positionHdPresentation();\n        this.#resetHdTransform();\n        this.#updateHdScaleBar(true);\n      };", 'fallback scale init')
text = once(text, "      this.destroyed = true;", "      this.destroyed = true;\n      if (this.hdScaleBarTimer) clearTimeout(this.hdScaleBarTimer);", 'destroy timer')
new.write_text(text, encoding='utf-8')
new_sha = subprocess.check_output(['git', 'hash-object', str(new)], text=True).strip()

viewer = Path('viewer/GV-beta-0010E.py')
v = viewer.read_text(encoding='utf-8')
v = once(v, '            fov,hdUrl:hd.href,sourceUrl:source.href,', '            fov,imageFovDegrees:fieldDegrees,hdUrl:hd.href,sourceUrl:source.href,', 'viewer image fov')
v, count = re.subn(r'gv-random-galaxy-0028\.js\?v=[0-9a-f]+', f'gv-random-galaxy-0029.js?v={new_sha}', v, count=1)
if count != 1:
    raise SystemExit('viewer URL: expected one match')
v = once(v, "await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0028');", "await loadScript(RANDOM_GALAXY_URL,'gvRandomGalaxy0029');", 'viewer dataset')
v = once(v, "if(window.GalaxyRandomGalaxy?.VERSION!=='0011')throw new Error('RANDOM GALAXY 0028 PATH / 0011 VERIFIED CORE EXPORT MISSING');", "if(window.GalaxyRandomGalaxy?.VERSION!=='0012')throw new Error('RANDOM GALAXY 0029 PATH / 0012 VERIFIED CORE EXPORT MISSING');", 'viewer module check')
viewer.write_text(v, encoding='utf-8')

app = Path('android/galaxy-viewer-10e')
assets = app / 'app/src/main/assets'
shutil.copyfile(viewer, assets / 'viewer/GV-beta-0010E.py')
shutil.copyfile('viewer/artwork/icon.svg', assets / 'artwork/icon.svg')
shutil.copyfile('viewer/artwork/Fonts/Space Age Regular/Space Age Regular.otf', assets / 'artwork/Space-Age.otf')

splash = assets / 'viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html'
s = splash.read_text(encoding='utf-8')
s = once(s, 'messageHoldEnd:12196,messageFadeEnd:12696,blackAt:12196,launchAt:12696', 'messageHoldEnd:13696,messageFadeEnd:14196,blackAt:13696,launchAt:14196', 'splash final hold')
s = once(s, 'renderAt(0,false);rafId=requestAnimationFrame(frame)', 'renderAt(0,false);setTimeout(()=>{devLast=performance.now();rafId=requestAnimationFrame(frame)},1000)', 'splash opening pause')
splash.write_text(s, encoding='utf-8')

shell = assets / 'index.html'
shell.write_text(r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 10E</title><style>@font-face{font-family:"Space Age";src:url("artwork/Space-Age.otf") format("opentype");font-style:normal;font-weight:400;font-display:block}*{box-sizing:border-box;font-family:"Space Age",sans-serif!important}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(58vw,280px);height:min(58vw,280px);max-width:280px;max-height:280px;object-fit:contain;object-position:center;background:transparent}.v{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}#gv-splash-frame{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000;visibility:hidden}#gv-launch-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;background:#000;color:#FFD85A;white-space:pre-wrap;font:400 14px/1.45 "Space Age",sans-serif}</style></head><body><div id="gv-apk-cover"><img src="artwork/icon.svg" alt="GALAXY VIEWER"><div class="v">VERSION 10E</div></div><iframe id="gv-splash-frame"></iframe><div id="gv-launch-error"></div><script>(async()=>{'use strict';const R='https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/',c=document.getElementById('gv-apk-cover'),p=document.getElementById('gv-splash-frame'),e=document.getElementById('gv-launch-error');const delay=ms=>new Promise(r=>setTimeout(r,ms));const t=async u=>{const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);return r.text()};const x=s=>{const h=[...s.matchAll(/display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)/g)],j=[...s.matchAll(/display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)/g)];if(h.length!==1||j.length!==1)throw new Error('Viewer extraction failed');return[h[0][1],j[0][1]]};const q=async()=>{try{const m=JSON.parse(await t(R+'gv-current-viewer.json?t='+Date.now()));return[m,await t(R+m.viewer+'?t='+Date.now())]}catch(z){const m=JSON.parse(await t('viewer/gv-current-viewer.json'));return[m,await t('viewer/'+m.viewer)]}};const warm=async s=>{try{const urls=[...new Set([...s.matchAll(/https:\/\/[^'\"`\s]+/g)].map(m=>m[0]))];const primary=urls.filter(u=>/aladin|viewer\/modules\/|gv-hubble-galaxies-full/i.test(u));await Promise.allSettled(primary.map(u=>fetch(u,{cache:'force-cache'})));const cu=primary.find(u=>/gv-hubble-galaxies-full/i.test(u));if(!cu)return;const r=await fetch(cu,{cache:'force-cache'});if(!r.ok)return;const j=await r.json();const a=Array.isArray(j?.entries)?[...j.entries]:[];for(let i=a.length-1;i>0;i--){const k=Math.floor(Math.random()*(i+1));[a[i],a[k]]=[a[k],a[i]]}const imgs=a.slice(0,10).map(o=>String(o?.githubImageUrl||o?.selectedImageUrl||'')).filter(u=>/^https:\/\//.test(u));Promise.allSettled(imgs.map(u=>fetch(u,{cache:'force-cache'}))).catch(()=>{})}catch(_){}};const ready=()=>new Promise((ok,no)=>{const d=performance.now()+30000;const f=()=>{if(document.getElementById('aladin-cosmic-command-test')?.querySelector('canvas')&&window.aladin_cosmic_command_test)return ok();if(performance.now()>d)return no(new Error('10E Viewer readiness timeout'));setTimeout(f,100)};f()});const splash=()=>new Promise((ok,no)=>{let timer=0,done=false;const finish=()=>{if(done)return;done=true;if(timer)clearTimeout(timer);ok()};p.addEventListener('load',()=>{try{p.contentWindow.addEventListener('galaxy-splash-complete',finish,{once:true});p.style.visibility='visible';c.remove();timer=setTimeout(()=>no(new Error('10E splash completion timeout')),22000)}catch(z){no(z)}},{once:true});p.addEventListener('error',()=>no(new Error('10E splash failed to load')),{once:true});p.src='viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html'});try{const started=performance.now();const payload=q().then(v=>{warm(v[1]);return v});await delay(Math.max(0,3500-(performance.now()-started)));await splash();const[m,s]=await payload;if(m.version!=='10E')throw new Error('Manifest did not select 10E');const[h,j]=x(s);document.body.insertAdjacentHTML('beforeend',h);const z=document.createElement('script');z.textContent=j;document.body.appendChild(z);await ready();p.remove()}catch(z){e.style.display='block';e.textContent='GALAXY VIEWER 10E FAILED TO LOAD\n\n'+String(z?.stack||z)}})();</script></body></html>''', encoding='utf-8')

manifest = app / 'app/src/main/AndroidManifest.xml'
m = manifest.read_text(encoding='utf-8')
m = once(m, '<application android:allowBackup="false" android:label="Galaxy Viewer 10E"', '<application android:allowBackup="false" android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher" android:label="Galaxy Viewer 10E"', 'manifest icon')
manifest.write_text(m, encoding='utf-8')

gradle = app / 'app/build.gradle'
g = gradle.read_text(encoding='utf-8')
g = once(g, "applicationId 'com.gear66me.galaxyviewer10e'; minSdk 29; targetSdk 35; versionCode 1007; versionName '10E-generic'", "applicationId 'com.gear66me.galaxyviewer10e.r2'; minSdk 29; targetSdk 35; versionCode 1008; versionName '10E-generic-r2'", 'package version')
gradle.write_text(g, encoding='utf-8')

java = app / 'app/src/main/java/com/gear66me/galaxyviewer10e/MainActivity.java'
j = java.read_text(encoding='utf-8')
j = once(j, 'import android.graphics.Color;', 'import android.graphics.Color; import android.graphics.Typeface;', 'java typeface import')
j = once(j, 'TextView t=new TextView(this);t.setText(', 'TextView t=new TextView(this);t.setTypeface(Typeface.createFromAsset(getAssets(),"artwork/Space-Age.otf"));t.setText(', 'java error font')
java.write_text(j, encoding='utf-8')

mip = app / 'app/src/main/res/mipmap-xxxhdpi'
mip.mkdir(parents=True, exist_ok=True)
shutil.copyfile('viewer/artwork/App Icons/GV-app-icon-512-dark.png', mip / 'ic_launcher.png')

compile(viewer.read_text(encoding='utf-8'), str(viewer), 'exec')
print('NEW_MODULE_SHA=' + new_sha)
