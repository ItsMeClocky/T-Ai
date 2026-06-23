import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Bottom Sheet HTML just before the end of body
bottom_sheet_html = """
  <!-- Bottom Sheet -->
  <div id="bottomSheetOverlay" class="fixed inset-0 bg-black/40 z-[60] hidden transition-opacity opacity-0 duration-300" onclick="closeBottomSheet()"></div>
  <div id="bottomSheet" class="fixed inset-x-0 bottom-0 bg-white dark:bg-[#131314] rounded-t-3xl shadow-[0_-8px_30px_rgba(0,0,0,0.12)] dark:shadow-[0_-8px_30px_rgba(0,0,0,0.4)] z-[70] transform translate-y-full transition-transform duration-300 ease-out flex flex-col max-h-[85vh]">
    <div class="flex justify-center p-3">
      <div class="w-12 h-1.5 bg-gray-300 dark:bg-gray-600 rounded-full"></div>
    </div>
    <div class="px-6 pb-2">
      <h3 id="bottomSheetTitle" class="text-xl font-semibold mb-4">Seleziona</h3>
    </div>
    <div id="bottomSheetContent" class="overflow-y-auto px-4 pb-8 space-y-1">
      <!-- Options inserted dynamically -->
    </div>
  </div>
"""
content = content.replace('</body>', bottom_sheet_html + '\n</body>')

# 2. Add Bottom Sheet JS logic
bottom_sheet_js = """
  // Bottom Sheet Logic
  function openBottomSheet(targetInputId, targetLabelId, title, optionsArray, currentValue) {
    const overlay = document.getElementById('bottomSheetOverlay');
    const sheet = document.getElementById('bottomSheet');
    const titleEl = document.getElementById('bottomSheetTitle');
    const contentEl = document.getElementById('bottomSheetContent');

    titleEl.innerText = title;
    contentEl.innerHTML = '';

    optionsArray.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = "w-full flex items-center justify-between px-4 py-3 rounded-xl hover:bg-[#f0f4f9] dark:hover:bg-[#1e1f20] transition";
      const isSelected = opt.value === currentValue;
      btn.innerHTML = `<span class="text-[15px] ${isSelected ? 'font-semibold text-[#1a73e8]' : 'text-[#1f1f1f] dark:text-[#e3e3e3]'}">${opt.label}</span>
                       ${isSelected ? '<i data-lucide="check" class="w-5 h-5 text-[#1a73e8]"></i>' : ''}`;
      btn.onclick = () => {
        document.getElementById(targetInputId).value = opt.value;
        document.getElementById(targetLabelId).innerText = opt.label;
        closeBottomSheet();
      };
      contentEl.appendChild(btn);
    });
    
    lucide.createIcons();
    
    history.pushState({ modal: 'bottomSheet' }, '');
    overlay.classList.remove('hidden');
    sheet.classList.remove('translate-y-full');
    
    setTimeout(() => overlay.classList.remove('opacity-0'), 10);
  }

  function closeBottomSheet(fromPopState=false) {
    const overlay = document.getElementById('bottomSheetOverlay');
    const sheet = document.getElementById('bottomSheet');
    
    if(!fromPopState) history.back();
    
    sheet.classList.add('translate-y-full');
    overlay.classList.remove('opacity-0');
    setTimeout(() => overlay.classList.add('opacity-0'), 10); // trigger transition
    
    setTimeout(() => overlay.classList.add('hidden'), 300);
  }
"""
content = content.replace('// History API Routing for Modals', bottom_sheet_js + '\n  // History API Routing for Modals')

# Update popstate
content = content.replace('if (isSettingsOpen) closeSettings(true);', 'if (!document.getElementById(\'bottomSheet\').classList.contains(\'translate-y-full\')) { closeBottomSheet(true); return; }\n    if (isSettingsOpen) closeSettings(true);')

# 3. Replace <select> with <button> + <input type="hidden">
# We have 4 selects. We will define their options in JS globally.
options_js = """
  const optionsModel = [
    {value: 'T-Ai 1.8 GIIP-mini', label: 'T-Ai 1.8 GIIP-mini'},
    {value: 'T-Ai 1.7', label: 'T-Ai 1.7'},
    {value: 'T-Ai 1.7 GIIP-Y', label: 'T-Ai 1.7 GIIP-Y'},
    {value: 'T-Ai 1.6', label: 'T-Ai 1.6'},
    {value: 'T-Ai 1.6 SOLO-Y', label: 'T-Ai 1.6 SOLO-Y'},
    {value: 'T-Ai 1.5', label: 'T-Ai 1.5'},
    {value: 'T-Ai 1.5 SOLO-Y', label: 'T-Ai 1.5 SOLO-Y'},
    {value: 'T-Ai 1.4', label: 'T-Ai 1.4'},
    {value: 'T-Ai 1.4 SOLO-Y', label: 'T-Ai 1.4 SOLO-Y'},
    {value: 'T-Ai 1.3', label: 'T-Ai 1.3'},
    {value: 'T-Ai 1.3 SOLO-Y', label: 'T-Ai 1.3 SOLO-Y'}
  ];
  const optionsPersona = [
    {value: 'default', label: 'T-Ai Standard'},
    {value: 'tutor', label: 'Tutor paziente'},
    {value: 'coder', label: 'Code reviewer'},
    {value: 'siciliano', label: 'Siciliano diretto'},
    {value: 'psicologo', label: 'Psicologo breve'},
    {value: 't-emojai', label: 'T-EmojAI'}
  ];
  const optionsLangUi = [
    {value: 'it-IT', label: 'Italiano'},
    {value: 'en-US', label: 'English'},
    {value: 'es-ES', label: 'Español'},
    {value: 'fr-FR', label: 'Français'}
  ];
  const optionsLangModel = [
    {value: 'auto', label: 'Automatico'},
    {value: 'it-IT', label: 'Italiano'},
    {value: 'en-US', label: 'English'},
    {value: 'es-ES', label: 'Español'},
    {value: 'fr-FR', label: 'Français'},
    {value: 'de-DE', label: 'Deutsch'},
    {value: 'ja-JP', label: '日本語'},
    {value: 'ru-RU', label: 'Русский'},
    {value: 'zh-CN', label: '中文 (简体)'},
    {value: 'ar-SA', label: 'العربية'},
    {value: 'ko-KR', label: '한국어'},
    {value: 'hi-IN', label: 'हिन्दी'},
    {value: 'nl-NL', label: 'Nederlands'}
  ];
"""
content = content.replace('// Bottom Sheet Logic', options_js + '\n  // Bottom Sheet Logic')

# Update HTML inputs
import re

select_pattern1 = re.compile(r'<select id="defaultModel".*?</select>', re.DOTALL)
content = select_pattern1.sub('''<input type="hidden" id="defaultModel" value="T-Ai 1.8 GIIP-mini">
          <button type="button" onclick="openBottomSheet('defaultModel', 'defaultModelLabel', 'Seleziona Modello', optionsModel, document.getElementById('defaultModel').value)" class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] text-[14px]">
            <span id="defaultModelLabel">T-Ai 1.8 GIIP-mini</span>
            <i data-lucide="chevron-down" class="w-4 h-4 opacity-60"></i>
          </button>''', content)

select_pattern2 = re.compile(r'<select id="personaSelect".*?</select>', re.DOTALL)
content = select_pattern2.sub('''<input type="hidden" id="personaSelect" value="default">
          <button type="button" onclick="openBottomSheet('personaSelect', 'personaSelectLabel', 'Seleziona Persona', optionsPersona, document.getElementById('personaSelect').value)" class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] text-[14px]">
            <span id="personaSelectLabel">T-Ai Standard</span>
            <i data-lucide="chevron-down" class="w-4 h-4 opacity-60"></i>
          </button>''', content)

select_pattern3 = re.compile(r'<select id="uiLanguage".*?</select>', re.DOTALL)
content = select_pattern3.sub('''<input type="hidden" id="uiLanguage" value="it-IT">
          <button type="button" onclick="openBottomSheet('uiLanguage', 'uiLanguageLabel', 'Lingua Interfaccia', optionsLangUi, document.getElementById('uiLanguage').value)" class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] text-[14px]">
            <span id="uiLanguageLabel">Italiano</span>
            <i data-lucide="chevron-down" class="w-4 h-4 opacity-60"></i>
          </button>''', content)

select_pattern4 = re.compile(r'<select id="modelLanguage".*?</select>', re.DOTALL)
content = select_pattern4.sub('''<input type="hidden" id="modelLanguage" value="auto">
          <button type="button" onclick="openBottomSheet('modelLanguage', 'modelLanguageLabel', 'Lingua Risposte', optionsLangModel, document.getElementById('modelLanguage').value)" class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] text-[14px]">
            <span id="modelLanguageLabel">Automatico</span>
            <i data-lucide="chevron-down" class="w-4 h-4 opacity-60"></i>
          </button>''', content)

# 4. We need to update the labels when settings open, because init() sets the hidden input values but not the labels.
# Inside function openSettings()
open_settings_patch = """function openSettings() {
    history.pushState({ modal: 'settings' }, '');
    
    // Update labels to match input values
    const dm = document.getElementById('defaultModel').value;
    const ps = document.getElementById('personaSelect').value;
    const ul = document.getElementById('uiLanguage').value;
    const ml = document.getElementById('modelLanguage').value;
    
    document.getElementById('defaultModelLabel').innerText = optionsModel.find(o => o.value === dm)?.label || dm;
    document.getElementById('personaSelectLabel').innerText = optionsPersona.find(o => o.value === ps)?.label || ps;
    document.getElementById('uiLanguageLabel').innerText = optionsLangUi.find(o => o.value === ul)?.label || ul;
    document.getElementById('modelLanguageLabel').innerText = optionsLangModel.find(o => o.value === ml)?.label || ml;
"""
content = content.replace("function openSettings() {\n    history.pushState({ modal: 'settings' }, '');", open_settings_patch)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("BottomSheet Update Done")
