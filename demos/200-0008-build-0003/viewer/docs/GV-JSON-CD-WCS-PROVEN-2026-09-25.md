# Galaxy Viewer — Proven JSON/CD-Matrix Image Registration

Date: 2026-09-25
Status: Gate 2E PASS; JSON runtime geometry is the approved experimental baseline.

## Proven result
Gate 2E loads the runtime master JSON record, downloads the selected JPEG, measures the JPEG's actual decoded pixel dimensions, constructs a TAN WCS with a full CD matrix, injects the JPEG with A.image(), and positions the Aladin camera from the same JSON geometry.

The embedded JPEG AVM/WCS decode path is retained only as a diagnostic comparison. It is not the runtime authority because testing showed stale/inconsistent embedded metadata.

## Runtime authority
Catalog:
viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0001.json

Geometry fields:
- ra
- dec
- fovXDegrees (fallback fovDegrees)
- fovYDegrees (fallback fovDegrees)
- aladinRotation (fallback spatialRotationDeg)
- imageUrl

Actual NAXIS1/NAXIS2 are taken from createImageBitmap(blob), not assumed from catalog metadata.

## Exact WCS construction
For image width W, height H, horizontal FoV FX, vertical FoV FY and JSON rotation theta:

sx = FX / W
sy = FY / H
t  = theta * pi / 180

CD1_1 = -sx * cos(t)
CD1_2 = -sy * sin(t)
CD2_1 = -sx * sin(t)
CD2_2 =  sy * cos(t)

WCS:
- NAXIS = 2
- CTYPE1 = RA---TAN
- CTYPE2 = DEC--TAN
- EQUINOX = 2000
- LONPOLE = 180
- CUNIT1/2 = deg
- CRVAL1/2 = JSON ra/dec
- CRPIX1 = (W + 1) / 2
- CRPIX2 = (H + 1) / 2
- CD matrix as above
- NAXIS1 = actual JPEG W
- NAXIS2 = actual JPEG H

This center-pixel rule is deliberate: the JSON RA/Dec is placed at the geometric center of the decoded JPEG.

## Image injection
A.image(objectUrl, {
  imgFormat: "jpeg",
  wcs: constructedWcs,
  opacity: imageOpacity
})

Then:
aladin.setOverlayImageLayer(layer, layerName)
aladin.gotoRaDec(ra, dec)
aladin.setFoV(baseFov)
aladin.setRotation(aladinRotation)

Gate 2E uses baseFov = 2.5 * max(fovXDegrees, fovYDegrees).

## Controls proven in Gate 2E
- ROT: aladin.setRotation(value)
- FoV: baseFov * 2^sliderValue, applied with aladin.setFoV()
- IMAGE opacity: layer.setOpacity(percent / 100)
- Random image defaults back to JSON mode.

## Aladin version
IMPORTANT: Gate 2E does NOT pin 3.8.1, 3.8.2, or 3.9.0. Its HTML loads:
https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js
and the matching latest CSS.

Therefore the exact CDN build served during the successful test must not be claimed as 3.8.x without an independent runtime/version check. The repository's aladin-source-clone/package.json currently declares 3.9.0-beta, but Gate 2E is using the CDS /latest CDN, not that repository clone.

Before production integration, pin the tested Aladin build as a separate controlled gate so this proven WCS algorithm is not mixed with a library-version change.

## Change-control rule
Gate 2E is frozen as the known-good reference. Production integration should transplant the JSON/CD-matrix path without modifying its geometry equations. Embedded AVM decode must not override JSON geometry.

## Diagnostic successors
- Gate 2E: known-good JSON/CD-matrix baseline.
- Gate 2F: adds side-by-side WCS-decoded and JSON-decoded panels, live Aladin telemetry, and downloadable settings; it must not replace Gate 2E until separately tested.
