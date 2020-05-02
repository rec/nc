from . import terminal
import subprocess
import sys
import time

DEFAULT_COLUMNS = 64


def run(context, demo, print, use_none=True, reverse=False):
    if not context.count:
        raise ValueError('Terminal does not support colors')

    colors = list(context.colors.values())
    if use_none:
        colors.insert(0, None)

    for c1 in colors:
        for c2 in colors:
            fg, bg = (c1, c2) if reverse else (c2, c1)
            with context(fg, bg, print):
                demo(fg, bg)


def long_demo(lines_per_second=32, print=print, sleep=time.sleep, count=None):
    sleep_time = lines_per_second and (1 / lines_per_second)

    def demo(fg, bg):
        print()
        print(fg, bg, sep=', ', end='')
        sleep_time and sleep and sleep(sleep_time)

    run(terminal.Context(count), demo, print)


def point_demo(print=print, count=None, columns=None):
    if not columns:
        try:
            _, columns = subprocess.check_output(['stty', 'size']).split()
            columns = int(columns)
        except Exception:
            columns = DEFAULT_COLUMNS

    context = terminal.Context(count)
    chars = context.count
    while chars > columns:
        chars //= 2

    i = 0

    def demo(fg, bg):
        nonlocal i
        i += 1

        print('•', end='')
        if i % chars:
            sys.stdout.flush()
        else:
            context.print_codes(print=print)
            print()
            time.sleep(0.05)

    run(context, demo, print, False)


if __name__ == '__main__':  # pragma: no cover
    point_demo()
