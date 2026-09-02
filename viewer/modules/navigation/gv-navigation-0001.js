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
    MAX_FOV:237.6,
    TRANSLATE_START:.30,
    FOV_APEX:.50,
    TRANSLATE_END:.70,
    ROTATION_START:.30,
    ROTATION_END:.70,
    ALADIN_COMMAND_GATE_MS:32,
    TELEMETRY_SAMPLE_MS:100,
    TRAVEL_OPTIONS:Object.freeze([17,15,12,9,6])
  });

  const finite=value=>Number.isFinite(Number(value))?Number(value):null;
  const clamp=(value,min,max)=>Math.max(min,Math.min(max,Number(value)));
  const clamp01=value=>clamp(value,0,1);
  const normalizeSigned=value=>((Number(value)+180)%360+360)%360-180;
  const shortestRotation=(a,b)=>Math.abs(normalizeSigned(Number(b)-Number(a)));
  const toRadians=degrees=>Number(degrees)*Math.PI/180;
  const toDegrees=radians=>Number(radians)*180/Math.PI;

  function parseOrientation(value){
    if(finite(value)!==null)return normalizeSigned(value);
    const text=String(value??'').trim();
    if(!text)return null;
    if(/north\s+is\s+up/i.test(text))return 0;
    const match=text.match(/North\s+is\s+([0-9]+(?:\.[0-9]+)?)\s*°?\s*(right|left)\s+of\s+vertical/i);
    if(!match)return null;
    const angle=Number(match[1]);
    return normalizeSigned((match[2].toLowerCase()==='left'?-1:1)*angle);
  }

  function identityOf(record){
    if(!record||typeof record!=='object')return '';
    const parts=[record.provider,record.source,record.catalog,record.database,record.archiveId,record.id,record.key,record.designation,record.name]
      .map(value=>String(value??'').trim().toLowerCase()).filter(Boolean);
    return parts.join('|');
  }

  function normalizeRecord(record){
    if(!record||typeof record!=='object')return null;
    const ra=finite(record.ra);
    const dec=finite(record.dec);
    const orientation=parseOrientation(
      record.aladinRotation ??
      record.orientation ??
      record.rotation ??
      record.northOrientation
    );
    const identity=identityOf(record);
    if(!identity||ra===null||dec===null||orientation===null)return null;
    if(ra<0||ra>=360||dec<-90||dec>90)return null;
    const provider=String(record.provider||record.source||record.catalog||'').trim();
    if(!provider)return null;
    return Object.freeze({
      identity,
      ra,
      dec,
      orientation,
      provider,
      sourceRecord:record
    });
  }

  function deduplicateEligible(records){
    const map=new Map();
    for(const raw of Array.isArray(records)?records:[]){
      const record=normalizeRecord(raw);
      if(!record||map.has(record.identity))continue;
      map.set(record.identity,record);
    }
    return [...map.values()];
  }

  // ==================== SECTION 2 — SPHERICAL / ORIENTATION MATH ====================
  function greatCircleDeg(a,b){
    const ra1=toRadians(a.ra),dec1=toRadians(a.dec);
    const ra2=toRadians(b.ra),dec2=toRadians(b.dec);
    const cosine=
      Math.sin(dec1)*Math.sin(dec2)+
      Math.cos(dec1)*Math.cos(dec2)*Math.cos(ra1-ra2);
    return toDegrees(Math.acos(clamp(cosine,-1,1)));
  }

  function compatibleEdge(a,b){
    const travelDeg=greatCircleDeg(a,b);
    const rotationDeg=shortestRotation(a.orientation,b.orientation);
    const compatible=
      travelDeg>=CONSTANTS.TRAVEL_MIN_DEG&&
      travelDeg<=CONSTANTS.TRAVEL_MAX_DEG&&
      rotationDeg>=CONSTANTS.ROTATION_MIN_DEG&&
      rotationDeg<=CONSTANTS.ROTATION_MAX_DEG;
    return Object.freeze({compatible,travelDeg,rotationDeg});
  }

  // ==================== SECTION 3 — COMPATIBILITY GRAPH ====================
  function buildGraph(batch){
    const n=batch.length;
    const neighbors=Array.from({length:n},()=>[]);
    const edgeTelemetry=new Map();
    for(let i=0;i<n;i++){
      for(let j=i+1;j<n;j++){
        const edge=compatibleEdge(batch[i],batch[j]);
        edgeTelemetry.set(`${i}:${j}`,edge);
        if(!edge.compatible)continue;
        neighbors[i].push(j);
        neighbors[j].push(i);
      }
    }
    return Object.freeze({batch,neighbors,edgeTelemetry});
  }

  function isConnected(graph){
    if(!graph.batch.length)return false;
    const visited=new Set([0]);
    const stack=[0];
    while(stack.length){
      const node=stack.pop();
      for(const next of graph.neighbors[node]){
        if(visited.has(next))continue;
        visited.add(next);
        stack.push(next);
      }
    }
    return visited.size===graph.batch.length;
  }

  function graphStats(graph){
    const degree=graph.neighbors.map(list=>list.length);
    return Object.freeze({
      minDegree:degree.length?Math.min(...degree):0,
      meanDegree:degree.length?degree.reduce((a,b)=>a+b,0)/degree.length:0,
      maxDegree:degree.length?Math.max(...degree):0,
      zeroDegree:degree.filter(value=>value===0).length,
      connected:isConnected(graph)
    });
  }

  // ==================== SECTION 4 — ROUTE SOLVER ====================
  function shuffled(values,random=Math.random){
    const out=[...values];
    for(let i=out.length-1;i>0;i--){
      const j=Math.floor(random()*(i+1));
      [out[i],out[j]]=[out[j],out[i]];
    }
    return out;
  }

  function lowDegreeStarts(graph,random=Math.random){
    const indices=graph.neighbors.map((_,index)=>index);
    indices.sort((a,b)=>graph.neighbors[a].length-graph.neighbors[b].length);
    const minimum=indices.length?graph.neighbors[indices[0]].length:0;
    const band=indices.filter(index=>graph.neighbors[index].length<=minimum+2);
    return shuffled(band,random);
  }

  function solveRoute(graph,random=Math.random){
    const required=graph.batch.length;
    const starts=lowDegreeStarts(graph,random);
    const allStarts=starts.length?starts:shuffled([...Array(required).keys()],random);

    const attemptFrom=start=>{
      const route=[start];
      const used=new Set([start]);
      while(route.length<required){
        const current=route[route.length-1];
        const candidates=graph.neighbors[current].filter(index=>!used.has(index));
        if(!candidates.length)return null;
        const scored=candidates.map(index=>{
          const remaining=graph.neighbors[index].filter(next=>!used.has(next)&&next!==current).length;
          return {index,remaining,tie:random()};
        });
        scored.sort((a,b)=>a.remaining-b.remaining||a.tie-b.tie);
        const next=scored[0].index;
        route.push(next);
        used.add(next);
      }
      return route;
    };

    for(let attempt=0;attempt<CONSTANTS.ROUTE_RESTART_ATTEMPTS;attempt++){
      const start=allStarts[attempt%allStarts.length];
      const route=attemptFrom(start);
      if(route?.length===required)return Object.freeze({route,restarts:attempt});
    }
    return null;
  }

  function validateRoute(graph,route,anchor=null){
    if(!Array.isArray(route)||route.length!==CONSTANTS.ROUTE_REQUIRED_LENGTH)return false;
    if(new Set(route).size!==route.length)return false;
    if(anchor){
      const seam=compatibleEdge(anchor,graph.batch[route[0]]);
      if(!seam.compatible)return false;
    }
    for(let i=0;i<route.length-1;i++){
      const a=Math.min(route[i],route[i+1]);
      const b=Math.max(route[i],route[i+1]);
      if(!graph.edgeTelemetry.get(`${a}:${b}`)?.compatible)return false;
    }
    return true;
  }

  function sampleBatch(eligible,size,random=Math.random){
    if(eligible.length<size)return null;
    return shuffled(eligible,random).slice(0,size);
  }

  function solveBatch(eligible,{anchor=null,random=Math.random}={}){
    let batchAttempts=0;
    for(;;){
      batchAttempts++;
      const batch=sampleBatch(eligible,CONSTANTS.NAV_BATCH_SIZE,random);
      if(!batch)return null;
      const graph=buildGraph(batch);
      const stats=graphStats(graph);
      if(stats.zeroDegree||!stats.connected)continue;
      const solved=solveRoute(graph,random);
      if(!solved)continue;
      if(!validateRoute(graph,solved.route,anchor))continue;
      const ordered=solved.route.map(index=>graph.batch[index]);
      const edges=[];
      for(let i=0;i<ordered.length-1;i++){
        const edge=compatibleEdge(ordered[i],ordered[i+1]);
        edges.push(Object.freeze({
          from:ordered[i].identity,
          to:ordered[i+1].identity,
          travelDeg:edge.travelDeg,
          rotationDeg:edge.rotationDeg
        }));
      }
      const seam=anchor?compatibleEdge(anchor,ordered[0]):null;
      return Object.freeze({
        ordered:Object.freeze(ordered),
        stats,
        batchAttempts,
        restartCount:solved.restarts,
        edges:Object.freeze(edges),
        seam
      });
    }
  }

  // ==================== SECTION 5 — ATOMIC ROUTE QUEUE ====================
  class RoutePlanner{
    constructor(records,{random=Math.random}={}){
      this.random=random;
      this.eligible=deduplicateEligible(records);
      this.queue=[];
      this.nextBatch=null;
      this.batchId=0;
      this.nextBatchPromise=null;
      this.currentTail=null;
      this.telemetry=[];
      this.travelSeconds=17;
    }

    ensureInitial(){
      if(this.queue.length)return this.getState();
      const solved=solveBatch(this.eligible,{random:this.random});
      if(!solved)throw new Error('NAVIGATION INITIAL 130 ROUTE COULD NOT BE SOLVED');
      this.#commitSolved(solved);
      return this.getState();
    }

    #commitSolved(solved){
      this.batchId++;
      this.queue=solved.ordered.map(item=>item.sourceRecord);
      this.currentTail=solved.ordered[solved.ordered.length-1];
      this.telemetry.push(Object.freeze({
        type:'BATCH_COMMIT',batchId:this.batchId,at:Date.now(),
        batchAttempts:solved.batchAttempts,restarts:solved.restartCount,
        graph:solved.stats,seam:solved.seam,
        edges:solved.edges
      }));
    }

    peek(){this.ensureInitial();return this.queue[0]||null}

    commitArrival(record){
      this.ensureInitial();
      if(!this.queue.length)return null;
      const expected=this.queue[0];
      if(identityOf(expected)!==identityOf(record))
        throw new Error('NAVIGATION COMMIT IDENTITY MISMATCH');
      const arrived=this.queue.shift();
      if(this.queue.length===CONSTANTS.QUEUE_REFILL_TRIGGER)this.prepareNextBatch();
      if(!this.queue.length&&this.nextBatch){
        const solved=this.nextBatch;
        this.nextBatch=null;
        this.#commitSolved(solved);
      }
      return arrived;
    }

    prepareNextBatch(){
      if(this.nextBatch||this.nextBatchPromise)return this.nextBatchPromise;
      const anchor=this.currentTail;
      this.nextBatchPromise=Promise.resolve().then(()=>{
        const solved=solveBatch(this.eligible,{anchor,random:this.random});
        if(!solved)throw new Error('NAVIGATION NEXT 130 ROUTE COULD NOT BE SOLVED');
        this.nextBatch=solved;
        return solved;
      }).finally(()=>{this.nextBatchPromise=null});
      return this.nextBatchPromise;
    }

    getUpcoming(count=10){
      this.ensureInitial();
      return this.queue.slice(0,Math.max(0,Number(count)||0));
    }

    getState(){
      return Object.freeze({
        version:VERSION,
        eligible:this.eligible.length,
        batchId:this.batchId,
        remaining:this.queue.length,
        nextBatchReady:Boolean(this.nextBatch),
        nextBatchPlanning:Boolean(this.nextBatchPromise),
        travelSeconds:this.travelSeconds,
        firstTravelSeconds:this.travelSeconds/2
      });
    }

    setTravelSeconds(value){
      const next=Number(value);
      if(!CONSTANTS.TRAVEL_OPTIONS.includes(next))
        throw new Error(`NAVIGATION TRAVEL TIME NOT ALLOWED: ${value}`);
      this.travelSeconds=next;
      return this.travelSeconds;
    }

    getTravelSeconds({firstHome=false}={}){
      return firstHome?this.travelSeconds/2:this.travelSeconds;
    }
  }

  // ==================== SECTION 6 — TIMING / MOTION ====================
  function s7(value){
    const t=clamp01(value);
    return 35*t**4-84*t**5+70*t**6-20*t**7;
  }

  function translationProgress(u){
    const t=clamp01(u);
    if(t<=CONSTANTS.TRANSLATE_START)return 0;
    if(t>=CONSTANTS.TRANSLATE_END)return 1;
    return s7((t-CONSTANTS.TRANSLATE_START)/(CONSTANTS.TRANSLATE_END-CONSTANTS.TRANSLATE_START));
  }

  function fovAt(u,startFov,destinationFov){
    const t=clamp01(u);
    const start=Number(startFov),destination=Number(destinationFov),maximum=CONSTANTS.MAX_FOV;
    if(!(start>0)||!(destination>0))throw new Error('NAVIGATION FOV MUST BE POSITIVE');
    if(t<=CONSTANTS.FOV_APEX){
      const progress=s7(t/CONSTANTS.FOV_APEX);
      return Math.exp(Math.log(start)+(Math.log(maximum)-Math.log(start))*progress);
    }
    const progress=s7((t-CONSTANTS.FOV_APEX)/(1-CONSTANTS.FOV_APEX));
    return Math.exp(Math.log(maximum)+(Math.log(destination)-Math.log(maximum))*progress);
  }

  function rotationProgress(u){
    const t=clamp01(u);
    if(t<=CONSTANTS.ROTATION_START)return 0;
    if(t>=CONSTANTS.ROTATION_END)return 1;
    return s7((t-CONSTANTS.ROTATION_START)/(CONSTANTS.ROTATION_END-CONSTANTS.ROTATION_START));
  }

  // ==================== SECTION 7 — TELEMETRY ====================
  class TelemetryRecorder{
    constructor(){this.reset()}
    reset(){this.startedAt=0;this.frames=[];this.commands=[];this.observed=[];this.lastFrameAt=null}
    start(){this.reset();this.startedAt=performance.now();return this.startedAt}
    frame(now,u,phase){
      if(this.lastFrameAt!==null)this.frames.push({elapsedMs:now-this.startedAt,u,phase,dtMs:now-this.lastFrameAt});
      this.lastFrameAt=now;
    }
    command(data){this.commands.push({...data})}
    observe(data){this.observed.push({...data})}
    summary(){
      const intervals=this.frames.map(item=>Number(item.dtMs)).filter(Number.isFinite).sort((a,b)=>a-b);
      const q=p=>intervals.length?intervals[Math.min(intervals.length-1,Math.floor((intervals.length-1)*p))]:null;
      return Object.freeze({
        count:intervals.length,
        medianMs:q(.5),p95Ms:q(.95),p99Ms:q(.99),maxMs:intervals.length?intervals[intervals.length-1]:null,
        over25ms:intervals.filter(value=>value>25).length,
        over33ms:intervals.filter(value=>value>33).length,
        over50ms:intervals.filter(value=>value>50).length,
        excursionsOver33ms:this.frames.filter(item=>Number(item.dtMs)>33),
        commands:this.commands,
        observed:this.observed,
        frames:this.frames
      });
    }
  }

  // ==================== SECTION 8 — PUBLIC API ====================
  function create(records,options={}){
    const planner=new RoutePlanner(records,options);
    planner.ensureInitial();
    return planner;
  }

  global.GalaxyViewerNavigation=Object.freeze({
    VERSION,
    CONSTANTS,
    create,
    deduplicateEligible,
    greatCircleDeg,
    shortestRotation,
    compatibleEdge,
    buildGraph,
    graphStats,
    solveBatch,
    s7,
    translationProgress,
    fovAt,
    rotationProgress,
    TelemetryRecorder
  });
})(globalThis);
