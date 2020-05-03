from . import terminal
import subprocess
import sys
import time

DEFAULT_COLUMNS = 64


class Demo:
    def __init__(self, print, sleep, count, reverse):
        self.print = print
        self.sleep = sleep
        self.context = terminal.Context(count)
        self.reverse = reverse

        if not self.context:
            raise ValueError('Terminal does not support colors')

    def demo(self, is_long):
        return self.long() if is_long else self.short()

    def long(self):
        self.run(self.one_long, True)

    def one_long(self, fg, bg):
        self.print()
        self.print(fg, bg, sep=', ', end='')
        sleep_time = 0.01
        sleep_time and self.sleep and self.sleep(sleep_time)

    def short(self):
        try:
            cmd = ['stty', 'size']
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            _, columns = out.split()
            columns = int(columns)
        except Exception:
            columns = DEFAULT_COLUMNS

        self.chars = self.context.count
        while self.chars > columns:
            self.chars //= 2

        self.run(self.one_short, False)

    def one_short(self, fg, bg):
        print('•', end='')
        if (self.count + 1) % self.chars:
            sys.stdout.flush()
        else:
            self.context.print_codes(print=print)
            print()
            sleep_time = 0.05
            sleep_time and self.sleep and self.sleep(sleep_time)

    def run(self, demo, use_none):
        colors = list(self.context.colors.values())
        if use_none:
            colors.insert(0, None)

        self.count = 0
        for c1 in colors:
            for c2 in colors:
                fg, bg = (c1, c2) if self.reverse else (c2, c1)
                with self.context(fg, bg, self.print):
                    demo(fg, bg)
                self.count += 1


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


def demo(print, sleep, count, reverse, long):
    Demo(print, sleep, count, reverse).demo(long)


if __name__ == '__main__':  # pragma: no cover
    point_demo()
