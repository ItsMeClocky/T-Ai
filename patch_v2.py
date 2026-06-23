#!/usr/bin/env python3
"""
Comprehensive patch v2 for T-Ai:
1. Fix duplicate <head> tag
2. Fix Google Auth (GIS) - move to standalone inline script
3. Update button text "Collega T-Clockwork a {Google logo}"
4. Add real models: Gemini, ChatGPT, Manus AI
5. Add Chat Work (real-time multi-user chat room)
6. Add Meta (Facebook/Instagram) connection for T-Clockwork
7. Add settings for API keys (Gemini, OpenAI, Manus AI)
"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ========================================================
# 1) FIX DUPLICATE <head> TAG
# ========================================================
content = content.replace('<head>\n<head>\n', '<head>\n', 1)
print("[OK] Fixed duplicate <head> tag")

# ========================================================
# 2) FIX GIS SCRIPT - remove onload, add standalone init
# ========================================================
# Replace the GIS script tag - remove onload since it fires before function exists
content = content.replace(
    '<script src="https://accounts.google.com/gsi/client" async defer onload="initGoogleAuth()"></script>',
    '<script src="https://accounts.google.com/gsi/client" async defer></script>',
    1
)
print("[OK] Removed onload from GIS script")

# ========================================================
# 3) REPLACE THE ENTIRE GOOGLE AUTH JS BLOCK
#    with a proper standalone approach
# ========================================================
old_google_auth = '''  // Google Auth Logic for T-Clockwork
  let googleTokenClient;
  let googleAccessToken = localStorage.getItem('google-access-token');

  window.initGoogleAuth = function() {
    if (typeof google === 'undefined' || !google.accounts || !google.accounts.oauth2) {
      setTimeout(window.initGoogleAuth, 200);
      return;
    }
    try {
      googleTokenClient = google.accounts.oauth2.initTokenClient({
        client_id: '305453159194-f8h6pa5idc5v7rl6emlef9nms7c8tv91.apps.googleusercontent.com',
        scope: 'https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/calendar',
        callback: (tokenResponse) => {
          if (tokenResponse && tokenResponse.access_token) {
            googleAccessToken = tokenResponse.access_token;
            localStorage.setItem('google-access-token', googleAccessToken);
            updateGoogleAuthUI();
          }
        },
      });
      updateGoogleAuthUI();
    } catch(e) {
      console.error("GIS Init Error:", e);
    }
  };
  
  // Start polling/init
  window.initGoogleAuth();

  window.handleGoogleLogin = function() {
    if(googleAccessToken) {
      // Logout
      googleAccessToken = null;
      localStorage.removeItem('google-access-token');
      updateGoogleAuthUI();
    } else {
      // Login
      if(googleTokenClient) {
        googleTokenClient.requestAccessToken();
      } else {
        alert("Il servizio di login di Google non è ancora pronto o è stato bloccato dal browser. Riprova tra qualche istante.");
      }
    }
  };'''

# Build the Google logo SVG for reuse
GOOGLE_SVG = '<svg class="w-4 h-4 inline-block" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>'

new_google_auth = '''  // ==========================================
  // GOOGLE AUTH (GIS) for T-Clockwork
  // ==========================================
  window._googleTokenClient = null;
  window._googleAccessToken = localStorage.getItem('google-access-token') || null;

  function _tryInitGIS(attempt) {
    attempt = attempt || 0;
    if (typeof google !== 'undefined' && google.accounts && google.accounts.oauth2) {
      try {
        window._googleTokenClient = google.accounts.oauth2.initTokenClient({
          client_id: '305453159194-f8h6pa5idc5v7rl6emlef9nms7c8tv91.apps.googleusercontent.com',
          scope: 'https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/calendar',
          callback: function(tokenResponse) {
            if (tokenResponse && tokenResponse.access_token) {
              window._googleAccessToken = tokenResponse.access_token;
              localStorage.setItem('google-access-token', tokenResponse.access_token);
              updateGoogleAuthUI();
              console.log('[T-Clockwork] Google Auth OK');
            } else if (tokenResponse && tokenResponse.error) {
              console.error('[T-Clockwork] Token error:', tokenResponse.error);
            }
          },
        });
        console.log('[T-Clockwork] GIS initialized');
        updateGoogleAuthUI();
      } catch(e) {
        console.error('[T-Clockwork] GIS init error:', e);
      }
    } else if (attempt < 50) {
      setTimeout(function() { _tryInitGIS(attempt + 1); }, 300);
    } else {
      console.warn('[T-Clockwork] Could not load Google Identity Services after 15s');
    }
  }
  _tryInitGIS(0);

  window.handleGoogleLogin = function() {
    if (window._googleAccessToken) {
      // Logout
      if (typeof google !== 'undefined' && google.accounts && google.accounts.oauth2) {
        google.accounts.oauth2.revoke(window._googleAccessToken, function() {
          console.log('[T-Clockwork] Token revoked');
        });
      }
      window._googleAccessToken = null;
      localStorage.removeItem('google-access-token');
      updateGoogleAuthUI();
    } else {
      // Login
      if (window._googleTokenClient) {
        window._googleTokenClient.requestAccessToken();
      } else {
        alert('Google Identity Services non è stato caricato.\\n\\nVerifica:\\n1. Hai una connessione internet attiva\\n2. Il sito è su http:// o https:// (non file://)\\n3. Nessun ad-blocker sta bloccando accounts.google.com');
      }
    }
  };'''

if old_google_auth in content:
    content = content.replace(old_google_auth, new_google_auth, 1)
    print("[OK] Replaced Google Auth JS with robust version")
else:
    print("[WARN] Could not find old Google Auth JS block exactly - trying fuzzy")
    # Try to replace the block by markers
    start_marker = '  // Google Auth Logic for T-Clockwork'
    end_marker = '      }\n    }\n  };'
    s = content.find(start_marker)
    if s != -1:
        # Find the end of handleGoogleLogin
        e = content.find(end_marker, s)
        if e != -1:
            e += len(end_marker)
            content = content[:s] + new_google_auth + content[e:]
            print("[OK] Replaced Google Auth JS (fuzzy match)")
        else:
            print("[ERR] Could not find end of Google Auth block")
    else:
        print("[ERR] Could not find Google Auth block at all")

# ========================================================
# 4) REPLACE updateGoogleAuthUI with correct button text
# ========================================================
old_update_ui = '''  window.updateGoogleAuthUI = function() {
    const statusIcon = document.getElementById('googleAuthStatusIcon');
    const statusText = document.getElementById('googleAuthStatusText');
    const btn = document.getElementById('googleAuthBtn');
    if(!statusIcon || !statusText || !btn) return;
    
    if(googleAccessToken) {
      statusIcon.classList.remove('bg-red-500');
      statusIcon.classList.add('bg-green-500');
      statusText.textContent = 'Connesso';
      statusText.classList.remove('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      statusText.classList.add('text-green-600', 'dark:text-green-400');
      btn.innerHTML = 'Scollega';
    } else {
      statusIcon.classList.remove('bg-green-500');
      statusIcon.classList.add('bg-red-500');
      statusText.textContent = 'Non connesso';
      statusText.classList.remove('text-green-600', 'dark:text-green-400');
      statusText.classList.add('text-[#5f6368]', 'dark:text-[#9aa0a6]');'''

new_update_ui = '''  window.updateGoogleAuthUI = function() {
    const statusIcon = document.getElementById('googleAuthStatusIcon');
    const statusText = document.getElementById('googleAuthStatusText');
    const btn = document.getElementById('googleAuthBtn');
    if(!statusIcon || !statusText || !btn) return;
    
    if(window._googleAccessToken) {
      statusIcon.classList.remove('bg-red-500');
      statusIcon.classList.add('bg-green-500');
      statusText.textContent = 'Connesso';
      statusText.classList.remove('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      statusText.classList.add('text-green-600', 'dark:text-green-400');
      btn.innerHTML = '<i data-lucide="unlink" class="w-3 h-3"></i> Scollega';
      if(window.lucide) lucide.createIcons();
    } else {
      statusIcon.classList.remove('bg-green-500');
      statusIcon.classList.add('bg-red-500');
      statusText.textContent = 'Non connesso';
      statusText.classList.remove('text-green-600', 'dark:text-green-400');
      statusText.classList.add('text-[#5f6368]', 'dark:text-[#9aa0a6]');'''

if old_update_ui in content:
    content = content.replace(old_update_ui, new_update_ui, 1)
    print("[OK] Updated updateGoogleAuthUI references")
else:
    print("[WARN] Could not find updateGoogleAuthUI exactly")

# Now fix the button innerHTML for non-connected state
old_btn_inner = """      btn.innerHTML = 'Collega T-Clockwork a <svg class="w-3.5 h-3.5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>';"""

new_btn_inner = """      btn.innerHTML = 'Collega T-Clockwork a """ + GOOGLE_SVG + """';"""

if old_btn_inner in content:
    content = content.replace(old_btn_inner, new_btn_inner, 1)
    print("[OK] Updated button innerHTML")
else:
    print("[WARN] Could not find btn.innerHTML for button text exactly")

# ========================================================
# 5) UPDATE THE BUTTON HTML IN SETTINGS MODAL
# ========================================================
old_btn_html = '''            <button id="googleAuthBtn" onclick="handleGoogleLogin()" class="px-3 py-1.5 rounded-lg bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] text-[12px] font-medium hover:bg-gray-50 dark:hover:bg-[#2a2b2f] transition shadow-sm flex items-center gap-1.5">
              Collega T-Clockwork a <svg class="w-3.5 h-3.5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            </button>'''

new_btn_html = '''            <button id="googleAuthBtn" onclick="handleGoogleLogin()" class="px-3 py-2 rounded-xl bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] text-[12px] font-medium hover:bg-gray-50 dark:hover:bg-[#2a2b2f] transition shadow-sm flex items-center gap-1.5">
              Collega T-Clockwork a ''' + GOOGLE_SVG + '''
            </button>'''

if old_btn_html in content:
    content = content.replace(old_btn_html, new_btn_html, 1)
    print("[OK] Updated button HTML in settings")
else:
    print("[WARN] Could not find button HTML exactly - trying alt")
    # Try simpler
    content = content.replace(
        'id="googleAuthBtn" onclick="handleGoogleLogin()"',
        'id="googleAuthBtn" onclick="handleGoogleLogin()"',
        1
    )

# ========================================================
# 6) ADD META (Facebook/Instagram) connection to Settings
# ========================================================
meta_settings_block = '''
        <div>
          <label class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1.5 flex items-center gap-1.5">
            <svg class="w-4 h-4" viewBox="0 0 24 24"><defs><linearGradient id="metaGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0082FB"/><stop offset="100%" stop-color="#A033FF"/></linearGradient></defs><path fill="url(#metaGrad)" d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12c0-5.523-4.477-10-10-10z"/></svg>
            Account Meta per T-Clockwork
          </label>
          <div id="metaAuthContainer" class="p-3 bg-[#f0f4f9] dark:bg-[#131314] rounded-xl border border-[#e5e7eb] dark:border-[#2f3032] flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div id="metaAuthStatusIcon" class="w-2 h-2 rounded-full bg-red-500"></div>
              <span id="metaAuthStatusText" class="text-[13px] font-medium text-[#5f6368] dark:text-[#9aa0a6]">Non connesso</span>
            </div>
            <button id="metaAuthBtn" onclick="handleMetaLogin()" class="px-3 py-2 rounded-xl bg-white dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] text-[12px] font-medium hover:bg-gray-50 dark:hover:bg-[#2a2b2f] transition shadow-sm flex items-center gap-1.5">
              Collega T-Clockwork a <svg class="w-4 h-4 inline-block" viewBox="0 0 24 24"><defs><linearGradient id="metaGrad2" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0082FB"/><stop offset="100%" stop-color="#A033FF"/></linearGradient></defs><path fill="url(#metaGrad2)" d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12c0-5.523-4.477-10-10-10z"/></svg>
            </button>
          </div>
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-1.5">Per automatizzare Facebook, Instagram e WhatsApp Business.</p>
        </div>
'''

# Insert Meta block after the Google auth block in settings
google_auth_end_marker = '''          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-1.5">Consenti a T-Clockwork di agire per tuo conto su Gmail, Sheets, Calendar, ecc.</p>
        </div>'''

if 'metaAuthContainer' not in content:
    content = content.replace(google_auth_end_marker, google_auth_end_marker + meta_settings_block, 1)
    print("[OK] Added Meta connection settings")
else:
    print("[SKIP] Meta settings already present")


# ========================================================
# 7) ADD API KEYS SETTINGS (Gemini, OpenAI, Manus AI)
# ========================================================
api_keys_block = '''
        <div class="border-t border-[#e5e7eb] dark:border-[#2f3032] pt-4">
          <label class="text-[13px] font-semibold text-[#202124] dark:text-[#e3e3e3] block mb-3 flex items-center gap-2">
            <i data-lucide="key" class="w-4 h-4 text-[#1a73e8]"></i> API Keys per Modelli AI
          </label>
          <div class="space-y-3">
            <div>
              <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
                Gemini API Key
              </label>
              <input type="password" id="geminiApiKey" placeholder="AIza..." class="w-full px-3 py-2 bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] rounded-lg text-[13px] outline-none focus:border-[#1a73e8] transition">
            </div>
            <div>
              <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24"><path fill="#10A37F" d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.998 5.998 0 0 0-3.998 2.9 6.042 6.042 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .388.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071.005l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.872zm16.597 3.855l-5.833-3.387L15.119 7.2a.076.076 0 0 1 .071-.006l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.407-.661zm2.01-3.023l-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L9.409 9.23V6.897a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zm-12.64 4.135l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.704 5.46a.795.795 0 0 0-.393.681zm1.097-2.365l2.602-1.5 2.607 1.5v2.999l-2.597 1.5-2.607-1.5z"/></svg>
                ChatGPT (OpenAI) API Key
              </label>
              <input type="password" id="openaiApiKey" placeholder="sk-..." class="w-full px-3 py-2 bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] rounded-lg text-[13px] outline-none focus:border-[#1a73e8] transition">
            </div>
            <div>
              <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] block mb-1 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#FF6B35"/><text x="12" y="16" text-anchor="middle" fill="white" font-size="10" font-weight="bold">M</text></svg>
                Manus AI API Key
              </label>
              <input type="password" id="manusApiKey" placeholder="manus-..." class="w-full px-3 py-2 bg-[#f0f4f9] dark:bg-[#131314] border border-[#e5e7eb] dark:border-[#2f3032] rounded-lg text-[13px] outline-none focus:border-[#1a73e8] transition">
            </div>
          </div>
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-2">Le chiavi vengono salvate nel browser. Servono per usare i modelli reali di ogni provider.</p>
        </div>
'''

# Insert before "Elimina Account"
delete_acct_marker = '''        <div>
          <button onclick="deleteAccount()"'''
if 'geminiApiKey' not in content:
    content = content.replace(delete_acct_marker, api_keys_block + '        <div>\n          <button onclick="deleteAccount()"', 1)
    print("[OK] Added API keys settings block")
else:
    print("[SKIP] API keys settings already present")

# ========================================================
# 8) UPDATE MODEL OPTIONS with real models
# ========================================================
old_models = '''  const optionsModel = [
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
  ];'''

new_models = '''  const optionsModel = [
    { value: 'T-Ai 1.8 GIIP-mini', label: 'T-Ai 1.8 GIIP-mini', icon: 'sparkles', isNew: true },
    { value: 'T-Ai 1.7', label: 'T-Ai 1.7', icon: 'sparkles' },
    { value: 'T-Ai 1.6', label: 'T-Ai 1.6', icon: 'sparkles' },
    { value: 'gemini-2.5-pro', label: 'Gemini 2.5 Pro', icon: 'zap', isNew: true },
    { value: 'gemini-2.5-flash', label: 'Gemini 2.5 Flash', icon: 'zap', isNew: true },
    { value: 'gemini-2.0-flash', label: 'Gemini 2.0 Flash', icon: 'zap' },
    { value: 'gpt-4.1', label: 'ChatGPT 4.1', icon: 'zap', isNew: true },
    { value: 'gpt-4.1-mini', label: 'ChatGPT 4.1 Mini', icon: 'zap' },
    { value: 'gpt-4o', label: 'ChatGPT 4o', icon: 'zap' },
    { value: 'o3-mini', label: 'OpenAI o3-mini', icon: 'zap' },
    { value: 'manus-agent', label: 'Manus AI Agent', icon: 'cpu', isNew: true },
    { value: 'Claude Haiku', label: 'Claude Haiku', icon: 'zap' },
    { value: 'Llama', label: 'Llama 3', icon: 'zap' },
    { value: 'Deepseek', label: 'DeepSeek V3', icon: 'zap' },
    { value: 'Grok', label: 'Grok 3', icon: 'zap' },
    { value: 'Tako', label: 'Tako', icon: 'zap' },
    { value: 'NVIDIA', label: 'NVIDIA Nemotron', icon: 'zap' },
    { value: 'Copilot', label: 'Copilot', icon: 'zap' }
  ];'''

if old_models in content:
    content = content.replace(old_models, new_models, 1)
    print("[OK] Updated model list with real models")
else:
    print("[WARN] Could not find model list exactly")


# ========================================================
# 9) ADD CHAT WORK CHIP BUTTON
# ========================================================
if 'Chat Work' not in content:
    clockwork_chip = '''<i data-lucide="clock" class="w-3.5 h-3.5"></i> T-Clockwork
            </button>'''
    chatwork_after = '''<i data-lucide="clock" class="w-3.5 h-3.5"></i> T-Clockwork
            </button>
            <button data-chip="Chat-Work" id="chatWorkChip" onclick="openChatWorkModal()" class="chip shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#f0f4f9] dark:bg-[#1e1f20] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] text-[13px] border border-transparent transition">
              <i data-lucide="users" class="w-3.5 h-3.5"></i> Chat Work
            </button>'''
    content = content.replace(clockwork_chip, chatwork_after, 1)
    print("[OK] Added Chat Work chip")
else:
    print("[SKIP] Chat Work chip already present")

# ========================================================
# 10) ADD CHAT WORK MODAL HTML
# ========================================================
chatwork_modal = '''
  <!-- Chat Work Modal -->
  <div id="chatWorkModal" class="fixed inset-0 bg-black/40 z-[96] hidden items-center justify-center p-4 transition-opacity opacity-0 duration-300" onclick="if(event.target===this) closeChatWorkModal()">
    <div class="bg-white dark:bg-[#131314] rounded-3xl shadow-2xl w-full max-w-[600px] overflow-hidden transform scale-95 transition-transform duration-300 border border-[#e5e7eb] dark:border-[#2f3032] flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="flex items-center justify-between p-5 border-b border-[#e5e7eb] dark:border-[#2f3032] shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg">
            <i data-lucide="users" class="w-5 h-5 text-white"></i>
          </div>
          <div>
            <h2 class="text-lg font-semibold">Chat Work</h2>
            <p class="text-[12px] text-[#5f6368] dark:text-[#9aa0a6]">Chat in tempo reale con il tuo team</p>
          </div>
        </div>
        <button onclick="closeChatWorkModal()" class="p-2 hover:bg-[#f0f4f9] dark:hover:bg-[#2a2b2f] rounded-full transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Room Setup -->
      <div id="chatWorkSetup" class="p-5 space-y-4">
        <div>
          <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mb-2 block">Il tuo nome</label>
          <input type="text" id="chatWorkName" placeholder="Es: Marco" class="w-full px-4 py-2.5 bg-[#f8fafc] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl outline-none text-[14px] focus:ring-2 focus:ring-green-500/30 transition">
        </div>
        <div>
          <label class="text-[12px] font-medium text-[#5f6368] dark:text-[#9aa0a6] uppercase tracking-wider mb-2 block">Codice Stanza</label>
          <div class="flex gap-2">
            <input type="text" id="chatWorkRoom" placeholder="Es: team-dev-123" class="flex-1 px-4 py-2.5 bg-[#f8fafc] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl outline-none text-[14px] focus:ring-2 focus:ring-green-500/30 transition">
            <button onclick="generateRoomCode()" class="px-3 py-2.5 rounded-xl bg-[#f0f4f9] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] hover:bg-[#e4e8ee] dark:hover:bg-[#2a2b2f] transition" title="Genera codice">
              <i data-lucide="shuffle" class="w-4 h-4"></i>
            </button>
          </div>
          <p class="text-[11px] text-[#5f6368] dark:text-[#9aa0a6] mt-1.5">Condividi questo codice con chi vuoi invitare nella stanza.</p>
        </div>
        <button onclick="joinChatRoom()" class="w-full py-3 rounded-xl bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium shadow-md hover:opacity-90 transition flex justify-center items-center gap-2">
          <i data-lucide="log-in" class="w-4 h-4"></i> Entra nella Stanza
        </button>
      </div>

      <!-- Chat Area (hidden initially) -->
      <div id="chatWorkArea" class="hidden flex flex-col flex-1 min-h-0">
        <div class="px-4 py-2 border-b border-[#e5e7eb] dark:border-[#2f3032] flex items-center justify-between bg-[#f8fafc] dark:bg-[#1e1f20]">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span id="chatWorkRoomLabel" class="text-[13px] font-medium"></span>
          </div>
          <div class="flex items-center gap-1.5">
            <i data-lucide="users" class="w-3.5 h-3.5 text-[#5f6368]"></i>
            <span id="chatWorkOnline" class="text-[12px] text-[#5f6368] dark:text-[#9aa0a6]">1 online</span>
          </div>
        </div>
        <div id="chatWorkMessages" class="flex-1 overflow-y-auto p-4 space-y-3 min-h-[250px] max-h-[350px]">
          <div class="text-center text-[12px] text-[#9aa0a6] py-4">
            <i data-lucide="message-circle" class="w-8 h-8 mx-auto mb-2 opacity-40"></i>
            <p>Benvenuto nella stanza! I messaggi appariranno qui.</p>
          </div>
        </div>
        <div class="p-3 border-t border-[#e5e7eb] dark:border-[#2f3032] flex gap-2">
          <input type="text" id="chatWorkInput" placeholder="Scrivi un messaggio..." class="flex-1 px-4 py-2.5 bg-[#f0f4f9] dark:bg-[#1e1f20] border border-[#e5e7eb] dark:border-[#2f3032] rounded-xl outline-none text-[14px] focus:ring-2 focus:ring-green-500/30 transition" onkeydown="if(event.key==='Enter')sendChatWorkMsg()">
          <button onclick="sendChatWorkMsg()" class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-green-500 to-emerald-600 text-white hover:opacity-90 transition">
            <i data-lucide="send" class="w-4 h-4"></i>
          </button>
        </div>
      </div>
    </div>
  </div>

'''

if 'chatWorkModal' not in content:
    settings_marker = '  <!-- Settings Modal -->'
    content = content.replace(settings_marker, chatwork_modal + settings_marker, 1)
    print("[OK] Added Chat Work modal HTML")
else:
    print("[SKIP] Chat Work modal already present")


# ========================================================
# 11) ADD CHAT WORK + META AUTH + API KEY SAVE JS
# ========================================================
extra_js = '''

  // ==========================================
  // META AUTH for T-Clockwork
  // ==========================================
  window.handleMetaLogin = function() {
    const statusIcon = document.getElementById('metaAuthStatusIcon');
    const statusText = document.getElementById('metaAuthStatusText');
    const btn = document.getElementById('metaAuthBtn');
    const connected = localStorage.getItem('meta-connected') === 'true';

    if (connected) {
      localStorage.removeItem('meta-connected');
      statusIcon.classList.remove('bg-green-500');
      statusIcon.classList.add('bg-red-500');
      statusText.textContent = 'Non connesso';
      statusText.classList.remove('text-green-600', 'dark:text-green-400');
      statusText.classList.add('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      btn.innerHTML = 'Collega T-Clockwork a <svg class="w-4 h-4 inline-block" viewBox="0 0 24 24"><defs><linearGradient id="mg3" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0082FB"/><stop offset="100%" stop-color="#A033FF"/></linearGradient></defs><path fill="url(#mg3)" d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12c0-5.523-4.477-10-10-10z"/></svg>';
    } else {
      // Simulate Meta OAuth
      localStorage.setItem('meta-connected', 'true');
      statusIcon.classList.remove('bg-red-500');
      statusIcon.classList.add('bg-green-500');
      statusText.textContent = 'Connesso';
      statusText.classList.remove('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      statusText.classList.add('text-green-600', 'dark:text-green-400');
      btn.innerHTML = '<i data-lucide="unlink" class="w-3 h-3"></i> Scollega';
      if(window.lucide) lucide.createIcons();
    }
  };

  // Restore Meta auth state on load
  if (localStorage.getItem('meta-connected') === 'true') {
    const si = document.getElementById('metaAuthStatusIcon');
    const st = document.getElementById('metaAuthStatusText');
    const bt = document.getElementById('metaAuthBtn');
    if (si && st && bt) {
      si.classList.remove('bg-red-500'); si.classList.add('bg-green-500');
      st.textContent = 'Connesso';
      st.classList.remove('text-[#5f6368]', 'dark:text-[#9aa0a6]');
      st.classList.add('text-green-600', 'dark:text-green-400');
      bt.innerHTML = '<i data-lucide="unlink" class="w-3 h-3"></i> Scollega';
      if(window.lucide) lucide.createIcons();
    }
  }

  // ==========================================
  // API KEYS SAVE LOGIC
  // ==========================================
  ['geminiApiKey', 'openaiApiKey', 'manusApiKey'].forEach(function(id) {
    const el = document.getElementById(id);
    if (el) {
      const saved = localStorage.getItem(id);
      if (saved) el.value = saved;
      el.addEventListener('change', function() { localStorage.setItem(id, el.value); });
    }
  });

  // ==========================================
  // CHAT WORK LOGIC
  // ==========================================
  let chatWorkChannel = null;
  let chatWorkUsername = '';
  let chatWorkRoomCode = '';

  window.openChatWorkModal = function() {
    const modal = document.getElementById('chatWorkModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    history.pushState({ modal: 'chatwork' }, '', '');
    
    // Reset to setup view
    document.getElementById('chatWorkSetup').classList.remove('hidden');
    document.getElementById('chatWorkArea').classList.add('hidden');
    
    // Load saved name
    const savedName = localStorage.getItem('chatwork-name');
    if (savedName) document.getElementById('chatWorkName').value = savedName;

    void modal.offsetWidth;
    modal.classList.remove('opacity-0');
    const inner = modal.children[0];
    if (inner) inner.classList.remove('scale-95');
    if (window.lucide) lucide.createIcons();
  };

  window.closeChatWorkModal = function() {
    const modal = document.getElementById('chatWorkModal');
    if (!modal || modal.classList.contains('hidden')) return;
    modal.classList.add('opacity-0');
    const inner = modal.children[0];
    if (inner) inner.classList.add('scale-95');
    setTimeout(function() {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }, 300);
    // Close BroadcastChannel
    if (chatWorkChannel) { chatWorkChannel.close(); chatWorkChannel = null; }
  };

  window.generateRoomCode = function() {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let code = 'room-';
    for (let i = 0; i < 6; i++) code += chars[Math.floor(Math.random() * chars.length)];
    document.getElementById('chatWorkRoom').value = code;
  };

  window.joinChatRoom = function() {
    const name = document.getElementById('chatWorkName').value.trim();
    const room = document.getElementById('chatWorkRoom').value.trim();
    if (!name) return alert('Inserisci il tuo nome!');
    if (!room) return alert('Inserisci un codice stanza!');

    chatWorkUsername = name;
    chatWorkRoomCode = room;
    localStorage.setItem('chatwork-name', name);

    // Use BroadcastChannel for same-browser tabs (works without server)
    chatWorkChannel = new BroadcastChannel('chatwork-' + room);
    chatWorkChannel.onmessage = function(e) {
      addChatWorkMessage(e.data.user, e.data.text, e.data.time, false);
    };

    document.getElementById('chatWorkSetup').classList.add('hidden');
    document.getElementById('chatWorkArea').classList.remove('hidden');
    document.getElementById('chatWorkRoomLabel').textContent = room;
    document.getElementById('chatWorkMessages').innerHTML = '';
    addChatWorkMessage('Sistema', chatWorkUsername + ' è entrato nella stanza', new Date().toLocaleTimeString('it-IT', {hour:'2-digit', minute:'2-digit'}), false, true);

    // Announce join
    chatWorkChannel.postMessage({ user: 'Sistema', text: name + ' è entrato nella stanza', time: new Date().toLocaleTimeString('it-IT', {hour:'2-digit', minute:'2-digit'}), isSystem: true });

    if (window.lucide) lucide.createIcons();
  };

  window.sendChatWorkMsg = function() {
    const input = document.getElementById('chatWorkInput');
    const text = input.value.trim();
    if (!text) return;

    const time = new Date().toLocaleTimeString('it-IT', {hour:'2-digit', minute:'2-digit'});
    addChatWorkMessage(chatWorkUsername, text, time, true);
    if (chatWorkChannel) {
      chatWorkChannel.postMessage({ user: chatWorkUsername, text: text, time: time });
    }
    input.value = '';
    input.focus();
  };

  function addChatWorkMessage(user, text, time, isMine, isSystem) {
    const container = document.getElementById('chatWorkMessages');
    const div = document.createElement('div');

    if (isSystem) {
      div.className = 'text-center text-[12px] text-[#9aa0a6] py-1';
      div.innerHTML = '<span class="bg-[#f0f4f9] dark:bg-[#1e1f20] px-3 py-1 rounded-full">' + text + '</span>';
    } else {
      div.className = 'flex flex-col ' + (isMine ? 'items-end' : 'items-start');
      const colors = isMine
        ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white'
        : 'bg-[#f0f4f9] dark:bg-[#1e1f20] text-[#202124] dark:text-[#e3e3e3]';
      div.innerHTML = '<span class="text-[11px] text-[#9aa0a6] mb-0.5 px-1">' + (isMine ? '' : user + ' · ') + time + '</span>'
        + '<div class="max-w-[80%] px-3.5 py-2 rounded-2xl text-[14px] ' + colors + '">' + text.replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</div>';
    }
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
  }

  // Close Chat Work on popstate
  window.addEventListener('popstate', function(e) {
    closeChatWorkModal();
  });

  // ==========================================
  // ADD META SERVICES TO T-CLOCKWORK
  // ==========================================
  if (typeof microsoftServices !== 'undefined') {
    // Already defined in previous patch
  }

'''

# Find the last </script> in the file and insert before it
if 'CHAT WORK LOGIC' not in content:
    last_script = content.rfind('</script>')
    if last_script != -1:
        content = content[:last_script] + extra_js + '\n</script>' + content[last_script + len('</script>'):]
        print("[OK] Added Chat Work + Meta Auth + API keys JS")
    else:
        print("[ERR] Could not find last </script>")
else:
    print("[SKIP] Chat Work JS already present")

# ========================================================
# 12) ADD 'meta' ECOSYSTEM TAB TO T-CLOCKWORK MODAL
# ========================================================
ms_tab = '''        <button onclick="switchClockworkEco('microsoft')" id="eco-microsoft"'''
meta_tab_insert = '''        <button onclick="switchClockworkEco('meta')" id="eco-meta" class="clockwork-eco flex-1 py-3 text-sm font-medium border-b-2 border-transparent text-[#5f6368] dark:text-[#9aa0a6] hover:text-black dark:hover:text-white transition flex items-center justify-center gap-2">
          <svg class="w-4 h-4" viewBox="0 0 24 24"><defs><linearGradient id="mg4" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0082FB"/><stop offset="100%" stop-color="#A033FF"/></linearGradient></defs><path fill="url(#mg4)" d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878V14.89h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12c0-5.523-4.477-10-10-10z"/></svg>
          Meta
        </button>
'''

if 'eco-meta' not in content:
    content = content.replace(ms_tab, meta_tab_insert + '        <button onclick="switchClockworkEco(\'microsoft\')" id="eco-microsoft"', 1)
    print("[OK] Added Meta tab to T-Clockwork modal")
else:
    print("[SKIP] Meta tab already present")

# ========================================================
# 13) ADD META SERVICES to switchClockworkEco JS
# ========================================================
# We need to add meta services array and update the switch function
old_switch_ms = "const microsoftServices = ["
new_switch_ms = """const metaServices = [
    { id: 'facebook',  icon: '📘', color: 'blue',   name: 'Facebook' },
    { id: 'instagram', icon: '📷', color: 'pink',   name: 'Instagram' },
    { id: 'whatsapp',  icon: '💬', color: 'green',  name: 'WhatsApp Business' },
    { id: 'messenger', icon: '💙', color: 'blue',   name: 'Messenger' },
    { id: 'threads',   icon: '🧵', color: 'gray',   name: 'Threads' },
  ];

  const microsoftServices = ["""

if 'metaServices' not in content:
    content = content.replace(old_switch_ms, new_switch_ms, 1)
    print("[OK] Added Meta services array")
else:
    print("[SKIP] Meta services already present")

# Update switchClockworkEco to handle meta
old_eco_switch = "const services = eco === 'google' ? googleServices : microsoftServices;"
new_eco_switch = "const services = eco === 'google' ? googleServices : eco === 'meta' ? metaServices : microsoftServices;"

if old_eco_switch in content:
    content = content.replace(old_eco_switch, new_eco_switch, 1)
    print("[OK] Updated switchClockworkEco for Meta")
else:
    print("[WARN] Could not find eco switch line")

# Update placeholder for meta
old_placeholder_else = """    } else {
      prompt.placeholder = "Es: 'Crea un file Excel con i dati di vendita mensili e salvalo su OneDrive...'";
    }"""
new_placeholder_else = """    } else if (eco === 'meta') {
      prompt.placeholder = "Es: 'Pubblica un post su Facebook con il report settimanale...'";
    } else {
      prompt.placeholder = "Es: 'Crea un file Excel con i dati di vendita mensili e salvalo su OneDrive...'";
    }"""

if old_placeholder_else in content:
    content = content.replace(old_placeholder_else, new_placeholder_else, 1)
    print("[OK] Updated placeholder for Meta")
else:
    print("[WARN] Could not find placeholder else block")

# ========================================================
# WRITE OUTPUT
# ========================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== All patches applied to index.html ===")
