/*
GALAXY VIEWER NAVIGATION PERFORMANCE 0001
ECO-ID: ECO-20260906-NAV-PERFORMANCE-MODULE-007

Independent optional navigation-performance recorder.
OFF by default. No permanent monkey-patching. No navigation-law ownership.
*/
(function(){
  'use strict';

  const VERSION='0001';
  const ALLOWED_DURATIONS=Object.freeze([17,15,12,9,6]);

  let enabled=false;
  let activeRun=null;
  let lastTelemetry=null;

  const finite=value=>{
    const n=Number(value);
    return Number.isFinite(n)?n:null;
  };

  const clamp01=value=>Math.max(0,Math.min(1,Number(value)||0));

  const percentile=(values,p)=>{
    const a=values.filter(Number.isFinite).slice().sort((x,y)=>x-y);
    if(!a.length)return null;
    return a[Math.min(a.length-1,Math.floor((a.length-1)*p))];
  };

  const mean=values=>{
    const a=values.filter(Number.isFinite);
    return a.length?a.reduce((s,x)=>s+x,0)/a.length:null;
  };

  const maxFinite=values=>{
    const a=values.filter(Number.isFinite);
    return a.length?Math.max(...a):null;
  };

  const minFinite=values=>{
    const a=values.filter(Number.isFinite);
    return a.length?Math.min(...a):null;
  };

  const shortestRotationDelta=(a,b)=>{
    if(!Number.isFinite(a)||!Number.isFinite(b))return null;
    return ((b-a+540)%360)-180;
  };

  const skySeparationDeg=(ra1,dec1,ra2,dec2)=>{
    if(![ra1,dec1,ra2,dec2].every(Number.isFinite))return null;
    const r=Math.PI/180;
    const d1=dec1*r,d2=dec2*r;
    const dra=(ra2-ra1)*r;
    const y=Math.sqrt(
      Math.pow(Math.cos(d2)*Math.sin(dra),2)+
      Math.pow(
        Math.cos(d1)*Math.sin(d2)-
        Math.sin(d1)*Math.cos(d2)*Math.cos(dra),
        2
      )
    );
    const x=
      Math.sin(d1)*Math.sin(d2)+
      Math.cos(d1)*Math.cos(d2)*Math.cos(dra);
    return Math.atan2(y,x)/r;
  };

  const phaseFor=(u,start=.30,end=.70)=>
    u<start?'ZOOM_OUT':
    u<end?'TRANSLATION':
    'ZOOM_IN';

  const readState=aladin=>{
    let rd=[null,null];
    let fv=[null,null];
    let rotation=null;

    try{rd=aladin.getRaDec?.()||rd}catch(_){}
    try{fv=aladin.getFov?.()||fv}catch(_){}
    try{rotation=aladin.getRotation?.()??null}catch(_){}

    const ra=finite(rd?.[0]);
    const dec=finite(rd?.[1]);
    const fovX=finite(Array.isArray(fv)?fv[0]:fv);
    const fovY=finite(Array.isArray(fv)?fv[1]:fv);
    const log2Fov=fovX>0?Math.log2(fovX):null;

    return {ra,dec,fovX,fovY,log2Fov,rotation:finite(rotation)};
  };

  const frameStats=(frames,budgetMs)=>{
    const dt=frames.map(x=>x.dtMs).filter(Number.isFinite);
    const over=dt.filter(x=>x>budgetMs);
    const excess=dt.reduce((s,x)=>s+Math.max(0,x-budgetMs),0);
    const total=dt.reduce((s,x)=>s+x,0);
    const missed=dt.reduce(
      (s,x)=>s+Math.max(0,Math.ceil(x/budgetMs)-1),
      0
    );

    return {
      count:dt.length,
      meanMs:mean(dt),
      medianMs:percentile(dt,.50),
      p95Ms:percentile(dt,.95),
      p99Ms:percentile(dt,.99),
      maxMs:maxFinite(dt),
      refreshBudgetMs:budgetMs,
      framesOverBudget:over.length,
      percentFramesOverBudget:dt.length?100*over.length/dt.length:0,
      estimatedMissedRefreshes:missed,
      stutterExcessMs:excess,
      stutterSeverityIndex:total>0?excess/total:0
    };
  };

  const phaseStats=(frames,phase,budgetMs)=>{
    const rows=frames.filter(x=>x.phase===phase);
    const absVelocity=rows.map(x=>Math.abs(x.zoomVelocityOctavesPerSec));
    const absAcceleration=rows.map(x=>Math.abs(x.zoomAccelerationOctavesPerSec2));
    const absJerk=rows.map(x=>Math.abs(x.zoomJerkOctavesPerSec3));

    return {
      phase,
      frames:rows.length,
      maxAbsZoomSpeedOctavesPerSec:maxFinite(absVelocity),
      maxAbsAccelerationOctavesPerSec2:maxFinite(absAcceleration),
      maxAbsJerkOctavesPerSec3:maxFinite(absJerk),
      frameTiming:frameStats(rows,budgetMs)
    };
  };

  const summarize=(run,endedAt)=>{
    const frames=run.frames;
    const observedFov=frames.map(x=>x.observed.fovX);
    const commandedFov=run.commands
      .map(x=>x.commanded?.fov)
      .filter(Number.isFinite);

    const startFov=run.startState.fovX;
    const destinationFov=
      [...observedFov].reverse().find(Number.isFinite)??null;

    const maxObservedFov=maxFinite(observedFov);
    const maxCommandedFov=maxFinite(commandedFov);

    const zoomVelocity=frames
      .map(x=>x.zoomVelocityOctavesPerSec)
      .filter(Number.isFinite);

    const acceleration=frames
      .map(x=>x.zoomAccelerationOctavesPerSec2)
      .filter(Number.isFinite);

    const jerk=frames
      .map(x=>x.zoomJerkOctavesPerSec3)
      .filter(Number.isFinite);

    const skyVelocity=frames
      .map(x=>x.skyVelocityDegPerSec)
      .filter(Number.isFinite);

    const rotationVelocity=frames
      .map(x=>Math.abs(x.rotationVelocityDegPerSec))
      .filter(Number.isFinite);

    const budgetMs=run.configuration.refreshBudgetMs;

    let fovRatioFromStart=null;
    let fovRatioToDestination=null;
    let octaveExcursion=null;

    if(maxObservedFov>0&&startFov>0)
      fovRatioFromStart=maxObservedFov/startFov;

    if(maxObservedFov>0&&destinationFov>0)
      fovRatioToDestination=maxObservedFov/destinationFov;

    const lowFov=minFinite([startFov,destinationFov]);
    if(maxObservedFov>0&&lowFov>0)
      octaveExcursion=Math.log2(maxObservedFov/lowFov);

    return {
      elapsedSec:(endedAt-run.startedAt)/1000,

      fov:{
        startFov,
        destinationFov,
        maxObservedFov,
        maxCommandedFov,
        fovRatioFromStart,
        fovRatioToDestination,
        octaveExcursion
      },

      motion:{
        maxZoomOutSpeedOctavesPerSec:maxFinite(zoomVelocity),
        maxZoomInSpeedOctavesPerSec:
          Math.abs(Math.min(0,minFinite(zoomVelocity)??0)),
        maxAccelerationOctavesPerSec2:
          Math.max(0,maxFinite(acceleration)??0),
        maxDecelerationOctavesPerSec2:
          Math.abs(Math.min(0,minFinite(acceleration)??0)),
        maxAbsJerkOctavesPerSec3:
          maxFinite(jerk.map(Math.abs)),
        maxSkyVelocityDegPerSec:maxFinite(skyVelocity),
        maxRotationVelocityDegPerSec:maxFinite(rotationVelocity)
      },

      frameTiming:frameStats(frames,budgetMs),

      phases:{
        zoomOut:phaseStats(frames,'ZOOM_OUT',budgetMs),
        translation:phaseStats(frames,'TRANSLATION',budgetMs),
        zoomIn:phaseStats(frames,'ZOOM_IN',budgetMs)
      }
    };
  };

  function enable(){
    enabled=true;
    return getState();
  }

  function disable(){
    enabled=false;
    return getState();
  }

  function isEnabled(){
    return enabled;
  }

  function getState(){
    return Object.freeze({
      version:VERSION,
      enabled,
      active:Boolean(activeRun),
      hasLastTelemetry:Boolean(lastTelemetry)
    });
  }

  function getLastTelemetry(){
    return lastTelemetry;
  }

  function downloadLastTelemetry(){
    if(!lastTelemetry)return false;

    const blob=new Blob(
      [JSON.stringify(lastTelemetry,null,2)],
      {type:'application/json'}
    );

    const link=document.createElement('a');
    link.href=URL.createObjectURL(blob);
    link.download=
      `gv-navigation-performance-0001-${lastTelemetry.configuration.travelSeconds}s-${Date.now()}.json`;

    document.body.appendChild(link);
    link.click();
    link.remove();

    setTimeout(()=>URL.revokeObjectURL(link.href),1000);
    return true;
  }

  async function run(configuration={}){
    if(!enabled)
      throw new Error('NAVIGATION PERFORMANCE MODULE IS DISABLED');

    if(activeRun)
      throw new Error('NAVIGATION PERFORMANCE RUN ALREADY ACTIVE');

    const core=configuration.core||window.GalaxyViewerCore||null;
    const aladin=configuration.aladin||core?.aladin||null;
    const randomGalaxy=
      configuration.randomGalaxy||
      core?.randomGalaxy||
      window.GalaxyViewerRandomGalaxy||
      null;

    if(!aladin)
      throw new Error('NAVIGATION PERFORMANCE ALADIN INSTANCE MISSING');

    if(!randomGalaxy||typeof randomGalaxy.travelToRandom!=='function')
      throw new Error('NAVIGATION PERFORMANCE RANDOM GALAXY INSTANCE MISSING');

    const requestedDuration=
      finite(configuration.travelSeconds) ??
      finite(randomGalaxy.options?.travelSeconds) ??
      17;

    if(!ALLOWED_DURATIONS.includes(requestedDuration))
      throw new Error(
        `NAVIGATION PERFORMANCE INVALID DURATION ${requestedDuration}; `+
        `ALLOWED ${ALLOWED_DURATIONS.join('/')}`
      );

    const refreshHz=
      finite(configuration.refreshHz)>0
        ? finite(configuration.refreshHz)
        : 60;

    const phaseStart=
      finite(configuration.phaseStart) ??
      finite(randomGalaxy.options?.translateStart) ??
      .30;

    const phaseEnd=
      finite(configuration.phaseEnd) ??
      finite(randomGalaxy.options?.translationComplete) ??
      .70;

    const runRecord={
      schema:'GV-NAVIGATION-PERFORMANCE-0001',
      moduleVersion:VERSION,
      viewerVersion:core?.version??null,
      randomGalaxyVersion:window.GalaxyRandomGalaxy?.VERSION??null,
      startedAt:performance.now(),
      generatedAt:new Date().toISOString(),
      configuration:{
        travelSeconds:requestedDuration,
        refreshHz,
        refreshBudgetMs:1000/refreshHz,
        phaseStart,
        phaseEnd
      },
      startState:readState(aladin),
      destination:null,
      error:null,
      commands:[],
      frames:[],
      summary:null,
      lastFrameAt:null,
      rafId:0
    };

    activeRun=runRecord;

    const oldTravelSeconds=randomGalaxy.options?.travelSeconds;
    if(randomGalaxy.options)
      randomGalaxy.options.travelSeconds=requestedDuration;

    const commandState={
      ra:runRecord.startState.ra,
      dec:runRecord.startState.dec,
      fov:runRecord.startState.fovX,
      rotation:runRecord.startState.rotation
    };

    const originals=new Map();

    const instrument=method=>{
      const original=aladin[method];
      if(typeof original!=='function')return;

      const wrapped=function(...args){
        const active=activeRun;

        if(active===runRecord){
          if(method==='gotoRaDec'){
            commandState.ra=finite(args[0]);
            commandState.dec=finite(args[1]);
          }else if(method==='setFov'){
            commandState.fov=finite(args[0]);
          }else if(method==='setRotation'){
            commandState.rotation=finite(args[0]);
          }

          const now=performance.now();
          const elapsedSec=(now-runRecord.startedAt)/1000;
          const u=clamp01(elapsedSec/requestedDuration);

          runRecord.commands.push({
            elapsedSec,
            u,
            phase:phaseFor(u,phaseStart,phaseEnd),
            method,
            args:[...args],
            commanded:{...commandState}
          });
        }

        return original.apply(aladin,args);
      };

      originals.set(method,{original,wrapped});
      aladin[method]=wrapped;
    };

    for(const method of ['gotoRaDec','setFov','setRotation'])
      instrument(method);

    const sampleFrame=now=>{
      if(activeRun!==runRecord)return;

      const elapsedSec=(now-runRecord.startedAt)/1000;
      const u=clamp01(elapsedSec/requestedDuration);
      const observed=readState(aladin);

      const previous=runRecord.frames[runRecord.frames.length-1]||null;
      const dtMs=
        runRecord.lastFrameAt===null
          ? null
          : now-runRecord.lastFrameAt;

      let zoomVelocity=null;
      let zoomAcceleration=null;
      let zoomJerk=null;
      let skyVelocity=null;
      let rotationVelocity=null;

      if(previous&&dtMs>0){
        const dt=dtMs/1000;

        if(
          Number.isFinite(observed.log2Fov)&&
          Number.isFinite(previous.observed.log2Fov)
        ){
          zoomVelocity=
            (observed.log2Fov-previous.observed.log2Fov)/dt;
        }

        if(
          Number.isFinite(zoomVelocity)&&
          Number.isFinite(previous.zoomVelocityOctavesPerSec)
        ){
          zoomAcceleration=
            (zoomVelocity-previous.zoomVelocityOctavesPerSec)/dt;
        }

        if(
          Number.isFinite(zoomAcceleration)&&
          Number.isFinite(previous.zoomAccelerationOctavesPerSec2)
        ){
          zoomJerk=
            (zoomAcceleration-previous.zoomAccelerationOctavesPerSec2)/dt;
        }

        const separation=skySeparationDeg(
          previous.observed.ra,
          previous.observed.dec,
          observed.ra,
          observed.dec
        );

        if(Number.isFinite(separation))
          skyVelocity=separation/dt;

        const rotationDelta=shortestRotationDelta(
          previous.observed.rotation,
          observed.rotation
        );

        if(Number.isFinite(rotationDelta))
          rotationVelocity=rotationDelta/dt;
      }

      runRecord.lastFrameAt=now;

      runRecord.frames.push({
        elapsedSec,
        u,
        phase:phaseFor(u,phaseStart,phaseEnd),
        dtMs,
        commanded:{...commandState},
        observed,
        octavePosition:
          Number.isFinite(observed.log2Fov)&&
          Number.isFinite(runRecord.startState.log2Fov)
            ? observed.log2Fov-runRecord.startState.log2Fov
            : null,
        zoomVelocityOctavesPerSec:zoomVelocity,
        zoomAccelerationOctavesPerSec2:zoomAcceleration,
        zoomJerkOctavesPerSec3:zoomJerk,
        skyVelocityDegPerSec:skyVelocity,
        rotationVelocityDegPerSec:rotationVelocity
      });

      runRecord.rafId=requestAnimationFrame(sampleFrame);
    };

    runRecord.rafId=requestAnimationFrame(sampleFrame);

    try{
      runRecord.destination=await randomGalaxy.travelToRandom();
    }catch(error){
      runRecord.error={
        name:String(error?.name||'Error'),
        message:String(error?.message||error),
        stack:String(error?.stack||'')
      };
      throw error;
    }finally{
      cancelAnimationFrame(runRecord.rafId);

      for(const [method,state] of originals){
        if(aladin[method]===state.wrapped)
          aladin[method]=state.original;
      }

      if(randomGalaxy.options)
        randomGalaxy.options.travelSeconds=oldTravelSeconds;

      const endedAt=performance.now();
      runRecord.summary=summarize(runRecord,endedAt);

      lastTelemetry=Object.freeze({
        schema:runRecord.schema,
        moduleVersion:runRecord.moduleVersion,
        viewerVersion:runRecord.viewerVersion,
        randomGalaxyVersion:runRecord.randomGalaxyVersion,
        generatedAt:runRecord.generatedAt,
        configuration:Object.freeze({...runRecord.configuration}),
        startState:Object.freeze({...runRecord.startState}),
        destination:runRecord.destination,
        error:runRecord.error,
        summary:runRecord.summary,
        commands:runRecord.commands,
        frames:runRecord.frames
      });

      activeRun=null;
    }

    return lastTelemetry;
  }

  window.GalaxyViewerNavigationPerformance=Object.freeze({
    VERSION,
    ALLOWED_DURATIONS,
    enable,
    disable,
    isEnabled,
    getState,
    run,
    getLastTelemetry,
    downloadLastTelemetry
  });
})();
