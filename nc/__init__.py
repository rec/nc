from . import _colors
import sys

_DEFAULT_SCHEMES = 'wikipedia', 'x11', 'juce'


class NamedColors:
    Colors = _colors.Colors
    _COLORS = None

    @property
    def COLORS(self):
        if not self._COLORS:
            self._COLORS = self.Colors(*_DEFAULT_SCHEMES)

        return self._COLORS

    @property
    def Color(self):
        return self.COLORS.Color

    def __getattr__(self, name):
        try:
            return globals()[name]
        except KeyError:
            pass
        return getattr(self.COLORS, name)


sys.modules[__name__] = NamedColors()
NamedColors.__doc__ = """NamedColors"""
