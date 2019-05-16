from nc import default
from nc import util
from nc.colors2 import Colors
from nc.schemes import juce
import unittest


class ColorsTest(unittest.TestCase):
    def test_colors(self):
        colors = default.nc.COLORS
        self.assertEqual(colors.red, (0xFF, 0, 0))
        self.assertEqual(colors.to_string(colors.red), 'Red')
        self.assertEqual(colors.to_string((0xFE, 0, 0)), '(254, 0, 0)')

    def test_secondaries(self):
        colors = Colors('juce')
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
