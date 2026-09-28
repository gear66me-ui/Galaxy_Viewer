package com.gear66me.galaxyviewer.webbrowser;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class MainActivity extends Activity {
    private static final String RAW = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/";
    private static final String MASTER = RAW + "viewer/image-databases/master-database/gv-master-catalog.json";
    private static final int CYAN = Color.rgb(119,233,255);
    private static final int DEEP = Color.rgb(2,7,19);
    private static final int BLUE = Color.rgb(8,47,112);

    private final ExecutorService io = Executors.newSingleThreadExecutor();
    private final Random rng = new Random();
    private final List<Source> pool = new ArrayList<>();
    private final List<Source> randomHistory = new ArrayList<>();
    private int randomHistoryPos = -1;
    private int randomSequence = 0;

    private WebView web;
    private WebView providerIcon;
    private WebView gvIcon;
    private TextView urlText;
    private TextView statusText;
    private TextView titleText;
    private Source current;

    static final class Source {
        final String provider, name, url, type, icon;
        Source(String provider, String name, String url, String type, String icon) {
            this.provider=provider; this.name=name; this.url=url; this.type=type; this.icon=icon;
        }
    }

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        immersive();
        setContentView(buildUi());
        configureWebView();
        statusText.setText("LOADING GALAXY VIEWER MASTER CATALOG…");
        loadCatalogPool();
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

    private View buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(8),dp(8),dp(8),dp(8));
        root.setBackground(spaceBackground());

        LinearLayout top = row();
        titleText = label("GALAXY VIEWER", 18, true);
        titleText.setGravity(Gravity.CENTER);
        top.addView(box(titleText), new LinearLayout.LayoutParams(0, dp(58), 1f));
        providerIcon = iconWebView();
        LinearLayout.LayoutParams ip = new LinearLayout.LayoutParams(dp(58),dp(58));
        ip.setMargins(dp(7),0,0,0);
        top.addView(box(providerIcon),ip);
        root.addView(top, matchWrap());

        LinearLayout controls = row();
        controls.setPadding(dp(6),dp(6),dp(6),dp(6));
        controls.setBackground(neonBox(13));

        TextView back = button("‹",34);
        TextView forward = button("›",34);
                back.setOnClickListener(v -> goBackSafe());
        forward.setOnClickListener(v -> randomWebsite());

        controls.addView(back, new LinearLayout.LayoutParams(dp(48),dp(48)));
        LinearLayout.LayoutParams fp = new LinearLayout.LayoutParams(dp(48),dp(48)); fp.setMargins(dp(6),0,dp(6),0);
        controls.addView(forward,fp);

        LinearLayout address = row();
        address.setGravity(Gravity.CENTER_VERTICAL);
        address.setPadding(dp(10),0,dp(10),0);
        address.setBackground(darkInset());
        TextView lock = label("🔒",17,false);
        urlText = label("Loading catalog…",14,false);
        urlText.setSingleLine(true);
        urlText.setEllipsize(android.text.TextUtils.TruncateAt.END);
        address.addView(lock,new LinearLayout.LayoutParams(dp(28),dp(44)));
        address.addView(urlText,new LinearLayout.LayoutParams(0,dp(44),1f));
        controls.addView(address,new LinearLayout.LayoutParams(0,dp(48),1f));
        

        LinearLayout.LayoutParams cp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,dp(62)); cp.setMargins(0,dp(7),0,dp(7));
        root.addView(controls,cp);

        FrameLayout webFrame = new FrameLayout(this);
        webFrame.setPadding(dp(2),dp(2),dp(2),dp(2));
        webFrame.setBackground(neonBox(15));
        web = new WebView(this);
        web.setBackgroundColor(Color.BLACK);
        web.setHorizontalScrollBarEnabled(false);
        web.setVerticalScrollBarEnabled(true);
        webFrame.addView(web,new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.MATCH_PARENT));
        root.addView(webFrame,new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,0,1f));

        statusText = label("READY",11,false);
        statusText.setSingleLine(true);
        statusText.setEllipsize(android.text.TextUtils.TruncateAt.END);
        statusText.setGravity(Gravity.CENTER_VERTICAL);
        statusText.setPadding(dp(9),0,dp(9),0);
        LinearLayout.LayoutParams sp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,dp(28)); sp.setMargins(0,dp(5),0,dp(5));
        root.addView(statusText,sp);

        LinearLayout footer = row();
        footer.setGravity(Gravity.CENTER_VERTICAL);
        footer.setPadding(dp(6),dp(5),dp(6),dp(5));
        footer.setBackground(neonBox(14));
        TextView footBack = button("‹",34);
        footBack.setOnClickListener(v -> finish());
        TextView footText = label("BACK TO GALAXY VIEWER",15,true);
        footText.setGravity(Gravity.CENTER);
        footText.setOnClickListener(v -> finish());
        gvIcon = iconWebView();
        setIconHtml(gvIcon,"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg");
        footer.addView(footBack,new LinearLayout.LayoutParams(dp(54),dp(52)));
        footer.addView(footText,new LinearLayout.LayoutParams(0,dp(52),1f));
        footer.addView(gvIcon,new LinearLayout.LayoutParams(dp(54),dp(52)));
        root.addView(footer,new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,dp(64)));
        return root;
    }

    private void configureWebView() {
        WebSettings s=web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setSupportZoom(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false);
        s.setTextZoom(100);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setCacheMode(WebSettings.LOAD_DEFAULT);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        s.setUserAgentString(s.getUserAgentString()+" GalaxyViewerWebBrowser/0001");
        web.setWebChromeClient(new WebChromeClient());
        web.setWebViewClient(new WebViewClient(){
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri u=request.getUrl();
                if(u==null || !"https".equalsIgnoreCase(u.getScheme())) return true;
                return false;
            }
            @Override public void onPageFinished(WebView view,String url) {
                urlText.setText(url==null?"":url);
                String fit="(function(){try{var m=document.querySelector('meta[name=viewport]');if(!m){m=document.createElement('meta');m.name='viewport';document.head.appendChild(m);}m.content='width=device-width,initial-scale=1,maximum-scale=5,user-scalable=yes';var s=document.getElementById('gvwb-fit');if(!s){s=document.createElement('style');s.id='gvwb-fit';s.textContent='html,body{max-width:100%!important;overflow-x:hidden!important}img,video,iframe,canvas,svg{max-width:100%!important;height:auto}pre,code{white-space:pre-wrap!important;word-break:break-word!important}';document.head.appendChild(s);}}catch(e){}})();";
                view.evaluateJavascript(fit,null);
            }
        });
    }

    private void loadCatalogPool() {
        io.execute(() -> {
            try {
                JSONObject master = new JSONObject(fetch(MASTER));
                JSONObject catalogs = master.getJSONObject("catalogs");
                Iterator<String> keys = catalogs.keys();
                List<Source> found = new ArrayList<>();
                while(keys.hasNext()) {
                    String key=keys.next();
                    String path=catalogs.optString(key,"");
                    if(path.isEmpty()) continue;
                    try {
                        JSONObject catalog=new JSONObject(fetch(RAW+path));
                        String archive=catalog.optString("sourceArchiveUrl","");
                        JSONArray entries=catalog.optJSONArray("entries");
                        int before=found.size();
                        if(entries!=null) for(int i=0;i<entries.length();i++) {
                            JSONObject e=entries.optJSONObject(i); if(e==null) continue;
                            String provider=first(e.optString("provider"),catalog.optString("provider"),catalog.optString("providerLabel"),key);
                            String name=first(e.optString("displayName"),e.optString("commonName"),e.optString("name"),e.optString("title"),e.optString("archiveId"),"Unknown object");
                            String page=firstHttps(e.optString("sourceUrl"),e.optString("pageUrl"),e.optString("releaseUrl"),e.optString("astroPixSourceUrl"));
                            String direct=firstHttps(e.optString("selectedImageUrl"),e.optString("hdUrl"),e.optString("imageUrl"),firstArray(e.optJSONArray("jpegCandidates")));
                            String chosen=!page.isEmpty()?page:direct;
                            if(chosen.isEmpty()) continue;
                            String type=!page.isEmpty()?"SOURCE PAGE":"DIRECT IMAGE FALLBACK";
                            String slug=provider.toLowerCase().replaceAll("[^a-z0-9]+","-").replaceAll("(^-|-$)","");
                            String icon=firstHttps(e.optString("providerIconUrl"),e.optString("provider_icon_url"));
                            if(icon.isEmpty()&&!slug.isEmpty()) icon="https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/providers/"+Uri.encode(slug)+"/"+Uri.encode(slug)+"-icon.png";
                            found.add(new Source(provider,name,chosen,type,icon));
                        }
                        if(found.size()==before && isHttps(archive)) found.add(new Source(key,key+" archive",archive,"PROVIDER ARCHIVE", ""));
                    } catch(Exception ignored) {}
                }
                Collections.shuffle(found,rng);
                runOnUiThread(() -> {
                    pool.clear(); pool.addAll(found);
                    if(pool.isEmpty()) {
                        statusText.setText("MASTER CATALOG LOADED — NO USABLE HTTPS SOURCE URLS");
                        urlText.setText(MASTER);
                    } else {
                        statusText.setText("SOURCE POOL READY · "+pool.size()+" URLS");
                        randomWebsite();
                    }
                });
            } catch(Exception ex) {
                runOnUiThread(() -> {
                    statusText.setText("CATALOG ERROR · "+ex.getClass().getSimpleName()+": "+String.valueOf(ex.getMessage()));
                    urlText.setText(MASTER);
                });
            }
        });
    }

    private void randomWebsite() {
        if(pool.isEmpty()) return;
        Source next=pool.get(rng.nextInt(pool.size()));
        if(pool.size()>1 && current!=null) {
            for(int tries=0;tries<8 && next.url.equals(current.url);tries++) next=pool.get(rng.nextInt(pool.size()));
        }
        if(randomHistoryPos < randomHistory.size()-1) randomHistory.subList(randomHistoryPos+1,randomHistory.size()).clear();
        randomHistory.add(next); randomHistoryPos=randomHistory.size()-1;
        loadSource(next);
    }

    private void previousRandomSource() {
        if(randomHistoryPos>0) { randomHistoryPos--; loadSource(randomHistory.get(randomHistoryPos)); }
    }

    private void goBackSafe() {
        if(web!=null && web.canGoBack()) web.goBack();
        else previousRandomSource();
    }

    private void loadSource(Source source) {
        current=source; randomSequence++;
        urlText.setText(source.url);
        statusText.setText(source.provider+" · "+source.name+" · RANDOM "+randomSequence+"/"+pool.size()+" · "+source.type);
        if(source.icon!=null&&!source.icon.isEmpty()) setIconHtml(providerIcon,source.icon);
        else setIconHtml(providerIcon,"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg");
        web.loadUrl(source.url);
    }

    private static String fetch(String u) throws Exception {
        HttpURLConnection c=(HttpURLConnection)new URL(u).openConnection();
        c.setConnectTimeout(12000); c.setReadTimeout(20000); c.setInstanceFollowRedirects(true);
        c.setRequestProperty("User-Agent","GalaxyViewerWebBrowser/0001");
        int code=c.getResponseCode(); if(code<200||code>=300) throw new Exception("HTTP "+code);
        BufferedReader r=new BufferedReader(new InputStreamReader(c.getInputStream()));
        StringBuilder b=new StringBuilder(); String line; while((line=r.readLine())!=null)b.append(line).append('\n');
        r.close(); c.disconnect(); return b.toString();
    }

    private WebView iconWebView() {
        WebView w=new WebView(this); w.setBackgroundColor(Color.TRANSPARENT); w.setVerticalScrollBarEnabled(false); w.setHorizontalScrollBarEnabled(false);
        w.getSettings().setJavaScriptEnabled(false); w.getSettings().setLoadWithOverviewMode(true); w.getSettings().setUseWideViewPort(true);
        w.setOnTouchListener((v,e)->true); return w;
    }
    private void setIconHtml(WebView w,String src) {
        String safe=src.replace("&","&amp;").replace("\"","&quot;").replace("<","&lt;").replace(">","&gt;");
        String h="<!doctype html><meta name='viewport' content='width=device-width,initial-scale=1'><style>html,body{margin:0;width:100%;height:100%;background:transparent;overflow:hidden}body{display:grid;place-items:center}img{width:88%;height:88%;object-fit:contain;border-radius:12px}</style><img src=\""+safe+"\">";
        w.loadDataWithBaseURL("https://gear66me-ui.github.io/",h,"text/html","UTF-8",null);
    }

    private LinearLayout row(){ LinearLayout x=new LinearLayout(this); x.setOrientation(LinearLayout.HORIZONTAL); return x; }
    private TextView label(String text,int sp,boolean futuristic) {
        TextView t=new TextView(this); t.setText(text); t.setTextColor(Color.rgb(239,255,255)); t.setTextSize(sp);
        t.setGravity(Gravity.CENTER_VERTICAL); t.setTypeface(Typeface.create(futuristic?"sans-serif-light":"sans-serif",futuristic?Typeface.BOLD:Typeface.NORMAL));
        if(futuristic) t.setLetterSpacing(.08f); return t;
    }
    private TextView button(String text,int sp) {
        TextView t=label(text,sp,false); t.setGravity(Gravity.CENTER); t.setTypeface(Typeface.DEFAULT_BOLD); t.setBackground(neonButton()); t.setClickable(true); t.setFocusable(true); return t;
    }
    private View box(View child) {
        FrameLayout f=new FrameLayout(this); f.setPadding(dp(3),dp(3),dp(3),dp(3)); f.setBackground(neonBox(14));
        f.addView(child,new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.MATCH_PARENT)); return f;
    }
    private GradientDrawable neonBox(int radius) {
        GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{Color.rgb(4,17,44),Color.rgb(9,56,130),Color.rgb(4,19,48)});
        g.setCornerRadius(dp(radius)); g.setStroke(dp(2),CYAN); return g;
    }
    private GradientDrawable neonButton() {
        GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{Color.rgb(6,22,56),Color.rgb(10,63,154),Color.rgb(18,139,225)});
        g.setCornerRadius(dp(11)); g.setStroke(dp(1),CYAN); return g;
    }
    private GradientDrawable darkInset() {
        GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{Color.rgb(4,14,40),Color.rgb(0,4,15)});
        g.setCornerRadius(dp(11)); g.setStroke(dp(1),Color.rgb(55,142,176)); return g;
    }
    private GradientDrawable spaceBackground() {
        GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{Color.rgb(2,10,28),Color.BLACK}); return g;
    }
    private LinearLayout.LayoutParams matchWrap(){ return new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT); }
    private int dp(int n){ return Math.round(n*getResources().getDisplayMetrics().density); }

    private static String first(String... values){ for(String v:values) if(v!=null&&!v.trim().isEmpty()) return v.trim(); return ""; }
    private static String firstHttps(String... values){ for(String v:values) if(isHttps(v)) return v.trim(); return ""; }
    private static String firstArray(JSONArray a){ if(a==null)return ""; for(int i=0;i<a.length();i++){String s=a.optString(i,""); if(isHttps(s))return s;} return ""; }
    private static boolean isHttps(String s){ try{return s!=null&&"https".equalsIgnoreCase(Uri.parse(s.trim()).getScheme());}catch(Exception e){return false;} }

    @Override public void onBackPressed(){ goBackSafe(); }
    @Override protected void onDestroy(){ if(web!=null)web.destroy(); if(providerIcon!=null)providerIcon.destroy(); if(gvIcon!=null)gvIcon.destroy(); io.shutdownNow(); super.onDestroy(); }
}
