import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the loading screen HTML to have the 5s timer
loader_old = """<span id="loadingTime" class="px-5 py-2.5 bg-black/60 backdrop-blur-md rounded-full text-white font-medium shadow-xl text-sm">Tempo stimato: 5s</span>"""
if loader_old not in content:
    # If it's still 8s
    content = content.replace("Tempo stimato: 8s", "Tempo stimato: 5s")

# 2. Add the JS logic right before the LAST </script>
js_to_inject = """
  // Loading Screen Logic
  let timeLeft = 5;
  let isDelayed = Math.random() > 0.4;
  let extraTime = isDelayed ? Math.floor(Math.random() * 4) + 3 : 0;
  let phase = 1;

  const timeEl = document.getElementById('loadingTime');
  const loader = document.getElementById('loadingScreen');
  
  if (timeEl) timeEl.innerText = `Tempo stimato: ${timeLeft}s`;
  
  const interval = setInterval(() => {
    timeLeft--;
    
    if (phase === 1) {
      if (timeLeft > 0) {
        if (timeEl) timeEl.innerText = `Tempo stimato: ${timeLeft}s`;
      } else {
        if (isDelayed) {
          phase = 2;
          timeLeft = extraTime;
          if (timeEl) timeEl.innerText = `Caricamento aggiuntivo di dati dal 'T15 Servers', tempo stimato di ${timeLeft}s`;
        } else {
          clearInterval(interval);
          if (loader) {
            loader.classList.add('opacity-0');
            setTimeout(() => loader.remove(), 1000);
          }
        }
      }
    } else if (phase === 2) {
      if (timeLeft > 0) {
        if (timeEl) timeEl.innerText = `Caricamento aggiuntivo di dati dal 'T15 Servers', tempo stimato di ${timeLeft}s`;
      } else {
        clearInterval(interval);
        if (loader) {
          loader.classList.add('opacity-0');
          setTimeout(() => loader.remove(), 1000);
        }
      }
    }
  }, 1000);

  // Bottom Sheet Logic
  const optionsModel = [
    { value: 'T-Ai 1.8 GIIP-mini', label: 'T-Ai 1.8 GIIP-mini', icon: 'sparkles', isNew: true },
    { value: 'T-Ai 1.7', label: 'T-Ai 1.7', icon: 'sparkles' },
    { value: 'T-Ai 1.6', label: 'T-Ai 1.6', icon: 'sparkles' },
    { value: 'GPT', label: 'GPT', icon: 'zap' },
    { value: 'Gemini', label: 'Gemini', icon: 'zap' },
    { value: 'Llama', label: 'Llama', icon: 'zap' },
    { value: 'Claude Haiku', label: 'Claude Haiku', icon: 'zap' },
    { value: 'Deepseek', label: 'Deepseek', icon: 'zap' },
    { value: 'Grok', label: 'Grok', icon: 'zap' },
    { value: 'Tako', label: 'Tako', icon: 'zap' },
    { value: 'NVIDIA', label: 'NVIDIA', icon: 'zap' },
    { value: 'Adobe', label: 'Adobe', icon: 'zap' },
    { value: 'Copilot', label: 'Copilot', icon: 'zap' }
  ];

  const optionsPersona = [
    { value: 'default', label: 'T-Ai Standard', icon: 'bot' },
    { value: 'dev', label: 'Sviluppatore Esperto', icon: 'code' },
    { value: 'creative', label: 'Scrittore Creativo', icon: 'pen-tool' },
    { value: 'friendly', label: 'Amico Informale', icon: 'smile' }
  ];

  window.openBottomSheet = function(inputId, labelId, title, options, currentValue) {
    const overlay = document.getElementById('bottomSheetOverlay');
    const sheet = document.getElementById('bottomSheet');
    const content = document.getElementById('bottomSheetContent');
    const titleEl = document.getElementById('bottomSheetTitle');
    
    titleEl.innerText = title;
    content.innerHTML = '';
    
    options.forEach(opt => {
      const isSelected = opt.value === currentValue;
      const btn = document.createElement('button');
      btn.className = `w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition-colors ${isSelected ? 'bg-[#1a73e8]/10 text-[#1a73e8]' : 'hover:bg-[#f0f4f9] dark:hover:bg-[#2a2b2f]'}`;
      
      let iconHtml = opt.icon ? `<i data-lucide="${opt.icon}" class="w-5 h-5 ${isSelected ? 'text-[#1a73e8]' : 'opacity-70'}"></i>` : '';
      let newBadge = opt.isNew ? `<span class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-[#1a73e8]/15 text-[#1a73e8] font-medium">New</span>` : '';
      
      btn.innerHTML = `${iconHtml} <span class="font-medium text-[15px] ${isSelected ? 'text-[#1a73e8]' : ''}">${opt.label}</span> ${newBadge}`;
      
      btn.onclick = () => {
        document.getElementById(inputId).value = opt.value;
        document.getElementById(labelId).innerText = opt.label;
        localStorage.setItem(`t-ai-${inputId === 'defaultModel' ? 'model' : 'persona'}`, opt.value);
        closeBottomSheet();
      };
      content.appendChild(btn);
    });
    
    if(window.lucide) lucide.createIcons();
    
    overlay.classList.remove('hidden');
    // flush
    void overlay.offsetWidth;
    overlay.classList.remove('opacity-0');
    sheet.classList.remove('translate-y-full');
    
    // push state per il tasto indietro
    history.pushState({ modal: 'bottomSheet' }, '', '');
  };

  window.closeBottomSheet = function() {
    const overlay = document.getElementById('bottomSheetOverlay');
    const sheet = document.getElementById('bottomSheet');
    if(!overlay || overlay.classList.contains('hidden')) return;
    
    overlay.classList.add('opacity-0');
    sheet.classList.add('translate-y-full');
    setTimeout(() => {
      overlay.classList.add('hidden');
    }, 300);
  };
"""

# inject right before the last </script>
parts = content.rsplit('</script>', 1)
content = parts[0] + js_to_inject + '\n</script>' + parts[1]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected JS successfully")
