/*
RANDOM GALAXY 0230
FORWARD-ONLY TRUE CAMERA AUTHORITY FIX
CAMERA = CATALOG / AVM CRVAL RA-DEC ONLY.
DERIVED IMAGE CENTER = AUDIT ONLY.
*/
/*
RANDOM GALAXY 0229 — FORWARD-ONLY WCS IMAGE-CENTER CAMERA AUTHORITY REPAIR
BASELINE SOURCE: RANDOM GALAXY 0227
AUTHORIZED CHANGE:
- Use derived WCS geometric image center for precomputed AVM camera RA/Dec when available.
- Keep CRVAL/CRPIX/WCS metadata intact.
- No catalog, navigation, AVM, vignette, queue, or UI redesign.
*/
/*
RANDOM GALAXY 0218 — PRECOMPUTED FRAMING READY DEADLOCK FIX
BASELINE: RANDOM GALAXY 0217
- Fixes startup PREPARING IMAGE deadlock after FUTURE[0] decode.
- Precomputed AVM/WCS authority itself satisfies the framing-ready contract.
- Removes circular dependency where Random required framing READY before click,
  but framing READY was only requested after click.
- No vignette, download, navigation choreography, catalog, or HD UI changes.
*/
/*
RANDOM GALAXY 0217 — NONBLOCKING VIGNETTE + COMPRESSED CACHE WARM
BASELINE: RANDOM GALAXY 0216
- Restores compressed-byte cache warming for precomputed AVM records without decoding FUTURE[1..9].
- AVM vignette preparation is hidden/background preparation and no longer a Random-button or flight gate.
- Preserves githubImageUrl through the travel handoff so AVM can prefer a canvas-safe mirror.
- Fixes sub-million travel distance scaling to THOUSAND LIGHT-YEARS instead of six-digit raw LIGHT-YEARS.
*/
/*
RANDOM GALAXY 0216 — AVM REFERENCE/SCREEN RASTER NORMALIZATION
BASELINE: RANDOM GALAXY 0215
- Fixes FUTURE[0] retry loop caused by comparing AVM ReferenceDimension with provider screen-JPEG dimensions.
- AVM ReferenceDimension remains metadata-space authority; it is not treated as the downloaded screen raster size.
- On the one allowed FUTURE[0] pixel decode, rescale precomputed WCS to the actual decoded JPEG dimensions.
- Preserve strict JPEG header/decode mismatch checking for normal fetched-Blob preparation.
- No navigation choreography, queue depth, AVM 0048, catalogs, HD UI, or distance presentation changes.
*/
/*
RANDOM GALAXY 0215 — PRECOMPUTED AUTHORITY CONTRACT REPAIR
BASELINE: RANDOM GALAXY 0214
- Accepts PRECOMPUTED_IMAGE_AVM and PRECOMPUTED_CATALOG_FALLBACK at the AR129-B handoff/history contracts.
- Makes AVM horizontal FoV / FOV X the navigation/display FoV while preserving FOV Y independently.
- Uses precomputed AVM reference dimensions to prepare 1,814 image-AVM records without background cross-origin JPEG fetch.
- FUTURE[0] still performs the only pixel decode, using the exact AVM catalog image URL.
- Rejects the current document / HTML documents as HD image sources.
- Extends Random request cleanup across the complete claimed-destination pre-travel path.
*/
/*
RANDOM GALAXY 0214 — PRECOMPUTED AVM AUTHORITY
BASELINE: RANDOM GALAXY 0213
- Loads the 1,871-record gv-avm-runtime-catalog-0001 supplied by the viewer.
- FOV X is authoritative; FOV Y remains preserved for image geometry.
- Future JPEGs stay compressed while AVM/WCS comes from the JSON catalog.
- Runtime XMP/AVM parsing is bypassed in the preparation path.
- Background preparation no longer falls back to a decoded HTMLImageElement.
- FUTURE[0] pixel decode remains just-in-time because visible display still needs pixels.
- AVM 0048, distance presentation, catalogs, navigation choreography, and HD UI are otherwise unchanged.
*/
/*
RANDOM GALAXY 0213 — AK SCOPE REPAIR
- Fixes the metadata-state propagation crash in outer hdStateFor().
- 0212 called preparation-engine-private acceptedAvmAuthority() from
  the navigation runtime scope where that function does not exist.
- Adds an equivalent local authority predicate in the navigation scope.
- Metadata-first / FUTURE[0]-only pixel decode architecture is unchanged.
*/
/*
RANDOM GALAXY 0212 — METADATA-FIRST / JUST-IN-TIME PIXEL DECODE
BASELINE: RANDOM GALAXY 0211
- Future queue keeps compressed JPEG + AVM/WCS metadata.
- Background future records never create decoded pixel surfaces.
- FUTURE[0] alone is pixel-decoded just in time for visible staging/travel.
- JPEG dimensions come from the SOF header, without IDCT/RGB/RGBA decode.
- Catalog-WCS fallback remains for incomplete embedded AVM.
- AVM 0048 unchanged. No sidecar database.
*/
/*
RANDOM GALAXY 0211 — CORRECTED DIRECT AVM FAST PATH
BASELINE: RANDOM GALAXY 0209

- Uses the JPEG Blob only transiently while the download worker owns it.
- Does NOT retain the Blob on prepared queue items.
- Reads XMP/AVM directly from the already-downloaded JPEG.
- Normalizes AVM WCS from reference dimensions to actual decoded JPEG dimensions.
- Direct AVM successes bypass the serialized hidden-Aladin metadata lane.
- Existing hidden Aladin extraction remains the compatibility fallback.
- AVM 0048 visible blending is unchanged.
- No AVM sidecar database is used.
*/
/*
RANDOM GALAXY 0208 — AVM DOWNLOAD/TRAVEL BOTTLENECK FIX
- Reuses the already-downloaded JPEG blob for runtime AVM/WCS authority.
- Preserves FUTURE[0] priority into the serialized AVM lane.
- Requires FUTURE[0]'s visible AVM stage to finish before travel begins.
- Removes click-time fire-and-forget AVM work during flyViewport().
*/
/*
RANDOM GALAXY 0202 — LONG-SESSION MEMORY + TRAVEL HUD STABILITY
- Caps execution tracing to bound long-session JavaScript memory.
- Reduces retained decoded history images while preserving the 10-slot future queue.
- Travel HUD distance now follows Navigation 0020's actual distance callback.
- Accepted Random state text is TRAVELING.
- Navigation choreography, AVM registration, queue ordering, and provider behavior are unchanged.

RANDOM GALAXY 0201 — TRAVEL PROVIDER ICON SIZE MATCH
- Travel/course provider tile increased from 36x36 px to exactly 48x48 px.
- Matches the VIEW HD provider tile size.
- Right text clearance increased from 58 px to 70 px (+12 px), preserving spacing mathematically.
- No navigation, readiness, AVM, HD, or travel behavior changes.

RANDOM GALAXY 0200 — VISIBLE-READY AUTHORITATIVE
- The visible HD/AVM readiness state is authoritative for RANDOM GALAXY enablement.
- Hidden Aladin/WCS staging remains a background optimization and never blocks the button.
- Click-time AVM work is fire-and-forget so navigation starts immediately.
- First accepted tap still gives immediate PREPARING TRIP + comet feedback.
- FIFO ownership, Monte Carlo ordering, HD preparation, and travel choreography are unchanged.

GALAXY VIEWER ENGINEERING CHANGE ORDER — RANDOM GALAXY 0053
AUTHORIZED BASELINE: gv-random-galaxy-0124.js blob a4a9ddb3c28751dfbbf9fcdf04278c80e1020013.
AUTHORIZED CHANGES: readable compact arrival presentation, five-field HD science banner, exact retained decoded-image handoff for immediate HD display, and generic provider identity. Touch-through interaction, 36px provider controls, top-centered HD viewing, no post-arrival reframing, and configured travel behavior are preserved.
*/
/*
RANDOM GALAXY 0219 — CORS-SAFE CATALOG-FALLBACK PREPARATION
BASELINE: RANDOM GALAXY 0218
- PRECOMPUTED_CATALOG_FALLBACK records no longer enter the CORS-readable Blob fetch/retry loop.
- Their compressed JPEG is warmed with the existing no-cors cache path and retained as metadata-only.
- FUTURE[0] alone performs the direct image decode, then builds the sidecar catalog-fallback WCS from the real raster dimensions.
- Eliminates the yellow/red 5-second retry flicker caused by provider CORS rejection.
- No navigation choreography, queue depth, vignette, catalogs, HD UI, or distance presentation changes.
*/
/*
RANDOM GALAXY 0220 — PREPARATION AUTHORITY SCOPE REPAIR
BASELINE: RANDOM GALAXY 0219
- Fixes three preparation-engine call sites that incorrectly referenced the navigation-scope gv0213AcceptedAvmAuthority().
- Uses the preparation-engine-local acceptedAvmAuthority() predicate at FUTURE[0] decode/readiness gates.
- Preserves 0219 CORS-safe catalog-fallback handling, FUTURE[1..9] metadata-only behavior, queue depth, navigation, AVM, vignette, catalogs, and distance presentation.
*/
/*
RANDOM GALAXY 0221 — FUTURE0 RETRY OWNERSHIP REPAIR
BASELINE: RANDOM GALAXY 0220
- Removes a failed FUTURE[0] prepared item from prefetchReady before retry so duplicate suppression cannot block fresh work.
- Activates the existing poisoned-head ejection after the bounded retry limit and promotes the next FIFO destination.
- Extends bounded head-healing to the normal post-startup monitor path.
- Adds execution trace markers around decode start, failed-resource eviction, retry request, poisoned-head ejection, and next-head promotion.
- No JPEG decoder, Aladin, vignette, navigation choreography, catalogs, queue depth, or HD UI changes.
*/
/*
RANDOM GALAXY 0222 — AVM AUTO-STAGE RETRY STORM GUARD
BASELINE: RANDOM GALAXY 0221
- After one automatic FUTURE[0] AVM stage failure, suppresses repeated automatic restaging of that same FIFO head.
- Clears the suppression when the FIFO head changes or a stage succeeds.
- Uses a macrotask yield after AVM stage completion instead of immediate recursive readiness re-entry.
- Navigation remains nonblocking when vignette preparation fails.
- No JPEG decode, HD queue, navigation choreography, catalog, vignette math, or HD UI changes.
*/
/*
RANDOM GALAXY 0223 — WCS IMAGE-CENTER + HORIZONTAL-FOV AUTHORITY
BASELINE: RANDOM GALAXY 0222
- Derives the true sky coordinate of the JPEG geometric center from normalized WCS.
- CRVAL/CRPIX remain WCS reference metadata; CRVAL is not assumed to be image center.
- fovDegrees is horizontal WCS FoV in every AVM preparation path.
- Adds WCS/camera geometry tracing.
- No catalog edits, zoom multiplier, curated-FoV changes, Navigation changes, or AVM changes.
*/
(function (global) {
  'use strict';

  const VERSION='0232';

  // 0067 instrumentation only — no Random navigation behavior change.
  const gvInitialTraceEnabled=
    global.GalaxyViewerDiagnostics?.getState?.().enabled!==false;
  const GV_TRACE=global.__GV_RANDOM_EXEC_TRACE__={
    version:'0067',
    source:'gv-random-galaxy-0124.js',
    enabled:gvInitialTraceEnabled,
    startedAt:gvInitialTraceEnabled?performance.now():0,
    seq:0,
    events:[],
    last:null
  };

  function setExecutionTracingEnabled(next){
    const enabled=Boolean(next);
    if(enabled&&!GV_TRACE.startedAt)
      GV_TRACE.startedAt=performance.now();
    GV_TRACE.enabled=enabled;
    return enabled;
  }

  function gvTrace(line,step,detail=null){
    if(!GV_TRACE.enabled)return null;
    try{
      const entry={
        seq:++GV_TRACE.seq,
        elapsedMs:Math.round((performance.now()-GV_TRACE.startedAt)*1000)/1000,
        sourceLine0066:Number(line),
        step:String(step),
        detail
      };
      GV_TRACE.events.push(entry);
      if(GV_TRACE.events.length>2000)
        GV_TRACE.events.splice(0,GV_TRACE.events.length-2000);
      GV_TRACE.last=entry;
      return entry;
    }catch(_){return null}
  }

  function gvTraceError(line,step,error){
    return GV_TRACE.enabled&&gvTrace(line,step,{
      name:String(error?.name||'Error'),
      message:String(error?.message||error||'UNKNOWN'),
      stack:String(error?.stack||'')
    });
  }
  const ARCHIVE_PRELOAD_TARGET=3;

  const FONT_URLS = Object.freeze({
    spaceAge: 'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf',
    digits: 'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/GV-Coordinate-Digits-0005.otf'
  });

  const FONT_NAMES = Object.freeze({
    spaceAge: 'GV Random Galaxy Space Age 0053',
    digits: 'GV Random Galaxy Digits 0053'
  });

  const DEFAULTS = Object.freeze({
    geminiEndpoint: null,
    travelSeconds: 15,
    firstHomeTravelSeconds: 9,
    firstHomeTranslationSeconds: 4,
    maxFov: 120,
    translateStart: 11/30,
    turnPoint: 0.50,
    translate90: 19/30,
    translationComplete: 11/15,
    aitEntryFov: 95,
    sinReturnFov: 24,
    arrivalProjection: 'MOL',
    wideProjection: 'AIT',
    integerSlots: 6,
    fractionSlots: 2,
    prefetch: true,
    requestEvent: 'gv-random-galaxy-request',
    bindClick: false,
    hdMinScale: 1,
    hdMaxScale: 8,
    hdScaleSettleMs: 200
  });

  async function requestPortraitOrientation(reason = 'random-galaxy') {
    try {
      const orientation = globalThis.screen && globalThis.screen.orientation;
      if (!orientation || typeof orientation.lock !== 'function') return false;
      await orientation.lock('portrait');
      return true;
    } catch (error) {
      console.debug('GALAXY RANDOM PORTRAIT REQUEST SKIPPED', reason, error);
      return false;
    }
  }

  const reinforcePortraitOrientation = () => {
    requestPortraitOrientation('lifecycle').catch(() => {});
  };

  requestPortraitOrientation('module-load').catch(() => {});
  globalThis.addEventListener?.('pageshow', reinforcePortraitOrientation, { passive: true });
  globalThis.addEventListener?.('focus', reinforcePortraitOrientation, { passive: true });
  globalThis.addEventListener?.('orientationchange', reinforcePortraitOrientation, { passive: true });
  globalThis.document?.addEventListener?.('visibilitychange', () => {
    if (!globalThis.document.hidden)
      requestPortraitOrientation('visibility-return').catch(() => {});
  }, { passive: true });

  const instances = new WeakMap();
  let fontsPromise = null;

  function clamp(value, min, max) { return Math.max(min, Math.min(max, Number(value))); }
  function clamp01(value) { return clamp(value, 0, 1); }
  function smootherstep(value) {
    const t = clamp01(value);
    return t * t * t * (t * (t * 6 - 15) + 10);
  }
  function navigationSmootherstep(value) {
    const t = clamp01(value);
    return 35*t*t*t*t - 84*t*t*t*t*t + 70*t*t*t*t*t*t - 20*t*t*t*t*t*t*t;
  }
  function cleanText(value) { return String(value == null ? '' : value).replace(/\s+/g, ' ').trim(); }

  // 0196 — travel HUD provider resolver promoted to module scope.
  // Exact logic retained from the existing 0195 HD provider resolver.
  function providerIdentityFor(destination){
      const provider=String(destination?.provider||"").trim();
      const telescope=String(destination?.telescope||"").trim();
      const evidence=[
          provider,telescope,destination?.source,destination?.hdUrl,destination?.sourceUrl
      ].map(value=>String(value||"").trim().toLowerCase()).filter(Boolean).join(" ");

      if(/(?:^|[^a-z0-9])(?:noirlab|noir lab|noirlabs|noir labs|noao|gemini)(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"noirlab",label:"NOIRLAB"});
      if(/(?:^|[^a-z0-9])(?:eso|european southern observatory)(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"eso",label:"ESO"});
      if(/(?:^|[^a-z0-9])(?:hubble|hst|esahubble)(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"hubble",label:"HUBBLE"});
      if(/(?:^|[^a-z0-9])(?:jwst|james webb|webb|esawebb)(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"jwst",label:"JWST"});
      if(/(?:^|[^a-z0-9])spitzer(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"spitzer",label:"SPITZER"});
      if(/(?:^|[^a-z0-9])chandra(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"chandra",label:"CHANDRA"});
      if(/(?:^|[^a-z0-9])euclid(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"euclid",label:"EUCLID"});
      if(/(?:^|[^a-z0-9])galex(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"galex",label:"GALEX"});
      if(/(?:^|[^a-z0-9])herschel(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"herschel",label:"HERSCHEL"});
      if(/(?:^|[^a-z0-9])nrao(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"nrao",label:"NRAO"});
      if(/(?:^|[^a-z0-9])nustar(?:[^a-z0-9]|$)/i.test(evidence)) return Object.freeze({slug:"nustar",label:"NUSTAR"});

      const label=String(provider||telescope||"").trim().toUpperCase();
      const slug=String(provider||telescope||"").trim().toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"");
      return Object.freeze({slug,label});
  }

  const PROVIDER_ICON_URLS=Object.freeze({
      chandra:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Chandra/Chandra.jpg",
      eso:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/ESO/ESO.jpg",
      euclid:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Euclid/Euclid.jpg",
      galex:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/GALEX/GALEX.jpg",
      herschel:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Herschel/Herschel.jpg",
      hubble:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble.jpg",
      jwst:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/JWST/JWST.jpg",
      nrao:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NRAO/NRAO.jpg",
      noirlab:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NoirLabs/NOIRLab.jpg",
      nustar:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/NuSTAR/NuSTAR.jpg",
      spitzer:"https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Spitzer/Spitzer.jpg"
  });

  function providerIconUrl(destination){
      const {slug}=providerIdentityFor(destination);
      if(PROVIDER_ICON_URLS[slug])return PROVIDER_ICON_URLS[slug];

      const explicit=String(destination?.providerIconUrl||destination?.provider_icon_url||"").trim();
      return /^https:\/\//i.test(explicit)?explicit:"";
  }
  function finiteNumber(value) {
    if(value===null||value===undefined||value==='')return null;
    const n=Number(value);
    return Number.isFinite(n)?n:null;
  }

  function normalizeFullRotationDelta(value){
    let angle=Number(value)||0;
    while(angle>180)angle-=360;
    while(angle<=-180)angle+=360;
    return angle;
  }

  function validHttpsUrl(value) {
    try {
      const url = new URL(String(value));
      if (url.protocol !== 'https:') return null;

      const host = String(url.hostname || '').toLowerCase();
      const path = String(url.pathname || '').toLowerCase();

      if (
        host === 'gear66me-ui.github.io' &&
        path.endsWith('/generic-app.html')
      ) return null;

      return url;
    } catch (_) { return null; }
  }
  function rejectNonObservationLabel(value) {
    return /\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/i.test(cleanText(value));
  }

  function toVector(ra, dec) {
    const r = Number(ra) * Math.PI / 180;
    const d = Number(dec) * Math.PI / 180;
    return [Math.cos(d) * Math.cos(r), Math.cos(d) * Math.sin(r), Math.sin(d)];
  }
  function vectorToRaDec(vector) {
    const [x, y, z] = vector;
    return [
      (Math.atan2(y, x) * 180 / Math.PI + 360) % 360,
      Math.atan2(z, Math.sqrt(x * x + y * y)) * 180 / Math.PI
    ];
  }
  function angularSeparationRadians(a, b) {
    const va = toVector(a.ra, a.dec);
    const vb = toVector(b.ra, b.dec);
    return Math.acos(clamp(va[0] * vb[0] + va[1] * vb[1] + va[2] * vb[2], -1, 1));
  }
  function routeDistanceMillionLy(source,destination,options={}) {
    const dA=finiteNumber(source&&source.distance);
    const dB=finiteNumber(destination&&destination.distance);

    if(options.homeDeparture===true){
      return dB>0
        ? {value:dB,exactRoute:true,unavailable:false,estimated:false,homeRoute:true}
        : {value:0,exactRoute:false,unavailable:true,estimated:false,homeRoute:true};
    }

    if(dA>0&&dB>0){
      const theta=angularSeparationRadians(source,destination);
      return {
        value:Math.sqrt(Math.max(0,dA*dA+dB*dB-2*dA*dB*Math.cos(theta))),
        exactRoute:true,
        unavailable:false,
        estimated:false
      };
    }

    const fallback=dB>0?dB:(dA>0?dA:0);
    return fallback>0
      ? {value:fallback,exactRoute:false,unavailable:false,estimated:true}
      : {value:0,exactRoute:false,unavailable:true,estimated:false};
  }
  function scaledDistance(millionLy) {
    let value = finiteNumber(millionLy);
    value = value == null || value < 0 ? 0 : value;
    if (value < 1) return { value: value * 1_000, unit: 'THOUSAND LIGHT-YEARS' };
    if (value < 1000) return { value, unit: 'MILLION LIGHT-YEARS' };
    return { value: value / 1000, unit: 'BILLION LIGHT-YEARS' };
  }

  function formatWholeAstronomyScale(lightYears, noun = 'LIGHT-YEARS') {
    const value = finiteNumber(lightYears);
    if (value == null || value < 0) return '';
    if (value < 1_000_000) return `${Math.round(value).toLocaleString('en-US')} ${noun}`;
    if (value < 1_000_000_000) return `${Math.round(value / 1_000_000).toLocaleString('en-US')} MILLION ${noun}`;
    return `${Math.round(value / 1_000_000_000).toLocaleString('en-US')} BILLION ${noun}`;
  }
  function formatCompactHdScale(lightYears) {
    const value = finiteNumber(lightYears);
    if (value == null || value <= 0) return '';
    if (value >= 1_000_000_000) return `${value / 1_000_000_000}G LY`;
    if (value >= 1_000_000) return `${value / 1_000_000}M LY`;
    if (value >= 1_000) return `${value / 1_000}K LY`;
    return `${value} LY`;
  }
  function formatDistanceMly(millionLy) {
    const value = finiteNumber(millionLy);
    return value == null || value <= 0 ? '' : formatWholeAstronomyScale(value * 1_000_000);
  }
  function formatAgeYears(years) {
    const value = finiteNumber(years);
    if (value == null || value <= 0) return '';
    if (value < 1_000_000) return `${Math.round(value).toLocaleString('en-US')} YEARS`;
    if (value < 1_000_000_000) return `${Math.round(value / 1_000_000).toLocaleString('en-US')} MILLION YEARS`;
    return `${Math.round(value / 1_000_000_000).toLocaleString('en-US')} BILLION YEARS`;
  }
  function formatImageSpanValue(lightYears) {
  const value = finiteNumber(lightYears);
  if (value == null || value <= 0) return '';
  if (value < 1_000) return `${Math.round(value)}`;
  const scale = value >= 1_000_000_000 ? 1_000_000_000 : value >= 1_000_000 ? 1_000_000 : 1_000;
  const suffix = scale === 1_000_000_000 ? 'B' : scale === 1_000_000 ? 'M' : 'K';
  const q = value / scale;
  const rounded = q >= 10 ? Math.round(q) : Math.round(q * 10) / 10;
  return `${Number(rounded.toFixed(1))}${suffix}`;
}
function formatPhysicalSize(size) {
  if (!size) return '';
  if (Array.isArray(size) && size.length >= 2) {
    const a = finiteNumber(size[0]), b = finiteNumber(size[1]);
    if (a == null || b == null || a <= 0 || b <= 0) return '';
    return `${formatImageSpanValue(a)} × ${formatImageSpanValue(b)} LIGHT-YEARS`;
  }
  const value = finiteNumber(size);
  return value == null || value <= 0 ? '' : `${formatImageSpanValue(value)} LIGHT-YEARS`;
}

  async function ensureFonts() {
    if (fontsPromise) return fontsPromise;
    fontsPromise = (async () => {
      const faces = [
        new FontFace(FONT_NAMES.spaceAge, `url("${FONT_URLS.spaceAge}")`, { style: 'normal', weight: '400' }),
        new FontFace(FONT_NAMES.digits, `url("${FONT_URLS.digits}")`, { style: 'normal', weight: '400' })
      ];
      const loaded = await Promise.all(faces.map((face) => face.load()));
      loaded.forEach((face) => document.fonts.add(face));
      await Promise.all([
        document.fonts.load(`400 12px "${FONT_NAMES.spaceAge}"`, 'DISTANCE TO EARTH CONSTELLATION GALAXY AGE VIEW HD IMAGE'),
        document.fonts.load(`400 18px "${FONT_NAMES.digits}"`, '0123456789.')
      ]);
      await document.fonts.ready;
      return true;
    })();
    return fontsPromise;
  }

function installRandomWaitComet(button) {
  if (!(button instanceof Element)) return;
  if (!document.getElementById('gvrg-random-wait-comet-0031-style')) {
    const style=document.createElement('style'); style.id='gvrg-random-wait-comet-0031-style';
    style.textContent=`#gv-random-galaxy .gvrg-random-layout{display:grid;grid-template-columns:20px auto 20px;align-items:center;justify-content:center;column-gap:13px}#gv-random-galaxy .gvrg-random-label{display:block;grid-column:2;text-align:center}#gv-random-galaxy .gvrg-random-star-wrap{position:relative;display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;margin:0;flex:0 0 20px;line-height:20px;transform:none}#gv-random-galaxy .gvrg-random-star-wrap-left{grid-column:1}#gv-random-galaxy .gvrg-random-star-wrap-right{grid-column:3;transform:translateX(-2px)}#gv-random-galaxy .gvrg-random-star{display:block;font:16px/20px system-ui,sans-serif;transform:translateY(-.5px)}#gv-random-galaxy .gvrg-random-comet{position:absolute;left:50%;top:50%;width:0;height:0;opacity:0;pointer-events:none;z-index:2;animation:gvrg-random-comet-orbit-0031 2.8s linear infinite;animation-play-state:paused}#gv-random-galaxy .gvrg-random-comet i{position:absolute;left:-1.5px;top:-1.5px;width:3px;height:3px;border-radius:50%;background:#FF8420;transform:rotate(var(--a)) translateY(-8px) scale(var(--s));opacity:var(--o);box-shadow:0 0 3px rgba(255,132,32,.85)}#gv-random-galaxy .gvrg-random-comet i:nth-child(1){--a:0deg;--s:1;--o:1;background:#FF4414;box-shadow:0 0 2px 1px #FF4414,0 0 5px 1px #FF8420}#gv-random-galaxy .gvrg-random-comet i:nth-child(2){--a:-15deg;--s:.88;--o:.84}#gv-random-galaxy .gvrg-random-comet i:nth-child(3){--a:-30deg;--s:.76;--o:.68}#gv-random-galaxy .gvrg-random-comet i:nth-child(4){--a:-45deg;--s:.64;--o:.52}#gv-random-galaxy .gvrg-random-comet i:nth-child(5){--a:-60deg;--s:.52;--o:.38}#gv-random-galaxy .gvrg-random-comet i:nth-child(6){--a:-75deg;--s:.42;--o:.26}#gv-random-galaxy .gvrg-random-comet i:nth-child(7){--a:-90deg;--s:.32;--o:.16}#gv-random-galaxy .gvrg-random-comet i:nth-child(8){--a:-105deg;--s:.24;--o:.08}#gv-random-galaxy.gvrg-random-busy .gvrg-random-comet{opacity:1;animation-play-state:running}#gv-random-galaxy .gvrg-random-comet-left{animation-delay:-1.4s}.gvrg-fov-sub{font-size:.72em;letter-spacing:.25px;white-space:nowrap}@keyframes gvrg-random-comet-orbit-0031{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}`;
    document.head.appendChild(style);
  }
  const layoutReady=button.querySelector('.gvrg-random-layout .gvrg-random-star-wrap-left')&&button.querySelector('.gvrg-random-layout .gvrg-random-label')&&button.querySelector('.gvrg-random-layout .gvrg-random-star-wrap-right');
  if (!layoutReady) {
    button.innerHTML='<span class="gvrg-random-layout"><span class="gvrg-random-star-wrap gvrg-random-star-wrap-left" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet gvrg-random-comet-left"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span><span class="gvrg-random-label">RANDOM GALAXY</span><span class="gvrg-random-star-wrap gvrg-random-star-wrap-right" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span></span>';
    button.setAttribute('aria-label','RANDOM GALAXY');
  }
}
function setRandomWaitComet(button,active){if(!(button instanceof Element))return;installRandomWaitComet(button);button.classList.toggle('gvrg-random-busy',Boolean(active));}

function fitRandomButtonLabel(button,label){
  if(!(button instanceof Element)||!(label instanceof Element))return null;
  const text=String(label.textContent||'');
  const buttonStyle=getComputedStyle(button);
  const labelStyle=getComputedStyle(label);
  const storedMax=Number(button.dataset.gvrgLabelMaxFontPx);
  const maxFontPx=Number.isFinite(storedMax)&&storedMax>0?storedMax:(parseFloat(buttonStyle.fontSize)||15.5);
  if(!(Number.isFinite(storedMax)&&storedMax>0))button.dataset.gvrgLabelMaxFontPx=String(maxFontPx);
  const canvas=fitRandomButtonLabel._canvas||(fitRandomButtonLabel._canvas=document.createElement('canvas'));
  const ctx=canvas.getContext('2d');
  if(!ctx)return null;
  ctx.font=`${labelStyle.fontStyle} ${labelStyle.fontWeight} ${maxFontPx}px ${labelStyle.fontFamily}`;
  const letterSpacing=parseFloat(labelStyle.letterSpacing)||0;
  const measured=ctx.measureText(text).width+Math.max(0,text.length-1)*letterSpacing;
  const horizontalPadding=(parseFloat(buttonStyle.paddingLeft)||0)+(parseFloat(buttonStyle.paddingRight)||0);
  const fixedLayoutWidth=20+20+13+13;
  const available=Math.max(1,button.clientWidth-horizontalPadding-fixedLayoutWidth);
  const fittedPx=measured>available?maxFontPx*(available/measured):maxFontPx;
  label.style.fontSize=`${Math.max(1,fittedPx).toFixed(2)}px`;
  return Object.freeze({text,availablePx:available,measuredAtMaxPx:measured,maxFontPx,fittedPx});
}

function setRandomButtonText(button,text,{busy=false,ready=false,imageWait=false}={}){
  if(!(button instanceof Element))return;
  installRandomWaitComet(button);
  const label=button.querySelector('.gvrg-random-label');
  const resolvedText=String(text||'RANDOM GALAXY');
  button.classList.toggle('gvrg-random-busy',Boolean(busy));
  button.classList.toggle('gvrg-random-ready',Boolean(ready));
  button.classList.toggle('gvrg-random-image-wait',Boolean(imageWait));
  if(label){
    label.textContent=resolvedText;
    fitRandomButtonLabel(button,label);
    requestAnimationFrame(()=>fitRandomButtonLabel(button,label));
  }
  button.setAttribute('aria-label',resolvedText);
  if(!document.getElementById('gvrg-random-ready-0148-style')){
    const style=document.createElement('style');
    style.id='gvrg-random-ready-0148-style';
    style.textContent=
      '#gv-random-galaxy.gvrg-random-ready{border-color:#78FFAB!important;color:#78FFAB!important;box-shadow:0 0 10px rgba(120,255,171,.72),inset 0 0 10px rgba(120,255,171,.12)!important}' +
      '#gv-random-galaxy.gvrg-random-ready .gvrg-random-star{filter:drop-shadow(0 0 5px rgba(120,255,171,.95))}';
    document.head.appendChild(style);
  }
  if(!document.getElementById('gvrg-random-image-wait-0157-style')){
    const style=document.createElement('style');
    style.id='gvrg-random-image-wait-0157-style';
    style.textContent=
      '#gv-random-galaxy.gvrg-random-image-wait{background:linear-gradient(145deg,#030B18 0%,#071B36 42%,#0A2E59 72%,#0D447B 100%)!important;border-color:#3E83C6!important;color:#FF6426!important;text-shadow:0 0 3px rgba(255,68,20,.95),0 0 8px rgba(255,132,32,.72)!important;box-shadow:inset 0 0 10px rgba(26,104,180,.28),0 0 8px rgba(9,48,92,.55)!important;filter:none!important}' +
      '#gv-random-galaxy.gvrg-random-image-wait .gvrg-random-star{filter:drop-shadow(0 0 4px rgba(255,157,45,.70))}';
    document.head.appendChild(style);
  }
}

  class FixedDistanceRenderer {
    constructor(host, options = {}) {
      this.host = host;
      this.integerSlots = Number(options.integerSlots || DEFAULTS.integerSlots);
      this.fractionSlots = Number(options.fractionSlots || DEFAULTS.fractionSlots);
      this.integerCells = [];
      this.fractionCells = [];
      this.root = this.#build();
      this.host.replaceChildren(this.root);
    }
    #build() {
      const root = document.createElement('span');
      root.className = 'gvrg-distance-number';
      const number = document.createElement('span');
      number.className = 'gvrg-number-cells';
      for (let i = 0; i < this.integerSlots; i += 1) {
        const cell = document.createElement('span');
        cell.className = 'gvrg-digit-cell';
        cell.textContent = '0';
        number.appendChild(cell);
        this.integerCells.push(cell);
      }
      const decimal = document.createElement('span');
      decimal.className = 'gvrg-decimal-cell';
      decimal.textContent = '.';
      this.decimalCell = decimal;
      number.appendChild(decimal);
      for (let i = 0; i < this.fractionSlots; i += 1) {
        const cell = document.createElement('span');
        cell.className = 'gvrg-digit-cell';
        cell.textContent = '0';
        number.appendChild(cell);
        this.fractionCells.push(cell);
      }
      const unit = document.createElement('span');
      unit.className = 'gvrg-distance-unit';
      unit.textContent = 'MILLION LIGHT-YEARS';
      this.unitEl = unit;
      root.append(number, unit);
      return root;
    }
    async calibrate() {
      await ensureFonts();
      [...this.integerCells, ...this.fractionCells].forEach((cell) => { cell.style.width = '13px'; });
      this.decimalCell.style.width = '8px';
      this.render(0);
    }
    renderUnavailable() {
      this.integerCells.forEach((cell,index)=>{
        cell.textContent=index===this.integerCells.length-1?'—':'0';
        cell.style.visibility=index===this.integerCells.length-1?'visible':'hidden';
      });
      this.decimalCell.style.visibility='hidden';
      this.fractionCells.forEach(cell=>{cell.textContent='0';cell.style.visibility='hidden'});
      this.unitEl.textContent='';
      this.root.setAttribute('aria-label','—');
    }
    render(millionLy) {
      this.decimalCell.style.visibility='visible';
      this.fractionCells.forEach(cell=>{cell.style.visibility='visible'});
      const scaled = scaledDistance(millionLy);
      const safe = clamp(scaled.value, 0, 999999.99);
      const [integerPart, fractionPart = ''] = safe.toFixed(this.fractionSlots).split('.');
      const integer = integerPart.padStart(this.integerSlots, ' ').slice(-this.integerSlots);
      const fraction = fractionPart.padEnd(this.fractionSlots, '0').slice(0, this.fractionSlots);
      this.integerCells.forEach((cell, index) => {
        const character = integer[index];
        cell.textContent = character === ' ' ? '0' : character;
        cell.style.visibility = character === ' ' ? 'hidden' : 'visible';
      });
      this.fractionCells.forEach((cell, index) => { cell.textContent = fraction[index]; });
      this.unitEl.textContent = scaled.unit;
      this.root.setAttribute('aria-label', `${safe.toFixed(this.fractionSlots)} ${scaled.unit}`);
    }
  }

  class GalaxyRandomNavigationWindow {
    constructor(options = {}) {
      this.futureTarget = Math.max(1, Number(options.futureTarget || 10));
      this.historyTarget = Math.max(1, Number(options.historyTarget || 10));
      this.hotTarget = Math.max(1, Number(options.hotTarget || 5));
      this.keyOf = typeof options.keyOf === 'function'
        ? options.keyOf
        : (destination) => cleanText(destination && (destination.archiveId || destination.name)).toLowerCase();

      this.future = [];
      this.backHistory = [];
      this.forwardHistory = [];
      this.current = null;
      this.locked = null;
      this.pending = null;
    }

    #destination(item) {
      return item && item.destination ? item.destination : item;
    }

    #key(item) {
      const explicit = cleanText(item && item.key).toLowerCase();
      if (explicit) return explicit;
      return cleanText(this.keyOf(this.#destination(item))).toLowerCase();
    }

    #dedupe(items) {
      const seen = new Set();
      const out = [];
      for (const item of items || []) {
        const key = this.#key(item);
        if (!key || seen.has(key)) continue;
        seen.add(key);
        out.push(item);
      }
      return out;
    }

    #blockedKeys() {
      const blocked = new Set();
      const currentKey = this.#key(this.current);
      const lockedKey = this.#key(this.locked);
      if (currentKey) blocked.add(currentKey);
      if (lockedKey) blocked.add(lockedKey);
      for (const item of [...this.backHistory, ...this.forwardHistory]) {
        const key = this.#key(item);
        if (key) blocked.add(key);
      }
      for (const item of this.future) {
        const key = this.#key(item);
        if (key) blocked.add(key);
      }
      return blocked;
    }

    setCurrent(destination) {
      this.current = destination || null;
      return this.current;
    }

    replaceFuture(destinations) {
      const blocked = new Set([
        this.#key(this.current),
        ...this.backHistory.map(item => this.#key(item)),
        ...this.forwardHistory.map(item => this.#key(item))
      ].filter(Boolean));

      this.future = this.#dedupe(destinations)
        .filter(item => item?.destination && !blocked.has(this.#key(item)))
        .slice(0, this.futureTarget);

      return this.getState();
    }

    appendFuture(bundle) {
      const key = this.#key(bundle);
      if (!key || !bundle?.destination || this.future.length >= this.futureTarget) return false;
      if (this.#blockedKeys().has(key)) return false;
      this.future.push(bundle);
      return true;
    }

    needsFuture() {
      return Math.max(0, this.futureTarget - this.future.length);
    }

    peekNext() {
      return this.future.length ? this.future[0] : null;
    }

    getFuture() {
      return Object.freeze([...this.future]);
    }

    getHistory() {
      return Object.freeze([...this.backHistory]);
    }

    getForwardHistory() {
      return Object.freeze([...this.forwardHistory]);
    }

    isNextReady(predicate) {
      const next = this.peekNext();
      if (!next || typeof predicate !== 'function') return false;
      return Boolean(predicate(next));
    }

    lockReadyNext(predicate) {
      if (this.locked) {
        if (typeof predicate === 'function' && !predicate(this.locked)) return null;
        return this.locked;
      }
      const next = this.peekNext();
      if (!next || typeof predicate !== 'function' || !predicate(next)) return null;
      this.locked = next;
      return this.locked;
    }

    lockNext() {
      if (this.locked) return this.locked;
      const next = this.peekNext();
      if (!next) return null;
      this.locked = next;
      return this.locked;
    }

    rollbackLocked() {
      const locked = this.locked;
      this.locked = null;
      return locked;
    }

    claimLocked() {
      if (!this.locked) throw new Error('No locked Random Galaxy destination to claim.');

      const lockedKey = this.#key(this.locked);
      const firstKey = this.#key(this.future[0]);

      if (!lockedKey || lockedKey !== firstKey)
        throw new Error('Random Galaxy FIFO invariant violated before claim.');

      const bundle = this.future[0];
      const destination = this.#destination(bundle);
      this.pending = Object.freeze({ kind: 'random', bundle, destination });
      this.locked = null;
      return bundle;
    }

    commitLocked(resolvedDestination = null) {
      const claimed = this.claimLocked();
      return this.commitPending(resolvedDestination || this.#destination(claimed));
    }

    lockHistoryBack() {
      if (this.pending || this.locked || !this.backHistory.length) return null;
      const destination = this.backHistory[this.backHistory.length - 1];
      this.pending = Object.freeze({ kind: 'back', destination });
      return destination;
    }

    lockHistoryForward() {
      if (this.pending || this.locked || !this.forwardHistory.length) return null;
      const destination = this.forwardHistory[this.forwardHistory.length - 1];
      this.pending = Object.freeze({ kind: 'forward', destination });
      return destination;
    }

    canBack() {
      return this.backHistory.length > 0 && !this.pending;
    }

    canForward() {
      return this.forwardHistory.length > 0 && !this.pending;
    }

    commitPending(resolvedDestination = null) {
      if (!this.pending) throw new Error('No pending Random Galaxy navigation to commit.');

      const pending = this.pending;
      const committed = resolvedDestination || pending.destination;
      const previous = this.current;

      if (pending.kind === 'random') {
        const pendingKey = this.#key(pending.bundle || pending.destination);
        const firstKey = this.#key(this.future[0]);

        if (!pendingKey || pendingKey !== firstKey)
          throw new Error('Random Galaxy pending FIFO invariant violated before commit.');

        this.future.shift();

        if (previous && this.#key(previous) !== this.#key(committed)) {
          this.backHistory.push(previous);
          if (this.backHistory.length > this.historyTarget)
            this.backHistory.splice(0, this.backHistory.length - this.historyTarget);
        }
        this.forwardHistory.length = 0;
      } else if (pending.kind === 'back') {
        const expected = this.backHistory[this.backHistory.length - 1];
        if (this.#key(expected) !== this.#key(pending.destination))
          throw new Error('Random Galaxy back-history invariant violated.');
        this.backHistory.pop();
        if (previous && this.#key(previous) !== this.#key(committed)) {
          this.forwardHistory.push(previous);
          if (this.forwardHistory.length > this.historyTarget)
            this.forwardHistory.splice(0, this.forwardHistory.length - this.historyTarget);
        }
      } else if (pending.kind === 'forward') {
        const expected = this.forwardHistory[this.forwardHistory.length - 1];
        if (this.#key(expected) !== this.#key(pending.destination))
          throw new Error('Random Galaxy forward-history invariant violated.');
        this.forwardHistory.pop();
        if (previous && this.#key(previous) !== this.#key(committed)) {
          this.backHistory.push(previous);
          if (this.backHistory.length > this.historyTarget)
            this.backHistory.splice(0, this.backHistory.length - this.historyTarget);
        }
      } else {
        throw new Error('Unknown Random Galaxy pending navigation kind.');
      }

      this.current = committed;
      this.pending = null;
      return committed;
    }

    rollbackPending() {
      if (!this.pending) {
        this.locked = null;
        return null;
      }

      const pending = this.pending;
      this.pending = null;
      this.locked = null;

      if (pending.kind === 'random') {
        const item = pending.bundle || pending.destination;
        const key = this.#key(item);

        if (key && this.#key(this.future[0]) !== key)
          throw new Error('Random Galaxy pending FIFO invariant violated during rollback.');
      }

      return pending.destination;
    }

    historyBack(indexFromNewest = 0) {
      const index = this.backHistory.length - 1 - Math.max(0, Number(indexFromNewest) || 0);
      return index >= 0 ? this.backHistory[index] : null;
    }

    hotKeys() {
      const ordered = [];
      const add = destination => {
        const key = this.#key(destination);
        if (key && !ordered.includes(key) && ordered.length < this.hotTarget)
          ordered.push(key);
      };

      // Five-hot neighborhood:
      // current + two immediately behind + two immediately ahead.
      add(this.current);

      for (let i = this.backHistory.length - 1, count = 0;
           i >= 0 && count < 2 && ordered.length < this.hotTarget;
           i--, count++)
        add(this.backHistory[i]);

      // During travel the claimed/locked future bundle must remain hot.
      if (this.pending) add(this.pending.bundle || this.pending.destination);

      for (let i = this.forwardHistory.length - 1;
           i >= 0 && ordered.length < this.hotTarget;
           i--)
        add(this.forwardHistory[i]);

      for (let i = 0;
           i < this.future.length && ordered.length < this.hotTarget;
           i++)
        add(this.future[i]);

      return Object.freeze(ordered.slice(0, this.hotTarget));
    }

    getState() {
      return Object.freeze({
        futureTarget: this.futureTarget,
        historyTarget: this.historyTarget,
        hotTarget: this.hotTarget,
        futureCount: this.future.length,
        historyCount: this.backHistory.length,
        forwardCount: this.forwardHistory.length,
        current: this.current,
        locked: this.locked,
        pending: this.pending,
        next: this.peekNext(),
        future: this.getFuture(),
        history: this.getHistory(),
        forwardHistory: this.getForwardHistory(),
        hotKeys: this.hotKeys()
      });
    }
  }

  const HOME_BOOTSTRAP_STYLE_ID = 'gvrg-home-bootstrap-style';

  function bootstrapHomePresentation(viewerRoot = document.body) {
    if (!(viewerRoot instanceof Element))
      throw new TypeError('GalaxyRandomGalaxy.bootstrapHomePresentation requires an Element viewerRoot.');

    let universe = viewerRoot.querySelector('#gv-universe-context');
    let home = viewerRoot.querySelector('#gv-we-are-here');

    // Idempotent: reuse presentation if it already exists.
    if (universe && home)
      return Object.freeze({ universeContext: universe, homeOverlay: home });

    // Clean up an incomplete stale pair rather than duplicating IDs.
    universe?.remove();
    home?.remove();

    if (!document.getElementById(HOME_BOOTSTRAP_STYLE_ID)) {
      const style = document.createElement('style');
      style.id = HOME_BOOTSTRAP_STYLE_ID;
      style.textContent = `
#gv-universe-context{position:absolute;left:50%;top:auto;bottom:calc(50% + min(25vw,50dvh) + 8px);z-index:7095;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;width:min(310px,76vw);pointer-events:none;transition:opacity .2s ease;font-family:"${FONT_NAMES.spaceAge}",sans-serif}
#gv-universe-context .gv-universe-label{padding:5px 8px 6px;border:1px solid rgba(124,203,255,.78);border-radius:6px;background:rgba(8,27,58,.68);box-shadow:0 0 9px rgba(88,191,255,.18);color:#DDF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 6px rgba(88,191,255,.42);font:400 9px/1.25 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.65px}
#gv-universe-context .gv-universe-count{display:block;margin-top:2px;color:#7CCBFF;font-size:10px;letter-spacing:.8px}
#gv-universe-context .gv-universe-leader{position:relative;width:1px;height:18px;background:rgba(124,203,255,.86);box-shadow:0 0 7px rgba(88,191,255,.48)}
#gv-universe-context .gv-universe-leader::after{content:"";position:absolute;left:50%;bottom:-1px;width:0;height:0;transform:translateX(-50%);border-left:5px solid transparent;border-right:5px solid transparent;border-top:8px solid #7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.68))}
#gv-universe-context.gv-hidden{opacity:0;visibility:hidden}
#gv-we-are-here{position:absolute;inset:0;z-index:7090;pointer-events:none;transition:opacity .2s ease;font-family:"${FONT_NAMES.spaceAge}",sans-serif}
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 25px);bottom:calc(50% - 140px);width:1px;min-height:36px;transform:translateX(-50%);background:rgba(124,203,255,.88);box-shadow:0 0 8px rgba(88,191,255,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.75))}
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:calc(50% + 140px);transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(124,203,255,.88);border-radius:6px;background:rgba(8,27,58,.74);color:#EAF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(88,191,255,.58);box-shadow:0 0 10px rgba(88,191,255,.24)}
#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:8px;color:#7CCBFF;font:400 15px/1.2 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1.25px}
#gv-we-are-here .gv-earth-icon{position:relative;isolation:isolate;display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:drop-shadow(0 0 2px rgba(87,255,147,.34))}
#gv-we-are-here .gv-earth-icon::before{content:"";position:absolute;left:50%;top:50%;width:31px;height:31px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(87,255,147,.27) 0%,rgba(77,255,143,.13) 46%,rgba(77,255,143,0) 76%);filter:blur(3px);z-index:-1}
#gv-we-are-here .gv-home-sub{margin-top:4px;color:#CDEEFF;font:400 10px/1.3 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px}
#gv-we-are-here .gv-home-hint{margin-top:5px;color:#A6DFFF;font:400 9px/1.3 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.8px}
#gv-we-are-here.gv-hidden{opacity:0;visibility:hidden}
`;
      document.head.appendChild(style);
    }

    universe = document.createElement('div');
    universe.id = 'gv-universe-context';
    universe.setAttribute('aria-live', 'polite');
    universe.dataset.gvrgHomeBootstrap = VERSION;
    universe.innerHTML =
      '<div class="gv-universe-label">' +
        'THIS IS OUR MAP OF THE OBSERVABLE UNIVERSE' +
        '<span class="gv-universe-count">EST. ~2 TRILLION GALAXIES</span>' +
      '</div>' +
      '<div class="gv-universe-leader" aria-hidden="true"></div>';

    home = document.createElement('div');
    home.id = 'gv-we-are-here';
    home.setAttribute('aria-live', 'polite');
    home.dataset.gvrgHomeBootstrap = VERSION;
    home.innerHTML =
      '<div class="gv-home-leader" aria-hidden="true"></div>' +