from dataclasses import dataclass, field
from typing import List, Tuple

import pygame

from pygario.gui.ui_component import UIComponent


@dataclass
class Container(UIComponent):
    corner_radius: int = 0
    border_width: int = 0
    border_color: Tuple[int, int, int] = (0,0,0)
    components: List[UIComponent] = field(init=False)

    def __post_init__(self):
        self.components = list()

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(
            window,
            self.color,
            (self.top_left.x, self.top_left.y, self.width, self.height),
            border_radius=self.corner_radius
            )

        # if self.border_width > 0:
        #     pygame.draw.rect(
        #     window,
        #     self.border_color,
        #     (self.top_left.x, self.top_left.y, self.width, self.height),
        #     width=self.border_width,
        #     border_radius=self.corner_radius
        #     )
        
        for component in self.components:
            component.draw(window)
    
    def add_component(self, component: UIComponent):
        import weakref
        component.parent = weakref.ref(self)
        self.components.append(component)
    
    def update(self, deltatime: float):
        for component in self.components:
            component.update(deltatime)