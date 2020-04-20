import pygame
import numpy as np
import time

pygame.init()

# Ancho y alto de la pantalla
width, height = 1000, 1000
# Se crea la pantalla
screen = pygame.display.set_mode((height, width))

# Color del fondo
bg = 25, 25, 25

# Se añade el color a la pantalla
screen.fill(bg)

# Creación de las celdas
# Cantidad de celdas en el eje x como en el eje y
nxC, nyC = 50, 50
# Ancho y alto de las celdas
dimCW = width / nxC
dimCH = height / nyC

# Obtener el estado de las celdas, se crea una matríz
# Vivas = 1, Muertas = 0
gameState = np.zeros((nxC, nyC))

# Automata palo
# gameState[5,3] = 1
# gameState[5,4] = 1
# gameState[5,5] = 1

# Control de la ejecución del juego
pauseExect = False

# Bucle de ejecución
while True:
    # Copia del estado actual del juego
    newGameState = np.copy(gameState)

    # Limpiar de nuevo la pantalla para evitar sobrepocisión
    screen.fill(bg)
    # Delay
    time.sleep(0.1)

    # Registro de los eventos de teclado y ratón
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        #print(mouseClick) # (0, 0, 1) Click derecho, boton de la mitad, click derecho

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            # Que celda estamos pulsando
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]

    for y in range(0, nxC):
        for x in range(0, nyC):
            if not pauseExect:
                # Calculando el número de vecinos
                n_heigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x) % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y) % nyC] + \
                          gameState[(x + 1) % nxC, (y) % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x) % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Regla 1: Una célula muerta con exactamente 3 vecinas vivas, "revive"
                if gameState[x, y] == 0 and n_heigh == 3:
                    newGameState[x, y] = 1

                # Regla 2: Una célula viva con menos de 2 o mas de 3 vecinas vivas, "muere"
                if gameState[x, y] == 1 and (n_heigh < 1 or n_heigh > 3):
                    newGameState[x, y] = 0

            # Creamos el poligono de cada celda a dibujar
            poly = [
                ((x) * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x) * dimCW, (y + 1) * dimCH),
            ]

            # Dibujar cada celda para cada par de x y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)
    # Actualizamos la pantalla
    pygame.display.flip()