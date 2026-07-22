from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-23.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-23-base.py", "exec"))


display(Javascript(r'''
(() => {
  const LEFT_TRIANGLE = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M24.2 4.9 Q26.2 4.2 26.2 6.5 L26.2 25.5 Q26.2 27.8 24.2 27.1 L8.9 18.1 Q5.9 16.3 8.9 13.9 Z"></path></svg>';
  const RIGHT_TRIANGLE = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7.8 4.9 Q5.8 4.2 5.8 6.5 L5.8 25.5 Q5.8 27.8 7.8 27.1 L23.1 18.1 Q26.1 16.3 23.1 13.9 Z"></path></svg>';

  function installViewer24Triangles() {
    const root = document.getElementById('viewer14-root');
    const previous = document.getElementById('viewer21PreviousButton');
    const next = document.getElementById('viewer21NextButton');
    if (!root || !previous || !next) return false;

    previous.innerHTML = LEFT_TRIANGLE;
    next.innerHTML = RIGHT_TRIANGLE;
    previous.classList.add('viewer24-triangle-button', 'viewer24-left-triangle');
    next.classList.add('viewer24-triangle-button', 'viewer24-right-triangle');

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-24';
    return true;
  }

  const existingStyle = document.getElementById('viewer24-triangle-style');
  if (existingStyle) existingStyle.remove();

  const style = document.createElement('style');
  style.id = 'viewer24-triangle-style';
  style.textContent = `
    #viewer14-root .viewer24-triangle-button svg {
      width: 24px;
      height: 24px;
      overflow: visible;
    }
    #viewer14-root .viewer24-triangle-button polygon {
      display: none !important;
    }
    #viewer14-root .viewer24-triangle-button path {
      stroke-width: 1.8;
      stroke-linejoin: round;
      stroke-linecap: round;
      vector-effect: non-scaling-stroke;
      shape-rendering: geometricPrecision;
      transition: filter 90ms ease, fill 90ms ease, stroke 90ms ease, transform 90ms ease;
      transform-origin: center;
    }
    #viewer14-root .viewer24-left-triangle path {
      fill: #ff303f;
      stroke: #ff303f;
    }
    #viewer14-root .viewer24-right-triangle path {
      fill: #9dff00;
      stroke: #9dff00;
    }
    #viewer14-root .viewer24-left-triangle:hover:not(:disabled) path,
    #viewer14-root .viewer24-left-triangle:focus-visible:not(:disabled) path {
      fill: #ff5a66;
      stroke: #ff5a66;
    }
    #viewer14-root .viewer24-right-triangle:hover:not(:disabled) path,
    #viewer14-root .viewer24-right-triangle:focus-visible:not(:disabled) path {
      fill: #caff38;
      stroke: #caff38;
    }
    #viewer14-root .viewer24-left-triangle:active:not(:disabled) path {
      fill: #ff8a94;
      stroke: #ff8a94;
      filter: drop-shadow(0 0 2px #ff303f) drop-shadow(0 0 4px #ff303f);
      transform: scale(1.08);
    }
    #viewer14-root .viewer24-right-triangle:active:not(:disabled) path {
      fill: #efff85;
      stroke: #efff85;
      filter: drop-shadow(0 0 2px #9dff00) drop-shadow(0 0 4px #9dff00);
      transform: scale(1.08);
    }
    #viewer14-root .viewer24-triangle-button:disabled path {
      opacity: .35;
      filter: none;
    }
  `;
  document.head.appendChild(style);

  installViewer24Triangles();
  const timer = setInterval(() => {
    if (installViewer24Triangles()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installViewer24Triangles();
    clearInterval(timer);
  }, 16000);
})();
'''))