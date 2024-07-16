from typing import Tuple

from dataclasses import dataclass

from pygario_server.vector import Vector2D


@dataclass
class Cell:
    id: int
    pos: Vector2D
    radius: float
    color: Tuple[int, int, int]

    def serialize(self) -> bytes:
        color_str = ','.join(str(c) for c in self.color)
        return f"{self.id},{self.pos.x:.6},{self.pos.y:.6},{self.radius:.6},{color_str}".encode('utf-8')