from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-36.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-36-base.py", "exec"))


display(Javascript(r'''
(() => {
  function text(v){ return String(v ?? '').trim(); }
  function currentName(){
    const g=window.viewer30CurrentGalaxy||window.viewer27LastDisplayedGalaxy||{};
    if(text(g.name)) return text(g.name);
    const row=[...(document.querySelectorAll('#viewer14Status tr')||[])].find(r=>/^object$/i.test(text(r.querySelector('th')?.textContent)));
    return text(row?.querySelector('td')?.textContent)||'galaxy';
  }
  function prompt(){
    const name=currentName();
    return `Search the web for reliable information about ${name}. Give galaxy type, distance, redshift, radial velocity, apparent magnitude, angular size, physical size, stellar-population age or best-supported age estimate, discovery/history, and why it is scientifically or visually interesting. Clearly separate measured values from estimates and cite authoritative astronomy sources.`;
  }
  async function copyPrompt(p){ try{ await navigator.clipboard.writeText(p); }catch(_){ } }
  function appShareIntent(pkg,p){
    return `intent:#Intent;action=android.intent.action.SEND;type=text/plain;package=${pkg};S.android.intent.extra.TEXT=${encodeURIComponent(p)};end`;
  }
  function launch(appUrl,webUrl){
    let hidden=false;
    const mark=()=>{hidden=true};
    document.addEventListener('visibilitychange',mark,{once:true});
    window.location.href=appUrl;
    setTimeout(()=>{ if(!hidden&&!document.hidden) window.open(webUrl,'_blank','noopener,noreferrer'); },1100);
  }
  window.viewer37ChatGPTSearch=async()=>{const p=prompt();await copyPrompt(p);launch(appShareIntent('com.openai.chatgpt',p),'https://chatgpt.com/');};
  window.viewer37GeminiSearch=async()=>{const p=prompt();await copyPrompt(p);launch(appShareIntent('com.google.android.apps.bard',p),'https://gemini.google.com/app');};

  const icons={
    chatgpt:`<svg class="v37i" viewBox="0 0 24 24"><path fill="none" stroke="#000" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M8.2 4.1A4.1 4.1 0 0 1 15 3.7a4.1 4.1 0 0 1 4.6 5.5 4.1 4.1 0 0 1-.4 7 4.1 4.1 0 0 1-6.4 3.9 4.1 4.1 0 0 1-6.8-2.7 4.1 4.1 0 0 1-.3-7.3 4.1 4.1 0 0 1 2.5-6Z"/><path fill="none" stroke="#000" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="m8.1 4.3 7.1 4.1v7.2l-6.3 3.7m10.3-10-7.2 4.1-6.3-3.6m.4 7.5v-8l6-3.5 6.9 4"/></svg>`,
    gemini:`<svg class="v37i" viewBox="0 0 24 24"><defs><linearGradient id="g37" x1="3" y1="21" x2="21" y2="3"><stop stop-color="#4285f4"/><stop offset=".38" stop-color="#7c4dff"/><stop offset=".7" stop-color="#d946ef"/><stop offset="1" stop-color="#ff8a65"/></linearGradient></defs><path fill="url(#g37)" d="M12 1.6c.75 5.25 4.15 8.65 9.4 9.4-5.25.75-8.65 4.15-9.4 9.4-.75-5.25-4.15-8.65-9.4-9.4 5.25-.75 8.65-4.15 9.4-9.4Z"/></svg>`,
    chrome:`<svg class="v37i" viewBox="0 0 24 24"><path fill="#ea4335" d="M12 2a10 10 0 0 1 8.66 5H12a5 5 0 0 0-4.33 2.5L4.78 4.5A9.96 9.96 0 0 1 12 2Z"/><path fill="#fbbc05" d="M20.66 7A10 10 0 0 1 14.5 21.68l4.33-7.5A5 5 0 0 0 12 7h8.66Z"/><path fill="#34a853" d="M14.5 21.68A10 10 0 0 1 4.78 4.5l4.33 7.5A5 5 0 0 0 14.5 16.5v5.18Z"/><circle cx="12" cy="12" r="4" fill="#4285f4"/></svg>`,
    copy:`<svg class="v37i" viewBox="0 0 24 24"><rect x="8" y="7" width="11" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M16 7V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h3" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>`
  };
  function decorate(id,icon,label,handler){const b=document.getElementById(id);if(!b)return;b.innerHTML=`${icons[icon]}<span>${label}</span>`;if(handler)b.onclick=handler;}
  function install(){
    const root=document.getElementById('viewer14-root'); if(!root)return false;
    const h=root.querySelector('h3'); if(h)h.textContent='Galaxy Viewer — VIEWER-37';
    decorate('viewer36ChatGPTSearch','chatgpt','Search',window.viewer37ChatGPTSearch);
    decorate('viewer36GeminiSearch','gemini','Search',window.viewer37GeminiSearch);
    decorate('viewer29ChromeButton','chrome','Chrome Search');
    decorate('viewer29CopyButton','copy','Copy');
    return true;
  }
  document.getElementById('viewer37-style')?.remove();
  const s=document.createElement('style');s.id='viewer37-style';s.textContent=`
  #viewer14Status .v37i{width:18px;height:18px;display:block;flex:0 0 18px}
  #viewer14Status #viewer36ChatGPTSearch,#viewer14Status #viewer36GeminiSearch,#viewer14Status #viewer29ChromeButton,#viewer14Status #viewer29CopyButton{display:inline-flex!important;align-items:center!important;gap:7px!important;padding:7px 11px!important;border-radius:9px!important;font-size:13px!important;font-weight:800!important;box-shadow:0 2px 7px rgba(0,0,0,.28)!important}
  #viewer14Status #viewer36ChatGPTSearch{background:#fff!important;color:#000!important;border:1px solid #d5d5d5!important}
  #viewer14Status #viewer36GeminiSearch{background:linear-gradient(135deg,#eef4ff,#f7efff 50%,#fff3fb)!important;color:#3b3b65!important;border:1px solid #b9c7ff!important}
  #viewer14Status #viewer29ChromeButton{background:#fff!important;color:#202124!important;border:1px solid #dadce0!important}
  #viewer14Status #viewer29CopyButton{background:#173f55!important;color:#dff7ff!important;border:1px solid #35c6ff!important}`;document.head.appendChild(s);
  install();const t=setInterval(install,150);setTimeout(()=>clearInterval(t),16000);
})();
'''))
