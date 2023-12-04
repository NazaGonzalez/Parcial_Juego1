import pygame
from random import *
from funciones import *
from mapa import *
from inicio import *
from jugador import *
from enemigos import *
from config import *



#-----inicializa todos los modulos de pygame con sus funciones-----
pygame.init()


#------------------evento personalizado---------------------------
CAMBIO_DIR_ENEMIGOS = pygame.USEREVENT + 1
pygame.time.set_timer(CAMBIO_DIR_ENEMIGOS, 3000)

NUEVO_PODER = pygame.USEREVENT + 2
pygame.time.set_timer(NUEVO_PODER, 15000)


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
            if e.key == pygame.K_s:
                MOV_AB = False
            if e.key == pygame.K_d:
                MOV_DE = False    
            if e.key == pygame.K_a:
                MOV_IZ = False

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
    direccion_jugador((MOV_AR, MOV_AB, MOV_DE, MOV_IZ), jugador, VELOCIDAD, ANCHO, ALTO)

    # impaccto de jugador con laberinto
    impacto_obstaculos((MOV_AR, MOV_AB, MOV_IZ, MOV_DE), obstaculos, jugador)

    # movimiento enemigos
    movimiento_enemigos(enemigos, DIRECCIONES_ENEMIGOS, VELOCIDAD, obstaculos, ANCHO, ALTO)

    # traga monedas
    CONTADOR_PUNTOS = traga_monedas(monedas, poderes, jugador, SONIDO_MONEDA, CONTADOR_PUNTOS)

    # poder
    CONTADOR_PODER, SUENA_MUSICA_PODER = activar_poder(poderes, jugador, SONIDO_PODER, CONTADOR_PODER, SUENA_MUSICA_PODER, TIEMPO_PODER)

    # choque enemigo y jugador
    CONTADOR_VIDAS, CONTADOR_PUNTOS = choque_jugador_enemigo(ANCHO, ALTO, enemigos, jugador, CONTADOR_VIDAS, CONTADOR_PUNTOS)

    # ataque
    atacar(ATAQUE, proyectiles, (MOV_AR, MOV_AB, MOV_DE, MOV_IZ), jugador, DIRECCIONES_ENEMIGOS, imagen_ataque)

    # agarrar poder
    CONTADOR_PUNTOS = movimiento_balas(proyectiles, DIRECCIONES_ENEMIGOS, VELOCIDAD + 2, obstaculos, enemigos, CONTADOR_PUNTOS, ANCHO, ALTO)
            
    # recarga nivel 
    if len(monedas) == 0:
        SONIDO_PODER.stop()
        pygame.mixer.music.pause()
        monedas = recarga_nivel(monedas, jugador, mapa, TAM_CELDA, SONIDO_VICTORIA)
        CONTADOR_VIDAS += 1
        CONTADOR_NIVEL += 1
        pygame.mixer.music.unpause()

    if CONTADOR_VIDAS <= 0:
        JUGANDO = False
        

#-----------------------imprimir en pantalla----------------------
    imprimir_fotogramas(PANTALLA, monedas, obstaculos, poderes, enemigos, jugador, proyectiles, fondo, imagen_moneda, imagen_muros)

    texto_vidas = FUENTE.render(":" + str(CONTADOR_VIDAS), True, NEGRO)
    imprimir_datos_partida(PANTALLA, vida, texto_vidas, marco_vidas)
    texto_puntos = FUENTE.render(":" + str(CONTADOR_PUNTOS), True, NEGRO)
    imprimir_datos_partida(PANTALLA, puntos, texto_puntos, marco_puntos)


#----------------------actualizar pantalla------------------------
    pygame.display.flip()

NOMBRE_RECORD, PUNTUACION_RECORD  = cargar_record("record.json", CONTADOR_PUNTOS, NOMBRE_JUGADOR)


#-------------------------fin del juago---------------------------
pantalla_fin(PANTALLA, imagen_pant_ini, SONIDO_FINAL, FUENTE, CONTADOR_PUNTOS, PUNTUACION_RECORD, NOMBRE_RECORD, NEGRO)
