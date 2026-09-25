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
| Ubidots: simulador Python con requests | Verificado en nube | `evidencias/ubidots/python-envio-real.txt`; cinco envíos |
| Ubidots: dos variables adicionales | Verificado | `luminosity` y `pressure` recibidas y visibles |
| Ubidots: recepción desde Python | Verificado | 25 valores aceptados; HTTP 200 y códigos internos 201 |
| Ubidots: actualización con curl | Verificado | `evidencias/ubidots/curl-envio-real.json` |
| Ubidots: actualización con Postman | Verificado mediante Newman | 12 aserciones; envío y consulta de las cinco variables |
| Ubidots: gauge, mapa y barras | Verificado | Capturas 07 y 08 del dashboard real |
| Ubidots: widgets de las dos nuevas variables | Verificado | Indicador de luminosidad y línea de presión |
| Ubidots: actualización visible en tiempo real | Verificado | 34→24 °C, 78→65 %, 820→550 lux y 754→750 hPa |
| Ubidots: evento y envío de correo | Verificado | `evento-configuracion.json`; `evento-logs.json`, éxito a las 21:08:03 |
| Ubidots: correo recibido | Verificado en captura aportada por Natalia | Captura 11: Notifications Ubidots, Recibidos, 9:08 p. m.; `correo-recepcion.json` documenta su procedencia |

## Alcance de las capturas

Las capturas muestran resultados reales en el navegador o registros de ejecuciones realizadas. Un panel local de evidencias es una presentación de los registros; no es un dashboard de Ubidots. Las capturas no sustituyen los archivos JSON, XML y texto originales incluidos.

## Entrega académica

El repositorio organiza el trabajo y permite su revisión por el profesor. Publicarlo no equivale a enviarlo por CampusDigital. No se ha realizado una entrega en el portal del curso desde esta tarea.
