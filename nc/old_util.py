"""Legacy functions"""

from . import util


def scale(color):
    return tuple(c / 255 for c in color)


def unscale(color):
    return tuple(round(c * 255) for c in color)


def from_number(s):
    # DEPRECATED
    h = util.from_hex(s)
    return float(s) if h is None else h


def one_table(color_list):
    colors, names, canonical = {}, {}, {}
    for name, color in color_list.items():
        color255 = util.to_rgb(color)
        cname = util.canonical_name(name)
        colors[name] = canonical[cname] = color255, scale(color255)
        names.setdefault(color255, []).append(name)

    def name_key(name):
        # Sort first by length, then alphabetically
        return len(name), name.lower()

    for k, v in names.items():
        names[k] = sorted(v, key=name_key)[0]

    return colors, names, canonical
