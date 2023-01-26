import sys
import pygame as pg
#------------------------------------------------------
from data.scripts.Game import Game
from data.scripts.Utils import *


def main() -> None:

    pg.init()

    pg.display.set_caption("Tours de Hanoï")
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    # Variables
    game = Game(window)
    
    # Game loop
    game_runing = True
    while game_runing:

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            # Event d'apuit de touches de clavier qui update le jeu (le jeu fonctione par event)
            elif event.type == pg.KEYDOWN: game.use_key(event.key)
      
        # Déssine le jeu 
        game.draw()

        pg.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()