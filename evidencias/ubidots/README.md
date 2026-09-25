# Ejecución real de Ubidots STEM

Pruebas del 24 de septiembre de 2026 (America/Bogota; los JSON pueden usar UTC del 25).

| Evidencia | Qué demuestra |
|---|---|
| `python-envio-real.txt` | Cinco muestras, cada una con cinco variables; respuesta HTTP 200 y códigos internos 201 |
| `curl-envio-real.json` | Recepción real de las cinco variables enviadas con curl |
| `postman-newman.txt` y `.json` | Colección Postman ejecutada por Newman: 12 aserciones correctas, sin fallos |
| `lectura-valores-reales.json` | Consulta independiente de los últimos valores guardados |
| `normal-24.json` | Base del evento: temperatura 24 °C |
| `alerta-34.json` | Cruce del umbral con temperatura 34 °C, humedad 78 %, luminosidad 820 lux, presión 754 hPa |
| `recuperacion-24.json` | Regreso a 24 °C, 65 %, 550 lux y 750 hPa; lectura confirmada |
| `evento-configuracion.json` | Condición `temperature > 30`, acción email y evento activo sin repetición periódica |
| `evento-logs.json` | Registro oficial `action_emails`, `successful_execution: true`, a las 21:08:03 de Colombia |
| `eventos-registro.txt` | Texto de accesibilidad de la pantalla de registros, con estado `Sent` |

El token y el correo se ocultan en los archivos publicados. Las capturas 07–10 de `../pantallazos/` corresponden a la aplicación real de Ubidots. En la captura 09 se ocultó la columna Message desde los controles de la aplicación para evitar publicar la dirección de correo; se conserva el estado Sent, el evento y la hora. No se alteraron los píxeles de las capturas.

Los valores y las coordenadas son simulados con fines académicos; el envío HTTPS y su recepción en Ubidots son reales. La captura 08 registra la actualización automática posterior a la muestra de recuperación.

**Límite de la evidencia:** `Sent` y `successful_execution` confirman el envío desde Ubidots, pero no prueban la recepción en la bandeja institucional. Ese último paso permanece pendiente de inspección del correo. El evento queda activo, la temperatura termina en 24 °C y no queda un simulador enviando datos continuamente.

La configuración de texto del correo se corrigió después de la primera prueba para conservar nombres legibles. Los registros originales reflejan el texto usado en cada momento; no se reescribió la evidencia histórica.

La captura 01-resumen.png se conserva como registro histórico de la primera fase, anterior a conectar la cuenta de Ubidots. Su aviso de pendiente ya fue resuelto para recepción de datos, dashboard y envío del correo. El estado vigente está en la matriz de requisitos y en este informe.
