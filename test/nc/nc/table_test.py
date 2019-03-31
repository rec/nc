import unittest
from nc import table


class TableTest(unittest.TestCase):
    def test_simple(self):
        colors = table.Table(False)
        self.assertEqual(colors.to_color('RED'), (255, 0, 0))
        self.assertEqual(colors.to_string((255, 0, 0)), 'Red')
        with self.assertRaises(ValueError):
            colors.to_color('rod')

    def test_all_named_colors(self):
        colors = table.Table()
        all_colors = sorted(colors)
        self.assertEqual(1336, len(all_colors))
        actual = all_colors[:4] + all_colors[-4:]
        expected = [
            'Absolute Zero',
            'Acid green',
            'Aero',
            'Aero blue',
            'Yellow-green (Color Wheel)',
            'Yellow-green (Crayola)',
            'Zaffre',
            'Zomp']

        self.assertEqual(actual, expected)

    def test_normal(self):
        colors = table.Table()
        self.assertEqual(colors.to_color('RED'), (1, 0, 0))
        self.assertEqual(colors.to_string((1, 0, 0)), 'Red')
        with self.assertRaises(ValueError):
            colors.to_color('rod')
