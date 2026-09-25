# Reproducir la práctica

## Opción A: máquina independiente

Requisitos en el computador: Git, Vagrant, proveedor VirtualBox y espacio suficiente para una VM Ubuntu. En Apple Silicon se necesita una caja ARM compatible con el proveedor. La ejecución documentada se hizo en Ubuntu 22.04 ARM64 ya existente; una nueva VM puede requerir ajustes del proveedor.

```bash
git clone https://github.com/nathernandez1189/practica-rest-mysql-ubidots.git
cd practica-rest-mysql-ubidots
vagrant up servidorRest
vagrant ssh servidorRest
cd /home/vagrant/practica-rest-equipo
.venv/bin/pytest -v
python3 scripts/verify_http.py --host 127.0.0.1
```

En esta opción, desde el computador anfitrión usar `192.168.60.3`. El aprovisionamiento crea una contraseña aleatoria local en `.env`, una base `rest_equipo` y tres servicios; no publica MySQL fuera de la VM.

## Opción B: entorno en el que se obtuvieron las evidencias

En el Mac de la práctica:

```bash
cd ~/prueba
vagrant up servidorUbuntu --no-provision
vagrant ssh servidorUbuntu
cd /home/vagrant/practica-rest-equipo
.venv/bin/pytest -v
bash scripts/curl_crud.sh http://127.0.0.1:5000
bash scripts/curl_crud.sh http://127.0.0.1:5001
bash scripts/curl_crud.sh http://127.0.0.1:5002
python3 scripts/verify_http.py --host 127.0.0.1
bash scripts/mysql.sh -e 'SHOW TABLES; DESCRIBE books; SELECT * FROM books;'
```

Desde el Mac se accede a las APIs en `192.168.100.3`, puertos 5000 (memoria), 5001 (Python/MySQL) y 5002 (JavaScript/MySQL).

## Colección Postman

Importar `postman/REST-equipo.postman_collection.json`. Cambiar la variable `base_url` al servicio elegido. Ejecutar los ocho requests en orden o con Collection Runner. Solo se elimina el libro creado por la colección.

Ejecución automatizada equivalente:

```bash
npx --yes newman@6.2.1 run postman/REST-equipo.postman_collection.json \
  --env-var base_url=http://192.168.100.3:5001
```

Los resultados incluidos se obtuvieron con Newman, no mediante clics en la aplicación Postman.

## Comprobar persistencia con apagado

En el repositorio local, antes de apagar:

```bash
python3 scripts/test_persistence.py before --host 192.168.100.3
```

En otra terminal del Mac:

```bash
cd ~/prueba
vagrant halt servidorUbuntu
vagrant status servidorUbuntu
vagrant up servidorUbuntu --no-provision
```

Cuando estén activos los servicios, regresar al repositorio local:

```bash
python3 scripts/test_persistence.py after --host 192.168.100.3
```

El script espera que desaparezca el registro de memoria y que permanezcan idénticos los registros MySQL creados por Python y JavaScript. Los marcadores persistentes se conservan como evidencia. Cada repetición crea nuevos marcadores.

## Copia de seguridad y apagado

Dentro de Ubuntu:

```bash
bash scripts/backup.sh > respaldo-rest_equipo.sql
```

Guardar el archivo antes de destruir cualquier VM. Para detener el laboratorio sin borrar el disco:

```bash
cd ~/prueba
vagrant halt servidorUbuntu
```

No usar `vagrant destroy` si se necesita conservar la base. Los servicios y datos vuelven al encender la VM.

## Ubidots

Seguir [UBIDOTS.md](UBIDOTS.md). El token nunca va en el repositorio. La simulación `--dry-run` no equivale a completar la práctica en la nube.

## Regenerar los documentos

Los archivos de evidencia deben estar presentes, incluida la comprobación de persistencia completada.

```bash
pip install -r requirements-docs.txt
python scripts/generar_panel.py
python scripts/generar_informe.py
```

El PDF usa Arial si está disponible en macOS y Helvetica en otros sistemas. Las capturas se toman del navegador y se conservan como evidencia; los generadores no inventan pantallazos.
