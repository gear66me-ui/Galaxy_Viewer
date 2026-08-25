# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0012N

## Status

- Repository: `gear66me-ui/Galaxy_Viewer`
- Branch: `beta`
- Release target: `viewer/GV-beta-0012N.py`
- Engineering/source cleanup: **IN PROGRESS**
- Runtime/browser acceptance: **PENDING**
- User visual acceptance: **PENDING**
- Detailed ECO path: `docs/engineering-change-orders/0012N/GV-ECO-0012N.md`
- Master index: `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`

## 1. Conversation / authorization summary

The user directed that Galaxy Viewer engineering history be kept by the book and made quickly traceable. The governing request is summarized as:

> “We need to keep track of everything in one place.”

The user also required that production Python/JavaScript files stop carrying long release-history commentary. Source files should contain only a concise ECO pointer plus comments needed to explain current runtime behavior. Detailed history, rationale, mistakes, rework, line ranges, hashes, validation, and final disposition belong in the ECO records.

The user authorized the following change-control organization during the 12N cleanup:

1. Maintain one master ECO index at `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`.
2. Keep the newest ECO at the top of the master index.
3. Maintain one detailed logbook per ECO.
4. Starting with 12N, place each detailed ECO in its own numbered folder under `docs/engineering-change-orders/`.
5. The master index links directly to every detailed ECO so the full history is one click away.
6. Each detailed ECO records the concise user request, affected source file(s), source regions/line ranges, before/after identities, implementation summary, mistakes/rework, verification evidence, and release state.
7. Do not paste giant code blocks into the ECO unless a small source excerpt is required for forensic proof.
8. Do not use production source as an engineering diary.

This hybrid master-index + per-ECO-logbook method is the authoritative recordkeeping method beginning with GV-ECO-0012N. Earlier ECO files remain valid historical evidence and may be indexed or migrated separately without rewriting their contents.

## 2. 12N objective

Repair and reorganize Galaxy Viewer 12N as one disciplined standalone implementation. Preserve legitimate accumulated behavior while removing structural disorder, obsolete lineage commentary, wrapper-era residue, stale dependency assumptions, and duplicated ownership where proven.

The release target is a real standalone `viewer/GV-beta-0012N.py`; it must not obtain its implementation by fetching, extracting, patching, or executing a predecessor Galaxy Viewer source file at runtime.

## 3. Lineage / roll-up context

12N is the standalone consolidation target for legitimate work accumulated through the 12-series repair lineage.

GitHub review established that root 12G through 12L were repair-loader / patching revisions built around the standalone 12F implementation. Those revisions introduced or attempted to preserve items including organized component paths, later Random Galaxy revisions, diagnostics/download analytics integration, Random preparation handling, and startup instrumentation. Those functional deltas are being preserved only where they belong in the final standalone architecture; the runtime wrapper/source-extraction mechanism itself is not part of the final 12N design.

The Termux working 12N was created as a standalone working source and is now undergoing structural cleanup and verification before any source release commit.

## 4. Recordkeeping / source-comment rule

Production source must stay concise.

For `viewer/GV-beta-0012N.py` and later changed source files:

- keep one concise ECO pointer near the top;
- use functional comments only when they explain the current algorithm/runtime behavior;
- do not include historical ownership notes such as “0034 owns...” or “0036 owns...”;
- do not narrate predecessor releases or patch history in runtime source;
- record engineering chronology and rationale here instead.

The intended source pointer for 12N is the master index entry for `GV-ECO-0012N`, which in turn links to this detailed record.

## 5. Known process/rework history recorded for traceability

This ECO records the following rework so it is not lost:

- Wrapper-style 12G–12M lineage complicated the final standalone architecture and required reconstruction rather than continued wrapper layering.
- Module/component relocation on GitHub was valid, but several viewer references and dependency chains were not cleanly consolidated afterward.
- The Termux workspace accumulated multiple ECO/worktree directories and became unsuitable as the authority for repository structure; GitHub `beta` is the authority for canonical repository paths and contents, while Termux is only the active working/staging environment.
- 12N was initially treated as closer to release-ready than justified by source/runtime evidence; subsequent forensic audit showed unresolved ownership and startup issues.
- A separate flat `GV-ECO-0012N.md` was initially created during this cleanup. The recordkeeping system is now being normalized to a master index plus a numbered 12N folder so there is one clear navigation path.

These notes are engineering traceability, not a claim that every listed problem has already been repaired.

## 6. Current working source identity

- Path: `viewer/GV-beta-0012N.py`
- Current working SHA-256 after REQ-095: `ca14c6a289e2587ad674fa28e14e4e327299d376b9a88b39258a8845a9b2cc37`
- Current working line count after REQ-095: `1960`
- Current working byte count after REQ-095: `101689`
- Python syntax: **PASS**
- Embedded JavaScript syntax: **PASS**
- Source committed to GitHub: **NO — cleanup/validation gate still open**

## 7. REQ-094 — header/comment discipline cleanup

### User requirement

Keep production source clean and move historical change narration into the ECO record.

### Before

- SHA-256: `2aaba4e481558644d8566a59ae2a00ed17900ba29f2cf3920c7b7734b698a7ec`
- Lines: `1967`
- Bytes: `102215`

### Changed source regions

REQ-093 identified obsolete embedded-JavaScript lineage comments at approximately:

- JS line 1454 — obsolete `0034` startup-history comment.
- JS line 1710 — obsolete `0034` history-transaction ownership comment.
- JS line 1771 — obsolete `0034` Aladin-arrival ownership comment.
- JS line 1831 — obsolete `0036` FIFO-bundle ownership comment.

### Implementation

- Established one ECO header/reference area.
- Removed four obsolete lineage comments.
- Preserved active runtime code and active `0042` references.

### After

- SHA-256: `81b1d8207577c7d903663fe25a9d21a07bf2c66e4b35ccd6405ac20783934a39`
- Lines: `1959`
- Bytes: `101688`
- Python AST: **PASS**
- Embedded JavaScript syntax: **PASS**
- Legacy lineage comments remaining: `0`

## 8. REQ-095 — startup/load-order structural reorganization

### User requirement

Make 12N read in disciplined execution order, beginning with loading/startup and then the externally loaded viewer components, instead of leaving startup machinery scattered later in the file.

### Before

- SHA-256: `81b1d8207577c7d903663fe25a9d21a07bf2c66e4b35ccd6405ac20783934a39`

REQ-093 pre-change embedded-JavaScript locations:

- `loadScript(...)`: around JS line 1206.
- Aladin preload state/startup: around JS lines 1238–1280.
- external component load group: around JS lines 1368–1372.
- catalog startup promise: around JS line 1367.
- main Aladin gate: around JS lines 1379–1382.

### Implementation

Moved the existing startup machinery without intentionally changing behavior so the beginning of the runtime follows this order:

1. script loader;
2. Aladin preload/startup;
3. Hamburger load;
4. Coordinate load;
5. Target load;
6. Random Galaxy load;
7. runtime mutable state and remaining implementation.

No duplicate copy of the moved startup blocks was retained.

### After / current locations

- `loadScript(...)`: around embedded JS line 49.
- Aladin preload start: around embedded JS line 118.
- external component load block: around embedded JS line 136.
- runtime mutable state: around embedded JS line 143.
- catalog startup promise: around embedded JS line 1374.
- main Aladin gate: around embedded JS line 1380.

### After identity

- SHA-256: `ca14c6a289e2587ad674fa28e14e4e327299d376b9a88b39258a8845a9b2cc37`
- Lines: `1960`
- Bytes: `101689`
- one script-loader implementation: **PASS**
- one Aladin preload implementation: **PASS**
- one external component-load block: **PASS**
- startup order contract: **PASS**
- Python syntax: **PASS**
- embedded JavaScript syntax: **PASS**

## 9. Open 12N findings / planned work

The following remain open and must not be promoted to PASS until actually resolved and tested:

1. Runtime state and function blocks still need functional grouping and ordering.
2. Random-navigation/prefetch ownership between 12N integration code and the active Random Galaxy implementation needs consolidation review.
3. Isolated Aladin prewarm currently uses `srcdoc`; final necessity/architecture remains under review.
4. Generic raw-GitHub script loading currently includes fetch-to-inline-script behavior; final necessity/architecture remains under review.
5. The GitHub-hosted Aladin mirror has not yet passed Android runtime initialization.
6. External components must be audited and converted to standalone revisions with no hidden predecessor dependency.
7. Source URLs/paths must be verified against authoritative GitHub locations.
8. Final 12N source requires syntax, runtime, Random Galaxy, history, HD/prefetch, Aladin and archive validation before release.

## 10. Release gate

12N is not release-ready until all applicable checks pass:

- structural order audit;
- single-ownership audit;
- no predecessor-viewer runtime dependency;
- no stale lineage commentary;
- correct GitHub paths;
- standalone external-component dependency audit;
- Python syntax validation;
- embedded JavaScript syntax validation;
- browser/Android runtime validation;
- Random Galaxy behavior validation;
- Back/Forward/history validation;
- HD/prefetch/Aladin/archive bundle validation;
- final GitHub fetch-back, diff accounting, and requirement closure.

## 11. Current disposition

- `12N_RELEASE_READY=NO`
- `APP_RUNTIME_VALIDATED=NO`
- `SOURCE_COMMIT_PENDING=YES`
- `MASTER_INDEX_REQUIRED=YES`
- `DETAILED_ECO_ORGANIZED=YES`
