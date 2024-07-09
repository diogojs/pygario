from typing import Union
import pygame

from dataclasses import dataclass, field
from pygario.game_object import GameObject
from pygario.color import Color
from pygario.vector import Vector2D
from pygario.viewport import Viewport


@dataclass
class Label(GameObject):
    text: str
    color: Union[tuple, Color] = Color.BLACK
    font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.font = pygame.font.SysFont("comicsans", 10)

    def draw(self, window: pygame.Surface, viewport: Viewport) -> None:
        actual_color = self.color if isinstance(self.color, tuple) else self.color.value
        position_in_viewport = (self.pos.x + viewport.up_left.x, self.pos.y + viewport.up_left.y)
        txt = self.font.render(self.text, True, actual_color)
        window.blit(txt, position_in_viewport)
