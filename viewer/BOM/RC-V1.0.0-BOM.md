# Galaxy Viewer RC-V1.0.0 — Production Bill of Materials

Audit scope: production runtime dependency closure rooted at `viewer/releases/launch/Galaxy-Viewer-Launch/index.html` and `viewer/RC-V1.0.0.py` on branch `release`.

Policy: allowlist only. Production-controlled runtime code, data, artwork, fonts, launch assets and browser chrome must exist on `release` or be pinned to an immutable repository commit. No production runtime dependency may point to another repository branch. Labs, demos, archives, historical browser builds and temporary engineering files are excluded.

## 1. Production entry chain

- `viewer/releases/launch/Galaxy-Viewer-Launch/index.html` — hosted launcher.
- `viewer/gv-current-viewer.json` — selects `RC-V1.0.0.py`, build **0053**.
- `viewer/RC-V1.0.0.py` — main runtime, 1,670 physical lines / 105,906 characters in the audited release file.
- `viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/` — frozen final splash package.

The launcher reads the release pointer and release viewer directly from `raw.githubusercontent.com/.../Galaxy_Viewer/release/viewer/`.

## 2. Native host contract

The currently proven native behavior is **APK-0008**.

- AndroidX WebKit support library: **1.12.1**
- Browser user-agent identity: `GalaxyViewerWebBrowser/0057`
- Landing-only provider prewarm
- explicit prewarm loading/ready/failed state
- provider cookie persistence
- fast provider handoff
- browser-shell state resynchronization after hosted chrome reload
- no embedded viewer payload
- no embedded browser HTML/config payload

The production AAB has not yet been built. Its target package is `com.gear66me.galaxyviewer`; it must preserve the APK-0008 native behavior.

## 3. Hosted browser

- `viewer/Web-Browser/web-browser-current.json` — active browser pointer, version **0026**
- `viewer/Web-Browser/Web-Browser-0026/config.json`
- `viewer/Web-Browser/Web-Browser-0026/top.html`
- `viewer/Web-Browser/Web-Browser-0026/bottom.html`

Browser-relative assets are present on release:
- `viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg`
- `viewer/artwork/Fonts/Space Age Regular GV-9/Space Age GV-9A.otf`
- provider artwork under `viewer/artwork/`

## 4. Runtime modules loaded by RC-V1.0.0.py

- `viewer/modules/hamburger-menu/gv-hamburger-menu-0011.js`
- `viewer/modules/coordinate-overlay/gv-coordinate-overlay-0006.js`
- `viewer/modules/target-simbad/gv-target-simbad-0005.js`
- `viewer/modules/galaxy-route-engine/gv-galaxy-route-engine-002.js`
- `viewer/modules/galaxy-navigator/gv-galaxy-navigator-001.js`
- `viewer/modules/hud/gv-heads-up-display-0001.js`
- `viewer/modules/random-galaxy/gv-random-travel-presentation.js`
- `viewer/modules/destination-presentation/gv-destination-presentation-0017.js`
- `viewer/modules/about/gv-about-presentation-0013.js`

The running RC pins these modules and Aladin assets through immutable jsDelivr commit:
`9f4e06549d0918acac8d21bc1a8695aee3611a74`.

## 5. Astronomy engine / vendor

- `aladin-source-clone/src/css/aladin.css`
- `viewer/vendor/aladin-lite/3.8.2/aladin.js`

Both files are present on release; the live RC references the immutable commit above.

## 6. Runtime catalogs

- `viewer/image-databases/master-database/gv-master-catalog.json`
- `viewer/image-databases/master-database/avm-metadata/gv-avm-runtime-catalog-0001.json`
- `viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0035-ESA-FOV.json`
- `viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0007-AVM-ESA-FOV.json`
- `viewer/image-databases/ESO/databases/gv-eso-galaxies-full-0001.json`
- `viewer/image-databases/Chandra/databases/gv-chandra-galaxies-full-0007.json`
- `viewer/image-databases/Spitzer/databases/gv-spitzer-galaxies-full-0011.json`
- `viewer/image-databases/NoirLab/databases/gv-noirlab-galaxies-full-0001.json`

The AVM runtime catalog metadata now identifies `release` as its source branch and points its source master catalog to the release URL.

## 7. Fonts

- `viewer/artwork/Fonts/Space Age Regular/Space Age Regular.otf`
- `viewer/artwork/Fonts/Space Age Regular GV-9/Space Age GV-9A.otf`
- `viewer/artwork/Fonts/Space Age Regular GV-9/GV-Coordinate-Digits-0005.otf`
- `viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/Space-Age.otf`

## 8. Navigation / UI artwork

- `viewer/artwork/icon.svg`
- `viewer/artwork/runtime/navigation/galaxy-viewer-target-icon.svg`
- `viewer/artwork/compass/compass.png`
- `viewer/artwork/startup/galaxy-viewer-startup.png`
- `viewer/artwork/app_icon_4.png`

## 9. Provider artwork

- `viewer/artwork/Hubble/Hubble.jpg`
- `viewer/artwork/JWST/JWST.jpeg`
- `viewer/artwork/ESO/ESO.jpg`
- `viewer/artwork/Chandra/Chandra.jpg`
- `viewer/artwork/Spitzer/Spitzer.jpg`
- `viewer/artwork/NoirLabs/NOIRLab.jpg`
- `viewer/artwork/Euclid/Euclid.jpg`
- `viewer/artwork/Herschel/Herschel.jpg`
- `viewer/artwork/GALEX/GALEX.jpg`
- `viewer/artwork/NuSTAR/NuSTAR.jpg`
- `viewer/artwork/NRAO/NRAO.jpg`

## 10. Constellation artwork

- `viewer/artwork/Constellations/*.SVG`

All 88 IAU constellation SVGs present on release are part of the runtime artwork family.

## 11. Frozen final splash

- `viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/index.html`
- `viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/Galaxy-Splash.png`
- `viewer/releases/splash/Galaxy-Viewer-Singularity-FINAL/Space-Age.otf`

## 12. External runtime services

These are intentional external services, not alternate repository branches:

- jsDelivr — immutable commit-pinned repository assets
- raw.githubusercontent.com — release-branch viewer/catalog delivery
- GitHub Pages — release checkout published at `gear66me-ui.github.io/Galaxy_Viewer/`
- `gv-cloudflare-auto-astrometry-curator-0015.gear66me.workers.dev` — image/astrometry proxy
- SIMBAD and provider source websites/images — destination-dependent astronomy/provider services

## 13. Release isolation status

- Launcher present on release: PASS
- Viewer pointer selects RC-V1.0.0 build 0052: PASS
- Browser pointer selects Web-Browser 0026: PASS
- Browser 0026 chrome/config present on release: PASS
- Runtime modules/catalogs/artwork/fonts/splash present on release: PASS
- AVM metadata source branch/catalog corrected to release: PASS
- Production Pages checkout source: release
- Embedded viewer/browser payload in native shell: NONE
- Production AAB: NOT YET BUILT — awaiting device confirmation after release publication

## 14. Excluded from production BOM

- `viewer/archive/**`
- demos and temporary demos
- AVM labs / diagnostics / test pages
- historical browser versions
- old viewer versions and development pointers
- curation sessions and engineering audits
- historical APKs
- temporary build/repair artifacts
