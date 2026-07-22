from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-20.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-20-base.py", "exec"))


display(Javascript(r'''
(() => {
  const HISTORY_KEY = 'galaxy-viewer-viewer21-history';

  function loadHistory() {
    try {
      const saved = JSON.parse(localStorage.getItem(HISTORY_KEY) || 'null');
      if (saved && Array.isArray(saved.items) && Number.isInteger(saved.index)) {
        return {
          items: saved.items,
          index: Math.max(-1, Math.min(saved.index, saved.items.length - 1))
        };
      }
    } catch (_) {}
    return {items: [], index: -1};
  }

  window.viewer21History = loadHistory();
  window.viewer21RestoringHistory = false;

  function saveHistory() {
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(window.viewer21History));
    } catch (_) {}
    updateArrows();
  }

  function updateArrows() {
    const history = window.viewer21History || {items: [], index: -1};
    const previous = document.getElementById('viewer21PreviousButton');
    const next = document.getElementById('viewer21NextButton');
    if (previous) previous.disabled = history.index <= 0;
    if (next) next.disabled = history.index < 0 || history.index >= history.items.length - 1;
  }

  function restoreHistory(index) {
    const history = window.viewer21History;
    if (!history || index < 0 || index >= history.items.length) return;
    history.index = index;
    window.viewer21RestoringHistory = true;
    try {
      window.viewer14ShowGalaxy(history.items[index]);
    } finally {
      window.viewer21RestoringHistory = false;
      saveHistory();
    }
  }

  window.viewer21PreviousGalaxy = () => restoreHistory(window.viewer21History.index - 1);
  window.viewer21NextGalaxy = () => restoreHistory(window.viewer21History.index + 1);

  function installHistoryCapture() {
    if (typeof window.viewer14ShowGalaxy !== 'function') return false;
    if (window.viewer14ShowGalaxy.viewer21Wrapped) return true;

    const originalShowGalaxy = window.viewer14ShowGalaxy;
    const wrappedShowGalaxy = function(galaxy) {
      originalShowGalaxy(galaxy);
      if (!window.viewer21RestoringHistory) {
        const history = window.viewer21History;
        if (history.index < history.items.length - 1) {
          history.items = history.items.slice(0, history.index + 1);
        }
        history.items.push(JSON.parse(JSON.stringify(galaxy)));
        history.index = history.items.length - 1;
        saveHistory();
      }
    };
    wrappedShowGalaxy.viewer21Wrapped = true;
    window.viewer14ShowGalaxy = wrappedShowGalaxy;
    return true;
  }

  function installButtons() {
    const root = document.getElementById('viewer14-root');
    const randomButton = document.getElementById('viewer14RandomButton');
    if (!root || !randomButton) return false;

    let previous = document.getElementById('viewer21PreviousButton');
    if (!previous) {
      previous = document.createElement('button');
      previous.id = 'viewer21PreviousButton';
      previous.type = 'button';
      previous.className = 'viewer21-history-button viewer21-previous-button';
      previous.textContent = '←';
      previous.title = 'Previous galaxy';
      previous.setAttribute('aria-label', 'Previous galaxy');
      previous.onclick = window.viewer21PreviousGalaxy;
      randomButton.insertAdjacentElement('beforebegin', previous);
    }

    let next = document.getElementById('viewer21NextButton');
    if (!next) {
      next = document.createElement('button');
      next.id = 'viewer21NextButton';
      next.type = 'button';
      next.className = 'viewer21-history-button viewer21-next-button';
      next.textContent = '→';
      next.title = 'Next galaxy';
      next.setAttribute('aria-label', 'Next galaxy');
      next.onclick = window.viewer21NextGalaxy;
      randomButton.insertAdjacentElement('afterend', next);
    }

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-21';
    updateArrows();
    return true;
  }

  const style = document.createElement('style');
  style.textContent = `
    #viewer14-root .viewer21-history-button {
      min-width: 48px;
      padding: 14px 17px;
      font-size: 25px;
      line-height: 1;
      font-weight: 900;
      border: 2px solid #8a4fd4;
      box-shadow: 0 0 10px rgba(138,79,212,.72);
    }
    #viewer14-root .viewer21-previous-button {
      background: #8a4fd4;
      color: #ff3030;
      text-shadow: 0 0 5px #ff0000;
    }
    #viewer14-root .viewer21-next-button {
      background: #8a4fd4;
      color: #35e86f;
      text-shadow: 0 0 5px #00b83f;
    }
    #viewer14-root .viewer21-history-button:disabled {
      opacity: .35;
      box-shadow: none;
      cursor: default;
    }
  `;
  document.head.appendChild(style);

  installHistoryCapture();
  installButtons();
  const timer = setInterval(() => {
    const captureReady = installHistoryCapture();
    const buttonsReady = installButtons();
    if (captureReady && buttonsReady) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    installHistoryCapture();
    installButtons();
    clearInterval(timer);
  }, 16000);
})();
'''))
