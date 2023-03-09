from nc.palette import juce, wikipedia, x11
from . wikipedia import wikitext, SOURCES, WIKI_URL

X11 = 'https://en.wikipedia.org/wiki/X11_color_names#Color_name_chart'
JUCE = (
    'https://github.com/juce-framework/JUCE/blob/master/'
    'modules/juce_graphics/colour/juce_Colours.cpp'
)

WIKIS = SOURCES['wikipedia'][1:]


X_COLORS = {i.lower() for i in x11.COLORS}
J_COLORS = {i.lower() for i in juce.COLORS}
W_COLORS = {i.lower() for i in wikipedia.COLORS}

_PAGES = [None, None, None]


def color_source(name):
    name = name.lower()
    ng = name.replace('gray', 'grey')
    if name in X_COLORS:
        return X_COLORS
    if ng in J_COLORS:
        return JUCE
    if name in W_COLORS:
        return _wiki_url(name)
    if ng in W_COLORS:
        return _wiki_url(ng)


def _wiki_url(name):
    ch = name[0].upper()
    if 'A' <= ch <= 'F':
        w = 0
    elif 'G' <= ch <= 'M':
        w = 1
    elif 'N' <= ch <= 'Z':
        w = 2
    else:
        assert False

    return _wiki_source(w)[name]


def _wiki_source(i):
    if d := _PAGES[i]:
        return d

    d = {}
    for line in wikitext(WIKIS[i]).splitlines():
        old_l = line
        while line and not line.startswith('name='):
            _, _, line = line.partition('|')
        if not line:
            continue
        name, _, rest = line.partition('=')
        if name != 'name' or not rest.startswith('[['):
            continue
        rest, _, _ = rest[2:].partition(']]')
        if not rest:
            continue
        url, _, name = rest.partition('|')
        name = (name or url).lower()
        d[name] = WIKI_URL + url

    _PAGES[i] = d
    return d
