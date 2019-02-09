def run_test(test):
	try:
		test()
	except Exception as e:
		return e


def _run(unit, reporter, before_each=[], after_each=[]):
	if 'before_each' in unit:
		before_each = before_each + [unit['before_each']]
	if 'after_each' in unit:
		after_each = [unit['after_each']] + after_each

	if 'before' in unit:
		unit['before']()

	for name, test in unit['tests']:
		for fn in before_each:
			fn()

		reporter.test(name, run_test(test))

		for fn in after_each:
			fn()

	for name, subunit in unit['units']:
		reporter.enter_unit(name)
		_run(subunit, reporter, before_each=before_each, after_each=after_each)
		reporter.leave_unit(name)

	if 'after' in unit:
		unit['after']()


def run(unit, reporter):
	reporter.enter_run()
	_run(unit, reporter)
	return reporter.leave_run()
