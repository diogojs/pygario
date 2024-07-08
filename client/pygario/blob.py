from typing import List
from pygario.cell import Cell
from pygario.vector import Vector2D

from pygario.constants import *


class Blob(Cell):
    def move(self, dx: float, dy: float):
        self.pos.add(Vector2D(dx, dy))
    
    def move(self, dist: Vector2D):
        self.pos.add(dist)
    
    def update(self, deltatime: int):
        from pygario.game import Game
        dist = Game.Mouse - Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        if (dist.magnitude() < INITIAL_RADIUS/4):
            return
        
        dist.set_magnitude(INITIAL_SPEED)
        self.move(dist)
        self._keep_inside_map()

        self.check_collisions(Game.map_grid)
    
    def check_collisions(self, cells_grid: List[List[Cell]]):
        import math
        # grid_col = self.pos.x // GRID_SIZE
        # grid_row = self.pos.y // GRID_SIZE
        # range_col = (grid_col - self.radius // GRID_SIZE, grid_col + self.radius // GRID_SIZE)
        # range_row    = (grid_row - self.radius // GRID_SIZE, grid_row + self.radius // GRID_SIZE)

        for grid_cell in cells_grid:
            for cell in grid_cell:
                dist = (self.pos - cell.pos).magnitude()
                if dist < self.radius:
                    # cell.enabled = False
                    self.radius = math.sqrt(self.radius**2 + cell.radius**2)
                    grid_cell.remove(cell)

    def _keep_inside_map(self):
        if self.pos.x < self.radius:
            self.pos.x = self.radius
        if self.pos.y < self.radius:
            self.pos.y = self.radius
        
        if self.pos.x + self.radius > MAP_WIDTH:
            self.pos.x = MAP_WIDTH - self.radius
        if self.pos.y + self.radius > MAP_HEIGHT:
            self.pos.y = MAP_HEIGHT - self.radius