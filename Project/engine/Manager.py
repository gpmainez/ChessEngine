import random
from abc import abstractmethod, ABC

from engine.Board import Board, FILE_DICT
from engine.Generator import MoveGenerator, calcualte_bit


def get_index_from_mouse(pos, sq_size):
    x, y = pos
    col = x // sq_size
    row = y // sq_size
    rank = 7 - row
    file = col

    return (rank * 8) + file


class BaseGameManager(ABC):
    def __init__(self):
        self.board = Board()
        self.generator = MoveGenerator()
        self.file_dict = FILE_DICT
        self.revert_file_dict = {value: key for key, value in self.file_dict.items()}

        self.parse_dict = {
            'wp': "white_pawns", 'wr': "white_rooks", 'wn': "white_knights", 'wb': "white_bishops",
            'wk': "white_king", 'wq': "white_queen",
            'bp': "black_pawns", 'br': "black_rooks", 'bn': "black_knights", 'bb': "black_bishops",
            'bk': "black_king", 'bq': "black_queen"
        }

        self.castle_map = {

            'w_short': {
                'king_piece': 'white_king', 'king_start': 0, 'king_end': 6,
                'rook_piece': 'white_rooks', 'rook_start': 0, 'rook_end': 5
            },
            'w_long': {
                'king_piece': 'white_king', 'king_start': 0, 'king_end': 2,
                'rook_piece': 'white_rooks', 'rook_start': 0, 'rook_end': 3
            },
            'b_short': {
                'king_piece': 'black_king', 'king_start': 0, 'king_end': 62,
                'rook_piece': 'black_rooks', 'rook_start': 0, 'rook_end': 61
            },
            'b_long': {
                'king_piece': 'black_king', 'king_start': 0, 'king_end': 58,
                'rook_piece': 'black_rooks', 'rook_start': 0, 'rook_end': 59
            }
        }
        #domyslna strategia komputera
        from engine.Strategy import RandomMoveStrategy
        self.ai_strategy = RandomMoveStrategy()

    #wykonuje ruch komputera
    def make_ai_move(self) -> bool:
        if not self.ai_strategy:
            return False
        #pobierz najlepszy ruch ze strategii
        move = self.ai_strategy.get_best_move(self)
        if move:
            start, target = move
            return self.try_to_move(start, target)
        return False

    def piece_validation(self, strt_pos):
        square = self.board.get_piece(strt_pos)

        if square is None:
            return 0
        allowed_moves = self.generator.move_piece_validation(square, strt_pos, self.board)
        return allowed_moves

    def square_under_attack(self, square, attack_color):

        if attack_color == 'black':
            enemy_pawns = self.board.black_pawns
            enemy_knights = self.board.black_knights
            enemy_bishops = self.board.black_bishops
            enemy_rooks = self.board.black_rooks
            enemy_queen = self.board.black_queen
            enemy_king = self.board.black_king
            attacked_by_pawn = self.generator.white_pawn_attacks[square]
        else:
            enemy_pawns = self.board.white_pawns
            enemy_knights = self.board.white_knights
            enemy_bishops = self.board.white_bishops
            enemy_rooks = self.board.white_rooks
            enemy_queen = self.board.white_queen
            enemy_king = self.board.white_king
            attacked_by_pawn = self.generator.black_pawn_attacks[square]

        if attacked_by_pawn & enemy_pawns:
            return True

        attacked_by_knight = self.generator.move_knight(square, 0)
        if attacked_by_knight & enemy_knights:
            return True

        attacked_by_bishop = self.generator.move_bishop(square, 0, self.board.all_pieces)
        if attacked_by_bishop & (enemy_bishops | enemy_queen):
            return True

        attacked_by_rook = self.generator.move_rook(square, 0, self.board.all_pieces)
        if attacked_by_rook & (enemy_rooks | enemy_queen):
            return True

        attacked_by_king = self.generator.move_king(square, 0)
        if attacked_by_king & enemy_king:
            return True

        return False

    def legal_moves(self, start_pos):
        legal_move = self.piece_validation(start_pos)

        if legal_move == 0:
            return 0

        piece_ui_code = self.board.get_piece(start_pos)
        if not piece_ui_code:
            return 0

        legal_mask = 0

        selected_piece_name = self.parse_dict[piece_ui_code]

        piecie_color = selected_piece_name.startswith('w')
        current_move_color = 'white' if piecie_color else 'black'
        attack_color = 'black' if piecie_color else 'white'

        target_squares = calcualte_bit(legal_move)

        for target_pos in target_squares:

            piece_under_attack = self.board.get_piece(target_pos)
            capture = self.parse_dict[piece_under_attack] if piece_under_attack else None

            is_ep = False
            if selected_piece_name in ['white_pawns', 'black_pawns'] and target_pos == self.board.en_passant_target:
                if abs(start_pos - target_pos) in [7, 9]:
                    is_ep = True
                    capture = 'black_pawns' if piecie_color else 'white_pawns'

            self.board.make_move(selected_piece_name, start_pos, target_pos, capture, is_ep)

            if piecie_color:
                king_idx = self.board.white_king.bit_length() - 1
            else:
                king_idx = self.board.black_king.bit_length() - 1

            if not self.square_under_attack(king_idx, attack_color):
                legal_mask |= (1 << target_pos)

            self.board.undo_move()

        if selected_piece_name in ['white_king', 'black_king']:
            legal_mask |= self.castle(current_move_color)

        return legal_mask

    def check_game_state(self):
        is_white_turn = self.board.white_to_move
        attack_color = 'black' if is_white_turn else 'white'

        player_pieces = self.board.white_pieces if is_white_turn else self.board.black_pieces
        player_pieces_idx = calcualte_bit(player_pieces)

        for square in player_pieces_idx:
            if self.legal_moves(square) > 0:
                return "CONTINUE"

        if is_white_turn:
            king_idx = self.board.white_king.bit_length() - 1
        else:
            king_idx = self.board.black_king.bit_length() - 1

        if self.square_under_attack(king_idx, attack_color):
            return "CHECKMATE"
        else:
            return "STALEMATE"

    def make_move_engine(self, start_pos, target_pos, promo_choice='q'):
        piece = self.parse_dict[self.board.get_piece(start_pos)]
        target_piece = self.board.get_piece(target_pos)

        piecie_color = piece.startswith('w')

        en_passant = False
        promotion = None
        rook_move = None
        castle_mask = 0

        if piece == 'white_king':
            castle_mask |= 0b0011
        elif piece == 'black_king':
            castle_mask |= 0b1100
        elif piece == 'white_rooks':
            if start_pos == self.castle_map['w_short']['rook_start']:
                castle_mask |= 0b0001
            elif start_pos == self.castle_map['w_long']['rook_start']:
                castle_mask |= 0b0010
        elif piece == 'black_rooks':
            if start_pos == self.castle_map['b_short']['rook_start']:
                castle_mask |= 0b0100
            elif start_pos == self.castle_map['b_long']['rook_start']:
                castle_mask |= 0b1000

        for key, pos_dict in self.castle_map.items():
            if start_pos == pos_dict['king_start'] and target_pos == pos_dict['king_end'] and piece == pos_dict[
                'king_piece']:
                rook_move = pos_dict['rook_start'], pos_dict['rook_end']

        if piece == "white_pawns" or piece == "black_pawns":
            if target_pos == self.board.en_passant_target and abs(start_pos - target_pos) in [7, 9]:
                en_passant = True
                capture = 'black_pawns' if piecie_color else 'white_pawns'
            else:
                capture = self.parse_dict[target_piece] if target_piece else None
                target_row = target_pos // 8

                if target_row == 7 and piece == "white_pawns":
                    promo_dict = {'q': 'white_queen', 'r': 'white_rooks', 'b': 'white_bishops', 'n': 'white_knights'}
                    promotion = promo_dict.get(promo_choice, 'white_queen')
                elif target_row == 0 and piece == "black_pawns":
                    promo_dict = {'q': 'black_queen', 'r': 'black_rooks', 'b': 'black_bishops', 'n': 'black_knights'}
                    promotion = promo_dict.get(promo_choice, 'black_queen')
        else:
            capture = self.parse_dict[target_piece] if target_piece else None

        self.board.make_move(piece, start_pos, target_pos, capture, en_passant, promotion, rook_move, castle_mask)

    def try_to_move(self, start_pos, target_pos,promo_choice='q'):

        moves = self.legal_moves(start_pos)

        if moves == 0:
            return False

        if not (moves & 1 << target_pos):
            return False

        piece = self.parse_dict[self.board.get_piece(start_pos)]
        piecie_color = piece.startswith('w')

        if piecie_color != self.board.white_to_move:
            return False

        self.make_move_engine(start_pos, target_pos,promo_choice)

        state = self.check_game_state()
        if state == "CHECKMATE":
            print(f"SZACH MAT! Wygrywa: {'Biały' if not self.board.white_to_move else 'Czarny'}")
        elif state == "STALEMATE":
            print("REMIS! Pat.")

        return True

    def user_move_parser(self, start_pos, ending_pos):
        start = self.revert_file_dict[start_pos]
        finish = self.revert_file_dict[ending_pos]

        return start, finish

    def valid_move_ui(self, start_pos):

        moves = self.legal_moves(start_pos)

        if moves == 0:
            return []

        valid_squares = calcualte_bit(moves)

        return valid_squares

    @abstractmethod
    def setup_board(self):
        pass

    @abstractmethod
    def castle(self, color):
        pass


class BasicGameManager(BaseGameManager):
    def __init__(self):
        super().__init__()
        # self.board = Board()
        # self.generator = MoveGenerator()
        #
        # self.file_dict = {'a1': 0, 'b1': 1, 'c1': 2, 'd1': 3, 'e1': 4, 'f1': 5, 'g1': 6, 'h1': 7,
        #                   'a2': 8, 'b2': 9, 'c2': 10, 'd2': 11, 'e2': 12, 'f2': 13, 'g2': 14, 'h2': 15,
        #                   'a3': 16, 'b3': 17, 'c3': 18, 'd3': 19, 'e3': 20, 'f3': 21, 'g3': 22, 'h3': 23,
        #                   'a4': 24, 'b4': 25, 'c4': 26, 'd4': 27, 'e4': 28, 'f4': 29, 'g4': 30, 'h4': 31,
        #                   'a5': 32, 'b5': 33, 'c5': 34, 'd5': 35, 'e5': 36, 'f5': 37, 'g5': 38, 'h5': 39,
        #                   'a6': 40, 'b6': 41, 'c6': 42, 'd6': 43, 'e6': 44, 'f6': 45, 'g6': 46, 'h6': 47,
        #                   'a7': 48, 'b7': 49, 'c7': 50, 'd7': 51, 'e7': 52, 'f7': 53, 'g7': 54, 'h7': 55,
        #                   'a8': 56, 'b8': 57, 'c8': 58, 'd8': 59, 'e8': 60, 'f8': 61, 'g8': 62, 'h8': 63
        #                   }
        # self.revert_file_dict = {value: key for key, value in self.file_dict.items()}
        #
        # self.parse_dict = {
        #     'wp': "white_pawns", 'wr': "white_rooks", 'wn': "white_knights", 'wb': "white_bishops",
        #     'wk': "white_king", 'wq': "white_queen",
        #     'bp': "black_pawns", 'br': "black_rooks", 'bn': "black_knights", 'bb': "black_bishops",
        #     'bk': "black_king", 'bq': "black_queen"
        # }

    def setup_board(self):
        fen_mask = f"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.castle_map['w_long']['rook_start'] = 0
        self.castle_map['b_long']['rook_start'] = 56

        self.castle_map['w_short']['rook_start'] = 7
        self.castle_map['b_short']['rook_start'] = 63

        self.castle_map['w_long']['king_start'] = 4
        self.castle_map['w_short']['king_start'] = 4
        self.castle_map['b_long']['king_start'] = 60
        self.castle_map['b_short']['king_start'] = 60

        self.board.load_fen(fen_mask)

    # def piece_validation(self, strt_pos):
    #     square = self.board.get_piece(strt_pos)
    #
    #     if square is None:
    #         return 0
    #     allowed_moves = self.generator.move_piece_validation(square, strt_pos, self.board)
    #     return allowed_moves
    #
    # def square_under_attack(self, square, attack_color):
    #
    #     if attack_color == 'black':
    #         enemy_pawns = self.board.black_pawns
    #         enemy_knights = self.board.black_knights
    #         enemy_bishops = self.board.black_bishops
    #         enemy_rooks = self.board.black_rooks
    #         enemy_queen = self.board.black_queen
    #         enemy_king = self.board.black_king
    #         attacked_by_pawn = self.generator.white_pawn_attacks[square]
    #     else:
    #         enemy_pawns = self.board.white_pawns
    #         enemy_knights = self.board.white_knights
    #         enemy_bishops = self.board.white_bishops
    #         enemy_rooks = self.board.white_rooks
    #         enemy_queen = self.board.white_queen
    #         enemy_king = self.board.white_king
    #         attacked_by_pawn = self.generator.black_pawn_attacks[square]
    #
    #     if attacked_by_pawn & enemy_pawns:
    #         return True
    #
    #     attacked_by_knight = self.generator.move_knight(square, 0)
    #     if attacked_by_knight & enemy_knights:
    #         return True
    #
    #     attacked_by_bishop = self.generator.move_bishop(square, 0, self.board.all_pieces)
    #     if attacked_by_bishop & (enemy_bishops | enemy_queen):
    #         return True
    #
    #     attacked_by_rook = self.generator.move_rook(square, 0, self.board.all_pieces)
    #     if attacked_by_rook & (enemy_rooks | enemy_queen):
    #         return True
    #
    #     attacked_by_king = self.generator.move_king(square, 0)
    #     if attacked_by_king & enemy_king:
    #         return True
    #
    #     return False
    #
    # def legal_moves(self, start_pos):
    #     legal_move = self.piece_validation(start_pos)
    #
    #     if legal_move == 0:
    #         return 0
    #
    #     piece_ui_code = self.board.get_piece(start_pos)
    #     if not piece_ui_code:
    #         return 0
    #
    #     legal_mask = 0
    #
    #     selected_piece_name = self.parse_dict[piece_ui_code]
    #
    #     piecie_color = selected_piece_name.startswith('w')
    #     current_move_color = 'white' if piecie_color else 'black'
    #     attack_color = 'black' if piecie_color else 'white'
    #
    #     target_squares = calcualte_bit(legal_move)
    #
    #     for target_pos in target_squares:
    #
    #         piece_under_attack = self.board.get_piece(target_pos)
    #         capture = self.parse_dict[piece_under_attack] if piece_under_attack else None
    #
    #         is_ep = False
    #         if selected_piece_name in ['white_pawns', 'black_pawns'] and target_pos == self.board.en_passant_target:
    #             is_ep = True
    #             capture = 'black_pawns' if piecie_color else 'white_pawns'
    #
    #         self.board.make_move(selected_piece_name, start_pos, target_pos, capture, is_ep)
    #
    #         if piecie_color:
    #             king_idx = self.board.white_king.bit_length() - 1
    #         else:
    #             king_idx = self.board.black_king.bit_length() - 1
    #
    #         if not self.square_under_attack(king_idx, attack_color):
    #             legal_mask |= (1 << target_pos)
    #
    #         self.board.undo_move()
    #
    #     if selected_piece_name in ['white_king', 'black_king']:
    #         legal_mask |= self.castle(current_move_color)
    #
    #     return legal_mask

    def castle(self, color):

        castle_mask = 0

        if color == 'black':
            short_castle = 4
            long_castle = 8

            short_castle_squares = (1 << 61) | (1 << 62)
            long_castle_squares = (1 << 57) | (1 << 58) | (1 << 59)

        else:
            short_castle = 1
            long_castle = 2

            short_castle_squares = (1 << 5) | (1 << 6)
            long_castle_squares = (1 << 1) | (1 << 2) | (1 << 3)

        if self.board.castling_rights & short_castle:
            if (self.board.all_pieces & short_castle_squares) == 0:

                if color == 'white':
                    if (not self.square_under_attack(4, 'black')
                            and not self.square_under_attack(5, 'black')
                            and not self.square_under_attack(6, 'black')):
                        castle_mask |= (1 << 6)

                elif color == 'black':
                    if (not self.square_under_attack(60, 'white')
                            and not self.square_under_attack(61, 'white')
                            and not self.square_under_attack(62, 'white')):
                        castle_mask |= (1 << 62)

        if self.board.castling_rights & long_castle:
            if (self.board.all_pieces & long_castle_squares) == 0:

                if color == 'white':
                    if (not self.square_under_attack(4, 'black')
                            and not self.square_under_attack(3, 'black')
                            and not self.square_under_attack(2, 'black')):
                        castle_mask |= (1 << 2)

                elif color == 'black':
                    if (not self.square_under_attack(60, 'white')
                            and not self.square_under_attack(59, 'white')
                            and not self.square_under_attack(58, 'white')):
                        castle_mask |= (1 << 58)

        return castle_mask


# def check_game_state(self):
#     is_white_turn = self.board.white_to_move
#     attack_color = 'black' if is_white_turn else 'white'
#
#     player_pieces = self.board.white_pieces if is_white_turn else self.board.black_pieces
#     player_pieces_idx = calcualte_bit(player_pieces)
#
#     for square in player_pieces_idx:
#         if self.legal_moves(square) > 0:
#             return "CONTINUE"
#
#     if is_white_turn:
#         king_idx = self.board.white_king.bit_length() - 1
#     else:
#         king_idx = self.board.black_king.bit_length() - 1
#
#     if self.square_under_attack(king_idx, attack_color):
#         return "CHECKMATE"
#     else:
#         return "STALEMATE"
#
# def try_to_move(self, start_pos, target_pos):
#
#     moves = self.legal_moves(start_pos)
#
#     if moves == 0:
#         return False
#
#     if not (moves & 1 << target_pos):
#         return False
#
#     piece = self.parse_dict[self.board.get_piece(start_pos)]
#     target_piece = self.board.get_piece(target_pos)
#
#     piecie_color = piece.startswith('w')
#
#     if piecie_color != self.board.white_to_move:
#         return False
#
#     en_passant = False
#     promotion = None
#
#     if piece == "white_pawns" or piece == "black_pawns":
#
#         if target_pos == self.board.en_passant_target:
#             en_passant = True
#
#             if piece == 'white_pawns':
#                 capture = 'black_pawns'
#             else:
#                 capture = 'white_pawns'
#
#         else:
#             capture = self.parse_dict[target_piece] if target_piece else None
#
#             target_row = target_pos // 8
#             if target_row == 7 and piece == "white_pawns":
#                 promotion = 'white_queen'
#             elif target_row == 0 and piece == "black_pawns":
#                 promotion = 'black_queen'
#     else:
#         capture = self.parse_dict[target_piece] if target_piece else None
#
#     self.board.make_move(piece, start_pos, target_pos, capture, en_passant, promotion)
#
#     state = self.check_game_state()
#     if state == "CHECKMATE":
#         print(f"SZACH MAT! Wygrywa: {'Biały' if not self.board.white_to_move else 'Czarny'}")
#     elif state == "STALEMATE":
#         print("REMIS! Pat.")
#
#     return True
#
# def user_move_parser(self, start_pos, ending_pos):
#     start = self.revert_file_dict[start_pos]
#     finish = self.revert_file_dict[ending_pos]
#
#     return start, finish
#
# def valid_move_ui(self, start_pos):
#
#     moves = self.legal_moves(start_pos)
#
#     if moves == 0:
#         return []
#
#     valid_squares = calcualte_bit(moves)
#
#     return valid_squares


class FisherChessGameManager(BaseGameManager):
    def __init__(self):
        super().__init__()

    def setup_starting_pieces(self):
        row: list[str | None] = [None] * 8

        row[random.choice([0, 2, 4, 6])] = 'B'
        row[random.choice([1, 3, 5, 7])] = 'B'

        empty_spots = [i for i in range(8) if row[i] is None]
        row[random.choice(empty_spots)] = 'Q'

        empty_spots = [i for i in range(8) if row[i] is None]
        knight_spots = random.sample(empty_spots, 2)
        row[(knight_spots[0])] = 'N'
        row[(knight_spots[1])] = 'N'

        empty_spots = [i for i in range(8) if row[i] is None]
        row[(empty_spots[0])] = 'R'
        row[(empty_spots[1])] = 'K'
        row[(empty_spots[2])] = 'R'

        placement = "".join([piece if piece is not None else "" for piece in row])

        return placement

    def setup_board(self):
        fen960 = self.setup_starting_pieces()
        fen_mask = f"{fen960.lower()}/pppppppp/8/8/8/8/PPPPPPPP/{fen960} w KQkq - 0 1"
        is_first_rook = True

        for i, c in enumerate(fen960.upper()):
            if c == 'R':
                if is_first_rook:
                    self.castle_map['w_long']['rook_start'] = i
                    self.castle_map['b_long']['rook_start'] = i + 56
                    is_first_rook = False
                else:
                    self.castle_map['w_short']['rook_start'] = i
                    self.castle_map['b_short']['rook_start'] = i + 56

            elif c == 'K':
                self.castle_map['w_long']['king_start'] = i
                self.castle_map['w_short']['king_start'] = i
                self.castle_map['b_long']['king_start'] = i + 56
                self.castle_map['b_short']['king_start'] = i + 56

        self.board.load_fen(fen_mask)

    def _get_right_bit(self, color, side):
        if color == 'white':
            right_bit = 1 if side == 'short' else 2
        else:
            right_bit = 4 if side == 'short' else 8

        return right_bit

    def castle(self, color):
        castle_mask = 0
        enemy_color = 'black' if color == 'white' else 'white'

        for side in ['short', 'long']:
            key = f"{color[0]}_{side}"
            castle_piecess = self.castle_map.get(key)

            if not castle_piecess: continue

            right_bit = self._get_right_bit(color, side)
            #can compare number with binary
            # 0001 W short
            # 0010 W long
            # 0100 B short
            # 1000 B long

            if not (self.board.castling_rights & right_bit):
                continue

            start_k, end_k = castle_piecess['king_start'], castle_piecess['king_end']
            start_r, end_r = castle_piecess['rook_start'], castle_piecess['rook_end']

            #either queenside -  or kingside +
            step = 1 if end_k > start_k else -1
            king_path = range(start_k, end_k + step, step)

            king_safe = all(not self.square_under_attack(sq, enemy_color) for sq in king_path)
            if not king_safe: continue

            min_path = min(start_k, start_r, end_k, end_r)
            max_path = max(start_k, start_r, end_k, end_r)

            path_clear = True
            for sq in range(min_path, max_path + 1):

                if sq == start_k or sq == start_r:
                    continue
                if self.board.all_pieces & (1 << sq):
                    path_clear = False
                    break

            if path_clear:
                castle_mask |= (1 << end_k)

        return castle_mask


#wzorzec fabryki - tworzy odpowiedni manager na podstawie trybu gry
class GameManagerFactory:
    #dostepne tryby i ich etykiety
    MODES = {
        "standard": "Szachy standardowe",
        "fisher":   "Chess960 (Fischer Random)",
    }

    @staticmethod
    def create(mode: str) -> "BaseGameManager":
        if mode == "standard":
            m = BasicGameManager()
        elif mode == "fisher":
            m = FisherChessGameManager()
        else:
            raise ValueError(f"nieznany tryb gry: {mode}")
        m.setup_board()
        return m
