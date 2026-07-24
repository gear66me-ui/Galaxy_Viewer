const grid = document.getElementById('banner-grid');
const submitBtn = document.getElementById('submit-btn');

let selectedIndex = null;

const banners = Array.from({ length: 10 }, (_, i) => `assets/banner${i + 1}.jpg`);

banners.forEach((src, index) => {
  const container = document.createElement('div');
  container.className = 'banner';

  const img = document.createElement('img');
  img.src = src;
  img.alt = `Banner ${index + 1}`;

  container.appendChild(img);

  container.addEventListener('click', () => {
    document.querySelectorAll('.banner').forEach(b => b.classList.remove('selected'));
    container.classList.add('selected');
    selectedIndex = index + 1;
  });

  grid.appendChild(container);
});

submitBtn.addEventListener('click', () => {
  if (selectedIndex === null) {
    alert('Please select a banner first');
    return;
  }

  alert(`You voted for Banner ${selectedIndex}`);
});
