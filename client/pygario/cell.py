from typing import Union
import pygame

from dataclasses import dataclass
from pygario.constants import MINIMUM_RADIUS
from pygario.game_object import GameObject
from pygario.color import Color
from pygario.viewport import Viewport


@dataclass
class Cell(GameObject):
    radius: float
    color: Union[tuple, Color]

    def draw(self, window: pygame.Surface, viewport: Viewport) -> None:
        actual_color = self.color if isinstance(self.color, tuple) else self.color.value
        position_in_viewport = (self.pos.x - viewport.up_left.x, self.pos.y - viewport.up_left.y)
        position_in_viewport = (position_in_viewport[0]/viewport.scale, position_in_viewport[1]/viewport.scale)
        radius_in_viewport = self.radius/viewport.scale
        if radius_in_viewport < MINIMUM_RADIUS:
            radius_in_viewport = MINIMUM_RADIUS
        pygame.draw.circle(window,
                           actual_color,
                           position_in_viewport,
                           radius_in_viewport)
