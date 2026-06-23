import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_js = """  // Loading Screen Logic
  window.addEventListener('load', () => {
    let timeLeft = 8;
    const timeEl = document.getElementById('loadingTime');
    const loader = document.getElementById('loadingScreen');
    
    const interval = setInterval(() => {
      timeLeft--;
      if (timeEl) timeEl.innerText = `Tempo stimato: ${timeLeft}s`;
      
      if (timeLeft <= 0) {
        clearInterval(interval);
        if (loader) {
          loader.classList.add('opacity-0');
          setTimeout(() => loader.remove(), 1000);
        }
      }
    }, 1000);
  });"""

new_js = """  // Loading Screen Logic
  window.addEventListener('load', () => {
    let timeLeft = 5;
    let isDelayed = Math.random() > 0.4; // 60% probabilità di ritardo
    let extraTime = isDelayed ? Math.floor(Math.random() * 4) + 3 : 0; // 3-6 secondi extra
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
  });"""

content = content.replace(old_js, new_js)

# Also update the default text in HTML to say 5s
content = content.replace('Tempo stimato: 8s</span>', 'Tempo stimato: 5s</span>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated Loader Logic")
