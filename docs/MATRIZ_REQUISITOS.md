# Matriz de cumplimiento y evidencias

Fecha de ejecución: 24 de septiembre de 2026, zona America/Bogota. Los registros de herramientas pueden usar UTC del 25 de septiembre.

| Guía / requisito | Estado | Evidencia o límite |
|---|---|---|
| REST: Python Flask sobre Ubuntu/Vagrant | Verificado | `evidencias/entorno.txt`; VM existente `servidorUbuntu` |
| REST: CRUD de libros en memoria | Verificado | Código, pruebas HTTP y curl, puerto 5000 |
| REST: pruebas curl | Verificado | `evidencias/curl-memoria.txt` |
| REST: pruebas Postman | Verificado mediante Newman | Colección de Postman; `newman-5000.*`. Interfaz gráfica no ejecutada |
| MySQL: tabla y registros | Verificado | `evidencias/mysql-tabla.txt` |
| MySQL: API Flask persistente | Verificado | `apirest_mysql.py`; pruebas HTTP, puerto 5001 |
| MySQL: pruebas curl | Verificado | `evidencias/curl-mysql.txt` |
| MySQL: pruebas Postman | Verificado mediante Newman | `evidencias/newman-5001.*`. Interfaz gráfica no ejecutada |
| MySQL: explicar efecto de apagar VM | Prueba de apagado/encendido registrada | `vm-apagada.txt`, `vm-encendido.txt`, `persistencia.json` |
| MySQL: desafío en otro lenguaje | Verificado | JavaScript + MySQL, puerto 5002; HTTP, curl y Newman |
| Ubidots: simulador Python con requests | Implementado; pruebas locales aprobadas | `testUbidots.py`, `tests/test_ubidots.py` |
| Ubidots: dos variables adicionales | Implementado y generado localmente | `luminosity`, `pressure`; cinco variables en el payload |
| Ubidots: recepción desde Python | Pendiente de cuenta/token | No se hicieron envíos reales a una cuenta |
| Ubidots: actualización con curl | Script preparado; pendiente en nube | `scripts/ubidots_curl.sh` |
| Ubidots: actualización con Postman | Colección preparada; pendiente en nube | `postman/Ubidots.postman_collection.json` |
| Ubidots: gauge de humedad, mapa y barras de temperatura | Pendiente de cuenta | Procedimiento exacto en `docs/UBIDOTS.md` |
| Ubidots: widgets de las dos nuevas variables | Pendiente de cuenta | Indicador de luminosidad y línea de presión previstos |
| Ubidots: actualización visible en tiempo real | Pendiente de cuenta | No se certifica con una simulación local |
| Ubidots: evento y correo recibido | Pendiente de cuenta y destinatario autorizado | No se creó ni se envió una alerta real |

## Alcance de las capturas

Las capturas muestran resultados reales en el navegador o registros de ejecuciones realizadas. Un panel local de evidencias es una presentación de los registros; no es un dashboard de Ubidots. Las capturas no sustituyen los archivos JSON, XML y texto originales incluidos.

## Entrega académica

El repositorio organiza el trabajo y permite su revisión por el profesor. Publicarlo no equivale a enviarlo por CampusDigital. No se ha realizado una entrega en el portal del curso desde esta tarea.
