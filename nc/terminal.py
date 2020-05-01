from .colors import Colors
from .schemes import terminal16

import contextlib
import time


COLORS = Colors('terminal16')


def _closest(color):
    return terminal16.CODES[str(COLORS.closest(color))]


@contextlib.contextmanager
def color_context(fg=None, bg=None, print=print):
    fg = terminal16.fg(_closest(fg))[0] if fg else 0
    bg = terminal16.bg(_closest(bg))[0] if bg else 0
    if fg or bg:
        print('\33[%d;%dm' % (fg, bg), end='')
    try:
        yield
    finally:
        if fg or bg:
            print('\33[0;0m', end='')


def demo(lines_per_second=32, print=print, sleep=time.sleep):
    sleep_time = lines_per_second and (1 / lines_per_second)

    for n1, c1 in COLORS.items():
        for n2, c2 in COLORS.items():
            with color_context(c2, c1, print=print):
                print()
                print(n2, n1, sep=', ', end='')
                sleep_time and sleep and sleep(sleep_time)
    print()


if __name__ == '__main__':  # pragma: no cover
    demo()
