# Índice de evidencias

Registros obtenidos el 24 de septiembre de 2026 (America/Bogota; algunas marcas están en UTC del día 25).

| Archivo | Qué demuestra |
|---|---|
| `entorno.txt` | Ubuntu, arquitectura, Python, Node, MySQL y servicios activos |
| `pytest.txt`, `pytest.xml` | 35 pruebas Python aprobadas; parte IoT con dobles de prueba |
| `http-real.json` | 42 respuestas correctas contra tres servicios HTTP reales |
| `curl-*.txt` | CRUD y errores con curl: 7 respuestas por implementación |
| `newman-*.txt`, `.json`, `.xml` | Colecciones Postman ejecutadas con Newman: 20 aserciones por implementación |
| `mysql-tabla.txt` | Motor, tabla, campos y registros iniciales |
| `persistencia.json` | Registros antes y después del apagado: memoria 404, MySQL 200 |
| `vm-apagada.txt`, `vm-encendido.txt` | Ciclo real de apagado/encendido de servidorUbuntu |
| `mysql-despues-encendido.txt` | Libros guardados tras el encendido |
| `respaldo-rest_equipo.sql` | Copia de seguridad de los libros del laboratorio |
| `dependencias.txt` | Versiones instaladas durante las pruebas |
| `ubidots-simulacion-local.txt` | Payload de cinco variables; **sin envío a Ubidots** |
| `SHA256SUMS.txt` | Huellas de los archivos de evidencia (excluye su propia huella) |

## Pantallazos

- `01-resumen.png`: captura de un panel local que resume los registros auditables.
- `02-persistencia.png`: comparación antes/después y estado de apagado.
- `03-mysql.png`: registro de la consulta SQL en el panel local.
- `04-postman-newman.png`: resumen de la ejecución de la colección Postman con Newman.
- `05-curl.png`: registro de respuestas curl.
- `06-api-mysql-en-vivo.png`: **consulta directa al servidor REST activo** desde Chrome, después del encendido.

Las primeras cinco capturas son de un visor HTML generado desde los archivos reales de esta carpeta. La sexta corresponde directamente a la API. No son capturas de la plataforma Ubidots ni de la interfaz gráfica de Postman. No se fabricaron capturas de acciones no ejecutadas.
