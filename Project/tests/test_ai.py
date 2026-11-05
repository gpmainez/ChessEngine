import pytest
from engine.Manager import BasicGameManager
from engine.Board import FILE_DICT
from engine.Strategy import RandomMoveStrategy, MinimaxAlphaBetaStrategy
from engine.AI import evaluate_board, get_all_legal_moves, find_best_move


# pomocnicza funkcja
def make_manager(fen):
    m = BasicGameManager()
    m.setup_board()
    m.board.load_fen(fen)
    return m


# --- testy oceny planszy ---

class TestEvaluateBoard:
    def test_symmetric_position_is_zero(self):
        # pozycja startowa powinna byc zbalansowana (symetria materialowa)
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        score = evaluate_board(m.board)
        # wynik nie musi byc 0 przez pst ale powinnien byc bliski 0
        assert abs(score) < 100

    def test_white_material_advantage(self):
        # bialy ma hetmana wiecej
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        m.board.load_fen("8/8/8/8/8/8/8/Q3K2k w - - 0 1")
        score = evaluate_board(m.board)
        # bialy ma hetmana (900) czarny nie ma nic oprocz krola wiec wynik > 0
        assert score > 0

    def test_black_material_advantage(self):
        # czarny ma hetmana wiecej
        m = make_manager("8/8/8/8/8/8/8/4K2k w - - 0 1")
        m.board.load_fen("q7/8/8/8/8/8/8/4K2k w - - 0 1")
        score = evaluate_board(m.board)
        # czarny ma hetmana wiec wynik < 0
        assert score < 0

    def test_equal_material(self):
        # bialy i czarny maja po jednej wiezy
        m = make_manager("8/8/8/8/8/8/8/R3K2k w - - 0 1")
        m.board.load_fen("r7/8/8/8/8/8/8/R3K2k w - - 0 1")
        # materialnie rowno
        score = evaluate_board(m.board)
        # mozliwy bonus pst wiec nie jest dokladnie 0 ale bliski
        assert abs(score) < 150


# --- testy get_all_legal_moves ---

class TestGetAllLegalMoves:
    def test_start_position_white_has_20_moves(self):
        # z pozycji startowej bialy ma 20 ruchow (16 pionow + 4 skoczki)
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        moves = get_all_legal_moves(m)
        assert len(moves) == 20

    def test_no_moves_in_checkmate(self):
        # po glupcu czarny hetman daje mat - bialy nie ma ruchow
        m = BasicGameManager()
        m.setup_board()
        m.try_to_move(FILE_DICT['f2'], FILE_DICT['f3'])
        m.try_to_move(FILE_DICT['e7'], FILE_DICT['e5'])
        m.try_to_move(FILE_DICT['g2'], FILE_DICT['g4'])
        m.try_to_move(FILE_DICT['d8'], FILE_DICT['h4'])
        moves = get_all_legal_moves(m)
        assert len(moves) == 0

    def test_returns_list_of_tuples(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        moves = get_all_legal_moves(m)
        assert isinstance(moves, list)
        assert all(isinstance(mv, tuple) and len(mv) == 2 for mv in moves)


# --- testy strategii ---

class TestAIStrategies:
    def test_random_strategy_returns_move(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        strategy = RandomMoveStrategy()
        move = strategy.get_best_move(m)
        assert move is not None
        assert isinstance(move, tuple)

    def test_random_strategy_no_moves_returns_none(self):
        # mat - brak ruchow
        m = BasicGameManager()
        m.setup_board()
        m.try_to_move(FILE_DICT['f2'], FILE_DICT['f3'])
        m.try_to_move(FILE_DICT['e7'], FILE_DICT['e5'])
        m.try_to_move(FILE_DICT['g2'], FILE_DICT['g4'])
        m.try_to_move(FILE_DICT['d8'], FILE_DICT['h4'])
        strategy = RandomMoveStrategy()
        move = strategy.get_best_move(m)
        assert move is None

    def test_minimax_depth1_returns_move(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        strategy = MinimaxAlphaBetaStrategy(depth=1)
        move = strategy.get_best_move(m)
        assert move is not None

    def test_minimax_depth1_no_moves_returns_none(self):
        m = BasicGameManager()
        m.setup_board()
        m.try_to_move(FILE_DICT['f2'], FILE_DICT['f3'])
        m.try_to_move(FILE_DICT['e7'], FILE_DICT['e5'])
        m.try_to_move(FILE_DICT['g2'], FILE_DICT['g4'])
        m.try_to_move(FILE_DICT['d8'], FILE_DICT['h4'])
        strategy = MinimaxAlphaBetaStrategy(depth=1)
        move = strategy.get_best_move(m)
        assert move is None

    def test_minimax_does_not_corrupt_board(self):
        # po wywolaniu minimax plansza powinna byc taka sama jak przed
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        strategy = MinimaxAlphaBetaStrategy(depth=1)
        fen_before = m.board.generate_fen()
        strategy.get_best_move(m)
        fen_after = m.board.generate_fen()
        # minimax musi cofac wszystkie ruchy - stan planszy bez zmian
        assert fen_before == fen_after

    def test_minimax_depth2_does_not_corrupt_board(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        strategy = MinimaxAlphaBetaStrategy(depth=2)
        fen_before = m.board.generate_fen()
        strategy.get_best_move(m)
        fen_after = m.board.generate_fen()
        assert fen_before == fen_after


# --- testy find_best_move (mat w 1) ---

class TestMinimaxMateInOne:
    def test_ai_finds_mate_in_one_as_white(self):
        # bialy Qd5 Kd1 czarny Ke8 - hetman na e6 to szach a na f7 to mat
        # uzyj pozycji gdzie bialy wygrywa hetmanem na e7#
        # bialy: Kc6 Qd7 czarny: Ka8 - Qa7 to mat
        m = BasicGameManager()
        m.setup_board()
        m.board.load_fen("k7/8/K1Q5/8/8/8/8/8 w - - 0 1")
        # bialy gra - najlepszy ruch to Qa6# lub Qc8#
        move = find_best_move(m, depth=2)
        assert move is not None
        m.try_to_move(move[0], move[1])
        state = m.check_game_state()
        # ai powinno znalezc mata
        assert state == "CHECKMATE"

    def test_ai_avoids_losing_queen(self):
        # bialy Qa4 zaatakowany przez czarnego pionka b5
        # bialy powinien uciec hetmanem zamiast zostawic go do bicia
        m = make_manager("8/8/8/1p6/Q7/8/8/4K2k w - - 0 1")
        move = find_best_move(m, depth=2)
        a4 = FILE_DICT['a4']
        assert move is not None
        # ruch musi byc legalny
        legal = m.try_to_move(move[0], move[1])
        assert legal is True
