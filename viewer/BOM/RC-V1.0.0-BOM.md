# Galaxy Viewer RC-V1.0.0 — Bill of Materials

Audit scope: production runtime dependency closure rooted at `viewer/RC-V1.0.0.py` on branch `release`.
Policy: allowlist only. This BOM lists runtime-required code, data, artwork and launch assets; labs, demos, archives and temporary engineering files are excluded.

## 1. Production entry points
- viewer/RC-V1.0.0.py — main runtime, 1,294 physical lines / 79,318 bytes
- viewer/gv-current-viewer.json — active pointer to RC-V1.0.0.py, build 0001

## 2. Runtime modules loaded by RC-V1.0.0.py
- viewer/modules/hamburger-menu/gv-hamburger-menu-0009.js — menu/UI
- viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js — coordinate presentation
- viewer/modules/target-simbad/gv-target-simbad-0005.js — SIMBAD target control
- viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js — master-catalog loading, normalization, Monte Carlo route/reserve planning, URL validation/quarantine
- viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js — navigation controller
- viewer/modules/hud/gv-heads-up-display-0001.js — HUD
- viewer/modules/random-galaxy/gv-random-travel-presentation.js — Random/travel presentation
- viewer/modules/destination-presentation/gv-destination-presentation-0017.js — arrival, destination, HD and provider-browser handoff
- viewer/modules/about/gv-about-presentation-0013.js — About presentation

The former monolithic Random Galaxy responsibility is therefore distributed across the main runtime + route engine + navigator + Random/travel presentation + destination presentation. Physical line counts are not a reliable size metric because several modules are densely/minified formatted.

## 3. Astronomy engine / vendor
- aladin-source-clone/src/css/aladin.css
- viewer/vendor/aladin-lite/3.8.2/aladin.js

## 4. Runtime catalogs
- viewer/image-databases/master-database/gv-master-catalog.json — master pointer
- viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0001.json — AVM/WCS runtime metadata
- viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json
- viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json
- viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json
- viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0007.json
- viewer/image-databases/Spitzer/databases/gv-spitzer-galaxies-full-0011.json
- viewer/image-databases/NoirLab/databases/gv-noirlab-galaxies-full-0001.json

The master catalog also contains curation paths. Those are engineering/curation metadata, not loaded by the production route engine and are intentionally not part of the runtime BOM.

## 5. Fonts
- viewer/artwork/Fonts/Space Age Regular/Space Age Regular.otf
- viewer/artwork/Fonts/Space Age Regular GV-9/Space Age GV-9A.otf
- viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0005.otf
- viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/Space-Age.otf

## 6. Navigation / UI artwork
- viewer/artwork/icon.svg
- viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg
- viewer/artwork/compass/compass.png
- viewer/artwork/app_icon_4.png — approved Android launcher source

## 7. Provider artwork
- viewer/artwork/Hubble/Hubble.jpg
- viewer/artwork/JWST/JWST.jpeg
- viewer/artwork/ESO/ESO.jpg
- viewer/artwork/Chandra/Chandra.jpg
- viewer/artwork/Spitzer/Spitzer.jpg
- viewer/artwork/NoirLabs/NOIRLab.jpg
- viewer/artwork/Euclid/Euclid.jpg
- viewer/artwork/Herschel/Herschel.jpg
- viewer/artwork/GALEX/GALEX.jpg
- viewer/artwork/NuSTAR/NuSTAR.jpg
- viewer/artwork/NRAO/NRAO.jpg

Provider artwork is selected dynamically from destination/provider identity, so the provider set is included even where a filename is not a literal in the main Python file.

## 8. Constellation artwork
Required dynamic family:
- viewer/artwork/Constellations/*.SVG

All 88 IAU constellation SVG files present on release are part of the BOM. Destination presentation derives the filename dynamically from the destination constellation (for example ANDROMEDA -> ANDROMEDA.SVG).

## 9. Frozen final splash
- viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html
- viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/Galaxy-Splash.png
- viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/Space-Age.otf

This package is frozen and must be copied/packaged unchanged.

## 10. External runtime services
- jsDelivr GitHub CDN — release-branch JS/CSS/artwork delivery
- raw.githubusercontent.com — release-branch catalogs/artwork delivery
- gv-cloudflare-auto-astrometry-curator-0015.gear66me.workers.dev/api/image — image proxy used by the main runtime
- SIMBAD / provider source URLs — destination-dependent external navigation/data behavior

External galaxy image URLs contained inside provider catalogs are data payload dependencies, not repository files; they are validated at runtime by the route engine.

## 11. Dependency verification result
Repository presence check: PASS for every repository file listed above.
Beta/release content identity: artwork, all 88 constellation SVGs, catalogs, Aladin 3.8.2, final splash, compass and approved app_icon_4 are present on release and match their beta source blobs.
Production modules intentionally use release URLs rather than beta URLs.

Correction to the earlier preliminary check: Space Age GV-9A.otf and compass.png ARE present on release. The earlier “missing” result came from testing percent-encoded URL paths as literal Git repository paths. The decoded repository paths resolve correctly.

## 12. Excluded from production BOM
- viewer/archive/**
- demo/** and demo2/**
- temporary-demos/**
- AVM labs / diagnostics / test pages
- old viewer versions and beta pointers
- curation sessions, selected previews and curation audits
- historical APKs
- temporary build/repair artifacts

## 13. Release gate
BOM repository dependency closure: PASS.
APK build gate: NOT YET PASSING. GitHub Actions run 36637923880 failed in android-actions/setup-android@v3 before APK generation; no RC APK was produced by that run. This build-system failure is separate from the runtime BOM.
