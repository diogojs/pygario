import sys
import contextlib
import weakref

from pygario.blob import Blob
from pygario.gui.container import Container
from pygario.gui.label import Label
from pygario.scenes.scene import Scene

with contextlib.redirect_stdout(None):
    import pygame

from typing import List

from pygario.player import Player
from pygario.cell import Cell
from pygario.color import Color
from pygario.constants import *
from pygario.viewport import Viewport
from pygario.vector import Vector2D


class MenuScene(Scene):
    def __init__(self):
        """
        Create Menu structure
        """
        self.font = pygame.font.SysFont("comicsans", 12)

        width = 400
        height = 300
        self.container = Container(
            Vector2D((WINDOW_WIDTH/2)-(width/2), (WINDOW_HEIGHT/2)-(height/2)-50),
            Vector2D((WINDOW_WIDTH/2)+(width/2), (WINDOW_HEIGHT/2)+(height/2)-50),
            Color.WHITE.value,
            corner_radius=20.0)
        self.container.add_component(
            Label(
                  Vector2D(65, 50),
                  Vector2D(),
                  Color.BLACK.value,
                  "Pygar.io",
                  font_size=58,
                  bold=True
                  )
        )

    def draw(self, window: pygame.Surface, deltatime: float):
        window.fill((200,200,200))

        self.container.draw(window)

        # debug info
        txt = self.font.render(f"deltatime: {deltatime}\nFPS: {1000/deltatime}", True, Color.BLACK.value)
        position_in_viewport = (10, 10)
        window.blit(txt, position_in_viewport)

        # update window
        pygame.display.update()

    def update(self, deltatime: float):
        pass
