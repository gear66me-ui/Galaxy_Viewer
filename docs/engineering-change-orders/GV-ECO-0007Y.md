# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007Y

**Release:** `GV-beta-0007Y`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007X.py`  
**Status:** IMPLEMENTED — FETCH-BACK REVIEW PASS; RUNTIME CONTRACT EMBEDDED; USER VISUAL ACCEPTANCE PENDING

## 1. Requested change

1. Install the approved standalone Projection glow prototype and approved Mollweide glow 0003 prototype into the viewer.
2. Keep the Projection icon geometry unchanged.
3. Replace the viewer Mollweide icon geometry with the exact approved 0003 geometry: rounded ellipse, denser wireframe, purple grid stopping short of the cyan boundary, 20% smaller, centered.
4. Both Projection and Mollweide square tiles must use the same visible inside-edge inset glow.
5. Both actual SVG drawings must glow on the same synchronized 6.4-second cycle, with the same easing and phase.
6. Preserve the existing Projection/Mollweide submenu layout and all unrelated Galaxy Viewer behavior.
7. Implement and commit first; fetch the committed files back and review them; only after review passes, commit this ECO proof record.

## 2. Authorized paths

- `viewer/GV-beta-0007Y.py`
- `mobile/beta/7Y.html`
- `docs/engineering-change-orders/GV-ECO-0007Y.md`

No previous viewer release was modified.

## 3. Implementation performed

### Projection

The existing approved Projection SVG geometry from the 7X baseline is preserved. 7Y only applies the shared approved glow behavior to its existing 30×30 SVG.

### Mollweide

The embedded Mollweide SVG was corrected during post-commit review to match the approved standalone `mollweide-icon-glow-0003.html` geometry exactly:

- outer ellipse: `cx=32`, `cy=32`, `rx=25.5`, `ry=16.5`;
- horizontal center grid: `M11 32H53`;
- upper/lower curved latitude lines use the approved 0003 paths;
- five internal longitude paths use the approved 0003 paths;
- all purple grid paths terminate inside the cyan ellipse and do not intersect the outer boundary.

In the viewer, Mollweide is rendered at `24×24px`, which is 20% smaller than the prior `30×30px` viewer size, and the 36×36 tile uses `display:grid; place-items:center` with no transform offset.

### Shared glow

Both Projection and Mollweide tile shells explicitly disable tile-element animation. Each uses the same `::before` inset layer with `gv-7y-inner-edge-pulse`. Both SVGs use `gv-7y-icon-stroke-pulse`.

One shared timing source is used:

```css
--gv-7y-cycle: 6.4s
```

Both animations use:

```css
cubic-bezier(.42,0,.18,1)
```

The synchronization function removes prior synchronization classes from both controls, forces one layout flush, and adds `gv-7y-sync` to both controls in the same execution step.

## 4. Review defect caught and corrected

The first 7Y commit did not reproduce the approved 0003 Mollweide geometry exactly. The fetch-back review compared the embedded SVG against `mobile/beta/mollweide-icon-glow-0003.html` and found differences in ellipse radii and grid paths.

That implementation was **not accepted**.

Corrective viewer commit:

`5591d7f1b4669a1c569780efc2e4d11fb56cdce6`

replaced the embedded Mollweide SVG with the exact approved 0003 geometry and added an explicit runtime geometry check.

The launcher was then updated to load the corrected viewer commit:

`e5f38f19a5cd49bb94ce8c4c9ca32dfad4f45685`

## 5. Fetch-back verification

Corrected source blob SHA:

`d5360e9c12783810d1da8a1b27a5084e1221b57e`

Corrected launcher blob SHA:

`b81f17656d9e8581bab68c7235ae3b2850b39171`

Verified in the fetched source:

- the exact requested scope is embedded at the top of the file;
- Projection geometry is not replaced by 7Y;
- Mollweide geometry contains the approved 0003 ellipse radii and exact representative approved paths;
- Mollweide SVG is fixed at `24×24px`;
- Mollweide tile uses grid centering with no transform offset;
- both tile shells have their own animation disabled;
- both tile `::before` layers use `gv-7y-inner-edge-pulse`;
- both SVGs use `gv-7y-icon-stroke-pulse`;
- both animation durations are `6.4s`;
- both animations use the same easing and simultaneous phase restart.

Verified in the fetched launcher:

- it loads corrected viewer commit `5591d7f1b4669a1c569780efc2e4d11fb56cdce6`;
- no application logic beyond the established launcher loader/error contract was added.

## 6. Software/runtime proof

`GV-beta-0007Y.py` exposes `window.GV7Y_VALIDATION` after both controls exist.

The runtime validator checks:

- Projection tile animation name is `none`;
- Mollweide tile animation name is `none`;
- both tile interiors use `gv-7y-inner-edge-pulse`;
- both interior durations are `6.4s`;
- both SVGs use `gv-7y-icon-stroke-pulse`;
- both SVG durations are `6.4s`;
- Mollweide rendered width and height are `24px`;
- Mollweide is centered in its tile within `1.1px` on both axes;
- the rendered Mollweide SVG contains the exact approved 0003 geometry markers.

If any check fails, the viewer throws:

```text
GV-BETA-0007Y CONTRACT FAILED
```

## 7. Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Approved Projection geometry preserved | PASS |
| Exact approved Mollweide 0003 geometry installed | PASS after corrective review |
| Mollweide 20% smaller | PASS — 30px → 24px |
| Mollweide centered | PASS BY SOURCE + RUNTIME CONTRACT |
| Projection inside-edge tile glow | PASS |
| Mollweide inside-edge tile glow | PASS |
| Projection SVG glow | PASS |
| Mollweide SVG glow | PASS |
| Same 6.4s cycle/easing/phase | PASS |
| Existing submenu layout preserved | PASS BY ADDITIVE OVERRIDE DESIGN |
| Unrelated viewer behavior modified | NO — standalone additive 7Y release over 7X |
| Fetch-back source review | PASS |
| Fetch-back launcher review | PASS |
| User visual acceptance | PENDING |

## 8. Release launcher

`mobile/beta/7Y.html`
