import pygame
import os
import json
import sys

def crear_bloque(left = 0, top = 0, width = 50, heigth = 50, dir = 1, imagen = None)-> dict:
    """crear bloque

    Args:
        left (int, optional): punto left del rect deseado. Defaults to 0.
        top (int, optional): punto top del rect deseado. Defaults to 0.
        width (int, optional): ancho del rect deseado. Defaults to 50.
        heigth (int, optional): alto del rect deseado. Defaults to 50.
        color (tuple, optional): color del rect deseado. Defaults to (255, 255, 255).
        dir (int, optional): direccion del rect deseado. Defaults to 1.
        imagen (_type_, optional): imagen del rect deseado. Defaults to None.

    Returns:
        dict: diccionario con los datos del elemento rect deseado
    """
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, heigth))    
    return {"rect": pygame.Rect(left, top, width, heigth), "direc": dir, "imagen": imagen}


def punto_en_rec(punto: tuple, rect: pygame.Rect)->bool:
    """punto en rec

    Args:
        punto (tuple): punto que se desea verificar
        rect (pygame.Rect): rect en relacion a la verificacion

    Returns:
        bool: respuesta de la comparacion
    """
    x, y = punto
    valor = False
    if x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom:
        valor =  True
    return valor


def detectar_choque(rec1: pygame.rect.Rect, rec2: pygame.rect.Rect)->bool:
    """detectar choque

    Args:
        rec1 (pygame.rect.Rect): rectangulo con el que se comprobara el impacto
        rec2 (pygame.rect.Rect): rectangulo con el que se comprobara el impacto

    Returns:
        bool: respuesta
    """
    rta = False
    for r1, r2 in [(rec1, rec2), (rec2, rec1)]:
        if punto_en_rec(r1.topleft, r2) or \
           punto_en_rec(r1.topright, r2) or \
           punto_en_rec(r1.bottomleft, r2) or \
           punto_en_rec(r1.bottomright, r2):
            rta = True
        return rta
        

def pausa():
    """pausa
    """
    while True:
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            return

 
def esta(lista:list, item:str)->bool:
    """esta

    Args:
        lista (list): lista para comprobar
        item (str): item a comprobar

    Returns:
        bool: se indicara si hay o no coinsidencia
    """
    rta = False
    for elemento in lista:
        if(elemento == item):
            rta = True
            break
        return rta
    

def crear_cartel (ventana: pygame.surface.Surface, texto: str, fuente: pygame.font.Font, coordenadas: tuple, color_fuente = (255, 255, 255))-> None:
    """cartel

    Args:
        ventana (pygame.surface.Surface): superficie en la que se desea el cartel
        texto (str): tecto del cartel
        fuente (pygame.font.Font): fuente del tecto
        coordenadas (tuple): punto de imagen
        color_fuente (tuple, optional): color de la fuente. Defaults to (255, 255, 255).
    """
    sup_texto = fuente.render(texto, True, color_fuente)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = coordenadas
    ventana.blit(sup_texto, rect_texto)




def cargar_record(archivo_json: str, puntuacion_actual: int, nombre_jugador: str)-> str and int:
    """cargar record

    Args:
        archivo_json (str): nombre del archivo del record
        puntuacion_actual (int): puntuacion final del jugador 
        nombre_jugador (str): nombre del jugador

    Returns:
        str and int: nombre del portador del recor actual y los puntos
    """
    if os.path.exists(archivo_json):
        with open(archivo_json, "r") as archivo:
            lector = json.load(archivo)
            nombre_record = lector["nombre"]
            puntuacion_record = lector["puntos"]

        if puntuacion_actual > puntuacion_record:
            nombre_record = nombre_jugador
            puntuacion_record = puntuacion_actual
            with open(archivo_json, "w") as archivo: 
                datos = {"nombre": nombre_record, "puntos": puntuacion_record}
                json.dump(datos, archivo)
    else:
        with open(archivo_json, "w") as archivo: 
                nombre_record = nombre_jugador
                puntuacion_record = puntuacion_actual
                datos = {"nombre": nombre_jugador, "puntos": puntuacion_record}
                json.dump(datos, archivo)

    return nombre_record, puntuacion_record


def pantalla_fin(ventana: pygame.surface.Surface, foto_fondo: pygame.surface.Surface, sonido: pygame.mixer.Sound, fuente: pygame.font.Font, puntos_partida: int, puntos_mas_alto: int, nombre_mas_alto: str, color: tuple)-> None:
    """pantalla fin

    Args:
        ventana (pygame.surface.Surface): pantalla de juego
        foto_fondo (pygame.surface.Surface): imagen de fondo deseada
        sonido (pygame.mixer.Sound): sonido de derrota
        fuente (pygame.font.Font): fuente del texto
        puntos_partida (int): puntuacion final del jugador
        puntos_mas_alto (int): record establesido
        nombre_mas_alto (str): nombre del portador del record
        color (tuple): color del texto
    """
    rectangulo_ventana = ventana.get_rect()
    pygame.mixer.music.stop()

    ventana.blit(foto_fondo, (0, 0))
    sonido.play()

    pygame.mouse.set_visible(True)
    crear_cartel(ventana, "FIN DEL JUEGO", fuente, (rectangulo_ventana.width // 2, rectangulo_ventana.height // 2), color)
    crear_cartel(ventana, "Presione una tecla para continuar", fuente, (rectangulo_ventana.width // 2, rectangulo_ventana.height - 50), color)
    crear_cartel(ventana, "Puntuacion Final: " + str(puntos_partida), fuente, (rectangulo_ventana.width // 2, 25), color)
    crear_cartel(ventana, "El record es de " + nombre_mas_alto + ". Con " + str(puntos_mas_alto) + " puntos", fuente, (rectangulo_ventana.width // 2, 75), color)

    pygame.display.flip()
    pausa()
    pygame.quit()
    sys.exit() 

