from nc.schemes import juce
import nc
import unittest


class ColorsTest(unittest.TestCase):
    def test_namespace(self):
        # colors from nc.COLORS appear in the nc. namespace
        self.assertEqual(nc.red, (0xFF, 0, 0))
        self.assertEqual(str(nc.orange), 'Orange')
        self.assertEqual(nc.BurntSienna, (0x8A, 0x36, 0x0F))
        with self.assertRaises(AttributeError):
            nc.rod

    def test_colors(self):
        colors = nc.COLORS
        Color = colors.Color
        self.assertEqual(colors.red, (0xFF, 0, 0))
        self.assertEqual(str(colors.red), 'Red')
        self.assertEqual(str(Color(0xFE, 0, 0)), '(254, 0, 0)')
        self.assertEqual(str(Color(0, 0, 0)), 'Black')
        self.assertEqual(colors.BurntSienna, (0x8A, 0x36, 0x0F))
        self.assertEqual(str(colors.BurntSienna), 'Burnt sienna')

    def test_error(self):
        nc['red']
        with self.assertRaises(KeyError):
            nc['rod']
        with self.assertRaises(AttributeError):
            nc.rod

    def test_bug(self):
        self.assertEqual(nc.red, nc('red'))

    def test_secondaries(self):
        colors = nc.Colors('juce')
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
        all_colors = sorted(nc)
        self.assertEqual(1409, len(all_colors))
        actual = all_colors[:4] + all_colors[-4:]
        actual = [(a, nc[a]) for a in actual]
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
