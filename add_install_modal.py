import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace "Installa T-Ai" link with button
old_install_btn_regex = r'<a href="https://install-t-ai\.netlify\.app" target="_blank" rel="noopener noreferrer"\s*class="w-full flex items-center gap-3 bg-gradient-to-r from-\[#1a73e8\] to-\[#8b5cf6\] hover:opacity-90 text-white rounded-full py-3 px-4 transition shadow-sm">\s*<i data-lucide="download-cloud" class="w-5 h-5 shrink-0"></i>\s*<span class="sidebar-text text- font-medium">Installa T-Ai</span>\s*</a>'

new_install_btn = """<button onclick="openInstallModal()" class="w-full flex items-center gap-3 bg-gradient-to-r from-[#1a73e8] to-[#8b5cf6] hover:opacity-90 text-white rounded-full py-3 px-4 transition shadow-sm">
    <i data-lucide="download-cloud" class="w-5 h-5 shrink-0"></i>
    <span class="sidebar-text font-medium">Installa T-Ai</span>
  </button>"""

content = re.sub(old_install_btn_regex, new_install_btn, content, flags=re.DOTALL)

# 2. Add installModal HTML
install_modal_html = """
  <!-- Install Modal -->
  <div id="installModal" class="fixed inset-0 bg-black/40 z-[90] hidden items-center justify-center p-4 transition-opacity opacity-0 duration-300" onclick="if(event.target===this) closeInstallModal()">
    <div class="bg-white dark:bg-[#131314] rounded-3xl shadow-2xl w-full max-w-[500px] overflow-hidden transform scale-95 transition-transform duration-300 border border-[#e5e7eb] dark:border-[#2f3032] flex flex-col max-h-[85vh]">
      <div class="flex items-center justify-between p-5 border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <h2 class="text-lg font-semibold flex items-center gap-2">
          <i data-lucide="download-cloud" class="w-5 h-5 text-[#1a73e8]"></i> Installa T-Ai
        </h2>
        <button onclick="closeInstallModal()" class="p-2 hover:bg-[#f0f4f9] dark:hover:bg-[#2a2b2f] rounded-full transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      
      <div class="flex border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <button onclick="switchInstallTab('pc')" id="tab-pc" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition">PC / Mac</button>
        <button onclick="switchInstallTab('android')" id="tab-android" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition">Android</button>
        <button onclick="switchInstallTab('ios')" id="tab-ios" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition">iOS / iPad</button>
      </div>

      <div class="p-6 overflow-y-auto">
        <!-- PC Tab -->
        <div id="content-pc" class="install-content hidden space-y-4">
          <p class="text-[14px] text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed">
            Trasforma T-Ai in un'app desktop a tutti gli effetti, identica ad una vera app per <strong>Linux (KDE Plasma)</strong>, <strong>Windows</strong> o <strong>macOS</strong>. Non perderai mai il collegamento!
          </p>
          <ul class="space-y-3 text-[14px]">
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
              <span>Apri T-Ai usando <strong>Chrome</strong> o <strong>Edge</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Clicca sull'icona di installazione (una piccola icona a forma di monitor o app) situata all'estrema destra della barra degli indirizzi. <br><br><em>Oppure: Clicca i tre puntini del menu in alto a destra ➔ "Salva e condividi" ➔ "Installa pagina come app".</em></span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Conferma cliccando su <strong>Installa</strong>. Troverai T-Ai nel menu delle tue applicazioni!</span>
            </li>
          </ul>
        </div>

        <!-- Android Tab -->
        <div id="content-android" class="install-content hidden space-y-4">
          <p class="text-[14px] text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed">
            Aggiungi T-Ai alla tua schermata Home per usarla come un'app nativa a tutto schermo, velocissima e sempre a portata di dito.
          </p>
          <ul class="space-y-3 text-[14px]">
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
              <span>Apri T-Ai tramite il browser <strong>Google Chrome</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Tocca i tre puntini <i data-lucide="more-vertical" class="w-4 h-4 inline-block"></i> in alto a destra per aprire il menu.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Tocca <strong>"Aggiungi a schermata Home"</strong> (o "Installa app").</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Conferma. Troverai l'icona di T-Ai insieme alle tue altre app!</span>
            </li>
          </ul>
        </div>

        <!-- iOS Tab -->
        <div id="content-ios" class="install-content hidden space-y-4">
          <p class="text-[14px] text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed">
            Usa T-Ai su iPhone e iPad a tutto schermo, senza la barra di ricerca del browser in mezzo.
          </p>
          <ul class="space-y-3 text-[14px]">
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
              <span>Apri T-Ai utilizzando <strong>Safari</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Tocca l'icona <strong>Condividi</strong> in basso (il quadrato con la freccia rivolta verso l'alto).</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Scorri il menu verso il basso e tocca <strong>"Aggiungi alla schermata Home"</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Tocca <strong>"Aggiungi"</strong> in alto a destra. Fatto!</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
"""

# Insert modal HTML right before auth/login screen
auth_idx = content.find('<!-- Auth/Login Screen -->')
if auth_idx != -1:
    content = content[:auth_idx] + install_modal_html + content[auth_idx:]

# 3. Add JS logic right before the last </script>
install_js = """
  // Install Modal Logic
  window.openInstallModal = function() {
    const modal = document.getElementById('installModal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    // popstate
    history.pushState({ modal: 'install' }, '', '');
    
    // Auto detect OS
    const ua = navigator.userAgent.toLowerCase();
    let target = 'pc';
    if (/iphone|ipad|ipod/.test(ua)) target = 'ios';
    else if (/android/.test(ua)) target = 'android';
    
    switchInstallTab(target);

    // animate in
    void modal.offsetWidth;
    modal.classList.remove('opacity-0');
    modal.querySelector('div').classList.remove('scale-95');
  };

  window.closeInstallModal = function() {
    const modal = document.getElementById('installModal');
    if(!modal || modal.classList.contains('hidden')) return;
    
    modal.classList.add('opacity-0');
    modal.querySelector('div').classList.add('scale-95');
    setTimeout(() => {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }, 300);
  };

  window.switchInstallTab = function(target) {
    document.querySelectorAll('.install-tab').forEach(t => {
      t.classList.remove('border-[#1a73e8]', 'text-[#1a73e8]', 'dark:text-[#8ab4f8]');
      t.classList.add('border-transparent');
    });
    document.querySelectorAll('.install-content').forEach(c => c.classList.add('hidden'));
    
    const tab = document.getElementById('tab-' + target);
    const content = document.getElementById('content-' + target);
    if(tab && content) {
      tab.classList.remove('border-transparent');
      tab.classList.add('border-[#1a73e8]', 'text-[#1a73e8]', 'dark:text-[#8ab4f8]');
      content.classList.remove('hidden');
    }
  };

  // Add history back handling for install modal
  window.addEventListener('popstate', (e) => {
    closeInstallModal();
  });
"""

parts = content.rsplit('</script>', 1)
content = parts[0] + install_js + '\n</script>' + parts[1]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Install Modal Integration Complete!")
