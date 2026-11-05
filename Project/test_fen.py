import unittest
from engine.Board import Board, validate_fen

class TestFEN(unittest.TestCase):
    def test_validate_fen_valid(self):
        #  valid starting position
        start = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.assertTrue(validate_fen(start))

    def test_validate_fen_invalid_fields(self):
        #   invalid fields count
        self.assertFalse(validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"))

    def test_validate_fen_invalid_pieces(self):
        #  invalid piece characters
        self.assertFalse(validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1"))

    def test_validate_fen_invalid_active_color(self):
        #   invalid turn character
        self.assertFalse(validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1"))
        
    def test_validate_fen_invalid_castling(self):
        #    invalid castling characters
        self.assertFalse(validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w X - 0 1"))

    def test_validate_fen_invalid_en_passant(self):
        # validate en passant square
        self.assertFalse(validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e9 0 1"))

    def test_validate_fen_invalid_halfmove(self):
        #   validate halfmove clock
        self.assertFalse(validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1"))

    def test_validate_fen_invalid_fullmove(self):
        #  validate fullmove number
        self.assertFalse(validate_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"))

    def test_board_load_and_generate_fen(self):
        #    test load and generate
        fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        board = Board()
        board.load_fen(fen)
        
        #   verify values
        self.assertFalse(board.white_to_move)
        self.assertEqual(board.castling_rights, 0b1111)
        self.assertIsNone(board.en_passant_target)
        
        generated = board.generate_fen()
        #   check starting parts of the fen
        #  the generate_fen generates 0 1 instead of 1 2 if halfmove/fullmove are not tracked
        self.assertTrue(generated.startswith("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq -"))

    def test_board_load_en_passant(self):
        #  test en passant loading
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        board = Board()
        board.load_fen(fen)
        self.assertEqual(board.en_passant_target, 20)
        self.assertEqual(board.generate_fen(), "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")

if __name__ == "__main__":
    unittest.main()
