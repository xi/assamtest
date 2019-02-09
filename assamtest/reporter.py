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
		self.stats = {
			'SUCCESS': {},
			'INFO': {},
			'WARNING': {},
			'ERROR': {},
		}

	def render_level(self, msg, level, status):
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

	def leave_run(self):
		print()
		for level in ['SUCCESS', 'INFO', 'WARNING', 'ERROR']:
			for status, count in sorted(self.stats[level].items()):
				print(self.render_level('%i %s' % (count, status), level, status))

		if sum(self.stats['ERROR'].values()) != 0:
			return 1
		elif sum(sum(l.values()) for l in self.stats.values()) == 0:
			print(colored('No tests found', 'YELLOW'))
			return 5

	def enter_suite(self, name):
		self._print(name)
		self.stack.append(name)

	def leave_suite(self, name):
		self.stack.pop()

	def test(self, name, err, status, level):
		self.stats[level].setdefault(status, 0)
		self.stats[level][status] += 1

		if level == 'SUCCESS':
			self._print(self.render_level('', level, status) + colored(name, 'DIM'))
		else:
			self._print(self.render_level(name, level, status))

		if err and str(err):
			self._print('    %s' % err)
