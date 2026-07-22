from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-27.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-27-base.py", "exec"))


display(Javascript(r'''
(() => {
  let viewer29CurrentGalaxy = null;

  function parseMajorArcmin(value) {
    const text = String(value || '');
    const match = text.match(/([0-9]+(?:\.[0-9]+)?)\s*(?:×|x)/i) || text.match(/([0-9]+(?:\.[0-9]+)?)\s*arcmin/i);
    return match ? Number(match[1]) : NaN;
  }

  function tightMagicFov(galaxy) {
    const majorArcmin = parseMajorArcmin(galaxy?.angular_size);
    if (Number.isFinite(majorArcmin) && majorArcmin > 0) {
      return Math.max(0.018, Math.min(0.650, (majorArcmin / 60) * 1.18));
    }

    const original = Number(galaxy?.fov);
    if (!Number.isFinite(original) || original <= 0) return 0.035;

    if (original >= 1.0) return Math.max(0.250, original * 0.42);
    if (original >= 0.30) return Math.max(0.100, original * 0.40);
    if (original >= 0.10) return Math.max(0.032, original * 0.28);
    return Math.max(0.018, original * 0.62);
  }

  function galaxyText(galaxy) {
    const g = galaxy || viewer29CurrentGalaxy || {};
    const ra = Number(g.ra);
    const dec = Number(g.dec);
    return [
      `Object: ${g.name || 'Unknown galaxy'}`,
      `ICRS coordinates: ${Number.isFinite(ra) ? ra.toFixed(6) : 'unknown'} ${Number.isFinite(dec) ? dec.toFixed(6) : 'unknown'}`,
      `Galaxy age: ${g.age || 'unknown'}`,
      `Morphology: ${g.morphology || 'unknown'}`,
      `Redshift / Distance: ${g.redshift_distance || 'unknown'}`,
      `Physical size: ${g.physical_size || 'unknown'}`,
      `Magnitude: ${g.magnitude || 'unknown'}`,
      `Source catalog: ${g.catalog || 'unknown'}`
    ].join('\n');
  }

  window.viewer29CopyGalaxyInfo = async function() {
    const text = galaxyText();
    try {
      await navigator.clipboard.writeText(text);
    } catch (_) {
      const area = document.createElement('textarea');
      area.value = text;
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }
    const button = document.getElementById('viewer29CopyButton');
    if (button) {
      const original = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = original; }, 1100);
    }
  };

  window.viewer29ChromeSearch = function() {
    const g = viewer29CurrentGalaxy || {};
    const ra = Number(g.ra);
    const dec = Number(g.dec);
    const query = `${g.name || 'galaxy'} galaxy ${Number.isFinite(ra) ? `RA ${ra.toFixed(6)}` : ''} ${Number.isFinite(dec) ? `Dec ${dec.toFixed(6)}` : ''} age redshift distance morphology physical size magnitude`;
    window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, '_blank', 'noopener,noreferrer');
  };

  function installViewer29() {
    const root = document.getElementById('viewer14-root');
    if (!root || typeof window.viewer14ShowGalaxy !== 'function') return false;

    document.getElementById('viewer26MagicWrap')?.remove();
    document.querySelectorAll('.viewer26-magic-wrap').forEach(element => element.remove());

    if (!window.viewer14ShowGalaxy.viewer29Wrapped) {
      const originalShowGalaxy = window.viewer14ShowGalaxy;
      const wrappedShowGalaxy = function(galaxy) {
        const nextGalaxy = galaxy && typeof galaxy === 'object' ? {...galaxy} : galaxy;
        if (nextGalaxy && nextGalaxy.catalog === 'Aladin Magic 200') {
          nextGalaxy.fov = tightMagicFov(nextGalaxy);
        }
        viewer29CurrentGalaxy = nextGalaxy && typeof nextGalaxy === 'object' ? {...nextGalaxy} : viewer29CurrentGalaxy;
        return originalShowGalaxy(nextGalaxy);
      };
      wrappedShowGalaxy.viewer29Wrapped = true;
      window.viewer14ShowGalaxy = wrappedShowGalaxy;
    }

    if (typeof window.viewer14Panel === 'function' && !window.viewer14Panel.viewer29Wrapped) {
      const originalPanel = window.viewer14Panel;
      const wrappedPanel = function(galaxy, survey, fov) {
        viewer29CurrentGalaxy = galaxy && typeof galaxy === 'object' ? {...galaxy} : viewer29CurrentGalaxy;
        let html = originalPanel(galaxy, survey, fov);
        if (typeof html === 'string' && html.includes('fom-title')) {
          const controls = '<span class="viewer29-fom-controls"><button id="viewer29CopyButton" type="button" onclick="viewer29CopyGalaxyInfo()">Copy to Clipboard</button><button id="viewer29ChromeButton" type="button" onclick="viewer29ChromeSearch()">Chrome Search</button></span>';
          html = html.replace(/<div class="fom-title">([^<]*)<\/div>/, '<div class="fom-title"><span>$1</span>' + controls + '</div>');
        }
        return html;
      };
      wrappedPanel.viewer29Wrapped = true;
      window.viewer14Panel = wrappedPanel;
    }

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-29';
    return true;
  }

  const oldStyle = document.getElementById('viewer29-style');
  if (oldStyle) oldStyle.remove();
  const style = document.createElement('style');
  style.id = 'viewer29-style';
  style.textContent = `
    #viewer14Status .fom-title {
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:10px;
      flex-wrap:wrap;
    }
    #viewer14Status .viewer29-fom-controls {
      display:inline-flex;
      gap:7px;
      align-items:center;
    }
    #viewer14Status .viewer29-fom-controls button {
      padding:7px 10px;
      border-radius:7px;
      font-size:13px;
      font-weight:800;
      color:#ffffff;
      cursor:pointer;
    }
    #viewer29CopyButton { background:#159447; }
    #viewer29ChromeButton { background:#0b78b5; }
  `;
  document.head.appendChild(style);

  installViewer29();
  const timer = setInterval(() => {
    if (installViewer29()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installViewer29();
    clearInterval(timer);
  }, 16000);
})();
'''))
