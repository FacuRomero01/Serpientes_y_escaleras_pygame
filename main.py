import pygame
from menu import menu_principal
from juego import ejecutar_juego
from puntajes import pantalla_muestra_puntaje
from preguntas import preguntas

def main():
    """
    Función principal del programa. Inicializa pygame, configura la ventana
    y controla el flujo de navegación del juego a través de los distintos estados
    (menú, jugar, puntajes, salir)

    Args:
        No recibe argumentos

    Return:
        None
    """
    pygame.init()
    pygame.mixer.init()
    
    # Configuración inicial
    ancho, alto = 600, 600
    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Serpientes y Escaleras")
    
    estado_actual = "menu" 
    
    seguir = "s"
    while seguir == "s":
        if estado_actual == "menu":
            estado_actual = menu_principal(ventana, ancho)
        elif estado_actual == "jugar":
            estado_actual = ejecutar_juego(ventana, ancho, preguntas)
        elif estado_actual == "puntajes":
            estado_actual = pantalla_muestra_puntaje(ventana, ancho)
        elif estado_actual == "salir":
            seguir = "n"
    
    pygame.quit()

main()