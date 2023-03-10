from flask import Flask
from flask_ask import Ask, statement, question
import pygame, sys # También utilizamos el módulo sys
from pygame.locals import * # Si no utilizamos todas las funciones podemos usar sólo las locales de Pygame
from queue import Queue
from threading import Thread

app = Flask(__name__)
ask = Ask(app, '/')

# Creamos una cola para compartir información entre los hilos
queue = Queue()

# Función que maneja el hilo de Pygame
def game_thread(queue):

    # Iniciación de Pygame
    pygame.init()

    # Pantalla - Ventana
    PANTALLA = pygame.display.set_mode((1000, 600)) # Especificamos el tamaño de la ventana con 500px de ancho y 400px de alto

    # Fondo del juego
    fondo = pygame.image.load("Imagenes/ciudad.jpg")
    fondo = pygame.transform.scale(fondo, (1000, 600)) # Redimensionamos la imagen de fondo para ajustarla al tamaño de la ventana
    PANTALLA.blit(fondo,(0,0)) # Mostramos el fondo ajustando el fondo a toda la pantalla sin dejar márgenes (0,0)

    # Icono y Título
    pygame.display.set_caption('Exterminator') # Añadimos un título a la ventana
    icono = pygame.image.load("Imagenes/exterminator.png") # Cargamos la imagen con el icono
    icono = pygame.transform.scale(icono, (32, 32)) # Redimensionamos la imagen del icono
    pygame.display.set_icon(icono) # y lo añadimos a la ventana

    font = pygame.font.SysFont(None, 48)

    # Bucle del juego
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update() # Con esto nos aseguramos que la ventana se vaya actualizando

        # Esperamos a recibir un mensaje de la cola
        mensaje = queue.get()
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
game_thread = Thread(target=game_thread, args=(queue,))
game_thread.start()

@ask.launch # Para cuando el usuario lanza la skill
def start_skill():
    return question('Bienvenido al videojuego Multihilo. Elige entre futbol y baloncesto.')

# Definimos la ruta para el intent HelloWorldIntent
@ask.intent('FootballIntent')
def football():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    queue.put('Futbol')
    return question('Has elegido futbol.')

@ask.intent('BasketballIntent')
def basketball():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    queue.put('BALONCESTO')
    return question('Has elegido baloncesto.')

@ask.intent('EndgameIntent')
def endgame():
    queue.put('Clean')
    return statement('Fin del juego.')

# Definimos la ruta para la página principal de la aplicación web
@app.route('/')
def index():
    return 'Esta es la homepage del videojuego Multihilo.'

if __name__ == '__main__':
    app.run(debug=True)
    # Cuando la aplicación web se detiene, enviamos un mensaje None a la cola
    queue.put(None)
    # Esperamos a que el hilo de Pygame termine
    game_thread.join()