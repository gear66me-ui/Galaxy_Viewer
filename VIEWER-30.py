from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-29.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-29-base.py", "exec"))


display(Javascript(r'''
(() => {
  function text(value) {
    return String(value ?? '').trim();
  }

  function estimateAge(galaxy) {
    const existing = text(galaxy.age);
    if (existing && !/^not available$/i.test(existing) && !/^estimated 8[–-]12 billion/i.test(existing)) {
      return existing;
    }

    const morphology = text(galaxy.morphology).toLowerCase();
    const name = text(galaxy.name).toLowerCase();
    const combined = `${morphology} ${name}`;

    if (/(starburst|cigar|m\s*82|ngc\s*253|ngc\s*1569|ngc\s*1705|blue compact|bcd)/.test(combined)) {
      return 'Estimated dominant young population: 0.05–2 billion years; older underlying stars may be 8–12 billion years — activity/morphology estimate';
    }
    if (/(merger|interacting|antennae|tadpole|cartwheel|stephan|arp\s|peculiar|collisional|tidal|mouse|mice|medusa)/.test(combined)) {
      return 'Estimated luminosity-weighted population: 1–6 billion years; older component likely 8–12 billion years — interaction-based estimate';
    }
    if (/(elliptical|\be[0-7]\b|lenticular|\bs0\b|radio galaxy)/.test(combined)) {
      return 'Estimated luminosity-weighted stellar age: 9.5–12.5 billion years — early-type morphology estimate';
    }
    if (/(sa\(?[rs]*\)?a|sab|early spiral|sombrero|m\s*104)/.test(combined)) {
      return 'Estimated luminosity-weighted stellar age: 8–11 billion years — early-spiral morphology estimate';
    }
    if (/(sb|barred|ring|grand-design|spiral)/.test(combined)) {
      return 'Estimated luminosity-weighted stellar age: 5–10 billion years — spiral morphology estimate';
    }
    if (/(sc|sd|sm|irregular|magellanic|dwarf)/.test(combined)) {
      return 'Estimated luminosity-weighted stellar age: 2–8 billion years — late-type morphology estimate';
    }
    return 'Estimated luminosity-weighted stellar age: 6–10 billion years — broad galaxy-population estimate';
  }

  function parseMajorArcmin(value) {
    const numbers = text(value).match(/\d+(?:\.\d+)?/g);
    if (!numbers?.length) return null;
    const major = Math.max(...numbers.map(Number).filter(Number.isFinite));
    if (!Number.isFinite(major) || major <= 0) return null;
    if (/arcsec|arcsecond|″/.test(text(value).toLowerCase())) return major / 60;
    return major;
  }

  function tighterMagicFov(galaxy) {
    const majorArcmin = parseMajorArcmin(galaxy.angular_size);
    if (majorArcmin) {
      return Math.max(0.012, Math.min(1.8, (majorArcmin / 60) * 1.18));
    }
    const current = Number(galaxy.fov);
    if (Number.isFinite(current) && current > 0) {
      return Math.max(0.018, Math.min(0.35, current * 0.42));
    }
    return 0.055;
  }

  function reliableMagicSurvey(galaxy) {
    const current = text(galaxy.survey_id);
    const name = text(galaxy.name).toLowerCase();
    const knownOutreach = /(cartwheel|stephan|whirlpool|m51|sombrero|m104|antennae|tadpole|hoag|ngc 1300|ngc 1365|m101|m82|m64|m83|m74|ngc 628|ngc 1566|ngc 7496|ngc 1433|ngc 3351|centaurus a)/.test(name);
    if (knownOutreach && /(?:HST|JWST)\/EPO/.test(current)) return current;
    const dec = Number(galaxy.dec);
    return Number.isFinite(dec) && dec > -30
      ? 'P/PanSTARRS/DR1/color-z-zg-g'
      : 'P/DECaLS/DR5/color';
  }

  function install() {
    const root = document.getElementById('viewer14-root');
    if (!root || typeof window.viewer14ShowGalaxy !== 'function') return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-30';

    if (!window.viewer30OriginalShowGalaxy) {
      window.viewer30OriginalShowGalaxy = window.viewer14ShowGalaxy;
      window.viewer14ShowGalaxy = function(galaxy) {
        const g = {...galaxy};
        g.age = estimateAge(g);

        if (text(g.catalog).toLowerCase().includes('aladin magic 200')) {
          g.fov = tighterMagicFov(g);
          g.survey_id = reliableMagicSurvey(g);
        }

        window.viewer30CurrentGalaxy = g;
        const result = window.viewer30OriginalShowGalaxy(g);

        if (text(g.catalog).toLowerCase().includes('aladin magic 200')) {
          const apply = () => {
            try {
              window.viewer14Aladin.setImageSurvey(g.survey_id);
              window.viewer14Aladin.setFoV(g.fov);
            } catch (_) {}
          };
          apply();
          setTimeout(apply, 250);
          setTimeout(apply, 800);
          setTimeout(apply, 1800);
        }
        return result;
      };
    }

    window.viewer29ChromeSearch = function() {
      const g = window.viewer30CurrentGalaxy || {};
      let name = text(g.name);
      if (!name || /^galaxy$/i.test(name)) {
        const objectCell = [...root.querySelectorAll('#viewer14Status tr')]
          .find(row => /^object$/i.test(text(row.querySelector('th')?.textContent)))
          ?.querySelector('td');
        name = text(objectCell?.textContent) || 'galaxy';
      }
      const query = `${name} galaxy information age distance redshift physical size morphology magnitude`;
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
