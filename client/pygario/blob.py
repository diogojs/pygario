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

        # border-waving implementation
        # points = []
        # pi_rad = (math.pi/180)
        # for i in range(72):
        #     # TODO: reimplement/refine displacement
        #     # displacement = random.random() * 5
        #     cos = radius_in_viewport*math.cos(pi_rad*i*5)
        #     sin = radius_in_viewport*math.sin(pi_rad*i*5)
        #     # cos = cos + displacement if cos > 0 else cos - displacement
        #     # sin = sin + displacement if sin > 0 else sin - displacement
        #     p = (self.pos.x + cos, self.pos.y + sin)
        #     p = (p[0] - viewport.up_left.x, p[1] - viewport.up_left.y)
        #     p = (p[0]/viewport.scale, p[1]/viewport.scale)
        #     points.append(p)

        # pygame.draw.polygon(window, border_color, points, 10)
        # pygame.draw.polygon(window, actual_color, points, 0)

        self.label.draw(window, viewport, radius=self.radius)
