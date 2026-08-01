# Galaxy Viewer — Automated Change Control Log

This cumulative forensic record tracks changes pushed to the `beta` branch of `gear66me-ui/Galaxy_Viewer`.

The log is designed to answer future questions such as:

- What changed?
- Which files changed?
- What instruction authorized the change?
- What behavior was intended to remain untouched?
- Which commit introduced the change?
- Was the change isolated or did it affect multiple files?

## Operating rules

1. New entries are appended chronologically at the bottom.
2. Existing entries are not rewritten automatically.
3. The automated workflow records observable Git facts and does not invent intent.
4. The approved user instruction should be preserved in a change-order comment inside each authorized modified text file whenever that comment is part of the approved change.
5. The workflow extracts supported change-order markers from modified files when present.
6. Multi-file commits are marked for scope review.
7. Workflow-generated log-only commits are excluded to prevent recursion.
8. Git commits and file contents remain the authoritative technical evidence.

---

## GV-CC-0001 — Change-control system adopted

**Date:** 2026-07-31  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Status:** ACTIVE

### User instruction

Create a simple, automatic change-control system that records every repository change so future regressions can be traced. Preserve the approved instruction inside modified source files when authorized, allowing later comparison between what was requested and what actually changed.

### Current project state

- Galaxy Viewer development spans Python, HTML, JavaScript, mobile launcher files, artwork, manifests, service workers, catalogs, and GitHub Actions workflows.
- Development currently uses GitHub with Python and browser-based components, including Aladin Lite.
- Kotlin is a possible future Android application shell, and Swift is a possible future Apple application shell.
- The repository remains public for now.
- Private-source and public-deployment separation remains under consideration and has not been implemented.

### Problems motivating this system

- Development is distributed across many chats and standalone versions.
- Frequent versioning makes it difficult to remember why a change was made.
- A fix in one area may unintentionally alter unrelated behavior.
- A regression may not become visible until weeks or months after its introduction.
- Large files and connector limitations can make manual reconstruction cumbersome.
- Unauthorized or unrelated modifications are a major project concern.
- The project requires a durable record of the user's approved instruction, changed paths, preserved behavior, and rollback evidence.

### Approved implementation

1. Create this cumulative Change Control Log.
2. Create a GitHub Actions workflow that runs after pushes to `beta`.
3. Record commit metadata and every changed path automatically.
4. Mark multi-file changes for scope review.
5. Extract supported change-order comments from changed text files when present.
6. Do not invent reasons absent from commit metadata or source comments.
7. Prevent recursive log commits.
8. Keep the repository public.
9. Do not add launcher analytics in this change.
10. Do not modify existing viewer, launcher, mobile, artwork, catalog, manifest, service-worker, or workflow files.

### Authorized paths

- `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`
- `.github/workflows/automatic-change-control-log.yml`

### Protected paths

Every pre-existing repository path and all repository settings.

### Acceptance status

- Change Control Log created: **PASS**
- Automatic workflow created: **PENDING**
- Workflow syntax validation: **PENDING**
- Workflow execution on GitHub: **REQUIRES WORKFLOW RUN**
- Existing application behavior: **UNCHANGED BY DESIGN**

### Tags

`CHANGE-CONTROL`, `AUDIT`, `REGRESSION`, `AUTHORIZATION`, `BETA`, `WORKFLOW`

---
## AUTO-2e22a6c3c6dd — Add automatic Galaxy Viewer change control workflow

**Recorded:** 2026-07-31T21:47:44-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`2e22a6c3c6dd65475bb6865a0957dcc0d7aae895`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/2e22a6c3c6dd65475bb6865a0957dcc0d7aae895)  
**Parent/baseline:** `dfe6ab3383483027465b36d0e570b06905f31b3f`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/dfe6ab3383483027465b36d0e570b06905f31b3f...2e22a6c3c6dd65475bb6865a0957dcc0d7aae895)  
**Author:** German Arciniegas  
**Scope flag:** **SINGLE-FILE CHANGE**

### Commit message

```text
Add automatic Galaxy Viewer change control workflow
```

### Changed paths

- **ADDED:** `.github/workflows/automatic-change-control-log.yml` — additions: `211`, deletions: `0`

### Recorded instruction evidence

**`.github/workflows/automatic-change-control-log.yml`**

```text
"GALAXY VIEWER CHANGE ORDER",
"CHANGE ORDER:",
"USER INSTRUCTION:",
"AUTHORIZED CHANGES:",
"PRESERVED BEHAVIOR:",
"PURPOSE:",
```

### Search tags

`ADD`, `AUTOMATIC`, `CHANGE`, `CONTROL`, `GALAXY`, `GITHUB`, `LOG`, `VIEWER`, `WORKFLOW`, `WORKFLOWS`, `YML`

---
