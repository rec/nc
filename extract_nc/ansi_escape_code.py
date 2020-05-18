"""
Scrape https://en.wikipedia.org/wiki/ANSI_escape_code
"""

from . import wikipedia
import re
import safer

COLSPAN_RE = re.compile('colspan="(.)"')
ANSI_ESCAPE_PAGE = 'ANSI_escape_code&section=12'
TABLE_BEGIN = '{| '
TABLE_LINE = '|-\n'
DIR = wikipedia.PALETTE_DIR / 'terminal16'


def write_escapes():
    text = wikipedia.wikitext(ANSI_ESCAPE_PAGE)

    table = text.split(TABLE_BEGIN, maxsplit=1)[-1]
    table = table.split(wikipedia.TABLE_END, maxsplit=1)[0]

    _, header, *rows = table.split(TABLE_LINE)
    assert len(rows) == 16, str(rows)

    names = _read_header(header)
    names = [n.replace('&nbsp;', ' ') for n in names]
    assert len(names) == 11, str(names)

    nv = {}
    for row in rows:
        color, values = _read_row(row)
        for name, value in zip(names, values):
            nv.setdefault(name, {})[color] = value

    for name, values in nv.items():
        if all(i is not None for i in values):
            _write_file(name, values)


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


def _write_file(name, values):
    name = ''.join(i if i.isalnum() else '_' for i in name)
    name = name.replace('__', '_').lower()
    with safer.printer(DIR / (name + '.py')) as print:
        wikipedia.print_header('ANSI escape codes', print)
        print('COLORS = {')
        for color, value in values.items():
            print(f"    '{color}': {value},")
        print('}')


if __name__ == '__main__':
    write_escapes()
