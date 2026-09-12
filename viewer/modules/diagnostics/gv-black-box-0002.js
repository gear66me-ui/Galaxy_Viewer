/* Galaxy Viewer Black Box 0001 — passive crash-surviving navigation recorder */
(function(global){
  'use strict';
  const VERSION='0002';
  const DB_NAME='galaxy-viewer-black-box';
  const DB_VERSION=1;
  let dbPromise=null;
  function openDb(){
    if(dbPromise)return dbPromise;
    dbPromise=new Promise((resolve,reject)=>{
      const req=indexedDB.open(DB_NAME,DB_VERSION);
      req.onupgradeneeded=()=>{
        const db=req.result;
        if(!db.objectStoreNames.contains('runs'))db.createObjectStore('runs',{keyPath:'id'});
        if(!db.objectStoreNames.contains('samples')){const s=db.createObjectStore('samples',{keyPath:'id',autoIncrement:true});s.createIndex('runId','runId',{unique:false});}
      };
      req.onsuccess=()=>{const db=req.result;db.onversionchange=()=>{db.close();dbPromise=null;};resolve(db);};
      req.onerror=()=>{dbPromise=null;reject(req.error);};
    });
    return dbPromise;
  }
  async function startRun(metadata={}) {
    const db=await openDb();
    const id='gvbb-'+Date.now()+'-'+Math.random().toString(36).slice(2,10);
    const record={id,status:'ACTIVE',startedAt:new Date().toISOString(),endedAt:null,metadata};
    await new Promise((resolve,reject)=>{
      const tx=db.transaction('runs','readwrite');
      tx.objectStore('runs').put(record);
      tx.oncomplete=()=>resolve();
      tx.onerror=()=>reject(tx.error);
      tx.onabort=()=>reject(tx.error||new Error('BLACK BOX START ABORTED'));
    });
    return record;
  }

  async function appendSample(runId,sample={}) {
    const db=await openDb();
    const record={runId,recordedAt:new Date().toISOString(),sample};
    await new Promise((resolve,reject)=>{
      const tx=db.transaction('samples','readwrite');
      tx.objectStore('samples').add(record);
      tx.oncomplete=()=>resolve();
      tx.onerror=()=>reject(tx.error);
      tx.onabort=()=>reject(tx.error||new Error('BLACK BOX SAMPLE ABORTED'));
    });
    return record;
  }

  async function finishRun(runId,result={}) {
    const db=await openDb();
    const updated=await new Promise((resolve,reject)=>{
      let completedRecord=null;
      const tx=db.transaction('runs','readwrite');
      const store=tx.objectStore('runs');
      const req=store.get(runId);
      req.onsuccess=()=>{
        const record=req.result;
        if(!record){reject(new Error('BLACK BOX RUN NOT FOUND'));return;}
        record.status=result?.status==='ERROR'?'ERROR':'COMPLETE';
        record.endedAt=new Date().toISOString();
        record.result=result;
        completedRecord=record;
        store.put(record);
      };
      req.onerror=()=>reject(req.error);
      tx.oncomplete=()=>resolve(completedRecord);
      tx.onerror=()=>reject(tx.error);
      tx.onabort=()=>reject(tx.error||new Error('BLACK BOX FINISH ABORTED'));
    });
    return updated;
  }

  async function getIncompleteRuns(){
    const db=await openDb();
    const runs=await new Promise((resolve,reject)=>{
      const tx=db.transaction('runs','readonly');
      const req=tx.objectStore('runs').getAll();
      req.onsuccess=()=>resolve((req.result||[]).filter(r=>r&&r.status==='ACTIVE').sort((a,b)=>String(b.startedAt||'').localeCompare(String(a.startedAt||''))));
      req.onerror=()=>reject(req.error);
      tx.onabort=()=>reject(tx.error||new Error('BLACK BOX RECOVERY READ ABORTED'));
    });
    return runs;
  }

  async function getRunBundle(runId){
    const db=await openDb();
    const run=await new Promise((resolve,reject)=>{
      const tx=db.transaction('runs','readonly');
      const req=tx.objectStore('runs').get(runId);
      req.onsuccess=()=>resolve(req.result||null);
      req.onerror=()=>reject(req.error);
      tx.onabort=()=>reject(tx.error||new Error('BLACK BOX RUN READ ABORTED'));
    });
    const samples=await new Promise((resolve,reject)=>{
      const tx=db.transaction('samples','readonly');
      const req=tx.objectStore('samples').index('runId').getAll(IDBKeyRange.only(runId));
      req.onsuccess=()=>resolve(req.result||[]);
      req.onerror=()=>reject(req.error);
      tx.onabort=()=>reject(tx.error||new Error('BLACK BOX SAMPLE READ ABORTED'));
    });
    return {blackBoxVersion:VERSION,exportedAt:new Date().toISOString(),run,samples};
  }

  let activeRunPromise=null;
  let lastRunPromise=null;
  let writeChain=Promise.resolve();
  let lastSample=null;

  const finite=v=>Number.isFinite(Number(v))?Number(v):null;
  const clamp=(v,mn,mhx)=>Math.max(mn,Math.min(mx,v));
  function angleDeltaDeg(a,b){
    const a0n=finite(a),b0n=finite(b);
    if(a0n==null||b0n==null)return null;
    return ((b0n-a0n+540)%360)-180;
  }
  function skyDistanceDeg(ra1,dec1,ra2,dec2){
    const aa=finite(ra1),bb=finite(dec1),cc=finite(ra2),dd=finite(dec2);
    if([aa,bb,cc,dd].some(v=>v==null))return null;
    const r=Math.PI/180;
    const d11=bb*r,d22=dd*r,dr=(cc-aa)*r;
    const c=clamp(Math.sin(d11)*Math.sin(d22)+Math.cos(d11)*Math.cos(d22)*Math.cos(dr),-1,1);
    return Math.acos(c)/r ;
  }

  function enrichSample(sample={}){
    const out={...sample};
    const now=finite(out.elapsedMs);
    const prev=lastSample;
    if(prev&&now!=null){
      const dt=(now-Number(prev.elapsedMs))/1000;
      if(dt>0){
        const ra=finite(out.actualRa)??finite(out.commandedRa);
        const dec=finite(out.actualDec)??finite(out.commandedDec);
        const pra=finite(prev.actualRa)??finite(prev.commandedRa);
        const pdec=finite(prev.actualDec)??finite(prev.commandedDec);
        const dsky=skyDistanceDeg(pra,pdec,ra,dec);
        if(dsky!=null)out.skyVelocityDegPerSec=dsky/dt;
        const fov=finite(out.actualFov)??finite(out.commandedFov);
        const pfov=finite(prev.actualFov)??finite(prev.commandedFov);
        if(fov!=null&&pfov!=null)out.fovVelocityDegPerSec=(fov-pfov)/dt;
        const rot=finite(out.actualRotation)??finite(out.commandedRotation);
        const prot=finite(prev.actualRotation)??finite(prev.commandedRotation);
        const drot=angleDeltaDeg(prot,rot);
        if(drot!=null)out.rotationVelocityDegPerSec=drot/dt;
        if(finite(prev.skyVelocityDegPerSec)!=null&&finite(out.skyVelocityDegPerSec)!=null)out.skyAccelerationDegPerSec2=(Number(out.skyVelocityDegPerSec)-Number(prev.skyVelocityDegPerSec))/dt;
        if(finite(prev.fovVelocityDegPerSec)!=null&&finite(out.fovVelocityDegPerSec)!=null)out.fovAccelerationDegPerSec2=(Number(out.fovVelocityDegPerSec)-Number(prev.fovVelocityDegPerSec))/dt;
        if(finite(prev.rotationVelocityDegPerSec)!=null&&finite(out.rotationVelocityDegPerSec)!=null)out.rotationAccelerationDegPerSec2=(Number(out.rotationVelocityDegPerSec)-Number(prev.rotationVelocityDegPerSec))/dt;
      }
    }
    lastSample=out;
    return out;
  }

  function beginNavigation(metadata={}){
    lastSample=null;
    writeChain=Promise.resolve();
    activeRunPromise=startRun(metadata).catch(error=>{console.error('BLACK BOX START FAILURE',error);return null;});
    lastRunPromise=activeRunPromise;
    return activeRunPromise;
  }
  function recordNavigation(sample={}){
    if(!activeRunPromise)return false;
    const enriched=enrichSample(sample);
    const runPromise=activeRunPromise;
    writeChain=writeChain.then(async()=>{const run=await runPromise;if(run)await appendSample(run.id,enriched);}).catch(error=>console.error('BLACK BOX SAMPLE FAILURE',error));
    return true;
  }
  function recordCheckpoint(label,detail={}){
    const runPromise=activeRunPromise||lastRunPromise;
    if(!runPromise)return false;
    const event={recordType:"CHECKPOINT",label:String(label||"UNKNOWN"),perfMs:performance.now(),detail};
    writeChain=writeChain.then(async()=>{const run=await runPromise;if(run)await appendSample(run.id,event);}).catch(error=>console.error("BLACK BOX CHECKPOINT FAILURE",error));
    return true;
  }

  function endNavigation(result={}){
    if(!activeRunPromise)return Promise.resolve(null);
    const runPromise=activeRunPromise;
    activeRunPromise=null;
    lastSample=null;
    const done=writeChain.then(async()=>{const run=await runPromise;return run?await finishRun(run.id,result):null;}).catch(error=>{console.error('BLACK BOX FINISH FAILURE',error);return null;});
    return done;
  }

  function installEventBridge(){
    global.addEventListener('gv-black-box-nav-start',e=>beginNavigation(e.detail||{}));
    global.addEventListener('gv-black-box-nav-sample',e=>recordNavigation(e.detail||{}));
    global.addEventListener('gv-black-box-nav-finish',e=>endNavigation({status:'COMPLETE',...(e.detail||{})}));
    global.addEventListener('gv-black-box-nav-error',e=>endNavigation({status:'ERROR',...(e.detail||{})}));
    global.addEventListener("gv-black-box-checkpoint",e=>recordCheckpoint(e.detail?.label,e.detail?.detail||{}));
    global.addEventListener("error",e=>recordCheckpoint("WINDOW_ERROR",{message:e.message||null,filename:e.filename||null,lineno:e.lineno||null,colno:e.colno||null,stack:e.error?.stack||null}));
    global.addEventListener("unhandledrejection",e=>{const r=e.reason;recordCheckpoint("UNHANDLED_REJECTION",{message:String(r?.message||r||"UNKNOWN"),stack:r?.stack||null});});
  }

  installEventBridge();

  global.GalaxyBlackBox=Object.freeze({version:VERSION,openDb,startRun,appendSample,finishRun,getIncompleteRuns,getRunBundle,beginNavigation,recordNavigation,recordCheckpoint,endNavigation});
})(window);
