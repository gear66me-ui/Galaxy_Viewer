/*
GALAXY VIEWER ENGINEERING CHANGE ORDER — RANDOM GALAXY 0013
AUTHORIZED BASELINE: gv-random-galaxy-0010.js blob a4a9ddb3c28751dfbbf9fcdf04278c80e1020013.
AUTHORIZED CHANGES: readable compact arrival presentation, five-field HD science banner, exact retained decoded-image handoff for immediate HD display, and generic provider identity. Touch-through interaction, 36px provider controls, top-centered HD viewing, no post-arrival reframing, and configured travel behavior are preserved.
*/
(function (global) {
  'use strict';

  const VERSION = '0038';

  const FONT_URLS = Object.freeze({
    spaceAge: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001',
    digits: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/GV-Coordinate-Digits-0005.otf?v=7R-slashed-zero-coordinate-digits-0005'
  });

  const FONT_NAMES = Object.freeze({
    spaceAge: 'GV Random Galaxy Space Age 0013',
    digits: 'GV Random Galaxy Digits 0013'
  });

  const DEFAULT_PROVIDER_ICON_URL = 'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg';

  const DEFAULTS = Object.freeze({
    geminiEndpoint: null,
    travelSeconds: 18,
    firstHomeTravelSeconds: 7.5,
    maxFov: 330,
    translateStart: 0.34,
    turnPoint: 0.46,
    translate90: 0.58,
    translationComplete: 0.68,
    aitEntryFov: 95,
    sinReturnFov: 24,
    arrivalProjection: 'SIN',
    wideProjection: 'AIT',
    integerSlots: 6,
    fractionSlots: 2,
    prefetch: true,
    requestEvent: 'gv-random-galaxy-request',
    bindClick: false,
    catalogTarget: 1879,
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
  function cleanText(value) { return String(value == null ? '' : value).replace(/\s+/g, ' ').trim(); }
  function finiteNumber(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }
  function validHttpsUrl(value) {
    try {
      const url = new URL(String(value));
      return url.protocol === 'https:' ? url : null;
    } catch (_) { return null; }
  }
  function isSupportedProviderHost(hostname) {
    const host = String(hostname || '').toLowerCase();
    return host === 'esahubble.org' || host.endsWith('.esahubble.org')
      || host === 'esawebb.org' || host.endsWith('.esawebb.org')
      || host === 'chandra.harvard.edu' || host.endsWith('.chandra.harvard.edu');
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
  function greatCirclePosition(ra1, dec1, ra2, dec2, progress) {
    const a = toVector(ra1, dec1);
    const b = toVector(ra2, dec2);
    let dot = a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
    dot = clamp(dot, -1, 1);
    const omega = Math.acos(dot);
    const sinOmega = Math.sin(omega);
    if (Math.abs(sinOmega) < 1e-7) {
      return [
        Number(ra1) + (Number(ra2) - Number(ra1)) * progress,
        Number(dec1) + (Number(dec2) - Number(dec1)) * progress
      ];
    }
    const s1 = Math.sin((1 - progress) * omega) / sinOmega;
    const s2 = Math.sin(progress * omega) / sinOmega;
    return vectorToRaDec([
      a[0] * s1 + b[0] * s2,
      a[1] * s1 + b[1] * s2,
      a[2] * s1 + b[2] * s2
    ]);
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
    style.textContent=`#gv-random-galaxy .gvrg-random-layout{display:grid;grid-template-columns:20px auto 20px;align-items:center;justify-content:center;column-gap:13px}#gv-random-galaxy .gvrg-random-label{display:block;grid-column:2;text-align:center}#gv-random-galaxy .gvrg-random-star-wrap{position:relative;display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;margin:0;flex:0 0 20px;line-height:20px;transform:none}#gv-random-galaxy .gvrg-random-star-wrap-left{grid-column:1}#gv-random-galaxy .gvrg-random-star-wrap-right{grid-column:3;transform:translateX(-2px)}#gv-random-galaxy .gvrg-random-star{display:block;font:16px/20px system-ui,sans-serif;transform:translateY(-.5px)}#gv-random-galaxy .gvrg-random-comet{position:absolute;left:50%;top:50%;width:0;height:0;opacity:0;pointer-events:none;z-index:2;animation:gvrg-random-comet-orbit-0031 2.8s linear infinite;animation-play-state:paused}#gv-random-galaxy .gvrg-random-comet i{position:absolute;left:-1.5px;top:-1.5px;width:3px;height:3px;border-radius:50%;background:#62D8FF;transform:rotate(var(--a)) translateY(-8px) scale(var(--s));opacity:var(--o);box-shadow:0 0 3px rgba(98,216,255,.85)}#gv-random-galaxy .gvrg-random-comet i:nth-child(1){--a:0deg;--s:1;--o:1;background:#fff;box-shadow:0 0 2px 1px #fff,0 0 5px 1px #62D8FF}#gv-random-galaxy .gvrg-random-comet i:nth-child(2){--a:-15deg;--s:.88;--o:.84}#gv-random-galaxy .gvrg-random-comet i:nth-child(3){--a:-30deg;--s:.76;--o:.68}#gv-random-galaxy .gvrg-random-comet i:nth-child(4){--a:-45deg;--s:.64;--o:.52}#gv-random-galaxy .gvrg-random-comet i:nth-child(5){--a:-60deg;--s:.52;--o:.38}#gv-random-galaxy .gvrg-random-comet i:nth-child(6){--a:-75deg;--s:.42;--o:.26}#gv-random-galaxy .gvrg-random-comet i:nth-child(7){--a:-90deg;--s:.32;--o:.16}#gv-random-galaxy .gvrg-random-comet i:nth-child(8){--a:-105deg;--s:.24;--o:.08}#gv-random-galaxy.gvrg-random-busy .gvrg-random-comet{opacity:1;animation-play-state:running}#gv-random-galaxy .gvrg-random-comet-left{animation-delay:-1.4s}.gvrg-fov-sub{font-size:.72em;letter-spacing:.25px;white-space:nowrap}@keyframes gvrg-random-comet-orbit-0031{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}`;
    document.head.appendChild(style);
  }
  const layoutReady=button.querySelector('.gvrg-random-layout .gvrg-random-star-wrap-left')&&button.querySelector('.gvrg-random-layout .gvrg-random-label')&&button.querySelector('.gvrg-random-layout .gvrg-random-star-wrap-right');
  if (!layoutReady) {
    button.innerHTML='<span class="gvrg-random-layout"><span class="gvrg-random-star-wrap gvrg-random-star-wrap-left" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet gvrg-random-comet-left"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span><span class="gvrg-random-label">RANDOM GALAXY</span><span class="gvrg-random-star-wrap gvrg-random-star-wrap-right" aria-hidden="true"><span class="gvrg-random-star">✨</span><span class="gvrg-random-comet"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span></span></span>';
    button.setAttribute('aria-label','RANDOM GALAXY');
  }
}
function setRandomWaitComet(button,active){if(!(button instanceof Element))return;installRandomWaitComet(button);button.classList.toggle('gvrg-random-busy',Boolean(active));}

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

      const bundle = this.future.shift();
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
          this.future.unshift(item);
        if (this.future.length > this.futureTarget)
          this.future.length = this.futureTarget;
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
#gv-we-are-here .gv-earth-icon{display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:grayscale(1) sepia(1) saturate(8) hue-rotate(82deg) brightness(1.22) drop-shadow(0 0 4px rgba(87,255,147,.92)) drop-shadow(0 0 9px rgba(77,255,143,.48))}
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
        const centerX=rootRect.width/2;
        const centerY=rootRect.height/2;
    
        let dx=1,dy=0;
        try{
            if(typeof aladin.world2pix==='function'){
                const earthPixel=aladin.world2pix(home.ra,home.dec);
                const ex=Number(earthPixel?.[0]),ey=Number(earthPixel?.[1]);
                if(Number.isFinite(ex)&&Number.isFinite(ey)){
                    dx=ex-centerX;
                    dy=ey-centerY;
                }
            }
        }catch(_){}
    
        const magnitude=Math.hypot(dx,dy)||1;
        dx/=magnitude;
        dy/=magnitude;
    
        const relativeBottom=element=>{
            if(!element)return 0;
            const rect=element.getBoundingClientRect();
            if(rect.width<=0||rect.height<=0)return 0;
            return rect.bottom-rootRect.top;
        };
    
        const hamburgerControl=hamburgerHost.querySelector('button,[role="button"]')||hamburgerHost;
        const coordinateControl=coordinateHost;
        const targetControl=targetHost.querySelector('button,[role="button"]')||targetHost;
    
        const bannerWidth=Math.min(680,Math.max(40,rootRect.width-20));
        const apertureLeft=(rootRect.width-bannerWidth)/2;
        const apertureRight=apertureLeft+bannerWidth;
    
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
        const indicatorRect=earthReturnIndicator.root.getBoundingClientRect();
        const indicatorHalfW=Math.max(29,Number(indicatorRect.width||0)/2);
        const indicatorHalfH=Math.max(24,Number(indicatorRect.height||0)/2);
    
        const cardOrNavTop=
            cardRect&&cardRect.width>0&&cardRect.height>0
                ? cardRect.top-rootRect.top
                : navRect.top-rootRect.top;
    
        const lowerObstacleTop=
            scaleVisible
                ? Math.min(cardOrNavTop,scaleRect.top-rootRect.top)
                : cardOrNavTop;
    
        // Center-safe aperture: the full Earth-return indicator must remain
        // inside the Aladin sky area and above the physical scale ruler
        // (or the Random Galaxy card when the ruler is not visible).
        const safeLeft=apertureLeft+indicatorHalfW+4;
        const safeRight=apertureRight-indicatorHalfW-4;
        const apertureTop=Math.max(
            indicatorHalfH+4,
            topControlsBottom+6+indicatorHalfH
        );
        const apertureBottom=Math.max(
            apertureTop+1,
            Math.min(
                rootRect.height-indicatorHalfH-4,
                lowerObstacleTop-8-indicatorHalfH
            )
        );
    
        const apertureCenterX=(safeLeft+safeRight)/2;
        const apertureCenterY=(apertureTop+apertureBottom)/2;
        const halfW=Math.max(1,(safeRight-safeLeft)/2);
        const halfH=Math.max(1,(apertureBottom-apertureTop)/2);
    
        const edgeScale=Math.min(
            Math.abs(dx)>0.001 ? halfW/Math.abs(dx) : Infinity,
            Math.abs(dy)>0.001 ? halfH/Math.abs(dy) : Infinity
        );
    
        const edgeInset=4;
        const x=apertureCenterX+dx*Math.max(0,edgeScale-edgeInset);
        const y=apertureCenterY+dy*Math.max(0,edgeScale-edgeInset);
    
        earthReturnIndicator.root.style.left=`${x}px`;
        earthReturnIndicator.root.style.top=`${y}px`;
    
        const angle=Math.atan2(dy,dx)*180/Math.PI;
        earthReturnIndicator.arrow.style.transform=
            `translate(-50%,-50%) rotate(${angle}deg)`;
    
        const readoutRadius=27;
        const rx=-dx*readoutRadius;
        const ry=-dy*readoutRadius;
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
    if(hdBackToSky)hdBackToSky.addEventListener('click',()=>{onHideEarthReturn();requestAnimationFrame(()=>restoreAfterHdClose())},true);
    if(hdDownloadButton){
        hdDownloadButton.id='gv-hd-download-button';
        hdDownloadButton.setAttribute('aria-label','DOWNLOAD HD IMAGE');
        hdDownloadButton.setAttribute('title','DOWNLOAD HD IMAGE');
        hdControlRow.appendChild(hdDownloadButton);
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
        archiveRevealTimer=0;
        setArchiveLoading(false);
        archiveOverlay.removeAttribute('aria-hidden');
        archiveOverlay.style.removeProperty('visibility');
        archiveOverlay.style.removeProperty('opacity');
        archiveOverlay.style.pointerEvents='auto';
        archiveOverlay.classList.add('gv-open');
        archiveFrame.style.pointerEvents='auto';
    };
    const archiveQueueKey=destination=>destinationKey(destination);
    const chooseArchivePreloadDestination=()=>{
        const excluded=new Set([getActiveTargetKey(),...archivePreloadQueue.map(item=>item.key),activeArchivePreloadItem?.key,...archivePreloadFailedKeys].filter(Boolean));
        const prepared=getPrefetchReady().find(item=>{
            const destination=item?.destination;
            const key=item?.key||archiveQueueKey(destination);
            const sourceUrl=String(destination?.sourceUrl||'').trim();
            return key&&!excluded.has(key)&&/^https:\/\//i.test(sourceUrl);
        });
        return prepared?.destination||null;
    };
    const startNextArchivePreload=()=>{
        if(archivePreloadSuspended||isBackgroundWorkSuspended()||isNavigationPending()||archivePreloadLoadingItem)return;
        if(archivePreloadQueue.filter(item=>item.state==='ready').length>=ARCHIVE_PRELOAD_TARGET)return;
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
                item.state='ready';
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
        const index=archivePreloadQueue.findIndex(item=>item.state==='ready'&&String(item.destination?.name||'').trim().toLowerCase()!==excluded);
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
        if(!/^https:\/\//i.test(sourceUrl)||archiveSourceUrl===sourceUrl)return;
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
        requestAnimationFrame(()=>{if(isHdPresentationActive())try{hdArchiveButton.focus({preventScroll:true})}catch(_){}});
    };
    archiveBack.addEventListener('pointerdown',consumeArchiveBackEvent,true);
    archiveBack.addEventListener('pointerup',consumeArchiveBackEvent,true);
    archiveBack.addEventListener('click',event=>{
        consumeArchiveBackEvent(event);
        closeArchiveOverlay();
    },true);
    archiveFrame.addEventListener('load',()=>{
        if(!archiveSourceUrl||archiveClosing)return;
        const loadedUrl=String(archiveFrame.src||'').trim();
        if(loadedUrl!==archiveSourceUrl)return;
        archiveLoadedUrl=loadedUrl;
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
    function providerFor(destination){const provider=String(destination?.provider||'').trim().toUpperCase();return provider==='HUBBLE'||provider==='JWST'||provider==='CHANDRA'||provider==='SPITZER'?provider:''}
    hdArchiveButton.addEventListener('click',event=>{
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
        const destination=currentArchiveDestination();
        const sourceUrl=String(destination?.sourceUrl||'').trim();
        if(!/^https:\/\//i.test(sourceUrl))return;
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
        const telescope=provider==='CHANDRA'?'CHANDRA X-RAY OBSERVATORY':provider==='JWST'?'JAMES WEBB SPACE TELESCOPE':provider==='SPITZER'?'SPITZER SPACE TELESCOPE':'HUBBLE SPACE TELESCOPE';
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
        const iconUrl=provider==='CHANDRA'?CHANDRA_ICON_URL:provider==='JWST'?JWST_ICON_URL:provider==='SPITZER'?SPITZER_ICON_URL:HUBBLE_ICON_URL;
        if(randomGalaxy.viewHdButton){randomGalaxy.viewHdButton.textContent=`VIEW ${provider} IN HD`;randomGalaxy.viewHdButton.setAttribute('aria-label',`VIEW ${provider} IN HD`)}
        const buttonIcon=randomGalaxy.providerIconButton?.querySelector('img');
        if(buttonIcon){buttonIcon.src=iconUrl;buttonIcon.alt=`${provider} ARCHIVE`}
        hdArchiveIcon.src=iconUrl;
        hdArchiveIcon.alt=`${provider} ARCHIVE`;
        hdArchiveButton.setAttribute('aria-label',`OPEN ${provider} ARCHIVE SOURCE`);
        if(randomGalaxy.hdLoading&&provider!=='HUBBLE'&&/HUBBLE/i.test(randomGalaxy.hdLoading.textContent||''))randomGalaxy.hdLoading.textContent=String(randomGalaxy.hdLoading.textContent||'').replace(/HUBBLE/gi,provider);
        fitHdInfoText(destination);
    }
    
    resumeArchivePreloads();
    
    function applySmartHdCrop(){
        const image=randomGalaxy.hdImage;
        if(!(image instanceof HTMLImageElement)||!image.complete||!image.naturalWidth)return;
        image.style.objectFit='contain';
        image.style.objectPosition='50% 50%';
    }
    
    function isHdPresentationActive(){return Boolean(randomGalaxy.getState?.().hdOpen)}
    
    function resetHdPresentationGeometry(){
        const clear=(element,...names)=>{
            if(!element)return;
            for(const name of names)element.style.removeProperty(name);
        };
        clear(randomGalaxy.hdScience,'top','height','max-height');
        clear(randomGalaxy.hdViewport,'top','bottom','height','max-height','pointer-events');
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
        if(!isNavigationPending()&&!randomGalaxy.getState().busy)
            bottom.random.disabled=GalaxyRandomGalaxy.hasReadyNavigation?!GalaxyRandomGalaxy.hasReadyNavigation():true;
        onSetHistoryControls();
    }
    
    function positionHdInfoPanel(){
        if(!isHdPresentationActive())return;
        if(!randomGalaxy.hdOverlay||!randomGalaxy.hdViewport||!randomGalaxy.hdScience)return;
        const overlayRect=randomGalaxy.hdOverlay.getBoundingClientRect();
        const navRect=bottom.nav.getBoundingClientRect();
        if(!overlayRect.height||!overlayRect.width)return;
        const safeBottom=Math.min(overlayRect.bottom-HD_LAYOUT.edge,navRect.top-24);
        const available=Math.max(1,safeBottom-overlayRect.top-HD_LAYOUT.edge-HD_LAYOUT.gap*2);
        const bannerTarget=overlayRect.height*HD_LAYOUT.bannerRatio;
        const viewportWidth=Math.min(680,Math.max(1,randomGalaxy.hdViewport.getBoundingClientRect().width||overlayRect.width-20));
        const layoutScale=Math.min(1,available/Math.max(1,bannerTarget+viewportWidth+165));
        const bannerHeight=Math.max(1,Math.floor(bannerTarget*layoutScale));
        const imageHeight=Math.max(1,Math.floor(viewportWidth*layoutScale));
        const scienceTop=HD_LAYOUT.edge;
        const imageTop=scienceTop+bannerHeight+HD_LAYOUT.gap;
        const infoTop=imageTop+imageHeight+HD_LAYOUT.gap;
        const infoHeight=Math.max(165,Math.floor(safeBottom-(overlayRect.top+infoTop)));
        const set=(element,name,value)=>element.style.setProperty(name,value,'important');
        set(randomGalaxy.hdScience,'top',`${scienceTop}px`);set(randomGalaxy.hdScience,'height',`${bannerHeight}px`);set(randomGalaxy.hdScience,'max-height',`${bannerHeight}px`);
        set(randomGalaxy.hdViewport,'top',`${imageTop}px`);set(randomGalaxy.hdViewport,'bottom','auto');set(randomGalaxy.hdViewport,'height',`${imageHeight}px`);set(randomGalaxy.hdViewport,'max-height',`${imageHeight}px`);
        set(hdInfoPanel,'top',`${infoTop}px`);set(hdInfoPanel,'height',`${infoHeight}px`);set(hdInfoPanel,'max-height',`${infoHeight}px`);
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
        const rootRect=root.getBoundingClientRect();
        const versionTop=Math.ceil(overlayRect.top+infoTop+infoHeight+5-rootRect.top);
        bottom.version.style.bottom='auto';
        bottom.version.style.top=`${versionTop}px`;
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
        const result=originalShowHD();
        const destination=currentArchiveDestination();
        if(destination)preloadArchiveSource(destination);
        requestAnimationFrame(()=>requestAnimationFrame(settleHdPresentation));
        return result;
    };
    randomGalaxy.viewHdButton?.addEventListener('click',()=>requestAnimationFrame(settleHdPresentation),true);
    randomGalaxy.providerIconButton?.addEventListener('click',()=>requestAnimationFrame(settleHdPresentation),true);
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
  // Copied preparation engine; inactive until cutover.
  function createRandomPreparationEngine(options = {}) {
    const ALADIN_URL=options.aladinUrl||'';
    const HOME=options.home||{};
    const galaxyCatalog=options.galaxyCatalog||[];
    const chandraTestQueue=options.chandraTestQueue||[];
    let chandraTestOverrideActive=Boolean(options.chandraTestOverrideActive);
    let forcedDestination=null;
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
    const hdDownloadStatus=new Map();
    let prefetchFailedCount=0;
    let prefetchRetryTimer=0;
    let prefetchHealthTimer=0;
    let lastPrefetchHealth=Object.freeze({ready:0,loading:0,queued:0,total:0,activeKeys:Object.freeze([]),retryWait:Object.freeze([]),workers:Object.freeze([]),checkedAt:0});
    let priorityPrefetchDestination=null;
    let aladinPrefetchSerial=Promise.resolve();
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
    const aladinPrewarmedKeys=new Set();
    const aladinPreparedReceipts=new Map();
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
            const pool=available.length?available:catalog;
            return pool[Math.floor(Math.random()*pool.length)];
        }
    
        function releasePreparedItem(item){
            if(!item)return;
            try{if(item.image)item.image.src=''}catch(_){}
            try{if(item.objectUrl)URL.revokeObjectURL(item.objectUrl)}catch(_){}
        }
    
        function enforceHotPreparedWindow(){
            const hotOrder=[
                ...(randomNavigationWindow?.hotKeys?.() ||
                   randomNavigationWindow?.getState?.().hotKeys ||
                   [])
            ].slice(0,HEAVY_PREPARED_TARGET);
            const hotKeys=new Set(hotOrder);
            const retainedKeys=new Set();
    
            if(activePreparedItem?.key){
                if(hotKeys.has(activePreparedItem.key)){
                    retainedKeys.add(activePreparedItem.key);
                }else{
                    releasePreparedItem(activePreparedItem);
                    activePreparedItem=null;
                }
            }
    
            for(let i=historyPreparedItems.length-1;i>=0;i--){
                const item=historyPreparedItems[i];
                const keep=Boolean(
                    item?.key&&
                    hotKeys.has(item.key)&&
                    !retainedKeys.has(item.key)&&
                    retainedKeys.size<HEAVY_PREPARED_TARGET
                );
                if(keep){
                    retainedKeys.add(item.key);
                    continue;
                }
                historyPreparedItems.splice(i,1);
                releasePreparedItem(item);
            }
    
            for(let i=prefetchReady.length-1;i>=0;i--){
                const item=prefetchReady[i];
                const keep=Boolean(
                    item?.key&&
                    hotKeys.has(item.key)&&
                    !retainedKeys.has(item.key)&&
                    retainedKeys.size<HEAVY_PREPARED_TARGET
                );
                if(keep){
                    retainedKeys.add(item.key);
                    continue;
                }
                prefetchReady.splice(i,1);
                releasePreparedItem(item);
                if(item?.destination)setHdStatus(item.destination,'QUEUED');
            }
    
            for(const key of hotOrder){
                if(retainedKeys.has(key)||
                   prefetchLoading.has(key)||
                   prefetchQueued.some(destination=>destinationKey(destination)===key))
                    continue;
                const destination=galaxyCatalog.find(item=>destinationKey(item)===key);
                if(destination){
                    enqueuePrefetch(destination,key===activeTargetKey);
                    retainedKeys.add(key);
                }
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
                const value=String(url||'').trim();
                if(!/^https:\/\//i.test(value)||seen.has(value))return;
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
    
        async function prepareHdDestination(destination,signal=null){
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
                }
            }
            setHdStatus(destination,'RETRY-WAIT');
            throw lastError||new Error('HD PRELOAD HAS NO USABLE SOURCE');
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
                            projection:'SIN',
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
                        if(typeof aladinPrewarm.setProjection==='function')aladinPrewarm.setProjection('SIN');
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
    
        async function prepareAladinDestination(destination,force=false){
            if(backgroundWorkSuspended)throw abortError();
            const key=destinationKey(destination);
            if(!key)return false;
            if(aladinPrewarmedKeys.has(key)&&!force)return true;
            aladinPrewarmActiveKey=key;
            const isolated=await ensureAladinPrewarm();
            if(backgroundWorkSuspended||!isolated){aladinPrewarmActiveKey='';throw abortError()}
            try{
                if(typeof isolated.setFrame==='function')isolated.setFrame('ICRSd');
                if(typeof isolated.setProjection==='function')isolated.setProjection('SIN');
                if(typeof isolated.setRotation==='function'&&Number.isFinite(Number(destination.aladinRotation)))isolated.setRotation(Number(destination.aladinRotation));
                if(typeof isolated.gotoRaDec==='function')isolated.gotoRaDec(destination.ra,destination.dec);
                if(typeof isolated.setFov==='function')isolated.setFov(destination.fov);
            }catch(error){
                aladinPrewarmActiveKey='';
                throw error;
            }
            const completed=await new Promise(resolve=>{
                aladinPrewarmWaitResolve=resolve;
                aladinPrewarmTimer=setTimeout(()=>{
                    aladinPrewarmTimer=0;
                    if(aladinPrewarmWaitResolve===resolve)aladinPrewarmWaitResolve=null;
                    resolve(true);
                },ALADIN_PREWARM_DWELL_MS);
            });
            aladinPrewarmActiveKey='';
            if(!completed||backgroundWorkSuspended)throw abortError();
            const receipt=Object.freeze({
                key,
                ra:Number(destination.ra),
                dec:Number(destination.dec),
                fov:Number(destination.fov),
                rotation:Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):0,
                projection:'SIN',
                preparedAt:Date.now()
            });
            aladinPrewarmedKeys.add(key);
            aladinPreparedReceipts.set(key,receipt);
            aladinPrewarmLastKey=key;
            return receipt;
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
                return {x:cx,y:cy,angle,eccentricity,weight:sum};
            }catch(_){return null}
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
                const sourceImageProfile=imageLightProfile(sourceImage),sky=imageLightProfile(skyCanvas);
                if(!sourceImageProfile||!sky)return destination;
                const width=skyCanvas.clientWidth||skyCanvas.width||512,height=skyCanvas.clientHeight||skyCanvas.height||512;
                const desiredX=sourceImageProfile.x/FRAMING_SAMPLE_SIZE*width;
                const desiredY=sourceImageProfile.y/FRAMING_SAMPLE_SIZE*height;
                const currentX=sky.x/FRAMING_SAMPLE_SIZE*width;
                const currentY=sky.y/FRAMING_SAMPLE_SIZE*height;
                const maxDx=width*FRAMING_MAX_SHIFT_FRACTION,maxDy=height*FRAMING_MAX_SHIFT_FRACTION;
                const sampleX=width/2+clamp(currentX-desiredX,-maxDx,maxDx);
                const sampleY=height/2+clamp(currentY-desiredY,-maxDy,maxDy);
                if(typeof aladinPrewarm.pix2world!=='function')return destination;
                const world=aladinPrewarm.pix2world(sampleX,sampleY);
                const ra=Number(world?.[0]),dec=Number(world?.[1]);
                if(!Number.isFinite(ra)||!Number.isFinite(dec))return destination;
                const maxAngularShift=Math.max(.02,Number(destination.fov)*.30);
                if(angularSeparationDegrees(destination.ra,destination.dec,ra,dec)>maxAngularShift)return destination;
                let rotation=Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):null;
                if(rotation===null&&sourceImageProfile.eccentricity>.22&&sky.eccentricity>.22){
                    const delta=normalizeSignedAngle(sourceImageProfile.angle-sky.angle);
                    if(Number.isFinite(delta)&&Math.abs(delta)<=90)rotation=delta;
                }
                return Object.freeze({...destination,ra,dec,aladinRotation:rotation,framingCorrected:true});
            }catch(error){
                console.warn('GALAXY VIEWER OPTIONAL ARCHIVE FRAMING SKIPPED',error);
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
            const warmed=pool.filter(item=>aladinPrewarmedKeys.has(destinationKey(item)));
            const preferred=warmed.length?warmed:pool;
            return preferred[Math.floor(Math.random()*preferred.length)];
        }
    
        function chooseAladinAheadCandidates(destination,count=2){
            const blocked=blockedPrefetchKeys();
            blocked.add(destinationKey(destination));
            const pool=galaxyCatalog.filter(item=>{const key=destinationKey(item);return key&&!blocked.has(key)&&!aladinPrewarmedKeys.has(key)});
            const chosen=[];
            while(pool.length&&chosen.length<count){const index=Math.floor(Math.random()*pool.length);chosen.push(pool.splice(index,1)[0])}
            return chosen;
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
            const key=destinationKey(destination);
            const task=async()=>{
                if(backgroundWorkSuspended||!item?.image)return;
                try{
                    try{await prepareAladinDestination(destination,priority)}catch(error){
                        if(error?.name==='AbortError')return;
                        console.warn('GALAXY VIEWER ALADIN DESTINATION PREWARM WARNING',error);
                    }
                    if(backgroundWorkSuspended||aladinPrewarmLastKey!==key)return;
                    let preparedDestination=deriveSourceFraming(destination,item.image);
                    if(preparedDestination!==destination&&preparedDestination.framingCorrected){
                        try{await prepareAladinDestination(preparedDestination,true)}catch(error){
                            if(error?.name==='AbortError')return;
                            preparedDestination=destination;
                        }
                    }
                    item.destination=preparedDestination;
                }catch(error){
                    if(error?.name!=='AbortError')console.warn('GALAXY VIEWER SERIAL ALADIN PREWARM WARNING',error);
                }
            };
            const run=aladinPrefetchSerial.then(task,task);
            aladinPrefetchSerial=run.catch(()=>null);
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
                    prefetchRetryAfter.delete(key);
    
                    const hotKeys=new Set(
                        randomNavigationWindow?.hotKeys?.() ||
                        randomNavigationWindow?.getState?.().hotKeys ||
                        []
                    );
                    if(key!==activeTargetKey&&!hotKeys.has(key)){
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
                    scheduleAladinEnhancement(item,destination,priority);
                }catch(error){
                    if(error?.name==='AbortError'){
                        setHdStatus(destination,'SUSPENDED');
                        if(key===activeTargetKey)priorityPrefetchDestination=destination;
                        return;
                    }
                    prefetchFailedCount++;
                    setHdStatus(destination,'RETRY-WAIT');
                    prefetchRetryAfter.set(key,Date.now()+PREFETCH_RETRY_MS);
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
            while(prefetchLoading.size<PREFETCH_MAX_WORKERS&&prefetchQueued.length){
                const destination=prefetchQueued.shift();
                startPrefetch(destination,destinationKey(destination)===activeTargetKey);
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
    
        function setUnpreparedActive(destination){
            const key=destinationKey(destination);
            if(activePreparedItem&&activePreparedItem.key!==key)
                retainHistoryPrepared(activePreparedItem);
            activePreparedItem=null;
            activeTargetKey=key;
            priorityPrefetchDestination=destination;
            if(!backgroundWorkSuspended)queueMicrotask(fillPrefetchQueue);
            return {...destination,preparedHdUrl:'',preparedSource:'',preparedHdImage:null};
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
    
        function takeNextChandraTestDestination(excludeName=''){
            if(!chandraTestOverrideActive||!chandraTestQueue.length){chandraTestOverrideActive=false;return null}
            const excluded=String(excludeName||'').trim().toLowerCase();
            let index=chandraTestQueue.findIndex(item=>String(item?.name||'').trim().toLowerCase()!==excluded);
            if(index<0)index=0;
            const [destination]=chandraTestQueue.splice(index,1);
            if(!chandraTestQueue.length)chandraTestOverrideActive=false;
            return destination||null;
        }
    
        function randomGalaxyProvider({excludeName}={}){
            let destination=null;
            if(forcedDestination){
                releaseActiveArchivePreload();
                const requested=forcedDestination;
                forcedDestination=null;
                destination=consumeReady(requested,excludeName);
                if(!destination)destination=setUnpreparedActive(requested);
            }else{
                if(!galaxyCatalog.length)throw new Error('COMBINED GALAXY CATALOG IS EMPTY');
                releaseActiveArchivePreload();
                const chandraRequested=takeNextChandraTestDestination(excludeName);
                if(chandraRequested){
                    destination=consumeReady(chandraRequested,excludeName);
                    if(!destination)destination=setUnpreparedActive(chandraRequested);
                }else{
                    destination=consumeReady(null,excludeName);
                    if(!destination){
                        const requested=galaxyCatalog[Math.floor(Math.random()*galaxyCatalog.length)];
                        destination=setUnpreparedActive(requested);
                    }
                }
            }
            activeTargetKey=destinationKey(destination);
            if(Number.isFinite(Number(destination.aladinRotation))&&typeof window.aladin_cosmic_command_test?.setRotation==='function'){
                try{window.aladin_cosmic_command_test.setRotation(Number(destination.aladinRotation))}catch(error){console.warn('GALAXY VIEWER OPTIONAL ARRIVAL ROTATION SKIPPED',error)}
            }else if(typeof window.aladin_cosmic_command_test?.setRotation==='function'){
                try{window.aladin_cosmic_command_test.setRotation(0)}catch(_){}
            }
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
    
        function getAladinPrewarmState(){
            return Object.freeze({
                targetReady:PREFETCH_TARGET,
                cachedCount:aladinPrewarmedKeys.size,
                activeKey:aladinPrewarmActiveKey,
                queuedDestinations:[]
            });
        }

    const api={
      destinationKey,
      fillPrefetchQueue,
      enqueuePrefetch,
      consumeReady,
      setPreparedActive,
      setUnpreparedActive,
      prepareHdDestination,
      prepareAladinDestination,
      waitForPreparedKey,
      retainHistoryPrepared,
      takeHistoryPrepared,
      releasePreparedItem,
      enforceHotPreparedWindow,
      randomGalaxyProvider,
      getRandomNavigationState,
      getPrefetchState,
      getDownloadStatus,
      getAladinPrewarmState,
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
        return consumeReady(destination,excludeName)
            || setUnpreparedActive(destination);
      },

      requestHdPrefetch(destination){
        if(!destination)return '';
        enqueuePrefetch(destination,true);
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

      getAladinPreparedReceipt(key){
        return aladinPreparedReceipts.get(
          String(key||'').trim().toLowerCase()
        )||null;
      },

      isAladinPrepared(key){
        return Boolean(api.getAladinPreparedReceipt(key));
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
        options.earthReturnOptions
          ? createEarthReturnController({
              ...options.earthReturnOptions,
              root: this.viewerRoot,
              aladin: this.aladin
            })
          : null;
      this.#buildHomePresentation();
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
      this.ready = this.#initialize();
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
#gv-earth-return-indicator{position:absolute;left:50%;top:50%;z-index:7350;width:58px;height:48px;transform:translate(-50%,-50%);pointer-events:none;opacity:0;visibility:hidden;transition:opacity .12s linear}
#gv-earth-return-indicator.gv-visible{opacity:1;visibility:visible}
#gv-earth-return-indicator .gv-earth-return-arrow{position:absolute;left:50%;top:50%;width:17px;height:12px;transform:translate(-50%,-50%) rotate(0deg);transform-origin:50% 50%;filter:drop-shadow(0 0 3px rgba(87,255,147,.90)) drop-shadow(0 0 7px rgba(77,255,143,.42))}
#gv-earth-return-indicator .gv-earth-return-arrow::before{content:"";position:absolute;left:1px;top:1.5px;width:0;height:0;border-top:4.5px solid transparent;border-bottom:4.5px solid transparent;border-left:14px solid #78FFAB}
#gv-earth-return-indicator .gv-earth-return-readout{position:absolute;left:50%;top:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:52px;text-align:center;white-space:nowrap}
#gv-earth-return-indicator .gv-earth-return-icon{display:block;font:12px/12px system-ui,sans-serif;filter:grayscale(1) sepia(1) saturate(8) hue-rotate(82deg) brightness(1.22) drop-shadow(0 0 3px rgba(87,255,147,.92)) drop-shadow(0 0 7px rgba(77,255,143,.38))}
#gv-earth-return-indicator .gv-earth-return-distance{display:flex;align-items:baseline;justify-content:center;gap:2px;margin-top:2px;color:#78FFAB}
#gv-earth-return-indicator .gv-earth-return-value,#gv-earth-return-indicator .gv-earth-return-unit{display:block;color:#78FFAB;font:600 10.5px/12px "Space Age",sans-serif;letter-spacing:.35px;font-variant-numeric:tabular-nums;text-shadow:0 0 4px rgba(229,255,239,.88),0 0 8px rgba(87,255,147,.72),0 0 13px rgba(77,255,143,.34)}
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
#gv-we-are-here .gv-earth-icon{display:inline-flex;align-items:center;justify-content:center;font:22px/1 system-ui,sans-serif;filter:grayscale(1) sepia(1) saturate(8) hue-rotate(82deg) brightness(1.22) drop-shadow(0 0 4px rgba(87,255,147,.92)) drop-shadow(0 0 9px rgba(77,255,143,.48))}
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
.gvrg-value{min-width:0;min-height:15px;margin-top:1px;font:400 12px/1.16 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.15px;color:#ffffff;text-align:center;text-shadow:0 0 4px rgba(205,244,255,.18);white-space:normal;overflow-wrap:anywhere;pointer-events:none}
.gvrg-card-distance{display:block;min-width:0}
.gvrg-value-number{font:400 12px/1.16 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.15px}
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
#gv-random-galaxy{appearance:none;-webkit-appearance:none;position:static;display:flex;flex:1 1 auto;min-width:0;align-items:center;justify-content:center;height:36px;margin:0;padding:0 12px;border:1px solid #DDF8FF;border-radius:6px;background:linear-gradient(145deg,rgba(11,49,119,.96),rgba(20,132,219,.94));color:#EAF8FF;font:400 15.5px/1 "Space Age",sans-serif;letter-spacing:.38px;text-transform:uppercase;text-shadow:0 0 4px rgba(221,248,255,.76);box-shadow:inset 0 0 7px rgba(143,229,255,.28),0 0 8px rgba(41,109,189,.34);cursor:pointer;touch-action:manipulation;outline:none;pointer-events:auto}
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
#gv-travel-primary{box-sizing:border-box;width:calc(100vw - 24px);padding:4px 7px 5px;border:1px solid rgba(124,203,255,.76);border-radius:6px;background:rgba(8,27,58,.72);box-shadow:0 0 8px rgba(88,191,255,.14);text-align:center}
#gv-travel-course,#gv-travel-heading{font:400 13px/1.05 "Space Age",sans-serif;letter-spacing:.55px;color:#EAF8FF;text-align:center;text-shadow:0 0 4px rgba(88,191,255,.20)}
#gv-travel-course{font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#7CCBFF;text-shadow:0 0 7px rgba(88,191,255,.58)}
#gv-travel-heading{margin-top:1px;color:#A9DFFF}
#gv-travel-destination{margin-top:2px;font:400 16px/1.08 "Space Age",sans-serif;letter-spacing:.35px;color:#7CCBFF;text-shadow:0 0 7px rgba(88,191,255,.58);text-align:center;white-space:normal;overflow-wrap:anywhere}
#gv-travel-distance{box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;width:172px;height:34px;padding:2px 6px 1px;border:1px solid rgba(124,203,255,.78);border-radius:5px;background:rgba(8,27,58,.76);color:#78FFAB;text-align:center;text-shadow:0 0 4px rgba(229,255,239,.82),0 0 9px rgba(87,255,147,.34);white-space:nowrap}
#gv-travel-distance-value{position:relative;display:block;width:100%;height:18px;font:400 17px/18px "Space Age",sans-serif;letter-spacing:.32px;text-align:center;font-variant-numeric:tabular-nums}
#gv-travel-distance-integer{position:absolute;right:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:right;white-space:nowrap}
#gv-travel-distance-decimal{position:absolute;left:50%;top:0;width:6px;height:18px;transform:translateX(-50%);font:inherit;letter-spacing:0;text-align:center;white-space:nowrap}
#gv-travel-distance-fraction{position:absolute;left:calc(50% + 3px);top:0;height:18px;font:inherit;letter-spacing:inherit;text-align:left;white-space:nowrap}
#gv-travel-distance-unit{display:block;width:100%;height:12px;font:400 10.5px/12px "Space Age",sans-serif;letter-spacing:.45px;text-align:center;white-space:nowrap}
/* ============================================================ */
/* ECO-027B-1 HD / ARCHIVE PRESENTATION — OWNER 0034          */
/* ============================================================ */
#gv-random-galaxy{border:2px solid #7CCBFF!important;box-shadow:none!important;filter:brightness(1.10)}.gv-galaxy-history{border:2px solid #7CCBFF!important;box-shadow:none!important;filter:brightness(1.10);opacity:1!important}.gvrg-hd-science,.gvrg-hd-viewport,#gv-hd-info-panel{box-sizing:border-box!important;width:min(680px,calc(100vw - 20px))!important;border:0!important;border-radius:8px!important;position:absolute!important}.gvrg-hd-science::before,.gvrg-hd-viewport::before,#gv-hd-info-panel::before{content:""!important;position:absolute!important;inset:0!important;z-index:50!important;border-radius:8px!important;padding:1px!important;background:linear-gradient(135deg,#DDF8FF 0%,#8DDAFF 28%,#58BFFF 55%,#296DBD 100%)!important;-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0)!important;-webkit-mask-composite:xor!important;mask-composite:exclude!important;pointer-events:none!important;box-sizing:border-box!important}.gvrg-hd-science,#gv-hd-info-panel{background:transparent!important;box-shadow:inset 0 0 6px rgba(225,248,255,.06),0 0 8px rgba(124,203,255,.20)!important}.gvrg-hd-science{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;overflow:hidden!important;pointer-events:none!important}.gvrg-hd-science .gvrg-hd-science-item{padding:8px 8px!important}.gvrg-hd-science .gvrg-hd-science-value{font-size:10.5px!important}.gvrg-hd-viewport{position:absolute!important;left:50%!important;right:auto!important;transform:translateX(-50%)!important;aspect-ratio:auto!important;overflow:hidden!important;background:#02070F!important;box-shadow:inset 0 0 6px rgba(225,248,255,.08),0 0 8px rgba(124,203,255,.24)!important;pointer-events:auto!important}.gvrg-hd-viewport>img:not(#gv-hd-archive-button img){width:100%!important;height:100%!important;max-width:none!important;max-height:none!important;object-fit:contain!important;object-position:50% 50%;scale:1!important}.gvrg-hd-scale,.gvrg-hd-scale-label{font-size:13.5px!important}#gv-hd-info-panel{position:absolute;left:50%;z-index:4;transform:translateX(-50%);padding:9px 11px 10px;color:#DDF8FF;font:400 10.5px/1.45 "Space Age",sans-serif;letter-spacing:.42px;text-align:left;text-shadow:0 0 4px rgba(88,191,255,.22);display:flex;flex-direction:column;overflow:hidden;pointer-events:none}#gv-hd-info-title{flex:0 0 auto;margin-bottom:6px;color:#7CCBFF;font-size:12px;letter-spacing:.75px;text-align:center}#gv-hd-info-body{flex:1 1 auto;min-height:0;overflow:hidden;overflow-wrap:anywhere}.gvrg-credit{display:none!important}#gv-hd-control-row{position:absolute!important;left:11px!important;right:11px!important;bottom:10px!important;z-index:30!important;height:40px!important;display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;box-sizing:border-box!important;pointer-events:none!important}#gv-hd-control-row>.gvrg-back-button,#gv-hd-control-row>#gv-hd-download-button{position:static!important;left:auto!important;right:auto!important;top:auto!important;bottom:auto!important;flex:1 1 0!important;width:0!important;min-width:0!important;max-width:none!important;height:40px!important;min-height:40px!important;margin:0!important;padding:0 8px!important;gap:7px!important;box-sizing:border-box!important;align-items:center!important;justify-content:center!important;white-space:nowrap!important;overflow:hidden!important;font-size:10.5px!important;line-height:1!important;pointer-events:auto!important;touch-action:manipulation!important}#gv-hd-control-row>.gvrg-back-button>span:last-child,#gv-hd-control-row>#gv-hd-download-button>span:last-child{min-width:0!important;white-space:nowrap!important;overflow:visible!important;line-height:1!important}#gv-hd-control-row .gvrg-back-chevron,#gv-hd-control-row .gvrg-download-icon{width:18px!important;height:18px!important;flex:0 0 18px!important}#gv-hd-archive-button{position:absolute!important;right:14px!important;bottom:14px!important;z-index:40!important;width:36px!important;height:36px!important;margin:0!important;padding:2px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;box-sizing:content-box!important;border:2px solid transparent!important;border-radius:6px!important;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98)) padding-box,linear-gradient(145deg,#DDF8FF 0%,#7CCBFF 48%,#296DBD 100%) border-box!important;box-shadow:inset 0 0 6px rgba(225,248,255,.18),0 0 8px rgba(124,203,255,.40),0 0 13px rgba(41,109,189,.20)!important;filter:none!important;overflow:hidden!important;pointer-events:auto!important;touch-action:manipulation!important}#gv-hd-archive-button img{display:block!important;width:100%!important;height:100%!important;max-width:100%!important;max-height:100%!important;object-fit:contain!important;object-position:50% 50%!important;margin:0!important;padding:0!important;border:0!important;border-radius:4px!important;background:transparent!important;box-shadow:none!important}#gv-hd-archive-button .gv-hd-archive-comet{position:absolute;inset:4px;border-radius:50%;opacity:0;pointer-events:none;transform-origin:50% 50%}#gv-hd-archive-button .gv-hd-archive-comet::before{content:"";position:absolute;left:50%;top:-1px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#F8FFFF;box-shadow:0 0 4px #FFFFFF,0 0 8px #8FE5FF,0 0 12px #296DBD}#gv-hd-archive-button .gv-hd-archive-comet::after{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 250deg,rgba(15,54,122,0) 0deg,rgba(91,184,255,.22) 42deg,rgba(143,229,255,.56) 82deg,rgba(248,255,255,.92) 110deg,transparent 111deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));filter:drop-shadow(0 0 2px rgba(143,229,255,.72))}#gv-hd-archive-button.gv-archive-loading .gv-hd-archive-comet{opacity:1;animation:gvHdArchiveOrbit 1s linear infinite}@keyframes gvHdArchiveOrbit{to{transform:rotate(360deg)}}#gv-hd-download-button{border:2px solid #7CCBFF!important;border-radius:6px!important;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98))!important;color:#EAF8FF!important;box-shadow:none!important;filter:none!important}#gv-hd-download-button *{color:#EAF8FF!important;fill:#EAF8FF!important;stroke:#EAF8FF!important}#gv-hd-download-button .gvrg-download-icon{filter:drop-shadow(0 0 3px rgba(225,248,255,.92))!important}#gv-hd-download-button .gvrg-download-arrow{top:1px!important;width:3px!important;height:10px!important;background:#F7FDFF!important;border-radius:1px!important;box-shadow:0 0 3px rgba(225,248,255,.88)!important}#gv-hd-download-button .gvrg-download-arrow::after{bottom:-1px!important;width:8px!important;height:8px!important;border-right:3px solid #EAF8FF!important;border-bottom:3px solid #EAF8FF!important}#gv-hd-download-button .gvrg-download-bar{width:14px!important;height:3px!important;background:#F7FDFF!important;box-shadow:0 0 4px rgba(225,248,255,.92)!important}#gv-archive-overlay{position:fixed;inset:0;z-index:2147483000;background:#000;display:block;visibility:hidden;opacity:0;pointer-events:none}#gv-archive-overlay.gv-open{visibility:visible;opacity:1;pointer-events:auto}#gv-archive-frame{position:absolute;inset:0;width:100%;height:100%;border:0;background:#000;touch-action:auto!important;-webkit-overflow-scrolling:touch}#gv-archive-back{position:fixed;left:50%;bottom:max(18px,env(safe-area-inset-bottom));z-index:2147483647;transform:translateX(-50%);display:inline-flex;align-items:center;justify-content:center;gap:10px;height:48px;padding:0 12px;border:2px solid #7CCBFF;border-radius:7px;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98));color:#EAF8FF;font:400 13px/1 "Space Age",sans-serif;letter-spacing:.55px;text-transform:uppercase;white-space:nowrap;box-shadow:0 0 12px rgba(0,0,0,.75);pointer-events:auto;touch-action:manipulation;cursor:pointer}#gv-archive-arrow{position:relative;display:inline-flex;width:36px;height:36px;flex:0 0 36px;align-items:center;justify-content:center}#gv-archive-arrow::before,#gv-archive-arrow::after{content:"";position:absolute;left:50%;top:50%;width:17px;height:17px;border-style:solid;border-left:0;border-bottom:0;box-sizing:border-box;pointer-events:none}#gv-archive-arrow::before{border-width:6px;border-color:#7CCBFF;filter:drop-shadow(0 0 4px rgba(88,191,255,.90));transform:translate(-38%,-50%) rotate(-135deg)}#gv-archive-arrow::after{width:13px;height:13px;border-width:4px;border-color:#DFFBFF;filter:drop-shadow(0 0 3px rgba(98,216,255,.80));transform:translate(-34%,-50%) rotate(-135deg)}#gv-archive-target-tile{box-sizing:border-box;width:36px;height:36px;flex:0 0 36px;display:inline-flex;align-items:center;justify-content:center;border:2px solid #7CCBFF;border-radius:6px;background:linear-gradient(145deg,rgba(11,49,119,.98),rgba(20,132,219,.98));overflow:hidden}#gv-archive-target-tile img{display:block;width:28px;height:28px;object-fit:contain;flex:0 0 28px;margin:0;padding:0;border:0}


/* ============================================================
   REQ-026 / ECO-027B-2 — GALACTIC ICE VISUAL SYSTEM
   OWNER: gv-random-galaxy-0034.js
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
    const sizeFovSub = document.createElement('span');
    sizeFovSub.className = 'gvrg-fov-sub';
    sizeFovSub.textContent = '(FOV)';
    sizeRow.row.querySelector('.gvrg-label').append(document.createElement('br'), sizeFovSub);
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
      providerIcon.src = DEFAULT_PROVIDER_ICON_URL;
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
        const visible = /^(FINDING GALAXY|GALAXY UNAVAILABLE)/i.test(text);
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
      if (!this.provider) throw new Error('Random Galaxy 0032 requires a local galaxy provider.');
      const raw = await this.provider({ excludeName: cleanText(excludeName), module: this });
      return this.#normalizeProviderCandidate(raw && raw.destination ? raw.destination : raw);
    }

    #normalizeProviderCandidate(candidate) {
      if (!candidate || typeof candidate !== 'object') throw new Error('Galaxy provider returned no destination.');
      const name = cleanText(candidate.name || candidate.objectName);
      const ra = finiteNumber(candidate.ra);
      const dec = finiteNumber(candidate.dec);
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
      const imageFovDegrees = finiteNumber(candidate.imageFovDegrees ?? candidate.image_fov_degrees ?? candidate.fieldOfViewDegrees ?? candidate.field_of_view_degrees);
      const fov = finiteNumber(candidate.fov) ?? 0.25;
      const hdUrl = validHttpsUrl(candidate.hdUrl || candidate.hd_url);
      const sourceUrl = validHttpsUrl(candidate.sourceUrl || candidate.source_url);
      const imageType = cleanText(candidate.imageType || candidate.image_type);
      const category = cleanText(candidate.category);
      const telescope = cleanText(candidate.telescope || candidate.facility);
      const credit = cleanText(candidate.credit);
      if (!name) throw new Error('Galaxy destination is missing its galaxy name.');
      if (ra == null || ra < 0 || ra >= 360) throw new Error('Galaxy destination has invalid RA.');
      if (dec == null || dec < -90 || dec > 90) throw new Error('Galaxy destination has invalid Dec.');
      if (distance == null || distance <= 0) throw new Error('Galaxy destination has no usable distance.');
      if (!constellation) throw new Error('Galaxy destination has no constellation.');
      if (!hdUrl || !isSupportedProviderHost(hdUrl.hostname)) throw new Error('Galaxy destination has no verified provider HD asset.');
      if (!sourceUrl || !isSupportedProviderHost(sourceUrl.hostname)) throw new Error('Galaxy destination has no verified provider source page.');
      if (imageType && rejectNonObservationLabel(imageType)) throw new Error('Rejected non-observation galaxy entry.');
      if (category && !/galax/i.test(category)) throw new Error('Rejected non-galaxy entry.');
      if (telescope && !/(hubble|webb|chandra)/i.test(telescope)) throw new Error('Rejected entry without supported telescope data.');
      return Object.freeze({
        source: cleanText(candidate.source || 'GALAXY PROVIDER'),
        name, ra, dec, distance, constellation, age, ageYears, physicalSizeLy, designation, commonName, preparedHdUrl, preparedSource, preparedHdImage, imageFovDegrees,
        fov,
        hdUrl: hdUrl.href,
        sourceUrl: sourceUrl.href,
        credit,
        imageType: imageType || 'Observation',
        category: category || 'Galaxies',
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
    #translationProgress(t, immediate = false) {
      if (immediate) {
        if (t >= 0.5) return 1;
        return smootherstep(clamp01(t / 0.5));
      }
      const start = Number(this.options.translateStart);
      const ninety = Number(this.options.translate90);
      const complete = Number(this.options.translationComplete);
      if (t <= start) return 0;
      if (t <= ninety) return 0.90 * smootherstep((t - start) / (ninety - start));
      if (t <= complete) return 0.90 + 0.10 * smootherstep((t - ninety) / (complete - ninety));
      return 1;
    }
    #fovAt(t, startFov, destinationFov, immediate = false) {
      if (immediate) {
        if (t <= 0.5) return startFov;
        const progress = smootherstep(clamp01((t - 0.5) / 0.5));
        return Math.exp(Math.log(startFov) + (Math.log(destinationFov) - Math.log(startFov)) * progress);
      }
      const turn = Number(this.options.turnPoint);
      const maximum = Number(this.options.maxFov);
      if (t <= turn) {
        const progress = smootherstep(t / turn);
        return Math.exp(Math.log(startFov) + (Math.log(maximum) - Math.log(startFov)) * progress);
      }
      const progress = smootherstep((t - turn) / (1 - turn));
      return Math.exp(Math.log(maximum) + (Math.log(destinationFov) - Math.log(maximum)) * progress);
    }
    #distanceProgress(t) {
      const turn = Number(this.options.turnPoint);
      const ninety = Number(this.options.translate90);
      const complete = Number(this.options.translationComplete);
      if (t <= turn) return 0.20 * smootherstep(t / turn);
      if (t <= ninety) return 0.20 + 0.70 * smootherstep((t - turn) / (ninety - turn));
      if (t <= complete) return 0.90 + 0.08 * smootherstep((t - ninety) / (complete - ninety));
      return 0.98 + 0.02 * smootherstep((t - complete) / (1 - complete));
    }
    #showDistance(source, destination, route) {
      this.routeEl.textContent = route.exactRoute ? `${source.name.toUpperCase()} TO ${destination.name.toUpperCase()}` : `TO ${destination.name.toUpperCase()}`;
      this.distanceRenderer.render(0);
      if (this.progressFill) this.progressFill.style.width = '0%';
      this.distanceBox.style.opacity = '1';
    }
    #hideDistance() { this.distanceBox.style.opacity = '0'; }
    #hideCard() { this.card.classList.remove('gvrg-card-visible'); }
    #showCard(destination) {
      this.nameEl.textContent = destination.name.toUpperCase();
      this.designationValueEl.textContent = cleanText(destination.designation).toUpperCase();
      this.commonNameValueEl.textContent = cleanText(destination.commonName || destination.name).toUpperCase();
      this.distanceValueNumberEl.textContent = formatDistanceMly(destination.distance).replace(/\bMILLION LIGHT-YEARS\b/g, 'MLY');
      this.distanceValueUnitEl.textContent = '';
      this.constellationValueEl.textContent = cleanText(destination.constellation).toUpperCase();
      this.ageValueEl.textContent = destination.ageYears ? formatAgeYears(destination.ageYears) : cleanText(destination.age).toUpperCase();
      this.sizeValueEl.textContent = formatPhysicalSize(destination.physicalSizeLy);
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

    #exactActiveAladinState(destination = this.activeDestination) {
      if (!destination) return null;
      const ra = finiteNumber(destination.ra);
      const dec = finiteNumber(destination.dec);
      const fov = finiteNumber(destination.fov);
      if (ra === null || dec === null || fov === null || fov <= 0) return null;
      return Object.freeze({
        ra,
        dec,
        fov,
        rotation: finiteNumber(destination.aladinRotation) ?? 0,
        projection: cleanText(this.options.arrivalProjection || 'SIN') || 'SIN',
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
          if (typeof this.aladin.setFrame === 'function')
            this.aladin.setFrame('ICRSd');
        } catch (_) {}

        try {
          if (target.projection &&
              typeof this.aladin.setProjection === 'function')
            this.aladin.setProjection(target.projection);
        } catch (error) {
          console.warn(
            'GALAXY RANDOM ALADIN RECOVERY PROJECTION SKIPPED',
            reason,
            error
          );
        }

        try {
          if (Number.isFinite(Number(target.rotation)) &&
              typeof this.aladin.setRotation === 'function')
            this.aladin.setRotation(Number(target.rotation));
        } catch (error) {
          console.warn(
            'GALAXY RANDOM ALADIN RECOVERY ROTATION SKIPPED',
            reason,
            error
          );
        }

        try {
          if (typeof this.aladin.gotoRaDec === 'function')
            this.aladin.gotoRaDec(Number(target.ra), Number(target.dec));
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
            this.aladin.setFov(Number(target.fov));
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
      if (this.destroyed || this.hdOpen || this.aladinRecoveryBusy) return;
      if (!this.#aladinCanvasLooksStale()) return;

      this.aladinRecoveryBusy = true;

      setTimeout(() => {
        if (this.destroyed) {
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
      if (this.destroyed) return;

      requestAnimationFrame(() => {
        if (this.destroyed) return;

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
      const turn = 0.46;
      const ninety = 0.58;
      const complete = 0.68;

      if (t <= turn)
        return 0.20 * smootherstep(t / turn);

      if (t <= ninety)
        return 0.20 +
          0.70 * smootherstep(
            (t - turn) / (ninety - turn)
          );

      if (t <= complete)
        return 0.90 +
          0.08 * smootherstep(
            (t - ninety) / (complete - ninety)
          );

      return 0.98 +
        0.02 * smootherstep(
          (t - complete) / (1 - complete)
        );
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
        firstHomeTrip
          ? Number(this.options.firstHomeTravelSeconds)
          : Number(this.options.travelSeconds);

      const total =
        Number.isFinite(Number(route && route.value))
          ? Number(route.value)
          : 0;

      destinationEl.textContent =
        cleanText(destination && destination.name).toUpperCase();

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

    async travelToRandom() {
      requestPortraitOrientation('random-travel').catch(() => {});
      await this.ready;
      if (this.destroyed || this.busy) return null;
      this.busy = true;
      this.#hideRefreshSky();
      this.#hideHomePresentation();
      setRandomWaitComet(this.randomButton, true);
      this.arrived = false;
      this.#hideCard();
      this.backToSky({ recover: false });
      if (this.randomButton) this.randomButton.disabled = true;
      try {
        this.#setStatus('FINDING GALAXY');
        const destination = await this.#consumeDestination();
        this.activeDestination = destination;
        this.#setTravelStatus(destination.name);
        const coords = this.aladin.getRaDec();
        const fov = this.aladin.getFov();
        const startRA = Number(coords[0]);
        const startDec = Number(coords[1]);
        const startFov = Number(fov[0]);
        const destinationFov = Number(destination.fov);
        if (!Number.isFinite(startFov) || startFov <= 0)
          throw new Error('CURRENT ALADIN FOV IS INVALID');
        if (!Number.isFinite(destinationFov) || destinationFov <= 0)
          throw new Error('DESTINATION ALADIN FOV IS INVALID');
        const source = { ...this.currentGalaxy, ra: startRA, dec: startDec };
        const firstHomeTrip = this.#isHomeDeparture(source, startFov);
        const route = routeDistanceMillionLy(source, destination);
        this.#beginTravelHud(destination, route, firstHomeTrip);
        this.#showDistance(source, destination, route);
        this.#requestGeminiEnrichment(destination).then((result) => { if (result) this.lastGeminiEnrichment = result; }).catch(() => {});
        const duration = (
          firstHomeTrip
            ? Number(this.options.firstHomeTravelSeconds)
            : Number(this.options.travelSeconds)
        ) * 1000;
        const started = performance.now();
        await new Promise((resolve) => {
          const frame = (now) => {
            const t = Math.min(1, (now - started) / duration);
            const move = this.#translationProgress(t, firstHomeTrip);
            const position = greatCirclePosition(startRA, startDec, destination.ra, destination.dec, move);
            this.aladin.gotoRaDec(position[0], position[1]);
            const currentFov = this.#fovAt(t, startFov, destinationFov, firstHomeTrip);
            this.aladin.setFov(currentFov);
            this.distanceRenderer.render(route.value * this.#distanceProgress(t));
            if (this.progressFill) this.progressFill.style.width = `${(t * 100).toFixed(1)}%`;
            if (t < 1) { requestAnimationFrame(frame); return; }
            this.aladin.gotoRaDec(destination.ra, destination.dec);
            this.aladin.setFov(destinationFov);
            this.distanceRenderer.render(route.value);
            if (this.progressFill) this.progressFill.style.width = '100%';
            resolve();
          };
          requestAnimationFrame(frame);
        });
        this.currentGalaxy = { name: destination.name, ra: destination.ra, dec: destination.dec, distance: destination.distance };
        this.arrived = true;
        this.busy = false;
        setRandomWaitComet(this.randomButton, false);
        this.#hideDistance();
        this.#showCard(destination);
        this.#setStatus(`ARRIVED ${destination.name.toUpperCase()}`);
        if (this.randomButton) this.randomButton.disabled = false;

        // Random arrival always ends at the authoritative prepared framing.
        this.#recoverExactActiveAladin('random-arrival');
        this.#armRefreshSkyWatchdog('random-arrival');
        requestAnimationFrame(() =>
          this.#checkAndRecoverStaleAladin('random-arrival-postcheck')
        );

        this.#endTravelHud();

        if (this.onArrival) this.onArrival(destination, this);
        if (this.options.prefetch) this.prefetch().catch(() => {});
        return destination;
      } catch (error) {
        this.busy = false;
        setRandomWaitComet(this.randomButton, false);
        this.arrived = true;
        this.#hideDistance();
        this.#endTravelHud();
        if (this.randomButton) this.randomButton.disabled = false;
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
      const fovDegrees = finiteNumber(destination && destination.imageFovDegrees);
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
      requestPortraitOrientation('hd-view').catch(() => {});
      this.#hideRefreshSky();
      const destination = this.activeDestination;
      if (!destination || !destination.hdUrl) throw new Error('No HD image is available for the active destination.');

      // Preserve the user's exact sky position/zoom before HD obscures Aladin.
      if (!this.hdOpen)
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
      this.hdFallbackImage.src = destination.hdUrl;
      return destination.hdUrl;
    }
    async downloadHD() {
      const destination = this.activeDestination;
      if (!destination || !destination.hdUrl) throw new Error('No HD image is available for download.');
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
      const response = await fetch(destination.hdUrl, { cache: 'no-store' });
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
      return destination.hdUrl;
    }
    backToSky(options = {}) {
      requestPortraitOrientation('sky-return').catch(() => {});
      if (!this.hdOpen) return;

      const recover = options?.recover !== false;
      const restoreState =
        this.hdSkySnapshot ||
        this.#exactActiveAladinState();

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
          requestAnimationFrame(() =>
            this.#checkAndRecoverStaleAladin('hd-return-postcheck')
          );
        });
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
    installPreparationEngine(options = {}) {
      if(this.preparationEngine)
        return this.preparationEngine;

      this.preparationEngine=
        createRandomPreparationEngine(options);

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
      return {
        version: VERSION,
        busy: this.busy,
        arrived: this.arrived,
        hdOpen: this.hdOpen,
        hdScale: this.hdScale,
        currentGalaxy: { ...this.currentGalaxy },
        activeDestination: this.activeDestination,
        prefetched: Boolean(this.prefetchedDestination),
        hubbleOnly: true,
        galaxyOnly: true,
        catalogTarget: Number(this.options.catalogTarget) || 1879,
        catalogCount: this.catalogCount,
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
const VERSION='ACTIVE';
const FUTURE_TARGET=10;
const WEB_MAX=10;
const WEB_RETRY_MS=5000;
const POLL_MS=80;
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const keyOf=item=>String(item?.key||item?.destination?.archiveId||item?.destination?.name||item?.archiveId||item?.name||'').trim().toLowerCase();
let core=null;
let randomGalaxy=null;
let randomNavigationWindow=null;
let originalProvider=null;
let catalog=[];
let catalogByKey=new Map();
let catalogByName=new Map();
const futureRecords=new Map();
let activeRecord=null;
let nextSequence=0;
let historyBypass=false;
let installed=false;
let suspended=false;
let hdFeedbackBusy=false;
const webControllers=new Map();

function findDestinationByName(name){return catalogByName.get(String(name||'').trim().toLowerCase())||null}
function findDestinationByKey(key){return catalogByKey.get(String(key||'').trim().toLowerCase())||null}
function currentBlockedKeys(){
  const blocked=new Set();
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
  const state=core.getPrefetchState?.()||{};
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
  const pool=catalog.filter(destination=>!blocked.has(keyOf(destination)));
  if(!pool.length)return null;
  return pool[Math.floor(Math.random()*pool.length)];
}
function webStateFor(record){
  return record?.web||{state:'QUEUED',detail:'',nextRetryAt:0,sourceUrl:String(record?.destination?.sourceUrl||'').trim()};
}
function setWebState(record,state,detail=''){
  if(!record?.key)return;
  const old=webStateFor(record);
  record.web={
    state,
    detail:String(detail||''),
    nextRetryAt:state==='RETRY'?Date.now()+WEB_RETRY_MS:old.nextRetryAt||0,
    sourceUrl:String(record.destination?.sourceUrl||old.sourceUrl||'').trim()
  };
}
function suspendWeb(){
  suspended=true;
  const protectedKey=String(activeRecord?.key||'').trim().toLowerCase();
  for(const [key,controller] of webControllers){
    if(protectedKey&&String(key||'').trim().toLowerCase()===protectedKey)continue;
    try{controller.abort()}catch(_){}
    const record=activeRecord?.key===key?activeRecord:futureRecords.get(key);
    if(record)setWebState(record,'SUSPENDED');
  }
}
function resumeWeb(){
  suspended=false;
  for(const record of [activeRecord,...futureRecords.values()].filter(Boolean)){
    const state=webStateFor(record);
    if(state.state==='SUSPENDED')setWebState(record,'QUEUED');
  }
  pumpWeb();
}
function makeRecord(destination){
  const key=keyOf(destination);
  return {
    sequence:++nextSequence,
    key,
    destination,
    hd:{state:'QUEUED',resource:null,sourceKind:''},
    aladin:{
      state:'QUEUED',
      ra:Number(destination?.ra),
      dec:Number(destination?.dec),
      fov:Number(destination?.fov),
      rotation:Number.isFinite(Number(destination?.aladinRotation))?Number(destination.aladinRotation):0
    },
    web:{state:'QUEUED',detail:'',nextRetryAt:0,sourceUrl:String(destination?.sourceUrl||'').trim()}
  };
}
function startWeb(record){
  if(!record?.key||suspended||webControllers.size>=WEB_MAX||webControllers.has(record.key))return;
  const state=webStateFor(record);
  if(state.state==='READY'||state.state==='DOWNLOADING')return;
  if(state.state==='RETRY'&&Date.now()<Number(state.nextRetryAt||0))return;
  const sourceUrl=String(record.destination?.sourceUrl||'').trim();
  if(!/^https:\/\//i.test(sourceUrl)){setWebState(record,'FAILED','NO SOURCE URL');return}
  const controller=new AbortController();
  webControllers.set(record.key,controller);
  setWebState(record,'DOWNLOADING');
  fetch(sourceUrl,{mode:'no-cors',cache:'force-cache',credentials:'omit',signal:controller.signal,priority:'low'})
    .then(()=>setWebState(record,'READY'))
    .catch(error=>{if(error?.name==='AbortError'){setWebState(record,'SUSPENDED');return}setWebState(record,'RETRY',String(error?.message||error))})
    .finally(()=>{webControllers.delete(record.key);setTimeout(pumpWeb,0)});
}
function orderedFutureRecords(){
  return randomNavigationWindow.getFuture().filter(Boolean);
}
function pumpWeb(){
  if(suspended)return;
  const candidates=[activeRecord,...orderedFutureRecords()].filter(Boolean);
  for(const record of candidates){if(webControllers.size>=WEB_MAX)break;startWeb(record)}
}
let futureAladinSerial=Promise.resolve();

function syntheticUnavailableReceipt(record){
  return Object.freeze({
    key:record.key,
    ra:Number(record.destination?.ra),
    dec:Number(record.destination?.dec),
    fov:Number(record.destination?.fov),
    rotation:Number.isFinite(Number(record.destination?.aladinRotation))
      ? Number(record.destination.aladinRotation)
      : 0,
    projection:'SIN',
    preparedAt:Date.now(),
    unavailable:true
  });
}

function markAladinReady(record,receipt){
  record.aladin={
    state:'READY',
    receipt,
    requested:false,
    ra:Number(record.destination?.ra),
    dec:Number(record.destination?.dec),
    fov:Number(record.destination?.fov),
    rotation:Number.isFinite(Number(record.destination?.aladinRotation))
      ? Number(record.destination.aladinRotation)
      : 0
  };
}

function queueAladinPreparation(record){
  if(!record?.key)return;
  if(record.aladin?.state==='READY'||record.aladin?.requested)return;

  record.aladin={...record.aladin,state:'QUEUED',requested:true};

  const task=async()=>{
    if(!record?.key)return;

    if(suspended||core?.getBackgroundWorkSuspended?.()){
      record.aladin={...record.aladin,state:'SUSPENDED',requested:false};
      return;
    }

    record.aladin={...record.aladin,state:'PREPARING',requested:true};

    try{
      let receipt=await core?.ensureAladinPreparedForNavigation?.(
        record.destination
      );

      if(!receipt&&core?.isAladinPrepared?.(record.key)){
        receipt=
          core?.getAladinPreparedReceipt?.(record.key)||
          syntheticUnavailableReceipt(record);
      }

      const receiptKey=String(receipt?.key||"").trim().toLowerCase();

      if(receiptKey!==record.key){
        throw new Error(
          'RANDOM GALAXY FUTURE ALADIN RECEIPT IDENTITY MISMATCH'
        );
      }

      markAladinReady(record,receipt);
    }catch(error){
      // ensureAladinPrewarm can discover unavailability during this request.
      // Re-check the authoritative core fallback after the failure.
      if(core?.isAladinPrepared?.(record.key)){
        const receipt=
          core?.getAladinPreparedReceipt?.(record.key)||
          syntheticUnavailableReceipt(record);

        markAladinReady(record,receipt);
      }else{
        record.aladin={
          ...record.aladin,
          state:'RETRY',
          requested:false,
          receipt:null,
          detail:String(error?.message||error)
        };

        console.warn(
          'RANDOM GALAXY FUTURE ALADIN PREPARATION WARNING',
          record.key,error
        );
      }
    }finally{
      updateRandomButtonReadyState();
    }
  };

  // One hidden Aladin instance = one serialized preparation stream.
  futureAladinSerial=futureAladinSerial.then(task,task);
}

function prepareRecord(record){
  if(!record)return;

  core?.requestHdPrefetch?.(record.destination);
  queueAladinPreparation(record);

  if(!record.web)setWebState(record,'QUEUED');
  pumpWeb();
}
function addFuture(destination){
  if(!destination)return false;
  const key=keyOf(destination);
  if(!key||currentBlockedKeys().has(key))return false;
  const record=makeRecord(destination);
  if(!randomNavigationWindow.appendFuture(record))return false;
  futureRecords.set(key,record);
  prepareRecord(record);
  return true;
}
function pruneFutureRecords(){
  const allowed=new Set(randomNavigationWindow.getFuture().map(bundle=>bundle.key));
  for(const [key,record] of futureRecords){
    if(allowed.has(key))continue;
    futureRecords.delete(key);
    const controller=webControllers.get(key);
    if(controller){try{controller.abort()}catch(_){};webControllers.delete(key)}
  }
}
function reconcileFutureQueue(){
  pruneFutureRecords();

  const pipeline=pipelineDestinations();
  for(const destination of pipeline){
    if(randomNavigationWindow.needsFuture()<=0)break;
    addFuture(destination);
  }

  while(randomNavigationWindow.needsFuture()>0){
    const candidate=chooseUniqueDestination();
    if(!candidate||!addFuture(candidate))break;
  }

  if(!suspended&&!core?.getBackgroundWorkSuspended?.()){
    for(const record of orderedFutureRecords()){
      aladinStateFor(record);
      if(record.aladin?.state!=='READY'){
        queueAladinPreparation(record);
      }
    }
  }

  pumpWeb();
}
async function consumeNext(excludeName=''){
  reconcileFutureQueue();

  const excluded=String(excludeName||'').trim().toLowerCase();
  const readyForNavigation=bundle=>{
    const destination=bundle?.destination;
    const key=String(bundle?.key||'').trim().toLowerCase();
    if(!destination||!key)return false;
    hdStateFor(bundle);
    aladinStateFor(bundle);
    return String(destination.name||'').trim().toLowerCase()!==excluded&&
      key!==activeRecord?.key&&
      Boolean(bundle.hd?.resource)&&
      bundle.hd?.state==='READY'&&
      bundle.aladin?.state==='READY';
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

  let destination=core.activateQueuedDestination(record.destination,excludeName);
  activeRecord.destination=destination;

  const exactReceipt=await core.ensureAladinPreparedForNavigation?.(destination);
  if(!exactReceipt||String(exactReceipt.key||'').trim().toLowerCase()!==lockedKey){
    activeRecord=null;
    randomNavigationWindow.rollbackLocked();
    throw new Error('RANDOM GALAXY LOCKED BUNDLE ALADIN REVALIDATION FAILED');
  }
  activeRecord.aladin={
    state:'READY',
    receipt:exactReceipt,
    ra:Number(destination.ra),
    dec:Number(destination.dec),
    fov:Number(destination.fov),
    rotation:Number.isFinite(Number(destination.aladinRotation))?Number(destination.aladinRotation):0
  };

  const claimed=randomNavigationWindow.claimLocked();
  if(claimed!==record||keyOf(claimed)!==lockedKey){
    randomNavigationWindow.rollbackPending();
    throw new Error('RANDOM GALAXY CLAIMED BUNDLE IDENTITY MISMATCH');
  }

  setTimeout(reconcileFutureQueue,100);
  pumpWeb();
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
  const status=(core.getDownloadStatus?.()||[]).find(item=>String(item?.key||'').toLowerCase()===record.key);
  const state=normalizeHdState(status?.state);
  const resource=state==='READY'?core.getHdPreparedResource?.(record.key)||null:null;
  record.hd={
    state,
    resource,
    sourceKind:String(resource?.sourceKind||status?.sourceKind||'')
  };
  return {state,progress:state==='READY'?100:null,detail:record.hd.sourceKind};
}
function hasReadyNavigation(){
  reconcileFutureQueue();
  return randomNavigationWindow.isNextReady(bundle=>{
    if(!bundle?.destination||!bundle?.key)return false;
    hdStateFor(bundle);
    aladinStateFor(bundle);
    return Boolean(bundle.hd?.resource)&&
      bundle.hd?.state==='READY'&&
      bundle.aladin?.state==='READY';
  });
}
function updateRandomButtonReadyState(){
  if(!core?.randomGalaxyButton)return;
  if(core.getBackgroundWorkSuspended?.()||randomGalaxy?.getState?.().busy)return;
  core.randomGalaxyButton.disabled=!hasReadyNavigation();
}
function aladinStateFor(record){
  let state='QUEUED',progress=null;

  let receipt=
    core.getAladinPreparedReceipt?.(record.key)||
    record.aladin?.receipt||
    null;

  if(receipt){
    state='READY';
    progress=100;
  }else if(core?.isAladinPrepared?.(record.key)){
    receipt=syntheticUnavailableReceipt(record);
    state='READY';
    progress=100;
  }else if(core.getBackgroundWorkSuspended?.()){
    state='SUSPENDED';
  }else{
    const live=core.getAladinPrewarmState?.()||{};

    if(String(live.activeKey||'').toLowerCase()===record.key){
      state='PREPARING';
    }else if(record.aladin?.state==='RETRY'){
      state='RETRY';
    }
  }

  record.aladin={
    ...record.aladin,
    state,
    receipt,
    requested:Boolean(record.aladin?.requested),
    ra:Number(record.destination?.ra),
    dec:Number(record.destination?.dec),
    fov:Number(record.destination?.fov),
    rotation:Number.isFinite(Number(record.destination?.aladinRotation))
      ? Number(record.destination.aladinRotation)
      : 0
  };

  return {state,progress};
}
function webTelemetry(record){
  const state=webStateFor(record);
  return {state:state.state,progress:state.state==='READY'?100:null,detail:state.detail||''};
}
function telemetry(){
  return Object.freeze({
    version:VERSION,
    suspended:Boolean(core?.getBackgroundWorkSuspended?.()),
    active:activeRecord?Object.freeze({sequence:activeRecord.sequence,key:activeRecord.key,name:String(activeRecord.destination?.name||''),provider:String(activeRecord.destination?.provider||'')}):null,
    rows:Object.freeze(orderedFutureRecords().slice(0,FUTURE_TARGET).map(record=>Object.freeze({sequence:record.sequence,key:record.key,name:String(record.destination?.name||''),provider:String(record.destination?.provider||''),hd:Object.freeze(hdStateFor(record)),aladin:Object.freeze(aladinStateFor(record)),web:Object.freeze(webTelemetry(record))})))
  });
}
function installHdFeedback(){
  if(!randomGalaxy?.providerIconButton)return;
  const style=document.createElement('style');
  style.id='gv-prefetch-hd-feedback-style';
  style.textContent='.gvrg-hd-icon-button{position:relative!important}.gv-prefetch-hd-feedback{position:absolute;inset:5px;border-radius:50%;opacity:0;pointer-events:none;transform-origin:50% 50%}.gv-prefetch-hd-feedback::before{content:"";position:absolute;left:50%;top:-1px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#F8FFFF;box-shadow:0 0 4px #fff,0 0 8px #8FE5FF,0 0 11px #296DBD}.gv-prefetch-hd-feedback::after{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 250deg,transparent 0deg,rgba(91,184,255,.25) 42deg,rgba(143,229,255,.58) 82deg,rgba(248,255,255,.92) 110deg,transparent 111deg 360deg);-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));mask:radial-gradient(farthest-side,transparent calc(100% - 2px),#000 calc(100% - 2px))}.gvrg-hd-icon-button.gv-prefetch-hd-wait .gv-prefetch-hd-feedback{opacity:1;animation:gvPrefetchHdOrbit 1s linear infinite}@keyframes gvPrefetchHdOrbit{to{transform:rotate(360deg)}}';
  document.head.appendChild(style);
  const feedback=document.createElement('span');
  feedback.className='gv-prefetch-hd-feedback';feedback.setAttribute('aria-hidden','true');
  randomGalaxy.providerIconButton.appendChild(feedback);
  const waitForHd=async(key,timeout=2500)=>{const started=performance.now();for(;;){const state=hdStateFor({key});if(state.state==='READY')return true;if(performance.now()-started>=timeout)return false;await sleep(80)}};
  const handle=async event=>{
    const destination=randomGalaxy.getState?.().activeDestination;
    if(!destination||hdFeedbackBusy)return;
    event.preventDefault();event.stopPropagation();event.stopImmediatePropagation();
    hdFeedbackBusy=true;
    randomGalaxy.providerIconButton.classList.add('gv-prefetch-hd-wait');
    const key=keyOf(destination);
    core.requestHdPrefetch?.(destination);
    try{await Promise.all([sleep(1000),waitForHd(key,2500)]);randomGalaxy.showHD()}catch(error){console.error('GALAXY VIEWER PREFETCH HD ENTRY FAILURE',error);try{randomGalaxy.showHD()}catch(_){} }finally{randomGalaxy.providerIconButton.classList.remove('gv-prefetch-hd-wait');hdFeedbackBusy=false}
  };
  randomGalaxy.viewHdButton?.addEventListener('click',handle,true);
  randomGalaxy.providerIconButton?.addEventListener('click',handle,true);
}
function install(){
  if(installed)return true;
  core=window.GalaxyViewerCore;
  if(!core?.randomGalaxy||typeof core.getGalaxyCatalog!=='function'||typeof core.activateQueuedDestination!=='function')return false;
  randomGalaxy=core.randomGalaxy;
  randomNavigationWindow=core.randomNavigationWindow;
  if(!randomNavigationWindow)throw new Error('RANDOM GALAXY NAVIGATION WINDOW CORE EXPORT MISSING');
  originalProvider=randomGalaxy.provider;
  catalog=core.getGalaxyCatalog();
  catalogByKey=new Map(catalog.map(destination=>[keyOf(destination),destination]));
  catalogByName=new Map(catalog.map(destination=>[String(destination?.name||'').trim().toLowerCase(),destination]));
  reconcileFutureQueue();
  randomGalaxy.provider=async args=>{
    if(historyBypass){historyBypass=false;return originalProvider(args)}

    const destination=await consumeNext(args?.excludeName||'');
    if(!destination)throw new Error('AUTHORITATIVE NEXT GALAXY IS NOT READY');


    // The exact FIFO destination is now active and owns its prepared HD
    // resource. Only now may unrelated background preparation be suspended.
    core.suspendBackgroundWork?.();
    core.suspendArchivePreloads?.();

    return destination;
  };
  core.historyBackButton?.addEventListener('click',()=>{if(!core.historyBackButton.disabled)historyBypass=true},true);
  core.historyForwardButton?.addEventListener('click',()=>{if(!core.historyForwardButton.disabled)historyBypass=true},true);
  core.randomGalaxyButton?.addEventListener('click',()=>{setTimeout(()=>{if(core.getBackgroundWorkSuspended?.())suspendWeb()},0)},true);
  const monitor=setInterval(()=>{
    const nextSuspended=Boolean(core.getBackgroundWorkSuspended?.());
    if(nextSuspended!==suspended){if(nextSuspended)suspendWeb();else resumeWeb()}
    if(!nextSuspended)reconcileFutureQueue();
    if(!nextSuspended)updateRandomButtonReadyState();
  },POLL_MS);
  window.addEventListener('beforeunload',()=>{clearInterval(monitor);for(const controller of webControllers.values())try{controller.abort()}catch(_){};webControllers.clear()},{once:true});
  installHdFeedback();
  if(core.versionLabel){core.versionLabel.textContent='VERSION 12D';core.versionLabel.setAttribute('aria-label','GALAXY VIEWER VERSION 12D')}
  GalaxyRandomGalaxy.getPrefetchTelemetry=telemetry;GalaxyRandomGalaxy.reconcileFutureQueue=reconcileFutureQueue;GalaxyRandomGalaxy.hasReadyNavigation=hasReadyNavigation;GalaxyRandomGalaxy.prefetchRuntime=Object.freeze({version:VERSION,displayVersion:VERSION,core,randomGalaxy});
  installed=true;
  document.dispatchEvent(new CustomEvent('gv-prefetch-ready',{detail:{version:VERSION,rows:randomNavigationWindow.getState().futureCount}}));
  return true;
}
if(!install()){
  const onReady=()=>setTimeout(install,0);
  document.addEventListener('gv-viewer-ready',onReady,{once:true});
  const timer=setInterval(()=>{if(install())clearInterval(timer)},100);
  setTimeout(()=>clearInterval(timer),30000);
}
})();

  global.GalaxyRandomNavigationWindow = GalaxyRandomNavigationWindow;
  global.GalaxyRandomGalaxy = GalaxyRandomGalaxy;
})(window);
