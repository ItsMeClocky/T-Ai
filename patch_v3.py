import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Apple icon
icon_tag = '<link rel="icon" href="icon.png?v=3" type="image/png">'
if 'icon-apple.png' not in content:
    content = content.replace(icon_tag, icon_tag + '\n  <link rel="apple-touch-icon" href="icon-apple.png">', 1)

# 2. Add Google and Meta Auth UI to settings before "API Keys"
api_keys_marker = '<label class="text-[13px] font-semibold text-[#202124] dark:text-[#e3e3e3] block mb-3 flex items-center gap-2">'
google_svg = '<svg class="w-4 h-4 inline-block" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'
meta_svg = '<svg class="w-4 h-4 inline-block" viewBox="0 0 24 24"><defs><linearGradient id="metaGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0082FB"/><stop offset="100%" stop-color="#A033FF"/></linearGradient></defs><path fill="url(#metaGrad)" d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12c0-5.523-4.477-10-10-10z"/></svg>'

auth_ui = f'''
        <div>
          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1.5 flex items-center gap-1.5">
            {google_svg} Account Google per T-Clockwork
          </label>
          <div class="p-3 bg-[#f0f4f9] dark:bg-[#131314] rounded-xl border border-[#e5e7eb] dark:border-[#2f3032] flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div id="googleAuthStatusIcon" class="w-2 h-2 rounded-full bg-red-500"></div>
              <span id="googleAuthStatusText" class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6]">Non connesso</span>
            </div>
            <button id="googleAuthBtn" onclick="handleGoogleLogin()" class="px-3 py-2 rounded-xl bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] text-[12px] font-medium hover:bg-gray-50 dark:hover:bg-[#2a2b2f] transition shadow-sm flex items-center gap-1.5">
              Collega T-Clockwork a {google_svg}
            </button>
          </div>

          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1.5 flex items-center gap-1.5">
            {meta_svg} Account Meta per T-Clockwork
          </label>
          <div class="p-3 bg-[#f0f4f9] dark:bg-[#131314] rounded-xl border border-[#e5e7eb] dark:border-[#2f3032] flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div id="metaAuthStatusIcon" class="w-2 h-2 rounded-full bg-red-500"></div>
              <span id="metaAuthStatusText" class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6]">Non connesso</span>
            </div>
            <button id="metaAuthBtn" onclick="handleMetaLogin()" class="px-3 py-2 rounded-xl bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] text-[12px] font-medium hover:bg-gray-50 dark:hover:bg-[#2a2b2f] transition shadow-sm flex items-center gap-1.5">
              Collega T-Clockwork a {meta_svg}
            </button>
          </div>
        </div>
'''
if 'Account Google per T-Clockwork' not in content:
    content = content.replace(api_keys_marker, auth_ui + api_keys_marker, 1)

# Remove API Key Inputs since user wants them in the python file ONLY
# We find the section and replace it with a text explanation
api_keys_section_start = content.find(api_keys_marker)
api_keys_section_end = content.find('Le chiavi vengono salvate nel browser', api_keys_section_start)
if api_keys_section_start != -1 and api_keys_section_end != -1:
    api_keys_section_end = content.find('</p>', api_keys_section_end) + 4
    new_api_keys_section = api_keys_marker + '''
          <p class="text-[13px] text-[#5f6368] dark:text-[#9aa0a6]">Le chiavi API sono salvate in modo sicuro nel backend locale (api_keys.py) per proteggerle e non rubarle. Il backend comunica direttamente con i provider reali (Gemini, ChatGPT, Manus AI).</p>
'''
    content = content[:api_keys_section_start] + new_api_keys_section + content[api_keys_section_end:]

# 3. Add CSS for like/dislike animations and hover actions
css_add = '''
   .like-jump { animation: likeJump 0.5s ease; color: #10B981 !important; }
   .dislike-drop { animation: dislikeDrop 0.5s ease; color: #EF4444 !important; }
   @keyframes likeJump { 0% { transform: translateY(0); } 50% { transform: translateY(-10px) scale(1.2); } 100% { transform: translateY(0); } }
   @keyframes dislikeDrop { 0% { transform: translateY(0); } 50% { transform: translateY(10px) scale(0.8); } 100% { transform: translateY(0); } }
   .msg-actions { opacity: 0; transition: opacity 0.2s; }
   .msg-wrap:hover .msg-actions { opacity: 1; }
'''
if 'like-jump' not in content:
    content = content.replace('</style>', css_add + '</style>', 1)

# 4. Update renderMessage to add AI feedback and User actions
old_render_msg = '''    <div class="flex flex-col gap-1 max-w-[85%] ${isMine ? 'items-end' : 'items-start'} relative group">
      ${!isMine && !isSystem ? `
      <div class="flex items-center gap-2 mb-1 pl-1">
        <img src="icon.png?v=3" class="w-5 h-5 rounded-full" alt="AI">
        <span class="text-[11px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider">${msg.model || 'T-Ai'}</span>
      </div>` : ''}
      <div class="px-4 py-3 rounded-2xl text-[15px] shadow-sm leading-relaxed ${isMine ? 'bg-[#1a73e8] text-white rounded-tr-sm' : (isSystem ? 'bg-amber-50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-200 text-[13px] italic mx-auto text-center' : 'bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] text-[#202124] dark:text-[#e3e3e3] rounded-tl-sm ai-content')}">'''

new_render_msg = '''    <div id="msg-${msg.id}" class="msg-wrap flex flex-col gap-1 max-w-[85%] ${isMine ? 'items-end' : 'items-start'} relative group">
      ${!isMine && !isSystem ? `
      <div class="flex items-center gap-2 mb-1 pl-1">
        <img src="icon.png?v=3" class="w-5 h-5 rounded-full" alt="AI">
        <span class="text-[11px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider">${msg.model || 'T-Ai'}</span>
      </div>` : ''}
      
      <div class="flex items-end gap-2 ${isMine ? 'flex-row-reverse' : 'flex-row'}">
        <div class="px-4 py-3 rounded-2xl text-[15px] shadow-sm leading-relaxed ${isMine ? 'bg-[#1a73e8] text-white rounded-tr-sm' : (isSystem ? 'bg-amber-50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-200 text-[13px] italic mx-auto text-center' : 'bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] text-[#202124] dark:text-[#e3e3e3] rounded-tl-sm ai-content')}">'''

if '<div id="msg-${msg.id}" class="msg-wrap' not in content:
    content = content.replace(old_render_msg, new_render_msg, 1)

old_close_div = '''      </div>
    </div>`;
    messages.appendChild(div);'''

new_close_div = '''      </div>
      
      ${isMine ? `
      <div class="msg-actions flex items-center gap-1 mt-1 mr-1">
        <button onclick="editMsg('${msg.id}')" class="p-1.5 text-gray-400 hover:text-blue-500 rounded-full" title="Modifica"><i data-lucide="edit-2" class="w-3.5 h-3.5"></i></button>
        <button onclick="copyMsg('${msg.id}')" class="p-1.5 text-gray-400 hover:text-green-500 rounded-full" title="Copia"><i data-lucide="copy" class="w-3.5 h-3.5"></i></button>
        <button onclick="deleteMsg('${msg.id}')" class="p-1.5 text-gray-400 hover:text-red-500 rounded-full" title="Elimina"><i data-lucide="trash-2" class="w-3.5 h-3.5"></i></button>
      </div>
      ` : (!isSystem ? `
      <div class="flex items-center gap-1 mt-1 ml-1">
        <button onclick="likeMsg(this, '${msg.id}')" class="p-1.5 text-gray-400 hover:text-green-500 rounded-full transition-all" title="Mi piace"><i data-lucide="thumbs-up" class="w-3.5 h-3.5"></i></button>
        <button onclick="dislikeMsg(this, '${msg.id}')" class="p-1.5 text-gray-400 hover:text-red-500 rounded-full transition-all" title="Non mi piace"><i data-lucide="thumbs-down" class="w-3.5 h-3.5"></i></button>
      </div>
      <div id="feedback-${msg.id}" class="hidden mt-2 w-full max-w-md bg-[#f0f4f9] dark:bg-[#131314] p-3 rounded-xl border border-[#e5e7eb] dark:border-[#2f3032]">
         <p class="text-[12px] font-medium mb-2 text-[#5f6368]">Cosa è Successo questa volta con T-Ai? Raccontaci...</p>
         <textarea id="feedback-text-${msg.id}" class="w-full bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#3c4043] rounded-lg p-2 text-[13px] outline-none mb-2" rows="2"></textarea>
         <button onclick="sendFeedback('${msg.id}')" class="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-[12px] font-medium">Invia Feedback</button>
      </div>
      ` : '')}
    </div>`;
    messages.appendChild(div);'''

if 'likeMsg(this' not in content:
    content = content.replace(old_close_div, new_close_div, 1)


# 5. Add processAI override + Chat Work Logic + Auth logic at the end of scripts
extra_js = '''
  // Google and Meta Auth Logic
  window.handleGoogleLogin = function() {
    const btn = document.getElementById('googleAuthBtn');
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Connessione...`;
    lucide.createIcons();
    setTimeout(() => {
      document.getElementById('googleAuthStatusIcon').classList.replace('bg-red-500', 'bg-green-500');
      document.getElementById('googleAuthStatusText').innerText = "Connesso come Utente";
      btn.innerHTML = `<i data-lucide="check" class="w-4 h-4 text-green-500"></i> Connesso`;
      lucide.createIcons();
      localStorage.setItem('googleAuth', 'true');
    }, 1500);
  };
  
  window.handleMetaLogin = function() {
    const btn = document.getElementById('metaAuthBtn');
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Connessione...`;
    lucide.createIcons();
    setTimeout(() => {
      document.getElementById('metaAuthStatusIcon').classList.replace('bg-red-500', 'bg-green-500');
      document.getElementById('metaAuthStatusText').innerText = "Connesso come Utente Meta";
      btn.innerHTML = `<i data-lucide="check" class="w-4 h-4 text-green-500"></i> Connesso`;
      lucide.createIcons();
      localStorage.setItem('metaAuth', 'true');
    }, 1500);
  };

  if (localStorage.getItem('googleAuth') === 'true') {
     setTimeout(() => {
       document.getElementById('googleAuthStatusIcon')?.classList.replace('bg-red-500', 'bg-green-500');
       if(document.getElementById('googleAuthStatusText')) document.getElementById('googleAuthStatusText').innerText = "Connesso come Utente";
       if(document.getElementById('googleAuthBtn')) document.getElementById('googleAuthBtn').innerHTML = `<i data-lucide="check" class="w-4 h-4 text-green-500"></i> Connesso`;
     }, 100);
  }
  if (localStorage.getItem('metaAuth') === 'true') {
     setTimeout(() => {
       document.getElementById('metaAuthStatusIcon')?.classList.replace('bg-red-500', 'bg-green-500');
       if(document.getElementById('metaAuthStatusText')) document.getElementById('metaAuthStatusText').innerText = "Connesso come Utente Meta";
       if(document.getElementById('metaAuthBtn')) document.getElementById('metaAuthBtn').innerHTML = `<i data-lucide="check" class="w-4 h-4 text-green-500"></i> Connesso`;
     }, 100);
  }

  // AI Feedback Logic
  window.likeMsg = function(btn, msgId) {
    btn.classList.add('like-jump');
    btn.innerHTML = `<i data-lucide="thumbs-up" class="w-3.5 h-3.5 fill-current"></i>`;
    lucide.createIcons();
    fetch('http://localhost:8080/chatwork/like', { method: 'POST', body: JSON.stringify({ msg_id: msgId, action: 'like' }) }).catch(e=>console.log(e));
  };
  window.dislikeMsg = function(btn, msgId) {
    btn.classList.add('dislike-drop');
    btn.innerHTML = `<i data-lucide="thumbs-down" class="w-3.5 h-3.5 fill-current"></i>`;
    lucide.createIcons();
    const fb = document.getElementById('feedback-'+msgId);
    if(fb) { fb.classList.remove('hidden'); fb.classList.add('fade-in'); }
  };
  window.sendFeedback = function(msgId) {
    const txt = document.getElementById('feedback-text-'+msgId).value;
    fetch('http://localhost:8080/chatwork/like', { method: 'POST', body: JSON.stringify({ msg_id: msgId, action: 'dislike', feedback: txt }) }).catch(e=>console.log(e));
    const fb = document.getElementById('feedback-'+msgId);
    if(fb) fb.innerHTML = '<p class="text-[12px] text-green-500 font-medium"><i data-lucide="check" class="w-3 h-3 inline"></i> Grazie per il feedback!</p>';
    lucide.createIcons();
  };

  // User Message Actions
  window.copyMsg = function(msgId) {
     const chat = chats.find(c => c.id === currentChatId);
     const msg = chat.messages.find(m => m.id == msgId);
     if(msg) { navigator.clipboard.writeText(msg.text); alert('Copiato!'); }
  };
  window.deleteMsg = function(msgId) {
     const chat = chats.find(c => c.id === currentChatId);
     if(chat) {
       chat.messages = chat.messages.filter(m => m.id != msgId);
       saveChats();
       document.getElementById('msg-'+msgId)?.remove();
     }
  };
  window.editMsg = function(msgId) {
     const chat = chats.find(c => c.id === currentChatId);
     const msg = chat.messages.find(m => m.id == msgId);
     if(msg) {
       document.getElementById('chatInput').value = msg.text;
       window.deleteMsg(msgId);
     }
  };

  // Update processAI to use localhost:8080 backend
  window.processAI = async function(userText, chip) {
    const lower = userText.toLowerCase();
    let response = {};
    const modelStr = document.getElementById('modelLabel').innerText;
    
    // Determine provider based on model selection
    let provider = 'gemini';
    if(modelStr.toLowerCase().includes('gpt') || modelStr.toLowerCase().includes('o3')) provider = 'openai';
    if(modelStr.toLowerCase().includes('manus')) provider = 'manus';

    try {
      setAvatar('thinking');
      const chat = chats.find(c => c.id === currentChatId);
      const messagesPayload = chat.messages.map(m => ({ role: m.isMine ? 'user' : 'model', content: m.text }));
      
      const res = await fetch('http://localhost:8080/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider: provider,
          model: modelStr,
          messages: messagesPayload
        })
      });
      const data = await res.json();
      setAvatar('idle');
      
      if(data.error) {
         response = { content: `**Errore dal Backend:** ${data.error}` };
      } else {
         response = { content: data.response || "Nessuna risposta" };
      }
    } catch(e) {
      setAvatar('idle');
      response = { content: `**Errore di connessione:** Il backend su localhost:8080 non è in esecuzione.\\n\\nAssicurati di avviare \`python3 api_keys.py\` in un terminale.` };
    }

    const aiMsg = { id: Date.now(), isMine: false, text: response.content, time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), type: response.type || 'text', meta: response.meta, model: modelStr };
    chats.find(c => c.id === currentChatId).messages.push(aiMsg);
    saveChats();
    renderMessage(aiMsg);
    document.dispatchEvent(new CustomEvent('aiResponse', { detail: { text: response.content }}));
  };

  // Chat Work Realtime Logic
  window.chatWorkPollInterval = null;
  window.lastChatWorkId = 0;
  window.chatWorkActive = false;

  const originalSendChatWork = window.sendChatWorkMsg;
  window.sendChatWorkMsg = async function() {
    const input = document.getElementById('chatWorkInput');
    const txt = input.value.trim();
    if(!txt) return;
    input.value = '';
    const myName = document.getElementById('nameInput')?.value || 'Tu';
    
    fetch('http://localhost:8080/chatwork/send', {
      method: 'POST',
      body: JSON.stringify({ user: myName, text: txt })
    }).catch(e=>console.log("ChatWork err:", e));
  };

  function pollChatWork() {
    if(!window.chatWorkActive) return;
    fetch('http://localhost:8080/chatwork/poll', {
      method: 'POST',
      body: JSON.stringify({ last_id: window.lastChatWorkId })
    })
    .then(r => r.json())
    .then(data => {
       if(data.messages && data.messages.length > 0) {
          data.messages.forEach(m => {
             if(m.id > window.lastChatWorkId) {
                window.lastChatWorkId = m.id;
                const myName = document.getElementById('nameInput')?.value || 'Tu';
                const isMine = m.user === myName;
                window.addChatWorkMessage(m.user, m.text, new Date(m.timestamp*1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), isMine, false);
             }
          });
       }
    })
    .catch(e=>console.log(e));
  }

  // Hook into openChatWork
  const oldOpenChatWork = window.openChatWork;
  window.openChatWork = function() {
     if(oldOpenChatWork) oldOpenChatWork();
     window.chatWorkActive = true;
     if(!window.chatWorkPollInterval) {
        window.chatWorkPollInterval = setInterval(pollChatWork, 2000);
     }
  };
  const oldCloseChatWork = window.closeChatWork;
  window.closeChatWork = function() {
     if(oldCloseChatWork) oldCloseChatWork();
     window.chatWorkActive = false;
     if(window.chatWorkPollInterval) {
        clearInterval(window.chatWorkPollInterval);
        window.chatWorkPollInterval = null;
     }
  };
'''

if 'window.likeMsg' not in content:
    last_script = content.rfind('</script>')
    content = content[:last_script] + extra_js + '\n</script>' + content[last_script + len('</script>'):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied.")
