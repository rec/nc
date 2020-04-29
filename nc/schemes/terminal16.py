def fg(code):
    return (code,)


def bg(code):
    return (code + 10,)


COLORS = {
    'Black': (0, 0, 0),
    'Red': (222, 56, 43),
    'Green': (57, 181, 74),
    'Yellow': (255, 199, 6),
    'Blue': (0, 111, 184),
    'Magenta': (118, 38, 113),
    'Cyan': (44, 181, 233),
    'White': (204, 204, 204),
    'Bright black': (128, 128, 128),
    'Bright red': (255, 0, 0),
    'Bright green': (0, 255, 0),
    'Bright yellow': (255, 255, 0),
    'Bright blue': (0, 0, 255),
    'Bright magenta': (255, 0, 255),
    'Bright cyan': (0, 255, 255),
    'Bright white': (255, 255, 255),
}

CODES = {
    'Black': 30,
    'Red': 31,
    'Green': 32,
    'Yellow': 33,
    'Blue': 34,
    'Magenta': 35,
    'Cyan': 36,
    'White': 37,
    'Bright black': 90,
    'Bright red': 91,
    'Bright green': 92,
    'Bright yellow': 93,
    'Bright blue': 94,
    'Bright magenta': 95,
    'Bright cyan': 96,
    'Bright white': 97,
}
