# Sistema de Control de Dispositivos Inteligentes con Amazon Alexa

Este proyecto consiste en el desarrollo de una skill de Alexa para el control por voz de dispositivos inteligentes, incluyendo un videojuego en una Raspberry Pi, mejorando así la accesibilidad y promoviendo el desarrollo de software con Alexa.

## Índice

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Arquitectura](#arquitectura)
- [Agradecimientos](#agradecimientos)
- [Documentación](#documentación)

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

3. **Instala las dependencias:**
   
   ```sh
   pip install flask flask-ask pygame

5. **Configura ngrok:**
    - Regístrate en ngrok y descarga el binario.
    - Iniciar ngrok:
      
      ```sh
      ngrok http 5000

4. **Configura la skill en Amazon Developer Console**
    - Crea una nueva skill en la consola de desarrolladores de Amazon Alexa
    - Configura el endpoint de la skill usando la URL proporcionada por ngrok.

## Uso

1. **Ejecuta la aplicación:**
   
   ```sh
   python app.py

3. **Inicia la skill en tu dispositivo Alexa y prueba los comandos de voz.**
    - Ejemplo: "Alexa, abre juego de Raspberry Pi".

## Arquitectura



El sistema utiliza una arquitectura cliente-servidor donde Alexa actúa como cliente enviando comandos de voz a un servidor Flask ejecutándose en la Raspberry Pi. La Raspberry Pi interpreta los comandos y controla el videojuego y otros dispositivos conectados.

## Agradecimientos

![Arquitectura del sistema](/images/Arquitectura.png "Arquitectura del sistema")

Gracias a todos los que han contribuido a este proyecto, especialmente a Francisco Antonio Pujol López por su tutoría y a mi familia por su apoyo constante.

## Documentación

Enlace a la memoria completa del proyecto -> https://rua.ua.es/dspace/handle/10045/135389
