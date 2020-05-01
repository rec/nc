from .colors import Colors
import contextlib
import functools
import subprocess
import time

TERMINAL_ENVIRONMENT_VAR = '_NC_TERMINAL_COLOR_COUNT'


def context(fg=None, bg=None, print=print, count=None):
    return Context(count)(fg, bg, print)


def demo(lines_per_second=32, print=print, sleep=time.sleep, count=None):
    sleep_time = lines_per_second and (1 / lines_per_second)
    context = Context(count)

    items = [('None', None)] + list(context.colors.items())

    for n1, c1 in items:
        for n2, c2 in items:
            with context(c2, c1, print):
                print()
                print(n1, n2, sep=', ', end='')
                sleep_time and sleep and sleep(sleep_time)
    print()


@functools.lru_cache()
def color_count():
    cmd = 'tput', 'colors'
    try:
        count = int(subprocess.check_output(cmd, stderr=subprocess.STDOUT))
    except (FileNotFoundError, subprocess.CalledProcessError):
        return 0

    if count >= 256:
        return 256
    elif count >= 16:
        return 16
    elif count >= 8:
        return 8
    return 0


@functools.lru_cache()
class Context:
    def __init__(self, count=None):
        self.count = color_count() if count is None else count
        self.colors = Colors('terminal%d' % count) if count else None
        scheme = self.colors._schemes[0] if count else {}
        self.CODES = scheme.get('CODES')
        self.fg = scheme.get('fg')
        self.bg = scheme.get('bg')

    def __bool__(self):
        return bool(self.colors)

    @contextlib.contextmanager
    def __call__(self, fg=None, bg=None, print=print):
        def print_codes(*codes):
            result = '\33[%sm' % ';'.join(str(c) for c in codes)
            print(result, end='')

        def color_codes(color, coder):
            closest = self.colors.closest(color)
            code = self.CODES[str(closest)]
            print_codes(*coder(code))

        if self.CODES:
            if fg:
                color_codes(fg, self.fg)
            if bg:
                color_codes(bg, self.bg)

        yield

        if self.CODES and (fg or bg):
            print_codes(0)


if __name__ == '__main__':  # pragma: no cover
    demo()
