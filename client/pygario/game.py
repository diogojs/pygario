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


class Game:
    Mouse = Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    player: Blob
    blobs: List[Blob] = list()
    map_grid: List[List[Cell]] = list()

    @staticmethod
    def setup_pygame() -> pygame.Surface:
        pygame.init()
        pygame.font.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Blobs.io")
        return window

    def run(self):
        HOST = "localhost"
        if len(sys.argv) > 1:
            HOST = sys.argv[1]
        
        self.window = self.setup_pygame()
        clock = pygame.time.Clock()

        self.initialize()
        
        deltatime = 0
        while self.is_running:
            deltatime = clock.tick(144)

            # handle mouse events
            self.handle_events()
            
            # update objects
            self.game_update(deltatime)

            # draw objects
            self.game_draw()
        
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                
            elif event.type == pygame.MOUSEMOTION:
                self.__class__.Mouse.x = event.pos[0]
                self.__class__.Mouse.y = event.pos[1]

    def initialize(self):
        """
        Create Game main variables (player, map, cells/blobs)
        """
        self.player = Blob(0, Vector2D(INITIAL_RADIUS, INITIAL_RADIUS), INITIAL_RADIUS, Color.BLUE)
        for i in range(GRID_COLS * GRID_ROWS):
            self.map_grid.append(list())

        # initialize map grid
        for i in range(NUMBER_OF_CELLS):
            p = Vector2D(randint(0, MAP_WIDTH-1), randint(0, MAP_HEIGHT-1))
            r, g, b = randint(0, 6)*40, randint(0, 6)*40, randint(0, 6)*40
            new_cell = Cell(i+1, p, CELL_RADIUS, (r, g, b))
            grid_col = p.x // GRID_SIZE
            grid_row = p.y // GRID_SIZE
            self.map_grid[grid_col + grid_row * GRID_COLS].append(new_cell)

        self.is_running = True

    def game_draw(self):
        self.window.fill(Color.WHITE.value)
        viewport = Viewport(Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) - self.player.pos, self.player.radius)

        map_edges = pygame.draw.rect(self.window, Color.BLACK.value, (viewport.center.x, viewport.center.y, MAP_WIDTH, MAP_HEIGHT), 1)

        for grid_cell in self.map_grid:
            for cell in grid_cell:
                cell.draw(self.window, viewport)

        for obj in self.blobs:
            obj.draw(self.window, viewport)

        self.player.draw(self.window, viewport)

        # update window
        pygame.display.update()

    def game_update(self, deltatime: float):
        for grid_cell in self.map_grid:
            for cell in grid_cell:
                cell.update(deltatime)

        for obj in self.blobs:
            obj.update(deltatime)

        self.player.update(deltatime)
