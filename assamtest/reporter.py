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

	def enter_suite(self, name):
		pass

	def leave_suite(self, name):
		pass

	def test(self, name, err, status, level):
		pass


class SpecReporter(Reporter):
	def __init__(self):
		self.stack = []
		self.total = 0
		self.stats = {
			'SUCCESS': {},
			'INFO': {},
			'WARNING': {},
			'ERROR': {},
		}

	def _render(self, msg, level, status):
		if status == 'passed':
			char = '✓'
		elif status == 'failed':
			char = '✖'
		else:
			char = status[0].upper()
		color = {
			'SUCCESS': 'GREEN',
			'INFO': 'CYAN',
			'WARNING': 'YELLOW',
			'ERROR': 'RED',
		}[level]
		return colored('%s %s' % (char, msg), color)

	def _print(self, msg):
		print('  ' * len(self.stack) + msg)

	def enter_suite(self, name):
		self._print(name)
		self.stack.append(name)

	def test(self, name, err, status, level):
		self.total += 1
		self.stats[level].setdefault(status, 0)
		self.stats[level][status] += 1

		if level == 'SUCCESS':
			self._print(self._render('', level, status) + colored(name, 'DIM'))
		else:
			self._print(self._render(name, level, status))

		if err and str(err):
			self._print('    %s' % err)

	def leave_suite(self, name):
		self.stack.pop()

	def leave_run(self):
		if self.total == 0:
			print(colored('No tests found', 'YELLOW'))
			return 5

		print()
		for level in ['SUCCESS', 'INFO', 'WARNING', 'ERROR']:
			for status, count in sorted(self.stats[level].items()):
				print(self._render('%i %s' % (count, status), level, status))

		if sum(self.stats['ERROR'].values()) != 0:
			return 1
