from typing import Union

from dataclasses import dataclass

from pygario_server.vector import Vector2D


@dataclass
class Cell:
    id: int
    pos: Vector2D
    radius: float

    def serialize(self) -> bytes:
        return f"{self.id},{self.pos.x},{self.pos.y},{self.radius}".encode('utf-8')