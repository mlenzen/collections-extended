"""IndexedDict class definition.

.. versionadded:: 1.1
"""
from typing import Iterable, MutableMapping, Union, Mapping, Hashable, Tuple, Dict, List, Any, Optional

from ._util import NOT_SET, fix_seq_index

KEY_AND_INDEX_ERROR = TypeError(
	"Specifying both `key` and `index` is not allowed"
	)
KEY_EQ_INDEX_ERROR = TypeError(
	"Exactly one of `key` and `index` must be specified"
	)


class IndexedDict(MutableMapping):
	"""A Mapping that preserves insertion order and allows access by item index.

	The API is an extension of OrderedDict.

	.. automethod:: __init__
	"""

	def __init__(
			self,
			iterable: Union[
				Mapping[Hashable, Hashable],
				Iterable[Tuple[Hashable, Hashable]],
				None,
				] = None,
			**kwargs: Hashable,
			):
		"""Create an IndexedDict and initialize it like a dict."""
		self._dict: Dict[Hashable, Tuple[int, Any]] = {}  # key -> (index, value)
		self._list: List[Tuple[Hashable, Any]] = []  # index -> (key, value)
		self.update(iterable or [], **kwargs)

	def clear(self):
		"""Remove all items."""
		self._dict.clear()
		self._list.clear()

	def get(
			self,
			key: Hashable = NOT_SET,
			*,
			index: int = NOT_SET,
			d: Any = None,
			) -> Any:
		"""Return value with given key or index.

		If no value is found, return d (None by default).
		"""
		if index is NOT_SET and key is not NOT_SET:
			try:
				index, value = self._dict[key]
			except KeyError:
				return d
			else:
				return value
		elif index is not NOT_SET and key is NOT_SET:
			try:
				key, value = self._list[index]
			except IndexError:
				return d
			else:
				return value
		else:
			raise KEY_EQ_INDEX_ERROR

	def pop(
			self,
			key: Hashable = NOT_SET,
			*,
			index: int = None,
			d: Any = NOT_SET,
			) -> Any:
		"""Remove and return value with given key or index (last item by default).

		If key is not found, returns d if given,
		otherwise raises KeyError or IndexError.

		This is generally O(N) unless removing last item, then O(1).
		"""
		try:
			key, index, value = self._pop(key, index)
		except (KeyError, IndexError):
			if d is NOT_SET:
				raise
			else:
				return d
		self._fix_indices_after_delete(index)
		return value

	def _pop(self, key: Hashable, index: int) -> Any:
		if index is None and key is not NOT_SET:
			index, value = self._dict.pop(key)
			self._list.pop(index)
		elif key is NOT_SET:
			index = fix_seq_index(self, index)
			key, value = self._list.pop(index)
			self._dict.pop(key)
		else:
			raise KEY_AND_INDEX_ERROR
		return key, index, value

	def fast_pop(
			self,
			key: Hashable = NOT_SET,
			*,
			index: int = None,
			) -> Tuple[Any, int, Hashable, Any]:
		"""Pop a specific item quickly by swapping it to the end.

		Remove value with given key or index (last item by default) fast
		by swapping it to the last place first.

		Changes order of the remaining items (item that used to be last goes to
		the popped location).
		Returns tuple of (popped_value, new_moved_index, moved_key, moved_value).
		If key is not found raises KeyError or IndexError.

		Runs in O(1).
		"""
		if index is None and key is not NOT_SET:
			index, popped_value = self._dict.pop(key)
		elif key is NOT_SET:
			if index is None:
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

		# TODO can we remove this optimization, does it actually help?
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

	def popitem(self, last: bool = True) -> Tuple[Hashable, Any]:
		"""Remove and return last (default) or first (last=False) pair (key, value).

		Raises KeyError if the dictionary is empty.

		Runs in O(1) for last item, O(N) for first one.
		"""
		index = None if last else 0
		try:
			key, index, value = self._pop(NOT_SET, index)
		except IndexError:
			# Do this for backwards compatibility
			raise KeyError
		self._fix_indices_after_delete(starting_index=index)
		return key, value

	def move_to_end(
			self,
			key: Hashable = NOT_SET,
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

	def copy(self):
		"""Return a shallow copy."""
		ret = IndexedDict()
		ret._dict = self._dict.copy()
		ret._list = self._list.copy()
		return ret

	def index(self, key: Hashable) -> int:
		"""Return index of a record with given key.

		Runs in O(1).
		"""
		return self._dict[key][0]

	def key(self, index: int) -> Hashable:
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

	def __getitem__(self, key: Union[Hashable, None]):
		"""Return value corresponding to given key.

		Raises KeyError when the key is not present in the mapping.

		Runs in O(1).
		"""
		return self._dict[key][1]

	def __setitem__(self, key: Union[Hashable, None], value: Any):
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

	def __delitem__(self, key: Union[Hashable, None]):
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

	def _fix_indices_after_delete(self, starting_index: int = 0):
		for i, (k, v) in enumerate(self._list[starting_index:], starting_index):
			self._dict[k] = (i, v)
