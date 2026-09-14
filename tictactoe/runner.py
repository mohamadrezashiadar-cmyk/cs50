import pygame
import sys
import time
import math

import tictactoe as ttt

pygame.init()
size = width, height = 700, 640
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

BG_TOP = (18, 16, 40)
BG_BOTTOM = (40, 18, 55)
TILE = (34, 32, 58)
TILE_HOVER = (48, 45, 80)
WHITE = (240, 240, 245)
GRAY = (150, 148, 165)
BLUE = (99, 179, 255)
PINK = (255, 110, 160)
GREEN = (120, 235, 170)
GOLD = (255, 205, 110)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 26)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 42)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
smallFont = pygame.font.Font("OpenSans-Regular.ttf", 18)

background = pygame.Surface(size)
for y in range(height):
    t = y / height
    color = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
    pygame.draw.line(background, color, (0, y), (width, y))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def glow_text(surface, text, font, color, center, glow_radius=8):
    base = font.render(text, True, color)
    glow = pygame.Surface((base.get_width() + glow_radius * 4, base.get_height() + glow_radius * 4), pygame.SRCALPHA)
    for r in range(glow_radius, 0, -2):
        alpha = max(10, 60 - r * 6)
        layer = font.render(text, True, (*color, alpha))
        for dx in (-r, 0, r):
            for dy in (-r, 0, r):
                glow.blit(layer, (glow_radius * 2 + dx - base.get_width() / 2 + glow.get_width() / 2 - base.get_width() / 2,
                                   glow_radius * 2 + dy), special_flags=pygame.BLEND_RGBA_ADD)
    rect = base.get_rect(center=center)
    surface.blit(base, rect)


def draw_button(rect, text, font, hover=False, accent=WHITE):
    base_color = TILE_HOVER if hover else TILE
    pygame.draw.rect(screen, base_color, rect, border_radius=14)
    pygame.draw.rect(screen, accent if hover else GRAY, rect, 2, border_radius=14)
    label = font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_symbol(surface, symbol, center, size_px, progress, color):
    scale = min(1.0, progress)
    eased = 1 - (1 - scale) ** 3
    r = int(size_px * eased)
    if r <= 0:
        return
    if symbol == ttt.X:
        offset = int(r * 0.6)
        width_line = max(4, int(r * 0.14))
        pygame.draw.line(surface, color, (center[0] - offset, center[1] - offset),
                          (center[0] + offset, center[1] + offset), width_line)
        pygame.draw.line(surface, color, (center[0] + offset, center[1] - offset),
                          (center[0] - offset, center[1] + offset), width_line)
    else:
        width_line = max(4, int(r * 0.16))
        pygame.draw.circle(surface, color, center, int(r * 0.7), width_line)


def winning_line(board):
    lines = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
             [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
             [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
    for line in lines:
        values = [board[i][j] for i, j in line]
        if values[0] is not None and values[0] == values[1] == values[2]:
            return line
    return None


MENU, VS_SELECT, LOCAL_CHOOSE, PLAYING = range(4)

state = MENU
mode = None
user = None
board = ttt.initial_state()
ai_turn = False
scores = {ttt.X: 0, ttt.O: 0, "TIE": 0}
game_recorded = False
move_times = {}

while True:

    dt_now = time.time()
    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True

    screen.blit(background, (0, 0))

    if state == MENU:

        glow_text(screen, "TIC · TAC · TOE", largeFont, BLUE, (width / 2, 130), 6)

        botButton = pygame.Rect(width / 2 - 150, height / 2 - 40, 300, 60)
        humanButton = pygame.Rect(width / 2 - 150, height / 2 + 40, 300, 60)

        pulse = (math.sin(dt_now * 3) + 1) / 2
        draw_button(botButton, "Play vs Computer", mediumFont,
                    botButton.collidepoint(mouse_pos), lerp(GRAY, BLUE, pulse))
        draw_button(humanButton, "Play vs Human", mediumFont,
                    humanButton.collidepoint(mouse_pos), lerp(GRAY, PINK, pulse))

        if clicked:
            if botButton.collidepoint(mouse_pos):
                mode = "bot"
                state = LOCAL_CHOOSE
            elif humanButton.collidepoint(mouse_pos):
                mode = "human"
                board = ttt.initial_state()
                move_times = {}
                game_recorded = False
                state = PLAYING

    elif state == LOCAL_CHOOSE:

        glow_text(screen, "Choose your side", largeFont, WHITE, (width / 2, 130), 4)

        playXButton = pygame.Rect(width / 2 - 220, height / 2, 190, 60)
        playOButton = pygame.Rect(width / 2 + 30, height / 2, 190, 60)

        draw_button(playXButton, "Play as X", mediumFont, playXButton.collidepoint(mouse_pos), BLUE)
        draw_button(playOButton, "Play as O", mediumFont, playOButton.collidepoint(mouse_pos), PINK)

        if clicked:
            if playXButton.collidepoint(mouse_pos):
                user = ttt.X
                board = ttt.initial_state()
                move_times = {}
                ai_turn = False
                game_recorded = False
                state = PLAYING
            elif playOButton.collidepoint(mouse_pos):
                user = ttt.O
                board = ttt.initial_state()
                move_times = {}
                ai_turn = False
                game_recorded = False
                state = PLAYING

    elif state == PLAYING:

        tile_size = 110
        tile_gap = 12
        board_size = tile_size * 3 + tile_gap * 2
        origin_x = width / 2 - board_size / 2
        origin_y = 150

        game_over = ttt.terminal(board)
        current_player = ttt.player(board)

        if game_over and not game_recorded:
            winner = ttt.winner(board)
            scores["TIE" if winner is None else winner] += 1
            game_recorded = True

        is_local_turn = (mode == "human") or (mode == "bot" and current_player == user)

        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    origin_x + j * (tile_size + tile_gap),
                    origin_y + i * (tile_size + tile_gap),
                    tile_size, tile_size
                )

                can_click = board[i][j] == ttt.EMPTY and not game_over and is_local_turn
                base_color = TILE
                if can_click and rect.collidepoint(mouse_pos):
                    glow = (math.sin(dt_now * 6) + 1) / 2
                    base_color = lerp(TILE_HOVER, (60, 55, 100), glow)

                shadow_rect = rect.move(0, 5)
                pygame.draw.rect(screen, (10, 8, 22), shadow_rect, border_radius=18)
                pygame.draw.rect(screen, base_color, rect, border_radius=18)

                symbol = board[i][j]
                if symbol is not None:
                    key = (i, j)
                    if key not in move_times:
                        move_times[key] = dt_now
                    progress = (dt_now - move_times[key]) / 0.25
                    color = BLUE if symbol == ttt.X else PINK
                    draw_symbol(screen, symbol, rect.center, tile_size / 2, progress, color)

                row.append(rect)
            tiles.append(row)

        win_line = winning_line(board) if game_over else None
        if win_line:
            (i1, j1), _, (i3, j3) = win_line
            p1 = tiles[i1][j1].center
            p2 = tiles[i3][j3].center
            for width_glow, alpha_color in [(14, (255, 205, 110)), (6, GOLD)]:
                pygame.draw.line(screen, alpha_color, p1, p2, width_glow)

        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title_text, title_color = "It's a tie!", WHITE
            elif mode == "bot":
                title_text, title_color = ("You win!" if winner == user else f"{winner} wins!"), (
                    GREEN if winner == user else PINK)
            else:
                title_text, title_color = f"{winner} wins!", (BLUE if winner == ttt.X else PINK)
        elif mode == "bot":
            title_text, title_color = ("Your turn" if current_player == user else "Computer thinking"), (
                WHITE if current_player == user else GRAY)
        else:
            title_text, title_color = f"{current_player}'s turn", (BLUE if current_player == ttt.X else PINK)

        glow_text(screen, title_text, largeFont, title_color, (width / 2, 70), 6)

        score_text = f"X  {scores[ttt.X]}      O  {scores[ttt.O]}      Ties  {scores['TIE']}"
        score_surface = smallFont.render(score_text, True, GRAY)
        screen.blit(score_surface, score_surface.get_rect(center=(width / 2, height - 15)))

        if mode == "bot" and not game_over and current_player != user:
            if ai_turn:
                time.sleep(0.4)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        if clicked and is_local_turn and not game_over:
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse_pos):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 2 - 100, height - 120, 200, 45)
            menuButton = pygame.Rect(width / 2 - 100, height - 65, 200, 32)
            draw_button(againButton, "Play Again", mediumFont, againButton.collidepoint(mouse_pos), GOLD)
            menu_label = smallFont.render("Back to Menu", True, GRAY if not menuButton.collidepoint(mouse_pos) else WHITE)
            screen.blit(menu_label, menu_label.get_rect(center=menuButton.center))

            if clicked and againButton.collidepoint(mouse_pos):
                board = ttt.initial_state()
                move_times = {}
                ai_turn = False
                game_recorded = False
            elif clicked and menuButton.collidepoint(mouse_pos):
                state = MENU
                mode = None
                user = None
                board = ttt.initial_state()
                move_times = {}
                ai_turn = False
                game_recorded = False

    pygame.display.flip()
    clock.tick(60)
