from dataclasses import dataclass
import math
from typing import Tuple

@dataclass
class Vector2D:
    x: float = 0
    y: float = 0

    def add(self, other: 'Vector2D') -> None:
        self.x += other.x
        self.y += other.y
    
    def sub(self, other: 'Vector2D') -> None:
        self.x -= other.x
        self.y -= other.y

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        if isinstance(other, Vector2D):
            x = self.x + other.x
            y = self.y + other.y
        elif isinstance(other, tuple):
            x = self.x + other[0]
            y = self.y + other[1]
        else:
            raise TypeError(f"Vector2D can not be added with {type(other)}")
        return Vector2D(x, y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        x = self.x - other.x
        y = self.y - other.y
        return Vector2D(x, y)
    
    def __truediv__(self, scalar: float) -> 'Vector2D':
        x = self.x / scalar
        y = self.y / scalar
        return Vector2D(x, y)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def set_magnitude(self, scalar: float):
        old_magnitude = self.magnitude()
        self.x = self.x * scalar/old_magnitude
        self.y = self.y * scalar/old_magnitude

    def tuple(self) -> Tuple[float, float]:
        return self.x, self.y