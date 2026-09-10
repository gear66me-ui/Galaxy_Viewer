(function(global){
  "use strict";

  const VERSION="0001";

  const state={
    version:VERSION,
    enabled:true,
    installed:false,
    sessionId:"GVSL-"+Date.now()+"-"+Math.random().toString(36).slice(2,10),
    startedAt:performance.now(),
    seq:0,
    records:[],
    maxRecords:250000,

    condition:{
      label:"OBSERVATIONAL",
      doeRun:null,
      replicate:null,
      totalTravelSec:null,
      zoomOutSec:null,
      motionSec:null,
      zoomInSec:null
    },

    currentBurstId:0,
    lastCameraAt:null,
    lastCameraSeq:null,
    burstGapMs:1500,

    raf:{
      running:false,
      id:null,
      frameIndex:0,
      lastNow:null,
      lastDelta:null,
      pendingCommands:[]
    },

    originals:{},
    observers:[]
  };

  function finite(v){
    const n=Number(v);
    return Number.isFinite(n)?n:null;
  }

  function memory(){
    const m=performance.memory;
    return m ? {
      heapUsedBytes:finite(m.usedJSHeapSize),
      heapTotalBytes:finite(m.totalJSHeapSize),
      heapLimitBytes:finite(m.jsHeapSizeLimit)
    } : {};
  }

  function push(type,data={}){
    if(!state.enabled)return null;

    if(state.records.length>=state.maxRecords)
      state.records.shift();

    const e={
      seq:++state.seq,
      sessionId:state.sessionId,
      elapsedMs:+(performance.now()-state.startedAt).toFixed(3),
      type,
      conditionLabel:state.condition.label,
      doeRun:state.condition.doeRun,
      replicate:state.condition.replicate,
      totalTravelSec:state.condition.totalTravelSec,
      zoomOutSec:state.condition.zoomOutSec,
      motionSec:state.condition.motionSec,
      zoomInSec:state.condition.zoomInSec,
      ...data
    };

    state.records.push(e);
    return e;
  }

  function argsArray(args){
    return Array.from(args).map(v=>{
      const n=Number(v);
      return Number.isFinite(n) ? n : String(v);
    });
  }

  function wrap(aladin,name){
    const original=aladin?.[name];

    if(typeof original!=="function"){
      push("warning",{message:"METHOD MISSING",method:name});
      return;
    }

    if(original.__gvStutterLabWrapped)return;

    state.originals[name]=original;

    const wrapped=function(...args){
      const begin=performance.now();

      const gap=
        state.lastCameraAt===null
          ? Infinity
          : begin-state.lastCameraAt;

      if(gap>state.burstGapMs){
        state.currentBurstId++;
        push("burst_start",{
          burstId:state.currentBurstId,
          precedingIdleMs:Number.isFinite(gap)?+gap.toFixed(3):null
        });
      }

      let ok=true;
      let errorMessage="";

      try{
        return original.apply(this,args);
      }catch(error){
        ok=false;
        errorMessage=String(error?.message||error);
        throw error;
      }finally{
        const end=performance.now();

        const row=push("camera",{
          burstId:state.currentBurstId,
          method:name,
          args:argsArray(args),
          callStartMs:+(begin-state.startedAt).toFixed(3),
          callEndMs:+(end-state.startedAt).toFixed(3),
          callMs:+(end-begin).toFixed(3),
          rafDeltaBeforeMs:
            state.raf.lastDelta===null
              ? null
              : +state.raf.lastDelta.toFixed(3),
          ok,
          errorMessage,
          ...memory()
        });

        state.raf.pendingCommands.push({
          seq:row?.seq||null,
          method:name,
          callMs:+(end-begin).toFixed(3)
        });

        state.lastCameraAt=end;
        state.lastCameraSeq=row?.seq||null;
      }
    };

    Object.defineProperty(wrapped,"__gvStutterLabWrapped",{
      value:true
    });

    aladin[name]=wrapped;
  }

  function rafTick(now){
    if(!state.raf.running)return;

    const previous=state.raf.lastNow;
    const dt=previous===null ? null : now-previous;

    state.raf.lastNow=now;
    state.raf.lastDelta=dt;
    state.raf.frameIndex++;

    const commands=state.raf.pendingCommands.splice(0);
    const mask=[...new Set(commands.map(x=>x.method))].sort().join("+") || "NONE";

    push("frame",{
      frameIndex:state.raf.frameIndex,
      burstId:state.currentBurstId||null,
      rafDeltaMs:dt===null?null:+dt.toFixed(3),
      fps:dt&&dt>0?+(1000/dt).toFixed(3):null,

      over16_7:dt!==null&&dt>=16.7,
      over25:dt!==null&&dt>=25,
      over33_3:dt!==null&&dt>=33.3,
      over50:dt!==null&&dt>=50,
      over100:dt!==null&&dt>=100,

      commandCount:commands.length,
      commandMask:mask,
      cameraCallMsTotal:+commands
        .reduce((s,x)=>s+(Number(x.callMs)||0),0)
        .toFixed(3),

      commandSeqs:commands.map(x=>x.seq),

      ...memory()
    });

    state.raf.id=requestAnimationFrame(rafTick);
  }

  function installObservers(){
    if(typeof PerformanceObserver!=="function")return;

    const supported=PerformanceObserver.supportedEntryTypes||[];

    if(supported.includes("longtask")){
      try{
        const o=new PerformanceObserver(list=>{
          for(const e of list.getEntries()){
            push("longtask",{
              startTimeMs:+e.startTime.toFixed(3),
              durationMs:+e.duration.toFixed(3),
              burstId:state.currentBurstId||null,
              lastCameraSeq:state.lastCameraSeq
            });
          }
        });

        o.observe({entryTypes:["longtask"]});
        state.observers.push(o);
      }catch(_){}
    }

    if(supported.includes("long-animation-frame")){
      try{
        const o=new PerformanceObserver(list=>{
          for(const e of list.getEntries()){
            push("long_animation_frame",{
              startTimeMs:+e.startTime.toFixed(3),
              durationMs:+e.duration.toFixed(3),
              blockingDurationMs:finite(e.blockingDuration),
              burstId:state.currentBurstId||null,
              lastCameraSeq:state.lastCameraSeq
            });
          }
        });

        o.observe({entryTypes:["long-animation-frame"]});
        state.observers.push(o);
      }catch(_){}
    }
  }

  function install(aladin){
    if(state.installed)return api;

    if(!aladin)
      throw new Error("GV STUTTER LAB: ALADIN INSTANCE MISSING");

    state.installed=true;

    wrap(aladin,"setFov");
    wrap(aladin,"gotoRaDec");
    wrap(aladin,"setRotation");

    installObservers();

    state.raf.running=true;
    requestAnimationFrame(rafTick);

    push("install",{
      userAgent:navigator.userAgent,
      hardwareConcurrency:finite(navigator.hardwareConcurrency),
      deviceMemoryGB:finite(navigator.deviceMemory),
      devicePixelRatio:finite(global.devicePixelRatio),
      viewportWidth:finite(global.innerWidth),
      viewportHeight:finite(global.innerHeight),
      ...memory()
    });

    console.log("GV STUTTER LAB 0001 INSTALLED");

    return api;
  }

  function setCondition(label,factors={}){
    state.condition={
      ...state.condition,
      label:String(label||"UNLABELED"),
      ...factors
    };

    push("condition_change",{
      condition:{...state.condition}
    });

    return {...state.condition};
  }

  function mark(label,detail={}){
    return push("mark",{label,detail});
  }

  function reset(){
    state.records.length=0;
    state.seq=0;
    state.startedAt=performance.now();
    state.currentBurstId=0;
    state.lastCameraAt=null;
    state.lastCameraSeq=null;
    state.raf.frameIndex=0;
    state.raf.lastNow=null;
    state.raf.lastDelta=null;
    state.raf.pendingCommands.length=0;
    return true;
  }

  function snapshot(){
    return {
      metadata:{
        version:VERSION,
        sessionId:state.sessionId,
        createdAt:new Date().toISOString()
      },
      condition:{...state.condition},
      records:state.records.slice()
    };
  }

  function csvEscape(v){
    if(v===null||v===undefined)return "";

    let s=typeof v==="object" ? JSON.stringify(v) : String(v);

    if(/[",\n\r]/.test(s))
      s="\""+s.replace(/"/g,"\"\"")+"\"";

    return s;
  }

  function csv(type){
    const rows=state.records.filter(r=>r.type===type);

    const keys=[...new Set(rows.flatMap(r=>Object.keys(r)))];

    return [
      keys.join(","),
      ...rows.map(r=>keys.map(k=>csvEscape(r[k])).join(","))
    ].join("\n");
  }

  function download(name,text,type){
    const b=new Blob([text],{type});
    const u=URL.createObjectURL(b);
    const a=document.createElement("a");

    a.href=u;
    a.download=name;
    document.body.appendChild(a);
    a.click();
    a.remove();

    setTimeout(()=>URL.revokeObjectURL(u),2000);
  }

  function downloadJSON(){
    download(
      "gv-stutter-"+state.sessionId+".json",
      JSON.stringify(snapshot(),null,2),
      "application/json"
    );
  }

  function downloadFramesCSV(){
    download(
      "gv-stutter-frames-"+state.sessionId+".csv",
      csv("frame"),
      "text/csv"
    );
  }

  function downloadCameraCSV(){
    download(
      "gv-stutter-camera-"+state.sessionId+".csv",
      csv("camera"),
      "text/csv"
    );
  }

  const api=Object.freeze({
    VERSION,
    install,
    setCondition,
    mark,
    reset,
    snapshot,
    downloadJSON,
    downloadFramesCSV,
    downloadCameraCSV,
    get records(){return state.records},
    get state(){return state}
  });

  global.GVStutterLab=api;

  console.log("GV STUTTER LAB 0001 LOADED");
})(window);
