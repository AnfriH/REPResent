from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Any


class Colours(Enum):
    BLACK = (0, 0)
    RED = (0, 1)
    GREEN = (0, 2)
    BROWN = (0, 3)
    BLUE = (0, 4)
    PURPLE = (0, 5)
    CYAN = (0, 6)
    LIGHT_GRAY = (0, 7)

    DARK_GRAY = (1, 0)
    LIGHT_RED = (1, 1)
    LIGHT_GREEN = (1, 2)
    YELLOW = (1, 3)
    LIGHT_BLUE = (1, 4)
    LIGHT_PURPLE = (1, 5)
    LIGHT_CYAN = (1, 6)
    WHITE = (1, 7)

    NONE = None

    def __str__(self):
        if not self._value_:
            return ""

        light = 9 if self._value_[0] else 3
        return f"\033[{light}{self._value_[1]}m"

    def __or__(self, other):
        if not isinstance(other, Colours):
            raise TypeError
        return FullColour(self._value_, other._value_)


@dataclass
class FullColour:
    foreground: tuple[int, int]
    background: tuple[int, int]

    def __str__(self):
        tokens = []
        if self.foreground:
            tokens.append(f"{9 if self.foreground[0] else 3}{self.foreground[1]}")
        if self.background:
            tokens.append(f"{10 if self.background[0] else 4}{self.background[1]}")
        if not tokens:
            return ""

        return f"\033[{";".join(tokens)}m"


ColourType = Colours | FullColour


class EffectType:
    def __init__(self, *tokens: int):
        self.tokens = set(tokens)

    def __or__(self, other: Any):
        if not isinstance(other, EffectType):
            raise TypeError
        if self == Effects.NONE or other == Effects.NONE:
            raise ValueError(f"Cannot Union NONE type")
        return EffectType(*self.tokens, *other.tokens)

    def __iter__(self):
        return iter(self.tokens)

    def __str__(self):
        if not any(self.tokens):
            return ""
        return f"\033[{";".join(str(t) for t in self.tokens)}m"


class Effects(EffectType, Enum):
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    NEGATIVE = 7
    STRIKETHROUGH = 9
    NONE = None


# special token for clearing formatting if any
END = "\033[0m"


class Style(NamedTuple):
    colour: ColourType = Colours.NONE
    effect: EffectType = Effects.NONE

    def format(self, string: str):
        return f"{self.colour}{self.effect}{string}{END}"


EMPTY_STYLE = Style()
