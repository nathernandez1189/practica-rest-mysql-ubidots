# Práctica REST, MySQL e IoT

**Natalia Hernández Piedrahita · Miguel Ángel Diuza · Juan Ospina Tenorio**
Computación en la Nube · Especialización · 24 de septiembre de 2026

[![Pruebas REST e IoT](https://github.com/nathernandez1189/practica-rest-mysql-ubidots/actions/workflows/pruebas.yml/badge.svg)](https://github.com/nathernandez1189/practica-rest-mysql-ubidots/actions/workflows/pruebas.yml)

Implementación y evidencias de las guías **Práctica REST** y **Práctica REST + MySQL**. Incluye el desafío opcional en JavaScript.

> **Estado de entrega:** APIs y persistencia verificadas en Ubuntu. Ubidots STEM recibió las cinco variables desde Python, curl y Postman/Newman; el tablero y la actualización automática están comprobados. El evento `temperature > 30` envió la alerta y **su recepción está confirmada mediante la captura aportada por Natalia**. Los requisitos técnicos y sus evidencias están completos.

## Empezar por aquí

- [Informe de resultados en PDF](docs/Informe-Practica-REST-MySQL-IoT.pdf)
- [Matriz de requisitos y evidencias](docs/MATRIZ_REQUISITOS.md)
- [Cómo reproducir la práctica](docs/REPRODUCIR.md)
- [Guía de sustentación para los tres integrantes](docs/GUIA_SUSTENTACION.md)
- [Ubidots: resultados y reproducción](docs/UBIDOTS.md)
- [Fuentes y adaptaciones del material docente](docs/REFERENCIAS.md)

## Qué contiene

| Componente | Archivo | Almacenamiento | Puerto |
|---|---|---|---:|
| API Flask en memoria | `apirest.py` | Memoria del proceso | 5000 |
| API Flask + MySQL | `apirest_mysql.py` | MySQL 8.0 | 5001 |
| Desafío en JavaScript | `bonus-node/server.js` | La misma base MySQL | 5002 |
| Simulador IoT | `testUbidots.py` | Envío a Ubidots con token local | HTTPS |

```mermaid
flowchart LR
  C[curl / Postman / pruebas HTTP] --> M[Flask - memoria :5000]
  C --> P[Flask - MySQL :5001]
  C --> J[JavaScript :5002]
  P --> D[(MySQL - rest_equipo)]
  J --> D
  S[Simulador Python - 5 variables] --> U[Ubidots STEM - 5 widgets]
  U --> E[Evento temperature mayor de 30]
  E --> A[Correo enviado y recibido - evidencia confirmada]
```

## Resultados verificados

Los grupos siguientes contienen comprobaciones complementarias y parcialmente solapadas; no se suman como requisitos independientes.

| Prueba | Resultado | Evidencia |
|---|---:|---|
| Pruebas Python: API, errores y contrato IoT | 35 aprobadas | [pytest.txt](evidencias/pytest.txt) |
| HTTP real: memoria, MySQL y JavaScript | 42 respuestas correctas, 14 por API | [http-real.json](evidencias/http-real.json) |
| Colección Postman ejecutada por Newman | 60 aserciones correctas, 20 por API | [memoria](evidencias/newman-5000.txt), [MySQL](evidencias/newman-5001.txt), [JavaScript](evidencias/newman-5002.txt) |
| curl: CRUD y validaciones | 21 respuestas correctas, 7 por API | [memoria](evidencias/curl-memoria.txt), [MySQL](evidencias/curl-mysql.txt), [JavaScript](evidencias/curl-javascript.txt) |
| Consulta directa MySQL | Tabla, columnas y registros visibles | [mysql-tabla.txt](evidencias/mysql-tabla.txt) |
| Apagado y encendido de Ubuntu | Ver registro antes/después | [persistencia.json](evidencias/persistencia.json) |
| Ubidots desde Python | 5 envíos de 5 variables recibidos | [envío real](evidencias/ubidots/python-envio-real.txt) |
| Ubidots desde curl | 5 variables recibidas | [respuesta real](evidencias/ubidots/curl-envio-real.json) |
| Ubidots desde Postman/Newman | 12 aserciones correctas: envío y lectura | [resultado](evidencias/ubidots/postman-newman.txt) |
| Dashboard Ubidots | 5 widgets y actualización automática | [alerta 34 °C](evidencias/pantallazos/07-ubidots-alerta-34.png), [recuperación 24 °C](evidencias/pantallazos/08-ubidots-recuperacion-24.png) |
| Correo recibido | Verificado en la captura aportada por Natalia | [captura 11](evidencias/pantallazos/11-ubidots-correo-recibido.png) |
| Evento de temperatura | Correo enviado; ejecución exitosa | [registro oficial](evidencias/ubidots/evento-logs.json), [captura](evidencias/pantallazos/09-ubidots-evento-enviado.png) |

**Precisión sobre Postman:** se ejecutó la colección con Newman, su ejecutor oficial. No se presentan esos resultados como pruebas mediante la interfaz gráfica de Postman.

**Precisión sobre IoT:** las pruebas unitarias usan dobles y `--dry-run` genera datos locales. Las pruebas reales adicionales están en `evidencias/ubidots/`; consultan el servicio y comprueban los valores guardados. El registro `Sent` acredita el envío; la [captura original aportada por Natalia](evidencias/pantallazos/11-ubidots-correo-recibido.png) confirma la recepción a las 9:08 p. m. Se documenta su [procedencia](evidencias/ubidots/correo-recepcion.json) sin modificar la imagen.

![Tablero real de Ubidots](evidencias/pantallazos/08-ubidots-recuperacion-24.png)

## Uso rápido en el entorno probado

En el Mac:

```bash
cd ~/prueba
vagrant up servidorUbuntu --no-provision
vagrant ssh servidorUbuntu
```

En Ubuntu:

```bash
cd /home/vagrant/practica-rest-equipo
.venv/bin/pytest -v
bash scripts/curl_crud.sh http://127.0.0.1:5001
python3 scripts/verify_http.py
bash scripts/mysql.sh -e 'SHOW TABLES; SELECT * FROM books;'
```

Desde el Mac, `http://192.168.100.3:5001/books` permite consultar MySQL por REST. Las APIs funcionan en la red local del laboratorio; el repositorio público aloja código y evidencias, no el servidor de las APIs.

## Contrato HTTP

| Método y ruta | Acción | Respuesta normal |
|---|---|---|
| `GET /books` | Lista libros | 200 |
| `GET /books/<id>` | Consulta uno | 200 / 404 |
| `POST /books` | Crea un libro con `title` | 201 / 400 |
| `PUT /books/<id>` | Actualiza campos enviados | 200 / 400 / 404 |
| `DELETE /books/<id>` | Elimina el libro | 200 / 404 |
| `GET /health` | Comprueba servicio y almacenamiento | 200 / 503 |

Los campos `title`, `description` y `author` son textos de hasta 255 caracteres. El título no puede quedar vacío. No se aceptan campos adicionales. Los errores MySQL se exponen como 503 sin revelar detalles internos.

## ¿Qué ocurre con los datos al apagar la máquina?

La API en memoria pierde las modificaciones cuando termina su proceso. MySQL conserva las transacciones confirmadas en el disco de la VM y recupera los registros al encender. Esto no protege frente a eliminar la máquina, borrar el disco o corromperlo: se incluye una copia de seguridad de la base de práctica.

## Reproducibilidad y cuidado de datos

- Dependencias principales fijadas y versiones ejecutadas en `evidencias/dependencias.txt`.
- Colecciones Postman y resultados JSON/JUnit para repetir y auditar.
- Pruebas automáticas en GitHub Actions, incluyendo MySQL real como servicio de integración.
- Contraseñas y token solo en configuración local; `.env` y `.venv` están excluidos.
- La base del ejercicio es `rest_equipo`. Los scripts no eliminan bases ni proyectos existentes.
- El `Vagrantfile` incluido crea la alternativa `servidorRest`; las evidencias corresponden a `servidorUbuntu` ya existente. Consulte las [adaptaciones](docs/REFERENCIAS.md).
