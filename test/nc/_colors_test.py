from nc import _util
from nc.schemes import juce
import nc
import unittest


class ColorsTest(unittest.TestCase):
    def test_colors(self):
        colors = nc.COLORS
        self.assertEqual(colors.red, (0xFF, 0, 0))
        self.assertEqual(colors.to_string(colors.red), 'Red')
        self.assertEqual(colors.to_string((0xFE, 0, 0)), '(254, 0, 0)')
        self.assertEqual(colors.to_string((0, 0, 0)), 'Black')
        self.assertEqual(colors.BurntSienna, (0x8A, 0x36, 0x0F))
        self.assertEqual(colors.to_string((0x8A, 0x36, 0x0F)), 'Burnt sienna')
        with self.assertRaises(ValueError):
            colors.to_color('rod')

    def test_secondaries(self):
        colors = nc.Colors('juce')
        primaries = []
        for secondary in juce.SECONDARY_NAMES:
            rgb = colors[secondary]
            primary = colors.to_string(rgb)
            if primary == secondary:
                int_color = _util.to_int(*rgb)
                dupes = set(
                    k for k, v in juce.COLORS.items() if v == int_color
                )
                dupes.remove(primary)
                primaries.append(sorted(dupes)[0])

        self.assertEqual(sorted(primaries), [])

    def test_all_named_colors(self):
        colors = nc.COLORS
        all_colors = sorted(colors)
        self.assertEqual(1353, len(all_colors))
        actual = all_colors[:4] + all_colors[-4:]
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
            self.assertIn(i, nc.COLORS)
            nc.COLORS[i]

        for i in 'rod', 'wart', 'verd', 'vegas-mud':
            self.assertNotIn(i, nc.COLORS)
            with self.assertRaises(KeyError):
                nc.COLORS[i]

    def test_errors(self):
        with self.assertRaises(AttributeError):
            nc.COLORS.red = 0, 0, 0

        with self.assertRaises(KeyError):
            nc.COLORS['red'] = 0, 0, 0

    def test_dict_module(self):
        cdict = {'red': (0x80, 0, 0), 'grey': (0x80, 0x80, 0x80)}
        with self.assertRaises(AttributeError):
            nc.Colors({'COLOURS': cdict})
        colors = nc.Colors({'COLORS': cdict})
        self.assertIn('grey', colors)
        self.assertIn('gray', colors)

        colors = nc.Colors({'COLORS': cdict}, gray_munging=False)
        self.assertIn('grey', colors)
        self.assertNotIn('gray', colors)

    def test_import_XXX(self):
        colors = nc.Colors('test.nc._colors_test')
        self.assertEqual(colors.red, (0xFF, 0, 0))
        self.assertEqual(colors.rad, (0xFF, 0, 0))
        self.assertEqual(colors.to_string(colors.groan), 'Green')
        self.assertEqual(colors.to_string(colors.Blaue), 'Blue')
        self.assertEqual(colors.to_string(colors.rad), 'Red')


COLORS = {
    'Red': (0xFF, 0, 0),
    'Rad': (0xFF, 0, 0),
    'Groan': (0, 0xFF, 0),
    'Green': (0, 0xFF, 0),
    'Blue': (0, 0, 0xFF),
    'Blaue': (0, 0, 0xFF),
}

PRIMARY_NAMES = {'Red'}
