import random
from engine.Generator import calcualte_bit

#  wartosci figur szachowych
piece_values = {
    'wp': 100, 'wn': 320, 'wb': 330, 'wr': 500, 'wq': 900, 'wk': 20000,
    'bp': -100, 'bn': -320, 'bb': -330, 'br': -500, 'bq': -900, 'bk': -20000
}

#tablice pozycji dla pionow
pawn_pst = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
   10, 10, 20, 30, 30, 20, 10, 10,
   50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0
]

#tablice pozycji dla skoczkow
knight_pst = [
   -50,-40,-30,-30,-30,-30,-40,-50,
   -40,-20,  0,  5,  5,  0,-20,-40,
   -30,  5, 10, 15, 15, 10,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30,
   -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 10, 15, 15, 10,  0,-30,
   -40,-20,  0,  0,  0,  0,-20,-40,
   -50,-40,-30,-30,-30,-30,-40,-50
]

#funkcja oceny pozycji na planszy
def evaluate_board(board) -> int:
    score = 0
    #przechodzimy po wszystkich polach
    for sq in range(64):
        piece = board.get_piece(sq)
        if piece is None:
            continue
        
        #dodaj wartosc materialna
        score += piece_values[piece]
        
        #dodaj ocene pozycyjna
        if piece == 'wp':
            score += pawn_pst[sq]
        elif piece == 'bp':
            #lustrzane odbicie dla czarnych
            mirror_sq = (7 - (sq // 8)) * 8 + (sq % 8)
            score -= pawn_pst[mirror_sq]
        elif piece == 'wn':
            score += knight_pst[sq]
        elif piece == 'bn':
            mirror_sq = (7 - (sq // 8)) * 8 + (sq % 8)
            score -= knight_pst[mirror_sq]
            
    return score

#pobiera wszystkie legalne ruchy
def get_all_legal_moves(manager) -> list[tuple[int, int]]:
    legal_moves_list = []
    is_white = manager.board.white_to_move
    player_pieces = manager.board.white_pieces if is_white else manager.board.black_pieces
    active_squares = calcualte_bit(player_pieces)
    
    for start_sq in active_squares:
        moves_mask = manager.legal_moves(start_sq)
        target_squares = calcualte_bit(moves_mask)
        for target_sq in target_squares:
            legal_moves_list.append((start_sq, target_sq))
    return legal_moves_list

#minimax z odcieciem alpha beta
def minimax_ab(manager, depth: int, alpha: float, beta: float, maximizing: bool) -> int:
    #sprawdzamy stan gry lub glebokosc
    state = manager.check_game_state()
    if state == "CHECKMATE":
        #mat oznacza wygrana przeciwnika
        return -25000 if maximizing else 25000
    elif state == "STALEMATE":
        return 0
        
    if depth == 0:
        return evaluate_board(manager.board)
        
    moves = get_all_legal_moves(manager)
    if not moves:
        return evaluate_board(manager.board)
        
    if maximizing:
        max_eval = -999999
        for start, target in moves:
            #wykonaj ruch za pomoca zunifikowanego silnika w managerze (w tym roszady i promocje)
            manager.make_move_engine(start, target)
            
            evaluation = minimax_ab(manager, depth - 1, alpha, beta, False)
            manager.board.undo_move()
            
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break #odciecie beta
        return max_eval
    else:
        min_eval = 999999
        for start, target in moves:
            manager.make_move_engine(start, target)
            
            evaluation = minimax_ab(manager, depth - 1, alpha, beta, True)
            manager.board.undo_move()
            
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break #odciecie alpha
        return min_eval

#szuka najlepszego ruchu dla aktywnego gracza
def find_best_move(manager, depth: int) -> tuple[int, int] | None:
    moves = get_all_legal_moves(manager)
    if not moves:
        return None
        
    best_move = None
    is_white = manager.board.white_to_move
    
    #shuffle ruchow na poczatek dla szybszego alpha beta
    random.shuffle(moves)
    
    if is_white:
        best_val = -999999
        for start, target in moves:
            manager.make_move_engine(start, target)
            val = minimax_ab(manager, depth - 1, -999999, 999999, False)
            manager.board.undo_move()
            
            if val > best_val:
                best_val = val
                best_move = (start, target)
    else:
        best_val = 999999
        for start, target in moves:
            manager.make_move_engine(start, target)
            val = minimax_ab(manager, depth - 1, -999999, 999999, True)
            manager.board.undo_move()
            
            if val < best_val:
                best_val = val
                best_move = (start, target)
                
    return best_move
