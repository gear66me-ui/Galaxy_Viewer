/*
 * GALAXY VIEWER — RANDOM NAVIGATION MODULE 0018
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
 *   Bootstrap trip:         7.5 seconds
 *   Normal trip:              17 seconds
 *   Birdseye FOV:             120 degrees
 *
 * IMPORTANT
 *   This module plans metadata only.
 *   It does not download/decode images and does not own Random Galaxy UI,
 *   history, HD preload, archive preload, or Aladin preparation.
 */

(function(global){
  'use strict';

  const VERSION='0018';

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

    BOOTSTRAP_TRAVEL_SECONDS: 7.5,
    NORMAL_TRAVEL_SECONDS: 17,
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
    const value=finite(
      record?.fovDegrees ??
      record?.fieldOfViewDegrees
    );
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


  const NAVIGATION_WORKER_VERSION='0007';
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
        'NAVIGATION 0012 WORKER BASE URL UNAVAILABLE'
      );

    return new URL(
      'gv-navigation-worker-0007.js',
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
          new Error('NAVIGATION 0012 WORKER TIMEOUT')
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
              'NAVIGATION 0012 WORKER RESULT INVALID'
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
            `NAVIGATION 0012 WORKER ERROR: ${
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
        'NAVIGATION 0012 WORKER ROUTE MATERIALIZATION FAILURE'
      );
    }

    const route=routeMeta.map(item=>item.record);

    const anchor=anchorRecord
      ? normalizeRecord(anchorRecord)
      : null;

    const validation=validateRoute(routeMeta,anchor);

    if(!validation.ok){
      throw new Error(
        `NAVIGATION 0012 WORKER ROUTE VALIDATION FAILURE: ${
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
      // Rolling Monte Carlo buffer.
      this.refillPlan=null;
      this.refillPromise=null;
      this.refillError=null;
    }

    async solvePlan(anchorRecord=null){
      if(typeof Worker==='function' && this.rng===Math.random){
        const result=await solvePlanInWorker(this.catalog,anchorRecord);
        return materializeWorkerPlan(result,this.catalog,anchorRecord);
      }
      return planRoute(this.catalog,{anchorRecord,rng:this.rng});
    }

    async initialize(anchorRecord=null){
      this.plan=await this.solvePlan(anchorRecord);
      this.cursor=0;
      this.refillPlan=null;
      this.refillPromise=null;
      this.refillError=null;
      this.startRefill();
      return this.getState();
    }

    refillAnchor(){
      if(!this.plan?.route?.length)return null;
      return this.plan.route[this.plan.route.length-1] ?? null;
    }

    startRefill(){
      if(!this.plan || this.refillPlan || this.refillPromise)
        return this.refillPromise;

      const anchor=this.refillAnchor();
      if(!anchor)return null;

      this.refillError=null;
      this.refillPromise=this.solvePlan(anchor)
        .then(plan=>{
          this.refillPlan=plan;
          this.refillError=null;
          return plan;
        })
        .catch(error=>{
          this.refillPlan=null;
          this.refillError=error;
          console.error('NAVIGATION 0018 REFILL PLAN FAILURE',error);
          return null;
        })
        .finally(()=>{this.refillPromise=null;});

      return this.refillPromise;
    }

    promoteRefill(){
      if(!this.refillPlan)return false;

      const oldLast=this.plan?.routeMeta?.[this.plan.routeMeta.length-1] ?? null;
      const nextFirst=this.refillPlan?.routeMeta?.[0] ?? null;

      if(!oldLast || !nextFirst)
        throw new Error('NAVIGATION 0018 REFILL HANDOFF METADATA MISSING');

      const boundary=compatibility(oldLast,nextFirst);
      if(!boundary.compatible)
        throw new Error(
          'NAVIGATION 0018 REFILL HANDOFF INVALID: '+
          `travel=${boundary.travelDeg.toFixed(3)}deg `+
          `fov=${boundary.fovDeltaOctaves.toFixed(3)}oct`
        );

      this.plan=this.refillPlan;
      this.cursor=0;
      this.refillPlan=null;
      this.refillError=null;
      this.startRefill();
      return true;
    }

    ensureReadablePlan(){
      if(this.remaining()>0)return true;
      return this.promoteRefill();
    }

    peekNext(){
      this.ensureReadablePlan();
      return this.plan?.route?.[this.cursor] ?? null;
    }

    peekNextMeta(){
      this.ensureReadablePlan();
      return this.plan?.routeMeta?.[this.cursor] ?? null;
    }

    getUpcoming(count=10){
      const wanted=Math.max(0,Number(count)||0);
      if(!wanted)return [];

      this.ensureReadablePlan();
      if(!this.plan)return [];

      const active=this.plan.route.slice(this.cursor,this.cursor+wanted);

      if(active.length<wanted && this.refillPlan){
        active.push(...this.refillPlan.route.slice(0,wanted-active.length));
      }
      return active;
    }

    commitNext(expectedRecord=null){
      if(!this.plan)throw new Error('NAVIGATION NOT INITIALIZED');

      this.ensureReadablePlan();
      const current=this.plan?.routeMeta?.[this.cursor];

      if(!current)
        throw new Error(
          this.refillPromise
            ? 'NAVIGATION ROUTE EXHAUSTED — REFILL PENDING'
            : 'NAVIGATION ROUTE EXHAUSTED — REFILL UNAVAILABLE'
        );

      if(expectedRecord && identityOf(expectedRecord)!==current.key)
        throw new Error('NAVIGATION COMMIT IDENTITY MISMATCH');

      this.cursor++;
      if(this.remaining()===0)this.promoteRefill();
      return this.getState();
    }

    remaining(){
      return this.plan ? Math.max(0,this.plan.routeLength-this.cursor) : 0;
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
        refillReady:Boolean(this.refillPlan),
        refillPending:Boolean(this.refillPromise),
        refillFailed:Boolean(this.refillError),
        bootstrapTravelSeconds:CONSTANTS.BOOTSTRAP_TRAVEL_SECONDS,
        normalTravelSeconds:CONSTANTS.NORMAL_TRAVEL_SECONDS,
        birdseyeFovDeg:CONSTANTS.BIRDSEYE_FOV_DEG
      });
    }

    getPlan(){return this.plan;}
    getRefillPlan(){return this.refillPlan;}
  }

  // ==========================================================
  // ACTIVE VIEWPORT FLIGHT ENGINE — NAVIGATION 0018
  // Restored exact 12AR continuous choreography. No ellipse, no tangent solver,
  // no travel-plane state equations. Navigation is the sole visible-camera owner.
  // ==========================================================

  function flightClamp01(value){
    return Math.max(0,Math.min(1,Number(value)));
  }

  function flightNavigationSmootherstep(value){const t=flightClamp01(value);return 35*t**4-84*t**5+70*t**6-20*t**7;}

  function flightSmootherstep(value){
    const t=flightClamp01(value);
    return t*t*t*(t*(t*6-15)+10);
  }

  function flightNormalizeRotationDelta(value){
    let angle=Number(value)||0;
    while(angle>180)angle-=360;
    while(angle<=-180)angle+=360;
    return angle;
  }

  function flightGreatCirclePosition(ra1,dec1,ra2,dec2,progress){
    const d2r=Math.PI/180,r2d=180/Math.PI;
    const toVec=(ra,dec)=>{
      const r=Number(ra)*d2r,d=Number(dec)*d2r,cd=Math.cos(d);
      return [cd*Math.cos(r),cd*Math.sin(r),Math.sin(d)];
    };
    const a=toVec(ra1,dec1),b=toVec(ra2,dec2);
    const dot=Math.max(-1,Math.min(1,a[0]*b[0]+a[1]*b[1]+a[2]*b[2]));
    const omega=Math.acos(dot),u=flightClamp01(progress);
    let v;
    if(omega<1e-9){
      v=b;
    }else{
      const so=Math.sin(omega);
      const w0=Math.sin((1-u)*omega)/so,w1=Math.sin(u*omega)/so;
      v=[w0*a[0]+w1*b[0],w0*a[1]+w1*b[1],w0*a[2]+w1*b[2]];
    }
    let ra=Math.atan2(v[1],v[0])*r2d;
    if(ra<0)ra+=360;
    const dec=Math.atan2(v[2],Math.hypot(v[0],v[1]))*r2d;
    return [ra,dec];
  }

  function flightLogLerp(a,b,u){
    const x=Math.max(Number(a),1e-12),y=Math.max(Number(b),1e-12);
    const t=flightClamp01(u);
    return Math.exp(Math.log(x)+(Math.log(y)-Math.log(x))*t);
  }

  function flightRaDecToUnitXYZ(ra,dec){
    const r=Number(ra)*Math.PI/180,d=Number(dec)*Math.PI/180;
    if(!Number.isFinite(r)||!Number.isFinite(d))return null;
    const cd=Math.cos(d);
    return [cd*Math.cos(r),cd*Math.sin(r),Math.sin(d)];
  }

  let activeFlightControl=null;

  function abortActiveFlight(reason='external-abort'){
    const control=activeFlightControl;
    if(!control || control.settled || control.aborted)return false;
    control.aborted=true;
    control.reason=String(reason||'external-abort');
    try{global.GalaxyBlackBox?.recordCheckpoint?.('NAV_ABORT_REQUESTED',{reason:control.reason});}catch(_){}
    return true;
  }

  function flightStateAt(sec,{firstHomeTrip,startFov,finalFov,maxFov,startRotation,targetRotation}){
    const duration=firstHomeTrip?7.5:17;
    const t=flightClamp01((Math.max(0,Number(sec)||0))/duration);
    if(firstHomeTrip){
      const translationEnd=flightClamp01(4/duration);
      if(t<translationEnd){
        const p=flightSmootherstep(t/translationEnd);
        return {phase:'12AR_FIRST_TRANSLATE_ROTATE',translation:p,fov:startFov,rotation:startRotation+flightNormalizeRotationDelta(targetRotation-startRotation)*p};
      }
      const p=flightSmootherstep((t-translationEnd)/Math.max(1-translationEnd,0.000001));
      return {phase:'12AR_FIRST_FINAL_ZOOM',translation:1,fov:flightLogLerp(startFov,finalFov,p),rotation:targetRotation};
    }
    const translateStart=0.30;
    const translationComplete=0.70;
    let translation;
    if(t<=translateStart)translation=0;
    else if(t>=translationComplete)translation=1;
    else translation=flightNavigationSmootherstep((t-translateStart)/(translationComplete-translateStart));
    let fov;
    if(t<=0.50){const p=flightNavigationSmootherstep(t/0.50);fov=flightLogLerp(startFov,maxFov,p);}
    else{const p=flightNavigationSmootherstep((t-0.50)/0.50);fov=flightLogLerp(maxFov,finalFov,p);}
    const rotation=startRotation+flightNormalizeRotationDelta(targetRotation-startRotation)*translation;
    return {phase:'12AR_CONTINUOUS_TRIP',translation,fov,rotation};
  }

  async function flyViewport({
    aladin,source,destination,routeValue=0,startRA,startDec,startFov,destinationFov,
    firstHomeTrip=false,travelSeconds=CONSTANTS.NORMAL_TRAVEL_SECONDS,
    firstHomeTravelSeconds=CONSTANTS.BOOTSTRAP_TRAVEL_SECONDS,maxFov=CONSTANTS.BIRDSEYE_FOV_DEG,
    rotationStart=0,aladinTravelHz=15,onDistanceProgress=null,onTimelineProgress=null,trace=null,traceError=null
  }={}){
    if(!aladin)throw new Error('NAVIGATION 0018 ALADIN INSTANCE MISSING');
    const destinationRA=Number(destination?.ra),destinationDec=Number(destination?.dec);
    const finalFov=Number(destinationFov),startFovNumber=Number(startFov);
    if(!Number.isFinite(startFovNumber)||startFovNumber<=0)throw new Error('CURRENT ALADIN FOV IS INVALID');
    if(!Number.isFinite(finalFov)||finalFov<=0)throw new Error('DESTINATION ALADIN FOV IS INVALID');
    if(!Number.isFinite(destinationRA)||!Number.isFinite(destinationDec))throw new Error('DESTINATION COORDINATES ARE INVALID');

    const emitTrace=(code,label,detail)=>{try{if(typeof trace==='function')trace(code,label,detail);}catch(_){}};
    const emitTraceError=(code,label,error)=>{try{if(typeof traceError==='function')traceError(code,label,error);}catch(_){}};
    const durationSeconds=Number(firstHomeTrip?7.5:17),duration=durationSeconds*1000;
    const targetRotation=Number(destination?.aladinRotation);
    if(!Number.isFinite(targetRotation))throw new Error('DESTINATION aladinRotation IS REQUIRED FOR RANDOM GALAXY TRAVEL');
    let measuredRotation=NaN;
    try{measuredRotation=Number(aladin.getRotation?.());}catch(_){}
    const actualStartRotation=Number.isFinite(measuredRotation)?measuredRotation:Number(rotationStart)||0;

    let destinationCenterApplied=false,finalRotationApplied=false,zoomInRotationGuardChecked=false,lastAladinSample=-1,lastBlackBoxSample=-1;
    let lastCommandedRA=Number(startRA),lastCommandedDec=Number(startDec);
    const flightControl={aborted:false,reason:'',settled:false};
    if(activeFlightControl && !activeFlightControl.settled)throw new Error('NAVIGATION 0018 ACTIVE FLIGHT ALREADY EXISTS');
    activeFlightControl=flightControl;
    const started=performance.now();

    try{global.dispatchEvent(new CustomEvent('gv-black-box-nav-start',{detail:{
      moduleVersion:VERSION,firstHomeTrip:Boolean(firstHomeTrip),startedPerfMs:started,durationMs:duration,
      source:{name:String(source?.name||''),ra:Number(source?.ra),dec:Number(source?.dec)},
      destination:{name:String(destination?.name||''),ra:destinationRA,dec:destinationDec,fov:finalFov,rotation:targetRotation},
      start:{ra:Number(startRA),dec:Number(startDec),fov:startFovNumber,rotation:actualStartRotation},
      choreography:firstHomeTrip
        ? {geometry:'12AR_FIRST_TRANSLATE_ROTATE_THEN_ZOOM',translateRotateSeconds:4,finalZoomSeconds:3.5,translationEndFraction:4/7.5}
        : {geometry:'12AR_CONTINUOUS_SYMMETRIC',fovApexFraction:0.50,translateStartFraction:0.30,translateEndFraction:0.70,easing:'S7'}
    }}));}catch(_){}

    await new Promise((resolve,reject)=>{
      const frame=(now)=>{
        try{
if(flightControl.aborted){
  const error=new Error(`NAVIGATION 0018 ABORTED: ${flightControl.reason||'external-abort'}`);
  error.name='AbortError'; reject(error); return;
}
const elapsedMs=now-started,t=Math.min(1,elapsedMs/duration),sec=t*durationSeconds;
const sample=Math.floor(elapsedMs*Number(aladinTravelHz)/1000);
if(t<1 && sample!==lastAladinSample){
  const state=flightStateAt(sec,{firstHomeTrip,startFov:startFovNumber,finalFov,maxFov:Number(maxFov),startRotation:actualStartRotation,targetRotation});
  const zoomInStartFraction=firstHomeTrip?(4/durationSeconds):0.50;
  if(!zoomInRotationGuardChecked && t>=zoomInStartFraction){
    const currentSpecRotation=Number(destination?.aladinRotation);
    if(!Number.isFinite(currentSpecRotation) || Math.abs(flightNormalizeRotationDelta(currentSpecRotation-targetRotation))>1e-9)
      throw new Error('DESTINATION aladinRotation CHANGED OR INVALID BEFORE ZOOM IN');
    zoomInRotationGuardChecked=true;
    emitTrace(4780,'ROTATION_SPEC_PRE_ZOOM_IN_OK',{targetRotation,currentSpecRotation});
  }
  commandSetFov(aladin,state.fov);

  if(state.translation>0 && state.translation<1){
    const pos=flightGreatCirclePosition(startRA,startDec,destinationRA,destinationDec,state.translation);
    lastCommandedRA=Number(pos[0]); lastCommandedDec=Number(pos[1]);
    commandGotoRaDec(aladin,lastCommandedRA,lastCommandedDec);
  }else if(state.translation>=1 && !destinationCenterApplied){
    lastCommandedRA=destinationRA; lastCommandedDec=destinationDec;
    commandGotoRaDec(aladin,destinationRA,destinationDec);
    destinationCenterApplied=true;
  }

  if(Number.isFinite(state.rotation) && typeof aladin.setRotation==='function'){
    commandSetRotation(aladin,state.rotation);
    if(Math.abs(flightNormalizeRotationDelta(targetRotation-state.rotation))<0.01)finalRotationApplied=true;
  }

  const bbSample=Math.floor(elapsedMs*Number(aladinTravelHz)/1000);
  if(bbSample!==lastBlackBoxSample){
    lastBlackBoxSample=bbSample;
    let actualCoords=null,actualFov=null,actualRotation=null;
    try{actualCoords=aladin.getRaDec?.();}catch(_){}
    try{actualFov=aladin.getFov?.();}catch(_){}
    try{actualRotation=aladin.getRotation?.();}catch(_){}
    const commandedXYZ=flightRaDecToUnitXYZ(lastCommandedRA,lastCommandedDec);
    const actualXYZ=Array.isArray(actualCoords)?flightRaDecToUnitXYZ(Number(actualCoords[0]),Number(actualCoords[1])):null;
    try{global.dispatchEvent(new CustomEvent('gv-black-box-nav-sample',{detail:{
      moduleVersion:VERSION,elapsedMs,t,translationProgress:state.translation,phase:state.phase,
      commandedFov:Number(state.fov),commandedRotation:Number(state.rotation),
      commandedRa:Number(lastCommandedRA),commandedDec:Number(lastCommandedDec),
      commandedSkyX:commandedXYZ?.[0]??null,commandedSkyY:commandedXYZ?.[1]??null,commandedSkyZ:commandedXYZ?.[2]??null,
      actualSkyX:actualXYZ?.[0]??null,actualSkyY:actualXYZ?.[1]??null,actualSkyZ:actualXYZ?.[2]??null,
      actualRa:Array.isArray(actualCoords)?Number(actualCoords[0]):null,actualDec:Array.isArray(actualCoords)?Number(actualCoords[1]):null,
      actualFov:Number.isFinite(Number(actualFov))?Number(actualFov):null,
      actualRotation:Number.isFinite(Number(actualRotation))?Number(actualRotation):null,
      destinationCenterApplied:Boolean(destinationCenterApplied),finalRotationApplied:Boolean(finalRotationApplied)
    }}));}catch(_){}
  }
  lastAladinSample=sample;
}

if(typeof onDistanceProgress==='function')onDistanceProgress(Number(routeValue)*flightSmootherstep(t));
if(typeof onTimelineProgress==='function')onTimelineProgress(t);
if(t<1){requestAnimationFrame(frame);return;}

if(!destinationCenterApplied){commandGotoRaDec(aladin,destinationRA,destinationDec);destinationCenterApplied=true;}
commandSetFov(aladin,finalFov);
const finalSpecRotation=Number(destination?.aladinRotation);
if(!Number.isFinite(finalSpecRotation) || Math.abs(flightNormalizeRotationDelta(finalSpecRotation-targetRotation))>1e-9)
  throw new Error('DESTINATION aladinRotation CHANGED OR INVALID AT FINAL ROTATION COMMIT');
commandSetRotation(aladin,targetRotation);
finalRotationApplied=true;
if(typeof onDistanceProgress==='function')onDistanceProgress(Number(routeValue));
if(typeof onTimelineProgress==='function')onTimelineProgress(1);
resolve();
        }catch(error){emitTraceError(4775,'RAF_EXCEPTION',error);reject(error);}
      };
      requestAnimationFrame(frame);
    });

    flightControl.settled=true;
    if(activeFlightControl===flightControl)activeFlightControl=null;
    try{global.dispatchEvent(new CustomEvent('gv-black-box-nav-finish',{detail:{
      moduleVersion:VERSION,endedPerfMs:performance.now(),elapsedMs:performance.now()-started,durationMs:duration,
      firstHomeTrip:Boolean(firstHomeTrip),destination:{name:String(destination?.name||''),ra:destinationRA,dec:destinationDec}
    }}));}catch(_){}
    return Object.freeze({durationMs:duration,destinationCenterApplied:Boolean(destinationCenterApplied),finalRotationApplied:Boolean(finalRotationApplied)});
  }

  // Navigation 0006 is the sole owner of active-viewer motion commands.
  let lastNavigationCommandedRotation=NaN;
  function commandGotoRaDec(aladin,ra,dec){
    if(!aladin || typeof aladin.gotoRaDec !== 'function')
      throw new Error('NAVIGATION 0018 gotoRaDec UNAVAILABLE');
    aladin.gotoRaDec(ra,dec);
  }

  function commandSetFov(aladin,fov){
    if(!aladin || typeof aladin.setFov !== 'function')
      throw new Error('NAVIGATION 0018 setFov UNAVAILABLE');
    aladin.setFov(fov);
  }

  function commandSetRotation(aladin,rotation){
    if(!aladin || typeof aladin.setRotation !== 'function')
      throw new Error('NAVIGATION 0018 setRotation UNAVAILABLE');
    const commanded=Number(rotation);
    if(!Number.isFinite(commanded))throw new Error('NAVIGATION 0018 ROTATION COMMAND INVALID');
    lastNavigationCommandedRotation=commanded;
    aladin.setRotation(commanded);
    try{global.dispatchEvent(new CustomEvent('gv-navigation-rotation-command',{detail:{moduleVersion:VERSION,rotation:commanded}}));}catch(_){}
  }

  function getLastCommandedRotation(){
    return Number.isFinite(lastNavigationCommandedRotation)?lastNavigationCommandedRotation:null;
  }

  global.GalaxyViewerNavigation=Object.freeze({
    VERSION,
    CONSTANTS,
    commandGotoRaDec,
    commandSetFov,
    commandSetRotation,
    getLastCommandedRotation,
    abortActiveFlight,
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
