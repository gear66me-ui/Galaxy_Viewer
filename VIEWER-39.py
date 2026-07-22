from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-38.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-38-base.py", "exec"))


display(Javascript(r'''
(() => {
  function installViewer39() {
    const root = document.getElementById('viewer14-root');
    if (!root) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-39';
    return true;
  }

  document.getElementById('viewer39-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer39-style';
  style.textContent = `
    #viewer14Status #viewer36ChatGPTSearch,
    #viewer14Status #viewer36GeminiSearch,
    #viewer14Status #viewer29ChromeButton,
    #viewer14Status #viewer29CopyButton {
      background: linear-gradient(135deg, #123d73 0%, #315fa8 48%, #6846a8 100%) !important;
      color: #ffffff !important;
      border: 1px solid #70c9ff !important;
      box-shadow: 0 3px 10px rgba(49, 95, 168, .42), inset 0 1px 0 rgba(255,255,255,.18) !important;
    }

    #viewer14Status #viewer36ChatGPTSearch:hover,
    #viewer14Status #viewer36GeminiSearch:hover,
    #viewer14Status #viewer29ChromeButton:hover,
    #viewer14Status #viewer29CopyButton:hover {
      background: linear-gradient(135deg, #19508f 0%, #3d74c2 48%, #7b55c4 100%) !important;
      filter: brightness(1.08);
    }
  `;
  document.head.appendChild(style);

  installViewer39();
  const timer = setInterval(installViewer39, 150);
  setTimeout(() => clearInterval(timer), 16000);
})();
'''))
