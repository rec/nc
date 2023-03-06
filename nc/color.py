from functools import cached_property
from typing import Tuple
import collections
import colorsys
import math
import numbers

try:
    from typing import Self
except ImportError:
    from typing import Any as Self


COLOR_TUPLE = collections.namedtuple('Color', 'r g b')


class Color(COLOR_TUPLE):
    """A single Color, represented as a named triple of integers in the range
    [0, 256).
    """

    COLORS = None
    GAMMA = 2.5

    def __new__(cls, *args):
        return super().__new__(cls, *_make(cls, args))

    def __str__(self):
        return self.COLORS._rgb_to_name.get(self) or '({}, {}, {})'.format(
            *self
        )

    def __repr__(self):
        name = str(self)
        if not name.startswith('('):
            return "Color('%s')" % name
        return 'Color' + name

    def closest(self) -> Self:
        """
        Return the closest named color to `self`.  This is quite slow,
        particularly in large schemes.
        """
        return self.COLORS.closest(self)

    def distance2(self, other) -> int:
        """Return the square of the distance between this and another color"""
        d = (i - j for i, j in zip(self, other))
        return sum(i * i for i in d)

    def distance(self, other) -> float:
        """Return the distance between this and another color"""
        return math.sqrt(self.distance2(other))

    @cached_property
    def rgb(self) -> int:
        """Return an integer between 0 and 0xFFFFFF combining the components"""
        return self.r * 0x10000 + self.g * 0x100 + self.b

    @cached_property
    def brightness(self) -> float:
        """gamma-weighted average of intensities"""
        return (sum(c ** self.GAMMA for c in self) / 3) ** (1 / self.GAMMA)

    @cached_property
    def hsl(self) -> Tuple[int, int, int]:
        return colorsys.rgb_to_hsl(*self._to())

    @cached_property
    def hsv(self) -> Tuple[int, int, int]:
        return colorsys.rgb_to_hsv(*self._to())

    @cached_property
    def yiq(self) -> Tuple[int, int, int]:
        return colorsys.rgb_to_yiq(*self._to())

    @classmethod
    def from_hsl(cls, h, s, l) -> Self:  # noqa E741
        return cls._from(colorsys.hsl_to_rgb(h, s, l))

    @classmethod
    def from_hsv(cls, h, s, v) -> Self:
        return cls._from(colorsys.hsv_to_rgb(h, s, v))

    @classmethod
    def from_yiq(cls, y, i, q) -> Self:
        return cls._from(colorsys.yiq_to_rgb(y, i, q))

    def _to(self):
        return (i / 255 for i in self)

    @classmethod
    def _from(cls, rgb):
        return cls(*(min(255, int(265 * c)) for c in rgb))


def _make(cls, args):
    if not args:
        return cls.COLORS._default

    a = args[0] if len(args) == 1 else args
    if isinstance(a, numbers.Number):
        return _int_to_tuple(a)

    if not isinstance(a, str):
        if len(a) == 3:
            return tuple(int(i) for i in a)
        raise ValueError(_COLOR_ERROR)

    try:
        return cls.COLORS[a]
    except KeyError:
        pass

    if ',' not in a:
        return _int_to_tuple(_string_to_int(a))

    if a.startswith('(') and a.endswith(')'):
        a = a[1:-1]
    if a.startswith('[') and a.endswith(']'):
        a = a[1:-1]

    return tuple(_string_to_int(i) for i in a.split(','))


def _int_to_tuple(color):
    rg, b = color // 256, color % 256
    r, g = rg // 256, rg % 256
    return r, g, b


def _string_to_int(s):
    s = s.strip()

    for prefix in '0x', '#':
        if s.startswith(prefix):
            p = s[len(prefix) :].lstrip('0')
            return int(p or '0', 16)

    return int(s)


_COLOR_ERROR = 'Colors must have three components: r, g, b'
