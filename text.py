import itertools
import textwrap
from typing import Iterable, Iterator

from ansi import Colours, Effects, EffectType, Style, FullColour
from canvas import Texel


def line_wrap(texels: Iterable[Texel], width: int) -> Iterator[list[Texel]]:
    buffer: list[Texel] = []
    current_word: list[Texel] = []
    spaces = 0
    prev_char = 0

    for tx in texels:
        char = tx.text
        if char in (' ', '\n'):
            if prev_char:
                buffer, current_word, spaces, out = slice_helper(buffer, current_word, spaces, width)
                if out is not None:
                    yield out

            if char == ' ':
                spaces += 1
            else:
                yield buffer

                buffer = []
                spaces = 0
            prev_char = False
        else:
            current_word.append(tx)
            prev_char = True

    buffer, _, _, out = slice_helper(buffer, current_word, spaces, width)
    if out is not None:
        yield out
    yield buffer


def slice_helper(buffer: list, current_word: list, spaces: int, width: int):
    if len(current_word) > width:
        raise ValueError(f"Word \"{"".join(str(t) for t in current_word)}\" is wider than {width} chars")
    if len(current_word) + len(buffer) + spaces > width:
        return current_word, [], 0, buffer
    else:
        return buffer + [' ' for _ in range(spaces)] + current_word, [], 0, None


class TextParser:
    def __init__(self):
        self.effect_stack: list[EffectType] = []
        self.colour_stack: list[FullColour] = []

        self.index = 0

        self.state = {}

    def parse(self, string: str) -> Iterator[Texel]:
        while self.index < len(string):
            if self.match(string, "**", "bold", Effects.BOLD):
                pass
            elif self.match(string, "*", "italic", Effects.ITALIC):
                pass
            elif self.match(string, "~~", "strike", Effects.STRIKETHROUGH):
                pass
            elif self.match(string, "__", "underline", Effects.UNDERLINE):
                pass
            elif self.tag(string):
                pass
            elif string[self.index] == '\\':
                self.index += 1
                yield self.texel_char(string[self.index])
                self.index += 1
            else:
                yield self.texel_char(string[self.index])
                self.index += 1

    def tag(self, string: str) -> bool:
        if self.index + 3 > len(string):
            return False
        s = string[self.index:]
        if not s[:2] == "<$":
            return False
        tokens = s[2:].split('>', 1)
        if len(tokens) != 2:
            raise ValueError(f"Failed to parse text \"{string}\": Missing closing '>' at {self.index}")
        token = tokens[0]
        self.index += len(token) + 3
        if not token:
            self.effect_stack.pop()
            self.colour_stack.pop()
        else:
            colour = Colours.NONE
            effects = []
            for item in token.split():
                item = item.upper()
                if '|' in item:
                    fg, bg = item.split('|')
                    fg_colour = Colours[fg] if fg else (
                        Colours(self.colour_stack[-1].foreground) if self.colour_stack else Colours.NONE)
                    bg_colour = Colours[bg] if bg else (
                        Colours(self.colour_stack[-1].background) if self.colour_stack else Colours.NONE)
                    colour = fg_colour | bg_colour
                else:
                    effects.append(Effects[item])
            self.colour_stack.append(colour)
            self.effect_stack.append(EffectType(*(e.value for e in effects)))
        return True

    def match(self, string: str, token: str, flag: str, effect: EffectType) -> bool:
        if self.index + len(token) > len(string):
            return False
        if not string[self.index: self.index + len(token)] == token:
            return False
        state = self.state[flag] = not self.state.get(flag, False)
        self.index += len(token)
        if state:
            self.effect_stack.append(effect)
        elif self.effect_stack.pop() != effect:
            raise ValueError(f"Failed to parse text \"{string}\": Missing closing <{flag}> at {self.index}")
        return True

    def texel_char(self, char: str) -> Texel:
        if not self.effect_stack and not self.colour_stack:
            return Texel(char)
        return Texel(
            char,
            Style(
                self.colour_stack[-1] if self.colour_stack else Colours.NONE,
                EffectType(*itertools.chain.from_iterable(ef.tokens for ef in self.effect_stack))
            )
        )


def text_parse(string: str) -> Iterator[Texel]:
    return TextParser().parse(string)


def text_strip(string: str) -> str:
    return textwrap.dedent(string).removeprefix('\n').removesuffix('\n')
