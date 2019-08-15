"""util functions for collections_extended."""
from functools import wraps
import textwrap
from typing import Iterable, Hashable, Dict, Callable, Sized, Optional
import warnings


def hash_iterable(it: Iterable[Hashable]) -> int:
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


class SentinelType(type):

	_registry: Dict = {}


class Sentinel(SentinelType, metaclass=SentinelType):
	"""A class to create sentinel objects.

	The benefits vs. object() are a good repr and is picklable.

	Sentinels are also instances of themselves, so you can use the Sentinel
	as a type decorator. For example:

	>>> NOT_SET = Sentinel('not_set')
	>>> def f(arg: Union[int, None, NOT_SET] = NOT_SET):
		pass

	Inspired by https://pypi.org/project/sentinels/
	"""

	# def __getnewargs__(self):
	# 	return (self._name, )

	def __new__(mcs, name: str, parents=None, dct=None):
		"""Find the Sentinel object with name or create a new one."""
		try:
			return mcs._registry[name]
		except KeyError:
			parents = parents or tuple()
			dct = dct or {}
			new = super(SentinelType, mcs).__new__(mcs, name, parents, dct)
			mcs._registry[name] = new
			# new.__class__ = new
			return new

	def __init__(self, name: str):
		super(Sentinel, self).__init__(name, tuple(), {})
		# super().__init__()
		# self._name: str = name

	def __repr__(self):
		return '[%s]' % self.__name__

	def __bool__(self):
		return False

	def __eq__(self, other):
		return self is other

	@classmethod
	def create_with_type(cls, name: str):
		subclass = type(name, (Sentinel, ), {})
		instance = subclass(name)
		instance.type = subclass
		return instance


# NOT_SET = Sentinel.create_with_type('not_set')
NOT_SET = Sentinel('not_set')


def deprecated(msg: str, dep_version: str) -> Callable:
	"""Decorate a function, method or class to mark as deprecated.

	Raise DeprecationWarning and add a deprecation notice to the docstring.
	"""
	def wrapper(func: Callable) -> Callable:
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
			warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
			return func(*args, **kwargs)

		return inner

	return wrapper


def fix_seq_index(self: Sized, index: Optional[int]) -> int:
	"""Fix an index for a Sequence."""
	length = len(self)
	if index is None:
		return length - 1
	if index < 0:
		index += length
	if not 0 <= index < length:
		raise IndexError('index is out of range')
	return index
