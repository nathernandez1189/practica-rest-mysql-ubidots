#!/usr/bin/env bash
set -euo pipefail
BASE="${1:-http://127.0.0.1:5001}"
CURL_BODY=$(mktemp)
trap 'rm -f "$CURL_BODY"' EXIT
request() {
  local EXPECTED="$1" METHOD="$2" ROUTE="$3"
  shift 3
  echo "== $METHOD $ROUTE =="
  local CODE
  CODE=$(curl --silent --show-error --max-time 20 -o "$CURL_BODY" -w '%{http_code}' -X "$METHOD" "$BASE$ROUTE" "$@")
  cat "$CURL_BODY"; echo
  echo "HTTP $CODE (esperado $EXPECTED)"
  test "$CODE" = "$EXPECTED"
}
request 200 GET /books
request 201 POST /books -H 'Content-Type: application/json' --data '{"title":"Evidencia curl","author":"Natalia, Miguel y Juan Ospina"}'
BOOK_ID=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["book"]["id"])' "$CURL_BODY")
request 200 GET "/books/$BOOK_ID"
request 200 PUT "/books/$BOOK_ID" -H 'Content-Type: application/json' --data '{"description":"Actualizado con curl"}'
request 400 POST /books -H 'Content-Type: application/json' --data '{"title":""}'
request 200 DELETE "/books/$BOOK_ID"
request 404 GET "/books/$BOOK_ID"
echo 'RESULTADO: 7/7 respuestas correctas'
