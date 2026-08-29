# Galaxy Viewer Root-Cause Record
## RC-20260829-RANDOM-ROTATION-SCOPE

Date: 2026-08-29

Live diagnostic build:
- Viewer 12AM
- Random 0067
- Diagnostics 0006
- Publish commit: 93dcc0a0ec114bdaf0facec7bcd4e620fb787f63

## Symptom

RANDOM GALAXY accepted the click but visible travel never started.
The Viewer remained at Earth and returned immediately to READY.

## Flight-recorder result

Execution successfully reached:

1. PHYSICAL_RANDOM_CLICK
2. REQUEST_ENTER
3. REQUEST_TRAVEL_AWAIT_BEGIN
4. TRAVEL_ENTER
5. READY_AWAIT_BEGIN
6. READY_AWAIT_END
7. CONSUME_BEGIN
8. CONSUME_END
9. Aladin RA/Dec/FOV/rotation acquisition

The failure occurred before the first travel requestAnimationFrame.

## Proven exception

ReferenceError: normalizeFullRotationDelta is not defined

Runtime stack:

GalaxyRandomGalaxy.travelToRandom
gv-random-galaxy-0067.js:4726:29

async requestRandomNavigation
gv-random-galaxy-0067.js:6085:19

The failing operation is the rotation-delta calculation immediately before
the Random travel animation begins.

## Root cause

travelToRandom() calls normalizeFullRotationDelta(), but the function is not
visible in the lexical scope of GalaxyRandomGalaxy.travelToRandom().

The existing intended helper implementation is:

function normalizeFullRotationDelta(value){
    let angle=Number(value)||0;
    while(angle>180)angle-=360;
    while(angle<=-180)angle+=360;
    return angle;
}

Therefore this is a JavaScript runtime symbol / lexical-scope defect.

It is NOT a failure of:

- the Random button
- future[0] selection
- FIFO readiness
- HD downloading
- archive preload
- Aladin prewarm
- this.ready initialization
- destination availability

The diagnostic showed the 10-slot queue and resources becoming ready while
every Random attempt failed with the same ReferenceError.

## Authorized repair

Create Random 0068 from the audited 0067 diagnostic baseline.

Functional change:

Restore the existing normalizeFullRotationDelta() helper at module scope so
travelToRandom() can resolve it.

Do not alter the helper algorithm.

Do not alter:

- Random click semantics
- FIFO ownership
- history
- HD preparation
- archive preload
- Aladin prewarm
- travel timing
- travel choreography
- destination selection

Retain the flight recorder for the first post-repair test.

## Acceptance criteria

1. No normalizeFullRotationDelta ReferenceError.
2. Random reaches RAF_FRAME_EXECUTED.
3. Visible travel starts.
4. Travel reaches ARRIVAL.
5. future[0] becomes current after arrival.
6. Queue/history bookkeeping completes.
7. Downloads remain non-blocking for navigation.

## Prevention

Syntax validation is insufficient for this class of defect because an
unresolved runtime symbol is syntactically valid JavaScript.

Future Random changes must verify:
- caller-visible lexical scope for referenced helpers
- caught Promise rejections in diagnostics
- console.error capture
- execution-path tracing before changing unrelated subsystems
