from dataclasses import dataclass
import pygame

from pygario.vector import Vector2D

@dataclass
class GameObject:
    id: int
    pos: Vector2D

    def draw(self, window: pygame.Surface) -> None:
        pass
        
    def update(self, deltatime: int):
        pass
