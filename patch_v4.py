import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Mock Google and Meta Auth
mock_js = '''
  window.handleGoogleLogin = function() {
    const btn = document.getElementById('googleAuthBtn');
    if (!btn) return;
    
    if (localStorage.getItem('googleAuth') === 'true') {
        localStorage.removeItem('googleAuth');
        updateGoogleAuthUI();
        return;
    }

    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Connessione...`;
    if(window.lucide) lucide.createIcons();
    
    setTimeout(() => {
      localStorage.setItem('googleAuth', 'true');
      updateGoogleAuthUI();
    }, 1000);
  };

  window.updateGoogleAuthUI = function() {
    const statusIcon = document.getElementById('googleAuthStatusIcon');
    const statusText = document.getElementById('googleAuthStatusText');
    const btn = document.getElementById('googleAuthBtn');
    if(!statusIcon || !statusText || !btn) return;
    
    if(localStorage.getItem('googleAuth') === 'true') {
      statusIcon.classList.remove('bg-red-500');
      statusIcon.classList.add('bg-green-500');
      statusText.textContent = 'Connesso';
      statusText.classList.remove('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      statusText.classList.add('text-green-600', 'dark:text-green-400');
      btn.innerHTML = '<i data-lucide="unlink" class="w-3 h-3"></i> Scollega';
    } else {
      statusIcon.classList.remove('bg-green-500');
      statusIcon.classList.add('bg-red-500');
      statusText.textContent = 'Non connesso';
      statusText.classList.remove('text-green-600', 'dark:text-green-400');
      statusText.classList.add('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      btn.innerHTML = 'Collega T-Clockwork a <svg class="w-4 h-4 inline-block" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>';
    }
    if(window.lucide) lucide.createIcons();
  };

  window.handleMetaLogin = function() {
    const btn = document.getElementById('metaAuthBtn');
    if (!btn) return;

    if (localStorage.getItem('metaAuth') === 'true') {
        localStorage.removeItem('metaAuth');
        updateMetaAuthUI();
        return;
    }

    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Connessione...`;
    if(window.lucide) lucide.createIcons();
    
    setTimeout(() => {
      localStorage.setItem('metaAuth', 'true');
      updateMetaAuthUI();
    }, 1000);
  };

  window.updateMetaAuthUI = function() {
    const statusIcon = document.getElementById('metaAuthStatusIcon');
    const statusText = document.getElementById('metaAuthStatusText');
    const btn = document.getElementById('metaAuthBtn');
    if(!statusIcon || !statusText || !btn) return;
    
    if(localStorage.getItem('metaAuth') === 'true') {
      statusIcon.classList.remove('bg-red-500');
      statusIcon.classList.add('bg-green-500');
      statusText.textContent = 'Connesso';
      statusText.classList.remove('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      statusText.classList.add('text-green-600', 'dark:text-green-400');
      btn.innerHTML = '<i data-lucide="unlink" class="w-3 h-3"></i> Scollega';
    } else {
      statusIcon.classList.remove('bg-green-500');
      statusIcon.classList.add('bg-red-500');
      statusText.textContent = 'Non connesso';
      statusText.classList.remove('text-green-600', 'dark:text-green-400');
      statusText.classList.add('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      btn.innerHTML = 'Collega T-Clockwork a <svg class="w-4 h-4 inline-block" viewBox="0 0 24 24"><defs><linearGradient id="mg3" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0082FB"/><stop offset="100%" stop-color="#A033FF"/></linearGradient></defs><path fill="url(#mg3)" d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12c0-5.523-4.477-10-10-10z"/></svg>';
    }
    if(window.lucide) lucide.createIcons();
  };

  window.addEventListener('DOMContentLoaded', updateMetaAuthUI);
'''

# Find handleGoogleLogin and replace it and its helpers with the mock version
start_idx = content.find("window.handleGoogleLogin = function()")
end_idx = content.find("window.openCodeStudio = function()")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + mock_js + content[end_idx:]

# Meta auth handler was likely at the end or somewhere else. We find it and remove the old one.
meta_start = content.find("window.handleMetaLogin = function()")
if meta_start != -1:
    # Remove old handleMetaLogin block to avoid duplication
    meta_end = content.find("};", meta_start) + 2
    # Check if there is an updateMetaAuthUI function
    update_meta_start = content.find("window.updateMetaAuthUI = function()", meta_end)
    if update_meta_start != -1:
        meta_end = content.find("};", update_meta_start) + 2
    content = content[:meta_start] + content[meta_end:]


# 2. Replace the install modal HTML
new_install_modal = '''  <!-- Install Modal -->
  <div id="installModal" class="fixed inset-0 bg-black/40 z-[90] hidden items-center justify-center p-4 transition-opacity opacity-0 duration-300" onclick="if(event.target===this) closeInstallModal()">
    <div class="bg-white dark:bg-[#131314] rounded-3xl shadow-2xl w-full max-w-[520px] overflow-hidden transform scale-95 transition-transform duration-300 border border-[#e5e7eb] dark:border-[#2f3032] flex flex-col max-h-[85vh]">
      <div class="flex items-center justify-between p-5 border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <h2 class="text-lg font-semibold flex items-center gap-2">
          <i data-lucide="download-cloud" class="w-5 h-5 text-[#1a73e8]"></i> Installa T-Ai
        </h2>
        <button onclick="closeInstallModal()" class="p-2 hover:bg-[#f0f4f9] dark:hover:bg-[#2a2b2f] rounded-full transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      
      <div class="flex border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <button onclick="switchInstallTab('pc')" id="tab-pc" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-blue-600 text-blue-600 dark:text-blue-400 transition flex items-center justify-center gap-1.5">
          <i data-lucide="monitor" class="w-4 h-4"></i> Windows / Linux
        </button>
        <button onclick="switchInstallTab('apple')" id="tab-apple" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="apple" class="w-4 h-4"></i> Apple (Mac/iOS)
        </button>
        <button onclick="switchInstallTab('android')" id="tab-android" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="smartphone" class="w-4 h-4"></i> Android
        </button>
      </div>

      <div class="p-6 overflow-y-auto">
        <!-- Windows / Linux Tab -->
        <div id="content-pc" class="install-content space-y-5">
          <div class="flex items-center gap-3 p-3 bg-gradient-to-r from-[#1a73e8]/10 to-[#8b5cf6]/10 rounded-xl">
            <div class="w-10 h-10 rounded-full bg-[#1a73e8]/20 text-[#1a73e8] flex items-center justify-center shrink-0">
              <i data-lucide="monitor" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              T-Ai Web App per <strong>Windows</strong>, <strong>Fedora / Red Hat</strong> e <strong>Debian / Ubuntu</strong>. Funziona solo con browser basati su Chromium (Chrome, Edge, Brave).
            </p>
          </div>
          <div>
            <ul class="space-y-3 text-[14px]">
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
                <span>Apri <strong>Google Chrome</strong> o <strong>Microsoft Edge</strong>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
                <span>Vai sulla pagina di T-Ai.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
                <span>Clicca sull'icona <strong>Installa app</strong> (il monitor con la freccia in giù) nella barra in alto a destra, oppure vai su Menu ⋮ e clicca su <strong>Installa T-Ai</strong>.</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Apple Tab -->
        <div id="content-apple" class="install-content hidden space-y-5">
          <div class="flex items-center gap-3 p-3 bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 rounded-xl">
            <div class="w-10 h-10 rounded-full bg-black/5 dark:bg-white/10 flex items-center justify-center shrink-0">
              <i data-lucide="apple" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              Installazione per ecosistema Apple (MacOS, iOS, iPadOS).
            </p>
          </div>
          
          <h4 class="text-[14px] font-semibold mt-4 mb-2">MacOS</h4>
          <ul class="space-y-2 text-[13px] mb-4">
            <li><strong>1.</strong> Go to "Safari©"</li>
            <li><strong>2.</strong> Go to the T-Ai and tap the Share icon</li>
            <li><strong>3.</strong> Scroll down the options until you see the option "Add to the dock"</li>
            <li><strong>4.</strong> Then you will have to add it to the dock with the name of "T-Ai" and (if possible) "Web app" option enabled on</li>
          </ul>

          <h4 class="text-[14px] font-semibold mt-4 mb-2">iOS / iPadOS</h4>
          <ul class="space-y-2 text-[13px]">
            <li><strong>1.</strong> Go to "Safari©"</li>
            <li><strong>2.</strong> Go to T-Ai and tap the Share icon</li>
            <li><strong>3.</strong> When on the share screen scroll until you se the option "Add to Home Screen" and tap on it then you will have to add it with the name "T-Ai" and "Web app" option enabled</li>
          </ul>
        </div>

        <!-- Android Tab -->
        <div id="content-android" class="install-content hidden space-y-5">
          <div class="flex items-center gap-3 p-3 bg-[#e6f4ea] dark:bg-[#1e2e22] rounded-xl">
            <div class="w-10 h-10 rounded-full bg-green-500/20 text-green-600 flex items-center justify-center shrink-0">
              <i data-lucide="smartphone" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              Installazione per dispositivi Android.
            </p>
          </div>
          <ul class="space-y-3 text-[14px]">
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
              <span>Go to "Chrome©"</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Go to the T-Ai Page</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Tap on the ... at the up of the browser</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Scroll down until you finally see the "Add to Homepage" option</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">5</span>
              <span>After clicking on the "Add to homepage" option you have to add T-Ai with the name "T-Ai" and click on "Add" or "Save"</span>
            </li>
          </ul>
        </div>

      </div>
    </div>
  </div>'''

install_start = content.find('<!-- Install Modal -->')
install_end = content.find('<!-- Canvas Modal -->')

if install_start != -1 and install_end != -1:
    content = content[:install_start] + new_install_modal + '\n\n  ' + content[install_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Install Modal and Auth Logic Updated.")
