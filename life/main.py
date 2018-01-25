import pygame
from pygame import Color
import os
from life.grid_operations import *
from life.patterns import insert_pattern_into_grid
from life.rle_importer import import_rle

import easygui


GRID_LINES_COLOR = "#ccd1d1"
FONT_COLOR = "#17202a"  # "#424949"
CELL_COLOR = "#17202a"
CURSOR_COLOR = "#3498db"
PATTERN_COLOR = "#2ecc71"
PATTERN_BOX_COLOR = "#e74c3c"
BOX_COLOR = FONT_COLOR

W = H = GRID_CELLS = 2000
MARGIN = 20
LEGEND_SIZE = 300
FPS = 10
FPS_MIN = 1
FPS_MAX = 20
FONT_SIZE = 18
FONT_LINE_SPACING = 1.15

GAME_INFO_PLAY = """THE GAME OF LIFE

P - PLAY / PAUSE
C - CLEAR GRID
R - RANDOM GRID
L - GRID LINES
D - DEBUG
ESC / Q - QUIT
ARROW UP - FASTER
ARROW DOWN - SLOWER"""
GAME_INFO_PAUSE = """THE GAME OF LIFE

P - PLAY / PAUSE
C - CLEAR GRID
R - RANDOM GRID
I - IMPORT PATTERN
L - GRID LINES
D - DEBUG
ESC / Q - QUIT
ARROW UP - FASTER
ARROW DOWN - SLOWER
LEFT MOUSE - DRAW
   / INSERT PATTERN
RIGHT MOUSE - ERASE
   / CANCEL PATTERN"""


def draw_grid(surf, grid, cell_size):
    """Draw actual grid on surface"""
    for i in range(H):
        for j in range(W):
            if grid[i, j] == 1:
                pygame.draw.rect(surf, pygame.Color(CELL_COLOR),
                                 (j * cell_size,
                                  i * cell_size,
                                  cell_size, cell_size))


def draw_pattern(surf, pattern, position, cell_size):
    """Draw pattern preview on surface"""
    # x, y = position
    x_grid, y_grid = mouse_to_grid_position(position, cell_size)
    h, w = pattern.shape
    for i in range(h):
        for j in range(w):
            if pattern[i, j] == 1:
                pygame.draw.rect(surf, pygame.Color(PATTERN_COLOR),
                                 (j * cell_size + x_grid * cell_size,
                                  i * cell_size + y_grid * cell_size,
                                  cell_size, cell_size))
    pygame.draw.rect(surf, pygame.Color(PATTERN_BOX_COLOR),
                     (x_grid * cell_size, y_grid * cell_size,
                      w * cell_size, h * cell_size), 1)



def draw_grid_lines(surf, cell_size):
    """Draw lines separating grid cells on surface"""
    for i in range(H + 1):
        for j in range(W + 1):
            pygame.draw.line(surf, pygame.Color(GRID_LINES_COLOR),
                             (j * cell_size, 0),
                             (j * cell_size, H * cell_size))

            pygame.draw.line(surf, pygame.Color(GRID_LINES_COLOR),
                             (0, i * cell_size),
                             (W * cell_size, i * cell_size))


def draw_game_info_area(surf, size):
    # main rect
    pygame.draw.rect(surf, pygame.Color(BOX_COLOR),
                     (size + 0.5 * MARGIN, 0, LEGEND_SIZE - 0.5 * MARGIN, size), 2)
    # upper line
    pygame.draw.line(surf, pygame.Color(BOX_COLOR),
                     (size + 0.5 * MARGIN, MARGIN + 1.5 * FONT_SIZE * FONT_LINE_SPACING),
                     (size + LEGEND_SIZE,  MARGIN + 1.5 * FONT_SIZE * FONT_LINE_SPACING), 2)

    # pygame.draw.line(surf, pygame.Color(BOX_COLOR),
    #                  (size + 0.5 * MARGIN, MARGIN + 15.5 * FONT_SIZE * FONT_LINE_SPACING),
    #                  (size + LEGEND_SIZE, MARGIN + 15.5 * FONT_SIZE * FONT_LINE_SPACING), 2)
    #lower line
    pygame.draw.line(surf, pygame.Color(BOX_COLOR),
                     (size + 0.5 * MARGIN, size - 11.5 * FONT_SIZE * FONT_LINE_SPACING - MARGIN),
                     (size + LEGEND_SIZE, size - 11.5 * FONT_SIZE * FONT_LINE_SPACING - MARGIN), 2)


def display_game_info(surf, font, size, play):
    """Blits game info text on surface"""
    # TODO: height shouldn't be const
    game_info = GAME_INFO_PLAY if play else GAME_INFO_PAUSE
    for i, line in enumerate(game_info.splitlines()):
        surf.blit(font.render(line, 1, Color(FONT_COLOR)), (size + 1.5 * MARGIN, MARGIN + i * FONT_SIZE * FONT_LINE_SPACING))

# TODO: do usuniecia (przeniesione do debug)
# def display_fps(surf, font, fps, size):
#     surf.blit(font.render("FPS: {}".format(fps), 1, Color(FONT_COLOR)), (size + MARGIN, size - 2 * FONT_SIZE))


def display_debug(surf, font, debug_info, size):
    i = 0
    len_debug_info = len(debug_info)
    for key, val in debug_info.items():
        surf.blit(font.render("{} - {}".format(key, val), 1, Color(FONT_COLOR)),
                  (size + 1.5 * MARGIN, size - (len_debug_info - i + 0.5) * FONT_SIZE * FONT_LINE_SPACING - MARGIN))
        i += 1

    grid_position = mouse_to_grid_position(debug_info["POSITION"], debug_info["CELL_SIZE"])
    surf.blit(font.render("GRID POSITION - {}".format(grid_position), 1, Color(FONT_COLOR)),
              (size + 1.5 * MARGIN, size - (len_debug_info - i + 0.5) * FONT_SIZE * FONT_LINE_SPACING - MARGIN))


def draw_cell_at_cursor(surf, position, cell_size):
    x, y = position
    pygame.draw.rect(surf, pygame.Color(CURSOR_COLOR),
                     (int(x / cell_size) * cell_size,
                      int(y / cell_size) * cell_size,
                      cell_size, cell_size))


def add_cell(grid, position, cell_size):
    x_grid, y_grid = mouse_to_grid_position(position, cell_size)
    grid[y_grid, x_grid] = 1  # y, x order


def erase_cell(grid, position, cell_size):
    x_grid, y_grid = mouse_to_grid_position(position, cell_size)
    grid[y_grid , x_grid] = 0


def is_point_on_grid(position, cell_size):
    x, y = position
    if 0 < x <= W * cell_size and 0 < y <= H * cell_size:
        return True
    else:
        return False


def is_pattern_on_grid(grid, pattern, position, cell_size):
    x, y = position
    h, w = pattern.shape
    x2, y2 = x + (w - 1) * cell_size, y + (h - 1) * cell_size
    # check two nodes of bbox
    if is_point_on_grid(position, cell_size) and is_point_on_grid((x2, y2), cell_size):
        return True
    else:
        return False


def main():
    # PyGame initialization
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # centers window, must be before pygame.init()!
    pygame.init()  # initialize pygame
    font = pygame.font.SysFont("consolas", FONT_SIZE)
    clock = pygame.time.Clock()
    fps = FPS

    # determining surface size, etc.
    display_info = pygame.display.Info()  # create a video display information object
    screen_min_size = (display_info.current_w if display_info.current_w < display_info.current_h else display_info.current_h) * 0.88
    cell_size = int(screen_min_size / GRID_CELLS)
    size = cell_size * GRID_CELLS
    surface_size = (size + LEGEND_SIZE, size)
    surface = pygame.display.set_mode(surface_size)
    pygame.display.set_caption('The Game Of Life')

    cell_size = int(size / (H if H > W else W))

    grid_now = create_empty_grid(W, H)

    # game loop variables
    running = True
    play = False
    debug = False
    show_grid_lines = True if GRID_CELLS <= 100 else False
    pattern_imported = False
    # left_button_pressed = False
    # grid_is_empty = is_empty(grid_now)
    iteration = 1
    # mouse_x, mouse_y = 0, 0
    position = (0, 0)
    while running:
        # keep loop running at the right speed
        clock.tick(fps)
        iteration += 1
        pygame.display.set_caption("The Game Of Life [iteration: {} fps: {:.1f}]".format(iteration, clock.get_fps()))

        # grid_is_empty = is_empty(grid_now)

        # PROCESS INPUT (EVENTS)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    play = not play
                    pattern_imported = False
                elif event.key == pygame.K_l:
                    show_grid_lines = not show_grid_lines
                elif event.key == pygame.K_c:
                    clear_grid(grid_now)
                elif event.key == pygame.K_r:
                    grid_now = create_random_grid(W, H)
                    # grid_is_empty = False
                elif event.key == pygame.K_d:
                    debug = not debug
                elif event.key == pygame.K_i and not play:
                    pattern_file = easygui.fileopenbox(
                        msg="chose pattern file",
                        title="Open file",
                        default="*.rle")
                    # filetypes=["*.rle"])
                    if pattern_file is not None:
                        pattern = import_rle(pattern_file)
                        h, w = pattern.shape
                        if 0 < h <= H and 0 < w <= W:
                            pattern_imported = True
                        else:
                            easygui.msgbox("Pattern shape ({}x{}) is too big for this grid ({}x{})".format(h, w, H, W),
                                           "Warning!")
                elif event.key == pygame.K_DOWN:
                    fps = fps - 1 if fps > FPS_MIN else FPS_MIN
                elif event.key == pygame.K_UP:
                    fps = fps + 1 if fps < FPS_MAX else FPS_MAX
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not play:
                    if (pattern_imported and
                            is_pattern_on_grid(grid_now, pattern, event.pos, cell_size)):
                        if event.button == 1:  # LEFT=1
                            insert_pattern_into_grid(pattern, grid_now, mouse_to_grid_position(event.pos, cell_size))
                        elif event.button == 3:  # RIGHT=3
                            pattern_imported = False

                    elif is_point_on_grid(event.pos, cell_size):
                        if event.button == 1:  # LEFT=1
                            add_cell(grid_now, event.pos, cell_size)
                        elif event.button == 3:  # RIGHT=3
                            erase_cell(grid_now, event.pos, cell_size)

            elif event.type == pygame.MOUSEMOTION:  # Detected mouse motion
                position = event.pos  # set mouse positions to the new position
                if not play:
                    print()
                    if is_point_on_grid(event.pos, cell_size):
                        if pygame.mouse.get_pressed()[0] == 1:
                            add_cell(grid_now, event.pos, cell_size)
                        elif pygame.mouse.get_pressed()[2] == 1:
                            erase_cell(grid_now, event.pos, cell_size)

        # UPDATE
        if play:
            grid_now = update_grid(grid_now, H, W)

        # DRAW / RENDER
        surface.fill(Color('white'))
        draw_game_info_area(surface, size)
        display_game_info(surface, font, size, play)
        # display_fps(surface, font, fps, size)
        if debug:
            # debug_info = (running, play, debug, show_grid_lines, pattern_imported, position, size, cell_size)
            debug_info = {
                "FPS": fps,
                "RUNNING": running,
                "PLAY": play,
                "DEBUG": debug,
                "SHOW_GRID_LINES": show_grid_lines,
                "PATTERN_IMPORTED": pattern_imported,
                "GRID_SIZE": (H, W),
                "CELL_SIZE": cell_size,
                "SIZE": size,
                "POSITION": position}

            display_debug(surface, font, debug_info, size)

        draw_grid(surface, grid_now, cell_size)

        if show_grid_lines:
            draw_grid_lines(surface, cell_size)

        # pause mode
        if not play:
            if pattern_imported and is_pattern_on_grid(grid_now, pattern, position, cell_size):
                draw_pattern(surface, pattern, position, cell_size)
            elif is_point_on_grid(position, cell_size):
                draw_cell_at_cursor(surface, position, cell_size)


        # *after* drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
