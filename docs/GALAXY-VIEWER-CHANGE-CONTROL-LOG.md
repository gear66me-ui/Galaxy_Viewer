# GALAXY VIEWER — MASTER ENGINEERING CHANGE CONTROL INDEX

This is the single master index for Galaxy Viewer Engineering Change Orders (ECOs).

## Recordkeeping rule

- Newest ECO first.
- One concise master entry per ECO.
- Each master entry links to one detailed ECO logbook.
- Starting with GV-ECO-0012N, each detailed ECO is stored in its own numbered folder under `docs/engineering-change-orders/`.
- Production source files should contain only a concise pointer to the applicable ECO/master record plus functional comments needed for current runtime behavior.
- Engineering chronology, user-request summary, affected paths/regions, hashes, mistakes/rework, verification, and release disposition belong in the detailed ECO.
- Legacy ECO files created before this folder convention remain historical evidence and are indexed in place unless a separate migration is authorized.

---

## GV-ECO-0012N — Galaxy Viewer 12N standalone consolidation / structural cleanup

- **Date:** 2026-08-25
- **Target:** `viewer/GV-beta-0012N.py`
- **Status:** IN PROGRESS
- **Current working SHA-256:** `ca14c6a289e2587ad674fa28e14e4e327299d376b9a88b39258a8845a9b2cc37`
- **Summary:** Consolidate accumulated 12-series work into one disciplined standalone 12N implementation; remove source-history pollution; reorder startup; continue ownership/dependency cleanup; validate before source release commit.
- **Traceability note:** 12N cleanup is also where the master-index + per-ECO-folder recordkeeping convention was instituted after prior ECO/worktree sprawl made the engineering history unnecessarily hard to follow.
- **Detailed ECO:** [Open GV-ECO-0012N](engineering-change-orders/0012N/GV-ECO-0012N.md)

---

# Legacy ECO index

The following existing ECOs predate the numbered-folder convention. Their contents are preserved in place.

## GV-ECO-0007AE
- **Detailed ECO:** [Open GV-ECO-0007AE](engineering-change-orders/GV-ECO-0007AE.md)

## GV-ECO-0007AD
- **Detailed ECO:** [Open GV-ECO-0007AD](engineering-change-orders/GV-ECO-0007AD.md)

## GV-ECO-0007AC
- **Detailed ECO:** [Open GV-ECO-0007AC](engineering-change-orders/GV-ECO-0007AC.md)

## GV-ECO-0007AB
- **Detailed ECO:** [Open GV-ECO-0007AB](engineering-change-orders/GV-ECO-0007AB.md)

## GV-ECO-0007AA
- **Detailed ECO:** [Open GV-ECO-0007AA](engineering-change-orders/GV-ECO-0007AA.md)

## GV-ECO-0007Z
- **Detailed ECO:** [Open GV-ECO-0007Z](engineering-change-orders/GV-ECO-0007Z.md)

## GV-ECO-0007Y
- **Detailed ECO:** [Open GV-ECO-0007Y](engineering-change-orders/GV-ECO-0007Y.md)

## GV-ECO-0007X
- **Detailed ECO:** [Open GV-ECO-0007X](engineering-change-orders/GV-ECO-0007X.md)

## GV-ECO-0007W
- **Detailed ECO:** [Open GV-ECO-0007W](engineering-change-orders/GV-ECO-0007W.md)

## GV-ECO-0007V
- **Detailed ECO:** [Open GV-ECO-0007V](engineering-change-orders/GV-ECO-0007V.md)

## AUTO-de733c9100c3 — ECO-20260825-REQ157-TEST-RELEASE-032

**Recorded:** 2026-08-25T20:55:14-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`de733c9100c3f729fbaaca92cd37c1c322c88832`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/de733c9100c3f729fbaaca92cd37c1c322c88832)  
**Parent/baseline:** `5b82228e2d4d8f567ba6393346c57d9a486ae372`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/5b82228e2d4d8f567ba6393346c57d9a486ae372...de733c9100c3f729fbaaca92cd37c1c322c88832)  
**Author:** German Arciniegas  
**Actor:** `gear66me-ui`  
**ECO ID:** `ECO-20260825-REQ157-TEST-RELEASE-032`  
**Requirements:** `REQ-158-001,REQ-158-002,REQ-158-003`  
**Archive authorized:** `false`  
**Declared changed paths:** `3`  
**Actual changed paths:** `3`  
**Unexpected changed paths:** `0`  
**Forensic result:** **PASS**

### Path reconciliation

- Declared: `viewer/GV-beta-0012P.py, viewer/modules/diagnostics/gv-diagnostics-0004.js, viewer/modules/random-galaxy/gv-random-galaxy-0046.js`
- Actual: `viewer/GV-beta-0012P.py, viewer/modules/diagnostics/gv-diagnostics-0004.js, viewer/modules/random-galaxy/gv-random-galaxy-0046.js`
- Unexpected: `none`
- Declared but absent: `none`

### Complete changed-path accounting

#### `viewer/GV-beta-0012P.py`

- Git status: `A`
- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `4f8003b8280fd0c3e9c9094d92d1fd4801d615595db996b63ca4cc19a17d71f6`
- Bytes: `0` -> `105100`
- Lines: `0` -> `2039`
- Characters: `0` -> `105091`
- Inserted lines: `2039`
- Deleted lines: `0`
- Inserted characters: `105091`
- Deleted characters: `0`
- Changed diff blocks: `1`
- Line arithmetic: **PASS**
- Character arithmetic: **PASS**

#### `viewer/modules/diagnostics/gv-diagnostics-0004.js`

- Git status: `A`
- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `20213375c52df3743394a5745ce222799c365446cb218dadb3fc3064f0e539f0`
- Bytes: `0` -> `15036`
- Lines: `0` -> `257`
- Characters: `0` -> `14932`
- Inserted lines: `257`
- Deleted lines: `0`
- Inserted characters: `14932`
- Deleted characters: `0`
- Changed diff blocks: `1`
- Line arithmetic: **PASS**
- Character arithmetic: **PASS**

#### `viewer/modules/random-galaxy/gv-random-galaxy-0046.js`

- Git status: `A`
- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `e79d103014dd21095389816ee47d50018e481b3375ddc85d13d76b304823e972`
- Bytes: `0` -> `250220`
- Lines: `0` -> `5272`
- Characters: `0` -> `250183`
- Inserted lines: `5272`
- Deleted lines: `0`
- Inserted characters: `250183`
- Deleted characters: `0`
- Changed diff blocks: `1`
- Line arithmetic: **PASS**
- Character arithmetic: **PASS**

### Enforcement findings

- **PASS:** No executable-policy violation detected.

### Standing completion rule

This automated PASS proves only the checks GitHub can perform.
ChatGPT must still perform the requirement-to-hunk reconciliation and
the applicable source/syntax/runtime/visual/live-site/device tests before
calling the ECO complete.

---

## AUTO-b5a7fb4dafbc — GV-ECO-0012N

**Recorded:** 2026-08-25T00:51:36-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`b5a7fb4dafbcd4f910452ef23a5e422e7fcc6793`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/b5a7fb4dafbcd4f910452ef23a5e422e7fcc6793)  
**Parent/baseline:** `ee5fd68b7b25d75a110bbd002e49a0f5641f0a46`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/ee5fd68b7b25d75a110bbd002e49a0f5641f0a46...b5a7fb4dafbcd4f910452ef23a5e422e7fcc6793)  
**Author:** German Arciniegas  
**Actor:** `gear66me-ui`  
**ECO ID:** `GV-ECO-0012N`  
**Requirements:** `REQ-096`  
**Archive authorized:** `false`  
**Declared changed paths:** `1`  
**Actual changed paths:** `1`  
**Unexpected changed paths:** `0`  
**Forensic result:** **PASS**

### Path reconciliation

- Declared: `docs/engineering-change-orders/0012N/GV-ECO-0012N.md`
- Actual: `docs/engineering-change-orders/0012N/GV-ECO-0012N.md`
- Unexpected: `none`
- Declared but absent: `none`

### Complete changed-path accounting

#### `docs/engineering-change-orders/0012N/GV-ECO-0012N.md`

- Git status: `M`
- SHA-256 before: `bf2ffcd49bfc1085837ad26b0331b3e11493718bf47efc5f65686bf853d99794`
- SHA-256 after: `46853a6bfa5a95f26af43c6a760a9c3bbc2a6b3ea15c4c2028491f3aeff5176a`
- Bytes: `10396` -> `7813`
- Lines: `211` -> `159`
- Characters: `10360` -> `7793`
- Inserted lines: `52`
- Deleted lines: `104`
- Inserted characters: `1192`
- Deleted characters: `3759`
- Changed diff blocks: `33`
- Line arithmetic: **PASS**
- Character arithmetic: **PASS**

### Enforcement findings

- **PASS:** No executable-policy violation detected.

### Standing completion rule

This automated PASS proves only the checks GitHub can perform.
ChatGPT must still perform the requirement-to-hunk reconciliation and
the applicable source/syntax/runtime/visual/live-site/device tests before
calling the ECO complete.

---

## AUTO-8607aa183379 — GV-ECO-0012N

**Recorded:** 2026-08-25T00:48:03-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`8607aa183379cd56c63887872d14311194e1d596`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/8607aa183379cd56c63887872d14311194e1d596)  
**Parent/baseline:** `799f240d6890fea8ab5e1393dcb8e1b7aa87140c`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/799f240d6890fea8ab5e1393dcb8e1b7aa87140c...8607aa183379cd56c63887872d14311194e1d596)  
**Author:** German Arciniegas  
**Actor:** `gear66me-ui`  
**ECO ID:** `GV-ECO-0012N`  
**Requirements:** `CHANGE-CONTROL-STRUCTURE`  
**Archive authorized:** `false`  
**Declared changed paths:** `1`  
**Actual changed paths:** `1`  
**Unexpected changed paths:** `0`  
**Forensic result:** **PASS**

### Path reconciliation

- Declared: `docs/engineering-change-orders/GV-ECO-0012N.md`
- Actual: `docs/engineering-change-orders/GV-ECO-0012N.md`
- Unexpected: `none`
- Declared but absent: `none`

### Complete changed-path accounting

#### `docs/engineering-change-orders/GV-ECO-0012N.md`

- Git status: `D`
- SHA-256 before: `409ff064604d0ddd9f6d69194634b98aaeb4bb1ebccb20169cbbfd106f87a55f`
- SHA-256 after: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Bytes: `5834` -> `0`
- Lines: `148` -> `0`
- Characters: `5822` -> `0`
- Inserted lines: `0`
- Deleted lines: `148`
- Inserted characters: `0`
- Deleted characters: `5822`
- Changed diff blocks: `1`
- Line arithmetic: **PASS**
- Character arithmetic: **PASS**

### Enforcement findings

- **PASS:** No executable-policy violation detected.

### Standing completion rule

This automated PASS proves only the checks GitHub can perform.
ChatGPT must still perform the requirement-to-hunk reconciliation and
the applicable source/syntax/runtime/visual/live-site/device tests before
calling the ECO complete.

---
