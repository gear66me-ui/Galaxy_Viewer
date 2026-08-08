# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AA

**Release:** `GV-beta-0007AA`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007Z.py`  
**Status:** IMPLEMENTED — FETCH-BACK REVIEW PASS; USER VISUAL ACCEPTANCE PENDING

## 1. User request

1. Do not load or modify the splash animation in this release.
2. Correct the current icon errors only.
3. Center the approved Mollweide icon methodically rather than by a guessed translation.
4. Preserve the approved Mollweide `0003` geometry and 24×24 viewer size.
5. Make the inside of both Projection and Mollweide square icon tiles visibly glow.
6. Make the Projection and Mollweide SVG drawings glow with exactly the same timing, easing, intensity pattern, start, end and phase.
7. Preserve Projection geometry, Mollweide geometry, menu layout, text, coordinate strip, target/SIMBAD, galaxy navigation and every unrelated behavior.
8. Fetch the change-control workflow and log before execution; commit; fetch back; account for every touched file; only then create this ECO.

## 2. Change-control preflight

Before implementation, the following were fetched from `beta`:

- `.github/workflows/automatic-change-control-log.yml`
- `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md`

The active workflow requires complete per-file forensic accounting and exact line/character reconciliation for changed text files.

## 3. Authorized paths

Implementation:

- `viewer/GV-beta-0007AA.py`
- `mobile/beta/7AA.html`

Post-review record:

- `docs/engineering-change-orders/GV-ECO-0007AA.md`

No previous viewer release was modified.

## 4. Implementation

### 4.1 Mollweide centering

No fixed hand-tuned X/Y offset is used.

`centerMollweide()`:

1. resets the 7AA transform to `none`;
2. obtains the actual rendered tile rectangle;
3. obtains the actual rendered SVG rectangle;
4. obtains the painted SVG geometry bounds with `getBBox()`;
5. maps the painted bounds through the SVG viewBox into rendered pixels;
6. calculates `dx` and `dy` from the painted center to the 36×36 tile center;
7. applies exactly that calculated translation;
8. remeasures after translation.

The runtime contract requires residual X and Y centering error to each be below `0.40px`.

The inherited `transform:none!important` rule is overridden through the dedicated CSS variable:

`--gv-7aa-center-transform`

so the calculated correction is not silently suppressed.

### 4.2 Mollweide geometry and size

7AA does not replace the Mollweide SVG. It inherits the approved `0003` geometry from the 7Z/7Y baseline and preserves the viewer size at `24×24px`.

The runtime contract checks representative approved geometry markers including `rx="25.5" ry="16.5"`, `M11 32H53`, and the approved outer longitude path.

### 4.3 Explicit interior tile glow

7AA disables the inherited pseudo-element glow path and inserts a real child layer named:

`gv-7aa-inset`

inside each square icon tile. This layer is absolutely positioned at `inset:1px`, remains inside the tile, and carries inset-only shadows. No exterior halo is introduced by 7AA.

### 4.4 Identical synchronized glow

Projection and Mollweide both use the same interior animation:

`gv-7aa-innerPulse`

and the same SVG animation:

`gv-7aa-iconPulse`

Both use one shared cycle:

`6.4s`

and one shared easing curve:

`cubic-bezier(.42,0,.18,1)`

When Mollweide appears, the active animation class is removed from both controls, one layout flush is forced, then the same class is applied to both in the same execution step. This restarts both controls on the same phase.

Projection still starts independently before the submenu exists.

### 4.5 Splash isolation

7AA does not reference, load, modify, or launch a splash animation. The dedicated launcher loads only `GV-beta-0007AA.py`.

## 5. Implementation commits and fetch-back evidence

### Viewer

Commit:

`f7143014f4b6f56668dbcf0665d6bf845890be29`

Fetched blob SHA:

`5e71d6ae87e4dfb886f0260f6cbdbc6d63dfd78f`

Direct commit comparison to its parent reports exactly one path:

- `viewer/GV-beta-0007AA.py` — ADDED — 219 additions, 0 deletions.

### Launcher

Commit:

`ba95dd0e62322c2b16938422332c5c2db1dba7b2`

Fetched blob SHA:

`014c874f45fc88a6094fa723bc5f82c0c9f6ca9e`

Direct commit comparison to its parent reports exactly one path:

- `mobile/beta/7AA.html` — ADDED — 45 additions, 0 deletions.

## 6. Fetch-back review

Verified in committed viewer source:

- exact user request is preserved in source comments;
- 7Z is the baseline;
- no splash URL or splash loader is introduced;
- approved Mollweide SVG is not replaced;
- Mollweide remains 24×24px;
- centering is calculated from measured painted geometry;
- residual centering is runtime-validated below 0.40px per axis;
- both controls receive explicit `.gv-7aa-inset` child layers;
- both interior layers use the same animation name and duration;
- both SVGs use the same animation name and duration;
- both controls restart together when both are visible.

Verified in committed launcher:

- it loads viewer commit `f7143014f4b6f56668dbcf0665d6bf845890be29`;
- it does not load a splash animation;
- it contains no application logic outside the standard loader/error contract.

## 7. Runtime proof

`GV-beta-0007AA.py` exposes `window.GV7AA_VALIDATION`.

The validator checks:

- Projection explicit inset layer exists;
- Projection interior uses `gv-7aa-innerPulse` for `6.4s`;
- Projection SVG uses `gv-7aa-iconPulse` for `6.4s`;
- when Mollweide exists, its explicit inset and SVG use those exact same animation names and durations;
- Mollweide renders at 24×24px;
- Mollweide measured painted center is within 0.40px of the tile center on both axes;
- approved 0003 geometry markers remain present.

If any requirement fails, the viewer throws:

`GV-BETA-0007AA CONTRACT FAILED`

## 8. Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Splash not loaded/modified by 7AA | PASS |
| Mollweide approved geometry preserved | PASS |
| Mollweide size remains 24×24 | PASS |
| Mollweide centered by measured painted bounds | PASS BY IMPLEMENTATION + RUNTIME CONTRACT |
| Projection inside-tile glow uses explicit DOM layer | PASS |
| Mollweide inside-tile glow uses explicit DOM layer | PASS |
| Projection/Mollweide interior animation identical | PASS |
| Projection/Mollweide SVG animation identical | PASS |
| Same 6.4s clock/easing/phase | PASS |
| Projection geometry changed | NO |
| Menu layout changed | NO |
| Coordinates/target/SIMBAD/navigation changed | NO |
| Viewer commit changed paths accounted | PASS — one path |
| Launcher commit changed paths accounted | PASS — one path |
| Fetch-back source review | PASS |
| Fetch-back launcher review | PASS |
| User visual acceptance | PENDING |

## 9. Release launcher

`mobile/beta/7AA.html`
