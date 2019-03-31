import unittest

from nc import table, COLORS_255


class NamesTest(unittest.TestCase):
    def test_colors(self):
        t = table.Table(False)
        self.assertEqual(COLORS_255.red, (255, 0, 0))
        self.assertEqual(t.to_string((0, 0, 0)), 'Black')
        self.assertEqual(COLORS_255.BurntSienna, (0x8a, 0x36, 0x0f))
        self.assertEqual(t.to_string((0x8a, 0x36, 0x0f)), 'Burnt sienna')

    def test_toggle_255(self):
        toggle = table.Table(False).toggle
        self.assertEqual(toggle('red'), '(255, 0, 0)')
        self.assertEqual(toggle('(255, 0, 0)'), 'Red')
        self.assertEqual(toggle('(0, 0, 0)'), 'Black')

        self.assertEqual(toggle('#e97451'), 'Burnt sienna')
        self.assertEqual(toggle('0xe97451'), 'Burnt sienna')

    def test_toggle(self):
        toggle = table.Table().toggle
        self.assertEqual(toggle('(1.0, 0.0, 0.0)'), 'Red')

        self.assertEqual(toggle('red'), '(1.0, 0.0, 0.0)')
        self.assertEqual(toggle('(1.0, 0.0, 0.0)'), 'Red')
        self.assertEqual(toggle('(0.0, 0.0, 0.0)'), 'Black')

        self.assertEqual(toggle('#e97451'), 'Burnt sienna')
        self.assertEqual(toggle('0xe97451'), 'Burnt sienna')
