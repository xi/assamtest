assamtest is an experimental python test framework inspired by JavaScript
libraries such as [mocha](https://mochajs.org/) or
[jasmine](https://jasmine.github.io/).

-	everything is explicit, no magic
-	simple generated tests and suites
-	arbitrary nesting of test suites
-	compatible with converage
-	easily extendable with decorators and custom outcomes

## Usage

```python
# tests.py
import assamtest
from assamtest import expect

@assamtest.suite('A suite is just a function')
def my_suite():
	@assamtest.test('and so is a test')
	def my_test():
		a = True
		expect.true(a)
```

```
$ pip install assamtest
$ assamtest
A suite is just a function
  ✓ and so is a test

✓ 1 passed
```

## Why another test framework?

The idea for this library came out of my growing frustration with pytest,
especially its [`parametrize`][1] feature.

In jasmine, parametrization is trivial:

```js
describe('#isNumber', function() {
	[1, 1000000, 0, -1].forEach(function(i) {
		it('recognizes ' + i, function() {
			expect(isNumber(i)).toBe(true);
		});
	});
});
```

This is because the tests are [registered explicitly][2]. The popular python
test frameworks (pytest, unittest) on the other hand use an implicit mechanism
where each function that starts with 'test\_' is registered. This makes
parametrization way harder than it needs to be.

This library is an attempt to bring the explicit approach to python. However,
there are two important differences between the languages that make this
approach a bit less elegant in python:

-	The test functions will never be called explicitly, so there is really no
	need for a name. But python does not have anonymous functions. Not a big
	deal, but still awkward, especially for things like `before_each` and
	`after_each`.

-	In python, variables are local by default. If you want to write to variables
	from a descendant scope you have to use the `nonlocal` (or `global`) keyword.

[1]: https://docs.pytest.org/en/latest/parametrize.html
[2]: https://mochajs.org/#dynamically-generating-tests

## Reference

### `@test(name=None, args=[], decorators=[])`

Register a function as a test:

*	`name` (str): The name of this test (defaults to the function name)
*	`args` (list): Arguments that should be passed to the test function
*	`decorators` (list): The test function will be passed through these decorators before being executed

Async functions are automatically executed in an event loop.

```python
import assamtest
from assamtest import expect

@assamtest.test(args=['+', 5])
@assamtest.test(args=['*', 6])
def my_test(op, value):
	assamtest.expect.equal(eval('2 %s 3' % op), value)
```

### `@suite(name=None, args=[], decorators=[])`

Register a function as a suite:

```python
import assamtest
from assamtest import expect

@assamtest.suite()
def my_suite():
	@assamtest.before_each()
	def _before_each():
		pass  # do some setup here

	@assamtest.test()
	def my_test():
		expect.equal(2 + 2, 4)
```

The optional parameters are the same as for `test()`.

### `@before()` / `@after()`

Register a function to run before/after the whole suite.

There can be only one `before`/`after` function per suite.

### `@before_each()` / `@after_each()`

Register a function to run before/after every test.

There can be only one `before_each`/`after_each` function per suite.

### `expect`

A wrapper around the asserts from `unittest.TestCase` using snake case:

```python
from assamtest import expect

expect.equal(2 + 2, 4)
expect.not_equal(2 + 2, 5)
expect._in(2, [1, 2, 3])
with expect.raises(KeyError):
	{'foo': 0}['bar']
```

See also the [full list of available assertions](https://docs.python.org/3/library/unittest.html?highlight=unittest%20testcase#assert-methods>).

### `@decorators.skip`

Do not execute the test at all::

```python
import assamtest
from assamtest import expect
from assamtest.decorators import skip

@assamtest.test(decorators=[skip])
def my_test():
	expect.equal(2 + 2, 5)
```

### `@decorators.fail`

Invert the result of the test: If it would fail, pass instead. If it would
pass, fail instead::

```python
import assamtest
from assamtest import expect
from assamtest.decorators import fail

@assamtest.test(args=[4])
@assamtest.test(args=[5], decorators=[fail])
def my_test(value):
	expect.equal(2 + 2, value)
```

### `Outcome(err, status, level)`

Can be used to implement custom outcomes.

*	`err` (Exception|str|None): The reason for this outcome, e.g. an exception or a helpful message
*	`status` (str): The status, e.g. 'passed', 'failed', or 'skipped'
*	`level` ('SUCCESS'|'INFO'|'WARNING'|'ERROR'): A hint for the reporter how this outcome should be interpreted

A good example of how this can be used is `decorators.skip()`:

```python
import functools
from assamtest import Outcome

def skip(fn):
	@functools.wraps(fn)
	def wrapper(*args, **kwargs):
		raise Outcome(None, 'skipped', 'INFO')
	return wrapper
```
