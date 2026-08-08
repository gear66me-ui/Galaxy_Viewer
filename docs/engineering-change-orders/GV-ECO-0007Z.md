# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007Z

**Release:** `GV-beta-0007Z`  
**Branch:** `beta`  
**Baseline:** `viewer/GV-beta-0007Y.py`  
**Status:** IMPLEMENTED — FETCH-BACK REVIEW PASS; USER VISUAL ACCEPTANCE PENDING

## 1. Requested change

1. Restore the Mollweide glow behavior to match the approved standalone `mollweide-icon-glow-0003.html` pattern.
2. Make the left Projection icon tile actually glow using that same approved glow treatment.
3. Projection and Mollweide must use one disciplined glow system: same colors, intensity, inset depth, SVG bloom, 6.4-second timing, easing, start/end and phase.
4. Projection must glow even before the Mollweide submenu exists; when Mollweide appears, both controls must restart together in phase.
5. No geometry, size, centering, submenu layout, text, coordinate strip, target/SIMBAD, navigation, or unrelated behavior may change.
6. Implement first, commit, fetch back, review against this request, then commit this ECO proof record only if the review passes.

## 2. Defect found in 7Y

7Y changed the approved prototype glow pattern during viewer integration by using different inset-shadow radii/strength values, and Projection glow activation depended on the pair synchronization path instead of being guaranteed active before Mollweide existed.

That did not satisfy the approved behavior.

## 3. Authorized paths

- `viewer/GV-beta-0007Z.py`
- `mobile/beta/7Z.html`
- `docs/engineering-change-orders/GV-ECO-0007Z.md`

No previous viewer release was modified.

## 4. Implementation performed

### 4.1 One shared disciplined glow system

Both Projection and Mollweide use exactly the same CSS classes and keyframes:

```css
gv-7z-innerPulse
gv-7z-iconPulse
```

Both use:

```css
--gv-7z-cycle:6.4s;
cubic-bezier(.42,0,.18,1)
```

There are no independent colors, staggered delays, alternating palettes, or separate glow strengths between the two controls.

### 4.2 Prototype pattern preservation

The approved standalone prototypes use the same opacity, color and timing pattern. The 7Z inset-shadow spatial radii are proportionally reduced to fit the 36px viewer tiles while preserving the approved relative glow structure.

### 4.3 Projection standalone activation

Projection receives `gv-7z-glow` immediately after its DOM element exists, so its tile interior and SVG strokes pulse even before the Mollweide submenu is opened.

### 4.4 Pair synchronization

When Mollweide appears, 7Z removes previous synchronization classes from both controls, forces one layout flush, then applies `gv-7z-glow` to both controls in the same execution step. This restarts them on the same phase.

### 4.5 No authorized geometry/layout changes

7Z loads 7Y as its baseline and does not replace either Projection or Mollweide SVG geometry. It does not alter Mollweide size, centering, submenu layout, text, coordinates, target/SIMBAD, navigation or unrelated controls.

## 5. Implementation commits

- Viewer commit: `74e533db85b5cea06f58b069b9911fb880a6ecdc`
- Launcher commit: `4fcbabc3ffa70ad84ef152ed08c2339fdb6986d6`

## 6. Fetch-back review

Fetched viewer blob SHA:

`e5536e55880ef765a3631d0ca3a543baedb12c4f`

Fetched launcher blob SHA:

`b66b4ca96b276de11095ac9b0465e7c3253b7547`

Verified in the committed viewer source:

- the exact user request is embedded at the top of the source;
- Projection and Mollweide share one `gv-7z-innerPulse` definition;
- Projection and Mollweide share one `gv-7z-iconPulse` definition;
- both use the same 6.4-second cycle;
- both use the same easing curve;
- Projection starts its glow independently before Mollweide exists;
- when Mollweide exists, both are restarted together;
- no SVG geometry replacement occurs in 7Z;
- no menu-layout or unrelated application selectors are changed.

Verified in the committed launcher:

- it loads viewer commit `74e533db85b5cea06f58b069b9911fb880a6ecdc`;
- no application logic beyond the standard launcher loader/error contract was added.

## 7. Software/runtime proof

`GV-beta-0007Z.py` exposes `window.GV7Z_VALIDATION`.

The runtime validator checks:

- Projection interior animation uses `gv-7z-innerPulse`;
- Projection interior duration is `6.4s`;
- Projection SVG uses `gv-7z-iconPulse`;
- Projection SVG duration is `6.4s`;
- when Mollweide exists, its interior and SVG use those exact same animation names;
- when Mollweide exists, both controls have identical interior durations and identical SVG durations.

If any check fails, 7Z throws:

```text
GV-BETA-0007Z CONTRACT FAILED
```

## 8. Acceptance matrix

| Requirement | Engineering validation |
|---|---|
| Projection glows before submenu | PASS |
| Mollweide approved glow pattern restored | PASS BY SOURCE DESIGN |
| Projection and Mollweide use identical glow CSS | PASS |
| Same colors/intensity/timing/easing | PASS |
| Same phase when both visible | PASS BY IMPLEMENTATION |
| No stagger/Christmas-tree behavior | PASS |
| Projection geometry changed | NO |
| Mollweide geometry changed | NO |
| Mollweide size/centering changed | NO |
| Submenu layout changed | NO |
| Unrelated viewer behavior changed | NO |
| Fetch-back source review | PASS |
| Fetch-back launcher review | PASS |
| User visual acceptance | PENDING |

## 9. Release launcher

`mobile/beta/7Z.html`
