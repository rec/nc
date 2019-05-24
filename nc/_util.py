"""Functions that are not dependent on a specific NamedColors"""

import numbers


def to_rgb(color):
    rg, b = color // 256, color % 256
    r, g = rg // 256, rg % 256
    return r, g, b


def to_color(c):
    """Try to coerce the argument into an rgb color"""
    try:
        result = _to_color(c)
    except Exception:
        raise ValueError('Do not understand color %s' % c)

    if len(result) == 3:
        return result

    raise ValueError('Must be length 3')


def _to_color(c):
    if not c:
        return 0, 0, 0

    if c is True:
        return 0xFF, 0xFF, 0xFF

    if isinstance(c, numbers.Number):
        return to_rgb(c)

    if isinstance(c, tuple):
        return c

    if isinstance(c, list):
        return tuple(c)

    assert isinstance(c, str)
    if ',' in c:
        if c.startswith('(') and c.endswith(')'):
            c = c[1:-1]
        elif c.startswith('[') and c.endswith(']'):
            c = c[1:-1]
        return tuple(_from_int(i) for i in c.split(','))

    return to_rgb(_from_int(c))


def _from_int(s):
    s = s.strip()
    for prefix in '0x', '#':
        if s.startswith(prefix):
            p = s[len(prefix) :].lstrip('0')
            return int(p or '0', 16)
    return int(s)
