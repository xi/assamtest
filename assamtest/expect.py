from unittest import TestCase


class Wrapper:
	def __init__(self):
		self.case = TestCase()

	def __getattr__(self, key):
		camel_cased = ''.join(part.capitalize() for part in key.split('_'))
		return getattr(self.case, 'assert' + camel_cased)


expect = Wrapper()
