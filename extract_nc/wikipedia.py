from . import extract_color
import bs4
import datetime
import os
import pathlib
import re
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

ANSI_ESCAPE_PAGE = 'ANSI_escape_code&section=12'

TABLE_BEGIN = '{| '
TABLE_LINE = '|-\n'
TABLE_END = '|}\n'
SCHEME_DIR = pathlib.Path(__file__).parents[1] / 'nc' / 'schemes'

SPECIAL_COLORS = {
    ('Peach', 0xFFCBA4): 'Deep peach',
    ('Vermilion', 0xD9381E): 'Medium vermillion',
    ('Tea rose', 0xF88379): 'Tea rose orange',
}

COLSPAN_RE = re.compile('colspan="(.)"')


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
        filename = (SCHEME_DIR / name).with_suffix('.py')
        print('Creating', filename, '...', end='')
        with safer.printer(filename, 'w') as pr:
            colors(urls, title, pr)
        print('done')


def write_escapes():
    text = wikitext(ANSI_ESCAPE_PAGE)

    table = text.split(TABLE_BEGIN, maxsplit=1)[-1]
    table = table.split(TABLE_END, maxsplit=1)[0]

    _, header, *rows = table.split(TABLE_LINE)
    assert len(rows) == 16, str(rows)

    names = _read_header(header)
    names = [n.replace('&nbsp;', ' ') for n in names]
    assert len(names) == 11, str(names)

    name_to_values = {}
    for row in rows:
        color, values = _read_row(row)
        if not any(v is None for v in values):
            for name, value in zip(names, values):
                name_to_values.setdefault(name, {})[color] = value

    with safer.printer(SCHEME_DIR / 'escapes.py') as print:
        print_header('ASCII escape codes', print)
        first = True
        for name, values in name_to_values.items():
            if first:
                first = False
            else:
                print()

            name = ''.join(i if i.isalnum() else '_' for i in name)
            print(name.replace('__', '_').upper(), '= (')
            for color, value in values.items():
                print("    ('%s', %s)," % (color, value))
            print(')')


def _read_row(row):
    color = None
    items = []
    for row in row.splitlines():
        parts = [i.strip() for i in row.split('|') if i.strip()]
        if not color:
            color = parts[0]
        elif not parts:
            items.append(None)
        else:
            style, value, *_ = parts
            rgb = value.split('<')[0].split(',')
            rgb = tuple(int(i) for i in rgb)
            m = COLSPAN_RE.search(style)
            span = m and int(m.group(1)) or 1
            items += [rgb] * span

    assert len(items) == 11, '%s=%s' % (color, items)
    return color, items


def _read_header(header):
    for line in header.splitlines():
        if line.startswith('!'):
            line = line[1:].strip()
            if line.startswith('['):
                link = line.split(']')[0].strip('[]')
                yield link.split('|')[-1]
            elif '||' not in line:
                yield line.split('<')[0]


if __name__ == '__main__':
    if False:
        write_colors()
    else:
        print(write_escapes())
