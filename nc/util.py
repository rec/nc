"""Functions that are not dependent on a specific NamedColors"""

import string


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


_ALLOWED = set(string.ascii_letters + string.digits)
