# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AD

**Release:** `GV-beta-0007AD`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007AC.py`  
**Status:** IMPLEMENTED — FETCH-BACK / FORENSIC REVIEW PASS; RUNTIME + USER VISUAL ACCEPTANCE PENDING

## 1. Exact user request

Create a new standalone 7AD release that preserves 7AC and makes the left main-menu column and the right Projection submenu mathematically symmetric. The long text tiles on both sides must have the same calculated width, the square icon tiles must have identical square dimensions, and the whole two-column menu must fill the measured horizontal span from the existing left-menu edge to the measured right edge of the target button.

The long-tile width must be calculated from measured runtime geometry rather than guessed. The existing Space Age font family is preserved; the added width is used so labels such as PROJECTION, RETICLE ON/OFF, ORTHOGRAPHIC, and the other projection names do not need to be squeezed.

While Projection mode is open, LAYERS, GRID, SURVEY, and RETICLE ON/OFF must remain visible but be visually grayed/dimmed and must not glow or pulse. The Projection main row remains active. The inherited Projection and Mollweide glow behavior must remain unchanged. The five right-side projection rows and order remain unchanged, with the four new right icon tiles empty and unwired.

No splash, artwork, font, module, workflow, prior release, coordinate strip, hamburger, target/SIMBAD, Aladin initialization, galaxy catalog/navigation, bottom controls, service worker, manifest, or unrelated behavior is authorized to change.

## 2. Mandatory change-control preflight

Before writing 7AD, the following active `beta` files were fetched and reviewed:

- `.github/workflows/automatic-change-control-log.yml`
- `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`
- `viewer/GV-beta-0007AC.py`
- `mobile/beta/7AC.html`

The inherited menu DOM/CSS was also audited. The left menu uses five direct `.gv-viewer-menu-row` rows, each containing `.gv-viewer-menu-label` and `.gv-viewer-menu-icon`. The Projection submenu uses five `.gv-projection-option-row` rows, each containing `.gv-projection-option-label` and `.gv-projection-option-icon`.

The direct implementation commits were not allowed to touch any existing approved file.

## 3. Authorized paths

Implementation:

- `viewer/GV-beta-0007AD.py`
- `mobile/beta/7AD.html`

Post-review ECO record:

- `docs/engineering-change-orders/GV-ECO-0007AD.md`

No other direct path was authorized.

## 4. Mathematical symmetric-layout design

7AD measures runtime geometry rather than assigning a guessed long-tile width.

Definitions:

- `A` = usable horizontal span from the measured left edge of the existing left menu to the measured right edge of the target button.
- `S` = measured square icon width from the existing first left icon tile.
- `G` = measured text-to-icon gap from the existing first left row.
- `C` = explicit inter-column gap. For a disciplined single-gap system, 7AD sets `C = G`.
- `W` = calculated width of every long text tile on both sides.

Required equation:

`2W + 2S + 2G + C = A`

Therefore:

`W = (A - 2S - 2G - C) / 2`

7AD calculates `W` after the inherited 7AC menu exists, then applies that exact value to every left and right long label tile. It applies the same measured `S` to every left and right square icon tile.

The left group width is:

`groupWidth = W + G + S`

The right column starts at:

`rightLeft = leftStart + groupWidth + C`

The runtime contract independently re-evaluates the equation residual and requires matching long-tile and square-tile dimensions within `0.50 px`.

## 5. Exact implementation

### 5.1 Baseline preservation

`GV-beta-0007AD.py` loads the reviewed 7AC baseline by its fetched Git blob identifier:

`3c74f216768dd6c8cede63fc51e76b71d8da40d2`

7AD does not reproduce or replace the Projection SVG, Mollweide SVG, 7AB Web Animations keyframes, coordinate code, navigation, target logic, or other viewer systems.

### 5.2 Symmetric width application

After the five left and five right rows exist, 7AD:

1. measures the root rectangle;
2. measures the left menu start;
3. measures the target button right edge;
4. measures the existing square size `S`;
5. measures the existing text-to-icon gap `G`;
6. sets `C = G`;
7. calculates `W` from the approved equation;
8. applies one `groupWidth` to the left menu and right submenu;
9. applies the same `W` to all ten long text tiles;
10. applies the same `S` to all ten square icon tiles;
11. applies the same `G` as the text/icon gap and vertical row gap;
12. positions the right submenu so its rightmost square tile aligns with the measured target-button right boundary.

### 5.3 Typography

No font file or font family is changed.

The menu labels use the existing `Space Age` family inherited from the viewer. Both left and right menu label groups are explicitly normalized to the existing main-menu sizing philosophy:

- `font-size: 12px`
- `letter-spacing: .55px`

No condensed font, new font, or forced letter-spacing reduction is introduced.

### 5.4 Projection-mode inactive-row dimming

When the Projection submenu has the inherited `.gv-open` state, 7AD adds one state class to the viewer root:

`gv-7ad-projection-mode`

Only the four non-Projection left rows are targeted:

- LAYERS
- GRID
- SURVEY
- RETICLE ON/OFF

Their label and icon tiles remain visible and geometrically unchanged, but are given a disciplined gray/dim treatment using reduced opacity, grayscale/saturation reduction, brightness reduction, and a restrained static shadow.

Animations are explicitly suppressed on those four inactive rows and descendants while Projection mode is open.

The first Projection row is not targeted by the dimming selectors, so its selected state and inherited glow remain available.

### 5.5 Existing Projection/Mollweide glow

7AD does not define new Projection or Mollweide animation keyframes and does not change inherited glow timing, easing, intensity, geometry, or phase.

The runtime validator requires active running animations to remain present on both the main Projection icon and the Mollweide icon.

### 5.6 Projection rows/actions

The right-side order remains exactly:

1. MOLLWEIDE
2. SPHERICAL
3. ORTHOGRAPHIC
4. TANGENTIAL
5. SINUSOIDAL

The four new right-side icon tiles remain empty. No new SVGs, artwork, placeholders, or Aladin projection actions are introduced in 7AD.

### 5.7 Version and splash

Runtime version label advances only to `V-7AD`.

7AD and its launcher do not load a splash animation.

## 6. Viewer commit — complete forensic accounting

Commit:

`19f5a381314e1ebb336f7d25c4df9fdb54163301`

Fetched Git blob SHA:

`471600aa091123791196024c79df948782b728e4`

Direct comparison reports exactly one changed path:

- `viewer/GV-beta-0007AD.py` — **ADDED** — 216 additions, 0 deletions.

Automatic forensic accounting:

- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `b622c1f6f1979b2944a3732c83dcc228adbc3eaf37644eb6f47d8a80cf377b05`
- Bytes: `0 → 13309`
- Lines: `0 → 216`
- Characters: `0 → 13307`
- Inserted lines: `216`
- Deleted lines: `0`
- Inserted characters: `13307`
- Deleted characters: `0`
- Unified diff hunks: `1`
- Inserted blocks: `1`
- Deleted blocks: `0`
- Changed blocks: `1`
- Line balance: `0 + 216 - 0 = 216` — **PASS**
- Character balance: `0 + 13307 - 0 = 13307` — **PASS**

## 7. Launcher commit — complete forensic accounting

Commit:

`c1adb9e4b9f0634eaf67dc5b99eb87876ad37ea8`

Fetched Git blob SHA:

`aeb90d81dcd5bf1050cb0b5fd1517b85b5d98d38`

Direct comparison reports exactly one changed path:

- `mobile/beta/7AD.html` — **ADDED** — 45 additions, 0 deletions.

Automatic forensic accounting:

- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `421eca78c2a5e8888aeb8d2e6a8ad13e5e936cbb5be579d656a69d96d8da2437`
- Bytes: `0 → 2846`
- Lines: `0 → 45`
- Characters: `0 → 2839`
- Inserted lines: `45`
- Deleted lines: `0`
- Inserted characters: `2839`
- Deleted characters: `0`
- Unified diff hunks: `1`
- Inserted blocks: `1`
- Deleted blocks: `0`
- Changed blocks: `1`
- Line balance: `0 + 45 - 0 = 45` — **PASS**
- Character balance: `0 + 2839 - 0 = 2839` — **PASS**

## 8. Fetch-back review

The committed viewer source was fetched back from `beta` and reviewed after commit.

Verified:

- exact 7AD purpose/user-request comments are present;
- 7AC is the sole viewer baseline;
- long-tile width is derived from runtime geometry using the approved equation;
- no guessed `W` constant exists;
- the target-button right edge supplies the right boundary;
- one measured square size is applied to both columns;
- one measured text/icon gap is used across both columns;
- `C = G` provides one disciplined inter-column gap;
- right and left labels receive the same 12px / .55px menu typography;
- only the four inactive left rows are dimmed;
- inactive-row animations are suppressed only during Projection mode;
- no Projection/Mollweide animation keyframes are redefined;
- no new projection icons or actions are created;
- splash is not loaded.

The committed launcher was fetched back and verified to load viewer commit `19f5a381314e1ebb336f7d25c4df9fdb54163301` and no splash.

## 9. Line-by-line scope classification

Every line in `viewer/GV-beta-0007AD.py` was reviewed against the authorized categories and falls into one of:

1. 7AD ECO/source comments;
2. 7AC baseline loader / V-7AD metadata;
3. runtime geometry measurement;
4. mathematical symmetric-width calculation;
5. symmetric left/right menu layout CSS/JS;
6. authorized menu-label sizing/spacing caused by the wider tiles;
7. Projection-mode gray/dim state for LAYERS / GRID / SURVEY / RETICLE;
8. runtime validation code.

Every launcher line falls into the authorized launcher ECO metadata or standard 7AD loader/error wrapper.

No unexplained line was identified in either implementation file.

## 10. Runtime validation contract

7AD exposes:

`window.GV7AD_VALIDATION`

The browser contract checks:

1. version label is `V-7AD`;
2. exactly five left main-menu rows remain;
3. exactly five right Projection rows remain;
4. right projection labels remain in the approved order;
5. four new right icon tiles remain empty;
6. Mollweide SVG remains present;
7. all left/right long label widths match within `0.50 px`;
8. all left/right icon tiles match and remain square within `0.50 px`;
9. left/right text-to-icon gaps match measured `G`;
10. vertical row gaps match measured `G`;
11. the mathematical width equation reconciles with residual `<= 0.01 px`;
12. long-tile width delta remains within `0.50 px`;
13. square-tile dimension delta remains within `0.50 px`;
14. the rightmost menu tile aligns with the target-button right boundary within `0.50 px`;
15. the right menu begins below the target button rather than overlapping it;
16. inactive left rows are visibly dimmed when Projection mode is open;
17. inactive left rows have no running descendant animations when Projection mode is open;
18. Projection main row remains selected while Projection mode is open;
19. Projection icon retains running inherited animations;
20. Mollweide icon retains running inherited animations;
21. no new inline projection action appears on the four generated right rows;
22. no splash resource is loaded;
23. no duplicate right projection label exists.

A failure throws:

`GV-BETA-0007AD CONTRACT FAILED`

with the measured geometry and failed checks attached to `window.GV7AD_VALIDATION`.

**This runtime contract is embedded and fetch-back verified. It requires an actual browser load for runtime/visual acceptance, so runtime and user visual acceptance remain PENDING rather than being falsely claimed as passed.**

## 11. Acceptance matrix

| Requirement | Status |
|---|---|
| Workflow/log preflight | PASS |
| 7AC baseline fetched/reconfirmed | PASS |
| Viewer direct commit changed-path count = 1 | PASS |
| Launcher direct commit changed-path count = 1 | PASS |
| Viewer line reconciliation | PASS |
| Viewer character reconciliation | PASS |
| Launcher line reconciliation | PASS |
| Launcher character reconciliation | PASS |
| Every implementation line mapped to authorized scope | PASS |
| Mathematical symmetric-width algorithm present | PASS |
| Target right boundary measured at runtime | PASS |
| Same calculated long-tile width applied left/right | PASS BY IMPLEMENTATION; RUNTIME CHECK PENDING |
| Same measured square size applied left/right | PASS BY IMPLEMENTATION; RUNTIME CHECK PENDING |
| Projection-mode inactive-row dimming implemented | PASS BY IMPLEMENTATION; RUNTIME/VISUAL CHECK PENDING |
| Inactive-row pulse suppression implemented | PASS BY IMPLEMENTATION; RUNTIME CHECK PENDING |
| Projection/Mollweide glow code changed | NO |
| Four new projection actions wired | NO |
| Splash loaded/changed | NO |
| Existing approved release modified | NO |
| Runtime browser contract | EMBEDDED — EXECUTION PENDING |
| User visual acceptance | PENDING |

## 12. Explicitly not changed

7AD does **not** modify:

- `viewer/GV-beta-0007AC.py`
- `mobile/beta/7AC.html`
- any prior viewer/launcher release
- splash animation
- artwork
- font files
- coordinate module or coordinate strip
- hamburger
- target/SIMBAD implementation
- Aladin initialization
- galaxy catalog or navigation
- bottom controls
- service worker
- manifests
- workflow YML
- catalogs
- existing ECO documents
- Projection SVG geometry
- Mollweide SVG geometry or measured centering
- inherited Projection/Mollweide glow timing, keyframes, intensity, easing, or phase

## 13. Release launcher

`mobile/beta/7AD.html`

**Runtime acceptance and user visual acceptance remain PENDING until the live 7AD launcher is loaded.**
