from dataclasses import dataclass
from typing import Protocol, Iterator

from ansi import Style, EMPTY_STYLE


@dataclass(slots=True, frozen=True)
class Texel:
    text: str = " "
    style: Style = EMPTY_STYLE

    def __str__(self):
        return self.style.format(self.text)


EMPTY_TEXEL = Texel()


class Canvas(Protocol):
    def __setitem__(self, index: tuple[int, int], value: Texel):
        ...

    def __getitem__(self, index: tuple[int, int]) -> Texel:
        ...


@dataclass
class Offset(Canvas):
    x: int
    y: int
    canvas: Canvas

    def __setitem__(self, index: tuple[int, int], value: Texel):
        self.canvas[index[0] + self.x, index[1] + self.y] = value

    def __getitem__(self, index: tuple[int, int]) -> Texel:
        return self.canvas[index[0] - self.x, index[1] - self.y]


class Buffer(Canvas):
    def __init__(self, width: int, height: int, buffer: list[Texel]):
        if width <= 0 or height <= 0 or len(buffer) != width * height:
            raise ValueError

        self.width = width
        self.height = height
        self.buffer = buffer

    def __setitem__(self, index: tuple[int, int], value: Texel):
        x, y = index
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        self.buffer[x + y * self.width] = value

    def __getitem__(self, index: tuple[int, int]) -> Texel:
        x, y = index
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return EMPTY_TEXEL
        return self.buffer[x + y * self.width]

    def __iter__(self) -> Iterator[tuple[int, int, Texel]]:
        for i, tx in enumerate(self.buffer):
            yield i % self.width, i // self.width, tx

    def clear(self):
        self.buffer = [EMPTY_TEXEL for _ in range(self.width * self.height)]

    @classmethod
    def of_size(cls, width: int, height: int):
        return cls(width, height, [EMPTY_TEXEL for _ in range(width * height)])