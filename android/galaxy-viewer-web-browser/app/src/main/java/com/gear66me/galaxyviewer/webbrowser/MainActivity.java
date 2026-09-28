package com.gear66me.galaxyviewer.webbrowser;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public final class MainActivity extends Activity {
  private static final String POINTER="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/Web-Browser/web-browser-current.json";
  private WebView top, web, bottom;
  private String providerIcon="", sourceUrl="";
  private org.json.JSONArray sourceUrls=new org.json.JSONArray(); private int sourceIndex=0;

  @Override public void onCreate(Bundle b){
    super.onCreate(b); immersive();
    LinearLayout root=new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setBackgroundColor(Color.BLACK); root.setPadding(0,0,0,0);
    top=shell(); web=provider(); bottom=shell();
    LinearLayout.LayoutParams tp=new LinearLayout.LayoutParams(-1,dp(74)); root.addView(top,tp);
    FrameLayout frame=new FrameLayout(this); frame.setPadding(dp(2),dp(2),dp(2),dp(2));
    GradientDrawable fg=new GradientDrawable(); fg.setColor(Color.rgb(2,7,15)); fg.setStroke(dp(2),Color.rgb(8,45,96)); fg.setCornerRadius(dp(18)); frame.setBackground(fg);
    GradientDrawable wg=new GradientDrawable(); wg.setColor(Color.WHITE); wg.setCornerRadius(dp(16)); web.setBackground(wg); web.setClipToOutline(true); frame.setClipToOutline(true); frame.addView(web,0,new FrameLayout.LayoutParams(-1,-1)); android.widget.TextView ver=new android.widget.TextView(this); ver.setText("VERSION 0019"); ver.setTextColor(Color.rgb(120,255,171)); ver.setTextSize(9); ver.setBackgroundColor(Color.argb(210,2,7,15)); ver.setPadding(dp(4),dp(2),dp(4),dp(2)); FrameLayout.LayoutParams vp=new FrameLayout.LayoutParams(-2,-2,android.view.Gravity.TOP|android.view.Gravity.RIGHT); vp.topMargin=dp(4); vp.rightMargin=dp(5); frame.addView(ver,vp);
    LinearLayout.LayoutParams fp=new LinearLayout.LayoutParams(-1,0,1); fp.topMargin=0; fp.bottomMargin=0; root.addView(frame,fp);
    root.addView(bottom,new LinearLayout.LayoutParams(-1,dp(36)));
    setContentView(root); fetchPointer();
  }

  private WebView shell(){
    WebView v=new WebView(this); WebSettings s=v.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setCacheMode(WebSettings.LOAD_NO_CACHE); v.clearCache(true); v.setBackgroundColor(Color.BLACK);
    v.addJavascriptInterface(new Bridge(),"GV"); v.setWebViewClient(new WebViewClient()); return v;
  }
  private WebView provider(){
    WebView v=new WebView(this); WebSettings s=v.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setDatabaseEnabled(true); s.setUseWideViewPort(true); s.setLoadWithOverviewMode(false); s.setSupportZoom(true);
    s.setBuiltInZoomControls(true); s.setDisplayZoomControls(false); s.setCacheMode(WebSettings.LOAD_DEFAULT);
    s.setUserAgentString(s.getUserAgentString()+" GalaxyViewerWebBrowser/0005");
    v.setWebChromeClient(new WebChromeClient()); v.setWebViewClient(new WebViewClient(){
      @Override public void onPageFinished(WebView view,String url){ sourceUrl=url; syncShell(); }
    }); return v;
  }
  private void fetchPointer(){
    new Thread(()->{try{
      long t=System.currentTimeMillis();
      JSONObject p=getJson(POINTER+"?gv="+t);
      String config=p.getString("config");
      JSONObject c=getJson(config+(config.contains("?")?"&":"?")+"gv="+t);
      sourceUrl=c.getString("sourceUrl"); providerIcon=c.optString("providerIcon",""); sourceUrls=c.optJSONArray("sourceUrls"); if(sourceUrls==null)sourceUrls=new org.json.JSONArray().put(sourceUrl); sourceIndex=0;
      String th=c.getString("topShell"), bh=c.getString("bottomShell");
      runOnUiThread(()->{
        top.loadUrl(th+(th.contains("?")?"&":"?")+"gv="+System.currentTimeMillis());
        bottom.loadUrl(bh+(bh.contains("?")?"&":"?")+"gv="+System.currentTimeMillis());
        web.loadUrl(sourceUrl);
      });
    }catch(Exception e){ runOnUiThread(()->web.loadData("<h3>Galaxy Viewer Browser config error</h3><pre>"+esc(e.toString())+"</pre>","text/html","UTF-8")); }}).start();
  }
  private JSONObject getJson(String u)throws Exception{
    HttpURLConnection c=(HttpURLConnection)new URL(u).openConnection(); c.setUseCaches(false);
    c.setRequestProperty("Cache-Control","no-cache, no-store, max-age=0"); c.setRequestProperty("Pragma","no-cache");
    c.setConnectTimeout(12000); c.setReadTimeout(12000);
    BufferedReader r=new BufferedReader(new InputStreamReader(c.getInputStream())); StringBuilder b=new StringBuilder(); String x;
    while((x=r.readLine())!=null)b.append(x); r.close(); return new JSONObject(b.toString());
  }
  private void syncShell(){
    if(top==null)return; String js="javascript:if(window.setBrowserState)window.setBrowserState("+JSONObject.quote(sourceUrl)+","+JSONObject.quote(providerIcon)+")";
    top.loadUrl(js);
  }
  public final class Bridge{
    @JavascriptInterface public void back(){runOnUiThread(()->{if(web.canGoBack())web.goBack(); else syncShell();});}
    @JavascriptInterface public void forward(){runOnUiThread(()->{try{if(sourceUrls.length()>0){sourceIndex=(sourceIndex+1)%sourceUrls.length(); sourceUrl=sourceUrls.getString(sourceIndex); web.loadUrl(sourceUrl);}}catch(Exception ignored){}});}
    @JavascriptInterface public void exit(){runOnUiThread(()->finish());}
  }
  private void immersive(){getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY|View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN|View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_STABLE);}
  @Override public void onWindowFocusChanged(boolean h){super.onWindowFocusChanged(h);if(h)immersive();}
  @Override public void onBackPressed(){if(web!=null&&web.canGoBack())web.goBack();else finish();}
  private int dp(int n){return Math.round(n*getResources().getDisplayMetrics().density);}
  private static String esc(String s){return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;");}
}
