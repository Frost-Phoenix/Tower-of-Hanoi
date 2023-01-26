from data.scripts.Utils import Pos  


class Piece:
    """Permet de centraliser les atributs de chaque pieces"""

    def __init__(self, id: int, col: int, pos: tuple, width: int) -> None:
        self.id = id
        self.col = col
        self.width = width
        self.pos = Pos(pos)

