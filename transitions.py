import os
import time
from dataclasses import dataclass
from math import ceil
from random import random
from typing import Iterable

from canvas import Buffer, Texel
from display import Display

FRAME_RATE = 60


@dataclass
class Transition(Display):
    prev: Buffer
    next: Buffer
    duration: float

    @property
    def frames(self) -> int:
        return ceil(FRAME_RATE * self.duration)

    @property
    def width(self) -> int:
        return self.prev.width

    @property
    def height(self) -> int:
        return self.prev.height

    def draw(self):
        frames = self.frames
        delay = 1 / FRAME_RATE
        for frame in range(frames):
            self._render(self._draw_frame(frame / frames))
            time.sleep(delay)

    def _render(self, buffer: Iterable[Iterable[Texel]]):
        os.system("clear")
        for line in buffer:
            for tx in line:
                print(str(tx), end='')
            print()

    def _draw_frame(self, t: float) -> Iterable[Iterable[Texel]]:
        for yi in range(self.height):
            yield (self._draw_tx(t, xi, yi) for xi in range(self.width))

    def _draw_tx(self, t: float, x: int, y: int) -> Texel:
        ...


class Empty(Transition):
    def draw(self):
        pass


@dataclass
class Sweep(Transition):
    flip: bool = False
    axis: str = "x"

    def _draw_tx(self, t: float, x: int, y: int) -> Texel:
        t_flip = t if self.flip else 1 - t
        offset, axis = (t_flip * self.width, x) if self.axis == 'x' else (t_flip * self.height, y)
        return self.prev[x, y] if (offset < axis if self.flip else offset > axis) else self.next[x, y]


@dataclass
class Shift(Transition):
    flip: bool = False
    axis: str = "x"

    def _draw_tx(self, t: float, x: int, y: int) -> Texel:
        t_flip, prev_, next_ = (1 - t, self.prev, self.next) if self.flip else (t, self.prev, self.next)
        is_x = self.axis == 'x'
        xi, yi = (x + ceil(self.width * t_flip), y) if is_x else (x, y + ceil(self.height * t_flip))
        xi_2, yi_2, cond = (xi - self.width, yi, xi < self.width) if is_x else (xi, yi - self.height, yi < self.height)
        return prev_[xi, yi] if cond else next_[xi_2, yi_2]


@dataclass
class Fuzz(Transition):
    def __post_init__(self):
        self.buffer = [random() for _ in range(self.width * self.height)]

    def _draw_tx(self, t: float, x: int, y: int) -> Texel:
        return self.prev[x, y] if self.buffer[x + y * self.width] > t else self.next[x, y]
