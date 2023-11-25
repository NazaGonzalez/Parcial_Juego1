# Realizar el desarrollo de un juego estilo arcade utilizando Python y Pygame.

# Descripción:
# El juego debe incluir un jugador principal que puede moverse en la zona de juego sin salir de
# los límites de la pantalla, una variedad de obstáculos o enemigos, la capacidad de disparar o
# realizar acciones para defenderse, un sistema de vidas y puntuación, y la opción de incluir un
# elemento especial o poderes. Deberán crear una pantalla de inicio con botones de opciones y
# una pantalla de fin para mostrar la puntuación final del jugador.
# Requisitos del Juego:
# Pantalla de Inicio:
# Debe haber una pantalla de inicio con un título y botones para comenzar el juego, ver las
# opciones y salir del mismo.
# Jugador Principal:
# El jugador debe controlar un personaje o entidad que puede moverse en el espacio de juego.
# El personaje debe ser capaz de interactuar de alguna manera con el entorno disparando,
# saltando o realizando acciones para defenderse.
# Obstáculos o Enemigos:
# Debe haber una variedad de obstáculos o enemigos en la zona de juego que representen
# desafíos para el jugador.
# Los obstáculos o enemigos pueden ser de diferentes tipos y comportarse de manera única.
# 
# Vidas y Puntaje:
# El juego debe tener un sistema de vidas. El jugador comienza con un número determinado de
# vidas y pierde una vida cada vez que no logra superar un obstáculo o enemigo.
# Debe haber un sistema de puntuación que aumenta cada vez que el jugador supera un
# desafío o destruye un enemigo.
# Elemento Especiales o Poderes:
# Incluir un elemento especial o poderes que otorguen beneficios temporales al jugador.
# Pantalla de Fin:
# Cuando el jugador pierde todas sus vidas, se debe mostrar una pantalla de fin que muestre la
# puntuación final del jugador.
# Aplicar temas vistos en clases:
# ● Tipos de datos avanzados: listas, tuplas, diccionarios, sets.
# ● Funciones. El código debe estar debidamente modularizado y documentado. Tengan
# en cuenta los objetivos de la programación con funciones. Realizar módulos.py para la
# correcta organización de las mismas.
# ● Manejo de strings: para normalizar datos, realizar validaciones, etc.
# ● Archivos csv y Json. Se deberán utilizar los dos tipos de archivos tanto para persistir
# datos (score, premios, etc) como para leer los elementos del juego (rutas de imágenes,
# etc)
# ● Manejo de excepciones. Deberán controlar por lo menos cuatro tipos de excepciones.
# Pygame:
# ● Imágenes. Según la temática del juego a desarrollar, habrá imágenes estáticas y/o
# dinámicas (que van cambiando con cada acción del jugador)
# ● Fuentes: toda interacción con el jugador implica que esos mensajes se muestran por la
# ventana del juego. Por ejemplo: el texto de los botones, las vidas, score, etc.
# ● Rectángulos: para representar botones, o cualquier elemento del juego que necesiten.
# ● Manejo de eventos: teclas, mouse, eventos propios y temporizadores para la
# interacción con el usuario.
# ● Colisiones: entre el jugador principal y los objetos del juego (obstáculos, vidas, objetos
# especiales).
# ● Botones: por ejemplo para el manejo del menú principal
# ● Sonidos y música: debe haber una música de fondo y ante distintas acciones, un
# efecto de sonido distinto.
# Consideraciones:
# ● Aplicar las técnicas de programación vistas en clase.
# ● Todo código que les hayamos compartido o que hayan obtenido de las clases, debe ser
# reelaborado (intenten darle una impronta propia). No abusen del copy-paste.
# 
# ● ¿Pueden utilizar chat-gpt? Si, claro. Pero tengan en cuenta que toda pieza de código va
# a ser evaluada, y si no la pueden defender, el parcial no estará aprobado.
# ● La temática del juego no podrá ser la misma que la explicada en clases. por ejemplo: no
# podrán realizar un arcade de naves y meteoritos.
# ● El juego tiene que ser tipo arcade, pero no de plataformas, ya que para el segundo
# parcial abordaremos esta modalidad.

import pygame
from funciones import *
from random import *
import sys

#-----inicializa todos los modulos de pygame con sus funciones-----
pygame.init()


#-----------------------generar mapa------------------------------

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


#-----------------config pantalla principal------------------------
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

PANTALLA = pygame.display.set_mode((TAM_PANT))
pygame.display.set_caption("Juego1.")
pygame.display.set_icon(pygame.image.load("./src/assets/onepiece.png"))

#-----------------------direccion de movimiento---------------------

MOV_AR = False
MOV_AB = False
MOV_DE = False
MOV_IZ = False

TOCA_TOP = False
TOCA_BOT = False
TOCA_RIG = False
TOCA_LEF = False

DE = 1
IZ = 2
AR = 3
AB = 4
DIRECCIONES_ENEMIGOS = (DE, IZ, AR, AB)

VELOCIDAD = 2

ATAQUE = False
PODER = False

#--------------------crear reloj----------------------------------
RELOJ = pygame.time.Clock()

#-------------------------seteo sonidos---------------------------
try: 
    SUENA_MUSICA = True
    pygame.mixer.music.load("./src/assets/one_pce1.mp3")
    
    pygame.mixer.music.set_volume(1)

    SONIDO_VICTORIA = pygame.mixer.Sound("./src/assets/franky.mp3")
    SONIDO_MONEDA = pygame.mixer.Sound("./src/assets/moneda_son.mp3")
    SONIDO_PODER = pygame.mixer.Sound("./src/assets/poder_son.mp3")
    SONIDO_PODER.set_volume(0.5)
    SONIDO_FINAL = pygame.mixer.Sound("./src/assets/one-piece-zoro.mp3")
    SINIDO_INICIO = pygame.mixer.Sound("./src/assets/one-piece-luffy.mp3")
except Exception as e:
    print(f"¡Ocurrió un error al cargar los sonidos del juego!: {e}")

MUSICA_PODER = False

#---------------------cargar imagenes-----------------------------
try:    
    imagen_jugado1 = pygame.image.load("./src/assets/onepiece.png")
    
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
#------------------evento personalizado---------------------------
CAMBIO_DIR_ENEMIGOS = pygame.USEREVENT + 1
pygame.time.set_timer(CAMBIO_DIR_ENEMIGOS, 3000)

NUEVO_PODER = pygame.USEREVENT + 2
pygame.time.set_timer(NUEVO_PODER, 15000)


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
jugador = crear_bloque(ANCHO // 2, ALTO // 2, TAM_ENTIDADES, TAM_ENTIDADES, 0, imagen_jugado1)

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

proyectiles = []

poderes = []

JUGANDO = False
#-----------------------pantalla de inicio------------------------

PANTALLA.blit(imagen_pant_ini, (0, 0))
SINIDO_INICIO.play()

PANTALLA.blit(imagen_jugado1, (150, 75))

#boton inicio
PANTALLA.blit(cartel_inicio["imagen"], (CENT_PANT[0] - 110, -50))
PANTALLA.blit(cartel_salir["imagen"], (CENT_PANT[0] - 110, 460))

PANTALLA.blit(boton_inicio["sup_texto"], boton_inicio["rect"])
PANTALLA.blit(boton_salir["sup_texto"], boton_salir["rect"])

pygame.display.flip()
while not JUGANDO:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if punto_en_rec(mouse_pos, boton_inicio["rect"]):
                JUGANDO = True
            if punto_en_rec(mouse_pos, boton_salir["rect"]):
                JUGANDO = False
                pygame.quit()
                sys.exit() 


#quitar el cursor 
pygame.mouse.set_visible(False)

#-------------se inicializa la deteccion de eventos---------------
pygame.mixer.music.play(-1)

while JUGANDO:
    RELOJ.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            JUGANDO = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                MOV_AR = True
                MOV_AB = False
            elif e.key == pygame.K_s:
                MOV_AB = True
                MOV_AR = False
            elif e.key == pygame.K_d:
                MOV_DE = True
                MOV_IZ = False
            elif e.key == pygame.K_a:
                MOV_IZ = True
                MOV_DE = False
            
            elif e.key == pygame.K_SPACE:
                ATAQUE = True
            
            elif e.key == pygame.K_p:
                pygame.mixer.music.pause()
                pausa()
                pygame.mixer.music.unpause()

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_w:
                MOV_AR = False
                TOCA_TOP = False                
            if e.key == pygame.K_s:
                MOV_AB = False
                TOCA_BOT = False
            if e.key == pygame.K_d:
                MOV_DE = False
                TOCA_RIG = False     
            if e.key == pygame.K_a:
                MOV_IZ = False
                TOCA_LEF = False

            if e.key == pygame.K_SPACE:
                ATAQUE = False

        # cambio de direccion automatico de los enemigos
        if e.type == CAMBIO_DIR_ENEMIGOS:
            for enemigo in enemigos:
                enemigo["direc"] = choice(DIRECCIONES_ENEMIGOS)

        
        if e.type == NUEVO_PODER and len(poderes) < 4:
            poderes.append(crear_bloque(0, 0, TAM_ENTIDADES, TAM_ENTIDADES, dir = 0, imagen = imagen_poder))
            for poder in poderes:
                poder["rect"].left, poder["rect"].top = choice(((5, 5), (ANCHO - TAM_ENTIDADES, 5), (5, ALTO - TAM_ENTIDADES), (ANCHO - TAM_ENTIDADES, ALTO - TAM_ENTIDADES)))



#---------------------actualizar elementos------------------------
 
    # direccion del jugador    
    if MOV_AR and jugador["rect"].top >= 0:
        jugador["rect"].top -= VELOCIDAD
    elif MOV_AB and jugador["rect"].bottom <= ALTO:
        jugador["rect"].top += VELOCIDAD
    elif MOV_DE and jugador["rect"].right <= ANCHO:
        jugador["rect"].left += VELOCIDAD
    elif MOV_IZ and jugador["rect"].left >= 0:
        jugador["rect"].left -= VELOCIDAD

    # impaccto de jugador con laberinto
    try:
        if MOV_AR:
            for obstaculo in obstaculos:
                if detectar_choque(jugador["rect"], obstaculo["rect"]):
                    jugador["rect"].top += 5
                    TOCA_TOP = True
        if MOV_AB: 
            for obstaculo in obstaculos:
                if detectar_choque(jugador["rect"], obstaculo["rect"]):
                    jugador["rect"].top -= 5
                    TOCA_BOT = True
        if MOV_IZ:
            for obstaculo in obstaculos:
                if detectar_choque(jugador["rect"], obstaculo["rect"]):
                    jugador["rect"].left += 5
                    TOCA_LEF = True
        if MOV_DE:
            for obstaculo in obstaculos:
                if detectar_choque(jugador["rect"], obstaculo["rect"]):
                    jugador["rect"].left -= 5
                    TOCA_RIG = True
    except Exception as e:
        print(f"¡Ocurrió un error al detectar colisión del jugador!: {e}")



    # movimiento enemigos
    for enemigo in enemigos:
        if enemigo["direc"] == DE:
            enemigo["rect"].left += VELOCIDAD
        elif enemigo["direc"] == IZ:
            enemigo["rect"].left -= VELOCIDAD
        elif enemigo["direc"] == AR:
            enemigo["rect"].top -= VELOCIDAD
        elif enemigo["direc"] == AB:
            enemigo["rect"].top += VELOCIDAD

    # direccion de los enemigos
    for enemigo in enemigos:
        if enemigo["rect"].right >= ANCHO:#   choca a la derecha
            enemigo["rect"].left -= 5
            enemigo["direc"] = choice((AR, AB, IZ))

        elif enemigo["rect"].left <= 0:#   choca a la izquieda
            enemigo["rect"].left += 5
            enemigo["direc"] = choice((AR, AB, DE))  

        elif enemigo["rect"].top <= 0:#   choca arriba
            enemigo["rect"].top += 5
            enemigo["direc"] = choice((AB, DE, IZ))

        elif enemigo["rect"].bottom >= ALTO:#   choca abajo
            enemigo["rect"].top -= 5
            enemigo["direc"] = choice((AR, DE, IZ))

    # impacto de los enemigos con el laberinto
    try:
        if AR:
            for enemigo in enemigos:
                for obstaculo in obstaculos:
                    if detectar_choque(enemigo["rect"], obstaculo["rect"]):
                        enemigo["rect"].top += 5
                        enemigo["direc"] = choice((AB, DE, IZ))
        if AB:
            for enemigo in enemigos:
                for obstaculo in obstaculos:
                    if detectar_choque(enemigo["rect"], obstaculo["rect"]):
                        enemigo["rect"].top -= 5
                        enemigo["direc"] = choice((AR, DE, IZ))
        if DE:
            for enemigo in enemigos:
                for obstaculo in obstaculos:
                    if detectar_choque(enemigo["rect"], obstaculo["rect"]):
                        enemigo["rect"].left -= 5
                        enemigo["direc"] = choice((AB, AR, IZ))
        if IZ:
            for enemigo in enemigos:
                for obstaculo in obstaculos:
                    if detectar_choque(enemigo["rect"], obstaculo["rect"]):
                        enemigo["rect"].left += 5
                        enemigo["direc"] = choice((AB, DE, AR))
    except Exception as e:
        print(f"¡Ocurrió un error al detectar colisión de los enemigos!: {e}")

    # traga monedas
    for moneda in monedas[:]:
        for p in poderes:
            try:
                if detectar_choque(moneda["rect"], p["rect"]):
                    monedas.remove(moneda)
            except Exception as e:
                print(f"¡Ocurrió un error al detectar el cambio de moneda por poder!: {e}")
        try:
            if detectar_choque(moneda["rect"], jugador["rect"]):
                monedas.remove(moneda)
                SONIDO_MONEDA.play()
                CONTADOR_PUNTOS += 1
        except Exception as e:
            print(f"¡Ocurrió un error al detectar que el jugador agarro una moneda!: {e}")


    if CONTADOR_PODER > 0:
        PODER = True
        CONTADOR_PODER -= 1
        if CONTADOR_PODER <= 0:
            PODER = False
            MUSICA_PODER = False
            pygame.mixer.music.play(-1)
       
    
    # agarrar poder
    for p in poderes[:]:
        try:
            if detectar_choque(p["rect"], jugador["rect"]):
                poderes.remove(p)
                CONTADOR_PODER = TIEMPO_PODER
                if not MUSICA_PODER:
                    pygame.mixer.music.pause()
                    SONIDO_PODER.play()
                    MUSICA_PODER = True
                
        except Exception as e:
            print(f"¡Ocurrió un error al detectar que el jugador consiguio un poder!: {e}")
    

    # choque enemigo y jugador
    for enemigo in enemigos:
        try:
            if detectar_choque(enemigo["rect"], jugador["rect"]):
                if not PODER:
                    jugador["rect"].left = ANCHO // 2
                    jugador["rect"].top = ALTO // 2
                    CONTADOR_VIDAS -= 1
                else:
                    enemigo["rect"].left, enemigo["rect"].top = choice(((0, 0), (ANCHO, 0), (0, ALTO), (ANCHO, ALTO)))
                    CONTADOR_PUNTOS += 3
        except Exception as e:
            print(f"¡Ocurrió un error al detectar colisión entre entidades!: {e}")

    if CONTADOR_VIDAS <= 0:
        JUGANDO = False

            
    # recarga nivel 
    if len(monedas) == 0:
        monedas = listar_mapa(mapa, TAM_CELDA, 0)
        for moneda in monedas:
            
            moneda["rect"].width = 20
            moneda["rect"].height = 20

            moneda["rect"].top = moneda["rect"].top + 10
            moneda["rect"].left = moneda["rect"].left + 10
        CONTADOR_VIDAS += 1
        CONTADOR_NIVEL += 1
        SONIDO_VICTORIA.play()
        jugador["rect"].left = ANCHO // 2
        jugador["rect"].top = ALTO // 2
        PODER = False
        SONIDO_PODER.stop()


    # ataque
    if ATAQUE and len(proyectiles) == 0:
        if MOV_AR:
            proyectiles.append(crear_bloque(jugador["rect"].centerx, jugador["rect"].centery, 20, 20,dir = AR, imagen = imagen_ataque))
            CONTADOR_PUNTOS -= 1
        elif MOV_AB:
            proyectiles.append(crear_bloque(jugador["rect"].centerx, jugador["rect"].centery, 20, 20,dir = AB, imagen = imagen_ataque))
            CONTADOR_PUNTOS -= 1
        elif MOV_DE:
            proyectiles.append(crear_bloque(jugador["rect"].centerx, jugador["rect"].centery, 20, 20,dir = DE, imagen = imagen_ataque))
            CONTADOR_PUNTOS -= 1
        elif MOV_IZ:
            proyectiles.append(crear_bloque(jugador["rect"].centerx, jugador["rect"].centery, 20, 20,dir = IZ, imagen = imagen_ataque))
            CONTADOR_PUNTOS -= 1

    # mov proyectil
    for proyectil in proyectiles[:]:
        if proyectil["direc"] == DE:
            proyectil["rect"].left += VELOCIDAD + 2
        elif proyectil["direc"] == IZ:
            proyectil["rect"].left -= VELOCIDAD + 2
        elif proyectil["direc"] == AR:
            proyectil["rect"].top -= VELOCIDAD + 2
        elif proyectil["direc"] == AB:
            proyectil["rect"].top += VELOCIDAD + 2

        if proyectil["rect"].top < 0 or proyectil["rect"].left < 0 or proyectil["rect"].bottom > ALTO or proyectil["rect"].right > ANCHO:
            proyectiles.remove(proyectil)

        for obstaculo in obstaculos:
            try:
                if detectar_choque(proyectil["rect"], obstaculo["rect"]):
                    proyectiles.remove(proyectil)
            except Exception as e:
                print(f"¡Ocurrió un error al detectar la colicion del proyectil con obstaculos!: {e}")

        for enemigo in enemigos:
            try:
                if detectar_choque(proyectil["rect"], enemigo["rect"]):
                    proyectiles.remove(proyectil)
                    enemigo["rect"].left, enemigo["rect"].top = choice(((0, 0), (ANCHO, 0), (0, ALTO), (ANCHO, ALTO)))
                    CONTADOR_PUNTOS += 3
            except Exception as e:
                print(f"¡Ocurrió un error al detectar la colisión del proyectil con el enemigo!: {e}")
        


#-----------------------imprimir en pantalla----------------------
    # fondo
    PANTALLA.blit(fondo, (0, 0))
    # monedas
    for moneda in monedas:
        moneda["imagen"] = pygame.transform.scale(imagen_moneda, (moneda["rect"].width, moneda["rect"].height))
        PANTALLA.blit(moneda["imagen"], moneda["rect"])

    for p in poderes:
        PANTALLA.blit(p["imagen"], p["rect"])

    # jugador
    PANTALLA.blit(jugador["imagen"], jugador["rect"])
    # enemigos
    for enemigo in enemigos:
        PANTALLA.blit(enemigo["imagen"], enemigo["rect"])
    
    # obstaculos
    for obstaculo in obstaculos:
        obstaculo["imagen"] = pygame.transform.scale(imagen_muros, (obstaculo["rect"].width, obstaculo["rect"].height))
        PANTALLA.blit(obstaculo["imagen"], obstaculo["rect"])

    # vidas
    PANTALLA.blit(vida["imagen"], vida["rect"])
    texto_vidas = FUENTE.render(":" + str(CONTADOR_VIDAS), True, NEGRO)
    PANTALLA.blit(texto_vidas, marco_vidas)

    # puntos
    PANTALLA.blit(puntos["imagen"], puntos["rect"])
    texto_puntos = FUENTE.render(":" + str(CONTADOR_PUNTOS), True, NEGRO)
    PANTALLA.blit(texto_puntos, marco_puntos)

    # proyectil
    for proyectil in proyectiles:
        PANTALLA.blit(proyectil["imagen"], proyectil["rect"])


#----------------------actualizar pantalla------------------------
    pygame.display.flip()

#-------------------------fin del juago---------------------------
pygame.mixer.music.stop()

PANTALLA.blit(imagen_pant_ini, (0, 0))
SONIDO_FINAL.play()

pygame.mouse.set_visible(True)
cartel(PANTALLA, "FIN DEL JUEGO", FUENTE, CENT_PANT, NEGRO)
cartel(PANTALLA, "Precione una tecla para continuar", FUENTE, (ANCHO// 2, ALTO - 50), NEGRO)
cartel(PANTALLA, "Puntuacion Final: " + str(CONTADOR_PUNTOS), FUENTE, (ANCHO// 2, 50), NEGRO)

pygame.display.flip()
pausa()
pygame.quit()
sys.exit() 