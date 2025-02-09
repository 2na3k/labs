import os, sys

from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from labs.clients.base import ModelClientBase

"""
copied from here https://julienharbulot.com/python-dynamical-import.html
"""

path = os.path.dirname(os.path.abspath(__file__))

for py in [
    f[:-3] for f in os.listdir(path) if f.endswith(".py") and f != "__init__.py"
]:
    mod = __import__(".".join([__name__, py]), fromlist=[py])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)
