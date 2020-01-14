import collections
import numbers

COLOR_TUPLE = collections.namedtuple('Color', 'r g b')


class Color(COLOR_TUPLE):
    COLORS = None

    def __str__(self):
        return (self.COLORS._rgb_to_name.get(self)
                or '({}, {}, {})'.format(*self))

    def __repr__(self):
        name = str(self)
        if not name.startswith('('):
            return "Color('%s')" % name
        return 'Color' + name

    @property
    def rgb(self):
        return self.r * 0x10000 + self.g * 0x100 + self.b

    @classmethod
    def make(cls, *args):
        if not args:
            return cls.COLORS._default

        c = args[0] if len(args) == 1 else args
        if isinstance(c, cls):
            return c

        if isinstance(c, numbers.Number):
            return cls(*_int_to_tuple(c))

        if not isinstance(c, str):
            if len(c) == 3:
                return cls(*c)
            raise ValueError('Color needs exactly three components: r, g, b')

        try:
            return cls.COLORS[c]
        except KeyError:
            pass

        if ',' not in c:
            i = _string_to_int(c)
            return cls(*_int_to_tuple(i))

        if c.startswith('(') and c.endswith(')'):
            c = c[1:-1]
        if c.startswith('[') and c.endswith(']'):
            c = c[1:-1]

        components = [_string_to_int(i) for i in c.split(',')]
        return cls(*components)


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
