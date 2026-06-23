import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

loader_html = """
  <!-- Loading Screen -->
  <div id="loadingScreen" class="fixed inset-0 bg-white dark:bg-[#131314] z-[9999] flex items-center justify-center transition-opacity duration-1000 ease-out">
    <img src="t-ai.gif" alt="Loading T-Ai..." class="w-full h-full object-cover">
  </div>
"""

content = content.replace(
    '<body class="h-screen overflow-hidden bg-white dark:bg-[#131314] text-[#1f1f1f] dark:text-[#e3e3e3] antialiased">',
    '<body class="h-screen overflow-hidden bg-white dark:bg-[#131314] text-[#1f1f1f] dark:text-[#e3e3e3] antialiased">\n' + loader_html
)

loader_js = """
  // Loading Screen Logic
  window.addEventListener('load', () => {
    setTimeout(() => {
      const loader = document.getElementById('loadingScreen');
      if (loader) {
        loader.classList.add('opacity-0');
        setTimeout(() => loader.remove(), 1000);
      }
    }, 8000);
  });
"""

content = content.replace(
    '  // Bottom Sheet Logic',
    loader_js + '\n  // Bottom Sheet Logic'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added Loader")
