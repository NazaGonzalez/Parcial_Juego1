import pygame

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
    


def cartel (pantalla: pygame.surface.Surface, texto: str, fuente: pygame.font.Font, coordenadas: tuple, color_fuente = (255, 255, 255)):
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
        dict: _description_
    """
    sup_texto = fuente.render(texto, True, color)
    rect_texto = sup_texto.get_rect()

    boton = pygame.Surface(tam)#crea una superficie con las caractaristicas indicadas
    rect_boton = boton.get_rect()

    rect_boton.center = coordenadas
    rect_texto.center = rect_boton.center

    boton.blit(sup_texto, rect_boton)

    return {"boton": boton, "rect": rect_boton, "sup_texto": sup_texto, "rect_texto": rect_texto, "color": color}


            