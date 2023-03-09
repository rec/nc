from nc.palette import juce, wikipedia, x11

X11 = 'https://en.wikipedia.org/wiki/X11_color_names#Color_name_chart'
JUCE = (
    'https://github.com/juce-framework/JUCE/blob/master/'
    'modules/juce_graphics/colour/juce_Colours.cpp'
)
WIKI = 'https://en.wikipedia.org/wiki/List_of_colors:_{}%E2%80%93{}'


def color_source(name):
    if name in x11.COLORS:
        return
    if name in juce.COLORS:
        return JUCE
    if name in wikipedia.COLORS:
        ch = name[0].upper()
        if 'A' <= ch <= 'F':
            return WIKI.format('A', 'F')
        if 'G' <= ch <= 'M':
            return WIKI.format('G', 'M')
        if 'N' <= ch <= 'Z':
            return WIKI.format('N', 'Z')
