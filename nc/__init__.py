"""
# 🎨 `nc`: Named colors in Python 🎨

--

The module `nc` collects named colors in Python.

There are two ways to use `nc`.

The simple way is as an intuitive and forgiving interface to a
collection of over 2000 named colors, put together from almost 20 color
palettes scraped from the Internet.

In the simplest use, it's a collection of about 1700 colors, some
scraped from the Wikipedia (which includes some very strange colors),
with a neat API.

For more precise use, color collections can be put together from schemes
built into `nc` (currently `html`, `juce`, `pwg`, `wikipedia`, `x11`),
or from custom color schemes created by the user.

There is also a collection of [color swatches](swatches/) for the default
color collection.

# Examples

    import nc

    for c in nc.red, nc.light_green, nc.DarkGrey, nc['PUCE']:
        print(c, '=', *c)

    # Prints:
    #   Red = 255 0 0
    #   Light green = 144 238 144
    #   Dark grey = 85 85 85
    #   Puce = 204 136 153

    # Colors have red, green, blue or r, g, b components
    assert nc.yellow.red == nc.yellow.r == 0
    assert nc.yellow.green == nc.yellow.g == 255
    assert nc.yellow.blue == nc.yellow.b == 255

    # Lots of ways to reach colors
    assert nc.black == nc(0, 0, 0) == nc('0, 0, 0') == nc('(0, 0, 0)') == nc(0)

    # ``nc`` looks like a dict
    assert nc.red == nc['red'] == nc['RED']
    for name, color in nc.items():
        print(name, '=', *color)

    # Prints:
    #   Absolute Zero = 0 72 186
    #   Acid green = 176 191 26
    #   Aero = 124 185 232
    #   ... many more

    # closest() function

    from random import randrange
    for i in range(8):
        c1 = randrange(256), randrange(256), randrange(256)
        c2 = nc.closest(c1)
        print(c1, 'is closest to', c2, *c2)

    # Prints:
    #   (193, 207, 185) is closest to Honeydew 3 = 193 205 193
    #   (181, 162, 188) is closest to Lilac = 200 162 200
    #   (122, 110, 250) is closest to Slate blue 1 = 131 111 255
    #   (56, 218, 180) is closest to Turquoise = 64 224 208
"""
from . import colors as _colors
from . import color as _color
from functools import cached_property
from typing import Iterator
import sys

_DEFAULT_PALETTES = 'wikipedia', 'x11', 'juce'


class NC:
    colors = _colors
    Colors = _colors.Colors

    @cached_property
    def COLORS(self) -> _colors.Colors:
        """The underlying instance of `nc.colors.Colors with all the colors"""
        return self.Colors(*_DEFAULT_PALETTES)

    def __getattr__(self, name) -> _colors.Colors:
        """Gets a color as a name attribute"""
        try:
            return globals()[name]
        except KeyError:
            pass
        return getattr(self.COLORS, name)

    def __call__(self, *args, **kwargs) -> _colors.Colors:
        """"""
        return self.COLORS(*args, **kwargs)

    def __getitem__(self, name) -> _colors.Colors:
        """Gets a color by name"""
        return self.COLORS[name]

    def __contains__(self, x) -> bool:
        """Return true if this string name, tuple or color is in this list"""
        return x in self.COLORS

    def __len__(self) -> int:
        """Returns the number of colors"""
        return len(self.COLORS)

    def __iter__(self) -> Iterator[_colors.Colors]:
        """Iterate over all the colors in alphabetical order"""
        return iter(self.COLORS)


NamedColors = NC  # for backwards compatibility
NC.__doc__ = __doc__
sys.modules[__name__] = NC()
_color.Color.COLORS = NC.COLORS
