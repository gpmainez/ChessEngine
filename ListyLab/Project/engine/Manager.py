

from engine.Board import Board
from engine.Generator import MoveGenerator


class GameManager:
    def __init__(self):
        self.board = Board()
        self.generator = MoveGenerator()

