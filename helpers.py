from contextlib import contextmanager
from typing import Any

from ansi import Style, EMPTY_STYLE
from display import Presentation, Slide
from drawable import Box, Image, Empty, Text
from image import TextRenderer
from text import text_strip
from transitions import Sweep, Fuzz, Shift


class __Context:
    def __init__(self):
        self.stack = []
        self.last: str | None = None

    @contextmanager
    def __call__(self, elem):
        self.stack.append(elem)
        yield None
        self.stack.pop()

    @property
    def top(self):
        return self.stack[-1]


ctx = __Context()


@contextmanager
def presentation(width: int, height: int, **kwargs):
    p = Presentation(width, height, **kwargs)
    with ctx(p):
        yield
    p.run()


@contextmanager
def slide(key: str = None, *, copy: str = None):
    p: Presentation = ctx.top
    buffer = list(p.buffers[p.key_frames[copy]]) if copy else []
    with ctx(buffer):
        yield
    ctx.last = key
    p.add_slide(Slide.generate(p.width, p.height, buffer), buffer, key)


def cont(key: str = "$$$$$$$$$$$$$$$$$$"):
    return slide(key, copy=ctx.last)


@contextmanager
def box(charset: str, style: Style = EMPTY_STYLE):
    inner = []
    with ctx(inner):
        yield
    ctx.top.append(Box(inner[0], charset, style))


def image(x: int, y: int, width: int, path: str, colour: bool = False):
    buffer = ctx.top
    p = ctx.stack[0]
    renderer: TextRenderer = p.colour_renderer if colour else p.monochrome_renderer

    buffer.append(Image(x, y, renderer.cached_render(path, width)))


def empty(x: int, y: int, width: int, height: int):
    ctx.top.append(Empty(x, y, width, height))


def text(x: int, y: int, text_: str, width: int = None, centered: bool = False):
    ctx.top.append(Text(x, y, text_strip(text_), width, centered))


def transition(trans: Any, duration: float, **kwargs):
    ctx.top.add_transition(trans, duration, **kwargs)


sweep = Sweep
shift = Shift
fuzz = Fuzz
