import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific model options in the HTML
content = content.replace('T-Ai GPT', 'GPT')
content = content.replace('T-Ai Gemini', 'Gemini')
content = content.replace('T-Ai Llama', 'Llama')
content = content.replace('T-Ai Claude Haiku', 'Claude Haiku')
content = content.replace('T-Ai Deepseek', 'Deepseek')
content = content.replace('T-Ai Grok', 'Grok')
content = content.replace('T-Ai Tako', 'Tako')

# Make sure to keep T-Ai 1.8, 1.7 etc.
# Now let's add NVIDIA, Adobe, Copilot inside the HTML drop down right after Tako

tako_html_regex = r'(<button data-model="Tako".*?</button>)'
match = re.search(tako_html_regex, content, re.DOTALL)
if match:
    tako_block = match.group(1)
    new_models_html = """
                <button data-model="NVIDIA" class="model-option w-full text-left px-3 py-2 rounded-xl hover:bg-[#f0f4f9] dark:hover:bg-[#1e1f20] flex items-center gap-2">
                  <i data-lucide="zap" class="w-3.5 h-3.5 opacity-60"></i>
                  <span class="text-[14px]">NVIDIA</span>
                </button>
                <button data-model="Adobe" class="model-option w-full text-left px-3 py-2 rounded-xl hover:bg-[#f0f4f9] dark:hover:bg-[#1e1f20] flex items-center gap-2">
                  <i data-lucide="zap" class="w-3.5 h-3.5 opacity-60"></i>
                  <span class="text-[14px]">Adobe</span>
                </button>
                <button data-model="Copilot" class="model-option w-full text-left px-3 py-2 rounded-xl hover:bg-[#f0f4f9] dark:hover:bg-[#1e1f20] flex items-center gap-2">
                  <i data-lucide="zap" class="w-3.5 h-3.5 opacity-60"></i>
                  <span class="text-[14px]">Copilot</span>
                </button>
"""
    content = content.replace(tako_block, tako_block + new_models_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HTML models")
