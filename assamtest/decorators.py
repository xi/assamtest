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
