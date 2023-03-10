from flask import Flask
from flask_ask import Ask, statement, question
import pygame, sys # También utilizamos el módulo sys
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
    ANCHO, ALTO = 1000, 687
    PANTALLA = pygame.display.set_mode((ANCHO, ALTO)) # Especificamos el tamaño de la ventana con 500px de ancho y 400px de alto
    FPS = 60
    RELOJ = pygame.time.Clock()

    # Fondo del juego
    #fondo = pygame.image.load("Imagenes/Ciudad.png")
    fondo = pygame.image.load("Imagenes/Ciudad.png").convert() # Con convert se optimiza la imagen, acelerando el juego y consumiendo menos recursos
    #fondo = pygame.transform.scale(fondo, (1000, 687)) # Redimensionamos la imagen de fondo para ajustarla al tamaño de la ventana
    x = 0

    # Icono y Título
    pygame.display.set_caption('Exterminator') # Añadimos un título a la ventana
    icono = pygame.image.load("Imagenes/exterminator.png") # Cargamos la imagen con el icono
    icono = pygame.transform.scale(icono, (32, 32)) # Redimensionamos la imagen del icono
    pygame.display.set_icon(icono) # y lo añadimos a la ventana

    font = pygame.font.SysFont(None, 48)

    # Bucle del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Hacemos que el fondo se mueva de forma fluida
        x_relativa = x % fondo.get_rect().width
        PANTALLA.blit(fondo, (x_relativa - fondo.get_rect().width, 0))
        if x_relativa < ANCHO:
            PANTALLA.blit(fondo, (x_relativa,0)) # Si queremos que el fondo en lugar de moverse horizontalmente, lo haga verticalmente tendríamos que poner y_relativa en la coordenada Y, y dejar a 0 la coordenada X

        x -= 1 # Decrementamos en 1 px en cada iteración del bucle para que el fondo se mueva a la derecha, si en lugar de restar, sumamos la imagen se moverá hacia la izquierda
        pygame.display.update() # Con esto nos aseguramos que la ventana se vaya actualizando
        RELOJ.tick(FPS) # Con esto junto con el decremento de la x en 1 conseguimos mover un total de 60px por segundo

        if queue.qsize() > 0: # Nos aseguramos que la cola tenga elementos antes de intentar obtener uno de ellos

            mensaje = queue.get_nowait()

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

    app.run(debug=False) # Si desactivamos el modo debug evitamos que nos abra 2 ventanas de pygame
    # Cuando la aplicación web se detiene, enviamos un mensaje None a la cola
    queue.put(None)
    # Esperamos a que el hilo de Pygame termine
    game_thread.join()