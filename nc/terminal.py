from .colors import Colors
import contextlib
import functools
import subprocess
import time

TERMINAL_ENVIRONMENT_VAR = '_NC_TERMINAL_COLOR_COUNT'
SIZES = 256, 16, 8


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

    return next((s for s in SIZES if count >= s), 0)


@functools.lru_cache()
class Context:
    def __init__(self, count=None):
        self.count = color_count() if count is None else count
        if self.count:
            self.colors = Colors('terminal%s' % self.count)
            # Color = self.colors.Color
            scheme = self.colors._schemes[0]
            codes = scheme['CODES']
            self.CODES = {self.colors[k]: v for k, v in codes.items()}
            self.fg = scheme['fg']
            self.bg = scheme['bg']

    def __bool__(self):
        return bool(self.count)

    @contextlib.contextmanager
    def __call__(self, fg=None, bg=None, print=print):
        if not (self.count and (fg or bg)):
            yield
            return

        def print_codes(*codes):
            result = '\x1b[%sm' % ';'.join(str(c) for c in codes)
            print(result, end='')

        def color_codes(color, coder):
            if not color:
                return ()
            closest = self.colors.closest(color)
            try:
                code = self.CODES[closest]
            except KeyError:
                __builtins__['print']('!!!', color, closest, *color, *closest)
                raise
            return coder(code)

        codes = color_codes(fg, self.fg) + color_codes(bg, self.bg)
        print_codes(*codes)
        yield
        print_codes()


if __name__ == '__main__':  # pragma: no cover
    demo()
