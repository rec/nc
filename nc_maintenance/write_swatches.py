import nc


def _cell(color):
    tup = f'( {color.r:3}, {color.g:3}, {color.b:3} )'
    name = f'{color} {tuple(color)}'
    hex_color = f'#{color.rgb:06x}'
    style = f'color:{hex_color};'
    code = f'<code>{hex_color} {tup}</code>'
    return f'    <td "{style}">{code} {color}</td>'


def _row(color_row):
    cells = '\n'.join(_cell(c) for c in color_row)
    return f'  <tr>\n{cells}\n  </tr>'


def _table(name, colors, count=3):
    colors = list(colors.values())
    rows = (colors[i: i + count] for i in range(0, len(colors), count))
    body = '\n'.join(_row(r) for r in rows)

    label = f'<h2>{name.capitalize()}</h2>\n'
    return f'{label}<table><tbody>\n{body}\n</tbody></table>'


def write_swatches():
    print(_table('All colors', nc))


if __name__ == '__main__':
    write_swatches()
