# Sistema de Control de Dispositivos Inteligentes con Amazon Alexa

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

Este proyecto consiste en el desarrollo de una skill de Alexa para el control por voz de dispositivos inteligentes, incluyendo un videojuego en una Raspberry Pi, mejorando así la accesibilidad y promoviendo el desarrollo de software con Alexa.

## Índice

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Agradecimientos](#agradecimientos)Instala las dependencias:

sh
Copy code
pip install flask flask-ask pygame
Configura ngrok:

Regístrate en ngrok y descarga el binario.
Inicia ngrok:
sh
Copy code
ngrok http 5000
Configura la skill en Amazon Developer Console:

Crea una nueva skill en la consola de desarrolladores de Amazon Alexa.
Configura el endpoint de la skill usando la URL proporcionada por ngrok.
Uso
Ejecuta la aplicación:

sh
Copy code
python app.py
Inicia la skill en tu dispositivo Alexa y prueba los comandos de voz.

Ejemplo: "Alexa, abre juego de Raspberry Pi".
Arquitectura
El sistema utiliza una arquitectura cliente-servidor donde Alexa actúa como cliente enviando comandos de voz a un servidor Flask ejecutándose en la Raspberry Pi. La Raspberry Pi interpreta los comandos y controla el videojuego y otros dispositivos conectados.


Contribución
¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

Haz un fork del repositorio.
Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
Realiza los cambios y haz commit (git commit -m 'Añadir nueva funcionalidad').
Haz push a la rama (git push origin feature/nueva-funcionalidad).
Abre un Pull Request.
Licencia
Este proyecto está licenciado bajo la Licencia MIT.

Agradecimientos
Gracias a todos los que han contribuido a este proyecto, especialmente a Francisco Antonio Pujol López por su tutoría y a mi familia por su apoyo constante.

Enlace al Repositorio
TFG-SistemaControlDispositivosInteligentesAlexa

markdown
Copy code

### Notas adicionales:
1. **Imagen de Arquitectura:** El enlace `![Arquitectura](./images/arquitectura.png)` asume que existe una imagen llamada `arquitectura.png` en una carpeta llamada `images`. Si no existe, asegúrate de añadirla o ajusta el enlace según la ubicación real de la imagen.
2. **Archivo de Licencia:** El enlace `[Licencia MIT](LICENSE)` asume que tienes un archivo `LICENSE` en el directorio raíz de tu repositorio. Si no existe, puedes crear uno o ajustar el enlace a la ubicación correcta del archivo de licencia. 

Asegúrate de verificar que todos los enlaces y recursos estén correctamente configurados antes de subir el README.md a tu repositorio.






- [Enlace al Repositorio](#enlace-al-repositorio)

## Descripción

Este proyecto integra el asistente de voz Amazon Alexa con una Raspberry Pi para controlar dispositivos inteligentes a través de comandos de voz. Utiliza la biblioteca Flask-Ask y Pygame para crear un entorno interactivo donde los usuarios pueden controlar un videojuego y otros dispositivos como una bombilla inteligente.

## Características

- **Control de Voz:** Permite controlar un videojuego y otros dispositivos a través de comandos de voz.
- **Escalabilidad:** Diseñado con flexibilidad para adaptarse a futuros desarrollos y otros dispositivos inteligentes.
- **Interactividad:** Integración con Pygame para una experiencia de juego interactiva.
- **Accesibilidad:** Mejora la accesibilidad para personas con discapacidades, permitiéndoles interactuar con videojuegos y dispositivos inteligentes.

## Requisitos

- **Hardware:**
  - Raspberry Pi (modelo 4 recomendado)
  - Dispositivo con Amazon Alexa (e.g., Amazon Echo)
  - Bombilla inteligente (opcional)

- **Software:**
  - Python 3.x
  - Bibliotecas de Python: Flask, Flask-Ask, Pygame
  - ngrok (para túnel HTTP)

## Instalación

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/josehb96/TFG-SistemaControlDispositivosInteligentesAlexa.git
   cd TFG-SistemaControlDispositivosInteligentesAlexa


Documentación del proyecto -> https://rua.ua.es/dspace/handle/10045/135389
