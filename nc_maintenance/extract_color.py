PREFIX = '{{Colort/Color|'
SUFFIX = '}}'


def extract_color(line):
    if not (line.endswith(SUFFIX) and line.startswith(PREFIX)):
        return None

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


TEST_DATA = '\
{{Colort/Color|hex=0048BA|r=0 |g=72 |b=186|h=217|s=100|v=73 |\
name=[[List of Crayola crayon colors#Extreme Twistables colors|\
Absolute Zero]]|link target=A}}'

TEST_DATA2 = '\
{{Colort/Color|hex=CD5700|r=205|g=87|b=0|h=25|s=100|v=80|l=40|\
name=[[Tawny (color)|Tenné]] (tawny)}}'


def run_test():
    print(extract_color(TEST_DATA))
    print(extract_color(TEST_DATA2))


if __name__ == '__main__':
    run_test()
