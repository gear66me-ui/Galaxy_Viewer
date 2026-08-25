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

The user directed that Galaxy Viewer engineering history be kept by the book and made quickly traceable. Governing requests include: “We need to keep track of everything in one place,” keep production source clean, and place engineering history in ECO records rather than runtime comments.

The authorized recordkeeping method is:

1. One master ECO index at `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`.
2. Newest ECO first.
3. One detailed logbook per ECO.
4. Starting with 12N, one numbered folder per ECO under `docs/engineering-change-orders/`.
5. Master entries link directly to detailed ECO records.
6. Detailed ECOs record concise request summaries, affected files/regions, before/after identities, implementation, rework, verification, and disposition.
7. Production source carries only a concise ECO pointer plus functional comments needed for current behavior.

## 2. 12N objective

Repair and reorganize Galaxy Viewer 12N as one disciplined standalone implementation. Preserve legitimate accumulated behavior while removing structural disorder, obsolete lineage commentary, wrapper-era residue, stale dependency assumptions, and duplicated ownership where proven.

The release target is a real standalone `viewer/GV-beta-0012N.py`; it must not obtain its implementation by fetching, extracting, patching, or executing a predecessor Galaxy Viewer source file at runtime.

## 3. Lineage / roll-up context

12N is the standalone consolidation target for legitimate work accumulated through the 12-series repair lineage. Root 12G through 12L were repair-loader / patching revisions around the standalone 12F implementation. Legitimate functional deltas are to be preserved where they belong in the final standalone architecture; the runtime wrapper/source-extraction mechanism itself is not part of final 12N.

## 4. Recordkeeping / source-comment rule

For `viewer/GV-beta-0012N.py` and later changed source files:

- keep one concise ECO pointer near the top;
- use functional comments only when they explain current algorithm/runtime behavior;
- do not narrate predecessor releases or patch history in runtime source;
- record engineering chronology and rationale here instead.

## 5. Known process/rework history recorded for traceability

- Wrapper-style 12G–12M lineage complicated the final standalone architecture and required reconstruction rather than continued wrapper layering.
- Component relocation on GitHub was valid, but several viewer references and dependency chains were not cleanly consolidated afterward.
- The Termux workspace accumulated multiple ECO/worktree directories and became unsuitable as authority for repository structure; GitHub `beta` is canonical for repository paths/content and Termux is the working/staging environment.
- 12N was initially treated as closer to release-ready than justified; later audit exposed unresolved ownership/startup issues.
- A temporary flat 12N ECO record was created and then superseded by the master-index + numbered-folder convention.

## 6. Current working source identity

- Path: `viewer/GV-beta-0012N.py`
- Current working SHA-256 after REQ-096: `cd895018ac06455a9278159e0d2214fad84a1148ccbbcdac9454c4279ff73b26`
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
REQ-093 identified obsolete embedded-JavaScript lineage comments around JS lines 1454, 1710, 1771, and 1831.

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

### Pre-change locations
- `loadScript(...)`: around JS line 1206.
- Aladin preload state/startup: around JS lines 1238–1280.
- external component load group: around JS lines 1368–1372.

### Implementation
Moved existing startup machinery without intentionally changing behavior into this order: script loader, Aladin preload/startup, Hamburger, Coordinate, Target, Random Galaxy, then runtime mutable state and remaining implementation.

### After
- `loadScript(...)`: around embedded JS line 49.
- Aladin preload start: around embedded JS line 118.
- external component load block: around embedded JS line 136.
- runtime mutable state: around embedded JS line 143.
- SHA-256: `ca14c6a289e2587ad674fa28e14e4e327299d376b9a88b39258a8845a9b2cc37`
- Python syntax: **PASS**
- Embedded JavaScript syntax: **PASS**

## 9. REQ-096 — master ECO pointer

### User requirement
Every changed production source file must point directly to the master ECO record so the engineering history can be opened immediately without embedding a long history in source.

### Before
- SHA-256: `ca14c6a289e2587ad674fa28e14e4e327299d376b9a88b39258a8845a9b2cc37`
- Header contained the temporary local ECO identifier only.

### Changed source region
- `viewer/GV-beta-0012N.py` top header comment only.

### Implementation
Replaced the temporary ECO comment with a direct GitHub link to the `GV-ECO-0012N` section of `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`.

### After
- SHA-256: `cd895018ac06455a9278159e0d2214fad84a1148ccbbcdac9454c4279ff73b26`
- Python syntax: **PASS**
- Embedded JavaScript syntax: **PASS**
- Master ECO pointer: **PASS**
- Other source files modified: **NO**
- Source commit: **NO**
- Push: **NO**

## 10. Open 12N findings / planned work

1. Runtime state and function blocks still need functional grouping and ordering.
2. Random-navigation/prefetch ownership requires consolidation review.
3. Isolated Aladin prewarm currently uses `srcdoc`; final necessity/architecture remains under review.
4. Generic raw-GitHub script loading currently includes fetch-to-inline-script behavior and is scheduled for removal.
5. The GitHub-hosted Aladin mirror has not yet passed Android runtime initialization.
6. External components require standalone dependency cleanup.
7. Source URLs/paths require final verification.
8. Final 12N requires syntax, runtime, Random Galaxy, history, HD/prefetch, Aladin, and archive validation.

## 11. Release gate

12N remains not release-ready until all applicable structural, ownership, dependency, syntax, runtime, navigation, prefetch, Aladin, archive, and final GitHub reconciliation checks pass.

## 12. Current disposition

- `12N_RELEASE_READY=NO`
- `APP_RUNTIME_VALIDATED=NO`
- `SOURCE_COMMIT_PENDING=YES`
- `MASTER_INDEX_REQUIRED=YES`
- `DETAILED_ECO_ORGANIZED=YES`
