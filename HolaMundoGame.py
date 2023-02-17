from flask import flask, render_template # Importamos la clase Flask del módulo flask y la función render_template que permite renderizar plantillas HTML
from flask_ask import Ask, statement # Importamos la clase Ask del módulo flask_ask y la función statement que crea una respuesta a la solicitud de Alexa
from kasa import SmartPlug # Importamos la clase SmartPlug del módulo kasa que permite controlar dispositivos inteligentes como la bombilla TP-Link
import pygame # Importamos la librería Pygame, que se utilizará para crear el juego

app = Flask