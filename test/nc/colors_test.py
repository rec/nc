from nc.default import nc
from nc import util
from nc.schemes import juce
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
                int_color = util.to_int(*rgb)
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
        print(actual)
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
