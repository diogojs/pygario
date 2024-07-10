from typing import Union
import pygame

from dataclasses import dataclass, field
from pygario.cell import Cell
from pygario.constants import MINIMUM_RADIUS
from pygario.color import Color
from pygario.label import Label
from pygario.viewport import Viewport


@dataclass
class Blob(Cell):
    name: str
    label: Label = field(init=False)

    def __post_init__(self):
        self.label = Label(999, self.pos, self.name, Color.WHITE)

    def draw(self, window: pygame.Surface, viewport: Viewport) -> None:
        super().draw(window, viewport)

        self.label.draw(window, viewport, radius=self.radius)
