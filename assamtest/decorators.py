import asyncio
import functools

from .expect import expect


def fail(fn):
	@functools.wraps(fn)
	def wrapper(*args, **kwargs):
		with expect.raises(AssertionError):
			fn(*args, **kwargs)
	return wrapper


def skip(fn):
	@functools.wraps(fn)
	def wrapper(*args, **kwargs):
		pass
	return wrapper


def async_test(fn):
	@functools.wraps(fn)
	def wrapper(*args, **kwargs):
		coro = asyncio.coroutine(fn)
		future = coro(*args, **kwargs)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(future)
		loop.close()
	return wrapper
