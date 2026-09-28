package com.gear66me.galaxyviewer.webbrowser;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public final class MainActivity extends Activity {
  private static final String POINTER =
      "https://gear66me-ui.github.io/Galaxy_Viewer/viewer/Web-Browser/web-browser-current.json";

  private WebView web;

  @Override public void onCreate(Bundle state) {
    super.onCreate(state);
    immersive();
    web = new WebView(this);
    configure(web);
    setContentView(web);
    web.loadUrl(POINTER);
  }

  private void immersive() {
    getWindow().getDecorView().setSystemUiVisibility(
        View.SYSTEM_UI_FLAG_FULLSCREEN |
        View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
        View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY |
        View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
        View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
        View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
  }

  @Override public void onWindowFocusChanged(boolean hasFocus) {
    super.onWindowFocusChanged(hasFocus);
    if (hasFocus) immersive();
  }

  private void configure(WebView v) {
    WebSettings s = v.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    s.setDatabaseEnabled(true);
    s.setUseWideViewPort(true);
    s.setLoadWithOverviewMode(false);
    s.setSupportZoom(true);
    s.setBuiltInZoomControls(true);
    s.setDisplayZoomControls(false);
    s.setMediaPlaybackRequiresUserGesture(false);
    s.setUserAgentString(s.getUserAgentString() + " GalaxyViewerGenericBrowser/0004");

    v.setWebChromeClient(new WebChromeClient());
    v.setWebViewClient(new WebViewClient() {
      @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
        String u = request.getUrl() == null ? "" : request.getUrl().toString();
        if (u.startsWith("https://gear66me-ui.github.io/Galaxy_Viewer/viewer/Web-Browser/") &&
            u.endsWith("web-browser-current.json")) {
          return false;
        }
        return false;
      }

      @Override public void onPageFinished(WebView view, String url) {
        if (!url.startsWith(POINTER)) return;
        view.evaluateJavascript(
          "(function(){try{var p=JSON.parse(document.body.innerText);" +
          "var u=p.url||p.shellUrl||p.entryUrl||'';" +
          "if(u){location.replace(u);}else{document.body.innerHTML='<pre>WEB BROWSER POINTER HAS NO url</pre>';}" +
          "}catch(e){document.body.innerHTML='<pre>WEB BROWSER POINTER ERROR: '+e+'</pre>';}})();",
          null);
      }
    });
  }

  @Override public void onBackPressed() {
    if (web != null && web.canGoBack()) web.goBack(); else finish();
  }

  @Override protected void onDestroy() {
    if (web != null) web.destroy();
    super.onDestroy();
  }
}
