from . import colors
import sys

_DEFAULT_PALETTES = 'wikipedia', 'x11', 'juce'


class NamedColors:
    Colors = colors.Colors
    _COLORS = None

    @property
    def COLORS(self):
        if not self._COLORS:
            self._COLORS = self.Colors(*_DEFAULT_PALETTES)

        return self._COLORS

    def __getattr__(self, name):
        try:
            return globals()[name]
        except KeyError:
            pass
        return getattr(self.COLORS, name)

    def __call__(self, *args, **kwargs):
        return self.COLORS(*args, **kwargs)

    def __getitem__(self, name):
        return self.COLORS[name]

    def __contains__(self, x):
        """Return true if this string name appears in the table canonically"""
        return x in self.COLORS

    def __len__(self):
        return len(self.COLORS)

    def __iter__(self):
        return iter(self.COLORS)


sys.modules[__name__] = NamedColors()
NamedColors.__doc__ = """
DOX HERE"""
