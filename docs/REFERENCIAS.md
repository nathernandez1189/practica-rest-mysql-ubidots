# Referencias y adaptación

## Guías suministradas

- **Práctica REST + MySQL**, archivo `2023-03 Practica REST_MYSQL (1).pdf`, 2 páginas. Requisitos: Vagrant/Ubuntu, Python Flask, MySQL, inspección de tabla, curl, Postman y explicación de persistencia. Incluye desafío opcional en otro lenguaje.
- **Práctica REST**, archivo `2024-03 Practica REST_AI (1).pdf`, 7 páginas. Requisitos: API en memoria y envío a Ubidots; dos variables adicionales, cinco widgets y evento por correo.

No se redistribuyen los PDFs docentes dentro del repositorio público.

## Código de referencia del docente

| Repositorio | Revisión consultada |
|---|---|
| https://github.com/omondragon/APIRestFlask | `66f1591ff9f3586f993492b93c522ceb6fe4785d` |
| https://github.com/omondragon/APIRestFlaskMySQLUbuntu | `7e047120d3bbf3a24f773414e2e3d4671e77c231` |
| https://github.com/omondragon/UbidotsClient | `a59e27d6516fdedbea6cc83cbdeeac755e7d634f` |

Se conserva el recurso `/books` y los campos de la guía. La implementación entregada agrega validación, ids robustos, configuración local de secretos, consultas parametrizadas, pruebas y documentación. El cliente MySQL es PyMySQL para evitar dependencias de compilación en ARM; el motor ejecutado es MySQL, no SQLite ni una simulación.

## Diferencias del entorno ejecutado

La referencia crea `servidorRest` en `192.168.60.3`. Esta ejecución reutiliza la VM **servidorUbuntu**, Ubuntu 22.04 ARM64, en `192.168.100.3`, sin reemplazar su configuración ni los otros proyectos. Los archivos se instalan en `/home/vagrant/practica-rest-equipo` y usan una base y usuario exclusivos `rest_equipo`.

El `Vagrantfile` del repositorio describe la alternativa independiente `servidorRest` para reproducir la práctica. Ese archivo se valida como configuración, pero no se atribuye a una VM nueva que no fue creada en esta ejecución.

Para servir Flask se usa Gunicorn con un proceso y cuatro hilos. Las rutas y funciones son Flask; los servicios de Ubuntu facilitan que vuelvan a arrancar después del encendido.

## Documentación técnica

- [Flask](https://flask.palletsprojects.com/)
- [PyMySQL](https://pymysql.readthedocs.io/)
- [Newman, ejecutor de Postman](https://learning.postman.com/docs/collections/using-newman-cli/command-line-integration-with-newman/)
- [Ubidots en Python](https://help.ubidots.com/en/articles/569964-simulate-data-in-ubidots-using-python)
