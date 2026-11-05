import pytest
from engine.Board import Board, validate_fen, FILE_DICT


# --- testy walidacji fen ---

class TestValidateFen:
    def test_valid_start_position(self):
        #standardowa pozycja startowa
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        assert validate_fen(fen) is True

    def test_valid_midgame(self):
        fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        assert validate_fen(fen) is True

    def test_valid_no_castling(self):
        fen = "8/8/8/8/8/8/8/4K2k w - - 0 1"
        assert validate_fen(fen) is True

    def test_valid_en_passant(self):
        # en passant na e3
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        assert validate_fen(fen) is True

    def test_invalid_not_string(self):
        assert validate_fen(None) is False
        assert validate_fen(42) is False

    def test_invalid_too_few_fields(self):
        #brak pol fen
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -") is False

    def test_invalid_wrong_rows(self):
        # 7 rzedow zamiast 8
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP w KQkq - 0 1") is False

    def test_invalid_active_color(self):
        # nieprawidlowy kolor aktywnego gracza
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1") is False

    def test_invalid_castling_chars(self):
        #nieprawidlowy znak roszady
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w X - 0 1") is False

    def test_invalid_castling_duplicates(self):
        # duplikat znaku roszady
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KKQkq - 0 1") is False

    def test_invalid_en_passant_bad_rank(self):
        # en passant poza dopuszczalnym rankiem
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e9 0 1") is False

    def test_invalid_halfmove_negative(self):
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1") is False

    def test_invalid_fullmove_zero(self):
        # fullmove musi byc >= 1
        assert validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0") is False

    def test_invalid_piece_char(self):
        # X nie jest poprawna figura
        assert validate_fen("Xnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") is False

    def test_invalid_row_sum(self):
        # suma pol w rzedzie != 8
        assert validate_fen("rnbqkbnrr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") is False


# --- testy ladowania i generowania fen ---

class TestBoardFen:
    def setup_method(self):
        self.board = Board()

    def test_load_sets_white_to_move(self):
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert self.board.white_to_move is True

    def test_load_sets_black_to_move(self):
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        assert self.board.white_to_move is False

    def test_load_full_castling_rights(self):
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert self.board.castling_rights == 0b1111

    def test_load_partial_castling_rights(self):
        # tylko krotka roszada bialych
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w K - 0 1")
        assert self.board.castling_rights & 0b0001  # K
        assert not (self.board.castling_rights & 0b0010)  # brak Q

    def test_load_no_castling(self):
        self.board.load_fen("8/8/8/8/8/8/8/4K2k w - - 0 1")
        assert self.board.castling_rights == 0

    def test_load_en_passant_target(self):
        #e3 = indeks 20
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        assert self.board.en_passant_target == FILE_DICT['e3']

    def test_load_no_en_passant(self):
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert self.board.en_passant_target is None

    def test_generate_and_reload_roundtrip(self):
        #wczytaj fen potem generuj i sprawdz czy sie zgadza
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        self.board.load_fen(fen)
        generated = self.board.generate_fen()
        assert generated == fen

    def test_generate_fen_start_position(self):
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        generated = self.board.generate_fen()
        assert generated.startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")

    def test_get_piece_returns_correct(self):
        # po zaladowaniu startowej pozycji e1 to krol
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert self.board.get_piece(FILE_DICT['e1']) == 'wk'
        assert self.board.get_piece(FILE_DICT['e8']) == 'bk'
        assert self.board.get_piece(FILE_DICT['a1']) == 'wr'
        assert self.board.get_piece(FILE_DICT['a7']) == 'bp'

    def test_get_piece_empty_square(self):
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # e4 jest puste na poczatku
        assert self.board.get_piece(FILE_DICT['e4']) is None


# --- testy make_move i undo_move ---

class TestMakeUndoMove:
    def setup_method(self):
        self.board = Board()
        self.board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_make_move_pawn_e2_e4(self):
        e2 = FILE_DICT['e2']
        e4 = FILE_DICT['e4']
        self.board.make_move('white_pawns', e2, e4)
        assert self.board.get_piece(e4) == 'wp'
        assert self.board.get_piece(e2) is None

    def test_make_move_changes_turn(self):
        e2 = FILE_DICT['e2']
        e4 = FILE_DICT['e4']
        assert self.board.white_to_move is True
        self.board.make_move('white_pawns', e2, e4)
        assert self.board.white_to_move is False

    def test_make_move_sets_en_passant(self):
        #ruch o 2 pola ustawia en passant
        e2 = FILE_DICT['e2']
        e4 = FILE_DICT['e4']
        e3 = FILE_DICT['e3']
        self.board.make_move('white_pawns', e2, e4)
        assert self.board.en_passant_target == e3

    def test_make_move_no_en_passant_single_step(self):
        #ruch o 1 pole nie ustawia en passant
        e2 = FILE_DICT['e2']
        e3 = FILE_DICT['e3']
        self.board.make_move('white_pawns', e2, e3)
        assert self.board.en_passant_target is None

    def test_undo_restores_position(self):
        e2 = FILE_DICT['e2']
        e4 = FILE_DICT['e4']
        self.board.make_move('white_pawns', e2, e4)
        self.board.undo_move()
        assert self.board.get_piece(e2) == 'wp'
        assert self.board.get_piece(e4) is None

    def test_undo_restores_turn(self):
        e2 = FILE_DICT['e2']
        e4 = FILE_DICT['e4']
        self.board.make_move('white_pawns', e2, e4)
        self.board.undo_move()
        assert self.board.white_to_move is True

    def test_undo_restores_en_passant(self):
        # po cofnieciu ruchu en passant wraca do poprzedniego stanu (None)
        e2 = FILE_DICT['e2']
        e4 = FILE_DICT['e4']
        self.board.make_move('white_pawns', e2, e4)
        self.board.undo_move()
        assert self.board.en_passant_target is None

    def test_make_capture_removes_piece(self):
        #bial pionek bije czarnego
        board = Board()
        board.load_fen("8/8/8/8/8/p7/P7/8 w - - 0 1")
        a2 = FILE_DICT['a2']
        a3 = FILE_DICT['a3']
        board.make_move('white_pawns', a2, a3, 'black_pawns')
        assert board.get_piece(a3) == 'wp'
        # czarny pion zniknal
        assert not (board.black_pawns & (1 << a3))

    def test_undo_restores_captured_piece(self):
        board = Board()
        board.load_fen("8/8/8/8/8/p7/P7/8 w - - 0 1")
        a2 = FILE_DICT['a2']
        a3 = FILE_DICT['a3']
        board.make_move('white_pawns', a2, a3, 'black_pawns')
        board.undo_move()
        # czarny pion wraca
        assert board.get_piece(a3) == 'bp'
        assert board.get_piece(a2) == 'wp'

    def test_undo_empty_history_safe(self):
        # cofniecie bez historii nie rzuca wyjatku
        board = Board()
        board.load_fen("8/8/8/8/8/8/8/4K2k w - - 0 1")
        board.moves_history.clear()
        board.undo_move()  # nie powinno rzucac bledu


# --- testy bitboardow ---

class TestBitboards:
    def test_white_pieces_after_start(self):
        board = Board()
        board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        #biale figury zajmuja rzedy 1-2 (indeksy 0-15)
        assert board.white_pieces == (board.white_pawns | board.white_rooks |
                                      board.white_knights | board.white_bishops |
                                      board.white_queen | board.white_king)

    def test_all_pieces_count_at_start(self):
        board = Board()
        board.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # 32 figury na starcie
        count = bin(board.all_pieces).count('1')
        assert count == 32

    def test_all_pieces_after_capture(self):
        board = Board()
        board.load_fen("8/8/8/8/8/p7/P7/8 w - - 0 1")
        before = bin(board.all_pieces).count('1')
        a2 = FILE_DICT['a2']
        a3 = FILE_DICT['a3']
        board.make_move('white_pawns', a2, a3, 'black_pawns')
        after = bin(board.all_pieces).count('1')
        # jedno bicie = o 1 figura mniej
        assert after == before - 1
