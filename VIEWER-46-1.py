from __future__ import annotations

import urllib.request
from IPython.display import Javascript, display

# VIEWER-46-1
# Immutable working baseline: VIEWER-45 commit a9002326395ea21b6aab0e3968b77c30fcd80741.
# Authorized repairs only: disable broken overlay patches, stabilize title,
# restore Get Info behavior, combine physical/angular size, remove Interest score,
# and normalize the yellow-row font size and concise age text.

# Prevent the unstable post-viewer overlays from installing while preserving the
# working VIEWER-45 / VIEWER-41 viewer foundation and its original Get Info path.
display(Javascript(r'''
(() => {
  window['viewer42-bridge12-patch'] = true;
  window['viewer43-size-row-patch'] = true;
  window['viewer44-age-font-patch'] = true;
  window['viewer45-remove-interest-score'] = true;
  window.viewer46FinalTitle = 'Galaxy Viewer — VIEWER-46-1';
})();
'''))

BASE_URL = "https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/a9002326395ea21b6aab0e3968b77c30fcd80741/VIEWER-45.py"
with urllib.request.urlopen(BASE_URL, timeout=60) as response:
    source = response.read().decode("utf-8")
exec(compile(source, "VIEWER-45-immutable-base.py", "exec"))


display(Javascript(r'''
(() => {
  const PATCH_ID = 'viewer46-controlled-repair';
  if (window[PATCH_ID]) return;
  window[PATCH_ID] = true;

  const YELLOW = '#ffd84d';

  function clean(v){ return String(v ?? '').replace(/\s+/g,' ').trim(); }
  function status(){ return document.getElementById('viewer14Status'); }
  function rows(){ return [...(status()?.querySelectorAll('tr') || [])]; }
  function label(row){ return clean(row?.querySelector('th')?.textContent); }
  function rowBy(...names){
    const wanted = names.map(x => clean(x).toLowerCase());
    return rows().find(row => wanted.includes(label(row).toLowerCase()));
  }

  function installTitle(){
    const title = window.viewer46FinalTitle || 'Galaxy Viewer — VIEWER-46-1';
    let style = document.getElementById('viewer46TitleStyle');
    if(!style){
      style = document.createElement('style');
      style.id = 'viewer46TitleStyle';
      document.head.appendChild(style);
    }
    style.textContent = `#viewer14-root h3{font-size:0!important}#viewer14-root h3::after{content:"${title}";font-size:22px!important;color:#35c6ff!important}`;
  }

  function conciseAge(text){
    const value = clean(text);
    const match = value.match(/approximately\s+([0-9]+(?:\.[0-9]+)?)\s+billion\s+years/i);
    return match ? `Approximately ${match[1]} billion years` : value;
  }

  function normalFontSize(){
    const normal = rows().find(row => {
      const name = label(row).toLowerCase();
      return name && !['galaxy age','redshift (z) / distance','redshift / distance'].includes(name);
    });
    const cell = normal?.querySelector('td') || normal?.querySelector('th');
    return cell ? getComputedStyle(cell).fontSize : '16px';
  }

  function combineSizeRows(){
    const angular = rowBy('Angular size');
    const physical = rowBy('Physical size');
    let combined = rowBy('Physical size / Angular size','Physical / angular size');
    const radial = rowBy('Radial velocity');

    if(!combined && (angular || physical)) combined = physical || angular;
    if(!combined) return;

    const th = combined.querySelector('th');
    const td = combined.querySelector('td');
    const angularText = clean(angular?.querySelector('td')?.textContent);
    const physicalText = clean(physical?.querySelector('td')?.textContent);
    const existing = clean(td?.textContent);

    let next = existing;
    if(physicalText && angularText && physical !== angular) next = `${physicalText} / ${angularText}`;
    else if(!existing.includes(' / ')) {
      if(physicalText && angularText) next = `${physicalText} / ${angularText}`;
      else if(physicalText) next = physicalText;
      else if(angularText) next = angularText;
    }

    if(th && clean(th.textContent) !== 'Physical size / Angular size') th.textContent = 'Physical size / Angular size';
    if(td && next && clean(td.textContent) !== next) td.textContent = next;

    if(angular && angular !== combined) angular.remove();
    if(physical && physical !== combined) physical.remove();
    if(radial && combined.nextElementSibling !== radial) radial.parentNode.insertBefore(combined, radial);
  }

  function apply(){
    const table = status();
    if(!table) { installTitle(); return false; }

    rows().forEach(row => {
      if(label(row).toLowerCase() === 'interest score') row.remove();
    });

    combineSizeRows();

    const age = rowBy('Galaxy age');
    const ageCell = age?.querySelector('td');
    if(ageCell){
      const next = conciseAge(ageCell.textContent);
      if(next && clean(ageCell.textContent) !== next) ageCell.textContent = next;
    }

    const size = normalFontSize();
    ['Galaxy age','Redshift (z) / Distance','Redshift / Distance'].forEach(name => {
      const row = rowBy(name);
      if(!row) return;
      row.classList.remove('emphasis');
      [row.querySelector('th'), row.querySelector('td')].forEach(cell => {
        if(!cell) return;
        cell.style.setProperty('color', YELLOW, 'important');
        cell.style.setProperty('font-size', size, 'important');
        cell.style.setProperty('line-height', 'normal', 'important');
      });
    });

    installTitle();
    return true;
  }

  apply();
  const target = status();
  if(target){
    const observer = new MutationObserver(() => {
      clearTimeout(window.viewer46ApplyTimer);
      window.viewer46ApplyTimer = setTimeout(apply, 80);
    });
    observer.observe(target, {childList:true, subtree:true, characterData:true});
    window.viewer46Observer = observer;
  }
  window.viewer46Guard = setInterval(apply, 500);
})();
'''))
