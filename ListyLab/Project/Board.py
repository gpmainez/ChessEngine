class Board:
    def __init__(self):
        self.white_pawns = 0xFF00
        self.white_rooks = 0x81
        self.white_knights = 0x42
        self.white_bishops = 0x24
        self.white_queens = 0x08
        self.white_kings = 0x10

        self.black_pawns = self.white_pawns << 40
        self.black_rooks = self.white_rooks << 56
        self.black_knights = self.white_knights << 56
        self.black_bishops = self.white_bishops << 56
        self.black_queens = self.white_queens << 56
        self.black_kings = self.white_kings << 56

        self.moves_history = []

    @property
    def white_pieces(self):
        return self.white_pawns | self.white_rooks | self.white_knights | self.white_bishops | self.white_queens | self.white_kings

    @property
    def black_pieces(self):
        return self.black_pawns | self.black_rooks | self.black_knights | self.black_bishops | self.black_queens | self.black_kings

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
            "move": move}

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
            current_board_capture = getattr(self, last_move["capture_name"])
            setattr(self, last_move["capture_name"], current_board_capture)

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


    
