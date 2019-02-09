import argparse
import os
import sys
import importlib
import pkgutil

from . import stack, _unit_push, _unit_pop
from .reporter import SpecReporter
from .runner import run


def import_package(path):
	mod = importlib.import_module(path)
	d = mod.__file__
	if d.endswith('__init__.py'):
		d = os.path.dirname(d)
	for _, name, _ in pkgutil.iter_modules([d]):
		_unit_push()
		import_package(path + '.' + name)
		_unit_pop(name)


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('module', nargs='?', default='tests')
	return parser.parse_args()


args = parse_args()
import_package(args.module)
sys.exit(run(stack[-1], SpecReporter()))
