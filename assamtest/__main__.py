import argparse
import os
import sys
import importlib
import pkgutil

from .register import stack, _suite_push, _suite_pop
from .reporter import SpecReporter
from .runner import run


def import_package(path):
	mod = importlib.import_module(path)
	d = mod.__file__
	if d.endswith('__init__.py'):
		d = os.path.dirname(d)
	for _, name, _ in pkgutil.iter_modules([d]):
		_suite_push()
		import_package(path + '.' + name)
		_suite_pop(name)


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('module', nargs='?', default='tests')
	return parser.parse_args()


def main():
	sys.path.insert(0, '')
	args = parse_args()
	import_package(args.module)
	sys.exit(run(stack[-1], SpecReporter()))


if __name__ == '__main__':
	main()
