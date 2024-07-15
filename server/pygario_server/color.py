from enum import Enum
from typing import Tuple

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255),
    BLACK = (0, 0, 0)

    @staticmethod
    def get_random_preset() -> 'Color':
        from random import randint
        return list(Color)[(randint(0, len(Color)-1))]
    
    @staticmethod
    def get_random() -> Tuple[int, int, int]:
        from random import randint
        return (randint(0, 6)*40, randint(0, 6)*40, randint(0, 6)*40)