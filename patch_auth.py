import os

file_path = "/home/clocky/T-Ai/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Accedi Button
auth_btn = """
  <!-- Bottone Accedi / Registrati -->
  <button onclick="openAuthModal()" id="authSidebarBtn" class="w-full flex items-center gap-3 bg-[#dde3ea] hover:bg-[#d2d9e1] dark:bg-[#2c2f33] dark:hover:bg-[#35383d] rounded-full py-3 px-4 transition shadow-sm mb-2">
    <i data-lucide="user" class="w-5 h-5 shrink-0"></i>
    <span class="sidebar-text font-medium" id="authSidebarText">Accedi / Registrati</span>
  </button>
"""
if 'id="authSidebarBtn"' not in content:
    content = content.replace('<!-- Bottone Installa T-Ai -->', auth_btn + '\n  <!-- Bottone Installa T-Ai -->')

# 2. Add Auth Modal HTML
auth_modal = """
  <!-- Auth Modal -->
  <div id="authModal" class="fixed inset-0 bg-black/40 z-[95] hidden items-center justify-center p-4 transition-opacity opacity-0 duration-300" onclick="if(event.target===this) closeAuthModal()">
    <div class="bg-white dark:bg-[#131314] rounded-3xl shadow-2xl w-full max-w-[400px] overflow-hidden transform scale-95 transition-transform duration-300 border border-[#e5e7eb] dark:border-[#2f3032] flex flex-col">
      <div class="flex items-center justify-between p-5 border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <h2 class="text-lg font-semibold flex items-center gap-2">
          <i data-lucide="user" class="w-5 h-5 text-[#1a73e8]"></i> <span id="authTitle">Accedi</span>
        </h2>
        <button onclick="closeAuthModal()" class="p-2 hover:bg-[#f0f4f9] dark:hover:bg-[#2a2b2f] rounded-full transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="p-6 space-y-4 relative">
        <div id="authAlert" class="hidden absolute top-0 left-0 right-0 mx-6 mt-2 px-4 py-2 bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-lg text-sm font-medium border border-green-200 dark:border-green-800 text-center">
            Azione completata!
        </div>
        <div id="nameFieldGroup" class="hidden">
            <label class="block text-[13px] font-medium mb-1.5 text-[#5f6368] dark:text-[#9aa0a6]">Nome</label>
            <input type="text" id="authName" class="w-full bg-[#f0f4f9] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl px-4 py-2.5 outline-none focus:border-[#1a73e8] transition" placeholder="Il tuo nome">
        </div>
        <div>
            <label class="block text-[13px] font-medium mb-1.5 text-[#5f6368] dark:text-[#9aa0a6]">Email</label>
            <input type="email" id="authEmail" class="w-full bg-[#f0f4f9] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl px-4 py-2.5 outline-none focus:border-[#1a73e8] transition" placeholder="tua@email.com">
        </div>
        <div>
            <label class="block text-[13px] font-medium mb-1.5 text-[#5f6368] dark:text-[#9aa0a6]">Password</label>
            <input type="password" id="authPassword" class="w-full bg-[#f0f4f9] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl px-4 py-2.5 outline-none focus:border-[#1a73e8] transition" placeholder="••••••••">
        </div>
        
        <button id="authSubmitBtn" onclick="submitAuth()" class="w-full py-3 rounded-xl bg-gradient-to-r from-[#1a73e8] to-[#8b5cf6] text-white font-medium shadow-md hover:opacity-90 transition mt-2 flex justify-center items-center gap-2">
            Accedi
        </button>
        
        <p class="text-[13px] text-center text-[#5f6368] dark:text-[#9aa0a6] mt-4">
            <span id="authToggleText">Non hai un account?</span> 
            <button onclick="toggleAuthMode()" id="authToggleBtn" class="text-[#1a73e8] font-medium hover:underline">Registrati</button>
        </p>
      </div>
    </div>
  </div>
"""
if 'id="authModal"' not in content:
    content = content.replace('<!-- Install Modal -->', auth_modal + '\n\n  <!-- Install Modal -->')

# 3. Add Auth Javascript
auth_js = """
  // Auth Logic
  let isSignupMode = false;
  
  window.openAuthModal = function() {
    const modal = document.getElementById('authModal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    void modal.offsetWidth;
    modal.classList.remove('opacity-0');
    modal.querySelector('div').classList.remove('scale-95');
    document.getElementById('authAlert').classList.add('hidden');
  };

  window.closeAuthModal = function() {
    const modal = document.getElementById('authModal');
    if(!modal || modal.classList.contains('hidden')) return;
    modal.classList.add('opacity-0');
    modal.querySelector('div').classList.add('scale-95');
    setTimeout(() => {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }, 300);
  };

  window.toggleAuthMode = function() {
    isSignupMode = !isSignupMode;
    document.getElementById('authTitle').innerText = isSignupMode ? "Registrati" : "Accedi";
    document.getElementById('authSubmitBtn').innerText = isSignupMode ? "Registrati" : "Accedi";
    document.getElementById('authToggleText').innerText = isSignupMode ? "Hai già un account?" : "Non hai un account?";
    document.getElementById('authToggleBtn').innerText = isSignupMode ? "Accedi" : "Registrati";
    
    if (isSignupMode) {
      document.getElementById('nameFieldGroup').classList.remove('hidden');
    } else {
      document.getElementById('nameFieldGroup').classList.add('hidden');
    }
  };

  window.submitAuth = async function() {
    const email = document.getElementById('authEmail').value.trim();
    const password = document.getElementById('authPassword').value.trim();
    const name = document.getElementById('authName').value.trim();
    const btn = document.getElementById('authSubmitBtn');
    
    if(!email || !password || (isSignupMode && !name)) {
      alert("Compila tutti i campi!");
      return;
    }
    
    const action = isSignupMode ? "registrazione" : "login";
    btn.innerHTML = `<i data-lucide="loader-2" class="w-5 h-5 animate-spin"></i> Attendere...`;
    btn.disabled = true;
    if(window.lucide) window.lucide.createIcons();

    try {
      const res = await fetch('/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, name, action })
      });
      const data = await res.json();
      
      const alertBox = document.getElementById('authAlert');
      alertBox.innerText = `${action.charAt(0).toUpperCase() + action.slice(1)} effettuato con successo!`;
      alertBox.classList.remove('hidden');
      
      // Update sidebar state
      if(data.user) {
        document.getElementById('authSidebarText').innerText = `Ciao, ${data.user.name || data.user.email.split('@')[0]}`;
        document.getElementById('userNameLabel').innerText = data.user.name || data.user.email.split('@')[0];
      }
      
      setTimeout(() => {
        closeAuthModal();
        btn.innerText = isSignupMode ? "Registrati" : "Accedi";
        btn.disabled = false;
        alertBox.classList.add('hidden');
      }, 1500);
      
    } catch (err) {
      console.error(err);
      alert("Errore di connessione al server.");
      btn.innerText = isSignupMode ? "Registrati" : "Accedi";
      btn.disabled = false;
    }
  };
"""
if 'window.openAuthModal =' not in content:
    content = content.replace('// Install Modal Logic', auth_js + '\n\n  // Install Modal Logic')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied to index.html successfully.")
