import pygame
from funciones import *
from mapa import *
from inicio import *
pygame.init()
#-----------------------generar mapa------------------------------
NOMBRE_JUGADOR = input("Ingrese su nombre (hasta 4 caracteres): ")[:4]

TAM_CELDA = 50
mapa = [
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
]

JUGANDO = False

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

ANCHO = 800
ALTO = 600

TAM_PANT = (ANCHO, ALTO)
CENT_PANT = (ANCHO // 2, ALTO //2)

TAM_ENTIDADES = 38

FPS = 60

CONTADOR_NIVEL = 1
CONTADOR_VIDAS = 3
CONTADOR_PUNTOS = 0
CONTADOR_PODER = 0
TIEMPO_PODER = 15 * FPS

proyectiles = []

poderes = []

#-----------------------direccion de movimiento---------------------

MOV_AR = False
MOV_AB = False
MOV_DE = False
MOV_IZ = False

DE = 1
IZ = 2
AR = 3
AB = 4
DIRECCIONES_ENEMIGOS = (AR, AB, DE, IZ)

VELOCIDAD = 2

ATAQUE = False
#PODER = False

#-----------------config pantalla principal------------------------
PANTALLA = pygame.display.set_mode((TAM_PANT))
pygame.display.set_caption("Juego1.")
pygame.display.set_icon(pygame.image.load("./src/assets/onepiece.png"))

#--------------------crear reloj----------------------------------
RELOJ = pygame.time.Clock()


#-------------------------seteo sonidos---------------------------
SUENA_MUSICA_PODER = False

try: 
    
    pygame.mixer.music.load("./src/assets/one_pce1.mp3")
    
    pygame.mixer.music.set_volume(1)

    SONIDO_VICTORIA = pygame.mixer.Sound("./src/assets/franky.mp3")
    SONIDO_MONEDA = pygame.mixer.Sound("./src/assets/moneda_son.mp3")
    SONIDO_PODER = pygame.mixer.Sound("./src/assets/poder_son.mp3")
    SONIDO_PODER.set_volume(0.5)
    SONIDO_FINAL = pygame.mixer.Sound("./src/assets/one-piece-zoro.mp3")
    SONIDO_INICIO = pygame.mixer.Sound("./src/assets/one-piece-luffy.mp3")
except Exception as e:
    print(f"¡Ocurrió un error al cargar los sonidos del juego!: {e}")

#---------------------cargar imagenes-----------------------------
try:    
    imagen_jugador1 = pygame.image.load("./src/assets/onepiece.png")
    
    imagen_muros = pygame.image.load("./src/assets/muro.jpg")
    
    imagen_enemigo1 = pygame.image.load("./src/assets/enemigo1.png")
    imagen_enemigo2 = pygame.image.load("./src/assets/enemigo2.png")
    imagen_enemigo3 = pygame.image.load("./src/assets/enemigo3.png")
    imegen_enemigo4 = pygame.image.load("./src/assets/enemigo4.png")
    
    imagen_moneda = pygame.image.load("./src/assets/moneda.png")
    
    fondo = pygame.transform.scale(pygame.image.load("./src/assets/suelo.jpg"), TAM_PANT)
    
    imagen_pant_ini = pygame.transform.scale(pygame.image.load("./src/assets/fondo1.jpg"), TAM_PANT)
    
    imagen_vidas = pygame.image.load("./src/assets/corazon.png")
    
    imagen_puntos = pygame.image.load("./src/assets/puntos.png")
    
    imagen_ataque = pygame.image.load("./src/assets/cañon.png")
    
    imagen_poder = pygame.image.load("./src/assets/gomugomu.png")
    
    imagen_boton = pygame.image.load("./src/assets/cartel_mad.png")
except Exception as e:
    print(f"¡Ocurrió un error al cargar las imagenes del juego!: {e}")

#--------------------setear fuente--------------------------------
FUENTE = pygame.font.SysFont("Comic Sans MS", 40)
texto_vidas = FUENTE.render(":" + str(CONTADOR_VIDAS), True, NEGRO)

marco_vidas = texto_vidas.get_rect()
marco_vidas.left = 340
marco_vidas.top = 350
marco_vidas.width = marco_vidas.width - 50

texto_puntos = FUENTE.render(":" + str(CONTADOR_PUNTOS), True, NEGRO)

marco_puntos = texto_puntos.get_rect()
marco_puntos.left = 410
marco_puntos.top = 350
marco_puntos.width = marco_puntos.width - 50

#------------------------crear botones----------------------------

boton_inicio = boton_menu("INICIAR", (150, 50), (CENT_PANT[0], 50), FUENTE, NEGRO)
cartel_inicio = crear_bloque(0, 0, 250, 200, dir = 0, imagen = imagen_boton)

boton_salir = boton_menu("SALIR", (150, 50), (CENT_PANT[0], ALTO - 50), FUENTE, NEGRO)
cartel_salir = crear_bloque(0, 0, 250, 200, dir = 0, imagen = imagen_boton)

#-------------------------creamos bloques-------------------------
jugador = crear_bloque(ANCHO // 2, ALTO // 2, TAM_ENTIDADES, TAM_ENTIDADES, 0, imagen_jugador1)
jugador["poder"] = False

enemigos = []

enemigos.append(crear_bloque(0, 550, TAM_ENTIDADES, TAM_ENTIDADES, choice(DIRECCIONES_ENEMIGOS), imagen_enemigo1))
enemigos.append(crear_bloque(750, 0, TAM_ENTIDADES, TAM_ENTIDADES, choice(DIRECCIONES_ENEMIGOS), imagen_enemigo2))
enemigos.append(crear_bloque(750, 550, TAM_ENTIDADES, TAM_ENTIDADES, choice(DIRECCIONES_ENEMIGOS), imagen_enemigo3))
enemigos.append(crear_bloque(0, 0, TAM_ENTIDADES, TAM_ENTIDADES, choice(DIRECCIONES_ENEMIGOS), imegen_enemigo4))

obstaculos = listar_mapa(mapa, TAM_CELDA, 1)

monedas = []
monedas = listar_mapa(mapa, TAM_CELDA, 0, imagen_muros)
for moneda in monedas:
    moneda["rect"].width = 20
    moneda["rect"].height = 20
    moneda["rect"].top = moneda["rect"].top + 10
    moneda["rect"].left = moneda["rect"].left + 10

vida = crear_bloque(300, 350, 55, 55, dir = 0, imagen = imagen_vidas)

puntos = crear_bloque(380, 350, 40, 50, dir = 0, imagen = imagen_puntos)

#-----------------------pantalla de inicio------------------------

JUGANDO = pantalla_inicio(PANTALLA, SONIDO_INICIO, TAM_PANT, cartel_inicio, cartel_salir, boton_inicio, boton_salir, JUGANDO)


