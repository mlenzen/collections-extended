"""IndexedDict class definition.

.. versionadded:: 1.0.3
"""
from collections.abc import MutableMapping
from typing import Any, Dict, Generic, Hashable, Iterable, List, Mapping, Tuple, TypeVar, Union, Optional

from ._util import deprecation_warning
from .sentinel import NOT_SET, Sentinel

__all__ = ('IndexedDict', )

# TODO these should be ValueErrors
KEY_AND_INDEX_ERROR = TypeError(
	"Specifying both `key` and `index` is not allowed")
KEY_EQ_INDEX_ERROR = TypeError(
	"Exactly one of `key` and `index` must be specified")

K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


class IndexedDict(Generic[K, V], MutableMapping):
	"""A Mapping that preserves insertion order and allows access by item index.

	The API is an extension of OrderedDict.
	"""

	def __init__(
			self,
			iterable: Union[
				Mapping[K, V],
				Iterable[Tuple[K, V]],
				] = None,
			**kwargs: V,
			):
		"""Create an IndexedDict and initialize it like a dict."""
		self._dict: Dict[K, Tuple[int, V]] = {}  # key -> (index, value)
		self._list: List[Tuple[K, V]] = []  # index -> (key, value)
		self.update(iterable or [], **kwargs)

	def clear(self):
		"""Remove all items."""
		self._dict = {}
		self._list = []

	def get(
			self,
			key: K = NOT_SET,
			index: int = NOT_SET,
			default: V = NOT_SET,
			d: V = NOT_SET,
			) -> V:
		"""Return value with given `key` or `index`.

		If no value is found, return `default` (`None` by default).

		.. deprecated :: 1.0.3

		The `d` parameter has been renamed `default`. `d` will be removed in
		some future version.

		Args:
			key: The key of the value to get
			index: The index of the value to get
			default: The value to return if `key` is not found or `index` is
				out of bounds. If it is NOT_SET, None is returned.
			d: DEPRECATED: Old parameter name for `default`

		"""
		if d is not NOT_SET:
			if default is not NOT_SET:
				raise ValueError('Specified default and d')
			deprecation_warning(
				"IndexedDict.pop parameter 'd' has been renamed to 'default'"
				)
			default = d
		if default is NOT_SET:
			default = None

		if index is NOT_SET and key is not NOT_SET:
			try:
				index, value = self._dict[key]
			except KeyError:
				return default
			else:
				return value
		elif index is not NOT_SET and key is NOT_SET:
			try:
				key, value = self._list[index]
			except IndexError:
				return default
			else:
				return value
		else:
			raise KEY_EQ_INDEX_ERROR

	def pop(
			self,
			key: K = NOT_SET,
			index: int = NOT_SET,
			default: V = NOT_SET,
			d: V = NOT_SET,
			) -> V:
		"""Remove and return value.

		Optionally, specify the `key` or `index` of the value to pop.
		If `key` is specified and is not found a `KeyError` is raised unless
		`default` is specified. Likewise, if `index` is specified that is out of
		bounds, an `IndexError` is raised unless `default` is specified.

		Both `index` and `key` cannot be specified. If neither is specified,
		then the last value is popped.

		This is generally O(N) unless removing last item, then O(1).

		.. deprecated :: 1.0.3

		The `d` parameter has been renamed `default`. `d` will be removed in
		some future version.

		Args:
			key: The key of the value to pop
			index: The index of the value to pop
			default: The value to return if the key is not found or the index is
				out of bounds
			d: DEPRECATED: Old parameter name for `default`

		"""
		if d is not NOT_SET:
			if default is not NOT_SET:
				raise ValueError('Specified default and d')
			deprecation_warning(
				"IndexedDict.pop parameter 'd' has been renamed to 'default'"
				)
			default = d

		has_default = default is not NOT_SET
		if index is NOT_SET and key is not NOT_SET:
			index, value = self._pop_key(key, has_default)
		elif key is NOT_SET:
			key, index, value = self._pop_index(index, has_default)
		else:
			raise KEY_AND_INDEX_ERROR

		if index is None:
			return default
		else:
			self._fix_indices_after_delete(index)
			return value

	def _pop_key(
			self,
			key: K,
			has_default: bool,
			) -> Union[Tuple[int, V], Tuple[None, None]]:
		"""Remove an element by key."""
		try:
			index, value = self._dict.pop(key)
		except KeyError:
			if has_default:
				return None, None
			else:
				raise
		key2, value2 = self._list.pop(index)
		assert key is key2
		assert value is value2

		return index, value

	def _pop_index(
			self,
			index: int,
			has_default: bool,
			) -> Union[Tuple[None, None, None], Tuple[K, int, V]]:
		"""Remove an element by index, or last element."""
		try:
			if index is NOT_SET:
				index = len(self._list) - 1
				key, value = self._list.pop()
			else:
				key, value = self._list.pop(index)
				if index < 0:
					index += len(self._list) + 1
		except IndexError:
			if has_default:
				return None, None, None
			else:
				raise
		index2, value2 = self._dict.pop(key)
		assert index == index2
		assert value is value2

		return key, index, value

	def fast_pop(
			self,
			key: K = NOT_SET,
			index: int = NOT_SET,
			) -> Tuple[V, int, K, V]:
		"""Pop a specific item quickly by swapping it to the end.

		Remove value with given key or index (last item by default) fast
		by swapping it to the last place first.

		Changes order of the remaining items (item that used to be last goes to
		the popped location).
		Returns tuple of (popped_value, new_moved_index, moved_key, moved_value).
		If key is not found raises KeyError or IndexError.

		Runs in O(1).
		"""
		if index is NOT_SET and key is not NOT_SET:
			index, popped_value = self._dict.pop(key)
		elif key is NOT_SET:
			if index is NOT_SET:
				index = len(self._list) - 1
				key, popped_value2 = self._list[-1]
			else:
				key, popped_value2 = self._list[index]
				if index < 0:
					index += len(self._list)
			index2, popped_value = self._dict.pop(key)
			assert index == index2
		else:
			raise KEY_AND_INDEX_ERROR

		if key == self._list[-1][0]:
			# The item we're removing happens to be the last in the list,
			# no swapping needed
			_, popped_value2 = self._list.pop()
			assert popped_value is popped_value2
			return popped_value, len(self._list), key, popped_value
		else:
			# Swap the last item onto the deleted spot and
			# pop the last item from the list
			self._list[index] = self._list[-1]
			moved_key, moved_value = self._list.pop()
			self._dict[moved_key] = (index, moved_value)
			return popped_value, index, moved_key, moved_value

	def popitem(
			self,
			last: bool = NOT_SET,
			*,
			key: Union[K, Sentinel] = NOT_SET,
			index: Union[int, None, Sentinel] = NOT_SET,
			) -> Tuple[K, V]:
		"""Remove and return a (key, value) tuple.

		By default, the last item is popped.
		Optionally, specify the `key` or `index` of the value to pop.
		The `last` parameter is included to match the OrderedDict API. If `last`
		is passed then the first or last item is returned based on its
		truthiness.

		At most one of `index`, `last` and `key` can be specified.

		This is generally O(N) unless removing last item, then O(1).

		Args:
			key: The key of the value to pop
			index: The index of the value to pop
			last: Whether or not to pip the last item

		Raises:
			KeyError: If the dictionary is empty or a key is specified that is
				not present
			IndexError: If `index` is specified and is out of bounds
			ValueError: If more than one of `last`, `index` and `key` are
				specified

		"""
		if not self:
			raise KeyError('IndexedDict is empty')
		if sum(x is not NOT_SET for x in (last, key, index)) > 1:
			raise ValueError(
				"Cannot specify more than one of key, index and last"
				)
		if key is not NOT_SET:
			index, value = self._pop_key(key=key, has_default=False)
		else:
			if last is not NOT_SET:
				index = -1 if last else 0
			if index is NOT_SET:
				index = -1
			key, index, value = self._pop_index(index, has_default=False)
		self._fix_indices_after_delete(starting_index=index)
		return key, value

	def move_to_end(
			self,
			key: K = NOT_SET,
			index: int = NOT_SET,
			last: bool = True,
			):
		"""Move an existing element to the end (or beginning if last==False).

		Runs in O(N).
		"""
		if index is NOT_SET and key is not NOT_SET:
			index, value = self._dict[key]
		elif index is not NOT_SET and key is NOT_SET:
			key, value = self._list[index]

			# Normalize index
			if index < 0:
				index += len(self._list)
		else:
			raise KEY_EQ_INDEX_ERROR

		if last:
			index_range = range(len(self._list) - 1, index - 1, -1)
			self._dict[key] = (len(self._list) - 1, value)
		else:
			index_range = range(index + 1)
			self._dict[key] = (0, value)

		previous = (key, value)
		for i in index_range:
			self._dict[previous[0]] = i, previous[1]
			previous, self._list[i] = self._list[i], previous

	def copy(self) -> 'IndexedDict[K, V]':
		"""Return a shallow copy."""
		ret: IndexedDict[K, V] = IndexedDict()
		ret._dict = self._dict.copy()
		ret._list = list(self._list)
		return ret

	def index(self, key: K) -> int:
		"""Return index of a record with given key.

		Runs in O(1).
		"""
		return self._dict[key][0]

	def key(self, index: int) -> K:
		"""Return key of a record at given index.

		Runs in O(1).
		"""
		return self._list[index][0]

	def __len__(self):
		"""Return number of elements stored."""
		return len(self._list)

	def __repr__(self):
		return "{class_name}({data})".format(
			class_name=self.__class__.__name__,
			data=repr(self._list),
			)

	def __str__(self):
		# When Python 3.5 support is dropped, we can rely on dict order and this
		# can be simplified to:
		# return "{class_name}({data})".format(
		# 	class_name=self.__class__.__name__,
		# 	data=repr(dict(self)),
		# 	)
		data = ', '.join(
			'{k!r}: {v!r}'.format(k=k, v=v)
			for k, v in self.items()
			)
		return "{class_name}({{{data}}})".format(
			class_name=self.__class__.__name__,
			data=data,
			)

	def __getitem__(self, key):
		"""Return value corresponding to given key.

		Raises KeyError when the key is not present in the mapping.

		Runs in O(1).
		"""
		return self._dict[key][1]

	def __setitem__(self, key, value):
		"""Set item with given key to given value.

		If the key is already present in the mapping its order is unchanged,
		if it is not then it's added to the last place.

		Runs in O(1).
		"""
		if key in self._dict:
			index, old_value1 = self._dict[key]
			self._list[index] = key, value
		else:
			index = len(self._list)
			self._list.append((key, value))
		self._dict[key] = index, value

	def __delitem__(self, key):
		"""Remove item with given key from the mapping.

		Runs in O(n), unless removing last item, then in O(1).
		"""
		index, value = self._dict.pop(key)
		key2, value2 = self._list.pop(index)
		assert key == key2
		assert value is value2

		self._fix_indices_after_delete(index)

	def __contains__(self, key):
		"""Check if a key is present in the mapping.

		Runs in O(1).
		"""
		return key in self._dict

	def __iter__(self):
		"""Return iterator over the keys of the mapping in order."""
		return (item[0] for item in self._list)

	def _fix_indices_after_delete(self, starting_index=0):
		for i, (k, v) in enumerate(self._list[starting_index:], starting_index):
			self._dict[k] = (i, v)
