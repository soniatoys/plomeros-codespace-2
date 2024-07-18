# Minecraft Server Project

Este proyecto automatiza la configuración y ejecución de un servidor de Minecraft. Código extraido del proyecto de [LUCAST](https://github.com/Luc4st1574/MSP_MINECRAFT-SERVER-PROJECT) y adaptado a Python puro.

## Configuración obligatoria

Configura tu servidor editando las siguientes variables según tus necesidades:

- `version`: Versión de Minecraft, ej. `1.18.2`.
- `server_type`: Tipo de servidor (`paper`, `forge`, `fabric`, `vanilla`, etc.).
- `memory_allocation`: Asignación de memoria, ej. `-Xms10G -Xmx10G`.
- `server_flags`: Argumentos JVM adicionales para optimizar rendimiento.
- `tunnel_service`: Servicio de túnel para acceso externo (`ngrok` o `playit`).
- `authtoken`: Token de autenticación para `ngrok`.
- `region`: Region de seleccion para `ngrok`.

## Instrucciones de Uso

1. Crea un codespace de Jupyter, de las carpetas con un punto al comienzo, borrar todas y solo dejar .devcontainer.
2. Pasar el la script y el .env al codespace.
2. Configurar las variables mencionadas en la script.
3. Ejecutar el script para instalar y configurar el servidor.

## Más detalles

Para más detalles, suscribete al canal de [LUCAST](https://www.youtube.com/@lucast5740) y revisa sus últimos videos.
