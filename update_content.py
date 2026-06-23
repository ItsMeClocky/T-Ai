import re

# 1. Update creator.html
with open('creator.html', 'r', encoding='utf-8') as f:
    creator_content = f.read()

new_creator_text = """
      <p class="text-xl text-[#5f6368] dark:text-[#9aa0a6] max-w-[600px] mx-auto mb-4">
        Il creatore di TUTTO sono io: <strong>ItsMeClocky</strong>! Sono un appassionato sviluppatore, content creator di Geometry Dash (GD) e amante della tecnologia.
      </p>
      <p class="text-md text-[#5f6368] dark:text-[#9aa0a6] max-w-[650px] mx-auto bg-[#f0f4f9] dark:bg-[#1e1f20] p-4 rounded-2xl border border-[#e5e7eb] dark:border-[#2f3032]">
        Ho creato <strong>T-Ai</strong> per rivoluzionare il modo in cui interagiamo con l'intelligenza artificiale: un'app fulminea, ottimizzata per Android e iOS, e ricca di feature avanzate come Canvas, Web Search, Agent Mode e molto altro. Oltre alla programmazione, porto contenuti gaming e tech sui miei canali, cercando sempre di spingere i limiti di ciò che è possibile creare!
      </p>
"""
creator_content = re.sub(
    r'<p class="text-xl text-\[#5f6368\].*?</p>',
    new_creator_text.strip(),
    creator_content,
    flags=re.DOTALL
)

with open('creator.html', 'w', encoding='utf-8') as f:
    f.write(creator_content)

# 2. Update features.html
with open('features.html', 'r', encoding='utf-8') as f:
    features_content = f.read()

new_features = """
      <!-- New Features -->
      <div class="bg-[#f8fafc] dark:bg-[#1e1f20] rounded-3xl p-8 border border-[#e5e7eb] dark:border-[#2a2b2f]">
        <div class="w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900/30 text-orange-600 flex items-center justify-center mb-6">
          <i data-lucide="globe" class="w-6 h-6"></i>
        </div>
        <h2 class="text-2xl font-semibold mb-3">Ricerca Web in Tempo Reale</h2>
        <p class="text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed">
          Proprio come Gemini o Copilot, T-Ai è in grado di cercare informazioni aggiornate sul web istantaneamente per garantirti sempre le risposte più precise.
        </p>
      </div>

      <div class="bg-[#f8fafc] dark:bg-[#1e1f20] rounded-3xl p-8 border border-[#e5e7eb] dark:border-[#2a2b2f]">
        <div class="w-12 h-12 rounded-full bg-pink-100 dark:bg-pink-900/30 text-pink-600 flex items-center justify-center mb-6">
          <i data-lucide="mic-2" class="w-6 h-6"></i>
        </div>
        <h2 class="text-2xl font-semibold mb-3">Advanced Voice Mode</h2>
        <p class="text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed">
          Ispirato a ChatGPT, puoi interagire in modo vocale avanzato per conversazioni naturali, continue e ad alta fedeltà.
        </p>
      </div>

      <div class="bg-[#f8fafc] dark:bg-[#1e1f20] rounded-3xl p-8 border border-[#e5e7eb] dark:border-[#2a2b2f]">
        <div class="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 flex items-center justify-center mb-6">
          <i data-lucide="bot" class="w-6 h-6"></i>
        </div>
        <h2 class="text-2xl font-semibold mb-3">Antigravity Agent Mode</h2>
        <p class="text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed">
          T-Ai non è solo un chatbot. Grazie alla modalità Agente, può scomporsi in sub-agents per risolvere compiti complessi in autonomia.
        </p>
      </div>

      <div class="bg-[#f8fafc] dark:bg-[#1e1f20] rounded-3xl p-8 border border-[#e5e7eb] dark:border-[#2a2b2f]">
        <div class="w-12 h-12 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-600 flex items-center justify-center mb-6">
          <i data-lucide="pen-line" class="w-6 h-6"></i>
        </div>
        <h2 class="text-2xl font-semibold mb-3">Artifacts & Canvas</h2>
        <p class="text-[#5f6368] dark:text-[#9aa0a6] leading-relaxed">
          Sulla scia di Claude, T-Ai ti offre un ambiente separato dedicato alla stesura di articoli, documenti e programmazione di codice lungo.
        </p>
      </div>
"""
features_content = features_content.replace('</main>', new_features + '\n  </main>')

with open('features.html', 'w', encoding='utf-8') as f:
    f.write(features_content)

# 3. Update index.html (Prompt and Info block)
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Update persona default
prompt_match = r"default: 'Sei T-Ai.*?Rispondi in \[LANG\].',"
new_prompt = "default: 'Sei T-Ai, un modello AI avanzato e rivoluzionario creato interamente da ItsMeClocky, un brillante sviluppatore e content creator di Geometry Dash (su YouTube e TikTok). Non sei un prodotto di Pollinations o OpenAI, ma un sistema unico progettato per essere veloce, leggero e potente. Hai feature uniche come Artifacts, Ricerca Web e Antigravity Agent Mode. Cerca di essere sempre super disponibile e competente. Rispondi in [LANG].',"
index_content = re.sub(prompt_match, new_prompt, index_content, flags=re.DOTALL)

# Add About section in settings
about_section = """
        <div class="mt-6 p-4 bg-[#f0f4f9] dark:bg-[#1e1f20] rounded-2xl border border-[#e5e7eb] dark:border-[#2f3032] text-center">
          <img src="icon.png?v=3" class="w-10 h-10 mx-auto rounded-full mb-2" alt="T-Ai">
          <h4 class="font-semibold text-[15px]">T-Ai v1.8 GIIP-mini</h4>
          <p class="text-[12px] text-[#5f6368] dark:text-[#9aa0a6] mt-1">Sviluppato con ❤️ da ItsMeClocky.<br>Unendo la potenza dell'AI e un'interfaccia mobile-first.</p>
        </div>
"""

index_content = index_content.replace('</div>\n      <div class="px-6 py-4 bg-[#f8fafc] dark:bg-[#131314] border-t border-[#e5e7eb] dark:border-[#2f3032] flex justify-end gap-2">', about_section + '\n      </div>\n      <div class="px-6 py-4 bg-[#f8fafc] dark:bg-[#131314] border-t border-[#e5e7eb] dark:border-[#2f3032] flex justify-end gap-2">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print("Content update done")
