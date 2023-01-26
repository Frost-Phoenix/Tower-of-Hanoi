FPS = 60

WINDOW_WIDTH = 540
WINDOW_HEIGHT = 400

# Minimum de déplacement pour gagné en fonction de chaque nombres de disques
MIN_MOVES = [1, 3, 7, 15, 31, 63, 127]

# Differentes pallettes de couleurs pour les disques
RED_GRADIENT = [(250 - i * 30, 10, 10) for i in range(7)]
GREEN_GRADIENT = [(10,250 - i * 30, 10) for i in range(7)]
BLUE_GRADIENT = [(10,10,250 - i * 30) for i in range(7)]
RAINBOW = [(255, 0 , 0), (255, 127, 0), (255, 255, 0), (0, 250, 0), (0, 0, 255), (148, 0, 211), (75, 0, 130)]
PILARS_COLORS = [BLUE_GRADIENT, GREEN_GRADIENT, RED_GRADIENT, RAINBOW]


class Pos:
    """permet de simplifier l'acces à un couple de coordonées"""

    def __init__(self, pos: tuple) -> None:
        self.x = pos[0]
        self.y = pos[1]