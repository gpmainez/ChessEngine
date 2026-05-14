def precompute_moves(move_vector):
    moves = [0] * 64
    for square in range(64):
        row = square // 8
        file = square % 8
        mask = 0
        for x_jump, y_jump in move_vector:
            row_j = row + x_jump
            file_j = file + y_jump
            if 0 <= row_j <= 7 and 0 <= file_j <= 7:
                square_j = row_j * 8 + file_j
                mask = mask | (1 << square_j)
        moves[square] = mask
    return moves


def precompute_all_rays(directions_dict):
    rays = {dir_name: [0] * 64 for dir_name in directions_dict}
    for square in range(64):
        row = square // 8
        file = square % 8
        for dir_name, (x_jump, y_jump) in directions_dict.items():
            mask = 0
            for step in range(1, 8):
                r = row + (x_jump * step)
                f = file + (y_jump * step)
                if 0 <= r <= 7 and 0 <= f <= 7:
                    target_square = r * 8 + f
                    mask = mask | (1 << target_square)
                else:
                    break
            rays[dir_name][square] = mask
    return rays


def compute_slider_moves(arrays, directions_dict, square, all_pieces, same_color_pieces):
    moves = 0
    for dir_name, sense in directions_dict.items():

        obstacle = arrays[dir_name][square] & all_pieces
        if obstacle:
            if sense > 0:
                lowest_bit = obstacle & -obstacle
                lowest_bit_idx = lowest_bit.bit_length() - 1
            else:
                lowest_bit_idx = obstacle.bit_length() - 1
            moves = moves | (arrays[dir_name][square] ^ arrays[dir_name][lowest_bit_idx])
        else:
            moves = moves | arrays[dir_name][square]

    return moves & ~same_color_pieces

def calcualte_bit(mask):
    squares = []

    while mask > 0:
        file = mask & -mask
        idx = file.bit_length() - 1
        squares.append(idx)
        mask = mask & (mask - 1)

    return squares

class MoveGenerator:
    def __init__(self):
        king_vector = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        knight_vector = [(2, 1), (2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2), (-2, 1), (-2, -1)]
        white_pawn = [(1, 1), (1, -1)]
        black_pawn = [(-1, -1), (-1, 1)]

        self.directions = {'N': (1, 0), 'S': (-1, 0), 'E': (0, 1), 'W': (0, -1), 'NE': (1, 1), 'NW': (1, -1),
                           'SE': (-1, 1), 'SW': (-1, -1)
                           }

        self.king_moves = precompute_moves(king_vector)
        self.knight_moves = precompute_moves(knight_vector)
        self.white_pawn_attacks = precompute_moves(white_pawn)
        self.black_pawn_attacks = precompute_moves(black_pawn)
        self.rays = precompute_all_rays(self.directions)

    def move_knight(self, square, same_color_pieces):
        return self.knight_moves[square] & ~same_color_pieces

    def move_king(self, square, same_color_pieces):
        return self.king_moves[square] & ~same_color_pieces

    def move_bishop(self, square, same_color_pieces, all_pieces):
        directions = {'NE': 1, 'NW': 1, 'SE': -1, 'SW': -1}
        return compute_slider_moves(self.rays, directions, square, all_pieces, same_color_pieces)

    def move_rook(self, square, same_color_pieces, all_pieces):
        directions = {'N': 1, 'E': 1, 'S': -1, 'W': -1}
        return compute_slider_moves(self.rays, directions, square, all_pieces, same_color_pieces)

    def move_queen(self, square, same_color_pieces, all_pieces):
        return self.move_rook(square, same_color_pieces, all_pieces) | self.move_bishop(square, same_color_pieces,
                                                                                        all_pieces)

    def move_white_pawn(self, square, all_pieces, black_pieces, en_passant_target=None):
        moves = 0
        promotions = 0

        row = square // 8
        move = square + 8

        if not (all_pieces & (1 << move)):

            if row == 1:
                double_move = square + 16
                if not (all_pieces & (1 << double_move)):
                    moves = moves | (1 << double_move)
                    moves = moves | (1 << move)
            if row == 6:
                promotions = promotions | (1 << move)
            else:
                moves = moves | (1 << move)

        attacks = self.white_pawn_attacks[square]
        captures = attacks & black_pieces

        if row == 6:
            promotions = promotions | captures
        else:
            moves = moves | captures

        if en_passant_target is not None:
            ep_bit = (1 << en_passant_target)

            if attacks & ep_bit:
                moves = moves | ep_bit

        return moves, promotions

    def move_black_pawn(self, square, all_pieces, white_pieces, en_passant_target=None):
        moves = 0
        promotions = 0

        row = square // 8
        move = square - 8

        if not (all_pieces & (1 << move)):
            if row == 1:
                promotions |= (1 << move)
            else:
                moves |= (1 << move)
                if row == 6:
                    double_move = square - 16
                    if not (all_pieces & (1 << double_move)):
                        moves |= (1 << double_move)
        attacks = self.black_pawn_attacks[square]
        captures = attacks & white_pieces

        if row == 1:
            promotions |= captures
        else:
            moves |= captures

        if en_passant_target is not None:
            ep_bit = (1 << en_passant_target)

            if attacks & ep_bit:
                moves |= ep_bit

        return moves, promotions

    def move_piece_validation(self, piece_code, square, board):

        all_pieces = board.all_pieces
        white_pieces = board.white_pieces
        black_pieces = board.black_pieces

        is_white = piece_code.startswith('w')
        same_color = white_pieces if is_white else black_pieces

        if piece_code == 'wn' or piece_code == 'bn':
            return self.move_knight(square, same_color)

        elif piece_code == 'wk' or piece_code == 'bk':
            return self.move_king(square, same_color)

        elif piece_code == 'wb' or piece_code == 'bb':
            return self.move_bishop(square, same_color, all_pieces)

        elif piece_code == 'wr' or piece_code == 'br':
            return self.move_rook(square, same_color, all_pieces)

        elif piece_code == 'wq' or piece_code == 'bq':
            return self.move_queen(square, same_color, all_pieces)

        elif piece_code == 'wp':
            moves, promotions = self.move_white_pawn(square, all_pieces, black_pieces, board.en_passant_target)
            return moves | promotions

        elif piece_code == 'bp':
            moves, promotions = self.move_black_pawn(square, all_pieces, white_pieces, board.en_passant_target)
            return moves | promotions

        return 0

def print_bitboard(mask, title="Bitboard"):
    print(f"\n--- {title} ---")
    print("  a b c d e f g h")
    print("  ---------------")

    for rank in range(7, -1, -1):
        row_str = f"{rank + 1}|"
        for file in range(8):
            square = rank * 8 + file
            if mask & (1 << square):
                row_str += "X "
            else:
                row_str += ". "
        print(row_str)
    print("  ---------------\n")


gene = MoveGenerator()

print_bitboard(gene.rays['N'][27], "Wikeza D4")
print_bitboard(gene.knight_moves[28], "Skoczek eR")
