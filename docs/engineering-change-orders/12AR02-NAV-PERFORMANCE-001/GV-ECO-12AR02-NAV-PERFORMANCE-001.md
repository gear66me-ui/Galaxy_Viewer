# ECO-20260902-12AR02-NAV-PERFORMANCE-001

Repository: `gear66me-ui/Galaxy_Viewer`  
Branch: `beta`

## Authorization
User GO received in chat on 2026-09-02.

## Scope
Create-only engineering test derivative. No production pointer promotion. No modification of `GV-beta-0012AR.py`, `GV-beta-0012AR-01.py`, Random 0086/0086-01, diagnostics, catalogs, artwork, or production launcher.

## Baseline
`viewer/GV-beta-0012AR-01.py` Git blob: `2844f67ece7701692f64e30c7c36ed6c8d55c6a2`.

## Requirements
REQ-001 — Replace the single total-travel benchmark selector with independent Zoom Out, Translation, and Zoom In time controls.

REQ-002 — Default phase timing shall preserve a 17.0 s initial benchmark total: 5.1 s Zoom Out, 6.8 s Translation, 5.1 s Zoom In.

REQ-003 — During benchmark runs, translation and rotation normalized boundaries shall be derived from the three selected phase durations.

REQ-004 — During benchmark runs, FOV shall be commanded as sequential phases: logarithmic S7 Zoom Out to 237.6°, hold at 237.6° during Translation, logarithmic S7 Zoom In to destination FOV.

REQ-005 — Capture one performance record per `requestAnimationFrame` including timestamp, elapsed time, frame delta, phase, commanded state, and observed Aladin RA/Dec/FOV/rotation.

REQ-006 — Post-process after the run, not during animation, to calculate instantaneous FPS, FOV velocity, sky angular velocity, and rotation velocity.

REQ-007 — Report overall and phase-specific frame statistics including mean, median, P95, P99, maximum, and counts over 25/50/100/250 ms.

REQ-008 — Capture phase/event markers for navigation start, Zoom Out start, Translation start, Zoom In start, arrival, and errors.

REQ-009 — Capture preparation/readiness snapshots before claim, at phase boundaries, and after travel, including future[0]/pending identity, HD prepared state, Aladin prepared state, background-work suspension state, and available prefetch state. This is intended to forensic-test the observed green→red HD transition on Random Galaxy claim.

REQ-010 — Include source/destination route-edge travel and rotation values when available from the current/future records.

REQ-011 — Automatically download plot-ready JSON after each completed benchmark run.

REQ-012 — JSON filename shall encode Zoom Out, Translation, and Zoom In settings.

REQ-013 — Diagnostic acquisition shall avoid graph rendering, DOM tables, or JSON serialization during flight; expensive post-processing occurs only after arrival.

REQ-014 — Existing 12AR-01 remains byte-for-byte untouched.

REQ-015 — Production pointer remains unchanged unless separately authorized.

## Created source
`viewer/GV-beta-0012AR-02.py`

The derivative fetches the exact 12AR-01 baseline at runtime, verifies its Git blob before execution, changes only the visible/test version identity and the loaded-navigation benchmark block, then executes the verified derivative.

## Current status
Created and fetched back from `beta`. Production pointer not changed.
