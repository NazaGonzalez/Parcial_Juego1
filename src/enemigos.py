from funciones import *
from config import *
from random import *



# movimiento enemigos
def movimiento_enemigos(lista_enemigos: list, direcciones: tuple, velocidad: int, lista_obstaculos: list, ancho: int, alto: int)-> None:
    """movimiento enemigos

    Args:
        lista_enemigos (list): lista de los enemigos
        direcciones (tuple): direccion de movimiento de los enemigos
        velocidad (int): velocidad de movimiento de los enemigos
        lista_obstaculos (list): lista que representa el laberinto
        ancho (int): ancho de la pantalla 
        alto (int): alto de la pantalla
    """
    for enemigo in lista_enemigos:
        if enemigo["direc"] == direcciones[0]:
            enemigo["rect"].top -= velocidad
        elif enemigo["direc"] == direcciones[1]:
            enemigo["rect"].top += velocidad
        elif enemigo["direc"] == direcciones[2]:
            enemigo["rect"].left += velocidad
        elif enemigo["direc"] == direcciones[3]:
            enemigo["rect"].left -= velocidad

    limites_enemigos(lista_enemigos, direcciones, ancho, alto)

    impacto_enemigos_obstaculos(lista_enemigos, direcciones, lista_obstaculos)


# direccion de los enemigos
def limites_enemigos(lista_enemigos: list, direcciones: tuple, ancho: int, alto: int)-> None:
    """limites enemigos

    Args:
        lista_enemigos (list): lista de los enemigos
        direcciones (tuple): direccion de movimiento de los enemigos
        ancho (int): ancho de pantalla
        alto (int): alto de pantalla
    """
    for enemigo in lista_enemigos:
        if enemigo["rect"].top <= 0:#   choca arriba
            enemigo["rect"].top += 5
            enemigo["direc"] = choice((direcciones[1], direcciones[2], direcciones[3]))
        elif enemigo["rect"].bottom >= alto:#   choca abajo
            enemigo["rect"].top -= 5
            enemigo["direc"] = choice((direcciones[0], direcciones[2], direcciones[3]))
        elif enemigo["rect"].right >= ancho:#   choca a la derecha
            enemigo["rect"].left -= 5
            enemigo["direc"] = choice((direcciones[0], direcciones[1], direcciones[3]))
        elif enemigo["rect"].left <= 0:#   choca a la izquieda
            enemigo["rect"].left += 5
            enemigo["direc"] = choice((direcciones[0], direcciones[1], direcciones[2]))  


# impacto de los enemigos con el laberinto
def impacto_enemigos_obstaculos(lista_enemigos: list, direccion: tuple, lista_obstaculos: list)-> None:
    """impacto enemigos obstaculos

    Args:
        lista_enemigos (list): lista de los enemigos
        direccion (tuple): direccion de movimiento de los enemigos
        lista_obstaculos (list): lista que representa el laberinto
    """
    try:
        for enemigo in lista_enemigos:
            for obstaculo in lista_obstaculos:
                if detectar_choque(enemigo["rect"], obstaculo["rect"]):
                    if enemigo["direc"] == direccion[0]:
                        enemigo["rect"].top += 5
                        enemigo["direc"] = choice((direccion[1], direccion[2], direccion[3]))
                    elif enemigo["direc"] == direccion[1]:
                        enemigo["rect"].top -= 5
                        enemigo["direc"] = choice((direccion[0], direccion[2], direccion[3]))
                    elif enemigo["direc"] == direccion[2]:
                        enemigo["rect"].left -= 5
                        enemigo["direc"] = choice((direccion[0], direccion[1], direccion[3]))
                    elif enemigo["direc"] == direccion[3]:
                        enemigo["rect"].left += 5
                        enemigo["direc"] = choice((direccion[0], direccion[1], direccion[2]))
    except Exception as e:
        print(f"¡Ocurrió un error al detectar colisión de los enemigos!: {e}")            