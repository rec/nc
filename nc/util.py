"""Functions that are not dependent on a specific NameColors"""


def to_triplet(color):
    rg, b = color // 256, color % 256
    r, g = rg // 256, rg % 256
    return r, g, b


def scale(color):
    return tuple(c / 255 for c in color)


def unscale(color):
    return tuple(round(c * 255) for c in color)


def from_hex(s):
    for prefix in '0x', '#':
        if s.startswith(prefix):
            return int(s[len(prefix) :], 16)


def from_number(s):
    h = from_hex(s)
    return float(s) if h is None else h


def canonical_name(name):
    return ''.join(i for i in name.lower() if i not in _DISALLOWED)


_DISALLOWED = set(' _-\'".=')


def one_table(color_list):
    colors, names, canonical = {}, {}, {}
    for name, color in color_list.items():
        color255 = to_triplet(color)
        cname = canonical_name(name)
        colors[name] = canonical[cname] = color255, scale(color255)
        names.setdefault(color255, []).append(name)

    def name_key(name):
        # Sort first by length, then alphabetically
        return len(name), name.lower()

    for k, v in names.items():
        names[k] = sorted(v, key=name_key)[0]

    return colors, names, canonical
