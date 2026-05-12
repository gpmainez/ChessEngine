


class Board:
    def __init__(self):
        self.white_pawns = 0xFF00
        self.white_rooks = 0x81
        self.white_knights = 0x42
        self.white_bishops = 0x24
        self.white_queen = 0x08
        self.white_king = 0x10

        self.black_pawns = self.white_pawns << 40
        self.black_rooks = self.white_rooks << 56
        self.black_knights = self.white_knights << 56
        self.black_bishops = self.white_bishops << 56
        self.black_queen = self.white_queen << 56
        self.black_king = self.white_king << 56



        self.moves_history = []

    @property
    def white_pieces(self):
        return self.white_pawns | self.white_rooks | self.white_knights | self.white_bishops | self.white_queen | self.white_king

    @property
    def black_pieces(self):
        return self.black_pawns | self.black_rooks | self.black_knights | self.black_bishops | self.black_queen | self.black_king

    @property
    def all_pieces(self):
        return self.white_pieces | self.black_pieces

    def make_move(self, piece, start, target, capture_name=None):
        start_pos = 1 << start
        target_pos = 1 << target

        move = start_pos | target_pos

        current_board = getattr(self, piece)
        changed_board = current_board ^ move

        setattr(self, piece, changed_board)

        self.moves_history.append({
            "piece": piece,
            "start": start,
            "target": target,
            "capture_name": capture_name,
            "move": move
        }

        )

        if capture_name:
            current_board_capture = getattr(self, capture_name)

            board_capture = current_board_capture ^ target_pos
            setattr(self, capture_name, board_capture)

    def move_validation(self):
        if not self.moves_history:
            return

        last_move = self.moves_history[-1]

        current_board = getattr(self, last_move["piece"])
        changed_board = current_board ^ last_move["move"]
        setattr(self, last_move["piece"], changed_board)

        if last_move["capture_name"]:
            get_piece = 1 < last_move["target"]
            current_board_capture = getattr(self, last_move["capture_name"])
            setattr(self, last_move["capture_name"], current_board_capture | get_piece)

    def load_fen(self, fen):
        self.white_pawns = self.white_rooks = self.white_knights = \
        self.white_bishops = self.white_queen = self.white_king = 0
        self.black_pawns = self.black_rooks = self.black_knights = \
        self.black_bishops = self.black_queen = self.black_king = 0

        parts = fen.split(" ")
        rows = parts[0].split("/")

        for r, row in enumerate(rows):
            rank = 7 - r
            file = 0
            for char in row:
                if char.isdigit():
                    file += int(char)
                else:
                    square = rank * 8 + file
                    self._set_piece_by_char(char, square)
                    file += 1

    def _set_piece_by_char(self, char, square):
        piecie_dict = {
            'P': 'white_pawns', 'R': 'white_rooks', 'N': 'white_knights',
            'B': 'white_bishops', 'Q': 'white_queen', 'K': 'white_king',
            'p': 'black_pawns', 'r': 'black_rooks', 'n': 'black_knights',
            'b': 'black_bishops', 'q': 'black_queen', 'k': 'black_king'
        }
        attr = piecie_dict.get(char)
        if attr:
            val = getattr(self, attr)
            setattr(self, attr, val | (1 << square))


    def print_board(self, board):
        print("-" * 17)
        for rank in range(7, -1, -1):
            row_str = "|"
            for file in range(8):
                square = rank * 8 + file
                if board & (1 << square):
                    row_str += " X"
                else:
                    row_str += " ."
            print(row_str + " |")
        print("-" * 17)


if __name__ == "__main__":
    board = Board()
    board.print_board(board.all_pieces)
    board.make_move('white_knights',1,18)
    board.print_board(board.all_pieces)