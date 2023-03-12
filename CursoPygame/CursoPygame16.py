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

    # Fuentes
    consolas = pygame.font.match_font('consolas')
    times = pygame.font.match_font('times')
    arial = pygame.font.match_font('arial')
    courier = pygame.font.match_font('courier')

    class Jugador(pygame.sprite.Sprite):

        # Sprite del jugador
        def __init__(self):

            # Heredamos el init de la clase Sprite de Pygame
            super().__init__()

            # Rectángulo (jugador), recordemos que las imágenes en Pygame son rectángulos
            self.image = pygame.image.load("../Imagenes/Personaje.png").convert() # Convertimos la imagen a tipo Pygame para que el rendimiento mejore
            #self.image.fill(H_FA2F2F) # No indicamos ningún color al sprite porque queremos que se muestre la imagen

            self.image.set_colorkey(VERDE) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # Obtiene el rectángulo (sprite) de la imagen del jugador para poder manipularlo
            self.rect = self.image.get_rect()

            # SI QUEREMOS EL RECTÁNGULO ESTÁNDAR DEL SPRITE PARA VER CÓMO FUNCIONAN LAS COLISIONES:
            #self.image = pygame.Surface((97,117)) # Dibujamos sobre el sprite del jugador un rectángulo del tamaño en px de la imagen del jugador
            #self.image.fill(AZUL2)

            # Vamos a utilizar la técnica matemática CIRCULAR BOUNDING BOX para mejorar las colisiones
            self.radius = 35 # Establecemos el radio
            #pygame.draw.circle(self.image, AZUL2, self.rect.center, self.radius) # Para hacer pruebas

            self.rect.center = (400,600) # Podemos colocar el rectángulo en la posición inicial que queramos
            # Centra el rectángulo (sprite)
            #self.rect.center = (ANCHO // 2, ALTO // 2) # Este operador devuelve el resultado (integer) de dividir, redondeando si sale float

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

            # El personaje dispara
            if teclas[pygame.K_SPACE]:
                jugador.disparo()
                #jugador.disparo2() Por si queremos tener más cañones de disparo
                #jugador.disparo3()

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

        def disparo(self):
            #bala = Disparo(self.rect.centerx, self.rect.top + 20) # Hacemos que la bala se instancie en el centro del rectángulo del jugador y además arriba del rectángulo del jugador
            bala = Disparo(self.rect.right -20 , self.rect.centery + 7)
            spritesBalas.add(bala)
            
        """# Podemos aumentar el número de "cañones de disparo"
        def disparo2(self):
            bala = Disparo(self.rect.centerx + 23, self.rect.top + 30) # Hacemos que la bala se instancie en el centro del rectángulo del jugador y además arriba del rectángulo del jugador
            spritesBalas.add(bala)

        def disparo3(self):
            bala = Disparo(self.rect.centerx -23, self.rect.top + 30) # Hacemos que la bala se instancie en el centro del rectángulo del jugador y además arriba del rectángulo del jugador
            spritesBalas.add(bala)"""

    class Enemigo(pygame.sprite.Sprite):

        # Sprite del enemigo
        def __init__(self, rutaImagen, colorFondo, radio, velocidad_maxima):

            # Heredamos el init de la clase Sprite de Pygame
            super().__init__()

            # Rectángulo (enemigo), recordemos que las imágenes en Pygame son rectángulos
            #self.image = pygame.image.load(rutaImagen).convert() # Convertimos la imagen a tipo Pygame para que el rendimiento mejore
            self.image = pygame.transform.scale(pygame.image.load(rutaImagen).convert(), (79, 117)) # Cargamos la imagen y la redimensionamos a 10px de ancho y 20px de alto

            self.image.set_colorkey(colorFondo) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # SI QUEREMOS EL RECTÁNGULO ESTÁNDAR DEL SPRITE PARA VER CÓMO FUNCIONAN LAS COLISIONES:
            #self.image = pygame.Surface((79,117))
            #self.image.fill(ROJO)

            # Obtiene el rectángulo (sprite) de la imagen del jugador para poder manipularlo
            self.rect = self.image.get_rect()

            # Vamos a utilizar la técnica matemática CIRCULAR BOUNDING BOX para mejorar las colisiones
            self.radius = radio # Establecemos el radio
            #pygame.draw.circle(self.image, ROJO, self.rect.center, self.radius) # Para hacer pruebas

            # Hacemos que el enemigo pueda aparecer en cualquier lugar de la pantalla de forma aleatoria
            self.rect.x = random.randrange(ANCHO - self.rect.width) # Con esto vamos a poner como coordenada X del sprite un número aleatorio entre todos los píxeles del ancho de la pantalla y además controlamos que no se coloque fuera de los márgenes de la pantalla ya que tendrá en cuenta el ancho del propio rectángulo
            self.rect.y = random.randrange(ALTO - self.rect.height) # Con esto hacemos lo mismo pero para la coordenada Y

            # Velocidad inicial del enemigo para que se mueva sin que tenga que ocurrir nada antes
            #self.velocidad_x = 5
            #self.velocidad_y = 5
            # Si en lugar de que se muevan con una velocidad establecida lo hagan con una velocidad alaatoria
            self.velocidad_x = random.randrange(1, velocidad_maxima) # Con esto la velocidad será entre 1 y velocidad_maxima
            self.velocidad_y = random.randrange(1, velocidad_maxima)

        def update(self):

            # Actualiza la velocidad del enemigo
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            # Limita el margen izquierdo y hacemos que el enemigo rebote
            if self.rect.left < 0: # Cada vez que toque el borde izquierdo e intente salir de la pantalla 
                self.velocidad_x += 1 # Hacemos que rebote

            # Limita el margen derecho
            if self.rect.right > ANCHO:
                self.velocidad_x -= 1

            # Limita el margen inferior
            if self.rect.bottom > ALTO:
                self.velocidad_y -= 1

            # Limita el margen superior
            if self.rect.top < 0:
                self.velocidad_y += 1

    class Disparo(pygame.sprite.Sprite):
        def __init__(self, x, y): # Los parámetros x e y son para indicar la posición exacta de la zona donde se van a generar los disparos
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load("../Imagenes/bala.png").convert(), (20, 20)) # Cargamos la imagen y la redimensionamos a 10px de ancho y 20px de alto
            self.image.set_colorkey(VERDE)
            self.rect = self.image.get_rect() # Obtenemos el rectángulo de la imagen
            self.rect.bottom = y # La posición y va a ser la parte baja del rectángulo de la bala
            self.rect.centerx = x # Centramos a la posición de en medio del rectángulo del jugador
        
        def update(self):
            self.rect.x += 25
            #self.rect.y -= 25 # Con esto conseguimos que las balas vayan hacia arriba
            if self.rect.bottom < 0: # Cuando la bala salga por la parte superior de la pantalla
                self.kill() # Elimina dicha bala

    class Virus(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()

            self.img_aleatoria = random.randrange(3)

            if self.img_aleatoria == 0:
                self.image = pygame.transform.scale(pygame.image.load("../Imagenes/Virus.png").convert(), (100,100))
                self.radius = 50
            elif self.img_aleatoria == 1:
                self.image = pygame.transform.scale(pygame.image.load("../Imagenes/Virus.png").convert(), (50,50))
                self.radius = 25
            elif self.img_aleatoria == 2:
                self.image = pygame.transform.scale(pygame.image.load("../Imagenes/Virus.png").convert(), (25,25))
                self.radius = 12

            self.image.set_colorkey(ROJO)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(ANCHO - self.rect.width) # Posición inicial en x que van a tomar los virus instanciados evitando que se generen a medio trozo de la pantalla
            self.rect.y = -self.rect.width # Evitamos que se genere por dentro de la pantalla
            self.velocidad_y = random.randrange(1, 2)
        
        def update(self):
            self.rect.y += self.velocidad_y # Para que vaya el virus hacia abajo
            if self.rect.top > ALTO: # Si el virus desaparece de la pantalla por debajo, entonces que vuelva a tomar los valores iniciales
                self.rect.x = random.randrange(ANCHO - self.rect.width)
                self.rect.y = -self.rect.width
                # ANCHO
                self.velocidad_y = random.randrange(1, 2) # Y además que vuelva a tomar una velocidad aleatoria diferente

    # UNA IDEA MUY INTERESANTE ES CREAR SPRITES DE BOTIQUINES PARA QUE EL PERSONAJE PUEDA RECUPERAR SALUD O VOLVER A SER HUMANO POR EJEMPLO

    # Iniciación de Pygame, creación de la ventana, título y control de reloj.
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Movimiento")
    clock = pygame.time.Clock() # Para controlar los FPS

    # Sistema de puntuaciones
    puntuacion = 0

    def muestra_texto(pantalla, fuente, texto, color, dimensiones, x, y): 
        tipo_letra = pygame.font.Font(fuente, dimensiones) # Las dimensiones son el tamaño en px de la fuente
        superficie = tipo_letra.render(texto, True, color) # Creamos una variable para mostrar el texto, el True es si queremos que use antialiasing
        rectangulo = superficie.get_rect()
        rectangulo.center = (x,y) # Para poder manipular la posición de dicho rectángulo
        pantalla.blit(superficie, rectangulo) # Para que finalmente se pueda mostrar en la pantalla

    font = pygame.font.SysFont(None, 100)

    # Grupo de sprites
    sprites = pygame.sprite.Group() # Se agrupan los sprites para que trabajen en un conjunto y se almacene en la variable que queramos
    spritesEnemigosNivel1 = pygame.sprite.Group() # Como vamos a utilizar las colisiones necesitamos tener un grupo dedicado a los enemigos
    spritesEnemigosNivel2 = pygame.sprite.Group() # Como vamos a utilizar las colisiones necesitamos tener un grupo dedicado a los enemigos
    spritesEnemigosNivel3 = pygame.sprite.Group() # Como vamos a utilizar las colisiones necesitamos tener un grupo dedicado a los enemigos
    spritesBalas = pygame.sprite.Group()
    spritesVirus = pygame.sprite.Group() 

    max_enemies = 5 # Establecemos el máximo de enemigos

    # Instanciación del objeto jugador
    jugador = Jugador()

    '''# Instanciación de los objetos enemigos
    enemigoNivel1 = Enemigo("../Imagenes/Enemigo1.png", AZUL, 35, 2)
    enemigoNivel2 = Enemigo("../Imagenes/Enemigo2.png", VERDE, 35, 3)
    enemigoNivel3 = Enemigo("../Imagenes/Enemigo3.png", VERDE, 35, 4)'''

    '''# Instanciación de los virus
    for x in range(2):
        virus = Virus()
        spritesVirus.add(virus)'''

    #lista_enemigos = [] # Creamos la lista de enemigos para guardarnos las referencias y poder borrarlos posteriormente del juego

    # Bucle de juego
    ejecutando = True
    while ejecutando:

        #pantalla.blit(fondo, (0,0)) # Para añadir un fondo de nuestra elección usar esta línea

        if queue.qsize() > 0: # Nos aseguramos que la cola tenga elementos antes de intentar obtener uno de ellos

            mensaje = queue.get_nowait()

            # Si el mensaje es None, salimos del bucle y terminamos el hilo
            if mensaje is None:
                break
            # Si recibimos un mensaje de texto
            if isinstance(mensaje, str):

                if mensaje == 'Init': # Si se recibe este mensaje es para introducir al jugador en la partida

                    # EL ORDEN EN EL QUE INSTANCIAMOS LOS SPRITES DETERMINA CUAL APARECE POR ENCIMA DE OTRO, EL ÚLTIMO INSTANCIADO APARECERÁ POR ENCIMA 
                    
                    sprites.add(jugador) # Al grupo le añadimos jugador, para que tenga la imagen del jugador

                    """for x in range(random.randrange(max_enemies) + 1): # Generamos de 1 a 5 enemigos de forma aleatoria (con el +1 nos aseguramos que siempre va a haber por lo menos un enemigo instanciado)
                        lista_enemigos.append(enemigo) # Nos guardamos la referencia de cada enemigo en una lista para poder borrarlos todos cuando finalice el juego
                        spritesEnemigos.add(enemigo)
                    
                    spritesEnemigosNivel1.add(enemigoNivel1)
                    spritesEnemigosNivel2.add(enemigoNivel2)
                    spritesEnemigosNivel3.add(enemigoNivel3)"""

                    puntuacion = 0 # Reiniciamos la puntuación

                elif mensaje == 'Endgame': # Si se recibe el mensaje Endgame es para indicarnos que se vacie la ventana de juego

                    """sprites.remove(jugador) # Eliminamos al personaje de la pantalla
                    #jugador = None

                    for enemigo in lista_enemigos: # Eliminamos todos los sprites de enemigos de la pantalla
                        sprites.remove(enemigo)"""
                    
                    jugador.kill() 

                    #spritesEnemigos.empty()
                    
                    #lista_enemigos.clear() # Vaciamos la lista de enemigos

                    text = font.render('ENDGAME', True, ROJO)

                    # Obtener las dimensiones del texto
                    text_width, text_height = font.size("ENDGAME")

                    # Calcular la posición para centrar el texto
                    x = (ANCHO - text_width) // 2
                    y = (ALTO - text_height) // 2

                    screen = pygame.display.get_surface()
                    screen.blit(text, (x,y)) # Vamos a centrar el texto en la ventana de Pygame
                    pygame.display.update()
                    #end_session()
                    time.sleep(5)

                elif mensaje == 'Up' or mensaje == 'Down' or mensaje == 'Left' or mensaje == 'Right' or mensaje == 'UpLeft' or mensaje == 'UpRight' or mensaje == 'DownLeft' or mensaje == 'DownRight': # Si se nos ha pedido mover el personaje
                    
                    jugador.ejecutaMovimiento(mensaje)

                    # Dibujamos los sprites en la pantalla
                    sprites.draw(pantalla)

                    # Actualizamos los sprites
                    sprites.update()

                    # Actualizamos la pantalla
                    pygame.display.flip()

                    # Dibuja 

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
        spritesEnemigosNivel1.update()
        spritesEnemigosNivel2.update()
        spritesEnemigosNivel3.update()
        spritesBalas.update()
        spritesVirus.update()

        # Indicamos que el sprite de los enemigos va a ser el que provoque la colisión sobre el grupo de sprites colisionados (spritesEnemigos) y que no queremos que por defecto haya kill a los enemigos (False)
        #colision_personaje = pygame.sprite.spritecollide(jugador, spritesVirus, False, pygame.sprite.collide_circle) # spritecollide nos permite utilizar un sprite contra un grupo y ahí generamos una colisión, además aquí le indicamos que trabaje con colisiones circulares

        #colision_enemigo = pygame.sprite.spritecollide(jugador, spritesEnemigos, False, pygame.sprite.collide_circle) # spritecollide nos permite utilizar un sprite contra un grupo y ahí generamos una colisión, además aquí le indicamos que trabaje con colisiones circulares

        #colision_disparos = pygame.sprite.groupcollide(spritesEnemigos, spritesBalas, False, True) # Para colisiones grupales, el False sirve para que cuando se cree la colisión no se eliminan los enemigos, y el True sirve para que se eliminen las balas cada vez que impacten en algún enemigo  

        '''if colision_disparos:
            enemigo.image = pygame.image.load("../Imagenes/Sangre.png").convert()
            enemigo.image.set_colorkey(ROJO)
            enemigo.velocidad_y += 10 # Hacemos que el enemigo eliminado caiga hacia abajo
        if enemigo.rect.top > ALTO:
            enemigo.kill()
        if colision_personaje or colision_enemigo: 
            jugador.image = pygame.image.load("../Imagenes/Enemigo.png").convert()
            jugador.image.set_colorkey(VERDE)'''

        colision_disparos_enemigosNivel1 = pygame.sprite.groupcollide(spritesEnemigosNivel1, spritesBalas, True, True, pygame.sprite.collide_circle) 

        colision_disparos_enemigosNivel2 = pygame.sprite.groupcollide(spritesEnemigosNivel2, spritesBalas, True, True, pygame.sprite.collide_circle)

        colision_disparos_enemigosNivel3 = pygame.sprite.groupcollide(spritesEnemigosNivel3, spritesBalas, True, True, pygame.sprite.collide_circle)

        if colision_disparos_enemigosNivel1:
            puntuacion += 10
        
        if colision_disparos_enemigosNivel2:
            puntuacion += 20
        
        if colision_disparos_enemigosNivel3:
            puntuacion += 30

        # ESTO ES PARA HACER PRUEBAS PARA QUE EL JUEGO NO SE QUEDE VACÍO AL ACABAR CON TODOS LOS ENEMIGOS
        if not spritesEnemigosNivel1 and not spritesEnemigosNivel2 and not spritesEnemigosNivel3:

            enemigoNivel1 = Enemigo("../Imagenes/Enemigo1.png", AZUL, 35, 2)
            spritesEnemigosNivel1.add(enemigoNivel1)

            enemigoNivel2 = Enemigo("../Imagenes/Enemigo2.png", VERDE, 35, 3)
            spritesEnemigosNivel2.add(enemigoNivel2)

            enemigoNivel3 = Enemigo("../Imagenes/Enemigo3.png", VERDE, 35, 4)
            spritesEnemigosNivel3.add(enemigoNivel3)

        # Fondo de pantalla, dibujo de sprites y formas geométricas
        pantalla.fill(NEGRO) # Establecemos el color de fondo de la pantalla
        sprites.draw(pantalla) # Dibujamos los sprites en la pantalla
        spritesEnemigosNivel1.draw(pantalla)
        spritesEnemigosNivel2.draw(pantalla)
        spritesEnemigosNivel3.draw(pantalla)
        spritesBalas.draw(pantalla)
        spritesVirus.draw(pantalla)
        pygame.draw.line(pantalla, H_50D2FE, (400, 0), (400, 800), 1)
        pygame.draw.line(pantalla, AZUL, (0, 300), (800, 300), 1)

        # Dibuja los textos en la pantalla
        muestra_texto(pantalla, consolas, str(puntuacion), ROJO, 40, 700, 50) # Mostramos la puntuación en la pantalla

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