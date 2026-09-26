/*
GALAXY VIEWER ENGINEERING CHANGE ORDER — RANDOM GALAXY 0011
AUTHORIZED BASELINE: gv-random-galaxy-0010.js blob a4a9ddb3c28751dfbbf9fcdf04278c80e1020013.
AUTHORIZED CHANGES: readable compact arrival presentation, five-field HD science banner, exact retained decoded-image handoff for immediate HD display, and 0011 identity. Touch-through interaction, 36px Hubble controls, top-centered HD viewing, no post-arrival reframing, and 24.075-second travel are preserved.
*/
(function (global) {
  'use strict';

  const VERSION = '0011';

  const FONT_URLS = Object.freeze({
    spaceAge: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001',
    digits: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/GV-Coordinate-Digits-0005.otf?v=7R-slashed-zero-coordinate-digits-0005'
  });

  const FONT_NAMES = Object.freeze({
    spaceAge: 'GV Random Galaxy Space Age 0011',
    digits: 'GV Random Galaxy Digits 0011'
  });

  const HUBBLE_ICON_URL = 'https://gear66me-ui.github.io/Galaxy_Viewer/viewer/artwork/Hubble/Hubble-NASA-ESA-logo.png?v=9283e83cfbacd230551e9fc005794138be59709b';

  const DEFAULTS = Object.freeze({
    geminiEndpoint: null,
    travelSeconds: 24.075,
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
    hdMaxScale: 8
  });

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
  function isEsaHubbleHost(hostname) {
    const host = String(hostname || '').toLowerCase();
    return host === 'esahubble.org' || host.endsWith('.esahubble.org');
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
  function formatPhysicalSize(size) {
    if (!size) return '';
    if (Array.isArray(size) && size.length >= 2) {
      const a = finiteNumber(size[0]), b = finiteNumber(size[1]);
      if (a == null || b == null || a <= 0 || b <= 0) return '';
      if (a < 1_000_000 && b < 1_000_000) return `${Math.round(a).toLocaleString('en-US')} × ${Math.round(b).toLocaleString('en-US')} LIGHT-YEARS`;
      const scale = Math.max(a, b) >= 1_000_000_000 ? 1_000_000_000 : 1_000_000;
      const unit = scale === 1_000_000_000 ? 'BILLION LIGHT-YEARS' : 'MILLION LIGHT-YEARS';
      return `${Math.round(a / scale).toLocaleString('en-US')} × ${Math.round(b / scale).toLocaleString('en-US')} ${unit}`;
    }
    const value = finiteNumber(size);
    return value == null || value <= 0 ? '' : formatWholeAstronomyScale(value);
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
        document.fonts.load(`400 12px "${FONT_NAMES.spaceAge}"`, 'DISTANCE TO EARTH CONSTELLATION GALAXY AGE VIEW HUBBLE HD'),
        document.fonts.load(`400 18px "${FONT_NAMES.digits}"`, '0123456789.')
      ]);
      await document.fonts.ready;
      return true;
    })();
    return fontsPromise;
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

  class GalaxyRandomGalaxy {
    constructor(options = {}) {
      if (!options.aladin) throw new TypeError('GalaxyRandomGalaxy requires an Aladin instance.');
      if (!(options.host instanceof Element)) throw new TypeError('GalaxyRandomGalaxy requires a DOM Element host.');
      if (instances.has(options.host)) throw new Error('GalaxyRandomGalaxy is already mounted on this host.');

      this.options = { ...DEFAULTS, ...options };
      this.aladin = options.aladin;
      this.host = options.host;
      this.randomButton = options.randomButton instanceof Element ? options.randomButton : null;
      this.hubbleProvider = typeof options.hubbleProvider === 'function' ? options.hubbleProvider : null;
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
      this.currentGalaxy = this.#initialCurrent(options.currentGalaxy);
      this.onStatus = typeof options.onStatus === 'function' ? options.onStatus : null;
      this.onArrival = typeof options.onArrival === 'function' ? options.onArrival : null;
      this.onError = typeof options.onError === 'function' ? options.onError : null;

      this.root = this.#build();
      this.host.appendChild(this.root);
      this.distanceRenderer = new FixedDistanceRenderer(this.distanceNumberHost, this.options);

      this._randomClick = () => this.travelToRandom().catch((error) => this.#handleError(error));
      this._randomRequest = (event) => {
        event.preventDefault();
        event.stopPropagation();
        this.travelToRandom().catch((error) => this.#handleError(error));
      };
      this._hdClick = () => this.showHubbleHD();
      this._downloadClick = () => this.downloadHubbleHD().catch((error) => this.#handleError(error));
      this._backClick = () => this.backToSky();
      this._pointerDown = (event) => this.#onHdPointerDown(event);
      this._pointerMove = (event) => this.#onHdPointerMove(event);
      this._pointerUp = (event) => this.#onHdPointerUp(event);

      if (this.randomButton) {
        if (this.options.bindClick) this.randomButton.addEventListener('click', this._randomClick);
        this.randomButton.addEventListener(this.options.requestEvent, this._randomRequest);
      }
      this.viewHdButton.addEventListener('click', this._hdClick);
      this.hubbleIconButton.addEventListener('click', this._hdClick);
      this.downloadButton.addEventListener('click', this._downloadClick);
      this.backButton.addEventListener('click', this._backClick);
      this.hdViewport.addEventListener('pointerdown', this._pointerDown);
      this.hdViewport.addEventListener('pointermove', this._pointerMove);
      this.hdViewport.addEventListener('pointerup', this._pointerUp);
      this.hdViewport.addEventListener('pointercancel', this._pointerUp);

      instances.set(this.host, this);
      this.ready = this.#initialize();
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
.gvrg-status{display:none;position:absolute;left:50%;top:72px;transform:translateX(-50%);width:min(280px,82vw);padding:9px 12px;border:1px solid rgba(183,255,208,.86);border-radius:6px;background:rgba(0,18,10,.62);color:#eafff1;font:400 12px/1.3 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.8px;text-align:center;box-shadow:0 0 14px rgba(77,255,143,.30),inset 0 0 9px rgba(77,255,143,.09);opacity:0;visibility:hidden;transition:opacity .18s ease;pointer-events:none}
.gvrg-status-visible{opacity:1;visibility:visible}
.gvrg-status-kicker{font:400 9px/1.2 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1.7px;color:#9eeab9}
.gvrg-status-heading{margin-top:2px;font:400 12px/1.2 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;color:#dfffea}
.gvrg-status-destination{margin-top:3px;font:400 14px/1.22 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.9px;color:#78ffab;text-shadow:0 0 9px rgba(87,255,147,.70);white-space:normal;overflow-wrap:anywhere}
.gvrg-distance{display:none;position:absolute;left:50%;top:154px;transform:translateX(-50%);width:min(330px,88vw);padding:9px 11px 10px;border:1px solid rgba(183,255,208,.72);border-radius:6px;background:rgba(0,12,8,.66);box-shadow:0 0 13px rgba(77,255,143,.20);text-align:center;opacity:0;transition:opacity .20s linear}
.gvrg-distance-label{height:14px;font:400 9px/14px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:2px;color:#93dcae}
.gvrg-distance-number{display:flex;align-items:center;justify-content:center;gap:8px;height:28px;white-space:nowrap;overflow:hidden}
.gvrg-number-cells{display:inline-flex;align-items:baseline;justify-content:flex-end;flex:none}
.gvrg-digit-cell,.gvrg-decimal-cell{display:inline-flex;align-items:center;justify-content:center;flex:none;height:25px;font:400 20px/25px "${FONT_NAMES.digits}",sans-serif;color:#f2fff7;text-shadow:0 0 7px rgba(87,255,147,.34);transform:scaleY(1.08);transform-origin:center}
.gvrg-distance-unit{display:inline-flex;align-items:center;width:158px;height:25px;overflow:hidden;font:400 9px/25px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.7px;color:#dfffea;text-align:left;white-space:nowrap}
.gvrg-route{height:14px;font:400 8px/14px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;color:#a4d8b7;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.gvrg-progress{height:3px;margin-top:6px;border-radius:3px;background:rgba(183,255,208,.14);overflow:hidden}
.gvrg-progress-fill{width:0;height:100%;background:#66ff9f;box-shadow:0 0 8px rgba(102,255,159,.75);transition:width .08s linear}
.gvrg-card{position:absolute;left:50%;top:75%;transform:translate(-50%,-50%);width:min(286px,78vw);padding:7px 8px 8px;border:1px solid rgba(175,225,255,.88);border-radius:6px;background:rgba(0,8,17,.72);box-shadow:0 0 12px rgba(80,190,255,.26);opacity:0;transition:opacity .20s ease;pointer-events:none}
.gvrg-card-visible{opacity:1;pointer-events:none}
.gvrg-name{display:none}
.gvrg-science-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 7px;pointer-events:none}.gvrg-row{display:block;min-width:0;margin:0;padding:2px 0 3px;border-bottom:1px solid rgba(130,185,212,.10);text-align:center;pointer-events:none}
.gvrg-label{font:400 10px/1.12 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.48px;color:#b9e9ff;text-align:center;text-shadow:0 0 4px rgba(98,216,255,.24);pointer-events:none}
.gvrg-value{min-width:0;min-height:15px;margin-top:1px;font:400 12px/1.16 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.15px;color:#ffffff;text-align:center;text-shadow:0 0 4px rgba(205,244,255,.18);white-space:normal;overflow-wrap:anywhere;pointer-events:none}
.gvrg-card-distance{display:block;min-width:0}
.gvrg-value-number{font:400 12px/1.16 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.15px}
.gvrg-value-unit{display:none}
.gvrg-actions{display:grid;grid-template-columns:minmax(0,1fr) 36px;gap:5px;align-items:stretch;margin-top:6px;pointer-events:none}
.gvrg-button{appearance:none;border:1px solid rgba(175,225,255,.84);border-radius:5px;background:rgba(7,27,42,.95);color:#effbff;padding:6px 8px;font:400 9px/1 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.55px;cursor:pointer}
.gvrg-button:disabled{opacity:.45;cursor:default}
.gvrg-hd-primary{min-width:0;height:36px;padding:4px 8px;font:400 11px/1.05 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.55px;text-align:center;box-shadow:inset 0 0 8px rgba(98,216,255,.08),0 0 7px rgba(98,216,255,.12);pointer-events:auto}
.gvrg-hd-icon-button{width:36px;height:36px;padding:2px;display:flex;align-items:center;justify-content:center;overflow:hidden;pointer-events:auto}
.gvrg-hd-icon-button img{display:block;width:100%;height:100%;object-fit:contain;background:transparent;pointer-events:none}
.gvrg-hd{position:absolute;inset:0;display:none;z-index:20;background:#000;pointer-events:auto;overflow:hidden}
.gvrg-hd-open{display:block}
.gvrg-hd-viewport{position:absolute;inset:0;display:flex;align-items:flex-start;justify-content:center;overflow:hidden;touch-action:none;user-select:none;-webkit-user-select:none;cursor:grab}
.gvrg-hd-viewport:active{cursor:grabbing}
.gvrg-hd img{position:relative;inset:auto;width:auto;height:auto;max-width:100%;max-height:100%;object-fit:contain;background:#000;transform-origin:50% 0;will-change:transform;pointer-events:none;user-select:none;-webkit-user-drag:none}
.gvrg-hd-science{position:absolute;left:50%;top:max(4px,env(safe-area-inset-top));z-index:4;transform:translateX(-50%);width:min(560px,94vw);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2px 4px;padding:3px 5px;border:1px solid rgba(120,255,171,.84);border-radius:6px;background:rgba(0,12,9,.72);box-shadow:0 0 12px rgba(77,255,143,.22);text-align:center;pointer-events:none}
.gvrg-hd-science-item{min-width:0;padding:0 1px;pointer-events:none}
.gvrg-hd-science-label{font:400 8px/1.04 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.30px;color:#9eeab9;text-align:center;pointer-events:none}
.gvrg-hd-science-value{min-height:10px;margin-top:0;font:400 9px/1.06 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.08px;color:#ffffff;text-shadow:0 0 4px rgba(205,255,224,.20);text-align:center;white-space:normal;overflow-wrap:anywhere;pointer-events:none}
@media(min-width:520px){.gvrg-hd-science{grid-template-columns:repeat(5,minmax(0,1fr))}}
.gvrg-hd-footer{position:absolute;left:0;right:0;bottom:0;z-index:3;padding:28px 10px 10px;background:linear-gradient(transparent,rgba(0,0,0,.94));text-align:center;pointer-events:none}
.gvrg-hd-footer>*{pointer-events:auto}
.gvrg-credit{margin-bottom:8px;font:400 8px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.5px;color:#d8eff9}
.gvrg-hd-controls{display:flex;justify-content:center;gap:8px;flex-wrap:wrap}
.gvrg-hd-controls .gvrg-button{min-height:40px;font-size:11px}
.gvrg-hd-loading{position:absolute;left:50%;top:50%;z-index:2;transform:translate(-50%,-50%);font:400 9px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;color:#dff7ff;pointer-events:none}`;
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
      const commonNameRow = makeRow('NAME');
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
      const sizeRow = makeRow('SIZE');
      this.sizeValueEl = sizeRow.value;
      scienceGrid.append(designationRow.row, commonNameRow.row, distanceRow.row, constellationRow.row, ageRow.row, sizeRow.row);

      const actions = document.createElement('div');
      actions.className = 'gvrg-actions';
      const viewHd = document.createElement('button');
      viewHd.type = 'button';
      viewHd.className = 'gvrg-button gvrg-hd-primary';
      viewHd.textContent = 'VIEW HUBBLE HD';
      this.viewHdButton = viewHd;
      const hubbleIconButton = document.createElement('button');
      hubbleIconButton.type = 'button';
      hubbleIconButton.className = 'gvrg-button gvrg-hd-icon-button';
      hubbleIconButton.setAttribute('aria-label', 'VIEW HUBBLE HD');
      const hubbleIcon = document.createElement('img');
      hubbleIcon.src = HUBBLE_ICON_URL;
      hubbleIcon.alt = '';
      hubbleIcon.setAttribute('aria-hidden', 'true');
      hubbleIconButton.appendChild(hubbleIcon);
      this.hubbleIconButton = hubbleIconButton;
      actions.append(viewHd, hubbleIconButton);
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
      viewport.appendChild(hdImage);
      const loading = document.createElement('div');
      loading.className = 'gvrg-hd-loading';
      loading.textContent = 'LOADING HUBBLE HD';
      this.hdLoading = loading;

      const hdScience = document.createElement('div');
      hdScience.className = 'gvrg-hd-science';
      hdScience.setAttribute('aria-label', 'HUBBLE GALAXY INFORMATION');
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
      const hdSize = makeHdScienceItem('SIZE');
      this.hdSizeValueEl = hdSize.value;
      hdScience.append(hdDesignation.item, hdCommonName.item, hdDistance.item, hdAge.item, hdSize.item);
      this.hdScience = hdScience;

      const footer = document.createElement('div');
      footer.className = 'gvrg-hd-footer';
      const credit = document.createElement('div');
      credit.className = 'gvrg-credit';
      this.creditEl = credit;
      const controls = document.createElement('div');
      controls.className = 'gvrg-hd-controls';
      const download = document.createElement('button');
      download.type = 'button';
      download.className = 'gvrg-button';
      download.textContent = 'DOWNLOAD IMAGE';
      this.downloadButton = download;
      const back = document.createElement('button');
      back.type = 'button';
      back.className = 'gvrg-button';
      back.textContent = 'BACK TO SKY';
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
        this.#setStatus('FINDING HUBBLE GALAXY');
        this.prefetch().then(() => this.#setStatus('READY')).catch(() => this.#setStatus('READY'));
      } else this.#setStatus('READY');
      return this;
    }

    #setStatus(message) {
      const text = cleanText(message);
      if (this.statusEl) {
        this.statusEl.classList.remove('gvrg-status-travel');
        this.statusEl.textContent = text;
        const visible = /^(FINDING HUBBLE GALAXY|HUBBLE GALAXY UNAVAILABLE)/i.test(text);
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
      this.#setStatus('HUBBLE GALAXY UNAVAILABLE — TRY AGAIN');
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

    async #getHubbleCandidate(excludeName) {
      if (!this.hubbleProvider) throw new Error('Random Galaxy 0011 requires the local Hubble catalog provider.');
      const raw = await this.hubbleProvider({ excludeName: cleanText(excludeName), module: this });
      return this.#normalizeHubbleCandidate(raw && raw.destination ? raw.destination : raw);
    }

    #normalizeHubbleCandidate(candidate) {
      if (!candidate || typeof candidate !== 'object') throw new Error('Hubble provider returned no destination.');
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
      const fov = finiteNumber(candidate.fov) ?? 0.25;
      const hdUrl = validHttpsUrl(candidate.hdUrl || candidate.hd_url);
      const sourceUrl = validHttpsUrl(candidate.sourceUrl || candidate.source_url);
      const imageType = cleanText(candidate.imageType || candidate.image_type);
      const category = cleanText(candidate.category);
      const telescope = cleanText(candidate.telescope || candidate.facility);
      const credit = cleanText(candidate.credit || 'ESA/Hubble');
      if (!name) throw new Error('Hubble destination is missing its galaxy name.');
      if (ra == null || ra < 0 || ra >= 360) throw new Error('Hubble destination has invalid RA.');
      if (dec == null || dec < -90 || dec > 90) throw new Error('Hubble destination has invalid Dec.');
      if (distance == null || distance <= 0) throw new Error('Hubble destination has no usable distance.');
      if (!constellation) throw new Error('Hubble destination has no constellation.');
      if (!hdUrl || !isEsaHubbleHost(hdUrl.hostname)) throw new Error('Hubble destination has no verified ESA/Hubble HD asset.');
      if (!sourceUrl || !isEsaHubbleHost(sourceUrl.hostname)) throw new Error('Hubble destination has no verified ESA/Hubble source page.');
      if (imageType && rejectNonObservationLabel(imageType)) throw new Error('Rejected non-observation Hubble entry.');
      if (category && !/galax/i.test(category)) throw new Error('Rejected non-galaxy Hubble entry.');
      if (telescope && !/hubble/i.test(telescope)) throw new Error('Rejected entry without Hubble telescope data.');
      return Object.freeze({
        source: cleanText(candidate.source || 'ESA/HUBBLE GALAXIES CATALOG'),
        hubble: true,
        name, ra, dec, distance, constellation, age, ageYears, physicalSizeLy, designation, commonName, preparedHdUrl, preparedSource, preparedHdImage,
        fov: clamp(fov, 0.05, 8),
        hdUrl: hdUrl.href,
        sourceUrl: sourceUrl.href,
        credit,
        imageType: imageType || 'Observation',
        category: category || 'Galaxies',
        telescope: telescope || 'Hubble Space Telescope',
        archiveId: cleanText(candidate.archiveId || candidate.id)
      });
    }

    async prefetch() {
      if (this.destroyed) return null;
      if (this.prefetchedDestination) return this.prefetchedDestination;
      if (this.prefetchPromise) return this.prefetchPromise;
      const excludeName = this.currentGalaxy && this.currentGalaxy.name;
      this.prefetchPromise = this.#getHubbleCandidate(excludeName)
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
      return this.#getHubbleCandidate(this.currentGalaxy && this.currentGalaxy.name);
    }

    #translationProgress(t) {
      const start = Number(this.options.translateStart);
      const ninety = Number(this.options.translate90);
      const complete = Number(this.options.translationComplete);
      if (t <= start) return 0;
      if (t <= ninety) return 0.90 * smootherstep((t - start) / (ninety - start));
      if (t <= complete) return 0.90 + 0.10 * smootherstep((t - ninety) / (complete - ninety));
      return 1;
    }
    #fovAt(t, startFov, destinationFov) {
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
      this.distanceValueNumberEl.textContent = formatDistanceMly(destination.distance);
      this.distanceValueUnitEl.textContent = '';
      this.constellationValueEl.textContent = cleanText(destination.constellation).toUpperCase();
      this.ageValueEl.textContent = destination.ageYears ? formatAgeYears(destination.ageYears) : cleanText(destination.age).toUpperCase();
      this.sizeValueEl.textContent = formatPhysicalSize(destination.physicalSizeLy);
      this.viewHdButton.disabled = false;
      this.hubbleIconButton.disabled = false;
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
        source: 'ESA/Hubble'
      };
      const result = this.geminiProvider ? await this.geminiProvider(payload, this) : await this.#fetchJsonEndpoint(this.options.geminiEndpoint, payload);
      return result && typeof result === 'object' ? result : null;
    }

    async travelToRandom() {
      await this.ready;
      if (this.destroyed || this.busy) return null;
      this.busy = true;
      this.arrived = false;
      this.#hideCard();
      this.backToSky();
      if (this.randomButton) this.randomButton.disabled = true;
      try {
        this.#setStatus('FINDING HUBBLE GALAXY');
        const destination = await this.#consumeDestination();
        this.activeDestination = destination;
        this.#setTravelStatus(destination.name);
        const coords = this.aladin.getRaDec();
        const fov = this.aladin.getFov();
        const startRA = Number(coords[0]);
        const startDec = Number(coords[1]);
        const startFov = Math.max(0.02, Number(fov[0]));
        const destinationFov = Math.max(0.05, Number(destination.fov));
        const source = { ...this.currentGalaxy, ra: startRA, dec: startDec };
        const route = routeDistanceMillionLy(source, destination);
        this.#showDistance(source, destination, route);
        this.#requestGeminiEnrichment(destination).then((result) => { if (result) this.lastGeminiEnrichment = result; }).catch(() => {});
        const duration = Number(this.options.travelSeconds) * 1000;
        const started = performance.now();
        let projectionState = this.options.arrivalProjection;
        await new Promise((resolve) => {
          const frame = (now) => {
            const t = Math.min(1, (now - started) / duration);
            const move = this.#translationProgress(t);
            const position = greatCirclePosition(startRA, startDec, destination.ra, destination.dec, move);
            this.aladin.gotoRaDec(position[0], position[1]);
            const currentFov = this.#fovAt(t, startFov, destinationFov);
            this.aladin.setFov(currentFov);
            if (typeof this.aladin.setProjection === 'function') {
              if (projectionState === this.options.arrivalProjection && t < Number(this.options.turnPoint) && currentFov >= Number(this.options.aitEntryFov)) {
                this.aladin.setProjection(this.options.wideProjection);
                projectionState = this.options.wideProjection;
              }
              if (projectionState === this.options.wideProjection && t > Number(this.options.turnPoint) && currentFov <= Number(this.options.sinReturnFov)) {
                this.aladin.setProjection(this.options.arrivalProjection);
                projectionState = this.options.arrivalProjection;
              }
            }
            this.distanceRenderer.render(route.value * this.#distanceProgress(t));
            if (this.progressFill) this.progressFill.style.width = `${(t * 100).toFixed(1)}%`;
            if (t < 1) { requestAnimationFrame(frame); return; }
            this.aladin.gotoRaDec(destination.ra, destination.dec);
            this.aladin.setFov(destinationFov);
            if (typeof this.aladin.setProjection === 'function' && projectionState !== this.options.arrivalProjection) this.aladin.setProjection(this.options.arrivalProjection);
            this.distanceRenderer.render(route.value);
            if (this.progressFill) this.progressFill.style.width = '100%';
            resolve();
          };
          requestAnimationFrame(frame);
        });
        this.currentGalaxy = { name: destination.name, ra: destination.ra, dec: destination.dec, distance: destination.distance };
        this.arrived = true;
        this.busy = false;
        this.#hideDistance();
        this.#showCard(destination);
        this.#setStatus(`ARRIVED ${destination.name.toUpperCase()}`);
        if (this.randomButton) this.randomButton.disabled = false;
        if (this.onArrival) this.onArrival(destination, this);
        if (this.options.prefetch) this.prefetch().catch(() => {});
        return destination;
      } catch (error) {
        this.busy = false;
        this.arrived = true;
        this.#hideDistance();
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
    #positionHdViewportBelowScience() {
      const overlayRect = this.hdOverlay.getBoundingClientRect();
      const scienceRect = this.hdScience.getBoundingClientRect();
      this.hdViewport.style.top = `${Math.max(0, Math.ceil(scienceRect.bottom - overlayRect.top + 6))}px`;
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
    #applyHdTransform() {
      this.hdImage.style.transform = `translate3d(${this.hdTranslateX}px,${this.hdTranslateY}px,0) scale(${this.hdScale})`;
    }
    #resetHdTransform() {
      this.hdScale = 1;
      this.hdTranslateX = 0;
      this.hdTranslateY = 0;
      this.hdPointers.clear();
      this.hdGesture = null;
      this.#applyHdTransform();
    }
    #pointerPair() {
      const values = [...this.hdPointers.values()];
      if (values.length < 2) return null;
      const [a, b] = values;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const rect = this.hdViewport.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      return {
        distance: Math.hypot(dx, dy),
        midX: (a.x + b.x) / 2 - centerX,
        midY: (a.y + b.y) / 2 - centerY
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
      if (this.hdScale <= 1) {
        this.hdScale = 1;
        this.hdTranslateX = 0;
        this.hdTranslateY = 0;
      }
      this.#applyHdTransform();
    }
    #onHdPointerUp(event) {
      if (!this.hdPointers.has(event.pointerId)) return;
      event.preventDefault();
      this.hdPointers.delete(event.pointerId);
      if (this.hdPointers.size === 1) {
        const remaining = [...this.hdPointers.values()][0];
        this.hdGesture = { mode: 'pan', x: remaining.x, y: remaining.y, tx: this.hdTranslateX, ty: this.hdTranslateY };
      } else if (this.hdPointers.size === 0) this.hdGesture = null;
    }

    showHubbleHD() {
      const destination = this.activeDestination;
      if (!destination || !destination.hubble || !destination.hdUrl) throw new Error('No Hubble HD image is available for the active destination.');
      const preparedImage = destination.preparedHdImage instanceof HTMLImageElement && destination.preparedHdImage.complete && destination.preparedHdImage.naturalWidth ? destination.preparedHdImage : null;
      this.#populateHdScience(destination);
      this.creditEl.textContent = `CREDIT ${destination.credit || 'ESA/Hubble'}`;
      this.hdOverlay.classList.add('gvrg-hd-open');
      this.hdOpen = true;
      this.#positionHdViewportBelowScience();
      if (preparedImage) {
        this.#mountHdImage(preparedImage);
        this.hdImage.alt = destination.name;
        this.hdImage.onload = null;
        this.hdImage.onerror = null;
        this.hdLoading.textContent = '';
        this.hdLoading.style.display = 'none';
        this.#resetHdTransform();
        return destination.preparedHdUrl || preparedImage.currentSrc || preparedImage.src;
      }
      this.#mountHdImage(this.hdFallbackImage);
      this.hdFallbackImage.removeAttribute('src');
      this.hdFallbackImage.alt = destination.name;
      this.hdLoading.textContent = 'LOADING HUBBLE HD';
      this.hdLoading.style.display = 'block';
      this.hdFallbackImage.onload = () => { this.hdLoading.style.display = 'none'; };
      this.hdFallbackImage.onerror = () => { this.hdLoading.textContent = 'HUBBLE HD IMAGE COULD NOT LOAD'; this.hdLoading.style.display = 'block'; };
      this.#resetHdTransform();
      this.hdFallbackImage.src = destination.hdUrl;
      return destination.hdUrl;
    }
    async downloadHubbleHD() {
      const destination = this.activeDestination;
      if (!destination || !destination.hubble || !destination.hdUrl) throw new Error('No Hubble HD image is available for download.');
      const stem = cleanText(destination.archiveId || destination.name || 'hubble-hd').replace(/[^a-z0-9._-]+/gi, '-').replace(/^-+|-+$/g, '') || 'hubble-hd';
      const downloadUrl = destination.preparedHdUrl || destination.hdUrl;
      try {
        const response = await fetch(downloadUrl, { cache: destination.preparedHdUrl ? 'default' : 'no-store' });
        if (!response.ok) throw new Error(`Hubble HD download returned HTTP ${response.status}.`);
        const blob = await response.blob();
        const objectUrl = URL.createObjectURL(blob);
        const anchor = document.createElement('a');
        anchor.href = objectUrl;
        anchor.download = `${stem}-Hubble-HD.jpg`;
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
        setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
      } catch (_) {
        const anchor = document.createElement('a');
        anchor.href = destination.hdUrl;
        anchor.download = `${stem}-Hubble-HD.jpg`;
        anchor.target = '_blank';
        anchor.rel = 'noopener';
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
      }
      return destination.hdUrl;
    }
    backToSky() {
      if (!this.hdOpen) return;
      this.hdOverlay.classList.remove('gvrg-hd-open');
      if (this.hdImage === this.hdFallbackImage) this.hdFallbackImage.removeAttribute('src');
      this.hdFallbackImage.onload = null;
      this.hdFallbackImage.onerror = null;
      this.#resetHdTransform();
      this.hdOpen = false;
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
        discoverySource: 'LOCAL HUBBLE CATALOG PROVIDER',
        digitFont: FONT_URLS.digits,
        travelSeconds: Number(this.options.travelSeconds),
        geminiKeyEmbedded: false
      };
    }
    destroy() {
      if (this.destroyed) return;
      this.destroyed = true;
      if (this.randomButton) {
        if (this.options.bindClick) this.randomButton.removeEventListener('click', this._randomClick);
        this.randomButton.removeEventListener(this.options.requestEvent, this._randomRequest);
      }
      this.viewHdButton.removeEventListener('click', this._hdClick);
      this.hubbleIconButton.removeEventListener('click', this._hdClick);
      this.downloadButton.removeEventListener('click', this._downloadClick);
      this.backButton.removeEventListener('click', this._backClick);
      this.hdViewport.removeEventListener('pointerdown', this._pointerDown);
      this.hdViewport.removeEventListener('pointermove', this._pointerMove);
      this.hdViewport.removeEventListener('pointerup', this._pointerUp);
      this.hdViewport.removeEventListener('pointercancel', this._pointerUp);
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
  GalaxyRandomGalaxy.FONT_URLS = FONT_URLS;
  GalaxyRandomGalaxy.DEFAULTS = DEFAULTS;
  GalaxyRandomGalaxy.PROVIDER_CONTRACT = Object.freeze({
    hubbleDiscovery: {
      defaultSource: 'local validated ESA/Hubble catalog provider',
      browserOnly: true,
      backendRequired: false,
      catalogTarget: 1879,
      selection: 'Galaxy-category, Hubble-backed observation images only',
      liveArchiveScraping: false
    },
    optionalHubbleProvider: {
      request: { excludeName: 'optional previous destination name' },
      response: { destination: { name: 'required', ra: 'required ICRS degrees', dec: 'required ICRS degrees', distanceMly: 'required positive million light-years', constellation: 'required', age: 'optional authoritative age text', physicalSizeLy: 'optional authoritative physical size in light-years', designation: 'optional catalog designation', commonName: 'optional common/title name', preparedHdUrl: 'optional retained runtime object URL', preparedHdImage: 'optional retained decoded HTMLImageElement for immediate HD display', fov: 'optional degrees', hdUrl: 'required trusted ESA/Hubble image URL', sourceUrl: 'required trusted ESA/Hubble source URL', credit: 'required/preferred', imageType: 'Observation preferred', category: 'Galaxies required', telescope: 'Hubble Space Telescope required' } }
    },
    geminiEndpoint: {
      method: 'POST',
      optional: true,
      secretRule: 'Store GEMINI_API_KEY server-side only. Never place it in this JavaScript module.',
      modelHint: 'Gemini Flash-Lite'
    }
  });

  global.GalaxyRandomGalaxy = GalaxyRandomGalaxy;
})(window);
