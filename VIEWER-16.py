from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/737f8535605987c27830b24b83989335a73c31c3/VIEWER-15.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-15-base.py", "exec"))


display(Javascript(r'''
(() => {
  function distanceText(g) {
    let text = g.distance_bly || (String(g.redshift_distance || '').split('/')[1] || 'Not available').trim();
    const match = String(text).match(/^([0-9]+(?:\.[0-9]+)?)\s+billion\s+ly/i);
    if (match) {
      const billion = Number(match[1]);
      if (Number.isFinite(billion) && billion < 1) {
        return `${(billion * 1000).toFixed(2)} million ly`;
      }
    }
    return text || 'Not available';
  }

  function zText(g) {
    const text = String(g.redshift_distance || '');
    const first = text.split('/')[0].trim();
    return first || 'Not available';
  }

  function installLayout() {
    const randomButton = document.getElementById('viewer14RandomButton');
    const fetchButton = [...document.querySelectorAll('#viewer14-root button')].find(
      button => button.textContent.trim() === 'Fetch Coordinates'
    );
    const coordBox = document.getElementById('viewer14CoordBox');
    const infoButton = document.getElementById('viewer14InfoButton');
    if (!randomButton || !fetchButton || !coordBox || !infoButton) return false;
    if (document.getElementById('viewer16ActionRow')) return true;

    const parent = randomButton.parentElement;
    const marker = document.createComment('viewer16-controls');
    parent.insertBefore(marker, randomButton);

    const actionRow = document.createElement('div');
    actionRow.id = 'viewer16ActionRow';
    actionRow.className = 'viewer16-action-row';

    const coordinateRow = document.createElement('div');
    coordinateRow.id = 'viewer16CoordinateRow';
    coordinateRow.className = 'viewer16-coordinate-row';

    parent.insertBefore(actionRow, marker);
    parent.insertBefore(coordinateRow, marker);
    actionRow.appendChild(randomButton);
    actionRow.appendChild(fetchButton);
    coordinateRow.appendChild(coordBox);
    coordinateRow.appendChild(infoButton);
    marker.remove();
    return true;
  }

  const wait = setInterval(() => {
    const root = document.getElementById('viewer14-root');
    const heading = root?.querySelector('h3');
    if (!root || !heading || typeof viewer14Panel !== 'function') return;

    heading.textContent = 'Galaxy Viewer — VIEWER-16';
    installLayout();

    window.viewer14Panel = function(g, survey, fov) {
      const velocity = (
        g.velocity_kms !== null &&
        g.velocity_kms !== undefined &&
        Number.isFinite(Number(g.velocity_kms))
      ) ? `${Number(g.velocity_kms).toLocaleString(undefined, {maximumFractionDigits: 1})} km/s` : 'Not available';

      const combined = `${zText(g)} / ${distanceText(g)}`;
      const rows = [
        ['Object', g.name],
        ['Source catalog', g.catalog],
        ['ICRS coordinates', `${Number(g.ra).toFixed(6)} ${Number(g.dec).toFixed(6)}`],
        ['Galaxy age', g.age || 'Not available', 'emphasis'],
        ['Redshift (z) / Distance', combined, 'emphasis'],
        ['Morphological type', g.morphology || 'Not available'],
        ['Angular size', g.angular_size || 'Not available'],
        ['Radial velocity', velocity],
        ['Physical size', g.physical_size || 'Not available'],
        ['Magnitude', g.magnitude || 'Not available'],
        ['Interest score', g.interest_score ?? 'Not available'],
        ['Distance method', g.distance_method || 'Not available'],
        ['Displayed survey', survey],
        ['Field of view', `${fov.toFixed(3)}°`],
        ['Catalog elapsed time', `${Number(g.elapsed_seconds || 0).toFixed(2)} s`],
        ['Data source', g.source]
      ];

      return `<div class="fom-title">RANDOM GALAXY FIGURES OF MERIT</div><table>${rows.map(
        row => `<tr class="${row[2] || ''}"><th>${row[0]}</th><td>${row[1]}</td></tr>`
      ).join('')}</table>`;
    };

    clearInterval(wait);
  }, 100);

  setTimeout(() => clearInterval(wait), 15000);
})();
'''))


display(Javascript(r'''
(() => {
  const style = document.createElement('style');
  style.textContent = `
    #viewer14-root .viewer16-action-row,
    #viewer14-root .viewer16-coordinate-row {
      display: flex;
      align-items: center;
      gap: 8px;
      width: 100%;
      flex: 1 0 100%;
    }
    #viewer14-root .viewer16-action-row button,
    #viewer14-root .viewer16-coordinate-row button {
      padding: 8px 13px;
      font-size: 14px;
      min-height: 40px;
    }
    #viewer14-root .viewer16-action-row button {
      flex: 0 0 auto;
    }
    #viewer14-root .viewer16-coordinate-row input {
      flex: 0 1 360px;
      width: 360px;
      max-width: 360px;
      min-width: 220px;
      padding: 8px 10px;
      font-size: 14px;
    }
    #viewer14-root .viewer16-coordinate-row button {
      flex: 0 0 auto;
    }
    #viewer14-root .controls {
      gap: 8px;
    }
    #viewer14Status th,
    #viewer14Status td {
      padding: 8px 10px;
    }
    @media (max-width: 620px) {
      #viewer14-root .viewer16-action-row button {
        flex: 1 1 0;
      }
      #viewer14-root .viewer16-coordinate-row {
        flex-wrap: nowrap;
      }
      #viewer14-root .viewer16-coordinate-row input {
        flex: 1 1 auto;
        width: auto;
        min-width: 0;
        max-width: none;
      }
      #viewer14-root .viewer16-coordinate-row button {
        width: auto;
      }
    }
  `;
  document.head.appendChild(style);
})();
'''))