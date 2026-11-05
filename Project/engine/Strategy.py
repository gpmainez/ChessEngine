import random
from abc import ABC, abstractmethod
from engine.Board import Board

#klasa bazowa dla strategii komputera
class AIStrategy(ABC):
    @abstractmethod
    def get_best_move(self, manager) -> tuple[int, int] | None:
        pass

#wybiera ruch calkowicie losowo
class RandomMoveStrategy(AIStrategy):
    def get_best_move(self, manager) -> tuple[int, int] | None:
        from engine.Generator import calcualte_bit
        
        #szukamy wszystkich figur aktywnego gracza
        is_white = manager.board.white_to_move
        player_pieces = manager.board.white_pieces if is_white else manager.board.black_pieces
        active_squares = calcualte_bit(player_pieces)
        
        legal_moves = []
        #generuj legalne ruchy dla kazdej figury
        for start_sq in active_squares:
            moves_mask = manager.legal_moves(start_sq)
            target_squares = calcualte_bit(moves_mask)
            for target_sq in target_squares:
                legal_moves.append((start_sq, target_sq))
                
        if not legal_moves:
            return None
        #zwroc losowy ruch z listy
        return random.choice(legal_moves)

#szuka ruchu za pomoca minimax z alpha beta
class MinimaxAlphaBetaStrategy(AIStrategy):
    def __init__(self, depth: int):
        self.depth = depth #glebokosc przeszukiwania
        
    def get_best_move(self, manager) -> tuple[int, int] | None:
        from engine.AI import find_best_move
        #wywolaj algorytm minimax alpha beta
        return find_best_move(manager, self.depth)
