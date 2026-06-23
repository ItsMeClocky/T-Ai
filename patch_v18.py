import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add model option
content = content.replace(
    '<select id="defaultModel" class="w-full px-4 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] outline-none text-[14px]">\n            <option>T-Ai 1.7</option>',
    '<select id="defaultModel" class="w-full px-4 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] outline-none text-[14px]">\n            <option>T-Ai 1.8 GIIP-mini</option>\n            <option>T-Ai 1.7</option>'
)

# 2. Add modelMenu button
menu_btn = '''              <div id="modelMenu" class="hidden absolute top-full mt-2 left-0 bg-white dark:bg-[#2a2b2f] rounded-2xl shadow-xl border border-[#e5e7eb] dark:border-[#3c4043] w-64 overflow-hidden p-1.5 z-50 max-h-[320px] overflow-y-auto">
                <button data-model="T-Ai 1.8 GIIP-mini" class="model-option w-full text-left px-3 py-2 rounded-xl hover:bg-[#f0f4f9] dark:hover:bg-[#1e1f20] flex items-center gap-2">
                  <i data-lucide="sparkles" class="w-3.5 h-3.5 text-[#ec4899]"></i>
                  <span class="text-[14px] font-medium">T-Ai 1.8 GIIP-mini</span>
                  <span class="ml-auto text-[10px] px-1.5 py-0.5 rounded-full bg-[#ec4899]/15 text-[#ec4899] font-medium">New</span>
                </button>'''
content = content.replace(
    '<div id="modelMenu" class="hidden absolute top-full mt-2 left-0 bg-white dark:bg-[#2a2b2f] rounded-2xl shadow-xl border border-[#e5e7eb] dark:border-[#3c4043] w-64 overflow-hidden p-1.5 z-50 max-h-[320px] overflow-y-auto">',
    menu_btn
)

# 3. Add toolbar
toolbar = '''          <div class="flex items-center gap-2 mb-2 px-2 overflow-x-auto scrollbar-none w-full max-w-[840px] mx-auto">
            <button id="agentModeBtn" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] transition border border-[#e5e7eb] dark:border-[#3c4043] shrink-0" onclick="this.classList.toggle('text-[#1a73e8]'); this.classList.toggle('bg-[#e8f0fe]'); this.classList.toggle('dark:bg-[#1a73e8]/20'); this.classList.toggle('border-[#1a73e8]/30');">
              <i data-lucide="bot" class="w-3.5 h-3.5"></i> Antigravity Agents
            </button>
            <button id="webSearchBtn" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] transition border border-[#e5e7eb] dark:border-[#3c4043] shrink-0" onclick="this.classList.toggle('text-[#f59e0b]'); this.classList.toggle('bg-orange-50'); this.classList.toggle('dark:bg-orange-900/20'); this.classList.toggle('border-orange-500/30');">
              <i data-lucide="globe" class="w-3.5 h-3.5"></i> Cerca nel Web
            </button>
            <button id="advancedVoiceBtn" class="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] transition border border-[#e5e7eb] dark:border-[#3c4043] shrink-0 ml-auto" onclick="this.classList.toggle('text-[#ec4899]'); this.classList.toggle('bg-pink-50'); this.classList.toggle('dark:bg-pink-900/20'); this.classList.toggle('border-pink-500/30');">
              <i data-lucide="mic-2" class="w-3.5 h-3.5"></i> Advanced Voice
            </button>
          </div>
          <div class="relative bg-[#f0f4f9] dark:bg-[#1e1f20] rounded-[28px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] dark:shadow-none border border-[#e5e7eb] dark:border-[#2f3032] focus-within:shadow-[0_2px_8px_rgba(0,0,0,0.1)] transition-shadow">'''
content = content.replace(
    '<div class="relative bg-[#f0f4f9] dark:bg-[#1e1f20] rounded-[28px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] dark:shadow-none border border-[#e5e7eb] dark:border-[#2f3032] focus-within:shadow-[0_2px_8px_rgba(0,0,0,0.1)] transition-shadow">',
    toolbar
)

# 4. Rename Canvas to Artifacts / Canvas
content = content.replace('<h2 class="font-medium text-[15px] leading-tight">Canvas</h2>', '<h2 class="font-medium text-[15px] leading-tight">Artifacts / Canvas</h2>')
content = content.replace('> Canvas\n', '> Artifacts / Canvas\n')
content = content.replace('Canvas è perfetto', 'Artifacts / Canvas è perfetto')
content = content.replace('Ho aperto **Canvas** a destra.', 'Ho aperto **Artifacts / Canvas** a destra.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
