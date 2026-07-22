from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-33.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-33-base.py", "exec"))


display(Javascript(r'''
(() => {
  const INDEX = 6;
  const RA = 114.114542;
  const DEC = -69.525183;
  const FOV = 0.095;
  const SURVEY = 'P/DSS2/color';

  function forceNumberSeven() {
    const root = document.getElementById('viewer14-root');
    const select = document.getElementById('viewer27MagicSelect');
    if (!root || !select || !window.viewer14Aladin) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-34';

    const option = select.querySelector(`option[value="${INDEX}"]`);
    if (option) option.textContent = '7. Meathook Galaxy — NGC 2442';

    const apply = () => {
      try {
        document.getElementById('viewer14SurveySelect').value = SURVEY;
        const surveyButton = document.getElementById('viewer14SurveyButton');
        if (surveyButton) surveyButton.textContent = 'DSS2 Color ▾';
        window.viewer14Aladin.setImageSurvey(SURVEY);
        window.viewer14Aladin.gotoRaDec(RA, DEC);
        window.viewer14Aladin.setFoV(FOV);
      } catch (_) {}
    };

    if (!select.dataset.viewer34Installed) {
      const originalChange = select.onchange;
      select.onchange = event => {
        const index = Number(event.target.value);
        if (typeof originalChange === 'function') originalChange.call(select, event);
        if (index === INDEX) {
          apply();
          setTimeout(apply, 250);
          setTimeout(apply, 900);
          setTimeout(apply, 1800);
          setTimeout(apply, 3200);
        }
      };
      select.dataset.viewer34Installed = 'true';
    }

    if (Number(select.value) === INDEX) {
      apply();
      setTimeout(apply, 250);
      setTimeout(apply, 900);
      setTimeout(apply, 1800);
      setTimeout(apply, 3200);
    }
    return true;
  }

  forceNumberSeven();
  const timer = setInterval(() => {
    if (forceNumberSeven()) clearInterval(timer);
  }, 120);
  setTimeout(() => {
    forceNumberSeven();
    clearInterval(timer);
  }, 16000);
})();
'''))
