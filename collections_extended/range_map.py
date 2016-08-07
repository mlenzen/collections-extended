"""RangeMap class definition."""
from bisect import bisect_left, bisect_right
from collections import namedtuple, Container, Mapping


# Used to mark unmapped ranges
_empty = object()
_first = object()

MappedRange = namedtuple('MappedRange', ('start', 'stop', 'value'))


def _check_start_stop(start, stop):
	"""Check that start and stop are valid - orderable and in the right order.

	Raises:
		ValueError: if stop <= start
		TypeError: if unorderable
	"""
	if start is not None and stop is not None and stop <= start:
		raise ValueError('stop must be > start')


def _check_key_slice(key):
	if not isinstance(key, slice):
		raise TypeError('Can only set and delete slices')
	if key.step is not None:
		raise ValueError('Cannot set or delete slices with steps')


class RangeMap(Container):
	"""Map ranges of orderable elements to values."""

	def __init__(self, iterable=None, **kwargs):
		"""Create a RangeMap.

		A mapping or other iterable can be passed to initialize the RangeMap.
		If mapping is passed, it is interpreted as a mapping from range start
		indices to values.
		If an iterable is passed, each element will define a range in the
		RangeMap and should be formatted (start, stop, value).

		default_value is a an optional keyword argument that will initialize the
		entire RangeMap to that value. Any missing ranges will be mapped to that
		value. However, if ranges are subsequently deleted they will be removed
		and *not* mapped to the default_value.

		Args:
			iterable: A Mapping or an Iterable to initialize from.
			default_value: If passed, the return value for all keys less than the
				least key in mapping or missing ranges in iterable. If no mapping
				or iterable, the return value for all keys.
		"""
		default_value = kwargs.pop('default_value', _empty)
		if kwargs:
			raise TypeError('Unknown keyword arguments: %s' % ', '.join(kwargs.keys()))
		self._keys = [_first]
		self._values = [default_value]
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
		range_format = '({range.start}, {range.stop}): {range.value}'
		values = ', '.join([range_format.format(range=r) for r in self.ranges()])
		return 'RangeMap(%s)' % values

	def __repr__(self):
		range_format = '({range.start!r}, {range.stop!r}, {range.value!r})'
		values = ', '.join([range_format.format(range=r) for r in self.ranges()])
		return 'RangeMap([%s])' % values

	def _bisect_left(self, key):
		if key == _first:
			return 0
		else:
			return bisect_left(self._keys, key, lo=1)

	def _bisect_right(self, key):
		if key == _first:
			return 0
		else:
			return bisect_right(self._keys, key, lo=1)

	def ranges(self, start=None, stop=None):
		"""Generate MappedRanges for all mapped ranges.

		Yields:
			MappedRange
		"""
		_check_start_stop(start, stop)
		if start is None:
			start_loc = 1
		else:
			start_loc = self._bisect_right(start)
		if stop is None:
			stop_loc = len(self._keys)
		else:
			stop_loc = self._bisect_left(stop)
		start_val = self._values[start_loc - 1]
		candidate_keys = [start] + self._keys[start_loc:stop_loc] + [stop]
		candidate_values = [start_val] + self._values[start_loc:stop_loc]
		for i, value in enumerate(candidate_values):
			if value is not _empty:
				start_key = candidate_keys[i]
				stop_key = candidate_keys[i + 1]
				yield MappedRange(start_key, stop_key, value)

	def __contains__(self, value):
		try:
			self.__getitem(value) is not _empty
		except KeyError:
			return False
		else:
			return True

	def __bool__(self):
		if len(self._keys) > 1:
			return True
		else:
			return self._values[0] != _empty

	__nonzero__ = __bool__

	def __getitem(self, key):
		"""Get the value for a key (not a slice)."""
		if key == _first:
			loc = 0
		else:
			loc = self._bisect_right(key) - 1
		value = self._values[loc]
		if value is _empty:
			raise KeyError(key)
		else:
			return value

	def get(self, key, restval=None):
		"""Get the value of the range containing key, otherwise return restval."""
		try:
			return self.__getitem(key)
		except KeyError:
			return restval

	def get_range(self, start=None, stop=None):
		"""Return a RangeMap for the range start to stop.

		Returns:
			A RangeMap
		"""
		return self.from_iterable(self.ranges(start, stop))

	def set(self, value, start=None, stop=None):
		"""Set the range from start to stop to value."""
		_check_start_stop(start, stop)
		# start_index, stop_index will denote the sections we are replacing
		if start is None:
			start = _first
			start_index = 0
		else:
			start_index = self._bisect_left(start)
			prev_value = self._values[start_index - 1]
			if prev_value == value:
				# We're setting a range where the left range has the same
				# value, so create one big range
				start_index -= 1
				start = self._keys[start_index]
		if stop is None:
			new_keys = [start]
			new_values = [value]
			stop_index = len(self._keys)
		else:
			stop_index = self._bisect_right(stop)
			stop_value = self._values[stop_index - 1]
			stop_key = self._keys[stop_index - 1]
			if stop_key == stop and stop_value == value:
				new_keys = [start]
				new_values = [value]
			else:
				new_keys = [start, stop]
				new_values = [value, stop_value]
		self._keys[start_index:stop_index] = new_keys
		self._values[start_index:stop_index] = new_values

	def delete(self, start=None, stop=None):
		"""Delete the range from start to stop from self.

		Raises:
			KeyError: If part of the passed range isn't mapped.
		"""
		_check_start_stop(start, stop)
		if start is None:
			start_loc = 0
		else:
			start_loc = self._bisect_right(start) - 1
		if stop is None:
			stop_loc = len(self._keys)
		else:
			stop_loc = self._bisect_left(stop)
		for value in self._values[start_loc:stop_loc]:
			if value is _empty:
				raise KeyError((start, stop))
		self.set(_empty, start=start, stop=stop)  # this is inefficient, we've already found the sub ranges

	def empty(self, start=None, stop=None):
		"""Empty the range from start to stop.

		Like delete, but no Error is raised if the entire range isn't mapped.
		"""
		self.set(_empty, start=start, stop=stop)

	def clear(self):
		"""Remove all elements."""
		self._keys = [_first]
		self._values = [_empty]

	def __eq__(self, other):
		if isinstance(other, RangeMap):
			return (
				self._keys == other._keys and
				self._values == other._values
				)
		else:
			return False

	def __getitem__(self, key):
		try:
			_check_key_slice(key)
		except TypeError:
			return self.__getitem(key)
		else:
			return self.get_range(key.start, key.stop)

	def __setitem__(self, key, value):
		_check_key_slice(key)
		self.set(value, key.start, key.stop)

	def __delitem__(self, key):
		_check_key_slice(key)
		self.delete(key.start, key.stop)

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
