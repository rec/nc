from . import extract_color
import bs4
import datetime
import os
import pathlib
import requests
import sys

HEADER = """# This file was automatically generated on {}
# by script {}
# from {}

COLORS = {{"""

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

TABLE_END = '|}'


SPECIAL_COLORS = {
    ('Peach', 0xFFCBA4): 'Deep peach',
    ('Vermilion', 0xD9381E): 'Medium vermillion',
    ('Tea rose', 0xF88379): 'Tea rose orange',
}


def wikibox(url):
    if not url.startswith(WIKI_URL):
        url = WIKI_URL + url
    if not url.endswith(EDIT_STRING):
        url += EDIT_STRING
    text = requests.get(url).text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    return soup.find(id='wpTextbox1').text


def colors(urls, fp, title):
    timestamp = datetime.datetime.now().isoformat()
    header = HEADER.format(timestamp, sys.argv[0], title)
    print(header, file=fp)

    for url in urls:
        for line in wikibox(url).splitlines():
            if line.strip() == TABLE_END:
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
            print("    '{}': 0x{},".format(name, hexname), file=fp)

    print(FOOTER, file=fp)


def write_colors():
    schemes = pathlib.Path(__file__).parents[1] / 'nc' / 'schemes'
    for name, (title, *urls) in SOURCES.items():
        filename = (schemes / name).with_suffix('.py')
        fp = open(filename, 'w')
        print('Creating', filename, '...', end='')
        try:
            with fp:
                colors(urls, fp, title)
            print('done')
        except Exception:
            try:
                os.remove(filename)
            except Exception:
                print('FAILED')
            raise


if __name__ == '__main__':
    write_colors()
