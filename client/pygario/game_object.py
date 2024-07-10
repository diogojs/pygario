from dataclasses import dataclass
import pygame

from pygario.vector import Vector2D
from pygario.viewport import Viewport

@dataclass
class GameObject:
    id: int
    pos: Vector2D

    def draw(self, window: pygame.Surface, viewport: Viewport, **kwargs) -> None:
        pass
        
    def update(self, deltatime: int):
        pass
