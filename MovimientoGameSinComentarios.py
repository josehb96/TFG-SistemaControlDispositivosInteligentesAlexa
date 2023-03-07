from flask import Flask
from flask_ask import Ask, statement, question
import pygame 
from queue import Queue
from threading import Thread
import time

app = Flask(__name__)
ask = Ask(app, '/')

queue = Queue()

def game_thread(queue):

    ANCHO = 800
    ALTO = 600

    FPS = 30

    NEGRO = (0,0,0)
    BLANCO = (255,255,255)
    ROJO = (255,0,0)
    H_FA2F2F = (250,47,47)
    VERDE = (0,255,0)
    AZUL = (0,0,255)
    H_50D2FE = (94,210,254)
    AZUL2 = (64,64,255)
    
    class Jugador(pygame.sprite.Sprite):

        def __init__(self):

            super().__init__()

            self.image = pygame.image.load("Imagenes/Personaje.png").convert()

            self.image.set_colorkey(VERDE)

            self.rect = self.image.get_rect()

            self.rect.center = (ANCHO // 2, ALTO // 2)

            self.velocidad_x = 0
            self.velocidad_y = 0

        def update(self):

            self.velocidad_x = 0 
            self.velocidad_y = 0

            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_a]:
                self.velocidad_x = -10
            
            if teclas[pygame.K_d]:
                self.velocidad_x = 10

            if teclas[pygame.K_w]:
                self.velocidad_y = -10
            
            if teclas[pygame.K_s]:
                self.velocidad_y = 10

            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > ANCHO:
                self.rect.right = ANCHO

            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

            if self.rect.top < 0:
                self.rect.top = 0

        def ejecutaMovimiento(self, movimiento):

            self.velocidad_x = 0
            self.velocidad_y = 0

            if movimiento == 'Left':
                self.velocidad_x = -50
            
            elif movimiento == 'Right':
                self.velocidad_x = 50

            elif movimiento == 'Up':
                self.velocidad_y = -50
            
            elif movimiento == 'Down':
                self.velocidad_y = 50

            elif movimiento == 'UpLeft':
                self.velocidad_x = -50
                self.velocidad_y = -50 
            
            elif movimiento == 'UpRight':
                self.velocidad_x = 50
                self.velocidad_y = -50

            elif movimiento == 'DownLeft':
                self.velocidad_y = 50
                self.velocidad_x = -50
            
            elif movimiento == 'DownRight':
                self.velocidad_y = 50
                self.velocidad_x = 50

            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > ANCHO:
                self.rect.right = ANCHO

            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

            if self.rect.top < 0:
                self.rect.top = 0

    ejecutando = True
    while ejecutando:

        mensaje = queue.get()

        if mensaje is None:
            break
        if isinstance(mensaje, str):

            if mensaje == 'Init':

                pygame.init()
                pantalla = pygame.display.set_mode((ANCHO, ALTO))
                pygame.display.set_caption("Movimiento")
                clock = pygame.time.Clock()

                font = pygame.font.SysFont(None, 100)

                sprites = pygame.sprite.Group()
                jugador = Jugador()
                sprites.add(jugador)

            elif mensaje == 'Endgame':

                text = font.render('ENDGAME', True, ROJO)

                text_width, text_height = font.size("ENDGAME")

                x = (ANCHO - text_width) // 2
                y = (ALTO - text_height) // 2

                screen = pygame.display.get_surface()
                screen.blit(text, (x,y))
                pygame.display.update()
                time.sleep(5)

            elif mensaje == 'Up' or mensaje == 'Down' or mensaje == 'Left' or mensaje == 'Right' or mensaje == 'UpLeft' or mensaje == 'UpRight' or mensaje == 'DownLeft' or mensaje == 'DownRight': # Si se nos ha pedido mover el personaje
                
                jugador.ejecutaMovimiento(mensaje)

                sprites.draw(pantalla)

                sprites.update()

                pygame.display.flip()

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False

        sprites.update()

        pantalla.fill(NEGRO)
        sprites.draw(pantalla)
        pygame.draw.line(pantalla, H_50D2FE, (400, 0), (400, 800), 1)
        pygame.draw.line(pantalla, AZUL, (0, 300), (800, 300), 1)

        pygame.display.flip()

    pygame.quit()

game_thread = Thread(target=game_thread, args=(queue,))
game_thread.start()

@ask.launch 
def start_skill():
    queue.put('Init')
    return question('Bienvenido al videojuego Movimiento. Dime en qué dirección quieres moverte.')

@ask.intent('UpIntent')
def arriba():
    queue.put('Up')
    return question('El personaje se mueve hacia arriba.')

@ask.intent('DownIntent')
def abajo():
    queue.put('Down')
    return question('El personaje se mueve hacia abajo.')

@ask.intent('RightIntent')
def derecha():
    queue.put('Right')
    return question('El personaje se mueve hacia la derecha.')

@ask.intent('LeftIntent')
def izquierda():
    queue.put('Left')
    return question('El personaje se mueve hacia la izquierda.')

@ask.intent('UpLeftIntent')
def arribaIzquierda():
    queue.put('UpLeft')
    return question('El personaje se mueve arriba a la izquierda.')

@ask.intent('UpRightIntent')
def arribaDerecha():
    queue.put('UpRight')
    return question('El personaje se mueve arriba a la derecha.')

@ask.intent('DownLeftIntent')
def arribaIzquierda():
    queue.put('DownLeft')
    return question('El personaje se mueve abajo a la izquierda.')

@ask.intent('DownRightIntent')
def arribaDerecha():
    queue.put('DownRight')
    return question('El personaje se mueve abajo a la derecha.')

@ask.intent('EndgameIntent')
def endgame():
    queue.put('Endgame')
    return statement('Fin del juego.')

@app.route('/')
def index():
    return 'Esta es la homepage del videojuego Movimiento.'

if __name__ == '__main__':

    app.run(debug=False)
    queue.put(None)
    game_thread.join()