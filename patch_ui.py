#!/usr/bin/env python3
import re

FILE = "/home/clocky/T-Ai/index.html"
with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove .md and PDF export buttons
html = re.sub(
    r'<div class="flex gap-2">\s*<button id="exportMdBtn".*?</button>\s*<button id="exportPdfBtn".*?</button>\s*</div>',
    '',
    html,
    flags=re.DOTALL
)

# 2. Remove Installa T-Ai button
html = re.sub(
    r'<!-- Bottone Installa T-Ai -->\s*<button onclick="openInstallModal\(\)".*?</button>',
    '',
    html,
    flags=re.DOTALL
)

# 3. Replace Language settings
lang_pattern = r'<div>\s*<label[^>]*>Lingua interfaccia.*?</button>\s*<p[^>]*>Le risposte saranno generate in questa lingua.</p>\s*</div>'
new_lang_and_data = """        <div>
          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1.5">Lingua</label>
          <input type="hidden" id="appLanguage" value="it-IT">
          <button type="button" onclick="openBottomSheet('appLanguage', 'appLanguageLabel', 'Lingua', optionsLangUi, document.getElementById('appLanguage').value)" class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] text-[14px]">
            <span id="appLanguageLabel">Italiano</span>
            <i data-lucide="chevron-down" class="w-4 h-4 opacity-60"></i>
          </button>
        </div>

        <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
          <div class="flex items-center justify-between mb-2">
            <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6]">Salvataggio Dati</label>
            <div class="flex items-center bg-[#dde3ea] dark:bg-[#2c2f33] rounded-full p-1 cursor-pointer" onclick="toggleDataSaveMode()">
              <div id="btnCloud" class="px-3 py-1 rounded-full text-[12px] font-medium bg-white dark:bg-[#1e1f20] shadow-sm text-black dark:text-white transition">Cloud</div>
              <div id="btnLocale" class="px-3 py-1 rounded-full text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] transition">Locale</div>
            </div>
          </div>
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mb-3">Scegli se sincronizzare i dati con T-Cloud o salvarli solo sul dispositivo.</p>
          
          <div id="localDataOptions" class="hidden grid grid-cols-2 gap-2">
            <button onclick="exportData()" class="flex items-center justify-center gap-1.5 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[12px] font-medium transition border border-[#e5e7eb] dark:border-[#2f3032]">
              <i data-lucide="download" class="w-4 h-4"></i> Scarica .JSON
            </button>
            <button onclick="importData()" class="flex items-center justify-center gap-1.5 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#131314] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[12px] font-medium transition border border-[#e5e7eb] dark:border-[#2f3032]">
              <i data-lucide="upload" class="w-4 h-4"></i> Importa .JSON
            </button>
          </div>
        </div>
"""
html = re.sub(r'<div>\s*<label[^>]*>Lingua interfaccia.*?</button>\s*</div>\s*<div>\s*<label[^>]*>Lingua del modello.*?</button>\s*<p[^>]*>Le risposte saranno generate in questa lingua.</p>\s*</div>', new_lang_and_data, html, flags=re.DOTALL)

# Add js logic for toggle
js_logic = """
  window.dataSaveMode = 'cloud';
  window.toggleDataSaveMode = function() {
    window.dataSaveMode = window.dataSaveMode === 'cloud' ? 'locale' : 'cloud';
    const btnCloud = document.getElementById('btnCloud');
    const btnLocale = document.getElementById('btnLocale');
    const localOptions = document.getElementById('localDataOptions');
    
    if (window.dataSaveMode === 'cloud') {
      btnCloud.className = 'px-3 py-1 rounded-full text-[12px] font-medium bg-white dark:bg-[#1e1f20] shadow-sm text-black dark:text-white transition';
      btnLocale.className = 'px-3 py-1 rounded-full text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] transition';
      localOptions.classList.add('hidden');
      localStorage.setItem('tai_data_save_mode', 'cloud');
    } else {
      btnLocale.className = 'px-3 py-1 rounded-full text-[12px] font-medium bg-white dark:bg-[#1e1f20] shadow-sm text-black dark:text-white transition';
      btnCloud.className = 'px-3 py-1 rounded-full text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] transition';
      localOptions.classList.remove('hidden');
      localStorage.setItem('tai_data_save_mode', 'locale');
    }
  };

  function initDataSaveMode() {
    const saved = localStorage.getItem('tai_data_save_mode');
    if (saved === 'locale') {
      window.dataSaveMode = 'cloud';
      toggleDataSaveMode();
    }
  }
  setTimeout(initDataSaveMode, 100);
"""

if 'window.dataSaveMode' not in html:
    html = html.replace('// --- SETTINGS MODAL ---', '// --- SETTINGS MODAL ---\n' + js_logic)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)
print("UI patch applied")
