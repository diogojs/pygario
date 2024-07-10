from pygario.constants import INITIAL_RADIUS, SCALE_MULTIPLIER, WINDOW_WIDTH, WINDOW_HEIGHT
from pygario.vector import Vector2D

class Viewport():
    SCALE_DAMPING = {
        1: 0.4,
        5: 0.2,
        10: 0.1,
        20: 0.05,
        100: 0.01
    }

    def __init__(self, player_position: Vector2D, player_radius: float) -> None:
        self.scale = 1
        self.last_radius = player_radius
        self.up_left = player_position - Vector2D(WINDOW_WIDTH/2*self.scale, WINDOW_HEIGHT/2*self.scale)

    def update(self, player_position: Vector2D, player_radius: float):
        self.update_radius(player_radius)
        self.up_left = player_position - Vector2D(WINDOW_WIDTH/2*self.scale, WINDOW_HEIGHT/2*self.scale)

    def update_radius(self, radius: float):
        if radius == self.last_radius:
            return

        ratio = radius / INITIAL_RADIUS
        # multiplier = 1
        # for limit, damping in self.SCALE_DAMPING.items():
        #     if ratio > limit:
        #         multiplier = damping
        self.scale = 1 + (ratio - 1) * SCALE_MULTIPLIER
