import bisect
from collections import namedtuple, Container

# Singleton to mark unmapped ranges
_empty = object()

MappedRange = namedtuple('MappedRange', ('start', 'stop', 'value'))


def _remove_all(mapping, keys):
	'''Remove all keys from mapping.'''
	for key in keys:
		del mapping[key]


class RangeMap(Container):

	def __init__(self, mapping=None, default_value=_empty):
		'''
		Args:
			mapping: A Mapping from range start dates to values. The end of each
				range is the beginning of the next
		'''
		self._ordered_keys = []
		self._key_mapping = {}
		self._left_value = default_value
		if mapping:
			for key, value in sorted(mapping.items()):
				self.set(value, key)

	def __repr__(self):
		return 'RangeMap(%s)' % ', '.join(['({start}, {stop}): {value}'.format(
			start=item.start,
			stop=item.stop,
			value=repr(item.value),
			) for item in self.ranges()])

	@classmethod
	def from_iterable(cls, iterable):
		'''Create a RangeMap from an iterable where each item is a tuple
		(start, stop, value)
		'''
		obj = cls()
		for start, stop, value in iterable:
			obj.set(value, start=start, stop=stop)
		return obj

	def ranges(self):
		'''Generate MappedRanges for all mapped ranges.'''
		if len(self._ordered_keys) == 0:
			if self._left_value is not _empty:
				yield MappedRange(None, None, self._left_value)
		else:
			if self._left_value is not _empty:
				yield MappedRange(None, self._ordered_keys[0], self._left_value)
			for i, start_key in enumerate(self._ordered_keys[:-1]):
				value = self._key_mapping[start_key]
				if value is not _empty:
					yield MappedRange(start_key, self._ordered_keys[i+1], value)
			last_value = self._key_mapping[self._ordered_keys[-1]]
			if last_value is not _empty:
				yield MappedRange(self._ordered_keys[-1], None, last_value)

	def __contains__(self, value):
		return self.__getitem(value) is not _empty

	def __getitem(self, key):
		'''Helper method.'''
		loc = bisect.bisect_left(self._ordered_keys, key)
		if loc == 0 and (len(self._ordered_keys) == 0 or key < self._ordered_keys[loc]):
			return self._left_value
		else:
			if loc < len(self._ordered_keys) and key == self._ordered_keys[loc]:
				return self._key_mapping[self._ordered_keys[loc]]
			else:
				return self._key_mapping[self._ordered_keys[loc-1]]

	def get(self, key, restval=None):
		value = self.__getitem(key)
		if value is _empty:
			return restval
		else:
			return value

	def get_range(self, start=None, stop=None):
		raise NotImplementedError('yet')

	def set(self, value, start=None, stop=None):
		if start is None:
			if stop is None:
				self._ordered_keys = []
				self._key_mapping = {}
			else:
				stop_index = bisect.bisect_left(self._ordered_keys, stop)
				self._key_mapping[stop] = self.__getitem(stop)
				_remove_all(self._key_mapping, self._ordered_keys[:stop_index])
				if stop_index < len(self._ordered_keys) and self._ordered_keys[stop_index] == stop:
					self._ordered_keys[:stop_index+1] = [stop]
				else:
					self._ordered_keys[:stop_index] = [stop]
			self._left_value = value
		else:
			start_index = bisect.bisect_left(self._ordered_keys, start)
			if stop is None:
				stop_index = len(self._ordered_keys)
				new_keys = [start]
			else:
				stop_index = bisect.bisect_left(self._ordered_keys, stop)
				self._key_mapping[stop] = self.__getitem(stop)
				new_keys = [start, stop]
			_remove_all(self._key_mapping, self._ordered_keys[start_index:stop_index])
			if stop_index < len(self._ordered_keys) and self._ordered_keys[stop_index] == stop:
				self._ordered_keys[start_index:stop_index+1] = new_keys
			else:
				self._ordered_keys[start_index:stop_index] = new_keys
			self._key_mapping[start] = value

	def delete(self, start=None, stop=None):
		self.set(_empty, start=start, stop=stop)

	def __eq__(self, other):
		if isinstance(other, RangeMap):
			return (
				self._key_mapping == other._key_mapping and
				self._left_value == other._left_value
				)
		else:
			return NotImplemented

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

	def __setitem__(self, key, value):
		if not isinstance(key, slice):
			raise ValueError('Can only set slices')
		if key.step is not None:
			raise ValueError('Steps aren\'t allowed')
		self.set(value, key.start, key.stop)

	def __delitem__(self, index):
		if not isinstance(index, slice):
			raise ValueError('Can only delete slices')
		if index.step is not None:
			raise ValueError('Steps aren\'t allowed')
		self.delete(index.start, index.stop)

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
