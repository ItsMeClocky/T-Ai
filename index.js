/**
 * T-Ai Firebase Cloud Functions
 * Proxy sicuro: OpenAI (rotazione 3 chiavi), Google Search, Chat Work.
 */

const { onRequest } = require('firebase-functions/v2/https');
const { setGlobalOptions } = require('firebase-functions/v2');
const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');

if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}

if (!admin.apps.length) {
  admin.initializeApp();
}

const db = admin.firestore();

setGlobalOptions({ region: 'europe-west1', maxInstances: 10 });

const DEFAULT_GPT_MODEL = 'gpt-4o-mini';
const GOOGLE_SEARCH_CX =
  process.env.GOOGLE_SEARCH_CX || 'a0e7b8f1e0c1c4a58';

let currentOpenaiKeyIndex = 0;

/** Legge chiavi da env (secrets / .env) o da firebase functions:config (legacy). */
function getConfig() {
  let legacy = {};
  try {
    const { config } = require('firebase-functions');
    legacy = config() || {};
  } catch {
    legacy = {};
  }

  const openai = legacy.openai || {};
  const google = legacy.google || {};

  return {
    openaiKeys: [
      process.env.OPENAI_KEY_1 || openai.key1 || '',
      process.env.OPENAI_KEY_2 || openai.key2 || '',
      process.env.OPENAI_KEY_3 || openai.key3 || '',
    ],
    googleSearchKey:
      process.env.GOOGLE_SEARCH_KEY || google.search_key || '',
    geminiKey: process.env.GEMINI_API_KEY || legacy.gemini?.key || '',
    manusKey: process.env.MANUS_API_KEY || legacy.manus?.key || '',
    pollinationsKey:
      process.env.POLLINATIONS_API_KEY || legacy.pollinations?.key || 'pk_4cLLA14PbmP2lG42',
  };
}

async function tryOpenai(model, messages) {
  const { openaiKeys } = getConfig();
  const errors = [];

  for (let attempt = 0; attempt < openaiKeys.length; attempt++) {
    const idx = (currentOpenaiKeyIndex + attempt) % openaiKeys.length;
    const key = openaiKeys[idx];
    if (!key) continue;

    try {
      const res = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${key}`,
        },
        body: JSON.stringify({ model, messages }),
        signal: AbortSignal.timeout(30000),
      });

      if (!res.ok) {
        const body = await res.text();
        errors.push(`Key #${idx + 1}: HTTP ${res.status} — ${body.slice(0, 200)}`);
        console.warn(`[T-Ai] OpenAI key #${idx + 1} fallita: HTTP ${res.status}`);
        continue;
      }

      const result = await res.json();
      const text = result?.choices?.[0]?.message?.content ?? '';
      currentOpenaiKeyIndex = (idx + 1) % openaiKeys.length;
      return {
        response: text,
        model,
        provider: 'openai',
        gpt_available: true,
      };
    } catch (e) {
      errors.push(`Key #${idx + 1}: ${e.message}`);
      console.warn(`[T-Ai] OpenAI key #${idx + 1} errore:`, e.message);
    }
  }

  return { response: null, gpt_available: false, errors };
}

async function pollinationsGetSimple(messages) {
  const { pollinationsKey } = getConfig();
  let system = '';
  let userText = '';
  for (const m of messages) {
    const c = m.content;
    const text = Array.isArray(c)
      ? c.filter((p) => p.type === 'text').map((p) => p.text).join(' ')
      : String(c || '');
    if (m.role === 'system') system = text;
    else if (m.role === 'user' && text) userText = text;
  }
  const prompt = (system ? `${system}\n\n${userText}` : userText) || 'Ciao';
  try {
    const headers = {};
    if (pollinationsKey) headers.Authorization = `Bearer ${pollinationsKey}`;
    const res = await fetch(
      `https://text.pollinations.ai/${encodeURIComponent(prompt.slice(0, 4000))}?model=qwen-coder`,
      { headers, signal: AbortSignal.timeout(90000) }
    );
    const text = (await res.text()).trim();
    if (text && text.length > 2 && !text.startsWith('{')) {
      return { response: text, model: 'qwen-coder', provider: 'pollinations', gpt_available: false };
    }
  } catch (e) {
    console.warn('[T-Ai] Pollinations GET:', e.message);
  }
  return null;
}

async function pollinationsChat(messages, preferredModel = 'qwen-coder') {
  const { pollinationsKey } = getConfig();
  const models = [preferredModel, 'qwen-coder', 'openai-fast', 'openai', 'mistral'];
  const seen = new Set();

  for (const model of models) {
    if (seen.has(model)) continue;
    seen.add(model);
    try {
      const headers = { 'Content-Type': 'application/json' };
      if (pollinationsKey) headers.Authorization = `Bearer ${pollinationsKey}`;
      const res = await fetch('https://text.pollinations.ai/openai', {
        method: 'POST',
        headers,
        body: JSON.stringify({ model, messages, stream: false }),
        signal: AbortSignal.timeout(90000),
      });
      const result = await res.json().catch(() => ({}));
      const text = result?.choices?.[0]?.message?.content ?? '';
      if (text) {
        return {
          response: text,
          model,
          provider: 'pollinations',
          gpt_available: false,
        };
      }
      const err =
        typeof result.error === 'string'
          ? result.error
          : result.error?.message || `HTTP ${res.status}`;
      console.warn(`[T-Ai] Pollinations (${model}):`, err);
    } catch (e) {
      console.warn(`[T-Ai] Pollinations (${model}) errore:`, e.message);
    }
  }
  return pollinationsGetSimple(messages);
}

async function googleSearch(query) {
  const { googleSearchKey } = getConfig();
  if (!googleSearchKey || !query) return [];

  const params = new URLSearchParams({
    key: googleSearchKey,
    cx: GOOGLE_SEARCH_CX,
    q: query,
    num: '8',
    lr: 'lang_it',
    gl: 'it',
  });

  try {
    const res = await fetch(
      `https://www.googleapis.com/customsearch/v1?${params}`,
      { signal: AbortSignal.timeout(10000) }
    );
    if (!res.ok) {
      console.warn('[T-Ai] Google Search HTTP', res.status);
      return [];
    }
    const data = await res.json();
    return (data.items || []).map((i) => ({
      title: i.title || '',
      link: i.link || '',
      snippet: i.snippet || '',
      displayLink: i.displayLink || '',
    }));
  } catch (e) {
    console.warn('[T-Ai] Google Search error:', e.message);
    return [];
  }
}

async function callGemini(model, messages) {
  const { geminiKey } = getConfig();
  const contents = messages.map((m) => ({
    role: m.role === 'user' ? 'user' : 'model',
    parts: [{ text: m.content }],
  }));

  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${geminiKey}`;
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents }),
    signal: AbortSignal.timeout(60000),
  });
  const result = await res.json();
  const text =
    result?.candidates?.[0]?.content?.parts?.[0]?.text ?? '';
  return { response: text, model, provider: 'gemini', gpt_available: true };
}

async function callManus(model, messages) {
  const { manusKey } = getConfig();
  const res = await fetch('https://api.manus.ai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${manusKey}`,
    },
    body: JSON.stringify({ model, messages }),
    signal: AbortSignal.timeout(120000),
  });
  const result = await res.json();
  const text = result?.choices?.[0]?.message?.content ?? '';
  return { response: text, model, provider: 'manus', gpt_available: true };
}

const CHATWORK_COLLECTION = 'chatwork_messages';
const CHATWORK_MAX = 100;

async function trimChatworkMessages() {
  const snap = await db
    .collection(CHATWORK_COLLECTION)
    .orderBy('id', 'asc')
    .get();
  if (snap.size <= CHATWORK_MAX) return;
  const toDelete = snap.docs.slice(0, snap.size - CHATWORK_MAX);
  const batch = db.batch();
  toDelete.forEach((d) => batch.delete(d.ref));
  await batch.commit();
}

const app = express();
app.use(cors({ origin: true }));
app.use(express.json());

app.post('/generate', async (req, res) => {
  try {
    const provider = req.body.provider || 'openai';
    let model = req.body.model || DEFAULT_GPT_MODEL;
    const messages = req.body.messages || [];

    if (
      provider !== 'gemini' &&
      provider !== 'manus' &&
      !model.toLowerCase().includes('gpt') &&
      !model.toLowerCase().includes('o3')
    ) {
      model = DEFAULT_GPT_MODEL;
    }

    const cfg = getConfig();

    if (provider === 'gemini' && cfg.geminiKey) {
      return res.json(await callGemini(model, messages));
    }
    if (provider === 'manus' && cfg.manusKey) {
      return res.json(await callManus(model, messages));
    }

    const result = await tryOpenai(model, messages);
    if (result.gpt_available) {
      return res.json(result);
    }

    const poll = await pollinationsChat(messages);
    if (poll) {
      poll.notice = 'Tecnologia GPT non disponibile, generazione risposta autonoma';
      return res.json(poll);
    }

    const user =
      [...messages].reverse().find((m) => m.role === 'user')?.content || 'ciao';
    const ut = typeof user === 'string' ? user : 'Messaggio ricevuto';
    return res.json({
      response: `Ciao! Sono T-Ai. I servizi cloud non rispondono ora. Ho ricevuto: «${String(ut).slice(0, 200)}». Riprova tra poco.`,
      model: 't-ai-local',
      provider: 'local',
      gpt_available: false,
      notice: 'Tecnologia GPT non disponibile, generazione risposta autonoma',
      errors: result.errors || [],
    });
  } catch (e) {
    console.error('[T-Ai] /generate', e);
    return res.status(500).json({ error: String(e.message) });
  }
});

app.post('/search', async (req, res) => {
  const query = req.body.query || '';
  if (!query) return res.json({ results: [] });
  const results = await googleSearch(query);
  return res.json({ results });
});

app.post('/chatwork/send', async (req, res) => {
  try {
    const user = req.body.user || 'Anonimo';
    const text = req.body.text || '';
    const id = Date.now();
    const msg = {
      id,
      user,
      text,
      timestamp: Date.now() / 1000,
    };

    await db.collection(CHATWORK_COLLECTION).doc(String(id)).set(msg);
    await db.collection('chatwork_users').doc(user).set({ user, updatedAt: admin.firestore.FieldValue.serverTimestamp() }, { merge: true });
    await trimChatworkMessages();

    return res.json({ status: 'ok', message: msg });
  } catch (e) {
    console.error('[T-Ai] chatwork/send', e);
    return res.status(500).json({ error: String(e.message) });
  }
});

app.post('/chatwork/poll', async (req, res) => {
  try {
    const lastId = Number(req.body.last_id) || 0;
    const snap = await db
      .collection(CHATWORK_COLLECTION)
      .where('id', '>', lastId)
      .orderBy('id', 'asc')
      .limit(50)
      .get();

    const messages = snap.docs.map((d) => d.data());
    const usersSnap = await db.collection('chatwork_users').get();
    const users = usersSnap.docs.map((d) => d.id);

    return res.json({ messages, users });
  } catch (e) {
    console.error('[T-Ai] chatwork/poll', e);
    return res.status(500).json({ error: String(e.message) });
  }
});

app.post('/chatwork/like', async (req, res) => {
  try {
    const entry = {
      msg_id: req.body.msg_id || '',
      action: req.body.action || 'like',
      feedback: req.body.feedback || '',
      time: Date.now() / 1000,
    };
    await db.collection('feedback').add(entry);
    return res.json({ status: 'ok' });
  } catch (e) {
    console.error('[T-Ai] chatwork/like', e);
    return res.status(500).json({ error: String(e.message) });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: 'Not found' });
});

exports.taiApi = onRequest(
  {
    cors: true,
    timeoutSeconds: 120,
    memory: '512MiB',
  },
  app
);
