# GV 12AR-39 Navigation Forensic Audit

## Executive result
- PASS: normal Random Galaxy travel uses the 12AR continuous 17-second choreography: FOV out 0–50%, FOV in 50–100%, translation and rotation 30–70%, seventh-order smootherstep.
- PASS: first Earth departure is 7.5 seconds: first 4 seconds translate + rotate with FOV frozen, then coordinates lock and logarithmic zoom-in completes.
- PASS: destination `aladinRotation` is mandatory, with no zero fallback and no alternate destination orientation source in active travel.
- PASS: `aladinRotation` is checked again at zoom-in boundary and immediately before final rotation commit.
- PASS: final arrival reissues the exact captured `aladinRotation` through `commandSetRotation`.
- PASS: NAV ROT diagnostics is the exact numeric value stored immediately before the same value is passed to `aladin.setRotation(commanded)`.

## Hubble 0031
- Raw entries: 855
- Fully eligible: 855
- Rejections: `{}`

## Byte / character / token-word / line / function tally
| Transition | Old bytes | New bytes | Δ bytes | chars + | chars - | words + | words - | lines + | lines - | funcs + | funcs - |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| navigation 0016 → 0017 | 31952 | 32807 | +855 | 2126 | 1271 | 290 | 194 | 61 | 55 | 2 | 0 |
| worker 0005 → 0006 | 1367 | 1367 | +0 | 6 | 6 | 6 | 6 | 5 | 5 | 0 | 0 |
| viewer 12AR-38 → 12AR-39 | 61945 | 62144 | +199 | 295 | 99 | 68 | 15 | 12 | 11 | 0 | 0 |

### Navigation
- Old SHA-256: `3b40dd99104a1ca367824c67de06fca36884016e8360ba003f189a1cef333864`
- New SHA-256: `4ba703c25188d1ea3ccb8c6d438ac1644f17b9b6e0479dfc0c381b63db7e0ed7`
- Old/new characters: 31948 / 32803 (+855)
- Old/new tokenized words/symbols: 7967 / 8063
- Old/new lines: 1068 / 1074
- Old/new functions: 39 / 41
- Functions added: `['flightNavigationSmootherstep', 'getLastCommandedRotation']`
- Functions deleted: `[]`

### Worker
- Old SHA-256: `8fb36b2ed754256b18c65b5c54819b604b0e02478bab77abfc4d2e883c76c05b`
- New SHA-256: `96385d3edd84a1d9298939ba271620826181942c31e8e23eb7aef829c7f3c297`
- Old/new characters: 1363 / 1363 (+0)
- Old/new tokenized words/symbols: 328 / 328
- Old/new lines: 58 / 58
- Old/new functions: 0 / 0
- Functions added: `[]`
- Functions deleted: `[]`

### Viewer
- Old SHA-256: `059f4a7ec22ba82b50a8fd05d3600c357049e92621277c3e70c2d9d23e2b11bb`
- New SHA-256: `ca724a714e599afa8e9dc89e15cf14b19aecca6f87d5d22021d916e049010265`
- Old/new characters: 61921 / 62117 (+196)
- Old/new tokenized words/symbols: 15093 / 15146
- Old/new lines: 1450 / 1451
- Old/new functions: 38 / 38
- Functions added: `[]`
- Functions deleted: `[]`

## Rotation command sites
- Navigation 0017: `[(1045, 'aladin.setRotation(commanded);')]`
- Random Galaxy 0112: `[]`
- Viewer 12AR-39: `[(764, "if(typeof aladin.setRotation==='function')aladin.setRotation(0);")]`

## Algorithm review
- PASS: old five independent stop/start flight-phase labels are absent.
- PASS: great-circle center translation and FOV interpolation do not alter the rotation target.
- PASS: Random Galaxy does not directly call `setRotation`; Navigation owns active travel rotation.
- PASS: no `orientation`, `orientationDegrees`, or `archiveOrientation` destination field is accepted by `flyViewport` as a travel rotation target.
- PASS: invalid/missing `aladinRotation` aborts travel rather than silently substituting 0.
- PASS: source mutation is checked at zoom-in start and final commit.
- PASS: final rotation command is unconditional after validation and uses the original exact target.

## Static validation
- `node --check gv-navigation-0017.js`: PASS
- `node --check gv-navigation-worker-0006.js`: PASS
- `python -m py_compile GV-beta-0012AR-39.py`: PASS
