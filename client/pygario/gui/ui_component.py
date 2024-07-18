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
    _center: Vector2D = field(init=False)

    def __post_init__(self):
        self._center = None
        self.view_position = False

    @property
    def center(self) -> Vector2D:
        if self._center:
            return self._center

        return self.top_left + (self.bottom_right - self.top_left)/2
    
    @center.setter
    def center(self, value: Vector2D):
        self._center = value
        self._update_points(self.rendered_text.get_rect())

    def _update_points(self, txt_rect: pygame.Rect):
        half_rect = Vector2D(txt_rect.width/2, txt_rect.height/2)
        self.top_left = self.center - half_rect
        self.bottom_right = self.center + half_rect

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
        parent_position = self.parent.position
        self.view_position = (parent_position + self.position).tuple()

    def draw(self, window: pygame.Surface):
        pass

    def update(self, deltatime: float):
        pass