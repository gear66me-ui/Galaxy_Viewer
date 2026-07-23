from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# GALAXY-VIEWER-ALADIN-CLASSIC-LOCK
# Immutable functional core: reviewed VIEWER-46-4 commit.
CORE_URL = (
    "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/"
    "7faf2b22a47244e3fa1b74fdb7b6602d4758fd53/VIEWER-46-4.py"
)
with urllib.request.urlopen(CORE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-46-4-locked-core.py", "exec"))

# Lock only the Aladin control presentation to the compact white interface.
display(Javascript(r'''
(() => {
  const STYLE_ID = 'galaxyViewerAladinClassicLock';
  let style = document.getElementById(STYLE_ID);
  if(!style){
    style = document.createElement('style');
    style.id = STYLE_ID;
    document.head.appendChild(style);
  }
  style.textContent = `
    #viewer14-aladin .aladin-btn,
    #viewer14-aladin .aladin-input-text,
    #viewer14-aladin .aladin-input-select,
    #viewer14-aladin .aladin-location,
    #viewer14-aladin .aladin-cooFrame,
    #viewer14-aladin .aladin-fov,
    #viewer14-aladin .aladin-projection-control,
    #viewer14-aladin .aladin-fullScreen-control {
      color:#fff !important;
      border-color:rgba(255,255,255,.92) !important;
      background:#050505 !important;
      box-shadow:none !important;
      font-family:monospace !important;
      font-weight:400 !important;
    }
    #viewer14-aladin .aladin-btn {
      padding:.16rem .22rem !important;
      border-width:1px !important;
      border-radius:3px !important;
      line-height:1.15 !important;
    }
    #viewer14-aladin .aladin-input-text,
    #viewer14-aladin .aladin-input-select {
      padding:.20rem .34rem !important;
      border-width:1px !important;
      border-radius:3px !important;
      line-height:1.15 !important;
    }
    #viewer14-aladin .aladin-location .aladin-input-text {
      width:12.5rem !important;
    }
    #viewer14-aladin .aladin-small-sized-icon {width:1.05rem !important;height:1.05rem !important;}
    #viewer14-aladin .aladin-medium-sized-icon {width:1.32rem !important;height:1.32rem !important;}
    #viewer14-aladin .aladin-medium-sized {height:1.32rem !important;}
    #viewer14-aladin .aladin-small-sized {height:1.05rem !important;}
    #viewer14-aladin [data-theme=dark] .aladin-icon.aladin-icon-monochrome img,
    #viewer14-aladin .aladin-icon.aladin-icon-monochrome img {
      filter:brightness(0) invert(1) !important;
    }
    #viewer14-aladin .aladin-widgets-toolbar {margin-top:2.35rem !important;}
    #viewer14-aladin .aladin-location {top:.16rem !important;left:3.8rem !important;}
    #viewer14-aladin .aladin-cooFrame {top:.16rem !important;left:.16rem !important;}
    #viewer14-aladin .aladin-fullScreen-control {top:.16rem !important;right:.16rem !important;}
    #viewer14-aladin .aladin-projection-control {top:.16rem !important;right:2.25rem !important;}
  `;
})();
'''))
