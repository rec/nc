from . import _colors
from . import _util  # noqa: F401
import sys

_DEFAULT_SCHEMES = 'wikipedia', 'juce', 'pwg', 'html'


class _NC:
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
        except Exception:
            return globals()[name]


sys.modules[__name__] = _NC()
