import pygame
import sys
from frontUtlis import UserApi, get_index_from_mouse

pygame.init()

WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
COLOR_LIGHT = (240, 217, 181)
COLOR_DARK = (85, 107, 47)

COLOR_SELECTED = (233, 150, 122)
COLOR_LAST_MOVE = (233, 150, 122)

selected_square = None
last_move = None
legal_moves_to_draw = []

Images = {}
user_api = UserApi()

parse_dict = {'wp': "white_pawns", 'wr': "white_rooks", 'wn': "white_knights", 'wb': "white_bishops",
              'wk': "white_king", 'wq': "white_queen", 'bp': "black_pawns", 'br': "black_rooks", 'bn': "black_knights",
              'bb': "black_bishops",
              'bk': "black_king", 'bq': "black_queen"}


def draw_board(screen):
    """Rysuje czystą szachownicę."""
    for row in range(8):
        for col in range(8):
            color = COLOR_LIGHT if (row + col) % 2 == 0 else COLOR_DARK
            rect = pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)


def highlight_square(screen, index, color_rgba):
    if index is None:
        return

    r = 7 - (index // 8)
    c = index % 8

    s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
    s.fill(color_rgba)
    screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def loadImages():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        Images[piece] = pygame.transform.scale(
            pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for idx in range(64):

        char = board.get_piece(idx)

        if char is None:
            continue

        r = 7 - (idx // 8)
        c = idx % 8

        screen.blit(Images[char], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_legal_moves(screen, moves_list):
    if not moves_list:
        return

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    circle_color = (100, 100, 100, 150)
    circle_radius = SQ_SIZE // 6

    for index in moves_list:
        r = 7 - (index // 8)
        c = index % 8

        center_x = c * SQ_SIZE + (SQ_SIZE // 2)
        center_y = r * SQ_SIZE + (SQ_SIZE // 2)

        pygame.draw.circle(overlay, circle_color, (center_x, center_y), circle_radius)

    screen.blit(overlay, (0, 0))


def main():
    global selected_square, last_move, legal_moves_to_draw

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python Bitboard Engine GUI")
    clock = pygame.time.Clock()

    loadImages()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_idx = get_index_from_mouse(pygame.mouse.get_pos(), SQ_SIZE)

                    if selected_square is None:

                        if user_api.board.get_piece(clicked_idx) is not None:
                            selected_square = clicked_idx
                            print(user_api.board.get_piece(clicked_idx))
                            legal_moves_to_draw = user_api.valid_move_ui(selected_square)
                    else:
                        # second click
                        if selected_square != clicked_idx:
                            start, target = user_api.user_move_parser(selected_square, clicked_idx)
                            print("move from {} to {}".format(start, target))

                            legal = user_api.try_to_move(selected_square, clicked_idx)

                            if legal:
                                last_move = (selected_square, clicked_idx)
                            else:
                                print("err")

                        selected_square = None
                        legal_moves_to_draw = []


                elif event.button == 3:
                    selected_square = None
                    legal_moves_to_draw = []

        draw_board(screen)

        if last_move is not None:
            highlight_square(screen, last_move[0], COLOR_LAST_MOVE)
            highlight_square(screen, last_move[1], COLOR_LAST_MOVE)

        if selected_square is not None:
            highlight_square(screen, selected_square, COLOR_SELECTED)
        if legal_moves_to_draw:
            draw_legal_moves(screen, legal_moves_to_draw)

        draw_pieces(screen, user_api.board)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
