import os
from dataclasses import dataclass
from typing import Protocol, Iterable, Callable, Any

from canvas import Buffer
from drawable import Drawable
from image import TextRenderer, DEFAULT_FONT_WIDTH, DEFAULT_FONT, DEFAULT_FONT_FILE


class Display(Protocol):
    def draw(self):
        os.system("clear")
        self._draw_impl()

    def _draw_impl(self):
        ...


type TransitionFactory = Callable[[Buffer, Buffer, int, ...], Display]


@dataclass
class Slide(Display):
    buffer: Buffer

    def _draw_impl(self):
        for yi in range(self.buffer.height):
            print("".join(
                str(tx) for tx in self.buffer.buffer[yi * self.buffer.width: (yi + 1) * self.buffer.width]
            ))

    @classmethod
    def generate(cls, width: int, height: int, elems: Iterable[Drawable]) -> "Slide":
        buff = Buffer.of_size(width, height)
        for d in elems:
            d.draw(buff)
        return Slide(buff)


class Presentation:
    def __init__(self, width: int, height: int, **kwargs):
        self.width = width
        self.height = height
        self.slides: list[Slide] = []
        self.transitions: list[Display] = []
        self.buffers = []

        font_width = kwargs.get("font_width") or DEFAULT_FONT_WIDTH
        font = kwargs.get("font") or DEFAULT_FONT
        font_file = kwargs.get("font_file") or DEFAULT_FONT_FILE
        self.buffered_transition: tuple[TransitionFactory, int, dict[str, Any]] = None

        self.key_frames: dict[str, int] = {}

        self.colour_renderer = TextRenderer(font_width, font, font_file, grayscale=False)
        self.monochrome_renderer = TextRenderer(font_width, font, font_file, grayscale=True)

    def add_slide(self, slide: Slide, buffer: list[Drawable], key: str = None):
        if self.slides:
            first = self.slides[-1].buffer
            if self.buffered_transition:
                factory, duration, kwargs = self.buffered_transition
                self.transitions.append(factory(first, slide.buffer, duration, **kwargs))
            else:
                from transitions import Empty
                self.transitions.append(Empty(first, slide.buffer, 0))

        if key:
            self.key_frames[key] = len(self.slides)
        self.slides.append(slide)
        self.buffers.append(buffer)

    def add_transition(self, transition_factory: TransitionFactory, duration: int, **kwargs):
        self.buffered_transition = (transition_factory, duration, kwargs)

    def run(self):
        slide_index = 0
        slides = len(self.slides)
        while slide_index < slides:
            self.slides[slide_index].draw()
            ctrl = input()
            match ctrl:
                case '':
                    if slide_index < slides - 1:
                        self.transitions[slide_index].draw()
                    slide_index += 1
                case ';' | "back":
                    if slide_index > 0:
                        slide_index -= 1
                case '\'' | "skip":
                    slide_index += 1
                case 'exit':
                    break
                case _:
                    slide_index = self.key_frames.get(ctrl, slide_index)
