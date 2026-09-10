from pathlib import Path
p=Path.home()/"GV_AR05_PUSH/viewer/modules/diagnostics/gv-stutter-lab-0004.js"
s=p.read_text()
pairs=[
('phase:"ZOOM_OUT"','phase:"ARC_LEAD"',1),
('phase:"MOTION"','phase:"MOTION_OVERLAP"',1),
('phase:"ZOOM_IN"','phase:"ARC_TRAIL"',1),
('phaseStats("ZOOM_OUT")','phaseStats("ARC_LEAD")',1),
('phaseStats("MOTION")','phaseStats("MOTION_OVERLAP")',1),
('phaseStats("ZOOM_IN")','phaseStats("ARC_TRAIL")',1),
('zoomOutFrames:','arcLeadFrames:',1),
('zoomOutP95Ms:','arcLeadP95Ms:',1),
('zoomOutOver25:','arcLeadOver25:',1),
('motionFrames:','motionOverlapFrames:',1),
('motionP95Ms:','motionOverlapP95Ms:',1),
('motionOver25:','motionOverlapOver25:',1),
('zoomInFrames:','arcTrailFrames:',1),
('zoomInP95Ms:','arcTrailP95Ms:',1),
('zoomInOver25:','arcTrailOver25:',1),
]
for a,b,e in pairs:
 n=s.count(a);print(f"{a!r}: {n}")
 if n!=e: raise SystemExit(f"BAD COUNT {a!r}: {n}")
 s=s.replace(a,b)
a='''    profileId:state.condition.profileId,

    totalTravelSec:state.condition.totalTravelSec,'''
b='''    profileId:state.condition.profileId,

    choreographyMode:"CONTINUOUS_FOV_ARC",
    fovApexPct:50,
    motionStartPct:state.condition.zoomOutPct,
    motionEndPct:
      Number.isFinite(Number(state.condition.zoomOutPct)) &&
      Number.isFinite(Number(state.condition.motionPct))
        ? Number(state.condition.zoomOutPct)+Number(state.condition.motionPct)
        : null,
    motionWindowPct:state.condition.motionPct,

    totalTravelSec:state.condition.totalTravelSec,'''
n=s.count(a);print("RECORD METADATA ANCHOR:",n)
if n!=1: raise SystemExit("BAD RECORD METADATA ANCHOR")
s=s.replace(a,b,1)
a='''    profileId:
      run.profileId,

    totalTravelSec:
      run.totalTravelSec,'''
b='''    profileId:
      run.profileId,

    choreographyMode:
      "CONTINUOUS_FOV_ARC",

    fovApexPct:
      50,

    motionStartPct:
      run.zoomOutPct,

    motionEndPct:
      Number(run.zoomOutPct)+Number(run.motionPct),

    motionWindowPct:
      run.motionPct,

    totalTravelSec:
      run.totalTravelSec,'''
n=s.count(a);print("SUMMARY METADATA ANCHOR:",n)
if n!=1: raise SystemExit("BAD SUMMARY METADATA ANCHOR")
s=s.replace(a,b,1)
a='''  if(!r)
    return {phase:"IDLE",runElapsedMs:null};

  const s=(now-r.startedPerfMs)/1000;'''
b='''  if(!r)
    return {phase:"IDLE",runElapsedMs:null};

  if(!r.measurementStarted)
    return {phase:"PREPARED",runElapsedMs:null};

  if(
    r.measurementEndedPerfMs!==null &&
    r.measurementEndedPerfMs!==undefined &&
    now>Number(r.measurementEndedPerfMs)
  )
    return {
      phase:"POST_ANIMATION",
      runElapsedMs:round(
        Number(r.measurementEndedPerfMs)-
        Number(r.startedPerfMs)
      )
    };

  const s=(now-r.startedPerfMs)/1000;'''
n=s.count(a);print("PHASE GUARD ANCHOR:",n)
if n!=1: raise SystemExit("BAD PHASE GUARD ANCHOR")
s=s.replace(a,b,1)
p.write_text(s)
print("LAB0004 SEMANTICS PATCH WRITE: PASS")
