import pygame
from config import *
from funciones import *
from random import *
import sys
import csv
import os

#-----inicializa todos los modulos de pygame con sus funciones-----
pygame.init()

#------------------evento personalizado---------------------------
CAMBIO_DIR_ENEMIGOS = pygame.USEREVENT + 1
pygame.time.set_timer(CAMBIO_DIR_ENEMIGOS, 3000)

NUEVO_PODER = pygame.USEREVENT + 2
pygame.time.set_timer(NUEVO_PODER, 15000)

#------------------------crear botones----------------------------

boton_inicio = boton_menu("INICIAR", (150, 50), (CENT_PANT[0], 50), FUENTE, NEGRO)
cartel_inicio = crear_bloque(0, 0, 250, 200, dir = 0, imagen = imagen_boton)

boton_salir = boton_menu("SALIR", (150, 50), (CENT_PANT[0], ALTO - 50), FUENTE, NEGRO)
cartel_salir = crear_bloque(0, 0, 250, 200, dir = 0, imagen = imagen_boton)

#-------------------------creamos bloques-------------------------
jugador = crear_bloque(ANCHO // 2, ALTO // 2, TAM_ENTIDADES, TAM_ENTIDADES, 0, imagen_jugador1)

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
        if MOV_AB: 
            for obstaculo in obstaculos:
                if detectar_choque(jugador["rect"], obstaculo["rect"]):
                    jugador["rect"].top -= 5
        if MOV_IZ:
            for obstaculo in obstaculos:
                if detectar_choque(jugador["rect"], obstaculo["rect"]):
                    jugador["rect"].left += 5
        if MOV_DE:
            for obstaculo in obstaculos:
                if detectar_choque(jugador["rect"], obstaculo["rect"]):
                    jugador["rect"].left -= 5
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

if os.path.exists("puntuacion_mas_alta.csv"):
    with open("puntuacion_mas_alta.csv", "r") as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            PUNTUACION_MAS_ALTA = int(fila[0])


if CONTADOR_PUNTOS > PUNTUACION_MAS_ALTA:
    # Actualizar la puntuación más alta y guardarla en el archivo CSV
    PUNTUACION_MAS_ALTA = CONTADOR_PUNTOS
    with open("puntuacion_mas_alta.csv", "w", newline="") as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([PUNTUACION_MAS_ALTA])

#-------------------------fin del juago---------------------------
pygame.mixer.music.stop()

PANTALLA.blit(imagen_pant_ini, (0, 0))
SONIDO_FINAL.play()

pygame.mouse.set_visible(True)
crear_cartel(PANTALLA, "FIN DEL JUEGO", FUENTE, CENT_PANT, NEGRO)
crear_cartel(PANTALLA, "Precione una tecla para continuar", FUENTE, (ANCHO// 2, ALTO - 50), NEGRO)
crear_cartel(PANTALLA, "Puntuacion Final: " + str(CONTADOR_PUNTOS), FUENTE, (ANCHO// 2, 75), NEGRO)
crear_cartel(PANTALLA, "Puntuacion mas alta hasta ahora: " + str(PUNTUACION_MAS_ALTA), FUENTE, (ANCHO// 2, 25), NEGRO)

pygame.display.flip()
pausa()
pygame.quit()
sys.exit() 