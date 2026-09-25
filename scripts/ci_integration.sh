#!/usr/bin/env bash
set -euo pipefail
python - <<'PY'
from apirest_mysql import MySQLStore
from pathlib import Path
with MySQLStore().connect() as conn, conn.cursor() as cur:
    for statement in Path('init.sql').read_text().split(';'):
        if statement.strip(): cur.execute(statement)
    conn.commit()
PY
gunicorn --bind 127.0.0.1:5000 apirest:app > /tmp/rest-memory-ci.log 2>&1 &
MEMORY_PID=$!
gunicorn --bind 127.0.0.1:5001 apirest_mysql:app > /tmp/rest-mysql-ci.log 2>&1 &
MYSQL_API_PID=$!
node bonus-node/server.js > /tmp/rest-node-ci.log 2>&1 &
NODE_PID=$!
trap 'kill "$MEMORY_PID" "$MYSQL_API_PID" "$NODE_PID" 2>/dev/null || true' EXIT
python - <<'PY'
import time,urllib.request
for port in (5000,5001,5002):
    for attempt in range(30):
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/health',timeout=2) as r:
                assert r.status==200
            break
        except Exception:
            if attempt==29: raise
            time.sleep(1)
PY
python scripts/verify_http.py --output integration-results.json
for PORT in 5000 5001 5002; do
  npx --yes newman@6.2.1 run postman/REST-equipo.postman_collection.json --env-var "base_url=http://127.0.0.1:$PORT" --reporters cli,json --reporter-json-export "newman-$PORT.json"
done
