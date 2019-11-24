"""util functions for collections_extended."""
from functools import wraps
import textwrap
from typing import Iterable, Hashable, Dict, Callable, Sized, Optional
import warnings

__all__ = ('hash_iterable', 'deprecated')


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


def deprecation_warning(msg: str):
	"""Raise a deprecation warning."""
	warnings.warn(msg, category=DeprecationWarning, stacklevel=2)


def deprecated(msg: str, dep_version: str) -> Callable:
	"""Decorate a function, method or class to mark as deprecated.

	Raise DeprecationWarning and add a deprecation notice to the docstring.

	Args:
		msg: The message to document
		dep_version: The version in which this was deprecated
	See:
		https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-deprecated

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
			deprecation_warning(msg)
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
