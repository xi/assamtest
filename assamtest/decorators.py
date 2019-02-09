import asyncio
import functools

from .expect import expect
from .runner import Outcome


def fail(fn):
	@functools.wraps(fn)
	def wrapper(*args, **kwargs):
		with expect.raises(AssertionError):
			fn(*args, **kwargs)
	return wrapper


def skip(fn):
	@functools.wraps(fn)
	def wrapper(*args, **kwargs):
		raise Outcome(None, 'skipped', 'INFO')
	return wrapper


def synchronize(fn):
	@functools.wraps(fn)
	def wrapper(*args, **kwargs):
		coro = asyncio.coroutine(fn)
		future = coro(*args, **kwargs)
		loop = asyncio.get_event_loop()
		loop.run_until_complete(future)
		loop.close()
	return wrapper
