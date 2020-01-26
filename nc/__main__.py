from nc import Color, COLORS
from nc import terminal
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest='command')

    sp.add_parser('all', help=_HELP_ALL)

    c = sp.add_parser('color', help=_HELP_COLOR)
    c.add_argument('colors', nargs='+', help=_HELP_COLOR)

    t = sp.add_parser('terminal', help=_HELP_TERM)
    t.add_argument('speed', default=40, type=int, help=_HELP_SPEED)

    args = parser.parse_args()
    args.command = args.command or 'terminal'

    if args.command == 'terminal':
        return terminal.demo(getattr(args, 'speed', 40))

    errors = []
    if args.command == 'all':
        _, colors = zip(*sorted(COLORS.items()))
    else:
        colors = []
        print(args.command, dir(args))
        for c in args.colors:
            try:
                colors.append(Color(c))
            except ValueError:
                errors.append(c)

    if errors:
        print('Do not understand:', *errors, file=sys.stderr)

    if not colors:
        print('No valid colors specified!', file=sys.stderr)
        sys.exit(-1)

    for color in colors:
        print('%s: %s' % (color, tuple(color)))


COMMANDS = 'all', 'colors', 'terminal'
_HELP_COMMAND = 'Which command to execute'
_HELP_ALL = 'List all colors'
_HELP_COLOR = 'Names and values for colors'
_HELP_SPEED = 'Terminal demo speed in lines per second'
_HELP_TERM = 'Demonstrate terminal colors'


if __name__ == '__main__':
    main()
