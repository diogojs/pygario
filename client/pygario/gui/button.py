import pygame

from dataclasses import dataclass, field
from pygario.gui.ui_component import UIComponent


@dataclass
class Button(UIComponent):
    text: str
    font: pygame.font.Font
    corner_radius: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        self.rendered_text = self.font.render(self.text, True, (255,255,255))
    
    def draw(self, window: pygame.Surface) -> None:
        if self._center:
            self.view_position = self.rendered_text.get_rect(center=(self.parent.position + self._center).tuple())

        pygame.draw.rect(
            window,
            self.color,
            (self.view_position[0], self.view_position[1], self.width, self.height),
            border_radius=self.corner_radius
            )
        text_position = self.rendered_text.get_rect(center=(self.parent.position + self.center).tuple())
        window.blit(self.rendered_text, text_position)

    def update(self, deltatime: float):
        from pygario.game import Game
        from pygario.scenes.main_scene import MainScene
        
        area = pygame.Rect(self.view_position[0], self.view_position[1], self.width, self.height)
        if Game.MouseClick and area.collidepoint(Game.Mouse.tuple()):
            Game.add_scene(
                MainScene("Diogo")
            )