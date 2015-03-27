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
				self[key:] = value

	def _getitem(self, key):
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
			# return a RangeMap
			raise NotImplementedError('yet')
		else:
			value = self._getitem(key)
			if value is _empty:
				raise KeyError()
			else:
				return value

	# Implement MutableSequence
	def __setitem__(self, key, value):
		if not isinstance(key, slice):
			raise IndexError('Can only set intervals')
		if key.step is not None:
			raise IndexError('Steps aren\'t allowed')
		if key.start is None:
			if key.stop is None:
				self.ordered_keys = []
				self.key_mapping = {}
			else:
				stop_index = bisect.bisect_left(self.ordered_keys, key.stop)
				self.key_mapping[key.stop] = self._getitem(key.stop)
				_remove_all(self.key_mapping, self.ordered_keys[:stop_index])
				self.ordered_keys[:stop_index] = [key.stop]
			self._left_value = value
		else:
			start_index = bisect.bisect_left(self.ordered_keys, key.start)
			if key.stop is None:
				stop_index = len(self.ordered_keys)
				new_keys = [key.start]
			else:
				stop_index = bisect.bisect_left(self.ordered_keys, key.stop)
				self.key_mapping[key.stop] = self._getitem(key.stop)
				new_keys = [key.start, key.stop]
			_remove_all(self.key_mapping, self.ordered_keys[start_index:stop_index])
			self.ordered_keys[start_index:stop_index] = new_keys
			self.key_mapping[key.start] = value

	def __delitem__(self, index):
		if not isinstance(index, slice):
			raise IndexError('Can only delete intervals')
		raise NotImplementedError('yet')

	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.ordered_keys == other.ordered_keys and
			self.key_mapping == other.key_mapping and
			self._left_value == other._left_value
			)
