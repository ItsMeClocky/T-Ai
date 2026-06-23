import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """  <!-- Loading Screen -->
  <div id="loadingScreen" class="fixed inset-0 bg-white dark:bg-[#131314] z-[9999] flex items-center justify-center transition-opacity duration-1000 ease-out">
    <img src="t-ai.gif" alt="Loading T-Ai..." class="w-full h-full object-cover">
  </div>"""

new_html = """  <!-- Loading Screen -->
  <div id="loadingScreen" class="fixed inset-0 bg-white dark:bg-[#131314] z-[9999] flex items-center justify-center transition-opacity duration-1000 ease-out">
    <div class="absolute top-12 left-0 right-0 text-center z-10">
      <span id="loadingTime" class="px-5 py-2.5 bg-black/60 backdrop-blur-md rounded-full text-white font-medium shadow-xl text-sm">Tempo stimato: 8s</span>
    </div>
    <img src="t-ai.gif" alt="Loading T-Ai..." class="w-full h-full object-cover">
  </div>"""

content = content.replace(old_html, new_html)

old_js = """  // Loading Screen Logic
  window.addEventListener('load', () => {
    setTimeout(() => {
      const loader = document.getElementById('loadingScreen');
      if (loader) {
        loader.classList.add('opacity-0');
        setTimeout(() => loader.remove(), 1000);
      }
    }, 8000);
  });"""

new_js = """  // Loading Screen Logic
  window.addEventListener('load', () => {
    let timeLeft = 8;
    const timeEl = document.getElementById('loadingTime');
    const loader = document.getElementById('loadingScreen');
    
    const interval = setInterval(() => {
      timeLeft--;
      if (timeEl) timeEl.innerText = `Tempo stimato: ${timeLeft}s`;
      
      if (timeLeft <= 0) {
        clearInterval(interval);
        if (loader) {
          loader.classList.add('opacity-0');
          setTimeout(() => loader.remove(), 1000);
        }
      }
    }, 1000);
  });"""

content = content.replace(old_js, new_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Loader")
