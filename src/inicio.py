import pygame
import sys
from funciones import *


def boton_menu (texto: str, tam: tuple, coordenadas: tuple, fuente: pygame.font.Font, color: tuple)-> dict:
    """boton menu

    Args:
        texto (str): texto del boton
        tam (tuple): tamaño del boton
        coordenadas (tuple): espacio para el boton
        fuente (pygame.font.Font): fuente del texto
        color (tuple): color

    Returns:
        dict: diccionario con los datos del boton deseado
    """
    sup_texto = fuente.render(texto, True, color)
    rect_texto = sup_texto.get_rect()

    boton = pygame.Surface(tam)#crea una superficie con las caractaristicas indicadas
    rect_boton = boton.get_rect()

    rect_boton.center = coordenadas
    rect_texto.center = rect_boton.center

    boton.blit(sup_texto, rect_boton)

    return {"boton": boton, "rect": rect_boton, "sup_texto": sup_texto, "rect_texto": rect_texto, "color": color}


def botones_inicio(ventana: pygame.surface.Surface, cart_jugar: dict, cart_salir: dict, bot_jugar: dict, bot_salir: dict, tam_ventana: tuple):
    """botones inicio

    Args:
        ventana (pygame.surface.Surface): ventana en la cual imprimir los botones
        cart_jugar (dict): fondo del boton inicio
        cart_salir (dict): fondo del boton salir
        bot_jugar (dict): boton de inicio
        bot_salir (dict): boton de fin
        tam_ventana (tuple): tamalo de la ventana
    """
    cent_ventana = (tam_ventana[0] // 2, tam_ventana[1] // 2)

    ventana.blit(cart_jugar["imagen"], (cent_ventana[0] - 110, -50))
    ventana.blit(cart_salir["imagen"], (cent_ventana[0] - 110, 460))

    ventana.blit(bot_jugar["sup_texto"], bot_jugar["rect"])
    ventana.blit(bot_salir["sup_texto"], bot_salir["rect"])


def activ_botones(bot_jugar: dict, bot_salir: dict, jugar: bool)-> bool:
    """activ botones

    Args:
        bot_jugar (dict): boton de incio
        bot_salir (dict): boton de fin
        jugar (bool): variable en la que se almasena respuesta

    Returns:
        bool: valor para continuar o cerrar la app
    """
    while not jugar:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if punto_en_rec(mouse_pos, bot_jugar["rect"]):
                    jugar = True
                    return jugar
                if punto_en_rec(mouse_pos, bot_salir["rect"]):
                    jugar = False
                    pygame.quit()
                    sys.exit() 


def pantalla_inicio(ventana: pygame.surface.Surface, audio: pygame.mixer.Sound, tam_ventana: tuple, cart_jugar: dict, cart_salir: dict, bot_jugar: dict, bot_salir: dict, jugar: bool):
    """pantalla inicio

    Args:
        ventana (pygame.surface.Surface): ventana en la que imprimir la pantalla 
        audio (pygame.mixer.Sound): musica de fondo deseada
        tam_ventana (tuple): tamaño de la pantalla 
        cart_jugar (dict): fondo del boton de inicio
        cart_salir (dict): fondo del boton de fin
        bot_jugar (dict): boton de inicio
        bot_salir (dict): boton de fin
        jugar (bool): valor de respuesta

    Returns:
        bool: valor para continuar o cerrar la app
    """
    ventana.blit(pygame.transform.scale(pygame.image.load("./src/assets/fondo1.jpg"), tam_ventana), (0, 0))
    ventana.blit(pygame.image.load("./src/assets/onepiece.png"), (150, 75))
    audio.play()

    botones_inicio(ventana, cart_jugar, cart_salir, bot_jugar, bot_salir, tam_ventana)

    pygame.display.flip()

    jugar = activ_botones(bot_jugar, bot_salir, jugar)

    return jugar












