from nc.palette import juce, wikipedia, x11

X11 = 'https://en.wikipedia.org/wiki/X11_color_names#Color_name_chart'
JUCE = (
    'https://github.com/juce-framework/JUCE/blob/master/'
    'modules/juce_graphics/colour/juce_Colours.cpp'
)
WIKI = 'https://en.wikipedia.org/wiki/List_of_colors:_{}%E2%80%93{}'
WIKIS = WIKI.format('A', 'F'), WIKI.format('G', 'M'),  WIKI.format('N', 'Z')

X_COLORS = {i.lower() for i in x11.COLORS}
J_COLORS = {i.lower() for i in juce.COLORS}
W_COLORS = {i.lower() for i in wikipedia.COLORS}


def color_source(name):
    name = name.lower()
    ng = name.replace('gray', 'grey')
    if name in X_COLORS:
        return X_COLORS
    if ng in J_COLORS:
        return JUCE
    if name in W_COLORS or ng in W_COLORS:
        ch = name[0].upper()
        if 'A' <= ch <= 'F':
            return WIKIS[0]
        if 'G' <= ch <= 'M':
            return WIKIS[1]
        if 'N' <= ch <= 'Z':
            return WIKIS[2]
