"""util functions for collections_extended."""
from functools import wraps
import textwrap
from typing import Any, List
import warnings

__all__ = (
	'deprecated',
	'deprecation_warning',
	'hash_iterable',
	'list_remove_value',
)


def list_remove_value(lst: List, val: Any, max_count: int = None) -> int:
	"""Remove copies of a value from a list in-place.

	Args:
		lst: The list to remove values from
		val: The value to remove from the list
		max_count: The maximum number of values to remove from the list, None
			to indicate no maximum
	Returns:
		The number of values removed from the list
	"""
	max_count = len(lst) if max_count is None else max_count
	out = []
	count = 0
	for item in lst:
		if item == val and count < max_count:
			count += 1
		else:
			out += item
	lst[:] = out
	return count


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


def deprecation_warning(msg):
	"""Raise a deprecation warning."""
	warnings.warn(msg, category=DeprecationWarning, stacklevel=2)


def deprecated(msg, dep_version):
	"""Decorate a function, method or class to mark as deprecated.

	Raise DeprecationWarning and add a deprecation notice to the docstring.

	Args:
		msg: The message to document
		dep_version: The version in which this was deprecated
	See:
		https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-deprecated

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
