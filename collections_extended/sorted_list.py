"""SortedList class definition."""

import bisect
from collections import MutableSequence


class SortedList(MutableSequence):
	"""Extends list and keeps values in sorted order.

	A key can be specified like for sorted.

	All list methods are inherited but raise a ValueError if they result in
	inserting a value in the wrong order.

	SortedList cannot enforce correct ordering after mutable elements are
	added then modified.
	"""

	def __init__(self, iterable=None, key=None, reverse=None):
		self._data = list(sorted(iterable, key=key, reverse=reverse))
		# TODO this is inefficient, should only evaluate keys once
		self._set_key_data(key, reverse)

	def sort(self, key=None, reverse=False):
		self._data.sort(key=key, reverse=reverse)
		# TODO this is inefficient, should only evaluate keys once
		self._set_key_data(key, reverse)

	def _set_key_data(self, key, reverse):
		self._key = key
		self._reverse = reverse
		if self._key:
			self._keys = [self.key(v for v in self._data)]
		else:
			self._keys = self._data

	@property
	def key(self):
		if self._key is None:
			return lambda x: x
		else:
			return self._key

	@key.setter
	def key(self, new_value):
		if new_value != self._key:
			self.sort(key=new_value, reverse=self.reverse)

	@property
	def reverse(self):
		return self._reverse

	@reverse.setter
	def reverse(self, new_value):
		if new_value != self._reverse:
			self.sort(key=self.key, reverse=new_value)

	def __str__(self):
		return str(self._data)

	def __repr__(self):
		return 'SortedList({data!r})'.format(data=self._data)

	# Implement Container
	def __contains__(self, value):
		try:
			self.index(value)
		except ValueError:
			return False
		else:
			return True

	# Implement Sized
	def __len__(self):
		return len(self._data)

	# Implement Sequence
	def __getitem__(self, index):
		return self._data.__getitem__(index)

	def count(self, value, start=0, end=None):
		first_index = self.index_left(value, start=start, stop=end)
		out = 0
		for v in self[first_index:]:
			if v == value:
				out += 1
			else:
				break
		return out

	# Implement MutableSequence
	def __setitem__(self, index, value):
		value_key = self.key(value)
		if index - 1 >= 0 and value_key < self._keys[index - 1]:
			raise ValueError
		if index + 1 < len(self) and value_key > self._keys[index + 1]:
			raise ValueError
		self._data[index] = value
		self._keys[index] = value_key

	def __delitem__(self, index):
		self._data.__delitem__(index)
		if self._keys is not self._data:
			self._keys.__delitem__(index)

	def _insert(self, index, value, value_key):
		self._data.insert(index, value)
		if self._keys is not self._data:
			self._keys.insert(value_key)

	def insert(self, index, value):
		value_key = self.key(value)
		if index - 1 >= 0 and value_key < self._keys[index - 1]:
			raise ValueError
		if index + 1 < len(self) and value_key > self._keys[index + 1]:
			raise ValueError
		self._insert(index, value, value_key)

	def add_left(self, value):
		value_key = self.key(value)
		index = bisect.bisect_left(self._keys, value_key)
		self._insert(index, value, value_key)

	def add_right(self, value):
		value_key = self.key(value)
		index = bisect.bisect_right(self._keys, value_key)
		self._insert(index, value, value_key)

	add = add_right

	def index_left(self, value, start=0, stop=None):
		"""Return the index of the first occurence of value."""
		value_key = self.key(value)
		i = bisect.bisect_left(self._keys, value_key, start, stop)
		if i == len(self._keys) or self._data[i] != value:
			raise ValueError
		return i

	def index_right(self, value, start=0, stop=None):
		"""Return the index to the right of the last occurence of value."""
		value_key = self.key(value)
		i = bisect.bisect_right(self._keys, value_key, start, stop)
		if i == len(self._keys) or self._data[i] != value:
			raise ValueError
		return i

	index = index_left
