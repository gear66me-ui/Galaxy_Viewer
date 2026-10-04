# Galaxy Viewer Web Performance Logbook

Purpose: keep provider-loading experiments reproducible. Each APK entry records the native browser change, the hypothesis, and the user's observed behavior so later changes can be correlated instead of guessed.

## Baselines

### APK 0018 — WebKit 1.17.1 — Build 0060 viewer

Native identity: `APK-0018-DEV-0057-WEBKIT1171-CHANDRAFIT`

Preserved behavior:
- WebKit 1.17.1.
- Chandra-only fit-to-width overview mode.
- Provider cookies / DOM storage / normal `LOAD_DEFAULT` WebView cache.
- Hosted Galaxy Viewer Build 0060.
- Provider prewarm requested only after destination arrival.

Pre-APK19 provider architecture:
- Landing prewarm used renderer warm-up, preconnect, prefetch/prerender.
- Pressing WEB started a provider navigation even when the same requested provider page was already prewarming or had been loaded before.
- A 10-second watchdog could trigger a restart, followed by a longer retry window.
- Back to Sky hid the provider WebView but the next WEB press did not simply reveal/reuse it.

User observations, 2026-10-04:
- Hubble “Panoramic View of Andromeda” first provider launch took more than one minute.
- Returning to Galaxy Viewer and opening the same provider page again still took about 20 seconds.
- Some provider pages appeared not to benefit from prewarm/cache.
- Working hypothesis: pressing WEB before speculative prewarm is ready can replace/restart the provider navigation, discarding useful in-flight progress.

### Reference: TABLET 0002 — WebKit 1.14.0

Native identity: `DEV-0057-TABLET-2`

Known identifying feature:
- Red `57 TEST` badge.
- AndroidX WebKit 1.14.0.

User observation:
- Provider pages often launch much faster.
- Viewer stutter is somewhat higher but currently not catastrophic.
- Keep as an A/B reference; do not use as the APK19 baseline.

## Experiment: APK 0019 — Persistent provider load/reuse

Status: build requested.

Baseline rule: APK 0019 is APK 0018 plus provider-loading/cache instrumentation only. Do not remove Chandra fit-width or alter Galaxy Viewer travel/viewer behavior.

Hypothesis:
1. A real provider WebView load begun after landing will populate the browser's ordinary HTTP cache, cookies, DOM/storage and live page state more reliably than speculative prerender alone.
2. If WEB is pressed while that same load is still in progress, revealing the existing WebView without calling `loadUrl` or `navigate` again should preserve all progress.
3. If WEB is pressed after the page is ready, revealing the same live WebView should be nearly immediate.
4. Back to Sky should hide the provider only; it must not stop or reload the current provider page.
5. Only navigation to a different astronomical destination should stop the old provider load.

APK19 code changes:
- Heavy provider work still starts only after destination arrival.
- Landing prewarm becomes a real hidden `web.loadUrl(sourceUrl)`.
- Renderer warm-up and preconnect are retained.
- Speculative prefetch/prerender are not used for the primary same-page preload path.
- Provider layer is kept attached/invisible during background load.
- `LOAD_DEFAULT` cache remains enabled.
- Offscreen preraster is enabled for the provider WebView.
- Same requested URL on WEB press: reveal existing provider WebView; do not navigate/restart.
- No timeout-driven same-page restart on WEB press.
- Back to Sky: hide only, preserving provider WebView/network/DOM/render state.
- Different destination: cancel old provider work as before.

Diagnostic indicator:
- A tiny green horizontal bar is injected immediately below the provider icon in the hosted viewer.
- Bar width is Android WebView `onProgressChanged` (0–100). This is WebView's page-load progress estimate, not a byte-exact download percentage.
- A tiny LED at the right turns green only after `onPageFinished` for the current provider load.
- Full bar with dark LED means WebView reported 100% progress but the current page has not yet passed the ready gate.
- The indicator is APK19-only and is intentionally subtle.

## APK19 test sheet

For each test, record:

| Field | Observation |
|---|---|
| Provider / object | |
| Time spent on galaxy before pressing WEB | |
| Green bar percentage when WEB pressed | |
| Ready LED green before WEB press? | |
| First WEB press: time to usable page | |
| Did page visibly restart at WEB press? | |
| Back to Sky, then second WEB press: latency | |
| Second press reused exact page/scroll state? | |
| Viewer stutter during/after landing preload | |
| Network conditions / phone load notes | |
| Other behavior | |

Priority regression target: Hubble “Panoramic View of Andromeda”.
