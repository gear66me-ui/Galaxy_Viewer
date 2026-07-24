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

// 🔥 GOOGLE SHEETS INTEGRATION
const SCRIPT_URL = "YOUR_SCRIPT_URL_HERE";

submitBtn.addEventListener('click', async () => {
  if (selectedIndex === null) {
    alert('Please select a banner first');
    return;
  }

  try {
    const response = await fetch(SCRIPT_URL, {
      method: "POST",
      body: JSON.stringify({ banner: selectedIndex }),
      headers: { "Content-Type": "application/json" }
    });

    const result = await response.json();

    if (result.status === "success") {
      alert("Vote submitted successfully!");
    } else {
      alert("Error submitting vote.");
    }

  } catch (err) {
    alert("Network error.");
    console.error(err);
  }
});
