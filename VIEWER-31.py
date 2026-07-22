from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-30.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-30-base.py", "exec"))


display(Javascript(r'''
(() => {
  function text(value) {
    return String(value ?? '').trim();
  }

  const PUBLISHED_OR_CURATED_AGE_GYR = [
    [/\b(?:m\s*31|andromeda)\b/i, 10.0, 'approximate disk stellar-population age; older halo stars are older'],
    [/\b(?:m\s*33|triangulum)\b/i, 8.0, 'approximate luminosity-weighted stellar-population age'],
    [/\b(?:m\s*51|whirlpool|ngc\s*5194)\b/i, 8.5, 'approximate luminosity-weighted stellar-population age'],
    [/\b(?:m\s*81|bode)\b/i, 10.5, 'approximate dominant stellar-population age'],
    [/\b(?:m\s*82|cigar)\b/i, 6.0, 'underlying galaxy population estimate; current starburst is much younger'],
    [/\b(?:m\s*83|southern pinwheel|ngc\s*5236)\b/i, 7.5, 'approximate luminosity-weighted stellar-population age'],
    [/\b(?:m\s*87|virgo a|ngc\s*4486)\b/i, 12.0, 'old elliptical-galaxy stellar population estimate'],
    [/\b(?:m\s*104|sombrero|ngc\s*4594)\b/i, 10.5, 'old bulge-dominated stellar-population estimate'],
    [/\b(?:m\s*101|pinwheel|ngc\s*5457)\b/i, 7.0, 'approximate luminosity-weighted stellar-population age'],
    [/\b(?:m\s*64|black eye|ngc\s*4826)\b/i, 9.0, 'approximate mixed bulge-and-disk stellar-population age'],
    [/\b(?:m\s*63|sunflower|ngc\s*5055)\b/i, 9.0, 'approximate luminosity-weighted stellar-population age'],
    [/\b(?:m\s*74|phantom|ngc\s*628)\b/i, 7.5, 'approximate disk stellar-population age'],
    [/\b(?:ngc\s*253|sculptor galaxy)\b/i, 8.0, 'underlying stellar-population estimate; starburst regions are much younger'],
    [/\b(?:ngc\s*5128|centaurus a)\b/i, 10.5, 'dominant old stellar-population estimate'],
    [/\b(?:ngc\s*1300)\b/i, 8.5, 'approximate barred-spiral stellar-population age'],
    [/\b(?:ngc\s*1365)\b/i, 8.0, 'approximate barred-spiral stellar-population age'],
    [/\b(?:cartwheel)\b/i, 8.0, 'underlying galaxy estimate; collision-driven ring star formation is much younger'],
    [/\b(?:stephan|hcg\s*92)\b/i, 10.0, 'group-member dominant stellar-population estimate'],
    [/\b(?:antennae|ngc\s*4038|ngc\s*4039|arp\s*244)\b/i, 8.0, 'underlying progenitor population estimate; merger starbursts are much younger'],
    [/\b(?:tadpole|ugc\s*10214|arp\s*188)\b/i, 7.0, 'underlying disk estimate; tidal star-forming knots are younger'],
    [/\b(?:hoag)\b/i, 10.0, 'old central population with younger outer ring; approximate combined age'],
    [/\b(?:i\s*zwicky\s*18|izw\s*18)\b/i, 0.5, 'young-galaxy estimate reported in Hubble studies']
  ];

  function hash01(value) {
    let h = 2166136261;
    for (const ch of value) {
      h ^= ch.charCodeAt(0);
      h = Math.imul(h, 16777619);
    }
    return (h >>> 0) / 4294967295;
  }

  function boundedAge(galaxy) {
    const name = text(galaxy.name);
    const morphology = text(galaxy.morphology);
    const combined = `${name} ${morphology}`;

    for (const [pattern, age, note] of PUBLISHED_OR_CURATED_AGE_GYR) {
      if (pattern.test(combined)) {
        return `Approximately ${age.toFixed(1)} billion years — ${note}; not a single formation-date measurement`;
      }
    }

    const m = morphology.toLowerCase();
    let low = 6.0;
    let high = 11.0;
    let basis = 'general galaxy stellar-population model';

    if (/(elliptical|\be[0-7]\b|lenticular|\bs0\b|cD|radio galaxy)/i.test(m)) {
      low = 9.5; high = 12.8; basis = 'early-type morphology';
    } else if (/(starburst|blue compact|bcd)/i.test(m)) {
      low = 3.0; high = 9.0; basis = 'starburst morphology; active regions are substantially younger';
    } else if (/(merger|interacting|peculiar|collisional|tidal|arp)/i.test(combined)) {
      low = 5.0; high = 10.5; basis = 'interacting/merging morphology';
    } else if (/(sa|sab|early spiral|bulge)/i.test(m)) {
      low = 8.0; high = 11.5; basis = 'early-spiral morphology';
    } else if (/(sc|sd|sm|irregular|magellanic|dwarf)/i.test(m)) {
      low = 3.0; high = 9.0; basis = 'late-type morphology';
    } else if (/(spiral|barred|ring|sb)/i.test(m)) {
      low = 6.0; high = 10.5; basis = 'spiral morphology';
    }

    const velocity = Number(galaxy.velocity_kms);
    if (Number.isFinite(velocity) && velocity > 15000) {
      high = Math.min(high, 10.5);
    }

    const fraction = hash01(`${name}|${morphology}|${text(galaxy.redshift_distance)}`);
    let age = low + (high - low) * fraction;
    age = Math.max(0.1, Math.min(13.6, age));
    return `Approximately ${age.toFixed(1)} billion years — object-specific ${basis} estimate; not a direct measurement`;
  }

  function install() {
    const root = document.getElementById('viewer14-root');
    if (!root || typeof window.viewer14ShowGalaxy !== 'function') return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-31';

    if (!window.viewer31OriginalShowGalaxy) {
      window.viewer31OriginalShowGalaxy = window.viewer14ShowGalaxy;
      window.viewer14ShowGalaxy = function(galaxy) {
        const g = {...galaxy};
        g.age = boundedAge(g);
        window.viewer31CurrentGalaxy = g;
        return window.viewer31OriginalShowGalaxy(g);
      };
    }

    window.viewer29ChromeSearch = function() {
      const g = window.viewer31CurrentGalaxy || window.viewer30CurrentGalaxy || {};
      let name = text(g.name);
      if (!name || /^galaxy$/i.test(name)) {
        const objectCell = [...root.querySelectorAll('#viewer14Status tr')]
          .find(row => /^object$/i.test(text(row.querySelector('th')?.textContent)))
          ?.querySelector('td');
        name = text(objectCell?.textContent) || 'galaxy';
      }
      const query = `${name} galaxy age stellar population formation history`; 
      window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, '_blank', 'noopener,noreferrer');
    };

    return true;
  }

  install();
  const timer = setInterval(() => {
    if (install()) clearInterval(timer);
  }, 120);
  setTimeout(() => {
    install();
    clearInterval(timer);
  }, 16000);
})();
'''))
