from . import process_line
import bs4
import requests
import sys

WIKI_URL = 'https://en.wikipedia.org/w/index.php?title='
EDIT_STRING = '&action=edit'
_BASE = 'List_of_colors:_{0}%E2%80%93{1}'
PAGES = _BASE.format('A', 'F'), _BASE.format('G', 'M'), _BASE.format('N', 'Z')
X11_PAGE = 'X11_color_names'


def wikibox(url):
    if not url.startswith(WIKI_URL):
        url = WIKI_URL + url
    if not url.endswith(EDIT_STRING):
        url += EDIT_STRING
    text = requests.get(url).text
    open('/tmp/file.html', 'w').write(text)
    soup = bs4.BeautifulSoup(text, features='html.parser')
    return soup.find(id='wpTextbox1').text


def _colors(*urls):
    for url in urls:
        for line in wikibox(url).splitlines():
            p = process_line.process_line(line)
            if p:
                yield p


def wikipedia_colors():
    return _colors(*PAGES)


def x11_colors():
    return _colors(X11_PAGE)


def run_all():
    import yaml

    # yaml.dump_all(wikipedia_colors(), sys.stdout)
    yaml.dump_all(x11_colors(), sys.stdout)


if __name__ == '__main__':
    run_all()
