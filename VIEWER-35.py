from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-34.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-34-base.py", "exec"))


display(Javascript(r'''
(() => {
  function text(value) {
    return String(value ?? '').trim();
  }

  function currentObjectName() {
    const g = window.viewer30CurrentGalaxy || window.viewer27LastDisplayedGalaxy || {};
    if (text(g.name)) return text(g.name);

    const root = document.getElementById('viewer14-root');
    const objectRow = [...(root?.querySelectorAll('#viewer14Status tr') || [])]
      .find(row => /^object$/i.test(text(row.querySelector('th')?.textContent)));
    return text(objectRow?.querySelector('td')?.textContent) || 'galaxy';
  }

  async function chatGPTSearch() {
    const name = currentObjectName();
    const prompt = `Search the web for reliable information about ${name}. Summarize its galaxy type, distance, redshift, radial velocity, apparent magnitude, angular size, physical size, stellar-population age or best-supported age estimate, discovery/history, and why it is scientifically or visually interesting. Clearly distinguish measured values from estimates and cite authoritative astronomy sources.`;

    try {
      await navigator.clipboard.writeText(prompt);
    } catch (_) {}

    window.open('https://chatgpt.com/', '_blank', 'noopener,noreferrer');
  }
  window.viewer35ChatGPTSearch = chatGPTSearch;

  function install() {
    const root = document.getElementById('viewer14-root');
    if (!root) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-35';

    const title = root.querySelector('#viewer14Status .fom-title');
    if (!title) return false;

    if (!document.getElementById('viewer35ChatGPTSearch')) {
      const button = document.createElement('button');
      button.id = 'viewer35ChatGPTSearch';
      button.type = 'button';
      button.className = 'viewer35-chatgpt-search';
      button.textContent = 'ChatGPT Search';
      button.title = 'Copy a focused galaxy-research prompt and open ChatGPT';
      button.onclick = chatGPTSearch;
      title.appendChild(button);
    }
    return true;
  }

  document.getElementById('viewer35-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer35-style';
  style.textContent = `
    #viewer14Status .viewer35-chatgpt-search {
      padding:7px 11px!important;
      border-radius:7px!important;
      background:#10a37f!important;
      color:#fff!important;
      border:1px solid #19c39a!important;
      font-size:13px!important;
      font-weight:700!important;
      white-space:nowrap;
      margin-left:8px;
    }
    #viewer14Status .viewer35-chatgpt-search:hover {filter:brightness(1.12)}
  `;
  document.head.appendChild(style);

  install();
  const timer = setInterval(install, 150);
  setTimeout(() => clearInterval(timer), 16000);
})();
'''))
