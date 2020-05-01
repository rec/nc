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

    # items = [('None', None)] + list(context.colors.items())
    colors = context.colors.values()

    for bg in colors:
        for fg in colors:
            with context(fg, bg, print):
                print()
                print(fg, bg, sep=', ', end='')
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
        self.colors = Colors('terminal%s' % count) if count else None
        scheme = self.colors._schemes[0] if count else {}
        self.CODES = scheme.get('CODES')
        self.fg = scheme.get('fg')
        self.bg = scheme.get('bg')

    def __bool__(self):
        return bool(self.colors)

    @contextlib.contextmanager
    def __call__(self, fg=None, bg=None, print=print):
        def print_codes(*codes):
            result = '\x1b[%sm' % ';'.join(str(c) for c in codes)
            print(result, end='')

        def color_codes(color, coder):
            if not color:
                return ()
            closest = self.colors.closest(color)
            code = self.CODES[str(closest)]
            return coder(code)

        if self.CODES and (fg or bg):
            codes = color_codes(fg, self.fg) + color_codes(bg, self.bg)
            print_codes(*codes)

        yield

        if self.CODES and (fg or bg):
            print_codes()


if __name__ == '__main__':  # pragma: no cover
    demo()
