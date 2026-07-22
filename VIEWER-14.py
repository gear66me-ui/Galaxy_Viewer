from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/66a47b63b85b648648e52001441534edc9462114/VIEWER-14.py"

with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")

compile(source, "VIEWER-14-base.py", "exec")
exec(compile(source, "VIEWER-14-base.py", "exec"))

display(Javascript(r"""
(() => {
  const labels = {
    interesting: "Interesting Mix — 70% interesting / 30% random",
    all: "All Catalogs — equal random",
    Arp: "Arp peculiar galaxies",
    RC3: "RC3 bright galaxies",
    HyperLEDA: "HyperLEDA deep random"
  };

  const install = () => {
    const select = document.getElementById("viewer14CatalogMode");
    if (!select) return false;
    if (document.getElementById("viewer14CatalogButton")) return true;

    select.style.display = "none";

    const wrap = document.createElement("div");
    wrap.id = "viewer14CatalogMenuWrap";
    wrap.style.position = "relative";
    wrap.style.display = "inline-block";
    wrap.style.minWidth = "360px";

    const button = document.createElement("button");
    button.type = "button";
    button.id = "viewer14CatalogButton";
    button.textContent = (labels[select.value] || labels.interesting) + " ▾";
    button.style.width = "100%";
    button.style.textAlign = "left";
    button.style.background = "#000";
    button.style.color = "#7FDBFF";
    button.style.border = "1px solid #169ac7";
    button.style.borderRadius = "8px";
    button.style.padding = "12px";
    button.style.fontSize = "16px";
    button.style.fontWeight = "400";

    const menu = document.createElement("div");
    menu.id = "viewer14CatalogMenu";
    menu.style.display = "none";
    menu.style.position = "absolute";
    menu.style.left = "0";
    menu.style.right = "0";
    menu.style.top = "calc(100% + 4px)";
    menu.style.zIndex = "999999";
    menu.style.background = "#000";
    menu.style.border = "1px solid #169ac7";
    menu.style.borderRadius = "8px";
    menu.style.overflow = "hidden";
    menu.style.boxShadow = "0 8px 24px rgba(0,0,0,.75)";

    Object.entries(labels).forEach(([value, label]) => {
      const option = document.createElement("button");
      option.type = "button";
      option.textContent = label;
      option.style.display = "block";
      option.style.width = "100%";
      option.style.textAlign = "left";
      option.style.background = "#000";
      option.style.color = "#7FDBFF";
      option.style.border = "0";
      option.style.borderBottom = "1px solid #0b526f";
      option.style.borderRadius = "0";
      option.style.padding = "12px";
      option.style.fontSize = "16px";
      option.style.fontWeight = "400";
      option.addEventListener("click", event => {
        event.stopPropagation();
        select.value = value;
        select.dispatchEvent(new Event("change", {bubbles: true}));
        button.textContent = label + " ▾";
        menu.style.display = "none";
      });
      menu.appendChild(option);
    });

    button.addEventListener("click", event => {
      event.stopPropagation();
      menu.style.display = menu.style.display === "block" ? "none" : "block";
    });

    document.addEventListener("click", () => {
      menu.style.display = "none";
    });

    select.parentNode.insertBefore(wrap, select.nextSibling);
    wrap.appendChild(button);
    wrap.appendChild(menu);
    return true;
  };

  if (!install()) {
    const timer = setInterval(() => {
      if (install()) clearInterval(timer);
    }, 100);
    setTimeout(() => clearInterval(timer), 10000);
  }
})();
"""))
