# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007V

**Release:** `GV-beta-0007V`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007U.py`  
**Status:** IMPLEMENTED — SOURCE/FETCH-BACK VALIDATION PASS; RUNTIME CONTRACT EMBEDDED; USER VISUAL ACCEPTANCE PENDING

## User change order

1. The Projection icon tile and Mollweide icon tile must glow on the **inside of the square tile**, not by animating an exterior halo.
2. The Projection icon and Mollweide icon must pulse in exact unison: same start, same end, same cycle, same phase and same timing curve.
3. The pulse must remain slow and tense rather than blink rapidly.
4. The Mollweide preview must be less rounded/"watermelon" shaped and closer to the pointed all-sky Mollweide/CMB-map silhouette.
5. Execute the change, review it, verify the implementation against the request, then commit this engineering change order.
6. Preserve all unrelated Galaxy Viewer behavior.

## Authorized implementation paths

- `viewer/GV-beta-0007V.py`
- `mobile/beta/7V.html`
- `docs/engineering-change-orders/GV-ECO-0007V.md`

No previous viewer release was modified.

## Preserved behavior

- Hamburger menu implementation and behavior.
- Target/SIMBAD implementation and behavior.
- Aladin initialization.
- Coordinate overlay and coordinate font.
- Galaxy catalog and navigation.
- Layers, Grid, Survey and Reticle menu rows.
- Previous viewer releases including 7U.

## Implementation

### Shared interior pulse

`GV-beta-0007V.py` defines one timing source:

```css
--gv-projection-cycle: 6.4s
```

Both the Projection and Mollweide tile elements explicitly disable inherited tile animation:

```css
animation: none !important;
```

The animated illumination is placed on each tile's `::before` pseudo-element and uses radial gradients plus **inset-only** box shadows. The animated pseudo-element uses:

```css
gv-projection-interior-pulse
```

Both icon SVGs use the same:

```css
gv-projection-icon-pulse
```

### Phase synchronization

When both controls exist, 7V removes `gv-pulse-synced` from both controls, forces one layout flush, then applies `gv-pulse-synced` to both controls in the same execution step. This deliberately restarts both CSS animation timelines together rather than relying only on equal durations.

### Mollweide geometry

The Mollweide boundary was changed from a regular rounded ellipse to a custom symmetric Bezier outline with tighter left/right endpoints and broader central curvature. The interior grid remains symmetric around the vertical and horizontal center axes.

## Engineering review

### First review — FAIL / defect caught before ECO approval

The initial 7V implementation added the new interior pseudo-element pulse but inherited 7U's existing `2.6s` animation on the tile element itself. That inherited animation could still animate exterior `box-shadow` and background values.

This violated the change order and the implementation was **not approved**.

### Corrective action

Commit:

`874d5fdb9b38437b11cd96c87cb01df276e53448`

explicitly added `animation:none!important` to both tile elements and both base SVG rules before the synchronized 7V animations are applied.

### Runtime contract

Final viewer commit:

`62a051508e503179dbb52c4b0746b300f9d4643c`

adds `validatePulseContract()`.

When both controls exist it checks computed browser styles and throws a `GV-BETA-0007V PULSE CONTRACT FAILED` error unless all of the following are true:

- Projection tile animation name is `none`.
- Mollweide tile animation name is `none`.
- Both `::before` pseudo-elements use `gv-projection-interior-pulse`.
- Both interior animations have duration `6.4s`.
- Both SVGs use `gv-projection-icon-pulse`.
- Both SVG animations have duration `6.4s`.

On success it exposes:

```javascript
window.GV7V_VALIDATION = {
  passed: true,
  cycle: "6.4s",
  tileAnimation: "none",
  interiorAnimation: "gv-projection-interior-pulse",
  iconAnimation: "gv-projection-icon-pulse",
  phaseReset: "simultaneous-class-activation",
  mollweideGeometry: "pointed-all-sky"
}
```

## Fetch-back verification

The committed `viewer/GV-beta-0007V.py` was fetched back from `beta` after the corrective commit.

Verified in the fetched file:

- Change-order instruction is embedded in source.
- Cycle is `6.4s`.
- Tile elements explicitly set `animation:none!important`.
- Tile animated illumination is on `::before`.
- Animated tile shadows are `inset` only.
- Projection and Mollweide share the same interior animation definition.
- Projection and Mollweide share the same SVG animation definition.
- Synchronization function restarts both classes together.
- Pointed Mollweide SVG geometry is present.
- Runtime computed-style contract is present.

Fetched viewer blob SHA:

`f04b2ce1a1b49b5703689ba355ee2ad04fbdb401`

## Commits

- Initial 7V implementation: `e33bb575b0098b8368a9f0096b5f425545202974`
- Review correction removing inherited outer animation: `874d5fdb9b38437b11cd96c87cb01df276e53448`
- Final runtime-contract viewer revision: `62a051508e503179dbb52c4b0746b300f9d4643c`
- Current 7V launcher revision: `44d20e7f1f21caa4b8ee9228d18dfa184698239d`

## Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Projection tile interior pulses | PASS — implemented on `::before` |
| Mollweide tile interior pulses | PASS — implemented on `::before` |
| No animated exterior tile halo | PASS — inherited tile animation explicitly disabled |
| Projection and Mollweide same cycle | PASS — shared `6.4s` variable |
| Same animation definitions | PASS — shared keyframes |
| Same start/phase | PASS BY IMPLEMENTATION — both classes restarted together |
| Runtime divergence detection | PASS — computed-style contract embedded |
| More pointed Mollweide silhouette | PASS — custom symmetric Bezier outline installed |
| Unrelated viewer behavior modified | NO — 7V is a standalone additive release over 7U |
| User visual acceptance | PENDING |

## Release launcher

`mobile/beta/7V.html`

The launcher loads the final 7V viewer revision and preserves the existing launcher startup/error contract.
