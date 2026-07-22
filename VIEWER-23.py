from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-22.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-22-base.py", "exec"))


display(Javascript(r'''
(() => {
  function installViewer23Triangles() {
    const root = document.getElementById('viewer14-root');
    const previous = document.getElementById('viewer21PreviousButton');
    const next = document.getElementById('viewer21NextButton');
    if (!root || !previous || !next) return false;

    previous.textContent = '';
    next.textContent = '';
    previous.classList.add('viewer23-triangle-button', 'viewer23-left-triangle');
    next.classList.add('viewer23-triangle-button', 'viewer23-right-triangle');

    previous.innerHTML = '<svg viewBox="0 0 32 32" aria-hidden="true"><polygon points="24,5 8,16 24,27"></polygon></svg>';
    next.innerHTML = '<svg viewBox="0 0 32 32" aria-hidden="true"><polygon points="8,5 24,16 8,27"></polygon></svg>';

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-23';
    return true;
  }

  const oldStyle = document.getElementById('viewer22-triangle-style');
  if (oldStyle) oldStyle.remove();
  const existingStyle = document.getElementById('viewer23-triangle-style');
  if (existingStyle) existingStyle.remove();

  const style = document.createElement('style');
  style.id = 'viewer23-triangle-style';
  style.textContent = `
    #viewer14-root .viewer22-triangle-button::before,
    #viewer14-root .viewer23-triangle-button::before {
      content: none !important;
      display: none !important;
    }
    #viewer14-root .viewer23-triangle-button {
      position: relative;
      min-width: 29px !important;
      width: 29px !important;
      height: 29px !important;
      padding: 0 !important;
      overflow: visible !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      border-radius: 7px !important;
      box-shadow: none !important;
      text-shadow: none !important;
      filter: none !important;
    }
    #viewer14-root .viewer23-triangle-button svg {
      width: 24px;
      height: 24px;
      overflow: visible;
    }
    #viewer14-root .viewer23-triangle-button polygon {
      stroke-width: 1.8;
      stroke-linejoin: round;
      stroke-linecap: round;
      vector-effect: non-scaling-stroke;
      shape-rendering: geometricPrecision;
      filter: none;
      transition: filter 90ms ease, fill 90ms ease, stroke 90ms ease, transform 90ms ease;
      transform-origin: center;
    }
    #viewer14-root .viewer23-left-triangle polygon {
      fill: #ff001e;
      stroke: #ff001e;
    }
    #viewer14-root .viewer23-right-triangle polygon {
      fill: #9dff00;
      stroke: #9dff00;
    }
    #viewer14-root .viewer23-left-triangle:hover:not(:disabled) polygon,
    #viewer14-root .viewer23-left-triangle:focus-visible:not(:disabled) polygon {
      fill: #ff3049;
      stroke: #ff3049;
    }
    #viewer14-root .viewer23-right-triangle:hover:not(:disabled) polygon,
    #viewer14-root .viewer23-right-triangle:focus-visible:not(:disabled) polygon {
      fill: #caff38;
      stroke: #caff38;
    }
    #viewer14-root .viewer23-left-triangle:active:not(:disabled) polygon {
      fill: #ff6a7d;
      stroke: #ff6a7d;
      filter: drop-shadow(0 0 2px #ff001e) drop-shadow(0 0 4px #ff001e);
      transform: scale(1.08);
    }
    #viewer14-root .viewer23-right-triangle:active:not(:disabled) polygon {
      fill: #efff85;
      stroke: #efff85;
      filter: drop-shadow(0 0 2px #9dff00) drop-shadow(0 0 4px #9dff00);
      transform: scale(1.08);
    }
    #viewer14-root .viewer23-triangle-button:disabled polygon {
      opacity: .35;
      filter: none;
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