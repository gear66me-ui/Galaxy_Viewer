from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-31.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-31-base.py", "exec"))


display(Javascript(r'''
(() => {
  function text(value) {
    return String(value ?? '').trim();
  }

  function coverageSurvey(galaxy) {
    const dec = Number(galaxy?.dec);
    if (Number.isFinite(dec) && dec >= -30) {
      return 'P/PanSTARRS/DR1/color-z-zg-g';
    }
    return 'P/DSS2/color';
  }

  function installViewer32() {
    const root = document.getElementById('viewer14-root');
    if (!root || typeof window.viewer14ShowGalaxy !== 'function') return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-32';

    if (!window.viewer32OriginalShowGalaxy) {
      window.viewer32OriginalShowGalaxy = window.viewer14ShowGalaxy;

      window.viewer14ShowGalaxy = function(galaxy) {
        const g = {...galaxy};
        const isMagic = text(g.catalog).toLowerCase().includes('aladin magic 200');

        if (isMagic) {
          g.survey_id = coverageSurvey(g);
        }

        const result = window.viewer32OriginalShowGalaxy(g);

        if (isMagic) {
          const applyCoverage = () => {
            try {
              const survey = coverageSurvey(g);
              window.viewer14Aladin.setImageSurvey(survey);
              window.viewer14Aladin.gotoRaDec(Number(g.ra), Number(g.dec));
              window.viewer14Aladin.setFoV(Number(g.fov));

              const select = document.getElementById('viewer14SurveySelect');
              if (select) select.value = survey;
              const button = document.getElementById('viewer14SurveyButton');
              if (button) {
                button.textContent = survey === 'P/DSS2/color'
                  ? 'DSS2 Color ▾'
                  : 'Pan-STARRS DR1 Color ▾';
              }
            } catch (_) {}
          };

          applyCoverage();
          setTimeout(applyCoverage, 300);
          setTimeout(applyCoverage, 900);
          setTimeout(applyCoverage, 1800);
          setTimeout(applyCoverage, 3200);
        }

        return result;
      };
    }

    return true;
  }

  installViewer32();
  const timer = setInterval(() => {
    if (installViewer32()) clearInterval(timer);
  }, 120);
  setTimeout(() => {
    installViewer32();
    clearInterval(timer);
  }, 16000);
})();
'''))
