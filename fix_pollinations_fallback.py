#!/usr/bin/env python3
"""
Fix Pollinations queue full error by ensuring backend server is used first.
The backend server has 3 ChatGPT API keys as fallback.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the taiGenerateMessages function to prioritize backend
old_tai_generate = '''  async function taiGenerateMessages(messages, temp = null) {
    const backend = _resolveTaiBackend();
    try {
      const res = await fetch(`${backend}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages, temp })
      });
      if (res.ok) {
        const data = await res.json();
        if (data.notice) toast(data.notice);
        if (!res.ok) console.warn('[T-Ai] /generate HTTP', res.status, data);
      }
    } catch (e) {
      console.warn('[T-Ai] Backend GPT non disponibile, uso Pollinations:', e);
    }
    return _pollinationsFetch(_messagesForPollinations(messages), temp);
  }'''

new_tai_generate = '''  async function taiGenerateMessages(messages, temp = null) {
    const backend = _resolveTaiBackend();
    
    // Try backend server first (has 3 ChatGPT keys with rotation)
    if (backend) {
      try {
        const res = await fetch(`${backend}/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages, temp })
        });
        if (res.ok) {
          const data = await res.json();
          if (data.notice) toast(data.notice);
          if (data.response) return data.response;
          console.warn('[T-Ai] Backend returned no response');
        } else {
          console.warn('[T-Ai] Backend HTTP error:', res.status);
        }
      } catch (e) {
        console.warn('[T-Ai] Backend non disponibile, uso Pollinations:', e);
      }
    }
    
    // Fallback to Pollinations only if backend fails
    console.warn('[T-Ai] Backend non disponibile, tentativo Pollinations...');
    const pollinationsResult = _pollinationsFetch(_messagesForPollinations(messages), temp);
    
    // If Pollinations also fails with queue full, show helpful message
    if (pollinationsResult.includes('Queue full') || pollinationsResult.includes('temporaneamente occupato')) {
      return '**⚠️ Servizio AI al momento sovraccarico**\\n\\nIl servizio gratuito Pollinations ha raggiunto il limite di code. Per continuare a usare T-Ai senza interruzioni:\\n\\n1. Avvia il server backend: `python3 api_keys.py`\\n2. Questo attiverà le 3 chiavi ChatGPT come fallback\\n\\nIn alternativa, riprova tra qualche secondo.';
    }
    
    return pollinationsResult;
  }'''


if old_tai_generate in content:
    content = content.replace(old_tai_generate, new_tai_generate)
    print("[OK] Updated taiGenerateMessages to prioritize backend server")
else:
    print("[SKIP] taiGenerateMessages not found or already updated")

# Also update the _pollinationsFetch to handle queue full better
    console.warn('[T-Ai] Pollinations fallito:', lastErr);
    
    // Check if it's a queue full error
    if (lastErr.includes('Queue full') || lastErr.includes('queue full')) {
      return '**⚠️ Servizio AI sovraccarico (Pollinations)**\\n\\nIl servizio gratuito ha raggiunto il limite di code. Soluzioni:\\n\\n**Opzione 1 - Usa il backend (consigliato):**\\nAvvia `python3 api_keys.py` nel terminale per attivare le 3 chiavi ChatGPT come fallback.\\n\\n**Opzione 2 - Attendi:**\\nRiprova tra 10-20 secondi quando la libera.\\n\\n**Opzione 3 - Piano Premium:**\\nOttieni accesso illimitato su https://enter.pollinations.ai';
    }
    
    return lastErr
      ? `Servizio AI temporaneamente occupato. Riprova tra poco. (${lastErr.slice(0, 120)})`
      : 'Servizio AI non disponibile. Riprova più tardi.';
  }'''

new_pollinations_fetch_end = '''    console.warn('[T-Ai] Pollinations fallito:', lastErr);
    
    // Check if it's a queue full error
    if (lastErr.includes('Queue full') || lastErr.includes('queue full')) {
      return '**⚠️ Servizio AI sovraccarico (Pollinations)**\\n\\nIl servizio gratuito ha raggiunto il limite di code. Soluzioni:\\n\\n**Opzione 1 - Usa il backend (consigliato):**\\nAvvia `python3 api_keys.py` nel terminale per attivare le 3 chiavi ChatGPT come fallback.\\n\\n**Opzione 2 - Attendi:**\\nRiprova tra 10-20 secondi quando la libera.\\n\\n**Opzione 3 - Piano Premium:**\\nOttieni accesso illimitato su https://enter.pollinations.ai';
    }
    
    return lastErr
      ? `Servizio AI temporaneamente occupato. Riprova tra poco. (${lastErr.slice(0, 120)})`
      : 'Servizio AI non disponibile. Riprova più tardi.';
  }'''

if old_pollinations_fetch_end in content:
    content = content.replace(old_pollinations_fetch_end, new_pollinations_fetch_end)
    print("[OK] Updated _pollinationsFetch to handle queue full with better message")
else:
    print("[SKIP] _pollinationsFetch end not found or already updated")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== Pollinations fallback fix applied ===")
print("NOTE: To use the ChatGPT fallback, run: python3 api_keys.py")
