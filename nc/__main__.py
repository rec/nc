from nc import Color
from nc import terminal
import argparse
import nc
import sys

DEFAULT_SPEED = 40


def main(sys_args=None, print=print, color_count=None):
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest='command')

    sp.add_parser('all', help=_HELP_ALL)

    c = sp.add_parser('color', help=_HELP_COLOR)
    c.add_argument('colors', nargs='+', help=_HELP_COLOR)

    t = sp.add_parser('terminal', help=_HELP_TERM)
    t.add_argument(
        '-s', '--speed', default=DEFAULT_SPEED, type=int, help=_HELP_SPEED
    )
    t.add_argument('-c', '--colors', help=_HELP_COLORS)

    args = parser.parse_args(sys_args)
    if not args.command:
        args.command = 'terminal'
        # See https://stackoverflow.com/questions/46963172
        args.speed = DEFAULT_SPEED
        args.colors = None

    if args.command == 'terminal':
        return terminal.demo(args.speed, print=print, count=args.colors)

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
_HELP_COLORS = 'How many terminal colors to use?  Defaults to a good guess'
_HELP_COMMAND = 'Which command to execute'
_HELP_ALL = 'List all colors'
_HELP_COLOR = 'Names and values for colors'
_HELP_SPEED = 'Terminal demo speed in lines per second'
_HELP_TERM = 'Demonstrate terminal colors'


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
