def fail(fn):
	def wrapper():
		try:
			fn()
		except AssertionError:
			return
		assert False, 'Expected to fail'
	return wrapper


def skip(fn):
	def wrapper():
		pass
	return wrapper
