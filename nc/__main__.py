from nc import Color
from nc import demo
from nc import terminal
import argparse
import nc
import sys

DEFAULT_COMMAND = 'all'


def main(sys_args, color_count=None):
    args = _parse_args(sys_args)
    if args.command == 'terminal':
        colors = int(args.colors) if args.colors else args.colors
        return demo.demo(colors, args.reverse, args.long)

    errors = []

    if args.command == 'all':
        colors = sorted(nc.items())
    else:
        colors = []
        for c in args.colors:
            try:
                color = Color(c)
                colors.append((str(color), color))
            except ValueError:
                errors.append(c)

    if errors:
        print('Do not understand:', *errors, file=sys.stderr)

    if not colors:
        print('No valid colors specified!', file=sys.stderr)
        return -1

    context = terminal.Context(color_count)
    first = True
    for name, color in colors:
        assert type(name) is str
        assert 'Color' in type(color).__name__, type(color).__name__
        background = nc.black if sum(color) >= 0x180 else nc.white
        msg = '%s%s: %s' % ('' if first else '\n', name, tuple(color))
        first = False
        if context:
            with context(color, background, print):
                print(msg, end='')
        else:
            print(msg, end='')
    print()


def _parse_args(sys_args):
    parser = argparse.ArgumentParser(description=_DESCRIPTION)
    sp = parser.add_subparsers(dest='command')

    sp.add_parser('all', help=_HELP_ALL)

    c = sp.add_parser('color', help=_HELP_COLOR)
    c.add_argument('colors', nargs='+', help=_HELP_COLOR)

    t = sp.add_parser('terminal', help=_HELP_TERMINAL)
    t.add_argument('-c', '--colors', help=_HELP_COLORS)
    t.add_argument('-l', '--long', action='store_true', help=_HELP_LONG)
    t.add_argument('-r', '--reverse', action='store_true', help=_HELP_REVERSE)

    if '-h' not in sys_args and all(a.startswith('-') for a in sys_args):
        sys_args.insert(0, DEFAULT_COMMAND)

    return parser.parse_args(sys_args)


COMMANDS = 'all', 'colors', 'terminal'
_DESCRIPTION = """
pync: Named Color utilities from the `nc` Python library

See https://github.com/rec/nc for more information.
"""
_HELP_ALL = 'List all `nc` colors'
_HELP_COLOR = 'Convert names to colors and back from the command line'
_HELP_COLORS = (
    'How many terminal colors to use. Defaults to the terminal defaults'
)
_HELP_COMMAND = 'Which command to execute: choose from %s' % (
    ', '.join(COMMANDS)
)
_HELP_LONG = 'Print the full names of colors, not just a ' + demo.DEMO_CHAR
_HELP_REVERSE = 'Reverse foreground and background'
_HELP_TERMINAL = 'Print every combination of foreground and background color'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
