from . import terminal
import subprocess
import sys
import time

DEFAULT_COLUMNS = 64
DEMO_CHAR = '•'


class Demo:
    def __init__(self, terminal_colors, reverse, steps=0):
        self.context = terminal.Context(terminal_colors)
        self.reverse = reverse
        self.steps = steps

    def demo(self, is_long):
        if not self.context:
            print('Your terminal does not seem to support colors')
            print('Try `pync all` to see a list of colors')
            return -1

        return self.long() if is_long else self.short()

    def long(self):
        self._run(self._one_long, True)

    def short(self):
        cmd = ['stty', 'size']
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        except Exception:
            columns = DEFAULT_COLUMNS
        else:
            _, columns = out.split()
            columns = int(columns)

        self.chars = len(self.context)
        while self.chars > columns:
            self.chars //= 2

        self._run(self._one_short, False)

    def _one_long(self, fg, bg):
        print()
        print(fg, bg, sep=', ', end='')
        sleep_time = 0.01
        sleep_time and time.sleep(sleep_time)

    def _one_short(self, fg, bg):
        print(DEMO_CHAR, end='')
        if (self.count + 1) % self.chars:
            sys.stdout.flush()
        else:
            self.context.print_codes(print=print)
            print()
            sleep_time = 0.05
            sleep_time and time.sleep(sleep_time)

    def _run(self, demo, use_none):
        colors = list(self.context.colors.values())
        if use_none:
            colors.insert(0, None)

        self.count = 0
        for c1 in colors:
            for c2 in colors:
                fg, bg = (c1, c2) if self.reverse else (c2, c1)
                with self.context(fg, bg, print):
                    demo(fg, bg)
                self.count += 1
                if self.steps and self.steps <= self.count:
                    return


def demo(terminal_colors, reverse, long, steps=0):
    return Demo(terminal_colors, reverse, steps).demo(long)
