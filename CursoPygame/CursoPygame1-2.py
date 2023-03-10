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

    pygame.init()

    PANTALLA = pygame.display.set_mode((500, 400)) # Especificamos el tamaño de la ventana con 500px de ancho y 400px de alto
    pygame.display.set_caption('Mi primer juego :D') # Añadimos un título a la ventana

    # Nos creamos una paleta de colores personalizada para ahorrar tiempo
    BLANCO = (255,255,255)
    NEGRO = (0,0,0)
    ROJO = (255,0,0)
    AZUL = (0,0,255)
    VERDE = (0,255,0)

    HC74225 = (199,66,37)
    H61CD35 = (97,205,53)

    PANTALLA.fill(BLANCO) # Vamos a poner un fondo blanco en la ventana
    
    # Dibujamos un rectángulo
    # Hay que tener en cuenta los píxeles de la pantalla para no pasarnos con el tamaño
    # 100px desde el borde izquierdo de la pantalla (de izquierda a derecha) y 50px desde arriba hasta abajo
    # 100px de ancho y 50px de alto
    rectangulo1 = pygame.draw.rect(PANTALLA, ROJO, (100, 50, 100, 50)) # Si lo almacenamos en una variable podremos reutilizarlo
    print(rectangulo1) 

    # Dibujamos una línea
    # El 100 indica la distancia del borde izquierdo, el 199 donde acaba respecto a dicho borde y los 104 inclinan la línea a la izquierda o a la derecha. El 10 indica el grosor.
    pygame.draw.line(PANTALLA, VERDE, (100,104), (199,104),10)

    # Dibujamos un círculo
    # El 122 indica la posición respecto al eje X, el 250 respecto al eje Y, el 20 es el radio del círculo y el 0 indica el relleno a quitar del círculo
    pygame.draw.circle(PANTALLA, NEGRO, (122, 250), 20, 0)

    # Dibujamos una elipse
    # 275 la posición X, 200 la posición Y, tamaño X de 40 y tamaño Y de 80, por último quedaría el grueso que si no indicamos nada nos va a quedar totalmente opaco
    pygame.draw.ellipse(PANTALLA, H61CD35, (275, 200, 40, 80))
    #pygame.draw.ellipse(PANTALLA, H61CD35, (275, 200, 40, 80), 10) # Así nos quedaría hueco por ejemplo
    #pygame.draw.ellipse(PANTALLA, H61CD35, (100, 200, 40, 80), 10) # Si cambiamos la posición X de la elipse se superpondría al círculo

    # Forma de hacer polígonos
    #puntos = [(100,300),(100,100)]
    puntos = [(100,300),(100,100),(150,100)] # Hacemos un triángulo, si quisiéramos hacer un cuadrado añadimos una cuarta tupla y tendríamos un cuadrado
    pygame.draw.polygon(PANTALLA,(0,150,255), puntos, 8) # El 8 representa el grueso

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