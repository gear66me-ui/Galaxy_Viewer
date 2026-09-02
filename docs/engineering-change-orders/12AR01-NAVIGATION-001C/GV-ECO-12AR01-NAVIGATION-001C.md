# ECO-20260902-12AR01-NAVIGATION-ADMIN-001C

Repository: `gear66me-ui/Galaxy_Viewer`  
Branch: `beta`  
Archive authorized: `false`  
User GO: `true`  

## Requirements

REQ-001 through REQ-020 are the numbered requirements published in chat immediately before GO, covering N=130 route planning, refill at 120, metadata-only planning, preservation of the future-10 preparation window, route atomicity, S7 travel, first travel T/2, 17/15/12/9/6 settings, telemetry, standalone admin UI, hamburger replacement, literal 0086-01 and 12AR-01 uprevs, preserved prewarming/background work, persistent ECO traceability, pre-commit forensic gating, and conditional pointer promotion.

## Authoritative baselines

- `viewer/GV-beta-0012AR.py` — blob `6748b9a930f71af97ad2767f2bf197096d8f8907`
- `viewer/modules/random-galaxy/gv-random-galaxy-0086.js` — blob `04876b77875684115c7e4c0a7e61fe8dec336503`
- `viewer/modules/hamburger-menu/gv-hamburger-menu-0006.js` — blob `cbcdce09ff37e9885f1c5232f8c61a6d7d01e771`
- `viewer/gv-current-viewer.json` — blob `d56e9ad0e9d7ceb67906503364f8fb72abe327b9`

## Planned source operations

### `viewer/GV-beta-0012AR-01.py`

Create only from the exact complete 12AR baseline. Planned changes are limited to the ECO pointer, visible/version constants, module URLs/loader keys/version assertions for hamburger 0007, Navigation 0001, Navigation Admin 0001, and Random 0086-01; remove Viewer-owned travel timing overrides; instantiate/bind Navigation after authoritative catalog load; pass Navigation into Random. No benchmark UI is embedded in the Viewer.

### `viewer/modules/random-galaxy/gv-random-galaxy-0086-01.js`

Create only from the exact complete 0086 baseline. Planned changes are limited to version/ECO identity, Navigation delegation for ordinary translation/FOV/rotation timing, T/2 first-travel duration ownership, removal of effective ordinary late alignment displacement, telemetry hooks, sourcing the future-10 preparation window from the committed Navigation route, committing Navigation only after successful arrival, and preventing poisoned-head preparation handling from altering committed route membership. Existing HD/prewarm/archive/history/UI/preparation systems remain protected.

### `viewer/modules/navigation/gv-navigation-0001.js`

Create new module with nine explicit sections: constants/eligibility, sky/rotation math, graph, route solver, atomic queue/refill, travel timing, S7 motion, telemetry, public API.

### `viewer/modules/hamburger-menu/gv-navigation-admin-0001.js`

Create standalone hidden engineering interface for 17/15/12/9/6 travel setting selection and navigation data download.

### `viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js`

Create from exact hamburger 0006 baseline. Only version/ECO identity and the `DOWNLOAD ANALYTICS` menu slot are replaced with `TRAVEL SETTINGS` opening `GalaxyViewerNavigationAdmin`. Diagnostics, projection, survey and reticle behavior remain unchanged.

## Protected scope

Everything not explicitly listed above is default-deny protected, including `viewer/archive/**`, existing 12AR, existing 0086, existing hamburger 0005/0006, diagnostics modules, catalogs, artwork, APK/native wrapper, download analytics source, and unrelated Random Galaxy behavior.

# PRE-COMMIT VERIFICATION / ACTUAL CANDIDATE STATUS

## Baseline transfer gate

- Hamburger 0006 complete authoritative baseline reconstructed locally and verified by exact Git blob hash: `cbcdce09ff37e9885f1c5232f8c61a6d7d01e771` — PASS.
- Viewer 12AR complete authoritative baseline transfer into local working storage — BLOCKED by connector/display transfer limitation; authoritative blob identity known but exact full local byte stream is not available.
- Random 0086 complete authoritative baseline transfer into local working storage — BLOCKED by connector/display transfer limitation; authoritative blob identity known but exact full local byte stream is not available.

Because the project procedure forbids reconstructing those large baselines from displayed excerpts, 12AR-01 and 0086-01 candidates are intentionally NOT fabricated and no repository implementation commit is authorized at this stage.

## Standalone candidate counts

### `gv-navigation-0001.js`
- Git blob: `ea3d28394b0ca3a8879eb67dae04eb7332f07665`
- SHA-256: `c1bd1b31798208c9efcc4a86f8a90cf3a1e580710074d86ce8143ed9d6b2d908`
- Bytes: 16285
- Characters: 16266
- Lines: 449
- Blank / nonblank: 45 / 404
- Spaces / tabs: 2394 / 0
- LF / CR: 449 / 0
- Total whitespace: 2843
- Non-whitespace: 13423
- Word-like tokens: 1859
- Deterministic JS engineering tokens: 4322
- Node syntax: PASS

### `gv-navigation-admin-0001.js`
- Git blob: `4f9a859a97a3fc9f80b5681c4765fba2eefe5083`
- SHA-256: `e308894dce05d64fc1dae5cda24fc86ac1b2495d761aadafe359d55efe04b5c3`
- Bytes: 4826
- Characters: 4824
- Lines: 92
- Blank / nonblank: 9 / 83
- Spaces / tabs: 449 / 0
- LF / CR: 92 / 0
- Total whitespace: 541
- Non-whitespace: 4283
- Word-like tokens: 612
- Deterministic JS engineering tokens: 1459
- Node syntax: PASS

### Hamburger 0006 baseline → 0007 candidate
- Baseline Git blob: `cbcdce09ff37e9885f1c5232f8c61a6d7d01e771`
- Candidate Git blob: `441002e37903e001349643be35fb793f25c278bd`
- Baseline bytes / candidate bytes: 1828 / 1859
- Baseline characters / candidate characters: 1828 / 1859
- Baseline lines / candidate lines: 42 / 42
- Baseline spaces / candidate spaces: 206 / 207
- Baseline engineering tokens / candidate: 485 / 498
- Node syntax: PASS
- Diff hunks: 3
- Hunk 1: header/version/left label — maps REQ-011 and REQ-018
- Hunk 2: action branch `DOWNLOAD ANALYTICS` → `TRAVEL SETTINGS` — maps REQ-010/011/012
- Hunk 3: row[2] relabel — maps REQ-011
- Unmapped hunks: 0

## Solver / motion test

Deterministic synthetic 940-record catalog:
- eligible: 940
- committed route length: 130
- unique route members: 130
- all 129 internal edges valid: PASS
- minimum travel: 60.4851152651°
- maximum travel: 129.6849145523°
- minimum rotation: 40.4452886526°
- maximum rotation: 108.2656877395°
- T=17 first travel: 8.5 s
- translation at u=.30/.50/.70: 0 / 0.5 / 1
- FOV at u=.50: 237.6° within floating-point tolerance
- rotation reaches target by u=.70: PASS
- after ten route commits: 120 remaining
- next complete batch background planning/ready state: PASS

## Implementation progress after GO

The standalone components were committed one path at a time with immediate GitHub fetch-back verification.

- `viewer/modules/navigation/gv-navigation-0001.js` — initial write `6c94c5de534b390110e99ba11765d0e167d2e8ca` failed candidate-identity verification; recovery ECO 001D then committed exact verified blob in `0fb5a8f96ad9519f7805b3e4f575bfb7929d7270`; fetched-back blob `ea3d28394b0ca3a8879eb67dae04eb7332f07665` — PASS.
- `viewer/modules/hamburger-menu/gv-navigation-admin-0001.js` — commit `bfcfb04cd63e9cf1634db70f308dc2e51134794b`; fetched-back blob `4f9a859a97a3fc9f80b5681c4765fba2eefe5083` equals verified candidate — PASS.
- `viewer/modules/hamburger-menu/gv-hamburger-menu-0007.js` — commit `7a535e173d486844bae4b62294704830a457bd56`; fetched-back blob `441002e37903e001349643be35fb793f25c278bd` equals verified candidate — PASS.

The mandatory literal full-copy `12AR-01` and `0086-01` candidates remain blocked until exact complete authoritative baseline bytes can be transferred into working storage and verified against their Git blob SHAs. The live pointer remains unchanged.

## Final verification section

Reserved. After a future authorized implementation commit, this section must contain fetched-back committed blobs, complete before/after byte/character/line/space/token accounting, every unified diff hunk mapped to REQ IDs, three independent source reconciliation passes, adversarial protected-source inspection, and the explicit answer to `WHAT CHANGED THAT THE USER DID NOT REQUEST?`.
