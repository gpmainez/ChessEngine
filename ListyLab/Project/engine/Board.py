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

        #0001 W king
        #0010 W queen
        #0100 B king
        #1000 B queen
        self.castling_rights = 0b1111
        self.en_passant_target = None

        self.white_to_move = True
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
        #make move
        current_board = getattr(self, piece)
        setattr(self, piece, current_board ^ move)

        #necesary to unmake_move (pin situation)
        self.moves_history.append({
            "piece": piece,
            "start": start,
            "target": target,
            "capture_name": capture_name,
            "move": move,
            "prev_castling": self.castling_rights,
            "prev_en_passant": self.en_passant_target
        })


        if piece == 'white_king':
            self.castling_rights &= ~0b0011
        elif piece == 'white_rooks':
            if start == 0: self.castling_rights &= ~0b0010
            if start == 7: self.castling_rights &= ~0b0001
        elif piece == 'black_king':
            self.castling_rights &= ~0b1100
        elif piece == 'black_rooks':
            if start == 56: self.castling_rights &= ~0b1000
            if start == 63: self.castling_rights &= ~0b0100

        #jakos to dziala chuuj wie kopiuj wklej z stack overf
        self.en_passant_target = None
        if piece == 'white_pawns' and (target - start == 16):
            self.en_passant_target = start + 8
        elif piece == 'black_pawns' and (start - target == 16):
            self.en_passant_target = start - 8

        if capture_name:
            current_board_capture = getattr(self, capture_name)
            setattr(self, capture_name, current_board_capture ^ target_pos)

        self.white_to_move = not self.white_to_move

    #reset move(proper validation)
    def undo_move(self):
        if not self.moves_history:
            return

        last_move = self.moves_history.pop()

        self.castling_rights = last_move["prev_castling"]
        self.en_passant_target = last_move["prev_en_passant"]

        current_board = getattr(self, last_move["piece"])
        setattr(self, last_move["piece"], current_board ^ last_move["move"])

        if last_move["capture_name"]:

            captured_piece_pos = 1 << last_move["target"]
            current_board_capture = getattr(self, last_move["capture_name"])
            setattr(self, last_move["capture_name"], current_board_capture | captured_piece_pos)

        self.white_to_move = not self.white_to_move

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

    def generate_fen(self):
        pieces = [
            (self.white_pawns, 'P'), (self.white_rooks, 'R'), (self.white_knights, 'N'),
            (self.white_bishops, 'B'), (self.white_queen, 'Q'), (self.white_king, 'K'),
            (self.black_pawns, 'p'), (self.black_rooks, 'r'), (self.black_knights, 'n'),
            (self.black_bishops, 'b'), (self.black_queen, 'q'), (self.black_king, 'k')
        ]

        current_board = self.all_pieces

        fen_rows = []
        for rank in range(7, -1, -1):
            row_str = ""
            empty_count = 0

            for file in range(8):
                square = rank * 8 + file
                mask = 1 << square

                if current_board & mask:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0

                    for bitboard, char in pieces:
                        if bitboard & mask:
                            row_str += char
                            break
                else:
                    empty_count += 1
            if empty_count > 0:
                row_str += str(empty_count)

            fen_rows.append(row_str)

        ranks_part = "/".join(fen_rows)
        to_move = "w" if self.white_to_move else "b"

        return f"{ranks_part} {to_move} - - 0 1"

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
    board.make_move('white_knights', 1, 18)
    board.print_board(board.all_pieces)
