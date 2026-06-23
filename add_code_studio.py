import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML for Code Studio (inserted after canvasPanel)
code_studio_html = """
  <!-- Code Studio Panel -->
  <aside id="codeStudioPanel" class="fixed inset-y-0 right-0 w-full sm:w-[800px] bg-white dark:bg-[#1c1d1f] shadow-2xl translate-x-full transition-transform duration-300 z-50 flex flex-col border-l border-[#e5e7eb] dark:border-[#2f3032]">
    <div class="flex items-center justify-between px-4 py-3 border-b border-[#e5e7eb] dark:border-[#2f3032]">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-full bg-[#1a73e8]/10 text-[#1a73e8] flex items-center justify-center">
          <i data-lucide="code" class="w-4 h-4"></i>
        </div>
        <div>
          <h2 class="font-medium text-[15px] leading-tight">T-Code Studio</h2>
          <p class="text-[12px] text-[#5f6368] dark:text-[#9aa0a6]">Powered by OpenRouter</p>
        </div>
      </div>
      <button id="closeCodeStudio" class="p-2 hover:bg-[#f0f4f9] dark:hover:bg-[#2a2b2f] rounded-full">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
    </div>

    <div class="flex-1 overflow-hidden flex flex-col sm:flex-row">
      <!-- Left side: Code Input/Output -->
      <div class="flex-1 flex flex-col border-b sm:border-b-0 sm:border-r border-[#e5e7eb] dark:border-[#2f3032]">
        <div class="flex-1 overflow-auto p-4 flex flex-col">
          <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mb-2">Prompt / Codice da analizzare</label>
          <textarea id="codeStudioInput" class="w-full h-32 p-3 bg-[#f8fafc] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl outline-none resize-none text-[14px] mb-4" placeholder="Cosa deve fare il codice? Oppure incolla qui il codice da debuggare..."></textarea>
          
          <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mb-2">Risposta / Codice Generato</label>
          <div id="codeStudioOutput" class="flex-1 w-full p-4 bg-[#f8fafc] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl overflow-auto text-[14px] font-mono ai-content relative">
            <span class="text-gray-400">Il risultato apparirà qui...</span>
          </div>
        </div>
        <div class="p-4 border-t border-[#e5e7eb] dark:border-[#2f3032] bg-white dark:bg-[#1c1d1f]">
          <button id="codeStudioRunBtn" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-[#1a73e8] to-[#8b5cf6] text-white font-medium shadow-md hover:opacity-90 transition flex justify-center items-center gap-2">
            <i data-lucide="play" class="w-4 h-4"></i> Esegui Task
          </button>
        </div>
      </div>

      <!-- Right side: Settings -->
      <div class="w-full sm:w-[280px] p-4 flex flex-col gap-6 overflow-y-auto bg-[#f8fafc] dark:bg-[#1e1f20]">
        
        <div>
          <label class="text-[13px] font-semibold block mb-2">Modalità Operativa</label>
          <div class="flex flex-col gap-2">
            <label class="flex items-center gap-2 p-2 rounded-lg border border-[#e5e7eb] dark:border-[#2f3032] bg-white dark:bg-[#131314] cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition">
              <input type="radio" name="codeStudioMode" value="agent" class="accent-[#1a73e8]" checked>
              <span class="text-[14px]">API T-Code Agent</span>
            </label>
            <label class="flex items-center gap-2 p-2 rounded-lg border border-[#e5e7eb] dark:border-[#2f3032] bg-white dark:bg-[#131314] cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition">
              <input type="radio" name="codeStudioMode" value="reviewer" class="accent-[#1a73e8]">
              <span class="text-[14px]">T-Ai Code Reviewer</span>
            </label>
          </div>
        </div>

        <div>
          <label class="text-[13px] font-semibold block mb-2">OpenRouter API Key</label>
          <input type="password" id="openrouterKey" placeholder="sk-or-v1-..." class="w-full px-3 py-2 bg-white dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] rounded-lg text-[13px] outline-none focus:border-[#1a73e8] transition">
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-1">Richiesta per utilizzare i 300+ modelli. La chiave viene salvata localmente nel browser.</p>
        </div>

        <div>
          <label class="text-[13px] font-semibold block mb-2">Modello OpenRouter</label>
          <input type="text" id="openrouterModelInput" value="meta-llama/llama-3-8b-instruct:free" class="w-full px-3 py-2 bg-white dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] rounded-lg text-[13px] outline-none focus:border-[#1a73e8] transition">
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-1">Scegli tra i modelli gratuiti o premium di OpenRouter (es. anthropic/claude-3-opus).</p>
        </div>
      </div>
    </div>
  </aside>
"""

# Insert HTML after canvasPanel
canvas_end_idx = content.find('  <!-- Auth/Login Screen -->')
if canvas_end_idx != -1:
    content = content[:canvas_end_idx] + code_studio_html + content[canvas_end_idx:]
else:
    content = content.replace('</body>', code_studio_html + '\n</body>')

# 2. JS for Code Studio
code_studio_js = """
  // --- T-Code Studio Logic ---
  const codeStudioPanel = document.getElementById('codeStudioPanel');
  const closeCodeStudioBtn = document.getElementById('closeCodeStudio');
  const codeStudioInput = document.getElementById('codeStudioInput');
  const codeStudioOutput = document.getElementById('codeStudioOutput');
  const codeStudioRunBtn = document.getElementById('codeStudioRunBtn');
  const openrouterKeyInput = document.getElementById('openrouterKey');
  const openrouterModelInput = document.getElementById('openrouterModelInput');

  // Load saved key
  const savedOrKey = localStorage.getItem('openrouter-key');
  if(savedOrKey) openrouterKeyInput.value = savedOrKey;
  const savedOrModel = localStorage.getItem('openrouter-model');
  if(savedOrModel) openrouterModelInput.value = savedOrModel;

  openrouterKeyInput.addEventListener('change', () => localStorage.setItem('openrouter-key', openrouterKeyInput.value));
  openrouterModelInput.addEventListener('change', () => localStorage.setItem('openrouter-model', openrouterModelInput.value));

  window.openCodeStudio = function() {
    codeStudioPanel.classList.remove('translate-x-full');
    history.pushState({ modal: 'codeStudio' }, '', '');
    if(window.lucide) lucide.createIcons();
  };

  window.closeCodeStudio = function() {
    codeStudioPanel.classList.add('translate-x-full');
  };

  if(closeCodeStudioBtn) {
    closeCodeStudioBtn.addEventListener('click', () => {
      if(history.state && history.state.modal === 'codeStudio') history.back();
      else closeCodeStudio();
    });
  }

  codeStudioRunBtn.addEventListener('click', async () => {
    const prompt = codeStudioInput.value.trim();
    const apiKey = openrouterKeyInput.value.trim();
    const model = openrouterModelInput.value.trim() || 'meta-llama/llama-3-8b-instruct:free';
    const mode = document.querySelector('input[name="codeStudioMode"]:checked').value;

    if(!prompt) return alert('Inserisci un prompt o del codice!');
    if(!apiKey) return alert('Inserisci una OpenRouter API Key valida nelle impostazioni a destra!');

    codeStudioRunBtn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Elaborazione...';
    codeStudioRunBtn.disabled = true;
    codeStudioOutput.innerHTML = '<div class="text-[#5f6368] dark:text-[#9aa0a6] animate-pulse">In attesa della risposta da OpenRouter...</div>';
    if(window.lucide) lucide.createIcons();

    let systemPrompt = '';
    if(mode === 'reviewer') {
      systemPrompt = "Sei T-Ai Code Reviewer, un ingegnere software esperto. Il tuo compito è analizzare il codice fornito dall'utente, trovare bug, vulnerabilità di sicurezza e problemi di performance, e suggerire fix con spiegazioni e codice corretto formattato in markdown.";
    } else {
      systemPrompt = "Sei API T-Code Agent, un programmatore autonomo formidabile. Scrivi codice pulito, efficiente e commentato in base alle istruzioni dell'utente. Restituisci principalmente codice pronto all'uso formattato in markdown.";
    }

    try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'HTTP-Referer': window.location.href,
          'X-Title': 'T-Ai Code Studio',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: model,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: prompt }
          ]
        })
      });

      const data = await response.json();
      if(data.error) {
        codeStudioOutput.innerHTML = `<div class="text-red-500">Errore OpenRouter: ${data.error.message}</div>`;
      } else {
        const resultText = data.choices[0].message.content;
        codeStudioOutput.innerHTML = marked.parse(resultText);
        // Highlight syntax
        if(window.Prism) {
          codeStudioOutput.querySelectorAll('pre code').forEach((block) => {
            Prism.highlightElement(block);
          });
        }
      }
    } catch(err) {
      codeStudioOutput.innerHTML = `<div class="text-red-500">Errore di rete: ${err.message}</div>`;
    } finally {
      codeStudioRunBtn.innerHTML = '<i data-lucide="play" class="w-4 h-4"></i> Esegui Task';
      codeStudioRunBtn.disabled = false;
      if(window.lucide) lucide.createIcons();
    }
  });

  // Aggiorna History API global (popstate)
  const origPopstate = window.onpopstate;
  window.addEventListener('popstate', (e) => {
    closeCodeStudio(); // chiudi code studio se era aperto
  });

"""

# Inject JS before closing script
parts = content.rsplit('</script>', 1)
content = parts[0] + code_studio_js + '\n</script>' + parts[1]

# 3. Modify chip click to open Code Studio
content = content.replace(
    "else if (val === 'Codice') promptInput.placeholder = 'Cosa deve fare il codice?';",
    "else if (val === 'Codice') { openCodeStudio(); setTimeout(()=>{ chip.click(); }, 100); return; }"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("T-Code Studio logic integrated!")
