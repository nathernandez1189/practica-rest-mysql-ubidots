# Guía de sustentación del equipo

**Integrantes:** Natalia, Miguel y Juan Ospina.

El reparto siguiente es una propuesta para presentar el trabajo; no acredita quién escribió cada archivo.

## Natalia: API REST y pruebas (3 minutos)

1. Explicar que REST opera sobre recursos mediante HTTP; el recurso es `books`.
2. Mostrar `GET /books`, `POST /books`, `PUT /books/<id>` y `DELETE /books/<id>`.
3. Mostrar la colección de Postman y sus resultados de Newman.
4. Explicar los estados 200, 201, 400 y 404; mostrar un título vacío rechazado.

## Miguel: MySQL y persistencia (3 minutos)

1. Mostrar la tabla `books`, su clave primaria y sus columnas.
2. Explicar que las consultas parametrizadas tratan los valores como datos.
3. Mostrar `evidencias/persistencia.json`: antes y después del apagado de Ubuntu.
4. Contrastar memoria volátil con MySQL sobre disco. Apagar no elimina la base; destruir la VM o borrar el disco sí puede hacerlo.

## Juan Ospina: IoT y desafío (3 minutos)

1. Explicar el simulador y sus cinco variables, incluyendo luminosidad y presión.
2. Distinguir generación local de envío y recepción reales en Ubidots.
3. Mostrar las capturas 07 y 08 del dashboard real, el registro `Sent` del evento y la captura 11 del correo recibido, aportada por Natalia. Relacionar la hora 9:08 p. m. del mensaje con las 21:08:03 del registro.
4. Mostrar la implementación JavaScript y que responde al mismo contrato, usando la misma base de MySQL.

## Preguntas probables

**¿Por qué falla un id inexistente?** El servidor responde 404 porque el recurso no existe.

**¿Por qué el POST devuelve 201?** Indica creación; `Location` apunta al recurso creado.

**¿Qué pasa si elimino todos los libros en memoria?** El contador de ids continúa; no depende del último elemento de una lista vacía.

**¿Qué distingue PUT aquí?** Se sigue la guía: actualiza los campos suministrados y conserva los demás. Es una actualización parcial por compatibilidad con el ejercicio; una API nueva podría reservar PATCH para esa semántica.

**¿Qué pasa si MySQL no responde?** La API persistente devuelve 503 sin revelar credenciales.

**¿Por qué no usamos varios procesos para memoria?** Cada proceso tendría una copia distinta. La demostración usa un proceso con bloqueo para las operaciones compartidas.

**¿Hay inteligencia artificial entrenada?** No. Aunque el archivo se llama REST_AI, su contenido exige REST e IoT; no pide entrenar un modelo.

**¿Postman fue probado en su interfaz gráfica?** La colección se ejecutó con Newman, el ejecutor oficial de Postman. Consultar `evidencias/` para resultados; no atribuirlos a la interfaz gráfica.

**¿Esto está listo para exponerlo a Internet?** Es una práctica en red local sin autenticación de usuarios. No es un despliegue de producción.
