from enum import Enum
from typing import Tuple

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    DARK_GREY = (50, 50, 50)
    LIGHT_GREY = (200, 200, 200)


    @classmethod
    def get_random(cls) -> Tuple[int, int, int]:
        from random import randint

        return (randint(0, 6)*40, randint(0, 6)*40, randint(0, 6)*40)