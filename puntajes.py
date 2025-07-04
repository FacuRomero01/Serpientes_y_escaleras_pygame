import colores
import pygame


def guarda_puntaje(nombre, posicion, puntaje):
    with open("scores.csv", "a") as archivo:
        archivo.write(f"{nombre},{posicion},{puntaje}\n")

def pantalla_muestra_puntaje(ventana, ancho):
    coord_x_centro = ancho // 2
    y_inicial = 50
    espaciado = 50
    
    fuente = pygame.font.SysFont("Arial", 22)
    
    # Leer el archivo de puntajes
    puntajes = []
    with open("scores.csv", "r") as archivo:
        next(archivo)
        for linea in archivo:
            datos = linea.strip().split(",")
            if len(datos) == 3:
                puntajes.append((datos[0], datos[1], datos[2]))  # (nombre, posicion, puntaje)
    texto_titulo = fuente.render("Nombre - Casillero - Puntaje", True, colores.BLACK)
    texto_menu= fuente.render("Menú", True, colores.BLACK)
    rect_menu= texto_menu.get_rect(center=(coord_x_centro, y_inicial + 100 + espaciado + 300))

    ventana.fill(colores.WHITE)  # Limpia la ventana
    ventana.blit(texto_menu, rect_menu.topleft)
    ventana.blit(texto_titulo, (coord_x_centro - texto_titulo.get_width() // 2, y_inicial))
    # Mostrar cada puntaje

    ultimos_seis = puntajes[-6:]
    for i, (nombre, posicion, puntaje) in enumerate(ultimos_seis):
        texto_puntaje = fuente.render(f"{nombre} - Posición: {posicion} - Puntaje: {puntaje}", True, colores.BLACK)
        ventana.blit(texto_puntaje, (coord_x_centro - texto_puntaje.get_width() // 2, y_inicial + espaciado * (i + 1)))
    # Mantener la pantalla hasta que se presione una tecla
    flag_seguir = True
    while flag_seguir:
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