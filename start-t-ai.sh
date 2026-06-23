#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Avvio T-Ai su http://localhost:8080 ..."
if command -v xdg-open >/dev/null 2>&1; then
  (sleep 1.2 && xdg-open "http://localhost:8080") &
elif command -v open >/dev/null 2>&1; then
  (sleep 1.2 && open "http://localhost:8080") &
fi
exec python3 api_keys.py
