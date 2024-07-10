from typing import Union
import pygame

from dataclasses import dataclass, field
from pygario.color import Color
from pygario.constants import INITIAL_RADIUS, SCALE_MULTIPLIER
from pygario.game_object import GameObject
from pygario.viewport import Viewport


@dataclass
class Label(GameObject):
    text: str
    color: Union[tuple, Color] = Color.BLACK
    font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.INITIAL_FONT_SIZE = 12
        self.FONT_SIZE = 12
        self.font = pygame.font.SysFont("comicsans", self.FONT_SIZE)

    def draw(self, window: pygame.Surface, viewport: Viewport, **kwargs) -> None:
        radius = kwargs['radius'] if 'radius' in kwargs else INITIAL_RADIUS
        ratio = radius / INITIAL_RADIUS
        scale = 1 + (ratio - 1) * SCALE_MULTIPLIER
        if scale < 3:
            new_font_size = int(self.INITIAL_FONT_SIZE * scale**2)
            if new_font_size != self.FONT_SIZE:
                self.FONT_SIZE = new_font_size
                self.font = pygame.font.SysFont("comicsans", self.FONT_SIZE)

        actual_color = self.color if isinstance(self.color, tuple) else self.color.value
        position_in_viewport = (self.pos.x - viewport.up_left.x, self.pos.y - viewport.up_left.y)
        position_in_viewport = (position_in_viewport[0]/viewport.scale, position_in_viewport[1]/viewport.scale)
        txt = self.font.render(self.text, True, actual_color)
        position_in_viewport = (position_in_viewport[0] - txt.get_width()/2, position_in_viewport[1] - txt.get_height()/2)
        window.blit(txt, position_in_viewport)
