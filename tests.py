import assamtest
from assamtest import expect
from assamtest import decorators as _decorators

original_stack = None
stack = None


class TestReporter(assamtest.reporter.Reporter):
	def __init__(self):
		self.stats = {}

	def test(self, name, err, status, level):
		self.stats.setdefault(status, 0)
		self.stats[status] += 1


def expect_stats(**stats):
	reporter = TestReporter()
	assamtest.runner.run(stack[-1], reporter)
	expect.equal(reporter.stats, stats)


@assamtest.before_each()
def before_each():
	global original_stack, stack
	original_stack = assamtest.register.stack
	assamtest.register.stack = stack = [{'tests': [], 'suites': []}]


@assamtest.after_each()
def after_each():
	assamtest.register.stack = original_stack


@assamtest.test()
def test_simple():
	@assamtest.test(args=['+', 5])
	@assamtest.test(args=['*', 6])
	def my_test(op, value):
		expect.equal(eval('2 %s 3' % op), value)

	expect_stats(passed=2)


@assamtest.test()
def test_async():
	import asyncio

	@assamtest.test(args=[4])
	@assamtest.test(args=[5], decorators=[_decorators.fail])
	async def my_test(value):
		await asyncio.sleep(0.1)
		expect.equal(2 + 2, value)

	expect_stats(passed=2)


@assamtest.test()
def suite_simple():
	@assamtest.suite()
	def my_suite():
		@assamtest.before_each()
		def _before_each():
			pass  # do some setup here

		@assamtest.test()
		def my_test():
			expect.equal(2 + 2, 4)

	expect_stats(passed=1)


@assamtest.test()
def suite_nonlocal():
	@assamtest.suite()
	def my_suite():
		a = None

		@assamtest.test()
		def my_test1():
			expect.false(a)

		@assamtest.test()
		def my_test2():
			nonlocal a
			a = True
			expect.true(a)

		@assamtest.test()
		def my_test3():
			expect.true(a)

	expect_stats(passed=3)


@assamtest.test()
def expect_simple():
	expect.equal(2 + 2, 4)
	expect.not_equal(2 + 2, 5)
	expect._in(2, [1, 2, 3])
	with expect.raises(KeyError):
		{'foo': 0}['bar']


@assamtest.suite()
def decorators():
	@assamtest.test()
	def skip():
		@assamtest.test(decorators=[_decorators.skip])
		def my_test():
			expect.equal(2 + 2, 5)

		expect_stats(skipped=1)

	@assamtest.test()
	def fail():
		@assamtest.test(args=[4])
		@assamtest.test(args=[5], decorators=[_decorators.fail])
		def my_test(value):
			expect.equal(2 + 2, value)

		expect_stats(passed=2)
