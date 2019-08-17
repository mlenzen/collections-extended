"""util functions for collections_extended."""
from functools import wraps
import textwrap
import warnings


def hash_iterable(it):
	"""Perform a O(1) memory hash of an iterable of arbitrary length.

	hash(tuple(it)) creates a temporary tuple containing all values from it
	which could be a problem if it is large.

	See discussion at:
	https://groups.google.com/forum/#!msg/python-ideas/XcuC01a8SYs/e-doB9TbDwAJ
	"""
	hash_value = hash(type(it))
	for value in it:
		hash_value = hash((hash_value, value))
	return hash_value


class Sentinel(object):
	"""A class to create sentinel objects.

	The benefits vs. object() are a good repr it is picklable.

	Inspired by https://pypi.org/project/sentinels/
	"""

	_registry = {}

	def __getnewargs__(self):
		return self._name,

	def __new__(cls, _name):
		"""Find the Sentinel object with name or create a new one."""
		try:
			return cls._registry[_name]
		except KeyError:
			new = super(Sentinel, cls).__new__(cls)
			cls._registry[_name] = new
			return new

	def __init__(self, name):
		super(Sentinel, self).__init__()
		self._name = name

	def __repr__(self):
		return '<%s>' % self._name

	def __bool__(self):
		return False

	def __eq__(self, other):
		if other.__class__ == self.__class__:
			return self._name == other._name
		return False


NOT_SET = Sentinel('not_set')


def deprecation_warning(msg):
	"""Raise a deprecation warning."""
	warnings.warn(msg, category=DeprecationWarning, stacklevel=2)


def deprecated(msg, dep_version):
	"""Decorate a function, method or class to mark as deprecated.

	Raise DeprecationWarning and add a deprecation notice to the docstring.
	"""
	def wrapper(func):
		docstring = func.__doc__ or ''
		docstring_msg = '.. deprecated:: {version} {msg}'.format(
			version=dep_version,
			msg=msg,
			)
		if docstring:
			# We don't know how far to indent this message
			# so instead we just dedent everything.
			string_list = docstring.splitlines()
			first_line = string_list[0]
			remaining = textwrap.dedent(''.join(string_list[1:]))
			docstring = '\n'.join([
				first_line,
				remaining,
				'',
				docstring_msg,
				])
		else:
			docstring = docstring_msg
		func.__doc__ = docstring

		@wraps(func)
		def inner(*args, **kwargs):
			deprecation_warning(msg)
			return func(*args, **kwargs)

		return inner

	return wrapper
