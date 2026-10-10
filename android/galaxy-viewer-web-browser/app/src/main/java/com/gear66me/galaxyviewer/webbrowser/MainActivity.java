package com.gear66me.galaxyviewer.webbrowser;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.graphics.Outline;
import android.view.ViewOutlineProvider;
import android.os.Bundle;
import android.os.Message;
import android.content.Intent;
import android.net.Uri;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.view.ViewGroup;
import android.view.Gravity;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewCompat;
import androidx.webkit.WebViewFeature;
import androidx.webkit.PrerenderOperationCallback;
import androidx.webkit.PrerenderException;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public final class MainActivity extends Activity {
  private static final String POINTER="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/Web-Browser/web-browser-current.json";
  private WebView top, web, bottom, viewerWeb;
  private LinearLayout browserLayer;
  private View navigationCover=null;
  private Runnable pendingProviderLaunch=null;
  private WebViewAssetLoader assetLoader;
  private boolean browserMode=false, clearProviderEntryHistory=false;
  private View fullscreenView=null; private WebChromeClient.CustomViewCallback fullscreenCallback=null;
  private String providerIcon="", sourceUrl="", pendingProviderUrl="", pendingProviderIcon="", providerHomeUrl="", prewarmedUrl="";

  @Override public void onCreate(Bundle b){
    super.onCreate(b); immersive();
    assetLoader=new WebViewAssetLoader.Builder().addPathHandler("/assets/",new WebViewAssetLoader.AssetsPathHandler(this)).build();

    FrameLayout root=new FrameLayout(this); root.setBackgroundColor(Color.BLACK);
    viewerWeb=viewer();
    viewerWeb.addJavascriptInterface(new ViewerBridge(),"GVNative");
    root.addView(viewerWeb,new FrameLayout.LayoutParams(-1,-1));

    browserLayer=new LinearLayout(this); browserLayer.setOrientation(LinearLayout.VERTICAL); browserLayer.setBackgroundColor(Color.BLACK); browserLayer.setPadding(0,dp(12),0,dp(12));
    top=shell(); web=provider(); bottom=shell();
    LinearLayout.LayoutParams tp=new LinearLayout.LayoutParams(-1,dp(70)); browserLayer.addView(top,tp); top.setTag(tp);
    FrameLayout frame=new FrameLayout(this); frame.setPadding(0,0,0,0);
    GradientDrawable fg=new GradientDrawable(); fg.setColor(Color.rgb(2,7,15)); fg.setStroke(dp(2),Color.rgb(8,45,96)); fg.setCornerRadius(dp(10)); frame.setBackground(fg);
    frame.setOutlineProvider(ViewOutlineProvider.BACKGROUND); frame.setClipToOutline(true);
    web.setBackgroundColor(Color.TRANSPARENT);
    FrameLayout.LayoutParams wp=new FrameLayout.LayoutParams(-1,-1); wp.setMargins(dp(2),dp(2),dp(2),dp(2));
    GradientDrawable webClip=new GradientDrawable(); webClip.setColor(Color.TRANSPARENT); webClip.setCornerRadius(dp(8)); web.setBackground(webClip); web.setOutlineProvider(ViewOutlineProvider.BACKGROUND); web.setClipToOutline(true);
    frame.addView(web,wp);
    TextView test57=new TextView(this); test57.setText("◉ 57 TEST"); test57.setTextColor(Color.WHITE); test57.setTextSize(11); test57.setGravity(Gravity.CENTER); test57.setPadding(dp(7),dp(3),dp(7),dp(3));
    GradientDrawable test57Bg=new GradientDrawable(); test57Bg.setColor(Color.rgb(150,0,0)); test57Bg.setStroke(dp(1),Color.WHITE); test57Bg.setCornerRadius(dp(10)); test57.setBackground(test57Bg);
    FrameLayout.LayoutParams test57p=new FrameLayout.LayoutParams(-2,-2,Gravity.TOP|Gravity.RIGHT); test57p.setMargins(0,dp(8),dp(8),0); frame.addView(test57,test57p);
    LinearLayout.LayoutParams fp=new LinearLayout.LayoutParams(-1,0,1); fp.setMargins(dp(2),0,dp(2),0); browserLayer.addView(frame,fp);
    browserLayer.addView(bottom,new LinearLayout.LayoutParams(-1,dp(36)));
    browserLayer.setVisibility(View.GONE);
    root.addView(browserLayer,new FrameLayout.LayoutParams(-1,-1));
    navigationCover=new View(this); navigationCover.setBackgroundColor(Color.BLACK); navigationCover.setVisibility(View.GONE);
    root.addView(navigationCover,new FrameLayout.LayoutParams(-1,-1));
    setContentView(root);

    String launchUrl=launchSourceUrl(getIntent());
    if(launchUrl!=null&&launchPrewarm(getIntent())){ prewarmProvider(launchUrl); moveTaskToBack(true); }
    else { launchGalaxyViewer(); if(launchUrl!=null){ openProvider(launchUrl,launchProviderIcon(getIntent())); } }
  }

  private WebView viewer(){
    WebView v=new WebView(this); WebSettings s=v.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setDatabaseEnabled(true); s.setUseWideViewPort(true); s.setLoadWithOverviewMode(false); s.setSupportZoom(true);
    s.setBuiltInZoomControls(false); s.setDisplayZoomControls(false); s.setCacheMode(WebSettings.LOAD_NO_CACHE);
    s.setAllowFileAccess(false); s.setAllowContentAccess(false);
    s.setUserAgentString(s.getUserAgentString()+" GalaxyViewerWebBrowser/0057");
    v.setBackgroundColor(Color.BLACK); v.setWebChromeClient(new WebChromeClient());
    v.setWebViewClient(new WebViewClient(){
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest request){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(request.getUrl()); }
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,String url){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(Uri.parse(url)); }
      @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest request){
        Uri u=request.getUrl();
        if(u!=null&&"galaxyviewerbrowser".equalsIgnoreCase(u.getScheme())){
          String target=u.getQueryParameter("url");
          if(target!=null&&target.startsWith("https://")){ openProvider(target,u.getQueryParameter("icon")); return true; }
        }
        return false;
      }
    });
    return v;
  }

  private WebView shell(){
    WebView v=new WebView(this); WebSettings s=v.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setCacheMode(WebSettings.LOAD_NO_CACHE); v.clearCache(true); v.setBackgroundColor(Color.BLACK);
    v.addJavascriptInterface(new Bridge(),"GV"); v.setWebViewClient(new WebViewClient(){
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest request){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(request.getUrl()); }
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,String url){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(Uri.parse(url)); }
      @Override public void onPageFinished(WebView view,String url){
        if(view==top){
          view.evaluateJavascript("(function(){var s=document.createElement('style');s.textContent=\"@font-face{font-family:'GVLOCAL';src:url('https://appassets.androidplatform.net/assets/SpaceAge-GV-9A.otf') format('opentype');font-display:block}.title{font-family:'GVLOCAL','GV',sans-serif!important;color:#EAFBFF!important;text-shadow:0 0 3px rgba(180,240,255,.98),0 0 9px rgba(67,207,255,.92),0 0 16px rgba(41,132,255,.58)!important}\";document.head.appendChild(s)})()",null);
          fitTopShell();
        }
      }
    }); return v;
  }
  private void fitTopShell(){
    top.evaluateJavascript("(function(){return Math.ceil(document.documentElement.getBoundingClientRect().height)})()", value->{ try{ int css=(int)Math.ceil(Double.parseDouble(value.replace("\\\"",""))); LinearLayout.LayoutParams lp=(LinearLayout.LayoutParams)top.getLayoutParams(); lp.height=dp(css); top.setLayoutParams(lp); }catch(Exception ignored){} });
  }
  private WebView provider(){
    WebView v=new WebView(this); WebSettings s=v.getSettings(); s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true);
    s.setDatabaseEnabled(true); s.setUseWideViewPort(true); s.setLoadWithOverviewMode(false); s.setSupportZoom(true);
    s.setBuiltInZoomControls(true); s.setDisplayZoomControls(false); s.setCacheMode(WebSettings.LOAD_DEFAULT);
    s.setSupportMultipleWindows(true); s.setJavaScriptCanOpenWindowsAutomatically(true);
    s.setUserAgentString(s.getUserAgentString()+" GalaxyViewerWebBrowser/0057");
    v.setWebChromeClient(new WebChromeClient(){
      @Override public boolean onCreateWindow(WebView view,boolean isDialog,boolean isUserGesture,Message resultMsg){
        WebView popup=new WebView(MainActivity.this); WebSettings ps=popup.getSettings(); ps.setJavaScriptEnabled(true); ps.setDomStorageEnabled(true); ps.setSupportZoom(true); ps.setBuiltInZoomControls(true); ps.setDisplayZoomControls(false);
        popup.setWebViewClient(new WebViewClient(){
          private boolean handedOff=false;
          private boolean handoff(String url){ if(handedOff||url==null||url.isEmpty()||"about:blank".equals(url))return false; handedOff=true; web.loadUrl(url); popup.destroy(); return true; }
          @Override public boolean shouldOverrideUrlLoading(WebView v,WebResourceRequest r){ return handoff(r.getUrl()==null?null:r.getUrl().toString()); }
          @Override public boolean shouldOverrideUrlLoading(WebView v,String url){ return handoff(url); }
        });
        WebView.WebViewTransport transport=(WebView.WebViewTransport)resultMsg.obj; transport.setWebView(popup); resultMsg.sendToTarget(); return true;
      }
      @Override public void onShowCustomView(View view,CustomViewCallback callback){
        if(fullscreenView!=null){callback.onCustomViewHidden();return;}
        fullscreenView=view; fullscreenCallback=callback;
        FrameLayout decor=(FrameLayout)getWindow().getDecorView();
        decor.addView(view,new FrameLayout.LayoutParams(-1,-1));
        if(browserLayer!=null)browserLayer.setVisibility(View.INVISIBLE); immersive();
      }
      @Override public void onHideCustomView(){
        if(fullscreenView==null)return;
        ViewGroup parent=(ViewGroup)fullscreenView.getParent(); if(parent!=null)parent.removeView(fullscreenView);
        fullscreenView=null; if(fullscreenCallback!=null){fullscreenCallback.onCustomViewHidden();fullscreenCallback=null;}
        if(browserMode&&browserLayer!=null)browserLayer.setVisibility(View.VISIBLE); immersive();
      }
    }); v.setWebViewClient(new WebViewClient(){
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest request){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(request.getUrl()); }
      @Override public WebResourceResponse shouldInterceptRequest(WebView view,String url){ return assetLoader==null?null:assetLoader.shouldInterceptRequest(Uri.parse(url)); }
      @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest request){ Uri u=request.getUrl(); if(u!=null&&"galaxyviewerbrowser".equalsIgnoreCase(u.getScheme())){ String target=u.getQueryParameter("url"); if(target!=null&&target.startsWith("https://")){ openProvider(target,u.getQueryParameter("icon")); return true; } } return false; }
      @Override public void onPageFinished(WebView view,String url){ if(browserMode){ if(clearProviderEntryHistory){ web.clearHistory(); clearProviderEntryHistory=false; } sourceUrl=url; syncShell(); } }
    }); return v;
  }
  private void fetchPointer(){
    new Thread(()->{try{
      long t=System.currentTimeMillis();
      JSONObject p=getJson(POINTER+"?gv="+t);
      String config=p.getString("config");
      JSONObject c=getJson(config+(config.contains("?")?"&":"?")+"gv="+t);
      sourceUrl=c.getString("sourceUrl"); String launchUrl=launchSourceUrl(getIntent()); String launchIcon=launchProviderIcon(getIntent()); if(launchUrl!=null){sourceUrl=launchUrl;providerIcon=launchIcon;} else if(pendingProviderUrl!=null&&!pendingProviderUrl.isEmpty()){sourceUrl=pendingProviderUrl;providerIcon=pendingProviderIcon;pendingProviderUrl="";pendingProviderIcon="";} else {providerIcon=c.optString("providerIcon","");} providerHomeUrl=sourceUrl;
      String th=c.getString("topShell"), bh=c.getString("bottomShell");
      runOnUiThread(()->{
        top.loadUrl(th+(th.contains("?")?"&":"?")+"gv="+System.currentTimeMillis());
        bottom.loadUrl(bh+(bh.contains("?")?"&":"?")+"gv="+System.currentTimeMillis());
        // Do not load the last configured provider into the hidden WebView during app startup.
        // The provider display stays blank until an explicit openProvider() action; this prevents
        // a previous-session galaxy/page from flashing on first browser entry. Do not clear cache,
        // cookies, DOM storage, or pre-warmed content here.
        // Provider navigation and prewarming still load their requested URLs through their own paths.
      });
    }catch(Exception e){ runOnUiThread(()->web.loadData("<h3>Galaxy Viewer Browser config error</h3><pre>"+esc(e.toString())+"</pre>","text/html","UTF-8")); }}).start();
  }
  private boolean launchPrewarm(Intent intent){ try{ Uri d=intent==null?null:intent.getData(); return d!=null&&"galaxyviewerbrowser".equalsIgnoreCase(d.getScheme())&&"prewarm".equalsIgnoreCase(d.getQueryParameter("mode")); }catch(Exception ignored){} return false; }
  private void prewarmProvider(String u){
    if(u==null||!u.startsWith("https://")||u.equals(prewarmedUrl))return;
    prewarmedUrl=u;
    if(browserLayer!=null)browserLayer.setVisibility(View.GONE);
    try{
      if(WebViewFeature.isFeatureSupported(WebViewFeature.PRERENDER_WITH_URL)){
        WebViewCompat.prerenderUrlAsync(web,u,null,getMainExecutor(),new PrerenderOperationCallback(){
          @Override public void onPrerenderActivated(){}
          @Override public void onError(PrerenderException e){ if(u.equals(prewarmedUrl))web.loadUrl(u); }
        });
      }else web.loadUrl(u);
    }catch(Exception e){ web.loadUrl(u); }
  }
  private String launchProviderIcon(Intent intent){ try{ Uri d=intent==null?null:intent.getData(); if(d!=null&&"galaxyviewerbrowser".equalsIgnoreCase(d.getScheme())){ String icon=d.getQueryParameter("icon"); if(icon!=null&&icon.startsWith("https://"))return icon; } }catch(Exception ignored){} return ""; }
  private void launchGalaxyViewer(){ browserMode=false; if(browserLayer!=null)browserLayer.setVisibility(View.GONE); if(viewerWeb!=null)viewerWeb.loadUrl("https://gear66me-ui.github.io/Galaxy_Viewer/viewer/releases/launch/Galaxy-Viewer-Launch/index.html?gv="+System.currentTimeMillis()); }
  // Browser 0057 navigation contract: cover the outgoing page immediately, blank it before waiting,
  // then start/reveal only the requested destination after a minimum 2,000 ms from the button action.
  // Keep WebView cache/cookies/storage intact; the cover is visual isolation, not cache clearing.
  private void openProvider(String u,String icon){
    browserMode=true; clearProviderEntryHistory=true; pendingProviderUrl=u; pendingProviderIcon=icon==null?"":icon; providerIcon=pendingProviderIcon; sourceUrl=u; providerHomeUrl=u;
    if(pendingProviderLaunch!=null){new Handler(Looper.getMainLooper()).removeCallbacks(pendingProviderLaunch);pendingProviderLaunch=null;}
    boolean prepared=web!=null&&u.equals(prewarmedUrl)&&u.equals(web.getUrl());
    if(browserLayer!=null)browserLayer.setVisibility(View.INVISIBLE);
    if(navigationCover!=null)navigationCover.setVisibility(View.VISIBLE);
    if(web!=null&&!prepared){web.stopLoading();web.loadUrl("about:blank");}
    fetchPointer();
    pendingProviderLaunch=()->{
      pendingProviderLaunch=null;
      if(!browserMode||!u.equals(sourceUrl))return;
      if(web!=null&&!prepared)web.loadUrl(u);
      if(browserLayer!=null)browserLayer.setVisibility(View.VISIBLE);
      if(navigationCover!=null)navigationCover.setVisibility(View.GONE);
      immersive();
    };
    new Handler(Looper.getMainLooper()).postDelayed(pendingProviderLaunch,2000);
  }
  private void notifyViewerResumed(){
    if(viewerWeb!=null)viewerWeb.evaluateJavascript("window.dispatchEvent(new CustomEvent('gv-native-viewer-resumed'))",null);
  }
  private void returnToViewer(){ browserMode=false; if(browserLayer!=null)browserLayer.setVisibility(View.GONE); notifyViewerResumed(); }
  private void escapeToFreshViewer(){
    if(fullscreenView!=null){
      try{ ViewGroup parent=(ViewGroup)fullscreenView.getParent(); if(parent!=null)parent.removeView(fullscreenView); }catch(Exception ignored){}
      fullscreenView=null;
      if(fullscreenCallback!=null){ try{fullscreenCallback.onCustomViewHidden();}catch(Exception ignored){} fullscreenCallback=null; }
    }
    browserMode=false;
    clearProviderEntryHistory=false;
    pendingProviderUrl="";
    pendingProviderIcon="";
    sourceUrl="";
    if(web!=null){ try{web.stopLoading();}catch(Exception ignored){} }
    if(browserLayer!=null)browserLayer.setVisibility(View.GONE);
    launchGalaxyViewer();
  }
  private String launchSourceUrl(Intent intent){ try{ Uri d=intent==null?null:intent.getData(); if(d!=null&&"galaxyviewerbrowser".equalsIgnoreCase(d.getScheme())){ String u=d.getQueryParameter("url"); if(u!=null&&(u.startsWith("https://")||u.startsWith("http://")))return u; } }catch(Exception ignored){} return null; }
  @Override protected void onNewIntent(Intent intent){ super.onNewIntent(intent); setIntent(intent); String u=launchSourceUrl(intent); if(u!=null){ if(launchPrewarm(intent)){prewarmProvider(u);moveTaskToBack(true);}else openProvider(u,launchProviderIcon(intent)); } }
  private JSONObject getJson(String u)throws Exception{
    HttpURLConnection c=(HttpURLConnection)new URL(u).openConnection(); c.setUseCaches(false);
    c.setRequestProperty("Cache-Control","no-cache, no-store, max-age=0"); c.setRequestProperty("Pragma","no-cache");
    c.setConnectTimeout(12000); c.setReadTimeout(12000);
    BufferedReader r=new BufferedReader(new InputStreamReader(c.getInputStream())); StringBuilder b=new StringBuilder(); String x;
    while((x=r.readLine())!=null)b.append(x); r.close(); return new JSONObject(b.toString());
  }
  private void syncShell(){
    if(top==null)return; String js="javascript:if(window.setBrowserState)window.setBrowserState("+JSONObject.quote(sourceUrl)+","+JSONObject.quote(providerIcon)+","+(web.canGoBack()?"true":"false")+","+(web.canGoForward()?"true":"false")+")";
    top.loadUrl(js);
  }
  public final class ViewerBridge{
    @JavascriptInterface public void prewarm(String url){runOnUiThread(()->prewarmProvider(url));}
  }
  public final class Bridge{
    @JavascriptInterface public void back(){runOnUiThread(()->{restoreProviderHome();});}
    @JavascriptInterface public void forward(){runOnUiThread(()->{if(web.canGoForward())web.goForward(); else syncShell();});}
    @JavascriptInterface public void exit(){runOnUiThread(()->returnToViewer());}
  }
  private void restoreProviderHome(){
    if(fullscreenView!=null){
      try{ ViewGroup parent=(ViewGroup)fullscreenView.getParent(); if(parent!=null)parent.removeView(fullscreenView); }catch(Exception ignored){}
      fullscreenView=null;
      if(fullscreenCallback!=null){ try{fullscreenCallback.onCustomViewHidden();}catch(Exception ignored){} fullscreenCallback=null; }
      if(browserMode&&browserLayer!=null)browserLayer.setVisibility(View.VISIBLE);
    }
    if(web==null||providerHomeUrl==null||providerHomeUrl.isEmpty()){syncShell();return;}
    web.stopLoading();
    web.loadUrl(providerHomeUrl);
  }
  private void immersive(){getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN|View.SYSTEM_UI_FLAG_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY|View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN|View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION|View.SYSTEM_UI_FLAG_LAYOUT_STABLE);}
  @Override public void onWindowFocusChanged(boolean h){super.onWindowFocusChanged(h);if(h)immersive();}
  @Override public void onBackPressed(){if(browserMode){escapeToFreshViewer();}else{launchGalaxyViewer();}}
  private int dp(int n){return Math.round(n*getResources().getDisplayMetrics().density);}
  private static String esc(String s){return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;");}
}
