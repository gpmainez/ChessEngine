from Demos.mmapfile_demo import offset


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

        # 0001 W short
        # 0010 W long
        # 0100 B short
        # 1000 B long

        self.castle_positions = {}
        self.castling_rights = 0b1111
        self.en_passant_target = None

        self.white_to_move = True
        self.moves_history = []

        self.file_dict = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7,
                          'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15,
                          'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23,
                          'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
                          'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39,
                          'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47,
                          'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55,
                          'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63
                          }

    @property
    def white_pieces(self):
        return self.white_pawns | self.white_rooks | self.white_knights | self.white_bishops | self.white_queen | self.white_king

    @property
    def black_pieces(self):
        return self.black_pawns | self.black_rooks | self.black_knights | self.black_bishops | self.black_queen | self.black_king

    @property
    def all_pieces(self):
        return self.white_pieces | self.black_pieces

    def make_move(self, piece, start, target, capture_name=None, en_passant=False, promotion_piece=None, rook_move = None, removed_castle_rights = None):
        start_pos = 1 << start
        target_pos = 1 << target
        move = start_pos | target_pos

        if promotion_piece:
            current_pawns = getattr(self, piece)
            setattr(self, piece, current_pawns ^ (1 << start))

            current_promo = getattr(self, promotion_piece)
            setattr(self, promotion_piece, current_promo | (1 << target))
        else:
            # make move
            current_board = getattr(self, piece)
            setattr(self, piece, current_board ^ move)

        # if piece in ['white_king', 'black_king'] and abs(start - target) == 2:
        #     if target == 6:
        #         self.white_rooks ^= (1 << 7) | (1 << 5)
        #     elif target == 2:
        #         self.white_rooks ^= (1 << 0) | (1 << 3)
        #     elif target == 62:
        #         self.black_rooks ^= (1 << 63) | (1 << 61)
        #     elif target == 58:
        #         self.black_rooks ^= (1 << 56) | (1 << 59)

        if rook_move:
            rook_start, rook_end = rook_move
            rook_piece = 'white_rooks' if piece == 'white_king' else 'black_rooks'

            rook_move_mask = (1 << rook_start) | (1 << rook_end)
            current_rooks = getattr(self, rook_piece)
            setattr(self, rook_piece, current_rooks ^ rook_move_mask)

        # necesary to unmake_move (pin situation)
        self.moves_history.append({
            "piece": piece,
            "start": start,
            "target": target,
            "capture_name": capture_name,
            "move": move,
            "prev_castling": self.castling_rights,
            "prev_en_passant": self.en_passant_target,
            "is_en_passant": en_passant,
            "rook_move": rook_move,
        })

        # if piece == 'white_king':
        #     self.castling_rights &= ~0b0011
        # elif piece == 'white_rooks':
        #     if start == 0: self.castling_rights &= ~0b0010
        #     if start == 7: self.castling_rights &= ~0b0001
        # elif piece == 'black_king':
        #     self.castling_rights &= ~0b1100
        # elif piece == 'black_rooks':
        #     if start == 56: self.castling_rights &= ~0b1000
        #     if start == 63: self.castling_rights &= ~0b0100

        if removed_castle_rights:
            self.castling_rights &= ~removed_castle_rights

        self.en_passant_target = None
        if piece == 'white_pawns' and (target - start == 16):
            self.en_passant_target = start + 8
        elif piece == 'black_pawns' and (start - target == 16):
            self.en_passant_target = start - 8

        if capture_name:
            if en_passant:
                if piece == "white_pawns":
                    capture = target - 8
                else:
                    capture = target + 8

                current_board_capture = getattr(self, capture_name)
                setattr(self, capture_name, current_board_capture ^ (1 << capture))
            else:
                current_board_capture = getattr(self, capture_name)
                setattr(self, capture_name, current_board_capture ^ target_pos)

        self.white_to_move = not self.white_to_move

    # reset move(proper validation)

    def undo_move(self):
        if not self.moves_history:
            return

        last_move = self.moves_history.pop()

        self.castling_rights = last_move["prev_castling"]
        self.en_passant_target = last_move["prev_en_passant"]

        current_board = getattr(self, last_move["piece"])
        setattr(self, last_move["piece"], current_board ^ last_move["move"])

        if last_move["rook_move"]:
            rook_start, rook_end = last_move["rook_move"]
            rook_piece = 'white_rooks' if last_move["piece"] == 'white_king' else 'black_rooks'

            rook_move_mask = (1 << rook_start) | (1 << rook_end)
            current_rooks = getattr(self, rook_piece)

            setattr(self, rook_piece, current_rooks ^ rook_move_mask)

        if last_move["capture_name"]:
            if last_move.get("is_en_passant"):
                if last_move["piece"] == 'white_pawns':
                    captured_square = last_move["target"] - 8
                else:
                    captured_square = last_move["target"] + 8
                captured_piece_pos = 1 << captured_square
            else:
                captured_piece_pos = 1 << last_move["target"]

            current_board_capture = getattr(self, last_move["capture_name"])
            setattr(self, last_move["capture_name"], current_board_capture ^ captured_piece_pos)

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
                target = 1 << square

                if current_board & target:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0

                    for bitboard, char in pieces:
                        if bitboard & target:
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

    def get_piece(self, square_idx):
        target = 1 << square_idx
        piece = self.all_pieces & target

        if piece:
            if self.white_pawns & target:
                return 'wp'
            elif self.white_king & target:
                return 'wk'
            elif self.white_bishops & target:
                return 'wb'
            elif self.white_queen & target:
                return 'wq'
            elif self.white_knights & target:
                return 'wn'
            elif self.white_rooks & target:
                return 'wr'
            elif self.black_pawns & target:
                return 'bp'
            elif self.black_king & target:
                return 'bk'
            elif self.black_bishops & target:
                return 'bb'
            elif self.black_queen & target:
                return 'bq'
            elif self.black_knights & target:
                return 'bn'
            elif self.black_rooks & target:
                return 'br'
            return None

        else:
            return None

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
