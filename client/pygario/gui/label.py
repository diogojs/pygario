from typing import Union
import pygame

from dataclasses import dataclass, field
from pygario.color import Color
from pygario.gui.ui_component import UIComponent
from pygario.viewport import Viewport


@dataclass
class Label(UIComponent):
    text: str
    font_size: int
    bold: bool = False
    font: pygame.font.Font = field(init=False)

    def __post_init__(self):
        self.font = pygame.font.SysFont("verdana", self.font_size, self.bold)

    def draw(self, window: pygame.Surface) -> None:
        txt = self.font.render(self.text, True, self.color)
        
        parent_position = self.parent.position
        view_position = parent_position + self.position
        window.blit(txt, view_position.tuple())
