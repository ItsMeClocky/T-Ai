# T-Ai su Firebase (Hosting + Cloud Functions)

Backend proxy che sostituisce `api_keys.py` in produzione. Le chiavi API **non** vanno in `index.html`.

## Prerequisiti

1. [Firebase CLI](https://firebase.google.com/docs/cli): `npm install -g firebase-tools`
2. Account Google / progetto Firebase
3. Node.js 20+

## Configurazione progetto

```bash
cd /home/clocky/T-Ai
firebase login
firebase use --add   # scegli o crea il progetto
```

Modifica `.firebaserc` se serve: sostituisci `YOUR_FIREBASE_PROJECT_ID` con l’ID reale.

Abilita **Firestore** dalla console Firebase (Chat Work e feedback).

## Chiavi API (scegli un metodo)

### Metodo A — Secret Manager (consigliato)

```bash
cd functions
cp .env.example .env
# Compila .env solo per l’emulatore locale (non committare .env)

# In produzione (ripeti per ogni chiave):
firebase functions:secrets:set OPENAI_KEY_1
firebase functions:secrets:set OPENAI_KEY_2
firebase functions:secrets:set OPENAI_KEY_3
firebase functions:secrets:set GOOGLE_SEARCH_KEY
```

Dopo aver creato i secret, collegali alla function al deploy:

```bash
firebase deploy --only functions --set-secrets \
  OPENAI_KEY_1,OPENAI_KEY_2,OPENAI_KEY_3,GOOGLE_SEARCH_KEY
```

(Oppure imposta i secret come variabili d’ambiente nella console Google Cloud → Cloud Run → taiApi.)

### Metodo B — `functions:config` (legacy, ancora supportato)

```bash
firebase functions:config:set \
  openai.key1="sk-proj-..." \
  openai.key2="sk-proj-..." \
  openai.key3="sk-proj-..." \
  google.search_key="AIzaSy..."
```

Opzionali:

```bash
firebase functions:config:set gemini.key="..." manus.key="..."
```

### Emulatore locale

```bash
cd functions && npm install
cp .env.example .env
# Inserisci le chiavi in .env
firebase emulators:start --only functions,hosting
```

Apri `http://localhost:5000` — con hostname `localhost`, `index.html` usa ancora `http://localhost:8080` se tieni `api_keys.py` avviato; per testare solo Firebase, apri l’hosting emulator e imposta temporaneamente `TAI_BACKEND = ''` in `index.html`.

## Deploy

```bash
cd /home/clocky/T-Ai
cd functions && npm install && cd ..
firebase deploy
```

Solo hosting o solo functions:

```bash
firebase deploy --only hosting
firebase deploy --only functions
```

## URL e routing

| Endpoint | Descrizione |
|----------|-------------|
| `POST /generate` | OpenAI con rotazione 3 chiavi |
| `POST /search` | Google Custom Search (T-Deepsearch) |
| `POST /chatwork/send` | Messaggio Chat Work (Firestore) |
| `POST /chatwork/poll` | Poll messaggi |
| `POST /chatwork/like` | Feedback (Firestore) |

Su **Firebase Hosting**, i rewrite in `firebase.json` inviano queste path alla function `taiApi` sullo **stesso dominio** — `index.html` usa `TAI_BACKEND = ''` (stesso origin).

URL diretto function (senza rewrite):

`https://europe-west1-<PROJECT_ID>.cloudfunctions.net/taiApi/generate`

## Sviluppo locale classico

Puoi continuare con:

```bash
python3 api_keys.py
```

e aprire `index.html` da file o server locale: con hostname `localhost` il frontend punta a `http://localhost:8080`.

## File principali

| File | Ruolo |
|------|--------|
| `firebase.json` | Hosting + rewrite → `taiApi` |
| `functions/index.js` | Express: generate, search, chatwork |
| `functions/.env.example` | Template chiavi (senza valori reali) |
| `firestore.rules` | Regole Firestore (admin SDK in functions) |
| `index.html` | `TAI_BACKEND` automatico localhost vs produzione |

## Note

- **Chat Work** nell’UI usa `BroadcastChannel` (peer locale); gli endpoint `/chatwork/*` restano per compatibilità API e uso futuro con Firestore.
- Non committare `functions/.env`, `api_keys.py` con chiavi reali, o file `.firebase/`.
- Regione function: `europe-west1` (modificabile in `functions/index.js`).
