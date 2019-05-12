from . import process_line
import bs4
import requests
import sys

WIKI_URL = 'https://en.wikipedia.org/w/index.php?'
EDIT_STRING = '&action=edit'
_BASE = 'title=List_of_colors:_{0}%E2%80%93{1}'
PAGES = _BASE.format('A', 'F'), _BASE.format('G', 'M'), _BASE.format('N', 'Z')


def wikibox(url):
    if not url.startswith(WIKI_URL):
        url = WIKI_URL + url
    if not url.endswith(EDIT_STRING):
        url += EDIT_STRING
    text = requests.get(url).text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    return soup.find(id='wpTextbox1').text


def wikipedia_colors():
    for url in PAGES:
        for line in wikibox(url).splitlines():
            if line.startswith('{{') and '|hex=' in line:
                yield process_line.process_line(line)


def run_all():
    import yaml

    yaml.dump_all(wikipedia_colors(), sys.stdout)


if __name__ == '__main__':
    run_all()
