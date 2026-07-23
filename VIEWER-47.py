from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-47
# Locked base: reviewed VIEWER-46 final.
# Authorized change only: add the supplied galaxy image unchanged as the viewer header.
BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/main/VIEWER-46.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-46-base.py", "exec"))


display(Javascript(r'''
(() => {
  const HEADER_ID = 'viewer47GalaxyHeader';
  const STYLE_ID = 'viewer47GalaxyHeaderStyle';
  const IMAGE_URL = 'https://drive.google.com/uc?export=view&id=15gFwfeIxJtBDFrrEKg5R8F_HzDyHJWE2';

  function install(){
    const root = document.getElementById('viewer14-root');
    if(!root) return false;

    let style = document.getElementById(STYLE_ID);
    if(!style){
      style = document.createElement('style');
      style.id = STYLE_ID;
      document.head.appendChild(style);
    }
    style.textContent = `
      #viewer14-root > h3{display:none!important}
      #${HEADER_ID}{
        position:relative;
        width:100%;
        margin:0 0 14px 0;
        border:1px solid #137aa3;
        border-radius:10px;
        overflow:hidden;
        background:#000;
        box-sizing:border-box;
      }
      #${HEADER_ID} img{
        display:block;
        width:100%;
        height:auto;
        object-fit:contain;
        object-position:center;
        margin:0;
        padding:0;
        border:0;
      }
      #${HEADER_ID} .viewer47-title{
        position:absolute;
        inset:0;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#eefcff;
        font-family:"Arial Narrow",Arial,Helvetica,sans-serif;
        font-size:clamp(30px,6vw,78px);
        font-weight:300;
        letter-spacing:.28em;
        line-height:1;
        text-align:center;
        text-indent:.28em;
        text-shadow:0 0 7px #ffffff,0 0 15px #7fdbff,0 0 28px rgba(127,219,255,.75);
        white-space:nowrap;
        pointer-events:none;
      }
      @media(max-width:700px){
        #${HEADER_ID} .viewer47-title{
          font-size:clamp(22px,7vw,46px);
          letter-spacing:.18em;
          text-indent:.18em;
        }
      }
    `;

    let header = document.getElementById(HEADER_ID);
    if(!header){
      header = document.createElement('div');
      header.id = HEADER_ID;
      header.innerHTML = `<img src="${IMAGE_URL}" alt="Galaxy Viewer header"><div class="viewer47-title">GALAXY VIEWER</div>`;
      root.insertBefore(header, root.firstChild);
    }

    document.title = 'Galaxy Viewer — VIEWER-47';
    return true;
  }

  install();
  const timer = setInterval(() => {
    if(install()) clearInterval(timer);
  }, 250);
  setTimeout(() => clearInterval(timer), 20000);
})();
'''))
