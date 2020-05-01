# From https://jonasjacek.github.io/colors/
# See also https://misc.flogisoft.com/bash/tip_colors_and_formatting
# https://vim.fandom.com/wiki/Xterm256_color_names_for_console_Vim
from . import _terminal256


def fg(code):
    return 38, 5, code


def bg(code):
    return 48, 5, code


_COLORS = (
    ('Black', (0, 0, 0)),
    ('Red', (205, 0, 0)),
    ('Green', (0, 205, 0)),
    ('Yellow', (205, 205, 0)),
    ('Blue', (0, 0, 238)),
    ('Magenta', (205, 0, 205)),
    ('Cyan', (0, 205, 205)),
    ('White', (229, 229, 229)),
    ('Bright Black', (127, 127, 127)),
    ('Bright Red', (255, 0, 0)),
    ('Bright Green', (0, 255, 0)),
    ('Bright Yellow', (255, 255, 0)),
    ('Bright Blue', (92, 92, 255)),
    ('Bright Magenta', (255, 0, 255)),
    ('Bright Cyan', (0, 255, 255)),
    ('Bright White', (255, 255, 255)),
) + _terminal256.COLORS

assert len(_COLORS) == 256

COLORS = {k: v for k, v in _COLORS}
CODES = {k: i for i, (k, v) in enumerate(_COLORS)}
PRESERVE_CAPITALIZATION = True
