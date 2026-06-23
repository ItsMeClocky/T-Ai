# T-Ai — Guida avvio

## ⚠️ Perché “non funziona”?

Spesso le chiavi OpenAI hanno **quota esaurita** e Pollinations ha **0 Pollen**. T-Ai risponde comunque in **modalità autonoma locale**.

## Avvio corretto

```bash
cd /home/clocky/T-Ai
./start-t-ai.sh
```

Apri **http://localhost:8080** (non il file HTML a mano).

## Attivare AI vera (consigliato)

1. Copia `.env.example` → `.env`
2. Crea chiave **gratuita** su https://console.groq.com
3. In `.env`: `GROQ_API_KEY=gsk_...`
4. Riavvia `./start-t-ai.sh`

Oppure ricarica credito OpenAI / Pollen su enter.pollinations.ai.

## Test rapido

```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/generate -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"ciao"}]}'
```
