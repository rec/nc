from .terminal16 import fg, bg  # noqa: F401
from .terminal16 import COLORS as _COLORS, CODES as _CODES  # noqa: F401

COLORS = {k: v for k, v in _COLORS.items() if not k.startswith('Bright')}
CODES = {k: v for k, v in _CODES.items() if not k.startswith('Bright')}
