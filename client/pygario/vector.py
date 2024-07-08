from dataclasses import dataclass
import math

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
        x = self.x + other.x
        y = self.y + other.y
        return Vector2D(x, y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        x = self.x - other.x
        y = self.y - other.y
        return Vector2D(x, y)
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def set_magnitude(self, scalar: float):
        old_magnitude = self.magnitude()
        self.x = self.x * scalar/old_magnitude
        self.y = self.y * scalar/old_magnitude