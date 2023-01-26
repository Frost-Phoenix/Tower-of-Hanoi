import sys
import pygame as pg
from time import sleep
#------------------------------------------------------
from data.scripts.Utils import *
from data.scripts.Piece import Piece
from data.scripts.TextManager import TextManager


class Game:
    """Class qui gère la logique du jeu"""

    def __init__(self, display_surface: pg.Surface) -> None:
        """Initialisation des variables et du jeu"""
        self.display_surface = display_surface

        self.selected_col = None
        self.nb_pilars = 6
        self.pilars_color = 0
        self.pieces = []
        self.nb_moves = 0
        self.min_moves = MIN_MOVES[6]
        self.move_instant = False
        self.win = False

        self.textManager = TextManager()

        # Initialisation
        self.start()

    def start(self) -> None:
        """Crée les textes d'affichages au début du jeu et les piliers / disques"""
        self.textManager.add_txt("move_counter", "Moves : 0", (410,15))
        self.textManager.add_txt("min_nb_moves", f"Best solve : {self.min_moves} moves", (20,15))
        self.textManager.add_txt("solve", "S - solve", (51,340))
        self.textManager.add_txt("instant", "I - instant", (212,340))
        self.textManager.add_txt("color", "C - color", (391,340))
        self.gen_pilars()

    def gen_pilars(self) -> None:
        """Crée self.nb_pilars disques en les positionant sur le pilier de gauche"""
        self.pieces = []

        # Du plus grand disque au plus petit
        for i in range(self.nb_pilars, -1, -1): 
            self.pieces.append(Piece(i,                                                                 # id
                                     0,                                                                 # col
                                     (100 - (50 + 10 * i) // 2, 230 - (20 * (self.nb_pilars - i))),     # pos(x, y)
                                     50 + 10 * i))                                                      # width

    def move_pilar(self, current_col: int, new_col: int, speed: int, instant_move: bool) -> None:
        """Deplace un disque d'un pilier a uyn autre si cela est possible"""
        pilars_in_current_col = [piece for piece in self.pieces if piece.col == current_col]
        pilars_in_new_col = [piece for piece in self.pieces if piece.col == new_col]

        # Si il y a un disque dans la colone séléctioné 
        if len(pilars_in_current_col) != 0:
            min_index_in_new_col = 7
            for piece in pilars_in_new_col:
                if piece.id < min_index_in_new_col: min_index_in_new_col = piece.id

            index = 7
            pilar_to_move = None
            for piece in pilars_in_current_col:
                if piece.id < index and piece.id < min_index_in_new_col: pilar_to_move = piece

            # Si on peut déplacer la première pice de la colone sélctioné dans la colone destination 
            # Si la "taile" du disque choisi est inferieur a celle du premier de la colone destination
            if pilar_to_move != None:
                self.pieces[self.pieces.index(pilar_to_move)].col = new_col

                self.nb_moves += 1
                if len(pilars_in_new_col) == self.nb_pilars and new_col == 2: 
                    self.win = True
                    if self.nb_moves == self.min_moves: self.textManager.update_txt("move_counter", f"Moves : {self.nb_moves}", color=(225,250,10))
                    else: self.textManager.update_txt("move_counter", f"Moves : {self.nb_moves}", color=(10,250,10))
                else: self.textManager.update_txt("move_counter", f"Moves : {self.nb_moves}")

                if instant_move: 
                    piece.pos.x = 100 - piece.width // 2 + 170 * piece.col
                    self.pieces[self.pieces.index(pilar_to_move)].pos.y = 250 - (20 * len([piece for piece in self.pieces if piece.col == new_col]))
                # Animation
                else:
                    # Go up
                    while piece.pos.y != 50:
                        piece.pos.y -= 2
                        self.update_pygame(0.01 / speed)

                    # Go to the right pilar
                    delta_x = 2 if new_col > current_col else -2
                    while piece.pos.x != (100 - piece.width // 2 + 170 * new_col):
                        piece.pos.x += delta_x
                        self.update_pygame(0.01 / speed)

                    # Go down
                    while piece.pos.y != (250 - (len(pilars_in_new_col) + 1) * 20):
                        piece.pos.y += 2
                        self.update_pygame(0.01 / speed)

    def solve(self) -> None:
        """Fonction de resolution, donne une liste de déplacement a faire dans l'ordre puis les effectue"""
        def hanoi(src: int, dest: int, interm: int, n: int, sol: list) -> None:
            """fonction recurcive faite en cour qui remplie la liste de mouvement a faire pour la résolution"""
            if n == 1:
                # print("Déplace de", src, "à", dest)
                sol.append((src, dest))
                return

            hanoi(src, interm, dest, n - 1, sol)
            hanoi(src, dest, interm, 1, sol)
            hanoi(interm, dest, src, n - 1, sol)

        sol = []
        hanoi(0, 2, 1, len(self.pieces), sol)

        for src, dest in sol:
            self.move_pilar(src, dest, 100, False)

    def use_key(self, key: int) -> None:
        """Effectue les actions correspondentes à certaines touches"""
        # Touches 1 à 7 (& à è, pas le pavé numérique) qui change les nb de disques du jeu
        if key >= 49 and key <= 55: 
            self.win = False
            self.selected_col = None
            self.nb_moves = 0
            self.nb_pilars = key - 49 
            self.min_moves = MIN_MOVES[self.nb_pilars]
            self.textManager.update_txt("move_counter", f"Moves : {self.nb_moves}")
            self.textManager.update_txt("min_nb_moves", f"Best solve : {self.min_moves} moves")
            self.gen_pilars()
        # Fléches dirrectionelles qui sont utilisé pour bouger les disques, donc jouer manuellement
        elif key == pg.K_LEFT or key == pg.K_DOWN or key == pg.K_RIGHT: 
            if not self.win:
                if self.selected_col == None: self.selected_col = (key - 1073741904) % 3
                else: 
                    self.move_pilar(self.selected_col, (key - 1073741904) % 3, 10, self.move_instant)
                    self.selected_col = None
        # S pour lancer la résolution automatique
        elif key == pg.K_s: 
            self.nb_moves = 0
            self.textManager.update_txt("move_counter", f"Moves : {self.nb_moves}")
            self.gen_pilars()
            self.solve()
        # C pour changer la couleur des disques 
        elif key == pg.K_c: self.pilars_color = (self.pilars_color + 1) % len(PILARS_COLORS)
        elif key == pg.K_i: self.move_instant = not self.move_instant

    def update_pygame(self, delay: int) -> None:
        """Utiliser pour pas que la fenètre de jeu crach pendent les boucles commes pour l'animation du déplacement des pièces"""
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

        self.draw()
        pg.display.update()

        if delay > 0.0001: sleep(delay)

    def draw_pilar_base(self) -> None:
        """Affiches les pilier"""
        def draw_pilar(x: int, is_selected: bool) -> None:
            """Affiches un pilier du coordonées x"""
            # La base en vert si le pilier est séléctioner
            if is_selected: pg.draw.rect(self.display_surface, (10,225,10), (x, 250, 120, 20))
            else: pg.draw.rect(self.display_surface, (75,75,75), (x, 250, 120, 20))
            pg.draw.rect(self.display_surface, (150,150,150), (x + 50, 100, 20, 150))
        
        for x in [40, WINDOW_WIDTH // 2 - 60, WINDOW_WIDTH - 40 - 120]: 
            is_selected = (self.selected_col * 170 + 40 == x) if self.selected_col != None else False
            draw_pilar(x, is_selected)

    def draw_pieces(self) -> None:
        """Affiche les disques"""
        for piece in self.pieces:
            pg.draw.rect(self.display_surface, PILARS_COLORS[self.pilars_color][piece.id], (piece.pos.x, piece.pos.y, piece.width, 20))
    
    def draw_frame(self) -> None:
        """Affiche la zone en bas de l'écrant qui contient les textes d'indication"""
        pg.draw.rect(self.display_surface, (20,20,20), (0, 300, WINDOW_WIDTH, 100))
        pg.draw.rect(self.display_surface, (15,15,15), (3, 303, WINDOW_WIDTH-6, 94))

    def draw(self) -> None:
        """Fonction qui gère tout l'affichage"""
        self.display_surface.fill((25,25,25))
        self.draw_frame()
        self.draw_pilar_base()
        self.draw_pieces()
        self.textManager.draw(self.display_surface)