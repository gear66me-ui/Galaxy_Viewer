(function(global){
"use strict";

const VERSION="0002";
const DESIGN_SEED=20260908;

const TIMES=[10,15,20,25];

const PROFILES=[
  {id:"P30-40-30",zoomOutPct:30,motionPct:40,zoomInPct:30},
  {id:"P40-20-40",zoomOutPct:40,motionPct:20,zoomInPct:40},
  {id:"P45-10-45",zoomOutPct:45,motionPct:10,zoomInPct:45}
];

function finite(v){
  const n=Number(v);
  return Number.isFinite(n)?n:null;
}

function round(v,d=3){
  const n=Number(v);
  if(!Number.isFinite(n))return null;
  const p=10**d;
  return Math.round(n*p)/p;
}

function clamp(v,a,b){
  return Math.max(a,Math.min(b,Number(v)));
}

function normalizeRotationDelta(v){
  let a=Number(v)||0;
  while(a>180)a-=360;
  while(a<=-180)a+=360;
  return a;
}

function vector(ra,dec){
  const r=Number(ra)*Math.PI/180;
  const d=Number(dec)*Math.PI/180;

  return [
    Math.cos(d)*Math.cos(r),
    Math.cos(d)*Math.sin(r),
    Math.sin(d)
  ];
}

function angularSeparationDeg(a,b){
  try{
    const x=vector(a.ra,a.dec);
    const y=vector(b.ra,b.dec);

    const dot=clamp(
      x[0]*y[0]+x[1]*y[1]+x[2]*y[2],
      -1,1
    );

    return round(
      Math.acos(dot)*180/Math.PI,
      6
    );
  }catch(_){
    return null;
  }
}

function rng(seed){
  let a=seed>>>0;

  return function(){
    a=(a+0x6D2B79F5)|0;

    let t=Math.imul(
      a^(a>>>15),
      1|a
    );

    t=(
      t+
      Math.imul(
        t^(t>>>7),
        61|t
      )
    )^t;

    return ((t^(t>>>14))>>>0)/4294967296;
  };
}

function shuffle(rows,random){
  const a=rows.slice();

  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }

  return a;
}

function buildDesign(){
  const random=rng(DESIGN_SEED);
  const design=[];

  for(let replicate=1;replicate<=3;replicate++){
    const block=[];

    for(const totalTravelSec of TIMES){
      for(const p of PROFILES){
        block.push({
          replicate,
          block:replicate,

          conditionId:
            `T${totalTravelSec}_${p.id}`,

          profileId:p.id,

          totalTravelSec,

          zoomOutPct:p.zoomOutPct,
          motionPct:p.motionPct,
          zoomInPct:p.zoomInPct,

          zoomOutSec:
            totalTravelSec*p.zoomOutPct/100,

          motionSec:
            totalTravelSec*p.motionPct/100,

          zoomInSec:
            totalTravelSec*p.zoomInPct/100
        });
      }
    }

    design.push(
      ...shuffle(block,random)
    );
  }

  return design.map((row,i)=>({
    ...row,
    scheduleOrder:i+1
  }));
}

const DESIGN=buildDesign();

const state={
  sessionId:
    "GVDOE-"+
    Date.now()+
    "-"+
    Math.random().toString(36).slice(2,9),

  startedAt:performance.now(),

  installed:false,

  seq:0,
  records:[],
  runSummaries:[],

  scheduleIndex:0,
  activeRun:null,

  mode:"AUTO_DOE",
  manualCondition:null,

  condition:{
    label:"WAITING",
    scheduleOrder:null,
    replicate:null,
    block:null,
    conditionId:null,
    profileId:null,
    totalTravelSec:null,
    zoomOutSec:null,
    motionSec:null,
    zoomInSec:null,
    zoomOutPct:null,
    motionPct:null,
    zoomInPct:null
  },

  raf:{
    running:false,
    id:null,
    frameIndex:0,
    lastNow:null,
    lastDelta:null,
    pendingCommands:[]
  },

  currentBurstId:0,
  lastCameraAt:null,
  burstGapMs:1500,

  observers:[],
  panel:null,
  statusEl:null
};

function memorySnapshot(){
  const m=performance.memory;

  if(!m)return {};

  return {
    heapUsedBytes:finite(m.usedJSHeapSize),
    heapTotalBytes:finite(m.totalJSHeapSize),
    heapLimitBytes:finite(m.jsHeapSizeLimit)
  };
}

function phaseAt(now=performance.now()){
  const r=state.activeRun;

  if(!r)
    return {phase:"IDLE",runElapsedMs:null};

  const s=(now-r.startedPerfMs)/1000;

  if(s<r.zoomOutSec)
    return {phase:"ZOOM_OUT",runElapsedMs:round(s*1000)};

  if(s<r.zoomOutSec+r.motionSec)
    return {phase:"MOTION",runElapsedMs:round(s*1000)};

  return {phase:"ZOOM_IN",runElapsedMs:round(s*1000)};
}

function push(type,data={}){
  const phase=phaseAt();

  const row={
    seq:++state.seq,
    sessionId:state.sessionId,
    elapsedMs:round(performance.now()-state.startedAt),
    type,

    scheduleOrder:state.condition.scheduleOrder,
    replicate:state.condition.replicate,
    block:state.condition.block,
    conditionId:state.condition.conditionId,
    profileId:state.condition.profileId,

    totalTravelSec:state.condition.totalTravelSec,
    zoomOutSec:state.condition.zoomOutSec,
    motionSec:state.condition.motionSec,
    zoomInSec:state.condition.zoomInSec,

    phase:phase.phase,
    runElapsedMs:phase.runElapsedMs,

    ...data
  };

  state.records.push(row);
  return row;
}

function safeSnapshot(value,depth=0){
  if(value==null)return value;

  if(
    typeof value==="string" ||
    typeof value==="number" ||
    typeof value==="boolean"
  )return value;

  if(depth>2)return undefined;

  if(Array.isArray(value))
    return value.slice(0,20).map(v=>safeSnapshot(v,depth+1));

  if(typeof value!=="object")
    return undefined;

  const out={};
  const wanted=/prewarm|prefetch|prepare|ready|hot|queue|archive|provider|catalog|target|fov|rotation|travel|cache|suspend|pending/i;

  for(const key of Object.keys(value).slice(0,100)){
    if(depth===0 && !wanted.test(key))
      continue;

    try{
      const v=safeSnapshot(value[key],depth+1);
      if(v!==undefined)out[key]=v;
    }catch(_){}
  }

  return out;
}

function prewarmSnapshot(controller,destination){
  const out={
    capturedAtMs:round(performance.now()-state.startedAt),

    destination:{
      name:destination?.name||null,
      ra:finite(destination?.ra),
      dec:finite(destination?.dec),
      fovDegrees:finite(destination?.fovDegrees),
      aladinRotation:finite(destination?.aladinRotation),
      provider:destination?.provider||null,
      telescope:destination?.telescope||null,
      archiveId:destination?.archiveId||null,
      preparedHd:Boolean(destination?.preparedHdUrl),
      preparedSource:destination?.preparedSource||null
    }
  };

  try{
    out.controller=safeSnapshot(controller);
  }catch(_){}

  try{
    const d=global.GalaxyViewerDiagnostics;
    if(d){
      out.diagnostics=safeSnapshot(
        typeof d.getState==="function"
          ? d.getState()
          : d
      );
    }
  }catch(_){}

  try{
    out.aladin={
      raDec:controller?.aladin?.getRaDec?.()||null,
      fov:controller?.aladin?.getFov?.()||null,
      rotation:controller?.aladin?.getRotation?.()??null
    };
  }catch(_){}

  return out;
}

function beginBurst(now){
  const gap=
    state.lastCameraAt===null
      ? Infinity
      : now-state.lastCameraAt;

  if(gap>state.burstGapMs){
    state.currentBurstId++;

    push("burst_start",{
      burstId:state.currentBurstId,
      precedingIdleMs:
        Number.isFinite(gap)
          ? round(gap)
          : null
    });
  }

  return state.currentBurstId;
}

function wrapCamera(aladin,name){
  const original=aladin?.[name];

  if(typeof original!=="function"){
    push("warning",{method:name,message:"METHOD MISSING"});
    return;
  }

  if(original.__gvDoeWrapped)return;

  const wrapped=function(...args){
    const begin=performance.now();
    const burstId=beginBurst(begin);

    try{
      return original.apply(this,args);
    }finally{
      const end=performance.now();

      const row=push("camera",{
        burstId,
        method:name,
        args:args.slice(0,4),
        callMs:round(end-begin),
        rafDeltaBeforeMs:
          state.raf.lastDelta===null
            ? null
            : round(state.raf.lastDelta)
      });

      state.raf.pendingCommands.push({
        seq:row.seq,
        method:name,
        callMs:round(end-begin)
      });

      state.lastCameraAt=end;
    }
  };

  Object.defineProperty(
    wrapped,
    "__gvDoeWrapped",
    {value:true}
  );

  aladin[name]=wrapped;
}

function rafTick(now){
  if(!state.raf.running)return;

  const previous=state.raf.lastNow;
  const dt=previous===null?null:now-previous;

  state.raf.lastNow=now;
  state.raf.lastDelta=dt;
  state.raf.frameIndex++;

  const commands=state.raf.pendingCommands.splice(0);

  const row={
    frameIndex:state.raf.frameIndex,
    rafDeltaMs:dt===null?null:round(dt),
    fps:dt&&dt>0?round(1000/dt):null,

    over25:dt!==null&&dt>=25,
    over33_3:dt!==null&&dt>=33.3,
    over50:dt!==null&&dt>=50,
    over100:dt!==null&&dt>=100,

    commandCount:commands.length,

    commandMask:
      [...new Set(commands.map(c=>c.method))]
        .sort()
        .join("+") || "NONE",

    cameraCallMsTotal:
      round(
        commands.reduce(
          (sum,c)=>sum+(Number(c.callMs)||0),
          0
        )
      )
  };

  if(state.raf.frameIndex%60===0)
    Object.assign(row,memorySnapshot());

  push("frame",row);

  state.raf.id=requestAnimationFrame(rafTick);
}

function installObservers(){
  if(typeof PerformanceObserver!=="function")
    return;

  const types=PerformanceObserver.supportedEntryTypes||[];

  if(types.includes("longtask")){
    const o=new PerformanceObserver(list=>{
      for(const e of list.getEntries()){
        push("longtask",{
          durationMs:round(e.duration),
          startTimeMs:round(e.startTime)
        });
      }
    });

    o.observe({entryTypes:["longtask"]});
    state.observers.push(o);
  }

  if(types.includes("long-animation-frame")){
    const o=new PerformanceObserver(list=>{
      for(const e of list.getEntries()){
        push("long_animation_frame",{
          durationMs:round(e.duration),
          blockingDurationMs:finite(e.blockingDuration)
        });
      }
    });

    o.observe({entryTypes:["long-animation-frame"]});
    state.observers.push(o);
  }
}

function applyCondition(controller,row){
  const total=Number(row.totalTravelSec);
  const z1=Number(row.zoomOutSec);
  const motion=Number(row.motionSec);
  const z2=Number(row.zoomInSec);

  if(
    ![total,z1,motion,z2].every(Number.isFinite) ||
    total<=0 ||
    z1<0 ||
    motion<0 ||
    z2<0
  ){
    throw new Error("GV DOE INVALID PHASE VALUES");
  }

  if(Math.abs((z1+motion+z2)-total)>.000001)
    throw new Error("GV DOE PHASE SUM FAILURE");

  controller.options.travelSeconds=total;

  controller.options.turnPoint=
    z1/total;

  controller.options.translateStart=
    z1/total;

  controller.options.translationComplete=
    (z1+motion)/total;

  controller.options.translate90=
    (z1+motion)/total;
}

function currentCondition(){
  if(
    state.mode==="MANUAL" &&
    state.manualCondition
  ){
    return {
      ...state.manualCondition,
      conditionId:"MANUAL",
      profileId:"MANUAL",
      scheduleOrder:null,
      replicate:null,
      block:null
    };
  }

  return DESIGN[state.scheduleIndex]||null;
}

function prepareTravel(controller,context={}){
  if(context.firstHomeTrip){
    state.condition={
      ...state.condition,
      label:"FIRST-HOME-EXCLUDED"
    };

    push("first_home_start",{
      excludedFromDoe:true,
      destinationName:
        String(context.destination?.name||""),
      prewarm:
        prewarmSnapshot(
          controller,
          context.destination
        )
    });

    updatePanel();

    return {
      excluded:true
    };
  }

  if(state.activeRun)
    return state.activeRun;

  const row=currentCondition();

  if(!row){
    state.condition={
      ...state.condition,
      label:"DOE-COMPLETE"
    };

    updatePanel();

    return {
      complete:true
    };
  }

  applyCondition(controller,row);

  state.condition={
    label:row.conditionId||"MANUAL",

    scheduleOrder:
      row.scheduleOrder??null,

    replicate:
      row.replicate??null,

    block:
      row.block??null,

    conditionId:
      row.conditionId||"MANUAL",

    profileId:
      row.profileId||"MANUAL",

    totalTravelSec:
      row.totalTravelSec,

    zoomOutSec:
      row.zoomOutSec,

    motionSec:
      row.motionSec,

    zoomInSec:
      row.zoomInSec,

    zoomOutPct:
      row.zoomOutPct,

    motionPct:
      row.motionPct,

    zoomInPct:
      row.zoomInPct
  };

  const source=
    context.source||{};

  const destination=
    context.destination||{};

  const startRotation=
    finite(source.aladinRotation);

  const targetRotation=
    finite(destination.aladinRotation);

  const rotationDelta=
    startRotation!==null &&
    targetRotation!==null
      ? normalizeRotationDelta(
          targetRotation-startRotation
        )
      : null;

  const startFov=
    finite(context.startFov);

  const destinationFov=
    finite(destination.fovDegrees);

  const skyAngleDeg=
    angularSeparationDeg(
      source,
      destination
    );

  const fovRatio=
    startFov!==null &&
    destinationFov!==null &&
    startFov>0 &&
    destinationFov>0
      ? round(
          Math.max(
            startFov,
            destinationFov
          )/
          Math.min(
            startFov,
            destinationFov
          ),
          6
        )
      : null;

  const prewarmStart=
    prewarmSnapshot(
      controller,
      destination
    );

  const startRow=
    push("run_start",{
      sourceName:
        String(source.name||""),

      destinationName:
        String(destination.name||""),

      sourceRA:
        finite(source.ra),

      sourceDec:
        finite(source.dec),

      destinationRA:
        finite(destination.ra),

      destinationDec:
        finite(destination.dec),

      skyAngleDeg,

      startRotationDeg:
        startRotation,

      destinationRotationDeg:
        targetRotation,

      rotationDeltaSignedDeg:
        rotationDelta===null
          ? null
          : round(rotationDelta,6),

      rotationDeltaAbsDeg:
        rotationDelta===null
          ? null
          : round(
              Math.abs(rotationDelta),
              6
            ),

      startFovDeg:
        startFov,

      destinationFovDeg:
        destinationFov,

      fovRatio,

      maximumTravelFovDeg:
        finite(
          controller.options.maxFov
        ),

      aladinTravelHz:15,

      provider:
        String(destination.provider||""),

      telescope:
        String(destination.telescope||""),

      archiveId:
        String(destination.archiveId||""),

      preparedHd:
        Boolean(
          destination.preparedHdUrl
        ),

      preparedSource:
        String(
          destination.preparedSource||""
        ),

      prewarmStart
    });

  state.activeRun={
    ...row,

    startedPerfMs:
      performance.now(),

    startSeq:
      startRow.seq,

    controller,

    sourceName:
      String(source.name||""),

    destinationName:
      String(destination.name||""),

    skyAngleDeg,

    rotationDeltaAbsDeg:
      rotationDelta===null
        ? null
        : Math.abs(rotationDelta),

    startFovDeg:
      startFov,

    destinationFovDeg:
      destinationFov,

    fovRatio,

    prewarmStart
  };

  updatePanel();

  console.log(
    "GV DOE RUN",
    row.scheduleOrder,
    "OF 36",
    row.conditionId,
    "REP",
    row.replicate,
    "PHASES",
    round(row.zoomOutSec),
    round(row.motionSec),
    round(row.zoomInSec)
  );

  return {
    ...state.activeRun
  };
}

function simpleStats(values){
  const a=
    values
      .map(Number)
      .filter(Number.isFinite)
      .sort((x,y)=>x-y);

  if(!a.length)
    return {
      n:0,
      mean:null,
      p95:null,
      p99:null,
      max:null
    };

  const q=p=>{
    const i=(a.length-1)*p;
    const lo=Math.floor(i);
    const hi=Math.ceil(i);

    if(lo===hi)return a[lo];

    return (
      a[lo]+
      (a[hi]-a[lo])*
      (i-lo)
    );
  };

  return {
    n:a.length,

    mean:
      round(
        a.reduce((x,y)=>x+y,0)/
        a.length,
        4
      ),

    p95:
      round(q(.95),4),

    p99:
      round(q(.99),4),

    max:
      round(
        Math.max(...a),
        4
      )
  };
}

function completeTravel(info={}){
  if(info.firstHomeTrip){
    push("first_home_complete",{
      excludedFromDoe:true
    });

    state.condition={
      ...state.condition,
      label:"WAITING"
    };

    updatePanel();
    return;
  }

  if(!state.activeRun)
    return;

  const run=
    state.activeRun;

  const rows=
    state.records.filter(
      r=>r.seq>=run.startSeq
    );

  const frames=
    rows.filter(
      r=>
        r.type==="frame" &&
        Number.isFinite(
          Number(r.rafDeltaMs)
        )
    );

  const camera=
    rows.filter(
      r=>r.type==="camera"
    );

  const frameStats=
    simpleStats(
      frames.map(
        r=>r.rafDeltaMs
      )
    );

  const threshold=
    n=>
      frames.filter(
        r=>
          Number(r.rafDeltaMs)>=n
      ).length;

  function phaseStats(name){
    const f=
      frames.filter(
        r=>r.phase===name
      );

    const s=
      simpleStats(
        f.map(
          r=>r.rafDeltaMs
        )
      );

    return {
      frames:f.length,
      meanMs:s.mean,
      p95Ms:s.p95,
      p99Ms:s.p99,
      maxMs:s.max,
      over25:
        f.filter(
          r=>Number(r.rafDeltaMs)>=25
        ).length,
      over50:
        f.filter(
          r=>Number(r.rafDeltaMs)>=50
        ).length
    };
  }

  function commandStats(name){
    const c=
      camera.filter(
        r=>r.method===name
      );

    const s=
      simpleStats(
        c.map(
          r=>r.callMs
        )
      );

    return {
      count:c.length,
      meanMs:s.mean,
      p95Ms:s.p95,
      p99Ms:s.p99,
      maxMs:s.max
    };
  }

  const zoomOut=
    phaseStats("ZOOM_OUT");

  const motion=
    phaseStats("MOTION");

  const zoomIn=
    phaseStats("ZOOM_IN");

  const fov=
    commandStats("setFov");

  const goto=
    commandStats("gotoRaDec");

  const rotation=
    commandStats("setRotation");

  const summary={
    sessionId:
      state.sessionId,

    scheduleOrder:
      run.scheduleOrder,

    replicate:
      run.replicate,

    block:
      run.block,

    conditionId:
      run.conditionId,

    profileId:
      run.profileId,

    totalTravelSec:
      run.totalTravelSec,

    zoomOutSec:
      run.zoomOutSec,

    motionSec:
      run.motionSec,

    zoomInSec:
      run.zoomInSec,

    zoomOutPct:
      run.zoomOutPct,

    motionPct:
      run.motionPct,

    zoomInPct:
      run.zoomInPct,

    sourceName:
      run.sourceName,

    destinationName:
      run.destinationName,

    skyAngleDeg:
      round(
        run.skyAngleDeg,
        6
      ),

    rotationDeltaAbsDeg:
      round(
        run.rotationDeltaAbsDeg,
        6
      ),

    startFovDeg:
      run.startFovDeg,

    destinationFovDeg:
      run.destinationFovDeg,

    fovRatio:
      run.fovRatio,

    routeDistanceMly:
      finite(info.route?.value),

    frameCount:
      frames.length,

    frameMeanMs:
      frameStats.mean,

    frameP95Ms:
      frameStats.p95,

    frameP99Ms:
      frameStats.p99,

    frameMaxMs:
      frameStats.max,

    framesOver25:
      threshold(25),

    framesOver33_3:
      threshold(33.3),

    framesOver50:
      threshold(50),

    framesOver100:
      threshold(100),

    zoomOutFrames:
      zoomOut.frames,

    zoomOutP95Ms:
      zoomOut.p95Ms,

    zoomOutOver25:
      zoomOut.over25,

    motionFrames:
      motion.frames,

    motionP95Ms:
      motion.p95Ms,

    motionOver25:
      motion.over25,

    zoomInFrames:
      zoomIn.frames,

    zoomInP95Ms:
      zoomIn.p95Ms,

    zoomInOver25:
      zoomIn.over25,

    setFovCount:
      fov.count,

    setFovP95Ms:
      fov.p95Ms,

    gotoRaDecCount:
      goto.count,

    gotoRaDecP95Ms:
      goto.p95Ms,

    setRotationCount:
      rotation.count,

    setRotationP95Ms:
      rotation.p95Ms,

    elapsedExperimentMin:
      round(
        (
          performance.now()-
          state.startedAt
        )/60000,
        4
      ),

    heapUsedBytesEnd:
      finite(
        performance.memory
          ?.usedJSHeapSize
      ),

    prewarmStart:
      run.prewarmStart,

    prewarmEnd:
      prewarmSnapshot(
        run.controller,
        info.destination
      )
  };

  state.runSummaries.push(
    summary
  );

  push("run_end",{
    summary
  });

  if(state.mode==="AUTO_DOE")
    state.scheduleIndex++;

  state.activeRun=null;

  state.condition={
    ...state.condition,
    label:
      state.scheduleIndex>=DESIGN.length
        ? "DOE-COMPLETE"
        : "WAITING"
  };

  updatePanel();

  console.log(
    "GV DOE RUN COMPLETE",
    state.runSummaries.length,
    "OF 36"
  );
}

function abortTravel(error){
  push("run_abort",{
    error:
      String(
        error?.message||
        error||
        "UNKNOWN"
      )
  });

  // Do not advance DOE index.
  // Next Random click repeats the same condition.
  state.activeRun=null;

  state.condition={
    ...state.condition,
    label:"RETRY-SAME-CONDITION"
  };

  updatePanel();
}

function setManual(
  total,
  zoomOut,
  motion,
  zoomIn
){
  total=Number(total);
  zoomOut=Number(zoomOut);
  motion=Number(motion);
  zoomIn=Number(zoomIn);

  if(
    Math.abs(
      zoomOut+
      motion+
      zoomIn-
      total
    )>.000001
  ){
    throw new Error(
      "MANUAL PHASES MUST SUM TO TOTAL"
    );
  }

  state.mode="MANUAL";

  state.manualCondition={
    totalTravelSec:total,
    zoomOutSec:zoomOut,
    motionSec:motion,
    zoomInSec:zoomIn,

    zoomOutPct:
      round(
        zoomOut/total*100,
        4
      ),

    motionPct:
      round(
        motion/total*100,
        4
      ),

    zoomInPct:
      round(
        zoomIn/total*100,
        4
      )
  };

  updatePanel();

  return {
    ...state.manualCondition
  };
}

function useDOE(){
  state.mode="AUTO_DOE";
  state.manualCondition=null;

  updatePanel();

  return {
    mode:state.mode,
    nextRun:
      DESIGN[state.scheduleIndex]||null
  };
}

function csvEscape(v){
  if(v===null || v===undefined)return "";

  const s=
    typeof v==="object"
      ? JSON.stringify(v)
      : String(v);

  return /[",\n\r]/.test(s)
    ? "\""+s.replace(/"/g,"\"\"")+"\""
    : s;
}

function rowsCsv(rows){
  if(!rows.length)return "";

  const columns=[
    ...new Set(
      rows.flatMap(
        row=>Object.keys(row)
      )
    )
  ];

  return [
    columns.join(","),

    ...rows.map(
      row=>
        columns
          .map(
            key=>csvEscape(row[key])
          )
          .join(",")
    )
  ].join("\n");
}

function downloadText(name,text,mime){
  const blob=
    new Blob(
      [text],
      {type:mime}
    );

  const url=
    URL.createObjectURL(blob);

  const a=
    document.createElement("a");

  a.href=url;
  a.download=name;
  a.style.display="none";

  document.body.appendChild(a);
  a.click();
  a.remove();

  setTimeout(
    ()=>URL.revokeObjectURL(url),
    2000
  );
}

function downloadJSON(){
  const payload={
    metadata:{
      version:VERSION,
      sessionId:state.sessionId,
      designSeed:DESIGN_SEED,
      createdAt:new Date().toISOString(),
      totalPlannedRuns:DESIGN.length,
      completedRuns:state.runSummaries.length
    },

    design:DESIGN,

    runSummaries:
      state.runSummaries,

    records:
      state.records
  };

  downloadText(
    `gv-stutter-doe-${state.sessionId}.json`,
    JSON.stringify(payload,null,2),
    "application/json;charset=utf-8"
  );
}

function downloadRunsCSV(){
  downloadText(
    `gv-stutter-runs-${state.sessionId}.csv`,
    rowsCsv(state.runSummaries),
    "text/csv;charset=utf-8"
  );
}

function downloadFramesCSV(){
  downloadText(
    `gv-stutter-frames-${state.sessionId}.csv`,
    rowsCsv(
      state.records.filter(
        row=>row.type==="frame"
      )
    ),
    "text/csv;charset=utf-8"
  );
}

function downloadCameraCSV(){
  downloadText(
    `gv-stutter-camera-${state.sessionId}.csv`,
    rowsCsv(
      state.records.filter(
        row=>row.type==="camera"
      )
    ),
    "text/csv;charset=utf-8"
  );
}

function downloadPrewarmJSON(){
  const runs=
    state.runSummaries.map(
      run=>({
        sessionId:
          run.sessionId,

        scheduleOrder:
          run.scheduleOrder,

        replicate:
          run.replicate,

        block:
          run.block,

        conditionId:
          run.conditionId,

        sourceName:
          run.sourceName,

        destinationName:
          run.destinationName,

        skyAngleDeg:
          run.skyAngleDeg,

        rotationDeltaAbsDeg:
          run.rotationDeltaAbsDeg,

        startFovDeg:
          run.startFovDeg,

        destinationFovDeg:
          run.destinationFovDeg,

        fovRatio:
          run.fovRatio,

        prewarmStart:
          run.prewarmStart,

        prewarmEnd:
          run.prewarmEnd
      })
    );

  downloadText(
    `gv-prewarm-doe-${state.sessionId}.json`,
    JSON.stringify(
      {
        metadata:{
          sessionId:state.sessionId,
          designSeed:DESIGN_SEED,
          completedRuns:
            state.runSummaries.length
        },
        runs
      },
      null,
      2
    ),
    "application/json;charset=utf-8"
  );
}

function updatePanel(){
  if(!state.statusEl)return;

  if(
    state.scheduleIndex>=DESIGN.length &&
    !state.activeRun
  ){
    state.statusEl.textContent=
      `DOE COMPLETE ${state.runSummaries.length}/36`;

    return;
  }

  const row=
    state.activeRun ||
    currentCondition();

  if(!row){
    state.statusEl.textContent=
      "DOE COMPLETE";

    return;
  }

  const prefix=
    state.activeRun
      ? "RUNNING"
      : "NEXT";

  const order=
    row.scheduleOrder==null
      ? "--"
      : String(row.scheduleOrder).padStart(2,"0");

  const rep=
    row.replicate==null
      ? "-"
      : row.replicate;

  state.statusEl.textContent=
    `${prefix} ${order}/36 · `+
    `${row.totalTravelSec}s · `+
    `${round(row.zoomOutSec,2)}/`+
    `${round(row.motionSec,2)}/`+
    `${round(row.zoomInSec,2)}s · `+
    `R${rep}`;
}

function createPanel(){
  if(
    typeof document==="undefined" ||
    state.panel
  )return;

  const panel=
    document.createElement("div");

  panel.id=
    "gv-stutter-doe-panel";

  Object.assign(
    panel.style,
    {
      position:"fixed",
      top:"5px",
      left:"5px",
      zIndex:"2147483646",
      background:"rgba(0,0,0,.78)",
      color:"#fff",
      border:"1px solid rgba(255,255,255,.4)",
      borderRadius:"5px",
      padding:"5px 6px",
      fontFamily:"monospace",
      fontSize:"10px",
      lineHeight:"1.25",
      pointerEvents:"auto",
      maxWidth:"96vw"
    }
  );

  const status=
    document.createElement("div");

  status.style.whiteSpace=
    "nowrap";

  panel.appendChild(status);

  const buttons=
    document.createElement("div");

  Object.assign(
    buttons.style,
    {
      display:"flex",
      flexWrap:"wrap",
      gap:"3px",
      marginTop:"4px"
    }
  );

  const specs=[
    ["JSON",downloadJSON],
    ["RUNS",downloadRunsCSV],
    ["FRAMES",downloadFramesCSV],
    ["CAMERA",downloadCameraCSV],
    ["PREWARM",downloadPrewarmJSON]
  ];

  for(const [label,fn] of specs){
    const button=
      document.createElement("button");

    button.type="button";
    button.textContent=label;

    Object.assign(
      button.style,
      {
        fontSize:"9px",
        padding:"2px 4px"
      }
    );

    button.addEventListener(
      "click",
      event=>{
        event.preventDefault();
        event.stopPropagation();
        fn();
      }
    );

    buttons.appendChild(button);
  }

  panel.appendChild(buttons);
  document.body.appendChild(panel);

  state.panel=panel;
  state.statusEl=status;

  updatePanel();
}

function install(aladin){
  if(state.installed)
    return api;

  if(!aladin)
    throw new Error(
      "GV STUTTER DOE — ALADIN INSTANCE MISSING"
    );

  state.installed=true;

  wrapCamera(
    aladin,
    "setFov"
  );

  wrapCamera(
    aladin,
    "gotoRaDec"
  );

  wrapCamera(
    aladin,
    "setRotation"
  );

  installObservers();

  state.raf.running=true;

  state.raf.id=
    requestAnimationFrame(
      rafTick
    );

  createPanel();

  push("install",{
    version:VERSION,
    designSeed:DESIGN_SEED,
    designRuns:DESIGN.length,

    userAgent:
      String(
        navigator.userAgent||""
      ),

    hardwareConcurrency:
      finite(
        navigator.hardwareConcurrency
      ),

    deviceMemoryGB:
      finite(
        navigator.deviceMemory
      ),

    devicePixelRatio:
      finite(
        global.devicePixelRatio
      ),

    screenWidth:
      finite(
        global.screen?.width
      ),

    screenHeight:
      finite(
        global.screen?.height
      ),

    viewportWidth:
      finite(
        global.innerWidth
      ),

    viewportHeight:
      finite(
        global.innerHeight
      ),

    ...memorySnapshot()
  });

  console.log(
    "GV STUTTER DOE LAB 0002 INSTALLED — 36 RUNS"
  );

  return api;
}

const api=
  Object.freeze({
    VERSION,

    install,

    prepareTravel,
    completeTravel,
    abortTravel,

    setManual,
    useDOE,

    downloadJSON,
    downloadRunsCSV,
    downloadFramesCSV,
    downloadCameraCSV,
    downloadPrewarmJSON,

    getDesign:
      ()=>DESIGN.map(
        row=>({...row})
      ),

    getRunSummaries:
      ()=>state.runSummaries.map(
        row=>({...row})
      ),

    getStatus:
      ()=>({
        mode:
          state.mode,

        completedRuns:
          state.runSummaries.length,

        expectedRuns:
          DESIGN.length,

        scheduleIndex:
          state.scheduleIndex,

        activeRun:
          state.activeRun
            ? {...state.activeRun}
            : null,

        nextRun:
          DESIGN[state.scheduleIndex]
            ? {...DESIGN[state.scheduleIndex]}
            : null
      }),

    get records(){
      return state.records;
    },

    get state(){
      return state;
    }
  });

global.GVStutterLab=api;

console.log(
  "GV STUTTER DOE LAB 0002 LOADED"
);

})(window);
