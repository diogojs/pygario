import sys
import contextlib

from pygario.blob import Blob

with contextlib.redirect_stdout(None):
    import pygame

from random import randint
from typing import List

from pygario.player import Player
from pygario.cell import Cell
from pygario.color import Color
from pygario.constants import *
from pygario.viewport import Viewport
from pygario.vector import Vector2D


class Game:
    Mouse = Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    player: Player
    blobs_grid: List[List[Blob]] = list()
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
            self.game_draw(deltatime)
        
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_PAGEUP:
                    self.player.radius = self.player.radius*2
                
            elif event.type == pygame.MOUSEMOTION:
                self.__class__.Mouse.x = event.pos[0]
                self.__class__.Mouse.y = event.pos[1]

    def initialize(self):
        """
        Create Game main variables (player, map, cells/blobs)
        """
        # initial_pos = Vector2D(randint(INITIAL_RADIUS, MAP_WIDTH-INITIAL_RADIUS), randint(INITIAL_RADIUS, MAP_HEIGHT-INITIAL_RADIUS))
        initial_pos = Vector2D(INITIAL_RADIUS, INITIAL_RADIUS)
        self.player = Player(0, initial_pos, INITIAL_RADIUS, Color.BLUE, "Player1")
        self.viewport = Viewport(self.player.pos, self.player.radius)
        for i in range(GRID_COLS * GRID_ROWS):
            self.map_grid.append(list())
            self.blobs_grid.append(list())

        # initialize map grid
        for i in range(NUMBER_OF_CELLS):
            p = Vector2D(randint(0, MAP_WIDTH-1), randint(0, MAP_HEIGHT-1))
            r, g, b = randint(0, 6)*40, randint(0, 6)*40, randint(0, 6)*40
            new_cell = Cell(i+1, p, CELL_RADIUS, (r, g, b))
            grid_col = p.x // GRID_SIZE
            grid_row = p.y // GRID_SIZE
            self.map_grid[grid_col + grid_row * GRID_COLS].append(new_cell)
        
        b = Blob(123456, Vector2D(100, 100), 30, (200, 50, 50), "mari")
        grid_col = b.pos.x // GRID_SIZE
        grid_row = b.pos.y // GRID_SIZE
        self.blobs_grid[grid_col + grid_row * GRID_COLS].append(b)
        for i in range(NUMBER_OF_CELLS, NUMBER_OF_CELLS+10):
            p = Vector2D(randint(0, MAP_WIDTH-1), randint(0, MAP_HEIGHT-1))
            r, g, b = randint(0, 6)*40, randint(0, 6)*40, randint(0, 6)*40
            new_cell = Blob(i+1, p, CELL_RADIUS*randint(5, 10), (r, g, b), f"joana{i}")
            grid_col = p.x // GRID_SIZE
            grid_row = p.y // GRID_SIZE
            self.blobs_grid[grid_col + grid_row * GRID_COLS].append(new_cell)

        self.is_running = True
        self.font = pygame.font.SysFont("comicsans", 12)

    def game_draw(self, deltatime: float):
        self.window.fill(Color.WHITE.value)

        borders_up_left = (-self.viewport.up_left.x, -self.viewport.up_left.y)
        borders_up_left = (borders_up_left[0]/self.viewport.scale, borders_up_left[1]/self.viewport.scale)
        borders_size = (MAP_WIDTH/self.viewport.scale, MAP_HEIGHT/self.viewport.scale)
        map_borders = pygame.draw.rect(self.window, Color.BLACK.value, (borders_up_left, borders_size), 1)

        for grid_cell in self.map_grid:
            for cell in grid_cell:
                cell.draw(self.window, self.viewport)

        for grid_cell in self.blobs_grid:
            for obj in grid_cell:
                obj.draw(self.window, self.viewport)

        self.player.draw(self.window, self.viewport)

        # debug info
        txt = self.font.render(f"deltatime: {deltatime}\nFPS: {1000/deltatime}", True, Color.BLACK.value)
        position_in_viewport = (10, 10)
        self.window.blit(txt, position_in_viewport)

        # update window
        pygame.display.update()

    def game_update(self, deltatime: float):
        for grid_cell in self.map_grid:
            for cell in grid_cell:
                cell.update(deltatime)

        for grid_cell in self.blobs_grid:
            for obj in grid_cell:
                obj.update(deltatime)

        self.player.update(deltatime)
        self.viewport.update(self.player.pos, self.player.radius)
