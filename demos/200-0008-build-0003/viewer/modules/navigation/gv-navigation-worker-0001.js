'use strict';

const WORKER_VERSION='0001';

importScripts('gv-navigation-0004.js');

const api=self.GalaxyViewerNavigation;

if(!api || api.VERSION!=='0004'){
  throw new Error('NAVIGATION WORKER 0001 — NAVIGATION 0004 LOAD FAILURE');
}

self.onmessage=event=>{
  const data=event?.data||{};
  const id=data.id;

  if(data.type!=='PLAN'){
    self.postMessage({
      type:'PLAN_RESULT',
      id,
      ok:false,
      workerVersion:WORKER_VERSION,
      error:'NAVIGATION WORKER 0001 — UNKNOWN MESSAGE'
    });
    return;
  }

  try{
    const plan=api.planRoute(
      Array.isArray(data.catalog)?data.catalog:[],
      {anchorRecord:data.anchorRecord||null}
    );

    self.postMessage({
      type:'PLAN_RESULT',
      id,
      ok:true,
      workerVersion:WORKER_VERSION,
      navigationVersion:api.VERSION,
      poolSize:plan.poolSize,
      routeLength:plan.routeLength,
      sampleAttempt:plan.sampleAttempt,
      solverAttempt:plan.solverAttempt,
      solveTimeMs:plan.solveTimeMs,
      routeKeys:plan.route.map(record=>api.identityOf(record)),
      discardedKeys:plan.discarded.map(record=>api.identityOf(record))
    });
  }catch(error){
    self.postMessage({
      type:'PLAN_RESULT',
      id,
      ok:false,
      workerVersion:WORKER_VERSION,
      navigationVersion:api.VERSION,
      error:String(error?.stack||error)
    });
  }
};
