from nc import Color
from nc import demo
from nc import terminal
import argparse
import nc
import sys


def main(sys_args=None, color_count=None):
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest='command')

    sp.add_parser('all', help=_HELP_ALL)

    c = sp.add_parser('color', help=_HELP_COLOR)
    c.add_argument('colors', nargs='+', help=_HELP_COLOR)

    t = sp.add_parser('terminal', help=_HELP_TERM)
    t.add_argument('-c', '--colors', help=_HELP_COLORS)
    t.add_argument('-l', '--long', action='store_true', help=_HELP_LONG)
    t.add_argument('-r', '--reverse', action='store_true', help=_HELP_REVERSE)

    if sys_args is None:
        sys_args = sys.argv[1:]

    if all(a.startswith('-') for a in sys_args):
        sys_args.insert(0, 'terminal')

    args = parser.parse_args(sys_args)
    if args.command == 'terminal':
        colors = int(args.colors) if args.colors else args.colors
        return demo.demo(colors, args.reverse, args.long)

    errors = []

    if args.command == 'all':
        _, colors = zip(*sorted(nc.items()))
    else:
        colors = []
        for c in args.colors:
            try:
                colors.append(Color(c))
            except ValueError:
                errors.append(c)

    if errors:
        print('Do not understand:', *errors, file=sys.stderr)

    if not colors:
        print('No valid colors specified!', file=sys.stderr)
        return -1

    context = terminal.Context(color_count)
    if context:
        for color in colors:
            background = nc.black if sum(color) >= 0x180 else nc.white
            with context(color, background, print):
                print('\n%s: %s' % (color, tuple(color)), end='')
        print('\n')

    else:
        for color in colors:
            print('%s: %s' % (color, tuple(color)))


COMMANDS = 'all', 'colors', 'terminal'
_HELP_ALL = 'List all colors'
_HELP_COLOR = 'Names and values for colors'
_HELP_COLORS = (
    'How many terminal colors to use?  Defaults to the terminal defaults'
)
_HELP_COMMAND = 'Which command to execute'
_HELP_LONG = 'Print the long names of colors'
_HELP_REVERSE = 'Reverse foreground and background'
_HELP_TERM = 'Demonstrate terminal colors'


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
