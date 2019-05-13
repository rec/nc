from . import extract_color
import bs4
import requests
import sys

WIKI_URL = 'https://en.wikipedia.org/w/index.php?title='
EDIT_STRING = '&action=edit'
_BASE = 'List_of_colors:_{0}%E2%80%93{1}'
PAGES = _BASE.format('A', 'F'), _BASE.format('G', 'M'), _BASE.format('N', 'Z')
X11_PAGE = 'X11_color_names'
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
    open('/tmp/file.html', 'w').write(text)
    soup = bs4.BeautifulSoup(text, features='html.parser')
    return soup.find(id='wpTextbox1').text


def colors(*urls):
    for url in urls:
        for line in wikibox(url).splitlines():
            color = extract_color.extract_color(line)
            if color:
                hexname = color['hex'].strip().upper()

                name = color['name'].strip()
                if name.startswith('[['):
                    name = name[2:]
                if name.endswith(']]'):
                    name = name[:-2]
                name = name.split('|')[-1].strip().replace("'", "\\'")
                name = SPECIAL_COLORS.get((name, int(hexname, 16)), name)
                yield name, hexname


def wikipedia():
    return colors(*PAGES)


def x11():
    return colors(X11_PAGE)


def run_all():
    import yaml

    # yaml.dump_all(wikipedia(), sys.stdout)
    yaml.dump_all(x11(), sys.stdout)


if __name__ == '__main__':
    run_all()
