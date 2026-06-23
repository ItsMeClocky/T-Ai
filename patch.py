import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Sidebar HTML
content = re.sub(
    r'<div class="flex-1 overflow-y-auto px-3 scrollbar-thin">\s*<div id="chatList" class="space-y-0.5"></div>\s*</div>',
    '''<div class="flex-1 overflow-y-auto px-3 scrollbar-thin flex flex-col">
        <div class="px-1 mt-2 mb-3">
          <div class="relative">
            <i data-lucide="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#5f6368] dark:text-[#9aa0a6]"></i>
            <input id="searchChat" type="text" placeholder="Cerca chat..." class="w-full bg-transparent border border-[#e5e7eb] dark:border-[#3c4043] rounded-full pl-9 pr-3 py-1.5 text-[13px] outline-none focus:border-[#1a73e8] transition sidebar-text">
          </div>
        </div>
        <div id="chatList" class="space-y-0.5 flex-1 overflow-y-auto scrollbar-thin pb-4"></div>
      </div>''',
    content
)

# 2. Remove buttons from sidebar
content = re.sub(
    r'\s*<a href="features\.html" target="_blank"[^>]*>.*?</a>\s*<a href="terms\.html" target="_blank"[^>]*>.*?</a>',
    '',
    content,
    flags=re.DOTALL
)

# 3. Add to settings modal
settings_insert = '''        <div>
          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1.5">Link Utili</label>
          <div class="grid grid-cols-2 gap-3">
            <a href="features.html" target="_blank" class="flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] font-medium transition border border-[#e5e7eb] dark:border-[#2f3032]">
              <i data-lucide="star" class="w-4 h-4 text-[#f59e0b]"></i> Feature
            </a>
            <a href="terms.html" target="_blank" class="flex items-center justify-center gap-2 px-3 py-2 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] font-medium transition border border-[#e5e7eb] dark:border-[#2f3032]">
              <i data-lucide="file-text" class="w-4 h-4 text-[#5f6368] dark:text-[#9aa0a6]"></i> Termini
            </a>
          </div>
        </div>
'''
content = content.replace(
    '        </div>\n      </div>\n      <div class="p-4 border-t border-[#e5e7eb] dark:border-[#2f3032] flex justify-end">',
    settings_insert + '        </div>\n      </div>\n      <div class="p-4 border-t border-[#e5e7eb] dark:border-[#2f3032] flex justify-end">'
)

# 4. Footer text
content = content.replace(
    '<p class="text-[11px] text-center text-[#5f6368] dark:text-[#9aa0a6] mt-2.5">T-Ai è un modello AI e puo commetere errori, verifica le risposte importanti</p>',
    '<p class="text-[11px] text-center text-[#5f6368] dark:text-[#9aa0a6] mt-2.5">T-Ai è un modello AI e puo commetere errori, verifica le risposte importanti... <a href="terms.html" target="_blank" class="underline hover:text-black dark:hover:text-white">Clicca qui per i termini e condizioni di uso di T-Ai</a></p>'
)

# 5. Minimap HTML
content = content.replace(
    '<div id="messages" class="max-w-[840px] mx-auto px-4 md:px-6 py-6 space-y-6"></div>\n        </div>',
    '<div id="messages" class="max-w-[840px] mx-auto px-4 md:px-6 py-6 space-y-6"></div>\n          <div id="chatMinimap" class="fixed right-3 top-1/2 -translate-y-1/2 flex flex-col items-center gap-2 z-10 p-2"></div>\n        </div>'
)

# 6. Personas Object
personas_replacement = '''  const personas = {
    default: 'Sei T-Ai, un modello AI super intelligente, sicuro, privato e velocissimo basato sulla tecnologia Pollinations ed ECO-Pollinations. Rispondi in italiano in modo utile, conciso e super naturale. Offri risposte dettagliate e superiori agli altri modelli.',
    tutor: 'Sei un tutor paziente. Spiega passo-passo con esempi semplici.',
    coder: 'Sei un code reviewer senior. Dai codice pulito commentato in italiano.',
    siciliano: 'Parli diretto e caldo, con tono siciliano. Vai dritto al punto.',
    psicologo: 'Sei psicologo breve. Ascolti, validi, proponi 1-2 azioni concrete.',
    't-emojai': 'Sei T-EmojAI, un\\'intelligenza artificiale super espressiva! Usa moltissime emoji in ogni frase per esprimere emozioni e concetti. Sii estremamente amichevole, vivace e colorato! 🌟✨💖'
  };'''

content = re.sub(
    r'  const personas = \{.*?\};',
    personas_replacement,
    content,
    flags=re.DOTALL
)

# Also update persona Select HTML
content = content.replace(
    '<option value="psicologo">Psicologo</option>\n          </select>',
    '<option value="psicologo">Psicologo</option>\n            <option value="t-emojai">T-EmojAI</option>\n          </select>'
)

# 7. Add minimap logic to renderMessage
render_message_old = '''  function renderMessage(msg, animate=true) {
    const wrap = document.createElement('div');
    wrap.className = 'fade-in';'''

render_message_new = '''  function renderMessage(msg, animate=true) {
    const msgId = msg.id || 'msg-' + Date.now() + '-' + Math.floor(Math.random()*1000);
    msg.id = msgId;
    const wrap = document.createElement('div');
    wrap.id = msgId;
    wrap.className = 'fade-in';'''

content = content.replace(render_message_old, render_message_new)

# Add minimap dot at the end of renderMessage
render_message_append_old = "    messages.appendChild(wrap);\n    lucide.createIcons();"
render_message_append_new = '''    messages.appendChild(wrap);
    lucide.createIcons();
    const minimap = document.getElementById('chatMinimap');
    if (minimap) {
      const dot = document.createElement('div');
      dot.className = 'w-1.5 h-1.5 rounded-full cursor-pointer bg-gray-400 dark:bg-gray-500 hover:bg-[#1a73e8] transition relative group';
      dot.onclick = () => { document.getElementById(msgId).scrollIntoView({behavior: 'smooth', block: 'center'}); };
      let shortText = msg.content || '...';
      if(shortText.length > 50) shortText = shortText.substring(0,50) + '...';
      dot.innerHTML = `<div class="absolute right-4 top-1/2 -translate-y-1/2 w-48 bg-white dark:bg-[#1e1f20] text-[11px] p-2 rounded shadow-lg opacity-0 group-hover:opacity-100 pointer-events-none transition truncate border border-[#e5e7eb] dark:border-[#3c4043] z-[100] text-[#1f1f1f] dark:text-[#e3e3e3] whitespace-normal line-clamp-3">${escapeHtml(shortText)}</div>`;
      minimap.appendChild(dot);
    }'''

# Replace only the first occurrence after renderMessage logic
content = re.sub(
    r'(\s+messages\.appendChild\(wrap\);\s+lucide\.createIcons\(\);)',
    lambda m: render_message_append_new,
    content,
    count=2 # replace for both user and AI branches
)


# 8. Add getOSName and inject OS into createNewChat
os_func = '''  function getOSName() {
    const ua = navigator.userAgent;
    if (/android/i.test(ua)) return 'Android';
    if (/iPad|iPhone|iPod/.test(ua)) return 'Apple';
    if (/Win/.test(ua)) return 'Windows';
    if (/Mac/.test(ua)) return 'MacOS';
    if (/Linux/.test(ua)) return 'Linux';
    return '?';
  }

  function createNewChat(start = true) {'''

content = content.replace('  function createNewChat(start = true) {', os_func)

create_new_chat_old = "chats.unshift({ id: currentChatId, title: 'Nuova chat', messages: [], createdAt: Date.now() });"
create_new_chat_new = "chats.unshift({ id: currentChatId, title: 'Nuova chat', messages: [], createdAt: Date.now(), os: getOSName() });\n    if (document.getElementById('chatMinimap')) document.getElementById('chatMinimap').innerHTML = '';"
content = content.replace(create_new_chat_old, create_new_chat_new)

# Clear minimap in loadChat
load_chat_old = "messages.innerHTML = '';\n    chat.messages.forEach(msg => {"
load_chat_new = "messages.innerHTML = '';\n    if (document.getElementById('chatMinimap')) document.getElementById('chatMinimap').innerHTML = '';\n    chat.messages.forEach(msg => {"
content = content.replace(load_chat_old, load_chat_new)


# 9. Update renderChatList to handle search, grouping, OS icon, mini description
render_chat_list_old = r'''  function renderChatList\(\) \{
    chatList.innerHTML = chats\.map\(c => `
      <div class="relative group">
        <button data-id="\$\{c\.id\}" class="w-full text-left px-3 py-2 rounded-\[16px\] hover:bg-\[\#e4e8ee\] dark:hover:bg-\[\#2a2b2f\] flex items-center gap-2\.5 transition \$\{c\.id===currentChatId && !isGhost\?'bg-\\[#d3e3fd\\] dark:bg-\\[#2e3c51\\]':''\}">
          <i data-lucide="message-square" class="w-4 h-4 shrink-0 opacity-60"></i>
          <span class="sidebar-text truncate text-\[13px\] flex-1">\$\{c\.title\}</span>
        </button>
        <button data-menu="\$\{c\.id\}" class="absolute right-1\.5 top-1/2 -translate-y-1/2 p-1\.5 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-black/10 dark:hover:bg-white/10 sidebar-text transition">
          <i data-lucide="more-horizontal" class="w-3\.5 h-3\.5"></i>
        </button>
        <div id="menu-\$\{c\.id\}" class="hidden absolute right-2 top-8 z-50 bg-white dark:bg-\[\#2a2b2f\] rounded-xl shadow-xl border border-\[\#e5e7eb\] dark:border-\[\#3c4043\] w-40 overflow-hidden">
          <button data-action="rename" data-id="\$\{c\.id\}" class="w-full text-left px-3 py-2\.5 text-\[13px\] hover:bg-\[\#f0f4f9\] dark:hover:bg-\[\#1e1f20\] flex items-center gap-2\.5">
            <i data-lucide="pencil" class="w-4 h-4"></i>Rinomina
          </button>
          <button data-action="delete" data-id="\$\{c\.id\}" class="w-full text-left px-3 py-2\.5 text-\[13px\] hover:bg-\[\#f0f4f9\] dark:hover:bg-\[\#1e1f20\] flex items-center gap-2\.5 text-\[\#d93025\]">
            <i data-lucide="trash-2" class="w-4 h-4"></i>Elimina
          </button>
        </div>
      </div>
    `\)\.join\(''\);'''

render_chat_list_new = '''  function renderChatList() {
    const searchTerm = document.getElementById('searchChat')?.value.toLowerCase() || '';
    const filteredChats = chats.filter(c => c.title.toLowerCase().includes(searchTerm) || (c.messages.some(m => m.content.toLowerCase().includes(searchTerm))));
    
    const groups = { 'Oggi': [], 'Ieri': [], '7 Giorni fa': [], 'Più vecchie': [] };
    const now = Date.now();
    const day = 24 * 60 * 60 * 1000;
    
    filteredChats.forEach(c => {
      const diff = now - c.createdAt;
      if (diff < day) groups['Oggi'].push(c);
      else if (diff < 2*day) groups['Ieri'].push(c);
      else if (diff < 7*day) groups['7 Giorni fa'].push(c);
      else groups['Più vecchie'].push(c);
    });

    let html = '';
    for (const [g, list] of Object.entries(groups)) {
      if (list.length === 0) continue;
      html += `<div class="px-3 py-2 text-[10px] font-bold text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mt-2">${g}</div>`;
      html += list.map(c => {
        const lastMsgObj = c.messages.slice().reverse().find(m => m.role === 'user');
        const lastMsg = lastMsgObj?.content || 'Nuova chat...';
        const shortMsg = lastMsg.length > 25 ? lastMsg.substring(0, 25) + '...' : lastMsg;
        let osIcon = 'help-circle';
        if(c.os === 'Windows' || c.os === 'MacOS' || c.os === 'Linux') osIcon = 'monitor';
        else if(c.os === 'Android' || c.os === 'Apple') osIcon = 'smartphone';
        
        return `
        <div class="relative group">
          <button data-id="${c.id}" class="w-full text-left px-3 py-2 rounded-[16px] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] flex flex-col gap-0.5 transition ${c.id===currentChatId && !isGhost?'bg-[#d3e3fd] dark:bg-[#2e3c51]':''}">
            <div class="flex items-center gap-2 w-full">
              <i data-lucide="${osIcon}" class="w-3.5 h-3.5 shrink-0 opacity-60"></i>
              <span class="sidebar-text truncate text-[13px] flex-1 font-medium">${escapeHtml(c.title)}</span>
            </div>
            <span class="sidebar-text truncate text-[11px] text-[#5f6368] dark:text-[#9aa0a6] pl-[22px] w-full">${escapeHtml(shortMsg)}</span>
          </button>
          <button data-menu="${c.id}" class="absolute right-1.5 top-1/2 -translate-y-1/2 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-black/10 dark:hover:bg-white/10 sidebar-text transition">
            <i data-lucide="more-horizontal" class="w-3.5 h-3.5"></i>
          </button>
          <div id="menu-${c.id}" class="hidden absolute right-2 top-8 z-50 bg-white dark:bg-[#2a2b2f] rounded-xl shadow-xl border border-[#e5e7eb] dark:border-[#3c4043] w-40 overflow-hidden">
            <button data-action="rename" data-id="${c.id}" class="w-full text-left px-3 py-2.5 text-[13px] hover:bg-[#f0f4f9] dark:hover:bg-[#1e1f20] flex items-center gap-2.5">
              <i data-lucide="pencil" class="w-4 h-4"></i>Rinomina
            </button>
            <button data-action="delete" data-id="${c.id}" class="w-full text-left px-3 py-2.5 text-[13px] hover:bg-[#f0f4f9] dark:hover:bg-[#1e1f20] flex items-center gap-2.5 text-[#d93025]">
              <i data-lucide="trash-2" class="w-4 h-4"></i>Elimina
            </button>
          </div>
        </div>
      `}).join('');
    }
    chatList.innerHTML = html || `<p class="px-3 py-2 text-[12px] text-[#5f6368] sidebar-text text-center mt-2">Nessuna chat trovata</p>`;'''

content = re.sub(render_chat_list_old, render_chat_list_new, content)

# Event listener for searchChat
init_listener = "      const ls = document.getElementById('lenSlider'); if(ls){ ls.value=lengthLevel; ls.oninput=e=>{ lengthLevel=parseInt(e.target.value); document.getElementById('lenVal').textContent=['breve','medio','lungo'][lengthLevel-1]; localStorage.setItem('t-ai-len',lengthLevel); }; }"
init_listener_new = init_listener + "\n      document.getElementById('searchChat')?.addEventListener('input', () => { renderChatList(); lucide.createIcons(); });"
content = content.replace(init_listener, init_listener_new)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

