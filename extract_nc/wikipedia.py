from . import extract_color
import bs4
import datetime
import pathlib
import requests
import safer
import sys

HEADER = """# This file was automatically generated on {}
# by script {}
# from {}
"""

FOOTER = '}'

WIKI_URL = 'https://en.wikipedia.org/w/index.php?title='
EDIT_STRING = '&action=edit'
_BF = 'List_of_colors:_{0}%E2%80%93{1}'.format
SOURCES = {
    'wikipedia': (
        'the Wikipedia English color pages',
        _BF('A', 'F'),
        _BF('G', 'M'),
        _BF('N', 'Z'),
    ),
    'x11': ('X11 colors', 'X11_color_names&section=2'),
    'pwg': ('PWG 5101.1 colors', 'X11_color_names&section=10'),
}

TABLE_END = '|}\n'
PALETTE_DIR = pathlib.Path(__file__).parents[1] / 'nc' / 'palette'

SPECIAL_COLORS = {
    ('Peach', 0xFFCBA4): 'Deep peach',
    ('Vermilion', 0xD9381E): 'Medium vermillion',
    ('Tea rose', 0xF88379): 'Tea rose orange',
}


def print_header(title, print):
    timestamp = datetime.datetime.now().isoformat()
    header = HEADER.format(timestamp, sys.argv[0], title)
    print(header)


def wikitext(url):
    if not url.startswith(WIKI_URL):
        url = WIKI_URL + url
    if not url.endswith(EDIT_STRING):
        url += EDIT_STRING
    text = requests.get(url).text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    return soup.find(id='wpTextbox1').text


def colors(urls, title, print):
    print_header(title, print)
    print('COLORS = {{')
    for url in urls:
        for line in wikitext(url).splitlines():
            if line == TABLE_END:
                break
            color = extract_color.extract_color(line)
            if not color:
                continue
            if 'hex' in color:
                hexname = color['hex'].strip()
            else:
                rgb = color['r'], color['g'], color['b']
                hexname = ''.join('%02x' % int(c) for c in rgb)
            hexname = hexname.upper()
            name = color['name'].strip()
            if name.startswith('[['):
                name = name[2:]
            if name.endswith(']]'):
                name = name[:-2]
            name = name.split('|')[-1].strip().replace("'", "\\'")
            name = SPECIAL_COLORS.get((name, int(hexname, 16)), name)
            print("    '{}': 0x{},".format(name, hexname))

    print(FOOTER)


def write_colors():
    for name, (title, *urls) in SOURCES.items():
        filename = (PALETTE_DIR / name).with_suffix('.py')
        print('Creating', filename, '...', end='')
        with safer.printer(filename, 'w') as pr:
            colors(urls, title, pr)
        print('done')


if __name__ == '__main__':
    write_colors()
