"""RangeMap class definition."""
from bisect import bisect_left, bisect_right
from collections import namedtuple, Container, Mapping


# Used to mark unmapped ranges
_empty = object()
_first = object()

MappedRange = namedtuple('MappedRange', ('start', 'stop', 'value'))


def _check_start_stop(start, stop):
	if start is not None and stop is not None and stop <= start:
		raise ValueError('stop must be > start')


class RangeMap(Container):
	"""Map ranges of orderable elements to values."""

	def __init__(self, iterable=None, default_value=_empty):
		"""Create a RangeMap.

		A mapping or other iterable can be passed to initialize the RangeMap.
		If mapping is passed, it is interpreted as a mapping from range start
		indices to values.
		If an iterable is passed, each element will define a range in the
		RangeMap and should be formatted (start, stop, value).

		Args:
			iterable: A Mapping or an Iterable to initialize from.
			default_value: If passed, the return value for all keys less than the
				least key in mapping. If no mapping, the return value for all keys.
		"""
		self._ordered_keys = [_first]
		self._key_mapping = {_first: default_value}
		if iterable:
			if isinstance(iterable, Mapping):
				self._init_from_mapping(iterable)
			else:
				self._init_from_iterable(iterable)

	@classmethod
	def from_mapping(cls, mapping):
		"""Create a RangeMap from a mapping of interval starts to values."""
		obj = cls()
		obj._init_from_mapping(mapping)
		return obj

	def _init_from_mapping(self, mapping):
		for key, value in sorted(mapping.items()):
			self.set(value, key)

	@classmethod
	def from_iterable(cls, iterable):
		"""Create a RangeMap from an iterable of tuples defining each range.

		Each element of the iterable is a tuple (start, stop, value).
		"""
		obj = cls()
		obj._init_from_iterable(iterable)
		return obj

	def _init_from_iterable(self, iterable):
		for start, stop, value in iterable:
			self.set(value, start=start, stop=stop)

	def __str__(self):
		values = ', '.join(['({start}, {stop}): {value}'.format(
			start=item.start,
			stop=item.stop,
			value=item.value,
			) for item in self.ranges()])
		return 'RangeMap(%s)' % values

	def __repr__(self):
		values = ', '.join(['({start!r}, {stop!r}, {value!r})'.format(
			start=item.start,
			stop=item.stop,
			value=item.value,
			) for item in self.ranges()])
		return 'RangeMap([%s])' % values

	def _bisect_left(self, key):
		if key == _first:
			return 0
		else:
			return bisect_left(self._ordered_keys, key, lo=1)

	def _bisect_right(self, key):
		if key == _first:
			return 0
		else:
			return bisect_right(self._ordered_keys, key, lo=1)

	def ranges(self, start=None, stop=None):
		"""Generate MappedRanges for all mapped ranges.

		Yields:
			MappedRange
		"""
		_check_start_stop(start, stop)
		if start is None:
			start_loc = 1
			start = _first
		else:
			start_loc = self._bisect_right(start)
		if stop is None:
			stop_loc = len(self._ordered_keys)
		else:
			stop_loc = self._bisect_left(stop)
		candidate_keys = [start] + self._ordered_keys[start_loc:stop_loc] + [stop]
		for start_key, stop_key in zip(candidate_keys[:-1], candidate_keys[1:]):
			value = self.__getitem(start_key)
			if value is not _empty:
				if start_key == _first:
					start_key = None
				yield MappedRange(start_key, stop_key, value)

	def __contains__(self, value):
		return self.__getitem(value) is not _empty

	def __getitem(self, key):
		"""Get the value for a key (not a slice)."""
		try:
			return self._key_mapping[key]
		except KeyError:
			loc = self._bisect_right(key) - 1
			return self._key_mapping[self._ordered_keys[loc]]

	def get(self, key, restval=None):
		"""Get the value of the range containing key, otherwise return restval."""
		value = self.__getitem(key)
		if value is _empty:
			return restval
		else:
			return value

	def get_range(self, start=None, stop=None):
		"""Return a RangeMap for the range start to stop.

		Returns:
			A RangeMap
		"""
		return self.from_iterable(self.ranges(start, stop))

	def set(self, value, start=None, stop=None):
		"""Set the range from start to stop to value."""
		_check_start_stop(start, stop)
		if start is None:
			start = _first
			start_index = 0
		else:
			start_index = self._bisect_left(start)
			prev_key = self._ordered_keys[start_index - 1]
			prev_value = self._key_mapping[prev_key]
			if prev_value == value:
				start_index -= 1
				start = prev_key
		if stop is None:
			new_keys = [start]
			stop_index = len(self._ordered_keys)
		else:
			stop_index = self._bisect_left(stop)
			new_keys = [start, stop]
			self._key_mapping[stop] = self.__getitem(stop)
			if stop_index < len(self._ordered_keys):
				next_key = self._ordered_keys[stop_index]
				if next_key == stop:
					new_keys = [start]
					next_value = self._key_mapping[next_key]
					if next_value == value:
						stop_index += 1
		for key in self._ordered_keys[start_index:stop_index]:
			del self._key_mapping[key]
		self._ordered_keys[start_index:stop_index] = new_keys
		self._key_mapping[start] = value

	def delete(self, start=None, stop=None):
		"""Delete the range from start to stop from self."""
		self.set(_empty, start=start, stop=stop)

	def clear(self):
		self._ordered_keys = [_first]
		self._key_mapping = {_first: _empty}

	def __eq__(self, other):
		if isinstance(other, RangeMap):
			return self._key_mapping == other._key_mapping
		else:
			return False

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
		"""Implement __setslice__ to override behavior in Python 2.

		This is required because empty slices pass integers in python2 as opposed
		to None in python 3.
		"""
		raise SyntaxError('Assigning slices doesn\t work in Python 2, use set')

	def __delslice__(self, i, j):
		raise SyntaxError('Deleting slices doesn\t work in Python 2, use delete')

	def __getslice__(self, i, j):
		raise SyntaxError('Getting slices doesn\t work in Python 2, use get_range.')
