from dataclasses import dataclass
from typing import Protocol

from ansi import Style, EMPTY_STYLE
from canvas import Canvas, Texel, Buffer, Offset
from text import line_wrap, text_parse


class Drawable(Protocol):
    x: int
    y: int
    width: int
    height: int

    def draw(self, canvas: Canvas):
        ...


# does nothing. are protocols instantiable?
@dataclass
class Empty(Drawable):
    x: int
    y: int
    width: int
    height: int

    def draw(self, canvas: Canvas):
        pass


@dataclass
class Image(Drawable):
    x: int
    y: int
    buffer: Buffer

    def draw(self, canvas: Canvas):
        for ix, iy, tx in self.buffer:
            canvas[self.x + ix, self.y + iy] = tx

    @property
    def width(self) -> int:
        return self.buffer.width

    @property
    def height(self) -> int:
        return self.buffer.height


class Text(Drawable):
    def __init__(self, x: int, y: int, text: str, width: int = None, centered: bool = False):
        self.x = x
        self.y = y
        self.centered = centered

        # TODO: parse and colour text
        texels = list(text_parse(text))

        if not width and '\n' not in text:
            self.width = len(texels)
            self.buffer = [texels, ]
            return
        if not width:
            width = max(len(line) for line in "".join(t.text for t in texels).split('\n'))
        self.width = width
        self.buffer = list(line_wrap(texels, width))

    @property
    def height(self) -> int:
        return len(self.buffer)

    def draw(self, canvas: Canvas):
        for yi, row in enumerate(self.buffer):
            for xi, px in enumerate(row):
                offset = (self.width - len(row)) // 2 if self.centered else 0
                canvas[self.x + xi + offset, self.y + yi] = px


class Box(Drawable):
    def __init__(self, inner: Drawable, charset: str, style: Style = EMPTY_STYLE):
        self.charset = [Texel(ch, style) for ch in charset]
        self.inner = inner

    def draw(self, canvas: Canvas):
        for yi in range(self.inner.height):
            canvas[self.x, self.y + yi + 1] = self.charset[0]
            canvas[self.x + self.width - 1, self.y + yi + 1] = self.charset[0]
        for xi in range(self.inner.width):
            canvas[self.x + xi + 1, self.y] = self.charset[1]
            canvas[self.x + xi + 1, self.y + self.height - 1] = self.charset[1]
        canvas[self.x, self.y] = self.charset[2]
        canvas[self.x + self.width - 1, self.y] = self.charset[3]
        canvas[self.x, self.y + self.height - 1] = self.charset[4]
        canvas[self.x + self.width - 1, self.y + self.height - 1] = self.charset[5]

        self.inner.draw(Offset(1, 1, canvas))

    @property
    def x(self):
        return self.inner.x

    @property
    def y(self):
        return self.inner.y

    @property
    def width(self):
        return self.inner.width + 2

    @property
    def height(self):
        return self.inner.height + 2
