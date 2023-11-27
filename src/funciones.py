import pygame
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


def listar_mapa(mapa: list, tam: float, bloque: int = 1, imagen: pygame.Surface = None)-> list:
    """listar mapa

    Args:
        mapa (list): lsita de lista que represente el laverinto deseado
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
    for r1, r2 in [(rec1, rec2), (rec2, rec1)]:
        if punto_en_rec(r1.topleft, r2) or \
           punto_en_rec(r1.topright, r2) or \
           punto_en_rec(r1.bottomleft, r2) or \
           punto_en_rec(r1.bottomright, r2):
            return True
        else:
            return False
        

def pausa ():
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
    


def crear_cartel (pantalla: pygame.surface.Surface, texto: str, fuente: pygame.font.Font, coordenadas: tuple, color_fuente = (255, 255, 255)):
    """cartel

    Args:
        pantalla (pygame.surface.Surface): superficie en la que se desea el cartel
        texto (str): tecto del cartel
        fuente (pygame.font.Font): fuente del tecto
        coordenadas (tuple): punto de imagen
        color_fuente (tuple, optional): color de la fuente. Defaults to (255, 255, 255).
    """
    sup_texto = fuente.render(texto, True, color_fuente)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = coordenadas
    pantalla.blit(sup_texto, rect_texto)


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