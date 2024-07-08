from pygario.constants import INITIAL_RADIUS
from pygario.vector import Vector2D


class Viewport():
    def __init__(self, center: Vector2D, radius: float) -> None:
        self.center = center
        self.scale = INITIAL_RADIUS / radius
    
    def update_radius(self, radius: float):
        self.scale = INITIAL_RADIUS / radius
