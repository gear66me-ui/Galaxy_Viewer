"use strict";
const fs=require("fs"),vm=require("vm");
const file=process.argv[2];
let NOW=0,rafCalls=0;
const observers=[];
class PO{
  static supportedEntryTypes=["longtask","long-animation-frame"];
  constructor(cb){this.cb=cb;this.types=[];observers.push(this)}
  observe(x){this.types=x.entryTypes||[]}
}
function emit(type,start=NOW){
  const entry={startTime:start,duration:70,blockingDuration:15};
  for(const o of observers){
    if(o.types.includes(type))o.cb({getEntries:()=>[entry]});
  }
}
const perf={now:()=>NOW};
const win={
  devicePixelRatio:2,
  screen:{width:1080,height:2340},
  innerWidth:1080,innerHeight:2200
};
const ctx={
  window:win,
  console,
  performance:perf,
  PerformanceObserver:PO,
  requestAnimationFrame:()=>++rafCalls,
  navigator:{userAgent:"GV-DOE-MOCK",hardwareConcurrency:8,deviceMemory:4},
  setTimeout,clearTimeout,
  Math,Number,String,Boolean,Array,Object,JSON,Date,Map,Set,WeakMap,Error
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(file,"utf8"),ctx,{filename:file});
const L=win.GVStutterLab;
function A(x,m){if(!x)throw Error("ASSERT FAIL - "+m)}
function count(t){return L.records.filter(r=>r.type===t).length}
const calls={f:0,g:0,r:0};
const aladin={
  setFov(){calls.f++},gotoRaDec(){calls.g++},setRotation(){calls.r++},
  getRaDec(){return[0,0]},getFov(){return[1,1]},getRotation(){return 0}
};
const C={aladin,options:{
  travelSeconds:17,maxFov:120,translateStart:.3,turnPoint:.5,
  translate90:.7,translationComplete:.7
}};
const S=i=>({
  name:"S"+i,
  ra:(i*7)%360,
  dec:-20+i%30,
  distance:20+i,
  aladinRotation:(i*11)%360
});
const D=i=>({
  name:"D"+i,
  ra:(i*7+80)%360,
  dec:-10+i%20,
  distance:80+i,
  aladinRotation:(i*11+60)%360,
  fovDegrees:.2,
  provider:"MOCK"
});

console.log("============================================================");
console.log(" GALAXY VIEWER — LAB0004 MOCK RUNTIME");
console.log("============================================================");

A(L&&L.VERSION==="0004","LAB0004 API/version");
L.install(aladin);
A(rafCalls===0,"install created RAF");
console.log("INSTALL IDLE RAF: 0 — PASS");

const design=L.getDesign();
A(design.length===36,"design length");
A(new Set(design.map(x=>x.conditionId)).size===12,"condition count");
for(let b=1;b<=3;b++){
  const rows=design.filter(r=>r.block===b);
  A(rows.length===12&&new Set(rows.map(r=>r.conditionId)).size===12,"block "+b);
}
console.log("DOE DESIGN 36 / 12 / 3 BLOCKS: PASS");

// First-home bootstrap must never enter the DOE.
L.prepareTravel(C,{
  firstHomeTrip:true,
  source:S(0),
  destination:D(0),
  startFov:1
});
L.beginAnimation({firstHomeTrip:true,startedPerfMs:0});
L.sampleAnimationFrame(16.7);
L.endAnimation({firstHomeTrip:true,endedPerfMs:100});
L.completeTravel({firstHomeTrip:true,destination:D(0)});
A(
  L.getStatus().scheduleIndex===0 &&
  L.getStatus().completedRuns===0 &&
  count("frame")===0,
  "first-home exclusion"
);
console.log("FIRST-HOME EXCLUSION: PASS");

// Abort one measured attempt. Same DOE condition must remain next.
NOW=1000;
L.prepareTravel(C,{source:S(1),destination:D(1),startFov:1});
const retryOrder=L.getStatus().activeRun.scheduleOrder;
A(L.beginAnimation({startedPerfMs:NOW,durationMs:10000}).started,"abort begin");
NOW+=16.7;
aladin.setFov(1);
aladin.gotoRaDec(1,2);
aladin.setRotation(3);
L.sampleAnimationFrame(NOW);
L.abortTravel(Error("MOCK"));
A(L.getStatus().completedRuns===0,"abort advanced completed count");
A(L.getStatus().nextRun.scheduleOrder===retryOrder,"abort changed DOE condition");
console.log("ABORT / RETRY SAME CONDITION: PASS");

let activeLT=0,activeLF=0;
for(let i=0;i<36;i++){
  const row=design[i], s=S(i+10), d=D(i+10);
  NOW+=200;

  L.prepareTravel(C,{source:s,destination:d,startFov:1});
  const start=NOW;
  const dur=row.totalTravelSec*1000;

  A(
    L.getStatus().activeRun.scheduleOrder===row.scheduleOrder,
    "wrong schedule order "+(i+1)
  );

  const begun=L.beginAnimation({
    startedPerfMs:start,
    durationMs:dur,
    source:s,
    destination:d
  });
  A(begun.started,"begin "+(i+1));

  for(const f of [.25,.50,.75,1]){
    NOW=start+dur*f;

    aladin.setFov(120-100*f);
    aladin.gotoRaDec(d.ra,d.dec);
    aladin.setRotation(d.aladinRotation);

    if(i===0 && f===.50){
      emit("longtask");
      emit("long-animation-frame");
      activeLT++;
      activeLF++;
    }

    L.sampleAnimationFrame(NOW);
  }

  NOW=start+dur;
  A(
    L.endAnimation({
      endedPerfMs:NOW,
      destination:d
    }).ended,
    "end "+(i+1)
  );

  // After exact animation end, but before completeTravel:
  // camera calls, observer entries, and sampler calls must be silent.
  const postEndRecords=L.records.length;
  NOW+=25;
  emit("longtask");
  emit("long-animation-frame");
  aladin.setFov(2);
  aladin.gotoRaDec(3,4);
  aladin.setRotation(5);
  L.sampleAnimationFrame(NOW);
  A(
    L.records.length===postEndRecords,
    "post-end telemetry leak "+(i+1)
  );

  L.completeTravel({
    destination:d,
    route:{value:100}
  });

  const idleRecords=L.records.length;
  const idleFrames=count("frame");
  const idleCamera=count("camera");

  // Fully idle after run completion must also remain silent.
  NOW+=25;
  emit("longtask");
  emit("long-animation-frame");
  aladin.setFov(2);
  aladin.gotoRaDec(3,4);
  aladin.setRotation(5);
  L.sampleAnimationFrame(NOW);

  A(L.records.length===idleRecords,"idle record leak "+(i+1));
  A(count("frame")===idleFrames,"idle frame leak "+(i+1));
  A(count("camera")===idleCamera,"idle camera leak "+(i+1));
  A(L.getStatus().completedRuns===i+1,"completed count "+(i+1));
  A(L.getStatus().scheduleIndex===i+1,"schedule advance "+(i+1));
}
const st=L.getStatus();
const sum=L.getRunSummaries();
const frames=L.records.filter(r=>r.type==="frame");

A(
  st.completedRuns===36 &&
  st.scheduleIndex===36 &&
  st.nextRun===null,
  "final state"
);
A(sum.length===36,"summary count");

for(const x of sum){
  A(
    Math.abs(x.measuredDurationMs-x.totalTravelSec*1000)<.001,
    "duration run "+x.scheduleOrder
  );
}

A(frames.every(x=>x.phase!=="IDLE"),"idle frame exists");
A(rafCalls===0,"lab requested RAF");
A(
  count("longtask")===activeLT &&
  count("long_animation_frame")===activeLF,
  "observer idle leak"
);

const reps={};
for(const x of sum)
  reps[x.conditionId]=(reps[x.conditionId]||0)+1;

A(
  Object.values(reps).every(x=>x===3),
  "replicate counts"
);

console.log("36/36 ADVANCEMENT: PASS");
console.log("12 CONDITIONS x 3 REPLICATES: PASS");
console.log("MEASURED DURATION = COMMANDED: PASS");
console.log("ACTIVE FRAMES:",frames.length);
console.log("IDLE FRAMES: 0 — PASS");
console.log("IDLE CAMERA ACCUMULATION: 0 — PASS");
console.log("POST-END/IDLE OBSERVER LEAK: 0 — PASS");
console.log("LAB-OWNED RAF REQUESTS:",rafCalls,"— PASS");
console.log(JSON.stringify(st,null,2));
console.log("============================================================");
console.log("LAB0004 MOCK RUNTIME VALIDATION COMPLETE — PASS");
console.log("============================================================");
