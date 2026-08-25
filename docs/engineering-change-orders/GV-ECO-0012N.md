# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0012N

## Status

- Repository: `gear66me-ui/Galaxy_Viewer`
- Branch: `beta`
- Release target: `GV-beta-0012N.py`
- Engineering/source cleanup: **IN PROGRESS**
- Runtime/browser acceptance: **PENDING**
- User visual acceptance: **PENDING**

## 1. Authorized scope

Repair and reorganize Galaxy Viewer 12N as one disciplined standalone implementation. Preserve functional behavior while removing structural disorder, obsolete lineage commentary, duplicated startup placement, wrapper-era residue, and stale dependency assumptions. Production source must contain only a concise ECO reference at the top; change history, rationale, line/range accounting, before/after identities, validation evidence, and release decisions belong in this ECO record.

## 2. Source documentation rule

`viewer/GV-beta-0012N.py` must not become an engineering diary. It may contain functional comments only when they explain current runtime behavior or algorithmic intent. It must not contain legacy ownership/version-history comments such as `0034 owns...`, `0036 owns...`, predecessor-release narration, or patch-history commentary.

The authoritative engineering record for this cleanup is this file:

`docs/engineering-change-orders/GV-ECO-0012N.md`

## 3. Current working source identity

- Path: `viewer/GV-beta-0012N.py`
- Current SHA-256 after REQ-095: `ca14c6a289e2587ad674fa28e14e4e327299d376b9a88b39258a8845a9b2cc37`
- Current line count after REQ-095: `1960`
- Current byte count after REQ-095: `101689`
- Python syntax: **PASS**
- Embedded JavaScript syntax: **PASS**
- Source commit to GitHub: **PENDING UNTIL CLEANUP/VALIDATION GATE**

## 4. REQ-094 — header/comment discipline cleanup

### Before

- SHA-256: `2aaba4e481558644d8566a59ae2a00ed17900ba29f2cf3920c7b7734b698a7ec`
- Lines: `1967`
- Bytes: `102215`

### Authorized change

Established one ECO header and removed obsolete release-lineage commentary while preserving executable behavior.

Pre-change embedded-JavaScript locations identified by REQ-093 and removed as obsolete commentary:

- JS line 1454: `0034` startup-history comment.
- JS line 1710: `0034` history-transaction ownership comment.
- JS line 1771: `0034` Aladin-arrival ownership comment.
- JS line 1831: `0036` FIFO-bundle ownership comment.

No active `0042` runtime URL, load, or version-gate code was removed.

### After

- SHA-256: `81b1d8207577c7d903663fe25a9d21a07bf2c66e4b35ccd6405ac20783934a39`
- Lines: `1959`
- Bytes: `101688`
- Python AST: **PASS**
- Embedded JavaScript syntax: **PASS**
- Legacy lineage comments remaining: `0`

## 5. REQ-095 — startup/load-order structural reorganization

### Before

- SHA-256: `81b1d8207577c7d903663fe25a9d21a07bf2c66e4b35ccd6405ac20783934a39`

### Pre-change locations from REQ-093

- `loadScript(...)`: embedded JS line 1206.
- Aladin preload state/startup: embedded JS lines 1238–1280.
- External component load group: embedded JS lines 1368–1372.
- Catalog startup promise: embedded JS line 1367.
- Main Aladin gate: embedded JS lines 1379–1382.

### Authorized change

Moved existing startup machinery without intentionally changing its behavior so the file begins in execution order:

1. Native script loader.
2. Aladin preload/startup.
3. Hamburger load.
4. Coordinate load.
5. Target load.
6. Random Galaxy load.
7. Runtime mutable state and remaining implementation.

No duplicate startup copies were retained.

### Post-change execution locations

- `loadScript(...)`: embedded JS line 49.
- Aladin preload start: embedded JS line 118.
- External component load block: embedded JS line 136.
- Runtime mutable state begins: embedded JS line 143.
- Catalog startup promise: embedded JS line 1374.
- Main Aladin gate: embedded JS line 1380.

### After

- SHA-256: `ca14c6a289e2587ad674fa28e14e4e327299d376b9a88b39258a8845a9b2cc37`
- Lines: `1960`
- Bytes: `101689`
- One script-loader implementation: **PASS**
- One Aladin preload implementation: **PASS**
- One external component-load block: **PASS**
- Startup order contract: **PASS**
- Python syntax: **PASS**
- Embedded JavaScript syntax: **PASS**

## 6. Known unresolved 12N cleanup findings

The following remain open and must be resolved before 12N can be called release-ready:

1. Runtime state/function blocks remain structurally out of order and need functional grouping.
2. Random-navigation/prefetch ownership between 12N integration code and the active Random Galaxy implementation requires explicit consolidation review.
3. Isolated Aladin prewarm uses `srcdoc`; necessity and final architecture remain under review.
4. The generic raw-GitHub script-loading path fetches source and assigns `script.textContent`; necessity and final architecture remain under review.
5. Aladin GitHub-mirror runtime initialization has not yet passed Android runtime validation.
6. External component files must subsequently be audited and converted to standalone revisions with no hidden predecessor dependency.
7. Final 12N source must be committed to GitHub only after structural cleanup and validation gates pass.

## 7. Release gate

12N is not release-ready until all of the following pass:

- Structural order audit.
- Single-ownership audit for runtime responsibilities.
- No wrapper/predecessor-viewer fetch architecture.
- No stale lineage commentary.
- Correct GitHub module paths.
- Module standalone-dependency audit.
- Python syntax validation.
- Embedded JavaScript syntax validation.
- Android/browser runtime validation.
- Random Galaxy functional validation.
- Back/forward/history validation.
- HD/prefetch/Aladin/archive bundle validation.
- Final GitHub fetch-back and SHA accounting.

## 8. Current release status

- `12N_RELEASE_READY=NO`
- `APP_RUNTIME_VALIDATED=NO`
- `SOURCE_COMMIT_PENDING=YES`
- `ECO_RECORD_ON_GITHUB=YES`
