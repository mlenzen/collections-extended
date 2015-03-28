import bisect

# Singleton to mark
_empty = object()


def _remove_all(mapping, keys):
	'''Remove all keys from mapping.'''
	for key in keys:
		del mapping[key]


class RangeMap():

	def __init__(self, mapping=None, default_value=_empty):
		'''
		Args:
			mapping: A Mapping from range start dates to values. The end of each
				range is the beginning of the next
		'''
		self.ordered_keys = []
		self.key_mapping = {}
		self._left_value = default_value
		if mapping:
			for key, value in sorted(mapping.items()):
				self.set(value, key)

	def __getitem(self, key):
		'''Helper method.'''
		loc = bisect.bisect_left(self.ordered_keys, key)
		if loc == 0 and (len(self.ordered_keys) == 0 or key < self.ordered_keys[loc]):
			return self._left_value
		else:
			if loc < len(self.ordered_keys) and key == self.ordered_keys[loc]:
				return self.key_mapping[self.ordered_keys[loc]]
			else:
				return self.key_mapping[self.ordered_keys[loc-1]]

	def __getitem__(self, key):
		if isinstance(key, slice):
			if key.step:
				raise ValueError('Steps aren\'t allowed')
			# return a RangeMap
			return self.get_range(key.start, key.stop)
		else:
			value = self.__getitem(key)
			if value is _empty:
				raise KeyError()
			else:
				return value

	def get(self, key, restval=None):
		value = self.__getitem(key)
		if value is _empty:
			return restval
		else:
			return value

	def get_range(self, start, stop):
		raise NotImplementedError('yet')

	# Python2 - override slice methods
	def __setslice__(self, i, j, value):
		'''Implement __setslice__ to override behavior in Python 2.
		This is required because empty slices pass integers in python2 as opposed
		to None in python 3.
		'''
		raise SyntaxError('Assigning slices doesn\t work in Python 2, use set')

	def __delslice__(self, i, j):
		raise SyntaxError('Deleting slices doesn\t work in Python 2, use delete')

	def __getslice__(self, i, j):
		raise SyntaxError('Getting slices doesn\t work in Python 2, use get_range.')

	def __setitem__(self, key, value):
		if not isinstance(key, slice):
			raise ValueError('Can only set slices')
		if key.step is not None:
			raise ValueError('Steps aren\'t allowed')
		self.set(value, key.start, key.stop)

	def set(self, value, start=None, stop=None):
		if start is None:
			if stop is None:
				self.ordered_keys = []
				self.key_mapping = {}
			else:
				stop_index = bisect.bisect_left(self.ordered_keys, stop)
				self.key_mapping[stop] = self.__getitem(stop)
				_remove_all(self.key_mapping, self.ordered_keys[:stop_index])
				self.ordered_keys[:stop_index] = [stop]
			self._left_value = value
		else:
			start_index = bisect.bisect_left(self.ordered_keys, start)
			if stop is None:
				stop_index = len(self.ordered_keys)
				new_keys = [start]
			else:
				stop_index = bisect.bisect_left(self.ordered_keys, stop)
				self.key_mapping[stop] = self.__getitem(stop)
				new_keys = [start, stop]
			_remove_all(self.key_mapping, self.ordered_keys[start_index:stop_index])
			self.ordered_keys[start_index:stop_index] = new_keys
			self.key_mapping[start] = value

	def delete(self, start=None, stop=None):
		raise NotImplementedError('yet')

	def __delitem__(self, index):
		if not isinstance(index, slice):
			raise IndexError('Can only delete slices')
		self.delete(index.start, index.stop)

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.ordered_keys == other.ordered_keys and
			self.key_mapping == other.key_mapping and
			self._left_value == other._left_value
			)
