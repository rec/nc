"""
https://serverfault.com/a/91873
"""

from . import wikipedia
from nc.palette.terminal16 import xterm
import nc
import safer

FILE = wikipedia.PALETTE_DIR / '_terminal256.py'

COLORS = nc.Colors('juce', 'x11', 'html', 'pwg')
old_print = print


def write_256():
    with safer.printer(FILE) as print:
        wikipedia.print_header('an algorithm', print)
        print('COLORS = (')
        count = 0

        cube = range(0, 256, 51)  # (0, 95, 135, 175, 215, 255)
        colors_seen = set(xterm.COLORS)

        def add_name(r, g, b):
            color = COLORS.closest((r, g, b))
            name = str(color)
            index = 0
            while name in colors_seen:
                name = '%s %s' % (color, chr(index + ord('B')))
                index += 1
            colors_seen.add(name)
            print(f"    ('{name}', ({r}, {g}, {b})),")
            nonlocal count
            count += 1

        for r in cube:
            for g in cube:
                for b in cube:
                    add_name(r, g, b)

        for i in range(12, 248, 10):
            add_name(i, i, i)

        print(')')
        print()
        print('PRESERVE_CAPITALIZATION = True')

    old_print('count =', count)


if __name__ == '__main__':
    write_256()
