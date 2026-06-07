import pygame
import sys
import random
from engine.Manager import get_index_from_mouse, GameManagerFactory
from engine.Board import validate_fen, FILE_DICT, REVERT_FILE_DICT
from engine.Strategy import RandomMoveStrategy, MinimaxAlphaBetaStrategy
from engine.Bridge import GameInterfaceBridge

pygame.init()

WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
COLOR_LIGHT = (240, 217, 181)
COLOR_DARK = (85, 107, 47)

COLOR_SELECTED = (233, 150, 122)
COLOR_LAST_MOVE = (194, 202, 134)
COLOR_MENU_BG = (30, 30, 30)
COLOR_MENU_BTN = (60, 80, 60)
COLOR_MENU_HOVER = (90, 120, 90)
COLOR_MENU_TEXT = (230, 230, 220)

selected_square = None
player_last_move = None
computer_last_move = None
legal_moves_to_draw = []

Images = {}
#manager i bridge tworzone po wyborze trybu
manager = GameManagerFactory.create("standard")
bridge = GameInterfaceBridge(manager)
current_difficulty = 3 # domyslnie Medium (depth 3)

vs_ai = True
ai_color = False #czarne to komputer
flipped = False

def get_coords(idx):
    if flipped:
        return idx // 8, 7 - (idx % 8)
    else:
        return 7 - (idx // 8), idx % 8

def get_index_from_mouse(pos, sq_size):
    x, y = pos
    col = x // sq_size
    row = y // sq_size
    if flipped:
        rank = row
        file = 7 - col
    else:
        rank = 7 - row
        file = col
    return (rank * 8) + file

#poziomy trudnosci ai
DIFFICULTY_LEVELS = [
    {"name": "Extra Easy", "desc": "losowe ruchy"},
    {"name": "Easy", "desc": "minimax depth 1"},
    {"name": "Medium", "desc": "minimax depth 3"},
    {"name": "Hard", "desc": "minimax depth 5"},
]

#tryby gry dostepne w menu
GAME_MODES = [
    {"mode": "standard", "name": "Szachy standardowe",   "desc": "klasyczny uklad figur"},
    {"mode": "fisher",   "name": "Chess960 (Fischer)",    "desc": "losowy uklad figur"},
]

#kolory gracza dostepne w menu
COLOR_CHOICES = [
    {"color": "white",  "name": "Biale",  "desc": "zaczynasz gre jako pierwszy"},
    {"color": "black",  "name": "Czarne",  "desc": "komputer zaczyna gre jako pierwszy"},
    {"color": "random", "name": "Losowo",  "desc": "losowy wybor koloru"},
    {"color": "both",   "name": "Bez AI",  "desc": "ruch obydwoma kolorami (sam ze soba)"},
]

parse_dict = {'wp': "white_pawns", 'wr': "white_rooks", 'wn': "white_knights", 'wb': "white_bishops",
              'wk': "white_king", 'wq': "white_queen", 'bp': "black_pawns", 'br': "black_rooks", 'bn': "black_knights",
              'bb': "black_bishops",
              'bk': "black_king", 'bq': "black_queen"}


def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = COLOR_LIGHT if (row + col) % 2 == 0 else COLOR_DARK
            rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)


def highlight_square(screen, index, color_rgba):
    if index is None:
        return

    r, c = get_coords(index)

    s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
    s.fill(color_rgba)
    screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def loadImages():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        Images[piece] = pygame.transform.scale(
            pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, skip_idx=None):
    #  draw all figuras on board
    #   optionally skip drawing one figura
    for idx in range(64):
        if idx == skip_idx:
            continue

        char = bridge.get_piece(idx)

        if char is None:
            continue

        r, c = get_coords(idx)

        screen.blit(Images[char], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))



def draw_legal_moves(screen, moves_list):
    if not moves_list:
        return

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    CIRCLE_COLOR = (120, 135, 95)
    circle_radius = SQ_SIZE // 6

    # calculate index arry[64] -> [r][c]
    for index in moves_list:
        r, c = get_coords(index)

        center_x = c * SQ_SIZE + (SQ_SIZE // 2)
        center_y = r * SQ_SIZE + (SQ_SIZE // 2)

        pygame.draw.circle(overlay, CIRCLE_COLOR, (center_x, center_y), circle_radius)

    screen.blit(overlay, (0, 0))


def animate_move(screen, start, target, figura_char, clock, p_move, c_move):
    #  lerp animation function
    #   smoothly slides figura from start to target
    #  locks input during animation and clears queue
    if start is None or target is None or figura_char is None:
        return

    start_r, start_c = get_coords(start)
    target_r, target_c = get_coords(target)

    start_x = start_c * SQ_SIZE
    start_y = start_r * SQ_SIZE
    target_x = target_c * SQ_SIZE
    target_y = target_r * SQ_SIZE

    for step in range(1, 16):
        t = step / 15.0
        curr_x = start_x + (target_x - start_x) * t
        curr_y = start_y + (target_y - start_y) * t

        draw_board(screen)

        #  highlight last moves
        if p_move is not None:
            highlight_square(screen, p_move[0], COLOR_LAST_MOVE)
            highlight_square(screen, p_move[1], COLOR_LAST_MOVE)
        if c_move is not None:
            highlight_square(screen, c_move[0], COLOR_LAST_MOVE)
            highlight_square(screen, c_move[1], COLOR_LAST_MOVE)

        # highlight king in check
        king_in_check = bridge.get_king_in_check()
        if king_in_check is not None:
            highlight_square(screen, king_in_check, (255, 0, 0, 150))

        #  draw all figuras except the animating one which is at target
        draw_pieces(screen, skip_idx=target)

        #   draw the animating figura
        screen.blit(Images[figura_char], pygame.Rect(curr_x, curr_y, SQ_SIZE, SQ_SIZE))

        pygame.display.flip()
        clock.tick(60)
        pygame.event.pump()

    #  clear event queue to discard user inputs
    pygame.event.clear()


def do_ai_move(screen, clock):
    """helper - wykonaj ruch komputera i animuj go"""
    global computer_last_move, player_last_move

    #  draw board before ai thinks
    draw_board(screen)
    if player_last_move is not None:
        highlight_square(screen, player_last_move[0], COLOR_LAST_MOVE)
        highlight_square(screen, player_last_move[1], COLOR_LAST_MOVE)
    if computer_last_move is not None:
        highlight_square(screen, computer_last_move[0], COLOR_LAST_MOVE)
        highlight_square(screen, computer_last_move[1], COLOR_LAST_MOVE)

    king_in_check = bridge.get_king_in_check()
    if king_in_check is not None:
        highlight_square(screen, king_in_check, (255, 0, 0, 150))

    draw_pieces(screen)
    pygame.display.flip()

    pygame.display.set_caption("AI mysli...")
    ai_move = bridge.make_ai_move(current_difficulty)
    pygame.display.set_caption("Python Bitboard Engine GUI")

    if ai_move:
        start_idx = FILE_DICT[ai_move[0]]
        target_idx = FILE_DICT[ai_move[1]]
        computer_last_move = (start_idx, target_idx)

        # animate computer move
        figura_char = bridge.get_piece(target_idx)
        animate_move(screen, start_idx, target_idx, figura_char, clock,
                     player_last_move, computer_last_move)


def draw_difficulty_menu(screen):
    #rysuje menu wyboru trudnosci ai
    screen.fill(COLOR_MENU_BG)

    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_btn = pygame.font.SysFont("Arial", 22)
    font_desc = pygame.font.SysFont("Arial", 16)

    title = font_title.render("Wybierz poziom AI", True, COLOR_MENU_TEXT)
    title_rect = title.get_rect(center=(WIDTH // 2, 60))
    screen.blit(title, title_rect)

    mouse_pos = pygame.mouse.get_pos()
    btn_rects = []
    btn_w = 320
    btn_h = 70
    start_y = 120
    gap = 15

    for i, lvl in enumerate(DIFFICULTY_LEVELS):
        x = (WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + gap)
        rect = pygame.Rect(x, y, btn_w, btn_h)

        #hover effect
        color = COLOR_MENU_HOVER if rect.collidepoint(mouse_pos) else COLOR_MENU_BTN
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_MENU_TEXT, rect, width=2, border_radius=8)

        # nazwa poziomu
        label = font_btn.render(f"{i} - {lvl['name']}", True, COLOR_MENU_TEXT)
        label_rect = label.get_rect(center=(rect.centerx, rect.y + 25))
        screen.blit(label, label_rect)

        #opis strategii
        desc = font_desc.render(lvl["desc"], True, (170, 170, 160))
        desc_rect = desc.get_rect(center=(rect.centerx, rect.y + 50))
        screen.blit(desc, desc_rect)

        btn_rects.append(rect)

    #  hint na dole
    hint = font_desc.render("kliknij aby wybrac poziom trudnosci", True, (130, 130, 120))
    hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(hint, hint_rect)

    pygame.display.flip()
    return btn_rects


def difficulty_menu(screen, clock):
    #ekran wyboru trudnosci - blokuje do momentu wyboru
    global current_difficulty
    while True:
        btn_rects = draw_difficulty_menu(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(btn_rects):
                    if rect.collidepoint(event.pos):
                        # Map index to difficulty: 0 -> 0, 1 -> 1, 2 -> 3, 3 -> 5
                        diff_mapping = {0: 0, 1: 1, 2: 3, 3: 5}
                        current_difficulty = diff_mapping[i]
                        print(f"ai level set to {DIFFICULTY_LEVELS[i]['name']}")
                        return

        clock.tick(30)


def draw_mode_menu(screen):
    #rysuje menu wyboru trybu gry
    screen.fill(COLOR_MENU_BG)

    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_btn   = pygame.font.SysFont("Arial", 22)
    font_desc  = pygame.font.SysFont("Arial", 16)

    title = font_title.render("Wybierz tryb gry", True, COLOR_MENU_TEXT)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

    mouse_pos = pygame.mouse.get_pos()
    btn_rects = []
    btn_w, btn_h, gap = 320, 70, 20
    start_y = 150

    for i, gm in enumerate(GAME_MODES):
        x = (WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + gap)
        rect = pygame.Rect(x, y, btn_w, btn_h)

        color = COLOR_MENU_HOVER if rect.collidepoint(mouse_pos) else COLOR_MENU_BTN
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_MENU_TEXT, rect, width=2, border_radius=8)

        label = font_btn.render(gm["name"], True, COLOR_MENU_TEXT)
        screen.blit(label, label.get_rect(center=(rect.centerx, rect.y + 25)))

        desc = font_desc.render(gm["desc"], True, (170, 170, 160))
        screen.blit(desc, desc.get_rect(center=(rect.centerx, rect.y + 50)))

        btn_rects.append(rect)

    hint = font_desc.render("kliknij aby wybrac tryb", True, (130, 130, 120))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 40)))

    pygame.display.flip()
    return btn_rects


def mode_menu(screen, clock):
    #ekran wyboru trybu - zwraca wybrany tryb jako string
    global manager, bridge
    while True:
        btn_rects = draw_mode_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(btn_rects):
                    if rect.collidepoint(event.pos):
                        chosen = GAME_MODES[i]["mode"]
                        #fabryka tworzy nowy manager dla wybranego trybu
                        manager = GameManagerFactory.create(chosen)
                        bridge = GameInterfaceBridge(manager)
                        print(f"game mode: {GAME_MODES[i]['name']}")
                        return
        clock.tick(30)


def draw_color_menu(screen):
    #rysuje menu wyboru koloru gracza
    screen.fill(COLOR_MENU_BG)

    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_btn   = pygame.font.SysFont("Arial", 22)
    font_desc  = pygame.font.SysFont("Arial", 16)

    title = font_title.render("Wybierz swoj kolor", True, COLOR_MENU_TEXT)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 70)))

    mouse_pos = pygame.mouse.get_pos()
    btn_rects = []
    btn_w, btn_h, gap = 320, 70, 15
    start_y = 140

    for i, col in enumerate(COLOR_CHOICES):
        x = (WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + gap)
        rect = pygame.Rect(x, y, btn_w, btn_h)

        color = COLOR_MENU_HOVER if rect.collidepoint(mouse_pos) else COLOR_MENU_BTN
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_MENU_TEXT, rect, width=2, border_radius=8)

        label = font_btn.render(col["name"], True, COLOR_MENU_TEXT)
        screen.blit(label, label.get_rect(center=(rect.centerx, rect.y + 25)))

        desc = font_desc.render(col["desc"], True, (170, 170, 160))
        screen.blit(desc, desc.get_rect(center=(rect.centerx, rect.y + 50)))

        btn_rects.append(rect)

    hint = font_desc.render("kliknij aby wybrac kolor", True, (130, 130, 120))
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

    pygame.display.flip()
    return btn_rects


def color_menu(screen, clock):
    #ekran wyboru koloru - ustawia globalne ai_color
    global ai_color, vs_ai, flipped
    while True:
        btn_rects = draw_color_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(btn_rects):
                    if rect.collidepoint(event.pos):
                        chosen = COLOR_CHOICES[i]["color"]
                        if chosen == "white":
                            vs_ai = True
                            ai_color = False #ai jest czarne
                        elif chosen == "black":
                            vs_ai = True
                            ai_color = True  #ai jest biale
                        elif chosen == "random":
                            vs_ai = True
                            ai_color = random.choice([True, False])
                        elif chosen == "both":
                            vs_ai = False
                            ai_color = None
                        
                        flipped = (vs_ai and ai_color == True)
                        print(f"vs_ai set to {vs_ai}, ai color set to {ai_color}, flipped to {flipped}")
                        return
        clock.tick(30)


def choose_promotion(screen, color_prefix, clock):
    pieces_to_draw = [f'{color_prefix}q', f'{color_prefix}r', f'{color_prefix}b', f'{color_prefix}n']
    promo_codes = ['q', 'r', 'b', 'n']


    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))


    menu_w, menu_h = 4 * SQ_SIZE + 20, SQ_SIZE + 20
    menu_x = (WIDTH - menu_w) // 2
    menu_y = (HEIGHT - menu_h) // 2

    pygame.draw.rect(screen, COLOR_LIGHT, (menu_x, menu_y, menu_w, menu_h), border_radius=10)
    pygame.draw.rect(screen, COLOR_DARK, (menu_x, menu_y, menu_w, menu_h), width=4, border_radius=10)


    rects = []
    for i, piece_key in enumerate(pieces_to_draw):
        px = menu_x + 10 + (i * SQ_SIZE)
        py = menu_y + 10
        screen.blit(Images[piece_key], (px, py))
        rects.append(pygame.Rect(px, py, SQ_SIZE, SQ_SIZE))

    pygame.display.flip()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        return promo_codes[i]
        clock.tick(30)

def draw_game_over(screen, state):
    #rysuje overlay po koncu gry
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont("Arial", 42, bold=True)
    font_sub = pygame.font.SysFont("Arial", 20)

    if state == "CHECKMATE":
        #kto wygral - przeciwna strona do tej ktora nie ma ruchow
        winner = "Czarny" if bridge.white_to_move else "Bialy"
        msg = f"SZACH MAT! Wygrywa {winner}"
        color = (220, 80, 60)
    else:
        msg = "REMIS - PAT"
        color = (180, 180, 80)

    text = font_big.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(text, text_rect)

    #podpowiedz restart
    hint = font_sub.render("Nacisnij R aby zagrac ponownie", True, (200, 200, 200))
    hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(hint, hint_rect)


def check_and_get_state():
    #sprawdza stan gry i zwraca go
    res = bridge.get_game_result()
    return res if res is not None else "CONTINUE"


def main():
    global selected_square, player_last_move, computer_last_move, legal_moves_to_draw

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python Bitboard Engine GUI")
    clock = pygame.time.Clock()

    loadImages()

    # najpierw wybor trybu gry potem trudnosci i koloru
    mode_menu(screen, clock)
    difficulty_menu(screen, clock)
    color_menu(screen, clock)

    #   wykonaj ruch ai jesli gra jako pierwsze (biale)
    if vs_ai and bridge.white_to_move == ai_color:
        do_ai_move(screen, clock)

    game_over_state = None  #None CHECKMATE lub STALEMATE

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    #  restart - wybierz tryb trudnosc i kolor od nowa
                    selected_square = None
                    player_last_move = None
                    computer_last_move = None
                    legal_moves_to_draw = []
                    game_over_state = None
                    mode_menu(screen, clock)
                    difficulty_menu(screen, clock)
                    color_menu(screen, clock)
                    if vs_ai and bridge.white_to_move == ai_color:
                        do_ai_move(screen, clock)
                    continue

                #  zablokuj klawisze podczas game over (oprocz R i Q)
                if game_over_state:
                    continue

                if event.key == pygame.K_s:
                    #   save board state
                    if bridge.save_game("savegame.fen"):
                        print("saved game to savegame.fen")
                    else:
                        print("failed to save game")

                elif event.key == pygame.K_l:
                    #  load board state
                    if bridge.load_game("savegame.fen"):
                        selected_square = None
                        player_last_move = None
                        computer_last_move = None
                        legal_moves_to_draw = []
                        game_over_state = None

                        #  sprawdz stan gry po wczytaniu
                        state = check_and_get_state()
                        if state != "CONTINUE":
                            game_over_state = state
                        elif vs_ai and bridge.white_to_move == ai_color:
                            do_ai_move(screen, clock)
                            state = check_and_get_state()
                            if state != "CONTINUE":
                                game_over_state = state

                        print("loaded game from savegame.fen")
                    else:
                        print("failed to load game from savegame.fen")

                elif event.key == pygame.K_d:
                    #  zmiana poziomu trudnosci w trakcie gry
                    difficulty_menu(screen, clock)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                #  blokada klikania po koncu gry
                if game_over_state:
                    continue

                if event.button == 1:
                    clicked_idx = get_index_from_mouse(pygame.mouse.get_pos(), SQ_SIZE)
                    #  if selected square has figura
                    if selected_square is None:
                        if bridge.get_piece(clicked_idx) is not None:
                            selected_square = clicked_idx
                            print(bridge.get_piece(clicked_idx))
                            clicked_square_str = REVERT_FILE_DICT[selected_square]
                            legal_moves_str = bridge.get_legal_moves(clicked_square_str)
                            legal_moves_to_draw = [FILE_DICT[mv] for mv in legal_moves_str]
                    else:
                        #  second click
                        if selected_square != clicked_idx:
                            start = REVERT_FILE_DICT[selected_square]
                            target = REVERT_FILE_DICT[clicked_idx]

                            moving_piece = bridge.get_piece(selected_square)
                            target_row = clicked_idx // 8


                            promo_choice = 'q'

                            if moving_piece == 'wp' and target_row == 7:
                                promo_choice = choose_promotion(screen, 'w', clock)
                            elif moving_piece == 'bp' and target_row == 0:
                                promo_choice = choose_promotion(screen, 'b', clock)


                            legal = bridge.make_move(start, target, promo_choice)

                            if legal:
                                player_last_move = (selected_square, clicked_idx)

                                #  animate player move
                                figura_char = bridge.get_piece(clicked_idx)
                                animate_move(screen, selected_square, clicked_idx, figura_char, clock, player_last_move, computer_last_move)

                                #  sprawdz stan po ruchu gracza
                                state = check_and_get_state()
                                if state != "CONTINUE":
                                    game_over_state = state
                                elif vs_ai and bridge.white_to_move == ai_color:
                                    #  ruch ai tylko gdy gra trwa
                                    do_ai_move(screen, clock)
                                    state = check_and_get_state()
                                    if state != "CONTINUE":
                                        game_over_state = state
                            else:
                                print("err")

                        selected_square = None
                        legal_moves_to_draw = []


                elif event.button == 3:
                    selected_square = None
                    legal_moves_to_draw = []

        draw_board(screen)

        if player_last_move is not None:
            highlight_square(screen, player_last_move[0], COLOR_LAST_MOVE)
            highlight_square(screen, player_last_move[1], COLOR_LAST_MOVE)

        if computer_last_move is not None:
            highlight_square(screen, computer_last_move[0], COLOR_LAST_MOVE)
            highlight_square(screen, computer_last_move[1], COLOR_LAST_MOVE)

        king_in_check = bridge.get_king_in_check()
        if king_in_check is not None:
            highlight_square(screen, king_in_check, (255, 0, 0, 150))

        if selected_square is not None and not game_over_state:
            highlight_square(screen, selected_square, COLOR_SELECTED)
        if legal_moves_to_draw and not game_over_state:
            draw_legal_moves(screen, legal_moves_to_draw)

        draw_pieces(screen)

        #  nakladka konca gry na wierzchu planszy
        if game_over_state:
            draw_game_over(screen, game_over_state)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
