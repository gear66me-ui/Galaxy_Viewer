from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-39.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-39-base.py", "exec"))


display(Javascript(r'''
(() => {
  function text(value) {
    return String(value ?? '').trim();
  }

  function currentObjectName() {
    const g = window.viewer30CurrentGalaxy || window.viewer27LastDisplayedGalaxy || {};
    if (text(g.name)) return text(g.name);

    const rows = [...(document.querySelectorAll('#viewer14Status tr') || [])];
    const objectRow = rows.find(row => /^object$/i.test(text(row.querySelector('th')?.textContent)));
    return text(objectRow?.querySelector('td')?.textContent) || 'galaxy';
  }

  function researchPrompt() {
    const name = currentObjectName();
    return `Search for reliable astronomy information about ${name}. Confirm its identity and summarize galaxy type and morphology, coordinates, distance, redshift, radial velocity, apparent magnitude, angular size, physical size, stellar-population age or best-supported age estimate, discovery history, notable structures, and why it is scientifically or visually interesting. Clearly separate measured values from estimates and cite authoritative sources such as NASA, ESA, ESO, SIMBAD, NED, peer-reviewed papers, or major observatories.`;
  }

  async function copyWithoutReplacingPanel(button) {
    const prompt = researchPrompt();
    try {
      await navigator.clipboard.writeText(prompt);
    } catch (_) {
      const area = document.createElement('textarea');
      area.value = prompt;
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      document.execCommand('copy');
      area.remove();
    }

    const label = button.querySelector('span');
    const oldText = label ? label.textContent : button.textContent;
    if (label) label.textContent = 'Copied';
    else button.textContent = 'Copied';
    setTimeout(() => {
      if (label) label.textContent = oldText;
      else button.textContent = oldText;
    }, 1100);
  }

  function liveButtons() {
    const title = document.querySelector('#viewer14Status .fom-title');
    if (!title) return [];
    return [...title.querySelectorAll('button')];
  }

  function identifyButtons() {
    const buttons = liveButtons();
    const result = {copy:null, chrome:null, gemini:null, chatgpt:null};

    for (const button of buttons) {
      const label = text(button.textContent).toLowerCase();
      const id = text(button.id).toLowerCase();
      const title = text(button.title).toLowerCase();

      if (id.includes('copy') || label === 'copy' || title.includes('copy')) result.copy = button;
      else if (id.includes('chrome') || label.includes('chrome') || title.includes('google')) result.chrome = button;
      else if (id.includes('gemini') || title.includes('gemini')) result.gemini = button;
      else if (id.includes('chatgpt') || title.includes('chatgpt')) result.chatgpt = button;
    }
    return result;
  }

  function applyButtonStyle(button) {
    if (!button) return;
    button.style.setProperty('background', 'linear-gradient(135deg, #173f7a 0%, #315fa8 45%, #6846a8 100%)', 'important');
    button.style.setProperty('background-color', '#315fa8', 'important');
    button.style.setProperty('color', '#ffffff', 'important');
    button.style.setProperty('border', '1px solid #78d6ff', 'important');
    button.style.setProperty('box-shadow', '0 3px 11px rgba(63, 92, 190, .52), inset 0 1px 0 rgba(255,255,255,.22)', 'important');
  }

  function installViewer40() {
    const root = document.getElementById('viewer14-root');
    const status = document.getElementById('viewer14Status');
    if (!root || !status) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-40';

    const title = status.querySelector('.fom-title');
    const titleLabel = title?.querySelector('.viewer36-title-label');
    if (titleLabel) titleLabel.textContent = 'Galaxy Info';

    const found = identifyButtons();
    Object.values(found).forEach(applyButtonStyle);

    if (found.copy && found.copy.dataset.viewer40Copy !== 'true') {
      const replacement = found.copy.cloneNode(true);
      replacement.dataset.viewer40Copy = 'true';
      replacement.onclick = event => {
        event.preventDefault();
        event.stopPropagation();
        copyWithoutReplacingPanel(replacement);
      };
      found.copy.replaceWith(replacement);
      applyButtonStyle(replacement);
    }

    return true;
  }

  document.getElementById('viewer40-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer40-style';
  style.textContent = `
    #viewer14Status .fom-title button {
      background:linear-gradient(135deg,#173f7a 0%,#315fa8 45%,#6846a8 100%)!important;
      background-color:#315fa8!important;
      color:#fff!important;
      border:1px solid #78d6ff!important;
      box-shadow:0 3px 11px rgba(63,92,190,.52),inset 0 1px 0 rgba(255,255,255,.22)!important;
    }
    #viewer14Status .fom-title button:hover {
      background:linear-gradient(135deg,#20569a 0%,#4277c7 45%,#805bc7 100%)!important;
      filter:brightness(1.08)!important;
    }
  `;
  document.head.appendChild(style);

  installViewer40();
  const timer = setInterval(installViewer40, 120);
  setTimeout(() => clearInterval(timer), 20000);

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      setTimeout(installViewer40, 60);
      setTimeout(installViewer40, 220);
      setTimeout(installViewer40, 600);
    }
  });
  window.addEventListener('focus', () => {
    setTimeout(installViewer40, 60);
    setTimeout(installViewer40, 260);
  });
  window.addEventListener('pageshow', () => {
    setTimeout(installViewer40, 80);
    setTimeout(installViewer40, 300);
  });

  const observer = new MutationObserver(() => installViewer40());
  const status = document.getElementById('viewer14Status');
  if (status) observer.observe(status, {childList:true, subtree:true});
})();
'''))
