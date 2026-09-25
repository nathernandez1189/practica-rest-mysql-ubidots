#!/usr/bin/env bash
set -euo pipefail
: "${UBIDOTS_TOKEN:?Configura UBIDOTS_TOKEN de forma local}"
DEVICE="${UBIDOTS_DEVICE:-equipo-rest}"
[[ "$DEVICE" =~ ^[a-z0-9][a-z0-9_-]*$ ]] || exit 1
# El token se entrega por stdin, no en argumentos visibles ni en la URL.
printf 'header = "X-Auth-Token: %s"\n' "$UBIDOTS_TOKEN" | curl --config - \
 --fail-with-body --silent --show-error --max-time 20 \
 -H 'Content-Type: application/json' -X POST \
 --data '{"temperature":24,"humidity":65,"luminosity":550,"pressure":750,"position":{"value":1,"context":{"lat":4.711,"lng":-74.0721}}}' \
 "https://industrial.api.ubidots.com/api/v1.6/devices/$DEVICE/"
