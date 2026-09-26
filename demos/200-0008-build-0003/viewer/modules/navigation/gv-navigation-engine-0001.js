/*
 * GALAXY VIEWER — NAVIGATION ENGINE 0001
 *
 * Standalone implementation of:
 * viewer/modules/navigation/GALAXY-VIEWER-RANDOM-NAVIGATION-TRAVEL-ENGINE-SPECIFICATION.txt
 *
 * This module owns route planning mathematics and parametric travel choreography.
 * It deliberately does NOT download catalogs/assets, decode images, mutate archive
 * state, or own existing Random Galaxy history/provider/preparation systems.
 */
(function (global) {
  'use strict';

  const VERSION = '0001';

  const DEFAULTS = Object.freeze({
    planningPoolSize: 100,
    skyTargetMinDeg: 60,
    skyTargetMaxDeg: 130,
    rotationTargetDeg: 90,
    rotationFallback1Deg: 105,
    rotationFallback2Deg: 120,
    rotationAbsoluteMaxDeg: 180,
    prefetchTarget: 10,
    prefetchPriorityLevel: 5,
    prefetchEmergencyLevel: 3,
    nextPlanTrigger: 10,
    totalTravelTimeSec: 20,
    translationStartU: 0.20,
    translationEndU: 0.80,
    rotationStartU: 0.25,
    rotationEndU: 0.75,
    zoomOutPrimaryEndU: 0.33,
    zoomInPrimaryStartU: 0.67,
    birdseyeFovDeg: 237.6,
    routeTargetDeg: 107,
    routeOptimizationPasses: 8,
    routeSearchRestarts: 30,
    spatialRelaxMinDeg: 45,
    spatialRelaxMaxDeg: 145,
    randomTieTolerance: 0.02,
    animationEnabled: true
  });

  const STATES = Object.freeze({
    IDLE: 'IDLE',
    ENSURE_FUTURE: 'ENSURE_FUTURE',
    READY: 'READY',
    CLAIMED: 'CLAIMED',
    TRAVELING: 'TRAVELING',
    ARRIVED: 'ARRIVED',
    COMMITTED: 'COMMITTED'
  });

  const CONSTRAINT_LEVELS = Object.freeze({
    NORMAL: 0,
    ROTATION_CUSHION: 1,
    ROTATION_RELAXATION: 2,
    SPATIAL_RELAXATION: 3,
    LAST_RESORT: 4
  });

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, Number(value)));
  }

  function clamp01(value) {
    return clamp(value, 0, 1);
  }

  function finiteNumber(value) {
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  }

  function normalize360(value) {
    const n = finiteNumber(value);
    if (n === null) return 0;
    return ((n % 360) + 360) % 360;
  }

  function parseOrientation(value) {
    if (value === null || value === undefined || value === '') return 0;
    if (typeof value === 'number') return normalize360(value);

    const text = String(value).trim();
    if (!text) return 0;
    if (/^north\s+is\s+up$/i.test(text) || /^north[- ]?up$/i.test(text)) return 0;

    const numeric = text.match(/^([+-]?\d+(?:\.\d+)?)\s*°?$/);
    if (numeric) return normalize360(Number(numeric[1]));

    const directional = text.match(/north\s+is\s+([0-9]+(?:\.[0-9]+)?)\s*°?\s*(right|left)\s+of\s+vertical/i);
    if (directional) {
      const magnitude = Number(directional[1]);
      return normalize360(directional[2].toLowerCase() === 'left' ? -magnitude : magnitude);
    }

    return 0;
  }

  function shortestRotationSigned(fromDeg, toDeg) {
    const a = normalize360(fromDeg);
    const b = normalize360(toDeg);
    let delta = ((b - a + 540) % 360) - 180;
    if (delta === -180) delta = 180;
    return delta;
  }

  function shortestRotationDistance(fromDeg, toDeg) {
    return Math.abs(shortestRotationSigned(fromDeg, toDeg));
  }

  function degToRad(value) {
    return Number(value) * Math.PI / 180;
  }

  function radToDeg(value) {
    return Number(value) * 180 / Math.PI;
  }

  function toVector(raDeg, decDeg) {
    const ra = degToRad(raDeg);
    const dec = degToRad(decDeg);
    const c = Math.cos(dec);
    return [c * Math.cos(ra), c * Math.sin(ra), Math.sin(dec)];
  }

  function vectorToRaDec(vector) {
    const x = Number(vector[0]);
    const y = Number(vector[1]);
    const z = Number(vector[2]);
    return Object.freeze({
      ra: normalize360(radToDeg(Math.atan2(y, x))),
      dec: radToDeg(Math.atan2(z, Math.sqrt(x * x + y * y)))
    });
  }

  function greatCircleDistanceDeg(a, b) {
    const va = toVector(a.ra, a.dec);
    const vb = toVector(b.ra, b.dec);
    const dot = clamp(va[0] * vb[0] + va[1] * vb[1] + va[2] * vb[2], -1, 1);
    return radToDeg(Math.acos(dot));
  }

  function greatCirclePosition(a, b, progress) {
    const p = clamp01(progress);
    const va = toVector(a.ra, a.dec);
    const vb = toVector(b.ra, b.dec);
    const dot = clamp(va[0] * vb[0] + va[1] * vb[1] + va[2] * vb[2], -1, 1);
    const omega = Math.acos(dot);
    const sinOmega = Math.sin(omega);

    if (Math.abs(sinOmega) < 1e-8) {
      const dra = ((Number(b.ra) - Number(a.ra) + 540) % 360) - 180;
      return Object.freeze({
        ra: normalize360(Number(a.ra) + dra * p),
        dec: Number(a.dec) + (Number(b.dec) - Number(a.dec)) * p
      });
    }

    const s0 = Math.sin((1 - p) * omega) / sinOmega;
    const s1 = Math.sin(p * omega) / sinOmega;
    return vectorToRaDec([
      va[0] * s0 + vb[0] * s1,
      va[1] * s0 + vb[1] * s1,
      va[2] * s0 + vb[2] * s1
    ]);
  }

  function smootherstep(value) {
    const t = clamp01(value);
    return t * t * t * (t * (t * 6 - 15) + 10);
  }

  function windowProgress(u, start, end) {
    if (u <= start) return 0;
    if (u >= end) return 1;
    return smootherstep((u - start) / (end - start));
  }

  function logInterpolate(a, b, progress) {
    const x = finiteNumber(a);
    const y = finiteNumber(b);
    if (x === null || y === null || x <= 0 || y <= 0) {
      throw new Error('FOV values must be finite and greater than zero');
    }
    return Math.exp(Math.log(x) + (Math.log(y) - Math.log(x)) * clamp01(progress));
  }

  function mulberry32(seed) {
    let state = Number(seed) >>> 0;
    return function random() {
      state += 0x6D2B79F5;
      let t = state;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function destinationKey(record) {
    return String(
      record?.destinationKey ?? record?.key ?? record?.archiveId ?? record?.id ?? record?.name ?? ''
    ).trim().toLowerCase();
  }

  function normalizeDestination(record) {
    if (!record || typeof record !== 'object') throw new TypeError('Destination must be an object');
    const key = destinationKey(record);
    const ra = finiteNumber(record.ra);
    const dec = finiteNumber(record.dec);
    const fov = finiteNumber(record.fov ?? record.fieldOfView ?? record.fieldOfViewDegrees);

    if (!key) throw new Error('Destination key is required');
    if (ra === null || ra < 0 || ra >= 360) throw new Error(`Invalid RA for ${key}`);
    if (dec === null || dec < -90 || dec > 90) throw new Error(`Invalid Dec for ${key}`);
    if (fov === null || fov <= 0) throw new Error(`Invalid FOV for ${key}`);

    const orientation = parseOrientation(
      record.orientation ?? record.aladinRotation ?? record.rotation ?? 0
    );

    return Object.freeze({
      ...record,
      destinationKey: key,
      ra,
      dec,
      fov,
      orientation,
      provider: String(record.provider ?? ''),
      hdIdentity: record.hdIdentity ?? record.hdUrl ?? record.selectedImageUrl ?? record.githubImageUrl ?? null
    });
  }

  function sampleUnique(records, size, random = Math.random) {
    const unique = [];
    const seen = new Set();
    for (const record of records || []) {
      const normalized = normalizeDestination(record);
      if (seen.has(normalized.destinationKey)) continue;
      seen.add(normalized.destinationKey);
      unique.push(normalized);
    }

    for (let i = unique.length - 1; i > 0; i -= 1) {
      const j = Math.floor(random() * (i + 1));
      const tmp = unique[i];
      unique[i] = unique[j];
      unique[j] = tmp;
    }

    return unique.slice(0, Math.min(Number(size) || 0, unique.length));
  }

  function buildMatrices(records) {
    const n = records.length;
    const sky = Array.from({ length: n }, () => new Float64Array(n));
    const rotation = Array.from({ length: n }, () => new Float64Array(n));
    const fovRatio = Array.from({ length: n }, () => new Float64Array(n));

    for (let i = 0; i < n; i += 1) {
      for (let j = i + 1; j < n; j += 1) {
        const d = greatCircleDistanceDeg(records[i], records[j]);
        const r = shortestRotationDistance(records[i].orientation, records[j].orientation);
        const f = Math.max(records[i].fov, records[j].fov) / Math.min(records[i].fov, records[j].fov);
        sky[i][j] = sky[j][i] = d;
        rotation[i][j] = rotation[j][i] = r;
        fovRatio[i][j] = fovRatio[j][i] = f;
      }
      fovRatio[i][i] = 1;
    }

    return Object.freeze({ sky, rotation, fovRatio });
  }

  function constraintForLevel(config, level) {
    switch (level) {
      case CONSTRAINT_LEVELS.NORMAL:
        return { minSky: config.skyTargetMinDeg, maxSky: config.skyTargetMaxDeg, maxRotation: config.rotationTargetDeg };
      case CONSTRAINT_LEVELS.ROTATION_CUSHION:
        return { minSky: config.skyTargetMinDeg, maxSky: config.skyTargetMaxDeg, maxRotation: config.rotationFallback1Deg };
      case CONSTRAINT_LEVELS.ROTATION_RELAXATION:
        return { minSky: config.skyTargetMinDeg, maxSky: config.skyTargetMaxDeg, maxRotation: config.rotationFallback2Deg };
      case CONSTRAINT_LEVELS.SPATIAL_RELAXATION:
        return { minSky: config.spatialRelaxMinDeg, maxSky: config.spatialRelaxMaxDeg, maxRotation: config.rotationFallback2Deg };
      default:
        return { minSky: 0, maxSky: 180, maxRotation: config.rotationAbsoluteMaxDeg };
    }
  }

  function edgeLegal(matrices, i, j, constraint) {
    const d = matrices.sky[i][j];
    const r = matrices.rotation[i][j];
    return d >= constraint.minSky && d <= constraint.maxSky && r <= constraint.maxRotation;
  }

  function routeStats(route, records, matrices, level) {
    const skyLegs = [];
    const rotationLegs = [];
    for (let k = 1; k < route.length; k += 1) {
      skyLegs.push(matrices.sky[route[k - 1]][route[k]]);
      rotationLegs.push(matrices.rotation[route[k - 1]][route[k]]);
    }

    function summary(values) {
      if (!values.length) return Object.freeze({ min: 0, mean: 0, median: 0, max: 0, sigma: 0 });
      const sorted = [...values].sort((a, b) => a - b);
      const mean = values.reduce((a, b) => a + b, 0) / values.length;
      const variance = values.reduce((sum, value) => sum + (value - mean) ** 2, 0) / values.length;
      const mid = Math.floor(sorted.length / 2);
      const median = sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
      return Object.freeze({ min: sorted[0], mean, median, max: sorted[sorted.length - 1], sigma: Math.sqrt(variance) });
    }

    return Object.freeze({
      constraintLevel: level,
      sky: summary(skyLegs),
      rotation: summary(rotationLegs),
      routeKeys: Object.freeze(route.map(index => records[index].destinationKey))
    });
  }

  function routeCost(route, matrices, config, level) {
    if (route.length < 2) return Infinity;
    const constraint = constraintForLevel(config, level);
    const distances = [];
    let rotationCost = 0;
    let fovCost = 0;
    let fallbackPenalty = level * 1e6;

    for (let i = 1; i < route.length; i += 1) {
      const a = route[i - 1];
      const b = route[i];
      if (!edgeLegal(matrices, a, b, constraint)) return Infinity;
      const d = matrices.sky[a][b];
      distances.push(d);
      rotationCost += matrices.rotation[a][b] / Math.max(1, constraint.maxRotation);
      fovCost += Math.abs(Math.log(Math.max(1e-9, matrices.fovRatio[a][b])));
    }

    const mean = distances.reduce((a, b) => a + b, 0) / distances.length;
    const variance = distances.reduce((sum, d) => sum + (d - mean) ** 2, 0) / distances.length;
    const centerPenalty = Math.abs(mean - config.routeTargetDeg);
    return fallbackPenalty + variance * 100 + centerPenalty * 25 + rotationCost * 4 + fovCost;
  }

  function nodeDegrees(matrices, remaining, constraint) {
    const degree = new Map();
    for (const i of remaining) {
      let count = 0;
      for (const j of remaining) if (i !== j && edgeLegal(matrices, i, j, constraint)) count += 1;
      degree.set(i, count);
    }
    return degree;
  }

  function constructRoute(records, matrices, config, level, random, anchorIndex = null) {
    const constraint = constraintForLevel(config, level);
    const all = new Set(records.map((_, index) => index));
    const route = [];

    let current;
    if (anchorIndex !== null && all.has(anchorIndex)) {
      current = anchorIndex;
    } else {
      const degree = nodeDegrees(matrices, all, constraint);
      const sorted = [...all].sort((a, b) => (degree.get(a) - degree.get(b)) || (random() - 0.5));
      current = sorted[0];
    }

    route.push(current);
    all.delete(current);

    while (all.size) {
      const degree = nodeDegrees(matrices, all, constraint);
      const candidates = [...all].filter(index => edgeLegal(matrices, current, index, constraint));
      if (!candidates.length) return null;

      let bestScore = Infinity;
      let near = [];

      for (const candidate of candidates) {
        const d = matrices.sky[current][candidate];
        const r = matrices.rotation[current][candidate];
        const f = Math.abs(Math.log(Math.max(1e-9, matrices.fovRatio[current][candidate])));
        const difficulty = degree.get(candidate) ?? 0;
        const score =
          Math.abs(d - config.routeTargetDeg) * 1.0 +
          r * 0.08 +
          f * 2.5 +
          difficulty * 0.15;

        if (score < bestScore) {
          bestScore = score;
          near = [candidate];
        } else if (score <= bestScore * (1 + config.randomTieTolerance)) {
          near.push(candidate);
        }
      }

      const chosen = near[Math.floor(random() * near.length)] ?? candidates[0];
      route.push(chosen);
      all.delete(chosen);
      current = chosen;
    }

    return route;
  }

  function optimizeRoute(route, matrices, config, level, random) {
    let best = [...route];
    let bestCost = routeCost(best, matrices, config, level);

    for (let pass = 0; pass < config.routeOptimizationPasses; pass += 1) {
      let improved = false;

      for (let trial = 0; trial < Math.max(20, best.length * 2); trial += 1) {
        const a = 1 + Math.floor(random() * Math.max(1, best.length - 2));
        const b = 1 + Math.floor(random() * Math.max(1, best.length - 2));
        if (a === b) continue;
        const candidate = [...best];
        const tmp = candidate[a];
        candidate[a] = candidate[b];
        candidate[b] = tmp;
        const cost = routeCost(candidate, matrices, config, level);
        if (cost < bestCost) {
          best = candidate;
          bestCost = cost;
          improved = true;
        }
      }

      for (let trial = 0; trial < Math.max(20, best.length); trial += 1) {
        let a = 1 + Math.floor(random() * Math.max(1, best.length - 3));
        let b = a + 1 + Math.floor(random() * Math.max(1, best.length - a - 1));
        if (b >= best.length) b = best.length - 1;
        const candidate = best.slice(0, a).concat(best.slice(a, b + 1).reverse(), best.slice(b + 1));
        const cost = routeCost(candidate, matrices, config, level);
        if (cost < bestCost) {
          best = candidate;
          bestCost = cost;
          improved = true;
        }
      }

      if (!improved) break;
    }

    return Object.freeze({ route: best, cost: bestCost });
  }

  function planBoard(records, config, random, anchorKey = '') {
    const started = typeof performance !== 'undefined' ? performance.now() : Date.now();
    const matrices = buildMatrices(records);
    const anchorIndex = anchorKey ? records.findIndex(record => record.destinationKey === anchorKey) : null;

    for (let level = 0; level <= CONSTRAINT_LEVELS.LAST_RESORT; level += 1) {
      let best = null;
      for (let restart = 0; restart < config.routeSearchRestarts; restart += 1) {
        const route = constructRoute(records, matrices, config, level, random, anchorIndex >= 0 ? anchorIndex : null);
        if (!route) continue;
        const optimized = optimizeRoute(route, matrices, config, level, random);
        if (!best || optimized.cost < best.cost) best = optimized;
      }
      if (best) {
        const ended = typeof performance !== 'undefined' ? performance.now() : Date.now();
        return Object.freeze({
          success: true,
          level,
          route: Object.freeze(best.route.map(index => records[index])),
          stats: routeStats(best.route, records, matrices, level),
          matrices,
          planningMs: ended - started
        });
      }
    }

    const ended = typeof performance !== 'undefined' ? performance.now() : Date.now();
    return Object.freeze({ success: false, level: null, route: Object.freeze([]), stats: null, matrices, planningMs: ended - started });
  }

  function buildTrajectory(sourceInput, targetInput, options = {}) {
    const source = normalizeDestination(sourceInput);
    const target = normalizeDestination(targetInput);
    const config = Object.freeze({ ...DEFAULTS, ...options });
    const durationSec = finiteNumber(options.totalTravelTimeSec ?? config.totalTravelTimeSec);
    if (durationSec === null || durationSec <= 0) throw new Error('TOTAL_TRAVEL_TIME must be greater than zero');

    const birdseye = Math.max(
      source.fov,
      target.fov,
      finiteNumber(options.birdseyeFovDeg ?? config.birdseyeFovDeg) || config.birdseyeFovDeg
    );
    const rotationDelta = shortestRotationSigned(source.orientation, target.orientation);
    const skyDistanceDeg = greatCircleDistanceDeg(source, target);

    function stateAtElapsedMs(elapsedMs) {
      const u = clamp01(Number(elapsedMs) / (durationSec * 1000));
      if (!config.animationEnabled || options.animationEnabled === false) {
        return Object.freeze({
          u: 1,
          elapsedMs: Math.max(0, Number(elapsedMs) || 0),
          ra: target.ra,
          dec: target.dec,
          fov: target.fov,
          rotation: target.orientation,
          translationProgress: 1,
          rotationProgress: 1,
          zoomPhase: 'INSTANT',
          done: true
        });
      }

      const translationProgress = windowProgress(u, config.translationStartU, config.translationEndU);
      const rotationProgress = windowProgress(u, config.rotationStartU, config.rotationEndU);
      const position = greatCirclePosition(source, target, translationProgress);

      let fov;
      let zoomPhase;
      if (u <= config.zoomOutPrimaryEndU) {
        fov = logInterpolate(source.fov, birdseye, smootherstep(u / config.zoomOutPrimaryEndU));
        zoomPhase = 'ZOOM_OUT';
      } else if (u < config.zoomInPrimaryStartU) {
        fov = birdseye;
        zoomPhase = 'CRUISE';
      } else {
        fov = logInterpolate(
          birdseye,
          target.fov,
          smootherstep((u - config.zoomInPrimaryStartU) / (1 - config.zoomInPrimaryStartU))
        );
        zoomPhase = 'ZOOM_IN';
      }

      return Object.freeze({
        u,
        elapsedMs: Math.max(0, Number(elapsedMs) || 0),
        ra: position.ra,
        dec: position.dec,
        fov,
        rotation: normalize360(source.orientation + rotationDelta * rotationProgress),
        translationProgress,
        rotationProgress,
        zoomPhase,
        done: u >= 1
      });
    }

    return Object.freeze({
      source,
      target,
      durationSec,
      skyDistanceDeg,
      rotationDistanceDeg: Math.abs(rotationDelta),
      signedRotationDeg: rotationDelta,
      fovRatio: Math.max(source.fov, target.fov) / Math.min(source.fov, target.fov),
      birdseyeFovDeg: birdseye,
      stateAtElapsedMs
    });
  }

  class NavigationEngine {
    constructor(options = {}) {
      this.config = Object.freeze({ ...DEFAULTS, ...options });
      this.state = STATES.IDLE;
      this.currentDestination = null;
      this.currentRoute = Object.freeze([]);
      this.routeCursor = 0;
      this.nextRoute = Object.freeze([]);
      this.future = Object.freeze([]);
      this.history = [];
      this.planningPromise = null;
      this.preparationState = new Map();
      this.totalTravelTime = this.config.totalTravelTimeSec;
      this.claimed = null;
      this.diagnostics = [];
      this.lastPlan = null;
      this.random = typeof options.random === 'function' ? options.random : Math.random;
      this.planningPoolId = 0;
    }

    setTotalTravelTime(seconds) {
      const value = finiteNumber(seconds);
      if (value === null || value <= 0) throw new Error('TOTAL_TRAVEL_TIME must be greater than zero');
      this.totalTravelTime = value;
      return value;
    }

    setAnimationEnabled(enabled) {
      this.config = Object.freeze({ ...this.config, animationEnabled: Boolean(enabled) });
      return this.config.animationEnabled;
    }

    filterEligible(catalog, context = {}) {
      const excluded = new Set();
      const add = value => {
        const key = typeof value === 'string' ? value.trim().toLowerCase() : destinationKey(value);
        if (key) excluded.add(key);
      };

      add(context.currentGalaxy);
      add(context.excludeName);
      for (const item of context.history || []) add(item);
      for (const item of context.future || this.future || []) add(item);
      for (const item of context.quarantined || []) add(item);
      for (const item of context.unavailable || []) add(item);

      const result = [];
      const seen = new Set();
      for (const raw of catalog || []) {
        let record;
        try { record = normalizeDestination(raw); } catch (_) { continue; }
        if (excluded.has(record.destinationKey)) continue;
        if (seen.has(record.destinationKey)) continue;
        if (typeof context.isEligible === 'function' && !context.isEligible(record)) continue;
        seen.add(record.destinationKey);
        result.push(record);
      }
      return result;
    }

    plan(catalog, context = {}) {
      this.state = STATES.ENSURE_FUTURE;
      const random = context.seed === undefined ? this.random : mulberry32(context.seed);
      const eligible = this.filterEligible(catalog, context);
      const pool = sampleUnique(eligible, Math.min(this.config.planningPoolSize, eligible.length), random);
      this.planningPoolId += 1;

      if (!pool.length) {
        this.state = STATES.IDLE;
        throw new Error('No eligible destinations available for navigation planning');
      }

      const anchorRaw = context.anchor ?? this.currentDestination;
      let records = pool;
      let anchorKey = '';
      if (anchorRaw) {
        const anchor = normalizeDestination(anchorRaw);
        anchorKey = anchor.destinationKey;
        if (!records.some(record => record.destinationKey === anchorKey)) records = [anchor, ...records];
      }

      const result = planBoard(records, this.config, random, anchorKey);
      if (!result.success) {
        this.state = STATES.IDLE;
        throw new Error('Navigation planner could not construct a usable route');
      }

      let route = [...result.route];
      if (anchorKey && route[0]?.destinationKey === anchorKey) route = route.slice(1);
      if (route.length > this.config.planningPoolSize) route = route.slice(0, this.config.planningPoolSize);

      this.currentRoute = Object.freeze(route);
      this.routeCursor = 0;
      this.future = Object.freeze(route.slice(0, this.config.prefetchTarget));
      this.lastPlan = Object.freeze({
        planningPoolId: this.planningPoolId,
        selectedPoolSize: pool.length,
        eligibleCount: eligible.length,
        constraintLevel: result.level,
        mode: result.level === 0 ? 'NORMAL' : `FALLBACK_${result.level}`,
        planningMs: result.planningMs,
        stats: result.stats,
        futureLength: this.future.length,
        future0: this.future[0]?.destinationKey ?? null,
        duplicateFutureKeys: this.future.length !== new Set(this.future.map(destinationKey)).size,
        routeLength: route.length,
        offAnimationCriticalPath: Boolean(context.offAnimationCriticalPath)
      });
      this.diagnostics.push(this.lastPlan);
      this.state = this.future.length ? STATES.READY : STATES.IDLE;
      return this.lastPlan;
    }

    getWatermarkState() {
      const length = this.future.length;
      if (length <= this.config.prefetchEmergencyLevel) return 'EMERGENCY';
      if (length <= this.config.prefetchPriorityLevel) return 'PRIORITY';
      if (length < this.config.prefetchTarget) return 'REFILL';
      return 'NORMAL';
    }

    shouldPlanNextRoute() {
      return Math.max(0, this.currentRoute.length - this.routeCursor) <= this.config.nextPlanTrigger;
    }

    claimHead() {
      if (this.claimed) return this.claimed;
      const head = this.future[0];
      if (!head) return null;
      this.claimed = head;
      this.state = STATES.CLAIMED;
      return head;
    }

    beginTravel() {
      if (!this.claimed) throw new Error('Cannot begin travel without a claimed future[0]');
      this.state = STATES.TRAVELING;
      return this.claimed;
    }

    arrive() {
      if (!this.claimed) throw new Error('Cannot arrive without a claimed destination');
      this.state = STATES.ARRIVED;
      return this.claimed;
    }

    commit() {
      if (!this.claimed) throw new Error('Cannot commit without a claimed destination');
      if (this.future[0]?.destinationKey !== this.claimed.destinationKey) {
        throw new Error('future[0] identity changed while navigation was claimed');
      }

      const committed = this.claimed;
      this.currentDestination = committed;
      this.history.push(committed);
      this.routeCursor += 1;
      this.claimed = null;
      this.future = Object.freeze(this.currentRoute.slice(this.routeCursor, this.routeCursor + this.config.prefetchTarget));
      this.state = STATES.COMMITTED;
      this.state = this.future.length ? STATES.READY : STATES.IDLE;
      return committed;
    }

    rollback() {
      const rolledBack = this.claimed;
      this.claimed = null;
      this.state = this.future.length ? STATES.READY : STATES.IDLE;
      return rolledBack;
    }

    createTrajectory(source, target, options = {}) {
      return buildTrajectory(source, target, {
        ...this.config,
        ...options,
        totalTravelTimeSec: options.totalTravelTimeSec ?? this.totalTravelTime
      });
    }

    async animate(source, target, adapter, options = {}) {
      const trajectory = this.createTrajectory(source, target, options);
      const raf = options.requestAnimationFrame ?? global.requestAnimationFrame?.bind(global);
      const now = options.now ?? (() => global.performance?.now?.() ?? Date.now());
      const apply = adapter?.applyState;

      if (typeof apply !== 'function') throw new TypeError('animate requires adapter.applyState(state)');

      if (!this.config.animationEnabled || options.animationEnabled === false) {
        const state = trajectory.stateAtElapsedMs(trajectory.durationSec * 1000);
        apply(state);
        return Object.freeze({ trajectory, actualTravelDurationMs: 0, frames: 1, frameIntervals: Object.freeze([]) });
      }
      if (typeof raf !== 'function') throw new Error('requestAnimationFrame is required for animated travel');

      const started = now();
      let previous = null;
      const frameIntervals = [];
      let frameCount = 0;

      await new Promise((resolve, reject) => {
        const frame = timestamp => {
          try {
            const elapsed = Math.max(0, Number(timestamp) - started);
            if (previous !== null) frameIntervals.push(Number(timestamp) - previous);
            previous = Number(timestamp);
            frameCount += 1;
            const state = trajectory.stateAtElapsedMs(elapsed);
            apply(state);
            if (state.done) return resolve();
            raf(frame);
          } catch (error) {
            reject(error);
          }
        };
        raf(frame);
      });

      const actual = Math.max(0, now() - started);
      const diagnostic = Object.freeze({
        sourceKey: trajectory.source.destinationKey,
        targetKey: trajectory.target.destinationKey,
        sky_distance_deg: trajectory.skyDistanceDeg,
        rotation_distance_deg: trajectory.rotationDistanceDeg,
        signed_rotation_deg: trajectory.signedRotationDeg,
        source_fov: trajectory.source.fov,
        target_fov: trajectory.target.fov,
        fov_ratio: trajectory.fovRatio,
        requested_travel_T: trajectory.durationSec,
        actual_travel_duration_ms: actual,
        frames: frameCount,
        frameIntervals: Object.freeze([...frameIntervals])
      });
      this.diagnostics.push(diagnostic);
      return Object.freeze({ trajectory, actualTravelDurationMs: actual, frames: frameCount, frameIntervals: Object.freeze([...frameIntervals]) });
    }

    getState() {
      return Object.freeze({
        version: VERSION,
        state: this.state,
        currentDestination: this.currentDestination,
        routeCursor: this.routeCursor,
        currentRouteLength: this.currentRoute.length,
        nextRouteLength: this.nextRoute.length,
        future: this.future,
        future0: this.future[0] ?? null,
        claimed: this.claimed,
        watermark: this.getWatermarkState(),
        shouldPlanNextRoute: this.shouldPlanNextRoute(),
        totalTravelTimeSec: this.totalTravelTime,
        lastPlan: this.lastPlan
      });
    }
  }

  function selfTest() {
    const failures = [];
    const assert = (condition, label) => { if (!condition) failures.push(label); };

    assert(shortestRotationDistance(359, 0) === 1, '359->0 shortest rotation');
    assert(shortestRotationDistance(350, 10) === 20, '350->10 shortest rotation');
    assert(shortestRotationDistance(10, 350) === 20, '10->350 shortest rotation');
    assert(shortestRotationDistance(0, 180) === 180, '0->180 shortest rotation');
    assert(parseOrientation(null) === 0, 'missing orientation defaults to north-up');
    assert(parseOrientation('North is up') === 0, 'North is up parsing');
    assert(parseOrientation('North is 8.5° left of vertical') === 351.5, 'left orientation parsing');

    const a = { destinationKey: 'a', ra: 0, dec: 0, fov: 1, orientation: 350 };
    const b = { destinationKey: 'b', ra: 90, dec: 0, fov: 2, orientation: 10 };
    assert(Math.abs(greatCircleDistanceDeg(a, b) - 90) < 1e-9, 'great-circle 90-degree separation');

    const trajectory20 = buildTrajectory(a, b, { totalTravelTimeSec: 20 });
    const trajectory15 = buildTrajectory(a, b, { totalTravelTimeSec: 15 });
    const halfway20 = trajectory20.stateAtElapsedMs(10000);
    const halfway15 = trajectory15.stateAtElapsedMs(7500);
    assert(Math.abs(halfway20.translationProgress - halfway15.translationProgress) < 1e-12, 'T scaling translation');
    assert(Math.abs(halfway20.rotationProgress - halfway15.rotationProgress) < 1e-12, 'T scaling rotation');

    const sample = sampleUnique([
      a,
      b,
      { destinationKey: 'c', ra: 180, dec: 0, fov: 1, orientation: 0 },
      { destinationKey: 'c', ra: 180, dec: 0, fov: 1, orientation: 0 }
    ], 100, mulberry32(1));
    assert(sample.length === 3, 'unique random sample');

    return Object.freeze({ ok: failures.length === 0, failures: Object.freeze(failures), version: VERSION });
  }

  const API = Object.freeze({
    VERSION,
    DEFAULTS,
    STATES,
    CONSTRAINT_LEVELS,
    NavigationEngine,
    normalize360,
    parseOrientation,
    shortestRotationSigned,
    shortestRotationDistance,
    greatCircleDistanceDeg,
    greatCirclePosition,
    smootherstep,
    sampleUnique,
    buildMatrices,
    buildTrajectory,
    mulberry32,
    selfTest
  });

  global.GalaxyViewerNavigationEngine = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof globalThis !== 'undefined' ? globalThis : window);
