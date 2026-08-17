package com.gear66me.galaxyviewer9i;

import android.app.Activity;
import android.app.DownloadManager;
import android.content.ContentValues;
import android.content.Context;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.webkit.DownloadListener;
import android.webkit.JavascriptInterface;
import android.webkit.URLUtil;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.OutputStream;

public final class MainActivity extends Activity {
    private static final String APP_URL = "file:///android_asset/index.html";
    private static final String APP_HOST = "gear66me-ui.github.io";
    private static final String APP_PATH = "/Galaxy_Viewer/";
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);

        webView = new WebView(this);
        webView.setBackgroundColor(0xFF000000);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setAllowContentAccess(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setMediaPlaybackRequiresUserGesture(false);

        webView.addJavascriptInterface(new DownloadBridge(this), "GalaxyViewerAndroid");
        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new WebViewClient() {
            private boolean allowed(Uri uri) {
                if (uri == null) return false;
                if ("file".equalsIgnoreCase(uri.getScheme())) {
                    String path = uri.getPath();
                    return path != null && path.startsWith("/android_asset/");
                }
                return "https".equalsIgnoreCase(uri.getScheme())
                        && APP_HOST.equalsIgnoreCase(uri.getHost())
                        && uri.getPath() != null
                        && uri.getPath().startsWith(APP_PATH);
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return !allowed(request.getUrl());
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return !allowed(Uri.parse(url));
            }
        });
        webView.setDownloadListener(new GalaxyDownloadListener());
        webView.loadUrl(APP_URL);
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    private final class GalaxyDownloadListener implements DownloadListener {
        @Override
        public void onDownloadStart(String url, String userAgent, String contentDisposition, String mimetype, long contentLength) {
            String filename = URLUtil.guessFileName(url, contentDisposition, mimetype);
            if (url != null && url.startsWith("blob:")) {
                String script = "(async()=>{try{const r=await fetch(" + JSONObject.quote(url)
                        + ");const b=await r.blob();const fr=new FileReader();fr.onloadend=()=>GalaxyViewerAndroid.saveDataUrl("
                        + JSONObject.quote(filename) + ",fr.result);fr.readAsDataURL(b);}catch(e){console.error(e);}})()";
                webView.evaluateJavascript(script, null);
                return;
            }
            Uri uri = Uri.parse(url);
            if (!"https".equalsIgnoreCase(uri.getScheme())) return;
            DownloadManager.Request request = new DownloadManager.Request(uri);
            request.setTitle(filename);
            request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, filename);
            DownloadManager manager = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
            manager.enqueue(request);
        }
    }

    private static final class DownloadBridge {
        private final Context context;

        DownloadBridge(Context context) {
            this.context = context.getApplicationContext();
        }

        @JavascriptInterface
        public void saveDataUrl(String filename, String dataUrl) {
            try {
                int comma = dataUrl == null ? -1 : dataUrl.indexOf(',');
                if (comma < 0) throw new IllegalArgumentException("Invalid download data");
                String header = dataUrl.substring(0, comma);
                String mime = "image/jpeg";
                int colon = header.indexOf(':');
                int semi = header.indexOf(';');
                if (colon >= 0 && semi > colon) mime = header.substring(colon + 1, semi);
                byte[] bytes = Base64.decode(dataUrl.substring(comma + 1), Base64.DEFAULT);

                ContentValues values = new ContentValues();
                values.put(MediaStore.Downloads.DISPLAY_NAME, filename == null || filename.isEmpty() ? "Hubble-HD.jpg" : filename);
                values.put(MediaStore.Downloads.MIME_TYPE, mime);
                values.put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/Galaxy Viewer");
                Uri target = context.getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
                if (target == null) throw new IllegalStateException("Could not create Android download");
                try (OutputStream output = context.getContentResolver().openOutputStream(target)) {
                    if (output == null) throw new IllegalStateException("Could not open Android download");
                    output.write(bytes);
                }
                Toast.makeText(context, "Hubble image downloaded", Toast.LENGTH_SHORT).show();
            } catch (Exception error) {
                Toast.makeText(context, "Image download failed", Toast.LENGTH_LONG).show();
            }
        }
    }
}
