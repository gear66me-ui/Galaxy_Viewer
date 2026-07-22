from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-36.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-36-base.py", "exec"))


display(Javascript(r'''
(() => {
  const chatGPTIcon = `
    <span class="viewer37-chatgpt-badge" aria-hidden="true">
      <svg class="viewer37-chatgpt-icon" viewBox="0 0 24 24">
        <path fill="none" stroke="#000" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M8.2 4.1A4.1 4.1 0 0 1 15 3.7a4.1 4.1 0 0 1 4.6 5.5 4.1 4.1 0 0 1-.4 7 4.1 4.1 0 0 1-6.4 3.9 4.1 4.1 0 0 1-6.8-2.7 4.1 4.1 0 0 1-.3-7.3 4.1 4.1 0 0 1 2.5-6Z"/>
        <path fill="none" stroke="#000" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="m8.1 4.3 7.1 4.1v7.2l-6.3 3.7m10.3-10-7.2 4.1-6.3-3.6m.4 7.5v-8l6-3.5 6.9 4"/>
      </svg>
    </span>`;

  const geminiIcon = `
    <svg class="viewer37-gemini-icon" viewBox="0 0 24 24" aria-hidden="true">
      <defs>
        <linearGradient id="viewer37GeminiGradient" x1="2" y1="22" x2="22" y2="2" gradientUnits="userSpaceOnUse">
          <stop offset="0" stop-color="#4c6fff"/>
          <stop offset="0.35" stop-color="#7b61ff"/>
          <stop offset="0.68" stop-color="#c45cff"/>
          <stop offset="1" stop-color="#ff78b6"/>
        </linearGradient>
      </defs>
      <path fill="url(#viewer37GeminiGradient)" d="M12 1.5c.75 5.35 4.15 8.75 9.5 9.5-5.35.75-8.75 4.15-9.5 9.5-.75-5.35-4.15-8.75-9.5-9.5 5.35-.75 8.75-4.15 9.5-9.5Z"/>
    </svg>`;

  function installViewer37() {
    const root = document.getElementById('viewer14-root');
    const chatGPTButton = document.getElementById('viewer36ChatGPTSearch');
    const geminiButton = document.getElementById('viewer36GeminiSearch');
    if (!root || !chatGPTButton || !geminiButton) return false;

    const heading = root.querySelector('h3');
    if (heading) heading.textContent = 'Galaxy Viewer — VIEWER-37';

    chatGPTButton.innerHTML = `${chatGPTIcon}<span>Search</span>`;
    geminiButton.innerHTML = `${geminiIcon}<span>Search</span>`;
    return true;
  }

  document.getElementById('viewer37-style')?.remove();
  const style = document.createElement('style');
  style.id = 'viewer37-style';
  style.textContent = `
    #viewer14Status .viewer37-chatgpt-badge{
      width:20px;height:20px;display:inline-flex;align-items:center;justify-content:center;
      flex:0 0 20px;background:#fff;border-radius:50%;box-shadow:0 0 0 1px rgba(0,0,0,.18);
    }
    #viewer14Status .viewer37-chatgpt-icon{width:16px;height:16px;display:block}
    #viewer14Status .viewer37-gemini-icon{width:19px;height:19px;display:block;flex:0 0 19px}
  `;
  document.head.appendChild(style);

  installViewer37();
  const timer = setInterval(() => {
    if (installViewer37()) clearInterval(timer);
  }, 120);
  setTimeout(() => {
    installViewer37();
    clearInterval(timer);
  }, 16000);
})();
'''))
