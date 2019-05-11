import bs4
import requests
import sys


_BASE = (
    'https://en.wikipedia.org/w/index.php?title=List_of_colors:'
    '_{0}%E2%80%93{1}&action=edit'
)
PAGES = _BASE.format('A', 'F'), _BASE.format('G', 'M'), _BASE.format('N', 'Z')

TEST_DATA = '\
{{Colort/Color|hex=0048BA|r=0 |g=72 |b=186|h=217|s=100|v=73 |\
name=[[List of Crayola crayon colors#Extreme Twistables colors|\
Absolute Zero]]|link target=A}}'

TEST_DATA2 = '\
{{Colort/Color|hex=CD5700|r=205|g=87|b=0|h=25|s=100|v=80|l=40|\
name=[[Tawny (color)|Tenné]] (tawny)}}'

PREFIX = '{{Colort/Color|'
SUFFIX = '}}'


def get_lines():
    for begin, end in 'AF', 'GM', 'NZ':
        url = _BASE.format(begin, end)
        text = requests.get(url).text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        item = soup.find(id='wpTextbox1').text

        for line in item.splitlines():
            if line.startswith('{{') and '|hex=' in line:
                yield process_line(line)


def process_line(line):
    assert line.endswith(SUFFIX)
    assert line.startswith(PREFIX)
    line = line[len(PREFIX) : -len(SUFFIX)]

    result = {}
    while line:
        name, line = line.split('=', 1)
        value = ''
        while True:
            try:
                a, b = line.split('|', 1)
            except ValueError:
                value += line
                line = ''
                break

            try:
                c, d = line.split('[[', 1)
            except ValueError:
                c = None

            if c is None or len(a) < len(c):
                value += a
                line = b
                break

            # We have a [[ before a |!
            e, line = d.split(']]', 1)
            value += '%s[[%s]]' % (c, e)

        result[name] = value

    return result


def run_test():
    print(process_line(TEST_DATA))
    print(process_line(TEST_DATA2))


def run_all():
    import yaml

    yaml.dump_all(get_lines(), sys.stdout)


if __name__ == '__main__':
    run_all()
