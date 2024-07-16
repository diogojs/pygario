import sys
import contextlib

from pygario.blob import Blob
from pygario.client import Client
from pygario.scenes.main_scene import MainScene
from pygario.scenes.scene import Scene

with contextlib.redirect_stdout(None):
    import pygame

from typing import List

from pygario.constants import *
from pygario.vector import Vector2D


class Game:
    client: Client = None
    scene_stack: List[Scene] = list()
    Mouse = Vector2D(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    clock: pygame.time.Clock = None
    is_running: bool = False

    @staticmethod
    def setup_pygame() -> pygame.Surface:
        pygame.init()
        pygame.font.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Blobs.io")
        return window

    def run(self):
        host = "localhost"
        if len(sys.argv) > 1:
            host = sys.argv[1]
        Game.client = Client(host, PORT)

        self.window = self.setup_pygame()
        Game.clock = pygame.time.Clock()

        deltatime = 0
        Game.scene_stack.append(MainScene())

        Game.is_running = True
        while Game.is_running:
            deltatime = Game.clock.tick(144)

            current_scene = Game.scene_stack[-1]

            # handle mouse events
            current_scene.handle_events()
            
            # update objects
            current_scene.update(deltatime)

            # draw objects
            current_scene.draw(self.window, deltatime)
        
        pygame.quit()
