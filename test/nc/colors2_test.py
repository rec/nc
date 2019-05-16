import unittest

from nc import default


class ColorsTest(unittest.TestCase):
    def test_colors(self):
        default.nc.COLORS
        self.assertEqual(default.nc.COLORS.red, (0xFF, 0, 0))
