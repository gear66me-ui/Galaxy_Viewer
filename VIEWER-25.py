from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-24.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-24-base.py", "exec"))


display(Javascript(r'''
(() => {
  function installViewer25Red() {
    const root = document.getElementById('viewer14-root');
    const previous = document.getElementById('viewer21PreviousButton');
    if (!root || !previous) return false;

    previous.classList.add('viewer25-left-triangle');
    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-25';
    return true;
  }

  const existingStyle = document.getElementById('viewer25-red-style');
  if (existingStyle) existingStyle.remove();

  const style = document.createElement('style');
  style.id = 'viewer25-red-style';
  style.textContent = `
    #viewer14-root .viewer25-left-triangle path {
      fill: #ff1a1a !important;
      stroke: #ff1a1a !important;
    }
    #viewer14-root .viewer25-left-triangle:hover:not(:disabled) path,
    #viewer14-root .viewer25-left-triangle:focus-visible:not(:disabled) path {
      fill: #ff4d4d !important;
      stroke: #ff4d4d !important;
    }
    #viewer14-root .viewer25-left-triangle:active:not(:disabled) path {
      fill: #ff8080 !important;
      stroke: #ff8080 !important;
      filter: drop-shadow(0 0 2px #ff1a1a) drop-shadow(0 0 4px #ff1a1a) !important;
      transform: scale(1.08);
    }
  `;
  document.head.appendChild(style);

  installViewer25Red();
  const timer = setInterval(() => {
    if (installViewer25Red()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installViewer25Red();
    clearInterval(timer);
  }, 16000);
})();
'''))