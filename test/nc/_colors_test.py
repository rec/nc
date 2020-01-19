from nc.schemes import juce
from nc import Color
from nc import Colors
from nc import COLORS
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
                dupes = set(k for k, v in juce.COLORS.items() if v == i_color)
                dupes.remove(primary)
                primaries.append(sorted(dupes)[0])

        self.assertEqual(sorted(primaries), [])

    def test_all_named_colors(self):
        all_colors = sorted(COLORS)
        self.assertEqual(1409, len(all_colors))
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
