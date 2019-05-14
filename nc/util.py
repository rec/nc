"""Functions that are not dependent on a specific NamedColors"""

import numbers
import string

_ALLOWED = set(string.ascii_letters + string.digits)


def to_rgb(color):
    rg, b = color // 256, color % 256
    r, g = rg // 256, rg % 256
    return r, g, b


def from_hex(s):
    for prefix in '0x', '#':
        if s.startswith(prefix):
            return int(s[len(prefix) :], 16)


def from_int(s):
    h = from_hex(s)
    return int(s) if h is None else h


def canonical_name(name):
    return ''.join(i for i in name.lower() if i in _ALLOWED)


def to_color(c):
    """Try to coerce the argument into an rgb color"""
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

    if ',' in c:
        c = c.lstrip('(').rstrip(')').lstrip('[').rstrip(']')
        return tuple(from_int(i) for i in c.split(','))

    h = from_hex(c)
    if h is not None:
        return to_rgb(h)

    try:
        n = int(c)
    except Exception:
        raise ValueError('Do not understand color name %s' % c)

    return n, n, n
