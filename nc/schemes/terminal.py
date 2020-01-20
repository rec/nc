import contextlib
import time

COLORS = {
    'Black': (1, 1, 1),
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
    'Black': (30, 40),
    'Red': (31, 41),
    'Green': (32, 42),
    'Yellow': (33, 43),
    'Blue': (34, 44),
    'Magenta': (35, 45),
    'Cyan': (36, 46),
    'White': (37, 47),
    'Bright black': (90, 100),
    'Bright red': (91, 101),
    'Bright green': (92, 102),
    'Bright yellow': (93, 103),
    'Bright blue': (94, 104),
    'Bright magenta': (95, 105),
    'Bright cyan': (96, 106),
    'Bright white': (97, 107),
}


def _closest(color):
    def dist(c):
        return sum(abs(i - j) for i, j in zip(c, color))

    closest = sorted((dist(c), n) for n, c in COLORS.items())[0][1]
    return CODES[closest]


@contextlib.contextmanager
def color_context(fg=None, bg=None, print=print):
    fg = fg and _closest(fg)[0] or 0
    bg = bg and _closest(bg)[1] or 0
    if fg or bg:
        print('\33[%d;%dm' % (fg, bg), end='')
    try:
        yield
    finally:
        if fg or bg:
            print('\33[0;0m', end='')


def demo(lines_per_second=32):
    sleep_time = 1 / lines_per_second

    for n1, c1 in COLORS.items():
        for n2, c2 in COLORS.items():
            with color_context(c2, c1):
                print()
                print(n2, n1, sep=', ', end='')
                time.sleep(sleep_time)
    print()


if __name__ == '__main__':
    demo()
