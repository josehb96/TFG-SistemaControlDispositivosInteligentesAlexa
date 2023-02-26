from flask import Flask
from flask_ask import Ask, statement, question
import pygame
from queue import Queue
from threading import Thread

app = Flask(__name__)
ask = Ask(app, '/')

# Creamos una cola para compartir información entre los hilos
queue = Queue()

# Función que maneja el hilo de Pygame
def game_thread(queue):
    pygame.init()
    pygame.display.set_mode((640, 480))
    font = pygame.font.SysFont(None, 48)
    while True:
        # Esperamos a recibir un mensaje de la cola
        mensaje = queue.get()
        # Si el mensaje es None, salimos del bucle y terminamos el hilo
        if mensaje is None:
            break
        # Si recibimos un mensaje de texto, lo mostramos en la pantalla
        if isinstance(mensaje, str):
            text = font.render(mensaje, True, (255, 255, 255))
            screen = pygame.display.get_surface()
            screen.blit(text, (200, 200))
            pygame.display.update()

# Creamos el hilo de Pygame y lo iniciamos
game_thread = Thread(target=game_thread, args=(queue,))
game_thread.start()

# Definimos la ruta para el intent HelloWorldIntent
@ask.intent('HelloWorldIntent')
def hello_world():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    queue.put('Hola Mundo Jose')
    return question('Hola Mundo Jose')

@ask.intent('BasketballIntent')
def basketball():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    queue.put('BALONCESTO')
    return question('BALONCESTO')

# Definimos la ruta para la página principal de la aplicación web
@app.route('/')
def index():
    return 'Bienvenido al videojuego Hola Mundo'

if __name__ == '__main__':
    app.run(debug=True)
    # Cuando la aplicación web se detiene, enviamos un mensaje None a la cola
    queue.put(None)
    # Esperamos a que el hilo de Pygame termine
    game_thread.join()
