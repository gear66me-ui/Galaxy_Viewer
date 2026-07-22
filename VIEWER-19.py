from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/a507fd654d4d4a9075c020d69f91eeb706191d0b/VIEWER-18.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-18-base.py", "exec"))


display(Javascript(r'''
(() => {
  const installLayout = () => {
    const root = document.getElementById('viewer14-root');
    const catalogSelect = document.getElementById('viewer14CatalogMode');
    const catalogWrap = document.getElementById('viewer14CatalogMenuWrap');
    const surveyWrap = root?.querySelector('.survey-menu-wrap');
    const progress = root?.querySelector('.catalog-progress');
    if (!root || !catalogSelect || !catalogWrap || !surveyWrap || !progress) return false;

    const catalogControls = catalogSelect.closest('.controls');
    const surveyControls = surveyWrap.closest('.controls');
    if (!catalogControls || !surveyControls) return false;

    let libraryLabel = [...catalogControls.querySelectorAll('label')].find(label =>
      label.textContent.toLowerCase().includes('random galaxy library') ||
      label.textContent.trim() === 'Library'
    );
    if (libraryLabel) libraryLabel.textContent = 'Library';

    let surveyLabel = [...surveyControls.querySelectorAll('label')].find(label =>
      label.textContent.toLowerCase().includes('displayed survey') ||
      label.textContent.trim() === 'Survey'
    );
    if (surveyLabel) surveyLabel.textContent = 'Survey';

    catalogControls.id = 'viewer19LibrarySurveyRow';
    catalogControls.classList.add('viewer19-library-survey-row');

    if (surveyLabel) catalogControls.appendChild(surveyLabel);
    catalogControls.appendChild(surveyWrap);

    let progressRow = document.getElementById('viewer19ProgressRow');
    if (!progressRow) {
      progressRow = document.createElement('div');
      progressRow.id = 'viewer19ProgressRow';
      progressRow.className = 'controls viewer19-progress-row';
      catalogControls.insertAdjacentElement('afterend', progressRow);
    }
    progressRow.appendChild(progress);

    if (surveyControls !== catalogControls && !surveyControls.children.length) {
      surveyControls.remove();
    }

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-19';
    return true;
  };

  installLayout();
  const layoutTimer = setInterval(() => {
    if (installLayout()) clearInterval(layoutTimer);
  }, 100);
  setTimeout(() => {
    installLayout();
    clearInterval(layoutTimer);
  }, 16000);
})();
'''))


display(Javascript(r'''
(() => {
  const style = document.createElement('style');
  style.textContent = `
    #viewer14-root .viewer19-library-survey-row {
      display: flex;
      align-items: center;
      gap: 9px;
      flex-wrap: nowrap;
      width: 100%;
    }
    #viewer14-root .viewer19-library-survey-row label {
      flex: 0 0 auto;
      white-space: nowrap;
    }
    #viewer14-root .viewer19-library-survey-row #viewer14CatalogMenuWrap {
      flex: 1 1 0;
      min-width: 220px !important;
      max-width: none;
    }
    #viewer14-root .viewer19-library-survey-row .survey-menu-wrap {
      flex: 1 1 0;
      min-width: 210px;
      max-width: none;
    }
    #viewer14-root .viewer19-progress-row {
      width: 100%;
    }
    #viewer14-root .viewer19-progress-row .catalog-progress {
      flex: 1 1 100%;
      width: 100%;
      min-width: 0;
      max-width: none;
    }
    @media (max-width: 720px) {
      #viewer14-root .viewer19-library-survey-row {
        gap: 6px;
      }
      #viewer14-root .viewer19-library-survey-row #viewer14CatalogMenuWrap,
      #viewer14-root .viewer19-library-survey-row .survey-menu-wrap {
        min-width: 0 !important;
      }
    }
  `;
  document.head.appendChild(style);
})();
'''))


display(Javascript(r'''
(() => {
  const installGetInfo = () => {
    if (!window.viewer14Aladin || typeof window.viewer14Panel !== 'function') return false;

    window.viewer14GetInfo = async function() {
      const button = document.getElementById('viewer14InfoButton');
      const parts = document.getElementById('viewer14CoordBox').value.trim().split(/\s+/).map(Number);
      if (parts.length < 2 || !Number.isFinite(parts[0]) || !Number.isFinite(parts[1])) {
        viewer14Status('Get Info failed: fetch valid coordinates first.');
        return;
      }

      let center = [parts[0], parts[1]];
      let fov = viewer14Load().fov;
      try { center = window.viewer14Aladin.getRaDec(); } catch (_) {}
      try {
        const currentFov = Number(window.viewer14Aladin.getFov());
        if (Number.isFinite(currentFov) && currentFov > 0) fov = currentFov;
      } catch (_) {}
      const survey = viewer14Norm(
        document.getElementById('viewer14SurveySelect')?.value || viewer14Load().survey
      );

      button.disabled = true;
      viewer14ProgressStart('SIMBAD 30 arcsecond cone');
      viewer14Status(`Fetching SIMBAD information for ${parts[0].toFixed(6)} ${parts[1].toFixed(6)}…`);
      try {
        const response = await google.colab.kernel.invokeFunction(
          'viewer14.getInfo',
          [parts[0], parts[1]],
          {}
        );
        const galaxy = viewer14Result(response);
        if (!galaxy || galaxy.ok !== true) throw Error(galaxy?.error || 'SIMBAD lookup failed');
        viewer14ProgressDone('SIMBAD', `${Number(galaxy.elapsed_seconds || 0).toFixed(2)} s`);
        viewer14Status(viewer14Panel(galaxy, survey, fov));
        viewer14Save({ra: Number(center[0]), dec: Number(center[1]), survey, fov});
      } catch (error) {
        viewer14ProgressFail('SIMBAD');
        viewer14Status('Get Info failed: ' + String(error?.message || error));
      } finally {
        button.disabled = false;
      }
    };
    return true;
  };

  installGetInfo();
  const timer = setInterval(() => {
    if (installGetInfo()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installGetInfo();
    clearInterval(timer);
  }, 16000);
})();
'''))
