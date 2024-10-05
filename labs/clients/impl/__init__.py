import os, sys

from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from labs.clients.base import ModelClientBase

"""
copied from here https://julienharbulot.com/python-dynamical-import.html
"""


# # iterate through the modules in the current package
# package_dir = Path(__file__).resolve().parent
# for _, module_name, _ in iter_modules([package_dir]):
#     # import the module and iterate through its attributes
#     module = import_module(f"{__name__}.{module_name}")
#     for attribute_name in dir(module):
#         attribute = getattr(module, attribute_name)

#         if isclass(attribute) and isinstance(attribute, ModelClientBase):
#             # Add the class to this package's variables
#             globals()[attribute_name] = attribute


path = os.path.dirname(os.path.abspath(__file__))

# OG LOOP
# for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
#     mod = __import__('.'.join([__name__, py]), fromlist=[py])
#     classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
#     for cls in classes:
#         setattr(sys.modules[__name__], cls.__name__, cls)

for py in [
    f[:-3] for f in os.listdir(path) if f.endswith(".py") and f != "__init__.py"
]:
    mod = __import__(".".join([__name__, py]), fromlist=[py])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)
