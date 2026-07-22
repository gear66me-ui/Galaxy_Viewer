from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-37.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-37-base.py", "exec"))


display(Javascript(r'''
(() => {
  let savedStatusHtml = '';

  function installViewer38() {
    const root = document.getElementById('viewer14-root');
    const status = document.getElementById('viewer14Status');
    if (!root || !status) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-38';

    return true;
  }

  function capturePanel() {
    const status = document.getElementById('viewer14Status');
    if (status && status.innerHTML.trim()) savedStatusHtml = status.innerHTML;
    try { if (typeof window.viewer14Save === 'function') window.viewer14Save(); } catch (_) {}
  }

  function restorePanel() {
    const restore = () => {
      const status = document.getElementById('viewer14Status');
      if (status && savedStatusHtml) status.innerHTML = savedStatusHtml;
      installViewer38();
    };
    setTimeout(restore, 40);
    setTimeout(restore, 180);
    setTimeout(restore, 500);
  }

  document.getElementById('viewer38-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer38-style';
  style.textContent = `
    #viewer14Status #viewer36ChatGPTSearch,
    #viewer14Status #viewer36GeminiSearch,
    #viewer14Status #viewer29ChromeButton,
    #viewer14Status #viewer29CopyButton {
      background:linear-gradient(135deg,#0b4f6c,#137aa3 52%,#169ac7)!important;
      color:#f4fbff!important;
      border:1px solid #35c6ff!important;
      box-shadow:0 3px 10px rgba(0,174,239,.24)!important;
    }
    #viewer14Status #viewer36ChatGPTSearch:hover,
    #viewer14Status #viewer36GeminiSearch:hover,
    #viewer14Status #viewer29ChromeButton:hover,
    #viewer14Status #viewer29CopyButton:hover {
      filter:brightness(1.13)!important;
    }
  `;
  document.head.appendChild(style);

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) capturePanel();
    else restorePanel();
  });
  window.addEventListener('pagehide', capturePanel);
  window.addEventListener('pageshow', restorePanel);
  window.addEventListener('blur', capturePanel);
  window.addEventListener('focus', restorePanel);

  installViewer38();
  const timer = setInterval(installViewer38, 150);
  setTimeout(() => clearInterval(timer), 16000);
})();
'''))
