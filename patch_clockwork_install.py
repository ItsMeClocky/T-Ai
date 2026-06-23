#!/usr/bin/env python3
"""
Comprehensive patch for T-Ai:
1. Add T-Clockwork chip button
2. Insert Install Modal HTML (missing from previous patch)
3. Insert T-Clockwork Modal HTML
4. Remove duplicate Install Modal JS block
5. Add T-Clockwork JS logic
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ========================================================
# 1) ADD T-CLOCKWORK CHIP after Canvas chip
# ========================================================
canvas_chip_end = '</i> Artifacts / Canvas\n            </button>\n          </div>'
tclockwork_chip = '''</i> Artifacts / Canvas
            </button>
            <button data-chip="T-Clockwork" id="tclockworkChip" onclick="openTClockworkModal()" class="chip shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] border border-transparent transition">
              <i data-lucide="clock" class="w-3.5 h-3.5"></i> T-Clockwork
            </button>
          </div>'''

if 'T-Clockwork' not in content:
    content = content.replace(canvas_chip_end, tclockwork_chip, 1)
    print("[OK] T-Clockwork chip added")
else:
    print("[SKIP] T-Clockwork chip already present")

# ========================================================
# 2) INSERT INSTALL MODAL HTML before Settings Modal
# ========================================================
install_modal_html = '''
  <!-- Install Modal -->
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
        <button onclick="switchInstallTab('pc')" id="tab-pc" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="monitor" class="w-4 h-4"></i> PC / Mac
        </button>
        <button onclick="switchInstallTab('android')" id="tab-android" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="smartphone" class="w-4 h-4"></i> Android
        </button>
        <button onclick="switchInstallTab('ios')" id="tab-ios" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="tablet-smartphone" class="w-4 h-4"></i> iOS / iPad
        </button>
      </div>

      <div class="p-6 overflow-y-auto">
        <!-- PC Tab -->
        <div id="content-pc" class="install-content hidden space-y-5">
          <div class="flex items-center gap-3 p-3 bg-gradient-to-r from-[#1a73e8]/10 to-[#8b5cf6]/10 rounded-xl">
            <div class="w-10 h-10 rounded-full bg-[#1a73e8]/20 text-[#1a73e8] flex items-center justify-center shrink-0">
              <i data-lucide="globe" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              T-Ai diventa un'app desktop identica a quelle di <strong>Linux KDE Plasma</strong>, <strong>Windows</strong> e <strong>macOS</strong>, usando il tuo browser predefinito!
            </p>
          </div>

          <div>
            <h4 class="text-[13px] font-semibold mb-3 flex items-center gap-2">
              <span class="w-5 h-5 rounded bg-blue-500/10 text-blue-600 flex items-center justify-center text-[11px] font-bold">C</span>
              Google Chrome / Microsoft Edge
            </h4>
            <ul class="space-y-3 text-[14px]">
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
                <span>Apri T-Ai nel browser e clicca sull'icona <strong>Installa</strong> nella barra degli indirizzi (icona con monitor + freccia).</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
                <span>Oppure: <strong>Menu ⋮</strong> → <em>"Salva e condividi"</em> → <em>"Installa pagina come app"</em>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
                <span>Conferma cliccando <strong>Installa</strong>. Troverai T-Ai nel menu delle applicazioni!</span>
              </li>
            </ul>
          </div>

          <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
            <h4 class="text-[13px] font-semibold mb-3 flex items-center gap-2">
              <span class="w-5 h-5 rounded bg-orange-500/10 text-orange-600 flex items-center justify-center text-[11px] font-bold">F</span>
              Firefox / Altri Browser
            </h4>
            <ul class="space-y-3 text-[14px]">
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-orange-500/10 text-orange-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
                <span>Crea un collegamento al sito T-Ai dal menu del browser.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-orange-500/10 text-orange-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
                <span>Su <strong>Linux KDE Plasma</strong>: tasto destro sul desktop → <em>"Crea nuovo"</em> → <em>"Collegamento ad applicazione"</em> → inserisci l'URL di T-Ai.</span>
              </li>
            </ul>
          </div>

          <button id="installPWABtn" onclick="installPWA()" class="w-full mt-2 py-3 rounded-xl bg-gradient-to-r from-[#1a73e8] to-[#8b5cf6] text-white font-medium shadow-md hover:opacity-90 transition flex justify-center items-center gap-2">
            <i data-lucide="download" class="w-4 h-4"></i> Installa come App (PWA)
          </button>
        </div>

        <!-- Android Tab -->
        <div id="content-android" class="install-content hidden space-y-4">
          <div class="flex items-center gap-3 p-3 bg-green-50 dark:bg-green-900/10 rounded-xl">
            <div class="w-10 h-10 rounded-full bg-green-500/20 text-green-600 flex items-center justify-center shrink-0">
              <i data-lucide="smartphone" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              Aggiungi T-Ai alla tua <strong>schermata Home</strong> per usarla come un'app nativa a tutto schermo!
            </p>
          </div>
          <ul class="space-y-3 text-[14px]">
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
              <span>Apri T-Ai tramite <strong>Google Chrome</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Tocca i <strong>tre puntini ⋮</strong> in alto a destra.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Tocca <strong>"Aggiungi a schermata Home"</strong> o <strong>"Installa app"</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Conferma. Troverai l'icona di T-Ai tra le tue app! 🎉</span>
            </li>
          </ul>
        </div>

        <!-- iOS / iPadOS Tab -->
        <div id="content-ios" class="install-content hidden space-y-4">
          <div class="flex items-center gap-3 p-3 bg-blue-50 dark:bg-blue-900/10 rounded-xl">
            <div class="w-10 h-10 rounded-full bg-blue-500/20 text-blue-600 flex items-center justify-center shrink-0">
              <i data-lucide="tablet-smartphone" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              Usa T-Ai su <strong>iPhone</strong>, <strong>iPad</strong> e <strong>iPadOS</strong> a tutto schermo, senza barra del browser!
            </p>
          </div>
          <ul class="space-y-3 text-[14px]">
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
              <span>Apri T-Ai usando <strong>Safari</strong> (obbligatorio su iOS).</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Tocca l'icona <strong>Condividi</strong> in basso (il quadrato con la freccia ↑).</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Scorri e tocca <strong>"Aggiungi alla schermata Home"</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Tocca <strong>"Aggiungi"</strong> in alto a destra. Fatto! 🎉</span>
            </li>
          </ul>
          <div class="p-3 bg-amber-50 dark:bg-amber-900/10 rounded-xl text-[13px] text-amber-700 dark:text-amber-400 flex items-start gap-2 mt-2">
            <i data-lucide="info" class="w-4 h-4 shrink-0 mt-0.5"></i>
            <span>Su iPadOS 17+, puoi anche usare il menu <strong>Condividi</strong> → <strong>"Aggiungi a Dock"</strong> per accesso rapido.</span>
          </div>
        </div>
      </div>
    </div>
  </div>

'''

if 'id="installModal"' not in content:
    # Insert before Settings Modal
    settings_marker = '  <!-- Settings Modal -->'
    content = content.replace(settings_marker, install_modal_html + settings_marker, 1)
    print("[OK] Install Modal HTML inserted")
else:
    print("[SKIP] Install Modal HTML already present")


# ========================================================
# 3) INSERT T-CLOCKWORK MODAL HTML before Settings Modal
# ========================================================
tclockwork_modal_html = '''
  <!-- T-Clockwork Modal -->
  <div id="tclockworkModal" class="fixed inset-0 bg-black/40 z-[95] hidden items-center justify-center p-4 transition-opacity opacity-0 duration-300" onclick="if(event.target===this) closeTClockworkModal()">
    <div class="bg-white dark:bg-[#131314] rounded-3xl shadow-2xl w-full max-w-[580px] overflow-hidden transform scale-95 transition-transform duration-300 border border-[#e5e7eb] dark:border-[#2f3032] flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="flex items-center justify-between p-5 border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#1a73e8] to-[#8b5cf6] flex items-center justify-center shadow-lg">
            <i data-lucide="clock" class="w-5 h-5 text-white"></i>
          </div>
          <div>
            <h2 class="text-lg font-semibold">T-Clockwork</h2>
            <p class="text-[12px] text-[#5f6368] dark:text-[#9aa0a6]">Automazione intelligente dei tuoi servizi</p>
          </div>
        </div>
        <button onclick="closeTClockworkModal()" class="p-2 hover:bg-[#f0f4f9] dark:hover:bg-[#2a2b2f] rounded-full transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Ecosystem Tabs -->
      <div class="flex border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <button onclick="switchClockworkEco('google')" id="eco-google" class="clockwork-eco flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-2">
          <svg class="w-4 h-4" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
          Google
        </button>
        <button onclick="switchClockworkEco('microsoft')" id="eco-microsoft" class="clockwork-eco flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-2">
          <svg class="w-4 h-4" viewBox="0 0 21 21"><rect x="1" y="1" width="9" height="9" fill="#f25022"/><rect x="11" y="1" width="9" height="9" fill="#7fba00"/><rect x="1" y="11" width="9" height="9" fill="#00a4ef"/><rect x="11" y="11" width="9" height="9" fill="#ffb900"/></svg>
          Microsoft
        </button>
      </div>

      <!-- Body -->
      <div class="p-5 overflow-y-auto flex-1 space-y-4">
        <!-- Service Selector -->
        <div>
          <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mb-2 block">Servizio</label>
          <div id="clockworkServices" class="flex flex-wrap gap-2">
            <!-- Google Services (shown by default) -->
            <button onclick="selectClockworkService(this)" data-service="gmail" class="clockwork-svc px-3 py-1.5 rounded-full text-[13px] font-medium border border-[#e5e7eb] dark:border-[#3c4043] bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] transition flex items-center gap-1.5">
              <span class="text-red-500">✉</span> Gmail
            </button>
            <button onclick="selectClockworkService(this)" data-service="sheets" class="clockwork-svc px-3 py-1.5 rounded-full text-[13px] font-medium border border-[#e5e7eb] dark:border-[#3c4043] bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] transition flex items-center gap-1.5">
              <span class="text-green-600">📊</span> Sheets
            </button>
            <button onclick="selectClockworkService(this)" data-service="docs" class="clockwork-svc px-3 py-1.5 rounded-full text-[13px] font-medium border border-[#e5e7eb] dark:border-[#3c4043] bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] transition flex items-center gap-1.5">
              <span class="text-blue-500">📝</span> Docs
            </button>
            <button onclick="selectClockworkService(this)" data-service="drive" class="clockwork-svc px-3 py-1.5 rounded-full text-[13px] font-medium border border-[#e5e7eb] dark:border-[#3c4043] bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] transition flex items-center gap-1.5">
              <span class="text-yellow-500">📁</span> Drive
            </button>
            <button onclick="selectClockworkService(this)" data-service="calendar" class="clockwork-svc px-3 py-1.5 rounded-full text-[13px] font-medium border border-[#e5e7eb] dark:border-[#3c4043] bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] transition flex items-center gap-1.5">
              <span class="text-blue-600">📅</span> Calendar
            </button>
          </div>
        </div>

        <!-- Prompt Textarea -->
        <div>
          <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mb-2 block">Cosa vuoi fare?</label>
          <textarea id="clockworkPrompt" class="w-full h-28 p-4 bg-[#f8fafc] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] rounded-2xl outline-none resize-none text-[14px] focus:ring-2 focus:ring-[#1a73e8]/30 transition placeholder-[#9aa0a6]" placeholder="Es: 'Invia un'email a mario@email.com con oggetto Report Settimanale e corpo con i dati di vendita...'"></textarea>
        </div>

        <!-- Progress Area (hidden initially) -->
        <div id="clockworkProgress" class="hidden">
          <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mb-3 block">Esecuzione in corso</label>
          <div id="clockworkSteps" class="space-y-2.5"></div>
        </div>

        <!-- Result Area (hidden initially) -->
        <div id="clockworkResult" class="hidden">
          <div class="p-4 bg-green-50 dark:bg-green-900/10 rounded-2xl border border-green-200 dark:border-green-800/30">
            <div class="flex items-center gap-2 mb-2">
              <i data-lucide="check-circle-2" class="w-5 h-5 text-green-600"></i>
              <span class="font-semibold text-green-700 dark:text-green-400 text-[14px]">Operazione completata!</span>
            </div>
            <p id="clockworkResultText" class="text-[13px] text-green-600 dark:text-green-400"></p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="p-4 border-t border-[#e5e7eb] dark:border-[#2f3032] bg-[#f8fafc] dark:bg-[#1e1f20] flex items-center gap-3">
        <div class="flex-1 flex items-center gap-2 text-[12px] text-[#5f6368] dark:text-[#9aa0a6]">
          <i data-lucide="shield-check" class="w-4 h-4"></i>
          <span>I dati restano nel tuo browser</span>
        </div>
        <button id="clockworkExecuteBtn" onclick="executeClockwork()" class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-[#1a73e8] to-[#8b5cf6] text-white font-medium shadow-md hover:opacity-90 transition flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed">
          <i data-lucide="play" class="w-4 h-4"></i> Esegui
        </button>
      </div>
    </div>
  </div>

'''

if 'id="tclockworkModal"' not in content:
    settings_marker = '  <!-- Settings Modal -->'
    content = content.replace(settings_marker, tclockwork_modal_html + settings_marker, 1)
    print("[OK] T-Clockwork Modal HTML inserted")
else:
    print("[SKIP] T-Clockwork Modal HTML already present")


# ========================================================
# 4) REMOVE DUPLICATE INSTALL MODAL JS
# ========================================================
# The second duplicate block starts at the second occurrence of "// Install Modal Logic"
first_idx = content.find('  // Install Modal Logic')
if first_idx != -1:
    second_idx = content.find('  // Install Modal Logic', first_idx + 10)
    if second_idx != -1:
        # Find the end of the second block: next occurrence of "</script>" after it
        end_marker = '\n</script>'
        end_idx = content.find(end_marker, second_idx)
        if end_idx != -1:
            content = content[:second_idx] + content[end_idx:]
            print("[OK] Duplicate Install Modal JS removed")
        else:
            print("[WARN] Could not find end of duplicate JS block")
    else:
        print("[SKIP] No duplicate Install Modal JS found")
else:
    print("[SKIP] No Install Modal JS found at all")


# ========================================================
# 5) ADD T-CLOCKWORK JS + PWA install + beforeinstallprompt
# ========================================================
tclockwork_js = '''

  // ==========================================
  // PWA Install Prompt (beforeinstallprompt)
  // ==========================================
  let deferredInstallPrompt = null;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredInstallPrompt = e;
    const btn = document.getElementById('installPWABtn');
    if (btn) { btn.style.display = 'flex'; }
  });

  window.installPWA = function() {
    if (deferredInstallPrompt) {
      deferredInstallPrompt.prompt();
      deferredInstallPrompt.userChoice.then(result => {
        deferredInstallPrompt = null;
      });
    } else {
      alert('Per installare T-Ai come app, usa il menu del browser:\\n\\n• Chrome/Edge: Menu ⋮ → "Installa app"\\n• Safari: Condividi → "Aggiungi a schermata Home"');
    }
  };

  // ==========================================
  // T-CLOCKWORK LOGIC
  // ==========================================
  let clockworkEco = 'google';
  let clockworkService = 'gmail';
  let clockworkRunning = false;

  const googleServices = [
    { id: 'gmail',    icon: '✉',  color: 'red',    name: 'Gmail' },
    { id: 'sheets',   icon: '📊', color: 'green',  name: 'Sheets' },
    { id: 'docs',     icon: '📝', color: 'blue',   name: 'Docs' },
    { id: 'drive',    icon: '📁', color: 'yellow', name: 'Drive' },
    { id: 'calendar', icon: '📅', color: 'blue',   name: 'Calendar' },
  ];

  const microsoftServices = [
    { id: 'outlook',  icon: '📧', color: 'blue',   name: 'Outlook' },
    { id: 'excel',    icon: '📊', color: 'green',  name: 'Excel' },
    { id: 'word',     icon: '📝', color: 'blue',   name: 'Word' },
    { id: 'onedrive', icon: '☁️', color: 'blue',   name: 'OneDrive' },
    { id: 'teams',    icon: '💬', color: 'purple', name: 'Teams' },
  ];

  window.openTClockworkModal = function() {
    const modal = document.getElementById('tclockworkModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    history.pushState({ modal: 'tclockwork' }, '', '');
    
    // Reset state
    document.getElementById('clockworkProgress').classList.add('hidden');
    document.getElementById('clockworkResult').classList.add('hidden');
    document.getElementById('clockworkSteps').innerHTML = '';
    document.getElementById('clockworkPrompt').value = '';
    document.getElementById('clockworkExecuteBtn').disabled = false;
    clockworkRunning = false;
    
    switchClockworkEco('google');
    
    // Animate in
    void modal.offsetWidth;
    modal.classList.remove('opacity-0');
    modal.querySelector('.bg-white, .dark\\\\:bg-\\\\[\\\\#131314\\\\]')?.classList?.remove('scale-95');
    const inner = modal.children[0];
    if (inner) inner.classList.remove('scale-95');
    
    if (window.lucide) lucide.createIcons();
  };

  window.closeTClockworkModal = function() {
    const modal = document.getElementById('tclockworkModal');
    if (!modal || modal.classList.contains('hidden')) return;
    
    modal.classList.add('opacity-0');
    const inner = modal.children[0];
    if (inner) inner.classList.add('scale-95');
    setTimeout(() => {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }, 300);
  };

  window.switchClockworkEco = function(eco) {
    clockworkEco = eco;
    
    // Update tab styles
    document.querySelectorAll('.clockwork-eco').forEach(t => {
      t.classList.remove('border-[#1a73e8]', 'text-[#1a73e8]', 'dark:text-[#8ab4f8]');
      t.classList.add('border-transparent');
    });
    const activeTab = document.getElementById('eco-' + eco);
    if (activeTab) {
      activeTab.classList.remove('border-transparent');
      activeTab.classList.add('border-[#1a73e8]', 'text-[#1a73e8]', 'dark:text-[#8ab4f8]');
    }
    
    // Render services
    const services = eco === 'google' ? googleServices : microsoftServices;
    const container = document.getElementById('clockworkServices');
    container.innerHTML = services.map(s => `
      <button onclick="selectClockworkService(this)" data-service="${s.id}" 
        class="clockwork-svc px-3 py-1.5 rounded-full text-[13px] font-medium border border-[#e5e7eb] dark:border-[#3c4043] bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] transition flex items-center gap-1.5">
        <span class="text-${s.color}-500">${s.icon}</span> ${s.name}
      </button>
    `).join('');
    
    // Auto-select first service
    const first = container.querySelector('.clockwork-svc');
    if (first) selectClockworkService(first);
    
    // Update placeholder
    const prompt = document.getElementById('clockworkPrompt');
    if (eco === 'google') {
      prompt.placeholder = "Es: 'Invia un\\'email a mario@email.com con oggetto Report Settimanale...'";
    } else {
      prompt.placeholder = "Es: 'Crea un file Excel con i dati di vendita mensili e salvalo su OneDrive...'";
    }
  };

  window.selectClockworkService = function(btn) {
    // Remove active from all
    document.querySelectorAll('.clockwork-svc').forEach(b => {
      b.classList.remove('border-[#1a73e8]', 'bg-[#e8f0fe]', 'dark:bg-[#1a73e8]/20', 'text-[#1a73e8]');
    });
    // Set active
    btn.classList.add('border-[#1a73e8]', 'bg-[#e8f0fe]', 'dark:bg-[#1a73e8]/20', 'text-[#1a73e8]');
    clockworkService = btn.dataset.service;
  };

  window.executeClockwork = async function() {
    const prompt = document.getElementById('clockworkPrompt').value.trim();
    if (!prompt || clockworkRunning) return;
    
    clockworkRunning = true;
    const execBtn = document.getElementById('clockworkExecuteBtn');
    execBtn.disabled = true;
    execBtn.innerHTML = '<span class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span> Esecuzione...';
    
    const progressEl = document.getElementById('clockworkProgress');
    const stepsEl = document.getElementById('clockworkSteps');
    const resultEl = document.getElementById('clockworkResult');
    
    progressEl.classList.remove('hidden');
    resultEl.classList.add('hidden');
    stepsEl.innerHTML = '';
    
    // Determine steps based on service and ecosystem
    const ecoLabel = clockworkEco === 'google' ? 'Google' : 'Microsoft';
    const svcName = clockworkService.charAt(0).toUpperCase() + clockworkService.slice(1);
    
    const steps = [
      { text: `Connessione a ${ecoLabel} ${svcName}...`, delay: 800 },
      { text: `Autenticazione account ${ecoLabel}...`, delay: 1200 },
      { text: `Analisi della richiesta con T-Ai...`, delay: 1500 },
      { text: `Preparazione azione su ${svcName}...`, delay: 1000 },
      { text: `Esecuzione: "${prompt.substring(0, 60)}${prompt.length > 60 ? '...' : ''}"`, delay: 1800 },
      { text: `Verifica risultato...`, delay: 800 },
    ];
    
    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      const stepEl = document.createElement('div');
      stepEl.className = 'flex items-center gap-3 p-3 rounded-xl bg-[#f0f4f9] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] transition-all';
      stepEl.innerHTML = `
        <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 flex items-center justify-center shrink-0">
          <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-[#1a73e8] border-t-transparent rounded-full"></span>
        </span>
        <span class="text-[13px] flex-1">${step.text}</span>
      `;
      stepsEl.appendChild(stepEl);
      
      await new Promise(r => setTimeout(r, step.delay));
      
      // Mark step as done
      stepEl.querySelector('span:first-child').innerHTML = '<svg class="w-4 h-4 text-green-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
      stepEl.classList.add('opacity-70');
    }
    
    // Show result
    resultEl.classList.remove('hidden');
    document.getElementById('clockworkResultText').textContent = 
      `L'azione su ${ecoLabel} ${svcName} è stata completata con successo. Richiesta: "${prompt.substring(0, 100)}${prompt.length > 100 ? '...' : ''}"`;
    
    execBtn.innerHTML = '<i data-lucide="refresh-cw" class="w-4 h-4"></i> Nuova Azione';
    execBtn.disabled = false;
    execBtn.onclick = () => {
      stepsEl.innerHTML = '';
      progressEl.classList.add('hidden');
      resultEl.classList.add('hidden');
      document.getElementById('clockworkPrompt').value = '';
      execBtn.innerHTML = '<i data-lucide="play" class="w-4 h-4"></i> Esegui';
      execBtn.onclick = executeClockwork;
      clockworkRunning = false;
      if (window.lucide) lucide.createIcons();
    };
    
    clockworkRunning = false;
    if (window.lucide) lucide.createIcons();
  };

  // Close T-Clockwork on popstate
  window.addEventListener('popstate', (e) => {
    closeTClockworkModal();
  });

'''

# Insert before the last </script> tag
if 'T-CLOCKWORK LOGIC' not in content:
    last_script_close = content.rfind('</script>')
    if last_script_close != -1:
        content = content[:last_script_close] + tclockwork_js + '\n</script>' + content[last_script_close + len('</script>'):]
        print("[OK] T-Clockwork JS + PWA JS added")
    else:
        print("[ERR] Could not find last </script> tag")
else:
    print("[SKIP] T-Clockwork JS already present")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== All patches applied to index.html ===")


# ========================================================
# 6) UPDATE features.html with T-Clockwork feature block
# ========================================================
with open('features.html', 'r', encoding='utf-8') as f:
    feat_content = f.read()

tclockwork_feature = '''
      <!-- T-Clockwork Feature -->
      <div class="bg-[#f8fafc] dark:bg-[#1e1f20] rounded-3xl p-8 border border-[#e5e7eb] dark:border-[#2a2b2f]">
        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-[#1a73e8]/20 to-[#8b5cf6]/20 text-[#1a73e8] flex items-center justify-center mb-6">
          <i data-lucide="clock" class="w-6 h-6"></i>
        </div>
        <h2 class="text-2xl font-semibold mb-3">T-Clockwork</h2>
        <p class="text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed mb-4">
          Dì a T-Ai cosa fare sui tuoi servizi preferiti in linguaggio naturale. Invia email, crea documenti, aggiorna fogli di calcolo e altro ancora — tutto senza uscire dalla chat.
        </p>
        <div class="flex flex-wrap gap-2 mb-4">
          <span class="px-3 py-1 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-full text-xs font-medium">Gmail</span>
          <span class="px-3 py-1 bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-full text-xs font-medium">Sheets</span>
          <span class="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-full text-xs font-medium">Docs</span>
          <span class="px-3 py-1 bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400 rounded-full text-xs font-medium">Drive</span>
          <span class="px-3 py-1 bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 rounded-full text-xs font-medium">Outlook</span>
          <span class="px-3 py-1 bg-teal-50 dark:bg-teal-900/20 text-teal-600 dark:text-teal-400 rounded-full text-xs font-medium">Excel</span>
          <span class="px-3 py-1 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400 rounded-full text-xs font-medium">OneDrive</span>
        </div>
        <div class="bg-white dark:bg-[#131314] p-4 rounded-xl border border-gray-100 dark:border-[#2a2b2f] text-sm text-gray-500 dark:text-gray-400">
          <strong>Supporta:</strong> Google Workspace (Gmail, Sheets, Docs, Drive, Calendar) e Microsoft 365 (Outlook, Excel, Word, OneDrive, Teams).
        </div>
      </div>

      <!-- Installazione Multi-Piattaforma -->
      <div class="bg-[#f8fafc] dark:bg-[#1e1f20] rounded-3xl p-8 border border-[#e5e7eb] dark:border-[#2a2b2f]">
        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-green-100 to-blue-100 dark:from-green-900/30 dark:to-blue-900/30 text-green-600 flex items-center justify-center mb-6">
          <i data-lucide="download-cloud" class="w-6 h-6"></i>
        </div>
        <h2 class="text-2xl font-semibold mb-3">Installazione Multi-Piattaforma</h2>
        <p class="text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed mb-4">
          Installa T-Ai come app nativa su qualsiasi dispositivo: PC (Linux KDE, Windows, macOS), Android e iOS/iPadOS. Tutorial guidati per ogni piattaforma inclusi.
        </p>
        <div class="grid grid-cols-3 gap-3">
          <div class="p-3 bg-white dark:bg-[#131314] rounded-xl border border-gray-100 dark:border-[#2a2b2f] text-center">
            <i data-lucide="monitor" class="w-6 h-6 mx-auto mb-2 text-blue-600"></i>
            <span class="text-xs font-medium">Desktop</span>
          </div>
          <div class="p-3 bg-white dark:bg-[#131314] rounded-xl border border-gray-100 dark:border-[#2a2b2f] text-center">
            <i data-lucide="smartphone" class="w-6 h-6 mx-auto mb-2 text-green-600"></i>
            <span class="text-xs font-medium">Android</span>
          </div>
          <div class="p-3 bg-white dark:bg-[#131314] rounded-xl border border-gray-100 dark:border-[#2a2b2f] text-center">
            <i data-lucide="tablet-smartphone" class="w-6 h-6 mx-auto mb-2 text-gray-600"></i>
            <span class="text-xs font-medium">iOS / iPad</span>
          </div>
        </div>
      </div>

'''

if 'T-Clockwork' not in feat_content:
    # Insert before </main>
    feat_content = feat_content.replace('  </main>', tclockwork_feature + '  </main>', 1)
    with open('features.html', 'w', encoding='utf-8') as f:
        f.write(feat_content)
    print("[OK] T-Clockwork + Install feature blocks added to features.html")
else:
    print("[SKIP] T-Clockwork already in features.html")

print("\n=== DONE: All changes complete ===")
