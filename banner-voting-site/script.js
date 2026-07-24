const grid = document.getElementById('banner-grid');

// Placeholder image paths (replace with actual URLs from your Google Drive later)
const banners = Array.from({ length: 10 }, (_, i) => `assets/banner${i + 1}.jpg`);

banners.forEach((src, index) => {
  const container = document.createElement('div');
  container.className = 'banner';

  const img = document.createElement('img');
  img.src = src;
  img.alt = `Banner ${index + 1}`;

  const label = document.createElement('div');
  label.className = 'banner-label';
  label.innerText = `Banner ${index + 1}`;

  container.appendChild(img);
  container.appendChild(label);
  grid.appendChild(container);
});
