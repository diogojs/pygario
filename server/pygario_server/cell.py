from typing import Union

from dataclasses import dataclass

from pygario_server.vector import Vector2D


@dataclass
class Cell:
    id: int
    pos: Vector2D
    radius: float