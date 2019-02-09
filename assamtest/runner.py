class Outcome(Exception):
	def __init__(self, err, status, level):
		self.err = err
		self.status = status
		self.level = level

	def __str__(self):
		return str(self.err or '')


def run_test(test):
	try:
		test()
	except Outcome as err:
		return err, err.status, err.level
	except AssertionError as err:
		return err, 'failed', 'ERROR'
	except Exception as err:
		return err, 'errored', 'ERROR'
	return None, 'passed', 'SUCCESS'


def _run(suite, reporter, before_each=[], after_each=[]):
	if 'before_each' in suite:
		before_each = before_each + [suite['before_each']]
	if 'after_each' in suite:
		after_each = [suite['after_each']] + after_each

	if 'before' in suite:
		suite['before']()

	for name, test in suite['tests']:
		for fn in before_each:
			fn()

		reporter.test(name, *run_test(test))

		for fn in after_each:
			fn()

	for name, subsuite in suite['suites']:
		reporter.enter_suite(name)
		_run(subsuite, reporter, before_each=before_each, after_each=after_each)
		reporter.leave_suite(name)

	if 'after' in suite:
		suite['after']()


def run(suite, reporter):
	reporter.enter_run()
	_run(suite, reporter)
	return reporter.leave_run()
