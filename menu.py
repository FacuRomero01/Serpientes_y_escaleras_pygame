import pygame
import colores

def menu_principal(ventana, ancho):
    """
    Función que muestra el menú principal del juego, permitiendo al usuario
    elegir entre jugar, ver puntajes o salir

    Args:
        ventana: Objeto ventana de pygame donde se renderiza el menú.
        ancho (int): Ancho de la ventana, utilizado para centrar los botones

    Return:
        str: Devuelve "jugar" si se selecciona comenzar el juego,
            "puntajes" si se selecciona ver puntajes,
            o "salir" si se decide salir del juego
    """
    fondo = pygame.image.load("./pygame/fondo.jpg")

    coord_x_centro = ancho // 2
    y_inicial = 200
    espaciado = 100

    fuente = pygame.font.SysFont("Arial", 30)
    texto_jugar = fuente.render("Jugar", True, colores.BLACK)
    texto_puntajes = fuente.render("Puntajes", True, colores.BLACK)
    texto_salir = fuente.render("Salir", True, colores.BLACK)

    rect_jugar = texto_jugar.get_rect(center=(coord_x_centro, y_inicial))
    rect_puntajes = texto_puntajes.get_rect(center=(coord_x_centro, y_inicial + espaciado))
    rect_salir = texto_salir.get_rect(center=(coord_x_centro, y_inicial + espaciado * 2))

    res = None
    flag_correr = True
    while flag_correr:

        ventana.blit(fondo,(0,0))
        pygame.draw.rect(ventana, colores.RED1, rect_jugar)
        pygame.draw.rect(ventana, colores.RED1, rect_puntajes)
        pygame.draw.rect(ventana, colores.RED1, rect_salir)

        ventana.blit(texto_jugar, rect_jugar.topleft)
        ventana.blit(texto_puntajes, rect_puntajes.topleft)
        ventana.blit(texto_salir, rect_salir.topleft)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                flag_correr = False
                res = "salir"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if rect_jugar.collidepoint(evento.pos):
                            flag_correr = False
                            res = "jugar"
                        elif rect_puntajes.collidepoint(evento.pos):
                            flag_correr = False
                            res = "puntajes"
                        elif rect_salir.collidepoint(evento.pos):
                            flag_correr = False
                            res = "salir"

        pygame.display.flip()
    return res
