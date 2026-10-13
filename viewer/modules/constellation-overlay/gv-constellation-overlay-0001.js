/* Galaxy Viewer constellation overlay module 0001.
 * Uses published Hipparcos constellation line definitions; no galaxy catalog changes.
 */
(() => {
  "use strict";
  const VERSION = "0001";
  const LINE_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line.csv";
  const STAR_URL = "https://cdn.jsdelivr.net/gh/creativival/hipparcos_planetarium_data_creator@main/data/hip_constellation_line_star.csv";
  const COLOR = "#8EDCFF";
  const WIDTH = 0.25;
  async function csv(url) {
    const r = await fetch(url, { cache: "force-cache" });
    if (!r.ok) throw new Error("CONSTELLATION DATA HTTP " + r.status);
    return r.text();
  }
  function parseStars(text) {
    const map = new Map();
    for (const line of text.split(/\r?\n/)) {
      const c = line.trim().split(",");
      if (c.length < 7) continue;
      const id = Number(c[0]), h = Number(c[1]), m = Number(c[2]), s = Number(c[3]);
      const ds = String(c[4]).trim(), d = Number(ds), dm = Number(c[5]), sec = Number(c[6]);
      if (![id,h,m,s,d,dm,sec].every(Number.isFinite)) continue;
      const ra = (h + m/60 + s/3600) * 15;
      const dec = Math.sign(d || (ds.startsWith("-") ? -1 : 1)) * (Math.abs(d) + dm/60 + sec/3600);
      map.set(id, [ra, dec]);
    }
    return map;
  }
  function parseLines(text) {
    const rows = [];
    for (const line of text.split(/\r?\n/)) {
      const c = line.trim().split(",");
      if (c.length >= 3 && c[0] && Number.isFinite(Number(c[1])) && Number.isFinite(Number(c[2]))) rows.push([c[0], Number(c[1]), Number(c[2])]);
    }
    return rows;
  }
  async function mount(aladin, api = window.GalaxyViewerHamburgerMenu) {
    if (!aladin || typeof aladin.addOverlay !== "function") throw new Error("CONSTELLATIONS: Aladin instance unavailable");
    if (!window.A?.graphicOverlay || !window.A?.polyline) throw new Error("CONSTELLATIONS: Aladin overlay API unavailable");
    const [lineText, starText] = await Promise.all([csv(LINE_URL), csv(STAR_URL)]);
    const stars = parseStars(starText), segments = parseLines(lineText);
    if (stars.size < 100 || segments.length < 100) throw new Error("CONSTELLATIONS: source data failed validation");
    const overlays = new Map();
    for (const [name, a, b] of segments) {
      let entry = overlays.get(name);
      if (!entry) {
        const obj = window.A.graphicOverlay({ color: COLOR, lineWidth: WIDTH });
        aladin.addOverlay(obj);
        entry = { obj, segments: 0 };
        overlays.set(name, entry);
      }
      const p1 = stars.get(a), p2 = stars.get(b);
      if (p1 && p2) { entry.obj.add(window.A.polyline([p1, p2])); entry.segments++; }
    }
    for (const {obj} of overlays.values()) obj.hide();
    let enabled = false;
    function setEnabled(next) {
      enabled = !!next;
      for (const {obj} of overlays.values()) enabled ? obj.show() : obj.hide();
      return enabled;
    }
    const result = Object.freeze({
      VERSION, get enabled() { return enabled; },
      setEnabled,
      toggle() { return setEnabled(!enabled); },
      constellationCount: overlays.size,
      segmentCount: [...overlays.values()].reduce((n, x) => n + x.segments, 0)
    });
    window.GalaxyViewerConstellations = result;
    return result;
  }
  window.GalaxyViewerConstellationOverlay = Object.freeze({ VERSION, mount });
})();
