from typing import Tuple

from dataclasses import dataclass

from pygario_server.cell import Cell


@dataclass
class Blob(Cell):
    name: str
    color: Tuple[int, int, int]