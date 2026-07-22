from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-22.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-22-base.py", "exec"))


display(Javascript(r'''
(() => {
  const LEFT_SVG = `
    <svg viewBox="0 0 32 32" width="22" height="22" aria-hidden="true" focusable="false">
      <polygon points="25,4 7,16 25,28"
               fill="#ff001e"
               stroke="#ff001e"
               stroke-width="3"
               stroke-linejoin="round" />
    </svg>`;

  const RIGHT_SVG = `
    <svg viewBox="0 0 32 32" width="22" height="22" aria-hidden="true" focusable="false">
      <polygon points="7,4 25,16 7,28"
               fill="#7fff00"
               stroke="#7fff00"
               stroke-width="3"
               stroke-linejoin="round" />
    </svg>`;

  function installViewer23Triangles() {
    const root = document.getElementById('viewer14-root');
    const previous = document.getElementById('viewer21PreviousButton');
    const next = document.getElementById('viewer21NextButton');
    if (!root || !previous || !next) return false;

    previous.innerHTML = LEFT_SVG;
    next.innerHTML = RIGHT_SVG;
    previous.classList.add('viewer23-triangle-button', 'viewer23-left-triangle');
    next.classList.add('viewer23-triangle-button', 'viewer23-right-triangle');

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-23';
    return true;
  }

  const oldStyle = document.getElementById('viewer23-triangle-style');
  if (oldStyle) oldStyle.remove();

  const style = document.createElement('style');
  style.id = 'viewer23-triangle-style';
  style.textContent = `
    #viewer14-root .viewer22-triangle-button::before {
      display: none !important;
    }
    #viewer14-root .viewer23-triangle-button {
      min-width: 29px !important;
      width: 29px !important;
      height: 29px !important;
      padding: 0 !important;
      border-radius: 7px !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      overflow: hidden !important;
      box-shadow: none !important;
      text-shadow: none !important;
      filter: none !important;
    }
    #viewer14-root .viewer23-triangle-button svg,
    #viewer14-root .viewer23-triangle-button polygon {
      filter: none !important;
      shape-rendering: geometricPrecision;
    }
  `;
  document.head.appendChild(style);

  installViewer23Triangles();
  const timer = setInterval(() => {
    if (installViewer23Triangles()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installViewer23Triangles();
    clearInterval(timer);
  }, 16000);
})();
'''))