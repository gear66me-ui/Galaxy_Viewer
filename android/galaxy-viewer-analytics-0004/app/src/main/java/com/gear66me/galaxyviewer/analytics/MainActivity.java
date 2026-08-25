package com.gear66me.galaxyviewer.analytics;

import android.app.Activity;
import android.content.ContentValues;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.provider.MediaStore;
import android.view.Gravity;
import android.view.View;
import android.webkit.ConsoleMessage;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
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
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public final class MainActivity extends Activity {
    private static final String APP_BASE =
            "https://gear66me-ui.github.io/Galaxy_Viewer/mobile/beta/analytics-app-0003.html";
    private static final String APP_HOST = "gear66me-ui.github.io";
    private static final String APP_PATH = "/Galaxy_Viewer/";
    private static final String DOWNLOAD_FOLDER = "Galaxy Viewer Analytics";
    private static final int MAX_NATIVE_EVENTS = 12000;
    private static final long NATIVE_WATCHDOG_MS = 16000L;

    private final JSONArray nativeEvents = new JSONArray();
    private final Handler handler = new Handler(Looper.getMainLooper());
    private long nativeStartMs;
    private WebView webView;
    private View splash;
    private Typeface spaceAge;
    private volatile boolean viewerReady = false;

    private final Runnable heartbeat = new Runnable() {
        @Override public void run() {
            logNative("NATIVE_HEARTBEAT", "viewerReady=" + viewerReady);
            handler.postDelayed(this, 1000L);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        nativeStartMs = SystemClock.elapsedRealtime();
        super.onCreate(savedInstanceState);
        spaceAge = getResources().getFont(R.font.space_age);
        logNative("APP_CREATE", "analytics-4");

        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);

        FrameLayout root = new FrameLayout(this);
        GradientDrawable bg = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{0xFF020812, 0xFF061D45, 0xFF0B4AA2, 0xFF1484DB});
        root.setBackground(bg);
        setContentView(root);

        webView = new WebView(this);
        webView.setBackgroundColor(Color.BLACK);
        webView.setVisibility(View.INVISIBLE);
        root.addView(webView, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT));

        buildSplash(root);
        buildBadge(root);
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
        logNative("WEBSETTINGS_READY", "LOAD_NO_CACHE");

        AuditBridge bridge = new AuditBridge();
        webView.addJavascriptInterface(bridge, "GalaxyViewerAndroid");
        webView.addJavascriptInterface(bridge, "GalaxyViewerDownloads");
        webView.addJavascriptInterface(bridge, "GalaxyViewerNativeAudit");

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
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                logNative("RESOURCE_REQUEST",
                        request.getMethod() + " " + request.getUrl() + " main=" + request.isForMainFrame());
                return null;
            }

            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                logNative("PAGE_STARTED", url);
            }

            @Override
            public void onPageCommitVisible(WebView view, String url) {
                logNative("PAGE_COMMIT_VISIBLE", url);
                view.setVisibility(View.VISIBLE);
                removeSplash();
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                logNative("PAGE_FINISHED", url);
                view.setVisibility(View.VISIBLE);
                removeSplash();
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                logNative("WEB_ERROR",
                        request.getUrl() + " code=" + error.getErrorCode() + " " + error.getDescription());
            }

            @Override
            public void onReceivedHttpError(WebView view, WebResourceRequest request, WebResourceResponse response) {
                logNative("HTTP_ERROR",
                        request.getUrl() + " status=" + response.getStatusCode() + " " + response.getReasonPhrase());
            }
        });

        handler.post(heartbeat);
        handler.postDelayed(() -> {
            if (!viewerReady) {
                logNative("STARTUP_WATCHDOG_16S", "viewer not ready");
                saveNativeAudit("NATIVE_WATCHDOG_16S");
            }
        }, NATIVE_WATCHDOG_MS);

        String freshUrl = APP_BASE
                + "?source=android-analytics-4"
                + "&analytics=4"
                + "&cacheBust=" + System.currentTimeMillis();
        logNative("LOAD_URL", freshUrl);
        webView.loadUrl(freshUrl);
    }

    @Override
    protected void onDestroy() {
        handler.removeCallbacksAndMessages(null);
        if (webView != null) {
            webView.stopLoading();
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }

    private void purgeAnalyticsWebData() {
        logNative("CACHE_PURGE_START", "analytics-only");
        try { webView.stopLoading(); logNative("CACHE_STEP", "stopLoading"); } catch (Exception e) { logNative("CACHE_ERROR", String.valueOf(e)); }
        try { webView.clearCache(true); logNative("CACHE_STEP", "clearCache"); } catch (Exception e) { logNative("CACHE_ERROR", String.valueOf(e)); }
        try { webView.clearHistory(); logNative("CACHE_STEP", "clearHistory"); } catch (Exception e) { logNative("CACHE_ERROR", String.valueOf(e)); }
        try { webView.clearFormData(); logNative("CACHE_STEP", "clearFormData"); } catch (Exception e) { logNative("CACHE_ERROR", String.valueOf(e)); }
        try { WebStorage.getInstance().deleteAllData(); logNative("CACHE_STEP", "deleteWebStorage"); } catch (Exception e) { logNative("CACHE_ERROR", String.valueOf(e)); }
        try {
            CookieManager cm = CookieManager.getInstance();
            cm.setAcceptCookie(true);
            cm.removeAllCookies(null);
            cm.removeSessionCookies(null);
            cm.flush();
            logNative("CACHE_STEP", "clearCookies");
        } catch (Exception e) { logNative("CACHE_ERROR", String.valueOf(e)); }
        logNative("CACHE_PURGE_END", "analytics-only");
    }

    private TextView text(String value, float size, int color) {
        TextView v = new TextView(this);
        v.setText(value);
        v.setTextSize(size);
        v.setTextColor(color);
        v.setGravity(Gravity.CENTER);
        v.setTypeface(spaceAge);
        return v;
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

        TextView title = text("GALAXY VIEWER", 25, 0xFFF3FBFF);
        title.setPadding(0, 24, 0, 8);
        box.addView(title);

        TextView analytics = text("ANALYTICS MODE 4", 15, 0xFF8FE8FF);
        analytics.setLetterSpacing(0.10f);
        box.addView(analytics);

        TextView fast = text("FAST START · 15 SECOND FAILURE GATE", 9, 0xFF78FFAB);
        fast.setPadding(0, 12, 0, 0);
        box.addView(fast);

        splash = box;
        root.addView(box, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT));
    }

    private void buildBadge(FrameLayout root) {
        TextView badge = text("ANALYTICS 4 · RECORDING", 9, 0xFFEAFBFF);
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

    private synchronized void logNative(String type, String detail) {
        try {
            JSONObject item = new JSONObject();
            item.put("elapsedMs", Math.max(0, SystemClock.elapsedRealtime() - nativeStartMs));
            item.put("epochMs", System.currentTimeMillis());
            item.put("type", type == null ? "EVENT" : type);
            item.put("detail", detail == null ? "" : detail);
            nativeEvents.put(item);
            while (nativeEvents.length() > MAX_NATIVE_EVENTS) nativeEvents.remove(0);
        } catch (Exception ignored) { }
    }

    private synchronized String nativeAuditJson(String reason) {
        try {
            JSONObject root = new JSONObject();
            root.put("version", "analytics-native-0004");
            root.put("reason", reason == null ? "EXPORT" : reason);
            root.put("elapsedMs", Math.max(0, SystemClock.elapsedRealtime() - nativeStartMs));
            root.put("viewerReady", viewerReady);
            root.put("events", new JSONArray(nativeEvents.toString()));
            return root.toString(2);
        } catch (Exception error) {
            return "{\"version\":\"analytics-native-0004\",\"events\":[]}";
        }
    }

    private void saveNativeAudit(String reason) {
        String stamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss", Locale.US).format(new Date());
        String name = "Galaxy-Viewer-Native-Startup-Audit-" + stamp + ".json";
        try {
            saveBytes(name, "application/json", nativeAuditJson(reason).getBytes(StandardCharsets.UTF_8));
            logNative("NATIVE_AUDIT_SAVED", name);
        } catch (Exception error) {
            logNative("NATIVE_AUDIT_SAVE_FAILED", String.valueOf(error));
        }
    }

    private void saveBytes(String filename, String mime, byte[] bytes) throws Exception {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Downloads.DISPLAY_NAME, safeFilename(filename));
        values.put(MediaStore.Downloads.MIME_TYPE, mime);
        values.put(MediaStore.Downloads.RELATIVE_PATH,
                Environment.DIRECTORY_DOWNLOADS + "/" + DOWNLOAD_FOLDER);
        values.put(MediaStore.Downloads.IS_PENDING, 1);
        Uri uri = getContentResolver().insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
        if (uri == null) throw new IllegalStateException("MediaStore insert failed");
        try (OutputStream out = getContentResolver().openOutputStream(uri)) {
            if (out == null) throw new IllegalStateException("Output stream unavailable");
            out.write(bytes);
            out.flush();
        }
        ContentValues done = new ContentValues();
        done.put(MediaStore.Downloads.IS_PENDING, 0);
        getContentResolver().update(uri, done, null, null);
    }

    private String safeFilename(String value) {
        String cleaned = String.valueOf(value == null ? "Galaxy-Viewer-Audit.json" : value)
                .replaceAll("[^A-Za-z0-9._-]", "_");
        return cleaned.isEmpty() ? "Galaxy-Viewer-Audit.json" : cleaned;
    }

    private void toast(String text) {
        runOnUiThread(() -> Toast.makeText(MainActivity.this, text, Toast.LENGTH_SHORT).show());
    }

    private final class AuditBridge {
        @JavascriptInterface
        public String getNativeAudit() { return nativeAuditJson("JS_EXPORT"); }

        @JavascriptInterface
        public void mark(String type, String detail) {
            if ("VIEWER_READY".equals(type)) viewerReady = true;
            logNative("JS_MARK_" + String.valueOf(type), detail);
        }

        @JavascriptInterface
        public void saveJson(String filename, String json) {
            try {
                String safe = safeFilename(filename);
                saveBytes(safe, "application/json",
                        (json == null ? "" : json).getBytes(StandardCharsets.UTF_8));
                logNative("JSON_SAVED", safe);
                toast("Analytics audit saved");
            } catch (Exception error) {
                logNative("JSON_SAVE_FAILED", String.valueOf(error));
                toast("Analytics audit save failed");
            }
        }
    }
}
