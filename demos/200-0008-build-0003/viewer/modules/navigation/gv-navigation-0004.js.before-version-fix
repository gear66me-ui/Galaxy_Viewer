/*
 * GALAXY VIEWER — RANDOM NAVIGATION MODULE 0002
 *
 * PURPOSE
 *   Metadata-only 130 -> 100 random route planner.
 *
 * FINAL NAVIGATION RULES
 *   Candidate pool:       130 unique destinations
 *   Committed route:      100 unique destinations
 *   Translation target:    95 degrees
 *   Translation limits:    42.5 .. 147.5 degrees
 *   FOV transition limit:  <= 5 octaves
 *   Rotation:              unrestricted; telemetry only
 *
 * STARTUP / TRAVEL
 *   Bootstrap random galaxy: exactly once per application launch
 *   Bootstrap trip:           9 seconds
 *   Normal trip:             18 seconds
 *   Birdseye FOV:            200 degrees
 *
 * IMPORTANT
 *   This module plans metadata only.
 *   It does not download/decode images and does not own Random Galaxy UI,
 *   history, HD preload, archive preload, or Aladin preparation.
 */

(function(global){
  'use strict';

  const VERSION = '0003';

  const CONSTANTS = Object.freeze({
    CANDIDATE_POOL_SIZE: 130,
    ROUTE_LENGTH: 100,

    TRANSLATION_TARGET_DEG: 95,
    TRANSLATION_MIN_DEG: 42.5,
    TRANSLATION_MAX_DEG: 147.5,

    MAX_FOV_OCTAVES: 5,

    ROTATION_RESTRICTED: false,

    ROUTE_RESTARTS: 128,
    MAX_SAMPLE_ATTEMPTS: 100,

    BOOTSTRAP_TRAVEL_SECONDS: 9,
    NORMAL_TRAVEL_SECONDS: 18,
    BIRDSEYE_FOV_DEG: 120
  });

  const finite = v => {
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  };

  const clean = v => String(v == null ? '' : v).replace(/\s+/g,' ').trim();

  const normalizeSigned = x =>
    ((Number(x) + 180) % 360 + 360) % 360 - 180;

  function identityOf(record){
    const provider = clean(
      record?.provider ??
      record?.source ??
      record?.catalog ??
      record?.database ??
      record?.telescope
    ).toLowerCase();

    const direct = clean(
      record?.navigationKey ??
      record?.destinationKey ??
      record?.archiveId ??
      record?.id ??
      record?.key
    ).toLowerCase();

    const ra = finite(record?.ra);
    const dec = finite(record?.dec);

    /*
     * archiveId/id values are NOT globally unique across providers.
     * Example: Hubble and JWST both use "potm2601a" for different objects.
     * Namespace direct IDs by provider. If provider metadata is absent,
     * RA/Dec prevent unrelated archive products from collapsing together.
     */
    if(direct){
      return provider
        ? `${provider}|${direct}`
        : `${direct}|${ra ?? ''}|${dec ?? ''}`;
    }

    const name = clean(
      record?.displayName ??
      record?.designation ??
      record?.name ??
      record?.title
    ).toLowerCase();

    if(!name || ra === null || dec === null) return '';

    return `${provider}|${name}|${ra}|${dec}`;
  }

  function fovOf(record){
    const value=finite(record?.fovDegrees);
    return value!==null && value>0 ? value : null;
  }

  function orientationOf(record){
    const value=finite(record?.aladinRotation);
    return value!==null ? normalizeSigned(value) : null;
  }

  function normalizeRecord(record){
    if(!record || typeof record !== 'object') return null;

    const key = identityOf(record);
    const ra = finite(record.ra);
    const dec = finite(record.dec);
    const fov = fovOf(record);

    if(!key) return null;
    if(ra === null || ra < 0 || ra >= 360) return null;
    if(dec === null || dec < -90 || dec > 90) return null;
    if(fov === null || fov <= 0) return null;

    return Object.freeze({
      key,
      ra,
      dec,
      fov,
      orientation: orientationOf(record),
      record
    });
  }

  function deduplicateEligible(catalog){
    const map = new Map();

    for(const raw of Array.isArray(catalog) ? catalog : []){
      const item = normalizeRecord(raw);
      if(!item || map.has(item.key)) continue;
      map.set(item.key,item);
    }

    return [...map.values()];
  }

  function greatCircleDeg(a,b){
    const ra1 = a.ra * Math.PI / 180;
    const de1 = a.dec * Math.PI / 180;
    const ra2 = b.ra * Math.PI / 180;
    const de2 = b.dec * Math.PI / 180;

    const c =
      Math.sin(de1) * Math.sin(de2) +
      Math.cos(de1) * Math.cos(de2) * Math.cos(ra1-ra2);

    return Math.acos(Math.max(-1,Math.min(1,c))) * 180 / Math.PI;
  }

  function fovOctaves(a,b){
    return Math.abs(Math.log2(a.fov / b.fov));
  }

  function rotationDeltaDeg(a,b){
    if(a.orientation === null || b.orientation === null) return null;
    return Math.abs(normalizeSigned(b.orientation-a.orientation));
  }

  function compatibility(a,b){
    const travelDeg = greatCircleDeg(a,b);
    const fovDeltaOctaves = fovOctaves(a,b);
    const rotationDeg = rotationDeltaDeg(a,b);

    const travelLegal =
      travelDeg >= CONSTANTS.TRANSLATION_MIN_DEG &&
      travelDeg <= CONSTANTS.TRANSLATION_MAX_DEG;

    const fovLegal =
      fovDeltaOctaves <= CONSTANTS.MAX_FOV_OCTAVES;

    return Object.freeze({
      compatible: travelLegal && fovLegal,
      travelLegal,
      fovLegal,
      travelDeg,
      fovDeltaOctaves,
      rotationDeg
    });
  }

  function shuffled(values,rng=Math.random){
    const a = [...values];

    for(let i=a.length-1;i>0;i--){
      const j = Math.floor(rng()*(i+1));
      [a[i],a[j]]=[a[j],a[i]];
    }

    return a;
  }

  function buildGraph(nodes,anchor=null){
    const n = nodes.length;
    const neighbors = Array.from({length:n},()=>[]);
    const edges = new Map();

    for(let i=0;i<n;i++){
      for(let j=i+1;j<n;j++){
        const e = compatibility(nodes[i],nodes[j]);
        edges.set(`${i}:${j}`,e);

        if(e.compatible){
          neighbors[i].push(j);
          neighbors[j].push(i);
        }
      }
    }

    const anchorCompatible = [];

    if(anchor){
      for(let i=0;i<n;i++){
        const e = compatibility(anchor,nodes[i]);
        edges.set(`A:${i}`,e);
        if(e.compatible) anchorCompatible.push(i);
      }
    }

    return {nodes,neighbors,edges,anchorCompatible};
  }

  function edgeOf(graph,a,b){
    const key = a < b ? `${a}:${b}` : `${b}:${a}`;
    return graph.edges.get(key);
  }

  function futureDegree(graph,index,used){
    let n = 0;

    for(const other of graph.neighbors[index]){
      if(!used.has(other)) n++;
    }

    return n;
  }

  function solve100From130(
    graph,
    {
      anchor=null,
      rng=Math.random,
      restarts=CONSTANTS.ROUTE_RESTARTS
    }={}
  ){
    const N = graph.nodes.length;
    const TARGET = CONSTANTS.ROUTE_LENGTH;

    if(N !== CONSTANTS.CANDIDATE_POOL_SIZE) return null;

    const starts = anchor
      ? [...graph.anchorCompatible]
      : graph.nodes
          .map((_,i)=>i)
          .filter(i=>graph.neighbors[i].length>0);

    if(!starts.length) return null;

    for(let attempt=1; attempt<=restarts; attempt++){
      const rankedStarts = shuffled(starts,rng).sort(
        (a,b)=>graph.neighbors[a].length-graph.neighbors[b].length
      );

      const startBand = rankedStarts.slice(
        0,
        Math.max(1,Math.ceil(rankedStarts.length*0.35))
      );

      const start = startBand[
        Math.floor(rng()*startBand.length)
      ];

      const path=[start];
      const used=new Set(path);

      while(path.length<TARGET){
        const current=path[path.length-1];

        const candidates=graph.neighbors[current]
          .filter(i=>!used.has(i));

        if(!candidates.length) break;

        const scored=candidates.map(next=>{
          const e=edgeOf(graph,current,next);

          return {
            next,
            remaining:futureDegree(graph,next,used),
            fov:e.fovDeltaOctaves,
            targetError:Math.abs(
              e.travelDeg-CONSTANTS.TRANSLATION_TARGET_DEG
            ),
            tie:rng()
          };
        });

        scored.sort((a,b)=>
          a.targetError-b.targetError ||
          a.fov-b.fov ||
          b.remaining-a.remaining ||
          a.tie-b.tie
        );

        const chosen=scored[0].next;
        path.push(chosen);
        used.add(chosen);
      }

      if(path.length===TARGET){
        return {
          indices:path,
          solverAttempt:attempt
        };
      }
    }

    return null;
  }

  function validateRoute(route,anchor=null){
    if(!Array.isArray(route))
      return {ok:false,reason:'NOT_ARRAY'};

    if(route.length!==CONSTANTS.ROUTE_LENGTH)
      return {ok:false,reason:'LENGTH'};

    if(new Set(route.map(x=>x.key)).size!==route.length)
      return {ok:false,reason:'DUPLICATE'};

    const edges=[];

    if(anchor){
      const seam=compatibility(anchor,route[0]);

      if(!seam.compatible)
        return {ok:false,reason:'ANCHOR_SEAM',edge:seam};

      edges.push({
        from:anchor.key,
        to:route[0].key,
        seam:true,
        ...seam
      });
    }

    for(let i=0;i<route.length-1;i++){
      const e=compatibility(route[i],route[i+1]);

      if(!e.compatible){
        return {
          ok:false,
          reason:'EDGE',
          index:i,
          edge:e
        };
      }

      edges.push({
        from:route[i].key,
        to:route[i+1].key,
        seam:false,
        ...e
      });
    }

    return {ok:true,edges};
  }

  function summary(values){
    const a=values
      .filter(Number.isFinite)
      .sort((x,y)=>x-y);

    if(!a.length) return null;

    const mean=a.reduce((s,x)=>s+x,0)/a.length;
    const variance=a.reduce(
      (s,x)=>s+(x-mean)**2,
      0
    )/a.length;

    const q=p=>{
      const x=(a.length-1)*p;
      const lo=Math.floor(x), hi=Math.ceil(x);
      if(lo===hi) return a[lo];
      return a[lo]+(a[hi]-a[lo])*(x-lo);
    };

    return Object.freeze({
      n:a.length,
      min:a[0],
      mean,
      median:q(.5),
      sigma:Math.sqrt(variance),
      p95:q(.95),
      p99:q(.99),
      max:a[a.length-1]
    });
  }

  function routeTelemetry(validation){
    const edges=validation?.edges||[];

    return Object.freeze({
      travel:summary(edges.map(e=>e.travelDeg)),
      fovOctaves:summary(edges.map(e=>e.fovDeltaOctaves)),
      rotation:summary(
        edges.map(e=>e.rotationDeg).filter(Number.isFinite)
      )
    });
  }

  function planRoute(
    catalog,
    {
      anchorRecord=null,
      rng=Math.random,
      maxSampleAttempts=CONSTANTS.MAX_SAMPLE_ATTEMPTS,
      restarts=CONSTANTS.ROUTE_RESTARTS
    }={}
  ){
    const eligible=deduplicateEligible(catalog);

    if(eligible.length<CONSTANTS.CANDIDATE_POOL_SIZE){
      throw new Error(
        `NAVIGATION ELIGIBLE CATALOG TOO SMALL: ${eligible.length}`
      );
    }

    const anchor=anchorRecord
      ? normalizeRecord(anchorRecord)
      : null;

    if(anchorRecord && !anchor)
      throw new Error('NAVIGATION ANCHOR INVALID');

    const started=
      typeof performance!=='undefined' && performance.now
        ? performance.now()
        : Date.now();

    for(
      let sampleAttempt=1;
      sampleAttempt<=maxSampleAttempts;
      sampleAttempt++
    ){
      const sample=shuffled(eligible,rng)
        .slice(0,CONSTANTS.CANDIDATE_POOL_SIZE);

      const graph=buildGraph(sample,anchor);

      const solved=solve100From130(
        graph,
        {anchor,rng,restarts}
      );

      if(!solved) continue;

      const route=solved.indices.map(i=>sample[i]);

      const validation=validateRoute(route,anchor);

      if(!validation.ok) continue;

      const finished=
        typeof performance!=='undefined' && performance.now
          ? performance.now()
          : Date.now();

      const used=new Set(route.map(x=>x.key));

      return Object.freeze({
        version:VERSION,
        poolSize:CONSTANTS.CANDIDATE_POOL_SIZE,
        routeLength:route.length,
        sampleAttempt,
        solverAttempt:solved.solverAttempt,
        solveTimeMs:finished-started,

        route:Object.freeze(route.map(x=>x.record)),

        routeMeta:Object.freeze(route),

        discarded:Object.freeze(
          sample
            .filter(x=>!used.has(x.key))
            .map(x=>x.record)
        ),

        validation:Object.freeze(validation),

        telemetry:routeTelemetry(validation)
      });
    }

    throw new Error(
      `NAVIGATION 130->100 FAILED AFTER ${maxSampleAttempts} SAMPLES`
    );
  }

  class RoutePlanner{
    constructor({catalog,rng=Math.random}={}){
      this.catalog=Array.isArray(catalog)?catalog:[];
      this.rng=rng;
      this.plan=null;
      this.cursor=0;
    }

    initialize(anchorRecord=null){
      this.plan=planRoute(
        this.catalog,
        {anchorRecord,rng:this.rng}
      );

      this.cursor=0;
      return this.getState();
    }

    peekNext(){
      return this.plan?.route?.[this.cursor] ?? null;
    }

    peekNextMeta(){
      return this.plan?.routeMeta?.[this.cursor] ?? null;
    }

    getUpcoming(count=10){
      if(!this.plan) return [];

      return this.plan.route.slice(
        this.cursor,
        this.cursor+Math.max(0,Number(count)||0)
      );
    }

    commitNext(expectedRecord=null){
      if(!this.plan)
        throw new Error('NAVIGATION NOT INITIALIZED');

      const current=this.plan.routeMeta[this.cursor];

      if(!current)
        throw new Error('NAVIGATION ROUTE EXHAUSTED');

      if(
        expectedRecord &&
        identityOf(expectedRecord)!==current.key
      ){
        throw new Error(
          'NAVIGATION COMMIT IDENTITY MISMATCH'
        );
      }

      this.cursor++;
      return this.getState();
    }

    remaining(){
      return this.plan
        ? Math.max(0,this.plan.routeLength-this.cursor)
        : 0;
    }

    getState(){
      return Object.freeze({
        version:VERSION,
        initialized:Boolean(this.plan),
        cursor:this.cursor,
        remaining:this.remaining(),
        routeLength:this.plan?.routeLength ?? 0,
        poolSize:this.plan?.poolSize ?? 0,
        solveTimeMs:this.plan?.solveTimeMs ?? null,
        bootstrapTravelSeconds:
          CONSTANTS.BOOTSTRAP_TRAVEL_SECONDS,
        normalTravelSeconds:
          CONSTANTS.NORMAL_TRAVEL_SECONDS,
        birdseyeFovDeg:
          CONSTANTS.BIRDSEYE_FOV_DEG
      });
    }

    getPlan(){
      return this.plan;
    }
  }

  global.GalaxyViewerNavigation=Object.freeze({
    VERSION,
    CONSTANTS,
    create:options=>new RoutePlanner(options),
    planRoute,
    deduplicateEligible,
    normalizeRecord,
    identityOf,
    greatCircleDeg,
    fovOctaves,
    rotationDeltaDeg,
    compatibility,
    validateRoute
  });

})(typeof window!=='undefined' ? window : globalThis);
