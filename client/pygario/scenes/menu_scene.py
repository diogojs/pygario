import sys
import contextlib
import weakref

from pygario.blob import Blob
from pygario.gui.button import Button
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
            corner_radius=20)
        
        
        TOP_MARGIN = 80
        SIDE_MARGIN = 40
        INNER_MARGIN = 20
        title = Label(None, None,
                  Color.BLACK.value,
                  "Pygar.io",
                  font_size=58,
                  bold=True
                  )
        title.center = Vector2D(self.container.width/2, TOP_MARGIN)
        self.container.add_component(title)

        label_name = Label(
                  Vector2D(SIDE_MARGIN, title.bottom_right.y + INNER_MARGIN),
                  None,
                  Color.DARK_GREY.value,
                  "Name:",
                  font_size=24
                  )
        self.container.add_component(label_name)

        button = Button(
            Vector2D(label_name.position.x + INNER_MARGIN, label_name.bottom_right.y + INNER_MARGIN),
            Vector2D(title.bottom_right.x - INNER_MARGIN, label_name.bottom_right.y + INNER_MARGIN + 50),
            Color.GREEN.value,
            "Play",
            pygame.font.SysFont(None, 24),
            corner_radius=5
        )
        self.container.add_component(button)

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
        self.container.update(deltatime)

    def finish(self):
        pass