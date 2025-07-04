import pygame
import colores
import random
from puntajes import guarda_puntaje

serp_esc = [
    0,  1,  0,  0,  0,  3,  0,  0,  0,  0,
    0,  1,  0,  0,  2,  1,  1,  0,  0,  0,
    1,  0,  0,  2,  0,  0,  0,  1,  0,  0,
    0
]

tablero = pygame.image.load("./pygame/Tablero.png")
tablero = pygame.transform.scale(tablero, (600, 600))

def obtener_posicion_casilla(numero_casilla) -> tuple:
    """
    Calcula la posicion del centro de una casilla del tablero de juego 6x6 con casillas del 0 al 30 (tablero de 600x600 px.)
    Las filas alternan se alternan en direccion de lectura como una S.
    El tablero empieza por la casilla 0 que se encuentra en la esquina inferior izquierda
    
    Fila 1 = Casilla 0
    Fila 2 = Casillas 1-6
    Fila 3 = Casillas 7-12
    Fila 4 = Casillas 13-18
    Fila 5 = Casillas 19-24
    Fila 6 = Casillas 25-30

    Args:
        numero_casilla (int): Entero que representa la posición actual del jugador.

    Return:
        tupla (int, int): Tupla de enteros que representa las coordenadas x,y de la casilla actual del jugador
    """

    tamaño_casilla = 100 
    
    if numero_casilla == 0 or numero_casilla < 0:
        # casilla 0 en esquina inferior izquierda (centro)
        x = 0 + tamaño_casilla // 2
        y = 600 - tamaño_casilla // 2
        return (x, y)
    
    fila = (numero_casilla - 1) // 6 + 1    # arranca en la fila 2
    columna_en_fila = (numero_casilla - 1) % 6
    
    if fila % 2 == 1:
        # filas impares (fila 3,5,7...) de izquierda a derecha
        x = columna_en_fila * tamaño_casilla
    else:
        # filas pares (fila 2,4,6...) de derecha a izquierda
        x = (5 - columna_en_fila) * tamaño_casilla
    
    # calcular Y
    y = 600 - (fila + 1) * tamaño_casilla + tamaño_casilla // 2
    
    # centrar la ficha en la casilla
    x += tamaño_casilla // 2
    
    return (x, y)

def capturar_texto(texto_actual:str, evento) -> str:
    """
    Función encargada de capturar el input del usuario y devolverlo cuando se presione ENTER

    Args:
        texto_actual (str): string incialmente vacio en donde se guardara el input del usuario

        evento: Objeto de evento de Pygame (pygame.event.Event) que contiene la tecla presionada
                y el carácter asociado (evento.unicode).

    Return:
        str: Texto actualizado después de procesar los eventos del teclado
    """
    if evento.key == pygame.K_BACKSPACE:
        texto_actual = texto_actual[:-1]
    else:
        texto_actual += evento.unicode
    return texto_actual

def pantalla_ingreso_nombre(ventana):
    """
    Muestra una pantalla interactiva en Pygame para permitir al usuario ingresar su nombre.
    Requiere importar el módulo "Colores"
    Requiere la funcion "capturar_texto"
    Requiere pygame previamente inicializado

    La función:
    - Presenta un mensaje de texto pidiendo el nombre.
    - Permite al usuario escribir usando el teclado, incluyendo corrección con la tecla Backspace.
    - Confirma el texto ingresado cuando se presiona ENTER, siempre que no esté vacío.
    - Finaliza y retorna None si el usuario cierra la ventana.
    
    Args:
        ventana: Superficie de Pygame donde se dibuja la interfaz de entrada de texto.

    Returns:
        str: El nombre ingresado como texto (sin espacios iniciales/finales) si el usuario confirma con ENTER
        None: Si la ventana se cierra antes de confirmar, devuelve None.
    """
    
    fuente = pygame.font.SysFont("Arial", 22)
    texto_ingresado = ""
    ejecutando = True
    
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                return None
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if texto_ingresado.strip() != "":
                        ejecutando = False
                        return texto_ingresado
                else:
                    texto_ingresado = capturar_texto(texto_ingresado, evento)
        
        ventana.fill(colores.WHITE)
        mensaje = fuente.render("Ingrese su nombre y presione ENTER:", True, colores.BLACK)
        texto_surface = fuente.render(texto_ingresado, True, colores.BLACK)
        
        ventana.blit(mensaje, (50, 200))
        ventana.blit(texto_surface, (50, 250))
        
        pygame.display.flip()

def selecciona_pregunta(preguntas:list) -> dict:
    preg_selec = random.choice(preguntas)
    return preg_selec

def valida_respuesta(pregunta:dict, respuesta:chr) -> bool:
    if respuesta == "a" or respuesta == "b" or respuesta == "c":
            res = respuesta == pregunta["respuesta_correcta"]
            
    return res

def pantalla_preguntas(ventana, ancho, preguntas):
    coord_x_centro = ancho // 2
    y_inicial = 200
    espaciado = 150
    
    preg_selec = selecciona_pregunta(preguntas)

    fuente = pygame.font.SysFont("Arial", 22)

    texto_pregunta = fuente.render(f"{preg_selec['pregunta']}", True, colores.BLACK)
    texto_resp_a = fuente.render(f"a. {preg_selec['respuesta_a']}", True, colores.BLACK)
    texto_resp_b = fuente.render(f"b. {preg_selec['respuesta_b']}", True, colores.BLACK)
    texto_resp_c = fuente.render(f"c. {preg_selec['respuesta_c']}", True, colores.BLACK)

    rect_pregunta = texto_pregunta.get_rect(center=(coord_x_centro, y_inicial))
    rect_resp_a = texto_resp_a.get_rect(center=(coord_x_centro-espaciado, y_inicial+100))
    rect_resp_b = texto_resp_b.get_rect(center=(coord_x_centro, y_inicial*2))
    rect_resp_c = texto_resp_c.get_rect(center=(coord_x_centro+espaciado, y_inicial+100))
    

    resp_selec = None
    res = None
    flag_seguir = True
    while flag_seguir:
        
        ventana.fill(colores.WHITE)
        pygame.draw.rect(ventana, colores.RED1, rect_pregunta)
        pygame.draw.rect(ventana, colores.RED1, rect_resp_a)
        pygame.draw.rect(ventana, colores.RED1, rect_resp_b)
        pygame.draw.rect(ventana, colores.RED1, rect_resp_c)
        
        ventana.blit(texto_pregunta, rect_pregunta.topleft)
        ventana.blit(texto_resp_a, rect_resp_a.topleft)
        ventana.blit(texto_resp_b, rect_resp_b.topleft)
        ventana.blit(texto_resp_c, rect_resp_c.topleft)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                flag_seguir = False
                res = "salir"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if rect_resp_a.collidepoint(evento.pos):
                        flag_seguir = False
                        resp_selec = "a"
                    elif rect_resp_b.collidepoint(evento.pos):
                        flag_seguir = False
                        resp_selec = "b"
                    elif rect_resp_c.collidepoint(evento.pos):
                        flag_seguir = False
                        resp_selec = "c"

        if resp_selec is not None:
            res = valida_respuesta(preg_selec, resp_selec)
        if res:
            preguntas.remove(preg_selec)

        pygame.display.flip()
    
    return res

def aplica_escaleras(posicion) -> int:
    salto = serp_esc[posicion]
    if salto > 0:
        print(f"¡Escalera! Avanzás {salto} casillas.")
        res = posicion + salto
    else:
        res = posicion
    
    return res

def aplica_serpientes(posicion) -> int:
    salto = serp_esc[posicion]
    if salto > 0:
        print(f"¡Serpiente! Retrocedes {salto} casillas.")
        res = posicion - salto
    else:
        res = posicion
    
    return res

def pantalla_sigue_jugando(ventana, ancho) -> bool:
    coord_x_centro = ancho // 2
    y_inicial = 200
    espaciado = 150

    fuente = pygame.font.SysFont("Arial", 22)
    texto_seguir = fuente.render("¿Desea seguir jugando?", True, colores.BLACK)
    texto_si = fuente.render("SI", True, colores.BLACK)
    texto_no = fuente.render("NO", True, colores.BLACK)
    
    rect_seguir = texto_seguir.get_rect(center=(coord_x_centro, y_inicial))
    rect_si = texto_si.get_rect(center=(coord_x_centro-espaciado, y_inicial+100))
    rect_no = texto_no.get_rect(center=(coord_x_centro+espaciado, y_inicial+100))
    
    res = None
    flag_seguir = True
    while flag_seguir:
        
        ventana.fill(colores.WHITE)
        pygame.draw.rect(ventana, colores.RED1, rect_seguir)
        pygame.draw.rect(ventana, colores.RED1, rect_si)
        pygame.draw.rect(ventana, colores.RED1, rect_no)

        # Dibujar textos encima
        ventana.blit(texto_seguir, rect_seguir.topleft)
        ventana.blit(texto_si, rect_si.topleft)
        ventana.blit(texto_no, rect_no.topleft)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                flag_seguir = False
                res = "salir"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if rect_si.collidepoint(evento.pos):
                            print("SI")
                            flag_seguir = False
                            res = True
                        elif rect_no.collidepoint(evento.pos):
                            print("NO")
                            flag_seguir = False
                            res = False

        pygame.display.flip()
    
    return res

def pantalla_resultado_final(ventana, ancho, puntaje, posicion, resultado):
    coord_x_centro = ancho // 2
    y_inicial = 150
    espaciado = 150
    
    fuente = pygame.font.SysFont("Arial", 22)
    texto_ganador = fuente.render("¡¡¡GANADOR!!!", True, colores.BLACK)
    texto_termino_juego = fuente.render("Se terminó el juego", True, colores.BLACK)
    texto_posicion= fuente.render(f"Usted terminó en la posición: {posicion}", True, colores.BLACK)
    texto_puntaje= fuente.render(f"Su puntaje fue de: {puntaje}", True, colores.BLACK)
    texto_menu= fuente.render("Menú", True, colores.BLACK)
    
    rect_ganador = texto_ganador.get_rect(center=(coord_x_centro, y_inicial))
    rect_termino_juego = texto_termino_juego.get_rect(center=(coord_x_centro, y_inicial))
    rect_menu= texto_menu.get_rect(center=(coord_x_centro, y_inicial + espaciado * 2))
    rect_posicion = texto_posicion.get_rect(center=(coord_x_centro, y_inicial + espaciado))
    rect_puntajes = texto_puntaje.get_rect(center=(coord_x_centro, y_inicial + espaciado + 50))
    
    res = None
    flag_seguir = True
    
    while flag_seguir:
        if resultado == "gano":
            ventana.fill(colores.WHITE)
            ventana.blit(texto_ganador, rect_ganador.topleft)
            ventana.blit(texto_posicion, rect_posicion.topleft)
            ventana.blit(texto_puntaje, rect_puntajes.topleft)
            ventana.blit(texto_menu, rect_menu.topleft)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    flag_seguir = False
                    res = "salir"

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if rect_menu.collidepoint(evento.pos):
                            res = "menu"
                            flag_seguir = False

        elif resultado == "perdio":
            ventana.fill(colores.WHITE)
            ventana.blit(texto_termino_juego, rect_termino_juego.topleft)
            ventana.blit(texto_posicion, rect_posicion.topleft)
            ventana.blit(texto_puntaje, rect_puntajes.topleft)
            ventana.blit(texto_menu, rect_menu.topleft)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    flag_seguir = False
                    res = "salir"

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if rect_menu.collidepoint(evento.pos):
                            res = "menu"
                            flag_seguir = False
    
        pygame.display.flip()
    return res

def ejecutar_juego(ventana, ancho, preguntas):

    res = None
    quiere_seguir = None
    pos_jugador = 15
    puntaje = 0
    flag_preguntas = True
    ejecutando = True
    

    nombre_jugador = pantalla_ingreso_nombre(ventana)
    print(nombre_jugador)
    
    if nombre_jugador == None:
        return "salir"
    
    while ejecutando:
        
        if len(preguntas) == 0:
            flag_preguntas = False
        else:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                    res =  "salir"
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                        res =  "menu"
                    elif evento.key == pygame.K_RETURN:
                        respuesta = pantalla_preguntas(ventana, ancho, preguntas)
                        if respuesta:
                            pos_jugador += 1
                            puntaje += 1
                            pos_jugador = aplica_escaleras(pos_jugador)
                            quiere_seguir = pantalla_sigue_jugando(ventana,ancho)
                        else:
                            pos_jugador -= 1
                            puntaje -= 1
                            if pos_jugador < 0:
                                pos_jugador = 0
                            if puntaje < 0:
                                puntaje = 0
                            pos_jugador = aplica_serpientes(pos_jugador)
                            quiere_seguir = pantalla_sigue_jugando(ventana,ancho)
                        print(pos_jugador)

        ventana.blit(tablero, (0,0))

        x, y = obtener_posicion_casilla(pos_jugador)
        pygame.draw.circle(ventana, colores.RED1, (x, y), 7)

        if pos_jugador == 30:
            resultado = "gano"
            res = pantalla_resultado_final(ventana,ancho,puntaje,pos_jugador,resultado)
            guarda_puntaje(nombre_jugador, pos_jugador, puntaje)

            ejecutando = False 
        elif quiere_seguir == False:
            resultado = "perdio"
            res = pantalla_resultado_final(ventana,ancho,puntaje,pos_jugador,resultado)
            guarda_puntaje(nombre_jugador, pos_jugador, puntaje)
            
            ejecutando = False
        elif flag_preguntas == False:
            resultado = "perdio"
            res = pantalla_resultado_final(ventana,ancho,puntaje,pos_jugador,resultado)
            guarda_puntaje(nombre_jugador, pos_jugador, puntaje)
            ejecutando = False
        
        pygame.display.flip()

    return res
