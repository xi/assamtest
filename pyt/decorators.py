from .expect import expect


def fail(fn):
	def wrapper():
		with expect.raises(AssertionError):
			fn()
	return wrapper


def skip(fn):
	def wrapper():
		pass
	return wrapper
