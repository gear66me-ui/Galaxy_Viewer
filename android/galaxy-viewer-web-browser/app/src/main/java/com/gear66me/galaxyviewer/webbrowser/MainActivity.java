package com.gear66me.galaxyviewer.webbrowser;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.graphics.Outline;
import android.view.ViewOutlineProvider;
import android.os.Bundle;
import android.content.Intent;
import android.net.Uri;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import androidx.webkit.WebViewAssetLoader;
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
  private WebViewAssetLoader assetLoader;
  private boolean browserMode=false;
  private String providerIcon="", sourceUrl="";
  private org.json.JSONArray sourceUrls=new org.json.JSONArray(); private int sourceIndex=0;

  @Override public void onCreate(Bundle b){
    super.onCreate(b); immersive();
    assetLoader=new WebViewAssetLoader.Builder().addPathHandler("/assets/",new WebViewAssetLoader.AssetsPathHandler(this)).build();
    LinearLayout root=new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setBackgroundColor(Color.BLACK); root.setPadding(0,0,0,0);
    top=shell(); web=provider(); bottom=shell();
    LinearLayout.LayoutParams tp=new LinearLayout.LayoutParams(-1,dp(70)); root.addView(top,tp); top.setTag(tp);
    FrameLayout frame=new FrameLayout(this); frame.setPadding(0,0,0,0);
    GradientDrawable fg=new GradientDrawable(); fg.setColor(Color.rgb(2,7,15)); fg.setStroke(dp(2),Color.rgb(8,45,96)); fg.setCornerRadius(dp(10)); frame.setBackground(fg);
    frame.setOutlineProvider(ViewOutlineProvider.BACKGROUND);
    frame.setClipToOutline(true);
    web.setBackgroundColor(Color.TRANSPARENT);
    FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1); wp.setMargins(dp(2),dp(2),dp(2),dp(2));
    GradientDrawable webClip=new GradientDrawable(); webClip.setColor(Color.TRANSPARENT); webClip.setCornerRadius(dp(8)); web.setBackground(webClip); web.setOutlineProvider(ViewOutlineProvider.BACKGROUND); web.setClipToOutline(true);
    frame.addView(web,0,wp);
    LinearLayout.LayoutParams fp=new LinearLayout.LayoutParams(-1,0,1); fp.setMargins(dp(2),0,dp(2),0); root.addView(frame,fp);
    root.addView(bottom,new LinearLayout.LayoutParams(-1,dp(36)));
    setContentView(root); String launchUrl=launchSourceUrl(getIntent()); if(launchUrl!=null){ browserMode=true; fetchPointer(); } else { launchGalaxyViewer(); }
  }

  private WebView shell(){
    WebView v=new WebView(this); WebSettings s=v.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setCacheMode(WebSettings.LOAD_NO_CACHE); v.clearCache(true); v.setBackgroundColor(Color.BLACK);
    v.addJavascriptInterface(new Bridge(),"GV"); v.setWebViewClient(new WebViewClient(){ @Override public void onPageFinished(WebView view,String url){ if(view==top) fitTopShell(); }}); return v;
  }
  private void fitTopShell(){
    top.evaluateJavascript("(function(){return Math.ceil(document.documentElement.getBoundingClientRect().height)})()", value->{ try{ int css=(int)Math.ceil(Double.parseDouble(value.replace("\\\"",""))); LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)top.getLayoutParams(); lp.height=dp(css); top.setLayoutParams(lp); }catch(Exception ignored){} });
  }
  private WebView provider(){
    WebView v=new WebView(this); WebSettings s=v.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setDatabaseEnabled(true); s.setUseWideViewPort(true); s.setLoadWithOverviewMode(false); s.setSupportZoom(true);
    s.setBuiltInZoomControls(true); s.setDisplayZoomControls(false); s.setCacheMode(WebSettings.LOAD_DEFAULT);
    s.setUserAgentString(s.getUserAgentString()+" GalaxyViewerWebBrowser/0030");
    v.setWebChromeClient(new WebChromeClient()); v.setWebViewClient(new WebViewClient(){
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest request){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(request.getUrl()); }
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,String url){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(Uri.parse(url)); }
      @Override public void onPageFinished(WebView view,String url){ sourceUrl=url; syncShell(); }
    }); return v;
  }
  private void fetchPointer(){
    new Thread(()->{try{
      long t=System.currentTimeMillis();
      JSONObject p=getJson(POINTER+"?gv="+t);
      String config=p.getString("config");
      JSONObject c=getJson(config+(config.contains("?")?"&":"?")+"gv="+t);
      sourceUrl=c.getString("sourceUrl"); providerIcon=c.optString("providerIcon",""); String launchUrl=launchSourceUrl(getIntent()); if(launchUrl!=null)sourceUrl=launchUrl; sourceUrls=c.optJSONArray("sourceUrls"); if(sourceUrls==null)sourceUrls=new org.json.JSONArray().put(sourceUrl); sourceIndex=0;
      String th=c.getString("topShell"), bh=c.getString("bottomShell");
      runOnUiThread(()->{
        top.loadUrl(th+(th.contains("?")?"&":"?")+"gv="+System.currentTimeMillis());
        bottom.loadUrl(bh+(bh.contains("?")?"&":"?")+"gv="+System.currentTimeMillis());
        web.loadUrl(sourceUrl);
      });
    }catch(Exception e){ runOnUiThread(()->web.loadData("<h3>Galaxy Viewer Browser config error</h3><pre>"+esc(e.toString())+"</pre>","text/html","UTF-8")); }}).start();
  }
  private void launchGalaxyViewer(){ browserMode=false; WebSettings s=web.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setAllowFileAccess(false); s.setAllowContentAccess(false); s.setCacheMode(WebSettings.LOAD_NO_CACHE); top.setVisibility(View.GONE); bottom.setVisibility(View.GONE); android.view.ViewParent parent=web.getParent(); if(parent instanceof FrameLayout){ FrameLayout frame=(FrameLayout)parent; LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)frame.getLayoutParams(); lp.setMargins(0,0,0,0); frame.setLayoutParams(lp); frame.setBackgroundColor(Color.BLACK); } web.loadUrl("https://appassets.androidplatform.net/assets/index.html"); }
  private String launchSourceUrl(Intent intent){ try{ Uri d=intent==null?null:intent.getData(); if(d!=null&&"galaxyviewerbrowser".equalsIgnoreCase(d.getScheme())){ String u=d.getQueryParameter("url"); if(u!=null&&(u.startsWith("https://")||u.startsWith("http://")))return u; } }catch(Exception ignored){} return null; }
  @Override protected void onNewIntent(Intent intent){ super.onNewIntent(intent); setIntent(intent); String u=launchSourceUrl(intent); if(u!=null){ browserMode=true; top.setVisibility(View.VISIBLE); bottom.setVisibility(View.VISIBLE); sourceUrl=u; fetchPointer(); } }
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
