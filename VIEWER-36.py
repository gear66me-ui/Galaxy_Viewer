from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-35.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-35-base.py", "exec"))


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

  function researchPrompt() {
    const name = currentObjectName();
    return `Search the web for reliable information about ${name}. Summarize its galaxy type, distance, redshift, radial velocity, apparent magnitude, angular size, physical size, stellar-population age or best-supported age estimate, discovery/history, and why it is scientifically or visually interesting. Clearly distinguish measured values from estimates and cite authoritative astronomy sources.`;
  }

  async function copyPrompt(prompt) {
    try {
      await navigator.clipboard.writeText(prompt);
    } catch (_) {}
  }

  function launchWithFallback(appUrl, webUrl) {
    let hidden = false;
    const markHidden = () => { hidden = true; };
    document.addEventListener('visibilitychange', markHidden, {once:true});
    window.location.href = appUrl;
    setTimeout(() => {
      if (!hidden && !document.hidden) {
        window.open(webUrl, '_blank', 'noopener,noreferrer');
      }
    }, 900);
  }

  async function chatGPTSearch() {
    const prompt = researchPrompt();
    await copyPrompt(prompt);
    const appUrl = 'intent://chatgpt.com/#Intent;scheme=https;package=com.openai.chatgpt;end';
    launchWithFallback(appUrl, 'https://chatgpt.com/');
  }

  async function geminiSearch() {
    const prompt = researchPrompt();
    await copyPrompt(prompt);
    const appUrl = 'intent://gemini.google.com/app#Intent;scheme=https;package=com.google.android.apps.bard;end';
    launchWithFallback(appUrl, 'https://gemini.google.com/app');
  }

  window.viewer36ChatGPTSearch = chatGPTSearch;
  window.viewer36GeminiSearch = geminiSearch;

  function install() {
    const root = document.getElementById('viewer14-root');
    if (!root) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-36';

    const title = root.querySelector('#viewer14Status .fom-title');
    if (!title) return false;

    let label = title.querySelector('.viewer36-title-label');
    if (!label) {
      const existingTextNode = [...title.childNodes].find(node => node.nodeType === Node.TEXT_NODE && text(node.textContent));
      if (existingTextNode) existingTextNode.remove();
      const existingSpan = [...title.children].find(el => el.tagName === 'SPAN' && !el.classList.contains('viewer36-title-label'));
      if (existingSpan && /RANDOM GALAXY FIGURES OF MERIT/i.test(text(existingSpan.textContent))) existingSpan.remove();
      label = document.createElement('span');
      label.className = 'viewer36-title-label';
      label.textContent = 'Galaxy Info';
      title.prepend(label);
    } else {
      label.textContent = 'Galaxy Info';
    }

    document.getElementById('viewer35ChatGPTSearch')?.remove();

    let actions = document.getElementById('viewer36SearchActions');
    if (!actions) {
      actions = document.createElement('span');
      actions.id = 'viewer36SearchActions';
      actions.className = 'viewer36-search-actions';
      actions.innerHTML = `
        <button id="viewer36GeminiSearch" type="button" class="viewer36-search viewer36-gemini">Gemini Search</button>
        <button id="viewer36ChatGPTSearch" type="button" class="viewer36-search viewer36-chatgpt">ChatGPT Search</button>`;
      title.appendChild(actions);
      document.getElementById('viewer36GeminiSearch').onclick = geminiSearch;
      document.getElementById('viewer36ChatGPTSearch').onclick = chatGPTSearch;
    }
    return true;
  }

  document.getElementById('viewer36-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer36-style';
  style.textContent = `
    #viewer14Status .fom-title{display:flex;align-items:center;justify-content:space-between;gap:10px}
    #viewer14Status .viewer36-title-label{white-space:nowrap}
    #viewer14Status .viewer36-search-actions{display:flex;align-items:center;gap:7px;margin-left:auto}
    #viewer14Status .viewer36-search{padding:7px 11px!important;border-radius:7px!important;font-size:13px!important;font-weight:700!important;white-space:nowrap}
    #viewer14Status .viewer36-chatgpt{background:#10a37f!important;color:#fff!important;border:1px solid #19c39a!important}
    #viewer14Status .viewer36-gemini{background:#1a73e8!important;color:#fff!important;border:1px solid #8ab4f8!important}
    #viewer14Status .viewer36-search:hover{filter:brightness(1.12)}
    @media(max-width:620px){
      #viewer14Status .fom-title{align-items:flex-start;flex-wrap:wrap}
      #viewer14Status .viewer36-search-actions{width:100%;margin-left:0}
    }
  `;
  document.head.appendChild(style);

  install();
  const timer = setInterval(install, 150);
  setTimeout(() => clearInterval(timer), 16000);
})();
'''))
