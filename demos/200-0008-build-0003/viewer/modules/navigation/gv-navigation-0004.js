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

  const VERSION = '0004';

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
    NORMAL_TRAVEL_SECONDS: 15,
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


  const NAVIGATION_WORKER_VERSION='0001';
  const NAVIGATION_WORKER_TIMEOUT_MS=60000;
  const NAVIGATION_MODULE_URL=
    typeof document!=='undefined' &&
    document.currentScript?.src
      ? document.currentScript.src
      : null;

  function solverRecord(record){
    if(!record || typeof record!=='object') return null;

    return {
      provider:record.provider ?? null,
      source:record.source ?? null,
      catalog:record.catalog ?? null,
      database:record.database ?? null,
      telescope:record.telescope ?? null,
      navigationKey:record.navigationKey ?? null,
      destinationKey:record.destinationKey ?? null,
      archiveId:record.archiveId ?? null,
      id:record.id ?? null,
      key:record.key ?? null,
      displayName:record.displayName ?? null,
      designation:record.designation ?? null,
      name:record.name ?? null,
      title:record.title ?? null,
      ra:finite(record.ra),
      dec:finite(record.dec),
      fovDegrees:fovOf(record),
      aladinRotation:finite(record.aladinRotation)
    };
  }

  function navigationWorkerUrl(){
    if(!NAVIGATION_MODULE_URL)
      throw new Error(
        'NAVIGATION 0004 WORKER BASE URL UNAVAILABLE'
      );

    return new URL(
      'gv-navigation-worker-0001.js',
      NAVIGATION_MODULE_URL
    ).href;
  }

  function solvePlanInWorker(catalog,anchorRecord=null){
    return new Promise((resolve,reject)=>{
      const worker=new Worker(navigationWorkerUrl());
      const id=
        `gv-nav-${Date.now()}-${Math.random().toString(16).slice(2)}`;

      let settled=false;

      const finish=(fn,value)=>{
        if(settled)return;
        settled=true;
        clearTimeout(timer);
        worker.terminate();
        fn(value);
      };

      const timer=setTimeout(
        ()=>finish(
          reject,
          new Error('NAVIGATION 0004 WORKER TIMEOUT')
        ),
        NAVIGATION_WORKER_TIMEOUT_MS
      );

      worker.onmessage=event=>{
        const data=event?.data||{};
        if(data.id!==id || data.type!=='PLAN_RESULT')return;

        if(
          data.ok!==true ||
          data.workerVersion!==NAVIGATION_WORKER_VERSION ||
          data.navigationVersion!==VERSION
        ){
          finish(
            reject,
            new Error(
              data.error ||
              'NAVIGATION 0004 WORKER RESULT INVALID'
            )
          );
          return;
        }

        finish(resolve,data);
      };

      worker.onerror=event=>{
        finish(
          reject,
          new Error(
            `NAVIGATION 0004 WORKER ERROR: ${
              event?.message||'UNKNOWN'
            }`
          )
        );
      };

      worker.postMessage({
        type:'PLAN',
        id,
        catalog:(Array.isArray(catalog)?catalog:[])
          .map(solverRecord)
          .filter(Boolean),
        anchorRecord:anchorRecord
          ? solverRecord(anchorRecord)
          : null
      });
    });
  }

  function materializeWorkerPlan(
    result,
    catalog,
    anchorRecord=null
  ){
    const eligible=deduplicateEligible(catalog);
    const byKey=new Map(
      eligible.map(item=>[item.key,item])
    );

    const routeKeys=
      Array.isArray(result?.routeKeys)
        ? result.routeKeys
        : [];

    const routeMeta=routeKeys.map(key=>byKey.get(key));

    if(
      routeMeta.length!==CONSTANTS.ROUTE_LENGTH ||
      routeMeta.some(item=>!item)
    ){
      throw new Error(
        'NAVIGATION 0004 WORKER ROUTE MATERIALIZATION FAILURE'
      );
    }

    const route=routeMeta.map(item=>item.record);

    const anchor=anchorRecord
      ? normalizeRecord(anchorRecord)
      : null;

    const validation=validateRoute(routeMeta,anchor);

    if(!validation.ok){
      throw new Error(
        `NAVIGATION 0004 WORKER ROUTE VALIDATION FAILURE: ${
          validation.reason||'UNKNOWN'
        }`
      );
    }

    const discardedKeys=
      Array.isArray(result?.discardedKeys)
        ? result.discardedKeys
        : [];

    const discarded=discardedKeys
      .map(key=>byKey.get(key)?.record)
      .filter(Boolean);

    return Object.freeze({
      version:VERSION,
      poolSize:Number(result.poolSize),
      routeLength:route.length,
      sampleAttempt:Number(result.sampleAttempt),
      solverAttempt:Number(result.solverAttempt),
      solveTimeMs:Number(result.solveTimeMs),
      route:Object.freeze(route),
      routeMeta:Object.freeze(routeMeta),
      discarded:Object.freeze(discarded),
      validation:Object.freeze(validation),
      telemetry:routeTelemetry(validation),
      workerVersion:NAVIGATION_WORKER_VERSION,
      offMainThread:true
    });
  }

  class RoutePlanner{
    constructor({catalog,rng=Math.random}={}){
      this.catalog=Array.isArray(catalog)?catalog:[];
      this.rng=rng;
      this.plan=null;
      this.cursor=0;
    }

    async initialize(anchorRecord=null){
      if(
        typeof Worker==='function' &&
        this.rng===Math.random
      ){
        const result=await solvePlanInWorker(
          this.catalog,
          anchorRecord
        );

        this.plan=materializeWorkerPlan(
          result,
          this.catalog,
          anchorRecord
        );
      }else{
        this.plan=planRoute(
          this.catalog,
          {anchorRecord,rng:this.rng}
        );
      }

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


  // ==========================================================
  // ACTIVE VIEWPORT FLIGHT ENGINE
  // Navigation 0004 owns trip timing, interpolation, RAF, and
  // all Aladin viewport mutation during an active flight.
  // ==========================================================

  function flightClamp01(value){
    return Math.max(0,Math.min(1,Number(value)));
  }

  function flightSmootherstep(value){
    const t=flightClamp01(value);
    return t*t*t*(t*(t*6-15)+10);
  }

  function flightNavigationSmootherstep(value){
    const t=flightClamp01(value);
    return 35*t*t*t*t-84*t*t*t*t*t+70*t*t*t*t*t*t-20*t*t*t*t*t*t*t;
  }

  function flightNormalizeRotationDelta(value){
    let angle=Number(value)||0;
    while(angle>180)angle-=360;
    while(angle<=-180)angle+=360;
    return angle;
  }

  function flightGreatCirclePosition(ra1,dec1,ra2,dec2,progress){
    const d2r=Math.PI/180;
    const r2d=180/Math.PI;
    const aRa=Number(ra1)*d2r;
    const aDec=Number(dec1)*d2r;
    const bRa=Number(ra2)*d2r;
    const bDec=Number(dec2)*d2r;
    const u=flightClamp01(progress);

    const ax=Math.cos(aDec)*Math.cos(aRa);
    const ay=Math.cos(aDec)*Math.sin(aRa);
    const az=Math.sin(aDec);
    const bx=Math.cos(bDec)*Math.cos(bRa);
    const by=Math.cos(bDec)*Math.sin(bRa);
    const bz=Math.sin(bDec);

    const dot=Math.max(-1,Math.min(1,ax*bx+ay*by+az*bz));
    const omega=Math.acos(dot);

    if(omega<1e-12)
      return [Number(ra2),Number(dec2)];

    const sinOmega=Math.sin(omega);
    const wa=Math.sin((1-u)*omega)/sinOmega;
    const wb=Math.sin(u*omega)/sinOmega;

    const x=wa*ax+wb*bx;
    const y=wa*ay+wb*by;
    const z=wa*az+wb*bz;

    let ra=Math.atan2(y,x)*r2d;
    if(ra<0)ra+=360;
    const dec=Math.atan2(z,Math.sqrt(x*x+y*y))*r2d;
    return [ra,dec];
  }

  function flightTranslationProgress(t,immediate=false){
    if(immediate)return flightClamp01(t);
    if(t<=4/15)return 0;
    if(t>=11/15)return 1;

    const I=(u)=>u**6-3*u**5+2.5*u**4;

    if(t<11/30){
      const u=(t-4/15)/(1.5/15);
      return (3/11)*I(u);
    }

    if(t<=19/30)
      return 3/22+(30/11)*(t-11/30);

    const u=(11/15-t)/(1.5/15);
    return 1-(3/11)*I(u);
  }

  function flightFovAt(t,startFov,destinationFov,maxFov,immediate=false){
    if(immediate){
      const u=flightClamp01(t);
      return Math.exp(
        Math.log(startFov)+
        (Math.log(destinationFov)-Math.log(startFov))*u
      );
    }

    const maximum=Number(maxFov);

    if(t<=11/30){
      const u=flightNavigationSmootherstep(
        flightClamp01(t/(11/30))
      );
      return Math.exp(
        Math.log(startFov)+
        (Math.log(maximum)-Math.log(startFov))*u
      );
    }

    if(t<=19/30)
      return maximum;

    const u=flightNavigationSmootherstep(
      flightClamp01((t-19/30)/(11/30))
    );

    return Math.exp(
      Math.log(maximum)+
      (Math.log(destinationFov)-Math.log(maximum))*u
    );
  }

  function flightDistanceProgress(t){
    return flightNavigationSmootherstep(t);
  }

  async function flyViewport({
    aladin,
    source,
    destination,
    routeValue=0,
    startRA,
    startDec,
    startFov,
    destinationFov,
    firstHomeTrip=false,
    travelSeconds=CONSTANTS.NORMAL_TRAVEL_SECONDS,
    firstHomeTravelSeconds=CONSTANTS.BOOTSTRAP_TRAVEL_SECONDS,
    firstHomeTranslationSeconds=4,
    maxFov=CONSTANTS.BIRDSEYE_FOV_DEG,
    translateStart=11/30,
    translate90=19/30,
    translationComplete=11/15,
    rotationStart=0,
    aladinTravelHz=15,
    onDistanceProgress=null,
    onTimelineProgress=null,
    trace=null,
    traceError=null
  }={}){

    if(!aladin)
      throw new Error('NAVIGATION 0004 ALADIN INSTANCE MISSING');

    const destinationRA=Number(destination?.ra);
    const destinationDec=Number(destination?.dec);
    const finalFov=Number(destinationFov);
    const startFovNumber=Number(startFov);

    if(!Number.isFinite(startFovNumber)||startFovNumber<=0)
      throw new Error('CURRENT ALADIN FOV IS INVALID');

    if(!Number.isFinite(finalFov)||finalFov<=0)
      throw new Error('DESTINATION ALADIN FOV IS INVALID');

    if(!Number.isFinite(destinationRA)||!Number.isFinite(destinationDec))
      throw new Error('DESTINATION COORDINATES ARE INVALID');

    const emitTrace=(code,label,detail)=>{
      try{if(typeof trace==='function')trace(code,label,detail);}catch(_){}
    };
    const emitTraceError=(code,label,error)=>{
      try{if(typeof traceError==='function')traceError(code,label,error);}catch(_){}
    };

    const duration=
      Number(firstHomeTrip?firstHomeTravelSeconds:travelSeconds)*1000;

    const firstHomeTranslationCompleteEnd=
      firstHomeTrip
        ? flightClamp01(
            Number(firstHomeTranslationSeconds)/
            Number(firstHomeTravelSeconds)
          )
        : 0;

    const rotationStartPoint=
      firstHomeTrip?0:Number(translateStart);

    const alignmentStart=
      firstHomeTrip
        ? firstHomeTranslationCompleteEnd
        : Number(translationComplete);

    const rotationEndPoint=
      firstHomeTrip
        ? alignmentStart
        : Number(translate90);

    const targetRotation=
      Number.isFinite(Number(destination?.aladinRotation))
        ? Number(destination.aladinRotation)
        : 0;

    const rotationDelta=
      flightNormalizeRotationDelta(
        targetRotation-Number(rotationStart)
      );

    let destinationCenterApplied=false;
    let finalRotationApplied=false;
    let lastAladinSample=-1;
    let lastBlackBoxSample=-1;

    const started=performance.now();

    emitTrace(4658,'RAF_SETUP_COMPLETE',{
      destinationRA,
      destinationDec,
      destinationFov:finalFov,
      targetRotation,
      duration,
      rotationStartPoint,
      alignmentStart,
      translateStart:Number(translateStart),
      translationComplete:Number(translationComplete),
      travelSeconds:Number(
        firstHomeTrip?firstHomeTravelSeconds:travelSeconds
      ),
      aladinTravelHz:Number(aladinTravelHz)
    });

    try{
      global.dispatchEvent(new CustomEvent('gv-black-box-nav-start',{detail:{
        moduleVersion:VERSION,
        firstHomeTrip:Boolean(firstHomeTrip),
        startedPerfMs:started,
        durationMs:duration,
        source:{
          name:String(source?.name||''),
          ra:Number(source?.ra),
          dec:Number(source?.dec)
        },
        destination:{
          name:String(destination?.name||''),
          ra:destinationRA,
          dec:destinationDec,
          fov:finalFov,
          rotation:targetRotation
        },
        start:{
          ra:Number(startRA),
          dec:Number(startDec),
          fov:startFovNumber,
          rotation:Number(rotationStart)
        },
        choreography:{
          travelSeconds:Number(
            firstHomeTrip?firstHomeTravelSeconds:travelSeconds
          ),
          maxFov:Number(maxFov),
          translateStart:Number(translateStart),
          translate90:Number(translate90),
          translationComplete:Number(translationComplete),
          rotationStartPoint:Number(rotationStartPoint),
          rotationEndPoint:Number(rotationEndPoint)
        }
      }}));
    }catch(_){}

    await new Promise((resolve,reject)=>{
      const frame=(now)=>{
        try{
          const t=Math.min(1,(now-started)/duration);
          emitTrace(4662,'RAF_FRAME_EXECUTED',{t,now});

          const aladinSample=
            Math.floor((now-started)*Number(aladinTravelHz)/1000);

          if(t<1&&aladinSample!==lastAladinSample){
            const alignmentProgress=
              firstHomeTrip
                ? 0
                : (
                    t<=alignmentStart
                      ? 0
                      : flightSmootherstep(
                          (t-alignmentStart)/(1-alignmentStart)
                        )
                  );

            let currentFov;

            if(firstHomeTrip){
              if(t<=firstHomeTranslationCompleteEnd){
                currentFov=startFovNumber;
              }else{
                const leg2Progress=
                  flightSmootherstep(
                    flightClamp01(
                      (t-firstHomeTranslationCompleteEnd)/
                      Math.max(
                        1-firstHomeTranslationCompleteEnd,
                        .000001
                      )
                    )
                  );

                currentFov=Math.exp(
                  Math.log(startFovNumber)+
                  (
                    Math.log(finalFov)-
                    Math.log(startFovNumber)
                  )*leg2Progress
                );
              }
            }else{
              currentFov=flightFovAt(
                t,
                startFovNumber,
                finalFov,
                Number(maxFov),
                false
              );
            }

            emitTrace(4690,'RAF_SET_FOV',{t,currentFov});
            commandSetFov(aladin,currentFov);

            if(firstHomeTrip){
              if(t<firstHomeTranslationCompleteEnd){
                const translationProgress=
                  flightSmootherstep(
                    flightClamp01(
                      t/
                      Math.max(
                        firstHomeTranslationCompleteEnd,
                        .000001
                      )
                    )
                  );

                const pos=flightGreatCirclePosition(
                  Number(startRA),
                  Number(startDec),
                  destinationRA,
                  destinationDec,
                  translationProgress
                );

                global.GalaxyBlackBox?.recordCheckpoint?.(
                  'FINAL_GOTO_BEGIN',
                  {t:Number(t),ra:destinationRA,dec:destinationDec}
                );

                commandGotoRaDec(aladin,pos[0],pos[1]);
              }else if(!destinationCenterApplied){
                global.GalaxyBlackBox?.recordCheckpoint?.(
                  'FINAL_GOTO_BEGIN',
                  {t:Number(t),ra:destinationRA,dec:destinationDec}
                );
                commandGotoRaDec(aladin,destinationRA,destinationDec);
                destinationCenterApplied=true;
              }
            }else{
              const translationProgress=
                flightTranslationProgress(t);

              if(
                translationProgress>0 &&
                !destinationCenterApplied &&
                alignmentProgress<=0
              ){
                const pos=flightGreatCirclePosition(
                  Number(startRA),
                  Number(startDec),
                  destinationRA,
                  destinationDec,
                  translationProgress
                );

                global.GalaxyBlackBox?.recordCheckpoint?.(
                  'FINAL_GOTO_BEGIN',
                  {t:Number(t),ra:destinationRA,dec:destinationDec}
                );

                commandGotoRaDec(aladin,pos[0],pos[1]);
              }

              if(translationProgress>=1)
                destinationCenterApplied=true;
            }

            if(
              t>=rotationStartPoint &&
              t<rotationEndPoint &&
              Number.isFinite(targetRotation) &&
              typeof aladin.setRotation==='function'
            ){
              const rotationProgress=
                firstHomeTrip
                  ? flightSmootherstep(
                      (t-rotationStartPoint)/
                      (rotationEndPoint-rotationStartPoint)
                    )
                  : flightClamp01(
                      (t-rotationStartPoint)/
                      (rotationEndPoint-rotationStartPoint)
                    );

              commandSetRotation(
                aladin,
                Number(rotationStart)+
                rotationDelta*rotationProgress
              );
            }else if(
              !finalRotationApplied &&
              t>=rotationEndPoint &&
              Number.isFinite(targetRotation) &&
              typeof aladin.setRotation==='function'
            ){
              commandSetRotation(aladin,targetRotation);
              finalRotationApplied=true;
            }

            if(
              !firstHomeTrip &&
              !destinationCenterApplied &&
              alignmentProgress>0
            ){
              global.GalaxyBlackBox?.recordCheckpoint?.(
                'FINAL_GOTO_BEGIN',
                {t:Number(t),ra:destinationRA,dec:destinationDec}
              );
              commandGotoRaDec(aladin,destinationRA,destinationDec);
            }

            const blackBoxSample=
              Math.floor((now-started)*4/1000);

            if(blackBoxSample!==lastBlackBoxSample){
              lastBlackBoxSample=blackBoxSample;
              try{
                const actualCoords=
                  typeof aladin.getRaDec==='function'
                    ? aladin.getRaDec()
                    : null;
                const actualFov=
                  typeof aladin.getFov==='function'
                    ? aladin.getFov()
                    : null;
                const actualRotation=
                  typeof aladin.getRotation==='function'
                    ? aladin.getRotation()
                    : null;

                const translationProgress=
                  firstHomeTrip
                    ? (
                        t<firstHomeTranslationCompleteEnd
                          ? flightSmootherstep(
                              flightClamp01(
                                t/Math.max(
                                  firstHomeTranslationCompleteEnd,
                                  .000001
                                )
                              )
                            )
                          : 1
                      )
                    : flightTranslationProgress(t);

                const phase=
                  firstHomeTrip
                    ? (
                        t<firstHomeTranslationCompleteEnd
                          ? 'FIRST_HOME_TRANSLATE_ROTATE'
                          : 'FIRST_HOME_ZOOM'
                      )
                    : (
                        t<=4/15
                          ? 'ZOOM_OUT'
                          : t<=11/30
                            ? 'ACCEL_TRANSLATE_ZOOM_OUT'
                            : t<=19/30
                              ? 'CRUISE_ROTATE'
                              : t<=11/15
                                ? 'DECEL_TRANSLATE_ZOOM_IN'
                                : 'ZOOM_IN_ONLY'
                      );

                let commandedRotation=Number(rotationStart);

                if(t>=rotationEndPoint){
                  commandedRotation=targetRotation;
                }else if(t>=rotationStartPoint){
                  const rp=
                    firstHomeTrip
                      ? flightSmootherstep(
                          (t-rotationStartPoint)/
                          (rotationEndPoint-rotationStartPoint)
                        )
                      : flightClamp01(
                          (t-rotationStartPoint)/
                          (rotationEndPoint-rotationStartPoint)
                        );

                  commandedRotation=
                    Number(rotationStart)+rotationDelta*rp;
                }

                global.dispatchEvent(
                  new CustomEvent(
                    'gv-black-box-nav-sample',
                    {detail:{
                      moduleVersion:VERSION,
                      elapsedMs:now-started,
                      t,
                      translationProgress,
                      phase,
                      commandedFov:Number(currentFov),
                      commandedRotation,
                      actualRa:
                        Array.isArray(actualCoords)
                          ? Number(actualCoords[0])
                          : null,
                      actualDec:
                        Array.isArray(actualCoords)
                          ? Number(actualCoords[1])
                          : null,
                      actualFov:
                        Number.isFinite(Number(actualFov))
                          ? Number(actualFov)
                          : null,
                      actualRotation:
                        Number.isFinite(Number(actualRotation))
                          ? Number(actualRotation)
                          : null,
                      destinationCenterApplied:
                        Boolean(destinationCenterApplied),
                      finalRotationApplied:
                        Boolean(finalRotationApplied)
                    }}
                  )
                );
              }catch(_){}
            }

            lastAladinSample=aladinSample;
          }

          if(typeof onDistanceProgress==='function')
            onDistanceProgress(
              Number(routeValue)*flightDistanceProgress(t)
            );

          if(typeof onTimelineProgress==='function')
            onTimelineProgress(t);

          if(t<1){
            requestAnimationFrame(frame);
            return;
          }

          if(
            !finalRotationApplied &&
            Number.isFinite(targetRotation) &&
            typeof aladin.setRotation==='function'
          ){
            commandSetRotation(aladin,targetRotation);
            finalRotationApplied=true;
          }

          if(!firstHomeTrip){
            global.GalaxyBlackBox?.recordCheckpoint?.(
              'FINAL_GOTO_BEGIN',
              {t:Number(t),ra:destinationRA,dec:destinationDec}
            );
            commandGotoRaDec(aladin,destinationRA,destinationDec);
          }

          global.GalaxyBlackBox?.recordCheckpoint?.(
            'FINAL_GOTO_END',
            {t:Number(t)}
          );

          commandSetFov(aladin,finalFov);

          global.GalaxyBlackBox?.recordCheckpoint?.(
            'FINAL_FOV_DONE',
            {t:Number(t),fov:finalFov}
          );

          if(typeof onDistanceProgress==='function')
            onDistanceProgress(Number(routeValue));

          if(typeof onTimelineProgress==='function')
            onTimelineProgress(1);

          resolve();

        }catch(error){
          emitTraceError(4775,'RAF_EXCEPTION',error);

          try{
            global.dispatchEvent(
              new CustomEvent(
                'gv-black-box-nav-error',
                {detail:{
                  moduleVersion:VERSION,
                  endedPerfMs:performance.now(),
                  elapsedMs:performance.now()-started,
                  durationMs:duration,
                  firstHomeTrip:Boolean(firstHomeTrip),
                  destination:{
                    name:String(destination?.name||''),
                    ra:destinationRA,
                    dec:destinationDec
                  },
                  error:{
                    name:String(error?.name||'Error'),
                    message:String(
                      error?.message||error||'Unknown error'
                    ),
                    stack:String(error?.stack||'')
                  }
                }}
              )
            );
          }catch(_){}

          reject(error);
        }
      };

      requestAnimationFrame(frame);
    });

    try{
      global.dispatchEvent(
        new CustomEvent(
          'gv-black-box-nav-finish',
          {detail:{
            moduleVersion:VERSION,
            endedPerfMs:performance.now(),
            elapsedMs:performance.now()-started,
            durationMs:duration,
            firstHomeTrip:Boolean(firstHomeTrip),
            destination:{
              name:String(destination?.name||''),
              ra:destinationRA,
              dec:destinationDec
            }
          }}
        )
      );
    }catch(_){}

    global.GalaxyBlackBox?.recordCheckpoint?.(
      'NAV_FINISH_DISPATCHED',
      {elapsedMs:performance.now()-started}
    );

    return Object.freeze({
      durationMs:duration,
      destinationCenterApplied:Boolean(destinationCenterApplied),
      finalRotationApplied:Boolean(finalRotationApplied)
    });
  }

  // Navigation 0004 is the sole owner of active-viewer motion commands.
  function commandGotoRaDec(aladin,ra,dec){
    if(!aladin || typeof aladin.gotoRaDec !== 'function')
      throw new Error('NAVIGATION 0004 gotoRaDec UNAVAILABLE');
    aladin.gotoRaDec(ra,dec);
  }

  function commandSetFov(aladin,fov){
    if(!aladin || typeof aladin.setFov !== 'function')
      throw new Error('NAVIGATION 0004 setFov UNAVAILABLE');
    aladin.setFov(fov);
  }

  function commandSetRotation(aladin,rotation){
    if(!aladin || typeof aladin.setRotation !== 'function')
      throw new Error('NAVIGATION 0004 setRotation UNAVAILABLE');
    aladin.setRotation(rotation);
  }

  global.GalaxyViewerNavigation=Object.freeze({
    VERSION,
    CONSTANTS,
    commandGotoRaDec,
    commandSetFov,
    commandSetRotation,
    flyViewport,
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
