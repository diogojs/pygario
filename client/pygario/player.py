from dataclasses import dataclass
from typing import List
from pygario.blob import Blob
from pygario.cell import Cell
from pygario.vector import Vector2D

from pygario.constants import *


@dataclass
class Player(Blob):
    def move(self, dx: float, dy: float):
        self.pos.add(Vector2D(dx, dy))
    
    def move(self, dist: Vector2D):
        self.pos.add(dist)
    
    def update(self, deltatime: int):
        from pygario.game import Game
        from pygario.scenes.main_scene import MainScene

        self.eaten = []

        dist = Game.Mouse - Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        if (dist.magnitude() < INITIAL_RADIUS/4):
            return
        
        dist.set_magnitude(INITIAL_SPEED)
        self.move(dist)
        self._keep_inside_map()

        self.check_collisions(MainScene.map_grid)
        self.check_collisions(MainScene.blobs_grid)

        self.update_server()


    def update_server(self):
        from pygario.game import Game

        if len(self.eaten) > 0:
            # {other_id: int, x: float, y: float, radius: float, velocity: vector2d} 
            data = f"eat;{self.pos.x:.6},{self.pos.y:.6},{self.radius:.6},"
            for eat in self.eaten:
                data += f"{eat.id},"
            Game.client.send(data.encode())
        else:
            data = f"move;{self.pos.x:.6},{self.pos.y:.6},{self.radius:.6}"
            Game.client.send(data.encode())
    
    def check_collisions(self, cells_grid: List[List[Cell]]):
        import math

        grid_col = self.pos.x // GRID_SIZE
        grid_row = self.pos.y // GRID_SIZE
        range_col = (int(grid_col - self.radius / GRID_SIZE), int((grid_col + self.radius / GRID_SIZE + 1)))
        range_row = (int(grid_row - self.radius / GRID_SIZE), int((grid_row + self.radius / GRID_SIZE + 1)))

        for i, grid_cell in enumerate(cells_grid):
            col = i % GRID_COLS
            row = i // GRID_COLS
            if (col >= range_col[0] and col <= range_col[1]
                and row >= range_row[0] and row <= range_row[1]):
                for obj in grid_cell:
                    if self.radius > obj.radius:
                        dist = (self.pos - obj.pos).magnitude()
                        if dist < self.radius:
                            print(f"ate {obj.id}")
                            self.radius = math.sqrt(self.radius**2 + obj.radius**2)
                            self.eaten.append(obj)
                            grid_cell.remove(obj)

    def _keep_inside_map(self):
        if self.pos.x < self.radius:
            self.pos.x = self.radius
        if self.pos.y < self.radius:
            self.pos.y = self.radius
        
        if self.pos.x + self.radius > MAP_WIDTH:
            self.pos.x = MAP_WIDTH - self.radius
        if self.pos.y + self.radius > MAP_HEIGHT:
            self.pos.y = MAP_HEIGHT - self.radius