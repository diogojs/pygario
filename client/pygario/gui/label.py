from typing import Union
import pygame

from dataclasses import dataclass, field
from pygario.gui.ui_component import UIComponent
from pygario.vector import Vector2D


@dataclass
class Label(UIComponent):
    text: str
    font_size: int
    bold: bool = False
    font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.font = pygame.font.SysFont("verdana", self.font_size, self.bold)
        self.rendered_text = self.font.render(self.text, True, self.color)
        if self.bottom_right is None and self.top_left is not None:
            self.bottom_right = self.top_left + Vector2D(self.rendered_text.get_rect().width, self.rendered_text.get_rect().height)

    def draw(self, window: pygame.Surface) -> None:
        if self._center:
            self.view_position = self.rendered_text.get_rect(center=(self.parent.position + self._center).tuple())
        window.blit(self.rendered_text, self.view_position)
