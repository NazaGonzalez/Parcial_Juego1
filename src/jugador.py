import pygame
from funciones import *
from random import *



# direccion del jugador    
def direccion_jugador(direcciones: tuple, personaje: dict, velocidad: int, ancho: int, alto: int)-> None:
    """direccion jugador

    Args:
        direcciones (tuple): direccion de moevimiento del jugador
        personaje (dict): personaje que representa al jugador
        velocidad (int): velocidad de movimiento del jugador
        ancho (int): ancho de pantalla
        alto (int): alto de pantalla
    """
    if direcciones[0] and personaje["rect"].top >= 0:
        personaje["rect"].top -= velocidad
    elif direcciones[1] and personaje["rect"].bottom <= alto:
        personaje["rect"].top += velocidad
    elif direcciones[2] and personaje["rect"].right <= ancho:
        personaje["rect"].left += velocidad
    elif direcciones[3] and personaje["rect"].left >= 0:
        personaje["rect"].left -= velocidad



def choque_jugador_enemigo(ancho_pantalla: int, alto_pantalla: int, lista_enemigos: list, personaje: dict, vidas: int, puntos: int)-> int and int:
    """_summary_

    Args:
        ancho_pantalla (int): ancho de pantalla
        alto_pantalla (int): alto de pantalla
        lista_enemigos (list): lista que contiene a los enemigos
        personaje (dict): personaje que representa al jugador
        vidas (int): cantidad de vidas del jugador
        puntos (int): puntos acumulados del jugador

    Returns:
        int and int: vidas restantes del jugador y sus puntos acumulados
    """
    for enemigo in lista_enemigos:
        try:
            if detectar_choque(enemigo["rect"], personaje["rect"]) and personaje["poder"]:
                enemigo["rect"].left, enemigo["rect"].top = choice(((0, 0), (ancho_pantalla, 0), (0, alto_pantalla), (ancho_pantalla, alto_pantalla)))
                puntos += 3
            elif detectar_choque(enemigo["rect"], personaje["rect"]) and not personaje["poder"]:
                personaje["rect"].left = ancho_pantalla // 2
                personaje["rect"].top = alto_pantalla // 2
                vidas -= 1
        except Exception as e:
            print(f"¡Ocurrió un error al detectar colisión entre entidades!: {e}")
    return vidas, puntos

# ataque
def atacar(atacar: bool, balas: list, direccion: tuple, personaje: dict, trayect: tuple, imagen)-> None:
    """atacar

    Args:
        atacar (bool): valor de la accion de ataque
        balas (list): lista con los proyectiles
        direccion (tuple): direccion de moevimiento del jugador
        personaje (dict): personaje que representa al jugador
        trayect (tuple): trayectoria del proyectil
        imagen (_type_): imagen deseada para el proyectil
    """
    if atacar and len(balas) == 0:
        if direccion[0]:
            balas.append(crear_bloque(personaje["rect"].centerx, personaje["rect"].centery, 20, 20, dir = trayect[0], imagen = imagen))
        elif direccion[1]:
            balas.append(crear_bloque(personaje["rect"].centerx, personaje["rect"].centery, 20, 20, dir = trayect[1], imagen = imagen))
        elif direccion[2]:
            balas.append(crear_bloque(personaje["rect"].centerx, personaje["rect"].centery, 20, 20, dir = trayect[2], imagen = imagen))
        elif direccion[3]:
            balas.append(crear_bloque(personaje["rect"].centerx, personaje["rect"].centery, 20, 20, dir = trayect[3], imagen = imagen))


def disparo_pared(lista_balas: list, lista_paredes: list)-> None:
    """disparo pared

    Args:
        lista_balas (list): lista con los proyectiles
        lista_paredes (list): lista que representa el laberinto
    """
    for proyectil in lista_balas[:]:
        for obstaculo in lista_paredes:
            try:
                if detectar_choque(proyectil["rect"], obstaculo["rect"]):
                    lista_balas.remove(proyectil)
            except Exception as e:
                    print(f"¡Ocurrió un error al detectar la colicion del proyectil con obstaculos!: {e}")


def matar_enemigo(lista_balas: list, lista_enemigos: list, puntos: int)-> int:
    """matar enemigo

    Args:
        lista_balas (list): lista con los proyectiles
        lista_enemigos (list): lista que contiene a los enemigos
        puntos (int): puntos acumulados del jugador

    Returns:
        int: puntos restantes del jugador
    """
    for proyectil in lista_balas[:]:
        for enemigo in lista_enemigos:
            try:
                if detectar_choque(proyectil["rect"], enemigo["rect"]):
                    lista_balas.remove(proyectil)
                    enemigo["rect"].left, enemigo["rect"].top = choice(((0, 0), (800, 0), (0, 600), (800, 600)))
                    puntos += 3
            except Exception as e:
                print(f"¡Ocurrió un error al detectar la colisión del proyectil con el enemigo!: {e}")
    return puntos


# mov proyectil
def movimiento_balas(lista_balas: list, direcciones: tuple, velocidad: int, lista_paredes: list, lista_enemigos: list, puntos: int, ancho: int, alto: int)-> int:
    """movimiento balas

    Args:
        lista_balas (list): lista con los proyectiles
        direcciones (tuple): direcciones del proyectil
        velocidad (int): velocidad del proyectil
        lista_paredes (list): lista que representa el laberinto
        lista_enemigos (list): lista que contiene a los enemigos
        puntos (int): puntos acumulados del jugador
        ancho (int): ancho de pantalla
        alto (int): alto de pantalla

    Returns:
        int: puntos restantes del jugador
    """
    for proyectil in lista_balas[:]:
        if proyectil["direc"] == direcciones[0]:
            proyectil["rect"].top -= velocidad
        elif proyectil["direc"] == direcciones[1]:
            proyectil["rect"].top += velocidad
        elif proyectil["direc"] == direcciones[2]:
            proyectil["rect"].left += velocidad
        elif proyectil["direc"] == direcciones[3]:
            proyectil["rect"].left -= velocidad

        if proyectil["rect"].top < 0 or proyectil["rect"].left < 0 or proyectil["rect"].bottom > alto or proyectil["rect"].right > ancho:
            lista_balas.remove(proyectil)

    disparo_pared(lista_balas, lista_paredes)

    matar_enemigo(lista_balas, lista_enemigos, puntos)

    return puntos


# agarrar poder
def agarrar_poder(lista_poderes: list, personaje: dict, sonido: pygame.mixer.Sound, duracion_poder: int, contador_poder: int, suena_musica: bool)-> int and bool:
    """agarrar poder

    Args:
        lista_poderes (list): lista con las monedas de poder
        personaje (dict): personaje que representa al jugador
        sonido (pygame.mixer.Sound): sonido deseado para la activacion del poder
        duracion_poder (int): tiempo de duracion del poder
        contador_poder (int): contador del tiempo
        suena_musica (bool): valor que defina si se escuchara la musica

    Returns:
        int and bool: tiempo restante al poder y si estaria o no activa la musica
    """
    for p in lista_poderes[:]:
        try:
            if detectar_choque(p["rect"], personaje["rect"]):
                lista_poderes.remove(p)
                contador_poder = duracion_poder
                if not suena_musica:
                    pygame.mixer.music.pause()
                    sonido.play(-1)
                    suena_musica = True
                
        except Exception as e:
            print(f"¡Ocurrió un error al detectar que el jugador consiguio un poder!: {e}")

    return contador_poder, suena_musica


def activar_poder(lista_poderes: list, personaje: dict, sonido: pygame.mixer.Sound, contador_poder: int, suena_musica: bool, duracion_poder: int)-> int and bool:
    """activar poder

    Args:
        lista_poderes (list): lista con las monedas de poder
        personaje (dict): personaje que representa al jugador
        sonido (pygame.mixer.Sound): _description_
        contador_poder (int): sonido deseado para la activacion del poder
        suena_musica (bool): valor que defina si se escuchara la musica
        duracion_poder (int): tiempo de duracion del poder

    Returns:
        int and bool: tiempo restante al poder y si estaria o no activa la musica
    """
    if contador_poder > 0:
        personaje["poder"] = True
        contador_poder -= 1
        if contador_poder <= 0:
            personaje["poder"] = False
            suena_musica = False
            sonido.stop()
            pygame.mixer.music.unpause()
    
    contador_poder, suena_musica = agarrar_poder(lista_poderes, personaje, sonido, duracion_poder, contador_poder, suena_musica)
    
    return contador_poder, suena_musica




