# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AC

**Release:** `GV-beta-0007AC`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007AB.py`  
**Status:** IMPLEMENTED — FETCH-BACK / FORENSIC REVIEW PASS; USER VISUAL ACCEPTANCE PENDING

## 1. User request

Expand the Projection submenu from its existing Mollweide row to five complete labeled rows in this exact order:

1. MOLLWEIDE
2. SPHERICAL
3. ORTHOGRAPHIC
4. TANGENTIAL
5. SINUSOIDAL

Each row must contain the existing long text-tile geometry plus a square icon tile immediately to its right. The four new icon tiles must remain intentionally empty. No new projection actions are wired to Aladin in this release.

The approved Mollweide row, 0003 SVG geometry, 24×24 size, measured centering, 7AB synchronized glow behavior, main Projection row/icon/glow, coordinate strip, hamburger, target/SIMBAD, Aladin initialization, galaxy catalog/navigation, bottom controls, fonts, colors, and all unrelated behavior must remain unchanged. Splash animation remains absent from this launcher/release.

## 2. Change-control preflight

Before implementation the active files were fetched from `beta`:

- `.github/workflows/automatic-change-control-log.yml`
- `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`
- `viewer/GV-beta-0007AB.py`
- `mobile/beta/7AB.html`

The inherited Projection submenu construction was also audited. The existing option row uses:

- submenu width: `158px`
- text tile: `120×36px`
- icon tile: `36×36px`
- text/icon horizontal gap: `2px`

7AC preserves that existing geometry and anchor.

## 3. Authorized paths

Implementation:

- `viewer/GV-beta-0007AC.py`
- `mobile/beta/7AC.html`

Post-review record:

- `docs/engineering-change-orders/GV-ECO-0007AC.md`

No existing viewer, launcher, splash, artwork, font, workflow, coordinate module, catalog, manifest, service-worker, or documentation file was modified by the direct implementation commits.

## 4. Exact implementation

### 4.1 Baseline preservation

`GV-beta-0007AC.py` loads the exact reviewed 7AB baseline using the fetched 7AB blob identifier:

`68d892fde62240d284a71263a2ab796d7e71f758`

7AC does not reproduce, replace, or edit the existing Projection/Mollweide SVG geometry or 7AB Web Animations glow implementation.

### 4.2 Submenu expansion

When `.gv-projection-submenu` and its existing direct child `.gv-projection-option-row` appear, 7AC uses that existing Mollweide row as the structural template.

The original Mollweide row remains in place and is not replaced.

Four new rows are cloned from that structure and appended in this order:

- SPHERICAL
- ORTHOGRAPHIC
- TANGENTIAL
- SINUSOIDAL

The submenu is changed only to a vertical flex stack with a `2px` row gap. Its existing `158px` width and anchor are retained.

### 4.3 New icon tiles

For each of the four cloned rows, the cloned square icon button is emptied with `innerHTML=""` before it is appended.

Therefore:

- no placeholder SVG is introduced;
- no question mark or temporary artwork is introduced;
- no AI-generated artwork is introduced;
- no new projection action is wired.

### 4.4 Clone isolation

IDs, inline event attributes, and inherited `data-*` attributes are stripped from cloned descendants before the new row-specific 7AC marker is assigned. DOM event listeners are not copied by `cloneNode`, so the new rows do not inherit the original Mollweide click handler by cloning.

### 4.5 Version

Only the runtime version label is advanced to:

`V-7AC`

## 5. Implementation commits and complete direct-path accounting

### Viewer source

Commit:

`4202e1d53fad061fad21ffec80cecff3fda2efdd`

Fetched Git blob SHA:

`3c74f216768dd6c8cede63fc51e76b71d8da40d2`

Direct commit comparison reports exactly one path:

- `viewer/GV-beta-0007AC.py` — **ADDED** — 140 additions, 0 deletions.

Independent automatic forensic accounting:

- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `3eb140e1376d69748c5f9579783e092fa20fcfd17f78d7b94c1ac0089e89475c`
- Bytes: `0 → 7511`
- Lines: `0 → 140`
- Characters: `0 → 7509`
- Inserted lines: `140`
- Deleted lines: `0`
- Inserted characters: `7509`
- Deleted characters: `0`
- Unified diff hunks: `1`
- Inserted blocks: `1`
- Deleted blocks: `0`
- Changed blocks: `1`
- Line balance: `0 + 140 - 0 = 140` — **PASS**
- Character balance: `0 + 7509 - 0 = 7509` — **PASS**

### Launcher

Commit:

`a626848a4f56a2e7efb3b465e6a41484bfba1ee0`

Fetched Git blob SHA:

`c8b425a5469e6cb2e90d46a87d25862ae403f773`

Direct commit comparison reports exactly one path:

- `mobile/beta/7AC.html` — **ADDED** — 45 additions, 0 deletions.

Independent automatic forensic accounting:

- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `b57b7d5c337941dc1ad14e7c9c609d042c24fbfc65363602d033db0b571c1e4a`
- Bytes: `0 → 2804`
- Lines: `0 → 45`
- Characters: `0 → 2797`
- Inserted lines: `45`
- Deleted lines: `0`
- Inserted characters: `2797`
- Deleted characters: `0`
- Unified diff hunks: `1`
- Inserted blocks: `1`
- Deleted blocks: `0`
- Changed blocks: `1`
- Line balance: `0 + 45 - 0 = 45` — **PASS**
- Character balance: `0 + 2797 - 0 = 2797` — **PASS**

## 6. Fetch-back review

The committed viewer source was fetched back from `beta` and verified to contain:

- the exact user request/change-order comments;
- the exact 7AB baseline URL/blob identifier;
- only the required two CSS rules for vertical submenu stacking;
- the five approved projection labels in the specified order;
- four cloned rows only;
- explicit clearing of the four new icon interiors;
- no new SVG/icon implementation;
- no Aladin projection wiring;
- the required runtime validation contract;
- V-7AC version-label update.

The committed launcher was fetched back and verified to:

- load viewer commit `4202e1d53fad061fad21ffec80cecff3fda2efdd`;
- contain only the standard viewer loader/error wrapper;
- not load a splash animation.

Direct commit comparisons confirm one intended new path per implementation commit and no existing-file modifications.

## 7. Line-by-line scope audit

Every line in the new viewer source falls into one of the authorized categories:

1. ECO / purpose / user-request / preserved-behavior comments;
2. required 7AB loader and V-7AC metadata;
3. authorized Projection submenu vertical-stack CSS;
4. authorized projection row cloning and labels;
5. authorized clearing/isolation of the four new icon tiles;
6. required 7AC software-validation contract.

Every line in the launcher falls into one of:

1. ECO/source comments;
2. required 7AC title/loading/version metadata;
3. standard launcher loader/error logic pointing to the reviewed 7AC viewer commit.

No changed line was identified that performs unrelated cleanup, refactoring, geometry changes, animation changes, splash integration, or feature work outside the approved scope.

## 8. Runtime validation contract

`GV-beta-0007AC.py` exposes `window.GV7AC_VALIDATION` after the Projection submenu exists.

It verifies:

- exactly five direct projection rows exist;
- label order is exactly MOLLWEIDE / SPHERICAL / ORTHOGRAPHIC / TANGENTIAL / SINUSOIDAL;
- exactly five label buttons exist;
- exactly five square icon buttons exist;
- Mollweide retains its SVG;
- the four new icon interiors are empty;
- all text-tile dimensions match;
- all icon-tile dimensions match and remain square;
- all vertical row gaps match the required `2px`;
- the Mollweide control retains running 7AB animations;
- the main Projection icon retains running 7AB animations;
- no duplicate projection labels exist;
- runtime version label is `V-7AC`.

A failed condition throws:

`GV-BETA-0007AC CONTRACT FAILED`

The four new projection actions remain intentionally unwired.

## 9. Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Five projection rows defined | PASS |
| Correct label order | PASS BY SOURCE + RUNTIME CONTRACT |
| Four new square icon tiles empty | PASS BY SOURCE + RUNTIME CONTRACT |
| Mollweide SVG untouched | PASS BY INHERITANCE + RUNTIME CONTRACT |
| Mollweide 7AB glow preserved | PASS BY INHERITANCE + RUNTIME CONTRACT |
| Main Projection glow preserved | PASS BY INHERITANCE + RUNTIME CONTRACT |
| Text tile dimensions consistent | PASS BY RUNTIME CONTRACT |
| Square tile dimensions consistent | PASS BY RUNTIME CONTRACT |
| 2px vertical row rhythm | PASS BY RUNTIME CONTRACT |
| New projections wired to Aladin | NO — intentionally deferred |
| Splash loaded/modified by 7AC | NO |
| Previous viewer/launcher modified | NO |
| Viewer forensic reconciliation | PASS |
| Launcher forensic reconciliation | PASS |
| Viewer fetch-back review | PASS |
| Launcher fetch-back review | PASS |
| User visual acceptance | PENDING |

## 10. Explicitly not changed

7AC does **not** modify:

- `viewer/GV-beta-0007AB.py`
- `mobile/beta/7AB.html`
- any previous viewer or launcher release
- Projection main-row geometry or icon
- Projection/Mollweide glow timing, keyframes, intensity, or synchronization
- Mollweide SVG geometry, size, or measured centering
- coordinate strip/module/font
- hamburger
- target/SIMBAD
- Aladin initialization
- galaxy catalog or navigation
- bottom controls
- splash animation
- artwork
- fonts
- service worker
- manifests
- workflows
- catalogs

## 11. Release launcher

`mobile/beta/7AC.html`

**User visual acceptance remains PENDING.**
