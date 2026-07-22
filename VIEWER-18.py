from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/3a227706a6dae3236210e7aeac92f91bda507bc9/VIEWER-17.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-17-base.py", "exec"))


display(Javascript(r'''
(() => {
  const enforceSingleRow = () => {
    const root = document.getElementById('viewer14-root');
    const randomButton = document.getElementById('viewer14RandomButton');
    const fetchButton = [...document.querySelectorAll('#viewer14-root button')].find(
      button => button.textContent.trim() === 'Fetch Coordinates'
    );
    const coordBox = document.getElementById('viewer14CoordBox');
    const infoButton = document.getElementById('viewer14InfoButton');
    if (!root || !randomButton || !fetchButton || !coordBox || !infoButton) return false;

    let row = document.getElementById('viewer17ControlRow');
    if (!row) {
      row = document.createElement('div');
      row.id = 'viewer17ControlRow';
      row.className = 'viewer17-control-row';
      const controls = randomButton.closest('.controls') || randomButton.parentElement;
      controls.insertBefore(row, controls.firstChild);
    }

    row.appendChild(randomButton);
    row.appendChild(fetchButton);
    row.appendChild(coordBox);
    row.appendChild(infoButton);

    const actionRow = document.getElementById('viewer16ActionRow');
    const coordinateRow = document.getElementById('viewer16CoordinateRow');
    if (actionRow && actionRow !== row && !actionRow.children.length) actionRow.remove();
    if (coordinateRow && coordinateRow !== row && !coordinateRow.children.length) coordinateRow.remove();

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-18';
    return true;
  };

  enforceSingleRow();
  const timer = setInterval(enforceSingleRow, 100);
  setTimeout(() => {
    enforceSingleRow();
    clearInterval(timer);
  }, 16000);
})();
'''))