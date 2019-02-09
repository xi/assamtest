stack = [{'tests': [], 'units': []}]


def _unit_push():
	stack.append({'tests': [], 'units': []})


def _unit_pop(name):
	tmp = stack.pop()
	if tmp['tests'] or tmp['units']:
		stack[-1]['units'].append((name, tmp))


def unit(name=None):
	def decorator(fn):
		_unit_push()
		fn()
		_unit_pop(name or fn.__name__)
		return fn
	return decorator


def test(name=None, args=[], decorators=[]):
	def decorator(fn):
		_name = name or fn.__name__
		if args:
			_name += ':' + ';'.join(str(arg) for arg in args)

		def wrapper():
			fn(*args)

		for d in decorators:
			wrapper = d(wrapper)

		stack[-1]['tests'].append((_name, wrapper))
		return fn
	return decorator


def before():
	def decorator(fn):
		stack[-1]['before'] = fn
		return fn
	return decorator


def before_each():
	def decorator(fn):
		stack[-1]['before_each'] = fn
		return fn
	return decorator


def after():
	def decorator(fn):
		stack[-1]['after'] = fn
		return fn
	return decorator


def after_each():
	def decorator(fn):
		stack[-1]['after_each'] = fn
		return fn
	return decorator
