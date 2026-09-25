# Ubidots: ejecución real y reproducción

**Estado verificado:** cuenta STEM operativa, dispositivo `equipo-rest`, cinco variables recibidas desde Python/curl/Postman y cinco widgets funcionando. Newman completó 12 aserciones sin fallos. El evento envió el correo y registró éxito a las 21:08:03 del 24 de septiembre de 2026 (Colombia). **La recepción está confirmada en la captura aportada por Natalia:** muestra Notifications Ubidots, la etiqueta Recibidos y las 9:08 p. m., coincidiendo con el registro del evento.

- [Evidencias originales y alcance](../evidencias/ubidots/README.md).
- [Dashboard del equipo](https://stem.ubidots.com/app/dashboards/6ab5d3c8d1003b3265a230eb), requiere iniciar sesión con la cuenta del equipo. El profesor puede revisar las capturas públicas sin acceder a esa cuenta.
- [Dispositivo](https://stem.ubidots.com/app/devices/6ab5d3a6e011e9a497bbcb99).

Los pasos siguientes permiten reproducir lo realizado con un token propio.

## 1. Cuenta y token

Para reproducir desde otra cuenta, registrarse en https://ubidots.com/stem, confirmar el correo e iniciar sesión. Guardar el token únicamente en el entorno local. No subirlo al repositorio ni incluirlo en capturas. En bash:

```bash
read -rsp 'Token de Ubidots: ' UBIDOTS_TOKEN; echo
export UBIDOTS_TOKEN
export UBIDOTS_DEVICE=equipo-rest
export UBIDOTS_URL=https://industrial.api.ubidots.com
```

## 2. Enviar desde Python

```bash
source .venv/bin/activate
python testUbidots.py --dry-run
python testUbidots.py --count 5 --interval 15
```

El primer comando solo genera datos locales. El segundo envía 25 valores (cinco variables por cinco envíos). El proceso es finito para no agotar los límites de la cuenta.

| Variable | Unidad | Representación |
|---|---|---|
| temperature | °C | Barras |
| humidity | % | Gauge / indicador, escala 0–100 |
| position | latitud y longitud simuladas | Mapa |
| luminosity | lux | Indicador numérico |
| pressure | hPa | Gráfica de línea |

Las coordenadas son ficticias, alrededor de Bogotá; no corresponden a la ubicación de los integrantes. Luminosidad y presión son las dos variables adicionales elegidas.

## 3. curl y Postman

```bash
bash scripts/ubidots_curl.sh
```

En Postman importar `postman/Ubidots.postman_collection.json`; crear la variable secreta local `ubidots_token` y establecer `device=equipo-rest`. No sincronizar ni exportar valores del token. Ejecutar las dos peticiones de la colección: POST de cinco variables y GET para comprobar los valores guardados. Las 12 aserciones revisan HTTP, los códigos internos 201 y la lectura de datos y coordenadas; HTTP 200 por sí solo no descarta fallos parciales. La ejecución real con Newman usó un entorno privado, excluido del repositorio, y validación TLS activa.

## 4. Dashboard

Se creó el dashboard **Práctica REST · Natalia, Miguel y Juan Ospina** con los cinco widgets de la tabla. Humedad usa escala 0–100. La posición ficticia se recibe en `position.context.lat/lng` y aparece sobre Bogotá. Se amplió la gráfica de presión y se seleccionó la última hora para apreciar los cambios.

Las capturas [07](../evidencias/pantallazos/07-ubidots-alerta-34.png) y [08](../evidencias/pantallazos/08-ubidots-recuperacion-24.png) registran temperatura 34→24, humedad 78→65, luminosidad 820→550 y presión 754→750. La segunda muestra se reflejó automáticamente en el tablero. Se restauró el valor normal y se detuvieron los envíos al concluir.

## 5. Evento y correo

Evento guardado: **Practica REST - temperatura > 30 C**, condición `temperature > 30`, demora cero, ventana diaria y zona `America/Bogota`. La acción email usa el correo institucional autorizado por Natalia. La repetición periódica está desactivada y el evento permanece activo. La dirección y el token se ocultan en el repositorio.

Prueba controlada reproducible (el segundo comando puede enviar un correo al destinatario configurado):

```bash
python scripts/verify_ubidots.py normal --output evidencias/ubidots/normal-24.json
python scripts/verify_ubidots.py alerta --output evidencias/ubidots/alerta-34.json
python scripts/verify_ubidots.py recuperacion --output evidencias/ubidots/recuperacion-24.json
```

Esperar a observar el tablero entre etapas. Cada comando valida los códigos internos de recepción y consulta los últimos valores hasta comprobar que coinciden. El flujo fue 24→34→24 °C. En Monitoring → Logs apareció **Sent**; el registro oficial contiene `successful_execution: true`. El asunto vigente es **Practica REST - Alerta de temperatura del equipo**. La primera prueba se envió antes de una corrección ortográfica del asunto, como consta en el registro histórico.

El último requisito quedó cerrado con la [captura 11 aportada por Natalia](../evidencias/pantallazos/11-ubidots-correo-recibido.png). Muestra la alerta en Recibidos a las 9:08 p. m., el dispositivo `equipo-rest` y el umbral de 30 °C. Se conserva el archivo original sin editar; la dirección del destinatario no está desplegada. Esta verificación se realizó sobre la captura compartida, sin acceder directamente al buzón. La procedencia y huella del archivo están en `evidencias/ubidots/correo-recepcion.json`.

## 6. Evidencias guardadas

- Respuesta real del envío Python con éxito por variable.
- Respuesta real del envío curl y Postman.
- Dispositivo con cinco variables y marcas de tiempo.
- Dashboard con gauge, mapa, barras y dos widgets adicionales.
- Configuración del evento, registro de correo enviado y captura original del mensaje recibido.

## Fuentes

- [Simulación oficial en Python](https://help.ubidots.com/en/articles/569964-simulate-data-in-ubidots-using-python)
- [Consultar los últimos valores](https://docs.ubidots.com/reference/get-device-last-values)
- [Consultar un evento](https://docs.ubidots.com/reference/get-event)
- [Registros de un evento](https://docs.ubidots.com/reference/get-event-logs)
- [Cuenta educativa STEM](https://ubidots.com/stem)
- [Límites actuales de STEM](https://help.ubidots.com/en/articles/639806-plans-billing-what-is-the-difference-between-ubidots-and-ubidots-stem)

Consultadas el 24 de septiembre de 2026. La cuenta STEM permite la práctica con un dispositivo y cinco variables, dentro de sus límites. La disponibilidad y los límites pueden cambiar.
