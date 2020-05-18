from . import color
import importlib
import re
import string

_ALLOWED = set(string.ascii_letters + string.digits)


class Colors:
    """DOX HERE"""

    def __init__(self, *palettes, canonicalize_gray='gray', default='black'):
        class Color(color.Color):
            COLORS = self

        super().__setattr__('Color', Color)

        gt = self._canonicalize_gray = canonicalize_gray
        if not gt:
            self._replacements = ()
        else:
            gt = 'gray' if gt is True else gt.lower()
            gf = 'grey' if gt == 'gray' else 'gray'
            if gt not in ('gray', 'grey'):
                raise ValueError('Don\'t understand canonicalize_gray=%s' % gt)

            self._replacements = (
                (re.compile(r'\b%s\b' % gf).sub, gt),
                (re.compile(r'\b%s\b' % gf.capitalize()).sub, gt.capitalize()),
            )

        self._name_to_rgb = {}
        self._rgb_to_name = {}
        self._palettes = [self._add_palette(s) for s in palettes]

        self._canonical_to_rgb = {
            self._canonical_name(k): v for k, v in self._name_to_rgb.items()
        }
        self._default = self.get(str(default)) or next(iter(self._rgb_to_name))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        return self._name_to_rgb.items()

    def values(self):
        return self._name_to_rgb.values()

    def keys(self):
        return self._name_to_rgb.keys()

    def closest(self, color):
        """
        Return the closest named color to `color`.  This can be quite slow,
        particularly if there are many colors.
        """
        if isinstance(color, list):
            color = tuple(color)
        if color in self._rgb_to_name:
            return color
        return min((c.distance2(color), c) for c in self.values())[1]

    def __call__(self, *args, **kwds):
        return self.Color(*args, **kwds)

    def __getitem__(self, name):
        """Try to convert string item into a color"""
        canonical = self._canonical_name(name)
        try:
            return self._canonical_to_rgb[canonical]
        except KeyError:
            pass
        raise KeyError(name)

    def __setitem__(self, name, rgb):
        raise KeyError(name)

    def __contains__(self, x):
        """Return true if this string name appears in the table canonically"""
        return self._canonical_name(x) in self._canonical_to_rgb

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            return super().__setattr__(name, value)
        raise AttributeError(name)

    def __len__(self):
        return len(self._name_to_rgb)

    def __iter__(self):
        return iter(self._name_to_rgb)

    def __eq__(self, x):
        return __class__ == x.__class__ and self._name_to_rgb == x._name_to_rgb

    def __ne__(self, x):
        return not (self == x)

    def __add__(self, x):
        cg, d = self._canonicalize_gray, self._default
        c = x if isinstance(x, __class__) else __class__(x)
        palettes = self._palettes + c._palettes
        return __class__(*palettes, canonicalize_gray=cg, default=d)

    def __radd__(self, x):
        other = __class__(
            x, canonicalize_gray=self._canonicalize_gray, default=self._default
        )
        return other + self

    def _add_palette(self, palette):
        if isinstance(palette, str):
            if '.' not in palette:
                palette = '.' + palette
            if palette.startswith('.'):
                palette = 'nc.palette' + palette

            palette = importlib.import_module(palette)

        if not isinstance(palette, dict):
            palette = palette.__dict__

        if 'COLORS' in palette:
            colors = palette['COLORS']
            primary_names = palette.get('PRIMARY_NAMES', ())

        else:
            colors = palette
            palette = {'COLORS': palette}
            primary_names = ()

        colors = {k: self.Color(v) for k, v in colors.items()}
        if not palette.get('PRESERVE_CAPITALIZATION'):
            colors = {k.capitalize(): v for k, v in colors.items()}

        for sub, rep in self._replacements:
            colors = {sub(rep, k): v for k, v in colors.items()}

        self._name_to_rgb.update(colors)

        def best_name(names):
            names.sort(key=lambda n: (len(n), n.lower()))
            pnames = (n for n in names if n in primary_names)
            return next(pnames, names[0])

        names = {}
        for n, c in colors.items():
            names.setdefault(c, []).append(n)

        self._rgb_to_name.update((k, best_name(v)) for k, v in names.items())
        return palette

    def _canonical_name(self, name):
        name = name.lower()
        if self._canonicalize_gray:
            name = name.replace('grey', 'gray')
        return ''.join(i for i in name if i in _ALLOWED)


"""Some colors have multiple names; a best name needs to be chosen.
   palette.PRIMARY_NAMES is a list of names to use by preference.
   Otherwise the shortest color name is chosen, and in a tie, the
   alphabetically first one.
"""
