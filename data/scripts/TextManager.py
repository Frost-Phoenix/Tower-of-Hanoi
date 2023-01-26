import pygame as pg 


class TextManager:
    """Permêt de gérer les textes"""
    
    def __init__(self) -> None:
        # Police d'écriture 
        self.font = pg.font.Font(r"data/font/upheavtt.ttf", 20)
        # Dictionaire qui contient tout les textes et qui sont identifier par une clé de type str
        self.texts = {}

    def add_txt(self, txt_id: str, txt: str, pos: tuple, color=(225,225,225)) -> None:
        """Ajoute un texte au dictionaire self.texts"""
        txt_surface = self.font.render(txt, False, color)
        txt_rect = txt_surface.get_rect(topleft = pos)
        
        self.texts[txt_id] = ([txt_surface, txt_rect])

    def update_txt(self, txt_id: str, new_txt: str, new_pos=None, color=(225,225,225)) -> None:
        """Update le texte d'un des textes"""
        if new_pos != None: self.add_txt(txt_id, new_txt, new_pos)
        else:
            txt_surface = self.font.render(new_txt, False, color)
            self.texts[txt_id][0] = txt_surface

    def draw(self, display_surface: pg.Surface) -> None:
        """Affiche tout les textes"""
        for txt in self.texts.values():
            display_surface.blit(txt[0], txt[1])