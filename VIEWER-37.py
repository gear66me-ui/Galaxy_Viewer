from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-36.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-36-base.py", "exec"))


display(Javascript(r'''
(() => {
  function text(value) {
    return String(value ?? '').trim();
  }

  function currentGalaxy() {
    const g = window.viewer30CurrentGalaxy || window.viewer27LastDisplayedGalaxy || {};
    const root = document.getElementById('viewer14-root');
    const rows = [...(root?.querySelectorAll('#viewer14Status tr') || [])];
    const rowValue = label => text(rows.find(row =>
      new RegExp(`^${label}$`, 'i').test(text(row.querySelector('th')?.textContent))
    )?.querySelector('td')?.textContent);

    return {
      name: text(g.name) || rowValue('Object') || 'Galaxy',
      coordinates: rowValue('ICRS coordinates'),
      morphology: text(g.morphology) || rowValue('Morphological type'),
      distance: text(g.redshift_distance) || rowValue('Redshift / Distance'),
      age: text(g.age) || rowValue('Galaxy age'),
      size: text(g.physical_size) || rowValue('Physical size'),
      magnitude: text(g.magnitude) || rowValue('Magnitude')
    };
  }

  function researchPrompt() {
    const g = currentGalaxy();
    return `Search for reliable astronomy information about ${g.name}. Confirm its identity and summarize galaxy type and morphology, coordinates, distance, redshift, radial velocity, apparent magnitude, angular size, physical size, stellar-population age or best-supported age estimate, discovery history, notable structures, and why it is scientifically or visually interesting. Clearly separate measured values from estimates and cite authoritative sources such as NASA, ESA, ESO, SIMBAD, NED, peer-reviewed papers, or major observatories. Viewer data: coordinates ${g.coordinates || 'not supplied'}; morphology ${g.morphology || 'not supplied'}; distance/redshift ${g.distance || 'not supplied'}; displayed age ${g.age || 'not supplied'}; physical size ${g.size || 'not supplied'}; magnitude ${g.magnitude || 'not supplied'}.`;
  }

  async function copyPrompt(showStatus = true) {
    const prompt = researchPrompt();
    try {
      await navigator.clipboard.writeText(prompt);
      if (showStatus && typeof window.viewer14Status === 'function') {
        window.viewer14Status(`Galaxy research prompt copied for ${currentGalaxy().name}.`);
      }
    } catch (_) {}
    return prompt;
  }

  function androidIntent(webUrl, packageName) {
    const withoutScheme = webUrl.replace(/^https?:\/\//, '');
    return `intent://${withoutScheme}#Intent;scheme=https;package=${packageName};S.browser_fallback_url=${encodeURIComponent(webUrl)};end`;
  }

  async function chatGPTSearch() {
    const prompt = await copyPrompt(false);
    const webUrl = `https://chatgpt.com/?q=${encodeURIComponent(prompt)}`;
    if (/Android/i.test(navigator.userAgent)) {
      window.location.href = androidIntent(webUrl, 'com.openai.chatgpt');
    } else {
      window.open(webUrl, '_blank', 'noopener,noreferrer');
    }
  }

  async function geminiSearch() {
    const prompt = await copyPrompt(false);
    const webUrl = `https://gemini.google.com/app?q=${encodeURIComponent(prompt)}`;
    if (/Android/i.test(navigator.userAgent)) {
      window.location.href = androidIntent(webUrl, 'com.google.android.apps.bard');
    } else {
      window.open(webUrl, '_blank', 'noopener,noreferrer');
    }
  }

  function chromeSearch() {
    const name = currentGalaxy().name;
    const query = `${name} galaxy information age distance redshift morphology physical size magnitude astronomy`;
    window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, '_blank', 'noopener,noreferrer');
  }

  window.viewer37CopyPrompt = () => copyPrompt(true);
  window.viewer37ChromeSearch = chromeSearch;
  window.viewer37GeminiSearch = geminiSearch;
  window.viewer37ChatGPTSearch = chatGPTSearch;

  const copyIcon = `
    <svg class="viewer37-icon" viewBox="0 0 24 24" aria-hidden="true">
      <rect x="8" y="7" width="11" height="13" rx="2" fill="#ffffff" stroke="#24364b" stroke-width="1.7"/>
      <rect x="5" y="4" width="11" height="13" rx="2" fill="#dce9f7" stroke="#24364b" stroke-width="1.7"/>
    </svg>`;

  const chromeIcon = `
    <svg class="viewer37-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path fill="#ea4335" d="M12 2a10 10 0 0 1 8.66 5H12a5 5 0 0 0-4.33 2.5L4.78 4.5A9.95 9.95 0 0 1 12 2Z"/>
      <path fill="#fbbc04" d="M4.78 4.5 9.1 12a5 5 0 0 0 2.9 4.58L9.1 21.6A10 10 0 0 1 4.78 4.5Z"/>
      <path fill="#34a853" d="M9.1 21.6 13.43 14a5 5 0 0 0 3.57-4.5h5.77A10 10 0 0 1 9.1 21.6Z"/>
      <circle cx="12" cy="12" r="4" fill="#4285f4" stroke="#ffffff" stroke-width="1.2"/>
    </svg>`;

  const geminiIcon = `
    <svg class="viewer37-icon" viewBox="0 0 24 24" aria-hidden="true">
      <defs><linearGradient id="viewer37GeminiGradient" x1="3" y1="21" x2="21" y2="3" gradientUnits="userSpaceOnUse"><stop stop-color="#1a73e8"/><stop offset=".38" stop-color="#7c4dff"/><stop offset=".7" stop-color="#d965d8"/><stop offset="1" stop-color="#f6a700"/></linearGradient></defs>
      <path fill="url(#viewer37GeminiGradient)" d="M12 1.6c.75 5.45 4.35 9.05 9.8 9.8-5.45.75-9.05 4.35-9.8 9.8-.75-5.45-4.35-9.05-9.8-9.8 5.45-.75 9.05-4.35 9.8-9.8Z"/>
    </svg>`;

  const chatGPTIcon = `
    <span class="viewer37-chatgpt-icon" aria-hidden="true">
      <svg class="viewer37-icon" viewBox="0 0 24 24">
        <path fill="none" stroke="#111111" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" d="M8.2 4.1A4.1 4.1 0 0 1 15 3.7a4.1 4.1 0 0 1 4.6 5.5 4.1 4.1 0 0 1-.4 7 4.1 4.1 0 0 1-6.4 3.9 4.1 4.1 0 0 1-6.8-2.7 4.1 4.1 0 0 1-.3-7.3 4.1 4.1 0 0 1 2.5-6Z"/>
        <path fill="none" stroke="#111111" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" d="m8.1 4.3 7.1 4.1v7.2l-6.3 3.7m10.3-10-7.2 4.1-6.3-3.6m.4 7.5v-8l6-3.5 6.9 4"/>
      </svg>
    </span>`;

  function install() {
    const root = document.getElementById('viewer14-root');
    const title = root?.querySelector('#viewer14Status .fom-title');
    if (!root || !title) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-37';

    [...title.childNodes].forEach(node => {
      if (node.nodeType === Node.TEXT_NODE && /RANDOM GALAXY FIGURES OF MERIT/i.test(text(node.textContent))) node.remove();
    });
    [...title.querySelectorAll('span')].forEach(span => {
      if (/RANDOM GALAXY FIGURES OF MERIT/i.test(text(span.textContent))) span.remove();
    });

    let label = title.querySelector('.viewer37-title-label');
    if (!label) {
      label = document.createElement('span');
      label.className = 'viewer37-title-label';
      title.prepend(label);
    }
    label.textContent = 'Galaxy Info';

    document.getElementById('viewer35ChatGPTSearch')?.remove();
    document.getElementById('viewer36SearchActions')?.remove();
    document.getElementById('viewer29ChromeButton')?.remove();
    document.getElementById('viewer29CopyButton')?.remove();

    let actions = document.getElementById('viewer37SearchActions');
    if (!actions) {
      actions = document.createElement('span');
      actions.id = 'viewer37SearchActions';
      actions.className = 'viewer37-search-actions';
      actions.innerHTML = `
        <button id="viewer37Copy" type="button" class="viewer37-action viewer37-copy" title="Copy galaxy research prompt">${copyIcon}<span>Copy</span></button>
        <button id="viewer37Chrome" type="button" class="viewer37-action viewer37-chrome" title="Search Google for this galaxy">${chromeIcon}<span>Search</span></button>
        <button id="viewer37Gemini" type="button" class="viewer37-action viewer37-gemini" title="Open Gemini app or website with this galaxy prompt">${geminiIcon}<span>Search</span></button>
        <button id="viewer37ChatGPT" type="button" class="viewer37-action viewer37-chatgpt" title="Open ChatGPT app or website with this galaxy prompt">${chatGPTIcon}<span>Search</span></button>`;
      title.appendChild(actions);
      document.getElementById('viewer37Copy').onclick = window.viewer37CopyPrompt;
      document.getElementById('viewer37Chrome').onclick = window.viewer37ChromeSearch;
      document.getElementById('viewer37Gemini').onclick = window.viewer37GeminiSearch;
      document.getElementById('viewer37ChatGPT').onclick = window.viewer37ChatGPTSearch;
    }
    return true;
  }

  document.getElementById('viewer37-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer37-style';
  style.textContent = `
    #viewer14Status .fom-title{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
    #viewer14Status .viewer37-title-label{white-space:nowrap;font-size:17px}
    #viewer14Status .viewer37-search-actions{display:flex;align-items:center;gap:6px;margin-left:auto;flex-wrap:wrap}
    #viewer14Status .viewer37-action{height:36px!important;min-width:86px!important;padding:6px 9px!important;border-radius:8px!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:6px!important;font-size:12px!important;font-weight:800!important;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,.28)}
    #viewer14Status .viewer37-icon{width:20px;height:20px;display:block;flex:0 0 20px}
    #viewer14Status .viewer37-copy{background:#eaf2fb!important;color:#172536!important;border:1px solid #9db5cb!important}
    #viewer14Status .viewer37-chrome{background:#ffffff!important;color:#202124!important;border:1px solid #cfd3d7!important}
    #viewer14Status .viewer37-gemini{background:#ffffff!important;color:#3c4043!important;border:1px solid #c9d2f4!important}
    #viewer14Status .viewer37-chatgpt{background:#ffffff!important;color:#111111!important;border:1px solid #b8b8b8!important}
    #viewer14Status .viewer37-chatgpt-icon{width:24px;height:24px;border-radius:6px;background:#ffffff;display:inline-flex;align-items:center;justify-content:center;flex:0 0 24px}
    #viewer14Status .viewer37-action:hover{filter:brightness(1.06);transform:translateY(-1px)}
    #viewer14Status .viewer37-action:active{transform:translateY(0)}
    @media(max-width:760px){
      #viewer14Status .viewer37-search-actions{width:100%;margin-left:0}
      #viewer14Status .viewer37-action{flex:1 1 92px;min-width:78px!important}
    }
  `;
  document.head.appendChild(style);

  install();
  const timer = setInterval(install, 150);
  setTimeout(() => clearInterval(timer), 16000);
})();
'''))
