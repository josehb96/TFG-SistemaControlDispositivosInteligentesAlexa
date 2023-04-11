from flask import Flask
from flask_ask import Ask, statement, question
import pygame
from queue import Queue
from threading import Thread
import time 
import random
from PyP100 import PyL530 # Librería para poder controlar la bombilla

app = Flask(__name__)
ask = Ask(app, '/')

# Preparamos la conexión a la bombilla para poder realizar peticiones a esta posteriormente
bombilla = PyL530.L530("192.168.68.100", "jose_basket96@hotmail.com", ".dF3-1Csep0")

bombilla.handshake() # Creamos las cookies necesarias para más métodos
bombilla.login() # Se envían las credenciales de inicio de sesión a la bombilla y se crea una clave y un vector de inicialización AES para su uso en métodos posteriores

# Creamos una cola para compartir información entre los hilos
queue = Queue()

# Función que maneja el hilo de Pygame
def game_thread(queue):

    # Tamaño de la screen de Pygame en píxeles
    ANCHO = 800
    ALTO = 600

    # FPS
    FPS = 30

    # Paleta de colores en RGB
    ROJO = (255,0,0)
    VERDE = (0,255,0)
    VERDE2 = (162,255,177)
    AZUL = (0,0,255)

    # Fuentes
    consolas = pygame.font.match_font('consolas')
    times = pygame.font.match_font('times')

    # Sonidos
    pygame.mixer.init() # Iniciamos el mixer de pygame
    sonidoDisparo = pygame.mixer.Sound("../Sonidos/Disparo.wav")
    impactoDisparo = pygame.mixer.Sound("../Sonidos/ImpactoDisparo.wav")
    sonidoHerido = pygame.mixer.Sound("../Sonidos/Herido.wav")
    sonidoCuracion = pygame.mixer.Sound("../Sonidos/Curacion.wav")
    ambiente = pygame.mixer.Sound("../Sonidos/Ambiente.mp3") # Por ejemplo

    # Para activar la música de ambiente es tán sencillo como descargar un sonido adecuado
    ambiente.play()

    class Personaje(pygame.sprite.Sprite):

        # Sprite del personaje
        def __init__(self):

            # Heredamos el init de la clase Sprite de Pygame
            super().__init__()

            # Rectángulo (personaje), recordemos que las imágenes en Pygame son rectángulos
            self.image = pygame.image.load("../Imagenes/Personaje.png").convert() # Convertimos la imagen a tipo Pygame para que el rendimiento mejore

            self.image.set_colorkey(VERDE) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # Obtiene el rectángulo (sprite) de la imagen del personaje para poder manipularlo
            self.rect = self.image.get_rect()

            # Vamos a utilizar la técnica matemática CIRCULAR BOUNDING BOX para mejorar las colisiones
            self.radius = 35 # Establecemos el radio

            self.rect.center = (400,600) # Podemos colocar el rectángulo en la posición inicial que queramos

            # Velocidad del personaje (inicial), inicialmente el personaje va a estar quieto
            self.velocidad_x = 0 
            self.velocidad_y = 0

            # Barra de salud
            self.salud = 100

            # Añadimos vidas
            self.vidas = 3

            # A qué dirección está apuntando actualmente el personaje
            self.direccionApuntado = "derecha" # Inicialmente siempre apunta a la derecha

        def update(self):

            # Velocidad predeterminada cada vuelta del bucle si no pulsas nada
            self.velocidad_x = 0 # Con esto se evita que el personaje se mueva de manera indefinida si no estamos pulsando nada
            self.velocidad_y = 0

            # Actualiza la posición del personaje
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            # Limita el margen izquierdo
            if self.rect.left < 0: # Cada vez que toque el borde izquierdo e intente salir de la screen 
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

            if "izquierda" in movimiento and self.direccionApuntado == "derecha":
                # Modificamos la orientación del personaje
                self.image = pygame.image.load("../Imagenes/PersonajeGirado.png").convert()
                self.image.set_colorkey(VERDE)
                self.direccionApuntado = "izquierda"
            elif "derecha" in movimiento and self.direccionApuntado == "izquierda":
                # Modificamos la orientación del personaje
                self.image = pygame.image.load("../Imagenes/Personaje.png").convert()
                self.image.set_colorkey(VERDE)
                self.direccionApuntado = "derecha"

            # Mueve el personaje hacia la izquierda
            if movimiento == 'izquierda':
                self.velocidad_x = -125 # Cada vez que se pulse la tecla se moverá 100px a la izquierda
            
            # Mueve el personaje hacia la derecha
            elif movimiento == 'derecha':
                self.velocidad_x = 125

            # Mueve el personaje hacia arriba
            elif movimiento == 'arriba':
                self.velocidad_y = -125 # Cada vez que se pulse la tecla se moverá 100px hacia arriba
            
            # Mueve el personaje hacia abajo
            elif movimiento == 'abajo':
                self.velocidad_y = 125

            # Mueve el personaje hacia arriba a la izquierda
            elif movimiento == 'arriba izquierda':
                self.velocidad_x = -125
                self.velocidad_y = -125
            
            # Mueve el personaje hacia arriba a la derecha
            elif movimiento == 'arriba derecha':
                self.velocidad_x = 125
                self.velocidad_y = -125

            # Mueve el personaje hacia abajo a la izquierda
            elif movimiento == 'abajo izquierda':
                self.velocidad_y = 125
                self.velocidad_x = -125
            
            # Mueve el personaje hacia abaja a la derecha
            elif movimiento == 'abajo derecha':
                self.velocidad_y = 125
                self.velocidad_x = 125

            # Actualiza la posición del personaje
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

        def disparo(self, direccion):
            if direccion == "derecha":
                if self.direccionApuntado == "izquierda": 
                    # Modificamos la orientación del personaje
                    self.image = pygame.image.load("../Imagenes/Personaje.png").convert()
                    self.image.set_colorkey(VERDE)
                bala = Disparo(self.rect.right -29 , self.rect.centery -13, direccion)
                spritesBalas.add(bala)
                sonidoDisparo.play() # Para activar el sonido al disparar
                self.direccionApuntado = "derecha"
            elif direccion == "izquierda":
                if self.direccionApuntado == "derecha":
                    # Modificamos la orientación del personaje
                    self.image = pygame.image.load("../Imagenes/PersonajeGirado.png").convert()
                    self.image.set_colorkey(VERDE)
                bala = Disparo(self.rect.left +7 , self.rect.centery -13, direccion)
                spritesBalas.add(bala)
                sonidoDisparo.play() # Para activar el sonido al disparar
                self.direccionApuntado = "izquierda"

    class Enemigo(pygame.sprite.Sprite):

        # Sprite del enemigo
        def __init__(self, colorFondo, nivel):

            # Heredamos el init de la clase Sprite de Pygame
            super().__init__()

            # Nivel del enemigo
            self.nivel = nivel

            # Dependiendo del nivel del enemigo creado le asignamos una imagen y otra, y una velocidad u otra
            if nivel == 1:
                self.rutaImagen = "../Imagenes/Enemigo1.png"
                self.rutaImagenGirada = "../Imagenes/Enemigo1Girado.png"
                self.salud = 15 # Barra de vida
            elif nivel == 2:
                self.rutaImagen = "../Imagenes/Enemigo2.png"
                self.rutaImagenGirada = "../Imagenes/Enemigo2Girado.png"
                self.salud = 30 # Barra de vida
            elif nivel == 3:
                self.rutaImagen = "../Imagenes/Enemigo3.png"
                self.rutaImagenGirada = "../Imagenes/Enemigo3Girado.png"
                self.salud = 45 # Barra de vida

            # Rectángulo (enemigo), recordemos que las imágenes en Pygame son rectángulos
            self.image = pygame.transform.scale(pygame.image.load(self.rutaImagen).convert(), (79, 117)) # Cargamos la imagen y la redimensionamos a 10px de ancho y 20px de alto

            # Color de fondo de la imagen
            self.colorFondo = colorFondo

            self.image.set_colorkey(colorFondo) # Con esta función podemos eliminar el color indicado por parámetro de la imagen+

            # Obtiene el rectángulo (sprite) de la imagen del personaje para poder manipularlo
            self.rect = self.image.get_rect()

            # Vamos a utilizar la técnica matemática CIRCULAR BOUNDING BOX para mejorar las colisiones
            self.radius = 35 # Establecemos el radio

            # Hacemos que el enemigo aparezca de forma aleatoria de la mitad hacia arriba de la ventana de pygame
            self.rect.x = random.randrange(ANCHO - self.rect.width) # Con esto vamos a poner como coordenada X del sprite un número aleatorio entre todos los píxeles del ancho de la screen y además controlamos que no se coloque fuera de los márgenes de la screen ya que tendrá en cuenta el ancho del propio rectángulo
            self.rect.y = random.randrange(ALTO/2 - self.rect.height) # Con esto hacemos lo mismo pero para la coordenada Y, pero limitando a la mitad de la ventana

            # Velocidad inicial del enemigo para que se mueva sin que tenga que ocurrir nada antes
            self.velocidad_x = 1
            self.velocidad_y = 1

        def update(self):

            # Actualiza la velocidad del enemigo
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            # Limita el margen izquierdo y hacemos que el enemigo rebote
            if self.rect.left < 0: # Cada vez que toque el borde izquierdo e intente salir de la screen 
                self.velocidad_x += 1 # Hacemos que rebote
                # Modificamos la imagen para reflejar el cambio de orientación
                self.image = pygame.transform.scale(pygame.image.load(self.rutaImagen).convert(), (79, 117)) # Cargamos la imagen y la redimensionamos a 10px de ancho y 20px de alto
                self.image.set_colorkey(self.colorFondo) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # Limita el margen derecho
            if self.rect.right > ANCHO:
                self.velocidad_x -= 1
                # Modificamos la imagen para reflejar el cambio de orientación
                self.image = pygame.transform.scale(pygame.image.load(self.rutaImagenGirada).convert(), (79, 117)) # Cargamos la imagen y la redimensionamos a 10px de ancho y 20px de alto
                self.image.set_colorkey(self.colorFondo) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # Limita el margen inferior
            if self.rect.bottom > ALTO:
                self.velocidad_y -= 1

            # Limita el margen superior
            if self.rect.top < 0:
                self.velocidad_y += 1

    class Disparo(pygame.sprite.Sprite):

        def __init__(self, x, y, direccionDisparo): # Los parámetros x e y son para indicar la posición exacta de la zona donde se van a generar los disparos
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load("../Imagenes/bala.png").convert(), (20, 20)) # Cargamos la imagen y la redimensionamos a 10px de ancho y 20px de alto
            self.image.set_colorkey(VERDE)
            self.rect = self.image.get_rect() # Obtenemos el rectángulo de la imagen
            self.rect.x = x
            self.rect.y = y
            self.direccion = direccionDisparo
                    
        def update(self):
            if self.direccion == "derecha":
                self.rect.x += 25
                if self.rect.x > ANCHO: # Cuando la bala salga por la parte derecha de la screen
                    self.kill() # Elimina dicha bala
            elif self.direccion == "izquierda":
                self.rect.x -= 25
                if self.rect.x < 0: # Cuando la bala salga por la parte izquierda de la screen
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
            self.rect.x = random.randrange(ANCHO - self.rect.width) # Posición inicial en x que van a tomar los virus instanciados evitando que se generen a medio trozo de la screen
            self.rect.y = -self.rect.width # Evitamos que se genere por dentro de la screen
            self.rect.y = 0
            self.velocidad_y = random.randrange(1, 2)
        
        def update(self):
            self.rect.y += self.velocidad_y # Para que vaya el virus hacia abajo
            if self.rect.top > ALTO: # Si el virus desaparece de la screen por debajo, entonces que vuelva a tomar los valores iniciales
                self.rect.x = random.randrange(ANCHO - self.rect.width)
                self.rect.y = -self.rect.width
                # ANCHO
                self.velocidad_y = random.randrange(1, 2) # Y además que vuelva a tomar una velocidad aleatoria diferente

    class Botiquin(pygame.sprite.Sprite):
        def __init__(self):

            super().__init__()

            self.image = pygame.transform.scale(pygame.image.load("../Imagenes/Botiquin.png").convert(), (32,32))
            self.radius = 16
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(ANCHO - self.rect.width) # Posición inicial en la coordenada "x" que van a tomar los botiquines instanciados evitando que se generen a medio trozo de la screen
            self.rect.y = -self.rect.width # Posicion inicial en la coordenada "y". Evitamos que se genere por dentro de la screen
            self.velocidad_y = 1
        
        def update(self):
            self.rect.y += self.velocidad_y # Para que vaya el botiquin hacia abajo
            if self.rect.top > ALTO: # Si el botiquin desaparece de la screen por debajo, entonces que vuelva a tomar los valores iniciales
                self.rect.x = random.randrange(ANCHO - self.rect.width)
                self.rect.y = -self.rect.width

    def show_text(screen, font, text, colour, sizes, x, y): 
        font_type = pygame.font.Font(font, sizes) # Las dimensiones son el tamaño en px de la fuente
        surface = font_type.render(text, True, colour) # Creamos una variable para mostrar el texto, el True es si queremos que use antialiasing
        rectangle = surface.get_rect()
        rectangle.center = (x,y) # Para poder manipular la posición de dicho rectángulo
        screen.blit(surface, rectangle) # Para que finalmente se pueda mostrar en la screen

    def barra_salud(screen, x, y, salud):
        length = 200
        width = 25
        calculo_barra = int((salud / 100) * length) # Calculamos el porcentaje vida respecto a la longitud de la barra
        border = pygame.Rect(x, y, length, width) # Creamos un borde para la barra de vida
        rectangulo = pygame.Rect(x, y, calculo_barra, width) # Creamos el rectángulo de la barra de vida
        pygame.draw.rect(screen, VERDE2, border, 3)
        pygame.draw.rect(screen, VERDE, rectangulo)


    mensaje = queue.get() # Esperamos hasta que se inicie la skill

    if mensaje == 'Init':

        # Iniciación de Pygame, creación de la ventana, título y control de reloj.
        pygame.init()
        screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Voz Letal")
        clock = pygame.time.Clock() # Para controlar los FPS

        bombilla.turnOn() # Encendemos la bombilla

        bombilla.setColor(0, 0)
        bombilla.setBrightness(50) # Establecemos el brillo de la bombilla al 50%

        # Sistema de puntuaciones
        puntos = 0

        # Grupo de sprites
        sprites = pygame.sprite.Group() # Se agrupan los sprites para que trabajen en un conjunto y se almacene en la variable que queramos
        spritesEnemigosNivel1 = pygame.sprite.Group() # Como vamos a utilizar las colisiones necesitamos tener un grupo dedicado a los enemigos
        spritesEnemigosNivel2 = pygame.sprite.Group() # Como vamos a utilizar las colisiones necesitamos tener un grupo dedicado a los enemigos
        spritesEnemigosNivel3 = pygame.sprite.Group() # Como vamos a utilizar las colisiones necesitamos tener un grupo dedicado a los enemigos
        spritesBalas = pygame.sprite.Group()
        spritesVirus = pygame.sprite.Group() 
        spritesBotiquines = pygame.sprite.Group()

        personaje = Personaje()
        sprites.add(personaje) # Al grupo le añadimos personaje, para que tenga la imagen del personaje

        fondo = pygame.image.load("../Imagenes/Fondo.png").convert() # Cargamos la imagen de fondo del videojuego

        posibles_movimientos = ["arriba", "abajo", "izquierda", "derecha", "abajo derecha", "abajo izquierda", "arriba derecha", "arriba izquierda"]

        # Bucle de juego
        ejecutando = True
        while ejecutando:

            screen.blit(pygame.transform.scale(fondo, (800,600)), (0,0)) # Para añadir un fondo de nuestra elección usar esta línea

            if queue.qsize() > 0: # Nos aseguramos que la cola tenga elementos antes de intentar obtener uno de ellos

                mensaje = queue.get_nowait()

                # Si recibimos un mensaje de texto
                if isinstance(mensaje, str):

                    if mensaje == 'Endgame': # Si se recibe el mensaje Endgame es para indicarnos que termine la ejecución del juego

                        bombilla.setColor(0, 100) # Ponemos la bombilla de color rojo para indicar que hemos perdido la partida o está se ha terminado precipitadamente

                        show_text(screen, times, "GAME OVER", ROJO, 100, 400, 300)

                        pygame.display.update() 
                        time.sleep(5)
                        ejecutando = False # Indicamos que el bucle de juego va a terminar

                    elif mensaje in posibles_movimientos: # Si se nos ha pedido mover el personaje
                        
                        personaje.ejecutaMovimiento(mensaje)

                    elif "dispara" in mensaje:

                        if mensaje == "dispara derecha":
                            personaje.disparo("derecha")

                        elif mensaje == "dispara izquierda":
                            personaje.disparo("izquierda")
                        
                        elif mensaje == "dispara direccion actual":
                            if personaje.direccionApuntado == "derecha":
                                personaje.disparo("derecha")
                            elif personaje.direccionApuntado == "izquierda":
                                personaje.disparo("izquierda")

            # Es lo que especifica la velocidad del bucle de juego
            clock.tick(FPS)

            # Eventos
            for event in pygame.event.get(): # Obtenemos una lista de todos los eventos en la cola de eventos de Pygame, que incluyen eventos del teclado, del mouse, de la ventana, etc.
                if event.type == pygame.QUIT: # Si el evento es de tipo `QUIT` indica que el usuario ha hecho clic en el botón "X" para cerrar la ventana.
                    ejecutando = False

            # Actualización de sprites
            sprites.update() # Con esto podemos hacer que todos los sprites (imágenes) se vayan actualizando en la screen
            spritesEnemigosNivel1.update()
            spritesEnemigosNivel2.update()
            spritesEnemigosNivel3.update()
            spritesBalas.update()
            spritesVirus.update()
            spritesBotiquines.update()

            # Instanciación de los virus
            if not spritesVirus:
                for x in range(2):
                    virus = Virus()
                    spritesVirus.add(virus)

            # Instanciación de los botiquines
            if not spritesBotiquines:
                botiquin = Botiquin()
                spritesBotiquines.add(botiquin)

            # ESTO ES PARA HACER PRUEBAS PARA QUE EL JUEGO NO SE QUEDE VACÍO AL ACABAR CON TODOS LOS ENEMIGOS
            if not spritesEnemigosNivel1 and not spritesEnemigosNivel2 and not spritesEnemigosNivel3:

                enemigoNivel1 = Enemigo(AZUL, 1)
                spritesEnemigosNivel1.add(enemigoNivel1)

                enemigoNivel2 = Enemigo(VERDE, 2)
                spritesEnemigosNivel2.add(enemigoNivel2)

                enemigoNivel3 = Enemigo(VERDE, 3)
                spritesEnemigosNivel3.add(enemigoNivel3)

            colision_disparos_virus = pygame.sprite.groupcollide(spritesVirus, spritesBalas, True, True, pygame.sprite.collide_circle)

            if colision_disparos_virus:
                impactoDisparo.play()
                puntos += 100

            colision_personaje_virus = pygame.sprite.spritecollide(personaje, spritesVirus, True, pygame.sprite.collide_circle)

            if colision_personaje_virus:
                bombilla.setColor(0, 100) # Ponemos la bombilla de color rojo para indicar que el personaje ha sido herido
                sonidoHerido.play()
                personaje.salud -= 50
                if puntos >= 0:
                    puntos -= 100
                    if puntos < 0:
                        puntos = 0
                bombilla.setColor(0, 0) # Volvemos al color blanco por defecto de la partida

            colision_personaje_botiquines = pygame.sprite.spritecollide(personaje, spritesBotiquines, True, pygame.sprite.collide_circle)

            if colision_personaje_botiquines:
                bombilla.setColor(120, 100) # Ponemos la bombilla de color verde para indicar la curación
                sonidoCuracion.play()
                personaje.salud += 10
                if personaje.salud > 100:
                    personaje.salud = 100
                bombilla.setColor(0, 0) # Volvemos al color blanco por defecto de la partida

            colision_personaje_enemigosNivel1 = pygame.sprite.spritecollide(personaje, spritesEnemigosNivel1, True, pygame.sprite.collide_circle) 
            if colision_personaje_enemigosNivel1:
                bombilla.setColor(0, 100) # Ponemos la bombilla de color rojo para indicar que el personaje ha sido herido
                sonidoHerido.play()
                # Podemos añadir una animación de explosión o de contacto
                personaje.salud -= 15
                if puntos >= 0: 
                    puntos -= 50
                    if puntos < 0: # Para evitar que aparezca una puntuación negativa
                        puntos = 0
                bombilla.setColor(0, 0) # Volvemos al color blanco por defecto de la partida

            colision_personaje_enemigosNivel2 = pygame.sprite.spritecollide(personaje, spritesEnemigosNivel2, True, pygame.sprite.collide_circle) 
            if colision_personaje_enemigosNivel2:
                bombilla.setColor(0, 100) # Ponemos la bombilla de color rojo para indicar que el personaje ha sido herido
                sonidoHerido.play() 
                # Podemos añadir una animación de explosión o de contacto
                personaje.salud -= 25
                if puntos >= 0: 
                    puntos -= 100
                    if puntos < 0: # Para evitar que aparezca una puntuación negativa
                        puntos = 0
                bombilla.setColor(0, 0) # Volvemos al color blanco por defecto de la partida


            colision_personaje_enemigosNivel3 = pygame.sprite.spritecollide(personaje, spritesEnemigosNivel3, True, pygame.sprite.collide_circle) 
            if colision_personaje_enemigosNivel3:
                bombilla.setColor(0, 100) # Ponemos la bombilla de color rojo para indicar que el personaje ha sido herido
                sonidoHerido.play() 
                # Podemos añadir una animación de explosión o de contacto
                personaje.salud -= 35
                if puntos >= 0: 
                    puntos -= 150
                    if puntos < 0: # Para evitar que aparezca una puntuación negativa
                        puntos = 0
                bombilla.setColor(0, 0) # Volvemos al color blanco por defecto de la partida

            colision_disparos_enemigosNivel1 = pygame.sprite.groupcollide(spritesEnemigosNivel1, spritesBalas, False, True, pygame.sprite.collide_circle) 
            
            if colision_disparos_enemigosNivel1:
                puntos += 100
                impactoDisparo.play()
                enemigoNivel1.salud -= 15

            if enemigoNivel1.salud <= 0:
                enemigoNivel1.kill()

            colision_disparos_enemigosNivel2 = pygame.sprite.groupcollide(spritesEnemigosNivel2, spritesBalas, False, True, pygame.sprite.collide_circle)

            if colision_disparos_enemigosNivel2:
                puntos += 150
                impactoDisparo.play()
                enemigoNivel2.salud -= 15

            if enemigoNivel2.salud <= 0:
                enemigoNivel2.kill()
            
            colision_disparos_enemigosNivel3 = pygame.sprite.groupcollide(spritesEnemigosNivel3, spritesBalas, False, True, pygame.sprite.collide_circle)
            
            if colision_disparos_enemigosNivel3:
                puntos += 200
                impactoDisparo.play()
                enemigoNivel3.salud -= 15

            if enemigoNivel3.salud <= 0:
                enemigoNivel3.kill()

            # Fondo de screen, dibujo de sprites y formas geométricas
            sprites.draw(screen) # Dibujamos los sprites en la screen
            spritesEnemigosNivel1.draw(screen)
            spritesEnemigosNivel2.draw(screen)
            spritesEnemigosNivel3.draw(screen)
            spritesBalas.draw(screen)
            spritesVirus.draw(screen)
            spritesBotiquines.draw(screen)

            advertencia = pygame.image.load("../Imagenes/WarningMini.png").convert()
            advertencia.set_colorkey(VERDE)

            screen.blit(pygame.transform.scale(personaje.image, (24,24)), (515,15))
            screen.blit(pygame.transform.scale(personaje.image, (24,24)), (480,15))
            screen.blit(pygame.transform.scale(personaje.image, (24,24)), (445,15))
            cruz_roja = pygame.image.load("../Imagenes/Cruz.png").convert()
            cruz_roja.set_colorkey(VERDE)

            if personaje.salud < 30:
                screen.blit(pygame.transform.scale(advertencia, (24,24)), (545,15))

            if personaje.salud <= 0 and personaje.vidas == 3:
                personaje.kill() # Eliminamos al personaje de la partida
                personaje = Personaje() # Y lo respawneamos
                sprites.add(personaje)
                personaje.vidas = 2

            if personaje.vidas == 2:
                if personaje.salud <= 0:
                    personaje.kill() # Eliminamos al personaje de la partida
                    personaje = Personaje() # Y lo respawneamos
                    sprites.add(personaje)
                    personaje.vidas = 1
                screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (515,15))

            if personaje.vidas == 1:
                if personaje.salud <= 0:
                    personaje.kill() # Eliminamos al personaje de la partida
                    personaje = Personaje() # Y lo respawneamos
                    sprites.add(personaje)
                    personaje.vidas = 0
                screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (515,15))
                screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (480,15))

            if personaje.vidas == 0:
                if personaje.salud <= 0:
                    personaje.kill() # Eliminamos al personaje de la partida
                    personaje.salud = 0
                screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (515,15))
                screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (480,15))
                screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (445,15))

                peticion_endgame = False
                while peticion_endgame == False:

                    bombilla.setColor(0, 100) # Ponemos la bombilla de color rojo para indicar que hemos perdido la partida

                    show_text(screen, times, "GAME OVER", ROJO, 100, 400, 300)


                    pygame.display.update()

                    mensaje = queue.get() # Bloqueamos el hilo de ejecución a la espera de la solicitud de fin del juego
                    if mensaje == 'Endgame':
                        peticion_endgame = True
                        ejecutando = False # Indicamos que el bucle de juego va a terminar

            # Si se alcanza una puntuación de 1000 se gana la partida
            if puntos >= 1000:
                
                bombilla.setColor(120, 100) # Ponemos la bombilla de color verde para indicar que hemos ganado la partida

                peticion_endgame = False
                while peticion_endgame == False:

                    show_text(screen, times, "HAS GANADO", VERDE, 100, 400, 300)

                    pygame.display.update()

                    mensaje = queue.get() # Bloqueamos el hilo de ejecución a la espera de la solicitud de fin del juego
                    if mensaje == 'Endgame':
                        peticion_endgame = True
                        ejecutando = False # Indicamos que el bucle de juego va a terminar

            # Dibuja los textos en la screen
            show_text(screen, consolas, str(puntos).zfill(4), ROJO, 40, 680, 60) # Mostramos la puntuación en la screen

            # Mostramos la barra del personaje actualizada
            barra_salud(screen, 580, 15, personaje.salud)

            # Actualizamos el contenido de la screen
            pygame.display.flip() # Permite que solo una porción de la screen se actualice, en lugar de toda el área de la screen. Si no se pasan argumentos, se actualizará la superficie completa.
        
        bombilla.setColor(0,0)
        bombilla.turnOff() # Apagamos la bombilla
        pygame.quit()

@ask.launch # Para cuando el usuario lanza la skill
def start_skill():
    # Creamos el hilo de Pygame y lo iniciamos
    pygame_thread = Thread(target=game_thread, args=(queue,))
    pygame_thread.start()
    # Indicamos a pygame que inicie el videojuego
    queue.put('Init')
    return question('Bienvenido a Voz Letal. ¿Deseas moverte o disparar?') \
        .reprompt("Dígame a dónde quiere moverse o disparar.")

lista_direcciones = ["arriba", "abajo", "izquierda", "derecha", "arriba izquierda", "arriba derecha", "abajo derecha", "abajo izquierda"]

@ask.intent('MovementIntent')
def realiza_movimiento(direccion):
    if direccion not in lista_direcciones:
        return question("Perdone, no le he entendido")
    # Indicamos al videojuego en qué dirección queremos que se mueva el personaje
    queue.put(direccion)
    return question('Te mueves hacia ' + direccion)

@ask.intent('ShootIntent', default={'direccion':'direccion actual'})
def realiza_disparo(direccion):
    if direccion != "derecha" and direccion != "izquierda" and direccion != "direccion actual":
        return question("Lo siento, sólo se puede disparar a derecha o izquierda")
    # Indicamos al videojuego que dispare
    queue.put("dispara " + direccion)
    return question('Disparas a la ' + direccion)

@ask.intent('AMAZON.StopIntent')
def paraEjecucion():
    queue.put('Endgame')
    return statement('Fin del juego.')

@ask.intent('EndgameIntent')
def endgame():
    queue.put('Endgame')
    return statement('Fin del juego.')

@ask.session_ended
def session_ended():
    queue.put('Endgame')
    return "{}", 200

# Definimos la ruta para la página principal de la aplicación web
@app.route('/')
def index():
    return 'Esta es la homepage del videojuego Voz Letal.'

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False) # Si desactivamos el modo debug evitamos que nos abra 2 ventanas de pygame