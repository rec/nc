import nc
import unittest


class ModuleTest(unittest.TestCase):
    def test_basics(self):
        assert nc('red') == nc.red
        assert nc['REd'] == nc.red
        assert 'Taupe' in nc
        assert len(nc) == 1319

        for i in nc:
            assert i == 'Absolute Zero'
            break
