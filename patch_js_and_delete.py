import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Delete Account Button in Settings
# We'll put it right above the "Link Utili" section.
delete_btn = """        <div>
          <button onclick="deleteAccount()" class="w-full px-4 py-2.5 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 font-medium border border-red-200 dark:border-red-900/30 hover:bg-red-100 dark:hover:bg-red-900/40 transition flex items-center justify-center gap-2">
            <i data-lucide="trash-2" class="w-4 h-4"></i> Elimina Account e Dati
          </button>
        </div>"""

content = content.replace('<div>\n          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1.5">Link Utili</label>', delete_btn + '\n        <div>\n          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1.5">Link Utili</label>')

# Insert JS logic at the top of the <script> block
js_logic = """
  // History API Routing for Modals
  window.addEventListener('popstate', (e) => {
    const isSettingsOpen = !document.getElementById('settingsModal').classList.contains('hidden');
    const isCanvasOpen = !document.getElementById('canvasPanel').classList.contains('translate-x-full');
    const isSidebarOpen = !document.getElementById('sidebar').classList.contains('-translate-x-full') && window.innerWidth < 1024;
    
    if (isSettingsOpen) closeSettings(true);
    if (isCanvasOpen) closeCanvasFunc(true);
    if (isSidebarOpen) closeMobileSidebar(true);
  });

  function deleteAccount() {
    if(confirm("Sei sicuro di voler eliminare il tuo account? Tutte le chat e le impostazioni verranno perse per sempre.")) {
      localStorage.clear();
      location.reload();
    }
  }
"""
content = content.replace('const params = new URLSearchParams(window.location.search);', js_logic + '\n  const params = new URLSearchParams(window.location.search);')

# Patch settingsModal opening
content = content.replace('function openSettings() {', 'function openSettings() {\n    history.pushState({ modal: \'settings\' }, \'\');')
content = content.replace('function closeSettings() {', 'function closeSettings(fromPopState=false) {\n    if(!fromPopState) history.back();')

# Patch Canvas opening (named openCanvas or we handle close separately)
# We will patch mobileMenu.onclick and closeMobileSidebar
content = content.replace('mobileMenu.onclick = () => { sidebar.classList.remove(\'-translate-x-full\'); overlay.classList.remove(\'hidden\'); };', 
'mobileMenu.onclick = () => { history.pushState({ modal: \'sidebar\' }, \'\'); sidebar.classList.remove(\'-translate-x-full\'); overlay.classList.remove(\'hidden\'); };')

content = content.replace('function closeMobileSidebar() { sidebar.classList.add(\'-translate-x-full\'); overlay.classList.add(\'hidden\'); }',
'function closeMobileSidebar(fromPopState=false) { if(!fromPopState && window.innerWidth < 1024 && !sidebar.classList.contains("-translate-x-full")) history.back(); sidebar.classList.add(\'-translate-x-full\'); overlay.classList.add(\'hidden\'); }')

# Patch Canvas (openCanvas and Canvas Panel close)
content = content.replace('function openCanvas(initial = \'\', lang = \'markdown\') {', 'function openCanvas(initial = \'\', lang = \'markdown\') {\n    history.pushState({ modal: \'canvas\' }, \'\');')
content = content.replace('$(\'#closeCanvas\').onclick = () => {', 'function closeCanvasFunc(fromPopState=false) { if(!fromPopState) history.back(); canvasPanel.classList.add(\'translate-x-full\'); setTimeout(() => canvasPanel.style.display=\'none\', 300); }\n  $(\'#closeCanvas\').onclick = () => { closeCanvasFunc(); };\n  //')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS Update Done")
