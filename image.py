import itertools
from math import ceil
from pathlib import Path

from pyvips import Image, Interpretation, error, OperationMath2, Kernel, CompassDirection

from ansi import ColourType, Colours, Style
from caching import Cache
from canvas import Texel, Buffer

GAMMA = 0.7
CHARSET = "▀▁▂▄▆▌▎▐░▒▓▔▖▗▘▙▛▜▝▟◜◝◞◟◠◡,`"

DEFAULT_FONT_WIDTH = 10
DEFAULT_FONT = "Hack Regular"
DEFAULT_FONT_FILE = "/usr/share/fonts/TTF/Hack-Regular.ttf"

CACHE_DIR = ".cache/images/"
CACHE = Cache[Buffer](CACHE_DIR)

# TODO: add file loader to shift this to disk
def from_hex(hex_):
    return tuple(int(hex_[i:i + 2], 16) for i in (0, 2, 4))

COLOURSPACE = {
    # Colours.BLACK: from_hex("232627"),
    Colours.RED: from_hex("ed1515"),
    Colours.GREEN: from_hex("21c33c"),
    Colours.BROWN: from_hex("f67400"),
    Colours.BLUE: from_hex("1d99f3"),
    Colours.PURPLE: from_hex("9b59b6"),
    Colours.CYAN: from_hex("1abc9c"),
    Colours.LIGHT_GRAY: from_hex("c8c8c8"),

    Colours.DARK_GRAY: from_hex("7f8c8d"),
    Colours.LIGHT_RED: from_hex("c0392b"),
    Colours.LIGHT_GREEN: from_hex("11d116"),
    Colours.YELLOW: from_hex("fdbc4b"),
    Colours.LIGHT_BLUE: from_hex("3daee9"),
    Colours.LIGHT_PURPLE: from_hex("8e44ad"),
    Colours.LIGHT_CYAN: from_hex("16a085"),
    Colours.WHITE: from_hex("ffffff"),
}


class TextRenderer:
    def __init__(self, width: int, font: str, font_file: Path | str, charset: str = CHARSET, grayscale: bool = True):
        if isinstance(font_file, str):
            fontfile = Path(font_file)

        self.width = width
        self.height = width * 2
        self.dpi = width * 10

        self.font = font
        self.font_file = font_file

        charset += ' █'

        self.grayscale = grayscale
        self.colourspace = None if grayscale else COLOURSPACE
        self.textures: dict[str, Image] = {char: self.generate_char(char) for char in charset}

    def generate_char(self, char: str) -> Image:
        if len(char) != 1:
            raise ValueError
        # empty characters get skipped
        if char == ' ':
            return Image.black(self.width, self.height)
        elif char == '█':
            return Image.black(self.width, self.height).new_from_image(255)
        # we use '█' as it ensures that the correct height offset is set (avoids autocrop)
        try:
            char_render: Image = Image.text(f"{char} █", dpi=self.dpi, font=self.font, fontfile=self.font_file)
            cropped_char: Image = char_render.crop(0, 0, char_render.width - self.width * 2, self.height)
        except error.Error as ex:
            raise ValueError(f"Cannot rasterise \'{char}\'", ex)

        return cropped_char.gravity(CompassDirection.CENTRE, self.width, self.height)

    def match_char(self, segment: Image) -> Texel:
        _, _, _, alpha = segment.bandsplit()
        mono_segment: Image = segment.colourspace(Interpretation.B_W)[0] * alpha.linear(1 / 255, 0)
        if (mono_segment == self.textures[' ']).min():
            char = ' '
        elif (mono_segment == self.textures['█']).min():
            char = '█'
        else:
            char = self.match_symbol(mono_segment)
        colour = Colours.NONE if self.grayscale else self.match_colour(segment)

        return Texel(char, Style(colour))

    def match_colour(self, segment: Image) -> ColourType:
        count = 0
        average = [0, 0, 0]
        r_l, g_l, b_l, a_l = (e.tolist() for e in segment.bandsplit())
        for yi, row in enumerate(r_l):
            for xi, r_px in enumerate(row):
                g_px = g_l[yi][xi]
                b_px = b_l[yi][xi]
                a_px = a_l[yi][xi]
                count += a_px
                average = [(a + b * a_px) for a, b in zip(average, (r_px, g_px, b_px))]
        colour = [e / count for e in average] if count != 0 else average
        out, _ = min(
            (
                (cls, sum(
                    (
                        (a - b) ** 2 for a, b in zip(vals, colour)
                    )
                )) for cls, vals in self.colourspace.items()
            ),
            key=lambda e: e[1]
        )
        return out

    def match_symbol(self, mono_segment: Image) -> str:
        char, _ = min(
            (
                (
                    char,
                    pattern.math2_const(OperationMath2.POW, GAMMA)
                    .subtract(mono_segment.math2_const(OperationMath2.POW, GAMMA))
                    .stats()(3, 0)[0]
                ) for char, pattern in self.textures.items()
            ),
            key=lambda e: e[1]
        )
        return char

    def render(self, image: Image, width: int) -> Buffer:
        target_width = self.width * width
        scale_factor = target_width / image.width

        scaled: Image = image.resize(scale_factor, kernel=Kernel.LANCZOS2)

        height = ceil(scaled.height / self.height)
        padded: Image = scaled.gravity(CompassDirection.CENTRE, target_width, self.height * height)

        screen_buffer = list(itertools.chain.from_iterable(
            (
                self.match_char(
                    padded.crop(xi * self.width, yi * self.height, self.width, self.height)
                ) for xi in range(width)
            ) for yi in range(height)
        ))
        return Buffer(width, height, screen_buffer)

    def cached_render(self, image: Path | str, width: int) -> Buffer:
        if isinstance(image, str):
            img_str = image
            image_path = Path(image)
        else:
            img_str = str(image)
            image_path = image

        def factory():
            image_file: Image = Image.new_from_file(img_str)
            if image_file.bands == 3:
                image_file = image_file.addalpha()

            return self.render(image_file, width)

        return CACHE.cached(f"{image_path.stem}_{image_path.suffix[1:]}_{width}_{self.grayscale}", factory)
