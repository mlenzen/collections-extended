"""util functions for collections_extended."""


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

	The benefits
	Inspired by https://pypi.org/project/sentinels/
	"""

	_registry = {}

	def __getnewargs__(self):
		return self._name,

	def __new__(cls, _name):
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
