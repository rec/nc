from . import terminal
import time


def demo(lines_per_second=32, print=print, sleep=time.sleep, count=None):
    sleep_time = lines_per_second and (1 / lines_per_second)
    context = terminal.Context(count)

    colors = [None] + list(context.colors.values())

    for bg in colors:
        for fg in colors:
            with context(fg, bg, print):
                print()
                print(fg, bg, sep=', ', end='')
                sleep_time and sleep and sleep(sleep_time)
    print()


if __name__ == '__main__':  # pragma: no cover
    demo()
