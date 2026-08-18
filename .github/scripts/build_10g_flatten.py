from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'android/galaxy-viewer-10e'
A = P / 'app/src/main/assets'

# Package identity
p = P / 'app/build.gradle'
s = p.read_text()
s = s.replace("applicationId 'com.gear66me.galaxyviewer10e.generic'", "applicationId 'com.gear66me.galaxyviewer10g'")
s = s.replace("versionCode 1010", "versionCode 1013")
s = s.replace("versionName '10E-generic-permanent-1'", "versionName '10G-flattened-3'")
p.write_text(s)

p = P / 'app/src/main/AndroidManifest.xml'
s = p.read_text().replace('android:label="Galaxy Viewer 10E"', 'android:label="Galaxy Viewer 10G"')
s = s.replace('android:name=".MainActivity"', 'android:name="com.gear66me.galaxyviewer10e.MainActivity"')
p.write_text(s)

java = r'''package com.gear66me.galaxyviewer10e;
import android.app.*; import android.graphics.*; import android.net.*; import android.os.*; import android.view.*; import android.webkit.*; import android.widget.*; import java.io.*;
public final class MainActivity extends Activity {
  private static final String H="appassets.androidplatform.net"; private WebView w;
  private WebResourceResponse asset(Uri u){try{if(u==null||!"https".equalsIgnoreCase(u.getScheme())||!H.equalsIgnoreCase(u.getHost()))return null;String p=u.getPath();if(p==null||!p.startsWith("/assets/"))return null;p=p.substring(8);if(p.isEmpty()||p.contains(".."))return null;InputStream in=getAssets().open(p);String e=MimeTypeMap.getFileExtensionFromUrl(p),m=MimeTypeMap.getSingleton().getMimeTypeFromExtension(e);if(m==null){if(p.endsWith(".js"))m="application/javascript";else if(p.endsWith(".json"))m="application/json";else if(p.endsWith(".svg"))m="image/svg+xml";else if(p.endsWith(".html"))m="text/html";else m="application/octet-stream";}return new WebResourceResponse(m,"UTF-8",in);}catch(Exception x){return null;}}
  @Override protected void onCreate(Bundle b){super.onCreate(b);getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY|View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN|View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_STABLE);w=new WebView(this);w.setBackgroundColor(Color.BLACK);WebSettings s=w.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setDatabaseEnabled(true);s.setAllowFileAccess(false);s.setAllowContentAccess(false);s.setMediaPlaybackRequiresUserGesture(false);s.setCacheMode(WebSettings.LOAD_DEFAULT);s.setUserAgentString(s.getUserAgentString()+" GalaxyViewer10G/flattened-3");w.setWebChromeClient(new WebChromeClient());w.setWebViewClient(new WebViewClient(){@Override public WebResourceResponse shouldInterceptRequest(WebView v,WebResourceRequest r){WebResourceResponse a=asset(r.getUrl());return a!=null?a:super.shouldInterceptRequest(v,r);}@Override public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest r){Uri u=r.getUrl();return u==null||!"https".equalsIgnoreCase(u.getScheme());}});setContentView(w);w.loadUrl("https://"+H+"/assets/index.html");}
  @Override public void onBackPressed(){if(w!=null&&w.canGoBack())w.goBack();else super.onBackPressed();}
}
'''
(P / 'app/src/main/java/com/gear66me/galaxyviewer10e/MainActivity.java').write_text(java)

src = (ROOT / 'viewer/GV-beta-0010F.py').read_text()
hs = re.findall(r'display\(HTML\(\"\"\"([\s\S]*?)\"\"\"\)\)', src)
js = re.findall(r'display\(Javascript\(r\"\"\"([\s\S]*?)\"\"\"\)\)', src)
if len(hs) != 1 or len(js) != 1:
    raise SystemExit(f'10F extraction failed: html={len(hs)} js={len(js)}')
info = (ROOT / 'viewer/modules/gv-info-module-0001.js').read_text()

head = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no"><meta name="theme-color" content="#000"><title>GALAXY VIEWER 10G</title><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000;color:#fff}#gv-apk-cover{position:fixed;inset:0;z-index:2147483646;display:flex;flex-direction:column;gap:18px;align-items:center;justify-content:center;background:#000}#gv-apk-cover img{display:block;width:min(58vw,280px);height:min(58vw,280px);object-fit:contain}.gv-apk-v{color:#FFD85A;font:16px/1 sans-serif;letter-spacing:1.2px}#gv-splash-frame{position:fixed;inset:0;width:100%;height:100%;border:0;z-index:2147483645;background:#000;visibility:hidden}#gv-launch-error{display:none;position:fixed;inset:0;z-index:2147483647;padding:24px;background:#000;color:#FFD85A;white-space:pre-wrap;font:14px/1.45 monospace}</style></head><body><div id="gv-apk-cover"><img src="artwork/icon.svg" alt="GALAXY VIEWER"><div class="gv-apk-v">VERSION 10G</div></div><iframe id="gv-splash-frame"></iframe><div id="gv-launch-error"></div>'''
stamp = '''<script>(()=>{const f=()=>{const v=document.getElementById('gv-version-label');if(v){v.textContent='VERSION 10G';v.setAttribute('aria-label','GALAXY VIEWER VERSION 10G')}const c=document.getElementById('gv-apk-cover');if(c){const n=c.querySelector('.gv-10e-version');if(n)n.remove();const x=c.querySelector('.gv-apk-v');if(x)x.textContent='VERSION 10G'}if(window.GalaxyViewerInfo10G)window.GalaxyViewerInfo10G.refresh()};f();setTimeout(f,400);setTimeout(f,1500)})();</script>'''
monitor = '''<script>(async()=>{'use strict';const c=document.getElementById('gv-apk-cover'),p=document.getElementById('gv-splash-frame'),e=document.getElementById('gv-launch-error'),start=performance.now(),delay=ms=>new Promise(r=>setTimeout(r,ms));let firstError='';window.addEventListener('error',x=>{if(!firstError)firstError=String(x.message||x.error||'window error')});window.addEventListener('unhandledrejection',x=>{if(!firstError)firstError=String(x.reason?.stack||x.reason||'unhandled rejection')});const ready=()=>document.getElementById('aladin-cosmic-command-test')?.querySelector('canvas')&&window.aladin_cosmic_command_test&&window.GalaxyViewerInfo10G;const wait=async()=>{const d=performance.now()+60000;while(performance.now()<d){if(ready())return true;await delay(75)}throw new Error('10G Viewer did not become interactive'+(firstError?'\\n\\nFIRST JAVASCRIPT ERROR:\\n'+firstError:''))};const splash=async()=>{await delay(Math.max(0,3500-(performance.now()-start)));return new Promise((ok,no)=>{let done=false,t=0;const fin=()=>{if(done)return;done=true;clearTimeout(t);ok()};p.addEventListener('load',()=>{try{p.contentWindow.addEventListener('galaxy-splash-complete',fin,{once:true});p.style.visibility='visible';c?.remove();t=setTimeout(()=>no(new Error('10G splash completion timeout')),22000)}catch(z){no(z)}},{once:true});p.addEventListener('error',()=>no(new Error('10G splash failed to load')),{once:true});p.src='viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html'})};try{const rp=wait();await splash();await rp;p.remove();c?.remove()}catch(z){e.style.display='block';e.textContent='GALAXY VIEWER 10G FAILED TO LOAD\\n\\n'+String(z?.stack||z)}})();</script>'''

out = head + hs[0] + '<script>' + js[0] + '</script><script>' + info + '</script>' + stamp + monitor + '</body></html>'
(A / 'index.html').write_text(out)

# Build-time assertions
text = (A / 'index.html').read_text()
assert 'VERSION 10G' in text
assert 'GalaxyViewerInfo10G' in text
assert 'GV-beta-0010G.py' not in text
assert 'fetch(VIEWER_URL' not in text
print('Flattened 10G index bytes:', len(text.encode()))
