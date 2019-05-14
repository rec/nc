from . import util
import numbers


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
        return tuple(util.from_int(i) for i in c.split(','))

    h = util.from_hex(c)
    if h is not None:
        return util.to_rgb(h)

    try:
        n = int(c)
    except Exception:
        raise ValueError('Do not understand color name %s' % c)

    return n, n, n
