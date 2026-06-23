#!/usr/bin/env python3
"""Patch index.html: i18n, API fallback, cloud sync, import/export."""
import re

FILE = "/home/clocky/T-Ai/index.html"
with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

changes = 0

# ====================================================================
# 1) Add "Privacy e Dati" section in Settings Modal (before "Elimina Account")
# ====================================================================
privacy_section = '''        <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-2 flex items-center gap-1.5" data-i18n="settings_privacy">
            <i data-lucide="shield" class="w-4 h-4"></i> Privacy e Dati
          </label>
          <div class="grid grid-cols-1 gap-2">
            <button onclick="exportDataJSON()" class="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] font-medium transition border border-[#e5e7eb] dark:border-[#2f3032]">
              <i data-lucide="download" class="w-4 h-4 text-[#1a73e8]"></i> <span data-i18n="export_data">Esporta Dati (JSON)</span>
            </button>
            <label class="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] font-medium transition border border-[#e5e7eb] dark:border-[#2f3032] cursor-pointer">
              <i data-lucide="upload" class="w-4 h-4 text-[#8b5cf6]"></i> <span data-i18n="import_data">Importa Dati (JSON)</span>
              <input type="file" accept=".json" onchange="importDataJSON(event)" hidden>
            </label>
            <button onclick="syncToCloud()" id="syncCloudBtn" class="flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-gradient-to-r from-[#1a73e8]/10 to-[#8b5cf6]/10 hover:from-[#1a73e8]/20 hover:to-[#8b5cf6]/20 text-[13px] font-medium transition border border-[#1a73e8]/20">
              <i data-lucide="cloud" class="w-4 h-4 text-[#1a73e8]"></i> <span data-i18n="sync_cloud">Sincronizza sul Cloud</span>
            </button>
          </div>
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-1.5" data-i18n="privacy_hint">Esporta i tuoi dati per trasferirli su un altro dispositivo in modo privato, oppure sincronizza con il cloud se hai un account.</p>
        </div>
'''
if 'exportDataJSON' not in html:
    html = html.replace(
        '''        <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
          <button onclick="deleteAccount()"''',
        privacy_section + '''        <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
          <button onclick="deleteAccount()"'''
    )
    changes += 1
    print("[1] Privacy section aggiunta nelle Impostazioni.")

# ====================================================================
# 2) Inject ALL_KEYS_FAILED handling in the JS fetch /generate calls
# ====================================================================
old_fetch_handler = "if (data.response) return data.response;\n        if (data.notice) toast(data.notice);"
new_fetch_handler = """if (data.error === 'ALL_KEYS_FAILED') { showApiKeyFallback(); return '⚠️ Le API Key del server sono esaurite. Inserisci la tua chiave personale nel pannello che è apparso, oppure riprova più tardi.'; }
        if (data.response) return data.response;
        if (data.notice) toast(data.notice);"""
if 'ALL_KEYS_FAILED' not in html:
    html = html.replace(old_fetch_handler, new_fetch_handler, 1)
    changes += 1
    print("[2] ALL_KEYS_FAILED handler iniettato nel primo fetch.")

old_fetch_handler2 = "if (data.response) return data.response;\n        if (data.gpt_available === false && data.notice) toast(data.notice);"
new_fetch_handler2 = """if (data.error === 'ALL_KEYS_FAILED') { showApiKeyFallback(); return '⚠️ Le API Key del server sono esaurite. Inserisci la tua chiave personale nel pannello che è apparso, oppure riprova più tardi.'; }
        if (data.response) return data.response;
        if (data.gpt_available === false && data.notice) toast(data.notice);"""
if 'ALL_KEYS_FAILED' not in html.split(new_fetch_handler.split('\n')[0], 1)[-1]:
    html = html.replace(old_fetch_handler2, new_fetch_handler2, 1)
    changes += 1
    print("[2b] ALL_KEYS_FAILED handler iniettato nel secondo fetch.")

# ====================================================================
# 3) Add custom_api_key to /generate request bodies
# ====================================================================
old_body1 = "body: JSON.stringify({ provider: 'openai', model: 'gpt-4o-mini', messages: normalized })"
new_body1 = "body: JSON.stringify({ provider: 'openai', model: 'gpt-4o-mini', messages: normalized, custom_api_key: localStorage.getItem('tai_custom_api_key') || undefined, custom_provider: localStorage.getItem('tai_custom_provider') || undefined })"
html = html.replace(old_body1, new_body1)
changes += 1
print("[3] custom_api_key aggiunto ai body delle richieste /generate.")

# ====================================================================
# 4) Inject the mega JS block before </body>: i18n, sync, fallback UI
# ====================================================================
mega_js = '''
<!-- API Key Fallback Modal -->
<div id="apiKeyFallbackPanel" class="hidden fixed bottom-24 left-1/2 -translate-x-1/2 z-[60] w-[92%] max-w-[500px] bg-white dark:bg-[#1e1f20] rounded-2xl shadow-2xl border border-[#e5e7eb] dark:border-[#2f3032] p-5 fade-in">
  <div class="flex items-center justify-between mb-3">
    <h3 class="font-semibold text-[15px] flex items-center gap-2"><i data-lucide="key" class="w-4 h-4 text-[#f59e0b]"></i> <span data-i18n="fallback_title">API Key Personale</span></h3>
    <button onclick="document.getElementById('apiKeyFallbackPanel').classList.add('hidden')" class="p-1.5 hover:bg-black/5 dark:hover:bg-white/10 rounded-full"><i data-lucide="x" class="w-4 h-4"></i></button>
  </div>
  <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6] mb-3" data-i18n="fallback_desc">I server di T-Ai sono sovraccarichi. Inserisci una tua chiave API gratuita per continuare:</p>
  <select id="fallbackProvider" class="w-full px-3 py-2 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] text-[13px] mb-2">
    <option value="groq">Groq (Gratis)</option>
    <option value="openrouter">OpenRouter (Gratis)</option>
    <option value="gemini">Google Gemini (Gratis)</option>
    <option value="openai">OpenAI (A pagamento)</option>
  </select>
  <input id="fallbackApiKey" type="text" placeholder="Incolla qui la tua API Key..." class="w-full px-3 py-2 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] text-[13px] mb-3 outline-none focus:ring-2 focus:ring-[#1a73e8]/30">
  <div class="flex flex-wrap gap-1.5 mb-3">
    <a href="https://console.groq.com/keys" target="_blank" class="text-[11px] px-2 py-1 rounded-full bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] border border-[#e5e7eb] dark:border-[#2f3032] text-[#1a73e8]">🔑 Groq</a>
    <a href="https://openrouter.ai/keys" target="_blank" class="text-[11px] px-2 py-1 rounded-full bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] border border-[#e5e7eb] dark:border-[#2f3032] text-[#1a73e8]">🔑 OpenRouter</a>
    <a href="https://aistudio.google.com/app/apikey" target="_blank" class="text-[11px] px-2 py-1 rounded-full bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] border border-[#e5e7eb] dark:border-[#2f3032] text-[#1a73e8]">🔑 Gemini</a>
    <a href="https://platform.openai.com/api-keys" target="_blank" class="text-[11px] px-2 py-1 rounded-full bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] border border-[#e5e7eb] dark:border-[#2f3032] text-[#1a73e8]">🔑 OpenAI</a>
  </div>
  <button onclick="saveCustomApiKey()" class="w-full py-2.5 rounded-xl bg-gradient-to-r from-[#1a73e8] to-[#8b5cf6] text-white font-medium text-[13px] hover:opacity-90 transition" data-i18n="save_key">Salva Chiave</button>
</div>

<script>
// ===== I18N SYSTEM =====
const i18n = {
  it: {
    welcome_title: "Ciao, sono T-Ai",
    welcome_sub: "Come posso aiutarti oggi?",
    new_chat: "Nuova chat",
    recent: "Recenti",
    dark_theme: "Tema scuro",
    settings: "Impostazioni",
    install: "Installa T-Ai",
    ask_placeholder: "Chiedi a T-Ai",
    image_chip: "Immagine",
    code_chip: "Codice",
    video_chip: "Video",
    web_search: "Cerca nel Web",
    settings_title: "Impostazioni",
    name_label: "Come ti chiamo",
    style_label: "Stile di risposta",
    model_label: "Modello predefinito",
    persona_label: "Persona",
    temp_label: "Temperatura",
    length_label: "Lunghezza",
    lang_ui: "Lingua interfaccia",
    lang_model: "Lingua del modello",
    cancel: "Annulla",
    save: "Salva",
    export_data: "Esporta Dati (JSON)",
    import_data: "Importa Dati (JSON)",
    sync_cloud: "Sincronizza sul Cloud",
    settings_privacy: "Privacy e Dati",
    privacy_hint: "Esporta i tuoi dati per trasferirli su un altro dispositivo in modo privato, oppure sincronizza con il cloud se hai un account.",
    fallback_title: "API Key Personale",
    fallback_desc: "I server di T-Ai sono sovraccarichi. Inserisci una tua chiave API gratuita per continuare:",
    save_key: "Salva Chiave",
    delete_account: "Elimina Account e Dati",
    disclaimer: "T-Ai \\u00e8 un modello AI e puo commetere errori, verifica le risposte importanti...",
    terms_link: "Clicca qui per i termini e condizioni di uso di T-Ai",
    sug1: "Crea un'immagine di...",
    sug2: "Scrivi codice Python per...",
    sug3: "Riassumi questo video",
    sug4: "Genera idea per TikTok",
    copy: "Copia",
    insert_chat: "Inserisci in chat",
    auto_save: "Salvataggio automatico",
    canvas_placeholder: "Inizia a scrivere... Artifacts / Canvas \\u00e8 perfetto per articoli, codice lungo, bozze e brainstorming.",
    loading_time: "Tempo stimato: 5s",
  },
  en: {
    welcome_title: "Hi, I'm T-Ai",
    welcome_sub: "How can I help you today?",
    new_chat: "New chat",
    recent: "Recent",
    dark_theme: "Dark theme",
    settings: "Settings",
    install: "Install T-Ai",
    ask_placeholder: "Ask T-Ai",
    image_chip: "Image",
    code_chip: "Code",
    video_chip: "Video",
    web_search: "Search the Web",
    settings_title: "Settings",
    name_label: "What should I call you",
    style_label: "Response style",
    model_label: "Default model",
    persona_label: "Persona",
    temp_label: "Temperature",
    length_label: "Length",
    lang_ui: "Interface language",
    lang_model: "Model language",
    cancel: "Cancel",
    save: "Save",
    export_data: "Export Data (JSON)",
    import_data: "Import Data (JSON)",
    sync_cloud: "Sync to Cloud",
    settings_privacy: "Privacy & Data",
    privacy_hint: "Export your data to transfer to another device privately, or sync to cloud if you have an account.",
    fallback_title: "Personal API Key",
    fallback_desc: "T-Ai servers are overloaded. Enter your own free API key to continue:",
    save_key: "Save Key",
    delete_account: "Delete Account & Data",
    disclaimer: "T-Ai is an AI model and can make mistakes, verify important answers...",
    terms_link: "Click here for T-Ai terms of use",
    sug1: "Create an image of...",
    sug2: "Write Python code to...",
    sug3: "Summarize this video",
    sug4: "Generate a TikTok idea",
    copy: "Copy",
    insert_chat: "Insert in chat",
    auto_save: "Auto-save",
    canvas_placeholder: "Start writing... Artifacts / Canvas is perfect for articles, long code, drafts and brainstorming.",
    loading_time: "Estimated time: 5s",
  },
  fr: {
    welcome_title: "Bonjour, je suis T-Ai",
    welcome_sub: "Comment puis-je vous aider aujourd'hui ?",
    new_chat: "Nouvelle discussion",
    recent: "R\\u00e9cents",
    dark_theme: "Th\\u00e8me sombre",
    settings: "Param\\u00e8tres",
    install: "Installer T-Ai",
    ask_placeholder: "Demandez \\u00e0 T-Ai",
    image_chip: "Image",
    code_chip: "Code",
    video_chip: "Vid\\u00e9o",
    web_search: "Rechercher sur le Web",
    settings_title: "Param\\u00e8tres",
    name_label: "Comment dois-je vous appeler",
    style_label: "Style de r\\u00e9ponse",
    model_label: "Mod\\u00e8le par d\\u00e9faut",
    persona_label: "Persona",
    temp_label: "Temp\\u00e9rature",
    length_label: "Longueur",
    lang_ui: "Langue de l'interface",
    lang_model: "Langue du mod\\u00e8le",
    cancel: "Annuler",
    save: "Enregistrer",
    export_data: "Exporter les donn\\u00e9es (JSON)",
    import_data: "Importer les donn\\u00e9es (JSON)",
    sync_cloud: "Synchroniser avec le Cloud",
    settings_privacy: "Confidentialit\\u00e9 et Donn\\u00e9es",
    privacy_hint: "Exportez vos donn\\u00e9es pour les transf\\u00e9rer vers un autre appareil de mani\\u00e8re priv\\u00e9e, ou synchronisez avec le cloud.",
    fallback_title: "Cl\\u00e9 API personnelle",
    fallback_desc: "Les serveurs de T-Ai sont surcharg\\u00e9s. Entrez votre propre cl\\u00e9 API gratuite pour continuer :",
    save_key: "Enregistrer la cl\\u00e9",
    delete_account: "Supprimer le compte et les donn\\u00e9es",
    disclaimer: "T-Ai est un mod\\u00e8le IA et peut commettre des erreurs, v\\u00e9rifiez les r\\u00e9ponses importantes...",
    terms_link: "Cliquez ici pour les conditions d'utilisation de T-Ai",
    sug1: "Cr\\u00e9er une image de...",
    sug2: "\\u00c9crire du code Python pour...",
    sug3: "R\\u00e9sumer cette vid\\u00e9o",
    sug4: "G\\u00e9n\\u00e9rer une id\\u00e9e TikTok",
    copy: "Copier",
    insert_chat: "Ins\\u00e9rer dans le chat",
    auto_save: "Sauvegarde automatique",
    canvas_placeholder: "Commencez \\u00e0 \\u00e9crire... Artifacts / Canvas est parfait pour les articles, le code long, les brouillons et le brainstorming.",
    loading_time: "Temps estim\\u00e9 : 5s",
  },
  es: {
    welcome_title: "Hola, soy T-Ai",
    welcome_sub: "\\u00bfC\\u00f3mo puedo ayudarte hoy?",
    new_chat: "Nuevo chat",
    recent: "Recientes",
    dark_theme: "Tema oscuro",
    settings: "Configuraci\\u00f3n",
    install: "Instalar T-Ai",
    ask_placeholder: "Pregunta a T-Ai",
    image_chip: "Imagen",
    code_chip: "C\\u00f3digo",
    video_chip: "Video",
    web_search: "Buscar en la Web",
    settings_title: "Configuraci\\u00f3n",
    name_label: "C\\u00f3mo te llamo",
    style_label: "Estilo de respuesta",
    model_label: "Modelo predeterminado",
    persona_label: "Persona",
    temp_label: "Temperatura",
    length_label: "Longitud",
    lang_ui: "Idioma de la interfaz",
    lang_model: "Idioma del modelo",
    cancel: "Cancelar",
    save: "Guardar",
    export_data: "Exportar Datos (JSON)",
    import_data: "Importar Datos (JSON)",
    sync_cloud: "Sincronizar con la Nube",
    settings_privacy: "Privacidad y Datos",
    privacy_hint: "Exporta tus datos para transferirlos a otro dispositivo de forma privada, o sincroniza con la nube si tienes cuenta.",
    fallback_title: "Clave API Personal",
    fallback_desc: "Los servidores de T-Ai est\\u00e1n sobrecargados. Introduce tu propia clave API gratuita para continuar:",
    save_key: "Guardar Clave",
    delete_account: "Eliminar Cuenta y Datos",
    disclaimer: "T-Ai es un modelo de IA y puede cometer errores, verifica las respuestas importantes...",
    terms_link: "Haz clic aqu\\u00ed para los t\\u00e9rminos y condiciones de uso de T-Ai",
    sug1: "Crear una imagen de...",
    sug2: "Escribir c\\u00f3digo Python para...",
    sug3: "Resumir este video",
    sug4: "Generar idea para TikTok",
    copy: "Copiar",
    insert_chat: "Insertar en chat",
    auto_save: "Guardado autom\\u00e1tico",
    canvas_placeholder: "Empieza a escribir... Artifacts / Canvas es perfecto para art\\u00edculos, c\\u00f3digo largo, borradores y lluvia de ideas.",
    loading_time: "Tiempo estimado: 5s",
  },
  de: {
    welcome_title: "Hallo, ich bin T-Ai",
    welcome_sub: "Wie kann ich dir heute helfen?",
    new_chat: "Neuer Chat",
    recent: "K\\u00fcrzlich",
    dark_theme: "Dunkles Thema",
    settings: "Einstellungen",
    install: "T-Ai installieren",
    ask_placeholder: "Frag T-Ai",
    image_chip: "Bild",
    code_chip: "Code",
    video_chip: "Video",
    web_search: "Im Web suchen",
    settings_title: "Einstellungen",
    name_label: "Wie soll ich dich nennen",
    style_label: "Antwortstil",
    model_label: "Standardmodell",
    persona_label: "Persona",
    temp_label: "Temperatur",
    length_label: "L\\u00e4nge",
    lang_ui: "Oberfl\\u00e4chensprache",
    lang_model: "Modellsprache",
    cancel: "Abbrechen",
    save: "Speichern",
    export_data: "Daten exportieren (JSON)",
    import_data: "Daten importieren (JSON)",
    sync_cloud: "Mit Cloud synchronisieren",
    settings_privacy: "Datenschutz & Daten",
    privacy_hint: "Exportiere deine Daten, um sie privat auf ein anderes Ger\\u00e4t zu \\u00fcbertragen, oder synchronisiere mit der Cloud.",
    fallback_title: "Pers\\u00f6nlicher API-Schl\\u00fcssel",
    fallback_desc: "Die T-Ai-Server sind \\u00fcberlastet. Gib deinen eigenen kostenlosen API-Schl\\u00fcssel ein, um fortzufahren:",
    save_key: "Schl\\u00fcssel speichern",
    delete_account: "Konto und Daten l\\u00f6schen",
    disclaimer: "T-Ai ist ein KI-Modell und kann Fehler machen, \\u00fcberpr\\u00fcfe wichtige Antworten...",
    terms_link: "Klicke hier f\\u00fcr die Nutzungsbedingungen von T-Ai",
    sug1: "Ein Bild erstellen von...",
    sug2: "Python-Code schreiben f\\u00fcr...",
    sug3: "Dieses Video zusammenfassen",
    sug4: "TikTok-Idee generieren",
    copy: "Kopieren",
    insert_chat: "In Chat einf\\u00fcgen",
    auto_save: "Automatisches Speichern",
    canvas_placeholder: "Fang an zu schreiben... Artifacts / Canvas ist perfekt f\\u00fcr Artikel, langen Code, Entw\\u00fcrfe und Brainstorming.",
    loading_time: "Gesch\\u00e4tzte Zeit: 5s",
  }
};

function getLang() {
  const uiLang = localStorage.getItem('tai_ui_language') || 'it-IT';
  if (uiLang.startsWith('en')) return 'en';
  if (uiLang.startsWith('fr')) return 'fr';
  if (uiLang.startsWith('es')) return 'es';
  if (uiLang.startsWith('de')) return 'de';
  return 'it';
}

function t(key) {
  const lang = getLang();
  return (i18n[lang] && i18n[lang][key]) || (i18n['it'] && i18n['it'][key]) || key;
}

function applyLanguage() {
  // data-i18n attribute based
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = t(key);
    if (val) el.textContent = val;
  });
  // Special elements by selector
  const welcomeH1 = document.querySelector('#welcome h1');
  if (welcomeH1) welcomeH1.textContent = t('welcome_title');
  const welcomeP = document.querySelector('#welcome h1 + p');
  if (welcomeP) welcomeP.textContent = t('welcome_sub');
  
  // Sidebar
  const newChatSpan = document.querySelector('#newChatBtn .sidebar-text');
  if (newChatSpan) newChatSpan.textContent = t('new_chat');
  
  const darkSpan = document.querySelector('#darkToggle .sidebar-text');
  if (darkSpan) darkSpan.textContent = t('dark_theme');

  const settingsSpan = document.querySelector('#settingsBtn .sidebar-text');
  if (settingsSpan) settingsSpan.textContent = t('settings');

  // Placeholder
  const promptInput = document.getElementById('promptInput');
  if (promptInput) promptInput.placeholder = t('ask_placeholder');

  // Chips
  const chips = document.querySelectorAll('.chip');
  const chipMap = { 'Immagine': 'image_chip', 'Codice': 'code_chip', 'Video': 'video_chip' };
  // Settings modal title
  const settingsTitle = document.querySelector('#settingsModal h2');
  if (settingsTitle) settingsTitle.textContent = t('settings_title');

  // Settings buttons
  const cancelBtn = document.querySelector('#settingsModal button[onclick="closeSettings()"]');
  // Suggestion texts
  const suggestions = document.querySelectorAll('.suggestion p');
  const sugKeys = ['sug1','sug2','sug3','sug4'];
  suggestions.forEach((s, i) => { if (sugKeys[i]) s.textContent = t(sugKeys[i]); });

  // Canvas
  const canvasEditor = document.getElementById('canvasEditor');
  if (canvasEditor) canvasEditor.placeholder = t('canvas_placeholder');
  const canvasCopy = document.getElementById('canvasCopy');
  if (canvasCopy) canvasCopy.textContent = t('copy');
  const canvasSave = document.getElementById('canvasSave');
  if (canvasSave) canvasSave.textContent = t('insert_chat');

  // Loading
  const loadingTime = document.getElementById('loadingTime');
  if (loadingTime) loadingTime.textContent = t('loading_time');

  // Recenti
  const recenti = document.querySelector('.sidebar-text.text-\\\\[12px\\\\]');

  // Install button
  const installSpan = document.querySelector('button[onclick="openInstallModal()"] .sidebar-text');
  if (installSpan) installSpan.textContent = t('install');
  
  // Search web btn
  const webSearchBtn = document.getElementById('webSearchBtn');
  if (webSearchBtn) {
    const span = webSearchBtn.childNodes;
    for (let n of span) {
      if (n.nodeType === 3 && n.textContent.trim()) { n.textContent = ' ' + t('web_search'); break; }
    }
  }

  if (window.lucide) lucide.createIcons();
  console.log('[T-Ai] Lingua UI applicata:', getLang());
}

// ===== SAVE SETTINGS HOOK =====
const _origSaveSettings = window.saveSettings;
window.saveSettings = function() {
  const uiLang = document.getElementById('uiLanguage');
  if (uiLang) localStorage.setItem('tai_ui_language', uiLang.value);
  if (_origSaveSettings) _origSaveSettings();
  setTimeout(applyLanguage, 100);
};

// ===== API KEY FALLBACK =====
window.showApiKeyFallback = function() {
  const panel = document.getElementById('apiKeyFallbackPanel');
  if (panel) {
    panel.classList.remove('hidden');
    if (window.lucide) lucide.createIcons();
  }
};

window.saveCustomApiKey = function() {
  const key = document.getElementById('fallbackApiKey').value.trim();
  const provider = document.getElementById('fallbackProvider').value;
  if (!key) { alert('Inserisci una chiave API valida!'); return; }
  localStorage.setItem('tai_custom_api_key', key);
  localStorage.setItem('tai_custom_provider', provider);
  document.getElementById('apiKeyFallbackPanel').classList.add('hidden');
  if (window.toast) toast('Chiave salvata! Riprova a inviare il messaggio.');
};

// ===== EXPORT / IMPORT DATA =====
window.exportDataJSON = function() {
  const data = {};
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    data[key] = localStorage.getItem(key);
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'T-Ai_backup_' + new Date().toISOString().split('T')[0] + '.json';
  a.click();
  URL.revokeObjectURL(a.href);
  if (window.toast) toast('Dati esportati con successo!');
};

window.importDataJSON = function(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      Object.keys(data).forEach(key => localStorage.setItem(key, data[key]));
      if (window.toast) toast('Dati importati! Ricaricamento...');
      setTimeout(() => location.reload(), 1500);
    } catch (err) {
      alert('File JSON non valido.');
    }
  };
  reader.readAsText(file);
};

// ===== CLOUD SYNC =====
window.syncToCloud = function() {
  const email = localStorage.getItem('tai_user_email');
  if (!email) {
    alert('Devi prima accedere con un account per sincronizzare i dati.');
    return;
  }
  const data = {};
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    data[key] = localStorage.getItem(key);
  }
  const backend = window._resolveTaiBackend ? _resolveTaiBackend() : '';
  if (!backend) { alert('Backend non raggiungibile.'); return; }
  
  fetch(backend + '/sync/upload', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ email, payload: data })
  })
  .then(r => r.json())
  .then(d => { if (window.toast) toast('Dati sincronizzati sul cloud!'); })
  .catch(e => { alert('Errore di sincronizzazione: ' + e.message); });
};

window.syncFromCloud = function(email) {
  const backend = window._resolveTaiBackend ? _resolveTaiBackend() : '';
  if (!backend || !email) return;
  
  fetch(backend + '/sync/download', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ email })
  })
  .then(r => r.json())
  .then(d => {
    if (d.payload && typeof d.payload === 'object') {
      Object.keys(d.payload).forEach(key => {
        if (!localStorage.getItem(key)) {
          localStorage.setItem(key, d.payload[key]);
        }
      });
      console.log('[T-Ai] Dati cloud scaricati per', email);
      if (window.toast) toast('Dati sincronizzati dal cloud!');
    }
  })
  .catch(e => console.warn('[T-Ai] Sync download error:', e));
};

// Hook into auth to save email and trigger sync
const _origSubmitAuth = window.submitAuth;
window.submitAuth = async function() {
  if (_origSubmitAuth) await _origSubmitAuth();
  const email = document.getElementById('authEmail')?.value?.trim();
  if (email) {
    localStorage.setItem('tai_user_email', email);
    syncFromCloud(email);
  }
};

// Apply language on load
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(applyLanguage, 500);
  // Auto-sync on load if logged in
  const email = localStorage.getItem('tai_user_email');
  if (email) syncFromCloud(email);
});
</script>
'''
if 'applyLanguage' not in html:
    html = html.replace('</body>', mega_js + '\n</body>')
    changes += 1
    print("[4] Mega JS block (i18n + sync + fallback) iniettato prima di </body>.")

# ====================================================================
# SAVE
# ====================================================================
with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\\nDone! {changes} modifiche applicate a index.html.")
