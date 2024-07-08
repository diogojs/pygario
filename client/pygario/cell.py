from typing import Union
import pygame

from dataclasses import dataclass, field
from pygario.game_object import GameObject
from pygario.color import Color
from pygario.vector import Vector2D
from pygario.viewport import Viewport


@dataclass
class Cell(GameObject):
    radius: float
    color: Union[tuple, Color]
    font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.font = pygame.font.SysFont("comicsans", 10)
        self.counter = 0

    def draw(self, window: pygame.Surface, viewport: Viewport) -> None:
        self.counter += 1
        if self.counter % 1000 == 0:
            print(self.id, self.pos)

        actual_color = self.color if isinstance(self.color, tuple) else self.color.value
        position_in_viewport = (self.pos.x + viewport.center.x, self.pos.y + viewport.center.y)
        pygame.draw.circle(window,
                           actual_color,
                           position_in_viewport,
                           self.radius)
        txt = self.font.render(str(self.id), True, Color.BLACK.value)
        window.blit(txt, position_in_viewport)
