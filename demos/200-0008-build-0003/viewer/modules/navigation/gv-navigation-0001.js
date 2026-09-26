/*
 * GALAXY VIEWER NAVIGATION MODULE 0001
 * ECO: ECO-20260902-12AR01-NAVIGATION-ADMIN-001C
 * Scope: N=130 metadata-only route planning, validated navigation motion,
 *        travel-time selection, and navigation telemetry.
 */
(function(global){
  'use strict';

  const VERSION='0001';

  // ==================== SECTION 1 — CONSTANTS / ELIGIBILITY ====================
  const CONSTANTS=Object.freeze({
    NAV_BATCH_SIZE:130,
    TRAVEL_TARGET_DEG:95,
    TRAVEL_MIN_DEG:60,
    TRAVEL_MAX_DEG:130,
    TRAVEL_HALF_BAND_DEG:35,
    ROTATION_TARGET_DEG:75,
    ROTATION_MIN_DEG:40,
    ROTATION_MAX_DEG:110,
    ROTATION_HALF_BAND_DEG:35,
    ROUTE_REQUIRED_LENGTH:130,
    ROUTE_RESTART_ATTEMPTS:30,
    BATCH_RESAMPLE_ON_FAILURE:true,
    QUEUE_TARGET:130,
    QUEUE_REFILL_TRIGGER:120,
    MAX_FOV_DEG:237.6,
    TRANSLATE_START:.30,
    FOV_APEX:.50,
    ROTATION_START:.30,
    TRANSLATE_END:.70,
    ROTATION_END:.70,
    ALADIN_COMMAND_GATE_MS:32,
    TELEMETRY_SAMPLE_MS:100,
    TRAVEL_SECONDS_OPTIONS:Object.freeze([17,15,12,9,6])
  });

  const clamp=(v,min,max)=>Math.max(min,Math.min(max,Number(v)));
  const clamp01=v=>clamp(v,0,1);
  const finite=v=>{const n=Number(v);return Number.isFinite(n)?n:null};
  const clean=v=>String(v==null?'':v).replace(/\s+/g,' ').trim();
  const normalizeSigned=x=>((Number(x)+180)%360+360)%360-180;

  function orientationFrom(record){
    for(const value of [record?.aladinRotation,record?.orientationDegrees,record?.orientation,record?.archiveOrientation]){
      const numeric=finite(value);
      if(numeric!==null)return normalizeSigned(numeric);
      const text=clean(value);
      if(!text)continue;
      if(/^north\s+is\s+up$/i.test(text))return 0;
      const match=text.match(/North\s+is\s+([0-9]+(?:\.[0-9]+)?)\s*°?\s*(right|left)\s+of\s+vertical/i);
      if(match){
        const amount=Number(match[1]);
        return normalizeSigned((match[2].toLowerCase()==='left'?-1:1)*amount);
      }
    }
    return null;
  }

  function providerFrom(record){
    return clean(record?.provider||record?.source||record?.catalog||record?.database||record?.telescope);
  }

  function identityOf(record){
    const direct=clean(record?.navigationKey||record?.key||record?.archiveId||record?.id);
    if(direct)return direct.toLowerCase();
    const name=clean(record?.designation||record?.name||record?.title).toLowerCase();
    const provider=providerFrom(record).toLowerCase();
    if(!name)return '';
    return `${provider}|${name}`;
  }

  function normalizeEligibleRecord(record){
    const ra=finite(record?.ra);
    const dec=finite(record?.dec);
    const orientation=orientationFrom(record);
    const provider=providerFrom(record);
    const key=identityOf(record);
    if(!key||ra===null||dec===null||orientation===null||!provider)return null;
    if(ra<0||ra>=360||dec<-90||dec>90)return null;
    return Object.freeze({key,ra,dec,orientation,provider,record});
  }

  function deduplicateEligible(catalog){
    const map=new Map();
    for(const raw of Array.isArray(catalog)?catalog:[]){
      const item=normalizeEligibleRecord(raw);
      if(!item||map.has(item.key))continue;
      map.set(item.key,item);
    }
    return [...map.values()];
  }

  // ==================== SECTION 2 — SKY / ROTATION MATHEMATICS ====================
  function greatCircleDeg(a,b){
    const ra1=a.ra*Math.PI/180,dec1=a.dec*Math.PI/180;
    const ra2=b.ra*Math.PI/180,dec2=b.dec*Math.PI/180;
    const cosD=
      Math.sin(dec1)*Math.sin(dec2)+
      Math.cos(dec1)*Math.cos(dec2)*Math.cos(ra1-ra2);
    return Math.acos(clamp(cosD,-1,1))*180/Math.PI;
  }

  function rotationDeltaDeg(a,b){
    return Math.abs(normalizeSigned(Number(b.orientation)-Number(a.orientation)));
  }

  function compatibility(a,b){
    const travelDeg=greatCircleDeg(a,b);
    const rotationDeg=rotationDeltaDeg(a,b);
    return Object.freeze({
      compatible:
        travelDeg>=CONSTANTS.TRAVEL_MIN_DEG&&
        travelDeg<=CONSTANTS.TRAVEL_MAX_DEG&&
        rotationDeg>=CONSTANTS.ROTATION_MIN_DEG&&
        rotationDeg<=CONSTANTS.ROTATION_MAX_DEG,
      travelDeg,
      rotationDeg
    });
  }

  // ==================== SECTION 3 — COMPATIBILITY GRAPH ====================
  function buildGraph(nodes,anchor=null){
    const n=nodes.length;
    const neighbors=Array.from({length:n},()=>[]);
    const edgeTelemetry=new Map();
    for(let i=0;i<n;i++){
      for(let j=i+1;j<n;j++){
        const edge=compatibility(nodes[i],nodes[j]);
        edgeTelemetry.set(`${i}:${j}`,edge);
        if(!edge.compatible)continue;
        neighbors[i].push(j);
        neighbors[j].push(i);
      }
    }
    const anchorCompatible=[];
    if(anchor){
      for(let i=0;i<n;i++){
        const edge=compatibility(anchor,nodes[i]);
        if(edge.compatible)anchorCompatible.push(i);
        edgeTelemetry.set(`A:${i}`,edge);
      }
    }
    return {nodes,neighbors,edgeTelemetry,anchorCompatible};
  }

  function isConnected(graph){
    if(!graph.nodes.length)return false;
    const seen=new Set([0]);
    const stack=[0];
    while(stack.length){
      const node=stack.pop();
      for(const next of graph.neighbors[node]){
        if(seen.has(next))continue;
        seen.add(next);stack.push(next);
      }
    }
    return seen.size===graph.nodes.length;
  }

  function graphStats(graph){
    const degrees=graph.neighbors.map(x=>x.length);
    const total=degrees.reduce((a,b)=>a+b,0);
    return Object.freeze({
      minDegree:degrees.length?Math.min(...degrees):0,
      meanDegree:degrees.length?total/degrees.length:0,
      maxDegree:degrees.length?Math.max(...degrees):0,
      connected:isConnected(graph),
      zeroDegreeCount:degrees.filter(x=>x===0).length
    });
  }

  // ==================== SECTION 4 — ROUTE SOLVER ====================
  function shuffled(values,rng=Math.random){
    const copy=[...values];
    for(let i=copy.length-1;i>0;i--){
      const j=Math.floor(rng()*(i+1));
      [copy[i],copy[j]]=[copy[j],copy[i]];
    }
    return copy;
  }

  function solveRoute(graph,{anchor=null,rng=Math.random,restarts=CONSTANTS.ROUTE_RESTART_ATTEMPTS}={}){
    const n=graph.nodes.length;
    if(n!==CONSTANTS.ROUTE_REQUIRED_LENGTH)return null;
    const stats=graphStats(graph);
    if(stats.zeroDegreeCount||!stats.connected)return null;

    const viableStarts=anchor
      ? graph.anchorCompatible
      : graph.nodes.map((_,i)=>i);
    if(!viableStarts.length)return null;

    const rankedStarts=[...viableStarts].sort((a,b)=>graph.neighbors[a].length-graph.neighbors[b].length);
    const lowDegreeBand=rankedStarts.slice(0,Math.max(1,Math.ceil(rankedStarts.length*.25)));

    for(let attempt=0;attempt<restarts;attempt++){
      const start=shuffled(lowDegreeBand,rng)[0];
      const path=[start];
      const used=new Set(path);
      let failed=false;

      while(path.length<n){
        const current=path[path.length-1];
        const candidates=graph.neighbors[current].filter(x=>!used.has(x));
        if(!candidates.length){failed=true;break}

        const scored=candidates.map(next=>{
          let remaining=0;
          for(const option of graph.neighbors[next])if(!used.has(option)&&option!==next)remaining++;
          return {next,remaining,tie:rng()};
        }).sort((a,b)=>a.remaining-b.remaining||a.tie-b.tie);

        const chosen=scored[0].next;
        path.push(chosen);
        used.add(chosen);
      }

      if(!failed&&path.length===n&&new Set(path).size===n){
        if(anchor&&!compatibility(anchor,graph.nodes[path[0]]).compatible)continue;
        return {indices:path,attempt:attempt+1};
      }
    }
    return null;
  }

  function validateRoute(route,anchor=null){
    if(!Array.isArray(route)||route.length!==CONSTANTS.ROUTE_REQUIRED_LENGTH)return {ok:false,reason:'LENGTH'};
    if(new Set(route.map(x=>x.key)).size!==route.length)return {ok:false,reason:'DUPLICATE'};
    const edges=[];
    if(anchor){
      const seam=compatibility(anchor,route[0]);
      if(!seam.compatible)return {ok:false,reason:'SEAM',edge:seam};
      edges.push({from:anchor.key,to:route[0].key,...seam,seam:true});
    }
    for(let i=0;i<route.length-1;i++){
      const edge=compatibility(route[i],route[i+1]);
      if(!edge.compatible)return {ok:false,reason:'EDGE',index:i,edge};
      edges.push({from:route[i].key,to:route[i+1].key,...edge,seam:false});
    }
    return {ok:true,edges};
  }

  // ==================== SECTION 5 — ATOMIC ROUTE QUEUE / REFILL ====================
  class RoutePlanner{
    constructor({catalog,rng=Math.random}={}){
      this.rng=rng;
      this.eligible=deduplicateEligible(catalog);
      this.route=[];
      this.cursor=0;
      this.nextBatch=null;
      this.nextBatchPromise=null;
      this.batchSerial=0;
      this.telemetry=[];
      this.selectedTravelSeconds=17;
      this.activeRun=null;
    }

    async initialize(anchorRecord=null){
      const anchor=anchorRecord?normalizeEligibleRecord(anchorRecord):null;
      this.route=await this.#generateAtomicBatch(anchor);
      this.cursor=0;
      return this.getState();
    }

    async #generateAtomicBatch(anchor=null){
      if(this.eligible.length<CONSTANTS.NAV_BATCH_SIZE)
        throw new Error(`NAVIGATION ELIGIBLE CATALOG TOO SMALL: ${this.eligible.length}`);

      let sampleAttempt=0;
      for(;;){
        sampleAttempt++;
        const sample=shuffled(this.eligible,this.rng).slice(0,CONSTANTS.NAV_BATCH_SIZE);
        const graph=buildGraph(sample,anchor);
        const stats=graphStats(graph);
        if(stats.zeroDegreeCount||!stats.connected)continue;
        const solved=solveRoute(graph,{anchor,rng:this.rng});
        if(!solved)continue;
        const route=solved.indices.map(i=>sample[i]);
        const validation=validateRoute(route,anchor);
        if(!validation.ok)continue;
        const batchId=++this.batchSerial;
        this.telemetry.push(Object.freeze({
          type:'BATCH_COMMITTED',batchId,sampleAttempt,solverAttempt:solved.attempt,
          graph:stats,routeKeys:route.map(x=>x.key),edges:validation.edges
        }));
        return route;
      }
    }

    remaining(){return Math.max(0,this.route.length-this.cursor)}
    peekNext(){return this.route[this.cursor]?.record||null}
    peekNextMeta(){return this.route[this.cursor]||null}

    async ensureRefillPlanning(){
      if(this.remaining()>CONSTANTS.QUEUE_REFILL_TRIGGER||this.nextBatch||this.nextBatchPromise)return;
      const tail=this.route[this.route.length-1]||null;
      this.nextBatchPromise=this.#generateAtomicBatch(tail)
        .then(batch=>{this.nextBatch=batch;return batch})
        .finally(()=>{this.nextBatchPromise=null});
      await this.nextBatchPromise;
    }

    async commitNext(expectedRecord){
      const current=this.route[this.cursor];
      if(!current)throw new Error('NAVIGATION ROUTE EMPTY');
      if(expectedRecord&&identityOf(expectedRecord)!==current.key)
        throw new Error('NAVIGATION COMMIT IDENTITY MISMATCH');
      this.cursor++;
      await this.ensureRefillPlanning();
      if(this.cursor>=this.route.length){
        if(!this.nextBatch)throw new Error('NAVIGATION NEXT BATCH NOT READY');
        this.route=this.nextBatch;
        this.nextBatch=null;
        this.cursor=0;
      }
      return this.getState();
    }

    getUpcoming(count=10){
      return this.route.slice(this.cursor,this.cursor+Math.max(0,Number(count)||0)).map(x=>x.record);
    }

    getState(){
      return Object.freeze({
        version:VERSION,
        remaining:this.remaining(),
        cursor:this.cursor,
        routeLength:this.route.length,
        nextBatchReady:Boolean(this.nextBatch),
        nextBatchPlanning:Boolean(this.nextBatchPromise),
        selectedTravelSeconds:this.selectedTravelSeconds,
        firstTravelSeconds:this.selectedTravelSeconds/2
      });
    }

    // ==================== SECTION 6 — TRAVEL TIMING ====================
    setTravelSeconds(seconds){
      const value=Number(seconds);
      if(!CONSTANTS.TRAVEL_SECONDS_OPTIONS.includes(value))throw new Error('NAVIGATION TRAVEL TIME NOT AUTHORIZED');
      this.selectedTravelSeconds=value;
      return this.getTravelConfig();
    }

    getTravelConfig(){
      return Object.freeze({
        travelSeconds:this.selectedTravelSeconds,
        firstTravelSeconds:this.selectedTravelSeconds/2,
        maxFov:CONSTANTS.MAX_FOV_DEG,
        translateStart:CONSTANTS.TRANSLATE_START,
        fovApex:CONSTANTS.FOV_APEX,
        rotationStart:CONSTANTS.ROTATION_START,
        translateEnd:CONSTANTS.TRANSLATE_END,
        rotationEnd:CONSTANTS.ROTATION_END,
        commandGateMs:CONSTANTS.ALADIN_COMMAND_GATE_MS
      });
    }

    // ==================== SECTION 7 — S7 MOTION MODEL ====================
    s7(x){const t=clamp01(x);return 35*t**4-84*t**5+70*t**6-20*t**7}

    translationProgress(u){
      if(u<=CONSTANTS.TRANSLATE_START)return 0;
      if(u>=CONSTANTS.TRANSLATE_END)return 1;
      return this.s7((u-CONSTANTS.TRANSLATE_START)/(CONSTANTS.TRANSLATE_END-CONSTANTS.TRANSLATE_START));
    }

    fovAt(u,startFov,destinationFov){
      const s=Number(startFov),d=Number(destinationFov),m=CONSTANTS.MAX_FOV_DEG;
      if(!(s>0)||!(d>0))throw new Error('NAVIGATION FOV INPUT INVALID');
      if(u<=CONSTANTS.FOV_APEX){
        const p=this.s7(clamp01(u/CONSTANTS.FOV_APEX));
        return Math.exp(Math.log(s)+(Math.log(m)-Math.log(s))*p);
      }
      const p=this.s7(clamp01((u-CONSTANTS.FOV_APEX)/(1-CONSTANTS.FOV_APEX)));
      return Math.exp(Math.log(m)+(Math.log(d)-Math.log(m))*p);
    }

    rotationAt(u,startRotation,targetRotation){
      const start=Number(startRotation)||0;
      const delta=normalizeSigned(Number(targetRotation)-start);
      if(u<=CONSTANTS.ROTATION_START)return start;
      if(u>=CONSTANTS.ROTATION_END)return start+delta;
      const p=this.s7((u-CONSTANTS.ROTATION_START)/(CONSTANTS.ROTATION_END-CONSTANTS.ROTATION_START));
      return start+delta*p;
    }

    // ==================== SECTION 8 — TELEMETRY ====================
    beginTelemetry({destinationKey='',firstTravel=false}={}){
      const config=this.getTravelConfig();
      this.activeRun={
        schema:'GV-NAVIGATION-TELEMETRY-0001',version:VERSION,
        startedAt:performance.now(),generatedAt:new Date().toISOString(),
        destinationKey:String(destinationKey||''),firstTravel:Boolean(firstTravel),config,
        commands:[],observed:[],frames:[],lastFrameAt:null
      };
      return this.activeRun;
    }

    recordCommand(data={}){
      if(!this.activeRun)return;
      this.activeRun.commands.push({elapsedMs:performance.now()-this.activeRun.startedAt,...data});
    }

    recordObserved(data={}){
      if(!this.activeRun)return;
      this.activeRun.observed.push({elapsedMs:performance.now()-this.activeRun.startedAt,...data});
    }

    recordFrame(now=performance.now(),phase=''){
      if(!this.activeRun)return;
      const previous=this.activeRun.lastFrameAt;
      this.activeRun.lastFrameAt=Number(now);
      if(previous==null)return;
      this.activeRun.frames.push({elapsedMs:Number(now)-this.activeRun.startedAt,dtMs:Number(now)-previous,phase:String(phase||'')});
    }

    finishTelemetry(){
      const run=this.activeRun;
      if(!run)return null;
      const values=run.frames.map(x=>x.dtMs).filter(Number.isFinite).sort((a,b)=>a-b);
      const quantile=p=>values.length?values[Math.min(values.length-1,Math.floor((values.length-1)*p))]:null;
      run.frameStats={
        count:values.length,medianMs:quantile(.50),p95Ms:quantile(.95),p99Ms:quantile(.99),
        maxMs:values.length?values[values.length-1]:null,
        over25ms:values.filter(x=>x>25).length,
        over33ms:values.filter(x=>x>33).length,
        over50ms:values.filter(x=>x>50).length,
        excursionsOver33ms:run.frames.filter(x=>x.dtMs>33)
      };
      run.routePlannerTelemetry=[...this.telemetry];
      this.activeRun=null;
      return run;
    }
  }

  // ==================== SECTION 9 — PUBLIC API ====================
  global.GalaxyViewerNavigation=Object.freeze({
    VERSION,
    CONSTANTS,
    create:options=>new RoutePlanner(options),
    deduplicateEligible,
    greatCircleDeg,
    rotationDeltaDeg,
    compatibility,
    validateRoute
  });
})(window);
