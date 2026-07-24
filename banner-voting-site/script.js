const grid = document.getElementById('banner-grid');

for (let i = 1; i <= 10; i++) {
  const div = document.createElement('div');
  div.className = 'banner';
  div.innerText = `Banner ${i}`;
  grid.appendChild(div);
}
