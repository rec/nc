from . import terminal16

fg = terminal16.fg
bg = terminal16.bg

COLORS = {
    'Black': (0, 0, 0),
    'Red': (255, 0, 0),
    'Green': (0, 255, 0),
    'Yellow': (255, 255, 0),
    'Blue': (0, 0, 255),
    'Magenta': (255, 0, 255),
    'Cyan': (0, 255, 255),
    'White': (255, 255, 255),
}

CODES = {c: terminal16.CODES[c] for c in COLORS}
