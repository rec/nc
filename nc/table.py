"""
Table of named colors
"""

import numbers
from . import tables


class Table:
    def __init__(self, normal=True):
        self.normal = normal

    def to_string(self, color, use_hex=False):
        """
        :param tuple color: an RGB 3-tuple of integer colors
        :returns: a string name for this color

        ``to_color(to_string(c)) == c`` is guaranteed to be true (but
        the reverse is not true, because to_color is a many-to-one
        function).
        """
        if self.normal:
            c = tables.unscale(color)
        else:
            color = c = tuple(color)

        if use_hex:
            return '#%02x%02x%02x' % c

        return tables.get_name(c) or str(color)

    def to_color(self, c):
        """Try to coerce the argument into a color - a 3-tuple of numbers-"""
        if isinstance(c, numbers.Number):
            return c, c, c
        if not c:
            raise ValueError('Cannot create color from empty "%s"' % c)
        if isinstance(c, tuple):
            return c
        if isinstance(c, list):
            return tuple(c)
        if not isinstance(c, str):
            raise ValueError('Do not understand color type %s' % c)

        colors = tables.get_color(c)
        if colors:
            return colors[self.normal]

        if ',' in c:
            c = c.lstrip('(').rstrip(')').lstrip('[').rstrip(']')
            return tuple(_from_number(i) for i in c.split(','))

        h = _from_hex(c)
        if h is not None:
            t = tables.to_triplet(h)
            return tables.scale(t) if self.normal else t

        try:
            n = float(c) if self.normal else int(c)
            return n, n, n
        except:
            raise ValueError('Do not understand color name %s' % c)

    def toggle(self, s):
        """
        Toggle back and forth between a name and a tuple representation.

        :param str s: a string which is either a text name, or a tuple-string:
                      a string with three numbers separated by commas

        :returns: if the string was a text name, return a tuple.  If it's a
                  tuple-string and it corresponds to a text name, return the
                  text name, else return the original tuple-string.
        """
        is_numeric = ',' in s or s.startswith('0x') or s.startswith('#')
        c = self.to_color(s)
        return self.to_string(c) if is_numeric else str(c)

    def __contains__(self, x):
        """Return true if this string or integer tuple appears in the table"""
        try:
            if not isinstance(x, str):
                x = self.to_string(x)
            return bool(tables.get_colors(x))
        except:
            return False

    def __iter__(self):
        return tables.color_names()


def _from_hex(s):
    for prefix in '0x', '#':
        if s.startswith(prefix):
            return int(s[len(prefix):], 16)


def _from_number(s):
    h = _from_hex(s)
    return float(s) if h is None else h
