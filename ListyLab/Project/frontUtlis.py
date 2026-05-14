from engine.Board import Board
from engine.Generator import MoveGenerator
from engine.Generator import calcualte_bit

def get_index_from_mouse(pos, sq_size):
    x, y = pos
    col = x // sq_size
    row = y // sq_size
    rank = 7 - row
    file = col

    return (rank * 8) + file


class UserApi:
    def __init__(self):
        self.board = Board()
        self.generator = MoveGenerator()
        self.file_dict = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7,
                          'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15,
                          'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23,
                          'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
                          'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39,
                          'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47,
                          'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55,
                          'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63
                          }
        self.revert_file_dict = {value: key for key, value in self.file_dict.items()}

        self.parse_dict = {
            'wp': "white_pawns", 'wr': "white_rooks", 'wn': "white_knights", 'wb': "white_bishops",
            'wk': "white_king", 'wq': "white_queen",
            'bp': "black_pawns", 'br': "black_rooks", 'bn': "black_knights", 'bb': "black_bishops",
            'bk': "black_king", 'bq': "black_queen"
        }

    def web_move_parser(self, start_pos, ending_pos):
        start = self.file_dict[start_pos]
        finish = self.file_dict[ending_pos]

        return start, finish

    def user_move_parser(self, start_pos, ending_pos):
        start = self.revert_file_dict[start_pos]
        finish = self.revert_file_dict[ending_pos]

        return start, finish

    def piece_validation(self, strt_pos):
        square = self.board.get_piece(strt_pos)

        if square is None:
            return 0
        allowed_moves = self.generator.move_piece_validation(square, strt_pos, self.board)
        return allowed_moves

    def try_to_move(self, start_pos, target_pos):

        moves = self.piece_validation(start_pos)

        if moves == 0:
            return False

        if not (moves & 1 << target_pos):
            return False

        piece = self.parse_dict[self.board.get_piece(start_pos)]
        target_piece = self.board.get_piece(target_pos)

        if target_piece:
            capture = self.parse_dict[target_piece]
        else:
            capture = None

        self.board.make_move(piece, start_pos, target_pos, capture)

        return True

    def valid_move_ui(self, start_pos):

        moves = self.piece_validation(start_pos)

        if moves == 0:
            return []

        valid_squares = calcualte_bit(moves)

        return valid_squares
