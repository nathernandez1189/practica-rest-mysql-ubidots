# Ubidots: conexión y verificación pendiente de cuenta

**Estado de esta entrega:** el simulador y su contrato HTTP tienen pruebas locales. La recepción en Ubidots, el dashboard y el correo no se pueden certificar hasta configurar una cuenta real. Ningún resultado de simulación local demuestra recepción en la nube.

## 1. Cuenta y token

Crear una cuenta educativa en https://ubidots.com/stem, confirmar el correo e iniciar sesión. Guardar el token únicamente en el entorno local. No subirlo al repositorio ni incluirlo en capturas. En bash:

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

En Postman importar `postman/Ubidots.postman_collection.json`; crear la variable secreta local `ubidots_token` y establecer `device=equipo-rest`. No sincronizar ni exportar valores del token. Ejecutar el envío y revisar también los códigos internos por variable en la respuesta; un HTTP 200 por sí solo no basta para descartar fallos parciales.

## 4. Dashboard

Crear un dashboard llamado **Práctica REST - Natalia, Miguel y Juan Ospina**. Agregar los cinco widgets de la tabla y seleccionar el dispositivo `equipo-rest`. Ejecutar cinco envíos; observar que cambian los valores y las marcas de tiempo. Guardar una captura completa sin mostrar tokens.

## 5. Evento y correo

Crear un evento para `temperature > 30` con acción de correo hacia la cuenta indicada por el integrante. Activarlo solo durante la prueba. Enviar primero temperatura 24 y después 34 para demostrar el cruce de umbral. Verificar el registro de ejecución y el correo recibido, y guardar capturas sin datos privados innecesarios. Acordar previamente con el titular el destinatario y el envío de este correo de prueba. Desactivar el evento al terminar si no se desea recibir más avisos.

## 6. Evidencias para cerrar esta parte

- Respuesta real del envío Python con éxito por variable.
- Respuesta real del envío curl y Postman.
- Dispositivo con cinco variables y marcas de tiempo.
- Dashboard con gauge, mapa, barras y dos widgets adicionales.
- Configuración del evento y correo recibido.

## Fuentes

- [Simulación oficial en Python](https://help.ubidots.com/en/articles/569964-simulate-data-in-ubidots-using-python)
- [Cuenta educativa STEM](https://ubidots.com/stem)
- [Límites actuales de STEM](https://help.ubidots.com/en/articles/639806-plans-billing-what-is-the-difference-between-ubidots-and-ubidots-stem)

Consultadas el 24 de septiembre de 2026. La cuenta STEM permite la práctica con un dispositivo y cinco variables, dentro de sus límites. La disponibilidad y los límites pueden cambiar.
