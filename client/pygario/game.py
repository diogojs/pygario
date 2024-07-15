import sys
import contextlib

from pygario.blob import Blob
from pygario.client import Client

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
    client: Client = None

    @staticmethod
    def setup_pygame() -> pygame.Surface:
        pygame.init()
        pygame.font.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Blobs.io")
        return window

    def run(self):
        host = "localhost"
        if len(sys.argv) > 1:
            host = sys.argv[1]
        Game.client = Client(host, PORT)

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
                Game.Mouse.x = event.pos[0]
                Game.Mouse.y = event.pos[1]

    def initialize(self):
        """
        Create Game main variables (player, map, cells/blobs)
        """
        self.client.connect("Diogo")
        cmd, data = self.client.get_data()

        if cmd == 'update':
            player_blob, cells, blobs = self.client.deserialize(data)

        # initial_pos = Vector2D(INITIAL_RADIUS, INITIAL_RADIUS)
        self.player = Player(
            player_blob.id,
            player_blob.pos,
            player_blob.radius,
            player_blob.color,
            player_blob.name
            )
        Game.map_grid = cells
        Game.blobs_grid = blobs

        self.is_running = True
        self.viewport = Viewport(self.player.pos, self.player.radius)
        self.font = pygame.font.SysFont("comicsans", 12)

    def game_draw(self, deltatime: float):
        self.window.fill(Color.WHITE.value)

        borders_up_left = (-self.viewport.up_left.x, -self.viewport.up_left.y)
        borders_up_left = (borders_up_left[0]/self.viewport.scale, borders_up_left[1]/self.viewport.scale)
        borders_size = (MAP_WIDTH/self.viewport.scale, MAP_HEIGHT/self.viewport.scale)
        map_borders = pygame.draw.rect(self.window, Color.BLACK.value, (borders_up_left, borders_size), 1)

        for grid_cell in Game.map_grid:
            for cell in grid_cell:
                cell.draw(self.window, self.viewport)

        for grid_cell in Game.blobs_grid:
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
        self.update_map()

        for grid_cell in self.map_grid:
            for cell in grid_cell:
                cell.update(deltatime)

        for grid_cell in self.blobs_grid:
            for obj in grid_cell:
                obj.update(deltatime)

        self.player.update(deltatime)
        self.viewport.update(self.player.pos, self.player.radius)

    def update_map(self):
        cmd, data = self.client.get_data()
        if cmd == 'update':
            player_blob, cells, blobs = self.client.deserialize(data)

        Game.map_grid = cells
        Game.blobs_grid = blobs
    
    def _find_cell_in_map(self, id: int, grid_cell: List[Cell]) -> int:
        for i in range(len(grid_cell)):
            if grid_cell[i].id == id:
                return i
        return -1