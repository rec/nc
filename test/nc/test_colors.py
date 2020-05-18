from nc import COLORS
from nc import Color
from nc import Colors
from nc.palette import juce
import unittest


class ColorsTest(unittest.TestCase):
    def test_colors(self):
        self.assertEqual(COLORS.red, (0xFF, 0, 0))
        self.assertEqual(str(COLORS.red), 'Red')
        self.assertEqual(str(Color(0xFE, 0, 0)), '(254, 0, 0)')
        self.assertEqual(str(Color(0, 0, 0)), 'Black')
        self.assertEqual(COLORS.BurntSienna, (0x8A, 0x36, 0x0F))
        self.assertEqual(str(COLORS.BurntSienna), 'Burnt sienna')
        self.assertEqual(str(COLORS.green), 'Green')

    def test_error(self):
        COLORS['red']
        with self.assertRaises(KeyError):
            COLORS['rod']
        with self.assertRaises(AttributeError):
            COLORS.rod

    def test_bug(self):
        self.assertEqual(COLORS.red, COLORS('red'))

    def test_secondaries(self):
        colors = Colors('juce')
        primaries = []
        for secondary in juce.SECONDARY_NAMES:
            rgb = colors[secondary]
            primary = str(rgb)
            if primary == secondary:
                i_color = rgb.as_int()
                dupes = {k for k, v in juce.COLORS.items() if v == i_color}
                dupes.remove(primary)
                primaries.append(sorted(dupes)[0])

        self.assertEqual(sorted(primaries), [])

    def test_roundtrips(self):
        # Make sure some famous colors roundtrip correctly
        for c in _ROUNDTRIP:
            self.assertEqual(str(Color(c)), c)

    def test_non_roundtrips(self):
        def canon(s):
            s = str(s).lower()

            for w in ' (web)', ' (x11/web color)', ' (pantone)':
                if s.endswith(w):
                    s = s[: -len(w)]

            w = 'web '
            if s.startswith(w):
                s = s[len(w) :]

            for c in ' 0123456789()#-':
                s = s.replace(c, '')

            return s

        non = sorted((k, v) for k, v in COLORS.items() if canon(v) != canon(k))
        self.assertEqual(len(non), 102)
        actual = non[:4] + non[-4:]
        expected = [
            ('Ao (English)', Color('Web green')),
            ('Aqua', Color('Cyan')),
            ('Aquamarine 3', Color('Medium aquamarine')),
            ('Arylide yellow', Color('Hansa yellow')),
            ('Wood brown', Color('Lion')),
            ('Yellow (NCS)', Color('Cyber yellow')),
            ('Yellow (process)', Color('Canary yellow')),
            ('Yellow Sunshine', Color('Lemon')),
        ]
        self.assertEqual(actual, expected)

    def test_all_named_colors(self):
        all_colors = sorted(COLORS)
        self.assertEqual(1319, len(all_colors))
        actual = all_colors[:4] + all_colors[-4:]
        actual = [(a, COLORS[a]) for a in actual]
        expected = [
            ('Absolute Zero', (0, 72, 186)),
            ('Acid green', (176, 191, 26)),
            ('Aero', (124, 185, 232)),
            ('Aero blue', (201, 255, 229)),
            ('Yellow-green (Color Wheel)', (48, 178, 26)),
            ('Yellow-green (Crayola)', (197, 227, 132)),
            ('Zaffre', (0, 20, 168)),
            ('Zomp', (57, 167, 142)),
        ]

        self.assertEqual(actual, expected)

    def test_keys_and_values(self):
        colors = {k: v for k, v in COLORS.items()}
        self.assertEqual(sorted(COLORS.keys()), sorted(colors.keys()))
        self.assertEqual(sorted(COLORS.values()), sorted(colors.values()))

    def test_contains(self):
        for i in 'red', 'white', 'verdigris', 'vegas-gold':
            self.assertIn(i, COLORS)
            COLORS[i]

        for i in 'rod', 'wart', 'verd', 'vegas-mud':
            self.assertNotIn(i, COLORS)
            with self.assertRaises(KeyError):
                COLORS[i]

    def test_errors(self):
        with self.assertRaises(AttributeError):
            COLORS.red = 0, 0, 0

        with self.assertRaises(KeyError):
            COLORS['red'] = 0, 0, 0

    def test_closest(self):
        colors = [[6, 57, 54], [118, 99, 74], [25, 111, 106], [122, 222, 176]]
        actual = [str(COLORS.closest(c)) for c in colors]

        ex = ['Rich black', 'Raw umber', 'Pine green', 'Medium aquamarine']
        assert ex == actual

    def test_closest_float(self):
        color = COLORS.closest((204.5, 182.7, 76.22))
        assert str(color) == 'Vegas gold'


_ROUNDTRIP = (
    'Red',
    'Orange',
    'Yellow',
    'Green',
    'Blue',
    'Indigo',
    'Violet',
    'Black',
    'White',
    'Purple',
    'Gray',
    'Cyan',
    'Magenta',
    'Olive',
    'Silver',
    'Navy',
    'Chartreuse',
)
