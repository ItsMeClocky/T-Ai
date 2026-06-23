import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

render_old = """  function renderChatList() {
    chatList.innerHTML = chats.map(c => `
      <div class="relative group">
        <button data-id="${c.id}" class="w-full text-left px-3 py-2 rounded-[16px] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] flex items-center gap-2.5 transition ${c.id===currentChatId && !isGhost?'bg-[#d3e3fd] dark:bg-[#2e3c51]':''}">
          <i data-lucide="message-square" class="w-4 h-4 shrink-0 opacity-60"></i>
          <span class="sidebar-text truncate text-[13px] flex-1">${c.title}</span>
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
    `).join('') || `<p class="px-3 py-2 text-[12px] text-[#5f6368] sidebar-text">Nessuna chat</p>`;"""

render_new = """  function renderChatList() {
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
    chatList.innerHTML = html || `<p class="px-3 py-2 text-[12px] text-[#5f6368] sidebar-text text-center mt-2">Nessuna chat trovata</p>`;"""

if render_old in content:
    content = content.replace(render_old, render_new)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Failed to find substring")
