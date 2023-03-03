"""
# 🎨 `nc`: Named colors 🎨

`nc` names colors.

There are two ways to use `nc`.

The simple way is as an intuitive and forgiving interface to a
collection of over 2000 named colors, put together from almost 20 color
palettes scraped from the Internet.

In the simplest use, it\'s a collection of about 1700 colors, some
scraped from the Wikipedia (which includes some very strange colors),
with a neat API.

For more precise use, color collections can be put together from schemes
built into `nc` (currently `html`, `juce`, `pwg`, `wikipedia`, `x11`),
and from custom color schemes created by the user.

Install `nc` from the command line using
[pip](https://pypi.org/project/pip/):

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
from functools import cached_property
import sys

_DEFAULT_PALETTES = 'wikipedia', 'x11', 'juce'


class NamedColors:
    """NamedColors is a collection of named colors that can act like
    an array or a dictionary.
    """
    colors = _colors
    Colors = _colors.Colors
    _COLORS = None

    @cached_property
    def COLORS(self):
        return self.Colors(*_DEFAULT_PALETTES)

    def __getattr__(self, name):
        try:
            return globals()[name]
        except KeyError:
            pass
        return getattr(self.COLORS, name)

    def __call__(self, *args, **kwargs):
        return self.COLORS(*args, **kwargs)

    def __getitem__(self, name):
        return self.COLORS[name]

    def __contains__(self, x):
        """Return true if this string name appears in the table canonically"""
        return x in self.COLORS

    def __len__(self):
        return len(self.COLORS)

    def __iter__(self):
        """Iterate over all the colors"""
        return iter(self.COLORS)


sys.modules[__name__] = NamedColors()
