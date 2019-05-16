from nc import COLORS
from nc._util import to_color
import unittest


class ToColorTest(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(to_color(0), COLORS.Black)
        self.assertEqual(to_color(255), COLORS.White)

    def test_fail(self):
        for n in None, False, {}, set():
            with self.assertRaises(TypeError):
                to_color(n)
        with self.assertRaises(ValueError):
            to_color('')
        with self.assertRaises(ValueError):
            to_color('rod')

    def test_tuple(self):
        self.assertEqual(to_color(COLORS.Black), COLORS.Black)
        self.assertEqual(to_color(COLORS.Yellow), COLORS.Yellow)

    def test_list(self):
        self.assertEqual(to_color([0, 0, 0]), COLORS.Black)
        self.assertEqual(to_color([255, 255, 255]), COLORS.White)

    def test_commas(self):
        self.assertEqual(to_color('(0, 0, 0)'), COLORS.Black)
        self.assertEqual(to_color('[255, 255, 255)'), COLORS.White)
        self.assertEqual(to_color('[0xFF, 0xFF, 0xFF)'), COLORS.White)
        with self.assertRaises(ValueError):
            to_color(']255, 255, 255[')

    def test_hex(self):
        self.assertEqual(to_color('0x00000'), COLORS.Black)
        self.assertEqual(to_color('#FFFFFF'), COLORS.White)
