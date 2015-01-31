""" bijection - a one-to-one onto mapping, a dict with unique values

TODO write long desc

This implementation kinda sucks because it stores everything twice.
"""

from collections import MutableMapping, Mapping


class bijection(MutableMapping):
	"""

	TODO write unit tests for bijection including dict methods like copy
	"""
	def __init__(self, iterable=None, inverse=None, **kwarg):
		self._data = {}
		if inverse is not None:
			self.inverse = inverse
		else:
			self.inverse = bijection(inverse=self)
		if iterable is not None:
			if isinstance(iterable, Mapping):
				for key, value in iterable.items():
					self[key] = value
			else:
				for pair in iterable:
					self[pair[0]] = pair[1]
		for key, value in kwarg.items():
			self[key] = value

	# Required for MutableMapping
	def __len__(self):
		return len(self._data)

	# Required for MutableMapping
	def __getitem__(self, key):
		return self._data[key]

	# Required for MutableMapping
	def __setitem__(self, key, value):
		if key in self:
			del self.inverse._data[self[key]]
		if value in self.inverse:
			del self._data[self.inverse[value]]
		self._data[key] = value
		self.inverse._data[value] = key

	# Required for MutableMapping
	def __delitem__(self, key):
		value = self._data.pop(key)
		del self.inverse._data[value]

	# Required for MutableMapping
	def __iter__(self):
		return iter(self._data)

	def __contains__(self, key):
		return key in self._data

	def clear(self):
		""" This should be more efficient than MutableMapping.clear """
		self._data.clear()
		self.inverse._data.clear()

	def copy(self):
		return bijection(self)

	def items(self):
		return self._data.items()

	def keys(self):
		return self._data.keys()

	def values(self):
		return self.inverse.keys()

	def __eq__(self, other):
		return isinstance(other, bijection) and self._data == other._data
