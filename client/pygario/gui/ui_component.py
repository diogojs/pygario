from dataclasses import dataclass, field
from typing import Tuple
import weakref

import pygame

from pygario.vector import Vector2D

@dataclass
class UIComponent:
    _parent: weakref = field(init=False)
    top_left: Vector2D
    bottom_right: Vector2D
    color: Tuple[int, int, int]

    @property
    def position(self) -> Vector2D:
        return self.top_left
    
    @position.setter
    def position(self, value: Vector2D):
        self.top_left = value
    
    @property
    def width(self) -> float:
        return self.bottom_right.x - self.top_left.x
    
    @width.setter
    def width(self, value: float):
        self.bottom_right.x = self.top_left.x + value

    @property
    def height(self) -> float:
        return self.bottom_right.y - self.top_left.y
    
    @height.setter
    def height(self, value: float):
        self.bottom_right.y = self.top_left.y + value
    
    @property
    def parent(self) -> 'UIComponent':
        return self._parent()
    
    @parent.setter
    def parent(self, value: weakref):
        self._parent = value

    def draw(self, window: pygame.Surface):
        pass