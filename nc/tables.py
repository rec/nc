from . import juce, wikipedia


def get_color(c):
    return _CANONICAL.get(_to_canonical(c))


def get_name(c):
    return _NAMES.get(c)


def color_names():
    return iter(_COLORS)


def to_triplet(color):
    rg, b = color // 256, color % 256
    r, g = rg // 256, rg % 256
    return r, g, b


def scale(color):
    return tuple(c / 255 for c in color)


def unscale(color):
    return tuple(round(c * 255) for c in color)


def _to_canonical(name):
    return ''.join(i for i in name.lower() if i not in _DISALLOWED)


_DISALLOWED = set(' _-\'".=')


def _one_table(color_list):
    colors, names, canonical = {}, {}, {}
    for name, color in color_list.items():
        color255 = to_triplet(color)
        cname = _to_canonical(name)
        colors[name] = canonical[cname] = color255, scale(color255)
        names.setdefault(color255, []).append(name)

    def name_key(name):
        # Sort first by length, then alphabetically
        return len(name), name.lower()

    for k, v in names.items():
        names[k] = sorted(v, key=name_key)[0]

    return colors, names, canonical


def _make_tables():
    colors, names, canonical = _one_table(wikipedia.COLORS)

    juce_tables = [{}, {}]
    for k, v in juce.COLORS.items():
        table = juce_tables[k in juce.SECONDARY_NAMES]
        k = k.capitalize()
        table[k] = v
        table[k.replace('grey', 'gray')] = v

    for i in 1, 0:
        jcolors, jnames, jcanonical = _one_table(juce_tables[i])
        colors.update(jcolors)
        names.update(jnames)
        canonical.update(jcanonical)

    return colors, names, canonical


_DISALLOWED = set(' _-\'".=')
_COLORS, _NAMES, _CANONICAL = _make_tables()
