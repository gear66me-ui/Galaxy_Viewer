/*
GALAXY VIEWER SPEED TEST — v0001
Created: 2026-07-28
Purpose: Compare the repository-hosted Aladin bundle with the official CDS 3.8.2 bundle.
Scope: Diagnostic only. This script is not part of the Galaxy Viewer runtime.

Design notes:
- Worldwide tests use Globalping TCP ping on port 443 from ten requested countries.
- Local tests download each exact JavaScript file three times with cache-busting.
- A timestamped JSON report is generated and downloaded after a complete run.
- Static GitHub Pages cannot commit generated reports back to the repository.
*/

(() => {
  "use strict";

  const VERSION = "v0001";
  const GLOBALPING_API = "https://api.globalping.io/v1/measurements";
  const ENDPOINTS = {
    github: {
      label: "GitHub clone",
      host: "gear66me-ui.github.io",
      url: "https://gear66me-ui.github.io/Galaxy_Viewer/aladin-source-clone/dist/aladin.js"
    },
    cds: {
      label: "Official CDS",
      host: "aladin.cds.unistra.fr",
      url: "https://aladin.cds.unistra.fr/AladinLite/api/v3/3.8.2/aladin.js"
    }
  };

  const LOCATIONS = [
    { code: "CO", label: "Colombia" },
    { code: "US", label: "United States" },
    { code: "FR", label: "France" },
    { code: "DE", label: "Germany" },
    { code: "BR", label: "Brazil" },
    { code: "JP", label: "Japan" },
    { code: "SG", label: "Singapore" },
    { code: "AU", label: "Australia" },
    { code: "CN", label: "China" },
    { code: "ZA", label: "South Africa" }
  ];

  const ui = {
    run: document.getElementById("run-all"),
    download: document.getElementById("download-report"),
    clear: document.getElementById("clear-results"),
    status: document.getElementById("status"),
    githubUrl: document.getElementById("github-url"),
    cdsUrl: document.getElementById("cds-url"),
    localBody: document.getElementById("local-body"),
    globalBody: document.getElementById("global-body"),
    metricLocations: document.getElementById("metric-locations"),
    metricGithubGlobal: document.getElementById("metric-github-global"),
    metricCdsGlobal: document.getElementById("metric-cds-global"),
    metricLocalWinner: document.getElementById("metric-local-winner"),
    githubBar: document.getElementById("github-bar"),
    cdsBar: document.getElementById("cds-bar"),
    githubLocal: document.getElementById("github-local"),
    cdsLocal: document.getElementById("cds-local"),
    reportName: document.getElementById("report-name"),
    measurementIds: document.getElementById("measurement-ids")
  };

  let latestReport = null;
  let latestFilename = null;

  ui.githubUrl.textContent = ENDPOINTS.github.url;
  ui.cdsUrl.textContent = ENDPOINTS.cds.url;

  function setStatus(message, type = "") {
    ui.status.textContent = message;
    ui.status.className = `status ${type}`.trim();
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  function median(values) {
    const valid = values.filter(Number.isFinite).sort((a, b) => a - b);
    if (!valid.length) return null;
    const middle = Math.floor(valid.length / 2);
    return valid.length % 2 ? valid[middle] : (valid[middle - 1] + valid[middle]) / 2;
  }

  function formatMs(value) {
    return Number.isFinite(value) ? `${value.toFixed(1)} ms` : "—";
  }

  function formatBytes(value) {
    if (!Number.isFinite(value)) return "—";
    if (value >= 1024 * 1024) return `${(value / (1024 * 1024)).toFixed(2)} MB`;
    if (value >= 1024) return `${(value / 1024).toFixed(1)} KB`;
    return `${value} B`;
  }

  function formatMbps(value) {
    return Number.isFinite(value) ? `${value.toFixed(2)} Mbps` : "—";
  }

  function safeText(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    })[character]);
  }

  function timestampForFilename(date = new Date()) {
    return date.toISOString().replace(/\.\d{3}Z$/, "Z").replace(/:/g, "-");
  }

  async function downloadOnce(endpointKey, runNumber) {
    const endpoint = ENDPOINTS[endpointKey];
    const cacheBuster = `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    const separator = endpoint.url.includes("?") ? "&" : "?";
    const url = `${endpoint.url}${separator}speedtest=${cacheBuster}`;
    const startedAt = performance.now();

    try {
      const response = await fetch(url, {
        method: "GET",
        mode: "cors",
        cache: "no-store",
        redirect: "follow"
      });
      const buffer = await response.arrayBuffer();
      const endedAt = performance.now();
      const totalMs = endedAt - startedAt;
      const bytes = buffer.byteLength;
      const throughputMbps = totalMs > 0 ? (bytes * 8) / (totalMs / 1000) / 1_000_000 : null;

      return {
        endpoint: endpointKey,
        label: endpoint.label,
        run: runNumber,
        ok: response.ok,
        status: response.status,
        statusText: response.statusText,
        bytes,
        totalMs,
        throughputMbps,
        finalUrl: response.url,
        error: null
      };
    } catch (error) {
      return {
        endpoint: endpointKey,
        label: endpoint.label,
        run: runNumber,
        ok: false,
        status: null,
        statusText: "Fetch failed",
        bytes: null,
        totalMs: performance.now() - startedAt,
        throughputMbps: null,
        finalUrl: url,
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }

  async function runLocalTests() {
    const results = [];
    ui.localBody.innerHTML = "";

    for (const endpointKey of ["github", "cds"]) {
      for (let run = 1; run <= 3; run += 1) {
        setStatus(`Local download: ${ENDPOINTS[endpointKey].label}, run ${run} of 3…`);
        const result = await downloadOnce(endpointKey, run);
        results.push(result);
        renderLocalRow(result);
        await sleep(250);
      }
    }

    renderLocalSummary(results);
    return results;
  }

  function renderLocalRow(result) {
    const row = document.createElement("tr");
    const statusClass = result.ok ? "good" : "bad";
    const statusText = result.ok ? `${result.status} OK` : (result.error || result.statusText || "Failed");
    row.innerHTML = `
      <td>${safeText(result.label)}</td>
      <td>${result.run}</td>
      <td class="${statusClass}">${safeText(statusText)}</td>
      <td>${formatBytes(result.bytes)}</td>
      <td>${formatMs(result.totalMs)}</td>
      <td>${formatMbps(result.throughputMbps)}</td>
    `;
    ui.localBody.appendChild(row);
  }

  function renderLocalSummary(results) {
    const githubMedian = median(results.filter(item => item.endpoint === "github" && item.ok).map(item => item.totalMs));
    const cdsMedian = median(results.filter(item => item.endpoint === "cds" && item.ok).map(item => item.totalMs));
    ui.githubLocal.textContent = formatMs(githubMedian);
    ui.cdsLocal.textContent = formatMs(cdsMedian);

    const max = Math.max(githubMedian || 0, cdsMedian || 0, 1);
    ui.githubBar.style.width = githubMedian ? `${Math.max(3, (githubMedian / max) * 100)}%` : "0";
    ui.cdsBar.style.width = cdsMedian ? `${Math.max(3, (cdsMedian / max) * 100)}%` : "0";

    let winner = "No valid comparison";
    if (Number.isFinite(githubMedian) && Number.isFinite(cdsMedian)) {
      if (Math.abs(githubMedian - cdsMedian) < 1) winner = "Tie";
      else winner = githubMedian < cdsMedian ? "GitHub" : "CDS";
    } else if (Number.isFinite(githubMedian)) {
      winner = "GitHub only reachable";
    } else if (Number.isFinite(cdsMedian)) {
      winner = "CDS only reachable";
    }
    ui.metricLocalWinner.textContent = winner;
  }

  async function createGlobalMeasurement(endpointKey) {
    const endpoint = ENDPOINTS[endpointKey];
    const body = {
      type: "ping",
      target: endpoint.host,
      locations: LOCATIONS.map(location => ({ country: location.code, limit: 1 })),
      measurementOptions: {
        packets: 3,
        protocol: "TCP",
        port: 443,
        ipVersion: 4
      }
    };

    const response = await fetch(GLOBALPING_API, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Globalping create failed for ${endpoint.label}: HTTP ${response.status} ${text}`);
    }

    return response.json();
  }

  async function pollMeasurement(id) {
    let delay = 1200;
    for (let attempt = 0; attempt < 25; attempt += 1) {
      const response = await fetch(`${GLOBALPING_API}/${encodeURIComponent(id)}`, {
        method: "GET",
        mode: "cors",
        cache: "no-store"
      });
      if (!response.ok) throw new Error(`Globalping result fetch failed: HTTP ${response.status}`);
      const data = await response.json();
      if (data.status && data.status !== "in-progress") return data;
      await sleep(delay);
      delay = Math.min(3500, Math.round(delay * 1.25));
    }
    throw new Error(`Globalping measurement ${id} timed out.`);
  }

  function locationKeyFromProbe(probe) {
    return probe?.location?.country || probe?.location?.countryCode || probe?.country || "Unknown";
  }

  function probeDescription(probe) {
    const location = probe?.location || {};
    const parts = [location.city, location.country, probe?.network].filter(Boolean);
    return parts.join(", ") || probe?.id || "Unknown probe";
  }

  function extractAverageMs(result) {
    const candidates = [
      result?.stats?.avg,
      result?.stats?.average,
      result?.timings?.avg,
      result?.timings?.average,
      result?.timings?.total,
      result?.avg
    ];
    for (const value of candidates) {
      const number = Number(value);
      if (Number.isFinite(number)) return number;
    }
    return null;
  }

  function normalizeGlobalResults(measurement, endpointKey) {
    return (measurement.results || []).map(item => ({
      endpoint: endpointKey,
      requestedCountry: locationKeyFromProbe(item.probe),
      probe: probeDescription(item.probe),
      probeId: item.probe?.id || null,
      averageMs: extractAverageMs(item.result),
      packetLoss: Number(item.result?.stats?.loss ?? item.result?.stats?.packetLoss),
      rawStatus: item.result?.status || null,
      rawOutput: item.result?.rawOutput || null
    }));
  }

  async function runGlobalTests() {
    ui.globalBody.innerHTML = "";
    setStatus("Creating GitHub worldwide measurement…");
    const githubCreated = await createGlobalMeasurement("github");
    setStatus("Creating CDS worldwide measurement…");
    const cdsCreated = await createGlobalMeasurement("cds");

    ui.measurementIds.textContent = `GitHub: ${githubCreated.id || "—"}; CDS: ${cdsCreated.id || "—"}`;

    setStatus("Waiting for GitHub worldwide probes…");
    const githubMeasurement = await pollMeasurement(githubCreated.id);
    setStatus("Waiting for CDS worldwide probes…");
    const cdsMeasurement = await pollMeasurement(cdsCreated.id);

    const github = normalizeGlobalResults(githubMeasurement, "github");
    const cds = normalizeGlobalResults(cdsMeasurement, "cds");
    const combined = renderGlobalComparison(github, cds);

    return {
      ids: { github: githubCreated.id, cds: cdsCreated.id },
      raw: { github: githubMeasurement, cds: cdsMeasurement },
      normalized: { github, cds },
      comparison: combined
    };
  }

  function findByRequestedCountry(results, code) {
    return results.find(item => item.requestedCountry === code) || null;
  }

  function renderGlobalComparison(github, cds) {
    const rows = [];
    const githubValues = [];
    const cdsValues = [];
    let completed = 0;

    for (const location of LOCATIONS) {
      const githubResult = findByRequestedCountry(github, location.code);
      const cdsResult = findByRequestedCountry(cds, location.code);
      const githubMs = githubResult?.averageMs ?? null;
      const cdsMs = cdsResult?.averageMs ?? null;
      if (Number.isFinite(githubMs)) githubValues.push(githubMs);
      if (Number.isFinite(cdsMs)) cdsValues.push(cdsMs);
      if (githubResult || cdsResult) completed += 1;

      let winner = "—";
      let difference = null;
      if (Number.isFinite(githubMs) && Number.isFinite(cdsMs)) {
        difference = githubMs - cdsMs;
        if (Math.abs(difference) < 1) winner = "Tie";
        else winner = difference < 0 ? "GitHub" : "CDS";
      } else if (Number.isFinite(githubMs)) {
        winner = "GitHub only";
      } else if (Number.isFinite(cdsMs)) {
        winner = "CDS only";
      }

      rows.push({ location, githubResult, cdsResult, githubMs, cdsMs, difference, winner });
    }

    ui.globalBody.innerHTML = rows.map(row => {
      const probe = row.githubResult?.probe || row.cdsResult?.probe || "No probe result";
      const differenceText = Number.isFinite(row.difference)
        ? `${row.difference > 0 ? "+" : ""}${row.difference.toFixed(1)} ms`
        : "—";
      const winnerClass = row.winner === "GitHub" || row.winner === "CDS" ? "good" : "warn";
      return `
        <tr>
          <td>${safeText(row.location.label)}</td>
          <td>${safeText(probe)}</td>
          <td>${formatMs(row.githubMs)}</td>
          <td>${formatMs(row.cdsMs)}</td>
          <td>${differenceText}</td>
          <td class="${winnerClass}">${safeText(row.winner)}</td>
        </tr>
      `;
    }).join("");

    const githubMedian = median(githubValues);
    const cdsMedian = median(cdsValues);
    ui.metricLocations.textContent = `${completed} / ${LOCATIONS.length}`;
    ui.metricGithubGlobal.textContent = formatMs(githubMedian);
    ui.metricCdsGlobal.textContent = formatMs(cdsMedian);

    return {
      rows,
      completedLocations: completed,
      githubMedianMs: githubMedian,
      cdsMedianMs: cdsMedian
    };
  }

  function buildReport(localResults, globalResults, startedAt, finishedAt) {
    return {
      schema: "galaxy-viewer-speed-test-report",
      version: VERSION,
      startedAt: startedAt.toISOString(),
      finishedAt: finishedAt.toISOString(),
      durationMs: finishedAt.getTime() - startedAt.getTime(),
      userAgent: navigator.userAgent,
      pageUrl: location.href,
      online: navigator.onLine,
      endpoints: ENDPOINTS,
      requestedLocations: LOCATIONS,
      localBrowserTests: localResults,
      worldwideTests: globalResults,
      limitations: [
        "Worldwide tests are TCP ping measurements on port 443, not complete-file throughput measurements.",
        "Local browser tests can be blocked by cross-origin policy even when an endpoint is reachable.",
        "The dashboard does not measure JavaScript parsing, A.init, WASM, survey tiles, SIMBAD, or first rendered frame.",
        "Generated reports download to the device and are not automatically committed to GitHub."
      ]
    };
  }

  function downloadJson(report, filename) {
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function runCompleteTest() {
    ui.run.disabled = true;
    ui.download.disabled = true;
    latestReport = null;
    latestFilename = null;
    const startedAt = new Date();

    try {
      setStatus("Starting complete diagnostic…");
      const localResults = await runLocalTests();

      let globalResults;
      try {
        globalResults = await runGlobalTests();
      } catch (error) {
        globalResults = {
          error: error instanceof Error ? error.message : String(error),
          ids: null,
          raw: null,
          normalized: null,
          comparison: null
        };
        ui.globalBody.innerHTML = `<tr><td colspan="6" class="bad">${safeText(globalResults.error)}</td></tr>`;
        setStatus(`Worldwide test failed: ${globalResults.error}`, "bad");
      }

      const finishedAt = new Date();
      latestReport = buildReport(localResults, globalResults, startedAt, finishedAt);
      latestFilename = `speed-test-${VERSION}-results-${timestampForFilename(finishedAt)}.json`;
      ui.reportName.textContent = latestFilename;
      ui.download.disabled = false;

      downloadJson(latestReport, latestFilename);
      if (!globalResults.error) {
        setStatus(`Complete. Report downloaded as ${latestFilename}.`, "good");
      } else {
        setStatus(`Local test completed; worldwide test failed. Partial report downloaded as ${latestFilename}.`, "warn");
      }
    } catch (error) {
      setStatus(`Test stopped: ${error instanceof Error ? error.message : String(error)}`, "bad");
    } finally {
      ui.run.disabled = false;
    }
  }

  function clearDisplay() {
    ui.localBody.innerHTML = '<tr><td colspan="6">No local test results yet.</td></tr>';
    ui.globalBody.innerHTML = '<tr><td colspan="6">No worldwide test results yet.</td></tr>';
    ui.metricLocations.textContent = `0 / ${LOCATIONS.length}`;
    ui.metricGithubGlobal.textContent = "—";
    ui.metricCdsGlobal.textContent = "—";
    ui.metricLocalWinner.textContent = "—";
    ui.githubLocal.textContent = "—";
    ui.cdsLocal.textContent = "—";
    ui.githubBar.style.width = "0";
    ui.cdsBar.style.width = "0";
    ui.measurementIds.textContent = "—";
    setStatus("Display cleared. Previously downloaded result files remain on your device.");
  }

  ui.run.addEventListener("click", runCompleteTest);
  ui.download.addEventListener("click", () => {
    if (latestReport && latestFilename) downloadJson(latestReport, latestFilename);
  });
  ui.clear.addEventListener("click", clearDisplay);
})();
