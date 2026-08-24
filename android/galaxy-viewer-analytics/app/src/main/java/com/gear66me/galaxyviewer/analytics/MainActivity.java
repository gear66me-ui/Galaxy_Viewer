package com.gear66me.galaxyviewer.analytics;

import android.app.Activity;
import android.app.DownloadManager;
import android.content.ContentValues;
import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.Gravity;
import android.view.View;
import android.webkit.CookieManager;
import android.webkit.DownloadListener;
import android.webkit.JavascriptInterface;
import android.webkit.URLUtil;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebStorage;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public final class MainActivity extends Activity {
    private static final String APP_BASE =
            "https://gear66me-ui.github.io/Galaxy_Viewer/mobile/beta/generic-app.html";
    private static final String APP_HOST = "gear66me-ui.github.io";
    private static final String APP_PATH = "/Galaxy_Viewer/";
    private static final String DOWNLOAD_FOLDER = "Galaxy Viewer Analytics";

    private WebView webView;
    private View splash;

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

        FrameLayout root = new FrameLayout(this);
        GradientDrawable rootGradient = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{0xFF020812, 0xFF061D45, 0xFF0B4AA2, 0xFF1484DB});
        root.setBackground(rootGradient);
        setContentView(root);

        webView = new WebView(this);
        webView.setBackgroundColor(Color.BLACK);
        webView.setVisibility(View.INVISIBLE);
        root.addView(webView, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT));

        buildSplash(root);
        buildAnalyticsBadge(root);

        purgeAnalyticsWebData();

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        DownloadBridge bridge = new DownloadBridge(this);
        webView.addJavascriptInterface(bridge, "GalaxyViewerAndroid");
        webView.addJavascriptInterface(bridge, "GalaxyViewerDownloads");

        webView.setWebChromeClient(new WebChromeClient());

        webView.setWebViewClient(new WebViewClient() {
            private boolean allowed(Uri uri) {
                return uri != null
                        && "https".equalsIgnoreCase(uri.getScheme())
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

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);

                view.evaluateJavascript(
                        "(async()=>{"
                                + "try{if(window.caches){for(const k of await caches.keys())await caches.delete(k)}}catch(e){}"
                                + "try{sessionStorage.clear()}catch(e){}"
                                + "})();",
                        null);

                view.setVisibility(View.VISIBLE);
                if (splash != null) {
                    ((FrameLayout)splash.getParent()).removeView(splash);
                    splash = null;
                }
            }
        });

        webView.setDownloadListener(new GalaxyDownloadListener());

        String freshUrl = APP_BASE
                + "?source=android-analytics"
                + "&analytics=1"
                + "&cacheBust=" + System.currentTimeMillis();

        webView.loadUrl(freshUrl);
    }

    private void purgeAnalyticsWebData() {
        try { webView.stopLoading(); } catch (Exception ignored) {}
        try { webView.clearCache(true); } catch (Exception ignored) {}
        try { webView.clearHistory(); } catch (Exception ignored) {}
        try { webView.clearFormData(); } catch (Exception ignored) {}
        try { WebStorage.getInstance().deleteAllData(); } catch (Exception ignored) {}

        try {
            CookieManager cookies = CookieManager.getInstance();
            cookies.setAcceptCookie(true);
            cookies.removeAllCookies(null);
            cookies.removeSessionCookies(null);
            cookies.flush();
        } catch (Exception ignored) {}
    }

    private void buildSplash(FrameLayout root) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setGravity(Gravity.CENTER);
        box.setPadding(36, 36, 36, 36);

        GradientDrawable bg = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{0xFF020812, 0xFF071D45, 0xFF0B3177, 0xFF1484DB});
        box.setBackground(bg);

        ImageView icon = new ImageView(this);
        icon.setImageResource(R.drawable.gv_app_icon);
        int iconSize = (int)(190 * getResources().getDisplayMetrics().density);
        box.addView(icon, new LinearLayout.LayoutParams(iconSize, iconSize));

        TextView title = new TextView(this);
        title.setText("GALAXY VIEWER");
        title.setTextColor(0xFFF3FBFF);
        title.setTextSize(26);
        title.setGravity(Gravity.CENTER);
        title.setPadding(0, 24, 0, 8);
        box.addView(title);

        TextView analytics = new TextView(this);
        analytics.setText("ANALYTICS MODE");
        analytics.setTextColor(0xFF8FE8FF);
        analytics.setTextSize(16);
        analytics.setGravity(Gravity.CENTER);
        analytics.setLetterSpacing(0.12f);
        box.addView(analytics);

        TextView fresh = new TextView(this);
        fresh.setText("FRESH CACHE · DIAGNOSTICS ENABLED");
        fresh.setTextColor(0xFFBFDFFF);
        fresh.setTextSize(10);
        fresh.setGravity(Gravity.CENTER);
        fresh.setPadding(0, 12, 0, 0);
        box.addView(fresh);

        splash = box;
        root.addView(box, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT));
    }

    private void buildAnalyticsBadge(FrameLayout root) {
        TextView badge = new TextView(this);
        badge.setText("ANALYTICS MODE");
        badge.setTextColor(0xFFEAFBFF);
        badge.setTextSize(9);
        badge.setGravity(Gravity.CENTER);
        badge.setPadding(14, 6, 14, 6);

        GradientDrawable badgeBg = new GradientDrawable(
                GradientDrawable.Orientation.LEFT_RIGHT,
                new int[]{0xDD081B3A, 0xDD0B4AA2, 0xDD1484DB});
        badgeBg.setCornerRadius(14f);
        badge.setBackground(badgeBg);

        FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.WRAP_CONTENT,
                FrameLayout.LayoutParams.WRAP_CONTENT);
        lp.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL;
        lp.topMargin = 8;
        root.addView(badge, lp);
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    private final class GalaxyDownloadListener implements DownloadListener {
        @Override
        public void onDownloadStart(
                String url,
                String userAgent,
                String contentDisposition,
                String mimetype,
                long contentLength) {

            String filename = URLUtil.guessFileName(url, contentDisposition, mimetype);

            if (url != null && url.startsWith("blob:")) {
                String script =
                        "(async()=>{try{const r=await fetch(" + JSONObject.quote(url)
                                + ");const b=await r.blob();const fr=new FileReader();"
                                + "fr.onloadend=()=>GalaxyViewerAndroid.saveDataUrl("
                                + JSONObject.quote(filename)
                                + ",fr.result);fr.readAsDataURL(b);}catch(e){console.error(e);}})()";
                webView.evaluateJavascript(script, null);
                return;
            }

            Uri uri = Uri.parse(url);
            if (!"https".equalsIgnoreCase(uri.getScheme())) return;

            DownloadManager.Request request = new DownloadManager.Request(uri);
            request.setTitle(filename);
            request.setNotificationVisibility(
                    DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            request.setDestinationInExternalPublicDir(
                    Environment.DIRECTORY_DOWNLOADS,
                    DOWNLOAD_FOLDER + "/" + safeFilename(filename));

            DownloadManager manager =
                    (DownloadManager)getSystemService(DOWNLOAD_SERVICE);
            manager.enqueue(request);
        }
    }

    private final class DownloadBridge {
        private final Context context;

        DownloadBridge(Context context) {
            this.context = context.getApplicationContext();
        }

        @JavascriptInterface
        public void saveJson(String filename, String json) {
            try {
                String safe = safeFilename(
                        filename == null || filename.isEmpty()
                                ? "Galaxy-Viewer-Analytics.json"
                                : filename);

                saveBytes(
                        safe,
                        "application/json",
                        json == null
                                ? new byte[0]
                                : json.getBytes(StandardCharsets.UTF_8));

                toast("Analytics saved");
                dispatchDownloadEvent("gv-native-download-complete", safe, null);
            } catch (Exception error) {
                toast("Analytics download failed");
                dispatchDownloadEvent(
                        "gv-native-download-failed",
                        filename,
                        String.valueOf(error.getMessage()));
            }
        }

        @JavascriptInterface
        public void saveDataUrl(String filename, String dataUrl) {
            try {
                int comma = dataUrl == null ? -1 : dataUrl.indexOf(',');
                if (comma < 0) throw new IllegalArgumentException("Invalid download data");

                String header = dataUrl.substring(0, comma);
                String mime = "application/octet-stream";
                int colon = header.indexOf(':');
                int semi = header.indexOf(';');
                if (colon >= 0 && semi > colon)
                    mime = header.substring(colon + 1, semi);

                byte[] bytes = Base64.decode(
                        dataUrl.substring(comma + 1),
                        Base64.DEFAULT);

                String safe = safeFilename(
                        filename == null || filename.isEmpty()
                                ? "Galaxy-Viewer-Download.bin"
                                : filename);

                saveBytes(safe, mime, bytes);

                toast("Download saved");
                dispatchDownloadEvent("gv-native-download-complete", safe, null);
            } catch (Exception error) {
                toast("Download failed");
                dispatchDownloadEvent(
                        "gv-native-download-failed",
                        filename,
                        String.valueOf(error.getMessage()));
            }
        }

        private void saveBytes(String filename, String mime, byte[] bytes)
                throws Exception {

            ContentValues values = new ContentValues();
            values.put(MediaStore.Downloads.DISPLAY_NAME, filename);
            values.put(MediaStore.Downloads.MIME_TYPE, mime);
            values.put(
                    MediaStore.Downloads.RELATIVE_PATH,
                    Environment.DIRECTORY_DOWNLOADS + "/" + DOWNLOAD_FOLDER);

            Uri target = context.getContentResolver().insert(
                    MediaStore.Downloads.EXTERNAL_CONTENT_URI,
                    values);

            if (target == null)
                throw new IllegalStateException("Could not create Android download");

            try (OutputStream output =
                         context.getContentResolver().openOutputStream(target)) {
                if (output == null)
                    throw new IllegalStateException("Could not open Android download");
                output.write(bytes);
            }
        }

        private void toast(String message) {
            webView.post(() ->
                    Toast.makeText(context, message, Toast.LENGTH_SHORT).show());
        }

        private void dispatchDownloadEvent(
                String eventName,
                String filename,
                String message) {

            String js =
                    "window.dispatchEvent(new CustomEvent("
                            + JSONObject.quote(eventName)
                            + ",{detail:{filename:"
                            + JSONObject.quote(filename == null ? "" : filename)
                            + ",message:"
                            + JSONObject.quote(message == null ? "" : message)
                            + "}}));";

            webView.post(() -> webView.evaluateJavascript(js, null));
        }
    }

    private static String safeFilename(String value) {
        String safe = value == null ? "download" : value.trim();
        safe = safe.replaceAll("[\\\\/:*?\"<>|]", "_");
        safe = safe.replace("..", "_");
        return safe.isEmpty() ? "download" : safe;
    }
}
