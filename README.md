## `@test(name=None, args=[], decorators=[])`

Register a function as a test:

*	`name` (str): The name of this test (defaults to the function name)
*	`args` (list): Arguments that should be passed to the test function
*	`decorators` (list): The test function will be passed through these decorators before being executed

```python
import assamtest
from assamtest import expect

@assamtest.test(args=['+', 5])
@assamtest.test(args=['*', 6])
def my_test(op, value):
	assamtest.expect.equal(eval('2 %s 3' % op), value)
```

## `@suite(name=None, args=[], decorators=[])`

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

## `@before()` / `@after()`

Register a function to run before/after the whole suite.

There can be only one `before`/`after` function per suite.

## `@before_each()` / `@after_each()`

Register a function to run before/after every test.

There can be only one `before_each`/`after_each` function per suite.

## `expect`

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

## `@decorators.skip`

Do not execute the test at all::

```python
import assamtest
from assamtest import expect
from assamtest.decorators import skip

@assamtest.test(decorators=[skip])
def my_test():
	expect.equal(2 + 2, 5)
```

## `@decorators.fail`

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

## `@decorator.synchronize`

Start an asyncio event loop for the test and wait for it to complete::

```python
import asyncio

import assamtest
from assamtest import expect
from assamtest.decorators import synchronize

@assamtest.test()
@synchronize
async def my_test():
	await asyncio.sleep(0.1)
	expect.equal(2 + 2, 4)
```

## `Outcome(err, status, level)`

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
