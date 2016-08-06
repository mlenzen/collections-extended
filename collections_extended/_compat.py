"""Python 2/3 compatibility helpers."""
import sys

is_py2 = sys.version_info[0] == 2

if is_py2:
	def keys_set(d):
		"""Return a set of passed dictionary's keys."""
		return set(d.keys())
else:
	keys_set = dict.keys


def handle_rich_comp_not_implemented():
	"""Correctly handle unimplemented rich comparisons.

	In Python 3, return NotImplemented.
	In Python 2, raise a TypeError.
	"""
	if is_py2:
		raise TypeError()
	else:
		return NotImplemented
