from bisect import bisect_left, bisect_right
from collections import namedtuple, Container

# Used to mark unmapped ranges
_empty = object()

MappedRange = namedtuple('MappedRange', ('start', 'stop', 'value'))


class RangeMap(Container):

	def __init__(self, mapping=None, default_value=_empty):
		'''
		Args:
			mapping: A Mapping from range start dates to values. The end of each
				range is the beginning of the next
			default_value: If passed, the return value for all keys less than the
				least key in mapping. If no mapping, the return value for all keys.
		'''
		self._ordered_keys = [None]
		self._key_mapping = {None: default_value}
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

	def ranges(self, start=None, stop=None):
		'''Generate MappedRanges for all mapped ranges.
		Yields:
			MappedRange
		'''
		candidate_keys = self._ordered_keys[:]
		if stop is not None:
			stop_loc = bisect_left(self._ordered_keys, stop, lo=1)
			candidate_keys = candidate_keys[:stop_loc]
		if start is not None:
			start_loc = bisect_right(self._ordered_keys, start, lo=1) - 1
			candidate_keys = candidate_keys[start_loc:]
		candidate_keys[0] = start
		candidate_keys.append(stop)
		for start_key, stop_key in zip(candidate_keys[:-1], candidate_keys[1:]):
			try:
				value = self._key_mapping[start_key]
			except KeyError:
				value = self.__getitem(start_key)
			if value is not _empty:
				yield MappedRange(start_key, stop_key, value)

	def __contains__(self, value):
		return self.__getitem(value) is not _empty

	def __getitem(self, key):
		'''Helper method.'''
		loc = bisect_right(self._ordered_keys, key, lo=1) - 1
		return self._key_mapping[self._ordered_keys[loc]]

	def get(self, key, restval=None):
		value = self.__getitem(key)
		if value is _empty:
			return restval
		else:
			return value

	def get_range(self, start=None, stop=None):
		'''
		Returns:
			A RangeMap
		'''
		return self.from_iterable(self.ranges(start, stop))

	def set(self, value, start=None, stop=None):
		if start is None:
			start_index = 0
		else:
			start_index = bisect_left(self._ordered_keys, start, 1)
		if stop is None:
			stop_index = len(self._ordered_keys)
			new_keys = [start]
		else:
			stop_index = bisect_right(self._ordered_keys, stop, 1)
			new_keys = [start, stop]
			stop_value = self.__getitem(stop)
		for key in self._ordered_keys[start_index:stop_index]:
			del self._key_mapping[key]
		if stop is not None:
			self._key_mapping[stop] = stop_value
		self._ordered_keys[start_index:stop_index] = new_keys
		self._key_mapping[start] = value

	def delete(self, start=None, stop=None):
		self.set(_empty, start=start, stop=stop)

	def __eq__(self, other):
		if isinstance(other, RangeMap):
			return self._key_mapping == other._key_mapping
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
