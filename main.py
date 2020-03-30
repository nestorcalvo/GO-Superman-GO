# -*- coding: utf-8 -*-
"""
Conceptos basicos de PDI
Por Nestor Calvo Ariza  nestor.calvo@udea.edu.co    CC 1118871837
    Santiago Patiño Munera santiago.patino@udea.edu.co  CC
27 de Marzo de 2020
"""

"""
1. Importamos las librerias basicas 
"""

import sys          # Libreria para trabajar con docmuentos y archivos de sistema
import pygame.locals as GAME_GLOBALS        # Para salir del juego
import pygame.event as GAME_EVENTS          # para detectar pulsasiones
import random       # Libreria para generar aleatoriedad
import cv2          # Libreria para operar la camara y la deteccion facial
import pygame       # Libreria para crear juegos en Python

"""
2. Definicion de variables importantes
"""
pygame.init()       # Inicializamos nuestro constructor de pygame
clock = pygame.time.Clock()     # Tiempo de nuestro juego para limitar en fps

windowWidth = 960       # Se define el ancho de la pantalla
windowHeight = 620          # Se define el alto de la pantalla

fps = 60    # Se fijan los valores de los frames por segundo

pantalla = pygame.display.set_mode([windowWidth, windowHeight])  # Creamos una pantalla de 960x620
cap = cv2.VideoCapture(0)  # Seleccionamos la primera camara (0) para hacer captura

pygame.display.set_caption('GO Superman GO')  # Establecemos el nombre de la ventana.

imagen_de_fondo = pygame.image.load("sprites/background.png").convert()  # Se carga la imagen del fondo
imagen_de_fondo = pygame.transform.scale(imagen_de_fondo, (windowWidth, windowHeight))  # Se escalan las imagenes para que queden acorde al tamaño de la ventana

imagen_de_incio = pygame.image.load("sprites/inicio.png").convert()  # Se carga la imagen del inicio

imagen_personaje = pygame.image.load("sprites/super_man.png").convert()  # Se carga la imagen del personaje
imagen_personaje = pygame.transform.scale(imagen_personaje, (40, 40))  # Se escala para poder hacerlo mas pequeño

imagen_de_fin = pygame.image.load("sprites/gameover.png").convert()  # Se carga la imagen que se mostrara cuando el jugador pierda
r_imagen_personaje = imagen_personaje.get_rect()  # Se almacena el rectangulo que recubre al jugador, sera usado para el analisis de colisiones

"""
3. Funcion para detectar el rostro del jugador
"""


def read_faces():
    global y_temp  # Se crea una variable y_temporal la cual sera usada para almacenar valores previos de y

    face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')  # Se toman los datos del modelo entrenado previamente para deteccion de rostro


    while 1: # Se mantiene un ciclo infinito para capturar todas las imagenes de la camara

        _, img = cap.read()  # Se almacena la imagen entregada por la camara

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Se convierte a escala de grises
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # Se aplica el modelo para detectar rostros en la imagen

        for (x, y, w, h) in faces: # Se realiza un for para cada imagen

            if y > y_temp + (h / 60) or y < y_temp - (h / 60):  # Se analiza si el valor se encuentra dentro de un rango de tolerancia
                y_temp = y  # Se almacena el valor en una variable temporal para comparar con la siguiente iteracion
                return y  # Se retorna el valor medido
            else:    # Si la condicion no se cumple
                return y_temp    # Se retorna el valor anterior como posicion
        k = cv2.waitKey(30)     # Se realizan esperas de 30 milisegundos para la tecla ESC
        if k > 0:    #Si se presiona una tecla
            break   # Se interrumpe el ciclo y no se siguen analizando imagenes
    cap.release()    # Se apaaga la camara
    cv2.destroyAllWindows()     #Se cierran las ventanas creadas


"""
4. Funcion para retornar el score del jugador
"""


def score():
    global counterPipe, flag_xi     # Se declara la variable que almacena el numero de obstaculos superados y banderas para analizar obstaculos ya contados
    for index, i in enumerate(X):   #Se crea un for para analizar cada obstaculo que va surgiendo
        if i < 93 and flag_xi[index] == False:      #Si la posicion de un tubo alcanza cierto valor y no se ha contado antes
            counterPipe += 1        # Se suma uno al contador
            flag_xi[index] = True       # Se cambia la bandera a True para mostrar que ya se hizo el conteo

    letra30 = pygame.font.SysFont("Arial", 30)      # Tamaño y tipo de letra que se usara para mostrar el resultado
    cont = str(counterPipe)      # Se convierte a string el valor del conteo para ser mostrado
    global imagenTextoPresent, rectanguloTextoPresent # Se declara las variables globales que tendran el texto y el rectangulo donde seran mostrados
    imagenTextoPresent = letra30.render("score:  " + cont, True, (255, 255, 255), (0, 0, 0)) #Se aplican las propiedades previamente definidas

    rectanguloTextoPresent = imagenTextoPresent.get_rect()      # Se define el rectangulo donde se mostrara el resultado asi como la posicion
    rectanguloTextoPresent.centerx = pantalla.get_rect().centerx     # Se centra el texto al rectangulo
    rectanguloTextoPresent.centery = 520    #Se elige el tamaño de la letra
    rectanguloTextoPresent.top = 30        #Se elije la pposicion superior del rectangulo de resultados
    rectanguloTextoPresent.left = 780        #Se elije la posicion izquierda del rectangulo de resultados

    pantalla.blit(imagenTextoPresent, rectanguloTextoPresent)        # Se muestra el rectangulo en la pantalla

    return counterPipe      # Se retorna el valor de los obstaculos superados




"""
5. Funcion para mostrar obstaculos en la pantalla
"""


def get_pipe():

    tubo1 = pygame.image.load("sprites/spikes.png").convert()    # Se carga la imagen de los obstaculos
    x = random.randrange(100, 350, 10)      # Se genera una funcion aleatoria para poder generar diferentes obstaculos
    tubo1 = pygame.transform.scale(tubo1, (52, x))      # Se escala el obstaculo inferior
    tubo2 = pygame.transform.scale(tubo1, (52, 635 - x - 150))       # Se escala el obstaculo superior, dejando un espacio entre ambos obstaculos
    tubo2 = pygame.transform.rotate(tubo2, 180)         # Se rota uno de los obstaculos para ser colocado en la parte superior
    lista = [[tubo1, x], [tubo2, 635 - x - 150]]        # Los obstaculos junto con sus posiciones son almacenados en una lista

    return lista # Se retorna la lista con la informacion de los obstaculos


"""
6. Funcion para analizar colision del personaje
"""


def colision():

    global r_imagen_personaje        #Se inicializa la variable que almacena el rectangulo del personaje
    global rect_tubo1_1, rect_tubo1_2,rect_tubo1_3, rect_tubo1_4, rect_tubo1_5, rect_tubo1_6        # Variables globales que contienen los obstaculos de la parte inferior
    global rect_tubo2_1, rect_tubo6_1, rect_tubo6_2      # Variables globales que contienen los obstaculos de la parte superior
    global lista1, lista2, lista3, lista4, lista5, lista6       # Variables globales que contienen la posicion de cada obstaculo
    global y_bird       # Variable global que contiene la posicion del personaje
    global X        # Variable global que almacenara los obstaculos en una lista para su posterior analisis

    flag_return = False     # Variable que se retorna, es falsa en caso de que no ocurra colision

    r_imagen_personaje.top = y_bird     # Se toma al personaje como un rectangulo y se almacenan el valor superior equivalente a la posicion en y del personaje
    r_imagen_personaje.left = 150    # Se almacena el valor izquierda del personaje, el cual es fijo

    for index, i in enumerate(X):       # For para recorrer todas las posibles colisiones con los obstaculos

        rect_tuboi_1[index].left = i      # El valor izquierdo del obstaculo inferior es la posicion del obstaculo en ese momento
        rect_tuboi_1[index].top = 635 - lista[index][0][1]      #El valor superior del obstaculo inferior depende del valor aleatoreo generado previamente
        rect_tuboi_2[index].left = i        # El valor izquierdo del obstaculo superior es la posicion del obstaculo en ese momento
        rect_tuboi_2[index].top = 0         # El valor superior del obstaculo superior es 0 debido a que este obstaculo esta en la parte mas alta de la pantalla
        if rect_tuboi_1[index].colliderect(r_imagen_personaje) or rect_tuboi_2[index].colliderect(r_imagen_personaje) or y_bird>590 or y_bird<=0: # Si el personaje colisiona con alguno de los obstaculos o con la parte superior e inferior del mapa
            flag_return = True      #Bandera que se va a retornar
            return True         #En caso de haber colision se retorna True
    return flag_return      #En caso de que no hayan colisiones se retorna la bandera return, la cual seria falsa


"""
7. Funcion para el movimiento de obstaculos 
"""


def move_pipe():  # Función que inicia el juego (Movimiento de los obstaculos)
    global imagen_de_fondo, posicion_base, vel, gameOver, X, counterPipe  # Se definen algunas variables globales para un posterior uso
    global rect_tubo1_1, rect_tubo1_2, rect_tubo2_1, rect_tubo2_2, rect_tubo3_1, rect_tubo3_2  # Se definen algunas variables globales para un posterior uso
    global rect_tubo4_1, rect_tubo4_2, rect_tubo5_1, rect_tubo5_2, rect_tubo6_1, rect_tubo6_2  # Se definen algunas variables globales para un posterior uso
    global lista, lista1, lista2, lista3, lista4, lista5, lista6  # Se definen algunas variables globales para un posterior uso
    global rect_tuboi_1, rect_tuboi_2, flag_xi, y_bird, aumento_vel  # Se definen algunas variables globales para un posterior uso

    pantalla.blit(imagen_de_fondo, posicion_base)  # Se proyecta la imagen de fondo
    position_y = read_faces()  # Se obtiene una posición en y en base a la pocición del rostro frente a la cámara

    x_bird = 150  # Posición en x para el personaje fijada en 150

    y_bird = position_y * 3.2 - 50  # Se escala la posición en y del personaje

    vel += aumento_vel  # Se aumenta velocidad a los obstaculos

    X = [i - vel for i in X]  # Se mueve cada tuvo a la izquierda
    lista = [lista1, lista2, lista3, lista4, lista5, lista6]  # Se genera un listado con todos los obstaculos
    rect_tuboi_1 = [rect_tubo1_1, rect_tubo2_1, rect_tubo3_1, rect_tubo4_1, rect_tubo5_1,
                    rect_tubo6_1]  # Se obtieenen los rectangulos de los obstaculos superiores
    rect_tuboi_2 = [rect_tubo1_2, rect_tubo2_2, rect_tubo3_2, rect_tubo4_2, rect_tubo5_2,
                    rect_tubo6_2]  # Se obtieenen los rectangulos de los obstaculos inferiores

    gameOver = colision()  # Verifico si el jugador toco un obstacula (¿perdió?)
    score()  # Obtengo el puntaje actual
    for index, i in enumerate(X):
        if X[index] <= -200:  # Comparo si cada obstaculo llegó a la posición -200 (fuera de pantalla, lado izquierdo)
            X[index] = 1000  # Se traslada cada obstaculo a la posición 1000 (fuera de pantalla, lado derecho)
            flag_xi[
                index] = False  # Se activa la bandera de que se debe contar el obstaculo correspondiente cuando el personaje lo supere (lo evada)
            lista[index] = get_pipe()  # Reemplazo los obstaculos anteriores por obstaculos nuevos aleatorios
            rect_tuboi_1[index], rect_tuboi_2[index] = lista[index][0][0].get_rect(), lista[index][0][
                0].get_rect()  # Se obtiene el rectangulo de cada obstaculo

    color = imagen_personaje.get_at((0, 0))  # Se obtiene el color del primer pixel de la imagen del personaje
    imagen_personaje.set_colorkey(
        color)  # Se elimina los pixeles que contengan el color anterior en el resto de la imagen (del personaje)
    pantalla.blit(imagen_personaje, [x_bird, y_bird])  # Se muestra al personaje en pantalla
    for index, i in enumerate(X):  # Se recorren todos los obstaculos
        pantalla.blit(lista[index][1][0], [X[index], 0])  # Se dibujan todos los obstaculos superiores
        pantalla.blit(lista[index][0][0],
                      [X[index], 635 - lista[index][0][1]])  # Se dibujan todos los obstaculos inferiores

    global imagenTextoPresent, rectanguloTextoPresent  # Defino variables globales tipo globales
    pantalla.blit(imagenTextoPresent, rectanguloTextoPresent)  # Muestro el puntaje en pantalla

    clock.tick(fps)  # Limitamos el programa a 60 fps
    pygame.display.update()  # Actualizo la pantalla
    return gameOver  # Se devuelve si el jugador perdió o no


lista1 = get_pipe()  # Primer par de tubos
rect_tubo1_1 = lista1[0][0].get_rect()  # Tubo de abajo
rect_tubo1_2 = lista1[1][0].get_rect()  # Tubo de arriba
lista2 = get_pipe()  # Segundo par de tubos
rect_tubo2_1 = lista2[0][0].get_rect()  # Tubo de abajo
rect_tubo2_2 = lista2[1][0].get_rect()  # Tubo de arriba
lista3 = get_pipe()  # Tercer par de tubos
rect_tubo3_1 = lista3[0][0].get_rect()  # Tubo de abajo
rect_tubo3_2 = lista3[1][0].get_rect()
lista4 = get_pipe()  # Cuarto par de tubos
rect_tubo4_1 = lista4[0][0].get_rect()  # Tubo de abajo
rect_tubo4_2 = lista4[1][0].get_rect()
lista5 = get_pipe()  # Quinto par de tubos
rect_tubo5_1 = lista5[0][0].get_rect()  # Tubo de abajo
rect_tubo5_2 = lista5[1][0].get_rect()  # Tubo de arriba
lista6 = get_pipe()  # Sexto par de tubos
rect_tubo6_1 = lista6[0][0].get_rect()  # Tubo de abajo
rect_tubo6_2 = lista6[1][0].get_rect()  # Tubo de arriba


def iniciar_variables():  # Función para inicializar algunas variables importantes
    global posicion_base, ofset, inicio_tubo, X, vel, y_temp  # Definición de varibles globales
    y_temp = 0  # variable temporal la cual sera usada para almacenar valores previos de y
    posicion_base = [0, 0]  # Posición inicial (eje de referencia)
    ofset = 200  # Separación entre cada par de tubos
    inicio_tubo = 1000  # El primer par de tubos inician en la posición 1000 (Fuera de la pantalla)
    X = [inicio_tubo + index * ofset for index in
         range(6)]  # El segundo par de tubos inicia en 1200, el tercero en 1400,..


gameStarted = False  # Bandera que indica que el juego no ha iniciado
gameOver = False  # Bandera que indica que el jugador no ha perdido

while True:  # Bucle principal

    for event in GAME_EVENTS.get():  # Se buscan todos lo eventos que puedan ocurrir
        if event.type == pygame.KEYDOWN:  # Eventos de pulsaciones en teclas

            if event.key == pygame.K_ESCAPE:  # Si la tecla ESC fue pulsada
                pygame.quit()  # Desactiva la biblioteca Pygame.
                sys.exit()  # Finalizar el programa
            if event.key == pygame.K_SPACE and gameStarted == False:  # Si  la tecla ESPACIO es pulsada pero no se está jugando
                iniciar_variables()  # Se inicializar algunas variables importantes
                iniciarVel = True  # Se activa una bandera que indican que se debe inicializar la velocidad
                gameStarted = True  # Se activa una bandera que indica que se está jugando
                gameOver = False  # Se activa una bandera que indica que no ha perdido

        if event.type == GAME_GLOBALS.QUIT:  # Si se clickea en la x de cerrar el programa
            pygame.quit()  # Desactiva la biblioteca Pygame.
            sys.exit()  # Finalizar el programa

    if (gameOver):  # Si el jugador perdió
        vel = 0  # velocidad de los tubos = 0
        aumento_vel = 0  # Aceleracción = 0, para mostrar el instante en que perdió
        gameStarted = False  # Se desactiva la bandera que indica que se está jugando

    if (gameStarted):  # Si se está jugando..
        if (iniciarVel == True):  # verifico si debo inicializar la velicidad
            vel = 5  # Inicializo la velocidad
            aumento_vel = 0.01  # Inicializo la aceleracción
            flag_xi = [False, False, False, False, False, False]
            counterPipe = 0  # Score en 0
            iniciarVel = False  # Indico que no debo volver a inicializar la velocidad

        gameOver = move_pipe()  # Empieza el juego

    else:  # Si no se está jugando
        if (gameOver == False):  # y tampoco ha perdido
            pantalla.blit(imagen_de_incio, [0, 0])  # Se muestra mensaje (pantalla) de inicio

        else:  # Si no está jugando pero ya perdió
            color = imagen_de_fin.get_at((0, 0))  # Obtengo el color del primer pixel de la imagen GAME OVER
            imagen_de_fin.set_colorkey(color)  # Elimino los pixeles con el color anterior anterior en toda la imagen
            pantalla.blit(imagen_de_fin, [287, 70])  # Se muestra la imagen de GAME OVER en pantalla

        clock.tick(fps)  # Limitamos el programa a 60 fps
        pygame.display.update()  # Actualizamos la pantalla

pygame.quit()  # Fin del juego
