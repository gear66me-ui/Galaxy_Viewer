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

Status: build successful.

Build record:
- Workflow run: `37213000341`
- Artifact ID: `11307551343`
- Workflow commit: `b63461051272e7d697e511667c6b2e15ced36b86`
- APK SHA-256: `3bb6392b7fe931fca648dcb19f6d2eae3e000ddfc0db4d2817b73c44dd238ec5`
- Verified embedded AndroidX WebKit version: `1.17.1`.

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


## Hosted instrumentation revision — Build 0061

Date: 2026-10-04.

Purpose: refine APK19 preload telemetry visibility without changing native provider/cache behavior.

Changes:
- Destination-card provider indicator reduced to a 24 px hairline, 1 px high, faint green, with a 2 px faint ready LED.
- View-HD provider indicator moved fully inside the 48 px provider/WEB button.
- HD indicator narrowed to 34 px and 2 px high.
- HD ready LED remains at the right edge of the bar.
- When the native provider load reports ready, tiny Space Age `READY ✓` appears beneath the HD progress bar.
- APK19 remains unchanged; this is hosted UI only.
- Viewer revision advanced from Build 0060 to Build 0061.

Module commit: `595348338fcd5a85d4999adf906d864b6e64a548`.
Viewer commit: `5ea02942e26b513421f37aa0a6de181860957f32`.
Pointer commit: `5d436ad94838d5d6c16cd6afe49cbea3f6960896`.


## Hosted instrumentation revision — Build 0062

Date: 2026-10-04.

Reason: Build 0061 inspection confirmed the HD provider status markup was nested inside the 48 px WEB tile, contrary to the intended layout.

Build 0062 changes:
- Moves the HD provider status out of the WEB button into a separate status block below it.
- Keeps breathing space between the WEB tile and the progress bar.
- Keeps the progress bar and small ready LED visible on the UHD/View-HD port.
- Latches progress/ready state in hosted UI so returning from the provider website restores the same full bar, green LED, and `READY ✓`.
- `READY ✓` remains visible until Back to Sky or destination departure.
- Back to Sky explicitly clears the latched provider status.
- APK19 native provider/cache behavior is unchanged.
- Destination-card hairline indicator remains faint and unchanged from Build 0061.

Module commit: `cbcddc1e2f07aa6c3b199b4746200c80ecc8e07f`.
Viewer commit: `6408c778215cf53b16831d49c5c323e3c8c15043`.
Pointer commit: `3cfee8526ab7aaccdf958387564dd47e7e0dc0f6`.


## Hosted instrumentation revision — Build 0063

Date: 2026-10-04.

Observed failure in Build 0062:
- Provider website could already be fully ready while the HD progress bar remained stale.
- Screenshot on NGC 3372 / NOIRLab showed the HD status bar and LED present but not advancing to READY.

Root cause:
- APK19 emits progress into `#gv-provider-native-progress` only while it can find `.gvdp-card.gvdp-visible .gvdp-icon`.
- Build 0062 removed `gvdp-visible` from the destination card when View HD opened.
- Native telemetry therefore removed the progress anchor while the provider WebView continued loading normally.
- Result: preload could succeed, but the HD mirror lost its live progress source.

Build 0063 correction:
- Keep the destination card logically `gvdp-visible` underneath the full-screen HD overlay so APK19 telemetry continues updating.
- No visual duplication occurs because the HD layer remains above it.
- HD progress bar reduced to 26 px.
- Ready LED separated from the bar by a visible gap.
- Tiny `DOWNLOADING` text is shown below the bar while loading.
- `DOWNLOADING` pulses on the same 1.65 s cadence as the WEB chevrons.
- At native ready, loading text is replaced by persistent `READY ✓`.
- Existing ready latch remains active until Back to Sky / destination departure.
- APK19 native code remains unchanged.

Module commit: `8d9f784bf32812e9d8e1a89423778bd40f6d94b3`.
Viewer commit: `752bdcea7c571f68b76350204d788025ccd0e5b3`.
Pointer commit: `7febbb961bd4a8815701e55999c310b60a74d154`.


## Hosted instrumentation revision — Build 0064

Date: 2026-10-04.

Purpose: preserve Build 0063 live APK19 WebView telemetry and refine the View-HD loading choreography.

Verified Build 0063 baseline preserved:
- View HD no longer removes the destination card's native telemetry target.
- APK19 native `onProgressChanged` remains visible to the hosted View-HD status.
- `onPageFinished` latches the ready state.
- Short provider progress bar and separated ready LED remain below the WEB icon.
- `DOWNLOADING` remains visible until ready; `READY ✓` remains latched until Back to Sky / destination departure.

Build 0064 visual sequence:
- Provider name begins the pulse.
- `WEB` follows.
- Three downward vectors pulse in sequence.
- `DOWNLOADING` is the final beat of the 1.65 s cycle.
- Once ready, the loading pulse is replaced by persistent `READY ✓`; no blinking ready state.

APK19 native provider/cache behavior remains unchanged.

Module commit: `de6641e8b0444e2b2115b83683f21380a0a132f4`.
Viewer commit: `a3d6f9964e1a1393b4ca5bd14db869b495ebee82`.
Pointer commit: `7420f6496298dce112af71d78ef845c99453460e`.


## Hosted instrumentation revision — Build 0065

Date: 2026-10-04.

Purpose: make provider status reflect ready-to-view usability rather than waiting only for the final native onPageFinished event.

Changes:
- Replaces `DOWNLOADING` with shorter `LOADING`.
- Reduces status font to 4.4 px Space Age with tighter tracking so it stays inside the View-HD viewport.
- Keeps the live progress bar tied to APK19 WebView `onProgressChanged`.
- Defines ready-to-view as either native finished or native progress >= 90%.
- At ready-to-view, the LED turns green and `READY ✓` latches.
- The bar itself continues to show the actual native progress percentage; it is not forced to 100.
- Existing Build 0064 pulse sequence is preserved, with `LOADING` as the final beat.
- APK19 remains unchanged.

Module commit: `d919817b976f157c4e44af4178c37041693b1c7c`.
Viewer commit: `f09a118f8421de0a1f8c0bb927a0175caa4e36e0`.
Pointer commit: `8b4a1a520cd6d7607b1de054741418d2ff9dc300`.


## Hosted instrumentation revision — Build 0066

Date: 2026-10-04.

Purpose: preserve provider READY state across same-destination website / View-HD / Back-to-Sky cycles.

Root cause in Build 0065:
- View-HD Back to Sky explicitly cleared the hosted provider progress/ready latch.
- The same handler then fell back to APK19 `GVNative.cancelProvider()`, which reset/stopped the native provider preload.
- Reopening View HD therefore defaulted to `LOADING` even when the same provider website had already been loaded and displayed.

Build 0066 changes:
- Back to Sky no longer clears provider progress/ready state for the current destination.
- Back to Sky no longer cancels APK19 provider work.
- Reopening View HD immediately resynchronizes the live native telemetry.
- Returning from the provider website immediately resynchronizes telemetry and preserves the ready latch.
- `READY ✓` remains latched for the current destination.
- Actual navigation to a different astronomical destination remains the destructive boundary: the existing viewer navigation path still cancels old provider work and the destination presentation `depart()` resets hosted status.
- APK19 itself is unchanged.

Module commit: `3a3d0d37d4c1260bf7f9184ac57ec4e5724c0ec4`.
Viewer commit: `91a49759a18f47ac3746891bcb7c5defaa9829ac`.
Pointer commit: `8716726a6f23b3d59f7e383c3d58c4b529e1dbed`.


## APK 0020 — provider-aware multi-origin preconnect

Date: 2026-10-04.

Purpose: reduce cold provider-launch latency by warming the provider page origin and known separate asset/CDN origins at destination landing.

Baseline: APK 0019 persistent provider cache/preload architecture.

APK 0020 changes:
- Keeps APK 0019 hidden provider WebView load, cache behavior, progress telemetry, return-state persistence, Chandra fit-width handling, and same-URL reuse unchanged.
- Always preconnects the active provider URL as before.
- Adds provider-aware secondary-origin preconnects:
  - ESA/Hubble: `https://cdn.esahubble.org/`
  - ESA/Webb: `https://cdn.esawebb.org/`
  - ESO: `https://cdn.eso.org/`
  - NOIRLab: `https://storage.noirlab.edu/`
- Spitzer and Chandra continue to preconnect their active source URL; their current page/image assets use the same provider origin, so no redundant second host is added.
- No hosted Galaxy Viewer build change.
- Browser 0027 remains current and unchanged.

Build identity:
- versionCode: `75`
- versionName: `APK-0020-DEV-0057-WEBKIT1171-MULTIORIGIN`
- WebKit: `1.17.1`
- workflow commit: `be4c3893e51e3e78953c247301fed0cb3591e102`
- workflow run: `37218684964`
- job: `111484387647`
- artifact ID: `11309585985`
- artifact: `Galaxy-Viewer-DEV-0057-WEBKIT1171-0020`
- APK SHA-256: `220315d02a0d2135d4237b451ba6541ccb244a81cdac0aab4d4b62dff4e5ef7f`
- APK signature verification: v3 verified, one signer.


## APK 0020 regression and APK 0021 rollback

Date: 2026-10-04.

Observed regression in APK 0020:
- On arrival, the travel presentation could remain visible instead of handing off cleanly to the destination card.
- The AVM image presentation could appear stalled at the same boundary.

Diagnosis:
- APK 0020 added provider-aware secondary-origin `Profile.preconnect(...)` calls on top of APK 0019.
- The hosted viewer invokes native provider prewarm immediately after destination arrival state is committed.
- AndroidX documents `Profile.preconnect()` as a UI-thread API that performs DNS/TCP/TLS connection setup and keeps connections open for roughly 30 seconds.
- The secondary-origin layer therefore introduced new native networking work at the arrival paint boundary. It is treated as the regression suspect and has been removed entirely.

APK 0021:
- versionCode: `76`
- versionName: `APK-0021-DEV-0057-WEBKIT1171-APK19RUNTIME`
- Restores APK 0019 runtime behavior exactly after the PY19 generation step.
- Retains APK 0019's original single active-provider `profile.preconnect(u)`.
- Removes APK 0020's `preconnectProviderOrigins(...)` helper and all secondary-origin preconnects.
- Hosted Galaxy Viewer remains Build 0066.
- Browser remains 0027 at this rollback point.

Build:
- workflow commit: `1f047faca760f60df725799267c2f1782654f2c2`
- workflow run: `37219382738`
- job: `111486438055`
- artifact ID: `11309496377`
- APK SHA-256: `e4de3c3bcc6381d586be0d1ecbe1e9d2afeccea696ef50a5a9f7889136ff4344`
- APK signature verification: v3 verified.


## Build 0067 / Browser 0028 — restrained Back to Sky + visible browser return acknowledgment

Date: 2026-10-04.

Build 0067 hosted viewer UI:
- Back to Sky is now a restrained enamel navigation control matching Random Galaxy geometry and typography.
- Height: 42 px.
- Border radius: 10 px.
- Font: 15.5 px Space Age.
- Added the same glass/enamel highlight vocabulary used by Random Galaxy.
- Removed all Back-to-Sky spinning star/comet/fireball decorations.
- Reduced button width to 68% and tightened the Galaxy Info panel.
- Preserved the existing brief green press acknowledgment.
- Preserved Build 0066 provider READY persistence and live telemetry behavior.

Build 0067 module commit: `e4df35e6459ad83dc832b9b1c7e36d86b0927aaf`.
Build 0067 viewer commit: `5167ac41a1cb284df1f1dc880417ff80b0801245`.
Build 0067 pointer commit: `e3c62d659cb22e13aa34b8e96d7f72086c52bac9`.

Browser 0028:
- Exact 0027 top shell preserved byte-for-byte.
- Exact 0027 bottom shell preserved except the return timing/paint logic.
- The left Back-to-Galaxy-Viewer tile and arrow still use the existing green flash class.
- Exit now waits for two `requestAnimationFrame` paint opportunities, then holds the green state for 520 ms before `GV.exit()`.
- This prevents the native WebView layer from disappearing before the green acknowledgment is visibly painted.
- Config changes are revision/path substitutions only.
- APK 0021 is unchanged.

Browser 0028 commits:
- top clone: `59c30c96487fdf88fd3093d9ebad992abf51d839`
- bottom timing fix: `deae1a1821c6f53e529cbda78bd35fd866a05cae`
- config: `14896051e1b7a1c8b46b945b147d41c789c4d6eb`
- current pointer: `b241691ed7ff1913910f47abff2d5d4579c7b3d8`


## Browser 0029 — full-tile green navigation acknowledgment

Date: 2026-10-04.

Purpose: make browser navigation feedback visually unambiguous and consistent.

Changes from Browser 0028:
- Back-to-Galaxy-Viewer return control: the entire left tile now turns green, including border, background, glow, and left arrow.
- Browser Back control: the entire left navigation tile and arrow turn green for 520 ms on press.
- Browser Forward control: the entire right navigation tile and arrow turn green for 520 ms on press.
- Return-to-Galaxy-Viewer keeps the Browser 0028 double-requestAnimationFrame paint gate and 520 ms hold before GV.exit().
- No browser navigation semantics changed.
- No Galaxy Viewer hosted code changed.
- No APK change; APK 0021 remains current.

Commits:
- top shell: `4bd20447e2e5916b64e42688489f3c8a992b4277`
- bottom shell: `8438aa69953448d98f2c1ec793c7bf0a6db30784`
- config: `849bb11674cdb117821cb38674da7b5153d2d9bd`
- pointer: `44bc5266088ac3799a7269f62187775fcaf3368e`


## Browser 0030 / Build 0068 — eliminate ghost Back flash and add immediate Random press feedback

Date: 2026-10-04.

Browser 0030 diagnosis and fix:
- Browser 0029 still used inline click handlers for Back/Forward. The tap used to open the browser could yield a synthesized click after the browser shell became visible, causing the Back tile to flash green on load.
- Browser 0030 removes inline click navigation from Back/Forward and requires a fresh pointer-down inside the browser shell for touch/mouse navigation.
- Synthesized touch clicks without a browser-shell pointer-down are ignored.
- Back and Forward still flash their entire tile, border/glow, and arrow green for 520 ms on deliberate presses.
- Back to Galaxy Viewer now flashes both the left arrow tile and the center BACK TO GALAXY VIEWER tile together for 520 ms before exit.
- The Browser 0028/0029 double-requestAnimationFrame paint hold is preserved for return-to-viewer.
- Config changes are revision/path substitutions only.

Browser 0030 commits:
- top shell: `a1c1031bdaa3c9547509fdfb47d1ce85adc33e7b`
- bottom shell: `a1dfae49e8ada1663ab05037fcf8fe7fd87a0dde`
- config: `d70aa426f33aa3e1e28888c74bf9b5e372c8248a`
- pointer: `700c758af7c6eb3885441b49e0e3ce2f979fdb74`

Build 0068:
- Galaxy Navigator adds a dedicated `gvrg-press-green` immediate press state for RANDOM GALAXY.
- RANDOM GALAXY turns green on pointer-down before navigation/preload work begins.
- The immediate acknowledgment is held for 520 ms; existing START/TRAVELING green state remains unchanged.
- Destination presentation remains pinned to Build 0067's simplified Back to Sky module.
- APK 0021 is unchanged.

Build 0068 commits:
- navigator: `2f65a097503c8d613a58c8b77d968e8767463cbd`
- viewer: `2de86b4ee929d79e267950001f12f880a0906e0b`
- pointer: `e0d0d9f3d9f1e3e3a3247353342451997765f875`


## Browser 0031 — unified Back to Galaxy Viewer control

Date: 2026-10-04.

Root cause:
- Browser 0030 still represented Back to Galaxy Viewer as two separate DOM controls: a left arrow tile and a center label tile.
- The UI attempted to synchronize two independent green states, which did not reliably produce a visibly green long return button on-device.

Browser 0031:
- Replaces the split arrow + label controls with one actual long button containing both the arrow and BACK TO GALAXY VIEWER text.
- One element owns the entire return visual state.
- On deliberate pointer-down, the single button is forced green using both class styling and inline `!important` background/border/shadow/color overrides.
- Forces layout, then gives two requestAnimationFrame paint opportunities.
- Holds the visible green state for 560 ms before calling `GV.exit()`.
- The arrow itself also changes to the same green state.
- Browser top shell is byte-for-byte identical to Browser 0030.
- Config differs from Browser 0030 only by revision/path substitutions.
- Galaxy Viewer Build 0068 and APK 0021 are unchanged.

Browser 0031 commits:
- top shell: `969b0dba0f60d9c24a6915f66694b28e5a59e55d`
- bottom shell: `d4d2037e7d417c6897022fe4ac25808d9d482a45`
- config: `2fc53f47b3dc1b1285350ad5d7e1b77d4f024b1a`
- pointer: `501274d9d982f6eafb577dc098e77764b4cd7066`


## Build 0071 — spherical startup + Survey progression controller

Date: 2026-10-04.

Projection:
- Startup projection changed from Mollweide `MOL` to Spherical `SIN`.
- Projection menu is synchronized to SPHERICAL at startup.
- Old second-trip automatic MOL→SIN apex trigger is disabled; current/manual projection is no longer force-switched during travel.

Survey behavior:
- Selecting a provider still automatically launches that provider's first image.
- After arrival, the center navigator becomes a Survey controller.
- It alternates every 1.4 s between `PROVIDER N OF TOTAL` and `PRESS FOR NEXT`.
- During travel the center button shows solid green `TRAVELING`.
- Pressing the center Survey controller advances sequentially to the next record.
- Back/Forward continue to move through the same provider sequence.
- Random Galaxy stars/comets are hidden while Survey mode is active.
- At the final record the prompt stops and the center control is disabled.
- Exiting Survey mode restores the normal Random Galaxy presentation.

Artifacts:
- Navigator 002 commit: `9b2b42806509c723e2eb294acddee118ac50e535`
- Viewer commits: `97ae312584e1cc34521f1092056ddfe3d1a67d6f`, `e0c758ef6eedf897378af515014066def369a976`, `de2663f97cd746baa6965a1fecf7eeca2c3487e3`
- Viewer pointer commit: `cde4e9dc2899d3e67d1f4d3c5be11c4d718aa227`
- Browser remains 0031.


## Build 0072 — restore delayed projection transition

Date: 2026-10-04.

Correction:
- Reverted Build 0071's unauthorized startup projection change.
- Launch is again Mollweide / MOL.
- First HOME → galaxy trip remains Mollweide.
- On the next outbound trip, at the 60° apex, projection switches Mollweide → Spherical / SIN.
- After that, projection remains current unless the user changes it manually.
- Survey auto-first-image behavior and Navigator 002 counter/prompt remain unchanged.
- Browser remains 0031; APK remains 0022.

Commits:
- viewer: `20f86c3a28c216e2f6380a1e1d59958d2b9853b0`
- pointer: `c0dc1d16f2cf28447711e7bae43a8b297fa5ff97`
