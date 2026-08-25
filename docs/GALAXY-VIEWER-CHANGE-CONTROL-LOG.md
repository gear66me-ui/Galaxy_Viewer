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
