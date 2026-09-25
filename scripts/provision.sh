#!/usr/bin/env bash
set -euo pipefail
LAB_DIR="${1:-/home/vagrant/practica-rest-equipo}"
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server python3-venv python3-pip curl
if ! command -v node >/dev/null || ! command -v npm >/dev/null; then
  DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs npm
fi
systemctl enable --now mysql
# Una instalación previa puede requerir MYSQL_ADMIN_PASSWORD; nunca cambia la cuenta root.
mysql_admin() {
  if [ -n "${MYSQL_ADMIN_PASSWORD:-}" ]; then
    MYSQL_PWD="$MYSQL_ADMIN_PASSWORD" mysql --protocol=socket --host=localhost -u root "$@"
  else
    mysql --protocol=socket --host=localhost -u root "$@"
  fi
}
if [ ! -f "$LAB_DIR/.env" ]; then
  LAB_PASSWORD=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
  umask 077
  printf 'MYSQL_HOST=127.0.0.1\nMYSQL_PORT=3306\nMYSQL_DB=rest_equipo\nMYSQL_USER=rest_equipo\nMYSQL_PASSWORD=%s\n' "$LAB_PASSWORD" > "$LAB_DIR/.env"
fi
set -a
source "$LAB_DIR/.env"
set +a
# Contraseña hex generada localmente; solo se crea un usuario propio de la práctica.
[[ "$MYSQL_PASSWORD" =~ ^[a-f0-9]{48}$ ]] || { echo 'Se requiere la contraseña local generada por este script'; exit 1; }
mysql_admin <<SQL
CREATE DATABASE IF NOT EXISTS rest_equipo CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'rest_equipo'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT SELECT,INSERT,UPDATE,DELETE ON rest_equipo.* TO 'rest_equipo'@'localhost';
SQL
mysql_admin rest_equipo < "$LAB_DIR/init.sql"
python3 -m venv "$LAB_DIR/.venv"
"$LAB_DIR/.venv/bin/pip" install -r "$LAB_DIR/requirements.txt"
cd "$LAB_DIR/bonus-node"
npm ci --omit=dev --no-audit --no-fund
for entry in 'memoria:apirest:5000' 'mysql:apirest_mysql:5001'; do
  IFS=: read -r LABEL MODULE PORT <<< "$entry"
  cat > "/etc/systemd/system/rest-equipo-$LABEL.service" <<UNIT
[Unit]
Description=Practica REST equipo - $LABEL
After=network.target mysql.service
[Service]
User=vagrant
WorkingDirectory=$LAB_DIR
EnvironmentFile=$LAB_DIR/.env
ExecStart=$LAB_DIR/.venv/bin/gunicorn --workers 1 --threads 4 --bind 0.0.0.0:$PORT $MODULE:app
Restart=on-failure
[Install]
WantedBy=multi-user.target
UNIT
done
cat > /etc/systemd/system/rest-equipo-node.service <<UNIT
[Unit]
Description=Practica REST equipo - desafio JavaScript MySQL
After=network.target mysql.service
[Service]
User=vagrant
WorkingDirectory=$LAB_DIR/bonus-node
EnvironmentFile=$LAB_DIR/.env
ExecStart=/usr/bin/node server.js
Restart=on-failure
[Install]
WantedBy=multi-user.target
UNIT
chown -R vagrant:vagrant "$LAB_DIR"
systemctl daemon-reload
systemctl enable --now rest-equipo-memoria rest-equipo-mysql rest-equipo-node
