import sys
import contextlib

from pygario.blob import Blob
from pygario.scenes.scene import Scene

with contextlib.redirect_stdout(None):
    import pygame

from typing import List

from pygario.player import Player
from pygario.cell import Cell
from pygario.color import Color
from pygario.constants import *
from pygario.viewport import Viewport
from pygario.vector import Vector2D


class MainScene(Scene):
    player: Player
    blobs_grid: List[List[Blob]] = list()
    map_grid: List[List[Cell]] = list()

    def __init__(self):
        self.initialize()

    def initialize(self):
        """
        Create Game main variables (player, map, cells/blobs)
        """
        from pygario.game import Game

        Game.client.connect("Diogo")
        cmd, data = Game.client.get_data()

        if cmd == 'update':
            player_blob, cells, blobs = Game.client.deserialize(data)

        # initial_pos = Vector2D(INITIAL_RADIUS, INITIAL_RADIUS)
        self.player = Player(
            player_blob.id,
            player_blob.pos,
            player_blob.radius,
            player_blob.color,
            player_blob.name
            )
        MainScene.map_grid = cells
        MainScene.blobs_grid = blobs

        self.viewport = Viewport(self.player.pos, self.player.radius)
        self.font = pygame.font.SysFont("comicsans", 12)

    def draw(self, window: pygame.Surface, deltatime: float):
        window.fill(Color.WHITE.value)

        borders_up_left = (-self.viewport.up_left.x, -self.viewport.up_left.y)
        borders_up_left = (borders_up_left[0]/self.viewport.scale, borders_up_left[1]/self.viewport.scale)
        borders_size = (MAP_WIDTH/self.viewport.scale, MAP_HEIGHT/self.viewport.scale)
        map_borders = pygame.draw.rect(window, Color.BLACK.value, (borders_up_left, borders_size), 1)

        for grid_cell in MainScene.map_grid:
            for cell in grid_cell:
                cell.draw(window, self.viewport)

        for grid_cell in MainScene.blobs_grid:
            for obj in grid_cell:
                obj.draw(window, self.viewport)

        self.player.draw(window, self.viewport)

        # debug info
        txt = self.font.render(f"deltatime: {deltatime}\nFPS: {1000/deltatime}", True, Color.BLACK.value)
        position_in_viewport = (10, 10)
        window.blit(txt, position_in_viewport)

        # update window
        pygame.display.update()

    def update(self, deltatime: float):
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
        from pygario.game import Game

        cmd, data = Game.client.get_data()
        if cmd == 'update':
            player_blob, cells, blobs = Game.client.deserialize(data)

        MainScene.map_grid = cells
        MainScene.blobs_grid = blobs
    
    def _find_cell_in_map(self, id: int, grid_cell: List[Cell]) -> int:
        for i in range(len(grid_cell)):
            if grid_cell[i].id == id:
                return i
        return -1