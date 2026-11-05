import pytest
from engine.Manager import BasicGameManager, FisherChessGameManager, GameManagerFactory
from engine.Board import FILE_DICT


# pomocnicza funkcja do tworzenia managera z fen
def make_manager(fen):
    m = BasicGameManager()
    m.setup_board()
    m.board.load_fen(fen)
    #ustaw castle_map dla standardowej pozycji
    return m


# --- testy generowania ruchow ---

class TestMoveGeneration:
    def test_pawn_initial_moves(self):
        #pion e2 moze ruszyc sie na e3 lub e4
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        e2 = FILE_DICT['e2']
        moves = m.valid_move_ui(e2)
        assert FILE_DICT['e3'] in moves
        assert FILE_DICT['e4'] in moves

    def test_pawn_blocked(self):
        # pion zablokowany przez wlasna figure
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # pionek a2 jest zablokowany przez skoczka na a1 (to wieża jest)
        # zaladuj pozycje gdzie pion jest zablokowany
        m.board.load_fen("8/8/8/8/P7/P7/8/4K2k w - - 0 1")
        a3 = FILE_DICT['a3']
        # pion na a3 jest zablokowany przez pion na a4
        moves = m.valid_move_ui(a3)
        assert len(moves) == 0

    def test_knight_moves_center(self):
        # skoczek w centrum ma 8 mozliwych ruchow
        m = make_manager("8/8/8/8/4N3/8/8/4K2k w - - 0 1")
        e4 = FILE_DICT['e4']
        moves = m.valid_move_ui(e4)
        assert len(moves) == 8

    def test_knight_moves_corner(self):
        # skoczek w rogu ma tylko 2 ruchy
        m = make_manager("8/8/8/8/8/8/8/N3K2k w - - 0 1")
        a1 = FILE_DICT['a1']
        moves = m.valid_move_ui(a1)
        assert len(moves) == 2

    def test_king_moves_center(self):
        #krol w centrum (bez szacha) ma 8 ruchow
        m = make_manager("8/8/8/8/4K3/8/8/7k w - - 0 1")
        e4 = FILE_DICT['e4']
        moves = m.valid_move_ui(e4)
        assert len(moves) == 8

    def test_no_moves_for_wrong_color(self):
        #biale nie moga ruszyc czarnymi figurami
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        e7 = FILE_DICT['e7']  # czarny pion
        moves = m.valid_move_ui(e7)
        # sprawdzamy przez try_to_move - valid_move_ui zwraca ruchy bez sprawdzania koloru
        # ale try_to_move powinien odrzucic ruch
        legal = m.try_to_move(e7, FILE_DICT['e5'])
        assert legal is False

    def test_rook_moves_open_file(self):
        # wieza na otwartej linii
        m = make_manager("8/8/8/8/8/8/8/R3K2k w - - 0 1")
        a1 = FILE_DICT['a1']
        moves = m.valid_move_ui(a1)
        # wieza moze chodzic po pliku a i po rzedzie 1 (bez kola króla)
        assert len(moves) > 0


# --- testy try_to_move ---

class TestTryToMove:
    def test_valid_pawn_move(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert m.try_to_move(FILE_DICT['e2'], FILE_DICT['e4']) is True

    def test_invalid_move_wrong_color(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # bialy nie moze grac czarnym pionem
        assert m.try_to_move(FILE_DICT['e7'], FILE_DICT['e5']) is False

    def test_invalid_move_empty_square(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # e4 jest puste na starcie
        assert m.try_to_move(FILE_DICT['e4'], FILE_DICT['e5']) is False

    def test_move_changes_board_state(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        e2 = FILE_DICT['e2']
        e4 = FILE_DICT['e4']
        m.try_to_move(e2, e4)
        assert m.board.get_piece(e4) == 'wp'
        assert m.board.get_piece(e2) is None

    def test_move_alternates_turn(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert m.board.white_to_move is True
        m.try_to_move(FILE_DICT['e2'], FILE_DICT['e4'])
        assert m.board.white_to_move is False

    def test_capture_removes_enemy(self):
        # bial pion bije czarnego
        m = make_manager("8/8/8/8/8/1p6/P7/4K2k w - - 0 1")
        a2 = FILE_DICT['a2']
        b3 = FILE_DICT['b3']
        result = m.try_to_move(a2, b3)
        assert result is True
        assert m.board.get_piece(b3) == 'wp'


# --- testy check_game_state ---

class TestGameState:
    def test_continue_at_start(self):
        m = make_manager("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert m.check_game_state() == "CONTINUE"

    def test_checkmate_fool_mate(self):
        # glupiec - mat w 2 ruchach
        # f3 g4 e5 Qh4#
        m = BasicGameManager()
        m.setup_board()
        m.try_to_move(FILE_DICT['f2'], FILE_DICT['f3'])
        m.try_to_move(FILE_DICT['e7'], FILE_DICT['e5'])
        m.try_to_move(FILE_DICT['g2'], FILE_DICT['g4'])
        m.try_to_move(FILE_DICT['d8'], FILE_DICT['h4'])
        # bialy krol jest w macie
        state = m.check_game_state()
        assert state == "CHECKMATE"

    def test_stalemate(self):
        # pat - krol czarny na a8 bialy qa6 bialy ka6 - czarny nie ma legalnych ruchow
        # pozycja: bialy K c6 Q b6 czarny K a8 - czarny gra
        m = make_manager("k7/8/KQ6/8/8/8/8/8 b - - 0 1")
        state = m.check_game_state()
        assert state == "STALEMATE"

    def test_square_under_attack_pawn(self):
        # pole e3 jest atakowane przez czarnego piona na d4
        m = make_manager("8/8/8/8/3p4/8/8/4K2k w - - 0 1")
        e3 = FILE_DICT['e3']
        assert m.square_under_attack(e3, 'black') is True

    def test_square_not_under_attack(self):
        # pole e4 nie jest atakowane
        m = make_manager("8/8/8/8/8/8/8/4K2k w - - 0 1")
        e4 = FILE_DICT['e4']
        assert m.square_under_attack(e4, 'black') is False


# --- testy roszady ---

class TestCastling:
    def test_white_short_castle_available(self):
        #bialy krol moze isć na g1 (krotka roszada) gdy pola sa wolne
        m = BasicGameManager()
        m.setup_board()
        # usuniecie figurur miedzy krolem a wieza
        m.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1")
        g1 = FILE_DICT['g1']
        e1 = FILE_DICT['e1']
        moves = m.valid_move_ui(e1)
        assert g1 in moves

    def test_white_short_castle_blocked(self):
        # wieza zablokowana przez skoczka
        m = BasicGameManager()
        m.setup_board()
        # pozycja startowa ma skoczka miedzy krolem a wieza
        e1 = FILE_DICT['e1']
        g1 = FILE_DICT['g1']
        moves = m.valid_move_ui(e1)
        # g1 nie dostepne bo skoczek blokuje
        assert g1 not in moves

    def test_white_no_castle_no_rights(self):
        # krol nie moze roszowac bez praw roszady
        m = BasicGameManager()
        m.setup_board()
        m.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w - - 0 1")
        g1 = FILE_DICT['g1']
        e1 = FILE_DICT['e1']
        moves = m.valid_move_ui(e1)
        assert g1 not in moves


# --- testy fabryki i chess960 ---

class TestGameManagerFactory:
    def test_factory_standard(self):
        # fabryka tworzy standardowy manager
        m = GameManagerFactory.create("standard")
        assert isinstance(m, BasicGameManager)
        assert m.board.get_piece(FILE_DICT['e2']) == 'wp'

    def test_factory_fisher(self):
        # fabryka tworzy manager fishera i losuje plansze
        m = GameManagerFactory.create("fisher")
        assert isinstance(m, FisherChessGameManager)
        # pawny na swoich miejscach
        for col_char in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            assert m.board.get_piece(FILE_DICT[col_char + '2']) == 'wp'
            assert m.board.get_piece(FILE_DICT[col_char + '7']) == 'bp' # get_piece accepts coordinate or index

    def test_factory_invalid_mode(self):
        # wyjatek dla nieznanego trybu
        with pytest.raises(ValueError):
            GameManagerFactory.create("unknown_mode")

