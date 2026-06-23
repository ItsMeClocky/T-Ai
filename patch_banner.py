#!/usr/bin/env python3
import re

FILE = "/home/clocky/T-Ai/index.html"
with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Insert the banner HTML right after <div id="app" class="flex h-full">
banner_html = """  <div id="app" class="flex h-full relative">
    <!-- Open Source Banner -->
    <div id="openSourceBanner" class="hidden absolute top-0 left-0 w-full bg-[#1a73e8] text-white text-[13px] text-center py-2 z-[99] shadow-md flex items-center justify-center gap-2">
      <i data-lucide="github" class="w-4 h-4"></i>
      <span data-i18n="os_banner">T-Ai è ora open source! Trova il codice su</span>
      <a href="https://github.com/ItsMeClocky/T-Ai/" target="_blank" class="underline font-bold hover:text-blue-200">GitHub</a>.
      <button onclick="this.parentElement.remove()" class="absolute right-3 top-1/2 -translate-y-1/2 p-1 hover:bg-black/20 rounded-full transition">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>
"""
if 'openSourceBanner' not in html:
    html = html.replace('<div id="app" class="flex h-full">', banner_html)

# Show banner when loader is removed
if 'loader.remove()' in html and 'openSourceBanner' not in html.split('loader.remove()')[1][:50]:
    html = html.replace(
        "loader.remove()",
        "loader.remove(); const osb = document.getElementById('openSourceBanner'); if(osb) { osb.classList.remove('hidden'); if(window.lucide) lucide.createIcons(); }"
    )

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Banner aggiunto con successo.")
