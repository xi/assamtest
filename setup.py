from setuptools import setup

setup(
	name='assamtest',
	version='0.0.0',
	description='mocha-style tests for python',
	url='https://github.com/xi/assamtest',
	author='Tobias Bengfort',
	author_email='tobias.bengfort@posteo.de',
	packages=['assamtest'],
	extras_require={
		'color': ['colorama'],
	},
	entry_points={'console_scripts': [
		'assamtest=assamtest.__main__:main',
	]},
	license='GPLv2+',
)
