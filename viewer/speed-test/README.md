# Galaxy Viewer Speed Test

> **DIAGNOSTIC ONLY**
>
> Files in this directory are not part of the Galaxy Viewer runtime. Do not import, load, or reference them from production viewer files, mobile launchers, service workers, or permanent launch pages.

## Purpose

This folder contains an isolated browser dashboard for comparing:

- the repository-hosted Aladin bundle; and
- the official CDS-hosted Aladin 3.8.2 bundle.

The dashboard performs two complementary tests:

1. **Worldwide network test** using Globalping probes from ten requested regions. The probes perform TCP ping tests on port 443 against the GitHub Pages and CDS hostnames.
2. **Local full-file browser test** from the device running the dashboard. This downloads the exact JavaScript files with cache-busting parameters and measures total transfer time and throughput.

## Dashboard URL

After GitHub Pages publishes the beta branch content:

`https://gear66me-ui.github.io/Galaxy_Viewer/viewer/speed-test/`

## Files

- `index.html` — visual dashboard.
- `scripts/benchmark.js` — measurement, comparison, rendering, and report-export logic.
- `results/` — reserved for manually committed result files.

## Tested endpoints

Repository clone:

`https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/dist/aladin.js`

Official CDS:

`https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js`

## Locations

The worldwide test requests one probe from each of these countries:

- Colombia
- United States
- France
- Germany
- Brazil
- Japan
- Singapore
- Australia
- China
- South Africa

Probe availability is controlled by Globalping. A requested country may occasionally return no probe or a nearby substitute.

## Result files

After a completed run, the dashboard automatically downloads a JSON report named like:

`speed-test-v0001-results-2026-07-28T19-30-45Z.json`

The browser saves that file to the device download folder. A static GitHub Pages page cannot commit files back into this repository without a GitHub token or an authenticated backend. Result files can be reviewed and manually uploaded to `viewer/speed-test/results/` when permanent repository storage is desired.

## Interpretation

- Global TCP latency identifies regional reachability and connection-delay differences.
- The local browser download measures complete-file delivery from the current device and network.
- Neither test measures Aladin parsing, initialization, WASM loading, survey-tile delivery, or first rendered astronomy frame.
- Do not switch production from CDS to the clone based on a single run. Compare repeated reports and use median values.

## Revision history

### v0001 — 2026-07-28

- Created isolated visual benchmark dashboard.
- Added ten-country Globalping TCP/443 comparison.
- Added three-run local full-file download comparison.
- Added automatic timestamped JSON report download.
- No Galaxy Viewer production files changed.
