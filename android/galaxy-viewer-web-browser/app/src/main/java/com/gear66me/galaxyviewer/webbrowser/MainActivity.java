package com.gear66me.galaxyviewer.webbrowser;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.LinearLayout;

public final class MainActivity extends Activity {
  private static final String START="https://www.spitzer.caltech.edu/image/ssc2006-01a1";
  private static final String TARGET="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg";
  private static final String SPITZER="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/providers/spitzer/spitzer-icon.png";
  private WebView top,web,bottom;

  @Override public void onCreate(Bundle b){super.onCreate(b); immersive(); setContentView(ui()); web.loadUrl(START);}
  private void immersive(){getWindow().getDecorView().setSystemUiVisibility(5894|View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);}
  @Override public void onWindowFocusChanged(boolean h){super.onWindowFocusChanged(h);if(h)immersive();}

  private View ui(){
    LinearLayout root=new LinearLayout(this); root.setOrientation(LinearLayout.VERTICAL); root.setPadding(dp(7),dp(7),dp(7),dp(7)); root.setBackgroundColor(Color.rgb(0,4,12));
    top=shell(topHtml()); top.addJavascriptInterface(new Bridge(),"Android");
    root.addView(top,new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,dp(82)));

    FrameLayout frame=new FrameLayout(this); frame.setPadding(dp(2),dp(2),dp(2),dp(2)); frame.setBackgroundColor(Color.rgb(67,207,255));
    web=new WebView(this); configure(web); frame.addView(web,new FrameLayout.LayoutParams(-1,-1));
    root.addView(frame,new LinearLayout.LayoutParams(-1,0,1f));

    bottom=shell(bottomHtml()); bottom.addJavascriptInterface(new Bridge(),"Android");
    LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(-1,dp(52)); bp.setMargins(0,dp(6),0,0); root.addView(bottom,bp);
    return root;
  }

  private WebView shell(String html){
    WebView v=new WebView(this); v.setBackgroundColor(Color.TRANSPARENT); v.setVerticalScrollBarEnabled(false);v.setHorizontalScrollBarEnabled(false);
    WebSettings s=v.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setAllowFileAccess(false);
    v.loadDataWithBaseURL("https://gear66me-ui.github.io/Galaxy_Viewer/",html,"text/html","UTF-8",null);return v;
  }
  private void configure(WebView v){
    WebSettings s=v.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setDatabaseEnabled(true);s.setUseWideViewPort(true);s.setLoadWithOverviewMode(true);s.setSupportZoom(true);s.setBuiltInZoomControls(true);s.setDisplayZoomControls(false);s.setTextZoom(100);s.setMediaPlaybackRequiresUserGesture(false);
    s.setUserAgentString(s.getUserAgentString()+" GalaxyViewerWebBrowser/0002");
    v.setWebChromeClient(new WebChromeClient());
    v.setWebViewClient(new WebViewClient(){
      @Override public boolean shouldOverrideUrlLoading(WebView w, WebResourceRequest r){return r.getUrl()==null||!"https".equalsIgnoreCase(r.getUrl().getScheme());}
      @Override public void onPageStarted(WebView w,String u,android.graphics.Bitmap f){setUrl(u);}
      @Override public void onPageFinished(WebView w,String u){setUrl(u);}
    });
  }
  private void setUrl(String u){if(top==null)return;String q=org.json.JSONObject.quote(u==null?"":u);top.evaluateJavascript("setUrl("+q+")",null);}
  private int dp(int n){return Math.round(n*getResources().getDisplayMetrics().density);}

  public final class Bridge{
    @JavascriptInterface public void back(){runOnUiThread(()->{if(web.canGoBack())web.goBack();});}
    @JavascriptInterface public void forward(){runOnUiThread(()->{if(web.canGoForward())web.goForward();else web.loadUrl(START);});}
    @JavascriptInterface public void close(){runOnUiThread(()->finish());}
  }

  private String css(){
    return "<style>@font-face{font-family:GV;src:url('https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/Space%20Age%20GV-9A.otf')}*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:transparent;color:#F4FDFF}body{font-family:GV,Arial,sans-serif}.r{display:grid;grid-template-columns:36px minmax(0,1fr) 36px;gap:5px;height:36px}.r+.r{margin-top:5px}.t,.b{position:relative;border:1px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,#081B3A 0%,#0B3177 44%,#123F86 70%,#296DBD 100%);box-shadow:inset 0 2px 2px rgba(225,251,255,.82),inset 0 -3px 5px rgba(0,0,0,.52),inset 0 0 13px rgba(41,153,255,.34),0 0 3px #DDF8FF,0 0 9px rgba(50,190,255,.72)}.title{display:flex;align-items:center;justify-content:center;font-size:15.5px;letter-spacing:.38px;text-shadow:0 0 5px #fff,0 0 11px rgba(88,191,255,.85)}.icon{display:grid;place-items:center}.icon img{width:34px;height:34px;object-fit:contain}.addr{display:flex;align-items:center;min-width:0;padding:0 6px 0 4px;font:12px/1 GV,Arial,sans-serif;white-space:nowrap;overflow:hidden}.url{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;opacity:.88}.lock{width:20px;flex:0 0 20px;text-align:center;font-family:Arial,sans-serif;font-size:14px}.b{border-radius:10px;cursor:pointer}.b:before{content:'';position:absolute;left:50%;top:50%;width:12.8px;height:12.8px;border:solid #F4FDFF;border-width:0 4px 4px 0;filter:drop-shadow(0 0 4px #8DDAFF) drop-shadow(0 0 8px #58BFFF)}.back:before{transform:translate(-38%,-50%) rotate(135deg)}.fwd:before{transform:translate(-62%,-50%) rotate(-45deg)}.foot{height:42px;display:grid;grid-template-columns:42px minmax(0,1fr) 42px;gap:5px}.foot .b{height:42px}.label{display:flex;align-items:center;justify-content:center;border-radius:10px;font-size:14px;letter-spacing:.32px}.foot .icon{border-radius:10px}.foot .icon img{width:34px;height:34px}</style>";
  }
  private String topHtml(){return "<!doctype html><meta name='viewport' content='width=device-width,initial-scale=1'>"+css()+"<div class='r'><div class='t icon'><img src='"+TARGET+"'></div><div class='t title'>GALAXY VIEWER</div><div class='t icon'><img src='"+SPITZER+"'></div></div><div class='r'><button class='b back' onclick='Android.back()'></button><div class='t addr'><span class='lock'>▣</span><span id='u' class='url'>LOADING…</span></div><button class='b fwd' onclick='Android.forward()'></button></div><script>function setUrl(x){document.getElementById('u').textContent=x}</script>";}
  private String bottomHtml(){return "<!doctype html><meta name='viewport' content='width=device-width,initial-scale=1'>"+css()+"<div class='foot'><button class='b back' onclick='Android.close()'></button><div class='t label' onclick='Android.close()'>BACK TO GALAXY VIEWER</div><div class='t icon' onclick='Android.close()'><img src='"+TARGET+"'></div></div>";}
  @Override public void onBackPressed(){if(web!=null&&web.canGoBack())web.goBack();else finish();}
  @Override protected void onDestroy(){if(top!=null)top.destroy();if(web!=null)web.destroy();if(bottom!=null)bottom.destroy();super.onDestroy();}
}