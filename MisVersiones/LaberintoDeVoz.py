from flask import Flask
from flask_ask import Ask, statement, question
import pygame, sys # También utilizamos el módulo sys
from queue import Queue
from threading import Thread
import random # Librería con utilidades para generar aleatoriedad y azar

app = Flask(__name__)
ask = Ask(app, '/')

# Creamos una cola para compartir información entre los hilos
cola = Queue()

# Función que maneja el hilo de Pygame
def hilo_juego(cola):

    # Iniciación de Pygame
    pygame.init()

    ANCHO = 640 # Definimos el ancho de la ventana de Pygame
    ALTO = 480 # Definimos el alto de la ventana de Pygame

    PANTALLA = pygame.display.set_mode(ANCHO, ALTO) # Configuramos la ventana del juego
    pygame.display.set_caption("Laberinto de voz")

    font = pygame.font.SysFont(None, 48)

    # Bucle del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if cola.qsize() > 0: # Nos aseguramos que la cola tenga elementos antes de intentar obtener uno de ellos

            mensaje = cola.get_nowait()

            # Si el mensaje es None, salimos del bucle y terminamos el hilo
            if mensaje is None:
                break
            # Si recibimos un mensaje de texto, lo mostramos en la pantalla
            if isinstance(mensaje, str):

                if mensaje == 'Clean': # Si se recibe el mensaje Clean es para indicarnos que se vacie la ventana de juego
                    screen = pygame.display.get_surface()
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                else:
                    text = font.render(mensaje, True, (255, 255, 255))
                    screen = pygame.display.get_surface()
                    screen.blit(text, (200, 200))
                    pygame.display.update()


# Creamos el hilo de Pygame y lo iniciamos
hilo_juego = Thread(target=hilo_juego, args=(cola,))
hilo_juego.start()

@ask.launch # Para cuando el usuario lanza la skill
def start_skill():
    return question('Bienvenido al videojuego Multihilo. Elige entre futbol y baloncesto.')

# Definimos la ruta para el intent HelloWorldIntent
@ask.intent('FootballIntent')
def football():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    cola.put('Futbol')
    return question('Has elegido futbol.')

@ask.intent('BasketballIntent')
def basketball():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    cola.put('BALONCESTO')
    return question('Has elegido baloncesto.')

@ask.intent('EndgameIntent')
def endgame():
    cola.put('Clean')
    return statement('Fin del juego.')

# Definimos la ruta para la página principal de la aplicación web
@app.route('/')
def index():
    return 'Esta es la homepage del videojuego Multihilo.'

if __name__ == '__main__':

    app.run(debug=False) # Si desactivamos el modo debug evitamos que nos abra 2 ventanas de pygame
    # Cuando la aplicación web se detiene, enviamos un mensaje None a la cola
    cola.put(None)
    # Esperamos a que el hilo de Pygame termine
    hilo_juego.join()