import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS in <head>
css_patch = """
    body { font-family: 'Inter', sans-serif; overscroll-behavior-y: none; }
    button, a, i, select { user-select: none; -webkit-user-select: none; }
    ::-webkit-scrollbar { display: none; }
    * { scrollbar-width: none; }
"""
content = re.sub(r'body \{ font-family: \'Inter\', sans-serif; \}', css_patch, content)

# 2. Update Header Padding
# Find: <header class="sticky top-0 z-20 bg-white/90 dark:bg-[#131314]/90 backdrop-blur-xl border-b border-[#e5e7eb] dark:border-[#2a2b2f]">
# Replace with: <header style="padding-top: env(safe-area-inset-top);" class="...">
content = content.replace('<header class="sticky top-0 z-20', '<header style="padding-top: env(safe-area-inset-top);" class="sticky top-0 z-20')

# 3. Update Input Container Padding
# Find: <div class="px-4 py-2 border-t border-[#e5e7eb] dark:border-[#2f3032] flex items-center justify-between">
# Or: <div class="px-4 py-2 border-t border-[#e5e7eb] dark:border-[#2f3032] flex flex-col gap-2 w-full"> (Depends on recent patches)
content = content.replace('class="px-4 py-2 border-t border-[#e5e7eb] dark:border-[#2f3032]', 'style="padding-bottom: max(0.5rem, env(safe-area-inset-bottom));" class="px-4 pt-2 border-t border-[#e5e7eb] dark:border-[#2f3032]')

# 4. Remove .scrollbar-thin everywhere
content = content.replace('scrollbar-thin', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("CSS Update Done")
