#!/usr/bin/env python3
"""
Update Install Modal with new platform instructions:
- Windows (chromium based browsers only)
- Fedora/Red Hat
- Debian/Ubuntu
- MacOS (dock instructions)
- iOS/iPadOS (updated)
- Android (updated)
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the PC Tab content with new detailed instructions
old_pc_tab = '''        <!-- PC Tab -->
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
        </div>'''

new_pc_tab = '''        <!-- PC Tab -->
        <div id="content-pc" class="install-content hidden space-y-5">
          <div class="flex items-center gap-3 p-3 bg-gradient-to-r from-[#1a73e8]/10 to-[#8b5cf6]/10 rounded-xl">
            <div class="w-10 h-10 rounded-full bg-[#1a73e8]/20 text-[#1a73e8] flex items-center justify-center shrink-0">
              <i data-lucide="globe" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              Installa T-Ai come app nativa su <strong>Windows</strong>, <strong>Linux</strong> (Fedora/Red Hat, Debian/Ubuntu) e <strong>macOS</strong>.
            </p>
          </div>

          <!-- Windows -->
          <div>
            <h4 class="text-[13px] font-semibold mb-3 flex items-center gap-2">
              <span class="w-5 h-5 rounded bg-blue-500/10 text-blue-600 flex items-center justify-center text-[11px] font-bold">W</span>
              Windows (Solo browser Chromium)
            </h4>
            <ul class="space-y-3 text-[14px]">
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
                <span>Apri T-Ai in <strong>Google Chrome</strong>, <strong>Microsoft Edge</strong>, o <strong>Brave</strong> (solo browser basati su Chromium).</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
                <span>Clicca sull'icona <strong>Installa</strong> nella barra degli indirizzi (icona con monitor + freccia).</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
                <span>Oppure: <strong>Menu ⋮</strong> → <em>"Installa app"</em> o <em>"Installa T-Ai come app"</em>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
                <span>Conferma cliccando <strong>Installa</strong>. Troverai T-Ai nel menu Start!</span>
              </li>
            </ul>
          </div>

          <!-- Fedora/Red Hat -->
          <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
            <h4 class="text-[13px] font-semibold mb-3 flex items-center gap-2">
              <span class="w-5 h-5 rounded bg-red-500/10 text-red-600 flex items-center justify-center text-[11px] font-bold">F</span>
              Fedora / Red Hat
            </h4>
            <ul class="space-y-3 text-[14px]">
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-red-500/10 text-red-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
                <span>Apri T-Ai in <strong>Google Chrome</strong>, <strong>Chromium</strong>, o <strong>Brave</strong>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-red-500/10 text-red-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
                <span>Clicca sul menu <strong>⋮</strong> → <em>"Installa app"</em> o <em>"Crea collegamento"</em>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-red-500/10 text-red-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
                <span>Oppure su GNOME: tasto destro → <em>"Aggiungi ad applicazioni"</em>.</span>
              </li>
            </ul>
          </div>

          <!-- Debian/Ubuntu -->
          <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
            <h4 class="text-[13px] font-semibold mb-3 flex items-center gap-2">
              <span class="w-5 h-5 rounded bg-orange-500/10 text-orange-600 flex items-center justify-center text-[11px] font-bold">D</span>
              Debian / Ubuntu
            </h4>
            <ul class="space-y-3 text-[14px]">
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-orange-500/10 text-orange-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
                <span>Apri T-Ai in <strong>Google Chrome</strong>, <strong>Chromium</strong>, o <strong>Brave</strong>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-orange-500/10 text-orange-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
                <span>Clicca sul menu <strong>⋮</strong> → <em>"Installa app"</em> o <em>"Crea collegamento"</em>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-orange-500/10 text-orange-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
                <span>Su GNOME: tasto destro → <em>"Aggiungi ad applicazioni"</em>.</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="w-6 h-6 rounded-full bg-orange-500/10 text-orange-600 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
                <span>Su KDE Plasma: tasto destro sul desktop → <em>"Crea nuovo"</em> → <em>"Collegamento ad applicazione"</em>.</span>
              </li>
            </ul>
          </div>

          <button id="installPWABtn" onclick="installPWA()" class="w-full mt-2 py-3 rounded-xl bg-gradient-to-r from-[#1a73e8] to-[#8b5cf6] text-white font-medium shadow-md hover:opacity-90 transition flex justify-center items-center gap-2">
            <i data-lucide="download" class="w-4 h-4"></i> Installa come App (PWA)
          </button>
        </div>'''

if old_pc_tab in content:
    content = content.replace(old_pc_tab, new_pc_tab)
    print("[OK] PC Tab updated with Windows, Fedora/Red Hat, Debian/Ubuntu instructions")
else:
    print("[SKIP] PC Tab content not found or already updated")

# Replace Android Tab with updated instructions
old_android_tab = '''        <!-- Android Tab -->
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
        </div>'''

new_android_tab = '''        <!-- Android Tab -->
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
              <span>Vai su <strong>Chrome©</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Vai alla pagina T-Ai.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Tocca sui <strong>...</strong> in alto al browser.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Scorri finché vedi l'opzione <strong>"Add to Homepage"</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-green-500/10 text-green-600 dark:text-green-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">5</span>
              <span>Dopo aver cliccato su <strong>"Add to homepage"</strong>, aggiungi T-Ai con il nome <strong>"T-Ai"</strong> e clicca su <strong>"Add"</strong> o <strong>"Save"</strong>.</span>
            </li>
          </ul>
        </div>'''

if old_android_tab in content:
    content = content.replace(old_android_tab, new_android_tab)
    print("[OK] Android Tab updated with new instructions")
else:
    print("[SKIP] Android Tab content not found or already updated")

# Replace iOS/iPadOS Tab with updated instructions
old_ios_tab = '''        <!-- iOS / iPadOS Tab -->
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
        </div>'''

new_ios_tab = '''        <!-- iOS / iPadOS Tab -->
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
              <span>Vai su <strong>"Safari©"</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Vai su T-Ai e tocca l'icona Condividi.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Quando sei sulla schermata di condivisione, scorri finché vedi l'opzione <strong>"Add to Home Screen"</strong> e toccala.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Poi dovrai aggiungerla con il nome <strong>"T-Ai"</strong> e l'opzione <strong>"Web app"</strong> abilitata.</span>
            </li>
          </ul>
          <div class="p-3 bg-amber-50 dark:bg-amber-900/10 rounded-xl text-[13px] text-amber-700 dark:text-amber-400 flex items-start gap-2 mt-2">
            <i data-lucide="info" class="w-4 h-4 shrink-0 mt-0.5"></i>
            <span><strong>MacOS:</strong> Vai su "Safari©" → Vai su T-Ai e tocca l'icona Condividi → Scorri le opzioni finché vedi l'opzione "Add to the dock" → Poi dovrai aggiungerla al dock con il nome "T-Ai" e (se possibile) l'opzione "Web app" abilitata.</span>
          </div>
        </div>'''

if old_ios_tab in content:
    content = content.replace(old_ios_tab, new_ios_tab)
    print("[OK] iOS/iPadOS Tab updated with new instructions including MacOS")
else:
    print("[SKIP] iOS/iPadOS Tab content not found or already updated")

# Add MacOS tab to the tabs section
old_tabs = '''      <div class="flex border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <button onclick="switchInstallTab('pc')" id="tab-pc" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="monitor" class="w-4 h-4"></i> PC / Mac
        </button>
        <button onclick="switchInstallTab('android')" id="tab-android" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="smartphone" class="w-4 h-4"></i> Android
        </button>
        <button onclick="switchInstallTab('ios')" id="tab-ios" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="tablet-smartphone" class="w-4 h-4"></i> iOS / iPad
        </button>
      </div>'''

new_tabs = '''      <div class="flex border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <button onclick="switchInstallTab('pc')" id="tab-pc" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="monitor" class="w-4 h-4"></i> PC
        </button>
        <button onclick="switchInstallTab('android')" id="tab-android" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="smartphone" class="w-4 h-4"></i> Android
        </button>
        <button onclick="switchInstallTab('ios')" id="tab-ios" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="tablet-smartphone" class="w-4 h-4"></i> iOS / iPad
        </button>
        <button onclick="switchInstallTab('macos')" id="tab-macos" class="install-tab flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-1.5">
          <i data-lucide="laptop" class="w-4 h-4"></i> MacOS
        </button>
      </div>'''

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
    print("[OK] Added MacOS tab to install modal tabs")
else:
    print("[SKIP] Tabs section not found or already updated")

# Add MacOS content section after iOS content
macos_content = '''        <!-- MacOS Tab -->
        <div id="content-macos" class="install-content hidden space-y-4">
          <div class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-900/10 rounded-xl">
            <div class="w-10 h-10 rounded-full bg-gray-500/20 text-gray-600 flex items-center justify-center shrink-0">
              <i data-lucide="laptop" class="w-5 h-5"></i>
            </div>
            <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">
              Installa T-Ai su <strong>macOS</strong> per accesso rapido dal Dock!
            </p>
          </div>
          <ul class="space-y-3 text-[14px]">
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-gray-500/10 text-gray-600 dark:text-gray-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">1</span>
              <span>Vai su <strong>"Safari©"</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-gray-500/10 text-gray-600 dark:text-gray-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">2</span>
              <span>Vai su T-Ai e tocca l'icona Condividi.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-gray-500/10 text-gray-600 dark:text-gray-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">3</span>
              <span>Scorri le opzioni finché vedi l'opzione <strong>"Add to the dock"</strong>.</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="w-6 h-6 rounded-full bg-gray-500/10 text-gray-600 dark:text-gray-400 flex items-center justify-center shrink-0 font-medium text-xs mt-0.5">4</span>
              <span>Poi dovrai aggiungerla al dock con il nome di <strong>"T-Ai"</strong> e (se possibile) l'opzione <strong>"Web app"</strong> abilitata.</span>
            </li>
          </ul>
        </div>

'''

# Insert MacOS content after iOS content
if 'content-ios' in content and 'content-macos' not in content:
    content = content.replace(
        '</div>\n\n  <!-- T-Clockwork Modal -->',
        macos_content + '</div>\n\n  <!-- T-Clockwork Modal -->'
    )
    print("[OK] Added MacOS content section")
else:
    print("[SKIP] MacOS content already exists or iOS content not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== Install modal updated successfully ===")
