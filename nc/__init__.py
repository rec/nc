from . import _colors
import sys

_DEFAULT_SCHEMES = 'wikipedia', 'juce', 'x11'


class NamedColors:
    Colors = _colors.Colors
    _COLORS = None

    @property  # noqa: F811
    def COLORS(self):
        if not self._COLORS:
            self._COLORS = self.Colors(*_DEFAULT_SCHEMES)

        return self._COLORS

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            pass
        try:
            return globals()[name]
        except KeyError:
            pass
        c = self.COLORS
        return getattr(c, name)

    def __getitem__(self, name):
        return self.COLORS[name]

    def __call__(self, *args, **kwds):
        return self.COLORS(*args, **kwds)

    def __contains__(self, x):
        return x in self.COLORSz

    def __len__(self):
        return len(self.COLORS)

    def __iter__(self):
        return iter(self.COLORS)


sys.modules[__name__] = NamedColors()
NamedColors.__doc__ = """NamedColors"""
