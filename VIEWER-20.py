from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/fce273f7f6a20944015bac3e6ed149f3c984ef4b/VIEWER-19.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-19-base.py", "exec"))


display(Javascript(r'''
(() => {
  const applyLabel = () => {
    const root = document.getElementById('viewer14-root');
    const select = document.getElementById('viewer14CatalogMode');
    const menu = document.getElementById('viewer14CatalogMenu');
    const button = document.getElementById('viewer14CatalogButton');
    if (!root || !select || !menu || !button) return false;

    const option = [...select.options].find(item => item.value === 'interesting');
    if (option) option.textContent = 'Aladin';

    const menuButtons = [...menu.querySelectorAll('button')];
    const interestingButton = menuButtons.find(item =>
      item.textContent.trim().startsWith('Interesting Mix') || item.textContent.trim() === 'Aladin'
    );
    if (interestingButton) interestingButton.textContent = 'Aladin';

    if (select.value === 'interesting') button.textContent = 'Aladin ▾';

    if (!select.dataset.viewer20LabelInstalled) {
      select.dataset.viewer20LabelInstalled = 'true';
      select.addEventListener('change', () => {
        if (select.value === 'interesting') {
          setTimeout(() => { button.textContent = 'Aladin ▾'; }, 0);
        }
      });
    }

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-20';
    return true;
  };

  applyLabel();
  const timer = setInterval(() => {
    if (applyLabel()) clearInterval(timer);
  }, 100);
  setTimeout(() => {
    applyLabel();
    clearInterval(timer);
  }, 16000);
})();
'''))
