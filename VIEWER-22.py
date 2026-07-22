from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-21.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-21-base.py", "exec"))


display(Javascript(r'''
(() => {
  function installViewer22Triangles() {
    const root = document.getElementById('viewer14-root');
    const previous = document.getElementById('viewer21PreviousButton');
    const next = document.getElementById('viewer21NextButton');
    if (!root || !previous || !next) return false;

    previous.textContent = '';
    next.textContent = '';
    previous.classList.add('viewer22-triangle-button', 'viewer22-left-triangle');
    next.classList.add('viewer22-triangle-button', 'viewer22-right-triangle');

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-22';
    return true;
  }

  const style = document.createElement('style');
  style.id = 'viewer22-triangle-style';
  style.textContent = `
    #viewer14-root .viewer22-triangle-button {
      position: relative;
      min-width: 48px;
      width: 48px;
      height: 48px;
      padding: 0;
      overflow: visible;
    }
    #viewer14-root .viewer22-triangle-button::before {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      width: 0;
      height: 0;
      transform: translate(-50%, -50%);
      filter: drop-shadow(0 0 4px currentColor) drop-shadow(0 0 9px currentColor) drop-shadow(0 0 15px currentColor);
    }
    #viewer14-root .viewer22-left-triangle {
      color: #ff001e;
    }
    #viewer14-root .viewer22-left-triangle::before {
      border-top: 15px solid transparent;
      border-bottom: 15px solid transparent;
      border-right: 27px solid #ff001e;
    }
    #viewer14-root .viewer22-right-triangle {
      color: #39ff14;
    }
    #viewer14-root .viewer22-right-triangle::before {
      border-top: 15px solid transparent;
      border-bottom: 15px solid transparent;
      border-left: 27px solid #39ff14;
    }
    #viewer14-root .viewer22-triangle-button:disabled::before {
      filter: drop-shadow(0 0 3px currentColor) drop-shadow(0 0 7px currentColor);
    }
  `;
  document.head.appendChild(style);

  installViewer22Triangles();
  const timer = setInterval(() => {
    if (installViewer22Triangles()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installViewer22Triangles();
    clearInterval(timer);
  }, 16000);
})();
'''))
