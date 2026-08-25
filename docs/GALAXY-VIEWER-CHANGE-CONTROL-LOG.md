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
