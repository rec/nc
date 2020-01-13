from . import _colors
from . import _util  # noqa: F401
import sys

_DEFAULT_SCHEMES = 'wikipedia', 'juce', 'pwg', 'html'


class NC:
    Colors = _colors.Colors
    _COLORS = None

    @property  # noqa: F811
    def COLORS(self):
        if not self._COLORS:
            self._COLORS = self.Colors(*_DEFAULT_SCHEMES)

        return self._COLORS

    def __getattr__(self, name):
        try:
            return getattr(self.COLORS, name)
        except Exception:
            pass
        try:
            return globals()[name]
        except KeyError:
            pass
        raise AttributeError(name)


sys.modules[__name__] = NC()
