try:
	import colorama
	colorama.init()
except ImportError:
	colorama = None


def colored(text, color):
	if colorama:
		c = getattr(colorama.Fore, color, getattr(colorama.Style, color, ''))
		return c + text + colorama.Style.RESET_ALL
	else:
		return text


class Reporter:
	def enter_run(self):
		pass

	def leave_run(self):
		pass

	def enter_unit(self, name):
		pass

	def leave_unit(self, name):
		pass

	def test(self, name, result):
		pass


class SpecReporter(Reporter):
	def __init__(self):
		self.stack = []
		self.stats = {
			'fail': 0,
			'pass': 0,
		}

	def _print(self, msg):
		print('  ' * len(self.stack) + msg)

	def leave_run(self):
		print()
		if self.stats['pass']:
			print(colored('✓ %i passing' % self.stats['pass'], 'GREEN'))
		if self.stats['fail']:
			print(colored('✖ %i failing' % self.stats['fail'], 'RED'))

		if self.stats['fail']:
			return 1

	def enter_unit(self, name):
		self._print(name)
		self.stack.append(name)

	def leave_unit(self, name):
		self.stack.pop()

	def test(self, name, result):
		if result:
			self.stats['fail'] += 1
			self._print(colored('✖ %s' % name, 'RED'))
			self._print('    %s' % result)
		else:
			self.stats['pass'] += 1
			self._print('%s %s' % (colored('✓', 'GREEN'), colored(name, 'DIM')))
