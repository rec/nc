import nc
import unittest


class CustomColorsTest(unittest.TestCase):
    def test_dict_module(self):
        cdict = {'red': (0x80, 0, 0), 'grey': (0x80, 0x80, 0x80)}
        colors = nc.Colors({'COLORS': cdict}, canonicalize_gray=True)
        with self.assertRaises(ValueError):
            nc.Colors({'COLOURS': cdict})

        print(list(colors))
        self.assertIn('grey', colors)
        self.assertIn('gray', colors)

        colors = nc.Colors({'COLORS': cdict}, canonicalize_gray=False)
        self.assertIn('grey', colors)
        self.assertNotIn('gray', colors)

    def test_gray_error(self):
        cdict = {'red': (0x80, 0, 0), 'grey': (0x80, 0x80, 0x80)}
        with self.assertRaises(ValueError) as e:
            nc.Colors({'COLORS': cdict}, canonicalize_gray='groy')
        a = e.exception.args[0]
        assert a == 'Don\'t understand canonicalize_gray=groy'

    def test_import(self):
        colors = nc.Colors('test.nc.test_custom_colors')
        self.assertEqual(colors.red, (0xFF, 0, 0))
        self.assertEqual(colors.rad, (0xFF, 0, 0))
        self.assertEqual(str(colors.groan), 'Green')
        self.assertEqual(str(colors.Blaue), 'Blue')
        self.assertEqual(str(colors.rad), 'Red')

    def test_addition(self):
        c1 = nc.Colors('test.nc.test_custom_colors')
        self.assertEqual(c1, c1)
        self.assertEqual(c1, c1 + c1)
        c2 = c1 + {'Red': (0x80, 0, 0)}
        self.assertEqual(c2.red, (0x80, 0, 0))
        self.assertEqual(c2, COLORS + nc.Colors({'Red': (0x80, 0, 0)}))
        self.assertNotEqual({'Red': (0x80, 0, 0)} + c1, c2)

    def test_simple(self):
        nc.Colors({'Red': (0x80, 0, 0)})


COLORS = {
    'Red': (0xFF, 0, 0),
    'Rad': (0xFF, 0, 0),
    'Groan': (0, 0xFF, 0),
    'Green': (0, 0xFF, 0),
    'Blue': (0, 0, 0xFF),
    'Blaue': (0, 0, 0xFF),
}

PRIMARY_NAMES = {'Red'}
