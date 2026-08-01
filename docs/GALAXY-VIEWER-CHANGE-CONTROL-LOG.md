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
## AUTO-277059952e93 — Add cinematic five-rotation siphon in Singularity 0021

**Recorded:** 2026-07-31T21:48:47-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`277059952e934201b972a5cf9e11223cf733955e`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/277059952e934201b972a5cf9e11223cf733955e)  
**Parent/baseline:** `cfb749a6d7f4626154a82949eb58d9c9deddfac0`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/cfb749a6d7f4626154a82949eb58d9c9deddfac0...277059952e934201b972a5cf9e11223cf733955e)  
**Author:** German Arciniegas  
**Scope flag:** **SINGLE-FILE CHANGE**

### Commit message

```text
Add cinematic five-rotation siphon in Singularity 0021
```

### Changed paths

- **ADDED:** `viewer/artwork/Splash/Galaxy-Viewer-Singularity-0021.html` — additions: `21`, deletions: `0`

### Recorded instruction evidence

Reason or user instruction not found in supported source comments. Refer to the commit message and exact diff; no intent has been invented.

### Search tags

`0021`, `ADD`, `ARTWORK`, `CINEMATIC`, `FIVE`, `GALAXY`, `HTML`, `ROTATION`, `SINGULARITY`, `SIPHON`, `SPLASH`, `VIEWER`

---
## AUTO-dff01b914ca1 — Add reliable bounded splash startup in Singularity 0022

**Recorded:** 2026-07-31T22:23:59-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`dff01b914ca1e41e4592e140f7e6f6f7fafc79b1`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/dff01b914ca1e41e4592e140f7e6f6f7fafc79b1)  
**Parent/baseline:** `1365174e5581d904430edd72dc169426c12c7958`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/1365174e5581d904430edd72dc169426c12c7958...dff01b914ca1e41e4592e140f7e6f6f7fafc79b1)  
**Author:** German Arciniegas  
**Scope flag:** **SINGLE-FILE CHANGE**

### Commit message

```text
Add reliable bounded splash startup in Singularity 0022
```

### Changed paths

- **ADDED:** `viewer/artwork/Splash/Galaxy-Viewer-Singularity-0022.html` — additions: `22`, deletions: `0`

### Recorded instruction evidence

Reason or user instruction not found in supported source comments. Refer to the commit message and exact diff; no intent has been invented.

### Search tags

`0022`, `ADD`, `ARTWORK`, `BOUNDED`, `GALAXY`, `HTML`, `RELIABLE`, `SINGULARITY`, `SPLASH`, `STARTUP`, `VIEWER`

---
## AUTO-a99821843800 — Add GV-beta-0006P coordinate aperture test

**Recorded:** 2026-07-31T22:35:22-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`a99821843800218a428d7696e9dded1bc4de4908`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/a99821843800218a428d7696e9dded1bc4de4908)  
**Parent/baseline:** `99f64c95d5b0e4d0627085e02f1347203423658c`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/99f64c95d5b0e4d0627085e02f1347203423658c...a99821843800218a428d7696e9dded1bc4de4908)  
**Author:** German Arciniegas  
**Scope flag:** **SINGLE-FILE CHANGE**

### Commit message

```text
Add GV-beta-0006P coordinate aperture test
```

### Changed paths

- **ADDED:** `viewer/GV-beta-0006P.py` — additions: `171`, deletions: `0`

### Recorded instruction evidence

Reason or user instruction not found in supported source comments. Refer to the commit message and exact diff; no intent has been invented.

### Search tags

`0006P`, `ADD`, `APERTURE`, `BETA`, `COORDINATE`, `TEST`, `VIEWER`

---
## AUTO-1c7cd5779f90 — Point beta mobile loader to GV-beta-0006P

**Recorded:** 2026-07-31T22:36:13-05:00  
**Repository:** `gear66me-ui/Galaxy_Viewer`  
**Branch:** `beta`  
**Source commit:** [`1c7cd5779f90562fb7244859fe35ee1ca7e134bf`](https://github.com/gear66me-ui/Galaxy_Viewer/commit/1c7cd5779f90562fb7244859fe35ee1ca7e134bf)  
**Parent/baseline:** `da465e0ecd5399791a3dcaa2909ca9f5024aab6e`  
**Comparison:** [View exact diff](https://github.com/gear66me-ui/Galaxy_Viewer/compare/da465e0ecd5399791a3dcaa2909ca9f5024aab6e...1c7cd5779f90562fb7244859fe35ee1ca7e134bf)  
**Author:** German Arciniegas  
**Scope flag:** **SINGLE-FILE CHANGE**

### Commit message

```text
Point beta mobile loader to GV-beta-0006P
```

### Changed paths

- **MODIFIED:** `mobile/beta/index.html` — additions: `17`, deletions: `17`

### Recorded instruction evidence

Reason or user instruction not found in supported source comments. Refer to the commit message and exact diff; no intent has been invented.

### Search tags

`0006P`, `BETA`, `HTML`, `INDEX`, `LOADER`, `MOBILE`, `POINT`

---
