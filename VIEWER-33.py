from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-32.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-32-base.py", "exec"))


display(Javascript(r'''
(() => {
  const REPLACEMENT_INDEX = 6;
  const REPLACEMENT = {
    ok: true,
    name: 'Meathook Galaxy — NGC 2442',
    catalog: 'Aladin Magic 200',
    ra: 114.114542,
    dec: -69.525183,
    fov: 0.095,
    survey_id: 'P/DSS2/color',
    morphology: 'Tidally distorted barred spiral galaxy',
    angular_size: '4.7 × 3.1 arcmin',
    redshift_distance: 'Use Get Info for live SIMBAD data',
    velocity_kms: null,
    physical_size: 'Approximately 75,000 light-years — literature estimate',
    magnitude: 'Use Get Info for catalog photometry',
    age: 'Approximately 7.9 billion years — object-specific morphology and activity estimate; not a direct measurement',
    interest_score: 'Aladin Magic 200 curated selection',
    distance_method: 'Use Get Info for catalog method',
    attempts: 1,
    elapsed_seconds: 0,
    source: 'Aladin Magic 200 replacement; NGC 2442 coordinates and framing'
  };

  function showReplacement() {
    if (typeof window.viewer14ShowGalaxy !== 'function') return false;
    window.viewer14ShowGalaxy({...REPLACEMENT});
    const select = document.getElementById('viewer27MagicSelect');
    if (select) select.value = String(REPLACEMENT_INDEX);
    return true;
  }

  function installViewer33() {
    const root = document.getElementById('viewer14-root');
    const select = document.getElementById('viewer27MagicSelect');
    const previous = document.getElementById('viewer27MagicPrevious');
    const next = document.getElementById('viewer27MagicNext');
    if (!root || !select || !previous || !next) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-33';

    const option = select.querySelector(`option[value="${REPLACEMENT_INDEX}"]`);
    if (option) option.textContent = '7. Meathook Galaxy — NGC 2442';

    if (!select.dataset.viewer33Installed) {
      const originalChange = select.onchange;

      const navigate = index => {
        const count = select.options.length;
        const normalized = (Number(index) + count) % count;
        select.value = String(normalized);
        if (normalized === REPLACEMENT_INDEX) {
          showReplacement();
        } else if (typeof originalChange === 'function') {
          originalChange.call(select, {target: select});
        } else {
          select.dispatchEvent(new Event('change', {bubbles: true}));
        }
      };

      select.onchange = event => {
        const index = Number(event.target.value);
        if (index === REPLACEMENT_INDEX) showReplacement();
        else if (typeof originalChange === 'function') originalChange.call(select, event);
      };

      previous.onclick = () => navigate(Number(select.value) - 1);
      next.onclick = () => navigate(Number(select.value) + 1);
      select.dataset.viewer33Installed = 'true';
    }

    if (Number(select.value) === REPLACEMENT_INDEX) showReplacement();
    return true;
  }

  installViewer33();
  const timer = setInterval(() => {
    if (installViewer33()) clearInterval(timer);
  }, 120);
  setTimeout(() => {
    installViewer33();
    clearInterval(timer);
  }, 16000);
})();
'''))
