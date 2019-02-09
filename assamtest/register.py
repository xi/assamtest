stack = [{'tests': [], 'suites': []}]


def _suite_push():
	stack.append({'tests': [], 'suites': []})


def _suite_pop(name):
	tmp = stack.pop()
	if tmp['tests'] or tmp['suites']:
		stack[-1]['suites'].append((name, tmp))


def _prepare(name, args, decorators, fn):
	_name = name or fn.__name__
	if args:
		_name += ':' + ';'.join(str(arg) for arg in args)

	def wrapper():
		fn(*args)

	for d in decorators:
		wrapper = d(wrapper)

	return _name, wrapper


def suite(name=None, args=[], decorators=[]):
	def decorator(fn):
		_name, wrapper = _prepare(name, args, decorators, fn)
		_suite_push()
		wrapper()
		_suite_pop(_name)
		return fn
	return decorator


def test(name=None, args=[], decorators=[]):
	def decorator(fn):
		_name, wrapper = _prepare(name, args, decorators, fn)
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
