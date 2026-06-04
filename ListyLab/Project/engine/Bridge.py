from engine.Manager import BaseGameManager
from engine.Board import FILE_DICT, REVERT_FILE_DICT, validate_fen
from engine.Strategy import RandomMoveStrategy, MinimaxAlphaBetaStrategy

class GameInterfaceBridge:
    def __init__(self, manager: BaseGameManager):
        """
        Initializes the bridge with a concrete implementor (game manager).
        """
        self.manager = manager

    def make_move(self, source_square: str, target_square: str) -> bool:
        """
        Attempts to make a player move using algebraic square coordinates.
        Returns True if the move is legal and was successfully executed; False otherwise.
        """
        if source_square not in FILE_DICT or target_square not in FILE_DICT:
            return False
        start_idx = FILE_DICT[source_square]
        target_idx = FILE_DICT[target_square]
        return self.manager.try_to_move(start_idx, target_idx)

    def make_ai_move(self, difficulty: int) -> tuple[str, str] | None:
        """
        Triggers AI move calculation at the specified difficulty/depth and makes the move.
        difficulty: 0 (Random), >0 (Minimax depth = difficulty)
        Returns the move as (source_square, target_square) in algebraic format, or None if no move.
        """
        if difficulty == 0:
            self.manager.ai_strategy = RandomMoveStrategy()
        else:
            self.manager.ai_strategy = MinimaxAlphaBetaStrategy(depth=difficulty)
            
        history_len_before = len(self.manager.board.moves_history)
        success = self.manager.make_ai_move()
        
        if success and len(self.manager.board.moves_history) > history_len_before:
            last_move = self.manager.board.moves_history[-1]
            start_str = REVERT_FILE_DICT[last_move["start"]]
            target_str = REVERT_FILE_DICT[last_move["target"]]
            return (start_str, target_str)
            
        return None

    def get_fen(self) -> str:
        """
        Returns the current FEN representation of the board state.
        """
        return self.manager.board.generate_fen()

    def is_game_over(self) -> bool:
        """
        Checks if the game has ended (CHECKMATE or STALEMATE).
        """
        state = self.manager.check_game_state()
        return state in ("CHECKMATE", "STALEMATE")

    def get_game_result(self) -> str | None:
        """
        Returns the game result ("CHECKMATE" or "STALEMATE") if over, or None otherwise.
        """
        state = self.manager.check_game_state()
        if state in ("CHECKMATE", "STALEMATE"):
            return state
        return None

    def get_legal_moves(self, square: str) -> list[str]:
        """
        Returns a list of legal target squares (as algebraic strings) for the piece at the given square.
        """
        if square not in FILE_DICT:
            return []
        idx = FILE_DICT[square]
        moves_bitmask = self.manager.legal_moves(idx)
        if moves_bitmask == 0:
            return []
        
        from engine.Generator import calcualte_bit
        dest_indices = calcualte_bit(moves_bitmask)
        return [REVERT_FILE_DICT[d_idx] for d_idx in dest_indices]

    def save_game(self, filename: str) -> bool:
        """
        Saves the current FEN representation of the board to a file.
        Returns True if successful, False otherwise.
        """
        try:
            fen = self.get_fen()
            with open(filename, "w") as f:
                f.write(fen)
            return True
        except Exception:
            return False

    def load_game(self, filename: str) -> bool:
        """
        Loads the board state from a FEN string in a file.
        Returns True if successful and FEN is valid, False otherwise.
        """
        try:
            with open(filename, "r") as f:
                fen = f.read().strip()
            if validate_fen(fen):
                self.manager.board.load_fen(fen)
                return True
            return False
        except Exception:
            return False

    # --- Convenience Additions for UI Cleanliness ---

    def get_piece(self, square: str | int) -> str | None:
        """
        Returns the piece code (e.g. 'wp', 'bk', etc.) at the specified square (str or int index).
        """
        if isinstance(square, int):
            return self.manager.board.get_piece(square)
        if square not in FILE_DICT:
            return None
        return self.manager.board.get_piece(FILE_DICT[square])

    @property
    def white_to_move(self) -> bool:
        """
        Returns True if it is currently White's turn, False otherwise.
        """
        return self.manager.board.white_to_move
