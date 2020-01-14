from nc import COLORS
from nc import Color
import unittest


class ToColorTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Color.make(), COLORS.Black)

    def test_numbers(self):
        self.assertEqual(Color.make(0), COLORS.Black)
        self.assertEqual(Color.make(0xFFFFFF), COLORS.White)

    def test_fail(self):
        with self.assertRaises(ValueError):
            Color.make('rod')

    def test_tuple(self):
        self.assertEqual(Color.make(COLORS.Black), COLORS.Black)
        self.assertEqual(Color.make(COLORS.Yellow), COLORS.Yellow)

    def test_list(self):
        self.assertEqual(Color.make([0, 0, 0]), COLORS.Black)
        self.assertEqual(Color.make([255, 255, 255]), COLORS.White)

    def test_commas(self):
        self.assertEqual(Color.make('(0, 0, 0)'), COLORS.Black)
        self.assertEqual(Color.make('[255, 255, 255]'), COLORS.White)
        with self.assertRaises(ValueError):
            Color.make('[255, 255, 255)')
        with self.assertRaises(ValueError):
            Color.make('(255, 255, 255]')
        with self.assertRaises(ValueError):
            Color.make(']255, 255, 255[')

    def test_hex(self):
        self.assertEqual(Color.make('0x00000'), COLORS.Black)
        self.assertEqual(Color.make('#FFFFFF'), COLORS.White)
