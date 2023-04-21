from flask import Flask
from flask_ask import Ask, statement, question
import pygame
from queue import Queue
from threading import Thread
import time 
import random
from PyP100 import PyL530 
import os

app = Flask(__name__)
ask = Ask(app, '/')

email = os.getenv('TAPOL530_EMAIL')
password = os.getenv('TAPOL530_PASSWORD')

bombilla = PyL530.L530("192.168.68.100", email, password)

bombilla.handshake() 
bombilla.login() 

queue = Queue()

def game_thread(queue):

    ANCHO = 800
    ALTO = 600

    FPS = 30

    ROJO = (255,0,0)
    VERDE = (0,255,0)
    VERDE2 = (162,255,177)
    AZUL = (0,0,255)

    consolas = pygame.font.match_font('consolas')
    times = pygame.font.match_font('times')

    pygame.mixer.init() 
    sonidoDisparo = pygame.mixer.Sound("../Sonidos/Disparo.wav")
    impactoDisparo = pygame.mixer.Sound("../Sonidos/ImpactoDisparo.wav")
    sonidoHerido = pygame.mixer.Sound("../Sonidos/Herido.wav")
    sonidoCuracion = pygame.mixer.Sound("../Sonidos/Curacion.wav")
    ambiente = pygame.mixer.Sound("../Sonidos/Ambiente.mp3") 

    ambiente.play()

    class Personaje(pygame.sprite.Sprite):

        def __init__(self):

            super().__init__()

            self.image = pygame.image.load("../Imagenes/Personaje.png").convert() 

            self.image.set_colorkey(VERDE) 

            self.rect = self.image.get_rect()

            self.radius = 35 

            self.rect.center = (400,600) 

            self.velocidad_x = 0 
            self.velocidad_y = 0

            self.salud = 100

            self.vidas = 3

            self.direccionApuntado = "derecha" 

        def update(self):

            self.velocidad_x = 0 
            self.velocidad_y = 0

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

            if "izquierda" in movimiento and self.direccionApuntado == "derecha":

                self.image = pygame.image.load("../Imagenes/PersonajeGirado.png").convert()
                self.image.set_colorkey(VERDE)
                self.direccionApuntado = "izquierda"
            elif "derecha" in movimiento and self.direccionApuntado == "izquierda":

                self.image = pygame.image.load("../Imagenes/Personaje.png").convert()
                self.image.set_colorkey(VERDE)
                self.direccionApuntado = "derecha"

            if movimiento == 'izquierda':
                self.velocidad_x = -125 

            elif movimiento == 'derecha':
                self.velocidad_x = 125

            elif movimiento == 'arriba':
                self.velocidad_y = -125 

            elif movimiento == 'abajo':
                self.velocidad_y = 125

            elif movimiento == 'arriba izquierda':
                self.velocidad_x = -125
                self.velocidad_y = -125

            elif movimiento == 'arriba derecha':
                self.velocidad_x = 125
                self.velocidad_y = -125

            elif movimiento == 'abajo izquierda':
                self.velocidad_y = 125
                self.velocidad_x = -125

            elif movimiento == 'abajo derecha':
                self.velocidad_y = 125
                self.velocidad_x = 125

            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

        def disparo(self, direccion):
            if direccion == "derecha":
                if self.direccionApuntado == "izquierda": 

                    self.image = pygame.image.load("../Imagenes/Personaje.png").convert()
                    self.image.set_colorkey(VERDE)
                bala = Disparo(self.rect.right -29 , self.rect.centery -13, direccion)
                spritesBalas.add(bala)
                sonidoDisparo.play() 
                self.direccionApuntado = "derecha"
            elif direccion == "izquierda":
                if self.direccionApuntado == "derecha":

                    self.image = pygame.image.load("../Imagenes/PersonajeGirado.png").convert()
                    self.image.set_colorkey(VERDE)
                bala = Disparo(self.rect.left +7 , self.rect.centery -13, direccion)
                spritesBalas.add(bala)
                sonidoDisparo.play() 
                self.direccionApuntado = "izquierda"

    class Enemigo(pygame.sprite.Sprite):

        def __init__(self, colorFondo, nivel):

            super().__init__()

            self.nivel = nivel

            if nivel == 1:
                self.rutaImagen = "../Imagenes/Enemigo1.png"
                self.rutaImagenGirada = "../Imagenes/Enemigo1Girado.png"
                self.salud = 15 
            elif nivel == 2:
                self.rutaImagen = "../Imagenes/Enemigo2.png"
                self.rutaImagenGirada = "../Imagenes/Enemigo2Girado.png"
                self.salud = 30 
            elif nivel == 3:
                self.rutaImagen = "../Imagenes/Enemigo3.png"
                self.rutaImagenGirada = "../Imagenes/Enemigo3Girado.png"
                self.salud = 45 

            self.image = pygame.transform.scale(pygame.image.load(self.rutaImagen).convert(), (79, 117)) 

            self.colorFondo = colorFondo

            self.image.set_colorkey(colorFondo) 

            self.rect = self.image.get_rect()

            self.radius = 35 

            self.rect.x = random.randrange(ANCHO - self.rect.width) 
            self.rect.y = random.randrange(ALTO/2 - self.rect.height) 

            self.velocidad_x = 1
            self.velocidad_y = 1

        def update(self):

            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            if self.rect.left < 0: 
                self.velocidad_x += 1 

                self.image = pygame.transform.scale(pygame.image.load(self.rutaImagen).convert(), (79, 117)) 
                self.image.set_colorkey(self.colorFondo) 

            if self.rect.right > ANCHO:
                self.velocidad_x -= 1

                self.image = pygame.transform.scale(pygame.image.load(self.rutaImagenGirada).convert(), (79, 117)) 
                self.image.set_colorkey(self.colorFondo) 

            if self.rect.bottom > ALTO:
                self.velocidad_y -= 1

            if self.rect.top < 0:
                self.velocidad_y += 1

    class Disparo(pygame.sprite.Sprite):

        def __init__(self, x, y, direccionDisparo): 
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load("../Imagenes/bala.png").convert(), (20, 20)) 
            self.image.set_colorkey(VERDE)
            self.rect = self.image.get_rect() 
            self.rect.x = x
            self.rect.y = y
            self.direccion = direccionDisparo
                    
        def update(self):
            if self.direccion == "derecha":
                self.rect.x += 25
                if self.rect.x > ANCHO: 
                    self.kill() 
            elif self.direccion == "izquierda":
                self.rect.x -= 25
                if self.rect.x < 0: 
                    self.kill() 

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
            self.rect.x = random.randrange(ANCHO - self.rect.width) 
            self.rect.y = -self.rect.width 
            self.rect.y = 0
            self.velocidad_y = random.randrange(1, 2)
        
        def update(self):
            self.rect.y += self.velocidad_y 
            if self.rect.top > ALTO: 
                self.rect.x = random.randrange(ANCHO - self.rect.width)
                self.rect.y = -self.rect.width

                self.velocidad_y = random.randrange(1, 2) 

    class Botiquin(pygame.sprite.Sprite):
        def __init__(self):

            super().__init__()

            self.image = pygame.transform.scale(pygame.image.load("../Imagenes/Botiquin.png").convert(), (32,32))
            self.radius = 16
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(ANCHO - self.rect.width) 
            self.rect.y = -self.rect.width 
            self.velocidad_y = 1
        
        def update(self):
            self.rect.y += self.velocidad_y 
            if self.rect.top > ALTO: 
                self.rect.x = random.randrange(ANCHO - self.rect.width)
                self.rect.y = -self.rect.width

    def show_text(screen, font, text, colour, sizes, x, y): 
        font_type = pygame.font.Font(font, sizes) 
        surface = font_type.render(text, True, colour) 
        rectangle = surface.get_rect()
        rectangle.center = (x,y) 
        screen.blit(surface, rectangle) 

    def barra_salud(screen, x, y, salud):
        length = 200
        width = 25
        calculo_barra = int((salud / 100) * length) 
        border = pygame.Rect(x, y, length, width) 
        rectangulo = pygame.Rect(x, y, calculo_barra, width) 
        pygame.draw.rect(screen, VERDE2, border, 3)
        pygame.draw.rect(screen, VERDE, rectangulo)

    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Voz Letal")
    clock = pygame.time.Clock() 

    bombilla.turnOn() 

    bombilla.setColor(0, 0)
    bombilla.setBrightness(50) 

    puntos = 0

    sprites = pygame.sprite.Group() 
    spritesEnemigosNivel1 = pygame.sprite.Group() 
    spritesEnemigosNivel2 = pygame.sprite.Group() 
    spritesEnemigosNivel3 = pygame.sprite.Group() 
    spritesBalas = pygame.sprite.Group()
    spritesVirus = pygame.sprite.Group() 
    spritesBotiquines = pygame.sprite.Group()

    personaje = Personaje()
    sprites.add(personaje) 

    fondo = pygame.image.load("../Imagenes/Fondo.png").convert() 

    posibles_movimientos = ["arriba", "abajo", "izquierda", "derecha", "abajo derecha", "abajo izquierda", "arriba derecha", "arriba izquierda"]

    ejecutando = True
    while ejecutando:

        screen.blit(pygame.transform.scale(fondo, (800,600)), (0,0)) 

        if queue.qsize() > 0: 

            mensaje = queue.get_nowait()

            if mensaje in posibles_movimientos: 
                
                personaje.ejecutaMovimiento(mensaje)

            elif "dispara" in mensaje:

                if mensaje == "dispara derecha":
                    personaje.disparo("derecha")

                elif mensaje == "dispara izquierda":
                    personaje.disparo("izquierda")
                
                else:
                    personaje.disparo(personaje.direccionApuntado)

            elif mensaje == 'Endgame': 

                bombilla.setColor(0, 100) 

                show_text(screen, times, "GAME OVER", ROJO, 100, 400, 300)

                pygame.display.update() 
                time.sleep(5)
                ejecutando = False 

        clock.tick(FPS)


        sprites.update() 
        spritesEnemigosNivel1.update()
        spritesEnemigosNivel2.update()
        spritesEnemigosNivel3.update()
        spritesBalas.update()
        spritesVirus.update()
        spritesBotiquines.update()

        if not spritesVirus:
            for x in range(2):
                virus = Virus()
                spritesVirus.add(virus)

        if not spritesBotiquines:
            botiquin = Botiquin()
            spritesBotiquines.add(botiquin)

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
            bombilla.setColor(0, 100) 
            sonidoHerido.play()
            personaje.salud -= 50
            if puntos >= 0:
                puntos -= 100
                if puntos < 0:
                    puntos = 0
            bombilla.setColor(0, 0) 

        colision_personaje_botiquines = pygame.sprite.spritecollide(personaje, spritesBotiquines, True, pygame.sprite.collide_circle)

        if colision_personaje_botiquines:
            bombilla.setColor(120, 100) 
            sonidoCuracion.play()
            personaje.salud += 10
            if personaje.salud > 100:
                personaje.salud = 100
            bombilla.setColor(0, 0) 

        colision_personaje_enemigosNivel1 = pygame.sprite.spritecollide(personaje, spritesEnemigosNivel1, True, pygame.sprite.collide_circle) 
        if colision_personaje_enemigosNivel1:
            bombilla.setColor(0, 100) 
            sonidoHerido.play()

            personaje.salud -= 15
            if puntos >= 0: 
                puntos -= 50
                if puntos < 0: 
                    puntos = 0
            bombilla.setColor(0, 0) 

        colision_personaje_enemigosNivel2 = pygame.sprite.spritecollide(personaje, spritesEnemigosNivel2, True, pygame.sprite.collide_circle) 
        if colision_personaje_enemigosNivel2:
            bombilla.setColor(0, 100) 
            sonidoHerido.play() 

            personaje.salud -= 25
            if puntos >= 0: 
                puntos -= 100
                if puntos < 0: 
                    puntos = 0
            bombilla.setColor(0, 0) 


        colision_personaje_enemigosNivel3 = pygame.sprite.spritecollide(personaje, spritesEnemigosNivel3, True, pygame.sprite.collide_circle) 
        if colision_personaje_enemigosNivel3:
            bombilla.setColor(0, 100) 
            sonidoHerido.play() 

            personaje.salud -= 35
            if puntos >= 0: 
                puntos -= 150
                if puntos < 0: 
                    puntos = 0
            bombilla.setColor(0, 0) 

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

        sprites.draw(screen) 
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
            personaje.kill() 
            personaje = Personaje() 
            sprites.add(personaje)
            personaje.vidas = 2

        elif personaje.vidas == 2:
            if personaje.salud <= 0:
                personaje.kill() 
                personaje = Personaje() 
                sprites.add(personaje)
                personaje.vidas = 1
            screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (515,15))

        elif personaje.vidas == 1:
            if personaje.salud <= 0:
                personaje.kill() 
                personaje = Personaje() 
                sprites.add(personaje)
                personaje.vidas = 0
            screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (515,15))
            screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (480,15))

        elif personaje.vidas == 0:
            if personaje.salud <= 0:
                personaje.kill() 
                personaje.salud = 0
            screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (515,15))
            screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (480,15))
            screen.blit(pygame.transform.scale(cruz_roja, (24,24)), (445,15))

            peticion_endgame = False
            while peticion_endgame == False:

                bombilla.setColor(0, 100) 

                show_text(screen, times, "GAME OVER", ROJO, 100, 400, 300)


                pygame.display.update()

                mensaje = queue.get() 
                if mensaje == 'Endgame':
                    peticion_endgame = True
                    ejecutando = False 

        if puntos >= 1000:
            
            bombilla.setColor(120, 100) 

            peticion_endgame = False
            while peticion_endgame == False:

                show_text(screen, times, "HAS GANADO", VERDE, 100, 400, 300)

                pygame.display.update()

                mensaje = queue.get() 
                if mensaje == 'Endgame':
                    peticion_endgame = True
                    ejecutando = False 

        show_text(screen, consolas, str(puntos).zfill(4), ROJO, 40, 680, 60) 

        barra_salud(screen, 580, 15, personaje.salud)

        pygame.display.flip() 
    
    bombilla.setColor(0,0)
    bombilla.turnOff() 
    pygame.quit()

@ask.launch 
def start_skill():

    pygame_thread = Thread(target=game_thread, args=(queue,))
    pygame_thread.start()

    return question('Bienvenido a Voz Letal. ¿Deseas moverte o disparar?') \
        .reprompt("Dígame a dónde quiere moverse o disparar.")

lista_direcciones = ["arriba", "abajo", "izquierda", "derecha", "arriba izquierda", "arriba derecha", "abajo derecha", "abajo izquierda"]

@ask.intent('MovementIntent')
def realiza_movimiento(direccion):
    if direccion not in lista_direcciones:
        return question("Perdone, no le he entendido")

    queue.put(direccion)
    return question('Te mueves hacia ' + direccion)

@ask.intent('ShootIntent', default={'direccion':'direccion actual'})
def realiza_disparo(direccion):
    if direccion != "derecha" and direccion != "izquierda" and direccion != "direccion actual":
        return question("Lo siento, sólo se puede disparar a derecha o izquierda")

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

@app.route('/')
def index():
    return 'Esta es la homepage del videojuego Voz Letal.'

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False) 