package com.gear66me.galaxyviewer10d;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public final class MainActivity extends Activity {
    private static final String POINTER="https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/mobile/beta/10D-app-target.json";
    private static final String HOST="gear66me-ui.github.io";
    private static final String PREFIX="/Galaxy_Viewer/";
    private static final String PREFS="gv10d", LAST="last_good_launch_url";
    private LinearLayout panel; private TextView status; private Button retry; private WebView web; private String target;

    @Override protected void onCreate(Bundle b){super.onCreate(b); immersive(); statusScreen(); resolve();}
    private void immersive(){getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY|View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN|View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_STABLE);}
    private void statusScreen(){panel=new LinearLayout(this);panel.setOrientation(LinearLayout.VERTICAL);panel.setGravity(Gravity.CENTER);panel.setPadding(48,48,48,48);panel.setBackgroundColor(Color.BLACK);status=new TextView(this);status.setTextColor(Color.WHITE);status.setTextSize(16);status.setGravity(Gravity.CENTER);panel.addView(status,new LinearLayout.LayoutParams(-1,-2));retry=new Button(this);retry.setText("RETRY");retry.setOnClickListener(v->resolve());LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-2,-2);p.topMargin=32;panel.addView(retry,p);show("GALAXY VIEWER 10D R4\n\nChecking current Viewer…",false);}
    private void show(String s,boolean r){runOnUiThread(()->{setContentView(panel);status.setText(s);retry.setVisibility(r?View.VISIBLE:View.GONE);});}
    private static String nonceUrl(String base){Uri u=Uri.parse(base);return u.buildUpon().appendQueryParameter("gvnocache",Long.toString(System.currentTimeMillis())).build().toString();}
    private void resolve(){show("GALAXY VIEWER 10D R4\n\nChecking current Viewer…",false);new Thread(()->{try{String u=new JSONObject(fetch(POINTER+"?t="+System.currentTimeMillis())).optString("launchUrl","").trim();validate(u);target=u;getSharedPreferences(PREFS,MODE_PRIVATE).edit().putString(LAST,u).apply();String fresh=nonceUrl(u);runOnUiThread(()->open(fresh));}catch(Exception e){SharedPreferences p=getSharedPreferences(PREFS,MODE_PRIVATE);String u=p.getString(LAST,"");try{if(u!=null&&!u.isEmpty()){validate(u);target=u;String fresh=nonceUrl(u);runOnUiThread(()->open(fresh));return;}}catch(Exception ignored){}show("GALAXY VIEWER 10D R4 — STARTUP ERROR\n\nCould not read the GitHub target file and no valid cached Viewer is available.\n\nPointer:\n"+POINTER+"\n\nError:\n"+e.getClass().getSimpleName()+": "+e.getMessage(),true);}},"gv10d-pointer").start();}
    private static String fetch(String s)throws Exception{HttpURLConnection c=(HttpURLConnection)new URL(s).openConnection();c.setConnectTimeout(12000);c.setReadTimeout(12000);c.setUseCaches(false);c.setRequestProperty("Cache-Control","no-cache, no-store, max-age=0");c.setRequestProperty("Pragma","no-cache");try{int code=c.getResponseCode();if(code<200||code>=300)throw new IllegalStateException("HTTP "+code);BufferedReader r=new BufferedReader(new InputStreamReader(c.getInputStream(),StandardCharsets.UTF_8));StringBuilder o=new StringBuilder();String l;while((l=r.readLine())!=null)o.append(l).append('\n');r.close();return o.toString();}finally{c.disconnect();}}
    private static void validate(String s){Uri u=Uri.parse(s);if(!"https".equalsIgnoreCase(u.getScheme())||!HOST.equalsIgnoreCase(u.getHost())||u.getPath()==null||!u.getPath().startsWith(PREFIX))throw new IllegalArgumentException("Invalid Galaxy Viewer target");}
    private void open(String u){if(web!=null){web.stopLoading();web.clearHistory();web.clearCache(true);web.destroy();}web=new WebView(this);web.setBackgroundColor(Color.BLACK);WebSettings s=web.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setDatabaseEnabled(true);s.setAllowFileAccess(false);s.setAllowContentAccess(false);s.setMediaPlaybackRequiresUserGesture(false);s.setCacheMode(WebSettings.LOAD_NO_CACHE);s.setUserAgentString(s.getUserAgentString()+" GalaxyViewer10D/10D-generic-r4");web.clearCache(true);web.clearHistory();web.setWebChromeClient(new WebChromeClient());web.setWebViewClient(new WebViewClient(){private boolean ok(Uri x){return x!=null&&"https".equalsIgnoreCase(x.getScheme())&&HOST.equalsIgnoreCase(x.getHost())&&x.getPath()!=null&&x.getPath().startsWith(PREFIX);}@Override public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest q){return !ok(q.getUrl());}@Override public boolean shouldOverrideUrlLoading(WebView v,String x){return !ok(Uri.parse(x));}@Override public void onReceivedError(WebView v,WebResourceRequest q,WebResourceError e){if(q.isForMainFrame())fail("WebView error "+e.getErrorCode()+": "+e.getDescription());}@Override public void onReceivedHttpError(WebView v,WebResourceRequest q,WebResourceResponse e){if(q.isForMainFrame()&&e.getStatusCode()>=400)fail("Viewer returned HTTP "+e.getStatusCode());}});setContentView(web);web.loadUrl(u);}
    private void fail(String d){show("GALAXY VIEWER 10D R4 — VIEWER LOAD ERROR\n\n"+d+"\n\nResolved target:\n"+(target==null?"(none)":target)+"\n\nPointer:\n"+POINTER,true);}
    @Override public void onBackPressed(){if(web!=null&&web.canGoBack())web.goBack();else super.onBackPressed();}
}
