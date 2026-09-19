/*
GALAXY VIEWER ENGINEERING CHANGE ORDER — RANDOM GALAXY 0053
AUTHORIZED BASELINE: gv-random-galaxy-0124.js blob a4a9ddb3c28751dfbbf9fcdf04278c80e1020013.
AUTHORIZED CHANGES: readable compact arrival presentation, five-field HD science banner, exact retained decoded-image handoff for immediate HD display, and generic provider identity. Touch-through interaction, 36px provider controls, top-centered HD viewing, no post-arrival reframing, and configured travel behavior are preserved.
*/
(function (global) {
  'use strict';

  const VERSION='0161';

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
  function finiteNumber(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
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
  function routeDistanceMillionLy(source, destination) {
    const dA = finiteNumber(source && source.distance);
    const dB = finiteNumber(destination && destination.distance);
    if (dA != null && dA > 0 && dB != null && dB > 0) {
      const theta = angularSeparationRadians(source, destination);
      return { value: Math.sqrt(Math.max(0, dA * dA + dB * dB - 2 * dA * dB * Math.cos(theta))), exactRoute: true };
    }
    return { value: dB != null && dB > 0 ? dB : 0, exactRoute: false };
  }
  function scaledDistance(millionLy) {
    let value = finiteNumber(millionLy);
    value = value == null || value < 0 ? 0 : value;
    if (value < 1) return { value: value * 1_000_000, unit: 'LIGHT-YEARS' };
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
    render(millionLy) {
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
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 16px);bottom:34%;width:1px;min-height:36px;transform:translateX(-50%);background:rgba(124,203,255,.88);box-shadow:0 0 8px rgba(88,191,255,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.75))}
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:66%;transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(124,203,255,.88);border-radius:6px;background:rgba(8,27,58,.74);color:#EAF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(88,191,255,.58);box-shadow:0 0 10px rgba(88,191,255,.24)}
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
      '<div class="gv-home-label">' +
        '<div class="gv-home-origin">' +
          '<span class="gv-earth-icon" aria-hidden="true">🌎</span>' +
          '<strong>WE ARE HERE</strong>' +
        '</div>' +
        '<div class="gv-home-sub">EARTH — MILKY WAY</div>' +
        '<div class="gv-home-hint">TAP RANDOM GALAXY TO BEGIN</div>' +
      '</div>';

    viewerRoot.append(universe, home);

    return Object.freeze({
      universeContext: universe,
      homeOverlay: home
    });
  }



  // ==========================================================
  // REQ-017F / ECO-026D
  // Complete Earth-return presentation + tracking controller.
  // ==========================================================

  function createEarthReturnIndicator(root){
          const indicator=document.createElement('div');
          indicator.id='gv-earth-return-indicator';
          indicator.setAttribute('aria-live','polite');
          indicator.setAttribute('aria-hidden','true');
          indicator.innerHTML='<span class="gv-earth-return-arrow" aria-hidden="true"></span><span class="gv-earth-return-readout"><span class="gv-earth-return-icon" aria-hidden="true">🌎</span><span class="gv-earth-return-distance"><span class="gv-earth-return-value">0.0</span><span class="gv-earth-return-unit">MLY</span></span></span>';
          root.appendChild(indicator);
          return {
              root:indicator,
              arrow:indicator.querySelector('.gv-earth-return-arrow'),
              readout:indicator.querySelector('.gv-earth-return-readout'),
              icon:indicator.querySelector('.gv-earth-return-icon'),
              value:indicator.querySelector('.gv-earth-return-value'),
              unit:indicator.querySelector('.gv-earth-return-unit')
          };
      }

  function createEarthReturnController(options = {}) {
    const root = options.root;
    const aladin = options.aladin;
    const home = options.home || {};
    const hamburgerHost = options.hamburgerHost || null;
    const coordinateHost = options.coordinateHost || null;
    const targetHost = options.targetHost || null;
    const nav = options.nav || null;
    const skyPhysicalScale = options.skyPhysicalScale || null;
    const getHdViewport =
      typeof options.getHdViewport === 'function'
        ? options.getHdViewport
        : () => null;
    const isHdOpen =
      typeof options.isHdOpen === 'function'
        ? options.isHdOpen
        : () => false;

    const isNavigationPending =
      typeof options.isNavigationPending === 'function'
        ? options.isNavigationPending
        : () => false;

    if (!(root instanceof Element))
      throw new TypeError(
        'Earth-return controller requires a viewer root.'
      );

    const earthReturnIndicator =
      createEarthReturnIndicator(root);

    let earthReturnFrame=0;
    let earthReturnDestination=null;

    const hideEarthReturnIndicator=()=>{
        cancelAnimationFrame(earthReturnFrame);
        earthReturnFrame=0;
        earthReturnDestination=null;
        earthReturnIndicator.root.classList.remove('gv-visible');
        earthReturnIndicator.root.setAttribute('aria-hidden','true');
    };

    const formatEarthReturnDistance=destination=>{
        const millionLy=Number(destination?.distance);
        if(!Number.isFinite(millionLy)||millionLy<=0)return null;
        if(millionLy>=1000)return {value:(millionLy/1000).toFixed(1),unit:'BLY'};
        if(millionLy<1)return {value:(millionLy*1000).toFixed(1),unit:'KLY'};
        return {value:millionLy.toFixed(1),unit:'MLY'};
    };

    const updateEarthReturnIndicator=()=>{
        if(!earthReturnDestination||isNavigationPending())return;

        const rootRect=root.getBoundingClientRect();
        const compassReticle=document.getElementById('gv-center-reticle');
        const compassRect=compassReticle?.getBoundingClientRect?.();
        const centerX=compassRect&&compassRect.width>0
            ? compassRect.left-rootRect.left+compassRect.width/2
            : rootRect.width/2;
        const centerY=compassRect&&compassRect.height>0
            ? compassRect.top-rootRect.top+compassRect.height/2
            : rootRect.height/2;

        let earthX=null,earthY=null;
        try{
            if(typeof aladin.world2pix==='function'){
                const earthPixel=aladin.world2pix(home.ra,home.dec,"ICRSd");
                const ex=Number(earthPixel?.[0]),ey=Number(earthPixel?.[1]);
                if(Number.isFinite(ex)&&Number.isFinite(ey)){
                    earthX=ex;
                    earthY=ey;
                }
            }
        }catch(_){}

        const relativeBottom=element=>{
            if(!element)return 0;
            const rect=element.getBoundingClientRect();
            if(rect.width<=0||rect.height<=0)return 0;
            return rect.bottom-rootRect.top;
        };

        const indicatorRect=earthReturnIndicator.root.getBoundingClientRect();
        const indicatorHalfW=Math.max(29,Number(indicatorRect.width||0)/2);
        const indicatorHalfH=Math.max(24,Number(indicatorRect.height||0)/2);
        const readoutRadius=27;
        const visibleHalfW=indicatorHalfW+readoutRadius;
        const visibleHalfH=indicatorHalfH+readoutRadius;

        const hdViewport=isHdOpen()?getHdViewport():null;
        const hdRect=hdViewport?.getBoundingClientRect?.();
        const useHdEnvelope=Boolean(
            hdRect&&hdRect.width>0&&hdRect.height>0
        );

        let safeLeft,safeRight,apertureTop,apertureBottom;

        if(useHdEnvelope){
            const hdPointerInset=10;
            const hdLeft=hdRect.left-rootRect.left;
            const hdRight=hdRect.right-rootRect.left;
            const hdTop=hdRect.top-rootRect.top;
            const hdBottom=hdRect.bottom-rootRect.top;

            safeLeft=hdLeft+hdPointerInset;
            safeRight=hdRight-hdPointerInset;
            apertureTop=hdTop+hdPointerInset;
            apertureBottom=hdBottom-hdPointerInset;
        }else{
            const hamburgerControl=hamburgerHost.querySelector('button,[role="button"]')||hamburgerHost;
            const coordinateControl=coordinateHost;
            const targetControl=targetHost.querySelector('button,[role="button"]')||targetHost;

            const bannerWidth=Math.min(680,Math.max(40,rootRect.width-20));
            const apertureLeft=(rootRect.width-bannerWidth)/2;
            const apertureRight=apertureLeft+bannerWidth;
            const aladinSideInset=10;

            const topControlsBottom=Math.max(
                relativeBottom(hamburgerControl),
                relativeBottom(coordinateControl),
                relativeBottom(targetControl)
            );

            const navRect=nav.getBoundingClientRect();
            const card=document.querySelector('#gv-random-galaxy .gvrg-card');
            const cardRect=card?.getBoundingClientRect?.();
            const scaleRect=skyPhysicalScale?.getBoundingClientRect?.();
            const scaleVisible=
                skyPhysicalScale?.style?.display!=='none' &&
                scaleRect&&scaleRect.width>0&&scaleRect.height>0;

            const cardOrNavTop=
                cardRect&&cardRect.width>0&&cardRect.height>0
                    ? cardRect.top-rootRect.top
                    : navRect.top-rootRect.top;

            const lowerObstacleTop=
                scaleVisible
                    ? Math.min(cardOrNavTop,scaleRect.top-rootRect.top)
                    : cardOrNavTop;

            safeLeft=apertureLeft+aladinSideInset;
            safeRight=apertureRight-aladinSideInset;
            apertureTop=Math.max(0,topControlsBottom+6);
            apertureBottom=Math.max(
                apertureTop+1,
                Math.min(rootRect.height,lowerObstacleTop-8)
            );
        }

        const apertureCenterX=(safeLeft+safeRight)/2;
        const apertureCenterY=(apertureTop+apertureBottom)/2;
        const halfW=Math.max(1,(safeRight-safeLeft)/2);
        const halfH=Math.max(1,(apertureBottom-apertureTop)/2);

        let dx=1,dy=0;
        if(Number.isFinite(earthX)&&Number.isFinite(earthY)){
            dx=earthX-centerX;
            dy=earthY-centerY;
        }
        const magnitude=Math.hypot(dx,dy)||1;
        dx/=magnitude;
        dy/=magnitude;

        const cornerRadius=Math.max(
            0,
            Math.min(24,halfW,halfH)
        );

        let edgeScale=Infinity;
        const absDx=Math.abs(dx);
        const absDy=Math.abs(dy);
        const straightHalfW=Math.max(0,halfW-cornerRadius);
        const straightHalfH=Math.max(0,halfH-cornerRadius);

        if(absDx>0.001){
            const tx=halfW/absDx;
            if(Math.abs(dy*tx)<=straightHalfH+0.001)
                edgeScale=Math.min(edgeScale,tx);
        }

        if(absDy>0.001){
            const ty=halfH/absDy;
            if(Math.abs(dx*ty)<=straightHalfW+0.001)
                edgeScale=Math.min(edgeScale,ty);
        }

        if(!Number.isFinite(edgeScale)){
            const cornerX=(dx<0?-1:1)*straightHalfW;
            const cornerY=(dy<0?-1:1)*straightHalfH;
            const projection=dx*cornerX+dy*cornerY;
            const cornerDistanceSq=
                cornerX*cornerX+cornerY*cornerY;
            const discriminant=Math.max(
                0,
                projection*projection-
                (cornerDistanceSq-cornerRadius*cornerRadius)
            );
            edgeScale=projection+Math.sqrt(discriminant);
        }

        const arrowTipInset=6.5;
        const compassArrowRadius=119;
        const x=centerX+dx*compassArrowRadius;
        const y=centerY+dy*compassArrowRadius;

        earthReturnIndicator.root.style.left=`${x}px`;
        earthReturnIndicator.root.style.top=`${y}px`;

        const angle=Math.atan2(dy,dx)*180/Math.PI;
        earthReturnIndicator.arrow.style.transform=
            `translate(-50%,-50%) rotate(${angle}deg)`;

        const readoutWidth=Math.max(1,Number(earthReturnIndicator.readout.offsetWidth)||0);
        const readoutHeight=Math.max(1,Number(earthReturnIndicator.readout.offsetHeight)||0);
        const readoutHalfW=readoutWidth/2;
        const readoutHalfH=readoutHeight/2;
        const iconWidth=Math.max(1,Number(earthReturnIndicator.icon?.offsetWidth)||0);
        const iconHeight=Math.max(1,Number(earthReturnIndicator.icon?.offsetHeight)||0);
        const iconHalfW=iconWidth/2;
        const iconHalfH=iconHeight/2;
        const iconCenterOffsetX=(Number(earthReturnIndicator.icon?.offsetLeft)||0)+iconHalfW-readoutHalfW;
        const iconCenterOffsetY=(Number(earthReturnIndicator.icon?.offsetTop)||0)+iconHalfH-readoutHalfH;
        const calloutMargin=8;
        const arrowBodyLength=14;
        const calloutGap=6;
        const iconRadialSupport=Math.abs(dx)*iconHalfW+Math.abs(dy)*iconHalfH;

        /*
         * REQ-001 — keep the complete Earth-return presentation at the
         * safe perimeter and never leave the CSS 50%/50% center fallback.
         */
        const anchorX=Number.isFinite(x)
            ? x
            : Math.max(safeLeft,safeRight-arrowTipInset);
        const anchorY=Number.isFinite(y)
            ? y
            : apertureCenterY;

        earthReturnIndicator.root.style.left=`${anchorX}px`;
        earthReturnIndicator.root.style.top=`${anchorY}px`;

        const minimumDistance=
            arrowBodyLength+calloutGap+iconRadialSupport;

        const perimeterBandDepth=Math.max(
            24,
            Math.min(52,Math.min(halfW,halfH)*0.28)
        );

        const calloutInset=Math.min(
            minimumDistance,
            perimeterBandDepth
        );

        const minX=safeLeft+readoutHalfW+calloutMargin;
        const maxX=safeRight-readoutHalfW-calloutMargin;
        const minY=apertureTop+readoutHalfH+calloutMargin;
        const maxY=apertureBottom-readoutHalfH-calloutMargin;

        const desiredX=
            anchorX-dx*calloutInset-iconCenterOffsetX;
        const desiredY=
            anchorY-dy*calloutInset-iconCenterOffsetY;

        let readoutX=
            minX<=maxX
                ? Math.min(maxX,Math.max(minX,desiredX))
                : anchorX;

        let readoutY=
            minY<=maxY
                ? Math.min(maxY,Math.max(minY,desiredY))
                : anchorY;

        /*
         * REQ-004 — protect the Galaxy Viewer reticle at six o'clock
         * without moving the astronomical arrow off its approved perimeter.
         * Only the inward readout/callout is displaced. Prefer downward
         * clearance; if unavailable, slide laterally inside the safe aperture.
         */
        const centerReticle=document.getElementById('gv-center-reticle');
        const centerReticleRect=centerReticle?.getBoundingClientRect?.();
        const centerReticleStyle=centerReticle
            ? getComputedStyle(centerReticle)
            : null;
        const centerReticleVisible=false;

        if(centerReticleVisible&&dy>0.001&&minX<=maxX&&minY<=maxY){
            const reticleClearance=8;
            const reticleLeft=
                centerReticleRect.left-rootRect.left-reticleClearance;
            const reticleRight=
                centerReticleRect.right-rootRect.left+reticleClearance;
            const reticleTop=
                centerReticleRect.top-rootRect.top-reticleClearance;
            const reticleBottom=
                centerReticleRect.bottom-rootRect.top+reticleClearance;

            const overlapsReticle=(px,py)=>
                px+readoutHalfW>reticleLeft &&
                px-readoutHalfW<reticleRight &&
                py+readoutHalfH>reticleTop &&
                py-readoutHalfH<reticleBottom;

            if(overlapsReticle(readoutX,readoutY)){
                const belowY=reticleBottom+readoutHalfH;

                if(belowY<=maxY){
                    readoutY=Math.max(readoutY,belowY);
                }else{
                    const leftX=reticleLeft-readoutHalfW;
                    const rightX=reticleRight+readoutHalfW;
                    const leftFits=leftX>=minX;
                    const rightFits=rightX<=maxX;

                    readoutY=maxY;

                    if(leftFits&&rightFits){
                        readoutX=
                            Math.abs(readoutX-leftX)<=Math.abs(rightX-readoutX)
                                ? leftX
                                : rightX;
                    }else if(leftFits){
                        readoutX=leftX;
                    }else if(rightFits){
                        readoutX=rightX;
                    }
                }
            }
        }

        const rx=readoutX-anchorX;
        const ry=readoutY-anchorY;

        earthReturnIndicator.readout.style.transform=
            `translate(calc(-50% + ${rx.toFixed(1)}px),calc(-50% + ${ry.toFixed(1)}px))`;

        earthReturnFrame=requestAnimationFrame(updateEarthReturnIndicator);
    };

    const showEarthReturnIndicator=destination=>{
        const formatted=formatEarthReturnDistance(destination);
        if(!formatted){hideEarthReturnIndicator();return}

        cancelAnimationFrame(earthReturnFrame);
        earthReturnDestination=destination;
        earthReturnIndicator.value.textContent=formatted.value;
        earthReturnIndicator.unit.textContent=formatted.unit;
        earthReturnIndicator.root.removeAttribute('aria-hidden');
        earthReturnIndicator.root.classList.add('gv-visible');
        updateEarthReturnIndicator();
    };



    return Object.freeze({
      show: showEarthReturnIndicator,
      hide: hideEarthReturnIndicator,

      destroy() {
        hideEarthReturnIndicator();
        earthReturnIndicator.root.remove();
      }
    });
  }



  // ==========================================================
  // REQ-017C / REQ-017D / ECO-026E-1
  // Archive/source + HD integration owner.
  // ==========================================================

  function installHdArchiveIntegration(randomGalaxy, options = {}) {
    if (!randomGalaxy)
      throw new TypeError(
        'HD/archive integration requires a Random Galaxy instance.'
      );

    const bottom = options.bottom;

    if (!bottom)
      throw new TypeError(
        'HD/archive integration requires viewer bottom controls.'
      );

    const TARGET_ICON_URL =
      cleanText(options.targetIconUrl);

    const HD_LAYOUT =
      options.hdLayout || {
        bannerRatio:403/1536,
        imageRatio:630/1536,
        gap:6,
        edge:6,
        iconInset:20
      };

    const getPrefetchReady =
      typeof options.getPrefetchReady === 'function'
        ? options.getPrefetchReady
        : () => [];

    const isBackgroundWorkSuspended =
      typeof options.isBackgroundWorkSuspended === 'function'
        ? options.isBackgroundWorkSuspended
        : () => false;

    const isNavigationPending =
      typeof options.isNavigationPending === 'function'
        ? options.isNavigationPending
        : () => false;

    const getActiveTargetKey =
      typeof options.getActiveTargetKey === 'function'
        ? options.getActiveTargetKey
        : () => '';

    const onSetHistoryControls =
      typeof options.onSetHistoryControls === 'function'
        ? options.onSetHistoryControls
        : () => {};

    const onHideEarthReturn =
      typeof options.onHideEarthReturn === 'function'
        ? options.onHideEarthReturn
        : () => {};

    // HD presentation: archive/source controls + Galaxy Info + BACK TO SKY.

    const hdScience=randomGalaxy.hdScience;
    if(hdScience){
        const scienceItems=[...hdScience.querySelectorAll('.gvrg-hd-science-item')];
        const constellationItems=scienceItems.filter(item=>String(item.querySelector('.gvrg-hd-science-label')?.textContent||'').trim().toUpperCase()==='CONST');
        let constellationItem=constellationItems.shift()||null;
        constellationItems.forEach(item=>item.remove());
        let constellationValue=null;
        if(!constellationItem){
            constellationItem=document.createElement('div');
            constellationItem.className='gvrg-hd-science-item';
            const key=document.createElement('div');
            key.className='gvrg-hd-science-label';
            key.textContent='CONST';
            constellationValue=document.createElement('div');
            constellationValue.className='gvrg-hd-science-value';
            constellationItem.append(key,constellationValue);
            const ageItem=scienceItems.find(item=>String(item.querySelector('.gvrg-hd-science-label')?.textContent||'').trim().toUpperCase()==='AGE');
            hdScience.insertBefore(constellationItem,ageItem||null);
        }else{
            constellationValue=constellationItem.querySelector('.gvrg-hd-science-value');
        }
        const syncHdConst=()=>{
            if(constellationValue)constellationValue.textContent=String(randomGalaxy.activeDestination?.constellation||randomGalaxy.constellationValueEl?.textContent||'').trim().toUpperCase();
        };
        if(randomGalaxy.constellationValueEl)new MutationObserver(syncHdConst).observe(randomGalaxy.constellationValueEl,{childList:true,subtree:true,characterData:true});
        randomGalaxy.viewHdButton?.addEventListener('click',syncHdConst,true);
        randomGalaxy.providerIconButton?.addEventListener('click',syncHdConst,true);
        syncHdConst();
    }

    const hdDownloadButton=randomGalaxy.downloadButton||null;

    const hdInfoPanel=document.createElement('div');
    hdInfoPanel.id='gv-hd-info-panel';
    hdInfoPanel.innerHTML='<div id="gv-hd-info-title">GALAXY INFO</div><div id="gv-hd-info-body"></div><div id="gv-hd-control-row"></div>';
    randomGalaxy.hdOverlay?.appendChild(hdInfoPanel);
    const hdInfoBody=hdInfoPanel.querySelector('#gv-hd-info-body');
    const hdControlRow=hdInfoPanel.querySelector('#gv-hd-control-row');
    randomGalaxy.hdViewport.dataset.gvFixedViewport='1';
    const hdBackToSky=randomGalaxy.backButton;
    if(hdBackToSky){
        // Preserve the established denomination exactly: BACK TO SKY.
        const backLabel=hdBackToSky.lastElementChild;
        if(backLabel)backLabel.textContent='BACK TO SKY';
        else hdBackToSky.textContent='BACK TO SKY';
        hdBackToSky.setAttribute('aria-label','BACK TO SKY');
        hdControlRow.appendChild(hdBackToSky);
    }
    function restoreAfterHdClose(attempt=0){
        if(isHdPresentationActive()){
            if(attempt<60)requestAnimationFrame(()=>restoreAfterHdClose(attempt+1));
            return;
        }
        resetHdPresentationGeometry();
        restoreNormalViewerPresentation();
        // 0034 owns BACK TO SKY Aladin state restoration.
    }
    if(hdBackToSky)hdBackToSky.addEventListener('click',()=>{try{document.body.classList.remove('gv-hd-open')}catch(_){};onHideEarthReturn();requestAnimationFrame(()=>restoreAfterHdClose())},true);
    if(hdDownloadButton){
        hdDownloadButton.id='gv-hd-download-button';
        hdDownloadButton.setAttribute('aria-label','DOWNLOAD HD IMAGE');
        hdDownloadButton.setAttribute('title','DOWNLOAD HD IMAGE');
        hdDownloadButton.remove();
    }
    if(randomGalaxy.creditEl)randomGalaxy.creditEl.remove();

    const hdArchiveButton=document.createElement('button');
    hdArchiveButton.id='gv-hd-archive-button';
    hdArchiveButton.type='button';
    hdArchiveButton.setAttribute('aria-label','OPEN ARCHIVE SOURCE');
    const hdArchiveIcon=document.createElement('img');
    hdArchiveIcon.alt='ARCHIVE SOURCE';
    const hdArchiveComet=document.createElement('span');
    hdArchiveComet.className='gv-hd-archive-comet';
    hdArchiveComet.setAttribute('aria-hidden','true');
    hdArchiveButton.append(hdArchiveIcon,hdArchiveComet);
    randomGalaxy.hdViewport?.appendChild(hdArchiveButton);
    hdArchiveButton.addEventListener('pointerdown',event=>event.stopPropagation(),true);
    hdArchiveButton.addEventListener('pointerup',event=>event.stopPropagation(),true);

    const archiveOverlay=document.createElement('div');
    archiveOverlay.id='gv-archive-overlay';
    let archiveFrame=document.createElement('iframe');
    archiveFrame.id='gv-archive-frame';
    archiveFrame.title='GALAXY ARCHIVE SOURCE';
    archiveFrame.setAttribute('scrolling','yes');
    const archiveBack=document.createElement('button');
    archiveBack.id='gv-archive-back';
    archiveBack.type='button';
    const archiveArrow=document.createElement('span');
    archiveArrow.id='gv-archive-arrow';
    archiveArrow.setAttribute('aria-hidden','true');
    const archiveTargetTile=document.createElement('span');
    archiveTargetTile.id='gv-archive-target-tile';
    archiveTargetTile.setAttribute('aria-hidden','true');
    const archiveTarget=document.createElement('img');
    archiveTarget.src=TARGET_ICON_URL;
    archiveTarget.alt='';
    archiveTarget.setAttribute('aria-hidden','true');
    archiveTargetTile.appendChild(archiveTarget);
    const archiveBackLabel=document.createElement('span');
    archiveBackLabel.textContent='BACK TO GALAXY VIEWER';
    archiveBack.append(archiveArrow,archiveBackLabel,archiveTargetTile);
    archiveBack.setAttribute('aria-label','BACK TO GALAXY VIEWER');
    archiveOverlay.append(archiveFrame,archiveBack);
    document.body.appendChild(archiveOverlay);
    let archiveSourceUrl='';
    let archiveLoadedUrl='';
    let archiveOpenRequested=false;
    let archiveClosing=false;
    let archiveLaunchReadyAt=0;
    let archiveRevealTimer=0;
    const archiveViewportMeta=document.querySelector('meta[name="viewport"]');
    const archiveViewportContent=archiveViewportMeta?.getAttribute('content')||'';
    const enableArchivePinchZoom=()=>{
        if(archiveViewportMeta)archiveViewportMeta.setAttribute('content','width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=5,user-scalable=yes,viewport-fit=cover');
    };
    const restoreArchiveViewport=()=>{
        if(archiveViewportMeta)archiveViewportMeta.setAttribute('content',archiveViewportContent);
    };
    const archivePreloadQueue=[];
    let archivePreloadSuspended=false;
    let archivePreloadLoadingItem=null;
    let archivePreloadController=null;
    let activeArchivePreloadItem=null;
    const archivePreloadFailedKeys=new Set();
    const setArchiveLoading=loading=>{
        hdArchiveButton.classList.toggle('gv-archive-loading',loading);
    };
    const loadArchiveFrameSource=sourceUrl=>{
        archiveFrame.src=sourceUrl;
    };
    const releaseActiveArchivePreload=()=>{
        activeArchivePreloadItem=null;
        archiveSourceUrl='';
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        try{archiveFrame.src='about:blank'}catch(_){}
    };
    const revealArchiveWhenReady=()=>{
        if(!archiveOpenRequested||archiveClosing||!archiveSourceUrl)return;

        const destination=currentArchiveDestination();
        const expectedSourceUrl=String(destination?.sourceUrl||'').trim();

        if(
            !isUsableArchiveSourceUrl(archiveSourceUrl) ||
            archiveLoadedUrl!==archiveSourceUrl ||
            expectedSourceUrl!==archiveSourceUrl
        )return;

        archiveRevealTimer=0;
        setArchiveLoading(false);
        archiveOverlay.removeAttribute('aria-hidden');
        archiveOverlay.style.removeProperty('visibility');
        archiveOverlay.style.removeProperty('opacity');
        archiveOverlay.style.pointerEvents='auto';
        archiveOverlay.classList.add('gv-open');
        archiveFrame.style.pointerEvents='auto';
    };
    const archiveQueueKey=destination=>String(destination?.archiveId||destination?.name||'').trim().toLowerCase();
    const isUsableArchiveSourceUrl=value=>{
        try{
            const url=new URL(String(value||'').trim(),window.location.href);

            if(url.protocol!=='https:')return false;

            const host=String(url.hostname||'').toLowerCase();
            const path=String(url.pathname||'').toLowerCase();

            if(
                host==='gear66me-ui.github.io' &&
                path.endsWith('/generic-app.html')
            )return false;

            return true;
        }catch(_){
            return false;
        }
    };
    const chooseArchivePreloadDestination=()=>{
        const excluded=new Set([getActiveTargetKey(),...archivePreloadQueue.map(item=>item.key),activeArchivePreloadItem?.key,...archivePreloadFailedKeys].filter(Boolean));
        const prepared=getPrefetchReady().find(item=>{
            const destination=item?.destination;
            const key=item?.key||archiveQueueKey(destination);
            const sourceUrl=String(destination?.sourceUrl||'').trim();
            return key&&!excluded.has(key)&&isUsableArchiveSourceUrl(sourceUrl);
        });
        return prepared?.destination||null;
    };
    const startNextArchivePreload=()=>{
        if(archivePreloadSuspended||isBackgroundWorkSuspended()||isNavigationPending()||archivePreloadLoadingItem)return;
        if(archivePreloadQueue.filter(item=>item.state==='preloaded').length>=ARCHIVE_PRELOAD_TARGET)return;
        let item=archivePreloadQueue.find(candidate=>candidate.state==='pending');
        if(!item){
            const destination=chooseArchivePreloadDestination();
            if(!destination)return;
            item={key:archiveQueueKey(destination),destination,sourceUrl:String(destination.sourceUrl||'').trim(),state:'pending'};
            archivePreloadQueue.push(item);
        }
        archivePreloadLoadingItem=item;
        item.state='loading';
        const controller=new AbortController();
        archivePreloadController=controller;
        fetch(item.sourceUrl,{mode:'no-cors',cache:'force-cache',credentials:'omit',signal:controller.signal,priority:'low'})
            .then(()=>{
                if(archivePreloadLoadingItem!==item)return;
                item.state='preloaded';
                item.loadedAt=performance.now();
            })
            .catch(error=>{
                if(error?.name==='AbortError'){
                    if(archivePreloadQueue.includes(item))item.state='pending';
                    return;
                }
                archivePreloadFailedKeys.add(item.key);
                const index=archivePreloadQueue.indexOf(item);
                if(index>=0)archivePreloadQueue.splice(index,1);
            })
            .finally(()=>{
                if(archivePreloadLoadingItem===item)archivePreloadLoadingItem=null;
                if(archivePreloadController===controller)archivePreloadController=null;
                if(!archivePreloadSuspended&&!isBackgroundWorkSuspended()&&!isNavigationPending())queueMicrotask(ensureArchivePreloadQueue);
            });
    };
    let ensureArchivePreloadQueue=()=>{
        if(archivePreloadSuspended||isBackgroundWorkSuspended()||isNavigationPending())return;
        while(archivePreloadQueue.length<ARCHIVE_PRELOAD_TARGET){
            const destination=chooseArchivePreloadDestination();
            if(!destination)break;
            archivePreloadQueue.push({key:archiveQueueKey(destination),destination,sourceUrl:String(destination.sourceUrl||'').trim(),state:'pending'});
        }
        startNextArchivePreload();
    };
    const suspendArchivePreloads=()=>{
        archivePreloadSuspended=true;
        const item=archivePreloadLoadingItem;
        const protectedKey=String(getActiveTargetKey()||'').trim().toLowerCase();
        if(item?.key&&protectedKey&&String(item.key).trim().toLowerCase()===protectedKey)return;
        archivePreloadLoadingItem=null;
        if(item&&archivePreloadQueue.includes(item)&&item.state==='loading')item.state='pending';
        if(archivePreloadController){try{archivePreloadController.abort()}catch(_){};archivePreloadController=null}
    };
    const resumeArchivePreloads=()=>{
        if(isNavigationPending())return;
        archivePreloadSuspended=false;
        queueMicrotask(ensureArchivePreloadQueue);
    };
    const consumeArchivePreloadedDestination=excludeName=>{
        const excluded=String(excludeName||'').trim().toLowerCase();
        const index=archivePreloadQueue.findIndex(item=>item.state==='preloaded'&&String(item.destination?.name||'').trim().toLowerCase()!==excluded);
        if(index<0)return null;
        return archivePreloadQueue.splice(index,1)[0];
    };
    const bindActiveArchivePreload=(item,destination)=>{
        if(!item)return;
        activeArchivePreloadItem=item;
        activeArchivePreloadItem.destination=destination;
        archiveSourceUrl='';
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        archiveClosing=false;
    };
    const preloadArchiveSource=destination=>{
        if(isNavigationPending()||isBackgroundWorkSuspended())return;
        const sourceUrl=String(destination?.sourceUrl||'').trim();
        if(!isUsableArchiveSourceUrl(sourceUrl)||archiveSourceUrl===sourceUrl)return;
        archiveSourceUrl=sourceUrl;
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        archiveClosing=false;
        archiveOverlay.classList.remove('gv-open');
        archiveOverlay.style.pointerEvents='none';
        archiveOverlay.setAttribute('aria-hidden','true');
        archiveFrame.style.pointerEvents='none';
        loadArchiveFrameSource(sourceUrl);
    };
    const consumeArchiveBackEvent=event=>{
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
    };
    const closeArchiveOverlay=()=>{
        if(archiveClosing)return;
        archiveClosing=true;
        setArchiveLoading(false);
        restoreArchiveViewport();
        archiveOverlay.classList.remove('gv-open');
        archiveOverlay.style.pointerEvents='none';
        archiveOverlay.style.visibility='hidden';
        archiveOverlay.style.opacity='0';
        archiveOverlay.setAttribute('aria-hidden','true');
        archiveFrame.style.pointerEvents='none';
        archiveFrame.blur();
        archiveOpenRequested=false;
        archiveLaunchReadyAt=0;
        clearTimeout(archiveRevealTimer);
        archiveRevealTimer=0;
        archiveClosing=false;
        requestAnimationFrame(()=>{
            if(!isHdPresentationActive())return;
            settleHdPresentation();
            try{hdArchiveButton.focus({preventScroll:true})}catch(_){}
        });
    };
    archiveBack.addEventListener('pointerdown',consumeArchiveBackEvent,true);
    archiveBack.addEventListener('pointerup',consumeArchiveBackEvent,true);
    archiveBack.addEventListener('click',event=>{
        consumeArchiveBackEvent(event);
        closeArchiveOverlay();
    },true);
    archiveFrame.addEventListener('load',()=>{
        if(!archiveSourceUrl||archiveClosing)return;

        const destination=currentArchiveDestination();
        const expectedSourceUrl=String(destination?.sourceUrl||'').trim();
        const loadedUrl=String(archiveFrame.src||'').trim();

        if(
            !isUsableArchiveSourceUrl(archiveSourceUrl) ||
            loadedUrl!==archiveSourceUrl ||
            expectedSourceUrl!==archiveSourceUrl
        )return;

        try{
            const observedUrl=String(
                archiveFrame.contentWindow?.location?.href||''
            ).trim();

            if(
                observedUrl &&
                observedUrl!=='about:blank' &&
                (
                    !isUsableArchiveSourceUrl(observedUrl) ||
                    observedUrl!==archiveSourceUrl
                )
            )return;
        }catch(_){
            // Cross-origin archive pages cannot expose their final URL.
            // Exact requested source identity is enforced above.
        }

        archiveLoadedUrl=archiveSourceUrl;
        revealArchiveWhenReady();
    });
    archiveFrame.addEventListener('error',()=>{
        const sourceUrl=archiveSourceUrl;
        const requested=archiveOpenRequested;
        archiveLoadedUrl='';
        archiveOpenRequested=false;
        archiveLaunchReadyAt=0;
        clearTimeout(archiveRevealTimer);
        archiveRevealTimer=0;
        setArchiveLoading(false);
        if(requested&&sourceUrl)closeArchiveOverlay();
    });
    function currentArchiveDestination(){return randomGalaxy.getState?.().activeDestination||randomGalaxy.activeDestination||null}
    function providerFor(destination){
        return String(destination?.provider||'').trim().toUpperCase();
    }

    function providerIdentityFor(destination){
        const provider=String(destination?.provider||'').trim();
        const telescope=String(destination?.telescope||'').trim();

        const evidence=[
            provider,
            telescope,
            destination?.source,
            destination?.hdUrl,
            destination?.sourceUrl
        ].map(value=>String(value||'').trim().toLowerCase()).filter(Boolean).join(' ');

        if(/(?:^|[^a-z0-9])(?:hubble|hst|esahubble)(?:[^a-z0-9]|$)/i.test(evidence))
            return Object.freeze({slug:'hubble',label:'HUBBLE'});

        if(/(?:^|[^a-z0-9])(?:jwst|james webb|webb|esawebb)(?:[^a-z0-9]|$)/i.test(evidence))
            return Object.freeze({slug:'jwst',label:'JWST'});

        if(/(?:^|[^a-z0-9])spitzer(?:[^a-z0-9]|$)/i.test(evidence))
            return Object.freeze({slug:'spitzer',label:'SPITZER'});

        if(/(?:^|[^a-z0-9])chandra(?:[^a-z0-9]|$)/i.test(evidence))
            return Object.freeze({slug:'chandra',label:'CHANDRA'});

        const label=String(provider||telescope||'').trim().toUpperCase();
        const slug=String(provider||telescope||'')
            .trim()
            .toLowerCase()
            .replace(/[^a-z0-9]+/g,'-')
            .replace(/^-+|-+$/g,'');

        return Object.freeze({slug,label});
    }

    function providerIconUrl(destination){
        const explicit=String(
            destination?.providerIconUrl ||
            destination?.provider_icon_url ||
            ''
        ).trim();

        if(/^https:\/\//i.test(explicit))return explicit;

        const {slug}=providerIdentityFor(destination);
        if(!slug)return '';

        const encoded=encodeURIComponent(slug);
        return `https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/providers/${encoded}/${encoded}-icon.png`;
    }
    hdArchiveButton.addEventListener('click',event=>{
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        const destination=currentArchiveDestination();
        const sourceUrl=String(destination?.sourceUrl||'').trim();
        if(!isUsableArchiveSourceUrl(sourceUrl))return;
        onHideEarthReturn();
        enableArchivePinchZoom();
        archiveOpenRequested=true;
        archiveClosing=false;
        archiveLaunchReadyAt=performance.now();
        setArchiveLoading(true);
        if(archiveSourceUrl!==sourceUrl){
            preloadArchiveSource(destination);
            archiveOpenRequested=true;
        }
        revealArchiveWhenReady();
    },true);


    function galaxyInfoText(destination){
        if(!destination)return '';
        const provider=providerFor(destination);
        const telescope=String(destination.telescope||provider||'TELESCOPE').trim().toUpperCase();
        const identity=String(destination.commonName||destination.designation||destination.name||'THIS GALAXY').trim().toUpperCase();
        const parts=[`${identity} — ${telescope} IMAGERY.`];
        if(destination.constellation)parts.push(`CONSTELLATION ${String(destination.constellation).trim().toUpperCase()}.`);
        const distance=Number(destination.distance);
        if(Number.isFinite(distance)&&distance>0)parts.push(`DISTANCE ${distance>=1000?(distance/1000).toFixed(2)+' BILLION':distance.toFixed(distance>=100?0:1)+' MILLION'} LIGHT-YEARS.`);
        if(destination.age)parts.push(`AGE ${String(destination.age).trim().toUpperCase()}.`);
        if(destination.imageType)parts.push(`${String(destination.imageType).trim().toUpperCase()} IMAGE.`);
        return parts.join(' ');
    }

    function renderHdInfoCandidate(words,count){
        hdInfoBody.replaceChildren();
        const bodyRect=hdInfoBody.getBoundingClientRect();
        const style=getComputedStyle(hdInfoBody);
        const font=style.font||`${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
        const measuredLineHeight=parseFloat(style.lineHeight);
        const fontSize=parseFloat(style.fontSize)||10.5;
        const lineHeight=Number.isFinite(measuredLineHeight)?measuredLineHeight:fontSize*1.45;
        const canvas=renderHdInfoCandidate._canvas||(renderHdInfoCandidate._canvas=document.createElement('canvas'));
        const context=canvas.getContext('2d');
        context.font=font;
        const controlRect=hdControlRow.getBoundingClientRect();
        const noWriteGap=14;
        const textBottom=Math.min(bodyRect.bottom,controlRect.top-noWriteGap);
        const sourceWords=count?words.slice(0,count):[];
        const lines=[];
        let index=0;
        const maxLines=Math.max(0,Math.floor((Math.max(0,textBottom-bodyRect.top)+.5)/lineHeight));
        const letterSpacing=parseFloat(style.letterSpacing)||0;
        const measure=value=>context.measureText(value).width+Math.max(0,value.length-1)*letterSpacing;
        for(let lineIndex=0;lineIndex<maxLines&&index<sourceWords.length;lineIndex++){
            const lineTop=bodyRect.top+lineIndex*lineHeight;
            const lineBottom=lineTop+lineHeight;
            if(lineBottom>textBottom+.5)break;
            const leftOffset=0;
            const availableWidth=bodyRect.width;
            if(availableWidth<24)break;
            let text='';
            while(index<sourceWords.length){
                const proposed=text?`${text} ${sourceWords[index]}`:sourceWords[index];
                if(text&&measure(proposed)>availableWidth)break;
                if(!text&&measure(proposed)>availableWidth){
                    text=proposed;
                    index++;
                    break;
                }
                text=proposed;
                index++;
            }
            if(!text)break;
            lines.push({text,width:availableWidth,left:leftOffset});
        }
        const truncated=index<sourceWords.length||count<words.length;
        if(truncated&&lines.length){
            let line=lines[lines.length-1];
            let text=line.text.replace(/\s*…$/,'');
            while(text&&measure(`${text} …`)>line.width)text=text.replace(/\s+\S+$/,'');
            line.text=text?`${text} …`:'…';
        }
        const fragment=document.createDocumentFragment();
        for(const line of lines){
            const row=document.createElement('div');
            row.textContent=line.text;
            Object.assign(row.style,{display:'block',marginLeft:`${line.left}px`,width:`${line.width}px`,height:`${lineHeight}px`,lineHeight:`${lineHeight}px`,whiteSpace:'nowrap',overflow:'hidden'});
            fragment.appendChild(row);
        }
        hdInfoBody.appendChild(fragment);
        return {renderedWords:index,lineCount:lines.length,truncated};
    }

    function fitHdInfoText(destination=currentArchiveDestination()){
        if(!hdInfoBody||!destination)return;
        const words=galaxyInfoText(destination).split(/\s+/).filter(Boolean);
        const metrics=renderHdInfoCandidate(words,words.length);
        hdInfoBody.dataset.fittedCharacters=String(hdInfoBody.textContent.length);
        hdInfoBody.dataset.fittedWords=String(metrics.renderedWords);
    }

    function syncHdProviderPresentation(destination=currentArchiveDestination()){
        if(!destination)return;

        const provider=providerFor(destination);
        const telescope=String(destination.telescope||'').trim().toUpperCase();
        const providerIdentity=providerIdentityFor(destination);
        const label=providerIdentity.label||provider||telescope||'IMAGE';
        const iconUrl=providerIconUrl(destination);

        if(randomGalaxy.viewHdButton){
            randomGalaxy.viewHdButton.textContent=`VIEW ${label} IN HD`;
            randomGalaxy.viewHdButton.setAttribute('aria-label',`VIEW ${label} IN HD`);
        }

        if(randomGalaxy.providerIconButton)
            randomGalaxy.providerIconButton.setAttribute('aria-label',`VIEW ${label} IN HD`);

        const applyProviderIcon=image=>{
            if(!(image instanceof HTMLImageElement))return;

            image.onerror=null;

            if(!iconUrl){
                image.removeAttribute('src');
                image.alt='';
                return;
            }

            image.src=iconUrl;
            image.alt=`${label} ARCHIVE`;
            image.onerror=()=>{
                image.onerror=null;
                image.removeAttribute('src');
            };
        };

        applyProviderIcon(randomGalaxy.providerIconButton?.querySelector('img'));
        applyProviderIcon(hdArchiveIcon);

        hdArchiveButton.setAttribute('aria-label',`OPEN ${label} ARCHIVE SOURCE`);
        fitHdInfoText(destination);
    }

    resumeArchivePreloads();

    function applySmartHdCrop(){
        const image=randomGalaxy.hdImage;
        if(!(image instanceof HTMLImageElement)||!image.complete||!image.naturalWidth)return;
        image.style.objectFit='contain';
        image.style.objectPosition='50% 50%';
    }

    function isHdPresentationActive(){const active=Boolean(randomGalaxy.getState?.().hdOpen);try{document.body.classList.toggle('gv-hd-open',active)}catch(_){};return active}

    let hdFixedViewportGeometry=null;

    function resetHdPresentationGeometry(){
        hdFixedViewportGeometry=null;
        const clear=(element,...names)=>{
            if(!element)return;
            for(const name of names)element.style.removeProperty(name);
        };
        clear(randomGalaxy.hdScience,'top','height','max-height');
        clear(randomGalaxy.hdViewport,'top','bottom','width','max-width','height','max-height','pointer-events');
        clear(hdInfoPanel,'top','height','max-height','pointer-events');
        clear(hdControlRow,'pointer-events','display','visibility','opacity','z-index');
        clear(hdBackToSky,'display','visibility','opacity','pointer-events');
        clear(hdDownloadButton,'display','visibility','opacity','pointer-events');
        clear(hdArchiveButton,'pointer-events');
        clear(randomGalaxy.hdOverlay,'pointer-events');
    }

    function restoreNormalViewerPresentation(){
        resetHdPresentationGeometry();
        bottom.version.style.top='';
        bottom.version.style.bottom='51px';
        if(!archiveOverlay.classList.contains('gv-open')){
            archiveOverlay.style.pointerEvents='none';
            archiveOverlay.setAttribute('aria-hidden','true');
            archiveFrame.style.pointerEvents='none';
        }
        bottom.nav.style.display='flex';
        bottom.random.style.display='flex';
        bottom.back.style.display='flex';
        bottom.forward.style.display='flex';
        bottom.version.style.display='block';
        onSetHistoryControls();
    }

    function positionHdInfoPanel(){
        if(!isHdPresentationActive())return;
        if(!randomGalaxy.hdOverlay||!randomGalaxy.hdViewport||!randomGalaxy.hdScience)return;
        const overlayRect=randomGalaxy.hdOverlay.getBoundingClientRect();
        const navRect=bottom.nav.getBoundingClientRect();
        if(!overlayRect.height||!overlayRect.width)return;
        const safeBottom=Math.min(overlayRect.bottom-HD_LAYOUT.edge,navRect.top-24);

        if(!hdFixedViewportGeometry){
            const available=Math.max(1,safeBottom-overlayRect.top-HD_LAYOUT.edge-HD_LAYOUT.gap*2);
            const bannerTarget=overlayRect.height*HD_LAYOUT.bannerRatio;
            const bannerContentHeight=Math.max(1,Math.ceil(randomGalaxy.hdScience.scrollHeight));
            const viewportTargetWidth=Math.min(680,Math.max(1,overlayRect.width-20));
            const layoutScale=Math.min(1,available/Math.max(1,bannerTarget+viewportTargetWidth+165));
            const bannerHeight=Math.max(bannerContentHeight,Math.floor(bannerTarget*layoutScale));
            const screenWidth=Math.max(1,Math.floor(window.visualViewport?.width||window.innerWidth||overlayRect.width));
            const hardImageFloor=Math.min(viewportTargetWidth,Math.max(320,Math.floor(Math.min(screenWidth-28,overlayRect.width-20)*0.96)));
            const rawImageSide=Math.floor(Math.min(viewportTargetWidth*layoutScale,available-bannerHeight-165));
            const imageSide=Math.min(viewportTargetWidth,Math.max(hardImageFloor,rawImageSide));
            const scienceTop=HD_LAYOUT.edge;
            const imageTop=scienceTop+bannerHeight+HD_LAYOUT.gap;
            const infoTop=imageTop+imageSide+HD_LAYOUT.gap;

            hdFixedViewportGeometry=Object.freeze({
                bannerHeight,
                imageSide,
                scienceTop,
                imageTop,
                infoTop
            });
        }

        const {
            bannerHeight,
            imageSide,
            scienceTop,
            imageTop,
            infoTop
        }=hdFixedViewportGeometry;

        // AR129T HD GEOMETRY — preserve full square image; move info below it.
        // IMPORTANT: an imageSide identifier already exists earlier in this
        // function, so this block intentionally uses resolvedImageSide.
        const measuredPanelWidth=
            Number(randomGalaxy.hdScience?.getBoundingClientRect?.().width);

        const panelWidth=Math.max(
            1,
            Math.floor(
                Number.isFinite(measuredPanelWidth)&&measuredPanelWidth>0
                    ? measuredPanelWidth
                    : Math.min(680,Math.max(1,overlayRect.width-20))
            )
        );

        // Square means ASPECT RATIO only.  We do not change the established
        // rounded visual corners.
        const resolvedImageSide=panelWidth;

        // GALAXY INFO starts only after the full square image.
        const resolvedInfoTop=
            Math.ceil(imageTop+resolvedImageSide+HD_LAYOUT.gap);

        // Compute the lower GALAXY INFO height from its actual text content.
        // This keeps the banner only as tall as the title + wrapped info lines
        // + controls require, while never extending below safeBottom.
        const infoSafeBottom=overlayRect.bottom-HD_LAYOUT.edge;
        const availableInfoHeight=Math.max(
            1,
            Math.floor(
                infoSafeBottom-(overlayRect.top+resolvedInfoTop)
            )
        );

        const infoDestination=currentArchiveDestination();
        const infoText=infoDestination
            ? galaxyInfoText(infoDestination)
            : '';

        const infoStyle=getComputedStyle(hdInfoBody);
        const infoFontSize=parseFloat(infoStyle.fontSize)||10.5;
        const parsedLineHeight=parseFloat(infoStyle.lineHeight);
        const infoLineHeight=Number.isFinite(parsedLineHeight)
            ? parsedLineHeight
            : infoFontSize*1.45;
        const infoLetterSpacing=parseFloat(infoStyle.letterSpacing)||0;

        const infoCanvas=
            positionHdInfoPanel._infoCanvas ||
            (positionHdInfoPanel._infoCanvas=document.createElement('canvas'));
        const infoContext=infoCanvas.getContext('2d');
        infoContext.font=
            infoStyle.font ||
            `${infoStyle.fontWeight} ${infoStyle.fontSize} ${infoStyle.fontFamily}`;

        const infoTextWidth=Math.max(24,panelWidth-22);
        const infoWords=String(infoText||'').split(/\s+/).filter(Boolean);

        const measureInfo=value=>
            infoContext.measureText(value).width+
            Math.max(0,value.length-1)*infoLetterSpacing;

        let infoLineCount=0;
        let infoWordIndex=0;

        while(infoWordIndex<infoWords.length){
            let line='';
            while(infoWordIndex<infoWords.length){
                const proposed=line
                    ? `${line} ${infoWords[infoWordIndex]}`
                    : infoWords[infoWordIndex];

                if(line && measureInfo(proposed)>infoTextWidth)break;

                line=proposed;
                infoWordIndex++;
            }
            if(!line)break;
            infoLineCount++;
        }

        const infoTitle=document.getElementById('gv-hd-info-title');
        const titleHeight=Math.max(
            12,
            Math.ceil(infoTitle?.getBoundingClientRect?.().height||0)
        );
        const controlHeight=Math.max(
            40,
            Math.ceil(hdControlRow?.getBoundingClientRect?.().height||0)
        );

        // Existing panel CSS: 9 top padding + title + 6 title margin +
        // wrapped body lines + 14 no-write gap + controls + 10 bottom padding.
        const contentInfoHeight=Math.ceil(
            9+
            titleHeight+
            6+
            Math.max(1,infoLineCount)*infoLineHeight+
            14+
            controlHeight+
            10
        );

        const resolvedInfoHeight=Math.max(
            1,
            Math.min(180,availableInfoHeight)
        );

        const set=(element,name,value)=>
            element.style.setProperty(name,value,'important');

        // Same left/right width for top banner, image viewport, lower banner.
        set(randomGalaxy.hdScience,'width',`${panelWidth}px`);
        set(randomGalaxy.hdScience,'max-width',`${panelWidth}px`);
        set(randomGalaxy.hdScience,'top',`${scienceTop}px`);
        set(randomGalaxy.hdScience,'height',`${bannerHeight}px`);
        set(randomGalaxy.hdScience,'max-height',`${bannerHeight}px`);

        set(randomGalaxy.hdViewport,'top',`${imageTop}px`);
        set(randomGalaxy.hdViewport,'bottom','auto');
        set(randomGalaxy.hdViewport,'width',`${resolvedImageSide}px`);
        set(randomGalaxy.hdViewport,'max-width',`${resolvedImageSide}px`);
        set(randomGalaxy.hdViewport,'height',`${resolvedImageSide}px`);
        set(randomGalaxy.hdViewport,'max-height',`${resolvedImageSide}px`);

        set(hdInfoPanel,'width',`${panelWidth}px`);
        set(hdInfoPanel,'max-width',`${panelWidth}px`);
        set(hdInfoPanel,'top',`${resolvedInfoTop}px`);
        set(hdInfoPanel,'height',`${resolvedInfoHeight}px`);
        set(hdInfoPanel,'max-height',`${resolvedInfoHeight}px`);

        // Restore/populate the lower GALAXY INFO body.
        if(hdInfoBody){
            hdInfoBody.style.removeProperty('display');
            hdInfoBody.style.setProperty('visibility','visible','important');
            hdInfoBody.style.setProperty('opacity','1','important');
            hdInfoBody.style.setProperty('min-height','0','important');
        }

        try{
            const infoDestination=currentArchiveDestination();
            if(infoDestination)fitHdInfoText(infoDestination);
        }catch(error){
            console.error('GV HD GALAXY INFO RESTORE FAILURE',error);
        }

        randomGalaxy.hdOverlay.style.pointerEvents='none';
        randomGalaxy.hdViewport.style.pointerEvents='auto';
        hdInfoPanel.style.pointerEvents='none';
        hdControlRow.style.pointerEvents='none';
        hdControlRow.style.display='flex';
        hdControlRow.style.visibility='visible';
        hdControlRow.style.opacity='1';
        hdControlRow.style.zIndex='30';
        if(hdBackToSky){
            hdBackToSky.style.display='flex';
            hdBackToSky.style.visibility='visible';
            hdBackToSky.style.opacity='1';
            hdBackToSky.style.pointerEvents='auto';
            hdBackToSky.disabled=false;
        }
        if(hdDownloadButton){
            hdDownloadButton.style.display='flex';
            hdDownloadButton.style.visibility='visible';
            hdDownloadButton.style.opacity='1';
            hdDownloadButton.style.pointerEvents='auto';
        }
        hdArchiveButton.style.pointerEvents='auto';
        const viewerRoot=randomGalaxy.viewerRoot;
        if(!(viewerRoot instanceof Element))return;
        // AR129T HD: version label intentionally hidden on HD screen.
        // restoreNormalViewerPresentation() restores the normal-view label.
        bottom.version.style.display='none';
        bottom.version.style.top='';
        bottom.version.style.bottom='';
        randomGalaxy.hdOverlay.querySelectorAll('button,a').forEach(element=>{element.style.pointerEvents='auto'});
        fitHdInfoText();
    }

    function settleHdPresentation(){
        if(!isHdPresentationActive())return;
        syncHdProviderPresentation();
        applySmartHdCrop();
        positionHdInfoPanel();
        const row=document.getElementById('gv-hd-control-row');
        if(row)row.style.display='flex';
        const image=randomGalaxy.hdImage;
        if(image instanceof HTMLImageElement&&!image.complete)
            image.addEventListener('load',()=>{
                if(!isHdPresentationActive())return;
                applySmartHdCrop();
                positionHdInfoPanel();
                syncHdProviderPresentation();
                if(row)row.style.display='flex';
            },{once:true});
    }

    function reconcileViewerPresentation(){
        if(isHdPresentationActive())settleHdPresentation();
        else restoreNormalViewerPresentation();
    }

    const originalShowHD=randomGalaxy.showHD.bind(randomGalaxy);
    randomGalaxy.showHD=function(){
        try{document.body.classList.add('gv-hd-open')}catch(_){}
        const result=originalShowHD();

        // A blocked HD request returns null while navigation owns the
        // viewer. Do not schedule presentation work for a view that did
        // not open.
        if(result==null)return result;

        const destination=currentArchiveDestination();
        if(destination)preloadArchiveSource(destination);

        requestAnimationFrame(()=>
          requestAnimationFrame(settleHdPresentation)
        );

        return result;
    };
    const handleViewerResize=()=>requestAnimationFrame(reconcileViewerPresentation);
    const handleViewerPageShow=()=>requestAnimationFrame(reconcileViewerPresentation);
    window.addEventListener('resize',handleViewerResize);
    window.addEventListener('pageshow',handleViewerPageShow);
    syncHdProviderPresentation();


    return Object.freeze({
      ensureArchivePreloadQueue:
        () => ensureArchivePreloadQueue(),

      suspendArchivePreloads:
        () => suspendArchivePreloads(),

      resumeArchivePreloads:
        () => resumeArchivePreloads(),

      releaseActiveArchivePreload:
        () => releaseActiveArchivePreload(),

      syncHdProviderPresentation:
        destination => syncHdProviderPresentation(destination),

      destroy() {
        try {
          window.removeEventListener('resize',handleViewerResize);
        } catch (_) {}

        try {
          window.removeEventListener('pageshow',handleViewerPageShow);
        } catch (_) {}

        try {
          if (archiveRevealTimer)
            clearTimeout(archiveRevealTimer);
        } catch (_) {}

        try {
          archivePreloadController?.abort();
        } catch (_) {}

        try {
          archiveFrame.src='about:blank';
        } catch (_) {}

        try {
          archiveOverlay.remove();
        } catch (_) {}
      }
    });
  }


  // REQ-017A / ECO-026F-A
  // Random Galaxy 0062 owns the active preparation engine.
  function createRandomPreparationEngine(options = {}) {
    const ALADIN_URL=options.aladinUrl||'';
    const HOME=options.home||{};
    const galaxyCatalog=options.galaxyCatalog||[];
    const randomNavigationWindow=options.randomNavigationWindow||null;
    const aladin=options.aladin||null;
    const A=options.A||global.A;
    const ensureArchivePreloadQueue=
      options.ensureArchivePreloadQueue||(()=>{});
    const releaseActiveArchivePreload=
      options.releaseActiveArchivePreload||(()=>{});

    const PREFETCH_TARGET=10;
    const HISTORY_PREPARED_TARGET=10;
    const HEAVY_PREPARED_TARGET=5;
    const PREFETCH_MAX_WORKERS=3;
    const PREFETCH_PROBE_CONCURRENCY=3;
    const PREFETCH_HEALTH_INTERVAL_MS=30000;
    const ALADIN_PREWARM_DWELL_MS=1400;
    const ALADIN_PREWARM_INIT_TIMEOUT_MS=5000;
    const PREFETCH_RETRY_MS=5000;
    const HD_PREFERRED_MAX_BYTES=1024*1024;
    const FRAMING_SAMPLE_SIZE=96;
    const FRAMING_MAX_SHIFT_FRACTION=0.18;
    const prefetchReady=[];
    const prefetchQueued=[];
    const prefetchLoading=new Map();
    const prefetchControllers=new Map();
    const prefetchRetryAfter=new Map();
    const hdFramingPromises=new Map();
    const hdDownloadStatus=new Map();
    let prefetchFailedCount=0;
    let prefetchRetryTimer=0;
    let prefetchHealthTimer=0;
    let lastPrefetchHealth=Object.freeze({ready:0,loading:0,queued:0,total:0,activeKeys:Object.freeze([]),retryWait:Object.freeze([]),workers:Object.freeze([]),checkedAt:0});
    let priorityPrefetchDestination=null;
    let aladinPrefetchSerial=Promise.resolve();

    function runAladinTransaction(task){
        const run=aladinPrefetchSerial.then(task,task);
        aladinPrefetchSerial=run.catch(()=>null);
        return run;
    }

    let activePreparedItem=null;
    const historyPreparedItems=[];
    let activeTargetKey='';
    let backgroundWorkSuspended=false;
    let aladinPrewarm=null;
    let aladinPrewarmHost=null;
    let aladinPrewarmReady=null;
    let aladinPrewarmUnavailable=false;
    let aladinPrewarmTimer=0;
    let aladinPrewarmWaitResolve=null;
    let aladinPrewarmActiveKey='';
    let aladinPrewarmLastKey='';
        function setHdStatus(destination,state,sourceKind=''){
            const key=destinationKey(destination);
            if(!key)return;
            const old=hdDownloadStatus.get(key)||{};
            hdDownloadStatus.set(key,{key,name:String(destination?.name||old.name||''),state,sourceKind:sourceKind||old.sourceKind||'',updatedAt:Date.now()});
        }
        function getDownloadStatus(){
            return Object.freeze([...hdDownloadStatus.values()].map(item=>Object.freeze({...item})));
        }
        function suspendBackgroundWork(){
            if(backgroundWorkSuspended)return;
            backgroundWorkSuspended=true;
            const navigationState=randomNavigationWindow?.getState?.();
            const protectedAladinKey=destinationKey(navigationState?.pending?.destination||navigationState?.locked?.destination||navigationState?.locked||null);
            const preserveProtectedAladin=Boolean(
                protectedAladinKey&&
                aladinPrewarm&&
                aladinPrewarmHost&&
                aladinPrewarmLastKey===protectedAladinKey
            );
            if(aladinPrewarmTimer){clearTimeout(aladinPrewarmTimer);aladinPrewarmTimer=0}
            if(aladinPrewarmWaitResolve){const resolve=aladinPrewarmWaitResolve;aladinPrewarmWaitResolve=null;resolve(false)}
            aladinPrewarmActiveKey='';
            if(!preserveProtectedAladin){
                aladinPrewarm=null;
                aladinPrewarmReady=null;
                try{aladinPrewarmHost?.remove()}catch(_){}
                aladinPrewarmHost=null;
            }
            for(const controller of prefetchControllers.values())try{controller.abort()}catch(_){}
        }
        function resumeBackgroundWork(){
            if(!backgroundWorkSuspended)return;
            backgroundWorkSuspended=false;
            for(const item of prefetchReady){
                if(item?.framingState==='PREPARING'&&item?.image){
                    scheduleAladinEnhancement(item,item.destination,true);
                }
            }
            enforceHotPreparedWindow();
            const active=galaxyCatalog.find(item=>destinationKey(item)===activeTargetKey);
            const alreadyReady=Boolean(activePreparedItem?.key===activeTargetKey||prefetchReady.some(item=>item.key===activeTargetKey));
            if(active&&!alreadyReady)priorityPrefetchDestination=active;
            queueMicrotask(fillPrefetchQueue);
        }
        function destinationKey(destination){return String(destination?.archiveId||destination?.name||'').trim().toLowerCase()}
        function chooseGalaxy(catalog,excludeName=''){
            const excluded=String(excludeName||'').trim().toLowerCase();
            const available=catalog.filter(item=>item.name.toLowerCase()!==excluded&&destinationKey(item)!==activeTargetKey);
            if(!available.length)return null;
            return available[Math.floor(Math.random()*available.length)];
        }

        function releasePreparedItem(item){
            if(!item)return;
            try{if(item.image)item.image.src=''}catch(_){}
            try{if(item.objectUrl&&String(item.objectUrl).startsWith('blob:'))URL.revokeObjectURL(item.objectUrl)}catch(_){}
        }

        function futurePreparedDestinations(){
            const future=
                randomNavigationWindow?.getFuture?.() ||
                randomNavigationWindow?.getState?.().future ||
                [];
            return future
                .map(item=>item?.destination||item)
                .filter(Boolean);
        }

        function futurePreparedKeys(){
            return new Set(
                futurePreparedDestinations()
                    .map(destination=>destinationKey(destination))
                    .filter(Boolean)
            );
        }

        function preparedRetentionKeys(){
            const keys=futurePreparedKeys();

            // Navigation hotness is additional ownership, not a replacement
            // for the authoritative ten-destination future HD window.
            for(const key of (
                randomNavigationWindow?.hotKeys?.() ||
                randomNavigationWindow?.getState?.().hotKeys ||
                []
            )){
                const normalized=String(key||'').trim().toLowerCase();
                if(normalized)keys.add(normalized);
            }

            if(activeTargetKey)keys.add(activeTargetKey);
            return keys;
        }

        function enforceHotPreparedWindow(){
            const futureDestinations=futurePreparedDestinations();
            const futureKeys=new Set(
                futureDestinations
                    .map(destination=>destinationKey(destination))
                    .filter(Boolean)
            );

            const hotOrder=[
                ...(randomNavigationWindow?.hotKeys?.() ||
                   randomNavigationWindow?.getState?.().hotKeys ||
                   [])
            ];
            const hotKeys=new Set(hotOrder);
            const retainedKeys=new Set();

            // The active HD resource belongs to the current destination and
            // must not consume one of the ten future-HD ownership positions.
            if(activePreparedItem?.key)
                retainedKeys.add(activePreparedItem.key);

            // Preserve the existing small navigation/history cache policy.
            // History retention is independent of the ten future resources.
            for(let i=historyPreparedItems.length-1;i>=0;i--){
                const item=historyPreparedItems[i];
                const keep=Boolean(
                    item?.key&&
                    hotKeys.has(item.key)&&
                    !futureKeys.has(item.key)&&
                    !retainedKeys.has(item.key)
                );

                if(keep){
                    retainedKeys.add(item.key);
                    continue;
                }

                historyPreparedItems.splice(i,1);
                releasePreparedItem(item);
            }

            // Every record that remains in the authoritative future window
            // owns its decoded HD resource. Do not evict it because it falls
            // outside the five-hot navigation neighborhood.
            for(let i=prefetchReady.length-1;i>=0;i--){
                const item=prefetchReady[i];
                const keep=Boolean(
                    item?.key&&
                    futureKeys.has(item.key)&&
                    !retainedKeys.has(item.key)
                );

                if(keep){
                    retainedKeys.add(item.key);
                    continue;
                }

                prefetchReady.splice(i,1);
                releasePreparedItem(item);
                if(item?.destination)setHdStatus(item.destination,'QUEUED');
            }

            // Keep feeding all missing future HD destinations until the full
            // ten-slot future window is READY.
            for(const destination of futureDestinations){
                const key=destinationKey(destination);
                if(!key||
                   retainedKeys.has(key)||
                   prefetchLoading.has(key)||
                   prefetchQueued.some(candidate=>destinationKey(candidate)===key))
                    continue;

                enqueuePrefetch(destination,key===activeTargetKey);
            }

            // Preserve prior current/history hot preparation behavior without
            // allowing it to evict any future-HD resource.
            for(const key of hotOrder){
                if(!key||
                   futureKeys.has(key)||
                   retainedKeys.has(key)||
                   prefetchLoading.has(key)||
                   prefetchQueued.some(destination=>destinationKey(destination)===key))
                    continue;

                const destination=galaxyCatalog.find(item=>destinationKey(item)===key);
                if(destination)
                    enqueuePrefetch(destination,key===activeTargetKey);
            }
        }

        async function decodePreparedBlob(blob){
            const objectUrl=URL.createObjectURL(blob);
            const image=new Image();
            image.decoding='async';
            image.loading='eager';
            image.src=objectUrl;
            try{
                if(image.decode){
                    try{await image.decode()}catch(_){
                        if(!(image.complete&&image.naturalWidth))await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HD PRELOAD FAILED')),{once:true})});
                    }
                }else if(!(image.complete&&image.naturalWidth)){
                    await new Promise((resolve,reject)=>{image.addEventListener('load',resolve,{once:true});image.addEventListener('error',()=>reject(new Error('HD PRELOAD FAILED')),{once:true})});
                }
                if(!image.naturalWidth||!image.naturalHeight)throw new Error('HD PRELOAD DECODED WITHOUT IMAGE DIMENSIONS');
                return {image,objectUrl};
            }catch(error){
                image.src='';
                URL.revokeObjectURL(objectUrl);
                throw error;
            }
        }

        function hdVariantRank(url){
            const value=String(url||'').toLowerCase();
            if(value.includes('/publicationjpg/'))return 60;
            if(value.includes('/large/'))return 50;
            if(value.includes('/screen/'))return 40;
            if(value.includes('/wallpaper'))return 30;
            if(value.includes('/thumb700'))return 20;
            if(value.includes('/thumb300'))return 10;
            return 45;
        }

        function buildHdSourceCandidates(destination){
            const sources=[];
            const seen=new Set();
            const add=(url,kind,rank=hdVariantRank(url))=>{
                const validated=validHttpsUrl(url);
                const value=validated?.href||'';
                if(!value||seen.has(value))return;
                seen.add(value);sources.push({url:value,kind,rank});
            };
            const github=String(destination.githubImageUrl||'').trim();
            const archive=String(destination.hdUrl||'').trim();
            if(github)add(github,'GITHUB',55);
            if(archive){
                const provider=destination.provider||'ARCHIVE';
                const match=archive.match(/^(https:\/\/[^/]+\/archives\/images\/)([^/]+)(\/[^?#]+(?:\?[^#]*)?)$/i);
                if(match){
                    for(const variant of ['publicationjpg','large','screen','wallpaper1','thumb700x','thumb300y'])add(match[1]+variant+match[3],provider,hdVariantRank('/'+variant+'/'));
                }
                add(archive,provider);
            }
            return sources.sort((a,b)=>b.rank-a.rank);
        }

        async function probeHdSourceBytes(source,signal=null){
            try{
                const head=await fetch(source.url,{method:'HEAD',cache:'force-cache',signal});
                if(head.ok){
                    const length=Number(head.headers.get('content-length'));
                    if(Number.isFinite(length)&&length>0)return length;
                }
            }catch(error){if(error?.name==='AbortError')throw error}
            try{
                const probe=await fetch(source.url,{method:'GET',headers:{Range:'bytes=0-0'},cache:'force-cache',signal});
                if(!probe.ok&&probe.status!==206)return null;
                const range=String(probe.headers.get('content-range')||'');
                const total=Number(range.match(/\/(\d+)$/)?.[1]);
                const length=Number(probe.headers.get('content-length'));
                try{await probe.body?.cancel()}catch(_){}
                if(Number.isFinite(total)&&total>0)return total;
                if(probe.status===200&&Number.isFinite(length)&&length>0)return length;
            }catch(error){if(error?.name==='AbortError')throw error}
            return null;
        }

        async function mapWithConcurrency(items,limit,worker){
            const results=new Array(items.length);
            let next=0;
            const count=Math.max(1,Math.min(Number(limit)||1,items.length));
            await Promise.all(Array.from({length:count},async()=>{
                for(;;){
                    const index=next++;
                    if(index>=items.length)return;
                    results[index]=await worker(items[index],index);
                }
            }));
            return results;
        }

        async function orderHdSourcesBySize(destination,signal=null){
            const sources=buildHdSourceCandidates(destination);
            if(sources.length<2)return sources;
            const probed=await mapWithConcurrency(sources,PREFETCH_PROBE_CONCURRENCY,async source=>({...source,bytes:await probeHdSourceBytes(source,signal)}));
            const preferred=[];
            const oversized=[];
            const unknown=[];
            for(const source of probed){
                const bytes=source.bytes;
                if(Number.isFinite(bytes)&&bytes>0&&bytes<=HD_PREFERRED_MAX_BYTES)preferred.push(source);
                else if(Number.isFinite(bytes)&&bytes>HD_PREFERRED_MAX_BYTES)oversized.push(source);
                else unknown.push(source);
            }
            preferred.sort((a,b)=>b.rank-a.rank||b.bytes-a.bytes);
            oversized.sort((a,b)=>a.bytes-b.bytes||a.rank-b.rank);
            unknown.sort((a,b)=>a.rank-b.rank);
            return [...preferred,...oversized,...unknown];
        }

        async function loadPreparedImageDirect(url,signal=null){
            const image=new Image();
            image.decoding='async';
            return await new Promise((resolve,reject)=>{
                let settled=false;
                const finish=(error=null)=>{
                    if(settled)return;
                    settled=true;
                    image.onload=null;
                    image.onerror=null;
                    if(signal)signal.removeEventListener('abort',onAbort);
                    if(error)reject(error);
                    else resolve({image,objectUrl:url});
                };
                const onAbort=()=>finish(new DOMException('HD PRELOAD SUSPENDED','AbortError'));
                image.onload=()=>image.complete&&image.naturalWidth
                    ? finish()
                    : finish(new Error('HD DIRECT IMAGE LOAD EMPTY'));
                image.onerror=()=>finish(new Error('HD DIRECT IMAGE LOAD FAILED'));
                if(signal?.aborted)return onAbort();
                if(signal)signal.addEventListener('abort',onAbort,{once:true});
                image.src=url;
            });
        }

        async function prepareHdDestinationFetch(destination,signal=null){
            const sources=await orderHdSourcesBySize(destination,signal);
            let lastError=null;
            for(const source of sources){
                try{
                    setHdStatus(destination,'DOWNLOADING',source.kind);
                    const response=await fetch(source.url,{cache:'force-cache',signal});
                    if(!response.ok)throw new Error('HD PRELOAD RETURNED HTTP '+response.status);
                    const blob=await response.blob();
                    if(signal?.aborted)throw new DOMException('HD PRELOAD SUSPENDED','AbortError');
                    setHdStatus(destination,'DECODING',source.kind);
                    const prepared=await decodePreparedBlob(blob);
                    setHdStatus(destination,'READY',source.kind);
                    return {key:destinationKey(destination),destination,image:prepared.image,objectUrl:prepared.objectUrl,sourceUrl:source.url,sourceKind:source.kind};
                }catch(error){
                    if(error?.name==='AbortError'){setHdStatus(destination,'SUSPENDED',source.kind);throw error}
                    lastError=error;
                    try{
                        setHdStatus(destination,'DECODING',source.kind);
                        const prepared=await loadPreparedImageDirect(source.url,signal);
                        setHdStatus(destination,'READY',source.kind);
                        return {key:destinationKey(destination),destination,image:prepared.image,objectUrl:prepared.objectUrl,sourceUrl:source.url,sourceKind:source.kind};
                    }catch(directError){
                        if(directError?.name==='AbortError'){setHdStatus(destination,'SUSPENDED',source.kind);throw directError}
                        lastError=directError;
                    }
                }
            }
            setHdStatus(destination,'RETRY-WAIT');
            throw lastError||new Error('HD PRELOAD HAS NO USABLE SOURCE');
        }
        // AR129T HD PREFETCH RECOVERY V2
        // Preferred path: existing fetch/blob loader.
        // Recovery path: direct Image load, which still downloads/caches the
        // asset but is not dependent on fetch/CORS behavior.
        async function prepareHdDestination(destination,signal=null){
            try{
                return await prepareHdDestinationFetch(destination,signal);
            }catch(fetchError){
                if(fetchError?.name==='AbortError')throw fetchError;

                const sources=buildHdSourceCandidates(destination);
                let lastError=fetchError;

                const decodeDirect=(url)=>new Promise((resolve,reject)=>{
                    const image=new Image();
                    image.decoding='async';
                    image.loading='eager';

                    let settled=false;
                    const cleanup=()=>{
                        image.onload=null;
                        image.onerror=null;
                        try{signal?.removeEventListener?.('abort',onAbort)}catch(_){}
                    };
                    const finish=(fn,value)=>{
                        if(settled)return;
                        settled=true;
                        cleanup();
                        fn(value);
                    };
                    const onAbort=()=>{
                        try{image.src=''}catch(_){}
                        finish(
                            reject,
                            typeof abortError==='function'
                                ? abortError('HD DIRECT PRELOAD ABORTED')
                                : new DOMException('HD DIRECT PRELOAD ABORTED','AbortError')
                        );
                    };

                    if(signal?.aborted){
                        onAbort();
                        return;
                    }

                    try{signal?.addEventListener?.('abort',onAbort,{once:true})}catch(_){}

                    image.onload=()=>{
                        if(!image.naturalWidth||!image.naturalHeight){
                            finish(reject,new Error('HD DIRECT PRELOAD HAS ZERO IMAGE DIMENSIONS'));
                            return;
                        }
                        finish(resolve,image);
                    };

                    image.onerror=()=>finish(
                        reject,
                        new Error('HD DIRECT IMAGE PRELOAD FAILED')
                    );

                    image.src=String(url||'');
                });

                for(const source of sources){
                    try{
                        if(signal?.aborted){
                            throw (
                                typeof abortError==='function'
                                    ? abortError('HD DIRECT PRELOAD ABORTED')
                                    : new DOMException('HD DIRECT PRELOAD ABORTED','AbortError')
                            );
                        }

                        setHdStatus(destination,'DOWNLOADING',source.kind||'DIRECT');
                        const image=await decodeDirect(source.url);

                        const item={
                            key:destinationKey(destination),
                            destination,
                            image,
                            objectUrl:String(source.url||''),
                            sourceUrl:String(source.url||''),
                            sourceKind:source.kind||'DIRECT',
                            directUrl:true
                        };

                        setHdStatus(destination,'READY',item.sourceKind);
                        return item;
                    }catch(error){
                        if(error?.name==='AbortError')throw error;
                        lastError=error;
                    }
                }

                console.warn(
                    'GALAXY VIEWER HD PREFETCH FETCH+DIRECT FAILURE',
                    destinationKey(destination),
                    lastError
                );
                throw lastError;
            }
        }


        function ensureAladinPrewarm(){
            if(backgroundWorkSuspended)return Promise.resolve(null);
            if(aladinPrewarmReady)return aladinPrewarmReady;
            aladinPrewarmReady=new Promise((resolve,reject)=>{
                let settled=false;
                let initTimeout=0;
                const finish=(callback,value)=>{
                    if(settled)return;
                    settled=true;
                    if(initTimeout){clearTimeout(initTimeout);initTimeout=0}
                    callback(value);
                };
                const frame=document.createElement('iframe');
                aladinPrewarmHost=frame;
                frame.id='gv-aladin-prewarm-frame';
                frame.setAttribute('aria-hidden','true');
                frame.tabIndex=-1;
                Object.assign(frame.style,{position:'fixed',left:'-10000px',top:'0',width:'512px',height:'512px',border:'0',opacity:'0',pointerEvents:'none',overflow:'hidden'});
                frame.srcdoc=`<!doctype html><html><head><link rel="stylesheet" href="https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.min.css"><style>html,body,#gv-prewarm{margin:0;width:512px;height:512px;overflow:hidden;background:#000}</style></head><body><div id="gv-prewarm"></div><script src="${ALADIN_URL}"><\/script></body></html>`;
                initTimeout=setTimeout(()=>finish(reject,new Error('ISOLATED ALADIN PREWARM INITIALIZATION TIMED OUT')),ALADIN_PREWARM_INIT_TIMEOUT_MS);
                frame.addEventListener('load',async()=>{
                    try{
                        if(backgroundWorkSuspended){finish(resolve,null);return}
                        const win=frame.contentWindow;
                        if(!win?.A?.init)throw new Error('ISOLATED ALADIN PREWARM EXPORT MISSING');
                        await win.A.init;
                        if(settled)return;
                        if(backgroundWorkSuspended){finish(resolve,null);return}
                        aladinPrewarm=win.A.aladin('#gv-prewarm',{
                            target:`${HOME.ra} ${HOME.dec}`,
                            survey:'P/DSS2/color',
                            fov:1,
                            projection:'MOL',
                            cooFrame:'ICRSd',
                            showReticle:false,
                            showZoomControl:false,
                            showFullscreenControl:false,
                            showLayersControl:false,
                            showGotoControl:false,
                            showCooGridControl:false,
                            showSettingsControl:false,
                            showSelectionModeControl:false,
                            showColorPickerControl:false,
                            showShareControl:false,
                            showSimbadPointerControl:false,
                            showProjectionControl:false,
                            showStatusBar:false,
                            showFrame:false,
                            showFov:false,
                            showCooLocation:false,
                            showContextMenu:false,
                            showCatalog:false,
                            showCooGrid:false
                        });
                        if(typeof aladinPrewarm.setFrame==='function')aladinPrewarm.setFrame('ICRSd');
                        if(typeof aladinPrewarm.setProjection==='function')aladinPrewarm.setProjection('MOL');
                        aladinPrewarmUnavailable=false;
                        finish(resolve,aladinPrewarm);
                    }catch(error){finish(reject,error)}
                },{once:true});
                frame.addEventListener('error',()=>finish(reject,new Error('ISOLATED ALADIN PREWARM FRAME FAILED TO LOAD')),{once:true});
                document.body.appendChild(frame);
            }).catch(error=>{
                console.warn('GALAXY VIEWER ISOLATED ALADIN PREWARM WARNING',error);
                aladinPrewarmUnavailable=true;
                aladinPrewarmReady=null;
                aladinPrewarm=null;
                try{aladinPrewarmHost?.remove()}catch(_){}
                aladinPrewarmHost=null;
                return null;
            });
            return aladinPrewarmReady;
        }

        function abortError(message='BACKGROUND PREPARATION SUSPENDED'){return new DOMException(message,'AbortError')}

        function avmAuthorityUrlFor(destination){
            for(const value of [
                destination?.avmSourceUrl,
                destination?.selectedImageUrl,
                destination?.screenUrl,
                destination?.hdUrl,
                destination?.largeUrl
            ]){
                const url=validHttpsUrl(value);
                if(url)return url.href;
            }
            return '';
        }

        function avmImageFormat(url){
            return /\\.png(?:[?#]|$)/i.test(String(url||''))?'png':'jpeg';
        }

        function normalizeAvmCameraRotation(value){
            let angle=Number(value);
            if(!Number.isFinite(angle))return null;
            angle=((angle+180)%360+360)%360-180;
            if(angle>90)angle-=180;
            if(angle<=-90)angle+=180;
            return angle;
        }

        function avmRawRotationFromWcs(wcs){
            const crota=Number(wcs?.CROTA2);
            if(Number.isFinite(crota))return crota;

            const cd12=Number(wcs?.CD1_2),cd22=Number(wcs?.CD2_2);
            if(Number.isFinite(cd12)&&Number.isFinite(cd22)&&(cd12!==0||cd22!==0))
                return Math.atan2(cd12,cd22)*180/Math.PI;

            const pc12=Number(wcs?.PC1_2),pc22=Number(wcs?.PC2_2);
            const cdelt1=Number(wcs?.CDELT1),cdelt2=Number(wcs?.CDELT2);
            if(
                Number.isFinite(pc12)&&Number.isFinite(pc22)&&
                Number.isFinite(cdelt1)&&Number.isFinite(cdelt2)
            ){
                const east=cdelt1*pc12;
                const north=cdelt2*pc22;
                if(east!==0||north!==0)
                    return Math.atan2(east,north)*180/Math.PI;
            }
            return null;
        }

        function avmVerticalFovFromWcs(wcs,callbackFov){
            const h=Number(wcs?.NAXIS2);
            if(Number.isFinite(h)&&h>0){
                const cd12=Number(wcs?.CD1_2),cd22=Number(wcs?.CD2_2);
                if(Number.isFinite(cd12)&&Number.isFinite(cd22)){
                    const perPixel=Math.hypot(cd12,cd22);
                    if(Number.isFinite(perPixel)&&perPixel>0)return perPixel*h;
                }

                const cdelt2=Number(wcs?.CDELT2);
                if(Number.isFinite(cdelt2)&&cdelt2!==0)return Math.abs(cdelt2)*h;

                const pc12=Number(wcs?.PC1_2),pc22=Number(wcs?.PC2_2);
                const cdelt1=Number(wcs?.CDELT1);
                if(
                    Number.isFinite(pc12)&&Number.isFinite(pc22)&&
                    Number.isFinite(cdelt1)&&Number.isFinite(cdelt2)
                ){
                    const perPixel=Math.hypot(cdelt1*pc12,cdelt2*pc22);
                    if(Number.isFinite(perPixel)&&perPixel>0)return perPixel*h;
                }
            }

            // Still runtime AVM/WCS authority: Aladin computed this callback
            // FoV from the image WCS. Deliberately no JSON fallback.
            const callback=Number(callbackFov);
            return Number.isFinite(callback)&&callback>0?callback:null;
        }

        function avmHorizontalFovFromWcs(wcs,callbackFov){
            const w=Number(wcs?.NAXIS1);
            if(Number.isFinite(w)&&w>0){
                const cd11=Number(wcs?.CD1_1),cd21=Number(wcs?.CD2_1);
                if(Number.isFinite(cd11)&&Number.isFinite(cd21)){
                    const perPixel=Math.hypot(cd11,cd21);
                    if(Number.isFinite(perPixel)&&perPixel>0)return perPixel*w;
                }

                const cdelt1=Number(wcs?.CDELT1);
                if(Number.isFinite(cdelt1)&&cdelt1!==0)return Math.abs(cdelt1)*w;

                const pc11=Number(wcs?.PC1_1),pc21=Number(wcs?.PC2_1);
                const cdelt2=Number(wcs?.CDELT2);
                if(
                    Number.isFinite(pc11)&&Number.isFinite(pc21)&&
                    Number.isFinite(cdelt1)&&Number.isFinite(cdelt2)
                ){
                    const perPixel=Math.hypot(cdelt1*pc11,cdelt2*pc21);
                    if(Number.isFinite(perPixel)&&perPixel>0)return perPixel*w;
                }
            }

            const callback=Number(callbackFov);
            return Number.isFinite(callback)&&callback>0?callback:null;
        }

        async function prepareRuntimeAvmAuthority(destination){
            if(backgroundWorkSuspended)throw abortError();

            const key=destinationKey(destination);
            const url=avmAuthorityUrlFor(destination);
            if(!key)throw new Error('AVM AUTHORITY DESTINATION KEY MISSING');
            if(!url)throw new Error('AVM AUTHORITY IMAGE URL MISSING');

            const isolated=await ensureAladinPrewarm();
            if(backgroundWorkSuspended||!isolated)throw abortError();

            const A=aladinPrewarmHost?.contentWindow?.A;
            if(!A?.image)throw new Error('ISOLATED ALADIN A.image EXPORT MISSING');

            const layerName='GV AVM AUTHORITY PREFETCH';
            try{
                if(typeof isolated.removeOverlayImageLayer==='function')
                    isolated.removeOverlayImageLayer(layerName);
            }catch(_){}

            return await new Promise((resolve,reject)=>{
                let settled=false;
                const timeout=setTimeout(
                    ()=>finish(new Error('RUNTIME AVM AUTHORITY PREFETCH TIMED OUT')),
                    20000
                );

                const finish=(error,value)=>{
                    if(settled)return;
                    settled=true;
                    clearTimeout(timeout);
                    try{
                        if(typeof isolated.removeOverlayImageLayer==='function')
                            isolated.removeOverlayImageLayer(layerName);
                    }catch(_){}
                    if(error)reject(error);else resolve(value);
                };

                try{
                    const layer=A.image(url,{
                        name:layerName,
                        imgFormat:avmImageFormat(url),
                        opacity:.01,
                        successCallback:(ra,dec,fov,image)=>{
                            try{
                                if(backgroundWorkSuspended)
                                    return finish(abortError());

                                const avmRa=Number(ra);
                                const avmDec=Number(dec);
                                const callbackFovValues=
                                    (Array.isArray(fov)?fov:[fov])
                                        .map(Number)
                                        .filter(value=>Number.isFinite(value)&&value>0);
                                const callbackFov=callbackFovValues.length
                                    ? Math.max(...callbackFovValues)
                                    : null;
                                const wcs=image?.options?.wcs||{};
                                const rawRotation=avmRawRotationFromWcs(wcs);
                                const cameraRotation=normalizeAvmCameraRotation(rawRotation);
                                const horizontalFov=avmHorizontalFovFromWcs(wcs,callbackFov);
                                const verticalFov=avmVerticalFovFromWcs(wcs,callbackFov);

                                if(!Number.isFinite(avmRa)||avmRa<0||avmRa>=360)
                                    throw new Error('RUNTIME AVM RA INVALID');
                                if(!Number.isFinite(avmDec)||avmDec<-90||avmDec>90)
                                    throw new Error('RUNTIME AVM DEC INVALID');
                                if(!Number.isFinite(horizontalFov)||horizontalFov<=0)
                                    throw new Error('RUNTIME AVM HORIZONTAL FoV INVALID');
                                if(!Number.isFinite(verticalFov)||verticalFov<=0)
                                    throw new Error('RUNTIME AVM VERTICAL FoV INVALID');
                                if(!Number.isFinite(rawRotation)||!Number.isFinite(cameraRotation))
                                    throw new Error('RUNTIME AVM ROTATION INVALID');

                                const prepared=Object.freeze({
                                    ...destination,
                                    ra:avmRa,
                                    dec:avmDec,
                                    fovDegrees:verticalFov,
                                    aladinRotation:cameraRotation,
                                    avmRa,
                                    avmDec,
                                    avmHorizontalFovDegrees:horizontalFov,
                                    avmVerticalFovDegrees:verticalFov,
                                    avmCallbackFov:
                                        Number.isFinite(callbackFov)&&callbackFov>0
                                            ? callbackFov
                                            : null,
                                    avmRotation:rawRotation,
                                    avmCameraRotation:cameraRotation,
                                    avmAuthorityUrl:url,
                                    avmAuthority:'RUNTIME_IMAGE_AVM',
                                    // AR119: preserve the complete WCS generated by
                                    // Aladin from the real AVM image. The visible
                                    // viewer receives this exact registration so it
                                    // never has to parse AVM metadata a second time.
                                    avmAuthorityWcs:Object.freeze(
                                        Object.fromEntries(
                                            Object.entries(wcs)
                                                .filter(([,value])=>
                                                    value!==undefined&&
                                                    value!==null&&
                                                    (
                                                        typeof value==='string'||
                                                        typeof value==='number'||
                                                        typeof value==='boolean'
                                                    )
                                                )
                                        )
                                    )
                                });

                                GV_TRACE.enabled&&gvTrace(11801,'AR118_RUNTIME_AVM_AUTHORITY',{
                                    key,
                                    name:String(destination?.name||''),
                                    url,
                                    catalogIgnored:{
                                        ra:destination?.ra,
                                        dec:destination?.dec,
                                        fovDegrees:destination?.fovDegrees,
                                        aladinRotation:destination?.aladinRotation
                                    },
                                    runtime:{
                                        ra:prepared.ra,
                                        dec:prepared.dec,
                                        horizontalFov:prepared.avmHorizontalFovDegrees,
                                        verticalFov:prepared.fovDegrees,
                                        callbackFov:prepared.avmCallbackFov,
                                        avmRotation:prepared.avmRotation,
                                        cameraRotation:prepared.aladinRotation
                                    }
                                });
                                finish(null,prepared);
                            }catch(error){
                                finish(error);
                            }
                        },
                        errorCallback:error=>finish(
                            error instanceof Error
                                ? error
                                : new Error(String(error||'RUNTIME AVM IMAGE LOAD FAILED'))
                        )
                    });
                    isolated.setOverlayImageLayer(layer,layerName);
                }catch(error){
                    finish(error);
                }
            });
        }

        function imageLightProfile(source){
            if(!source)return null;
            try{
                const canvas=document.createElement('canvas');
                canvas.width=FRAMING_SAMPLE_SIZE;canvas.height=FRAMING_SAMPLE_SIZE;
                const ctx=canvas.getContext('2d',{willReadFrequently:true});
                if(!ctx)return null;
                ctx.filter='blur(2px)';
                ctx.drawImage(source,0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE);
                const data=ctx.getImageData(0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE).data;
                const lum=[];
                for(let i=0;i<data.length;i+=4)lum.push(.2126*data[i]+.7152*data[i+1]+.0722*data[i+2]);
                const sorted=[...lum].sort((a,b)=>a-b);
                const background=sorted[Math.floor(sorted.length*.45)]||0;
                const threshold=sorted[Math.floor(sorted.length*.78)]||background;
                let sum=0,sx=0,sy=0;
                const weights=new Float64Array(lum.length);
                for(let y=0;y<FRAMING_SAMPLE_SIZE;y++)for(let x=0;x<FRAMING_SAMPLE_SIZE;x++){
                    const index=y*FRAMING_SAMPLE_SIZE+x;
                    const edge=Math.min(x,y,FRAMING_SAMPLE_SIZE-1-x,FRAMING_SAMPLE_SIZE-1-y);
                    const edgeFactor=clamp(edge/(FRAMING_SAMPLE_SIZE*.08),0,1);
                    const weight=Math.max(0,lum[index]-Math.max(background,threshold*.82))*edgeFactor;
                    weights[index]=weight;sum+=weight;sx+=weight*x;sy+=weight*y;
                }
                if(!(sum>1))return null;
                const cx=sx/sum,cy=sy/sum;
                let xx=0,yy=0,xy=0;
                for(let y=0;y<FRAMING_SAMPLE_SIZE;y++)for(let x=0;x<FRAMING_SAMPLE_SIZE;x++){
                    const weight=weights[y*FRAMING_SAMPLE_SIZE+x];if(!weight)continue;
                    const dx=x-cx,dy=y-cy;xx+=weight*dx*dx;yy+=weight*dy*dy;xy+=weight*dx*dy;
                }
                xx/=sum;yy/=sum;xy/=sum;
                const trace=xx+yy,disc=Math.sqrt(Math.max(0,(xx-yy)*(xx-yy)+4*xy*xy));
                const major=(trace+disc)/2,minor=(trace-disc)/2;
                const eccentricity=major>0?clamp(1-Math.max(0,minor)/major,0,1):0;
                const angle=.5*Math.atan2(2*xy,xx-yy)*180/Math.PI;
                const majorSigma=Math.sqrt(Math.max(0,major));
                const minorSigma=Math.sqrt(Math.max(0,minor));
                const scale=Math.max(majorSigma,minorSigma);
                return {x:cx,y:cy,angle,eccentricity,weight:sum,majorSigma,minorSigma,scale};
            }catch(_){return null}
        }

        function normalizeFullRotationDelta(value){
            let angle=Number(value)||0;
            while(angle>180)angle-=360;
            while(angle<=-180)angle+=360;
            return angle;
        }

        function alignHalfTurnToReference(axisDelta,referenceDelta){
            let angle=Number(axisDelta)||0;
            const reference=Number(referenceDelta)||0;
            while(angle-reference>90)angle-=180;
            while(angle-reference<-90)angle+=180;
            return angle;
        }

        function imagePointSources(source){
            if(!source)return [];
            try{
                const canvas=document.createElement('canvas');
                canvas.width=FRAMING_SAMPLE_SIZE;
                canvas.height=FRAMING_SAMPLE_SIZE;
                const ctx=canvas.getContext('2d',{willReadFrequently:true});
                if(!ctx)return [];
                ctx.drawImage(source,0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE);
                const data=ctx.getImageData(0,0,FRAMING_SAMPLE_SIZE,FRAMING_SAMPLE_SIZE).data;
                const lum=new Float64Array(FRAMING_SAMPLE_SIZE*FRAMING_SAMPLE_SIZE);
                for(let i=0,j=0;i<data.length;i+=4,j++)
                    lum[j]=.2126*data[i]+.7152*data[i+1]+.0722*data[i+2];

                const sorted=Array.from(lum).sort((a,b)=>a-b);
                const background=sorted[Math.floor(sorted.length*.50)]||0;
                const threshold=Math.max(
                    sorted[Math.floor(sorted.length*.92)]||background,
                    background+8
                );
                const candidates=[];

                for(let y=3;y<FRAMING_SAMPLE_SIZE-3;y++){
                    for(let x=3;x<FRAMING_SAMPLE_SIZE-3;x++){
                        const index=y*FRAMING_SAMPLE_SIZE+x;
                        const peak=lum[index];
                        if(peak<threshold)continue;

                        let localMaximum=true;
                        for(let dy=-1;dy<=1&&localMaximum;dy++){
                            for(let dx=-1;dx<=1;dx++){
                                if(!dx&&!dy)continue;
                                if(lum[(y+dy)*FRAMING_SAMPLE_SIZE+x+dx]>peak){
                                    localMaximum=false;
                                    break;
                                }
                            }
                        }
                        if(!localMaximum)continue;

                        let ring=0,ringCount=0;
                        for(let dy=-3;dy<=3;dy++)for(let dx=-3;dx<=3;dx++){
                            const r2=dx*dx+dy*dy;
                            if(r2>=4&&r2<=9){
                                ring+=lum[(y+dy)*FRAMING_SAMPLE_SIZE+x+dx];
                                ringCount++;
                            }
                        }
                        const ringMean=ringCount?ring/ringCount:background;
                        const contrast=peak-ringMean;
                        if(contrast<Math.max(4,(threshold-background)*.20))continue;

                        let weight=0,wx=0,wy=0;
                        for(let dy=-1;dy<=1;dy++)for(let dx=-1;dx<=1;dx++){
                            const value=Math.max(
                                0,
                                lum[(y+dy)*FRAMING_SAMPLE_SIZE+x+dx]-background
                            );
                            weight+=value;
                            wx+=value*(x+dx);
                            wy+=value*(y+dy);
                        }
                        if(!(weight>0))continue;
                        candidates.push({
                            x:wx/weight,
                            y:wy/weight,
                            strength:contrast*Math.sqrt(Math.max(1,peak-background))
                        });
                    }
                }

                candidates.sort((a,b)=>b.strength-a.strength);
                const selected=[];
                for(const candidate of candidates){
                    if(selected.some(point=>
                        Math.hypot(point.x-candidate.x,point.y-candidate.y)<5
                    ))continue;
                    selected.push(candidate);
                    if(selected.length>=12)break;
                }
                return selected;
            }catch(_){
                return [];
            }
        }

        function fitPointRegistration(sourcePoints,skyPoints){
            const source=(sourcePoints||[]).slice(0,10);
            const sky=(skyPoints||[]).slice(0,12);
            if(source.length<3||sky.length<3)return null;

            const inlierLimit=4.5;

            const evaluate=(scale,theta,tx,ty)=>{
                if(!Number.isFinite(scale)||scale<.35||scale>3)return null;
                const cos=Math.cos(theta),sin=Math.sin(theta);
                const used=new Set();
                const matches=[];
                let error2=0;

                for(const point of source){
                    const px=scale*(cos*point.x-sin*point.y)+tx;
                    const py=scale*(sin*point.x+cos*point.y)+ty;
                    let bestIndex=-1,bestDistance=Infinity;
                    for(let index=0;index<sky.length;index++){
                        if(used.has(index))continue;
                        const distance=Math.hypot(
                            sky[index].x-px,
                            sky[index].y-py
                        );
                        if(distance<bestDistance){
                            bestDistance=distance;
                            bestIndex=index;
                        }
                    }
                    if(bestIndex>=0&&bestDistance<=inlierLimit){
                        used.add(bestIndex);
                        matches.push({
                            source:point,
                            sky:sky[bestIndex],
                            distance:bestDistance
                        });
                        error2+=bestDistance*bestDistance;
                    }
                }

                if(matches.length<3)return null;
                const xs=matches.map(match=>match.source.x);
                const ys=matches.map(match=>match.source.y);
                const spread=Math.hypot(
                    Math.max(...xs)-Math.min(...xs),
                    Math.max(...ys)-Math.min(...ys)
                )/FRAMING_SAMPLE_SIZE;
                const rms=Math.sqrt(error2/matches.length);
                return {scale,theta,tx,ty,matches,rms,spread};
            };

            const refine=matches=>{
                if(!matches||matches.length<3)return null;
                const n=matches.length;
                let sx=0,sy=0,kx=0,ky=0;
                for(const match of matches){
                    sx+=match.source.x;sy+=match.source.y;
                    kx+=match.sky.x;ky+=match.sky.y;
                }
                sx/=n;sy/=n;kx/=n;ky/=n;

                let a=0,b=0,denominator=0;
                for(const match of matches){
                    const px=match.source.x-sx;
                    const py=match.source.y-sy;
                    const qx=match.sky.x-kx;
                    const qy=match.sky.y-ky;
                    a+=px*qx+py*qy;
                    b+=px*qy-py*qx;
                    denominator+=px*px+py*py;
                }
                if(!(denominator>1e-9))return null;
                const scale=Math.hypot(a,b)/denominator;
                const theta=Math.atan2(b,a);
                const cos=Math.cos(theta),sin=Math.sin(theta);
                const tx=kx-scale*(cos*sx-sin*sy);
                const ty=ky-scale*(sin*sx+cos*sy);
                return evaluate(scale,theta,tx,ty);
            };

            let best=null;
            for(let i=0;i<source.length-1;i++){
                for(let j=i+1;j<source.length;j++){
                    const sx=source[j].x-source[i].x;
                    const sy=source[j].y-source[i].y;
                    const sourceDistance=Math.hypot(sx,sy);
                    if(sourceDistance<7)continue;
                    const sourceAngle=Math.atan2(sy,sx);

                    for(let k=0;k<sky.length-1;k++){
                        for(let l=k+1;l<sky.length;l++){
                            for(let flip=0;flip<2;flip++){
                                const first=flip?sky[l]:sky[k];
                                const second=flip?sky[k]:sky[l];
                                const dx=second.x-first.x;
                                const dy=second.y-first.y;
                                const skyDistance=Math.hypot(dx,dy);
                                if(skyDistance<7)continue;

                                const scale=skyDistance/sourceDistance;
                                if(scale<.35||scale>3)continue;
                                const theta=Math.atan2(dy,dx)-sourceAngle;
                                const cos=Math.cos(theta),sin=Math.sin(theta);
                                const tx=
                                    first.x-
                                    scale*(cos*source[i].x-sin*source[i].y);
                                const ty=
                                    first.y-
                                    scale*(sin*source[i].x+cos*source[i].y);

                                const candidate=evaluate(scale,theta,tx,ty);
                                if(!candidate)continue;
                                if(
                                    !best||
                                    candidate.matches.length>best.matches.length||
                                    (
                                        candidate.matches.length===best.matches.length&&
                                        (
                                            candidate.rms<best.rms-.05||
                                            (
                                                Math.abs(candidate.rms-best.rms)<=.05&&
                                                candidate.spread>best.spread
                                            )
                                        )
                                    )
                                )best=candidate;
                            }
                        }
                    }
                }
            }

            if(!best)return null;
            best=refine(best.matches)||best;
            best=refine(best.matches)||best;

            const inliers=best.matches.length;
            const high=
                inliers>=4&&
                best.rms<=3.5&&
                best.spread>=.25;
            const medium=
                inliers>=3&&
                best.rms<=2.75&&
                best.spread>=.18;

            if(!high&&!medium)return null;

            const center=(FRAMING_SAMPLE_SIZE-1)/2;
            const cos=Math.cos(best.theta),sin=Math.sin(best.theta);
            const mappedCenterX=
                best.scale*(cos*center-sin*center)+best.tx;
            const mappedCenterY=
                best.scale*(sin*center+cos*center)+best.ty;

            return Object.freeze({
                inliers,
                rms:best.rms,
                spread:best.spread,
                scaleRatio:best.scale,
                rotationDelta:normalizeFullRotationDelta(
                    -best.theta*180/Math.PI
                ),
                mappedCenterX,
                mappedCenterY,
                confidence:high?'HIGH':'MEDIUM'
            });
        }

        function normalizeSignedAngle(value){
            let angle=Number(value)||0;
            while(angle>90)angle-=180;
            while(angle<-90)angle+=180;
            return angle;
        }

        function angularSeparationDegrees(ra1,dec1,ra2,dec2){
            const d=Math.PI/180;
            const a1=ra1*d,a2=ra2*d,b1=dec1*d,b2=dec2*d;
            const cosine=Math.sin(b1)*Math.sin(b2)+Math.cos(b1)*Math.cos(b2)*Math.cos(a1-a2);
            return Math.acos(clamp(cosine,-1,1))/d;
        }

        function deriveSourceFraming(destination,sourceImage){
            if(!sourceImage?.naturalWidth||!sourceImage?.naturalHeight||!aladinPrewarm||!aladinPrewarmHost)return destination;
            try{
                const skyCanvas=aladinPrewarmHost.contentDocument?.querySelector('canvas');
                if(!skyCanvas)return destination;

                // Independent registration signals. Neither estimator mutates
                // the visible Viewer; only the fused destination is exported.
                const sourceImageProfile=imageLightProfile(sourceImage);
                const skyProfile=imageLightProfile(skyCanvas);
                const sourcePoints=imagePointSources(sourceImage);
                const skyPoints=imagePointSources(skyCanvas);
                const pointFit=fitPointRegistration(sourcePoints,skyPoints);

                if(!sourceImageProfile||!skyProfile)return destination;

                const width=skyCanvas.clientWidth||skyCanvas.width||512;
                const height=skyCanvas.clientHeight||skyCanvas.height||512;
                const sampleCenter=(FRAMING_SAMPLE_SIZE-1)/2;

                const morphologyOffsetX=
                    skyProfile.x-sourceImageProfile.x;
                const morphologyOffsetY=
                    skyProfile.y-sourceImageProfile.y;

                const pointUsable=Boolean(
                    pointFit&&
                    (pointFit.confidence==='HIGH'||pointFit.confidence==='MEDIUM')
                );

                const offsetSampleX=pointUsable
                    ? pointFit.mappedCenterX-sampleCenter
                    : morphologyOffsetX;
                const offsetSampleY=pointUsable
                    ? pointFit.mappedCenterY-sampleCenter
                    : morphologyOffsetY;

                const maxSampleShift=
                    FRAMING_SAMPLE_SIZE*FRAMING_MAX_SHIFT_FRACTION;
                const boundedOffsetX=clamp(
                    offsetSampleX,
                    -maxSampleShift,
                    maxSampleShift
                );
                const boundedOffsetY=clamp(
                    offsetSampleY,
                    -maxSampleShift,
                    maxSampleShift
                );

                const sampleX=
                    width/2+
                    boundedOffsetX/FRAMING_SAMPLE_SIZE*width;
                const sampleY=
                    height/2+
                    boundedOffsetY/FRAMING_SAMPLE_SIZE*height;

                if(typeof aladinPrewarm.pix2world!=='function')return destination;
                const world=aladinPrewarm.pix2world(sampleX,sampleY,'ICRS');
                const ra=Number(world?.[0]);
                const dec=Number(world?.[1]);
                if(!Number.isFinite(ra)||!Number.isFinite(dec))return destination;

                const baseRa=Number(destination.ra);
                const baseDec=Number(destination.dec);
                const baseFov=Number(destination.fovDegrees);
                if(!Number.isFinite(baseFov)||baseFov<=0)return destination;

                const maxAngularShift=Math.max(.02,baseFov*.30);
                if(
                    angularSeparationDegrees(
                        baseRa,baseDec,ra,dec
                    )>maxAngularShift
                )return destination;

                const morphologyScaleRatio=
                    Number(skyProfile.scale)/
                    Number(sourceImageProfile.scale);
                const morphologyScaleReliable=
                    Number.isFinite(Number(sourceImageProfile.scale))&&
                    Number(sourceImageProfile.scale)>=2.5&&
                    Number.isFinite(Number(skyProfile.scale))&&
                    Number(skyProfile.scale)>=2.5&&
                    Number.isFinite(morphologyScaleRatio)&&
                    morphologyScaleRatio>=.40&&
                    morphologyScaleRatio<=2.50;

                const pointScaleReliable=
                    pointUsable&&
                    Number.isFinite(Number(pointFit.scaleRatio))&&
                    Number(pointFit.scaleRatio)>=.40&&
                    Number(pointFit.scaleRatio)<=2.50;

                const scaleRatio=pointScaleReliable
                    ? Number(pointFit.scaleRatio)
                    : morphologyScaleReliable
                        ? morphologyScaleRatio
                        : 1;

                const correctedFov=
                    pointScaleReliable||morphologyScaleReliable
                        ? clamp(
                            baseFov*scaleRatio,
                            baseFov*.50,
                            baseFov*2.00
                          )
                        : baseFov;

                const rawRotation=destination.aladinRotation;
                const baseRotation=
                    rawRotation!==null&&
                    rawRotation!==undefined&&
                    rawRotation!==''&&
                    Number.isFinite(Number(rawRotation))
                        ? Number(rawRotation)
                        : null;

                // Existing/catalog orientations are authoritative.
                // Rotation analysis is permitted only for null/missing values.
                const morphologyRotationReliable=
                    baseRotation===null&&
                    sourceImageProfile.eccentricity>.22&&
                    skyProfile.eccentricity>.22;

                const morphologyDelta=morphologyRotationReliable
                    ? normalizeSignedAngle(
                        sourceImageProfile.angle-skyProfile.angle
                      )
                    : null;

                // Null orientation: use only the parked-time morphology/blob
                // comparison. If that cannot resolve an angle, use North-up.
                const rotationDelta=
                    baseRotation===null&&morphologyDelta!==null
                        ? morphologyDelta
                        : 0;

                const rotationSource=
                    baseRotation!==null
                        ? 'CATALOG'
                        : morphologyDelta!==null
                            ? 'MORPHOLOGY'
                            : 'NORTH';

                const resolvedRotation=
                    baseRotation!==null
                        ? baseRotation
                        : morphologyDelta!==null
                            ? morphologyDelta
                            : 0;

                const centerChanged=
                    angularSeparationDegrees(
                        baseRa,baseDec,ra,dec
                    )>1e-7;
                const scaleChanged=
                    Math.abs(correctedFov-baseFov)>
                    Math.max(1e-7,baseFov*.005);
                const rotationChanged=
                    baseRotation===null||
                    Math.abs(rotationDelta)>.25;

                if(!centerChanged&&!scaleChanged&&!rotationChanged)
                    GV_TRACE.enabled&&gvTrace(2663,'TRAVEL_RETURN',{name:String(destination?.name||'')});
        return destination;

                return Object.freeze({
                    ...destination,
                    framingBaseRa:baseRa,
                    framingBaseDec:baseDec,
                    framingBaseFov:baseFov,
                    framingBaseRotation:baseRotation,
                    ra,
                    dec,
                    fov:correctedFov,
                    ...(baseRotation===null
                        ? {
                            aladinRotation:resolvedRotation,
                            framingRotationCandidate:resolvedRotation
                          }
                        : {}),
                    framingCorrected:true,
                    framingConfidence:
                        pointFit?.confidence==='HIGH'
                            ? 'POINT_HIGH'
                            : pointFit?.confidence==='MEDIUM'
                                ? 'POINT_MEDIUM'
                                : morphologyRotationReliable||
                                  morphologyScaleReliable
                                    ? 'MORPHOLOGY'
                                    : 'CATALOG',
                    framingRegistrationSource:rotationSource,
                    framingPointMatches:pointFit?.inliers??0,
                    framingPointRms:
                        Number.isFinite(Number(pointFit?.rms))
                            ? Number(pointFit.rms)
                            : null,
                    framingPointSpread:
                        Number.isFinite(Number(pointFit?.spread))
                            ? Number(pointFit.spread)
                            : null,
                    framingScaleRatio:
                        pointScaleReliable||morphologyScaleReliable
                            ? scaleRatio
                            : null,
                    framingRotationDelta:rotationDelta
                });
            }catch(error){
                console.warn(
                    'GALAXY VIEWER OPTIONAL ARCHIVE FRAMING SKIPPED',
                    error
                );
                return destination;
            }
        }

        function blockedPrefetchKeys(){
            const keys=new Set(prefetchReady.map(item=>item.key));
            for(const destination of prefetchQueued)keys.add(destinationKey(destination));
            for(const key of prefetchLoading.keys())keys.add(key);
            if(priorityPrefetchDestination)keys.add(destinationKey(priorityPrefetchDestination));
            if(activePreparedItem?.key)keys.add(activePreparedItem.key);
            for(const item of historyPreparedItems)if(item?.key)keys.add(item.key);
            if(activeTargetKey)keys.add(activeTargetKey);
            return keys;
        }

        function choosePrefetchCandidate(){
            const blocked=blockedPrefetchKeys(),now=Date.now();
            const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&now>=Number(prefetchRetryAfter.get(key)||0)});
            if(!pool.length)return null;
            return pool[Math.floor(Math.random()*pool.length)];
        }

        function inFlightDestination(excludeName=''){
            const excluded=String(excludeName||'').trim().toLowerCase();
            for(const key of prefetchLoading.keys()){
                const destination=galaxyCatalog.find(item=>destinationKey(item)===key&&item.name.toLowerCase()!==excluded);
                if(destination)return destination;
            }
            return null;
        }

        function scheduleRetryFill(){
            if(prefetchRetryTimer)return;
            const now=Date.now();
            const waits=[...prefetchRetryAfter.values()].map(value=>Number(value)-now).filter(value=>value>0);
            if(!waits.length)return;
            prefetchRetryTimer=setTimeout(()=>{prefetchRetryTimer=0;fillPrefetchQueue()},Math.max(100,Math.min(...waits)));
        }

        function queueHasKey(key){return prefetchQueued.some(destination=>destinationKey(destination)===key)}

        function enqueuePrefetch(destination,priority=false){
            const key=destinationKey(destination);
            if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItems.some(item=>item?.key===key))return false;
            const queuedIndex=prefetchQueued.findIndex(item=>destinationKey(item)===key);
            if(queuedIndex>=0){
                if(priority&&queuedIndex>0){const [queued]=prefetchQueued.splice(queuedIndex,1);prefetchQueued.unshift(queued)}
                return false;
            }
            if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return false}
            setHdStatus(destination,'QUEUED');
            if(priority)prefetchQueued.unshift(destination);else prefetchQueued.push(destination);
            return true;
        }

        function scheduleAladinEnhancement(item,destination,priority=false){
            // AR118: this historical enhancement seam is now a HARD AVM
            // authority gate. It may never publish catalog camera values.
            const task=async()=>{
                if(!item)return false;
                if(backgroundWorkSuspended){
                    item.framingState='SUSPENDED';
                    return false;
                }
                item.framingState='PREPARING';
                try{
                    item.destination=await prepareRuntimeAvmAuthority(destination);
                    item.framingState='READY';
                    return true;
                }catch(error){
                    if(error?.name==='AbortError'){
                        item.framingState='SUSPENDED';
                        return false;
                    }
                    item.framingState='RETRY';
                    console.warn('GALAXY VIEWER RUNTIME AVM AUTHORITY REJECTED',error);
                    throw error;
                }
            };
            return runAladinTransaction(task);
        }

        function startPrefetch(destination,priority=false){
            const key=destinationKey(destination);
            if(!key||prefetchLoading.has(key)||prefetchReady.some(item=>item.key===key)||activePreparedItem?.key===key||historyPreparedItems.some(item=>item?.key===key))return;
            if(!priority&&Date.now()<Number(prefetchRetryAfter.get(key)||0)){scheduleRetryFill();return}
            if(prefetchLoading.size>=PREFETCH_MAX_WORKERS){enqueuePrefetch(destination,priority);return}
            const controller=new AbortController();
            prefetchControllers.set(key,controller);
            const promise=(async()=>{
                try{
                    const item=await prepareHdDestination(destination,controller.signal);
                    item.destination=destination;
                    item.framingState='PREPARING';

                    // AR129-B: restore the AR118 hard AVM authority gate.
                    // Nothing enters the ready pool until the actual JPEG AVM/WCS
                    // has supplied RA, Dec, FoV, and camera rotation.
                    await scheduleAladinEnhancement(item,destination,priority);
                    if(
                        item.framingState!=='READY'||
                        item.destination?.avmAuthority!=='RUNTIME_IMAGE_AVM'
                    )throw new Error('RUNTIME AVM AUTHORITY DID NOT REACH READY');

                    prefetchRetryAfter.delete(key);

                    const retentionKeys=preparedRetentionKeys();
                    if(key!==activeTargetKey&&!retentionKeys.has(key)){
                        releasePreparedItem(item);
                        setHdStatus(destination,'QUEUED');
                        return;
                    }

                    if(key===activeTargetKey&&!activePreparedItem){
                        activePreparedItem=item;
                        window.GalaxyViewerRandomGalaxy?.setPreparedHdResource?.(key,item.objectUrl,item.sourceKind,item.image);
                    }else if(prefetchReady.length<PREFETCH_TARGET){
                        prefetchReady.push(item);
                    }else{
                        releasePreparedItem(item);
                        return;
                    }
                    enforceHotPreparedWindow();

                }catch(error){
                    if(error?.name==='AbortError'){
                        setHdStatus(destination,'SUSPENDED');
                        if(key===activeTargetKey)priorityPrefetchDestination=destination;
                        return;
                    }
                    prefetchFailedCount++;
                    setHdStatus(destination,'RETRY-WAIT');
                    prefetchRetryAfter.set(key,Date.now()+PREFETCH_RETRY_MS);
                    // Failed work must remain in the queue.
                    if(!queueHasKey(key))prefetchQueued.push(destination);
                    scheduleRetryFill();
                }
            })().finally(()=>{
                prefetchLoading.delete(key);
                prefetchControllers.delete(key);
                queueMicrotask(fillPrefetchQueue);
                queueMicrotask(ensureArchivePreloadQueue);
            });
            prefetchLoading.set(key,promise);
        }

        function fillPrefetchQueue(){
            if(backgroundWorkSuspended)return;

            if(priorityPrefetchDestination){
                const destination=priorityPrefetchDestination;
                priorityPrefetchDestination=null;
                enqueuePrefetch(destination,true);
            }

            let scans=prefetchQueued.length;

            while(
                prefetchLoading.size<PREFETCH_MAX_WORKERS &&
                prefetchQueued.length &&
                scans>0
            ){
                const destination=prefetchQueued.shift();
                const key=destinationKey(destination);
                const retryAt=Number(prefetchRetryAfter.get(key)||0);

                if(!key){
                    scans--;
                    continue;
                }

                // Retry-wait work rotates; it is never shifted and lost.
                if(Date.now()<retryAt){
                    prefetchQueued.push(destination);
                    scans--;
                    continue;
                }

                startPrefetch(destination,key===activeTargetKey);
                scans=prefetchQueued.length;
            }

            if(prefetchQueued.length)scheduleRetryFill();
        }

        function prefetchHealthCheck(){
            const ready=prefetchReady.length;
            const loading=prefetchLoading.size;
            const queued=prefetchQueued.length;
            const activeKeys=[...prefetchLoading.keys()];
            const retryWait=[...prefetchRetryAfter.entries()].filter(([,time])=>Date.now()<Number(time)).map(([key])=>key);
            const workers=activeKeys.map(key=>Object.freeze({...hdDownloadStatus.get(key)}));
            lastPrefetchHealth=Object.freeze({ready,loading,queued,total:ready+loading+queued,activeKeys:Object.freeze(activeKeys),retryWait:Object.freeze(retryWait),workers:Object.freeze(workers),checkedAt:Date.now()});
            if(!backgroundWorkSuspended&&lastPrefetchHealth.total<PREFETCH_TARGET)fillPrefetchQueue();
            return lastPrefetchHealth;
        }

        prefetchHealthTimer=setInterval(prefetchHealthCheck,PREFETCH_HEALTH_INTERVAL_MS);

        function destinationWithPrepared(item){
            return {...item.destination,preparedHdUrl:item.objectUrl,preparedSource:item.sourceKind,preparedHdImage:item.image};
        }

        function retainHistoryPrepared(item){
            if(!item?.key)return;
            const existing=historyPreparedItems.findIndex(candidate=>candidate?.key===item.key);
            if(existing>=0)historyPreparedItems.splice(existing,1);
            historyPreparedItems.unshift(item);
            while(historyPreparedItems.length>HISTORY_PREPARED_TARGET)
                releasePreparedItem(historyPreparedItems.pop());
            enforceHotPreparedWindow();
        }

        function takeHistoryPrepared(key){
            const index=historyPreparedItems.findIndex(item=>item?.key===key);
            return index>=0?historyPreparedItems.splice(index,1)[0]:null;
        }

        function setPreparedActive(item){
            if(activePreparedItem&&activePreparedItem!==item&&activePreparedItem.key!==item.key)
                retainHistoryPrepared(activePreparedItem);
            activePreparedItem=item;
            activeTargetKey=item.key;
        }

        function consumeReady(destination=null,excludeName=''){
            const requestedKey=destination?destinationKey(destination):'';
            if(requestedKey&&activePreparedItem?.key===requestedKey)return destinationWithPrepared(activePreparedItem);
            if(requestedKey){
                const item=takeHistoryPrepared(requestedKey);
                if(item){
                    if(activePreparedItem&&activePreparedItem.key!==item.key)
                        retainHistoryPrepared(activePreparedItem);
                    activePreparedItem=item;
                    activeTargetKey=item.key;
                    if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
                    return destinationWithPrepared(item);
                }
            }
            let index=-1;
            if(destination)index=prefetchReady.findIndex(item=>item.key===requestedKey);
            else{
                const excluded=String(excludeName||'').trim().toLowerCase();
                index=prefetchReady.findIndex(item=>item.destination.name.toLowerCase()!==excluded);
            }
            if(index<0)return null;
            const [item]=prefetchReady.splice(index,1);
            setPreparedActive(item);
            if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
            return destinationWithPrepared(item);
        }

        async function waitForPreparedKey(key){
            for(;;){
                if(activePreparedItem?.key===key)return true;
                const loading=prefetchLoading.get(key);
                if(loading){
                    try{await loading}catch(_){}
                    return activePreparedItem?.key===key;
                }
                if(priorityPrefetchDestination&&destinationKey(priorityPrefetchDestination)===key){
                    await new Promise(resolve=>setTimeout(resolve,25));
                    continue;
                }
                return false;
            }
        }

        function randomGalaxyProvider({excludeName}={}){
            let destination=null;
            if(!galaxyCatalog.length)throw new Error('COMBINED GALAXY CATALOG IS EMPTY');
            releaseActiveArchivePreload();
            destination=consumeReady(null,excludeName);
            if(!destination){
                throw new Error("NAVIGATION-OWNED DESTINATION IS NOT AVAILABLE");
            }
            activeTargetKey=destinationKey(destination);
            return destination;
        }

        function getRandomNavigationState(){
            const state=randomNavigationWindow.getState();
            return Object.freeze({
                futureTarget:state.futureTarget,
                historyTarget:state.historyTarget,
                hotTarget:state.hotTarget,
                futureCount:state.futureCount,
                historyCount:state.historyCount,
                hotCount:state.hotKeys.length,
                hotKeys:Object.freeze([...state.hotKeys]),
                currentKey:destinationKey(state.current),
                lockedKey:destinationKey(state.locked?.destination||state.locked),
                nextKey:destinationKey(state.next?.destination||state.next),
                forwardCount:state.forwardCount,
                pendingKind:String(state.pending?.kind||'')
            });
        }

        function getPrefetchState(){
            return Object.freeze({
                targetReady:PREFETCH_TARGET,
                maxWorkers:PREFETCH_MAX_WORKERS,
                readyCount:prefetchReady.length,
                loadingCount:prefetchLoading.size,
                queuedCount:prefetchQueued.length,
                pipelineCount:prefetchReady.length+prefetchLoading.size+prefetchQueued.length,
                failedCount:prefetchFailedCount,
                activeDownloadKeys:Object.freeze([...prefetchLoading.keys()]),
                activePreparedGalaxy:activePreparedItem?.destination?.name||'',
                activePreparedSource:activePreparedItem?.sourceKind||'',
                readyDestinations:prefetchReady.map(item=>item.destination.name),
                queuedDestinations:prefetchQueued.map(item=>item.name),
                health:lastPrefetchHealth,
                downloads:getDownloadStatus()
            });
        }

    const api={
      destinationKey,
      fillPrefetchQueue,
      enqueuePrefetch,
      consumeReady,
      setPreparedActive,
      prepareHdDestination,
      waitForPreparedKey,
      retainHistoryPrepared,
      takeHistoryPrepared,
      releasePreparedItem,
      enforceHotPreparedWindow,
      randomGalaxyProvider,
      getRandomNavigationState,
      getPrefetchState,
      getDownloadStatus,
      suspendBackgroundWork,
      resumeBackgroundWork,

      getBackgroundWorkSuspended(){
        return backgroundWorkSuspended;
      },

      getPrefetchReady(){
        return prefetchReady;
      },

      getActiveTargetKey(){
        return activeTargetKey;
      },

      activateQueuedDestination(destination,excludeName=''){
        return consumeReady(destination,excludeName)||null;
      },

      requestHdPrefetch(destination,priority=true){
        if(!destination)return '';
        enqueuePrefetch(destination,Boolean(priority));
        fillPrefetchQueue();
        return destinationKey(destination);
      },

      getHdPreparedResource(key){
        const normalized=
          String(key||'').trim().toLowerCase();

        return activePreparedItem?.key===normalized
          ? activePreparedItem
          : prefetchReady.find(item=>item?.key===normalized)
            || historyPreparedItems.find(item=>item?.key===normalized)
            || null;
      },

      isHdPrepared(key){
        return Boolean(api.getHdPreparedResource(key));
      },

      ensureHdFramingReady(destination){
        const key=destinationKey(destination);
        if(!key)return Promise.resolve(false);

        const item=api.getHdPreparedResource(key);
        if(!item)return Promise.resolve(false);

        if(
          item.framingState==='READY' &&
          item.destination?.avmAuthority==='RUNTIME_IMAGE_AVM'
        )return Promise.resolve(true);

        const existing=hdFramingPromises.get(key);
        if(existing)return existing;

        const promise=scheduleAladinEnhancement(
          item,
          destination,
          true
        ).then(ready=>Boolean(
          ready &&
          item.framingState==='READY' &&
          item.destination?.avmAuthority==='RUNTIME_IMAGE_AVM'
        )).finally(()=>{
          hdFramingPromises.delete(key);
        });

        hdFramingPromises.set(key,promise);
        return promise;
      },

      getGalaxyCatalog(){
        return Object.freeze([...galaxyCatalog]);
      },

      destroy(){
        if(prefetchRetryTimer)
          clearTimeout(prefetchRetryTimer);

        if(prefetchHealthTimer)
          clearInterval(prefetchHealthTimer);

        for(const controller of prefetchControllers.values()){
          try{controller.abort()}catch(_){}
        }

        prefetchControllers.clear();

        if(aladinPrewarmTimer)
          clearTimeout(aladinPrewarmTimer);

        if(aladinPrewarmWaitResolve){
          try{aladinPrewarmWaitResolve(false)}catch(_){}
        }
      }
    };

    return Object.freeze(api);
  }

  class GalaxyRandomGalaxy {
    constructor(options = {}) {
      if (!options.aladin) throw new TypeError('GalaxyRandomGalaxy requires an Aladin instance.');
      if (!(options.host instanceof Element)) throw new TypeError('GalaxyRandomGalaxy requires a DOM Element host.');
      if (instances.has(options.host)) throw new Error('GalaxyRandomGalaxy is already mounted on this host.');

      this.options = { ...DEFAULTS, ...options };
      this.aladin = options.aladin;
      this.host = options.host;
      this.viewerRoot =
        options.viewerRoot instanceof Element
          ? options.viewerRoot
          : (this.host.parentElement || document.body);
      this.randomButton = options.randomButton instanceof Element ? options.randomButton : null;
      installRandomWaitComet(this.randomButton);
      this.provider = typeof options.provider === 'function' ? options.provider : null;
      this.geminiProvider = typeof options.geminiProvider === 'function' ? options.geminiProvider : null;
      this.destroyed = false;
      this.busy = false;
      this.interactionOwner = null;
      this.arrived = true;
      this.activeDestination = null;
      this.lastGeminiEnrichment = null;
      this.prefetchedDestination = null;
      this.prefetchPromise = null;
      this.catalogCount = Number(options.catalogCount || 0);
      this.hdOpen = false;
      this.hdScale = 1;
      this.hdTranslateX = 0;
      this.hdTranslateY = 0;
      this.hdPointers = new Map();
      this.hdGesture = null;
      this.hdScaleBarValue = null;
      this.hdScaleBarTimer = 0;
      this.travelHudFrame = 0;

      // REQ-015F: Random Galaxy owns its Aladin recovery lifecycle.
      this.hdSkySnapshot = null;
      this.viewerHiddenSnapshot = null;
      this.viewerHiddenAt = 0;
      this.lastAladinRecoveryAt = 0;
      this.aladinRecoveryBusy = false;
      this.recoveryTimeoutMs = Math.max(1000, Number(options.recoveryTimeoutMs || 5000));

      // Last-resort Aladin recovery control.
      this.refreshSkyDelayMs = Math.max(5000, Number(options.refreshSkyDelayMs || 15000));
      this.refreshSkyTimer = 0;

      this.currentGalaxy = this.#initialCurrent(options.currentGalaxy);
      this.onStatus = typeof options.onStatus === 'function' ? options.onStatus : null;
      this.onArrival = typeof options.onArrival === 'function' ? options.onArrival : null;
      this.onError = typeof options.onError === 'function' ? options.onError : null;

      this.root = this.#build();
      this.host.appendChild(this.root);

      this.earthReturnController =
        false && options.earthReturnOptions
          ? createEarthReturnController({
              ...options.earthReturnOptions,
              root: this.viewerRoot,
              aladin: this.aladin,
              getHdViewport: () => this.hdViewport,
              isHdOpen: () => this.hdOpen
            })
          : null;
      this.distanceRenderer = new FixedDistanceRenderer(this.distanceNumberHost, this.options);

      this.refreshSkyButton = document.createElement('button');
      this.refreshSkyButton.type = 'button';
      this.refreshSkyButton.className = 'gvrg-refresh-sky';
      this.refreshSkyButton.setAttribute('aria-label','REFRESH SKY');
      this.refreshSkyButton.innerHTML =
        '<span class="gvrg-refresh-word">REFRESH</span>' +
        '<span class="gvrg-refresh-orbit" aria-hidden="true">' +
          '<span class="gvrg-refresh-arrow"></span>' +
          '<span class="gvrg-refresh-comet"><i></i></span>' +
        '</span>' +
        '<span class="gvrg-refresh-word">SKY</span>';
      this.refreshSkyButton.hidden = true;
      this.root.appendChild(this.refreshSkyButton);

      this._randomClick = () => this.travelToRandom().catch((error) => this.#handleError(error));
      this._randomRequest = (event) => {
        event.preventDefault();
        event.stopPropagation();
        this.travelToRandom().catch((error) => this.#handleError(error));
      };
      this._hdClick = () => this.showHD();
      this._downloadClick = () => this.downloadHD().catch((error) => this.#handleError(error));
      this._backClick = () => this.backToSky();
      this._pointerDown = (event) => this.#onHdPointerDown(event);
      this._pointerMove = (event) => this.#onHdPointerMove(event);
      this._pointerUp = (event) => this.#onHdPointerUp(event);

      this._refreshSkyClick = (event) => {
        event.preventDefault();
        event.stopPropagation();

        if (this.destroyed || this.busy || !this.arrived || this.hdOpen) return;

        const exact = this.#exactActiveAladinState(this.activeDestination);
        if (!exact) return;

        this.refreshSkyButton.classList.add('gvrg-refresh-working');
        this.#restoreAladinState(exact,'manual-refresh-sky');

        setTimeout(() => {
          this.refreshSkyButton?.classList.remove('gvrg-refresh-working');
          this.#hideRefreshSky();
        }, 1200);

        requestAnimationFrame(() =>
          this.#checkAndRecoverStaleAladin('manual-refresh-sky-postcheck')
        );
      };

      this._viewerPageShow = () => this.#handleViewerResume('pageshow');
      this._viewerFocus = () => this.#handleViewerResume('focus');
      this._viewerVisibility = () => {
        if (document.hidden) {
          this.viewerHiddenAt = performance.now();
          this.viewerHiddenSnapshot =
            this.hdSkySnapshot ||
            this.#captureAladinState() ||
            this.#exactActiveAladinState();
          return;
        }
        const elapsed = this.viewerHiddenAt
          ? performance.now() - this.viewerHiddenAt
          : 0;
        const snapshot = this.viewerHiddenSnapshot;
        this.viewerHiddenAt = 0;
        this.viewerHiddenSnapshot = null;
        if (elapsed >= this.recoveryTimeoutMs)
          this.#handleViewerResume('visibility-resume', snapshot);
      };

      if (this.randomButton) {
        if (this.options.bindClick) this.randomButton.addEventListener('click', this._randomClick);
        this.randomButton.addEventListener(this.options.requestEvent, this._randomRequest);
      }
      this.viewHdButton.addEventListener('click', this._hdClick);
      this.providerIconButton.addEventListener('click', this._hdClick);
      this.downloadButton.addEventListener('click', this._downloadClick);
      this.backButton.addEventListener('click', this._backClick);
      this.hdViewport.addEventListener('pointerdown', this._pointerDown);
      this.hdViewport.addEventListener('pointermove', this._pointerMove);
      this.hdViewport.addEventListener('pointerup', this._pointerUp);
      this.hdViewport.addEventListener('pointercancel', this._pointerUp);
      this.refreshSkyButton.addEventListener('click',this._refreshSkyClick);

      // HTML/browser + Android WebView lifecycle recovery.
      window.addEventListener('pageshow', this._viewerPageShow);
      window.addEventListener('focus', this._viewerFocus);
      document.addEventListener('visibilitychange', this._viewerVisibility);

      instances.set(this.host, this);
      this.__gvReadyState='PENDING';
      GV_TRACE.enabled&&gvTrace(3328,'READY_CREATED',{state:this.__gvReadyState});
      this.ready = this.#initialize();
      this.ready.then(
        ()=>{
          this.__gvReadyState='RESOLVED';
          GV_TRACE.enabled&&gvTrace(3328,'READY_RESOLVED',{state:this.__gvReadyState});
        },
        error=>{
          this.__gvReadyState='REJECTED';
          GV_TRACE.enabled&&gvTraceError(3328,'READY_REJECTED',error);
        }
      );
    }

    #buildHomePresentation() {
      const presentation = bootstrapHomePresentation(this.viewerRoot);

      this.universeContext = presentation.universeContext;
      this.homeOverlay = presentation.homeOverlay;

      // The regular 0034 stylesheet is active now; retire the temporary
      // early-bootstrap stylesheet without removing the adopted DOM.
      document.getElementById(HOME_BOOTSTRAP_STYLE_ID)?.remove();

      this.universeContext.removeAttribute('data-gvrg-home-bootstrap');
      this.homeOverlay.removeAttribute('data-gvrg-home-bootstrap');

      if (finiteNumber(this.currentGalaxy && this.currentGalaxy.distance) > 0)
        this.#hideHomePresentation();
    }

    #hideHomePresentation() {
      this.homeOverlay?.classList.add('gv-hidden');
      this.universeContext?.classList.add('gv-hidden');
    }

    #initialCurrent(currentGalaxy) {
      const coords = this.aladin.getRaDec ? this.aladin.getRaDec() : [0, 0];
      const supplied = currentGalaxy && typeof currentGalaxy === 'object' ? currentGalaxy : {};
      return {
        name: cleanText(supplied.name || 'CURRENT POSITION'),
        ra: finiteNumber(supplied.ra) ?? finiteNumber(coords[0]) ?? 0,
        dec: finiteNumber(supplied.dec) ?? finiteNumber(coords[1]) ?? 0,
        distance: finiteNumber(supplied.distance)
      };
    }

    #style() {
      const style = document.createElement('style');
      style.textContent = `
.gvrg-root,.gvrg-root *{box-sizing:border-box}
.gvrg-root{position:absolute;inset:0;z-index:9990;pointer-events:none;font-family:"${FONT_NAMES.spaceAge}",sans-serif;color:#eefaff}
#gv-universe-context{position:absolute;left:50%;top:auto;bottom:calc(50% + min(25vw,50dvh) + 8px);z-index:7095;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;width:min(310px,76vw);pointer-events:none;transition:opacity .2s ease}
#gv-universe-context .gv-universe-label{padding:5px 8px 6px;border:1px solid rgba(124,203,255,.78);border-radius:6px;background:rgba(8,27,58,.68);box-shadow:0 0 9px rgba(88,191,255,.18);color:#DDF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 6px rgba(88,191,255,.42);font:400 9px/1.25 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.65px}
#gv-universe-context .gv-universe-count{display:block;margin-top:2px;color:#7CCBFF;font-size:10px;letter-spacing:.8px}
#gv-universe-context .gv-universe-leader{position:relative;width:1px;height:18px;background:rgba(124,203,255,.86);box-shadow:0 0 7px rgba(88,191,255,.48)}
#gv-universe-context .gv-universe-leader::after{content:"";position:absolute;left:50%;bottom:-1px;width:0;height:0;transform:translateX(-50%);border-left:5px solid transparent;border-right:5px solid transparent;border-top:8px solid #7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.68))}
#gv-universe-context.gv-hidden{opacity:0;visibility:hidden}
#gv-we-are-here{position:absolute;inset:0;z-index:7090;pointer-events:none;transition:opacity .2s ease}
#gv-we-are-here .gv-home-leader{position:absolute;left:50%;top:calc(50% + 16px);bottom:34%;width:1px;min-height:36px;transform:translateX(-50%);background:rgba(124,203,255,.88);box-shadow:0 0 8px rgba(88,191,255,.58)}
#gv-we-are-here .gv-home-leader::before{content:"";position:absolute;left:50%;top:-8px;transform:translateX(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:8px solid #7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.75))}
#gv-we-are-here .gv-home-label{position:absolute;left:50%;top:66%;transform:translateX(-50%);width:min(260px,78vw);padding:6px 9px 7px;border:1px solid rgba(124,203,255,.88);border-radius:6px;background:rgba(8,27,58,.74);color:#EAF8FF;text-align:center;text-transform:uppercase;text-shadow:0 0 8px rgba(88,191,255,.58);box-shadow:0 0 10px rgba(88,191,255,.24)}
#gv-we-are-here .gv-home-origin{display:flex;align-items:center;justify-content:center;gap:8px;color:#7CCBFF;font:400 15px/1.2 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1.25px}
#gv-we-are-here .gv-earth-icon{position:relative;isolation:isolate;display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:drop-shadow(0 0 2px rgba(87,255,147,.34))}
#gv-we-are-here .gv-earth-icon::before{content:"";position:absolute;left:50%;top:50%;width:31px;height:31px;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(87,255,147,.27) 0%,rgba(77,255,143,.13) 46%,rgba(77,255,143,0) 76%);filter:blur(3px);z-index:-1}
#gv-we-are-here .gv-home-sub{margin-top:4px;color:#CDEEFF;font:400 10px/1.3 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px}
#gv-we-are-here .gv-home-hint{margin-top:5px;color:#A6DFFF;font:400 9px/1.3 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.8px}
#gv-we-are-here.gv-hidden{opacity:0;visibility:hidden}
.gvrg-status{display:none;position:absolute;left:50%;top:72px;transform:translateX(-50%);width:min(280px,82vw);padding:9px 12px;border:1px solid rgba(221,248,255,.86);border-radius:6px;background:rgba(11,49,119,.62);color:#EAF8FF;font:400 12px/1.3 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.8px;text-align:center;box-shadow:0 0 14px rgba(41,109,189,.30),inset 0 0 9px rgba(41,109,189,.09);opacity:0;visibility:hidden;transition:opacity .18s ease;pointer-events:none}
.gvrg-status-visible{opacity:1;visibility:visible}
.gvrg-status-kicker{font:400 9px/1.2 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1.7px;color:#9BE5FF}
.gvrg-status-heading{margin-top:2px;font:400 12px/1.2 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;color:#DDF8FF}
.gvrg-status-destination{margin-top:3px;font:400 14px/1.22 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.9px;color:#7CCBFF;text-shadow:0 0 9px rgba(88,191,255,.70);white-space:normal;overflow-wrap:anywhere}
.gvrg-distance{display:none;position:absolute;left:50%;top:154px;transform:translateX(-50%);width:min(330px,88vw);padding:9px 11px 10px;border:1px solid rgba(221,248,255,.72);border-radius:6px;background:rgba(8,27,58,.66);box-shadow:0 0 13px rgba(41,109,189,.20);text-align:center;opacity:0;transition:opacity .20s linear}
.gvrg-distance-label{height:14px;font:400 9px/14px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:2px;color:#9EDCFF}
.gvrg-distance-number{display:flex;align-items:center;justify-content:center;gap:8px;height:28px;white-space:nowrap;overflow:hidden}
.gvrg-number-cells{display:inline-flex;align-items:baseline;justify-content:flex-end;flex:none}
.gvrg-digit-cell,.gvrg-decimal-cell{display:inline-flex;align-items:center;justify-content:center;flex:none;height:25px;font:400 20px/25px "${FONT_NAMES.digits}",sans-serif;color:#F7FDFF;text-shadow:0 0 7px rgba(88,191,255,.34);transform:scaleY(1.08);transform-origin:center}
.gvrg-distance-unit{display:inline-flex;align-items:center;width:158px;height:25px;overflow:hidden;font:400 9px/25px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.7px;color:#DDF8FF;text-align:left;white-space:nowrap}
.gvrg-route{height:14px;font:400 8px/14px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;color:#A9DFFF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gvrg-progress{height:3px;margin-top:6px;border-radius:3px;background:rgba(221,248,255,.14);overflow:hidden}
.gvrg-progress-fill{width:0;height:100%;background:#58BFFF;box-shadow:0 0 8px rgba(88,191,255,.75);transition:width .08s linear}
.gvrg-card{position:absolute;left:50%;top:auto;bottom:64px;transform:translateX(-50%);width:calc(100vw - 24px);max-width:none;padding:4px 5px 4px;border:1px solid #7CCBFF;border-radius:6px;background:rgba(8,27,58,.78);box-shadow:inset 0 0 10px rgba(124,203,255,.10),0 0 14px rgba(41,109,189,.34);opacity:0;transition:opacity .20s ease;pointer-events:none}
.gvrg-card-visible{opacity:1;pointer-events:none}
.gvrg-name{display:none}
.gvrg-science-grid{display:grid;grid-template-columns:minmax(0,1.18fr) minmax(0,1.08fr) minmax(0,.74fr);gap:0;border-top:1px solid rgba(124,203,255,.28);border-left:1px solid rgba(124,203,255,.28);pointer-events:none}
.gvrg-row{display:block;min-width:0;margin:0;padding:1px 4px 2px;border-right:1px solid rgba(124,203,255,.28);border-bottom:1px solid rgba(124,203,255,.28);text-align:center;pointer-events:none}
.gvrg-row:nth-child(3n){border-right:0}
.gvrg-label{font:400 10px/1.12 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.48px;color:#7CCBFF;text-align:center;text-shadow:0 0 4px rgba(88,191,255,.42);pointer-events:none}
.gvrg-value{min-width:0;min-height:11px;margin-top:1px;font:400 9px/1.06 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.10px;color:#ffffff;text-align:center;text-shadow:0 0 4px rgba(205,244,255,.18);white-space:normal;overflow-wrap:anywhere;pointer-events:none}
.gvrg-card-distance{display:block;min-width:0}
.gvrg-value-number{font:400 9px/1.06 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.10px}
.gvrg-value-unit{display:none}
.gvrg-actions{display:flex;justify-content:center;align-items:stretch;gap:5px;margin-top:3px;pointer-events:none}
.gvrg-button{appearance:none;border:1px solid rgba(175,225,255,.84);border-radius:5px;background:rgba(7,27,42,.95);color:#effbff;padding:6px 8px;font:400 9px/1 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.55px;cursor:pointer}
.gvrg-button:disabled{opacity:.45;cursor:default}
.gvrg-hd-primary{width:min(190px,calc(100% - 41px));flex:0 1 190px;min-width:0;height:36px;padding:4px 8px;background:linear-gradient(145deg,rgba(11,49,119,.96),rgba(20,132,219,.94));color:#EAF8FF;font:400 11px/1.05 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.55px;text-align:center;text-shadow:0 0 4px rgba(221,248,255,.76);pointer-events:auto}
.gvrg-hd-icon-button{flex:0 0 36px;width:36px;height:36px;padding:2px;display:flex;align-items:center;justify-content:center;overflow:hidden;border:2px solid transparent;border-radius:5px;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98)) padding-box,linear-gradient(145deg,#DDF8FF 0%,#7CCBFF 48%,#296DBD 100%) border-box;pointer-events:auto}
.gvrg-hd-primary{border:2px solid #7CCBFF;box-shadow:inset 0 0 7px rgba(143,229,255,.28),0 0 8px rgba(88,191,255,.38),0 0 14px rgba(88,191,255,.18)}.gvrg-hd-icon-button{box-shadow:inset 0 0 7px rgba(225,248,255,.22),0 0 8px rgba(124,203,255,.42),0 0 14px rgba(41,109,189,.22)}
.gvrg-hd-icon-button img{display:block;width:100%;height:100%;object-fit:contain;background:transparent;pointer-events:none}
.gvrg-hd{position:absolute;inset:0;display:none;z-index:20;background:#000;pointer-events:auto;overflow:hidden}
.gvrg-hd-open{display:block}
.gvrg-hd-viewport{position:absolute;inset:0;display:flex;align-items:flex-start;justify-content:center;overflow:hidden;touch-action:none;user-select:none;-webkit-user-select:none;cursor:grab}
.gvrg-hd-viewport:active{cursor:grabbing}
.gvrg-hd img{position:relative;inset:auto;width:auto;height:auto;max-width:100%;max-height:100%;object-fit:contain;background:#000;transform-origin:50% 0;will-change:transform;pointer-events:none;user-select:none;-webkit-user-drag:none}
.gvrg-hd-science{position:absolute;left:50%;top:max(6px,env(safe-area-inset-top));z-index:4;transform:translateX(-50%);width:min(560px,92vw);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;padding:0;border:1px solid #7CCBFF;border-radius:6px;background:rgba(8,27,58,.72);box-shadow:inset 0 0 8px rgba(124,203,255,.08),0 0 12px rgba(41,109,189,.28);text-align:center;pointer-events:none;overflow:hidden}
.gvrg-hd-science-item{min-width:0;padding:6px 8px;border-right:1px solid rgba(124,203,255,.22);border-bottom:1px solid rgba(124,203,255,.22);pointer-events:none}
.gvrg-hd-science-item:nth-child(3n){border-right:0}
.gvrg-hd-science-item:nth-child(n+4){border-bottom:0}
.gvrg-hd-science-label{font:400 11.4px/1.08 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.22px;color:#7CCBFF;text-shadow:0 0 5px rgba(88,191,255,.42);text-align:center;pointer-events:none}
.gvrg-hd-science-value{min-height:15px;margin-top:1px;font:400 13.5px/1.12 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.04px;color:#ffffff;text-shadow:0 0 4px rgba(205,238,255,.20);text-align:center;white-space:normal;overflow-wrap:anywhere;pointer-events:none}
@media(min-width:520px){.gvrg-hd-science{grid-template-columns:repeat(5,minmax(0,1fr))}.gvrg-hd-science-item{border-bottom:0;border-right:1px solid rgba(124,203,255,.22)}.gvrg-hd-science-item:last-child{border-right:0}}
.gvrg-hd-footer{position:absolute;left:0;right:0;bottom:0;z-index:3;padding:28px 10px 10px;background:linear-gradient(transparent,rgba(0,0,0,.94));text-align:center;pointer-events:none}
.gvrg-hd-footer>*{pointer-events:auto}
.gvrg-credit{margin-bottom:8px;font:400 8px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.5px;color:#d8eff9}
.gvrg-hd-controls{display:flex;justify-content:center;gap:16px;flex-wrap:wrap}
.gvrg-hd-controls .gvrg-button{min-height:40px;font-size:11px}
.gvrg-download-button,.gvrg-back-button{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-width:156px;padding:7px 12px}
.gvrg-download-button{border-color:#9DEAFF;background:linear-gradient(145deg,rgba(7,49,104,.98),rgba(48,177,255,.96));color:#F2FBFF;text-shadow:0 0 4px rgba(206,244,255,.88);box-shadow:inset 0 0 8px rgba(11,61,255,.34),0 0 10px rgba(72,190,255,.54),0 0 18px rgba(5,140,255,.18)}
.gvrg-download-icon{position:relative;display:inline-block;width:20px;height:20px;flex:none;filter:drop-shadow(0 0 4px rgba(157,234,255,.82));pointer-events:none}
.gvrg-download-arrow{position:absolute;left:50%;top:1px;width:4px;height:12px;transform:translateX(-50%);background:#DFF7FF;border-radius:2px;box-shadow:0 0 4px rgba(157,234,255,.78)}
.gvrg-download-arrow::after{content:"";position:absolute;left:50%;bottom:-1px;width:9px;height:9px;border-right:4px solid #62D8FF;border-bottom:4px solid #62D8FF;transform:translateX(-50%) rotate(45deg);transform-origin:center;box-sizing:border-box}
.gvrg-download-bar{position:absolute;left:50%;bottom:0;width:16px;height:3px;transform:translateX(-50%);border-radius:2px;background:#DFF7FF;box-shadow:0 0 5px rgba(98,216,255,.88)}
.gvrg-back-button{border-color:#DDF8FF;background:linear-gradient(145deg,rgba(11,49,119,.96),rgba(20,132,219,.94));color:#EAF8FF;text-shadow:0 0 4px rgba(221,248,255,.76);box-shadow:inset 0 0 7px rgba(143,229,255,.28),0 0 8px rgba(41,109,189,.34)}
.gvrg-back-chevron{position:relative;display:inline-block;width:20px;height:20px;flex:none;pointer-events:none}
.gvrg-back-chevron::before,.gvrg-back-chevron::after{content:"";position:absolute;left:50%;top:50%;width:15px;height:15px;border-style:solid;border-left:0;border-bottom:0;box-sizing:border-box;pointer-events:none}
.gvrg-back-chevron::before{border-width:5px;border-color:#7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.90));transform:translate(-38%,-50%) rotate(-135deg)}
.gvrg-back-chevron::after{width:11px;height:11px;border-width:3px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-32%,-50%) rotate(-135deg)}
.gvrg-hd-scale{position:absolute;left:50%;bottom:12px;z-index:6;transform:translateX(-50%);display:none;flex-direction:column;align-items:center;gap:4px;pointer-events:none;color:#78FFAB;font:400 9px/1.05 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.7px;text-align:center;text-shadow:0 0 3px rgba(229,255,239,.72),0 0 7px rgba(87,255,147,.28);white-space:nowrap}
.gvrg-hd-scale-line{position:relative;height:10px;border-top:1px solid #78FFAB;filter:drop-shadow(0 0 2px rgba(120,255,171,.52))}
.gvrg-hd-scale-line::before,.gvrg-hd-scale-line::after{content:"";position:absolute;top:-5px;width:1px;height:9px;background:#78FFAB;box-shadow:0 0 2px rgba(120,255,171,.48)}
.gvrg-hd-scale-line::before{left:0}.gvrg-hd-scale-line::after{right:0}
.gvrg-hd-scale-label{font:400 9px/1.05 "${FONT_NAMES.spaceAge}",sans-serif;color:#78FFAB;letter-spacing:.7px;text-shadow:0 0 3px rgba(229,255,239,.72),0 0 7px rgba(87,255,147,.28)}
.gvrg-hd-loading{position:absolute;left:50%;top:50%;z-index:2;transform:translate(-50%,-50%);font:400 9px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;color:#dff7ff;pointer-events:none}
.gvrg-refresh-sky{position:absolute;left:50%;top:50%;z-index:85;transform:translate(-50%,-50%);box-sizing:border-box;width:46px;height:46px;margin:0;padding:2px 2px 3px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;border:2px solid #91DCFF;border-radius:7px;background:linear-gradient(145deg,rgba(8,35,92,.98),rgba(41,142,218,.97));color:#EAF9FF;box-shadow:inset 0 0 6px rgba(204,241,255,.18),0 0 8px rgba(83,197,255,.42),0 0 13px rgba(31,105,205,.22);font-family:"${FONT_NAMES.spaceAge}",sans-serif;pointer-events:auto;touch-action:manipulation;cursor:pointer}
.gvrg-refresh-sky[hidden]{display:none!important}
.gvrg-refresh-word{display:block;height:9px;font:400 7.4px/9px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.25px;color:#EAF9FF;text-shadow:0 0 3px rgba(160,225,255,.82);white-space:nowrap}
.gvrg-refresh-orbit{position:relative;display:block;width:20px;height:20px;flex:0 0 20px;margin:0}
.gvrg-refresh-arrow{position:absolute;inset:1px;border:2px solid #9BE5FF;border-left-color:transparent;border-radius:50%;filter:drop-shadow(0 0 2px rgba(138,224,255,.88))}
.gvrg-refresh-arrow::after{content:"";position:absolute;right:-3px;top:0;width:5px;height:5px;border-top:2px solid #DDF8FF;border-right:2px solid #DDF8FF;transform:rotate(20deg)}
.gvrg-refresh-comet{position:absolute;left:0;top:0;width:20px;height:20px;border-radius:50%;opacity:0;pointer-events:none;transform-origin:50% 50%}
.gvrg-refresh-comet::before{content:"";position:absolute;left:50%;top:-1px;width:5px;height:5px;margin-left:-2.5px;border-radius:50%;background:#F8FFFF;box-shadow:0 0 3px #FFFFFF,0 0 6px #9BE5FF,0 0 9px #317DD4}
.gvrg-refresh-comet i{position:absolute;left:50%;top:0;width:8px;height:2px;margin-left:-1px;border-radius:50%;background:linear-gradient(90deg,rgba(186,238,255,.85),rgba(77,161,235,0));transform:rotate(42deg);transform-origin:0 50%;filter:blur(.15px)}
.gvrg-refresh-sky.gvrg-refresh-working .gvrg-refresh-comet{opacity:1;animation:gvrgRefreshOrbit .9s linear infinite}
@keyframes gvrgRefreshOrbit{to{transform:rotate(360deg)}}
/* ============================================================ */
/* ECO-027B-1 RANDOM / TRAVEL PRESENTATION — OWNER 0034       */
/* ============================================================ */
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:static;display:flex;flex:1 1 auto;min-width:0;align-items:center;justify-content:center;height:36px;margin:0;padding:0 12px;border:1px solid #DDF8FF;border-radius:6px;background:linear-gradient(145deg,rgba(11,49,119,.96),rgba(20,132,219,.94));color:#EAF8FF;font:400 15.5px/1 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 4px rgba(221,248,255,.76);box-shadow:inset 0 0 7px rgba(143,229,255,.28),0 0 8px rgba(41,109,189,.34);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
#gv-random-galaxy:active{filter:brightness(1.08)}
.gv-galaxy-history{appearance:none;-webkit-appearance:none;position:relative;display:flex;flex:0 0 36px;align-items:center;justify-content:center;width:36px;height:36px;margin:0;padding:0;border:1px solid #DDF8FF;border-radius:6px;background:linear-gradient(145deg,rgba(11,49,119,.96),rgba(20,132,219,.94));color:transparent;box-shadow:inset 0 0 7px rgba(143,229,255,.28),0 0 8px rgba(41,109,189,.34);cursor:pointer;touch-action:manipulation;outline:none;overflow:hidden;pointer-events:auto}
.gv-galaxy-history::before,.gv-galaxy-history::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;pointer-events:none;box-sizing:border-box}
.gv-galaxy-history::before{border-width:6px;border-color:#7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.90));transform:translate(-62%,-50%) rotate(45deg)}
.gv-galaxy-history::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-66%,-50%) rotate(45deg)}
.gv-galaxy-history-back::before{transform:translate(-38%,-50%) rotate(-135deg)}
.gv-galaxy-history-back::after{transform:translate(-34%,-50%) rotate(-135deg)}
.gv-galaxy-history:disabled{opacity:.62;cursor:default;box-shadow:inset 0 0 7px rgba(143,229,255,.18),0 0 6px rgba(41,109,189,.24)}
#gv-travel-hud{position:absolute;left:50%;top:auto;bottom:64px;z-index:7350;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:4px;width:min(214px,68vw);padding:0;border:0;background:transparent;box-shadow:none;text-align:center;pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-travel-hud.gv-visible{opacity:1;visibility:visible}
#gv-travel-provider-icon{position:absolute;left:auto;right:12px;top:50%;transform:translateY(-50%);box-sizing:border-box;display:none;align-items:center;justify-content:center;overflow:hidden;width:36px;height:36px;padding:2px;border:2px solid transparent;border-radius:5px;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98)) padding-box,linear-gradient(145deg,#DDF8FF 0%,#7CCBFF 48%,#296DBD 100%) border-box;box-shadow:inset 0 0 7px rgba(225,248,255,.22),0 0 8px rgba(124,203,255,.42),0 0 14px rgba(41,109,189,.22);pointer-events:none;z-index:2}
#gv-travel-provider-icon img{display:block;width:100%;height:100%;object-fit:contain;background:transparent;pointer-events:none}
#gv-travel-primary{position:relative;box-sizing:border-box;width:calc(100vw - 24px);padding:4px 58px 5px 7px;min-height:54px;border:1px solid rgba(124,203,255,.76);border-radius:6px;background:rgba(8,27,58,.72);box-shadow:0 0 8px rgba(88,191,255,.14);text-align:center}
#gv-travel-course,#gv-travel-heading{font:400 13px/1.05 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.55px;color:#EAF8FF;text-align:center;text-shadow:0 0 4px rgba(88,191,255,.20)}
#gv-travel-course{font:400 16px/1.08 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.35px;color:#7CCBFF;text-shadow:0 0 7px rgba(88,191,255,.58)}
#gv-travel-heading{margin-top:1px;color:#A9DFFF}
#gv-travel-destination{margin-top:2px;font:400 16px/1.08 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.35px;color:#7CCBFF;text-shadow:0 0 7px rgba(88,191,255,.58);text-align:center;white-space:normal;overflow-wrap:anywhere}
#gv-travel-distance{box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;width:172px;height:34px;padding:2px 6px 1px;border:1px solid rgba(124,203,255,.78);border-radius:5px;background:rgba(8,27,58,.76);color:#78FFAB;text-align:center;text-shadow:0 0 4px rgba(229,255,239,.82),0 0 9px rgba(87,255,147,.34);white-space:nowrap}
#gv-travel-distance-value{position:relative;display:block;width:100%;height:18px;font:400 17px/18px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.32px;text-align:center;font-variant-numeric:tabular-nums}
#gv-travel-distance-integer{position:absolute;right:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:right;white-space:nowrap}
#gv-travel-distance-decimal{position:absolute;left:50%;top:0;width:6px;height:18px;transform:translateX(-50%);font:inherit;letter-spacing:0;text-align:center;white-space:nowrap}
#gv-travel-distance-fraction{position:absolute;left:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:left;white-space:nowrap}
#gv-travel-distance-unit{display:block;width:100%;height:12px;font:400 10.5px/12px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.45px;text-align:center;white-space:nowrap}
/* ============================================================ */
/* ECO-027B-1 HD / ARCHIVE PRESENTATION — OWNER 0034          */
/* ============================================================ */
#gv-random-galaxy{border:2px solid #7CCBFF!important;box-shadow:none!important;filter:brightness(1.10)}.gv-galaxy-history{border:2px solid #7CCBFF!important;box-shadow:none!important;filter:brightness(1.10);opacity:1!important}.gvrg-hd-science,.gvrg-hd-viewport,#gv-hd-info-panel{box-sizing:border-box!important;width:min(680px,calc(100vw - 20px))!important;border:0!important;border-radius:8px!important;position:absolute!important}.gvrg-hd-science::before,.gvrg-hd-viewport::before,#gv-hd-info-panel::before{content:""!important;position:absolute!important;inset:0!important;z-index:50!important;border-radius:8px!important;padding:1px!important;background:linear-gradient(135deg,#DDF8FF 0%,#8DDAFF 28%,#58BFFF 55%,#296DBD 100%)!important;-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0)!important;-webkit-mask-composite:xor!important;mask-composite:exclude!important;pointer-events:none!important;box-sizing:border-box!important}.gvrg-hd-science,#gv-hd-info-panel{background:transparent!important;box-shadow:inset 0 0 6px rgba(225,248,255,.06),0 0 8px rgba(124,203,255,.20)!important}.gvrg-hd-science{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;overflow:hidden!important;pointer-events:none!important}.gvrg-hd-science .gvrg-hd-science-item{padding:8px 8px!important}.gvrg-hd-science .gvrg-hd-science-value{font-size:10.5px!important}.gvrg-hd-viewport{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;aspect-ratio:1/1!important;height:auto!important;overflow:hidden!important;background:#02070F!important;box-shadow:inset 0 0 6px rgba(225,248,255,.08),0 0 8px rgba(124,203,255,.24)!important;pointer-events:auto!important}.gvrg-hd-viewport>img:not(#gv-hd-archive-button img){width:100%!important;height:100%!important;max-width:none!important;max-height:none!important;object-fit:contain!important;object-position:50% 50%;scale:1!important}.gvrg-hd-scale,.gvrg-hd-scale-label{font-size:13.5px!important}#gv-hd-info-panel{position:absolute;left:50%;z-index:4;transform:translateX(-50%);padding:9px 11px 10px;color:#DDF8FF;font:400 10.5px/1.45 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.42px;text-align:left;text-shadow:0 0 4px rgba(88,191,255,.22);display:flex;flex-direction:column;overflow:hidden;pointer-events:none}#gv-hd-info-title{flex:0 0 auto;margin-bottom:6px;color:#7CCBFF;font-size:12px;letter-spacing:.75px;text-align:center}#gv-hd-info-body{flex:1 1 auto;min-height:0;overflow:hidden;overflow-wrap:anywhere}.gvrg-credit{display:none!important}#gv-hd-control-row{position:absolute!important;left:11px!important;right:11px!important;bottom:10px!important;z-index:30!important;height:40px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;box-sizing:border-box!important;pointer-events:none!important}#gv-hd-control-row>.gvrg-back-button,#gv-hd-control-row>#gv-hd-download-button{position:static!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;flex:1 1 0!important;width:0!important;min-width:0!important;max-width:none!important;height:40px!important;min-height:40px!important;margin:0!important;padding:0 8px!important;gap:7px!important;box-sizing:border-box!important;align-items:center!important;justify-content:center!important;white-space:nowrap!important;overflow:hidden!important;font-size:10.5px!important;line-height:1!important;pointer-events:auto!important;touch-action:manipulation!important}#gv-hd-control-row>.gvrg-back-button>span:last-child,#gv-hd-control-row>#gv-hd-download-button>span:last-child{min-width:0!important;white-space:nowrap!important;overflow:visible!important;line-height:1!important}#gv-hd-control-row .gvrg-back-chevron,#gv-hd-control-row .gvrg-download-icon{width:18px!important;height:18px!important;flex:0 0 18px!important}#gv-hd-archive-button{position:absolute!important;left:auto!important;right:12px!important;top:auto!important;bottom:12px!important;z-index:60!important;flex:0 0 48px!important;width:48px!important;height:48px!important;margin:0!important;padding:2px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;box-sizing:border-box!important;border:2px solid transparent!important;border-radius:6px!important;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98)) padding-box,linear-gradient(145deg,#DDF8FF 0%,#7CCBFF 48%,#296DBD 100%) border-box!important;box-shadow:inset 0 0 6px rgba(225,248,255,.18),0 0 8px rgba(124,203,255,.40),0 0 13px rgba(41,109,189,.20)!important;filter:none!important;overflow:hidden!important;pointer-events:auto!important;touch-action:manipulation!important}#gv-hd-archive-button img{display:block!important;width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;object-position:50% 50%!important;margin:0!important;padding:0!important;border:0!important;border-radius:4px!important;background:transparent!important;box-shadow:none!important}#gv-hd-archive-button .gv-hd-archive-comet{position:absolute;inset:4px;border-radius:50%;opacity:0;pointer-events:none;transform-origin:50% 50%}#gv-hd-archive-button .gv-hd-archive-comet::before{content:"";position:absolute;left:50%;top:-1px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#F8FFFF;box-shadow:0 0 4px #FFFFFF,0 0 8px #8FE5FF,0 0 12px #296DBD}#gv-hd-archive-button .gv-hd-archive-comet::after{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 250deg,rgba(15,54,122,0) 0deg,rgba(91,184,255,.22) 42deg,rgba(143,229,255,.56) 82deg,rgba(248,255,255,.92) 110deg,transparent 111deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));filter:drop-shadow(0 0 2px rgba(143,229,255,.72))}#gv-hd-archive-button.gv-archive-loading .gv-hd-archive-comet{opacity:1;animation:gvHdArchiveOrbit 1s linear infinite}@keyframes gvHdArchiveOrbit{to{transform:rotate(360deg)}}#gv-hd-download-button{border:2px solid #7CCBFF!important;border-radius:6px!important;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98))!important;color:#EAF8FF!important;box-shadow:none!important;filter:none!important}#gv-hd-download-button *{color:#EAF8FF!important;fill:#EAF8FF!important;stroke:#EAF8FF!important}#gv-hd-download-button .gvrg-download-icon{filter:drop-shadow(0 0 3px rgba(225,248,255,.92))!important}#gv-hd-download-button .gvrg-download-arrow{top:1px!important;width:3px!important;height:10px!important;background:#F7FDFF!important;border-radius:1px!important;box-shadow:0 0 3px rgba(225,248,255,.88)!important}#gv-hd-download-button .gvrg-download-arrow::after{bottom:-1px!important;width:8px!important;height:8px!important;border-right:3px solid #EAF8FF!important;border-bottom:3px solid #EAF8FF!important}#gv-hd-download-button .gvrg-download-bar{width:14px!important;height:3px!important;background:#F7FDFF!important;box-shadow:0 0 4px rgba(225,248,255,.92)!important}#gv-archive-overlay{position:fixed;inset:0;z-index:2147483000;background:#000;display:block;visibility:hidden;opacity:0;pointer-events:none}#gv-archive-overlay.gv-open{visibility:visible;opacity:1;pointer-events:auto}#gv-archive-frame{position:absolute;inset:0;width:100%;height:100%;border:0;background:#000;touch-action:auto!important;-webkit-overflow-scrolling:touch}#gv-archive-back{position:fixed;left:50%;bottom:max(18px,env(safe-area-inset-bottom));z-index:2147483647;transform:translateX(-50%);display:inline-flex;align-items:center;justify-content:center;gap:10px;height:48px;padding:0 12px;border:2px solid #7CCBFF;border-radius:7px;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98));color:#EAF8FF;font:400 13px/1 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.55px;text-transform:uppercase;white-space:nowrap;box-shadow:0 0 12px rgba(0,0,0,.75);pointer-events:auto;touch-action:manipulation;cursor:pointer}#gv-archive-arrow{position:relative;display:inline-flex;width:36px;height:36px;flex:0 0 36px;align-items:center;justify-content:center}#gv-archive-arrow::before,#gv-archive-arrow::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;box-sizing:border-box;pointer-events:none}#gv-archive-arrow::before{border-width:6px;border-color:#7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.90));transform:translate(-38%,-50%) rotate(-135deg)}#gv-archive-arrow::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-34%,-50%) rotate(-135deg)}#gv-archive-target-tile{box-sizing:border-box;width:36px;height:36px;flex:0 0 36px;display:inline-flex;align-items:center;justify-content:center;border:2px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98));overflow:hidden}#gv-archive-target-tile img{display:block;width:28px;height:28px;object-fit:contain;flex:0 0 28px;margin:0;padding:0;border:0}


/* ============================================================
   REQ-026 / ECO-027B-2 — GALACTIC ICE VISUAL SYSTEM
   OWNER: gv-random-galaxy-0124.js
   ============================================================ */

.gvrg-card{
  border:2px solid transparent;
  background:
    linear-gradient(145deg,
      rgba(8,27,58,.97) 0%,
      rgba(11,49,119,.94) 40%,
      rgba(20,132,219,.84) 74%,
      rgba(41,109,189,.92) 100%
    ) padding-box,
    linear-gradient(135deg,
      #DDF8FF 0%,
      #8DDAFF 28%,
      #58BFFF 58%,
      #296DBD 100%
    ) border-box;
  box-shadow:
    inset 0 0 9px rgba(221,248,255,.12),
    0 0 9px rgba(88,191,255,.34),
    0 0 16px rgba(41,109,189,.20)
}

.gvrg-science-grid{
  border-color:rgba(124,203,255,.44)
}

.gvrg-row{
  border-color:rgba(88,191,255,.38)
}

.gvrg-label{
  color:#9BE5FF;
  text-shadow:
    0 0 4px rgba(221,248,255,.28),
    0 0 7px rgba(88,191,255,.42)
}

.gvrg-value{
  color:#F7FDFF;
  text-shadow:0 0 4px rgba(205,238,255,.24)
}

.gvrg-status,
.gvrg-distance{
  border:1px solid transparent;
  background:
    linear-gradient(145deg,
      rgba(8,27,58,.95),
      rgba(11,49,119,.88) 48%,
      rgba(20,132,219,.68) 78%,
      rgba(41,109,189,.80)
    ) padding-box,
    linear-gradient(135deg,
      #DDF8FF,
      #58BFFF 58%,
      #296DBD
    ) border-box;
  box-shadow:
    inset 0 0 7px rgba(221,248,255,.09),
    0 0 8px rgba(88,191,255,.24)
}

.gvrg-status-kicker{
  color:#9BE5FF
}

.gvrg-status-heading{
  color:#DDF8FF
}

.gvrg-status-destination{
  color:#7CCBFF;
  text-shadow:0 0 9px rgba(88,191,255,.68)
}

.gvrg-progress{
  background:rgba(124,203,255,.14)
}

.gvrg-progress-fill{
  background:
    linear-gradient(90deg,
      #296DBD 0%,
      #58BFFF 58%,
      #DDF8FF 100%
    );
  box-shadow:0 0 8px rgba(88,191,255,.72)
}

#gv-random-galaxy,
.gv-galaxy-history{
  border:2px solid transparent!important;
  background:
    linear-gradient(145deg,
      #081B3A 0%,
      #0B3177 40%,
      #1484DB 74%,
      #296DBD 100%
    ) padding-box,
    linear-gradient(135deg,
      #296DBD 0%,
      #58BFFF 38%,
      #8DDAFF 70%,
      #F4FDFF 100%
    ) border-box!important;
  box-shadow:
    inset 0 0 8px rgba(221,248,255,.14),
    0 0 9px rgba(88,191,255,.34)!important;
  filter:brightness(1.04)!important
}

#gv-random-galaxy{
  color:#EAF8FF;
  text-shadow:0 0 5px rgba(221,248,255,.54)
}

.gv-galaxy-history::before{
  border-color:#7CCBFF;
  filter:drop-shadow(0 0 4px rgba(88,191,255,.86))
}

#gv-travel-primary{
  border:1px solid transparent;
  background:
    linear-gradient(145deg,
      rgba(8,27,58,.95),
      rgba(11,49,119,.90) 50%,
      rgba(20,132,219,.70)
    ) padding-box,
    linear-gradient(135deg,
      #DDF8FF,
      #58BFFF 58%,
      #296DBD
    ) border-box;
  box-shadow:
    inset 0 0 7px rgba(221,248,255,.08),
    0 0 8px rgba(88,191,255,.24)
}

#gv-travel-course,
#gv-travel-destination{
  color:#7CCBFF;
  text-shadow:0 0 7px rgba(88,191,255,.62)
}

#gv-travel-heading{
  color:#A9DFFF
}

#gv-travel-distance{
  border:1px solid transparent;
  background:
    linear-gradient(145deg,
      rgba(8,27,58,.96),
      rgba(11,49,119,.90),
      rgba(41,109,189,.78)
    ) padding-box,
    linear-gradient(135deg,
      #DDF8FF,
      #58BFFF,
      #296DBD
    ) border-box
}

/* Travel distance text uses the approved green navigation palette. */

#gv-universe-context .gv-universe-label,
#gv-we-are-here .gv-home-label{
  border:1px solid transparent;
  background:
    linear-gradient(145deg,
      rgba(8,27,58,.94),
      rgba(11,49,119,.88),
      rgba(41,109,189,.78)
    ) padding-box,
    linear-gradient(135deg,
      #DDF8FF,
      #58BFFF,
      #296DBD
    ) border-box;
  box-shadow:
    inset 0 0 7px rgba(221,248,255,.09),
    0 0 8px rgba(88,191,255,.24)
}

#gv-universe-context .gv-universe-count,
#gv-we-are-here .gv-home-origin{
  color:#7CCBFF
}

#gv-we-are-here .gv-home-sub{
  color:#CDEEFF
}

#gv-we-are-here .gv-home-hint{
  color:#A6DFFF
}

.gvrg-hd-primary{
  border-color:#7CCBFF;
  background:
    linear-gradient(145deg,
      #081B3A,
      #0B3177 40%,
      #1484DB 74%,
      #296DBD
    );
  color:#EAF8FF;
  text-shadow:0 0 4px rgba(221,248,255,.72);
  box-shadow:
    inset 0 0 7px rgba(221,248,255,.14),
    0 0 8px rgba(88,191,255,.34)
}

.gvrg-hd-science{
  background:
    linear-gradient(145deg,
      rgba(8,27,58,.96),
      rgba(11,49,119,.92) 48%,
      rgba(20,132,219,.72) 78%,
      rgba(41,109,189,.82)
    )!important;
  box-shadow:
    inset 0 0 7px rgba(221,248,255,.08),
    0 0 9px rgba(88,191,255,.26)!important
}

.gvrg-hd-science-item{
  border-color:rgba(88,191,255,.38)
}

.gvrg-hd-science-label{
  color:#9BE5FF;
  text-shadow:0 0 5px rgba(88,191,255,.56)
}

.gvrg-hd-science-value{
  color:#F7FDFF;
  text-shadow:0 0 4px rgba(205,238,255,.24)
}

#gv-hd-info-panel{
  background:
    linear-gradient(145deg,
      rgba(8,27,58,.96),
      rgba(11,49,119,.92) 48%,
      rgba(20,132,219,.72) 78%,
      rgba(41,109,189,.82)
    )!important;
  color:#DDF8FF!important;
  text-shadow:0 0 4px rgba(88,191,255,.28)!important;
  box-shadow:
    inset 0 0 7px rgba(221,248,255,.08),
    0 0 9px rgba(88,191,255,.26)!important
}

#gv-hd-info-title{
  color:#9BE5FF!important
}

.gvrg-back-button,
#gv-archive-back{
  border-color:#7CCBFF!important;
  background:
    linear-gradient(145deg,
      #081B3A,
      #0B3177 40%,
      #1484DB 74%,
      #296DBD
    )!important;
  color:#EAF8FF!important;
  text-shadow:0 0 4px rgba(221,248,255,.68)
}

.gvrg-back-chevron::before,
#gv-archive-arrow::before{
  border-color:#7CCBFF!important;
  filter:drop-shadow(0 0 4px rgba(88,191,255,.86))!important
}

#gv-archive-target-tile{
  border-color:#7CCBFF!important;
  background:
    linear-gradient(145deg,
      #081B3A,
      #0B3177 40%,
      #1484DB 74%,
      #296DBD
    )!important
}
`;
      return style;
    }

    #build() {
      const root = document.createElement('div');
      root.className = 'gvrg-root';
      root.setAttribute('data-gvrg-version', VERSION);
      const style = this.#style();

      const status = document.createElement('div');
      status.className = 'gvrg-status';
      status.setAttribute('role', 'status');
      status.setAttribute('aria-live', 'polite');
      this.statusEl = status;

      const distance = document.createElement('div');
      distance.className = 'gvrg-distance';
      this.distanceBox = distance;
      const distanceLabel = document.createElement('div');
      distanceLabel.className = 'gvrg-distance-label';
      distanceLabel.textContent = 'DISTANCE TRAVELED';
      const distanceNumberHost = document.createElement('div');
      this.distanceNumberHost = distanceNumberHost;
      const route = document.createElement('div');
      route.className = 'gvrg-route';
      this.routeEl = route;
      const progress = document.createElement('div');
      progress.className = 'gvrg-progress';
      const progressFill = document.createElement('div');
      progressFill.className = 'gvrg-progress-fill';
      this.progressFill = progressFill;
      progress.appendChild(progressFill);
      distance.append(distanceLabel, distanceNumberHost, route, progress);

      const card = document.createElement('div');
      card.className = 'gvrg-card';
      this.card = card;
      const name = document.createElement('div');
      name.className = 'gvrg-name';
      this.nameEl = name;

      const makeRow = (label) => {
        const row = document.createElement('div');
        row.className = 'gvrg-row';
        const key = document.createElement('div');
        key.className = 'gvrg-label';
        key.textContent = label;
        const value = document.createElement('div');
        value.className = 'gvrg-value';
        row.append(key, value);
        return { row, value };
      };

      const scienceGrid = document.createElement('div');
      scienceGrid.className = 'gvrg-science-grid';
      const designationRow = makeRow('DESIGNATION');
      this.designationValueEl = designationRow.value;
      const commonNameRow = makeRow('NAME / PSEUDO');
      this.commonNameValueEl = commonNameRow.value;
      const distanceRow = makeRow('DISTANCE');
      distanceRow.value.classList.add('gvrg-card-distance');
      const distanceNumber = document.createElement('span');
      distanceNumber.className = 'gvrg-value-number';
      this.distanceValueNumberEl = distanceNumber;
      const distanceUnit = document.createElement('span');
      distanceUnit.className = 'gvrg-value-unit';
      this.distanceValueUnitEl = distanceUnit;
      distanceRow.value.append(distanceNumber, distanceUnit);
      const constellationRow = makeRow('CONSTELLATION');
      this.constellationValueEl = constellationRow.value;
      const ageRow = makeRow('AGE');
      this.ageValueEl = ageRow.value;
      const sizeRow = makeRow('IMAGE SIZE');
      this.sizeValueEl = sizeRow.value;
      scienceGrid.append(designationRow.row, commonNameRow.row, distanceRow.row, constellationRow.row, ageRow.row, sizeRow.row);

      const actions = document.createElement('div');
      actions.className = 'gvrg-actions';
      const viewHd = document.createElement('button');
      viewHd.type = 'button';
      viewHd.className = 'gvrg-button gvrg-hd-primary';
      viewHd.textContent = 'VIEW HD IMAGE';
      this.viewHdButton = viewHd;
      const providerIconButton = document.createElement('button');
      providerIconButton.type = 'button';
      providerIconButton.className = 'gvrg-button gvrg-hd-icon-button';
      providerIconButton.setAttribute('aria-label', 'VIEW HD IMAGE');
      const providerIcon = document.createElement('img');
      providerIcon.alt = '';
      providerIcon.setAttribute('aria-hidden', 'true');
      providerIconButton.appendChild(providerIcon);
      this.providerIconButton = providerIconButton;
      actions.append(viewHd, providerIconButton);
      card.append(name, scienceGrid, actions);

      const hd = document.createElement('div');
      hd.className = 'gvrg-hd';
      this.hdOverlay = hd;
      const viewport = document.createElement('div');
      viewport.className = 'gvrg-hd-viewport';
      this.hdViewport = viewport;
      const hdImage = document.createElement('img');
      hdImage.alt = '';
      this.hdFallbackImage = hdImage;
      this.hdImage = hdImage;
      const scaleBar = document.createElement('div');
      scaleBar.className = 'gvrg-hd-scale';
      this.hdScaleBar = scaleBar;
      const scaleLine = document.createElement('div');
      scaleLine.className = 'gvrg-hd-scale-line';
      this.hdScaleLine = scaleLine;
      const scaleLabel = document.createElement('div');
      scaleLabel.className = 'gvrg-hd-scale-label';
      this.hdScaleLabel = scaleLabel;
      scaleBar.append(scaleLabel, scaleLine);
      viewport.append(hdImage, scaleBar);
      const loading = document.createElement('div');
      loading.className = 'gvrg-hd-loading';
      loading.textContent = 'LOADING HD IMAGE';
      this.hdLoading = loading;

      const hdScience = document.createElement('div');
      hdScience.className = 'gvrg-hd-science';
      hdScience.setAttribute('aria-label', 'GALAXY INFORMATION');
      const makeHdScienceItem = (label) => {
        const item = document.createElement('div');
        item.className = 'gvrg-hd-science-item';
        const key = document.createElement('div');
        key.className = 'gvrg-hd-science-label';
        key.textContent = label;
        const value = document.createElement('div');
        value.className = 'gvrg-hd-science-value';
        item.append(key, value);
        return { item, value };
      };
      const hdDesignation = makeHdScienceItem('DESIGNATION');
      this.hdDesignationValueEl = hdDesignation.value;
      const hdCommonName = makeHdScienceItem('NAME / PSEUDONYM');
      this.hdCommonNameValueEl = hdCommonName.value;
      const hdDistance = makeHdScienceItem('DISTANCE');
      this.hdDistanceValueEl = hdDistance.value;
      const hdAge = makeHdScienceItem('AGE');
      this.hdAgeValueEl = hdAge.value;
      const hdSize = makeHdScienceItem('IMAGE SIZE');
    const hdSizeFovSub = document.createElement('span');
    hdSizeFovSub.className = 'gvrg-fov-sub';
    hdSizeFovSub.textContent = '(FOV)';
    hdSize.item.querySelector('.gvrg-hd-science-label').append(document.createElement('br'), hdSizeFovSub);
      this.hdSizeValueEl = hdSize.value;
      hdScience.append(hdDesignation.item, hdCommonName.item, hdDistance.item, hdAge.item, hdSize.item);
      this.hdScience = hdScience;

      const footer = document.createElement('div');
      footer.className = 'gvrg-hd-footer';
      this.hdFooter = footer;
      const credit = document.createElement('div');
      credit.className = 'gvrg-credit';
      this.creditEl = credit;
      const controls = document.createElement('div');
      controls.className = 'gvrg-hd-controls';
      const download = document.createElement('button');
      download.type = 'button';
      download.className = 'gvrg-button gvrg-download-button';
      const downloadIcon = document.createElement('span');
      downloadIcon.className = 'gvrg-download-icon';
      downloadIcon.setAttribute('aria-hidden', 'true');
      const downloadArrow = document.createElement('span');
      downloadArrow.className = 'gvrg-download-arrow';
      const downloadBar = document.createElement('span');
      downloadBar.className = 'gvrg-download-bar';
      downloadIcon.append(downloadArrow, downloadBar);
      const downloadLabel = document.createElement('span');
      downloadLabel.textContent = 'DOWNLOAD IMAGE';
      download.append(downloadIcon, downloadLabel);
      this.downloadButton = download;
      const back = document.createElement('button');
      back.type = 'button';
      back.className = 'gvrg-button gvrg-back-button';
      const backChevron = document.createElement('span');
      backChevron.className = 'gvrg-back-chevron';
      backChevron.setAttribute('aria-hidden', 'true');
      const backLabel = document.createElement('span');
      backLabel.textContent = 'BACK TO SKY';
      back.append(backChevron, backLabel);
      this.backButton = back;
      controls.append(download, back);
      footer.append(credit, controls);
      hd.append(viewport, loading, hdScience, footer);
      root.append(style, status, distance, card, hd);
      return root;
    }

    async #initialize() {
      await ensureFonts();
      this.#buildHomePresentation();
      await this.distanceRenderer.calibrate();
      if (this.options.prefetch) {
        this.#setStatus('FINDING GALAXY');
        this.prefetch().then(() => this.#setStatus('READY')).catch(() => this.#setStatus('READY'));
      } else this.#setStatus('READY');
      return this;
    }

    #setStatus(message) {
      const text = cleanText(message);
      if (this.statusEl) {
        this.statusEl.classList.remove('gvrg-status-travel');
        this.statusEl.textContent = text;
        const visible = /^GALAXY UNAVAILABLE/i.test(text);
        this.statusEl.classList.toggle('gvrg-status-visible', visible);
      }
      if (this.onStatus) this.onStatus(text, this);
    }
    #setTravelStatus(destinationName) {
      const destination = cleanText(destinationName).toUpperCase();
      if (this.statusEl) {
        const kicker = document.createElement('div');
        kicker.className = 'gvrg-status-kicker';
        kicker.textContent = 'COURSE LOCKED';
        const heading = document.createElement('div');
        heading.className = 'gvrg-status-heading';
        heading.textContent = 'HEADING TO';
        const destinationEl = document.createElement('div');
        destinationEl.className = 'gvrg-status-destination';
        destinationEl.textContent = destination;
        this.statusEl.replaceChildren(kicker, heading, destinationEl);
        this.statusEl.classList.add('gvrg-status-travel', 'gvrg-status-visible');
      }
      if (this.onStatus) this.onStatus(`COURSE LOCKED — HEADING TO ${destination}`, this);
    }
    #handleError(error) {
      const normalized = error instanceof Error ? error : new Error(String(error));
      this.#setStatus('GALAXY UNAVAILABLE — TRY AGAIN');
      if (this.onError) this.onError(normalized, this);
      else console.error('[GalaxyRandomGalaxy]', normalized);
    }

    async #fetchJsonEndpoint(endpoint, payload) {
      if (!endpoint) throw new Error('No endpoint configured.');
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload || {})
      });
      if (!response.ok) throw new Error(`Endpoint returned HTTP ${response.status}.`);
      return response.json();
    }

    async #getProviderCandidate(excludeName) {
      if (!this.provider) throw new Error('Random Galaxy 0062 requires a local galaxy provider.');
      const raw = await this.provider({ excludeName: cleanText(excludeName), module: this });
      return this.#normalizeProviderCandidate(raw && raw.destination ? raw.destination : raw);
    }

    #normalizeProviderCandidate(candidate) {
      if (!candidate || typeof candidate !== 'object') throw new Error('Galaxy provider returned no destination.');
      const name = cleanText(candidate.name || candidate.objectName);
      // AR118 AUTHORITY CONTRACT:
      // Catalog RA/Dec/FoV/rotation are NEVER navigation authority.
      // These four values must already have been extracted from the actual
      // prefetched AVM image before the destination can become READY.
      const ra = finiteNumber(candidate.avmRa);
      const dec = finiteNumber(candidate.avmDec);
      const fovDegrees = finiteNumber(candidate.avmVerticalFovDegrees);
      const avmHorizontalFovDegrees = finiteNumber(candidate.avmHorizontalFovDegrees);
      const aladinRotation = finiteNumber(candidate.avmCameraRotation);
      const avmRotation = finiteNumber(candidate.avmRotation);
      const avmCallbackFov = finiteNumber(candidate.avmCallbackFov);
      const avmAuthorityUrl = cleanText(candidate.avmAuthorityUrl);
      const avmAuthorityWcs =
        candidate.avmAuthorityWcs &&
        typeof candidate.avmAuthorityWcs==='object'
          ? Object.freeze({...candidate.avmAuthorityWcs})
          : null;
      const distance = finiteNumber(candidate.distance ?? candidate.distanceMly ?? candidate.distance_mly);
      const constellation = cleanText(candidate.constellation);
      const age = cleanText(candidate.age ?? candidate.ageEstimate ?? candidate.age_estimate ?? '');
      const ageYears = finiteNumber(candidate.ageYears ?? candidate.age_years);
      const physicalSizeLy = candidate.physicalSizeLy ?? candidate.physical_size_ly ?? null;
      const designation = cleanText(candidate.designation);
      const commonName = cleanText(candidate.commonName ?? candidate.common_name ?? candidate.displayName ?? name);
      const preparedHdUrl = cleanText(candidate.preparedHdUrl ?? candidate.prepared_hd_url);
      const preparedSource = cleanText(candidate.preparedSource ?? candidate.prepared_source);
      const preparedHdImage = candidate.preparedHdImage instanceof HTMLImageElement ? candidate.preparedHdImage : null;
      const hdUrl = validHttpsUrl(candidate.hdUrl || candidate.hd_url);
      const sourceUrl = validHttpsUrl(candidate.sourceUrl || candidate.source_url);
      const imageType = cleanText(candidate.imageType || candidate.image_type);
      const category = cleanText(candidate.category);
      const provider = cleanText(candidate.provider);
      const telescope = cleanText(candidate.telescope || candidate.facility);
      const credit = cleanText(candidate.credit);
      if (!name) throw new Error('Galaxy destination is missing its galaxy name.');
      if (ra == null || ra < 0 || ra >= 360) throw new Error('Galaxy destination has no valid runtime AVM RA.');
      if (dec == null || dec < -90 || dec > 90) throw new Error('Galaxy destination has no valid runtime AVM Dec.');
      if (distance == null || distance <= 0) throw new Error('Galaxy destination has no usable distance.');
      if (!constellation) throw new Error('Galaxy destination has no constellation.');
      if (fovDegrees == null || fovDegrees <= 0) throw new Error('Galaxy destination has no usable runtime AVM vertical FoV.');
      if (avmHorizontalFovDegrees == null || avmHorizontalFovDegrees <= 0) throw new Error('Galaxy destination has no usable runtime AVM horizontal FoV.');
      if (aladinRotation == null || avmRotation == null) throw new Error('Galaxy destination has no usable runtime AVM rotation.');
      if (!avmAuthorityWcs || !Number.isFinite(Number(avmAuthorityWcs.CRVAL1)) || !Number.isFinite(Number(avmAuthorityWcs.CRVAL2)) || !Number.isFinite(Number(avmAuthorityWcs.CRPIX1)) || !Number.isFinite(Number(avmAuthorityWcs.CRPIX2))) throw new Error('Galaxy destination has no complete runtime AVM WCS.');
      if (!hdUrl) throw new Error('Galaxy destination has no valid HTTPS HD asset.');
      if (!sourceUrl) throw new Error('Galaxy destination has no valid HTTPS source page.');
      if (imageType && rejectNonObservationLabel(imageType)) throw new Error('Rejected non-observation galaxy entry.');
      if (category && !/galax/i.test(category)) throw new Error('Rejected non-galaxy entry.');
      return Object.freeze({
        source: cleanText(candidate.source || 'GALAXY PROVIDER'),
        name, ra, dec, distance, constellation, age, ageYears, physicalSizeLy, designation, commonName, preparedHdUrl, preparedSource, preparedHdImage,
        fovDegrees, aladinRotation, avmRotation, avmCallbackFov, avmAuthorityUrl, avmAuthorityWcs,
        avmRa:ra, avmDec:dec, avmHorizontalFovDegrees, avmVerticalFovDegrees:fovDegrees, avmCameraRotation:aladinRotation,
        hdUrl: hdUrl.href,
        sourceUrl: sourceUrl.href,
        credit,
        imageType: imageType || 'Observation',
        category: category || 'Galaxies',
        provider,
        telescope,
        archiveId: cleanText(candidate.archiveId || candidate.id)
      });
    }

    async prefetch() {
      if (this.destroyed) return null;
      if (this.prefetchedDestination) return this.prefetchedDestination;
      if (this.prefetchPromise) return this.prefetchPromise;
      const excludeName = this.currentGalaxy && this.currentGalaxy.name;
      this.prefetchPromise = this.#getProviderCandidate(excludeName)
        .then((destination) => { this.prefetchedDestination = destination; return destination; })
        .finally(() => { this.prefetchPromise = null; });
      return this.prefetchPromise;
    }

    async #consumeDestination() {
      if (this.prefetchedDestination) {
        const destination = this.prefetchedDestination;
        this.prefetchedDestination = null;
        return destination;
      }
      if (this.prefetchPromise) {
        try {
          const destination = await this.prefetchPromise;
          this.prefetchedDestination = null;
          return destination;
        } catch (_) { this.prefetchedDestination = null; }
      }
      return this.#getProviderCandidate(this.currentGalaxy && this.currentGalaxy.name);
    }

    #isHomeDeparture(source, startFov) {
      return !(finiteNumber(source && source.distance) > 0) && Number(startFov) >= 300;
    }
    #showDistance(source, destination, route) {
      this.routeEl.textContent = route.exactRoute ? `${source.name.toUpperCase()} TO ${destination.name.toUpperCase()}` : `TO ${destination.name.toUpperCase()}`;
      this.distanceRenderer.render(0);
      if (this.progressFill) this.progressFill.style.width = '0%';
      this.distanceBox.style.opacity = '1';
    }
    #hideDistance() { this.distanceBox.style.opacity = '0'; }
    #hideCard() { this.card.classList.remove('gvrg-card-visible'); }

    // RANDOM 0134: safe presentation-only preview. No Aladin viewport writes.
    previewDestination(destination) {
      if (!destination) return false;
      this.activeDestination = destination;
      this.#showCard(destination);
      try {
        const explicit=String(
          destination?.providerIconUrl ||
          destination?.provider_icon_url ||
          ""
        ).trim();

        const evidence=[
          destination?.provider,
          destination?.telescope,
          destination?.source,
          destination?.hdUrl,
          destination?.sourceUrl
        ].map(value=>String(value||"").trim().toLowerCase())
         .filter(Boolean)
         .join(" ");

        let slug="";
        if(/(?:^|[^a-z0-9])(?:hubble|hst|esahubble)(?:[^a-z0-9]|$)/i.test(evidence))
          slug="hubble";
        else if(/(?:^|[^a-z0-9])(?:jwst|james webb|webb|esawebb)(?:[^a-z0-9]|$)/i.test(evidence))
          slug="jwst";
        else if(/(?:^|[^a-z0-9])spitzer(?:[^a-z0-9]|$)/i.test(evidence))
          slug="spitzer";
        else if(/(?:^|[^a-z0-9])chandra(?:[^a-z0-9]|$)/i.test(evidence))
          slug="chandra";

        const iconUrl=/^https:\/\//i.test(explicit)
          ? explicit
          : slug
            ? `https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/providers/${slug}/${slug}-icon.png`
            : "";

        const img=this.providerIconButton?.querySelector("img");

        if(img){
          img.onerror=null;
          if(iconUrl){
            img.src=iconUrl;
            img.onerror=()=>{
              img.onerror=null;
              img.removeAttribute("src");
            };
          }else{
            img.removeAttribute("src");
          }
        }
      } catch (_) {}
      return true;
    }

    #showCard(destination) {
      this.nameEl.textContent = destination.name.toUpperCase();
      this.designationValueEl.textContent = cleanText(destination.designation).toUpperCase();
      this.commonNameValueEl.textContent = cleanText(destination.commonName || destination.name).toUpperCase();
      const d=finiteNumber(destination.distance);
      const dUnit=d>=1?'MLY':d>=0.001?'KLY':'LY';
      const dScale=dUnit==='MLY'?1:dUnit==='KLY'?1000:1000000;
      const dLabel=this.distanceValueNumberEl.closest('.gvrg-row')?.querySelector('.gvrg-label');
      if(dLabel)dLabel.textContent=`DISTANCE (${dUnit})`;
      this.distanceValueNumberEl.textContent=d>0?Math.round(d*dScale).toLocaleString('en-US'):'';
      this.distanceValueUnitEl.textContent='';

      this.constellationValueEl.textContent=cleanText(destination.constellation).toUpperCase();

      let age=finiteNumber(destination.ageYears);
      if(!(age>0)){
        const raw=cleanText(destination.age).toUpperCase();
        const m=raw.match(/([0-9]+(?:\.[0-9]+)?)/);
        if(m){age=Number(m[1]);if(/BILLION/.test(raw))age*=1e9;else if(/MILLION/.test(raw))age*=1e6;else if(/THOUSAND/.test(raw))age*=1e3;}
      }
      const aUnit=age>=1e9?'BY':age>=1e6?'MY':age>=1e3?'KY':'Y';
      const aScale=aUnit==='BY'?1e9:aUnit==='MY'?1e6:aUnit==='KY'?1e3:1;
      const aLabel=this.ageValueEl.closest('.gvrg-row')?.querySelector('.gvrg-label');
      if(aLabel)aLabel.textContent=`AGE (${aUnit})`;
      this.ageValueEl.textContent=age>0?Math.round(age/aScale).toLocaleString('en-US'):'';

      const rawSize=Array.isArray(destination.physicalSizeLy)?destination.physicalSizeLy.slice(0,2):[destination.physicalSizeLy];
      const dims=rawSize.map(finiteNumber).filter(v=>v!=null&&v>0);
      const minDim=dims.length?Math.min(...dims):0;
      const sUnit=minDim>=1e6?'MLY':minDim>=1e3?'KLY':'LY';
      const sScale=sUnit==='MLY'?1e6:sUnit==='KLY'?1e3:1;
      const sLabel=this.sizeValueEl.closest('.gvrg-row')?.querySelector('.gvrg-label');
      if(sLabel)sLabel.textContent=`IMAGE SIZE (${sUnit})`;
      this.sizeValueEl.textContent=dims.map(v=>Math.round(v/sScale).toLocaleString('en-US')).join(' × ');
      this.viewHdButton.disabled = false;
      this.providerIconButton.disabled = false;
      this.card.classList.add('gvrg-card-visible');
    }

    async #requestGeminiEnrichment(destination) {
      if (!this.geminiProvider && !this.options.geminiEndpoint) return null;
      const payload = {
        name: destination.name,
        ra: destination.ra,
        dec: destination.dec,
        distanceMly: destination.distance,
        constellation: destination.constellation,
        source: 'GALAXY PROVIDER'
      };
      const result = this.geminiProvider ? await this.geminiProvider(payload, this) : await this.#fetchJsonEndpoint(this.options.geminiEndpoint, payload);
      return result && typeof result === 'object' ? result : null;
    }

    #hideRefreshSky() {
      if (this.refreshSkyTimer) {
        clearTimeout(this.refreshSkyTimer);
        this.refreshSkyTimer = 0;
      }
      if (this.refreshSkyButton) {
        this.refreshSkyButton.hidden = true;
        this.refreshSkyButton.classList.remove('gvrg-refresh-working');
      }
    }

    #aladinStateLooksUsable() {
      try {
        const coordinates = this.aladin.getRaDec?.();
        const fov = this.aladin.getFov?.();
        const ra = finiteNumber(coordinates?.[0]);
        const dec = finiteNumber(coordinates?.[1]);
        const fovValue = finiteNumber(fov?.[0]);

        return !this.#aladinCanvasLooksStale() &&
          ra !== null &&
          dec !== null &&
          fovValue !== null &&
          fovValue > 0;
      } catch (_) {
        return false;
      }
    }

    #armRefreshSkyWatchdog(reason = 'recovery') {
      this.#hideRefreshSky();

      if (this.destroyed || this.busy || !this.arrived || this.hdOpen)
        return;

      this.refreshSkyTimer = setTimeout(() => {
        this.refreshSkyTimer = 0;

        if (this.destroyed || this.busy || !this.arrived || this.hdOpen)
          return;

        if (this.#aladinStateLooksUsable()) return;

        console.warn(
          'GALAXY RANDOM ALADIN RECOVERY REQUIRES USER ACTION',
          reason,
          cleanText(this.activeDestination?.name)
        );

        if (this.refreshSkyButton)
          this.refreshSkyButton.hidden = false;
      }, this.refreshSkyDelayMs);
    }

    #r10ScreenFitFov(destination) {
      const callbackFov = finiteNumber(destination?.avmCallbackFov);
      const imageWidthFov = finiteNumber(destination?.avmHorizontalFovDegrees);
      const imageHeightFov = finiteNumber(destination?.avmVerticalFovDegrees);
      const legacyFov = finiteNumber(destination?.fovDegrees);

      const baseFov =
        callbackFov !== null && callbackFov > 0
          ? callbackFov
          : imageWidthFov !== null && imageWidthFov > 0 &&
            imageHeightFov !== null && imageHeightFov > 0
              ? Math.max(imageWidthFov,imageHeightFov)
              : legacyFov;

      if (baseFov === null || baseFov <= 0) return legacyFov;
      if (
        imageWidthFov === null || imageWidthFov <= 0 ||
        imageHeightFov === null || imageHeightFov <= 0
      ) return baseFov;

      let viewportWidth=null;
      let viewportHeight=null;
      try {
        const size=this.aladin.getSize?.();
        viewportWidth=finiteNumber(size?.[0]);
        viewportHeight=finiteNumber(size?.[1]);
      } catch (_) {}

      if (!(viewportWidth>0) || !(viewportHeight>0)) {
        try {
          const rect=this.aladin.getParentDiv?.()?.getBoundingClientRect?.();
          viewportWidth=finiteNumber(rect?.width);
          viewportHeight=finiteNumber(rect?.height);
        } catch (_) {}
      }

      if (!(viewportWidth>0) || !(viewportHeight>0)) return baseFov;

      // R10 gold standard: on a square viewport the larger AVM image axis
      // equals callbackFov exactly. For the live Galaxy Viewer viewport,
      // preserve that absolute scale and expand only as required by aspect.
      const imageAxisMax=Math.max(imageWidthFov,imageHeightFov);
      const r10Scale=baseFov/imageAxisMax;
      const r10Width=imageWidthFov*r10Scale;
      const r10Height=imageHeightFov*r10Scale;
      const screenAspect=viewportWidth/viewportHeight;
      const screenFov=Math.max(r10Width,r10Height*screenAspect);

      return Number.isFinite(screenFov)&&screenFov>0
        ? screenFov
        : baseFov;
    }

    #exactActiveAladinState(destination = this.activeDestination) {
      if (!destination) return null;
      const ra = finiteNumber(destination.ra);
      const dec = finiteNumber(destination.dec);
      const fov = finiteNumber(destination.fovDegrees);
      if (ra === null || dec === null || fov === null || fov <= 0) return null;
      return Object.freeze({
        ra,
        dec,
        fov,
        rotation: finiteNumber(destination.aladinRotation) ?? 0,
        projection: cleanText(this.options.arrivalProjection || 'MOL') || 'MOL',
        authoritative: true
      });
    }

    #captureAladinState() {
      try {
        const coordinates = this.aladin.getRaDec?.();
        const fov = this.aladin.getFov?.();
        const ra = finiteNumber(coordinates?.[0]);
        const dec = finiteNumber(coordinates?.[1]);
        const fovValue = finiteNumber(fov?.[0]);
        if (ra === null || dec === null || fovValue === null || fovValue <= 0) return null;

        let rotation = null;
        let projection = null;

        try {
          if (typeof this.aladin.getRotation === 'function')
            rotation = finiteNumber(this.aladin.getRotation());
        } catch (_) {}

        try {
          if (typeof this.aladin.getProjection === 'function') {
            const value = this.aladin.getProjection();
            if (typeof value === 'string' && value.trim())
              projection = value.trim();
          }
        } catch (_) {}

        return Object.freeze({
          ra,
          dec,
          fov: fovValue,
          rotation,
          projection,
          authoritative: false
        });
      } catch (_) {
        return null;
      }
    }

    #aladinCanvasLooksStale() {
      const scope =
        this.options.viewerRoot instanceof Element
          ? this.options.viewerRoot
          : document;
      const canvases = [...scope.querySelectorAll('canvas')];
      if (!canvases.length) return true;
      return !canvases.some((canvas) => {
        const rect = canvas.getBoundingClientRect();
        return rect.width > 1 &&
          rect.height > 1 &&
          canvas.width > 1 &&
          canvas.height > 1;
      });
    }

    #restoreAladinState(snapshot, reason = 'recovery') {
      const target =
        snapshot ||
        this.#captureAladinState() ||
        this.#exactActiveAladinState();

      if (!target || this.destroyed) return false;

      try { window.dispatchEvent(new Event('resize')); } catch (_) {}

      requestAnimationFrame(() => {
        if (this.destroyed) return;

        try {
          if (typeof this.aladin.gotoRaDec === 'function')
              global.GalaxyBlackBox?.recordCheckpoint?.("FINAL_GOTO_BEGIN",{t:Number(t),ra:Number(destination.ra),dec:Number(destination.dec)});
            void 0; // Navigation 0016 owns visible RA/Dec
        } catch (error) {
          console.warn(
            'GALAXY RANDOM ALADIN RECOVERY POSITION FAILED',
            reason,
            error
          );
        }

        try {
          if (Number.isFinite(Number(target.fov)) &&
              Number(target.fov) > 0 &&
              typeof this.aladin.setFov === 'function')
            void 0; // Navigation 0016 owns visible FOV
        } catch (error) {
          console.warn(
            'GALAXY RANDOM ALADIN RECOVERY FOV FAILED',
            reason,
            error
          );
        }
      });

      this.lastAladinRecoveryAt = performance.now();
      return true;
    }

    #recoverExactActiveAladin(reason = 'exact-recovery') {
      return this.#restoreAladinState(
        this.#exactActiveAladinState(),
        reason
      );
    }

    #checkAndRecoverStaleAladin(reason = 'stale-check') {
      if (this.destroyed || this.busy || this.hdOpen || this.aladinRecoveryBusy) return;
      if (!this.#aladinCanvasLooksStale()) return;

      this.aladinRecoveryBusy = true;

      setTimeout(() => {
        if (this.destroyed || this.busy) {
          this.aladinRecoveryBusy = false;
          return;
        }

        if (!this.#aladinCanvasLooksStale()) {
          this.aladinRecoveryBusy = false;
          return;
        }

        this.#recoverExactActiveAladin(reason);
        this.#armRefreshSkyWatchdog(reason);

        setTimeout(() => {
          this.aladinRecoveryBusy = false;
        }, 1200);
      }, 300);
    }

    #handleViewerResume(reason, savedSnapshot = null) {
      if (this.destroyed || this.busy) return;

      requestAnimationFrame(() => {
        if (this.destroyed || this.busy) return;

        // If HD is still open, preserve the sky snapshot and wait until
        // BACK TO SKY rather than touching the hidden Aladin surface.
        if (this.hdOpen) {
          if (savedSnapshot && !this.hdSkySnapshot)
            this.hdSkySnapshot = savedSnapshot;
          return;
        }

        const restoreState =
          savedSnapshot ||
          this.#captureAladinState() ||
          this.#exactActiveAladinState();

        if (restoreState)
          this.#restoreAladinState(restoreState, reason);

        this.#armRefreshSkyWatchdog(reason);

        requestAnimationFrame(() =>
          this.#checkAndRecoverStaleAladin(`${reason}-postcheck`)
        );
      });
    }


    #travelHudProgress(t) {
      return navigationSmootherstep(t);
    }

    #formatTravelHudDistance(millionLy) {
      const value =
        Number.isFinite(Number(millionLy)) && Number(millionLy) > 0
          ? Number(millionLy)
          : 0;

      const scaled =
        value >= 1000
          ? value / 1000
          : value;

      const [integer, fraction = '00'] =
        scaled.toFixed(2).split('.');

      return {
        integer,
        fraction: fraction.padEnd(2, '0').slice(0, 2),
        unit:
          value >= 1000
            ? 'BILLION LIGHT-YEARS'
            : 'MILLION LIGHT-YEARS'
      };
    }

    #beginTravelHud(destination, route, firstHomeTrip) {
      const hud =
        document.getElementById('gv-travel-hud');
      const primaryEl = document.getElementById('gv-travel-primary') || hud;

      const destinationEl =
        document.getElementById('gv-travel-destination');

      const distanceIntegerEl =
        document.getElementById('gv-travel-distance-integer');

      const distanceFractionEl =
        document.getElementById('gv-travel-distance-fraction');

      const distanceUnitEl =
        document.getElementById('gv-travel-distance-unit');

      if (
        !hud ||
        !destinationEl ||
        !distanceIntegerEl ||
        !distanceFractionEl ||
        !distanceUnitEl
      ) return;

      cancelAnimationFrame(this.travelHudFrame);

      const hudSeconds =
        Number(this.options.travelSeconds);

      const total =
        Number.isFinite(Number(route && route.value))
          ? Number(route.value)
          : 0;

      destinationEl.textContent =
        cleanText(destination && destination.name).toUpperCase();

      let travelProviderIcon =
        document.getElementById("gv-travel-provider-icon");

      if (!travelProviderIcon) {
        travelProviderIcon = document.createElement("span");
        travelProviderIcon.id = "gv-travel-provider-icon";
        travelProviderIcon.setAttribute("aria-hidden","true");

        const travelProviderImage = document.createElement("img");
        travelProviderImage.alt = "";
        travelProviderImage.setAttribute("aria-hidden","true");

        travelProviderIcon.appendChild(travelProviderImage);
        primaryEl.appendChild(travelProviderIcon);
      }

      const travelProviderImage =
        travelProviderIcon.querySelector("img");

      const travelProviderUrl = (()=>{
        const explicit=String(
          destination?.providerIconUrl ||
          destination?.provider_icon_url ||
          ""
        ).trim();

        if(/^https:\/\//i.test(explicit))
          return explicit;

        const evidence=[
          destination?.provider,
          destination?.archiveProvider,
          destination?.archive_provider,
          destination?.telescope,
          destination?.source,
          destination?.hdUrl,
          destination?.sourceUrl
        ].map(value=>String(value||"").trim().toLowerCase())
         .filter(Boolean)
         .join(" ");

        let slug="";

        if(/(?:^|[^a-z0-9])(?:hubble|hst|esahubble)(?:[^a-z0-9]|$)/i.test(evidence))
          slug="hubble";
        else if(/(?:^|[^a-z0-9])(?:jwst|james webb|webb|esawebb)(?:[^a-z0-9]|$)/i.test(evidence))
          slug="jwst";
        else if(/(?:^|[^a-z0-9])spitzer(?:[^a-z0-9]|$)/i.test(evidence))
          slug="spitzer";
        else if(/(?:^|[^a-z0-9])chandra(?:[^a-z0-9]|$)/i.test(evidence))
          slug="chandra";

        if(!slug)return "";

        return `https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/providers/${slug}/${slug}-icon.png`;
      })();

      if (travelProviderImage && travelProviderUrl) {
        travelProviderImage.onerror=null;
        travelProviderImage.src = travelProviderUrl;
        travelProviderIcon.style.display = "flex";

        travelProviderImage.onerror=()=>{
          travelProviderImage.onerror=null;
          travelProviderImage.removeAttribute("src");
          travelProviderIcon.style.display = "none";
        };
      } else {
        if (travelProviderImage) {
          travelProviderImage.onerror=null;
          travelProviderImage.removeAttribute("src");
        }
        travelProviderIcon.style.display = "none";
      }

      const initial =
        this.#formatTravelHudDistance(0);

      distanceIntegerEl.textContent =
        initial.integer;

      distanceFractionEl.textContent =
        initial.fraction;

      distanceUnitEl.textContent =
        initial.unit;

      hud.classList.add('gv-visible');

      const started =
        performance.now();

      const frame = (now) => {
        const t =
          Math.min(
            1,
            (now - started) / (hudSeconds * 1000)
          );

        const progress =
          firstHomeTrip
            ? t
            : this.#travelHudProgress(t);

        const shown =
          this.#formatTravelHudDistance(
            total * progress
          );

        distanceIntegerEl.textContent =
          shown.integer;

        distanceFractionEl.textContent =
          shown.fraction;

        distanceUnitEl.textContent =
          shown.unit;

        if (t < 1) {
          this.travelHudFrame =
            requestAnimationFrame(frame);
          return;
        }

        this.travelHudFrame = 0;
      };

      this.travelHudFrame =
        requestAnimationFrame(frame);
    }

    #endTravelHud() {
      cancelAnimationFrame(
        this.travelHudFrame
      );

      this.travelHudFrame = 0;

      const hud =
        document.getElementById('gv-travel-hud');

      if (hud)
        hud.classList.remove('gv-visible');
    }

    beginHdRequest() {
      if (this.destroyed) return false;
      if (this.interactionOwner === 'hd') return true;

      const takingOverNavigation=
        this.busy || this.interactionOwner === 'navigation';

      if (takingOverNavigation) {
        const aborted=
          global.GalaxyViewerNavigation?.abortActiveFlight?.('hd-request')===true;
        if (!aborted) {
          global.GalaxyBlackBox?.recordCheckpoint?.('HD_REQUEST_ABORT_NAV_FAILED',{
            busy:Boolean(this.busy),
            owner:String(this.interactionOwner||'')
          });
          return false;
        }
      } else if (this.interactionOwner && this.interactionOwner !== 'hd') {
        return false;
      }

      if (!this._hdInterlockSnapshot) {
        const snapshot=takingOverNavigation
          ? (this._navigationControlSnapshot||{})
          : {};
        this._hdInterlockSnapshot={
          randomDisabled:Boolean(snapshot.randomDisabled),
          viewHdDisabled:Boolean(snapshot.viewHdDisabled),
          providerDisabled:Boolean(snapshot.providerDisabled)
        };
        if (takingOverNavigation) this._navigationControlSnapshot=null;
      }

      this.interactionOwner='hd';
      // Random intentionally remains clickable so it can cancel HD and take over.
      if (this.randomButton) this.randomButton.disabled=false;
      if (this.viewHdButton) this.viewHdButton.disabled=true;
      if (this.providerIconButton) this.providerIconButton.disabled=true;

      global.GalaxyBlackBox?.recordCheckpoint?.(
        takingOverNavigation?'HD_TOOK_OVER_NAVIGATION':'HD_REQUEST_LOCK_CLAIMED',
        {}
      );
      return true;
    }

    cancelHdRequest(reason='cancelled') {
      if (this.hdOpen || this.interactionOwner !== 'hd') return false;
      const snapshot=this._hdInterlockSnapshot||null;
      this._hdInterlockSnapshot=null;
      this.interactionOwner=null;

      if (snapshot) {
        if (this.randomButton) this.randomButton.disabled=Boolean(snapshot.randomDisabled);
        if (this.viewHdButton) this.viewHdButton.disabled=Boolean(snapshot.viewHdDisabled);
        if (this.providerIconButton) this.providerIconButton.disabled=Boolean(snapshot.providerDisabled);
      }

      global.GalaxyBlackBox?.recordCheckpoint?.('HD_REQUEST_LOCK_RELEASED',{
        reason:String(reason||'cancelled')
      });
      return true;
    }

    async travelToRandom() {
      GV_TRACE.enabled&&gvTrace(4601,'TRAVEL_ENTER',{
        readyState:this.__gvReadyState||'UNKNOWN',
        busy:Boolean(this.busy),
        destroyed:Boolean(this.destroyed)
      });

      global.GalaxyBlackBox?.recordCheckpoint?.('RANDOM_REQUEST',{
        busy:Boolean(this.busy),
        hdOpen:Boolean(this.hdOpen),
        arrived:Boolean(this.arrived)
      });

      // Random takes ownership from HD synchronously before navigation starts.
      if (this.hdOpen || this.interactionOwner === 'hd') {
        global.GalaxyBlackBox?.recordCheckpoint?.('RANDOM_TAKEOVER_HD',{
          hdOpen:Boolean(this.hdOpen),
          owner:String(this.interactionOwner||'')
        });
        if (this.hdOpen) this.backToSky({recover:false});
        else this.cancelHdRequest('random-takeover');
      }

      // Claim navigation synchronously before the first await.
      if (this.destroyed || this.busy || (this.interactionOwner && this.interactionOwner !== 'navigation')) {
        global.GalaxyBlackBox?.recordCheckpoint?.('RANDOM_BLOCKED_BUSY',{
          busy:Boolean(this.busy),
          destroyed:Boolean(this.destroyed),
          hdOpen:Boolean(this.hdOpen),
          owner:String(this.interactionOwner||'')
        });
        return null;
      }
      this.interactionOwner='navigation';

      const priorControlState={
        randomDisabled:Boolean(this.randomButton?.disabled),
        viewHdDisabled:Boolean(this.viewHdButton?.disabled),
        providerDisabled:Boolean(this.providerIconButton?.disabled)
      };
      this._navigationControlSnapshot={...priorControlState};

      this.busy = true;

      if (this.randomButton)
        this.randomButton.disabled = true;

      if (this.viewHdButton)
        this.viewHdButton.disabled = true;

      if (this.providerIconButton)
        this.providerIconButton.disabled = true;

      global.GalaxyBlackBox?.recordCheckpoint?.('RANDOM_HD_LOCKED',{
        hdOpen:Boolean(this.hdOpen)
      });

      GV_TRACE.enabled&&gvTrace(4602,'PORTRAIT_REQUEST');
      requestPortraitOrientation('random-travel').catch(() => {});

      GV_TRACE.enabled&&gvTrace(4603,'READY_AWAIT_BEGIN',{
        state:this.__gvReadyState||'UNKNOWN'
      });

      try {
        await this.ready;
      } catch (error) {
        this.busy = false;
        this._navigationControlSnapshot=null;
        if (this.interactionOwner === 'navigation') this.interactionOwner=null;

        if (this.randomButton)
          this.randomButton.disabled = priorControlState.randomDisabled;

        if (this.viewHdButton)
          this.viewHdButton.disabled = priorControlState.viewHdDisabled;

        if (this.providerIconButton)
          this.providerIconButton.disabled = priorControlState.providerDisabled;

        global.GalaxyBlackBox?.recordCheckpoint?.('RANDOM_READY_FAILED',{
          message:String(error?.message||error||'UNKNOWN')
        });

        global.GalaxyBlackBox?.recordCheckpoint?.(
          'RANDOM_READY_FAILED_CONTROLS_RESTORED',
          {
            randomDisabled:Boolean(this.randomButton?.disabled),
            viewHdDisabled:Boolean(this.viewHdButton?.disabled),
            providerDisabled:Boolean(this.providerIconButton?.disabled)
          }
        );

        throw error;
      }

      GV_TRACE.enabled&&gvTrace(4603,'READY_AWAIT_END',{
        state:this.__gvReadyState||'UNKNOWN'
      });

      if (this.destroyed) {
        this.busy = false;
        if (this.interactionOwner === 'navigation') this.interactionOwner=null;
        return null;
      }

      GV_TRACE.enabled&&gvTrace(4604,'TRAVEL_GUARD',{
        busy:Boolean(this.busy),
        destroyed:Boolean(this.destroyed)
      });

      this.#hideRefreshSky();
      this.#hideHomePresentation();
      setRandomWaitComet(this.randomButton, true);
      this.arrived = false;
      this.#hideCard();

      try {
        GV_TRACE.enabled&&gvTrace(4614,'STATUS_FINDING');
        this.#setStatus('FINDING GALAXY');
        GV_TRACE.enabled&&gvTrace(4615,'CONSUME_BEGIN');
        const destination = await this.#consumeDestination();
        GV_TRACE.enabled&&gvTrace(4615,'CONSUME_END',{
          name:String(destination?.name||''),
          ra:Number(destination?.ra),
          dec:Number(destination?.dec),
          fov:Number(destination?.fovDegrees)
        });
        this.activeDestination = destination;
        if (this.viewHdButton) this.viewHdButton.disabled=false;
        if (this.providerIconButton) this.providerIconButton.disabled=false;
        GV_TRACE.enabled&&gvTrace(4616,'ACTIVE_DESTINATION_SET',{name:String(destination?.name||'')});
        this.#setTravelStatus(destination.name);
        GV_TRACE.enabled&&gvTrace(4618,'ALADIN_GET_RADEC_BEGIN',null);
        const coords = this.aladin.getRaDec();
        GV_TRACE.enabled&&gvTrace(4618,'ALADIN_GET_RADEC_END',{coords:Array.isArray(coords)?coords.slice(0,2):coords});
        GV_TRACE.enabled&&gvTrace(4619,'ALADIN_GET_FOV_BEGIN',null);
        const fov = this.aladin.getFov();
        GV_TRACE.enabled&&gvTrace(4619,'ALADIN_GET_FOV_END',{fov:Array.isArray(fov)?fov.slice(0,2):fov});
        GV_TRACE.enabled&&gvTrace(4629,'NUMERIC_STATE_BEGIN',null);
        const startRA = Number(coords[0]);
        const startDec = Number(coords[1]);
        const startFov = Number(fov[0]);
        const destinationFov = this.#r10ScreenFitFov(destination);
        GV_TRACE.enabled&&gvTrace(4632,'NUMERIC_STATE_COMPLETE',{startRA,startDec,startFov,destinationFov});
        if (!Number.isFinite(startFov) || startFov <= 0)
          throw new Error('CURRENT ALADIN FOV IS INVALID');
        if (!Number.isFinite(destinationFov) || destinationFov <= 0)
          throw new Error('DESTINATION ALADIN FOV IS INVALID');
        const source = { ...this.currentGalaxy, ra: startRA, dec: startDec };
        const firstHomeTrip = this.#isHomeDeparture(source, startFov);


        GV_TRACE.enabled&&gvTrace(4639,'ROUTE_CALC_BEGIN',null);
        const route = routeDistanceMillionLy(source, destination);
        GV_TRACE.enabled&&gvTrace(4639,'ROUTE_CALC_END',{routeValue:Number(route?.value)});
        this.#beginTravelHud(destination, route, firstHomeTrip);
        this.#showDistance(source, destination, route);
        await window.GalaxyViewerNavigation.flyViewport({
          aladin:this.aladin,
          source,
          destination,
          routeValue:Number(route?.value)||0,
          startRA,
          startDec,
          startFov,
          destinationFov,
          firstHomeTrip,
          rotationStart:
            finiteNumber(this.currentGalaxy?.aladinRotation)??0,
          onDistanceProgress:value=>{
            this.distanceRenderer.render(value);
          },
          onTimelineProgress:t=>{
            if(this.progressFill)
              this.progressFill.style.width=
                `${(t*100).toFixed(1)}%`;
          },
          trace:(code,label,detail)=>{
            GV_TRACE.enabled&&gvTrace(code,label,detail);
          },
          traceError:(code,label,error)=>{
            GV_TRACE.enabled&&gvTraceError(code,label,error);
          }
        });
        // Allow the already-final viewport to paint before declaring
        // arrival. This performs no additional rotation/recenter/zoom.
        GV_TRACE.enabled&&gvTrace(4783,'ARRIVAL_PAINT_WAIT_BEGIN',null);
        global.GalaxyBlackBox?.recordCheckpoint?.("ARRIVAL_PAINT_WAIT_BEGIN",{});
        await new Promise(resolve=>
          requestAnimationFrame(()=>requestAnimationFrame(resolve))
        );
        GV_TRACE.enabled&&gvTrace(4783,'ARRIVAL_PAINT_WAIT_END',null);
        global.GalaxyBlackBox?.recordCheckpoint?.("ARRIVAL_PAINT_WAIT_END",{});

        GV_TRACE.enabled&&gvTrace(4787,'ARRIVAL_SET_CURRENT',{name:String(destination?.name||'')});
        this.currentGalaxy = { name: destination.name, ra: destination.ra, dec: destination.dec, distance: destination.distance, aladinRotation: finiteNumber(destination.aladinRotation) ?? 0 };
        try{
          const gvRotationDestinationSnapshot=Object.freeze({
            designation:String(destination.designation||destination.catalogDesignation||destination.id||destination.name||''),
            name:String(destination.name||destination.pseudo||destination.commonName||destination.title||''),
            ra:finiteNumber(destination.ra),
            dec:finiteNumber(destination.dec),
            fovDegrees:finiteNumber(destination.fovDegrees),
            aladinRotation:finiteNumber(destination.aladinRotation),
            catalogSource:String(destination.catalogSource||destination.source||'')
          });
          try{global.GalaxyRandomGalaxy=global.GalaxyRandomGalaxy||{};global.GalaxyRandomGalaxy.currentDestination=gvRotationDestinationSnapshot;}catch(_){}
        }catch(_){}
        GV_TRACE.enabled&&gvTrace(4788,'ARRIVAL_TRUE',null);
        this.arrived = true;
        GV_TRACE.enabled&&gvTrace(4789,'ARRIVAL_BUSY_FALSE',null);
        this.busy = false;
        this._navigationControlSnapshot=null;
        if (this.interactionOwner === 'navigation') this.interactionOwner=null;
        setRandomWaitComet(this.randomButton, false);
        this.#hideDistance();
        GV_TRACE.enabled&&gvTrace(4792,'ARRIVAL_SHOW_CARD',null);
        global.GalaxyBlackBox?.recordCheckpoint?.("SHOW_CARD_BEGIN",{name:String(destination?.name||"")});
        this.#showCard(destination);
        global.GalaxyBlackBox?.recordCheckpoint?.("SHOW_CARD_END",{});
        GV_TRACE.enabled&&gvTrace(4793,'ARRIVAL_STATUS',null);
        this.#setStatus(`ARRIVED ${destination.name.toUpperCase()}`);
        if (this.randomButton) this.randomButton.disabled = false;

        this.#armRefreshSkyWatchdog('random-arrival');

        this.#endTravelHud();

        GV_TRACE.enabled&&gvTrace(4800,'ARRIVAL_CALLBACK',null);
        global.GalaxyBlackBox?.recordCheckpoint?.("ARRIVAL_CALLBACK_BEGIN",{});
        if (this.onArrival) this.onArrival(destination, this);
        global.GalaxyBlackBox?.recordCheckpoint?.("ARRIVAL_CALLBACK_END",{});
        setTimeout(() => {
          this.#requestGeminiEnrichment(destination)
            .then((result) => { if (result) this.lastGeminiEnrichment = result; })
            .catch(() => {});
        }, 0);
        if (this.options.prefetch) this.prefetch().catch(() => {});


        return destination;
      } catch (error) {
        GV_TRACE.enabled&&gvTraceError(4808,'TRAVEL_EXCEPTION',error);
        if (error?.code==='GV_NAV_ABORTED' && error?.reason==='hd-request') {
          this.busy=false;
          setRandomWaitComet(this.randomButton,false);
          this.arrived=false;
          this.#hideDistance();
          this.#endTravelHud();
          global.GalaxyBlackBox?.recordCheckpoint?.('TRAVEL_ABORTED_FOR_HD',{
            destination:String(this.activeDestination?.name||'')
          });
          return null;
        }
        this.busy = false;
        this._navigationControlSnapshot=null;
        if (this.interactionOwner === 'navigation') this.interactionOwner=null;
        setRandomWaitComet(this.randomButton, false);
        this.arrived = false;
        this.activeDestination = null;
        this.#hideDistance();
        this.#endTravelHud();

        // A real travel failure clears activeDestination below/above, so
        // HD must remain unavailable. This is availability state, not a
        // leaked HD/navigation interlock.
        if (this.viewHdButton)
          this.viewHdButton.disabled = true;

        if (this.providerIconButton)
          this.providerIconButton.disabled = true;

        if (this.randomButton)
          this.randomButton.disabled = true;

        global.GalaxyBlackBox?.recordCheckpoint?.(
          'TRAVEL_EXCEPTION_CONTROLS_SAFE',
          {
            randomDisabled:Boolean(this.randomButton?.disabled),
            viewHdDisabled:Boolean(this.viewHdButton?.disabled),
            providerDisabled:Boolean(this.providerIconButton?.disabled),
            activeDestination:Boolean(this.activeDestination),
            arrived:Boolean(this.arrived)
          }
        );

        throw error;
      }
    }
    async random() { return this.travelToRandom(); }

    #populateHdScience(destination) {
      const designation = cleanText(destination.designation).toUpperCase();
      const common = cleanText(destination.commonName);
      const normalizedDesignation = designation.replace(/\s+/g, '');
      const normalizedCommon = common.toUpperCase().replace(/\s+/g, '');
      const commonDisplay = common && (!normalizedDesignation || normalizedCommon !== normalizedDesignation) ? common.toUpperCase() : '';
      this.hdDesignationValueEl.textContent = designation;
      this.hdCommonNameValueEl.textContent = commonDisplay;
      this.hdDistanceValueEl.textContent = formatDistanceMly(destination.distance);
      this.hdAgeValueEl.textContent = destination.ageYears ? formatAgeYears(destination.ageYears) : cleanText(destination.age).toUpperCase();
      this.hdSizeValueEl.textContent = formatPhysicalSize(destination.physicalSizeLy);
    }
    #positionHdPresentation() {
      if (this.hdViewport?.dataset?.gvFixedViewport === '1') return;
      const overlayRect = this.hdOverlay.getBoundingClientRect();
      this.hdScience.style.top = '';
      this.hdViewport.style.top = '';
      this.hdViewport.style.bottom = '';
      this.hdViewport.style.height = '';
      const baseTop = Math.max(6, Number.parseFloat(getComputedStyle(this.hdScience).top) || 6);
      const footerRect = this.hdFooter.getBoundingClientRect();
      const scienceHeight = this.hdScience.getBoundingClientRect().height;
      const safeTop = overlayRect.top + baseTop;
      const safeBottom = Math.max(safeTop + 1, Math.min(overlayRect.bottom - 6, footerRect.top - 6));
      const availableHeight = Math.max(1, safeBottom - safeTop);
      const gap = 6;
      const naturalWidth = this.hdImage.naturalWidth;
      const naturalHeight = this.hdImage.naturalHeight;
      if (!naturalWidth || !naturalHeight) {
        this.hdScience.style.top = `${Math.max(0, Math.round(safeTop - overlayRect.top))}px`;
        this.hdViewport.style.top = `${Math.max(0, Math.round(safeTop + scienceHeight + gap - overlayRect.top))}px`;
        this.hdViewport.style.bottom = `${Math.max(0, Math.round(overlayRect.bottom - safeBottom))}px`;
        return;
      }
      const maxImageHeight = Math.max(1, availableHeight - scienceHeight - gap);
      const fit = Math.min(1, overlayRect.width / naturalWidth, maxImageHeight / naturalHeight);
      const imageHeight = Math.max(1, naturalHeight * fit);
      let imageTop = safeTop + (availableHeight - imageHeight) / 2;
      let scienceTop = imageTop - gap - scienceHeight;
      if (scienceTop < safeTop) {
        const shift = safeTop - scienceTop;
        scienceTop += shift;
        imageTop += shift;
      }
      if (imageTop + imageHeight > safeBottom) {
        const shift = imageTop + imageHeight - safeBottom;
        imageTop -= shift;
        scienceTop -= shift;
      }
      this.hdScience.style.top = `${Math.max(0, Math.round(scienceTop - overlayRect.top))}px`;
      this.hdViewport.style.top = `${Math.max(0, Math.round(imageTop - overlayRect.top))}px`;
      this.hdViewport.style.bottom = 'auto';
      this.hdViewport.style.height = `${Math.max(1, Math.round(imageHeight))}px`;
    }
    #mountHdImage(image) {
      if (!(image instanceof HTMLImageElement)) return false;
      if (this.hdImage !== image) {
        if (this.hdImage && this.hdImage.parentNode === this.hdViewport) this.hdViewport.replaceChild(image, this.hdImage);
        else if (image.parentNode !== this.hdViewport) this.hdViewport.appendChild(image);
        this.hdImage = image;
      }
      return true;
    }
    #hdScaleGeometry() {
      const destination = this.activeDestination;
      const distanceMly = finiteNumber(destination && destination.distance);
      const fovDegrees = finiteNumber(destination && destination.fovDegrees);
      const imageWidth = Number(this.hdImage && this.hdImage.offsetWidth);
      const viewportWidth = Number(this.hdViewport && this.hdViewport.clientWidth);
      const zoom = finiteNumber(this.hdScale);
      if (!(distanceMly > 0) || !(fovDegrees > 0) || !(imageWidth > 0) || !(viewportWidth > 0) || !(zoom > 0)) return null;
      const theta = fovDegrees * Math.PI / 180;
      const physicalWidthLy = 2 * distanceMly * 1_000_000 * Math.tan(theta / 2);
      if (!(physicalWidthLy > 0) || !Number.isFinite(physicalWidthLy)) return null;
      return { lyPerPx: physicalWidthLy / (imageWidth * zoom), viewportWidth };
    }
    #chooseHdScaleValue(geometry) {
      const targetFraction = 0.45;
      const targetLy = geometry.lyPerPx * geometry.viewportWidth * targetFraction;
      if (!(targetLy > 0)) return null;
      const exponent = Math.floor(Math.log10(targetLy));
      const candidates = [];
      for (let e = exponent - 2; e <= exponent + 2; e += 1)
        for (const m of [1, 2, 5])
          candidates.push(m * Math.pow(10, e));
      const scored = candidates.map(value => {
        const px = value / geometry.lyPerPx;
        const fraction = px / geometry.viewportWidth;
        const inBand = fraction >= 0.35 && fraction <= 0.55;
        return {
          value,
          score: Math.abs(fraction - targetFraction) + (inBand ? 0 : 10)
        };
      }).sort((a,b) => a.score - b.score);
      return scored.length ? scored[0].value : null;
    }
    #resetHdScaleBar() {
      if (this.hdScaleBarTimer) clearTimeout(this.hdScaleBarTimer);
      this.hdScaleBarTimer = 0;
      this.hdScaleBarValue = null;
      if (this.hdScaleBar) this.hdScaleBar.style.display = 'none';
    }
    #scheduleHdScaleBar() {
      if (this.hdScaleBarTimer) clearTimeout(this.hdScaleBarTimer);
      this.hdScaleBarTimer = setTimeout(() => {
        this.hdScaleBarTimer = 0;
        this.#updateHdScaleBar(true);
      }, Number(this.options.hdScaleSettleMs) || 200);
    }
    #updateHdScaleBar(selectNew = false) {
      if (!this.hdOpen || !this.hdScaleBar || !this.hdScaleLine || !this.hdScaleLabel) return;
      const geometry = this.#hdScaleGeometry();
      if (!geometry) { this.hdScaleBar.style.display = 'none'; return; }

      if (selectNew || !(this.hdScaleBarValue > 0))
        this.hdScaleBarValue = this.#chooseHdScaleValue(geometry);

      if (!(this.hdScaleBarValue > 0)) {
        this.hdScaleBar.style.display = 'none';
        return;
      }

      let widthPx = this.hdScaleBarValue / geometry.lyPerPx;
      let fraction = widthPx / geometry.viewportWidth;

      // Hysteresis: keep a stable nice value during small zoom changes,
      // but immediately select another 1/2/5 value outside the safe band.
      if (!selectNew && (fraction < 0.30 || fraction > 0.60)) {
        const replacement = this.#chooseHdScaleValue(geometry);
        if (replacement > 0) this.hdScaleBarValue = replacement;
        widthPx = this.hdScaleBarValue / geometry.lyPerPx;
        fraction = widthPx / geometry.viewportWidth;
      }

      // Absolute visual guard: the dog-bone can never exceed 60% of viewport.
      const hardMaxPx = geometry.viewportWidth * 0.60;
      this.hdScaleLine.style.width = `${Math.max(4, Math.min(hardMaxPx, widthPx))}px`;
      this.hdScaleLabel.textContent = formatCompactHdScale(this.hdScaleBarValue);
      this.hdScaleBar.setAttribute('aria-label', `IMAGE SCALE ${this.hdScaleLabel.textContent}`);
      this.hdScaleBar.style.display = 'flex';
    }
    #applyHdTransform() {
      this.hdImage.style.transform = `translate3d(${this.hdTranslateX}px,${this.hdTranslateY}px,0) scale(${this.hdScale})`;
    }
    #clampHdTranslation() {
      if (this.hdScale <= 1) {
        this.hdScale = 1;
        this.hdTranslateX = 0;
        this.hdTranslateY = 0;
        return;
      }
      const viewportWidth = this.hdViewport.clientWidth;
      const viewportHeight = this.hdViewport.clientHeight;
      const imageWidth = this.hdImage.offsetWidth;
      const imageHeight = this.hdImage.offsetHeight;
      const scaledWidth = imageWidth * this.hdScale;
      const scaledHeight = imageHeight * this.hdScale;
      const maxX = Math.max(0, (scaledWidth - viewportWidth) / 2);
      const minY = Math.min(0, viewportHeight - scaledHeight);
      this.hdTranslateX = clamp(this.hdTranslateX, -maxX, maxX);
      this.hdTranslateY = clamp(this.hdTranslateY, minY, 0);
    }
    #resetHdTransform() {
      this.hdScale = 1;
      this.hdTranslateX = 0;
      this.hdTranslateY = 0;
      this.hdPointers.clear();
      this.hdGesture = null;
      this.#applyHdTransform();
      this.#resetHdScaleBar();
    }
    #pointerPair() {
      const values = [...this.hdPointers.values()];
      if (values.length < 2) return null;
      const [a, b] = values;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const rect = this.hdViewport.getBoundingClientRect();
      const originX = rect.left + this.hdImage.offsetLeft + this.hdImage.offsetWidth / 2;
      const originY = rect.top + this.hdImage.offsetTop;
      return {
        distance: Math.hypot(dx, dy),
        midX: (a.x + b.x) / 2 - originX,
        midY: (a.y + b.y) / 2 - originY
      };
    }
    #onHdPointerDown(event) {
      if (!this.hdOpen) return;
      event.preventDefault();
      try { this.hdViewport.setPointerCapture(event.pointerId); } catch (_) {}
      this.hdPointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (this.hdPointers.size >= 2) {
        const pair = this.#pointerPair();
        if (pair) this.hdGesture = { mode: 'pinch', ...pair, scale: this.hdScale, tx: this.hdTranslateX, ty: this.hdTranslateY };
      } else this.hdGesture = { mode: 'pan', x: event.clientX, y: event.clientY, tx: this.hdTranslateX, ty: this.hdTranslateY };
    }
    #onHdPointerMove(event) {
      if (!this.hdOpen || !this.hdPointers.has(event.pointerId)) return;
      event.preventDefault();
      this.hdPointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (this.hdPointers.size >= 2) {
        const pair = this.#pointerPair();
        if (!pair) return;
        if (!this.hdGesture || this.hdGesture.mode !== 'pinch') this.hdGesture = { mode: 'pinch', ...pair, scale: this.hdScale, tx: this.hdTranslateX, ty: this.hdTranslateY };
        const start = this.hdGesture;
        const ratio = start.distance > 0 ? pair.distance / start.distance : 1;
        const nextScale = clamp(start.scale * ratio, Number(this.options.hdMinScale), Number(this.options.hdMaxScale));
        const scaleRatio = nextScale / start.scale;
        this.hdScale = nextScale;
        this.hdTranslateX = (start.tx - start.midX) * scaleRatio + pair.midX;
        this.hdTranslateY = (start.ty - start.midY) * scaleRatio + pair.midY;
      } else if (this.hdGesture?.mode === 'pan') {
        this.hdTranslateX = this.hdGesture.tx + event.clientX - this.hdGesture.x;
        this.hdTranslateY = this.hdGesture.ty + event.clientY - this.hdGesture.y;
      }
      this.#clampHdTranslation();
      this.#applyHdTransform();
      if (this.hdPointers.size >= 2) { this.#updateHdScaleBar(false); this.#scheduleHdScaleBar(); }
    }
    #onHdPointerUp(event) {
      if (!this.hdPointers.has(event.pointerId)) return;
      event.preventDefault();
      this.hdPointers.delete(event.pointerId);
      if (this.hdPointers.size === 1) {
        const remaining = [...this.hdPointers.values()][0];
        this.hdGesture = { mode: 'pan', x: remaining.x, y: remaining.y, tx: this.hdTranslateX, ty: this.hdTranslateY };
      } else if (this.hdPointers.size === 0) { this.hdGesture = null; this.#scheduleHdScaleBar(); }
    }

    showHD() {
      global.GalaxyBlackBox?.recordCheckpoint?.('HD_OPEN_REQUEST',{
        busy:Boolean(this.busy),
        hdOpen:Boolean(this.hdOpen),
        arrived:Boolean(this.arrived)
      });

      // First claimant wins. Claim HD before doing any asynchronous or
      // presentation work so Random cannot start behind the overlay.
      if (!this.beginHdRequest()) {
        global.GalaxyBlackBox?.recordCheckpoint?.('HD_OPEN_BLOCKED_NAV_BUSY',{
          busy:Boolean(this.busy),
          destroyed:Boolean(this.destroyed),
          owner:String(this.interactionOwner||'')
        });
        return null;
      }

      requestPortraitOrientation('hd-view').catch(() => {});
      this.#hideRefreshSky();

      const destination = this.activeDestination;
      const validatedHdUrl = validHttpsUrl(destination?.hdUrl);

      if (!destination || !validatedHdUrl) {
        this.cancelHdRequest('no-usable-hd');
        throw new Error('No usable HD image is available for the active destination.');
      }

      if (this.hdOpen)
        return validatedHdUrl.href;

      global.GalaxyBlackBox?.recordCheckpoint?.('HD_RANDOM_LOCKED',{});

      // Preserve the user's exact sky position/zoom before HD obscures Aladin.
      this.hdSkySnapshot =
        this.#captureAladinState() ||
        this.#exactActiveAladinState(destination);

      const preparedImage = destination.preparedHdImage instanceof HTMLImageElement && destination.preparedHdImage.complete && destination.preparedHdImage.naturalWidth ? destination.preparedHdImage : null;
      this.#populateHdScience(destination);
      this.creditEl.textContent = destination.credit ? `CREDIT ${destination.credit}` : '';
      this.hdOverlay.classList.add('gvrg-hd-open');
      this.hdOpen = true;
      if (preparedImage) {
        this.#mountHdImage(preparedImage);
        this.hdImage.alt = destination.name;
        this.hdImage.onload = null;
        this.hdImage.onerror = null;
        this.hdLoading.textContent = '';
        this.hdLoading.style.display = 'none';
        this.#positionHdPresentation();
        this.#resetHdTransform();
        this.#updateHdScaleBar(true);
        return destination.preparedHdUrl || preparedImage.currentSrc || preparedImage.src;
      }
      this.#mountHdImage(this.hdFallbackImage);
      this.hdFallbackImage.removeAttribute('src');
      this.hdFallbackImage.alt = destination.name;
      this.hdLoading.textContent = 'LOADING HD IMAGE';
      this.hdLoading.style.display = 'block';
      this.#positionHdPresentation();
      this.hdFallbackImage.onload = () => {
        this.hdLoading.style.display = 'none';
        this.#positionHdPresentation();
        this.#resetHdTransform();
        this.#updateHdScaleBar(true);
      };
      this.hdFallbackImage.onerror = () => { this.hdLoading.textContent = 'HD IMAGE COULD NOT LOAD'; this.hdLoading.style.display = 'block'; };
      this.#resetHdTransform();
      this.hdFallbackImage.src = validatedHdUrl.href;
      return validatedHdUrl.href;
    }
    async downloadHD() {
      const destination = this.activeDestination;
      const validatedHdUrl = validHttpsUrl(destination?.hdUrl);
      if (!destination || !validatedHdUrl) throw new Error('No usable HD image is available for download.');
      const stem = cleanText(destination.archiveId || destination.name || 'galaxy-hd').replace(/[^a-z0-9._-]+/gi, '-').replace(/^-+|-+$/g, '') || 'galaxy-hd';
      const filename = `${stem}-HD.jpg`;
      if (destination.preparedHdUrl) {
        const anchor = document.createElement('a');
        anchor.href = destination.preparedHdUrl;
        anchor.download = filename;
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
        return destination.preparedHdUrl;
      }
      const response = await fetch(validatedHdUrl.href, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HD image download returned HTTP ${response.status}.`);
      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      try {
        const anchor = document.createElement('a');
        anchor.href = objectUrl;
        anchor.download = filename;
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
      } finally {
        setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
      }
      return validatedHdUrl.href;
    }
    backToSky(options = {}) {
      requestPortraitOrientation('sky-return').catch(() => {});
      if (!this.hdOpen) return;

      const recover = options?.recover !== false;
      const restoreState =
        this.hdSkySnapshot ||
        this.#exactActiveAladinState();

      const interlockSnapshot=this._hdInterlockSnapshot||null;
      this._hdInterlockSnapshot=null;

      const releaseHdInterlock=()=>{
        if (this.interactionOwner === 'hd') this.interactionOwner=null;

        // Navigation should never coexist with HD in 0101. If it somehow
        // does, keep controls locked rather than exposing a second owner.
        if (this.busy || this.interactionOwner === 'navigation') {
          global.GalaxyBlackBox?.recordCheckpoint?.('HD_CLOSED_NAV_OWNS_LOCK',{});
          return;
        }

        if (interlockSnapshot) {
          if (this.randomButton)
            this.randomButton.disabled=
              Boolean(interlockSnapshot.randomDisabled);

          if (this.viewHdButton)
            this.viewHdButton.disabled=
              Boolean(interlockSnapshot.viewHdDisabled);

          if (this.providerIconButton)
            this.providerIconButton.disabled=
              Boolean(interlockSnapshot.providerDisabled);
        }

        global.GalaxyBlackBox?.recordCheckpoint?.('HD_CLOSED',{
          recover:Boolean(recover)
        });
      };

      this.hdOverlay.classList.remove('gvrg-hd-open');

      if (this.hdImage === this.hdFallbackImage)
        this.hdFallbackImage.removeAttribute('src');

      this.hdFallbackImage.onload = null;
      this.hdFallbackImage.onerror = null;
      this.#resetHdTransform();
      this.hdOpen = false;
      this.hdSkySnapshot = null;

      if (recover) {
        requestAnimationFrame(() => {
          this.#restoreAladinState(restoreState,'hd-return');
          this.#armRefreshSkyWatchdog('hd-return');

          requestAnimationFrame(() => {
            this.#checkAndRecoverStaleAladin('hd-return-postcheck');
            releaseHdInterlock();
          });
        });
      } else {
        releaseHdInterlock();
      }
    }
    setPreparedHdResource(key, preparedHdUrl, preparedSource = '', preparedHdImage = null) {
      const destination = this.activeDestination;
      const requested = cleanText(key).toLowerCase();
      const activeKey = cleanText(destination?.archiveId || destination?.name).toLowerCase();
      const prepared = cleanText(preparedHdUrl);
      const image = preparedHdImage instanceof HTMLImageElement && preparedHdImage.complete && preparedHdImage.naturalWidth ? preparedHdImage : null;
      if (!destination || !requested || activeKey !== requested || !prepared || !image) return false;
      this.activeDestination = Object.freeze({ ...destination, preparedHdUrl: prepared, preparedSource: cleanText(preparedSource), preparedHdImage: image });
      return true;
    }
    async enrichWithGemini(destination = this.activeDestination) {
      if (!destination) return null;
      return this.#requestGeminiEnrichment(destination);
    }
    installNavigationWindow(options = {}) {
      if (this.randomNavigationWindow)
        return this.randomNavigationWindow;

      const {
        current = this.options.currentGalaxy || this.currentGalaxy,
        ...windowOptions
      } = options;

      this.randomNavigationWindow =
        new GalaxyRandomNavigationWindow(windowOptions);

      this.randomNavigationWindow.setCurrent(current);
      return this.randomNavigationWindow;
    }

    installPreparationEngine(options = {}) {
      if(this.preparationEngine)
        return this.preparationEngine;

      const randomNavigationWindow =
        options.randomNavigationWindow ||
        this.randomNavigationWindow;

      if(!randomNavigationWindow)
        throw new Error('RANDOM GALAXY 0062 NAVIGATION WINDOW MISSING');

      this.preparationEngine=
        createRandomPreparationEngine({
          ...options,
          randomNavigationWindow
        });

      return this.preparationEngine;
    }

    installHdArchiveIntegration(options = {}) {
      if (this.hdArchiveIntegration)
        return this.hdArchiveIntegration;

      this.hdArchiveIntegration =
        installHdArchiveIntegration(this, options);

      return this.hdArchiveIntegration;
    }

    showEarthReturn(destination) {
      this.earthReturnController?.show(destination);
      return this;
    }

    hideEarthReturn() {
      this.earthReturnController?.hide();
      return this;
    }

    setCurrentGalaxy(currentGalaxy) {
      if (!currentGalaxy || typeof currentGalaxy !== 'object') throw new TypeError('setCurrentGalaxy requires a galaxy object.');
      const coords = this.aladin.getRaDec();
      this.currentGalaxy = {
        name: cleanText(currentGalaxy.name || 'CURRENT POSITION'),
        ra: finiteNumber(currentGalaxy.ra) ?? finiteNumber(coords[0]) ?? 0,
        dec: finiteNumber(currentGalaxy.dec) ?? finiteNumber(coords[1]) ?? 0,
        distance: finiteNumber(currentGalaxy.distance)
      };
      return this;
    }
    getState() {
      const destination=this.activeDestination;

      const expectedKey=cleanText(
        destination?.archiveId||destination?.name
      ).toLowerCase();

      const image=this.hdImage;

      const mounted=Boolean(
        image instanceof HTMLImageElement &&
        image.parentNode===this.hdViewport
      );

      const complete=Boolean(
        mounted &&
        image.complete
      );

      const naturalWidth=
        mounted
          ? Number(image.naturalWidth)||0
          : 0;

      const naturalHeight=
        mounted
          ? Number(image.naturalHeight)||0
          : 0;

      const decoded=Boolean(
        complete &&
        naturalWidth>0 &&
        naturalHeight>0
      );

      const viewportRect=
        this.hdViewport?.getBoundingClientRect?.()||null;

      const viewportWidth=
        Number(viewportRect?.width)||0;

      const viewportHeight=
        Number(viewportRect?.height)||0;

      const renderedWidth=
        mounted
          ? Number(image.offsetWidth)||0
          : 0;

      const renderedHeight=
        mounted
          ? Number(image.offsetHeight)||0
          : 0;

      const open=Boolean(
        this.hdOpen &&
        this.hdOverlay?.classList?.contains('gvrg-hd-open')
      );

      const preparedImage=
        destination?.preparedHdImage instanceof HTMLImageElement
          ? destination.preparedHdImage
          : null;

      const preparedUrl=
        cleanText(destination?.preparedHdUrl);

      const fallbackUrl=
        cleanText(destination?.hdUrl);

      const imageUrl=
        mounted
          ? cleanText(image.currentSrc||image.src)
          : '';

      const preparedMounted=Boolean(
        mounted &&
        preparedImage &&
        image===preparedImage &&
        preparedUrl &&
        imageUrl===preparedUrl
      );

      const fallbackMounted=Boolean(
        mounted &&
        image===this.hdFallbackImage &&
        fallbackUrl &&
        imageUrl===fallbackUrl
      );

      const sourceMatch=Boolean(
        preparedMounted||
        fallbackMounted
      );

      const visibleGeometry=Boolean(
        viewportWidth>0 &&
        viewportHeight>0 &&
        renderedWidth>0 &&
        renderedHeight>0
      );

      const presented=Boolean(
        open &&
        mounted &&
        decoded &&
        sourceMatch &&
        visibleGeometry
      );

      const presentationState=
        !open
          ? 'CLOSED'
          : !mounted
            ? 'UNMOUNTED'
            : !complete
              ? 'LOADING'
              : !decoded
                ? 'FAILED_OR_EMPTY'
                : !sourceMatch
                  ? 'IDENTITY_MISMATCH'
                  : !visibleGeometry
                    ? 'NOT_RENDERED'
                    : 'PRESENTED';

      return {
        version: VERSION,
        busy: this.busy,
        arrived: this.arrived,
        hdOpen: this.hdOpen,
        hdScale: this.hdScale,

        hdPresentation: Object.freeze({
          state:presentationState,
          open,
          presented,
          mounted,
          complete,
          decoded,
          sourceMatch,
          preparedMounted,
          fallbackMounted,
          source:
            preparedMounted
              ? 'PREPARED'
              : fallbackMounted
                ? 'FALLBACK'
                : '',
          expectedKey,
          imageUrl,
          preparedUrl,
          fallbackUrl,
          naturalWidth,
          naturalHeight,
          renderedWidth,
          renderedHeight,
          viewportWidth,
          viewportHeight
        }),

        currentGalaxy: { ...this.currentGalaxy },
        activeDestination: this.activeDestination,
        interactionOwner:this.interactionOwner,
        prefetched: Boolean(this.prefetchedDestination),
        galaxyOnly: true,
        catalogCount: Number(
          typeof this.options.getCatalogCount === 'function'
            ? this.options.getCatalogCount()
            : this.catalogCount
        ) || 0,
        discoverySource: 'LOCAL GALAXY PROVIDER',
        digitFont: FONT_URLS.digits,
        travelSeconds: Number(this.options.travelSeconds),
        geminiKeyEmbedded: false
      };
    }
    destroy() {
      if (this.destroyed) return;
      this.destroyed = true;
      this.#hideRefreshSky();
      this.#endTravelHud();
      this.earthReturnController?.destroy();
      this.earthReturnController = null;

      this.hdArchiveIntegration?.destroy();
      this.hdArchiveIntegration = null;
      this.homeOverlay?.remove();
      this.universeContext?.remove();
      this.homeOverlay = null;
      this.universeContext = null;
      if (this.hdScaleBarTimer) clearTimeout(this.hdScaleBarTimer);
      if (this.randomButton) {
        if (this.options.bindClick) this.randomButton.removeEventListener('click', this._randomClick);
        this.randomButton.removeEventListener(this.options.requestEvent, this._randomRequest);
      }
      this.viewHdButton.removeEventListener('click', this._hdClick);
      this.providerIconButton.removeEventListener('click', this._hdClick);
      this.downloadButton.removeEventListener('click', this._downloadClick);
      this.backButton.removeEventListener('click', this._backClick);
      this.hdViewport.removeEventListener('pointerdown', this._pointerDown);
      this.hdViewport.removeEventListener('pointermove', this._pointerMove);
      this.hdViewport.removeEventListener('pointerup', this._pointerUp);
      this.hdViewport.removeEventListener('pointercancel', this._pointerUp);
      this.refreshSkyButton.removeEventListener('click',this._refreshSkyClick);

      window.removeEventListener('pageshow', this._viewerPageShow);
      window.removeEventListener('focus', this._viewerFocus);
      document.removeEventListener('visibilitychange', this._viewerVisibility);

      this.hdFallbackImage.removeAttribute('src');
      if (this.standaloneButton) this.standaloneButton.remove();
      this.root.remove();
      instances.delete(this.host);
      if (this.standaloneHost) this.standaloneHost.remove();
    }
    static mount(host, options = {}) {
      const existing = instances.get(host);
      if (existing && !existing.destroyed) return existing;
      return new GalaxyRandomGalaxy({ ...options, host });
    }
    static launch(options = {}) {
      if (!options.aladin) throw new TypeError('GalaxyRandomGalaxy.launch requires an Aladin instance.');
      let host = options.host instanceof Element ? options.host : null;
      let standaloneHost = null;
      if (!host) {
        host = document.createElement('div');
        host.className = 'gvrg-standalone-host';
        host.style.cssText = 'position:fixed;inset:0;z-index:2147482000;pointer-events:none';
        document.body.appendChild(host);
        standaloneHost = host;
      }
      let randomButton = options.randomButton instanceof Element ? options.randomButton : null;
      let standaloneButton = null;
      if (!randomButton && options.standaloneControl !== false) {
        randomButton = document.createElement('button');
        randomButton.type = 'button';
        randomButton.className = 'gvrg-button gvrg-standalone-random';
        randomButton.textContent = cleanText(options.randomButtonLabel || 'RANDOM GALAXY');
        randomButton.style.cssText = 'position:absolute;right:14px;bottom:14px;z-index:10010;pointer-events:auto';
        host.appendChild(randomButton);
        standaloneButton = randomButton;
      }
      const instance = GalaxyRandomGalaxy.mount(host, { ...options, aladin: options.aladin, randomButton, bindClick: standaloneButton ? true : options.bindClick });
      instance.standaloneHost = standaloneHost;
      instance.standaloneButton = standaloneButton;
      return instance;
    }
  }

  GalaxyRandomGalaxy.VERSION = VERSION;
  GalaxyRandomGalaxy.bootstrapHomePresentation = bootstrapHomePresentation;
  GalaxyRandomGalaxy.FONT_URLS = FONT_URLS;
  GalaxyRandomGalaxy.DEFAULTS = DEFAULTS;
  GalaxyRandomGalaxy.PROVIDER_CONTRACT = Object.freeze({
    galaxyDiscovery: {
      defaultSource: 'local validated galaxy provider',
      browserOnly: true,
      backendRequired: false,
      selection: 'Galaxy-category observation images from supported providers',
      liveArchiveScraping: false
    },
    provider: {
      request: { excludeName: 'optional previous destination name' },
      response: { destination: { name: 'required', ra: 'required ICRS degrees', dec: 'required', distanceMly: 'required positive million light-years', constellation: 'required', age: 'optional authoritative age text', physicalSizeLy: 'optional authoritative physical size in light-years', designation: 'optional catalog designation', commonName: 'optional common/title name', preparedHdUrl: 'optional retained runtime object URL', preparedHdImage: 'optional retained decoded HTMLImageElement for immediate HD display', fov: 'optional degrees', hdUrl: 'required trusted provider image URL', sourceUrl: 'required trusted provider source URL', credit: 'optional/provider supplied', imageType: 'Observation preferred', category: 'Galaxies required', telescope: 'supported telescope/provider metadata' } }
    },
    geminiEndpoint: {
      method: 'POST',
      optional: true,
      secretRule: 'Store GEMINI_API_KEY server-side only. Never place it in this JavaScript module.',
      modelHint: 'Gemini Flash-Lite'
    }
  });


  // REQ-017I / ECO-026C — authoritative future-ten controller
(()=>{
'use strict';
const FUTURE_TARGET=10;
const POLL_MS=80;
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const keyOf=item=>String(item?.key||item?.destination?.archiveId||item?.destination?.name||item?.archiveId||item?.name||'').trim().toLowerCase();
let core=null;
let randomGalaxy=null;
let randomNavigationWindow=null;
let preparationEngine=null;
let archiveIntegration=null;
let catalog=[];
let catalogByKey=new Map();
let catalogByName=new Map();

const HEAD_HD_MAX_RETRIES=3;
const HEAD_HD_RETRY_DELAY_MS=1500;
const HEAD_HD_QUARANTINE_MS=60000;
const poisonedFutureUntil=new Map();

function isQuarantinedFutureKey(key){
  key=String(key||'').trim().toLowerCase();
  if(!key)return false;

  const until=Number(poisonedFutureUntil.get(key)||0);
  if(!until)return false;

  if(Date.now()>=until){
    poisonedFutureUntil.delete(key);
    return false;
  }

  return true;
}
const futureRecords=new Map();
let activeRecord=null;
let nextSequence=0;
let installed=false;
let suspended=false;
let hdFeedbackBusy=false;
let hdFeedbackSerial=0;
let randomRequestPending=false;
let randomRequestSerial=0;
let legacyPrefetchDrain=Promise.resolve();
let authoritativePendingDestination=null;
let failedHeadButton=null;
const RANDOM_REQUEST_TIMEOUT_MS=30000;

// AR129 - FUTURE[0] HD/AVM presentation readiness is the sole Random gate.
// Navigation Aladin prefetch and WEB preload are disabled.
const PENDING_HD_WAIT_TIMEOUT_MS=45000;
let startupHdGateReleased=false;

function updateStartupRandomButton(){
  if(!core?.randomGalaxyButton)return false;

  const button=core.randomGalaxyButton;

  if(startupHdGateReleased)return true;

  if(button.dataset.gv130aReadyTransition==='running')
    return false;

  const headReady=hasReadyNavigation();

  if(!headReady){
    setRandomButtonText(
      button,
      'DOWNLOADING IMAGE',
      {busy:true,imageWait:true}
    );
    button.disabled=true;
    return false;
  }

  if(button.dataset.gv130aReadyTransition!=='done'){
    button.dataset.gv130aReadyTransition='running';
    startupHdGateReleased=true;

    setRandomButtonText(
      button,
      'READY TO NAVIGATE',
      {busy:false,ready:true,imageWait:false}
    );
    button.disabled=false;

    setTimeout(()=>{
      button.dataset.gv130aReadyTransition='done';
      updateRandomButtonReadyState();
    },1000);

    return true;
  }

  startupHdGateReleased=true;
  button.disabled=false;
  return true;
}

async function waitForPendingHdReady(record,serial){
  const startedAt=performance.now();

  for(;;){
    if(serial!==randomRequestSerial)
      throw new Error('RANDOM REQUEST SUPERSEDED');

    const pending=randomNavigationWindow.getState().pending;
    if(
      pending?.kind!=='random' ||
      pending?.bundle!==record
    )throw new Error('RANDOM PENDING OWNERSHIP CHANGED');

    const hd=hdStateFor(record);

    if(hd.state==='READY' && hd.presentationReady){
      setRandomWaitComet(core?.randomGalaxyButton,false);
      return true;
    }

    setRandomWaitComet(core?.randomGalaxyButton,true);

    if(hd.state==='READY'){
      try{
        await preparationEngine.ensureHdFramingReady?.(record.destination);
      }catch(error){
        console.warn(
          'GALAXY VIEWER PENDING AVM FRAMING RETRY WARNING',
          record.key,
          error
        );
      }
    }else{
      preparationEngine.requestHdPrefetch?.(record.destination);
    }

    if(performance.now()-startedAt>=PENDING_HD_WAIT_TIMEOUT_MS)
      throw new Error('RANDOM PENDING PRESENTATION WAIT TIMEOUT');

    await sleep(POLL_MS);
  }
}

const SESSION_REPEAT_WINDOW=500;
const sessionVisitedKeys=new Set();
const sessionVisitedOrder=[];

function rememberCommittedDestination(destination){
  const key=keyOf(destination);
  if(!key)return;

  if(sessionVisitedKeys.has(key)){
    throw new Error(

    );
  }

  sessionVisitedKeys.add(key);
  sessionVisitedOrder.push(key);

  while(sessionVisitedOrder.length>SESSION_REPEAT_WINDOW){
    const expired=sessionVisitedOrder.shift();
    if(expired)sessionVisitedKeys.delete(expired);
  }
}


function findDestinationByName(name){return catalogByName.get(String(name||'').trim().toLowerCase())||null}
function findDestinationByKey(key){return catalogByKey.get(String(key||'').trim().toLowerCase())||null}
function currentBlockedKeys(){
  const blocked=new Set();
  for(const key of sessionVisitedKeys)blocked.add(key);
  for(const key of futureRecords.keys())blocked.add(key);
  if(activeRecord?.key)blocked.add(activeRecord.key);
  const navState=randomNavigationWindow.getState();
  for(const destination of [...navState.history,...navState.forwardHistory]){
    const key=keyOf(destination);
    if(key)blocked.add(key);
  }
  if(navState.pending?.destination){
    const key=keyOf(navState.pending.destination);
    if(key)blocked.add(key);
  }
  if(navState.current){
    const key=keyOf(navState.current);
    if(key)blocked.add(key);
  }
  if(navState.locked){
    const key=keyOf(navState.locked);
    if(key)blocked.add(key);
  }
  return blocked;
}
function uniqueRecords(records){
  const seen=new Set(),out=[];
  for(const record of records||[]){
    if(!record?.key||seen.has(record.key))continue;
    seen.add(record.key);out.push(record);
  }
  return out;
}
function pipelineDestinations(){
  const state=preparationEngine.getPrefetchState?.()||{};
  const names=[
    ...(state.readyDestinations||[]),
    ...(state.queuedDestinations||[])
  ];
  const seen=new Set(),out=[];
  for(const name of names){
    const destination=catalogByName.get(String(name||'').trim().toLowerCase());
    const key=keyOf(destination);
    if(!destination||!key||seen.has(key))continue;
    seen.add(key);out.push(destination);
  }
  return out;
}
function chooseUniqueDestination(){
  const blocked=currentBlockedKeys();
  const pool=catalog.filter(destination=>{
    const key=keyOf(destination);
    return key&&!blocked.has(key)&&!isQuarantinedFutureKey(key);
  });
  if(!pool.length)return null;
  return pool[Math.floor(Math.random()*pool.length)];
}

/*
 * RANDOM GALAXY 0092 — NAVIGATION 0012 SEAM
 *
 * Random Galaxy owns preparation, FIFO locking, travel, history and
 * commit/rollback. Navigation 0006 owns destination ordering after the
 * single bootstrap destination.
 */
let navigationPlanner=null;
let navigationPlannerPromise=null;
let navigationModulePromise=null;
let startupRoutePromise=null;

function navigation0008Url(){
  const scripts=[...document.scripts];
  const owner=
    scripts.find(script=>
      /\/random-galaxy\/gv-random-galaxy-01\d{2}\.js(?:[?#].*)?$/i.test(
        String(script.src||'')
      )
    ) ||
    document.currentScript ||
    null;

  if(owner?.src){
    return new URL(
      '../navigation/gv-navigation-0018.js',
      owner.src
    ).href;
  }

  return '/viewer/modules/navigation/gv-navigation-0018.js';
}

function applyNavigation0013RuntimeConfig(api=null){
  // Navigation 0006 owns active-flight choreography. Random keeps this
  // hook only as a module/config availability checkpoint.
  return api?.CONSTANTS||null;
}

function ensureNavigationModule0013(){
  const existing=window.GalaxyViewerNavigation;

  if(existing?.VERSION==='0018'){
    applyNavigation0013RuntimeConfig(existing);
    return Promise.resolve(existing);
  }

  if(existing && existing.VERSION!=='0018'){
    return Promise.reject(
      new Error(
        `NAVIGATION MODULE VERSION COLLISION: ${existing.VERSION}`
      )
    );
  }

  if(navigationModulePromise)return navigationModulePromise;

  navigationModulePromise=new Promise((resolve,reject)=>{
    const url=navigation0008Url();

    const prior=[...document.scripts].find(script=>
      script.dataset.gvNavigation0007==='1'
    );

    const finish=()=>{
      const api=window.GalaxyViewerNavigation;

      if(api?.VERSION!=='0018'){
        reject(
          new Error(
            'NAVIGATION 0018 EXPORT MISSING OR VERSION MISMATCH'
          )
        );
        return;
      }

      applyNavigation0013RuntimeConfig(api);
      resolve(api);
    };

    if(prior){
      if(prior.dataset.ready==='1'){
        finish();
        return;
      }

      prior.addEventListener('load',finish,{once:true});
      prior.addEventListener(
        'error',
        ()=>reject(
          new Error('NAVIGATION 0018 SCRIPT LOAD FAILED')
        ),
        {once:true}
      );
      return;
    }

    const script=document.createElement('script');
    script.src=url;
    script.async=true;
    script.dataset.gvNavigation0007='1';

    script.addEventListener(
      'load',
      ()=>{
        script.dataset.ready='1';
        finish();
      },
      {once:true}
    );

    script.addEventListener(
      'error',
      ()=>reject(
        new Error(`NAVIGATION 0018 SCRIPT LOAD FAILED: ${url}`)
      ),
      {once:true}
    );

    document.head.appendChild(script);
  }).catch(error=>{
    navigationModulePromise=null;
    throw error;
  });

  return navigationModulePromise;
}

async function ensureNavigationPlanner(anchorDestination=null){
  if(navigationPlanner)return navigationPlanner;
  if(navigationPlannerPromise)return navigationPlannerPromise;

  navigationPlannerPromise=(async()=>{
    const api=await ensureNavigationModule0013();

    if(typeof api.create!=='function')
      throw new Error('NAVIGATION 0018 CREATE API MISSING');

    /*
     * RANDOM 0121 — refresh the authoritative preparation catalog at the
     * planner boundary. install() may run while catalog loading is still in
     * progress, so its bootstrap snapshot must not become the lifetime
     * navigation catalog.
     */
    const latestCatalog=preparationEngine.getGalaxyCatalog();

    if(Array.isArray(latestCatalog) && latestCatalog.length){
      catalog=[...latestCatalog];
      catalogByKey=new Map(
        catalog.map(destination=>[keyOf(destination),destination])
      );
      catalogByName=new Map(
        catalog.map(destination=>[
          String(destination?.name||'').trim().toLowerCase(),
          destination
        ])
      );
    }

    const blocked=currentBlockedKeys();

    const eligibleCatalog=catalog.filter(destination=>{
      const key=keyOf(destination);
      return key &&
        !blocked.has(key) &&
        !isQuarantinedFutureKey(key);
    });

    if(eligibleCatalog.length<130){
      throw new Error(
        `RANDOM 0121 NAVIGATION CATALOG NOT READY: ${eligibleCatalog.length}/130`
      );
    }

    const planner=api.create({
      catalog:eligibleCatalog
    });

    if(
      !planner ||
      typeof planner.initialize!=='function' ||
      typeof planner.peekNext!=='function' ||
      typeof planner.getUpcoming!=='function' ||
      typeof planner.commitNext!=='function'
    ){
      throw new Error('NAVIGATION 0018 PLANNER API INCOMPLETE');
    }

    await planner.initialize(anchorDestination);

    navigationPlanner=planner;

    return planner;
  })();

  try{
    return await navigationPlannerPromise;
  }finally{
    navigationPlannerPromise=null;

    if(navigationPlanner){
      queueMicrotask(()=>{
        try{
          reconcileFutureQueue();
          updateRandomButtonReadyState();
        }catch(error){
          console.error(
            'RANDOM 0105 NAVIGATION 0018 RECONCILE FAILURE',
            error
          );
        }
      });
    }
  }
}

async function advanceNavigationPlannerAfterArrival(arrived){
  const arrivedKey=keyOf(arrived);

  if(arrivedKey && sessionVisitedKeys.has(arrivedKey)){
    throw new Error(

    );
  }

  if(!arrivedKey)
    throw new Error(
      'RANDOM 0092 ARRIVAL KEY MISSING'
    );

  if(!navigationPlanner){
    /*
     * Recovery only: if the planner was lost, rebuild from the galaxy
     * actually reached. Do not consume that galaxy as a planned item.
     */
    rememberCommittedDestination(arrived);
    await ensureNavigationPlanner(arrived);
    return;
  }

  const expected=navigationPlanner.peekNext();

  if(!expected || keyOf(expected)!==arrivedKey){
    throw new Error(
      'RANDOM 0105 NAVIGATION 0018 COMMIT IDENTITY MISMATCH'
    );
  }

  // AR125: Navigation 0018 must validate/commit the immutable planner record.
  // The arrived destination may contain runtime AVM RA/Dec substitutions.
  await navigationPlanner.commitNext(expected);
  rememberCommittedDestination(arrived);

  if(navigationPlanner.remaining()===0){
    navigationPlanner=null;
    navigationPlannerPromise=null;
    await ensureNavigationPlanner(arrived);
  }
}

function makeRecord(destination){
  const key=keyOf(destination);
  return {
    sequence:++nextSequence,
    key,
    destination,
    hd:{state:'QUEUED',resource:null,sourceKind:''}
  };
}
function orderedFutureRecords(){
  return randomNavigationWindow.getFuture().filter(Boolean);
}
function pumpPreparationPhases(){
  if(
    suspended ||
    preparationEngine?.getBackgroundWorkSuspended?.()
  )return;

  const future=orderedFutureRecords();
  if(!future.length)return;

  const head=future[0];
  const headHd=hdStateFor(head);

  // AR129: FUTURE[0] HD/AVM is the sole readiness gate.
  if(!(headHd.state==='READY' && headHd.presentationReady)){
    preparationEngine?.requestHdPrefetch?.(head.destination,true);
    return;
  }

  // Keep filling the remaining HD/AVM queue without delaying FUTURE[0].
  for(const record of future.slice(1)){
    const hd=hdStateFor(record);
    if(!(hd.state==='READY' && hd.presentationReady)){
      preparationEngine?.requestHdPrefetch?.(record.destination,false);
    }
  }

  updateRandomButtonReadyState();
}
function addFuture(destination){
  if(!destination)return false;
  const key=keyOf(destination);
  if(!key||isQuarantinedFutureKey(key)||currentBlockedKeys().has(key))return false;
  const record=makeRecord(destination);
  if(!randomNavigationWindow.appendFuture(record))return false;
  futureRecords.set(key,record);
  return true;
}
function pruneFutureRecords(){
  const allowed=new Set(randomNavigationWindow.getFuture().map(bundle=>bundle.key));
  for(const [key,record] of futureRecords){
    if(allowed.has(key))continue;
    futureRecords.delete(key);
  }
}
function reconcileFutureQueue(){
  pruneFutureRecords();

  /*
   * AR123 startup contract:
   * Navigation 0018 owns destination selection from the first route item.
   * No standalone Random Galaxy bootstrap destination is allowed.
   */
  if(!navigationPlanner&&!navigationPlannerPromise){
    void ensureNavigationPlanner(null).catch(error=>{
      if(!String(error?.message||'').includes('NAVIGATION CATALOG NOT READY')){
        console.error(
          'AR123 NAVIGATION 0018 STARTUP INITIALIZATION FAILURE',
          error
        );
      }
    });
  }

  /*
   * Only after Monte Carlo has completed do we feed destinations into the
   * Random future queue. Append the complete needed batch first; HD/AVM
   * preparation then proceeds with FUTURE[0] priority.
   */
  if(navigationPlanner){
    const needed=randomNavigationWindow.needsFuture();

    if(needed>0){
      const upcoming=navigationPlanner.getUpcoming(
        Math.max(FUTURE_TARGET,needed)
      );

      for(const destination of upcoming){
        if(randomNavigationWindow.needsFuture()<=0)break;

        const key=keyOf(destination);

        if(
          !key ||
          isQuarantinedFutureKey(key)
        )continue;

        addFuture(destination);
      }
    }
  }

  pumpPreparationPhases();
}
async function consumeNext(excludeName=''){
  reconcileFutureQueue();

  const excluded=String(excludeName||'').trim().toLowerCase();
  const readyForNavigation=bundle=>{
    const destination=bundle?.destination;
    const key=String(bundle?.key||'').trim().toLowerCase();
    if(!destination||!key)return false;
    const hd=hdStateFor(bundle);
    return String(destination.name||'').trim().toLowerCase()!==excluded&&
      key!==activeRecord?.key&&
      Boolean(bundle.hd?.resource)&&
      bundle.hd?.state==='READY'&&
      hd.presentationReady===true;
  };

  const locked=randomNavigationWindow.lockReadyNext(readyForNavigation);
  if(!locked)return null;

  const lockedKey=String(locked.key||'').trim().toLowerCase();
  const record=futureRecords.get(lockedKey)||null;
  if(!record||record!==locked){
    randomNavigationWindow.rollbackLocked();
    throw new Error('RANDOM GALAXY LOCKED BUNDLE IDENTITY MISMATCH');
  }

  activeRecord=record;

  let destination=preparationEngine.activateQueuedDestination(record.destination,excludeName);
  activeRecord.destination=destination;

  const claimed=randomNavigationWindow.claimLocked();
  if(claimed!==record||keyOf(claimed)!==lockedKey){
    randomNavigationWindow.rollbackPending();
    throw new Error('RANDOM GALAXY CLAIMED BUNDLE IDENTITY MISMATCH');
  }

  setTimeout(reconcileFutureQueue,100);
  return destination;
}
function normalizeHdState(state){
  const value=String(state||'').toUpperCase();
  if(value==='READY')return 'READY';
  if(value==='DOWNLOADING'||value==='DECODING')return value;
  if(value==='SUSPENDED')return 'SUSPENDED';
  if(value.includes('RETRY'))return 'RETRY';
  if(value==='QUEUED')return 'QUEUED';
  return value||'QUEUED';
}
function hdStateFor(record){
  const status=(preparationEngine.getDownloadStatus?.()||[]).find(item=>String(item?.key||'').toLowerCase()===record.key);
  const state=normalizeHdState(status?.state);
  const resource=state==='READY'?preparationEngine.getHdPreparedResource?.(record.key)||null:null;
  const expectedKey=String(record?.key||'').trim().toLowerCase();
  const stateKey=String(status?.key||'').trim().toLowerCase();
  const resourceKey=String(resource?.key||'').trim().toLowerCase();
  const identityMatch=state==='READY'
    ? Boolean(resource&&resourceKey===expectedKey)
    : Boolean(!stateKey||stateKey===expectedKey);
  const resourceUrl=String(
    resource?.objectUrl||
    resource?.url||
    resource?.src||
    ''
  ).trim();
  const preparedImage=resource?.image||null;
  const imageReady=Boolean(
    preparedImage instanceof HTMLImageElement &&
    preparedImage.complete &&
    Number(preparedImage.naturalWidth)>0 &&
    Number(preparedImage.naturalHeight)>0
  );
  const destinationMatch=Boolean(
    resource?.destination &&
    keyOf(resource.destination)===expectedKey
  );
  const resourceUrlReady=Boolean(resourceUrl);
  const hdReady=Boolean(
    state==='READY' &&
    resource &&
    identityMatch &&
    destinationMatch &&
    imageReady &&
    resourceUrlReady
  );
  const framingReady=
    state!=='READY' ||
    resource?.framingState==='READY';
  const presentationReady=Boolean(
    hdReady &&
    framingReady
  );
  const hdState=
    state==='READY'
      ? (hdReady ? 'READY' : 'RETRY')
      : state;

  const preparedDestination=
    presentationReady
      ? resource?.destination||null
      : null;
  if(
    state==='READY' &&
    identityMatch &&
    preparedDestination &&
    keyOf(preparedDestination)===expectedKey &&
    preparedDestination!==record.destination
  ){
    record.destination=preparedDestination;
    record.aladin={
      state:'QUEUED',
      receipt:null,
      requested:false,
      ra:Number(preparedDestination.ra),
      dec:Number(preparedDestination.dec),
      fov:Number(preparedDestination.fovDegrees),
      rotation:Number.isFinite(Number(preparedDestination.aladinRotation))
        ? Number(preparedDestination.aladinRotation)
        : 0
    };
  }

  record.hd={
    state:hdState,
    resource,
    sourceKind:String(resource?.sourceKind||status?.sourceKind||'')
  };
  return {
    state:hdState,
    progress:hdState==='READY'?100:null,
    detail:record.hd.sourceKind,
    expectedKey,
    stateKey,
    resourceKey,
    identityMatch,
    destinationMatch,
    imageReady,
    resourceUrlReady,
    framingReady,
    preparedReady:presentationReady,
    presentationReady,
    resourceUrl
  };
}

function showFailedHeadButton(_record){
  if(failedHeadButton){
    try{failedHeadButton.remove()}catch(_){}
    failedHeadButton=null;
  }
}

function retirePoisonedHead(record){
  if(!record?.key)return false;

  const future=[...randomNavigationWindow.getFuture()];
  if(!future.length||future[0]!==record)return false;

  const key=record.key;

  // Quarantine this destination so queue replenishment cannot select the
  // exact same broken HD asset again immediately.
  poisonedFutureUntil.set(
    key,
    Date.now()+HEAD_HD_QUARANTINE_MS
  );

  // Preserve the exact order of every healthy record behind future[0].
  randomNavigationWindow.replaceFuture(future.slice(1));
  futureRecords.delete(key);

  console.warn(
    'RANDOM GALAXY POISONED FUTURE HD EJECTED',
    key,
    'after',
    Number(record.hdRetryAttempts||0),
    'retries'
  );

  // Refill the missing tail position with a different usable destination.
  queueMicrotask(reconcileFutureQueue);
  return true;
}

function healHeadHdFailure(){
  const record=randomNavigationWindow.peekNext?.();
  if(!record?.key)return false;

  const hd=hdStateFor(record);

  if(hd.state==='READY'){
    record.hdRetryAttempts=0;
    record.hdNextRetryAt=0;
    return false;
  }

  if(hd.state!=='RETRY')return false;

  const now=Date.now();
  const retryAt=Number(record.hdNextRetryAt||0);

  if(now<retryAt)return false;

  const attempts=Number(record.hdRetryAttempts||0);

  if(attempts>=HEAD_HD_MAX_RETRIES){
    record.manualContinueRequired=true; showFailedHeadButton(record); return false;
  }

  record.hdRetryAttempts=attempts+1;
  record.hdNextRetryAt=now+HEAD_HD_RETRY_DELAY_MS;

  console.warn(
    'RANDOM GALAXY FUTURE[0] HD RETRY',
    record.key,
    record.hdRetryAttempts,
    'OF',
    HEAD_HD_MAX_RETRIES
  );

  // Priority prefetch intentionally bypasses the ordinary retry-wait
  // delay so the authoritative FIFO head gets a bounded recovery chance.
  preparationEngine.requestHdPrefetch?.(record.destination);

  return false;
}

// AR130A BUTTON STATE PATCH 001
function hasReadyNavigation(){
  if(healHeadHdFailure())return false;

  return randomNavigationWindow.isNextReady(bundle=>{
    if(!bundle?.destination||!bundle?.key)return false;

    const hd=hdStateFor(bundle);

    return Boolean(
      bundle.hd?.resource &&
      bundle.hd?.state==='READY' &&
      hd.presentationReady===true
    );
  });
}
const GV_AR129T_STARTUP_HD_READY_TARGET=5;
let gvAr129tStartupHdGateReleased=false;
let gvAr129tStartupHdReadyTimer=0;

function gvAr129tEnsureStartupHdStatusStyle(){
  return;
}

function gvAr129tStartupHdReadiness(){
  const future=orderedFutureRecords().slice(0,10);
  let ready=0;

  for(const record of future){
    if(hdStateFor(record).state==='READY')ready++;
  }

  const head=future[0]||null;
  const headReady=Boolean(head&&hdStateFor(head).state==='READY');

  return {ready,total:future.length,headReady};
}

function updateRandomButtonReadyState(){
  if(!core?.randomGalaxyButton)return;

  const button=core.randomGalaxyButton;
  const state=randomGalaxy?.getState?.()||{};

  if(button.dataset.gv130aReadyTransition==='running')
    return;

  if(!startupHdGateReleased){
    updateStartupRandomButton();
    return;
  }

  const busy=Boolean(
    randomRequestPending ||
    state.busy
  );

  const head=orderedFutureRecords()[0]||null;
  let headReady=false;

  if(head?.destination&&head?.key){
    const hd=hdStateFor(head);
    headReady=Boolean(
      head.hd?.resource &&
      head.hd?.state==='READY' &&
      hd.presentationReady===true
    );
  }

  button.disabled=Boolean(
    busy ||
    !headReady
  );

  if(busy)return;

  if(!headReady){
    setRandomButtonText(
      button,
      'DOWNLOADING IMAGE',
      {busy:true,imageWait:true}
    );
    return;
  }

  setRandomButtonText(
    button,
    'RANDOM GALAXY',
    {busy:false,ready:false,imageWait:false}
  );
}
async function waitForLockedReady(locked,serial){
  const started=performance.now();
  for(;;){
    if(serial!==randomRequestSerial)throw new Error("RANDOM REQUEST SUPERSEDED");
    if(randomNavigationWindow.getState().locked!==locked)throw new Error("RANDOM LOCK OWNERSHIP CHANGED");
    healHeadHdFailure();
    const hd=hdStateFor(locked);
    if(Boolean(locked.hd?.resource)&&locked.hd?.state==="READY"&&hd.presentationReady===true)return true;
    if(performance.now()-started>=RANDOM_REQUEST_TIMEOUT_MS){locked.manualContinueRequired=true;showFailedHeadButton(locked);throw new Error("RANDOM LOCKED FUTURE0 TIMEOUT");}
    await sleep(POLL_MS);
  }
}

async function waitForNavigationReleaseAfterHdTakeover(timeoutMs=1200){
  const started=performance.now();
  while(randomRequestPending||randomGalaxy?.getState?.().busy){
    if(performance.now()-started>=timeoutMs)return false;
    await sleep(16);
  }
  return true;
}

async function requestRandomNavigation(){
  GV_TRACE.enabled&&gvTrace(5937,'REQUEST_ENTER',{
    pending:Boolean(randomRequestPending),
    busy:Boolean(randomGalaxy?.getState?.().busy)
  });
  /*
   * RANDOM 0106 — HD and Random navigation are mutually exclusive with takeover.
   * A competing Random request is cancelled while HD owns or is acquiring
   * the viewer. This closes the HD preload wait race and any stale-control
   * programmatic entry path.
   */
  let tookOverHd=false;
  {
    const state=randomGalaxy?.getState?.()||{};
    if(
      state.hdOpen||
      state.interactionOwner==='hd'||
      hdFeedbackBusy
    ){
      tookOverHd=true;
      global.GalaxyBlackBox?.recordCheckpoint?.('RANDOM_REQUEST_TAKEOVER_HD',{
        hdOpen:Boolean(state.hdOpen),
        owner:String(state.interactionOwner||''),
        hdFeedbackBusy:Boolean(hdFeedbackBusy)
      });
      hdFeedbackSerial++;
      hdFeedbackBusy=false;
      if (state.hdOpen) randomGalaxy.backToSky?.({recover:false});
      else randomGalaxy.cancelHdRequest?.('random-takeover');
    }
  }

  if(tookOverHd && (randomRequestPending||randomGalaxy?.getState?.().busy)){
    const released=await waitForNavigationReleaseAfterHdTakeover();
    global.GalaxyBlackBox?.recordCheckpoint?.(
      released?'RANDOM_TAKEOVER_HD_RELEASED':'RANDOM_TAKEOVER_HD_RELEASE_TIMEOUT',
      {}
    );
    if(!released)return null;
  }

  if(randomRequestPending||randomGalaxy?.getState?.().busy)return null;

  const state=randomNavigationWindow?.getState?.()||{};
  const record=state.future?.[0]||null;

  if(!record)
    throw new Error('RANDOM 0065 FUTURE0 DESTINATION IS NOT AVAILABLE');

  let destination=record.destination||record;

  const locked=randomNavigationWindow.lockNext?.()||null;

  if(!locked||locked!==record||keyOf(locked)!==keyOf(record)){
    randomNavigationWindow.rollbackLocked?.();
    throw new Error('RANDOM 0070 PRE-TRAVEL FIFO LOCK IDENTITY MISMATCH');
  }

  const claimed=randomNavigationWindow.claimLocked?.()||null;

  if(!claimed||claimed!==record||keyOf(claimed)!==keyOf(record)){
    randomNavigationWindow.rollbackPending?.();
    throw new Error('RANDOM 0070 PRE-TRAVEL FIFO CLAIM IDENTITY MISMATCH');
  }

  randomRequestPending=true;
  const requestSerial=++randomRequestSerial;
  updateRandomButtonReadyState();

  // AR120 fallback: keep the exact claimed destination and wait only for
  // its HD resource when necessary. No destination substitution.
  await waitForPendingHdReady(record,requestSerial);

  /*
   * AP-REQ-016 — transfer the exact owned FIFO destination through the
   * preparation engine before visible travel.  This is not a readiness gate:
   * a prepared resource is attached when retained, otherwise the same exact
   * destination proceeds unprepared and showHD may use its normal fallback.
   */
  const handedOffDestination=
    preparationEngine.activateQueuedDestination(
      destination,
      randomGalaxy?.currentGalaxy?.name||''
    );

  if(
    !handedOffDestination||
    keyOf(handedOffDestination)!==keyOf(record)
  ){
    randomNavigationWindow.rollbackPending?.();
    throw new Error('RANDOM 0070 PREPARED HD HANDOFF IDENTITY MISMATCH');
  }

  if(
    handedOffDestination.avmAuthority!=='RUNTIME_IMAGE_AVM'||
    Number(handedOffDestination.ra)!==Number(handedOffDestination.avmRa)||
    Number(handedOffDestination.dec)!==Number(handedOffDestination.avmDec)||
    !Number.isFinite(Number(handedOffDestination.avmHorizontalFovDegrees))||
    Number(handedOffDestination.avmHorizontalFovDegrees)<=0||
    Number(handedOffDestination.fovDegrees)!==Number(handedOffDestination.avmVerticalFovDegrees)||
    Number(handedOffDestination.aladinRotation)!==Number(handedOffDestination.avmCameraRotation)
  ){
    randomNavigationWindow.rollbackPending?.();
    throw new Error('AR129-B RANDOM AVM CAMERA AUTHORITY REQUIRED');
  }

  destination=handedOffDestination;
  activeRecord=record;
  activeRecord.destination=destination;
  authoritativePendingDestination=destination;

  randomGalaxy.activeDestination=destination;

  /*
   * AR119 - VISIBLE AVM IS A PRE-TRAVEL REQUIREMENT.
   * The destination is already owned and its AVM/WCS was parsed during
   * preparation. Install that exact image registration in the visible
   * Aladin viewer BEFORE physical travel starts. The overlay module is not
   * allowed to move the camera; Navigation remains sole camera owner.
   */
  const avmApi=globalThis.GalaxyViewerAvmOverlayLab;
  if(
    !avmApi ||
    typeof avmApi.prepareForTravel!=='function'
  ){
    randomNavigationWindow.rollbackPending?.();
    throw new Error('AR119 VISIBLE AVM PRETRAVEL API MISSING');
  }

  const avmInstalled=await avmApi.prepareForTravel(destination);
  if(!avmInstalled){
    randomNavigationWindow.rollbackPending?.();
    throw new Error('AR119 VISIBLE AVM PRETRAVEL INSTALL FAILED');
  }

  GV_TRACE.enabled&&gvTrace(11901,'AR119_VISIBLE_AVM_READY_BEFORE_TRAVEL',{
    key:keyOf(destination),
    name:String(destination?.name||''),
    url:String(destination?.avmAuthorityUrl||'')
  });

  // travelToRandom consumes this exact destination directly.  When its HD
  // resource was READY, preparedHdUrl/preparedHdImage now travel with it.
  randomGalaxy.prefetchedDestination=destination;
  randomGalaxy.prefetchPromise=null;

  let downloadsSuspended=false;

  try{
    // Pause background I/O only AFTER the navigation destination is owned.
    // Suspension is for smoothness only and is never a navigation gate.
    preparationEngine.suspendBackgroundWork?.();
    archiveIntegration.suspendArchivePreloads?.();
    downloadsSuspended=true;

    GV_TRACE.enabled&&gvTrace(5983,'REQUEST_TRAVEL_AWAIT_BEGIN');
    const arrived=await randomGalaxy.travelToRandom();
    GV_TRACE.enabled&&gvTrace(5983,'REQUEST_TRAVEL_AWAIT_END',{arrived:Boolean(arrived)});

    if(!arrived)
      throw new Error('RANDOM 0065 TRAVEL DID NOT ARRIVE');

    // The exact FIFO bundle was claimed before visible travel began.
    // Arrival commits that already-owned pending destination.
    randomNavigationWindow.commitPending?.(arrived);

    /*
     * Advance Navigation 0006 only after physical travel succeeded and
     * Random Galaxy committed the exact arrived destination.
     */
    /*
     * RANDOM 0109 — arrival is the UI release boundary.
     * Monte Carlo/planner advancement is background work and must never keep
     * randomRequestPending true after visible travel has completed.
     */
    setTimeout(()=>{
      void advanceNavigationPlannerAfterArrival(arrived).catch(error=>{
        console.error(
          'RANDOM 0109 POST-ARRIVAL PLANNER FAILURE',
          error
        );

        /*
         * Preserve the successful visible arrival. Rebuild future planning
         * from the galaxy actually reached instead of corrupting FIFO state.
         */
        navigationPlanner=null;
        navigationPlannerPromise=null;

        void ensureNavigationPlanner(arrived).catch(recoveryError=>{
          console.error(
            'RANDOM 0109 PLANNER RECOVERY FAILURE',
            recoveryError
          );
        });
      }).finally(()=>{
        try{
          reconcileFutureQueue();
          updateRandomButtonReadyState();
          updateHistoryControls();
        }catch(error){
          console.error('RANDOM 0109 POST-ARRIVAL RECONCILE FAILURE',error);
        }
      });
    },0);

    setTimeout(reconcileFutureQueue,100);
    return arrived;

  }catch(error){
    GV_TRACE.enabled&&gvTraceError(6014,'REQUEST_EXCEPTION',error);
    randomNavigationWindow.rollbackPending?.();
    activeRecord=null;
    if(startupHdGateReleased)
      setRandomButtonText(core?.randomGalaxyButton,'RANDOM GALAXY');
    throw error;

  }finally{
    if(downloadsSuspended){
      preparationEngine.resumeBackgroundWork?.();
      archiveIntegration.resumeArchivePreloads?.();
    }

    authoritativePendingDestination=null;
    randomRequestPending=false;
    updateRandomButtonReadyState();
    updateHistoryControls();
  }
}

function updateHistoryControls(){
  if(!randomNavigationWindow)return;
  const state=randomGalaxy?.getState?.()||{};
  const busy=Boolean(
    randomRequestPending||
    state.busy||
    state.hdOpen||
    state.interactionOwner==='hd'||
    hdFeedbackBusy
  );
  if(core?.historyBackButton)
    core.historyBackButton.disabled=busy||!randomNavigationWindow.canBack();
  if(core?.historyForwardButton)
    core.historyForwardButton.disabled=busy||!randomNavigationWindow.canForward();
}

async function requestHistoryNavigation(direction){
  if(randomRequestPending||randomGalaxy?.getState?.().busy)return null;

  const requested=
    direction==='back'
      ? randomNavigationWindow.lockHistoryBack()
      : direction==='forward'
        ? randomNavigationWindow.lockHistoryForward()
        : null;

  if(!requested){
    updateHistoryControls();
    return null;
  }

  randomRequestPending=true;
  let travelWorkSuspended=false;
  updateHistoryControls();

  try{
    const destination=
      preparationEngine.activateQueuedDestination(
        requested,
        randomGalaxy?.currentGalaxy?.name||''
      );

    if(!destination||keyOf(destination)!==keyOf(requested))
      throw new Error("HISTORY DESTINATION HANDOFF MISMATCH");

    if(
      destination.avmAuthority!=='RUNTIME_IMAGE_AVM'||
      Number(destination.ra)!==Number(destination.avmRa)||
      Number(destination.dec)!==Number(destination.avmDec)||
      !Number.isFinite(Number(destination.avmHorizontalFovDegrees))||
      Number(destination.avmHorizontalFovDegrees)<=0||
      Number(destination.fovDegrees)!==Number(destination.avmVerticalFovDegrees)||
      Number(destination.aladinRotation)!==Number(destination.avmCameraRotation)
    )throw new Error("AR129-B HISTORY AVM CAMERA AUTHORITY REQUIRED");

    authoritativePendingDestination=destination;
    randomGalaxy.prefetchedDestination=destination;
    randomGalaxy.prefetchPromise=null;

    preparationEngine.suspendBackgroundWork?.();
    archiveIntegration.suspendArchivePreloads?.();
    travelWorkSuspended=true;

    const arrived=await randomGalaxy.travelToRandom();
    const pending=randomNavigationWindow.getState().pending;
    if(!arrived||pending?.kind!==direction)
      throw new Error("HISTORY NAVIGATION COMMIT INVARIANT FAILED");

    randomNavigationWindow.commitPending(arrived);
    updateHistoryControls();
    return arrived;
  }catch(error){
    if(randomNavigationWindow.getState().pending)
      randomNavigationWindow.rollbackPending();
    updateHistoryControls();
    throw error;
  }finally{
    if(travelWorkSuspended){
      preparationEngine.resumeBackgroundWork?.();
      archiveIntegration.resumeArchivePreloads?.();
    }
    authoritativePendingDestination=null;
    randomRequestPending=false;
    updateHistoryControls();
    updateRandomButtonReadyState();
  }
}

function telemetryIdentity(value){
  const bundle=value?.bundle||value||null;
  const destination=bundle?.destination||value?.destination||bundle||null;
  const key=String(bundle?.key||keyOf(destination)||'').trim().toLowerCase();
  if(!key)return null;
  return Object.freeze({
    key,
    name:String(destination?.name||destination?.displayName||''),
    provider:String(destination?.provider||'')
  });
}
function telemetry(){
  const nav=randomNavigationWindow.getState?.()||{};
  const future=orderedFutureRecords().slice(0,FUTURE_TARGET);
  const runtimeState=randomGalaxy?.getState?.()||{};
  const hdPresentation=runtimeState.hdPresentation||null;

  return Object.freeze({
    version:VERSION,
    suspended:Boolean(preparationEngine?.getBackgroundWorkSuspended?.()),
    backgroundSuspended:Boolean(preparationEngine?.getBackgroundWorkSuspended?.()),
    hdPresentation:hdPresentation
      ? Object.freeze({...hdPresentation})
      : null,
    active:activeRecord?Object.freeze({sequence:activeRecord.sequence,key:activeRecord.key,name:String(activeRecord.destination?.name||''),provider:String(activeRecord.destination?.provider||'')}):null,
    navigation:Object.freeze({
      current:telemetryIdentity(nav.current),
      locked:telemetryIdentity(nav.locked),
      pending:telemetryIdentity(nav.pending),
      future0:telemetryIdentity(future[0])
    }),
    rows:Object.freeze(future.map((record,index)=>Object.freeze({
      slot:index+1,
      sequence:record.sequence,
      key:record.key,
      name:String(record.destination?.name||''),
      provider:String(record.destination?.provider||''),
      destination:Object.freeze({
        ra:Number(record.destination?.ra),
        dec:Number(record.destination?.dec),
        fov:Number(record.destination?.fovDegrees),
        rotation:Number.isFinite(Number(record.destination?.aladinRotation))?Number(record.destination.aladinRotation):0,
        orientationSource:String(
          record.destination?.framingRegistrationSource ||
          (
            record.destination?.aladinRotation===null ||
            record.destination?.aladinRotation===undefined ||
            record.destination?.aladinRotation==='' ||
            !Number.isFinite(Number(record.destination?.aladinRotation))
              ? 'NORTH'
              : 'CATALOG'
          )
        ),
        sourceUrl:String(record.destination?.sourceUrl||''),
        selectedImageUrl:String(record.destination?.selectedImageUrl||''),
        githubImageUrl:String(record.destination?.githubImageUrl||'')
      }),
      hd:Object.freeze(hdStateFor(record)),
      aladin:Object.freeze({state:'UNAVAILABLE',detail:'PREFETCH DISABLED'}),
      web:Object.freeze({state:'UNAVAILABLE',detail:'PRELOAD DISABLED'})
    })))
  });
}
function installHdFeedback(){
  if(!randomGalaxy?.providerIconButton)return;
  const style=document.createElement('style');
  style.id='gv-prefetch-hd-feedback-style';
  style.textContent='.gvrg-hd-icon-button{position:relative!important}.gvrg-hd-primary.gv-hd-press-flash{opacity:1!important;background:linear-gradient(145deg,#0f5b2b,#21a65a)!important;border-color:#78FFAB!important;box-shadow:0 0 10px rgba(120,255,171,.72)!important}.gvrg-hd-icon-button.gv-prefetch-hd-wait{opacity:1!important}.gv-prefetch-hd-feedback{position:absolute;inset:5px;border-radius:50%;opacity:0;pointer-events:none;transform-origin:50% 50%}.gv-prefetch-hd-feedback::before{content:"";position:absolute;left:50%;top:-1px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#F8FFFF;box-shadow:0 0 4px #fff,0 0 8px #8FE5FF,0 0 11px #296DBD}.gv-prefetch-hd-feedback::after{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 250deg,transparent 0deg,rgba(91,184,255,.25) 42deg,rgba(143,229,255,.58) 82deg,rgba(248,255,255,.92) 110deg,transparent 111deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px))}.gvrg-hd-icon-button.gv-prefetch-hd-wait .gv-prefetch-hd-feedback{opacity:1;animation:gvPrefetchHdOrbit 1s linear infinite}@keyframes gvPrefetchHdOrbit{to{transform:rotate(360deg)}}';
  document.head.appendChild(style);
  const feedback=document.createElement('span');
  feedback.className='gv-prefetch-hd-feedback';feedback.setAttribute('aria-hidden','true');
  randomGalaxy.providerIconButton.appendChild(feedback);
  const waitForHd=async(key,timeout=2500)=>{const started=performance.now();for(;;){const state=hdStateFor({key});if(state.state==='READY')return true;if(performance.now()-started>=timeout)return false;await sleep(80)}};
  const handle=async event=>{
    const destination=randomGalaxy.getState?.().activeDestination;
    if(!destination||hdFeedbackBusy)return;
    event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();

    // Claim the HD/Random interlock synchronously on the original click.
    if(!randomGalaxy.beginHdRequest?.())return;

    const hdSerial=++hdFeedbackSerial;
    hdFeedbackBusy=true;
    randomGalaxy.viewHdButton?.classList.add('gv-hd-press-flash');
    const flashTimer=setTimeout(()=>randomGalaxy.viewHdButton?.classList.remove('gv-hd-press-flash'),220);
    const cometTimer=setTimeout(()=>randomGalaxy.providerIconButton?.classList.add('gv-prefetch-hd-wait'),180);
    const key=keyOf(destination);
    preparationEngine.requestHdPrefetch?.(destination);

    try{
      await waitForHd(key,2500);
      if(hdSerial!==hdFeedbackSerial)return;
      randomGalaxy.showHD();
    }catch(error){
      console.error('GALAXY VIEWER PREFETCH HD ENTRY FAILURE',error);
      if(hdSerial===hdFeedbackSerial){
        try{randomGalaxy.showHD()}catch(_){}
      }
    }finally{
      clearTimeout(flashTimer);
      clearTimeout(cometTimer);
      randomGalaxy.viewHdButton?.classList.remove('gv-hd-press-flash');
      randomGalaxy.providerIconButton?.classList.remove('gv-prefetch-hd-wait');
      if(hdSerial===hdFeedbackSerial){
        if(!randomGalaxy.hdOpen)randomGalaxy.cancelHdRequest?.('hd-entry-failed');
        hdFeedbackBusy=false;
      }
    }
  };
  randomGalaxy.viewHdButton?.addEventListener('click',handle,true);
  randomGalaxy.providerIconButton?.addEventListener('click',handle,true);
}
function install(){
  if(installed)return true;
  core=window.GalaxyViewerCore||window.GalaxyViewerRandomBootstrap;
  if(!core?.randomGalaxy)return false;

  randomGalaxy=core.randomGalaxy;
  randomNavigationWindow=randomGalaxy.randomNavigationWindow;

  if(!randomNavigationWindow)
    throw new Error('RANDOM GALAXY 0062 NAVIGATION WINDOW MISSING');

  preparationEngine=randomGalaxy.preparationEngine;
  archiveIntegration=randomGalaxy.hdArchiveIntegration;

  if(!preparationEngine)
    throw new Error('RANDOM GALAXY 0062 PREPARATION ENGINE MISSING');

  if(!archiveIntegration)
    throw new Error('RANDOM GALAXY 0062 HD/ARCHIVE INTEGRATION MISSING');
  const legacyPrefetchPromise=randomGalaxy.prefetchPromise;
  randomGalaxy.options.prefetch=false;
  randomGalaxy.prefetchedDestination=null;
  randomGalaxy.prefetchPromise=null;
  if(legacyPrefetchPromise){
    legacyPrefetchDrain=Promise.resolve(legacyPrefetchPromise).catch(()=>null).then(()=>{
      randomGalaxy.prefetchedDestination=
        randomRequestPending&&authoritativePendingDestination
          ? authoritativePendingDestination
          : null;
      randomGalaxy.prefetchPromise=null;
    });
  }
  catalog=preparationEngine.getGalaxyCatalog();
  catalogByKey=new Map(catalog.map(destination=>[keyOf(destination),destination]));
  catalogByName=new Map(catalog.map(destination=>[String(destination?.name||'').trim().toLowerCase(),destination]));
  setRandomButtonText(
    core?.randomGalaxyButton,
    'PREPARING TRIP',
    {busy:true}
  );
  if(core?.randomGalaxyButton)core.randomGalaxyButton.disabled=true;

  /*
   * AR123: do not create or prepare any future destination until the
   * Navigation 0018 Monte Carlo planner has completed.
   */
  startupRoutePromise=(async()=>{
    await ensureNavigationPlanner(null);
    reconcileFutureQueue();

    return true;
  })();

  randomGalaxy.provider=async args=>{
    const destination=await consumeNext(args?.excludeName||'');
    if(!destination)throw new Error('AUTHORITATIVE NEXT GALAXY IS NOT READY');


    // Navigation owns download suspension. The provider only supplies
    // the destination and may never pause or resume navigation resources.
    return destination;
  };
  core.historyBackButton?.addEventListener('click',event=>{
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    requestHistoryNavigation('back').catch(error=>console.error('GALAXY VIEWER BACK HISTORY FAILURE',error));
  },true);
  core.historyForwardButton?.addEventListener('click',event=>{
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    requestHistoryNavigation('forward').catch(error=>console.error('GALAXY VIEWER FORWARD HISTORY FAILURE',error));
  },true);
  core.randomGalaxyButton?.addEventListener('click',event=>{
    GV_TRACE.enabled&&gvTrace(6309,'PHYSICAL_RANDOM_CLICK',{
      trusted:Boolean(event?.isTrusted),
      disabled:Boolean(core.randomGalaxyButton?.disabled)
    });
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    requestRandomNavigation().catch(error=>{
      GV_TRACE.enabled&&gvTraceError(6313,'PHYSICAL_RANDOM_REJECTION',error);
      console.error('GALAXY VIEWER RANDOM NAVIGATION REQUEST FAILURE',error);
    });
  },true);
  const monitor=setInterval(()=>{
    const nextSuspended=Boolean(preparationEngine.getBackgroundWorkSuspended?.());
    suspended=nextSuspended;
    if(!nextSuspended)reconcileFutureQueue();
    if(!nextSuspended)updateRandomButtonReadyState();
    else if(!startupHdGateReleased)updateStartupRandomButton();
    updateHistoryControls();
  },POLL_MS);
  window.addEventListener('beforeunload',()=>{clearInterval(monitor)},{once:true});
  installHdFeedback();
  GalaxyRandomGalaxy.requestRandomNavigation=requestRandomNavigation;
  GalaxyRandomGalaxy.requestHistoryNavigation=requestHistoryNavigation;
  GalaxyRandomGalaxy.updateHistoryControls=updateHistoryControls;
  GalaxyRandomGalaxy.isNavigationPending=()=>Boolean(
    randomRequestPending||
    randomGalaxy?.getState?.().busy||
    randomNavigationWindow?.getState?.().pending
  );
  GalaxyRandomGalaxy.getPrefetchTelemetry=telemetry;GalaxyRandomGalaxy.reconcileFutureQueue=reconcileFutureQueue;GalaxyRandomGalaxy.hasReadyNavigation=hasReadyNavigation;GalaxyRandomGalaxy.prefetchRuntime=Object.freeze({version:VERSION,displayVersion:VERSION,core,randomGalaxy});
  GalaxyRandomGalaxy.waitForStartupRoute=()=>startupRoutePromise;
  installed=true;
  document.dispatchEvent(new CustomEvent('gv-prefetch-ready',{detail:{version:VERSION,rows:randomNavigationWindow.getState().futureCount}}));
  return true;
}
GalaxyRandomGalaxy.installPrefetchRuntime=install;
if(!install()){
  const onReady=()=>setTimeout(install,0);
  document.addEventListener('gv-viewer-ready',onReady,{once:true});
  const timer=setInterval(()=>{if(install())clearInterval(timer)},100);
  setTimeout(()=>clearInterval(timer),30000);
}
})();

  GalaxyRandomGalaxy.setExecutionTracingEnabled=setExecutionTracingEnabled;
  GalaxyRandomGalaxy.getExecutionTracingEnabled=()=>Boolean(GV_TRACE.enabled);

  global.GalaxyRandomNavigationWindow = GalaxyRandomNavigationWindow;
  global.GalaxyRandomGalaxy = GalaxyRandomGalaxy;
})(window);
