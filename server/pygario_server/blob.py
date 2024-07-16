from dataclasses import dataclass

from pygario_server.cell import Cell


@dataclass
class Blob(Cell):
    name: str

    def check_collision(self, other: 'Blob', margin: float = 0.0) -> bool:
        dist = (self.pos - other.pos).magnitude()
        return dist < (self.radius + other.radius + margin)
    
    def serialize(self) -> bytes:
        result = super().serialize()
        result += f",{self.name}".encode('utf-8')
        return result
