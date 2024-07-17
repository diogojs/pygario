from typing import Union
import pygame

from dataclasses import dataclass, field
from pygario.cell import Cell
from pygario.constants import MINIMUM_RADIUS
from pygario.color import Color
from pygario.label import Label
from pygario.viewport import Viewport

BORDER_WIDTH = 2

@dataclass
class Blob(Cell):
    name: str
    label: Label = field(init=False)

    def __post_init__(self):
        self.label = Label(999, self.pos, self.name, Color.WHITE)
        self.old_radius = self.radius

    def draw(self, window: pygame.Surface, viewport: Viewport) -> None:
        actual_color = self.color if isinstance(self.color, tuple) else self.color.value
        border_color = tuple(c*0.5 for c in actual_color)
        position_in_viewport = (self.pos.x - viewport.up_left.x, self.pos.y - viewport.up_left.y)
        position_in_viewport = (position_in_viewport[0]/viewport.scale, position_in_viewport[1]/viewport.scale)
        border_radius = self.radius + BORDER_WIDTH
        border_in_viewport = border_radius / viewport.scale
        radius_in_viewport = (self.radius-BORDER_WIDTH)/viewport.scale
        if radius_in_viewport < MINIMUM_RADIUS:
            radius_in_viewport = MINIMUM_RADIUS
        
        pygame.draw.circle(window,
                           border_color,
                           position_in_viewport,
                           border_in_viewport)
        pygame.draw.circle(window,
                           actual_color,
                           position_in_viewport,
                           radius_in_viewport)

        self.label.draw(window, viewport, radius=self.radius)
