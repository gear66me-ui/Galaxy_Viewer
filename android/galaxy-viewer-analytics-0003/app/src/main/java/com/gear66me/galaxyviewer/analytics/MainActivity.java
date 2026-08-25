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
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.Gravity;
import android.view.View;
import android.webkit.ConsoleMessage;
import android.webkit.CookieManager;
import android.webkit.DownloadListener;
import android.webkit.JavascriptInterface;
import android.webkit.URLUtil;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebStorage;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public final class MainActivity extends Activity {
    private static final String APP_BASE =
            "https://gear66me-ui.github.io/Galaxy_Viewer/mobile/beta/analytics-app-0002.html";
    private static final String APP_HOST = "gear66me-ui.github.io";
    private static final String APP_PATH = "/Galaxy_Viewer/";
    private static final String DOWNLOAD_FOLDER = "Galaxy Viewer Analytics";
    private static final int MAX_NATIVE_EVENTS = 20000;

    private final JSONArray nativeEvents = new JSONArray();
    private final Handler auditHandler = new Handler(Looper.getMainLooper());
    private long nativeStartMs;
    private WebView webView;
    private View splash;
    private boolean startupReady = false;
    private boolean startupAuditSaved = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        nativeStartMs = SystemClock.elapsedRealtime();
        super.onCreate(savedInstanceState);
        logNative("APP_CREATE", "analytics-3");

        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
        logNative("SYSTEM_UI_READY", "immersive");

        FrameLayout root = new FrameLayout(this);
        GradientDrawable rootGradient = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{0xFF020812, 0xFF061D45, 0xFF0B4AA2, 0xFF1484DB});
        root.setBackground(rootGradient);
        setContentView(root);
        logNative("ROOT_READY", "blue-gradient");

        webView = new WebView(this);
        webView.setBackgroundColor(Color.BLACK);
        webView.setVisibility(View.INVISIBLE);
        root.addView(webView, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT));
        logNative("WEBVIEW_CREATED", "invisible");

        buildSplash(root);
        buildAnalyticsBadge(root);
        logNative("NATIVE_SPLASH_READY", "ANALYTICS MODE 3");

        logNative("CACHE_PURGE_START", "all analytics web data");
        purgeAnalyticsWebData();
        logNative("CACHE_PURGE_END", "all analytics web data");

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
        logNative("WEBSETTINGS_READY", "LOAD_NO_CACHE");

        AuditBridge bridge = new AuditBridge(this);
        webView.addJavascriptInterface(bridge, "GalaxyViewerAndroid");
        webView.addJavascriptInterface(bridge, "GalaxyViewerDownloads");
        webView.addJavascriptInterface(bridge, "GalaxyViewerNativeAudit");
        logNative("JS_BRIDGES_READY", "downloads+native-audit+failsafe");

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(ConsoleMessage message) {
                logNative("CONSOLE_" + message.messageLevel().name(),
                        message.message() + " @" + message.sourceId() + ":" + message.lineNumber());
                return super.onConsoleMessage(message);
            }
        });

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
                boolean blocked = !allowed(request.getUrl());
                logNative(blocked ? "NAV_BLOCKED" : "NAV_ALLOWED", String.valueOf(request.getUrl()));
                return blocked;
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                boolean blocked = !allowed(Uri.parse(url));
                logNative(blocked ? "NAV_BLOCKED" : "NAV_ALLOWED", url);
                return blocked;
            }

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                logNative("RESOURCE_REQUEST",
                        request.getMethod() + " " + uri + " main=" + request.isForMainFrame());
                return null;
            }

            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                logNative("PAGE_STARTED", url);
            }

            @Override
            public void onPageCommitVisible(WebView view, String url) {
                super.onPageCommitVisible(view, url);
                logNative("PAGE_COMMIT_VISIBLE", url);
                view.setVisibility(View.VISIBLE);
                removeSplash();
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                logNative("PAGE_FINISHED", url);
                view.evaluateJavascript(
                        "(async()=>{try{if(window.caches){for(const k of await caches.keys())await caches.delete(k)}}catch(e){console.error('CACHE_STORAGE_CLEAR_FAILED',e)}})();",
                        null);
                view.setVisibility(View.VISIBLE);
                removeSplash();
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                super.onReceivedError(view, request, error);
                logNative("WEB_ERROR",
                        String.valueOf(request.getUrl()) + " code=" + error.getErrorCode()
                                + " " + error.getDescription());
            }

            @Override
            public void onReceivedHttpError(WebView view, WebResourceRequest request, WebResourceResponse errorResponse) {
                super.onReceivedHttpError(view, request, errorResponse);
                logNative("HTTP_ERROR",
                        String.valueOf(request.getUrl()) + " status=" + errorResponse.getStatusCode()
                                + " " + errorResponse.getReasonPhrase());
            }
        });

        webView.setDownloadListener(new GalaxyDownloadListener());

        startNativeHeartbeat();
        scheduleStartupWatchdog();

        String freshUrl = APP_BASE
                + "?source=android-analytics-3"
                + "&analytics=3"
                + "&cacheBust=" + System.currentTimeMillis();
        logNative("LOAD_URL", freshUrl);
        webView.loadUrl(freshUrl);
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (nativeStartMs != 0) logNative("APP_RESUME", "");
    }

    @Override
    protected void onPause() {
        if (nativeStartMs != 0) logNative("APP_PAUSE", "");
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        auditHandler.removeCallbacksAndMessages(null);
        super.onDestroy();
    }

    private void startNativeHeartbeat() {
        auditHandler.post(new Runnable() {
            private int second = 0;
            @Override
            public void run() {
                second++;
                logNative("NATIVE_HEARTBEAT", "second=" + second
                        + " ready=" + startupReady
                        + " auditSaved=" + startupAuditSaved);
                auditHandler.postDelayed(this, 1000L);
            }
        });
    }

    private void scheduleStartupWatchdog() {
        auditHandler.postDelayed(() -> {
            if (startupReady || startupAuditSaved) return;
            logNative("STARTUP_WATCHDOG_50S", "requesting JS audit save");
            if (webView != null) {
                webView.evaluateJavascript(
                        "(async()=>{try{if(window.__GV_ANALYTICS_SAVE_NOW__){await window.__GV_ANALYTICS_SAVE_NOW__('NATIVE_WATCHDOG_50S',{message:'Native startup watchdog fired'});}else if(window.GalaxyViewerNativeAudit&&window.GalaxyViewerNativeAudit.saveNativeAudit){window.GalaxyViewerNativeAudit.saveNativeAudit('JS_SAVE_UNAVAILABLE');}}catch(e){console.error('WATCHDOG_AUDIT_SAVE_FAILED',e)}})();",
                        null);
            }
            auditHandler.postDelayed(() -> {
                if (!startupReady && !startupAuditSaved) {
                    logNative("STARTUP_WATCHDOG_FALLBACK", "saving native-only audit");
                    saveNativeAuditFile("NATIVE_WATCHDOG_FALLBACK");
                }
            }, 5000L);
        }, 50000L);
    }

    private synchronized void logNative(String type, String detail) {
        try {
            JSONObject item = new JSONObject();
            item.put("elapsedMs", nativeStartMs == 0 ? 0 : SystemClock.elapsedRealtime() - nativeStartMs);
            item.put("epochMs", System.currentTimeMillis());
            item.put("type", type == null ? "EVENT" : type);
            item.put("detail", detail == null ? "" : detail);
            nativeEvents.put(item);
            while (nativeEvents.length() > MAX_NATIVE_EVENTS) nativeEvents.remove(0);
        } catch (Exception ignored) {}
    }

    private synchronized String nativeAuditJson() {
        try {
            JSONObject root = new JSONObject();
            root.put("version", "analytics-native-0003");
            root.put("elapsedMs", SystemClock.elapsedRealtime() - nativeStartMs);
            root.put("startupReady", startupReady);
            root.put("startupAuditSaved", startupAuditSaved);
            root.put("events", new JSONArray(nativeEvents.toString()));
            return root.toString();
        } catch (Exception error) {
            return "{\"version\":\"analytics-native-0003\",\"events\":[]}";
        }
    }

    private synchronized void saveNativeAuditFile(String reason) {
        if (startupAuditSaved) return;
        try {
            JSONObject payload = new JSONObject();
            payload.put("module", "GalaxyViewerNativeStartupAudit");
            payload.put("version", "0003");
            payload.put("reason", reason == null ? "UNKNOWN" : reason);
            payload.put("nativeAudit", new JSONObject(nativeAuditJson()));
            String filename = "Galaxy-Viewer-Native-Startup-Audit-" + System.currentTimeMillis() + ".json";
            saveBytes(filename, "application/json", payload.toString(2).getBytes(StandardCharsets.UTF_8));
            startupAuditSaved = true;
            logNative("NATIVE_AUDIT_SAVED", filename);
        } catch (Exception error) {
            logNative("NATIVE_AUDIT_SAVE_FAILED", String.valueOf(error));
        }
    }

    private void purgeAnalyticsWebData() {
        try { webView.stopLoading(); logNative("CACHE_STEP", "stopLoading"); } catch (Exception e) { logNative("CACHE_ERROR", "stopLoading " + e); }
        try { webView.clearCache(true); logNative("CACHE_STEP", "clearCache"); } catch (Exception e) { logNative("CACHE_ERROR", "clearCache " + e); }
        try { webView.clearHistory(); logNative("CACHE_STEP", "clearHistory"); } catch (Exception e) { logNative("CACHE_ERROR", "clearHistory " + e); }
        try { webView.clearFormData(); logNative("CACHE_STEP", "clearFormData"); } catch (Exception e) { logNative("CACHE_ERROR", "clearFormData " + e); }
        try { WebStorage.getInstance().deleteAllData(); logNative("CACHE_STEP", "deleteWebStorage"); } catch (Exception e) { logNative("CACHE_ERROR", "deleteWebStorage " + e); }
        try {
            CookieManager cookies = CookieManager.getInstance();
            cookies.setAcceptCookie(true);
            cookies.removeAllCookies(null);
            cookies.removeSessionCookies(null);
            cookies.flush();
            logNative("CACHE_STEP", "clearCookies");
        } catch (Exception e) { logNative("CACHE_ERROR", "clearCookies " + e); }
    }

    private void buildSplash(FrameLayout root) {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setGravity(Gravity.CENTER);
        box.setPadding(36, 36, 36, 36);
        GradientDrawable bg = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{0xFF020812, 0xFF061D45, 0xFF0B3177, 0xFF1484DB});
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
        analytics.setText("ANALYTICS MODE 3");
        analytics.setTextColor(0xFF8FE8FF);
        analytics.setTextSize(16);
        analytics.setGravity(Gravity.CENTER);
        analytics.setLetterSpacing(0.12f);
        box.addView(analytics);

        TextView fresh = new TextView(this);
        fresh.setText("FAILSAFE AUDIT · AUTO SAVE · EVERY SECOND");
        fresh.setTextColor(0xFF78FFAB);
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
        badge.setText("ANALYTICS 3 · RECORDING");
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

    private void removeSplash() {
        if (splash != null && splash.getParent() instanceof FrameLayout) {
            ((FrameLayout)splash.getParent()).removeView(splash);
            splash = null;
            logNative("NATIVE_SPLASH_REMOVED", "");
        }
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
            logNative("DOWNLOAD_REQUEST", filename + " " + url);
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
            request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS,
                    DOWNLOAD_FOLDER + "/" + safeFilename(filename));
            DownloadManager manager = (DownloadManager)getSystemService(DOWNLOAD_SERVICE);
            manager.enqueue(request);
        }
    }

    private final class AuditBridge {
        private final Context context;
        AuditBridge(Context context) { this.context = context.getApplicationContext(); }

        @JavascriptInterface
        public String getNativeAudit() { return nativeAuditJson(); }

        @JavascriptInterface
        public void mark(String type, String detail) { logNative("JS_MARK_" + type, detail); }

        @JavascriptInterface
        public void startupReady() {
            startupReady = true;
            logNative("STARTUP_READY", "JS confirmed viewer ready");
        }

        @JavascriptInterface
        public void saveNativeAudit(String reason) {
            saveNativeAuditFile(reason);
        }

        @JavascriptInterface
        public void saveJson(String filename, String json) {
            try {
                String safe = safeFilename(filename == null || filename.isEmpty() ? "Galaxy-Viewer-Diagnostics.json" : filename);
                saveBytes(safe, "application/json", json == null ? new byte[0] : json.getBytes(StandardCharsets.UTF_8));
                if (safe.startsWith("Galaxy-Viewer-Startup-Audit-")) startupAuditSaved = true;
                logNative("JSON_SAVED", safe + " bytes=" + (json == null ? 0 : json.length()));
                toast("Audit saved");
            } catch (Exception error) {
                logNative("JSON_SAVE_FAILED", String.valueOf(error));
                toast("Audit save failed");
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
                if (colon >= 0 && semi > colon) mime = header.substring(colon + 1, semi);
                byte[] bytes = Base64.decode(dataUrl.substring(comma + 1), Base64.DEFAULT);
                String safe = safeFilename(filename == null || filename.isEmpty() ? "Galaxy-Viewer-Download.bin" : filename);
                saveBytes(safe, mime, bytes);
                logNative("DATA_URL_SAVED", safe + " " + bytes.length);
                toast("Download saved");
            } catch (Exception error) {
                logNative("DATA_URL_SAVE_FAILED", String.valueOf(error));
                toast("Download failed");
            }
        }

        private void toast(String message) {
            webView.post(() -> Toast.makeText(context, message, Toast.LENGTH_SHORT).show());
        }
    }

    private void saveBytes(String filename, String mime, byte[] bytes) throws Exception {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Downloads.DISPLAY_NAME, filename);
        values.put(MediaStore.Downloads.MIME_TYPE, mime);
        values.put(MediaStore.Downloads.RELATIVE_PATH,
                Environment.DIRECTORY_DOWNLOADS + "/" + DOWNLOAD_FOLDER);
        Uri target = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
        if (target == null) throw new IllegalStateException("Could not create Android download");
        try (OutputStream output = getContentResolver().openOutputStream(target)) {
            if (output == null) throw new IllegalStateException("Could not open Android download");
            output.write(bytes);
        }
    }

    private static String safeFilename(String value) {
        String safe = value == null ? "download" : value.trim();
        safe = safe.replaceAll("[\\\\/:*?\"<>|]", "_");
        safe = safe.replace("..", "_");
        return safe.isEmpty() ? "download" : safe;
    }
}
