from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
BUILD_PROJECT = Path('/tmp/galaxy-viewer-10g-build')
TEN_G = ROOT / 'viewer/GV-beta-0010G.py'
SPLASH_SRC = ROOT / 'viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL'
ICON_SRC = ROOT / 'viewer/artwork/icon.svg'
FONT_SRC = ROOT / 'viewer/artwork/Fonts/Space Age Regular/Space Age Regular.otf'

# GALAXY VIEWER 10G APK PACKAGER
# 10G already exists before packaging begins. This script consumes 10G only.
# It creates a fresh disposable Android shell and never reads another Viewer
# release as a source, fallback, template, or runtime dependency.

assert TEN_G.is_file(), 'authoritative standalone 10G source is missing'
assert SPLASH_SRC.is_dir(), 'approved splash asset is missing'
assert ICON_SRC.is_file(), 'approved Galaxy Viewer icon is missing'
assert FONT_SRC.is_file(), 'approved Space Age font is missing'

standalone = TEN_G.read_text(encoding='utf-8')
assert "const VERSION='10G';" in standalone
assert "const DISPLAY_VERSION='10G';" in standalone
assert 'VERSION 10G' in standalone
assert 'gv-viewer-ready' in standalone
assert 'gv-viewer-failed' in standalone

# Runtime release-boundary gate: 10G may not fetch another Viewer release.
viewer_py_urls = re.findall(r'https?://[^\s\"\']*GV-beta-[^\s\"\']+\.py[^\s\"\']*', standalone, flags=re.I)
assert not viewer_py_urls, f'forbidden runtime Viewer release URL(s): {viewer_py_urls}'

html_blocks = re.findall(r'display\(HTML\("""([\s\S]*?)"""\)\)', standalone)
js_blocks = re.findall(r'display\(Javascript\(r"""([\s\S]*?)"""\)\)', standalone)
assert html_blocks, '10G HTML extraction failed'
assert js_blocks, '10G JavaScript extraction failed'
viewer_html = ''.join(html_blocks)
viewer_js = list(js_blocks)

# Fresh disposable Android project. No previous Android release tree is copied.
if BUILD_PROJECT.exists():
    shutil.rmtree(BUILD_PROJECT)
A = BUILD_PROJECT / 'app/src/main/assets'
JAVA = BUILD_PROJECT / 'app/src/main/java/com/gear66me/galaxyviewer10g'
A.mkdir(parents=True)
JAVA.mkdir(parents=True)

(BUILD_PROJECT / 'settings.gradle').write_text('''pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = 'GalaxyViewer10G'
include ':app'
''', encoding='utf-8')

(BUILD_PROJECT / 'build.gradle').write_text('''plugins {
    id 'com.android.application' version '8.7.3' apply false
}
''', encoding='utf-8')

(BUILD_PROJECT / 'app/build.gradle').write_text('''plugins { id 'com.android.application' }

android {
    namespace 'com.gear66me.galaxyviewer10g'
    compileSdk 35

    defaultConfig {
        applicationId 'com.gear66me.galaxyviewer10g'
        minSdk 26
        targetSdk 35
        versionCode 1016
        versionName '10G-standalone-apk-3'
    }

    buildTypes {
        debug { minifyEnabled false }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}
''', encoding='utf-8')

manifest = BUILD_PROJECT / 'app/src/main/AndroidManifest.xml'
manifest.write_text('''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:allowBackup="false"
        android:hardwareAccelerated="true"
        android:label="Galaxy Viewer 10G"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:exported="true"
            android:screenOrientation="fullSensor">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
''', encoding='utf-8')

values = BUILD_PROJECT / 'app/src/main/res/values'
values.mkdir(parents=True)
(values / 'styles.xml').write_text('''<resources>
    <style name="AppTheme" parent="android:style/Theme.Material.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:windowFullscreen">true</item>
        <item name="android:windowActionModeOverlay">true</item>
        <item name="android:windowNoTitle">true</item>
        <item name="android:colorAccent">#000000</item>
        <item name="android:navigationBarColor">#000000</item>
        <item name="android:statusBarColor">#000000</item>
    </style>
</resources>
''', encoding='utf-8')

(JAVA / 'MainActivity.java').write_text(r'''package com.gear66me.galaxyviewer10g;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_FULLSCREEN |
            View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
            View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY |
            View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
            View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        );

        webView = new WebView(this);
        webView.setBackgroundColor(0xFF000000);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setAllowFileAccessFromFileURLs(true);
        s.setAllowUniversalAccessFromFileURLs(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        WebView.setWebContentsDebuggingEnabled(true);
        setContentView(webView);
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (webView != null) webView.onResume();
    }

    @Override
    protected void onPause() {
        if (webView != null) webView.onPause();
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
''', encoding='utf-8')

# Copy only neutral assets required by the 10G APK shell.
(A / 'artwork').mkdir(parents=True)
shutil.copy2(ICON_SRC, A / 'artwork/icon.svg')
shutil.copy2(FONT_SRC, A / 'artwork/Space-Age.otf')
splash_dst = A / 'viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL'
shutil.copytree(SPLASH_SRC, splash_dst)

# Escape only the raw HTML parser sentinel. JavaScript restores runtime text.
vh = json.dumps(viewer_html).replace('</script', '<\\/script')
vj = json.dumps(viewer_js).replace('</script', '<\\/script')

bootstrap = f'''(async()=>{{'use strict';
const VIEWER_HTML={vh};
const VIEWER_JS={vj};
const VIEWER_TIMEOUT_MS=45000;
const SPLASH_FIRST_FRAME_TIMEOUT_MS=5000;
const SPLASH_COMPLETION_GRACE_MS=15000;
const ICON_MIN_HOLD_MS=3500;
const launchStartedAt=performance.now();
const launchCover=document.getElementById('gv-apk-cover');
const splashFrame=document.getElementById('gv-splash-frame');
const errorBox=document.getElementById('gv-launch-error');
const showError=e=>{{
  errorBox.style.display='block';
  errorBox.textContent='GALAXY VIEWER 10G FAILED TO LOAD\\n\\n'+String(e?.stack||e);
}};
const run=s=>{{const x=document.createElement('script');x.textContent=s;document.body.appendChild(x)}};
const mountViewerHtml=()=>{{
  const t=document.createElement('template');
  t.innerHTML=VIEWER_HTML;
  for(const old of [...t.content.querySelectorAll('script')]){{
    const fresh=document.createElement('script');
    for(const a of [...old.attributes])fresh.setAttribute(a.name,a.value);
    fresh.textContent=old.textContent;
    old.replaceWith(fresh);
  }}
  document.body.appendChild(t.content);
}};
const waitForIconMinimum=()=>new Promise(resolve=>setTimeout(resolve,Math.max(0,ICON_MIN_HOLD_MS-(performance.now()-launchStartedAt))));
const waitForAuthoritativeViewer=()=>new Promise((resolve,reject)=>{{
  let settled=false;
  const timer=setTimeout(()=>finishReject(new Error('GALAXY VIEWER 10G STARTUP TIMEOUT')),VIEWER_TIMEOUT_MS);
  const cleanup=()=>{{clearTimeout(timer);document.removeEventListener('gv-viewer-ready',ready);document.removeEventListener('gv-viewer-failed',failed)}};
  const finishResolve=detail=>{{if(settled)return;settled=true;cleanup();requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(detail)))}};
  const finishReject=err=>{{if(settled)return;settled=true;cleanup();reject(err)}};
  const ready=event=>finishResolve(event?.detail||null);
  const failed=event=>finishReject(new Error(String(event?.detail?.message||'10G Viewer startup failed')));
  document.addEventListener('gv-viewer-ready',ready,{{once:true}});
  document.addEventListener('gv-viewer-failed',failed,{{once:true}});
}});
const initializeViewer=async()=>{{
  mountViewerHtml();
  const authoritativeReady=waitForAuthoritativeViewer();
  VIEWER_JS.forEach(run);
  await authoritativeReady;
}};
const startSplash=async()=>{{
  await waitForIconMinimum();
  return new Promise((resolve,reject)=>{{
    let done=false;
    const finish=()=>{{if(done)return;done=true;resolve()}};
    const fail=e=>{{if(done)return;done=true;reject(e)}};
    splashFrame.addEventListener('load',()=>{{
      try{{
        const w=splashFrame.contentWindow;
        if(!w)throw new Error('SPLASH WINDOW UNAVAILABLE');
        w.addEventListener('galaxy-splash-complete',finish,{{once:true}});
        const firstFrameDeadline=performance.now()+SPLASH_FIRST_FRAME_TIMEOUT_MS;
        const reveal=()=>{{
          try{{
            const d=w.document,scene=d.getElementById('scene'),poster=d.getElementById('poster');
            if(scene?.style.opacity==='1'||poster?.style.visibility==='visible'){{
              if(launchCover?.isConnected)launchCover.remove();
              return;
            }}
            if(performance.now()>=firstFrameDeadline)return fail(new Error('SPLASH FIRST FRAME TIMEOUT'));
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
  const splashPromise=startSplash();
  await initializeViewer();
  await Promise.race([splashPromise,new Promise(resolve=>setTimeout(resolve,SPLASH_COMPLETION_GRACE_MS))]);
  requestAnimationFrame(()=>{{
    if(splashFrame?.isConnected)splashFrame.remove();
    if(launchCover?.isConnected)launchCover.remove();
  }});
}}catch(e){{
  console.error('GALAXY VIEWER 10G APK FAILURE',e);
  showError(e);
}}
}})();'''

head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 10G</title><style>@font-face{font-family:"Space Age";src:url("artwork/Space-Age.otf") format("opentype");font-style:normal;font-weight:400;font-display:block}*{box-sizing:border-box;font-family:"Space Age",sans-serif!important}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(58vw,280px);height:min(58vw,280px);max-width:280px;max-height:280px;object-fit:contain;object-position:center;background:transparent}.v{color:#FFD85A;font:400 16px/1 "Space Age",sans-serif;letter-spacing:1.2px;text-shadow:0 0 7px rgba(255,216,90,.55);white-space:nowrap}#gv-splash-frame{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000;visibility:visible}#gv-launch-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;background:#000;color:#FFD85A;white-space:pre-wrap;font:400 14px/1.45 "Space Age",sans-serif}</style></head><body><div id="gv-apk-cover"><img src="artwork/icon.svg" alt="GALAXY VIEWER"><div class="v">VERSION 10G</div></div><iframe id="gv-splash-frame" title="GALAXY VIEWER SPLASH"></iframe><div id="gv-launch-error" role="alert"></div>'''
out = head + '<script>' + bootstrap + '</script></body></html>'
(A / 'index.html').write_text(out, encoding='utf-8')

text_out = (A / 'index.html').read_text(encoding='utf-8')
assert 'VERSION 10G' in text_out
assert "const VERSION='10G';" in text_out
assert "const DISPLAY_VERSION='10G';" in text_out
assert 'font-family:"Space Age",sans-serif!important' in text_out
assert 'gv-viewer-ready' in text_out
assert 'gv-viewer-failed' in text_out
assert 'SPLASH_COMPLETION_GRACE_MS=15000' in text_out
assert 'APK_WEAK_READY_CONDITION_PASS' not in text_out
assert not re.search(r'GV-beta-[0-9A-Z-]+\.py', text_out, flags=re.I)
assert text_out.lower().count('</script>') == 1

print('AUTHORITATIVE 10G SOURCE READ-ONLY:', TEN_G)
print('10G source bytes:', TEN_G.stat().st_size)
print('Fresh disposable Android build:', BUILD_PROJECT)
print('Embedded APK index bytes:', len(text_out.encode('utf-8')))
print('STARTUP CONTRACT: authoritative 10G ready/fail; bounded splash after 10G readiness')
