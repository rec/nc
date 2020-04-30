from .windows_console import COLORS  # noqa: F401


def fg(code):
    return (code,)


def bg(code):
    return (code + 10,)


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
