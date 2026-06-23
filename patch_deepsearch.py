import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add T-Deepsearch chip button after Chat Work chip
chatwork_chip = '''            <button data-chip="Chat-Work" id="chatWorkChip" onclick="openChatWorkModal()" class="chip shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] border border-transparent transition">
              <i data-lucide="users" class="w-3.5 h-3.5"></i> Chat Work
            </button>'''

deepsearch_chip = chatwork_chip + '''
            <button data-chip="T-Deepsearch" id="deepsearchChip" onclick="toggleDeepSearch()" class="chip shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] border border-transparent transition">
              <i data-lucide="search" class="w-3.5 h-3.5"></i> T-Deepsearch
            </button>'''

if 'T-Deepsearch' not in content:
    content = content.replace(chatwork_chip, deepsearch_chip, 1)

# 2. Add CSS for deep search mode
deepsearch_css = '''
   /* T-Deepsearch Mode */
   .deepsearch-active { border-color: #f59e0b !important; box-shadow: 0 0 0 2px rgba(245,158,11,0.15), 0 2px 12px rgba(245,158,11,0.1) !important; }
   .deepsearch-badge { background: linear-gradient(135deg, #f59e0b, #ef4444); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; }
   .deepsearch-pulse { animation: dsPulse 2s ease-in-out infinite; }
   @keyframes dsPulse { 0%,100% { box-shadow: 0 0 0 0 rgba(245,158,11,0.3); } 50% { box-shadow: 0 0 0 6px rgba(245,158,11,0); } }
   .source-card { transition: transform 0.2s, box-shadow 0.2s; }
   .source-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
'''
if 'deepsearch-active' not in content:
    content = content.replace('</style>', deepsearch_css + '</style>', 1)

# 3. Add T-Deepsearch JS logic before the last </script>
deepsearch_js = r'''
  // ===== T-DEEPSEARCH =====
  window._deepsearchActive = false;
  const GOOGLE_SEARCH_KEY = 'AIzaSyB5ufUWX2HWX7H2vm3cAXNkMJzUEj8YBR8';

  window.toggleDeepSearch = function() {
    window._deepsearchActive = !window._deepsearchActive;
    const chip = document.getElementById('deepsearchChip');
    const inputBox = document.querySelector('#promptInput')?.closest('.relative');
    
    if (window._deepsearchActive) {
      chip.classList.add('!bg-gradient-to-r', '!from-amber-500/20', '!to-red-500/20', '!border-amber-500/40', 'text-amber-600', 'dark:text-amber-400');
      chip.innerHTML = '<i data-lucide="search" class="w-3.5 h-3.5"></i> T-Deepsearch <span class="ml-1 text-[10px] font-bold bg-amber-500 text-white px-1.5 py-0.5 rounded-full">ON</span>';
      if (inputBox) {
        inputBox.classList.add('deepsearch-active', 'deepsearch-pulse');
      }
      document.getElementById('promptInput').placeholder = 'Cerca nel web con T-Deepsearch...';
      // Add banner
      let banner = document.getElementById('deepsearchBanner');
      if (!banner) {
        banner = document.createElement('div');
        banner.id = 'deepsearchBanner';
        banner.className = 'flex items-center gap-2 px-4 py-2 mb-2 rounded-xl bg-gradient-to-r from-amber-500/10 to-red-500/10 border border-amber-500/20 fade-in';
        banner.innerHTML = '<i data-lucide="zap" class="w-4 h-4 text-amber-500"></i><span class="text-[12px] font-medium text-amber-600 dark:text-amber-400">Modalit\u00e0 T-Deepsearch attiva \u2014 Le risposte includeranno risultati da Google Search</span><button onclick="toggleDeepSearch()" class="ml-auto text-[11px] text-gray-400 hover:text-red-500 underline">Disattiva</button>';
        const inputArea = document.querySelector('#promptInput')?.closest('div[style]');
        if (inputArea) inputArea.prepend(banner);
      }
      if(window.lucide) lucide.createIcons();
    } else {
      chip.classList.remove('!bg-gradient-to-r', '!from-amber-500/20', '!to-red-500/20', '!border-amber-500/40', 'text-amber-600', 'dark:text-amber-400');
      chip.innerHTML = '<i data-lucide="search" class="w-3.5 h-3.5"></i> T-Deepsearch';
      if (inputBox) {
        inputBox.classList.remove('deepsearch-active', 'deepsearch-pulse');
      }
      document.getElementById('promptInput').placeholder = 'Chiedi a T-Ai';
      const banner = document.getElementById('deepsearchBanner');
      if (banner) banner.remove();
      if(window.lucide) lucide.createIcons();
    }
  };

  // Google Search via SerpAPI-style proxy or direct scraping
  async function googleSearch(query) {
    try {
      // Use Google Custom Search JSON API
      const url = `https://www.googleapis.com/customsearch/v1?key=${GOOGLE_SEARCH_KEY}&cx=a0e7b8f1e0c1c4a58&q=${encodeURIComponent(query)}&num=8&lr=lang_it&gl=it`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        if (data.items && data.items.length > 0) {
          return data.items.map(item => ({
            title: item.title,
            link: item.link,
            snippet: item.snippet || '',
            displayLink: item.displayLink || ''
          }));
        }
      }
    } catch(e) {
      console.warn('[T-Deepsearch] Google Custom Search failed:', e);
    }
    
    // Fallback: use DuckDuckGo instant answers
    try {
      const ddgUrl = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_redirect=1&no_html=1`;
      const res = await fetch(ddgUrl);
      const data = await res.json();
      const results = [];
      if (data.AbstractText) results.push({ title: data.Heading || query, link: data.AbstractURL || '', snippet: data.AbstractText, displayLink: 'Wikipedia' });
      if (data.RelatedTopics) {
        data.RelatedTopics.slice(0, 6).forEach(t => {
          if (t.Text && t.FirstURL) results.push({ title: t.Text.substring(0, 60), link: t.FirstURL, snippet: t.Text, displayLink: new URL(t.FirstURL).hostname });
        });
      }
      if (results.length > 0) return results;
    } catch(e) {
      console.warn('[T-Deepsearch] DuckDuckGo fallback failed:', e);
    }

    // Final fallback: use Pollinations to simulate search
    return null;
  }

  // Render search results as cards
  function renderSearchResults(results) {
    if (!results || results.length === 0) return '';
    let html = '<div class="mt-3 mb-4"><p class="text-[11px] font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wider mb-2 flex items-center gap-1.5"><i data-lucide="globe" class="w-3 h-3"></i> Fonti trovate</p><div class="grid gap-2">';
    results.forEach((r, i) => {
      html += `<a href="${r.link}" target="_blank" rel="noopener" class="source-card flex items-start gap-3 p-3 rounded-xl bg-[#f8f9fa] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] hover:border-amber-400/50 transition no-underline text-inherit">
        <span class="w-5 h-5 rounded-full bg-amber-500/10 text-amber-600 flex items-center justify-center shrink-0 font-bold text-[10px] mt-0.5">${i+1}</span>
        <div class="min-w-0">
          <p class="text-[13px] font-medium truncate text-[#1a73e8] dark:text-[#8ab4f8]">${r.title}</p>
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-0.5 line-clamp-2">${r.snippet}</p>
          <p class="text-[10px] text-[#80868b] mt-1 flex items-center gap-1"><i data-lucide="external-link" class="w-2.5 h-2.5"></i>${r.displayLink}</p>
        </div>
      </a>`;
    });
    html += '</div></div>';
    return html;
  }

  // Patch processAI to intercept T-Deepsearch
  const _originalProcessAI = processAI;
  window.processAI = async function(userText, chip) {
    if (!window._deepsearchActive && chip !== 'T-Deepsearch') {
      return _originalProcessAI(userText, chip);
    }

    const lower = userText.toLowerCase();
    setAvatar('thinking');

    try {
      // Step 1: Search Google
      const searchResults = await googleSearch(userText);

      // Step 2: Build context from search results
      let searchContext = '';
      if (searchResults && searchResults.length > 0) {
        searchContext = searchResults.map((r, i) => `[${i+1}] ${r.title}\n${r.snippet}\nURL: ${r.link}`).join('\n\n');
      }

      // Step 3: Ask AI to synthesize
      const pollinationsText = async (prompt, system = '') => {
        const res = await fetch('https://text.pollinations.ai/openai', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model: 'openai',
            messages: [
              ...(system ? [{ role: 'system', content: system }] : []),
              { role: 'user', content: prompt }
            ],
            temperature: 0.4,
            stream: false
          })
        });
        const data = await res.json();
        return data.choices?.[0]?.message?.content || 'Nessun risultato';
      };

      const systemPrompt = `Sei T-Ai in modalit\u00e0 T-Deepsearch: un assistente di ricerca avanzato. Hai accesso ai risultati di ricerca Google qui sotto. Usa queste fonti per dare una risposta completa, accurata e ben strutturata in italiano. Cita le fonti usando i numeri [1], [2], ecc. Se i risultati non sono sufficienti, usa anche le tue conoscenze ma segnalalo. Rispondi in modo dettagliato e approfondito.`;

      let fullPrompt;
      if (searchContext) {
        fullPrompt = `Domanda dell'utente: "${userText}"\n\n--- RISULTATI DI RICERCA GOOGLE ---\n${searchContext}\n\n--- FINE RISULTATI ---\n\nRispondi in modo approfondito usando le fonti sopra.`;
      } else {
        fullPrompt = `Domanda dell'utente: "${userText}"\n\nNon ho trovato risultati di ricerca Google. Rispondi usando le tue conoscenze, ma segnala che non hai potuto verificare con fonti web.`;
      }

      const aiText = await pollinationsText(fullPrompt, systemPrompt);
      setAvatar('idle');

      // Build final response with sources
      const sourcesHtml = renderSearchResults(searchResults);
      const finalContent = aiText + (sourcesHtml ? '\n\n' + sourcesHtml : '');

      const response = { content: finalContent, type: 'text', meta: { deepsearch: true, sources: searchResults } };
      const msg = addMessage('ai', response.content, response.type, response.meta);
      msg.model = 'T-Deepsearch';
      renderMessage(msg, true);
      lastAiText = response.content;
    } catch(e) {
      console.error('[T-Deepsearch] Error:', e);
      setAvatar('idle');
      const response = { content: `**Errore T-Deepsearch:** ${e.message}\n\nRiprova o disattiva T-Deepsearch.` };
      const msg = addMessage('ai', response.content, 'text', {});
      renderMessage(msg, true);
    }
  };
'''

if 'T-DEEPSEARCH' not in content:
    last_script = content.rfind('</script>')
    content = content[:last_script] + deepsearch_js + '\n</script>' + content[last_script + len('</script>'):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("T-Deepsearch patch applied successfully!")
