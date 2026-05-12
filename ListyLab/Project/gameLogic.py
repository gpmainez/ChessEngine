
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
                mask |= (1 << square_j)
        moves[square] = mask
    return moves


def precompute_all_rays(directions_dict):
    rays = {dir_name: [0] * 64 for dir_name in directions_dict}
    for square in range(64):
        row = square // 8
        file = square % 8
        for dir_name, (d_row, d_file) in directions_dict.items():
            mask = 0
            for step in range(1, 8):
                r = row + (d_row * step)
                f = file + (d_file * step)
                if 0 <= r <= 7 and 0 <= f <= 7:
                    target_square = r * 8 + f
                    mask |= (1 << target_square)
                else:
                    break
            rays[dir_name][square] = mask
    return rays


class MoveGenerator:
    def __init__(self):
        king_vector = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        knight_vector = [(2, 1), (2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2), (-2, 1), (-2, -1)]
        white_pawn = [(1, 1), (1, -1)]
        black_pawn = [(-1, -1), (-1, 1)]

        self.directions = {'N': (1, 0), 'S': (-1, 0), 'E': (0, 1), 'W': (0, -1),'NE': (1, 1), 'NW': (1, -1), 'SE': (-1, 1), 'SW': (-1, -1)
        }

        self.king_moves = precompute_moves(king_vector)
        self.knight_moves = precompute_moves(knight_vector)
        self.white_pawn_attacks = precompute_moves(white_pawn)
        self.black_pawn_attacks = precompute_moves(black_pawn)
        self.rays = precompute_all_rays(self.directions)


    def move_knight(self,square,same_color_pieces):
        return self.knight_moves[square]  & ~same_color_pieces

    def move_king(self,square,same_color_pieces):
        return self.king_moves[square] & ~same_color_pieces