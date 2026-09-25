#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
set -a
source .env
set +a
export MYSQL_PWD="$MYSQL_PASSWORD"
mysqldump --single-transaction --no-tablespaces --skip-add-locks \
  --host="$MYSQL_HOST" --port="${MYSQL_PORT:-3306}" --user="$MYSQL_USER" "$MYSQL_DB"
