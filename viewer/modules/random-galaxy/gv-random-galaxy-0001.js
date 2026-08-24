(function (global) {
  'use strict';

  const VERSION = '0001';

  const FONT_URLS = Object.freeze({
    spaceAge: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular/Space%20Age%20Regular.otf?v=6R-space-age-regular-001',
    digits: 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/artwork/Fonts/Space%20Age%20Regular%20GV-9/GV-Coordinate-Digits-0005.otf?v=7R-slashed-zero-coordinate-digits-0005'
  });

  const FONT_NAMES = Object.freeze({
    spaceAge: 'GV Random Galaxy Space Age 0001',
    digits: 'GV Random Galaxy Digits 0001'
  });

  const DEFAULTS = Object.freeze({
    hubbleEndpoint: '/api/random-hubble-galaxy',
    geminiEndpoint: null,
    travelSeconds: 28.89,
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
    prefetch: true
  });

  const instances = new WeakMap();
  let fontsPromise = null;

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, Number(value)));
  }

  function clamp01(value) {
    return clamp(value, 0, 1);
  }

  function smootherstep(value) {
    const t = clamp01(value);
    return t * t * t * (t * (t * 6 - 15) + 10);
  }

  function cleanText(value) {
    return String(value == null ? '' : value).replace(/\s+/g, ' ').trim();
  }

  function finiteNumber(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }

  function validHttpsUrl(value) {
    try {
      const url = new URL(String(value));
      return url.protocol === 'https:' ? url : null;
    } catch (_) {
      return null;
    }
  }

  function isEsaHubbleHost(hostname) {
    const host = String(hostname || '').toLowerCase();
    return host === 'esahubble.org' || host.endsWith('.esahubble.org');
  }

  function rejectNonObservationLabel(value) {
    const text = cleanText(value).toLowerCase();
    return /\b(artwork|illustration|collage|chart|simulation|diagram|artist(?:'s)? impression)\b/.test(text);
  }

  function toVector(ra, dec) {
    const r = Number(ra) * Math.PI / 180;
    const d = Number(dec) * Math.PI / 180;
    return [
      Math.cos(d) * Math.cos(r),
      Math.cos(d) * Math.sin(r),
      Math.sin(d)
    ];
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
    return Math.acos(clamp(
      va[0] * vb[0] + va[1] * vb[1] + va[2] * vb[2],
      -1,
      1
    ));
  }

  function routeDistanceMillionLy(source, destination) {
    const dA = finiteNumber(source && source.distance);
    const dB = finiteNumber(destination && destination.distance);

    if (dA != null && dA > 0 && dB != null && dB > 0) {
      const theta = angularSeparationRadians(source, destination);
      return {
        value: Math.sqrt(Math.max(
          0,
          dA * dA + dB * dB - 2 * dA * dB * Math.cos(theta)
        )),
        exactRoute: true
      };
    }

    return {
      value: dB != null && dB > 0 ? dB : 0,
      exactRoute: false
    };
  }

  function scaledDistance(millionLy) {
    let value = finiteNumber(millionLy);
    value = value == null || value < 0 ? 0 : value;

    if (value < 1) {
      return { value: value * 1_000_000, unit: 'LIGHT-YEARS' };
    }

    if (value < 1000) {
      return { value, unit: 'MILLION LIGHT-YEARS' };
    }

    return { value: value / 1000, unit: 'BILLION LIGHT-YEARS' };
  }

  function formatDistanceText(millionLy) {
    const scaled = scaledDistance(millionLy);
    return `${scaled.value.toFixed(2)} ${scaled.unit}`;
  }

  function createMeasureCanvas() {
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 256;
    canvas.hidden = true;
    return canvas;
  }

  function scanGlyphWidth(ctx, canvas, text, font, size) {
    const scale = 4;
    const width = 1024;
    const height = 256;

    canvas.width = width;
    canvas.height = height;
    ctx.clearRect(0, 0, width, height);

    ctx.save();
    ctx.scale(scale, scale);
    ctx.font = `400 ${size}px "${font}"`;
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#fff';
    ctx.fillText(text, 32, 48);
    ctx.restore();

    const data = ctx.getImageData(0, 0, width, height).data;
    let min = width;
    let max = -1;

    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        if (data[(y * width + x) * 4 + 3] > 24) {
          if (x < min) min = x;
          if (x > max) max = x;
        }
      }
    }

    return max < min ? 0 : (max - min + 1) / scale;
  }

  async function ensureFonts() {
    if (fontsPromise) return fontsPromise;

    fontsPromise = (async () => {
      const faces = [
        new FontFace(
          FONT_NAMES.spaceAge,
          `url("${FONT_URLS.spaceAge}")`,
          { style: 'normal', weight: '400' }
        ),
        new FontFace(
          FONT_NAMES.digits,
          `url("${FONT_URLS.digits}")`,
          { style: 'normal', weight: '400' }
        )
      ];

      const loaded = await Promise.all(faces.map((face) => face.load()));
      loaded.forEach((face) => document.fonts.add(face));

      await Promise.all([
        document.fonts.load(`400 12px "${FONT_NAMES.spaceAge}"`, 'DISTANCE TO EARTH CONSTELLATION VIEW HUBBLE HD'),
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
      this.canvas = createMeasureCanvas();
      this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });
      this.metrics = null;
      this.integerCells = [];
      this.fractionCells = [];
      this.decimalCell = null;
      this.unitEl = null;
      this.root = this.#build();
      this.host.replaceChildren(this.root, this.canvas);
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
      number.appendChild(decimal);
      this.decimalCell = decimal;

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

      let widest = 0;
      for (const character of '0123456789') {
        widest = Math.max(
          widest,
          scanGlyphWidth(this.ctx, this.canvas, character, FONT_NAMES.digits, 18)
        );
      }

      const digitWidth = Math.ceil(widest) + 2;
      const decimalWidth = Math.ceil(
        scanGlyphWidth(this.ctx, this.canvas, '.', FONT_NAMES.digits, 18)
      ) + 3;

      [...this.integerCells, ...this.fractionCells].forEach((cell) => {
        cell.style.width = `${digitWidth}px`;
      });

      this.decimalCell.style.width = `${decimalWidth}px`;
      this.metrics = { digitWidth, decimalWidth };
      this.render(0);
    }

    render(millionLy) {
      const scaled = scaledDistance(millionLy);
      const safe = clamp(scaled.value, 0, 999999.99);
      const [integerPart, fractionPart = ''] = safe
        .toFixed(this.fractionSlots)
        .split('.');

      const integer = integerPart
        .padStart(this.integerSlots, ' ')
        .slice(-this.integerSlots);

      const fraction = fractionPart
        .padEnd(this.fractionSlots, '0')
        .slice(0, this.fractionSlots);

      this.integerCells.forEach((cell, index) => {
        const character = integer[index];
        cell.textContent = character === ' ' ? '0' : character;
        cell.style.visibility = character === ' ' ? 'hidden' : 'visible';
      });

      this.fractionCells.forEach((cell, index) => {
        cell.textContent = fraction[index];
      });

      this.unitEl.textContent = scaled.unit;
      this.root.setAttribute(
        'aria-label',
        `${safe.toFixed(this.fractionSlots)} ${scaled.unit}`
      );
    }
  }

  class GalaxyRandomGalaxy {
    constructor(options = {}) {
      const aladin = options.aladin;
      const host = options.host;

      if (!aladin) {
        throw new TypeError('GalaxyRandomGalaxy requires an Aladin instance.');
      }

      if (!(host instanceof Element)) {
        throw new TypeError('GalaxyRandomGalaxy requires a DOM Element host.');
      }

      if (instances.has(host)) {
        throw new Error('GalaxyRandomGalaxy is already mounted on this host.');
      }

      this.options = { ...DEFAULTS, ...options };
      this.aladin = aladin;
      this.host = host;
      this.randomButton = options.randomButton instanceof Element
        ? options.randomButton
        : null;
      this.hubbleProvider = typeof options.hubbleProvider === 'function'
        ? options.hubbleProvider
        : null;
      this.geminiProvider = typeof options.geminiProvider === 'function'
        ? options.geminiProvider
        : null;

      this.destroyed = false;
      this.busy = false;
      this.arrived = true;
      this.activeDestination = null;
      this.lastGeminiEnrichment = null;
      this.prefetchedDestination = null;
      this.prefetchPromise = null;
      this.hdOpen = false;
      this.currentGalaxy = this.#initialCurrent(options.currentGalaxy);
      this.onStatus = typeof options.onStatus === 'function' ? options.onStatus : null;
      this.onArrival = typeof options.onArrival === 'function' ? options.onArrival : null;
      this.onError = typeof options.onError === 'function' ? options.onError : null;

      this.root = this.#build();
      this.host.appendChild(this.root);
      this.distanceRenderer = new FixedDistanceRenderer(
        this.distanceNumberHost,
        this.options
      );

      this._randomClick = () => {
        this.travelToRandom().catch((error) => this.#handleError(error));
      };

      this._hdClick = () => this.showHubbleHD();
      this._backClick = () => this.backToSky();

      if (this.randomButton) {
        this.randomButton.addEventListener('click', this._randomClick);
      }

      this.viewHdButton.addEventListener('click', this._hdClick);
      this.backButton.addEventListener('click', this._backClick);

      instances.set(this.host, this);
      this.ready = this.#initialize();
    }

    #initialCurrent(currentGalaxy) {
      const coords = this.aladin.getRaDec ? this.aladin.getRaDec() : [0, 0];
      const supplied = currentGalaxy && typeof currentGalaxy === 'object'
        ? currentGalaxy
        : {};

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
.gvrg-root{
  position:absolute;inset:0;z-index:9990;pointer-events:none;
  font-family:"${FONT_NAMES.spaceAge}",sans-serif;color:#eefaff
}
.gvrg-distance{
  position:absolute;left:50%;top:66.7%;transform:translate(-50%,-50%);
  width:min(430px,92%);padding:8px 10px 9px;border:1px solid rgba(175,225,255,.76);
  border-radius:5px;background:rgba(0,8,16,.80);box-shadow:0 0 13px rgba(90,195,255,.23);
  text-align:center;opacity:0;transition:opacity .20s linear
}
.gvrg-distance-label{
  height:12px;font:400 7px/12px "${FONT_NAMES.spaceAge}",sans-serif;
  letter-spacing:2px;color:#79a9c0
}
.gvrg-distance-number{
  display:flex;align-items:center;justify-content:center;gap:8px;
  height:25px;white-space:nowrap;overflow:hidden
}
.gvrg-number-cells{display:inline-flex;align-items:baseline;justify-content:flex-end;flex:none}
.gvrg-digit-cell,.gvrg-decimal-cell{
  display:inline-flex;align-items:center;justify-content:center;flex:none;
  height:23px;font:400 18px/23px "${FONT_NAMES.digits}",sans-serif;
  transform:scaleY(1.08);transform-origin:center
}
.gvrg-distance-unit{
  display:inline-flex;align-items:center;width:158px;height:23px;overflow:hidden;
  font:400 8px/23px "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.7px;
  color:#d9f4ff;text-align:left;white-space:nowrap
}
.gvrg-route{
  height:12px;font:400 7px/12px "${FONT_NAMES.spaceAge}",sans-serif;
  letter-spacing:1px;color:#7da6b9;white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.gvrg-card{
  position:absolute;left:50%;top:78%;transform:translate(-50%,-50%);
  width:min(510px,88%);padding:10px 13px;border:1px solid rgba(175,225,255,.72);
  border-radius:6px;background:rgba(0,8,17,.86);box-shadow:0 0 13px rgba(80,190,255,.20);
  opacity:0;transition:opacity .28s ease;pointer-events:none
}
.gvrg-card-visible{opacity:1;pointer-events:auto}
.gvrg-name{
  font:400 16px/1.15 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1.3px;
  color:#fff;text-shadow:0 0 7px rgba(145,220,255,.50);margin-bottom:7px
}
.gvrg-row{
  display:grid;grid-template-columns:minmax(110px,auto) 1fr;gap:8px;align-items:baseline;
  margin-top:4px
}
.gvrg-label{
  font:400 7px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1.15px;color:#82b9d4
}
.gvrg-value{
  min-width:0;font:400 9px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;
  letter-spacing:.7px;color:#e9f9ff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis
}
.gvrg-card-distance{display:flex;align-items:baseline;gap:6px;min-width:0}
.gvrg-value-number{
  font:400 10px/1.4 "${FONT_NAMES.digits}",sans-serif;letter-spacing:0
}
.gvrg-value-unit{
  font:400 8px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:.55px
}
.gvrg-actions{display:flex;gap:7px;align-items:center;margin-top:9px;pointer-events:auto}
.gvrg-button{
  appearance:none;border:1px solid rgba(175,225,255,.84);border-radius:4px;
  background:rgba(7,27,42,.95);color:#effbff;padding:7px 10px;
  font:400 8px/1 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;cursor:pointer
}
.gvrg-button:disabled{opacity:.45;cursor:default}
.gvrg-hd{
  position:absolute;inset:0;display:none;z-index:20;background:#000;pointer-events:auto
}
.gvrg-hd-open{display:block}
.gvrg-hd img{
  position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000
}
.gvrg-hd-footer{
  position:absolute;left:0;right:0;bottom:0;padding:24px 10px 10px;
  background:linear-gradient(transparent,rgba(0,0,0,.94));text-align:center
}
.gvrg-credit{
  margin-bottom:7px;font:400 7px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;
  letter-spacing:.5px;color:#d8eff9
}
.gvrg-hd-loading{
  position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  font:400 9px/1.4 "${FONT_NAMES.spaceAge}",sans-serif;letter-spacing:1px;color:#dff7ff
}`;
      return style;
    }

    #build() {
      const root = document.createElement('div');
      root.className = 'gvrg-root';
      root.setAttribute('data-gvrg-version', VERSION);

      const style = this.#style();

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

      distance.append(distanceLabel, distanceNumberHost, route);

      const card = document.createElement('div');
      card.className = 'gvrg-card';
      this.card = card;

      const name = document.createElement('div');
      name.className = 'gvrg-name';
      this.nameEl = name;

      const distanceRow = document.createElement('div');
      distanceRow.className = 'gvrg-row';

      const distanceKey = document.createElement('div');
      distanceKey.className = 'gvrg-label';
      distanceKey.textContent = 'DISTANCE TO EARTH';

      const distanceValue = document.createElement('div');
      distanceValue.className = 'gvrg-value gvrg-card-distance';

      const distanceNumber = document.createElement('span');
      distanceNumber.className = 'gvrg-value-number';
      this.distanceValueNumberEl = distanceNumber;

      const distanceUnit = document.createElement('span');
      distanceUnit.className = 'gvrg-value-unit';
      this.distanceValueUnitEl = distanceUnit;

      distanceValue.append(distanceNumber, distanceUnit);
      distanceRow.append(distanceKey, distanceValue);

      const constellationRow = document.createElement('div');
      constellationRow.className = 'gvrg-row';

      const constellationKey = document.createElement('div');
      constellationKey.className = 'gvrg-label';
      constellationKey.textContent = 'CONSTELLATION';

      const constellationValue = document.createElement('div');
      constellationValue.className = 'gvrg-value';
      this.constellationValueEl = constellationValue;

      constellationRow.append(constellationKey, constellationValue);

      const actions = document.createElement('div');
      actions.className = 'gvrg-actions';

      const viewHd = document.createElement('button');
      viewHd.type = 'button';
      viewHd.className = 'gvrg-button';
      viewHd.textContent = 'VIEW HUBBLE HD';
      this.viewHdButton = viewHd;

      actions.appendChild(viewHd);
      card.append(name, distanceRow, constellationRow, actions);

      const hd = document.createElement('div');
      hd.className = 'gvrg-hd';
      this.hdOverlay = hd;

      const hdImage = document.createElement('img');
      hdImage.alt = '';
      this.hdImage = hdImage;

      const loading = document.createElement('div');
      loading.className = 'gvrg-hd-loading';
      loading.textContent = 'LOADING HUBBLE HD';
      this.hdLoading = loading;

      const footer = document.createElement('div');
      footer.className = 'gvrg-hd-footer';

      const credit = document.createElement('div');
      credit.className = 'gvrg-credit';
      this.creditEl = credit;

      const back = document.createElement('button');
      back.type = 'button';
      back.className = 'gvrg-button';
      back.textContent = 'BACK TO SKY';
      this.backButton = back;

      footer.append(credit, back);
      hd.append(hdImage, loading, footer);

      root.append(style, distance, card, hd);
      return root;
    }

    async #initialize() {
      await ensureFonts();
      await this.distanceRenderer.calibrate();

      if (this.options.prefetch) {
        this.prefetch().catch(() => {});
      }

      this.#setStatus('READY');
      return this;
    }

    #setStatus(message) {
      const text = cleanText(message);
      if (this.onStatus) this.onStatus(text, this);
    }

    #handleError(error) {
      const normalized = error instanceof Error ? error : new Error(String(error));
      this.#setStatus(`ERROR ${normalized.message}`);
      if (this.onError) {
        this.onError(normalized, this);
        return;
      }
      console.error('[GalaxyRandomGalaxy]', normalized);
    }

    async #fetchJsonEndpoint(endpoint, payload, method = 'POST') {
      if (!endpoint) {
        throw new Error('No endpoint configured.');
      }

      const response = await fetch(endpoint, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: method === 'GET' ? undefined : JSON.stringify(payload || {})
      });

      if (!response.ok) {
        throw new Error(`Endpoint returned HTTP ${response.status}.`);
      }

      return response.json();
    }

    async #getHubbleCandidate(excludeName) {
      let raw;

      if (this.hubbleProvider) {
        raw = await this.hubbleProvider({
          excludeName: cleanText(excludeName),
          module: this
        });
      } else {
        raw = await this.#fetchJsonEndpoint(
          this.options.hubbleEndpoint,
          { excludeName: cleanText(excludeName) }
        );
      }

      const candidate = raw && raw.destination ? raw.destination : raw;
      return this.#normalizeHubbleCandidate(candidate);
    }

    #normalizeHubbleCandidate(candidate) {
      if (!candidate || typeof candidate !== 'object') {
        throw new Error('Hubble provider returned no destination.');
      }

      const name = cleanText(candidate.name || candidate.objectName);
      const ra = finiteNumber(candidate.ra);
      const dec = finiteNumber(candidate.dec);
      const distance = finiteNumber(
        candidate.distance ?? candidate.distanceMly ?? candidate.distance_mly
      );
      const constellation = cleanText(candidate.constellation);
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
      if (!hdUrl || !isEsaHubbleHost(hdUrl.hostname)) {
        throw new Error('Hubble destination has no verified ESA/Hubble HD asset.');
      }
      if (!sourceUrl || !isEsaHubbleHost(sourceUrl.hostname)) {
        throw new Error('Hubble destination has no verified ESA/Hubble source page.');
      }
      if (imageType && rejectNonObservationLabel(imageType)) {
        throw new Error('Rejected non-observation Hubble entry.');
      }
      if (category && !/galax/i.test(category)) {
        throw new Error('Rejected non-galaxy Hubble entry.');
      }
      if (telescope && !/hubble/i.test(telescope)) {
        throw new Error('Rejected entry without Hubble telescope data.');
      }

      return Object.freeze({
        source: 'HUBBLE',
        hubble: true,
        name,
        ra,
        dec,
        distance,
        constellation,
        fov: clamp(fov, 0.05, 8),
        hdUrl: hdUrl.href,
        sourceUrl: sourceUrl.href,
        credit,
        imageType,
        category,
        telescope
      });
    }

    async prefetch() {
      if (this.destroyed) return null;
      if (this.prefetchedDestination) return this.prefetchedDestination;
      if (this.prefetchPromise) return this.prefetchPromise;

      const excludeName = this.currentGalaxy && this.currentGalaxy.name;

      this.prefetchPromise = this.#getHubbleCandidate(excludeName)
        .then((destination) => {
          this.prefetchedDestination = destination;
          return destination;
        })
        .finally(() => {
          this.prefetchPromise = null;
        });

      return this.prefetchPromise;
    }

    async #consumeDestination() {
      if (this.prefetchedDestination) {
        const destination = this.prefetchedDestination;
        this.prefetchedDestination = null;
        return destination;
      }

      if (this.prefetchPromise) {
        const destination = await this.prefetchPromise;
        this.prefetchedDestination = null;
        return destination;
      }

      return this.#getHubbleCandidate(
        this.currentGalaxy && this.currentGalaxy.name
      );
    }

    #translationProgress(t) {
      const start = Number(this.options.translateStart);
      const ninety = Number(this.options.translate90);
      const complete = Number(this.options.translationComplete);

      if (t <= start) return 0;

      if (t <= ninety) {
        return 0.90 * smootherstep((t - start) / (ninety - start));
      }

      if (t <= complete) {
        return 0.90 + 0.10 * smootherstep((t - ninety) / (complete - ninety));
      }

      return 1;
    }

    #fovAt(t, startFov, destinationFov) {
      const turn = Number(this.options.turnPoint);
      const maximum = Number(this.options.maxFov);

      if (t <= turn) {
        const progress = smootherstep(t / turn);
        return Math.exp(
          Math.log(startFov) +
          (Math.log(maximum) - Math.log(startFov)) * progress
        );
      }

      const progress = smootherstep((t - turn) / (1 - turn));
      return Math.exp(
        Math.log(maximum) +
        (Math.log(destinationFov) - Math.log(maximum)) * progress
      );
    }

    #distanceProgress(t) {
      const turn = Number(this.options.turnPoint);
      const ninety = Number(this.options.translate90);
      const complete = Number(this.options.translationComplete);

      if (t <= turn) {
        return 0.20 * smootherstep(t / turn);
      }

      if (t <= ninety) {
        return 0.20 + 0.70 * smootherstep((t - turn) / (ninety - turn));
      }

      if (t <= complete) {
        return 0.90 + 0.08 * smootherstep((t - ninety) / (complete - ninety));
      }

      return 0.98 + 0.02 * smootherstep((t - complete) / (1 - complete));
    }

    #showDistance(source, destination, route) {
      this.routeEl.textContent = route.exactRoute
        ? `${source.name.toUpperCase()} TO ${destination.name.toUpperCase()}`
        : `TO ${destination.name.toUpperCase()}`;
      this.distanceRenderer.render(0);
      this.distanceBox.style.opacity = '1';
    }

    #hideDistance() {
      this.distanceBox.style.opacity = '0';
    }

    #hideCard() {
      this.card.classList.remove('gvrg-card-visible');
    }

    #showCard(destination) {
      this.nameEl.textContent = destination.name.toUpperCase();
      const scaled = scaledDistance(destination.distance);
      this.distanceValueNumberEl.textContent = scaled.value.toFixed(2);
      this.distanceValueUnitEl.textContent = scaled.unit;
      this.constellationValueEl.textContent = destination.constellation.toUpperCase();
      this.viewHdButton.disabled = false;
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

      let result;

      if (this.geminiProvider) {
        result = await this.geminiProvider(payload, this);
      } else {
        result = await this.#fetchJsonEndpoint(this.options.geminiEndpoint, payload);
      }

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

      let destination;

      try {
        this.#setStatus('FETCHING HUBBLE GALAXY');
        destination = await this.#consumeDestination();
        this.activeDestination = destination;
        this.#setStatus(`GALACTIC TRAVEL ${destination.name.toUpperCase()}`);

        const coords = this.aladin.getRaDec();
        const fov = this.aladin.getFov();
        const startRA = Number(coords[0]);
        const startDec = Number(coords[1]);
        const startFov = Math.max(0.02, Number(fov[0]));
        const destinationFov = Math.max(0.05, Number(destination.fov));
        const source = {
          ...this.currentGalaxy,
          ra: startRA,
          dec: startDec
        };
        const route = routeDistanceMillionLy(source, destination);

        this.#showDistance(source, destination, route);

        this.#requestGeminiEnrichment(destination)
          .then((result) => {
            if (result) {
              this.lastGeminiEnrichment = result;
            }
          })
          .catch(() => {});

        const duration = Number(this.options.travelSeconds) * 1000;
        const started = performance.now();
        let projectionState = this.options.arrivalProjection;

        await new Promise((resolve) => {
          const frame = (now) => {
            const t = Math.min(1, (now - started) / duration);
            const move = this.#translationProgress(t);
            const position = greatCirclePosition(
              startRA,
              startDec,
              destination.ra,
              destination.dec,
              move
            );

            this.aladin.gotoRaDec(position[0], position[1]);

            const currentFov = this.#fovAt(t, startFov, destinationFov);
            this.aladin.setFov(currentFov);

            if (typeof this.aladin.setProjection === 'function') {
              if (
                projectionState === this.options.arrivalProjection &&
                t < Number(this.options.turnPoint) &&
                currentFov >= Number(this.options.aitEntryFov)
              ) {
                this.aladin.setProjection(this.options.wideProjection);
                projectionState = this.options.wideProjection;
              }

              if (
                projectionState === this.options.wideProjection &&
                t > Number(this.options.turnPoint) &&
                currentFov <= Number(this.options.sinReturnFov)
              ) {
                this.aladin.setProjection(this.options.arrivalProjection);
                projectionState = this.options.arrivalProjection;
              }
            }

            this.distanceRenderer.render(
              route.value * this.#distanceProgress(t)
            );

            if (t < 1) {
              requestAnimationFrame(frame);
              return;
            }

            this.aladin.gotoRaDec(destination.ra, destination.dec);
            this.aladin.setFov(destinationFov);

            if (
              typeof this.aladin.setProjection === 'function' &&
              projectionState !== this.options.arrivalProjection
            ) {
              this.aladin.setProjection(this.options.arrivalProjection);
            }

            this.distanceRenderer.render(route.value);
            resolve();
          };

          requestAnimationFrame(frame);
        });

        this.currentGalaxy = {
          name: destination.name,
          ra: destination.ra,
          dec: destination.dec,
          distance: destination.distance
        };

        this.arrived = true;
        this.busy = false;
        this.#hideDistance();
        this.#showCard(destination);
        this.#setStatus(`ARRIVED ${destination.name.toUpperCase()}`);

        if (this.randomButton) this.randomButton.disabled = false;
        if (this.onArrival) this.onArrival(destination, this);

        if (this.options.prefetch) {
          this.prefetch().catch(() => {});
        }

        return destination;
      } catch (error) {
        this.busy = false;
        this.arrived = true;
        this.#hideDistance();
        if (this.randomButton) this.randomButton.disabled = false;
        throw error;
      }
    }

    async random() {
      return this.travelToRandom();
    }

    showHubbleHD() {
      const destination = this.activeDestination;

      if (!destination || !destination.hubble || !destination.hdUrl) {
        throw new Error('No Hubble HD image is available for the active destination.');
      }

      this.hdImage.removeAttribute('src');
      this.hdImage.alt = destination.name;
      this.hdLoading.textContent = 'LOADING HUBBLE HD';
      this.hdLoading.style.display = 'block';
      this.creditEl.textContent = `CREDIT ${destination.credit || 'ESA/Hubble'}`;
      this.hdOverlay.classList.add('gvrg-hd-open');
      this.hdOpen = true;

      this.hdImage.onload = () => {
        this.hdLoading.style.display = 'none';
      };

      this.hdImage.onerror = () => {
        this.hdLoading.textContent = 'HUBBLE HD IMAGE COULD NOT LOAD';
      };

      this.hdImage.src = destination.hdUrl;
      return destination.hdUrl;
    }

    backToSky() {
      if (!this.hdOpen) return;

      this.hdOverlay.classList.remove('gvrg-hd-open');
      this.hdImage.removeAttribute('src');
      this.hdImage.onload = null;
      this.hdImage.onerror = null;
      this.hdOpen = false;

      if (this.activeDestination) {
        this.aladin.gotoRaDec(
          this.activeDestination.ra,
          this.activeDestination.dec
        );
        this.aladin.setFov(this.activeDestination.fov);
      }
    }

    async enrichWithGemini(destination = this.activeDestination) {
      if (!destination) return null;
      return this.#requestGeminiEnrichment(destination);
    }

    setCurrentGalaxy(currentGalaxy) {
      if (!currentGalaxy || typeof currentGalaxy !== 'object') {
        throw new TypeError('setCurrentGalaxy requires a galaxy object.');
      }

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
        currentGalaxy: { ...this.currentGalaxy },
        activeDestination: this.activeDestination,
        prefetched: Boolean(this.prefetchedDestination),
        hubbleOnly: true,
        digitFont: FONT_URLS.digits,
        geminiKeyEmbedded: false
      };
    }

    destroy() {
      if (this.destroyed) return;

      this.destroyed = true;

      if (this.randomButton) {
        this.randomButton.removeEventListener('click', this._randomClick);
      }

      this.viewHdButton.removeEventListener('click', this._hdClick);
      this.backButton.removeEventListener('click', this._backClick);
      this.hdImage.removeAttribute('src');
      this.root.remove();
      instances.delete(this.host);
    }

    static mount(host, options = {}) {
      const existing = instances.get(host);
      if (existing && !existing.destroyed) return existing;

      return new GalaxyRandomGalaxy({
        ...options,
        host
      });
    }
  }

  GalaxyRandomGalaxy.VERSION = VERSION;
  GalaxyRandomGalaxy.FONT_URLS = FONT_URLS;
  GalaxyRandomGalaxy.DEFAULTS = DEFAULTS;
  GalaxyRandomGalaxy.PROVIDER_CONTRACT = Object.freeze({
    hubbleEndpoint: {
      method: 'POST',
      request: {
        excludeName: 'optional previous destination name'
      },
      response: {
        destination: {
          name: 'required',
          ra: 'required ICRS degrees',
          dec: 'required ICRS degrees',
          distanceMly: 'required positive million light-years',
          constellation: 'required',
          fov: 'optional degrees',
          hdUrl: 'required https://cdn.esahubble.org/... image',
          sourceUrl: 'required https://esahubble.org/images/.../',
          credit: 'required/preferred',
          imageType: 'Observation preferred',
          category: 'Galaxies preferred',
          telescope: 'Hubble Space Telescope preferred'
        }
      }
    },
    geminiEndpoint: {
      method: 'POST',
      secretRule: 'Store GEMINI_API_KEY server-side only. Never place it in this JavaScript module.',
      modelHint: 'Gemini Flash-Lite'
    }
  });

  global.GalaxyRandomGalaxy = GalaxyRandomGalaxy;
})(window);
