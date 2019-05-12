from .wikipedia import wikipedia_colors
import datetime
import sys

HEADER = """# This file was automatically generated on {timestamp}
# by script {script} from the Wikipedia English color pages.

COLORS = {{"""

FOOTER = '}'

SPECIAL_COLORS = {
    ('Peach', 0xFFCBA4): 'Deep peach',
    ('Vermilion', 0xD9381E): 'Medium vermillion',
    ('Tea rose', 0xF88379): 'Tea rose orange',
}


def get_name(color):
    name = color['name'].strip()
    if name.startswith('[['):
        name = name[2:]
    if name.endswith(']]'):
        name = name[:-2]
    return name.split('|')[-1].strip().replace("'", "\\'")


def run_all(colors=None):
    timestamp = datetime.datetime.now().isoformat()
    script = sys.argv[0]
    print(HEADER.format(**locals()))
    colors = wikipedia_colors() if colors is None else colors
    for color in colors:
        name = get_name(color)
        hex = color['hex'].strip().upper()
        name = SPECIAL_COLORS.get((name, int(hex, 16)), name)
        print("    '{name}': 0x{hex},".format(**locals()))
    print(FOOTER)


if __name__ == '__main__':
    run_all()
