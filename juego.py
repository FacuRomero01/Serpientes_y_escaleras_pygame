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
        res =  (x, y)
    
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
    
    res = (x, y)
    return res

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

def pantalla_ingreso_nombre(ventana)-> any:
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
        None: Si la ventana se cierra antes de confirmar, devuelve None
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
    """
    Función que utiliza "random" para elegir una pregunta al azar de una lista de preguntas

    Args:
        preguntas (list): lista que contiene multiples preguntas

    Return:
        dict: Devuelve la pregunta seleccionada 
    """
    preg_selec = random.choice(preguntas)
    return preg_selec

def valida_respuesta(pregunta:dict, respuesta:chr) -> bool:
    """
    Función que valida si la respuesta seleccionada es la correcta

    Args:
        pregunta (dict): Diccionario que contiene la pregunta, cada opcion y la repsuesta correcta

        respuesta (chr): Letra que representa la opcion a chequar si es correcta o no

    Return:
        Bool: Devuelve True si es la opción correcta y False si es incorrecta
    """
    if respuesta == "a" or respuesta == "b" or respuesta == "c":
            res = respuesta == pregunta["respuesta_correcta"]
            
    return res

def pantalla_preguntas(ventana, ancho, preguntas) -> bool:
    """
    Muestra una pantalla interactiva en Pygame que muestra la pregunta a responder y permite con el click izquierdo seleccionar sus posibles respuestas
    Requiere importar el módulo "Colores"
    Requiere la funcion "selecciona_pregunta"
    Requiere la funcion "valida_respuesta"
    Requiere pygame previamente inicializado

    La función:
    - Muestra por pantalla la pregunta a responder con sus 3 posibles opciones
    - Permite al usuario hacer click izquierdo en cualquiera de las 3 opcines para marcar cual elije
    - Chequea si la opcion es correcta o no, si lo es elimina la pregunta de la lista para que no se vuelva a preguntar
    - Finaliza y retorna el valor booleano de esa comparación
    - Si el usuario no responde en 15 segundos devuelve False
    
    Args:
        ventana: Superficie de Pygame donde se dibuja la interfaz de entrada de texto
        
        ancho (int): El ancho de la ventana
        
        preguntas (list): lista que contiene multiples preguntas

    Returns:
        Bool: devuelve el valor booleano True si es correcta la respuesta y False si no lo es
        str: En el caso que cierre la ventana devuelve "salir"
    """
    
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
    tiempo_inicio = pygame.time.get_ticks()
    tiempo_limite = 15000
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
        
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante_ms = tiempo_limite - (tiempo_actual - tiempo_inicio)
        tiempo_restante_seg = max(0, tiempo_restante_ms // 1000)
        
        texto_timer = fuente.render(f"Tiempo: {tiempo_restante_seg}s", True, colores.BLACK)
        ventana.blit(texto_timer, (ancho - texto_timer.get_width() - 10, 10))
        
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

        if tiempo_restante_ms <= 0:
            flag_seguir = False
            res = False
        
        if resp_selec is not None:
            res = valida_respuesta(preg_selec, resp_selec)
        if res:
            preguntas.remove(preg_selec)

        pygame.display.flip()
    
    return res

def aplica_escaleras(posicion) -> int:
    """
    Función que aplica el efecto de una escalera en la posición indicada.

    Args:
        posicion (int): La posición actual del jugador en el tablero.

    Return:
        int: Devuelve la nueva posición luego de aplicar la escalera (si corresponde).
    """
    salto = serp_esc[posicion]
    if salto > 0:
        print(f"¡Escalera! Avanzás {salto} casillas.")
        res = posicion + salto
    else:
        res = posicion
    
    return res

def aplica_serpientes(posicion) -> int:
    """
    Función que aplica el efecto de una serpiente en la posición indicada.

    Args:
        posicion (int): La posición actual del jugador en el tablero.

    Return:
        int: Devuelve la nueva posición luego de aplicar la serpiente (si corresponde).
    """
    salto = serp_esc[posicion]
    if salto > 0:
        print(f"¡Serpiente! Retrocedes {salto} casillas.")
        res = posicion - salto
    else:
        res = posicion
    
    return res

def pantalla_sigue_jugando(ventana, ancho) -> any:
    """
    Función que muestra una pantalla para consultar al jugador si desea seguir jugando.

    Args:
        ventana: Objeto ventana de pygame donde se renderiza la pantalla.
        ancho (int): Ancho de la ventana, utilizado para centrar los textos.

    Return:
        bool: Devuelve True si el jugador desea seguir jugando, False si no
        str: Devuelve "salir" si cierra la ventana.
    """
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

def pantalla_resultado_final(ventana, ancho, puntaje, posicion, resultado) -> any:
    """
    Función que muestra la pantalla de resultado final al terminar el juego,
    indicando si el jugador ganó o perdió, su posición y puntaje. en ammbos casos suena un audo de fondo dependiendo del resultado

    Args:
        ventana: Objeto ventana de pygame donde se renderiza la pantalla.
        ancho (int): Ancho de la ventana, utilizado para centrar los textos.
        puntaje (int): Puntaje final obtenido por el jugador.
        posicion (int): Posición final del jugador en el ranking o la partida.
        resultado (str): Resultado del juego ("gano" o "perdio").

    Return:
        str: Devuelve "menu" si el usuario quiere volver al menú, o "salir" si cierra la ventana.
    """
    coord_x_centro = ancho // 2
    y_inicial = 150
    espaciado = 150
    
    sonido_gano = pygame.mixer.Sound("./pygame/sonido_gano.mp3")
    sonido_perdio = pygame.mixer.Sound("./pygame/sonido_perdio.mp3")

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
    sonido_reproducido = False

    while flag_seguir:
        if resultado == "gano":
            if not sonido_reproducido:
                sonido_gano.play()
                sonido_reproducido = True
            
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
            if not sonido_reproducido:
                sonido_perdio.play()
                sonido_reproducido = True

            
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

def ejecutar_juego(ventana, ancho, preguntas) -> str:
    """
    Función principal que ejecuta el ciclo de juego, controlando el flujo de preguntas,
    movimiento del jugador en el tablero, aplicación de serpientes y escaleras,
    y la pantalla de resultados finales.

    Args:
        ventana: Objeto ventana de pygame donde se renderiza el juego.
        ancho (int): Ancho de la ventana, utilizado para centrar elementos gráficos.
        preguntas (list): Lista de preguntas que se utilizarán durante la partida.

    Return:
        str: Devuelve "menu" si el jugador quiere volver al menú, o "salir" si cierra el juego.
    """
    res = None
    quiere_seguir = None
    pos_jugador = 29
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
