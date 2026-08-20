# ESA Archive Link Health Test

This test uses the existing Galaxy Viewer catalogs only:

- `viewer/image-databases/Hubble/databases/gv-hubble-galaxies-full-0018.json`
- `viewer/image-databases/JWST/databases/gv-jwst-galaxies-full-0002.json`

No additional JSON catalog is created.

Run the GitHub Actions workflow **ESA archive link health test** from the Actions tab. The default test performs **3 cold-cache Chromium loads for every unique ESA/Hubble and ESA/Webb `sourceUrl`** found in those two catalogs.

Each run uses a fresh browser context, disables Chromium cache, blocks service workers, and records HTTP status, DOMContentLoaded time, full load time, settled/network-idle time, failed requests, redirects, DNS/connect/TLS/TTFB timing where available, and iframe/WebView blocking headers (`X-Frame-Options` and CSP `frame-ancestors`).

The workflow writes the official latest report back into this folder:

- `ESA-LINK-HEALTH-LATEST.md` — readable full report for every website
- `ESA-LINK-HEALTH-LATEST.csv` — sortable spreadsheet-style report
- `ESA-LINK-HEALTH-LATEST.html` — visual report with stale/slow/embed-blocked highlighting

Classification:

- **STALE/FAILED** — 404, 410, DNS failure, or no main-document response
- **VERY SLOW** — median full load >= 15 seconds
- **SLOW** — median full load >= 10 seconds
- **MODERATE** — median full load >= 5 seconds
- **FAST** — median full load < 5 seconds
- **EMBED BLOCKED** — response headers indicate the provider page may refuse iframe/WebView embedding even if direct browser navigation succeeds

Re-running the workflow overwrites the official `LATEST` reports with the newest measurements and commits them to branch `beta`.