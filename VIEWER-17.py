from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/d763405b44e606943fa547ea840dd2462e427824/VIEWER-16.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-16-base.py", "exec"))


display(Javascript(r'''
(() => {
  const install = () => {
    const root = document.getElementById('viewer14-root');
    const randomButton = document.getElementById('viewer14RandomButton');
    const fetchButton = [...document.querySelectorAll('#viewer14-root button')].find(
      button => button.textContent.trim() === 'Fetch Coordinates'
    );
    const coordBox = document.getElementById('viewer14CoordBox');
    const infoButton = document.getElementById('viewer14InfoButton');
    const actionRow = document.getElementById('viewer16ActionRow');
    const coordinateRow = document.getElementById('viewer16CoordinateRow');

    if (!root || !randomButton || !fetchButton || !coordBox || !infoButton) return false;

    let row = document.getElementById('viewer17ControlRow');
    if (!row) {
      row = document.createElement('div');
      row.id = 'viewer17ControlRow';
      row.className = 'viewer17-control-row';
      const controls = actionRow?.parentElement || randomButton.parentElement;
      controls.insertBefore(row, actionRow || controls.firstChild);
    }

    row.appendChild(randomButton);
    row.appendChild(fetchButton);
    row.appendChild(coordBox);
    row.appendChild(infoButton);

    if (actionRow && actionRow !== row) actionRow.remove();
    if (coordinateRow && coordinateRow !== row) coordinateRow.remove();

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-17';
    return true;
  };

  if (!install()) {
    const timer = setInterval(() => {
      if (install()) clearInterval(timer);
    }, 100);
    setTimeout(() => clearInterval(timer), 15000);
  }
})();
'''))


display(Javascript(r'''
(() => {
  const style = document.createElement('style');
  style.textContent = `
    #viewer14-root .viewer17-control-row {
      display: flex;
      align-items: center;
      gap: 7px;
      width: 100%;
      flex-wrap: nowrap;
    }
    #viewer14-root .viewer17-control-row button {
      flex: 0 0 auto;
      padding: 7px 11px;
      font-size: 13px;
      min-height: 38px;
      white-space: nowrap;
    }
    #viewer14-root .viewer17-control-row input {
      flex: 0 1 300px;
      width: 300px;
      min-width: 150px;
      max-width: 300px;
      padding: 7px 9px;
      font-size: 13px;
    }
    #viewer14CatalogMenuWrap {
      min-width: 300px !important;
    }
    #viewer14CatalogButton {
      padding: 9px 10px !important;
      font-size: 14px !important;
    }
    #viewer14-root .survey-menu-wrap {
      min-width: 240px;
    }
    #viewer14SurveyButton {
      padding: 9px 10px !important;
      font-size: 14px !important;
    }
    @media (max-width: 720px) {
      #viewer14-root .viewer17-control-row {
        gap: 5px;
      }
      #viewer14-root .viewer17-control-row button {
        padding: 6px 8px;
        font-size: 12px;
      }
      #viewer14-root .viewer17-control-row input {
        flex: 1 1 auto;
        width: auto;
        min-width: 0;
        max-width: none;
        font-size: 12px;
      }
      #viewer14CatalogMenuWrap {
        min-width: 260px !important;
      }
      #viewer14-root .survey-menu-wrap {
        min-width: 210px;
      }
    }
  `;
  document.head.appendChild(style);
})();
'''))