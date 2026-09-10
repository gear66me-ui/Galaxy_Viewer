from pathlib import Path
import sys

W = Path.home() / "GV_AR05_PUSH" / "viewer"

AR0 = W / "GV-beta-0012AR-14-DOE.py"
AR  = W / "GV-beta-0012AR-15-DOE.py"

LAB0 = W / "modules/diagnostics/gv-stutter-lab-0002.js"
LAB  = W / "modules/diagnostics/gv-stutter-lab-0003.js"

for p in (AR0, LAB0):
    if not p.is_file():
        raise SystemExit(f"SOURCE MISSING: {p}")

for p in (AR, LAB):
    if p.exists():
        raise SystemExit(f"COLLISION: {p}")

ar = AR0.read_text()
lab = LAB0.read_text()

print("SOURCE GATE: PASS")
print("AR14 :", AR0)
print("LAB02:", LAB0)

# ------------------------------------------------------------
# AR15 — version + telemetry lab loader
# ------------------------------------------------------------

if "12AR-14-DOE" not in ar:
    raise SystemExit("AR14 VERSION ANCHOR MISSING")

if "gv-stutter-lab-0002.js" not in ar:
    raise SystemExit("LAB0002 LOADER ANCHOR MISSING")

if "gvStutterLab0002" not in ar:
    raise SystemExit("LAB0002 LOADER ID ANCHOR MISSING")

ar = ar.replace(
    "12AR-14-DOE",
    "12AR-15-DOE"
)

ar = ar.replace(
    "gv-stutter-lab-0002.js",
    "gv-stutter-lab-0003.js"
)

ar = ar.replace(
    "gvStutterLab0002",
    "gvStutterLab0003"
)

ar = ar.replace(
    "RANDOM GALAXY 0092 HOME BOOTSTRAP EXPORT MISSING",
    "RANDOM GALAXY 0094 HOME BOOTSTRAP EXPORT MISSING"
)

print("AR15 VERSION/LOADER PATCH STAGED: PASS")

# ------------------------------------------------------------
# LAB0003 — authoritative GalaxyViewerCore telemetry reader
# ------------------------------------------------------------

if 'const VERSION="0002";' not in lab:
    raise SystemExit("LAB0002 VERSION ANCHOR MISSING")

lab = lab.replace(
    'const VERSION="0002";',
    'const VERSION="0003";',
    1
)

anchor = "function prewarmSnapshot(controller,destination){"

if lab.count(anchor) != 1:
    raise SystemExit(
        f"PREWARM SNAPSHOT ANCHOR COUNT={lab.count(anchor)}"
    )

helper = r"""
function jsonCopy(value){
  try{
    if(value===undefined)return null;
    return JSON.parse(JSON.stringify(value));
  }catch(_){
    return null;
  }
}

function coreTelemetrySnapshot(destination){
  const core=global.GalaxyViewerCore;
  const now=Date.now();

  const out={
    capturedAtEpochMs:now,
    coreAvailable:Boolean(core),

    destinationKey:null,

    aladinPrepared:null,
    hdPrepared:null,
    backgroundWorkSuspended:null,

    receipt:null,
    receiptAgeMs:null,

    aladinPrewarmState:null,
    prefetchState:null,
    navigationState:null,
    downloadStatus:null
  };

  if(!core)return out;

  let key="";

  try{
    key=String(
      core.randomGalaxy
        ?.preparationEngine
        ?.destinationKey
        ?.(destination)
        || ""
    ).trim().toLowerCase();
  }catch(_){}

  out.destinationKey=key||null;

  try{
    out.aladinPrewarmState=
      jsonCopy(
        core.getAladinPrewarmState?.()
      );
  }catch(_){}

  try{
    out.prefetchState=
      jsonCopy(
        core.getPrefetchState?.()
      );
  }catch(_){}

  try{
    out.navigationState=
      jsonCopy(
        core.getRandomNavigationState?.()
      );
  }catch(_){}

  try{
    out.backgroundWorkSuspended=
      Boolean(
        core.getBackgroundWorkSuspended?.()
      );
  }catch(_){}

  if(!key)return out;

  try{
    out.aladinPrepared=
      Boolean(
        core.isAladinPrepared?.(key)
      );
  }catch(_){}

  try{
    out.hdPrepared=
      Boolean(
        core.isHdPrepared?.(key)
      );
  }catch(_){}

  try{
    const receipt=
      core.getAladinPreparedReceipt?.(key)
      || null;

    out.receipt=
      jsonCopy(receipt);

    if(
      receipt &&
      Number.isFinite(
        Number(receipt.preparedAt)
      )
    ){
      out.receiptAgeMs=
        now-Number(receipt.preparedAt);
    }
  }catch(_){}

  try{
    const statuses=
      core.getDownloadStatus?.()
      || [];

    const match=
      statuses.find(
        item=>
          String(
            item?.key||""
          ).trim().toLowerCase()===key
      ) || null;

    out.downloadStatus=
      jsonCopy(match);
  }catch(_){}

  return out;
}

"""

lab = lab.replace(
    anchor,
    helper + anchor,
    1
)

controller_anchor = """  try{
    out.controller=safeSnapshot(controller);
"""

if lab.count(controller_anchor) != 1:
    raise SystemExit(
        "CONTROLLER SNAPSHOT ANCHOR FAILURE"
    )

lab = lab.replace(
    controller_anchor,
    """  out.core=
    coreTelemetrySnapshot(destination);

  try{
    out.controller=safeSnapshot(controller);
""",
    1
)

print("LAB0003 CORE TELEMETRY READER STAGED: PASS")

# ------------------------------------------------------------
# LAB0003 — flatten authoritative telemetry into run summaries
# ------------------------------------------------------------

summary_anchor = "  const summary={"

if lab.count(summary_anchor) != 1:
    raise SystemExit(
        f"SUMMARY ANCHOR COUNT={lab.count(summary_anchor)}"
    )

lab = lab.replace(
    summary_anchor,
    """  const prewarmEnd=
    prewarmSnapshot(
      run.controller,
      info.destination
    );

  const coreStart=
    run.prewarmStart?.core||{};

  const coreEnd=
    prewarmEnd?.core||{};

  const summary={""",
    1
)

old_end = """    prewarmEnd:
      prewarmSnapshot(
        run.controller,
        info.destination
      )
"""

if lab.count(old_end) != 1:
    raise SystemExit(
        "PREWARM END ANCHOR FAILURE"
    )

lab = lab.replace(
    old_end,
    """    prewarmEnd
""",
    1
)

start_anchor = """    prewarmStart:
      run.prewarmStart,
"""

if lab.count(start_anchor) != 1:
    raise SystemExit(
        "PREWARM START SUMMARY ANCHOR FAILURE"
    )

flat_fields = """    destinationKey:
      coreStart.destinationKey
      || coreEnd.destinationKey
      || null,

    aladinPreparedAtStart:
      coreStart.aladinPrepared ?? null,

    hdPreparedAtStart:
      coreStart.hdPrepared ?? null,

    prewarmReceiptAgeMsAtStart:
      finite(coreStart.receiptAgeMs),

    prewarmReceiptPreparedAtEpochMs:
      finite(
        coreStart.receipt?.preparedAt
      ),

    prewarmReceiptRaDeg:
      finite(
        coreStart.receipt?.ra
      ),

    prewarmReceiptDecDeg:
      finite(
        coreStart.receipt?.dec
      ),

    prewarmReceiptFovDeg:
      finite(
        coreStart.receipt?.fov
      ),

    prewarmReceiptRotationDeg:
      finite(
        coreStart.receipt?.rotation
      ),

    prewarmReceiptProjection:
      coreStart.receipt?.projection
      || null,

    prewarmCachedCountAtStart:
      finite(
        coreStart
          .aladinPrewarmState
          ?.cachedCount
      ),

    prewarmActiveKeyAtStart:
      coreStart
        .aladinPrewarmState
        ?.activeKey
      || null,

    prefetchReadyCountAtStart:
      finite(
        coreStart
          .prefetchState
          ?.readyCount
      ),

    prefetchLoadingCountAtStart:
      finite(
        coreStart
          .prefetchState
          ?.loadingCount
      ),

    prefetchQueuedCountAtStart:
      finite(
        coreStart
          .prefetchState
          ?.queuedCount
      ),

    prefetchPipelineCountAtStart:
      finite(
        coreStart
          .prefetchState
          ?.pipelineCount
      ),

    prefetchFailedCountAtStart:
      finite(
        coreStart
          .prefetchState
          ?.failedCount
      ),

    activePreparedGalaxyAtStart:
      coreStart
        .prefetchState
        ?.activePreparedGalaxy
      || null,

    activePreparedSourceAtStart:
      coreStart
        .prefetchState
        ?.activePreparedSource
      || null,

    hdDownloadStateAtStart:
      coreStart
        .downloadStatus
        ?.state
      || null,

    backgroundSuspendedAtStart:
      coreStart.backgroundWorkSuspended
      ?? null,

    aladinPreparedAtEnd:
      coreEnd.aladinPrepared ?? null,

    hdPreparedAtEnd:
      coreEnd.hdPrepared ?? null,

    prewarmReceiptAgeMsAtEnd:
      finite(coreEnd.receiptAgeMs),

    prewarmCachedCountAtEnd:
      finite(
        coreEnd
          .aladinPrewarmState
          ?.cachedCount
      ),

    prefetchReadyCountAtEnd:
      finite(
        coreEnd
          .prefetchState
          ?.readyCount
      ),

    prefetchLoadingCountAtEnd:
      finite(
        coreEnd
          .prefetchState
          ?.loadingCount
      ),

    prefetchQueuedCountAtEnd:
      finite(
        coreEnd
          .prefetchState
          ?.queuedCount
      ),

    backgroundSuspendedAtEnd:
      coreEnd.backgroundWorkSuspended
      ?? null,

"""

lab = lab.replace(
    start_anchor,
    flat_fields + start_anchor,
    1
)

print("LAB0003 FLAT PREWARM TELEMETRY STAGED: PASS")

# ------------------------------------------------------------
# FINAL WRITE
# ------------------------------------------------------------

AR.write_text(ar)
LAB.write_text(lab)

print("AR15 WRITTEN:", AR)
print("LAB0003 WRITTEN:", LAB)
print("PATCH EXECUTION COMPLETE")
