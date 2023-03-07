from flask import Flask
from flask_ask import Ask, statement, question
import pygame, sys # También utilizamos el módulo sys
from queue import Queue
from threading import Thread
import time
import random # Para hacer cosas aleatorias

app = Flask(__name__)
ask = Ask(app, '/')

# Creamos una cola para compartir información entre los hilos
queue = Queue()

# Función que maneja el hilo de Pygame
def game_thread(queue):

    # Tamaño de la pantalla de Pygame en píxeles
    ANCHO = 800
    ALTO = 600

    # FPS
    FPS = 30

    # Paleta de colores en RGB
    NEGRO = (0,0,0)
    BLANCO = (255,255,255)
    ROJO = (255,0,0)
    H_FA2F2F = (250,47,47)
    VERDE = (0,255,0)
    AZUL = (0,0,255)
    H_50D2FE = (94,210,254)
    AZUL2 = (64,64,255)

    class Jugador(pygame.sprite.Sprite):

        # Sprite del jugador
        def __init__(self):

            # Heredamos el init de la clase Sprite de Pygame
            super().__init__()

            # Rectángulo (jugador), recordemos que las imágenes en Pygame son rectángulos
            self.image = pygame.image.load("Imagenes/Personaje.png").convert() # Convertimos la imagen a tipo Pygame para que el rendimiento mejore
            #self.image.fill(H_FA2F2F) # No indicamos ningún color al sprite porque queremos que se muestre la imagen

            self.image.set_colorkey(VERDE) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # Obtiene el rectángulo (sprite) de la imagen del jugador para poder manipularlo
            self.rect = self.image.get_rect()

            # Centra el rectángulo (sprite)
            self.rect.center = (ANCHO // 2, ALTO // 2) # Este operador devuelve el resultado (integer) de dividir, redondeando si sale float
            #self.rect.center = (400,600) # Podemos colocar el rectángulo en la posición inicial que queramos

            # Velocidad del personaje (inicial)
            self.velocidad_x = 0 # Inicialmente el objeto va a estar quieto
            self.velocidad_y = 0

        def update(self):

            # Velocidad predeterminada cada vuelta del bucle si no pulsas nada
            # ESTO PARA TRABAJAR POR VOZ SEGURAMENTE NO NOS INTERESA
            self.velocidad_x = 0 # Con esto se evita que el personaje se mueva de manera indefinida si no estamos pulsando nada
            self.velocidad_y = 0

            # Mantiene las teclas pulsadas
            teclas = pygame.key.get_pressed()

            # Mueve el personaje hacia la izquierda
            if teclas[pygame.K_a]:
                self.velocidad_x = -10 # Cada vez que se pulse la tecla se moverá 10px a la izquierda
            
            # Mueve el personaje hacia la derecha
            if teclas[pygame.K_d]:
                self.velocidad_x = 10

            # Mueve el personaje hacia arriba
            if teclas[pygame.K_w]:
                self.velocidad_y = -10 # Cada vez que se pulse la tecla se moverá 10px hacia arriba
            
            # Mueve el personaje hacia abajo
            if teclas[pygame.K_s]:
                self.velocidad_y = 10

            # Actualiza la posición del personaje
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            # Limita el margen izquierdo
            if self.rect.left < 0: # Cada vez que toque el borde izquierdo e intente salir de la pantalla 
                self.rect.left = 0 # Se ajusta el personaje al borde izquierdo

            # Limita el margen derecho
            if self.rect.right > ANCHO:
                self.rect.right = ANCHO

            # Limita el margen inferior
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

            # Limita el margen superior
            if self.rect.top < 0:
                self.rect.top = 0

            """
            # Si queremos limitar aún más el recorrido y no hasta los bordes pues simplemente podemos hacerlo tal que así
            if self.rect.left < 300:
                self.rect.left = 300

            if self.rect.right > 500:
                self.rect.right = 500
            """        

        def ejecutaMovimiento(self, movimiento):

            # Velocidad predeterminada cada vuelta del bucle si no pulsas nada
            # ESTO PARA TRABAJAR POR VOZ SEGURAMENTE NO NOS INTERESA
            self.velocidad_x = 0 # Con esto se evita que el personaje se mueva de manera indefinida si no estamos pulsando nada
            self.velocidad_y = 0

            # Mueve el personaje hacia la izquierda
            if movimiento == 'Left':
                self.velocidad_x = -50 # Cada vez que se pulse la tecla se moverá 10px a la izquierda
            
            # Mueve el personaje hacia la derecha
            elif movimiento == 'Right':
                self.velocidad_x = 50

            # Mueve el personaje hacia arriba
            elif movimiento == 'Up':
                self.velocidad_y = -50 # Cada vez que se pulse la tecla se moverá 10px hacia arriba
            
            # Mueve el personaje hacia abajo
            elif movimiento == 'Down':
                self.velocidad_y = 50

            # Mueve el personaje hacia arriba a la izquierda
            elif movimiento == 'UpLeft':
                self.velocidad_x = -50
                self.velocidad_y = -50 
            
            # Mueve el personaje hacia arriba a la derecha
            elif movimiento == 'UpRight':
                self.velocidad_x = 50
                self.velocidad_y = -50

            # Mueve el personaje hacia abajo a la izquierda
            elif movimiento == 'DownLeft':
                self.velocidad_y = 50
                self.velocidad_x = -50
            
            # Mueve el personaje hacia abaja a la derecha
            elif movimiento == 'DownRight':
                self.velocidad_y = 50
                self.velocidad_x = 50

            # Actualiza la posición del personaje
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            # Limita el margen izquierdo
            if self.rect.left < 0: # Cada vez que toque el borde izquierdo e intente salir de la pantalla 
                self.rect.left = 0 # Se ajusta el personaje al borde izquierdo

            # Limita el margen derecho
            if self.rect.right > ANCHO:
                self.rect.right = ANCHO

            # Limita el margen inferior
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

            # Limita el margen superior
            if self.rect.top < 0:
                self.rect.top = 0

    class Enemigo(pygame.sprite.Sprite):

        # Sprite del enemigo
        def __init__(self):

            # Heredamos el init de la clase Sprite de Pygame
            super().__init__()

            # Rectángulo (enemigo), recordemos que las imágenes en Pygame son rectángulos
            self.image = pygame.image.load("Imagenes/Enemigo.png").convert() # Convertimos la imagen a tipo Pygame para que el rendimiento mejore

            self.image.set_colorkey(VERDE) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # Obtiene el rectángulo (sprite) de la imagen del jugador para poder manipularlo
            self.rect = self.image.get_rect()

    # Bucle de juego
    ejecutando = True
    while ejecutando:

        mensaje = queue.get()

        # Si el mensaje es None, salimos del bucle y terminamos el hilo
        if mensaje is None:
            break
        # Si recibimos un mensaje de texto
        if isinstance(mensaje, str):

            if mensaje == 'Init':

                # Iniciación de Pygame, creación de la ventana, título y control de reloj.
                pygame.init()
                pantalla = pygame.display.set_mode((ANCHO, ALTO))
                pygame.display.set_caption("Movimiento")
                clock = pygame.time.Clock() # Para controlar los FPS

                font = pygame.font.SysFont(None, 100)

                # Grupo de sprites, instanciación del objeto jugador.
                sprites = pygame.sprite.Group() # Se agrupan los sprites para que trabajen en un conjunto y se almacene en la variable que queramos
                jugador = Jugador()
                sprites.add(jugador) # Al grupo le añadimos jugador, para que tenga la imagen del jugador

            elif mensaje == 'Endgame': # Si se recibe el mensaje Endgame es para indicarnos que se vacie la ventana de juego
                #pantalla = pygame.display.get_surface()
                #pantalla.fill(NEGRO)
                #pygame.quit()
                #sys.exit()
                #pygame.display.update()
                #ejecutando = False
                text = font.render('ENDGAME', True, ROJO)

                # Obtener las dimensiones del texto
                text_width, text_height = font.size("ENDGAME")

                # Calcular la posición para centrar el texto
                x = (ANCHO - text_width) // 2
                y = (ALTO - text_height) // 2

                screen = pygame.display.get_surface()
                screen.blit(text, (x,y)) # Vamos a centrar el texto en la ventana de Pygame
                pygame.display.update()
                time.sleep(5)

            elif mensaje == 'Up' or mensaje == 'Down' or mensaje == 'Left' or mensaje == 'Right' or mensaje == 'UpLeft' or mensaje == 'UpRight' or mensaje == 'DownLeft' or mensaje == 'DownRight': # Si se nos ha pedido mover el personaje
                
                jugador.ejecutaMovimiento(mensaje)

                # Dibujamos los sprites en la pantalla
                sprites.draw(pantalla)

                # Actualizamos los sprites
                sprites.update()

                # Actualizamos la pantalla
                pygame.display.flip()

        # Es lo que especifica la velocidad del bucle de juego
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get(): # Obtenemos una lista de todos los eventos en la cola de eventos de Pygame, que incluyen eventos del teclado, del mouse, de la ventana, etc.
            if event.type == pygame.QUIT: # Si el evento es de tipo `QUIT` indica que el usuario ha hecho clic en el botón "X" para cerrar la ventana.
                ejecutando = False
                #pygame.quit()
                #sys.exit()

        # Actualización de sprites
        sprites.update() # Con esto podemos hacer que todos los sprites (imágenes) se vayan actualizando en la pantalla

        # Fondo de pantalla, dibujo de sprites y formas geométricas
        pantalla.fill(NEGRO) # Establecemos el color de fondo de la pantalla
        sprites.draw(pantalla) # Dibujamos los sprites en la pantalla
        pygame.draw.line(pantalla, H_50D2FE, (400, 0), (400, 800), 1)
        pygame.draw.line(pantalla, AZUL, (0, 300), (800, 300), 1)

        # Actualizamos el contenido de la pantalla
        pygame.display.flip() # Permite que solo una porción de la pantalla se actualice, en lugar de toda el área de la pantalla. Si no se pasan argumentos, se actualizará la superficie completa.

    pygame.quit()

# Creamos el hilo de Pygame y lo iniciamos
game_thread = Thread(target=game_thread, args=(queue,))
game_thread.start()

@ask.launch # Para cuando el usuario lanza la skill
def start_skill():
    # Indicamos a pygame que inicie el videojuego
    queue.put('Init')
    return question('Bienvenido al videojuego Movimiento. Dime en qué dirección quieres moverte.')

# Definimos la ruta para el intent UpIntent
@ask.intent('UpIntent')
def arriba():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('Up')
    return question('El personaje se mueve hacia arriba.')

# Definimos la ruta para el intent DownIntent
@ask.intent('DownIntent')
def abajo():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('Down')
    return question('El personaje se mueve hacia abajo.')

# Definimos la ruta para el intent RightIntent
@ask.intent('RightIntent')
def derecha():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('Right')
    return question('El personaje se mueve hacia la derecha.')

# Definimos la ruta para el intent DownIntent
@ask.intent('LeftIntent')
def izquierda():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('Left')
    return question('El personaje se mueve hacia la izquierda.')

# Definimos la ruta para el intent UpLeftIntent
@ask.intent('UpLeftIntent')
def arribaIzquierda():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('UpLeft')
    return question('El personaje se mueve arriba a la izquierda.')

# Definimos la ruta para el intent UpRightIntent
@ask.intent('UpRightIntent')
def arribaDerecha():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('UpRight')
    return question('El personaje se mueve arriba a la derecha.')

# Definimos la ruta para el intent DownLeftIntent
@ask.intent('DownLeftIntent')
def arribaIzquierda():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('DownLeft')
    return question('El personaje se mueve abajo a la izquierda.')

# Definimos la ruta para el intent DownRightIntent
@ask.intent('DownRightIntent')
def arribaDerecha():
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put('DownRight')
    return question('El personaje se mueve abajo a la derecha.')

@ask.intent('EndgameIntent')
def endgame():
    queue.put('Endgame')
    return statement('Fin del juego.')

# Definimos la ruta para la página principal de la aplicación web
@app.route('/')
def index():
    return 'Esta es la homepage del videojuego Movimiento.'

if __name__ == '__main__':

    app.run(debug=False) # Si desactivamos el modo debug evitamos que nos abra 2 ventanas de pygame
    # Cuando la aplicación web se detiene, enviamos un mensaje None a la cola
    queue.put(None)
    # Esperamos a que el hilo de Pygame termine
    game_thread.join()