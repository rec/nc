from .wikipedia import wikipedia
import datetime
import sys

HEADER = """# This file was automatically generated on {}
# by script {}
# from {}.

COLORS = {{"""

NAME = 'the Wikipedia English color pages'
FOOTER = '}'


def run_one(colors, fp, name):
    timestamp = datetime.datetime.now().isoformat()
    header = HEADER.format(timestamp, sys.argv[0], name)
    print(header, file=fp)

    for name, hexname in colors:
        print("    '{}': 0x{},".format(name, hexname))
    print(FOOTER)


def run_all(colors=None):
    colors = wikipedia() if colors is None else colors
    run_one(colors, sys.stdout, NAME)


if __name__ == '__main__':
    run_all()
