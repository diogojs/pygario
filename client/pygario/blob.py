import pygame

from dataclasses import dataclass
from pygario.cell import Cell
from pygario.color import Color
from pygario.vector import Vector2D

from pygario.constants import *


class Blob(Cell):
    def move(self, dx: float, dy: float):
        self.pos.add(Vector2D(dx, dy))
    
    def update(self, deltatime: int):
        dist = Mouse - Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        if (dist.magnitude() < INITIAL_RADIUS/4):
            return
        
        dist.set_magnitude(INITIAL_SPEED)
        self.pos += dist
        self._keep_inside_map()

    def _keep_inside_map(self):
        if self.pos.x < self.radius:
            self.pos.x = self.radius
        if self.pos.y < self.radius:
            self.pos.y = self.radius
        
        if self.pos.x + self.radius > MAP_WIDTH:
            self.pos.x = MAP_WIDTH - self.radius
        if self.pos.y + self.radius > MAP_HEIGHT:
            self.pos.y = MAP_HEIGHT - self.radius