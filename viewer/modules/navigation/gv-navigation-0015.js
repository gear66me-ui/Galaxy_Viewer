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

  const VERSION='0015';

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


  const NAVIGATION_WORKER_VERSION='0004';
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
      'gv-navigation-worker-0004.js',
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
  // Navigation 0008 owns trip timing, interpolation, RAF, and
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

  // Explicit source→destination travel plane for Aladin's 2.5-D camera.
  // S and D lie in the plane; N is orthogonal to it; Ts is the source tangent.
  function flightBuildTravelFrame(ra1,dec1,ra2,dec2){
    const d2r=Math.PI/180;
    const toVec=(ra,dec)=>{
      const r=Number(ra)*d2r;
      const d=Number(dec)*d2r;
      const cd=Math.cos(d);
      return [cd*Math.cos(r),cd*Math.sin(r),Math.sin(d)];
    };
    const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    const cross=(a,b)=>[
      a[1]*b[2]-a[2]*b[1],
      a[2]*b[0]-a[0]*b[2],
      a[0]*b[1]-a[1]*b[0]
    ];
    const norm=(v)=>Math.hypot(v[0],v[1],v[2]);
    const unit=(v)=>{const n=norm(v);return n>1e-15?v.map(x=>x/n):null;};
    const S=toVec(ra1,dec1);
    const D=toVec(ra2,dec2);
    const c=Math.max(-1,Math.min(1,dot(S,D)));
    const omega=Math.acos(c);
    if(omega<1e-12){
      return Object.freeze({S,D,N:[0,0,1],Ts:[0,0,0],omega});
    }
    let N=unit(cross(S,D));
    if(!N){
      const ref=Math.abs(S[2])<0.9?[0,0,1]:[0,1,0];
      N=unit(cross(S,ref));
    }
    let Ts=unit(cross(N,S));
    if(dot(Ts,D)<0){
      N=N.map(v=>-v);
      Ts=Ts.map(v=>-v);
    }
    return Object.freeze({S,D,N,Ts,omega});
  }

  function flightTravelFramePosition(frame,progress){
    const r2d=180/Math.PI;
    const s=flightClamp01(progress);
    if(frame.omega<1e-12)return [
      Math.atan2(frame.D[1],frame.D[0])*r2d<0
        ? Math.atan2(frame.D[1],frame.D[0])*r2d+360
        : Math.atan2(frame.D[1],frame.D[0])*r2d,
      Math.atan2(frame.D[2],Math.hypot(frame.D[0],frame.D[1]))*r2d
    ];
    const theta=s*frame.omega;
    const c=Math.cos(theta),q=Math.sin(theta);
    const x=c*frame.S[0]+q*frame.Ts[0];
    const y=c*frame.S[1]+q*frame.Ts[1];
    const z=c*frame.S[2]+q*frame.Ts[2];
    let ra=Math.atan2(y,x)*r2d;
    if(ra<0)ra+=360;
    const dec=Math.atan2(z,Math.hypot(x,y))*r2d;
    return [ra,dec];
  }

  function flightTravelFrameCrossTrackDeg(frame,ra,dec){
    const d2r=Math.PI/180,r2d=180/Math.PI;
    const r=Number(ra)*d2r,d=Number(dec)*d2r,cd=Math.cos(d);
    const p=[cd*Math.cos(r),cd*Math.sin(r),Math.sin(d)];
    const v=Math.max(-1,Math.min(1,p[0]*frame.N[0]+p[1]*frame.N[1]+p[2]*frame.N[2]));
    return Math.asin(v)*r2d;
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

  

    // ==========================================================
    // NAVIGATION 0012 — EXPLICIT TRAVEL-PLANE TRAJECTORY
    //
    // 0.0–3.5 s   zoom-out only, accelerating into vertical tangent
    // 3.5–6.5 s   zoom-out + translation + rotation, tangent to arch peak
    // 6.5–12.0 s  zoom-in + translation + rotation
    // 12.0–15.0 s all-axis slow deceleration into the exact target
    //
    // All normal-trip joins are C1 velocity-continuous.
    // Bootstrap trip remains on its dedicated choreography.
    // ==========================================================

    // ==========================================================
    // NAVIGATION 0012 — EXPLICIT 2.5-D TRAVEL-FRAME CHOREOGRAPHY
    // Spatial geometry = along-track on source/destination plane + log2(FOV).
    // Rotation is orientation only and never a spatial axis.
    // ==========================================================
    function flightHermiteScalar(p0,p1,m0,m1,u){
      const t=flightClamp01(u);
      const t2=t*t;
      const t3=t2*t;
      const h00=2*t3-3*t2+1;
      const h10=t3-2*t2+t;
      const h01=-2*t3+3*t2;
      const h11=t3-t2;
      return h00*Number(p0)+h10*Number(m0)+h01*Number(p1)+h11*Number(m1);
    }

    const FLIGHT_ARCH=Object.freeze({
      T0:0,
      T1:3.5,
      T2:6.5,
      T3:9,
      T4:12,
      T5:15,
      X2:0.30,
      X3:0.65,
      Z1_BELOW_MAX:1.0,
      FINAL_ZOOM_SHARE:0.75,
      VX_CRUISE:0.12,
      VZ_EXIT:0.45,
      VZ_ENTRY:-0.55
    });

    const FLIGHT_BOOTSTRAP=Object.freeze({
      T0:0,
      T1:1.25,
      T2:4.5,
      T3:6,
      T4:9,
      X1:0.10,
      X2:0.62,
      VX1:0.10,
      VX2:0.12,
      VZ2:-0.35,
      VZ3:-0.65,
      FINAL_ZOOM_SHARE:0.70
    });

    function flightHermiteSec(p0,p1,v0,v1,sec,sec0,sec1){
      const dt=Math.max(Number(sec1)-Number(sec0),1e-9);
      const u=flightClamp01((Number(sec)-Number(sec0))/dt);
      return flightHermiteScalar(p0,p1,Number(v0)*dt,Number(v1)*dt,u);
    }

    function flightTerminalProgressSeconds(sec,duration,accelSeconds=2,decelSeconds=2){
      const total=Math.max(Number(duration),1e-9);
      const a=Math.max(0,Math.min(Number(accelSeconds),total));
      const d=Math.max(0,Math.min(Number(decelSeconds),total-a));
      const cruise=Math.max(0,total-a-d);
      const denom=cruise+(a+d)/2;
      const vmax=denom>0?1/denom:1/total;
      const x=Math.max(0,Math.min(Number(sec),total));

      if(x<=a){
        if(a<=1e-9)return 0;
        return flightClamp01(
          vmax*(x/2-(a/(2*Math.PI))*Math.sin(Math.PI*x/a))
        );
      }

      const accelDistance=vmax*a/2;
      if(x<=a+cruise)
        return flightClamp01(accelDistance+vmax*(x-a));

      const u=x-a-cruise;
      if(d<=1e-9)return 1;
      const decelDistance=vmax*(u/2+(d/(2*Math.PI))*Math.sin(Math.PI*u/d));
      return flightClamp01(accelDistance+vmax*cruise+decelDistance);
    }

    function flightDomeLogFov(sec,duration,startFov,destinationFov,maxFov){
      const total=Math.max(Number(duration),1e-9);
      const x=Math.max(0,Math.min(Number(sec),total));
      const half=total/2;
      const z0=Math.log2(Number(startFov));
      const zm=Math.log2(Number(maxFov));
      const z1=Math.log2(Number(destinationFov));
      if(x<=half){
        const u=flightNavigationSmootherstep(x/half);
        return z0+(zm-z0)*u;
      }
      const u=flightNavigationSmootherstep((x-half)/half);
      return zm+(z1-zm)*u;
    }

    function flightArchStateAt(t,startFov,destinationFov,maxFov){
      const sec=flightClamp01(t)*15;
      const x=flightTerminalProgressSeconds(sec,15,2,2);
      const z=flightDomeLogFov(sec,15,startFov,destinationFov,maxFov);
      return Object.freeze({translation:x,fov:2**z,z});
    }

    function flightArchTranslationProgress(t,immediate=false){
      if(immediate)return flightClamp01(t);
      return flightTerminalProgressSeconds(flightClamp01(t)*15,15,2,2);
    }

    function flightArchFovAt(t,startFov,destinationFov,maxFov,immediate=false){
      if(immediate){
        const u=flightClamp01(t);
        return Math.exp(Math.log(startFov)+(Math.log(destinationFov)-Math.log(startFov))*u);
      }
      const sec=flightClamp01(t)*15;
      return 2**flightDomeLogFov(sec,15,startFov,destinationFov,maxFov);
    }

    const BOOTSTRAP_ENTRY=Object.freeze({
      duration:9,
      preAlignEnd:0.6,
      arcStart:1.5,
      tangentTime:7.0,
      finalZoomSeconds:2.0,
      arcStartTranslation:0.10
    });

    function flightBootstrapStateAtSeconds(sec,startFov,destinationFov){
      const {duration,preAlignEnd,arcStart,tangentTime,finalZoomSeconds,arcStartTranslation}=BOOTSTRAP_ENTRY;
      const time=Math.max(0,Math.min(duration,Number(sec)||0));
      const z0=Math.log2(Number(startFov));
      const z1=Math.log2(Number(destinationFov));
      const arcDuration=tangentTime-arcStart;
      const k=Math.PI/(2*arcDuration);
      // Solve the tangency FOV from C1 continuity with the final 2 s
      // straight, constant-deceleration zoom segment.
      const zT=(z1+k*z0)/(1+k);

      if(time<=preAlignEnd){
        return Object.freeze({
          translation:0,
          rotation:0,
          fov:2**z0,
          z:z0,
          phase:'BOOTSTRAP_PREALIGN_ROTATE_ONLY'
        });
      }

      if(time<=arcStart){
        // Pure great-circle translation after camera pre-alignment.
        // Cubic Hermite begins at zero velocity and matches the quarter-
        // ellipse along-track velocity at arc entry.
        const straightDuration=arcStart-preAlignEnd;
        const u=straightDuration>0
          ? flightClamp01((time-preAlignEnd)/straightDuration)
          : 1;
        const vEntry=(1-arcStartTranslation)*Math.PI/(2*arcDuration);
        const m1=vEntry*straightDuration;
        const h01=-2*u*u*u+3*u*u;
        const h11=u*u*u-u*u;
        const translation=arcStartTranslation*h01+m1*h11;
        return Object.freeze({
          translation:flightClamp01(translation),
          rotation:0,
          fov:2**z0,
          z:z0,
          phase:'BOOTSTRAP_STRAIGHT_TRANSLATION'
        });
      }

      if(time<=tangentTime){
        const u=flightClamp01((time-arcStart)/arcDuration);
        const theta=(Math.PI/2)*u;
        // Quarter ellipse in (along-track, log2-FOV) state space:
        // horizontal tangent at arc entry, vertical tangent at arrival.
        const translation=
          arcStartTranslation+
          (1-arcStartTranslation)*Math.sin(theta);
        const z=z0+(zT-z0)*(1-Math.cos(theta));
        const rotation=flightNavigationSmootherstep(u);
        return Object.freeze({
          translation:flightClamp01(translation),
          rotation:flightClamp01(rotation),
          fov:2**z,
          z,
          phase:'BOOTSTRAP_TANGENT_ENTRY_ARC'
        });
      }

      // Final 2 s: destination-centered straight zoom only.
      // Translation and rotation are exactly frozen at 1.0.
      const tau=Math.min(finalZoomSeconds,time-tangentTime);
      const delta=z1-zT;
      const v0=delta; // exact C1 match from the solved tangency condition
      const accel=-v0/finalZoomSeconds;
      const z=zT+v0*tau+0.5*accel*tau*tau;
      return Object.freeze({
        translation:1,
        rotation:1,
        fov:2**z,
        z,
        phase:'BOOTSTRAP_FINAL_STRAIGHT_ZOOM'
      });
    }

    function flightBootstrapStateAt(t,startFov,destinationFov){
      return flightBootstrapStateAtSeconds(
        flightClamp01(t)*BOOTSTRAP_ENTRY.duration,
        startFov,
        destinationFov
      );
    }

    function flightBootstrapTranslationProgress(t){
      return flightBootstrapStateAt(t,1,1).translation;
    }

    function flightBootstrapFovAt(t,startFov,destinationFov){
      return flightBootstrapStateAt(t,startFov,destinationFov).fov;
    }

    function flightRaDecToUnitXYZ(ra,dec){
      const r=Number(ra)*Math.PI/180;
      const d=Number(dec)*Math.PI/180;
      if(!Number.isFinite(r)||!Number.isFinite(d))return null;
      const cd=Math.cos(d);
      return [
        cd*Math.cos(r),
        cd*Math.sin(r),
        Math.sin(d)
      ];
    }
    let activeFlightControl=null;

    function abortActiveFlight(reason='external-abort'){
      const control=activeFlightControl;
      if(!control || control.settled || control.aborted)return false;
      control.aborted=true;
      control.reason=String(reason||'external-abort');
      try{
        global.GalaxyBlackBox?.recordCheckpoint?.('NAV_ABORT_REQUESTED',{reason:control.reason});
      }catch(_){}
      return true;
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
    translateStart=3.5/15,
    translate90=1,
    translationComplete=1,
    rotationStart=0,
    aladinTravelHz=15,
    onDistanceProgress=null,
    onTimelineProgress=null,
    trace=null,
    traceError=null
  }={}){

    if(!aladin)
      throw new Error('NAVIGATION 0015 ALADIN INSTANCE MISSING');

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

    const duration=Number(firstHomeTrip?CONSTANTS.BOOTSTRAP_TRAVEL_SECONDS:travelSeconds)*1000;

    const targetRotation=
      Number.isFinite(Number(destination?.aladinRotation))
        ? Number(destination.aladinRotation)
        : 0;

    const travelFrame=flightBuildTravelFrame(
      Number(startRA),Number(startDec),destinationRA,destinationDec
    );

    let destinationCenterApplied=false;
    let finalRotationApplied=false;
    let lastAladinSample=-1;
    let lastBlackBoxSample=-1;
    const flightControl={aborted:false,reason:'',settled:false};
    if(activeFlightControl && !activeFlightControl.settled)
      throw new Error('NAVIGATION 0015 ACTIVE FLIGHT ALREADY EXISTS');
    activeFlightControl=flightControl;
    let lastCommandedRA=Number(startRA);
    let lastCommandedDec=Number(startDec);

    const started=performance.now();

    emitTrace(4658,'RAF_SETUP_COMPLETE',{
      destinationRA,
      destinationDec,
      destinationFov:finalFov,
      targetRotation,
      duration,
      translateStart:Number(translateStart),
      translationComplete:Number(translationComplete),
      travelSeconds:Number(travelSeconds),
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
          travelSeconds:Number(firstHomeTrip?CONSTANTS.BOOTSTRAP_TRAVEL_SECONDS:travelSeconds),
          maxFov:Number(maxFov),
          translateStart:Number(translateStart),
          translate90:Number(translate90),
          translationComplete:Number(translationComplete),
          bootstrapProfile:{
            durationSeconds:9,
            preAlignEndSeconds:0.6,
            straightTranslationEndSeconds:1.5,
            tangencySeconds:7.0,
            finalStraightZoomSeconds:2.0,
            arcStartTranslation:0.10,
            geometry:'TRAVEL_PLANE_QUARTER_ELLIPSE_C1_NO_TRAVEL_ROTATION'
          },
          arch:{
            translateStart:3.5/15,
            apex:6.5/15,
            translateRotateEnd:9/15,
            translateZoomInEnd:12/15,
            translationAtDecel:0.85,
            translationSlopeAtDecel:1.20,
            fovAscentAtTranslateStart:0.55,
            fovAscentSlopeAtTranslateStart:2.20,
            fovDescentAtDecel:0.80,
            fovDescentSlopeAtDecel:1.20,
            blackBoxHz:Number(aladinTravelHz)
          }
        }
      }}));
    }catch(_){}

    await new Promise((resolve,reject)=>{
      const frame=(now)=>{
        try{
          if(flightControl.aborted){
            const error=new Error(`NAVIGATION 0012 ABORTED: ${flightControl.reason||'external-abort'}`);
            error.name='AbortError';
            error.code='GV_NAV_ABORTED';
            error.reason=flightControl.reason||'external-abort';
            try{
              global.dispatchEvent(new CustomEvent('gv-black-box-nav-abort',{detail:{moduleVersion:VERSION,elapsedMs:now-started,reason:error.reason}}));
            }catch(_){}
            flightControl.settled=true;
            if(activeFlightControl===flightControl)activeFlightControl=null;
            reject(error);
            return;
          }
          const t=Math.min(1,(now-started)/duration);
          emitTrace(4662,'RAF_FRAME_EXECUTED',{t,now});

          const aladinSample=
            Math.floor((now-started)*Number(aladinTravelHz)/1000);

          if(t<1&&aladinSample!==lastAladinSample){

            let currentFov;
            currentFov=firstHomeTrip
              ? flightBootstrapFovAt(t,startFovNumber,finalFov)
              : flightArchFovAt(
                  t,
                  startFovNumber,
                  finalFov,
                  Number(maxFov),
                  false
                );

            emitTrace(4690,'RAF_SET_FOV',{t,currentFov});
            commandSetFov(aladin,currentFov);

            const translationProgress=
              firstHomeTrip
                ? flightBootstrapTranslationProgress(t)
                : flightArchTranslationProgress(t);

            if(
              translationProgress>0 &&
              !destinationCenterApplied
            ){
              const pos=flightTravelFramePosition(travelFrame,translationProgress);

              global.GalaxyBlackBox?.recordCheckpoint?.(
                'FINAL_GOTO_BEGIN',
                {t:Number(t),ra:destinationRA,dec:destinationDec}
              );

              lastCommandedRA=Number(pos[0]);
              lastCommandedDec=Number(pos[1]);
              commandGotoRaDec(
                aladin,
                lastCommandedRA,
                lastCommandedDec
              );
            }

            if(translationProgress>=1)
              destinationCenterApplied=true;

            const blackBoxSample=
              Math.floor(
                (now-started)*
                Number(aladinTravelHz)/
                1000
              );

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

                const commandedXYZ=
                  flightRaDecToUnitXYZ(
                    lastCommandedRA,
                    lastCommandedDec
                  );

                const actualXYZ=
                  Array.isArray(actualCoords)
                    ? flightRaDecToUnitXYZ(
                        Number(actualCoords[0]),
                        Number(actualCoords[1])
                      )
                    : null;

                const actualCrossTrackDeg=
                  Array.isArray(actualCoords)
                    ? flightTravelFrameCrossTrackDeg(
                        travelFrame,Number(actualCoords[0]),Number(actualCoords[1])
                      )
                    : null;

                const translationProgress=
                  firstHomeTrip
                    ? flightBootstrapTranslationProgress(t)
                    : flightArchTranslationProgress(t);

                const phase=firstHomeTrip
                  ? (
                      t<=1.75/9
                        ? 'BOOTSTRAP_ACCEL_TRANSLATE_ZOOM_IN'
                        : t<=5.75/9
                          ? 'BOOTSTRAP_CRUISE_TRANSLATE_ZOOM_IN'
                          : t<=6.5/9
                            ? 'BOOTSTRAP_DECEL_TRANSLATE_ZOOM_IN'
                            : 'BOOTSTRAP_ZOOM_IN_ONLY'
                    )
                  : (
                      t<=2/15
                        ? 'ACCEL_TRANSLATE_ZOOM_OUT'
                        : t<=7.5/15
                          ? 'CRUISE_TRANSLATE_ZOOM_OUT'
                          : t<=13/15
                            ? 'CRUISE_TRANSLATE_ZOOM_IN'
                            : 'DECEL_TRANSLATE_ZOOM_IN'
                    );

                const commandedRotation=Number(rotationStart);

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
                      commandedRa:
                        Number.isFinite(lastCommandedRA)
                          ? lastCommandedRA
                          : null,
                      commandedDec:
                        Number.isFinite(lastCommandedDec)
                          ? lastCommandedDec
                          : null,
                      commandedSkyX:
                        Array.isArray(commandedXYZ)
                          ? Number(commandedXYZ[0])
                          : null,
                      commandedSkyY:
                        Array.isArray(commandedXYZ)
                          ? Number(commandedXYZ[1])
                          : null,
                      commandedSkyZ:
                        Array.isArray(commandedXYZ)
                          ? Number(commandedXYZ[2])
                          : null,
                      commandedStateX:Number(translationProgress),
                      commandedStateY:0,
                      commandedStateZ:Math.log2(Number(currentFov)),
                      travelPlaneCrossTrackDeg:0,
                      actualCrossTrackDeg:Number.isFinite(Number(actualCrossTrackDeg))
                        ? Number(actualCrossTrackDeg)
                        : null,
                      travelAngleDeg:Number(travelFrame.omega*180/Math.PI),
                      actualSkyX:
                        Array.isArray(actualXYZ)
                          ? Number(actualXYZ[0])
                          : null,
                      actualSkyY:
                        Array.isArray(actualXYZ)
                          ? Number(actualXYZ[1])
                          : null,
                      actualSkyZ:
                        Array.isArray(actualXYZ)
                          ? Number(actualXYZ[2])
                          : null,
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

          global.GalaxyBlackBox?.recordCheckpoint?.(
            'FINAL_GOTO_BEGIN',
            {t:Number(t),ra:destinationRA,dec:destinationDec}
          );
          lastCommandedRA=destinationRA;
          lastCommandedDec=destinationDec;
          commandGotoRaDec(
            aladin,
            lastCommandedRA,
            lastCommandedDec
          );

          global.GalaxyBlackBox?.recordCheckpoint?.(
            'FINAL_GOTO_END',
            {t:Number(t)}
          );

          commandSetFov(aladin,finalFov);

          global.GalaxyBlackBox?.recordCheckpoint?.(
            'FINAL_FOV_DONE',
            {t:Number(t),fov:finalFov}
          );

          // CLEAN SHOP 0015: the visible camera has exactly one
          // rotation write per galaxy trip, at completed arrival only.
          if(
            Number.isFinite(targetRotation) &&
            typeof aladin.setRotation==='function'
          ){
            commandSetRotation(aladin,targetRotation);
            finalRotationApplied=true;
            global.GalaxyBlackBox?.recordCheckpoint?.(
              'FINAL_ROTATION_DONE',
              {t:Number(t),rotation:targetRotation}
            );
          }

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

          flightControl.settled=true;
          if(activeFlightControl===flightControl)activeFlightControl=null;
          reject(error);
        }
      };

      requestAnimationFrame(frame);
    });

    flightControl.settled=true;
    if(activeFlightControl===flightControl)activeFlightControl=null;

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

  // Navigation 0006 is the sole owner of active-viewer motion commands.
  function commandGotoRaDec(aladin,ra,dec){
    if(!aladin || typeof aladin.gotoRaDec !== 'function')
      throw new Error('NAVIGATION 0014 gotoRaDec UNAVAILABLE');
    aladin.gotoRaDec(ra,dec);
  }

  function commandSetFov(aladin,fov){
    if(!aladin || typeof aladin.setFov !== 'function')
      throw new Error('NAVIGATION 0014 setFov UNAVAILABLE');
    aladin.setFov(fov);
  }

  function commandSetRotation(aladin,rotation){
    if(!aladin || typeof aladin.setRotation !== 'function')
      throw new Error('NAVIGATION 0015 setRotation UNAVAILABLE');
    aladin.setRotation(rotation);
  }

  global.GalaxyViewerNavigation=Object.freeze({
    VERSION,
    CONSTANTS,
    commandGotoRaDec,
    commandSetFov,
    commandSetRotation,
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
