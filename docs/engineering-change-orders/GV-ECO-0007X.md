# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007X

**Release:** `GV-beta-0007X`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007W.py`  
**Status:** IMPLEMENTED — FETCH-BACK REVIEW PASS; RUNTIME CONTRACT EMBEDDED; USER VISUAL ACCEPTANCE PENDING

## 1. Requested change

The user requested the following exact changes before implementation:

1. Make the **inside edge of both Projection and Mollweide square icon tiles visibly glow** as an inset neon ring/bloom.
2. The glow must be inside the tile, not an animated exterior halo and not merely a faint center haze.
3. Make the actual Projection icon strokes and Mollweide icon strokes glow in exact unison with those inset tile glows.
4. Both controls must share the same start, peak, fade, end, `6.4s` cycle, easing and phase.
5. Move the Mollweide icon drawing visually to the right inside its `36×36` tile so it no longer reads left-flushed.
6. Preserve Mollweide text tile, menu geometry, coordinate strip, target/SIMBAD, galaxy navigation and all unrelated behavior.
7. Implement first, commit, fetch back and review the committed source; only after that review passes, commit this engineering change order.

## 2. Authorized paths

- `viewer/GV-beta-0007X.py`
- `mobile/beta/7X.html`
- `docs/engineering-change-orders/GV-ECO-0007X.md`

No previous viewer release was modified.

## 3. Implementation performed

### 3.1 Inner-edge tile glow

Both Projection and Mollweide tile elements explicitly keep their shell animation disabled:

```css
animation:none!important;
```

Each tile uses the same `::before` layer with `inset:1px` and an inset-only neon ring/bloom. The animated keyframe is:

```css
gv-7x-inner-edge-pulse
```

At peak, the inner edge uses only inset shadows, including a bright inner ring plus deeper inward cyan/blue/violet bloom.

### 3.2 Icon-stroke glow

Both SVG drawings use the same keyframe:

```css
gv-7x-icon-stroke-pulse
```

The glow is applied with `drop-shadow()` to the SVG, so the actual Projection circle/grid/projection strokes and Mollweide ellipse/grid strokes brighten together.

### 3.3 Shared timing and phase

One cycle is used:

```css
--gv-7x-cycle:6.4s
```

Both inner-edge and SVG-stroke animations use:

```css
cubic-bezier(.42,0,.18,1)
```

`synchronize()` removes prior synchronization classes from both controls, forces one layout flush, then adds `gv-7x-sync` to both controls in the same execution step. This restarts both timelines together.

### 3.4 Mollweide rightward optical correction

Only the Mollweide SVG receives:

```css
transform:translateX(2.5px)!important;
```

The Projection SVG remains unshifted.

## 4. Implementation commits

### Viewer commit

`6401bf8015b75a631822cfeba40cde6e7261bc67`

### Launcher commit

`ddfff2374ad8bb5a0aed50f6250b702b673682c9`

## 5. Fetch-back review

The committed `viewer/GV-beta-0007X.py` was fetched back from `beta` after commit.

Fetched viewer blob SHA:

`aaefffb9a03e4bdc87e9735e3c00c1ebe7421941`

Verified in the fetched source:

- The exact user request is embedded at the top of the source.
- Projection tile shell animation is disabled.
- Mollweide tile shell animation is disabled.
- Both tile `::before` layers use `gv-7x-inner-edge-pulse`.
- The inner-edge animation uses inset-only box shadows.
- Both SVG drawings use `gv-7x-icon-stroke-pulse`.
- Both inner-edge animations use `6.4s`.
- Both SVG animations use `6.4s`.
- Both use the same easing curve.
- Both are restarted together by the same synchronization function.
- Mollweide receives an explicit `translateX(2.5px)` rightward optical correction.
- Projection receives no horizontal transform.

## 6. Software/runtime proof

`GV-beta-0007X.py` includes a browser runtime `validate()` contract. Once both controls exist, it checks the computed browser styles and geometry.

It verifies:

- Projection tile animation name = `none`.
- Mollweide tile animation name = `none`.
- Projection `::before` uses `gv-7x-inner-edge-pulse`.
- Mollweide `::before` uses `gv-7x-inner-edge-pulse`.
- Both inner-edge durations = `6.4s`.
- Projection SVG uses `gv-7x-icon-stroke-pulse`.
- Mollweide SVG uses `gv-7x-icon-stroke-pulse`.
- Both stroke-glow durations = `6.4s`.
- Mollweide SVG rendered center is shifted right between `2.0px` and `3.2px` relative to its tile center.

If any check fails, the viewer throws:

```text
GV-BETA-0007X CONTRACT FAILED
```

On success it exposes:

```javascript
window.GV7X_VALIDATION = {
  passed: true,
  checks: { ... },
  cycle: "6.4s",
  phase: "simultaneous-class-activation",
  mollweideVisualOffsetPx: 2.5
}
```

## 7. Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Projection inside-edge tile glow | PASS — inset-only `::before` pulse |
| Mollweide inside-edge tile glow | PASS — inset-only `::before` pulse |
| No animated exterior halo | PASS — tile shell animation disabled |
| Projection drawing glows | PASS — shared SVG stroke keyframe |
| Mollweide drawing glows | PASS — shared SVG stroke keyframe |
| Same 6.4s cycle | PASS |
| Same easing | PASS |
| Same phase/start | PASS BY IMPLEMENTATION — simultaneous synchronization class activation |
| Mollweide shifted right | PASS BY SOURCE + RUNTIME CONTRACT |
| Unrelated behavior modified | NO — standalone additive 7X release over 7W |
| Fetch-back review | PASS |
| User visual acceptance | PENDING |

## 8. Release launcher

`mobile/beta/7X.html`

The launcher loads the committed `GV-beta-0007X.py` revision and preserves the existing startup/error contract.
