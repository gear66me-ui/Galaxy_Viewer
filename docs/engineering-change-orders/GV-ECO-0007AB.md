# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AB

**Release:** `GV-beta-0007AB`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007AA.py`  
**Status:** IMPLEMENTED — FETCH-BACK REVIEW PASS; USER VISUAL ACCEPTANCE PENDING

## 1. User request

1. Do not load or modify the splash animation.
2. Fix only the current icon defects.
3. Center the approved Mollweide icon methodically rather than by guessed placement.
4. Preserve the approved Mollweide `0003` geometry and 24×24 size.
5. Make the INSIDE of both Projection and Mollweide square icon tiles visibly glow.
6. Make both icon drawings glow with exactly the same timing, easing, intensity pattern and phase.
7. Do not modify unrelated viewer behavior or geometry.
8. Fetch the change-control workflow and log before execution; commit implementation; fetch it back; account for every touched file; only then create this ECO.

## 2. Change-control preflight

Before implementation the active files were fetched from `beta`:

- `.github/workflows/automatic-change-control-log.yml`
- `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`

The workflow requires complete per-file forensic accounting and exact reconciliation.

## 3. Root cause found

The 7AA correction layer was inserted before portions of the inherited 7Z/7Y style and script chain had fully settled. Later inherited CSS used `!important` rules on the same SVG/tile properties. This allowed the inherited baseline to override or interfere with the new centering/glow treatment even though 7AA's own static source checks passed.

The screenshot supplied after 7AA confirmed two visible failures:

- the supposed interior glow rendered mainly as a thin dark inner outline rather than a luminous breathing tile interior;
- the Mollweide drawing remained visually off-center.

## 4. Authorized paths

Implementation:

- `viewer/GV-beta-0007AB.py`
- `mobile/beta/7AB.html`

Post-review record:

- `docs/engineering-change-orders/GV-ECO-0007AB.md`

No existing viewer, splash, artwork, font, workflow, coordinate module, catalog, manifest, or service-worker file was modified.

## 5. Implementation

### 5.1 Post-baseline enforcement

7AB loads the reviewed 7AA baseline and waits for the inherited runtime/style chain to settle before final icon correction.

The final corrections use inline `!important` layout properties where required, preventing later author stylesheet rules from silently overriding them.

### 5.2 Mollweide measured centering

The Mollweide tile is explicitly enforced as a centered grid.

The approved SVG is explicitly enforced at 24×24px.

The algorithm then:

1. sets the SVG transform to `none !important`;
2. reads the tile rectangle;
3. reads the SVG rectangle;
4. reads the actual painted SVG geometry with `getBBox()`;
5. maps that painted center through the SVG viewBox into rendered pixels;
6. computes the exact X/Y delta from painted center to tile center;
7. applies that exact translation inline with `!important`;
8. remeasures the painted center after translation.

The runtime validator requires the residual error to be less than `0.40px` on each axis.

No hand-tuned X/Y constant is used.

### 5.3 Interior tile glow

7AB no longer relies on inherited CSS pseudo-elements for the visible effect.

Each icon tile receives a real child element:

`gv-7ab-inset`

The layer is positioned inside the tile at `inset:2px` and is clipped by the square tile. Its animation changes both interior background illumination and multiple inset shadows. The peak frame includes a bright inner cyan ring plus cyan/blue/violet bloom extending inward from the tile edges.

No exterior glow is introduced by the 7AB layer.

### 5.4 Shared disciplined timing

7AB uses the Web Animations API instead of competing CSS animation declarations.

Both Projection and Mollweide use the exact same `insetFrames` array for tile-interior glow and the exact same `iconFrames` array for SVG glow.

Shared parameters:

- Duration: `6400ms`
- Easing: `cubic-bezier(.42,0,.18,1)`
- Iterations: infinite
- Fill: both

When both controls exist, all four animations are assigned the same `document.timeline` start time. Therefore both tile interiors and both SVGs use the same start, peak, fade and end phase.

### 5.5 Inherited animation suppression

7AB removes inherited glow classes from the two controlled tiles, cancels inherited animations on the relevant SVG/layer, and sets CSS `animation:none !important` on the final controlled elements. The Web Animations API then supplies the only active 7AB animation effect.

### 5.6 Splash isolation

7AB does not reference, load, or modify a splash animation. The 7AB launcher loads only `GV-beta-0007AB.py`.

## 6. Implementation commits and exact touched paths

### Viewer

Commit: `77f53bed25d8e4245cd0998ae3e0d1ce5f923d96`

Fetched blob SHA: `68d892fde62240d284a71263a2ab796d7e71f758`

Direct commit comparison reports exactly one changed path:

- `viewer/GV-beta-0007AB.py` — ADDED — 206 additions, 0 deletions.

### Launcher

Commit: `0394c13849901fe2567a5292d6583fb81f3d0072`

Fetched blob SHA: `886adb1825153914005903a52edd7af526b95b6a`

Direct commit comparison reports exactly one changed path:

- `mobile/beta/7AB.html` — ADDED — 45 additions, 0 deletions.

## 7. Fetch-back review

Verified in the committed viewer source:

- exact user request is preserved in source comments;
- 7AA is the baseline;
- no splash reference is introduced;
- approved Mollweide SVG is inherited rather than replaced;
- Mollweide size is enforced as 24×24px;
- centering is based on measured painted geometry;
- final transform is applied inline with `!important`;
- interior glow uses a real child layer;
- glow uses Web Animations rather than competing CSS animation precedence;
- both controls use identical keyframe arrays;
- both controls receive the exact same animation start time when paired.

Verified in the committed launcher:

- it loads viewer commit `77f53bed25d8e4245cd0998ae3e0d1ce5f923d96`;
- it does not load a splash animation;
- it contains only the standard viewer loader/error wrapper.

## 8. Runtime proof contract

The viewer exposes `window.GV7AB_VALIDATION`.

It verifies:

- Projection inner layer exists;
- Projection has exactly two owned animations;
- Projection animations are running;
- when Mollweide exists, Mollweide inner layer exists;
- Mollweide has exactly two owned animations;
- Mollweide animations are running;
- Projection and Mollweide animation start times are exactly identical;
- Mollweide renders at 24×24px;
- measured painted center error is below 0.40px per axis;
- approved `0003` geometry markers remain present;
- both icon tiles remain square.

A failed requirement throws `GV-BETA-0007AB CONTRACT FAILED`.

## 9. Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Splash not loaded/modified | PASS |
| Mollweide approved geometry preserved | PASS |
| Mollweide 24×24 size preserved | PASS |
| Mollweide centered from painted bounds | PASS BY IMPLEMENTATION + RUNTIME CONTRACT |
| Final centering protected from inherited `!important` CSS | PASS |
| Projection tile has real interior glow layer | PASS |
| Mollweide tile has real interior glow layer | PASS |
| Interior glow visibly extends inward | PASS BY IMPLEMENTATION; USER VISUAL CHECK PENDING |
| Projection and Mollweide use identical interior keyframes | PASS |
| Projection and Mollweide use identical SVG keyframes | PASS |
| Exact same paired animation start time | PASS BY IMPLEMENTATION + RUNTIME CONTRACT |
| Projection geometry changed | NO |
| Mollweide geometry changed | NO |
| Unrelated viewer code changed | NO |
| Viewer commit touched paths accounted | PASS — one path |
| Launcher commit touched paths accounted | PASS — one path |
| User visual acceptance | PENDING |

## 10. Release launcher

`mobile/beta/7AB.html`
