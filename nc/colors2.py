from . import util
import importlib


"""
Some colors have multiple names; a best name needs to be chosen.
module.PRIMARY_NAMES is a list of names to use by preference.
Otherwise the shortest color name is chosen, and in a tie, the
alphabetically first one.
"""


class Colors:
    def __init__(self, *modules, gray_munging=True):
        self._items = {}
        self._to_name = {}
        self._to_rgb = {}
        self._gray_munging = gray_munging

        for module in reversed(modules):
            self._add_module(module)

        self._modules = modules

    def to_color(self, c):
        """Try to coerce the argument into an rgb color"""
        try:
            return self[c]
        except Exception:
            return util.to_color(c)

    def to_string(self, c):
        """Convert a tuple to a string name"""
        try:
            return self._to_name[c]
        except Exception:
            return str(c)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, name):
        """Try to convert  string item into a color"""
        try:
            return self._to_rgb[util.canonical_name(name)]
        except KeyError:
            raise KeyError(name)

    def __setitem__(self, name, rgb):
        if not (isinstance(rgb, tuple) and len(rgb) == 3):
            raise ValueError('Bad color %s' % rgb)
        self._to_rgb[util.canonical_name(name)] = rgb

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __contains__(self, x):
        """Return true if this string or integer tuple appears in the table"""
        if isinstance(x, str):
            return util.canonical_name(x) in self._to_rgb
        if isinstance(x, tuple):
            return x in self._to_name

    def __iter__(self):
        return iter(self._items.items())

    def _add_module(self, module):
        original_module = module
        to_names = {}
        if isinstance(module, str):
            if '.' not in module:
                module = 'nc.schemes.' + module
            module = importlib.import_module(module)

        if not isinstance(module, dict):
            module = module.__dict__

        mcolors = module.get('COLORS', None)
        if mcolors is None:
            raise AttributeError('No COLORS %s' % original_module)

        for name, color in mcolors.items():
            rgb = util.to_rgb(color)
            to_names.setdefault(rgb, []).append(name)
            self._items[name] = rgb
            cname = util.canonical_name(name)
            self._to_rgb[cname] = rgb
            if self._gray_munging:
                self._to_rgb[cname.replace('gray', 'grey')] = rgb
                self._to_rgb[cname.replace('grey', 'gray')] = rgb

        primary_names = set(getattr(module, 'PRIMARY_NAMES', ()))

        def best_name(names):
            names.sort(key=lambda n: (len(n), n.lower()))
            pnames = (n for n in names if n in primary_names)
            return next(pnames, names[0])

        best_names = {k: best_name(v) for k, v in to_names.items()}
        self._to_name.update(best_names)
