from nc import Color, COLORS
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('colors', nargs='*')
    parser.add_argument(
        '-a', '--all', action='store_true', help='List all colors'
    )
    args = parser.parse_args()

    errors = []
    if args.all:
        _, colors = zip(*sorted(COLORS.items()))
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
        print(file=sys.stderr)
        print(parser.format_help(), file=sys.stderr)
        sys.exit(-1)

    for color in colors:
        print('%s: %s' % (color, tuple(color)))


if __name__ == '__main__':
    main()
