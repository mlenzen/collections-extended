"""RangeMap class definition."""
from abc import ABCMeta, abstractmethod
from bisect import bisect_left, bisect_right
from typing import Collection, Mapping, Set
from typing import Any, Hashable, Iterator, Iterable, Union, Tuple, Generator, Optional, overload

from .sentinel import NOT_SET


class MappedRange:
	"""Represents a subrange of a RangeMap.

	This is a glorified namedtuple.
	"""

	__slots__ = ('start', 'stop', 'value')

	def __init__(self, start: Hashable, stop: Hashable, value: Any):
		"""Create a mapped range.

		Args:
			start: The start of the range, inclusive.
			stop: The end of the range, exclusive.
			value: The mapped value.
		"""
		self.start = start
		self.stop = stop
		self.value = value

	# Implement __iter__ so we can unpack this
	def __iter__(self) -> Iterator:
		yield self.start
		yield self.stop
		yield self.value

	def __str__(self):
		return '[{start!r}, {stop!r}) -> {value!r}'.format(
			start=self.start,
			stop=self.stop,
			value=self.value,
			)

	def __repr__(self):
		return '{class_name}({start!r}, {stop!r}, {value!r})'.format(
			class_name=self.__class__.__name__,
			start=self.start,
			stop=self.stop,
			value=self.value,
			)

	def __eq__(self, other):
		if isinstance(other, MappedRange):
			return (self.start, self.stop, self.value) ==\
				(other.start, other.stop, other.value)
		return False


class RangeMapView(Collection):
	"""Base class for views of RangeMaps."""

	__metaclass__ = ABCMeta

	def __init__(self, mapping: 'RangeMap'):
		"""Create a RangeMapView from a RangeMap."""
		self._mapping = mapping

	def __len__(self) -> int:
		return len(self._mapping)

	@abstractmethod
	def __iter__(self):
		raise NotImplementedError

	@abstractmethod
	def __contains__(self, item: Any):
		raise NotImplementedError

	def __repr__(self) -> str:
		return '{0.__class__.__name__}({0._mapping!r})'.format(self)

	@property
	def mapping(self) -> 'RangeMap':
		"""Return the underlying RangeMap."""
		return self._mapping


class RangeMapKeysView(RangeMapView, Set):
	"""A view of the keys that mark the starts of subranges of a RangeMap.

	Since iterating over all the keys is impossible, the view only
	iterates over the keys that start each subrange.
	"""

	def __contains__(self, key: Hashable) -> bool:
		return key in self.mapping

	def __iter__(self) -> Iterator[Hashable]:
		for mapped_range in self.mapping.ranges():
			yield mapped_range.start


class RangeMapItemsView(RangeMapView, Set):
	"""A view of the items that mark the starts of subranges of a RangeMap.

	Since iterating over all the items is impossible, the view only
	iterates over the items that start each subrange.
	"""

	def __contains__(self, item):
		# TODO should item be a MappedRange instead of a 2-tuple
		key, value = item
		try:
			mapped_value = self.mapping[key]
		except KeyError:
			return False
		else:
			return mapped_value == value

	def __iter__(self):
		for mapped_range in self.mapping.ranges():
			yield (mapped_range.start, mapped_range.value)


class RangeMapValuesView(RangeMapView):
	"""A view on the values that mark the start of subranges of a RangeMap.

	Since iterating over all the values is impossible, the view only
	iterates over the values that start each subrange.
	"""

	def __contains__(self, value):
		for mapped_range in self.mapping.ranges():
			if mapped_range.value == value:
				return True
		return False

	def __iter__(self):
		for mapped_range in self.mapping.ranges():
			yield mapped_range.value


def _check_start_stop(start: Hashable, stop: Hashable):
	"""Check that start and stop are valid - orderable and in the right order.

	Raises:
		ValueError: if stop <= start
		TypeError: if unorderable
	"""
	if start is not None and stop is not None and stop <= start:
		raise ValueError('stop must be > start')


def _check_key_slice(key: Hashable):
	if not isinstance(key, slice):
		raise TypeError('Can only set and delete slices')
	if key.step is not None:
		raise ValueError('Cannot set or delete slices with steps')


class RangeMap(Mapping):
	"""Map ranges of orderable elements to values."""

	def __init__(
			self,
			iterable: Union[
				Mapping[Hashable, Any],
				Iterable[Tuple[Hashable, Hashable, Any]],
				] = None,
			default_value: Any = NOT_SET,
			):
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
		self._keys = [None]
		self._values = [default_value]
		if iterable:
			if isinstance(iterable, Mapping):
				self._init_from_mapping(iterable)
			else:
				self._init_from_iterable(iterable)

	@classmethod
	def from_mapping(cls, mapping: Mapping[Hashable, Any]) -> 'RangeMap':
		"""Create a RangeMap from a mapping of interval starts to values."""
		obj = cls()
		obj._init_from_mapping(mapping)
		return obj

	def _init_from_mapping(self, mapping: Mapping[Hashable, Any]):
		for key, value in sorted(mapping.items()):
			self.set(value, key)

	@classmethod
	def from_iterable(
			cls,
			iterable: Iterable[Tuple[Hashable, Hashable, Any]],
			) -> 'RangeMap':
		"""Create a RangeMap from an iterable of tuples defining each range.

		Each element of the iterable is a tuple (start, stop, value).
		"""
		obj = cls()
		obj._init_from_iterable(iterable)
		return obj

	def _init_from_iterable(self, iterable: Iterable[Tuple[Hashable, Hashable, Any]]):
		for start, stop, value in iterable:
			self.set(value, start=start, stop=stop)

	def __str__(self) -> str:
		range_format = '({range.start}, {range.stop}): {range.value}'
		values = ', '.join([range_format.format(range=r) for r in self.ranges()])
		return 'RangeMap(%s)' % values

	def __repr__(self) -> str:
		range_format = '({range.start!r}, {range.stop!r}, {range.value!r})'
		values = ', '.join([range_format.format(range=r) for r in self.ranges()])
		return 'RangeMap([%s])' % values

	def ranges(self, start: Hashable = None, stop: Hashable = None) -> Generator[MappedRange, None, None]:
		"""Generate MappedRanges for all mapped ranges.

		Yields:
			MappedRange
		"""
		_check_start_stop(start, stop)
		if start is None:
			start_loc = 1
		else:
			start_loc = bisect_right(self._keys, start, lo=1)
		if stop is None:
			stop_loc = len(self._keys)
		else:
			stop_loc = bisect_left(self._keys, stop, lo=1)
		start_val = self._values[start_loc - 1]
		candidate_keys = [start] + self._keys[start_loc:stop_loc] + [stop]
		candidate_values = [start_val] + self._values[start_loc:stop_loc]
		for i, value in enumerate(candidate_values):
			if value is not NOT_SET:
				start_key = candidate_keys[i]
				stop_key = candidate_keys[i + 1]
				yield MappedRange(start_key, stop_key, value)

	def __contains__(self, key: Hashable) -> bool:
		try:
			self._getitem(key)
		except KeyError:
			return False
		else:
			return True

	def __iter__(self):
		for key, value in zip(self._keys, self._values):
			if value is not NOT_SET:
				yield key

	def __bool__(self):
		# any(val is not NOT_SET for val in self._values)
		if len(self._keys) > 1:
			return True
		else:
			return self._values[0] != NOT_SET

	__nonzero__ = __bool__

	def _getitem(self, key: Hashable) -> Any:
		"""Get the value for a key (not a slice)."""
		if key is None:
			loc = 0
		else:
			loc = bisect_right(self._keys, key, lo=1) - 1
		value = self._values[loc]
		if value is NOT_SET:
			raise KeyError(key)
		else:
			return value

	def get(self, key: Hashable, restval: Any = None) -> Any:
		"""Get the value of the range containing key, otherwise return restval."""
		try:
			return self._getitem(key)
		except KeyError:
			return restval

	def get_range(self, start: Hashable = None, stop: Hashable = None) -> 'RangeMap':
		"""Return a RangeMap for the range start to stop."""
		return self.from_iterable(self.ranges(start, stop))

	def set(self, value: Any, start: Hashable = None, stop: Hashable = None):
		"""Set the range from start to stop to value."""
		_check_start_stop(start, stop)
		# start_index, stop_index will denote the section we are replacing
		if start is None:
			start_index = 0
		else:
			start_index = bisect_left(self._keys, start, lo=1)
			if self._values[start_index - 1] == value:
				# We're setting a range where the left range has the same
				# value, so create one big range
				start_index -= 1
				start = self._keys[start_index]
		new_keys = [start]
		new_values = [value]
		if stop is None:
			stop_index = len(self._keys)
		else:
			stop_index = bisect_right(self._keys, stop, lo=1)
			stop_value = self._values[stop_index - 1]
			if value != stop_value:
				new_keys.append(stop)
				new_values.append(stop_value)
		self._keys[start_index:stop_index] = new_keys
		self._values[start_index:stop_index] = new_values

	def delete(self, start: Hashable = None, stop: Hashable = None):
		"""Delete the range from start to stop from self.

		Raises:
			KeyError: If part of the passed range isn't mapped.
		"""
		_check_start_stop(start, stop)
		if start is None:
			start_loc = 0
		else:
			start_loc = bisect_right(self._keys, start, lo=1) - 1
		if stop is None:
			stop_loc = len(self._keys)
		else:
			stop_loc = bisect_left(self._keys, stop, lo=1)
		for value in self._values[start_loc:stop_loc]:
			if value is NOT_SET:
				raise KeyError((start, stop))
		# this is inefficient, we've already found the sub ranges
		self.set(NOT_SET, start=start, stop=stop)

	def empty(self, start: Hashable = None, stop: Hashable = None):
		"""Empty the range from start to stop.

		Like delete, but no Error is raised if the entire range isn't mapped.
		"""
		self.set(NOT_SET, start=start, stop=stop)

	def clear(self):
		"""Remove all elements."""
		self._keys = [None]
		self._values = [NOT_SET]

	@property
	def start(self) -> Optional[Hashable]:
		"""Get the start key of the first range.

		None if RangeMap is empty or unbounded to the left.
		"""
		if self._values[0] is NOT_SET:
			try:
				return self._keys[1]
			except IndexError:
				# This is empty or everything is mapped to a single value
				return None
		else:
			# This is unbounded to the left
			return self._keys[0]

	@property
	def end(self) -> Optional[Hashable]:
		"""Get the stop key of the last range.

		None if RangeMap is empty or unbounded to the right.
		"""
		if self._values[-1] is NOT_SET:
			return self._keys[-1]
		else:
			# This is unbounded to the right
			return None

	def __eq__(self, other: Any) -> bool:
		if isinstance(other, RangeMap):
			return (
				self._keys == other._keys
				and self._values == other._values
				)
		else:
			return False

	@overload
	def __getitem__(self, key: slice) -> 'RangeMap': ...

	@overload
	def __getitem__(self, key: Hashable) -> Any: ...

	def __getitem__(self, key):
		try:
			_check_key_slice(key)
		except TypeError:
			return self._getitem(key)
		else:
			return self.get_range(key.start, key.stop)

	def __setitem__(self, key: slice, value: Any):
		_check_key_slice(key)
		self.set(value, key.start, key.stop)

	def __delitem__(self, key: slice):
		_check_key_slice(key)
		self.delete(key.start, key.stop)

	def __len__(self) -> int:
		count = 0
		for v in self._values:
			if v is not NOT_SET:
				count += 1
		return count

	def keys(self) -> RangeMapKeysView:
		"""Return a view of the keys."""
		return RangeMapKeysView(self)

	def values(self) -> RangeMapValuesView:
		"""Return a view of the values."""
		return RangeMapValuesView(self)

	def items(self) -> RangeMapItemsView:
		"""Return a view of the item pairs."""
		return RangeMapItemsView(self)
