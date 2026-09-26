# Galaxy Viewer JSON-WCS Registration — Proven Gate 2E/2F

Status: experimental path validated visually by the Galaxy Viewer project on the random runtime catalog.

## Frozen working authority

The working image-registration authority is the Galaxy Viewer runtime JSON catalog:

`viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0001.json`

The embedded JPEG AVM/WCS decoder is retained only as a diagnostic comparison path. It is not the preferred runtime authority because embedded metadata can be stale.

## Aladin Lite build used by the successful gates

The successful Gate 1 through Gate 2F pages currently load:

`https://aladin.cds.unistra.fr/AladinLite/api/v3/latest/aladin.js`

and the corresponding `v3/latest` CSS.

Important: this is a moving `latest` endpoint, not a pinned 3.8.1/3.8.2/3.9.x build. Therefore the exact numeric Aladin release is not asserted by this document. Pinning a numeric release must be tested as a separate gate so the known-good behavior is not changed accidentally.

## What changed compared with the older synthetic WCS

The older Galaxy Viewer synthetic WCS represented scale with `CDELT1/CDELT2` plus `CROTA2`.

The passing gate instead constructs a full 2x2 CD matrix from:
- runtime JSON RA and Dec
- runtime JSON `fovXDegrees` and `fovYDegrees`
- runtime JSON `aladinRotation` (fallback `spatialRotationDeg`)
- the actual decoded JPEG pixel width and height

For image width W, height H, FoV X/Y and rotation theta:

```text
sx = fovXDegrees / W
sy = fovYDegrees / H
c  = cos(theta)
s  = sin(theta)

CD1_1 = -sx*c
CD1_2 = -sy*s
CD2_1 = -sx*s
CD2_2 =  sy*c
```

The WCS reference is deliberately centered on the actual fetched JPEG:

```text
CRVAL1 = runtime JSON RA
CRVAL2 = runtime JSON Dec
CRPIX1 = (actualJPEGWidth  + 1) / 2
CRPIX2 = (actualJPEGHeight + 1) / 2
NAXIS1 = actualJPEGWidth
NAXIS2 = actualJPEGHeight
CTYPE1 = RA---TAN
CTYPE2 = DEC--TAN
```

This is the critical difference: the registration does not trust stale JPEG reference dimensions, reference pixels, scale, or embedded rotation. The runtime catalog supplies the sky geometry; the browser supplies the dimensions of the exact JPEG actually being displayed.

## Load sequence

1. Select a runtime JSON record.
2. Fetch its `imageUrl` as a blob.
3. Decode the exact JPEG to obtain its actual width and height.
4. Construct the full CD-matrix WCS above.
5. Create the image with `A.image(..., {wcs: constructedWcs})`.
6. Install it with `aladin.setOverlayImageLayer(...)`.
7. Center Aladin at the JSON RA/Dec.
8. Set initial viewer FoV to `2.5 * max(fovXDegrees, fovYDegrees)`.
9. Set Aladin camera rotation to the JSON rotation.
10. Keep image opacity independent from the DSS/HiPS background.

## Gate controls

- Left vertical control: live Aladin camera rotation.
- Right vertical control: live Aladin field of view.
- Bottom horizontal control: injected JPEG opacity only.
- JSON LOAD: green when the proven JSON path is active.
- WCS DECODE LOAD: diagnostic comparison with embedded JPEG AVM/WCS.
- Gate 2F adds side-by-side metadata panels and downloadable settings.

## Production migration rule

Do not transplant the embedded AVM/WCS decode path into production as image-registration authority.

For the production Galaxy Viewer migration, transplant the proven JSON/CD-matrix path as an isolated change. Preserve navigation, travel choreography, HD banner/view, and unrelated UI behavior. Verify the production result against Gate 2E/2F before deleting or bypassing older WCS code.

## Proven gate files

- `viewer/tests/gate2c.html` — CD-matrix geometry baseline.
- `viewer/tests/gate2d.html` — JSON vs embedded decode.
- `viewer/tests/gate2e.html` — active mode indicator.
- `viewer/tests/gate2f.html` — metadata panels + settings export.
