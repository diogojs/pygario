import sys
import contextlib

with contextlib.redirect_stdout(None):
    import pygame

from random import randint
from typing import List

from pygario.blob import Blob
from pygario.cell import Cell
from pygario.color import Color
from pygario.constants import *
from pygario.viewport import Viewport
from pygario.vector import Vector2D


def setup_pygame() -> pygame.Surface:
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Blobs.io")
    return window


def main():
    HOST = "localhost"
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    
    window = setup_pygame()
    clock = pygame.time.Clock()
    player = Blob(0, Vector2D(INITIAL_RADIUS, INITIAL_RADIUS), INITIAL_RADIUS, Color.BLUE)

    map_grid: List[List[Cell]] = list()
    for i in range(GRID_COLS * GRID_ROWS):
        map_grid.append(list())

    blobs: List[Blob] = list()

    # initialize map
    for i in range(NUMBER_OF_CELLS):
        p = Vector2D(randint(0, MAP_WIDTH-1), randint(0, MAP_HEIGHT-1))
        r, g, b = randint(0, 6)*40, randint(0, 6)*40, randint(0, 6)*40
        new_cell = Cell(i+1, p, CELL_RADIUS, (r, g, b))
        grid_col = p.x // GRID_SIZE
        grid_row = p.y // GRID_SIZE
        map_grid[grid_col + grid_row * GRID_COLS].append(new_cell)
    
    is_running = True
    deltatime = 0
    while is_running:
        deltatime = clock.tick(144)

        # handle mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
            
            elif event.type == pygame.MOUSEMOTION:
                Mouse.x = event.pos[0]
                Mouse.y = event.pos[1]
        
        # update objects
        game_update(player, map_grid, blobs, deltatime)

        # draw objects
        game_draw(window, player, map_grid, blobs)
    
    pygame.quit()


def game_draw(window, player: Blob, map_grid: List[List[Cell]], blobs: List[Blob]):
    window.fill(Color.WHITE.value)
    viewport = Viewport(Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) - player.pos, player.radius)

    map_edges = pygame.draw.rect(window, Color.BLACK.value, (viewport.center.x, viewport.center.y, MAP_WIDTH, MAP_HEIGHT), 1)

    for grid_cell in map_grid:
        for cell in grid_cell:
            cell.draw(window, viewport)

    for obj in blobs:
        obj.draw(window, viewport)

    player.draw(window, viewport)

    # update window
    pygame.display.update()

def game_update(player: Blob, map_grid: List[List[Cell]], blobs: List[Blob], deltatime: float):
    for grid_cell in map_grid:
        for cell in grid_cell:
            cell.update(deltatime)

    for obj in blobs:
        obj.update(deltatime)

    player.update(deltatime)
        

main()