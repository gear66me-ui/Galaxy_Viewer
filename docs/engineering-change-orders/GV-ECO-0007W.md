# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007W

**Release:** `GV-beta-0007W`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007V.py`  
**Status:** IMPLEMENTED — FETCH-BACK VALIDATION PASS; RUNTIME CONTRACT EMBEDDED; USER VISUAL ACCEPTANCE PENDING

## 1. Requested change

The user requested the following exact changes before implementation:

1. Move the Mollweide 36×36 icon tile immediately beside the Mollweide text tile, using the same tight gap as the main Projection label/icon pair.
2. Make the actual Projection icon drawing glow: the circle/grid/projection edges must pulse.
3. Make the actual Mollweide ellipse/grid drawing glow at exactly the same time.
4. Make the inside edge/interior of both square icon tiles glow during that same pulse.
5. Projection and Mollweide must share the same start, end, cycle, easing and phase.
6. Use the established slow/tension pulse rather than a fast blink.
7. Do not animate an exterior tile halo; the tile shell/border must remain stable.
8. Keep the current Mollweide geometry in this ECO and center it precisely inside its square tile.
9. Preserve all unrelated Galaxy Viewer behavior.
10. After implementation, fetch the committed files back, verify the request against the committed source, embed software/runtime proof, then commit this ECO record.

## 2. Authorized paths

- `viewer/GV-beta-0007W.py`
- `mobile/beta/7W.html`
- `docs/engineering-change-orders/GV-ECO-0007W.md`

No previous viewer release was modified.

## 3. Preserved behavior

- Hamburger menu implementation and behavior.
- Target/SIMBAD implementation and behavior.
- Aladin initialization.
- Coordinate overlay and coordinate font.
- Galaxy catalog and galaxy navigation.
- Layers, Grid, Survey and Reticle menu rows.
- Previous viewer releases, including 7V.

## 4. Implementation performed

### 4.1 Mollweide tile adjacency

The Mollweide submenu row is explicitly locked to:

```css
grid-template-columns:120px 36px;
column-gap:2px;
width:158px;
```

The label is explicitly `120px × 36px` and the icon tile is explicitly `36px × 36px`. Selectors target the direct button children of the projection-option row so inherited submenu button widths cannot override the square icon tile.

### 4.2 Stable tile shell

Both icon tiles explicitly disable animation on the tile element:

```css
animation:none!important;
```

The tile shell therefore does not run the inherited outer-halo animation.

### 4.3 Interior tile glow

Both square tiles use the same `::before` interior layer and the same animation:

```css
gv-7w-inner-tile-pulse
```

The animated shadows in this keyframe are `inset` only. The glow therefore occurs inside the tile rather than as an animated exterior halo.

### 4.4 Icon-edge glow

Both actual SVG drawings use the same animation:

```css
gv-7w-icon-edge-pulse
```

The animation uses `drop-shadow()` on the SVG, causing the Projection circle/grid/projection strokes and Mollweide ellipse/grid strokes to glow together.

### 4.5 Shared timing and phase

One timing source is used:

```css
--gv-7w-cycle:6.4s
```

Both tile-interior and SVG-edge animations use the same easing:

```css
cubic-bezier(.42,0,.18,1)
```

When both controls exist, `synchronize()` removes the synchronization class from both controls, forces one layout flush, then applies `gv-7w-sync` to both controls in the same execution step. This deliberately restarts their animation timelines together.

### 4.6 Mollweide centering

The Mollweide icon tile is a 36×36 grid container using:

```css
display:grid;
place-items:center;
```

Both icon SVGs are fixed at 30×30 with zero margin and no transform offset.

## 5. Post-commit review

### Source commit

`97bb6d8adb46ebd1c1113a85af1f5ba68d1401b7`

### Launcher commit

`103cdd8d19cd9011cdab8b09ecde9ef2771ee945`

### Fetch-back source blob

`387cdbbe311361c7e9861cf6bc3d3ea9edaf9d1b`

### Fetch-back launcher blob

`f8d3b26ea3891be62bca9d3bdc80e19258ebef39`

The committed source and launcher were fetched back from branch `beta` after their commits.

Verified in the fetched source:

- The user request is embedded at the top of `GV-beta-0007W.py`.
- Projection/Mollweide submenu row is 158 px total.
- Mollweide label is 120 px wide.
- Mollweide icon tile is 36×36.
- The intended gap is 2 px.
- Both tile elements disable their own animation.
- Both tile interiors use `gv-7w-inner-tile-pulse`.
- Both SVG drawings use `gv-7w-icon-edge-pulse`.
- Both use the same 6.4 s cycle.
- Both use the same easing curve.
- Both are restarted in the same synchronization step.
- Mollweide SVG is centered by the square tile layout.

## 6. Software/runtime proof

`GV-beta-0007W.py` includes a browser runtime function `validate()` that evaluates the actual rendered/computed layout and animation contract after both controls exist.

The runtime contract checks:

- projection-option row rendered width = `158px`;
- Mollweide label rendered width = `120px`;
- Mollweide icon tile rendered width/height = `36px × 36px`;
- measured gap between Mollweide label and icon tile = `2px`;
- Projection tile element animation name = `none`;
- Mollweide tile element animation name = `none`;
- both `::before` layers use `gv-7w-inner-tile-pulse`;
- both interior animation durations = `6.4s`;
- both SVGs use `gv-7w-icon-edge-pulse`;
- both SVG animation durations = `6.4s`;
- Mollweide SVG center differs from its tile center by less than `1.1px`.

If any check fails, the viewer throws:

```text
GV-BETA-0007W CONTRACT FAILED
```

On success, the viewer exposes:

```javascript
window.GV7W_VALIDATION = {
  passed: true,
  checks: { ... },
  gap: 2,
  cycle: "6.4s",
  phase: "simultaneous-class-activation"
}
```

This runtime contract is the software proof mechanism for the requested layout and animation behavior. User visual acceptance remains a separate final check.

## 7. Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Mollweide icon directly beside text | PASS BY SOURCE + RUNTIME CONTRACT — 120 + 2 + 36 layout |
| Mollweide tile square | PASS — 36×36 locked |
| Projection drawing edges glow | PASS — shared SVG edge animation applied |
| Mollweide drawing edges glow | PASS — shared SVG edge animation applied |
| Projection tile interior glows | PASS — shared `::before` inset animation |
| Mollweide tile interior glows | PASS — shared `::before` inset animation |
| No animated exterior tile halo | PASS — tile elements set `animation:none` |
| Same start/end/cycle/easing | PASS BY IMPLEMENTATION — shared class/keyframes/6.4s/easing |
| Same phase | PASS BY IMPLEMENTATION — simultaneous class activation |
| Mollweide centered | PASS BY SOURCE + RUNTIME CONTRACT |
| Unrelated behavior changed | NO — standalone additive 7W release over 7V |
| Fetch-back verification | PASS |
| Runtime contract embedded | PASS |
| User visual acceptance | PENDING |

## 8. Release launcher

`mobile/beta/7W.html`

The launcher loads `GV-beta-0007W.py` and preserves the existing startup/error contract.
