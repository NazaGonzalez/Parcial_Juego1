import pygame
from funciones import *
from random import *



def listar_mapa(mapa: list, tam: float, bloque: int = 1, imagen: pygame.Surface = None)-> list:
    """listar mapa

    Args:
        mapa (list): lsita de lista que represente el laberinto deseado
        tam (float): tamaño deseado de cada bloque
        bloque (int, optional): defina que valor representara un obstaculo. Defaults to 1.
        imagen (pygame.Surface, optional): imagen de cada celda. Defaults to None.

    Returns:
        list: lista de objetos en base a la primer lista
    """
    rects_celdas = []
    for y, fila in enumerate(mapa):#devlovera el contador de integraciones y la tupla con el inidice y valor
        for x, celda in enumerate(fila):
            if celda == bloque:
                rects_celdas.append({"rect": pygame.Rect(x * tam, y * tam, tam, tam), "imagen": imagen})
    
    return rects_celdas


# impaccto de jugador con laberinto
def impacto_obstaculos(direccion: tuple, lista_obstaculos: list, personaje: dict)-> None:
    """impacto con obstaculos

    Args:
        direccion (tuple): direccion de movimiento del personaje
        lista_obstaculos (list): losta que contiene los obstaculos
        personaje (dict): personaje que representa al jugador 
    """
    try:
        if direccion[0]:
            for obstaculo in lista_obstaculos:
                if detectar_choque(personaje["rect"], obstaculo["rect"]):
                    personaje["rect"].top += 5
        elif direccion[1]: 
            for obstaculo in lista_obstaculos:
                if detectar_choque(personaje["rect"], obstaculo["rect"]):
                    personaje["rect"].top -= 5
        elif direccion[2]:
            for obstaculo in lista_obstaculos:
                if detectar_choque(personaje["rect"], obstaculo["rect"]):
                    personaje["rect"].left += 5
        elif direccion[3]:
            for obstaculo in lista_obstaculos:
                if detectar_choque(personaje["rect"], obstaculo["rect"]):
                    personaje["rect"].left -= 5
    except Exception as e:
        print(f"¡Ocurrió un error al detectar colisión del jugador!: {e}")


#imprimir laberinto
def imprimir_mapeado(ventana: pygame.surface.Surface, objetos: list, imagen: pygame.surface.Surface)-> None:
    """imprimir mapeado

    Args:
        ventana (pygame.surface.Surface): pantalla  del juego
        objetos (list): lista que contiene los obstaculos
        imagen (pygame.surface.Surface): imagen deseada
    """
    for objeto in objetos:
        objeto["imagen"] = pygame.transform.scale(imagen, (objeto["rect"].width, objeto["rect"].height))
        ventana.blit(objeto["imagen"], objeto["rect"])


def traga_monedas(lista_monedas: list, lista_poderes: list, personaje: dict, sonido: pygame.mixer.Sound, puntos: int)-> int:
    """traga monedas

    Args:
        lista_monedas (list): lista de monedas de puntos
        lista_poderes (list): lista monedas de poder
        personaje (dict): personaje que representa al jugador
        sonido (pygame.mixer.Sound): sonido de recoleccion de moneda
        puntos (int): puntuacion del jugador

    Returns:
        int: puntos acumulados
    """
    for moneda in lista_monedas[:]:
        for p in lista_poderes:
            try:
                if detectar_choque(moneda["rect"], p["rect"]):
                    lista_monedas.remove(moneda)
            except Exception as e:
                print(f"¡Ocurrió un error al detectar el cambio de moneda por poder!: {e}")
        try:
            if detectar_choque(moneda["rect"], personaje["rect"]):
                lista_monedas.remove(moneda)
                sonido.play()
                puntos += 1
        except Exception as e:
            print(f"¡Ocurrió un error al detectar que el jugador agarro una moneda!: {e}")
    return puntos


def recarga_nivel(lista_monedas: list, personaje: dict, matriz_mapa: list, escala: int, sonido: pygame.mixer.Sound)-> list:
    """recarga nivel

    Args:
        lista_monedas (list): lista de monedas de puntos
        personaje (dict): personaje que representa al jugador
        matriz_mapa (list): matris que representa el mapeado
        escala (int): tamaño de las seldas
        sonido (pygame.mixer.Sound): sonido de victoria

    Returns:
        list: lista de monedas de puntos actualizada
    """

    lista_monedas = listar_mapa(matriz_mapa, escala, 0)
    for moneda in lista_monedas:
            
        moneda["rect"].width = 20
        moneda["rect"].height = 20

        moneda["rect"].top = moneda["rect"].top + 10
        moneda["rect"].left = moneda["rect"].left + 10

    sonido.play()
    personaje["rect"].left = 800 // 2
    personaje["rect"].top = 600 // 2
    personaje["poder"] = False
        
    return lista_monedas


def imprimir_grupo(ventana: pygame.surface.Surface, grupo: list)-> None:
    """imprimir grupo

    Args:
        ventana (pygame.surface.Surface): pantalla de juego
        grupo (list): grupo de items a imprimir
    """
    for unidad in grupo:
            ventana.blit(unidad["imagen"], unidad["rect"])


def imprimir_fotogramas(ventana: pygame.surface.Surface, lista_monedas: list, lista_obstaculos: list, lista_poderes: list, lista_enemigos: list, personaje: dict, lista_balas: list, foto_fondo: pygame.surface.Surface, foto_moneda: pygame.surface.Surface, foto_muros: pygame.surface.Surface)-> None:
    """imprimir fotogramas

    Args:
        ventana (pygame.surface.Surface): pantalla de juego
        lista_monedas (list): lista de monedas de puntos
        lista_obstaculos (list): lista que representa al laberinto
        lista_poderes (list): lista de monedas de poder
        lista_enemigos (list): lista de los enemigos
        personaje (dict): personaje que representa al jugador
        lista_balas (list): lista de los proyectiles 
        foto_fondo (pygame.surface.Surface): imagen de fondo deseada
        foto_moneda (pygame.surface.Surface): imagen de las monedas de puntos
        foto_muros (pygame.surface.Surface): imagen del laberinto
    """
    ventana.blit(foto_fondo, (0, 0))
    imprimir_mapeado(ventana, lista_monedas, foto_moneda)

    ventana.blit(personaje["imagen"], personaje["rect"])

    imprimir_grupo(ventana, lista_poderes)
    imprimir_grupo(ventana, lista_enemigos)
    imprimir_grupo(ventana, lista_balas)

    imprimir_mapeado(ventana, lista_obstaculos, foto_muros)


def imprimir_datos_partida(ventana: pygame.surface.Surface, item: dict, texto: pygame.surface.Surface, marco: pygame.rect.Rect)-> None:
    """imprimir datos partida

    Args:
        ventana (pygame.surface.Surface): pantalla de juego
        item (dict): item a imprimir
        texto (pygame.surface.Surface): texto deseado en pantalla
        marco (pygame.rect.Rect): marco del texto deseado
    """
    ventana.blit(item["imagen"], item["rect"])
    ventana.blit(texto, marco)

