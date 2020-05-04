import collections
import math
import numbers

COLOR_TUPLE = collections.namedtuple('Color', 'r g b')


class Color(COLOR_TUPLE):
    """DOX HERE"""

    COLORS = None

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

    def closest(self):
        """
        Return the closest named color to `self`.  This is quite slow,
        particularly in large schemes.
        """
        return self.COLORS.closest(self)

    def distance2(self, other):
        """Return the square of the distance between this and anotther color"""
        d = (i - j for i, j in zip(self, other))
        return sum(i * i for i in d)

    def distance(self, other):
        return math.sqrt(self.distance2(other))

    @property
    def rgb(self):
        return self.r * 0x10000 + self.g * 0x100 + self.b


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
