"""Functions that depend on the juce + wikipedia NameColors"""

from .schemes import juce, wikipedia
from . import util


def get_color(c):
    return _CANONICAL.get(util.canonical_name(c))


def get_name(c):
    return _NAMES.get(c)


def color_names():
    return iter(_COLORS)


def _make_tables():
    colors, names, canonical = util.one_table(wikipedia.COLORS)

    juce_tables = [{}, {}]
    for k, v in juce.COLORS.items():
        table = juce_tables[k in juce.SECONDARY_NAMES]
        k = k.capitalize()
        table[k] = v
        table[k.replace('grey', 'gray')] = v

    for i in 1, 0:
        jcolors, jnames, jcanonical = util.one_table(juce_tables[i])
        colors.update(jcolors)
        names.update(jnames)
        canonical.update(jcanonical)

    return colors, names, canonical


_COLORS, _NAMES, _CANONICAL = _make_tables()
