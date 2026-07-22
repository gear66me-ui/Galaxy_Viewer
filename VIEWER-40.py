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

  function rowValue(label) {
    const rows = [...(document.querySelectorAll('#viewer14Status tr') || [])];
    const row = rows.find(item => new RegExp(`^${label}$`, 'i').test(text(item.querySelector('th')?.textContent)));
    return text(row?.querySelector('td')?.textContent);
  }

  function researchPrompt() {
    const g = window.viewer30CurrentGalaxy || window.viewer27LastDisplayedGalaxy || {};
    const name = text(g.name) || rowValue('Object') || 'Galaxy';
    return `Search for reliable astronomy information about ${name}. Confirm its identity and summarize galaxy type and morphology, coordinates, distance, redshift, radial velocity, apparent magnitude, angular size, physical size, stellar-population age or best-supported age estimate, discovery history, notable structures, and why it is scientifically or visually interesting. Clearly separate measured values from estimates and cite authoritative sources such as NASA, ESA, ESO, SIMBAD, NED, peer-reviewed papers, or major observatories. Viewer data: coordinates ${rowValue('ICRS coordinates') || 'not supplied'}; morphology ${text(g.morphology) || rowValue('Morphological type') || 'not supplied'}; distance/redshift ${text(g.redshift_distance) || rowValue('Redshift / Distance') || 'not supplied'}; displayed age ${text(g.age) || rowValue('Galaxy age') || 'not supplied'}; physical size ${text(g.physical_size) || rowValue('Physical size') || 'not supplied'}; magnitude ${text(g.magnitude) || rowValue('Magnitude') || 'not supplied'}.`;
  }

  async function copyWithoutReplacingPanel(event) {
    event?.preventDefault?.();
    event?.stopPropagation?.();
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

    const button = document.getElementById('viewer40Copy');
    const label = button?.querySelector('span:last-child');
    if (label) {
      label.textContent = 'Copied';
      setTimeout(() => { label.textContent = 'Copy'; }, 900);
    }
  }

  window.viewer40CopyPrompt = copyWithoutReplacingPanel;
  window.viewer37CopyPrompt = copyWithoutReplacingPanel;

  const copyIcon = `<svg class="viewer40-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="7" width="11" height="13" rx="2" fill="#ffffff" stroke="#15243d" stroke-width="1.7"/><rect x="5" y="4" width="11" height="13" rx="2" fill="#d9e8ff" stroke="#15243d" stroke-width="1.7"/></svg>`;
  const chromeIcon = `<svg class="viewer40-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="#ea4335" d="M12 2a10 10 0 0 1 8.66 5H12a5 5 0 0 0-4.33 2.5L4.78 4.5A9.95 9.95 0 0 1 12 2Z"/><path fill="#fbbc04" d="M4.78 4.5 9.1 12a5 5 0 0 0 2.9 4.58L9.1 21.6A10 10 0 0 1 4.78 4.5Z"/><path fill="#34a853" d="M9.1 21.6 13.43 14a5 5 0 0 0 3.57-4.5h5.77A10 10 0 0 1 9.1 21.6Z"/><circle cx="12" cy="12" r="4" fill="#4285f4" stroke="#ffffff" stroke-width="1.2"/></svg>`;
  const geminiIcon = `<svg class="viewer40-icon" viewBox="0 0 24 24" aria-hidden="true"><defs><linearGradient id="viewer40GeminiGradient" x1="3" y1="21" x2="21" y2="3" gradientUnits="userSpaceOnUse"><stop stop-color="#37b7ff"/><stop offset=".38" stop-color="#7c4dff"/><stop offset=".7" stop-color="#e35bd8"/><stop offset="1" stop-color="#ffc14d"/></linearGradient></defs><path fill="url(#viewer40GeminiGradient)" d="M12 1.6c.75 5.45 4.35 9.05 9.8 9.8-5.45.75-9.05 4.35-9.8 9.8-.75-5.45-4.35-9.05-9.8-9.8 5.45-.75 9.05-4.35 9.8-9.8Z"/></svg>`;
  const chatGPTIcon = `<span class="viewer40-chatgpt-icon" aria-hidden="true"><svg class="viewer40-icon" viewBox="0 0 24 24"><path fill="none" stroke="#111" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" d="M8.2 4.1A4.1 4.1 0 0 1 15 3.7a4.1 4.1 0 0 1 4.6 5.5 4.1 4.1 0 0 1-.4 7 4.1 4.1 0 0 1-6.4 3.9 4.1 4.1 0 0 1-6.8-2.7 4.1 4.1 0 0 1-.3-7.3 4.1 4.1 0 0 1 2.5-6Z"/><path fill="none" stroke="#111" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" d="m8.1 4.3 7.1 4.1v7.2l-6.3 3.7m10.3-10-7.2 4.1-6.3-3.6m.4 7.5v-8l6-3.5 6.9 4"/></svg></span>`;

  function ensureHeader() {
    const root = document.getElementById('viewer14-root');
    const title = root?.querySelector('#viewer14Status .fom-title');
    if (!root || !title) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-40';

    [...title.childNodes].forEach(node => {
      if (node.nodeType === Node.TEXT_NODE && /RANDOM GALAXY FIGURES OF MERIT/i.test(text(node.textContent))) node.remove();
    });
    [...title.querySelectorAll('span')].forEach(span => {
      if (/RANDOM GALAXY FIGURES OF MERIT/i.test(text(span.textContent))) span.remove();
    });

    title.querySelector('.viewer37-title-label')?.remove();
    title.querySelector('.viewer36-title-label')?.remove();
    let label = title.querySelector('.viewer40-title-label');
    if (!label) {
      label = document.createElement('span');
      label.className = 'viewer40-title-label';
      title.prepend(label);
    }
    label.textContent = 'Galaxy Info';

    document.getElementById('viewer29CopyButton')?.remove();
    document.getElementById('viewer29ChromeButton')?.remove();
    document.getElementById('viewer36SearchActions')?.remove();
    document.getElementById('viewer37SearchActions')?.remove();
    document.getElementById('viewer40SearchActions')?.remove();

    const actions = document.createElement('span');
    actions.id = 'viewer40SearchActions';
    actions.className = 'viewer40-search-actions';
    actions.innerHTML = `
      <button id="viewer40Copy" type="button" class="viewer40-action" title="Copy galaxy research prompt">${copyIcon}<span>Copy</span></button>
      <button id="viewer40Chrome" type="button" class="viewer40-action" title="Search Google for this galaxy">${chromeIcon}<span>Search</span></button>
      <button id="viewer40Gemini" type="button" class="viewer40-action" title="Open Gemini app or website with this galaxy prompt">${geminiIcon}<span>Search</span></button>
      <button id="viewer40ChatGPT" type="button" class="viewer40-action" title="Open ChatGPT app or website with this galaxy prompt">${chatGPTIcon}<span>Search</span></button>`;
    title.appendChild(actions);

    document.getElementById('viewer40Copy').onclick = copyWithoutReplacingPanel;
    document.getElementById('viewer40Chrome').onclick = window.viewer37ChromeSearch;
    document.getElementById('viewer40Gemini').onclick = window.viewer37GeminiSearch;
    document.getElementById('viewer40ChatGPT').onclick = window.viewer37ChatGPTSearch;
    return true;
  }

  document.getElementById('viewer40-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer40-style';
  style.textContent = `
    #viewer14Status .fom-title{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
    #viewer14Status .viewer40-title-label{white-space:nowrap;font-size:17px}
    #viewer14Status .viewer40-search-actions{display:flex;align-items:center;gap:7px;margin-left:auto;flex-wrap:wrap}
    #viewer14Status .viewer40-action{
      height:38px!important;min-width:90px!important;padding:6px 10px!important;border-radius:9px!important;
      display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:7px!important;
      font-size:12px!important;font-weight:800!important;white-space:nowrap;color:#fff!important;
      background:linear-gradient(135deg,#184b86 0%,#365fae 48%,#7047ae 100%)!important;
      border:1px solid #73d3ff!important;
      box-shadow:0 3px 11px rgba(54,95,174,.48),inset 0 1px 0 rgba(255,255,255,.20)!important;
    }
    #viewer14Status .viewer40-action:hover{background:linear-gradient(135deg,#2162a8 0%,#4777cf 48%,#875bc9 100%)!important;filter:brightness(1.08)}
    #viewer14Status .viewer40-icon{width:20px;height:20px;display:block;flex:0 0 20px}
    #viewer14Status .viewer40-chatgpt-icon{width:25px;height:25px;border-radius:6px;background:#fff;display:inline-flex;align-items:center;justify-content:center;flex:0 0 25px}
    @media(max-width:760px){#viewer14Status .viewer40-search-actions{width:100%;margin-left:0}#viewer14Status .viewer40-action{flex:1 1 92px;min-width:78px!important}}
  `;
  document.head.appendChild(style);

  ensureHeader();
  const status = document.getElementById('viewer14Status');
  if (status) {
    const observer = new MutationObserver(() => {
      clearTimeout(window.viewer40HeaderTimer);
      window.viewer40HeaderTimer = setTimeout(ensureHeader, 25);
    });
    observer.observe(status, {childList:true, subtree:true});
  }

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      setTimeout(ensureHeader, 50);
      setTimeout(ensureHeader, 220);
      setTimeout(ensureHeader, 600);
    }
  });
  window.addEventListener('focus', () => setTimeout(ensureHeader, 60));
  window.addEventListener('pageshow', () => setTimeout(ensureHeader, 80));

  const timer = setInterval(ensureHeader, 150);
  setTimeout(() => clearInterval(timer), 20000);
})();
'''))
