from nc import COLORS
from nc import Color
import unittest


class ColorTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Color(), COLORS.Black)

    def test_rgb(self):
        self.assertEqual(COLORS.Black.rgb, 0)
        self.assertEqual(COLORS.red.rgb, 0xFF0000)
        self.assertEqual(tuple(COLORS.green), (0, 255, 0))
        self.assertEqual(COLORS.green.rgb, 0x00FF00)
        self.assertEqual(COLORS.teal.rgb, 0x008080)

    def test_numbers(self):
        self.assertEqual(Color(0), COLORS.Black)
        self.assertEqual(Color(0xFFFFFF), COLORS.White)

    def test_fail(self):
        with self.assertRaises(ValueError):
            Color('rod')

    def test_tuple(self):
        self.assertEqual(Color(COLORS.Black), COLORS.Black)
        self.assertEqual(Color(COLORS.Yellow), COLORS.Yellow)

    def test_list(self):
        self.assertEqual(Color([0, 0, 0]), COLORS.Black)
        self.assertEqual(Color([255, 255, 255]), COLORS.White)

    def test_commas(self):
        self.assertEqual(Color('(0, 0, 0)'), COLORS.Black)
        self.assertEqual(Color('[255, 255, 255]'), COLORS.White)
        with self.assertRaises(ValueError):
            Color('[255, 255, 255)')
        with self.assertRaises(ValueError):
            Color('(255, 255, 255]')
        with self.assertRaises(ValueError):
            Color(']255, 255, 255[')

    def test_hex(self):
        self.assertEqual(Color('0x00000'), COLORS.Black)
        self.assertEqual(Color('#FFFFFF'), COLORS.White)

    def test_distance(self):
        self.assertEqual(COLORS.Black.distance2(COLORS.White), 3 * 255 ** 2)
        self.assertAlmostEqual(
            COLORS.Black.distance(COLORS.White), 441.6729559300637
        )

    def test_repr(self):
        self.assertEqual(repr(COLORS.red), "Color('Red')")
        self.assertEqual(repr(Color(2, 3, 4)), "Color(2, 3, 4)")

    def test_closest(self):
        values = list(COLORS.values())[:10]
        for c in values:
            assert c.closest() == c
