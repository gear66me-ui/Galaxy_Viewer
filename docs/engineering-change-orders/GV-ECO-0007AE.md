# GALAXY VIEWER ENGINEERING CHANGE ORDER — GV-ECO-0007AE

## Status

- Repository: `gear66me-ui/Galaxy_Viewer`
- Branch: `beta`
- Release: `GV-beta-0007AE`
- Engineering/source audit: **PASS**
- Runtime/browser acceptance: **PENDING**
- User visual acceptance: **PENDING**

## 1. Exact authorized user request

Create a new standalone 7AE release from the exact approved 7AD viewer and launcher without modifying any approved prior release. Make only these application changes:

1. Change the right-side Projection label `ORTHOGRAPHIC` to `ORTHO`.
2. Make all five right-side Projection labels use the same inherited Space Age visual treatment as the approved left-side menu labels by ensuring each right-side label contains exactly one `span.gv-space-age-glyph`.
3. Preserve the right-side labels in this exact order: `MOLLWEIDE`, `SPHERICAL`, `ORTHO`, `TANGENTIAL`, `SINUSOIDAL`.
4. Preserve the existing 12px Space Age button typography, including weight 400, line-height 1.15, letter-spacing .55px, color, and text-shadow.
5. Preserve all 7AD geometry, icon dimensions, spacing, glow, dimming, Projection active state, Mollweide SVG/centering, four empty generated icon tiles, all existing projection actions, coordinates, hamburger, target/SIMBAD, Aladin, galaxy navigation, bottom controls, colors, splash absence, fonts, modules, workflows, service worker, manifests, catalogs, and all unrelated behavior.
6. Update only the runtime version label to `V-7AE`.
7. Expose `window.GV7AE_VALIDATION` and throw `GV-BETA-0007AE CONTRACT FAILED` with diagnostic evidence if the 7AE runtime contract fails.

## 2. Approved baselines and protected scope

### Viewer baseline

- Path: `viewer/GV-beta-0007AD.py`
- Approved creation commit: `19f5a381314e1ebb336f7d25c4df9fdb54163301`
- Git blob SHA fetched during preflight: `471600aa091123791196024c79df948782b728e4`

### Launcher baseline

- Path: `mobile/beta/7AD.html`
- Approved creation commit: `c1adb9e4b9f0634eaf67dc5b99eb87876ad37ea8`
- Git blob SHA fetched during preflight: `aeb90d81dcd5bf1050cb0b5fd1517b85b5d98d38`

### Direct authorized paths

- `viewer/GV-beta-0007AE.py`
- `mobile/beta/7AE.html`
- `docs/engineering-change-orders/GV-ECO-0007AE.md`

### Protected paths

Every pre-existing application/release path is protected, including `viewer/GV-beta-0007AD.py`, `mobile/beta/7AD.html`, every earlier viewer and launcher, splash files, artwork, fonts, coordinate module/strip, hamburger, target/SIMBAD, Aladin initialization, galaxy catalog/navigation, bottom controls, service worker, manifests, workflows, catalogs, and existing ECO documents.

The existing automatic workflow is allowed to update only `docs/GALAXY-VIEWER-CHANGE-CONTROL-LOG.md` as a workflow-generated forensic record.

## 3. Forensic root cause

The defect was not caused by the numeric font size.

The inherited viewer defines `.gv-space-age-glyph` with `display:inline-block` and `transform:scaleY(1.5)`. The inherited left menu creates its label text and then `wrapVisibleText()` replaces visible text nodes with `span.gv-space-age-glyph`, so the approved left-side labels receive the 1.5 vertical glyph transform while the label buttons remain 12px Space Age.

The approved MOLLWEIDE row also retained an explicit `.gv-space-age-glyph` span from the 7U lineage.

In 7AC, the four generated Projection rows were cloned from the MOLLWEIDE row, but the generated label content was then assigned with:

`label.textContent = name`

That assignment removed the cloned glyph span. The resulting state was therefore:

- left menu: 12px Space Age + `scaleY(1.5)` glyph span;
- MOLLWEIDE: 12px Space Age + `scaleY(1.5)` glyph span;
- SPHERICAL / ORTHOGRAPHIC / TANGENTIAL / SINUSOIDAL: 12px Space Age with no glyph span and therefore no `scaleY(1.5)` treatment.

The approved fix is structural, not numeric: restore exactly one `.gv-space-age-glyph` wrapper inside every right-side Projection label and shorten ORTHOGRAPHIC to ORTHO.

## 4. Implemented viewer change

`viewer/GV-beta-0007AE.py` is a new standalone versioned wrapper that loads one immutable viewer baseline only:

`viewer/GV-beta-0007AD.py@19f5a381314e1ebb336f7d25c4df9fdb54163301`

After the five Projection submenu rows exist, 7AE obtains the existing `.gv-projection-option-label` buttons, preserves those button elements, and ensures each contains exactly one direct `span.gv-space-age-glyph` with the approved labels in the exact required order.

MOLLWEIDE is preserved structurally when already correct. The four generated labels have their plain text replaced by the required glyph span. No row is rebuilt or cloned by 7AE. No icon tile is modified. No projection event/action is added. The version label is changed to `V-7AE`.

### Typography result by source contract

- Font family remains Space Age.
- Font size remains 12px; 7AE contains no font-size assignment.
- Font weight remains 400.
- Line-height remains 1.15.
- Letter-spacing remains .55px.
- Existing color and text-shadow are inherited unchanged.
- The global `.gv-space-age-glyph` rule is not modified.
- The inherited `scaleY(1.5)` glyph treatment is restored to all five right-side labels.
- No font file is changed.

## 5. Explicitly unchanged behavior

Source review found no authorized change to or replacement of:

- long-tile width or height;
- square icon width or height;
- inter-column gap;
- vertical row gap;
- grid geometry or CSS geometry;
- icon SVG geometry;
- Mollweide SVG, size, or centering;
- animation keyframes, duration, easing, intensity, or phase;
- Projection/Mollweide glow implementation;
- Projection-mode dimming opacity/filter behavior;
- left-side menu typography or content;
- coordinate code or module;
- hamburger code;
- target/SIMBAD code;
- Aladin code;
- galaxy catalog/navigation;
- bottom controls;
- splash loading;
- font files;
- projection functionality/event handlers.

The 7AE source itself contains zero style-property writes, zero `addEventListener` calls, zero `cloneNode` calls, zero icon-markup assignments, and no font-size assignment.

## 6. Viewer commit forensic accounting

- Path: `viewer/GV-beta-0007AE.py`
- Status: **ADDED**
- Commit SHA: `5e9fa27ed2498211d353053740c535cce865d3b5`
- Git blob SHA: `2576e041d157576d4b8a0a99a0df54090cd9e8c6`
- Parent/baseline commit: `83c6494647fa5163b4a279298e2944b304e7e730`
- Direct commit changed-path count: `1`
- Only direct changed path: `viewer/GV-beta-0007AE.py`
- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `335e802bd457945262cc08472719c94a97ecb784f5bfa052cd089c5b92136c22`
- Bytes: `0` → `12338`
- Lines: `0` → `193`
- Characters: `0` → `12336`
- Inserted lines: `193`
- Deleted lines: `0`
- Inserted characters: `12336`
- Deleted characters: `0`
- Unified diff hunks: `1`
- Inserted blocks: `1`
- Deleted blocks: `0`
- Changed blocks: `1`
- Line reconciliation: `0 + 193 - 0 = 193` — **PASS**
- Character reconciliation: `0 + 12336 - 0 = 12336` — **PASS**
- Fetch-back verification: **PASS**
- GitHub compare, parent → commit: exactly one added path, `193` additions, `0` deletions — **PASS**
- Automatic forensic workflow reconciliation: **PASS**

## 7. Viewer complete line-scope classification

Every source line in the 193-line viewer is assigned to exactly one authorized changed-line category. Blank lines are assigned to the surrounding structural block so no line is unclassified.

| Viewer lines | Authorized category | Purpose |
|---|---|---|
| 1-2 | 2. 7AD baseline loader metadata | IPython display import and loader-block spacing. |
| 3-9 | 1. 7AE ECO/source comments | Release/ECO purpose, authorized scope, and preserved behavior. |
| 10-12 | 2. 7AD baseline loader metadata | JavaScript wrapper and immutable 7AD baseline URL. |
| 13 | 4. Approved Projection label list | Exact five-label list containing the approved `ORTHO` correction. |
| 14 | 8. Runtime validation code | Geometry/measurement tolerance used only by validator checks. |
| 15-27 | 2. 7AD baseline loader metadata | Startup wait, exact 7AD fetch/extraction/execution, root/version element acquisition. |
| 28 | 3. V-7AE version update | Sets runtime label to `V-7AE`. |
| 29-40 | 8. Runtime validation code | Pending validation state and non-mutating measurement/style/transform helpers. |
| 41-51 | 5. Right-side label lookup | Collects inherited left/right rows, labels, and icon elements for patching/validation. |
| 52-66 | 7. Creation/restoration of `span.gv-space-age-glyph` wrappers | Ensures exactly one direct glyph span while preserving an already-correct MOLLWEIDE wrapper. |
| 67-87 | 8. Runtime validation code | Captures inherited pre-patch typography, geometry, element identity, and Mollweide SVG evidence. |
| 88 | 7. Creation/restoration of `span.gv-space-age-glyph` wrappers | Applies the approved five labels through the wrapper-preserving/restoring function. |
| 89-192 | 8. Runtime validation code | Disconnects 7AE observer after patching, validates every contract item, exposes diagnostics, throws the required failure string, and waits for five inherited rows without rebuilding them. |
| 193 | 1. 7AE ECO/source comments | 7AE staged-source marker. |

Authorized category 6, `ORTHOGRAPHIC → ORTHO correction`, has no separate executable line because the correction is encoded inside the single approved label-list line (line 13), which is classified once under category 4 to preserve the one-line/one-category rule. No line is double-counted.

## 8. Implemented launcher change

`mobile/beta/7AE.html` is a new dedicated loader shell. It contains no Galaxy Viewer application logic and loads the exact reviewed viewer commit:

`viewer/GV-beta-0007AE.py@5e9fa27ed2498211d353053740c535cce865d3b5`

The launcher title/loading/error identifiers were updated only for 7AE. It does not load a splash.

## 9. Launcher commit forensic accounting

- Path: `mobile/beta/7AE.html`
- Status: **ADDED**
- Commit SHA: `c26299df1b5b28a5d973ecbe77e37deb9728f415`
- Git blob SHA: `af072de1bc151a842af1979b8739f0ea13c91ee8`
- Parent/baseline commit: `0fce53d54f74af8d6484311e6fa2e0f942700bd0`
- Direct commit changed-path count: `1`
- Only direct changed path: `mobile/beta/7AE.html`
- SHA-256 before: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- SHA-256 after: `81a3b4308f74dabd00e9b4aae1e434ea84ffd06f569e17e8b8f8f9fecb98279f`
- Bytes: `0` → `2899`
- Lines: `0` → `45`
- Characters: `0` → `2892`
- Inserted lines: `45`
- Deleted lines: `0`
- Inserted characters: `2892`
- Deleted characters: `0`
- Unified diff hunks: `1`
- Inserted blocks: `1`
- Deleted blocks: `0`
- Changed blocks: `1`
- Line reconciliation: `0 + 45 - 0 = 45` — **PASS**
- Character reconciliation: `0 + 2892 - 0 = 2892` — **PASS**
- Fetch-back verification: **PASS**
- GitHub compare, parent → commit: exactly one added path, `45` additions, `0` deletions — **PASS**
- Automatic forensic workflow reconciliation: **PASS**

## 10. Runtime validation contract

`window.GV7AE_VALIDATION` is exposed by 7AE. The validator is designed to verify:

1. Version label is `V-7AE`.
2. Exactly five Projection submenu rows exist.
3. Label order is exactly MOLLWEIDE, SPHERICAL, ORTHO, TANGENTIAL, SINUSOIDAL.
4. ORTHOGRAPHIC is absent from the Projection submenu.
5. Every right-side label has exactly one `span.gv-space-age-glyph`.
6. No right-side label has non-whitespace plain text outside that span.
7. Every glyph span computes to the matrix corresponding to `scaleY(1.5)`.
8. Every right-side label button computes to 12px font size.
9. Every right-side label button retains Space Age.
10. Every right-side label button retains .55px letter spacing.
11. Right-label typography button styles remain unchanged from the inherited pre-patch runtime state.
12. Left-side menu label HTML and computed typography remain unchanged.
13. Long-tile and square-tile geometry remain unchanged from the inherited pre-patch runtime state.
14. Projection-mode dimming contract remains present/functional.
15. Projection active state remains retained while open.
16. Projection glow remains running.
17. Mollweide glow remains running.
18. Mollweide SVG remains present and unchanged.
19. Four generated right icon tiles remain empty.
20. Existing row, label-button, and icon-button elements remain the same DOM nodes.
21. 7AE adds no inline projection action.
22. Splash remains unloaded.
23. No duplicate Projection labels exist.

On failure the runtime throws:

`GV-BETA-0007AE CONTRACT FAILED`

The exported diagnostics include failed checks, label names, wrapper counts, computed font sizes, computed transforms, font families, letter spacing, icon-empty states, projection-open state, baseline identity, font-size contract, glyph-transform contract, splash status, and projection-action status.

This ECO does **not** claim that browser/runtime validation has been executed successfully. Runtime/browser acceptance remains **PENDING** until the live launcher is exercised.

## 11. Acceptance matrix

| Requirement | Evidence/status |
|---|---|
| New 7AE viewer created without modifying 7AD | **PASS — source/commit audit** |
| New 7AE launcher created without modifying 7AD launcher | **PASS — source/commit audit** |
| Viewer loads exact 7AD creation commit only | **PASS — source inspection** |
| Launcher loads exact reviewed 7AE viewer commit | **PASS — source inspection** |
| ORTHOGRAPHIC changed to ORTHO in approved 7AE label list | **PASS — source inspection** |
| All five right labels structurally receive exactly one `.gv-space-age-glyph` | **PASS — implementation/source inspection; runtime enforcement present** |
| Numeric font size not increased | **PASS — no 7AE font-size assignment; runtime validator requires computed 12px** |
| Global glyph rule unchanged | **PASS — 7AE contains no CSS override** |
| Font files unchanged | **PASS — release path audit/source scope** |
| Geometry unchanged by 7AE source | **PASS — no 7AE style writes; runtime geometry guard present** |
| Glow implementation unchanged by 7AE source | **PASS — no animation/style writes; runtime running-state guards present** |
| Dimming implementation unchanged by 7AE source | **PASS — no dimming/style writes; runtime guard present** |
| Icons unchanged by 7AE source | **PASS — zero icon-markup assignments; Mollweide SVG guard present** |
| No projection action/event handler added by 7AE | **PASS — zero `addEventListener` calls; runtime inline-action guard present** |
| Viewer one-path commit | **PASS** |
| Launcher one-path commit | **PASS** |
| Viewer line/character forensic reconciliation | **PASS** |
| Launcher line/character forensic reconciliation | **PASS** |
| Browser/runtime contract execution | **PENDING** |
| Live-site behavior | **PENDING** |
| User visual acceptance | **PENDING** |

## 12. Release truthfulness statement

The engineering/source audits above are based on fetched repository source, returned GitHub commit/blob identities, exact GitHub commit comparisons, and the repository's automatic forensic reconciliation entries. No visual-success claim is made. No browser/runtime-success claim is made. No live-site-success claim is made. User visual acceptance remains **PENDING**.
