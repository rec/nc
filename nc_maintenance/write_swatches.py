from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional
import nc

SWATCH_PATH = Path(__file__).parents[1] / 'docs' / 'swatches'
SWATCH_PATH.mkdir(exist_ok=True, parents=True)

"""
sorted by:

* HSV, name
* name

backgrounds:

* gradiated (sorted down or up)
* 0 25 50 75 100

total 12.

"""


@dataclass
class Swatch:
    sort_key: Callable
    title: str
    filename: str
    background: Optional[nc.Color] = None
    count: int = 1
    reverse: bool = False

    def key(self, kv):
        return self.sort_key(*kv)

    def write(self):
        colors = sorted(nc.items(), key=self.key, reverse=self.reverse)

        offsets = range(0, len(colors), self.count)
        rows = (colors[i: i + self.count] for i in offsets)
        body = '\n'.join(self.row(r) for r in rows)

        tbody = f'<tbody>\n{body}\n</tbody>'
        style = _add_bg('font-family: monospace;', self.background)

        table = f'<table style="{style}"> {tbody} \n</table>\n'
        title = f'# {self.title}\n'
        document = f'{title}\n{table}'

        path = (SWATCH_PATH / self.filename).with_suffix('.md')
        path.write_text(document)
        print('Wrote', path)

    def row(self, color_row):
        cells = '\n'.join(self.cell(*c) for c in color_row)
        return f'  <tr>\n{cells}\n  </tr>'

    def cell(self, name, color):
        hex_color = f'#{color.rgb:06x}'
        triple = f'({color.r:3},{color.g:3},{color.b:3})'
        triple = triple.replace(' ', '&nbsp;')
        cell = f'{hex_color} {triple} {name}'

        bg = not self.background and _background(color)
        style = _add_bg(f'color: {hex_color};', bg)
        return f'    <td style="{style}"> {cell} </td>'


def _swatches():
    yield Swatch(
        sort_by_brightness,
        'Contrast (bright to dark)',
        'contrast-bright-to-dark',
    )

    yield Swatch(
        sort_by_brightness,
        'Contrast (dark to bright)',
        'contrast-dark-to-bright',
        reverse=True,
    )

    for gray in (0, 25, 50, 75, 100):
        for sort_key in sort_by_hsv, sort_by_name, sort_by_vhs:
            sort_name = sort_key.__name__.replace('_', ' ')
            file_stem = sort_key.__name__.replace('_', '-')
            b = 256 * gray / 100
            yield Swatch(
                sort_key,
                f'Gray {gray:03} {sort_name}',
                f'gray-{gray:03}-{file_stem}',
                nc.Color(b, b, b)
            )


def sort_by_brightness(name, color):
    return _brightness_comp(color), color.hsv, name


def sort_by_name(name, color):
    return name


def sort_by_hsv(name, color):
    return color.hsv, name


def sort_by_vhs(name, color):
    h, s, v = color.hsv
    return v, h, s, name


def _add_bg(style, bg):
    return style + f'background-color: #{bg.rgb:06x};' if bg else style


def _brightness_comp(color):
    return (round(color.brightness) + 128) % 256


def _background(color):
    b = _brightness_comp(color)
    return nc.Color(b, b, b)


def write_swatches():
    for s in _swatches():
        s.write()


if __name__ == '__main__':
    write_swatches()
