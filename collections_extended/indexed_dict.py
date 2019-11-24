"""IndexedDict class definition.

.. versionadded:: 1.1
"""
import collections

from ._util import deprecation_warning, fix_seq_index
from .sentinel import NOT_SET
from typing import (
	Any,
	Dict,
	Hashable,
	Iterable,
	List,
	Mapping,
	MutableMapping,
	NamedTuple,
	Optional,
	Tuple,
	Union,
	)


__all__ = ('IndexedDict', )

KEY_AND_INDEX_ERROR = TypeError(
	"Specifying both `key` and `index` is not allowed"
	)
KEY_EQ_INDEX_ERROR = TypeError(
	"Exactly one of `key` and `index` must be specified"
	)
KeyType = Union[Hashable, None]


class DictVal(NamedTuple):
	index: int
	value: Any


class ListVal(NamedTuple):
	key: KeyType
	val: Any


class IndexedDict(MutableMapping):
	"""A Mapping that preserves insertion order and allows access by item index.

	The API is an extension of OrderedDict.

	.. automethod:: __init__
	"""

	def __init__(
			self,
			iterable: Union[
				Mapping[Hashable, Any],
				Iterable[Tuple[Hashable, Any]],
				None,
				] = None,
			**kwargs: Hashable,
			):
		"""Create an IndexedDict and initialize it like a dict."""
		self._dict: Dict[KeyType, DictVal] = {}  # key -> (index, value)
		self._list: List[ListVal] = []  # index -> (key, value)
		self.update(iterable or [], **kwargs)

	def clear(self):
		"""Remove all items."""
		self._dict.clear()
		self._list.clear()

	def get(
			self,
			key: KeyType = NOT_SET,
			*,
			index: int = NOT_SET,
			default: Any = NOT_SET,
			d: Any = NOT_SET,
			) -> Any:
		"""Return value with given `key` or `index`.

		If no value is found, return `default` (`None` by default).

		.. deprecated :: 1.1
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
				dict_val = self._dict[key]
			except KeyError:
				return default
			else:
				return dict_val.value
		elif index is not NOT_SET and key is NOT_SET:
			try:
				list_val = self._list[index]
			except IndexError:
				return default
			else:
				return list_val.val
		else:
			raise KEY_EQ_INDEX_ERROR

	def pop(
			self,
			key: KeyType = NOT_SET,
			*,
			index: int = None,
			default: Any = NOT_SET,
			d: Any = NOT_SET,
			) -> Any:
		"""Remove and return value.

		Optionally, specify the `key` or `index` of the value to pop.
		If `key` is specified and is not found a `KeyError` is raised unless
		`default` is specified. Likewise, if `index` is specified that is out of
		bounds, an `IndexError` is raised unless `default` is specified.

		Both `index` and `key` cannot be specified. If neither is specified,
		then the last value is popped.

		This is generally O(N) unless removing last item, then O(1).

		.. deprecated :: 1.1
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

		try:
			key, index, value = self._pop(key, index)
		except (KeyError, IndexError):
			if default is NOT_SET:
				raise
			else:
				return default
		self._fix_indices_after_delete(index)
		return value

	def _pop(
			self,
			key: KeyType,
			index: Optional[int],
			) -> Tuple[KeyType, int, Any]:
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
			key: KeyType = NOT_SET,
			*,
			index: int = None,
			) -> Tuple[Any, int, KeyType, Any]:
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
		else:
			raise KEY_AND_INDEX_ERROR

		# TODO can we remove this optimization, does it actually help?
		if key == self._list[-1].key:
			# The item we're removing happens to be the last in the list,
			# no swapping needed
			self._list.pop()
			return popped_value, len(self._list), key, popped_value
		else:
			# Swap the last item onto the deleted spot and
			# pop the last item from the list
			self._list[index] = self._list[-1]
			moved_key, moved_value = self._list.pop()
			self._dict[moved_key] = DictVal(index, moved_value)
			return popped_value, index, moved_key, moved_value

	def popitem(self, last: bool = True) -> Tuple[KeyType, Any]:
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
			key: KeyType = NOT_SET,
			index: int = None,
			last: bool = True,
			):
		"""Move an existing element to the end (or beginning if last==False).

		Runs in O(N).
		"""
		if index is None and key is not NOT_SET:
			index, value = self._dict[key]
		elif index is not None and key is NOT_SET:
			index = fix_seq_index(self, index)
			key, value = self._list[index]
		else:
			raise KEY_EQ_INDEX_ERROR

		if last:
			index_range = range(len(self._list) - 1, index - 1, -1)
			self._dict[key] = DictVal(len(self._list) - 1, value)
		else:
			index_range = range(index + 1)
			self._dict[key] = DictVal(0, value)

		previous = ListVal(key, value)
		for i in index_range:
			self._dict[previous[0]] = DictVal(i, previous[1])
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
		return self._dict[key].index

	def key(self, index: int) -> KeyType:
		"""Return key of a record at given index.

		Runs in O(1).
		"""
		return self._list[index].key

	def __len__(self):
		"""Return number of elements stored."""
		return len(self._list)

	def __repr__(self):
		return "{class_name}({data})".format(
			class_name=self.__class__.__name__,
			data=repr([tuple(val) for val in self._list]),
			)

	def __str__(self):
		return "{class_name}({data})".format(
			class_name=self.__class__.__name__,
			data=repr({k: self[k] for k in self}),
			)

	def __getitem__(self, key: KeyType):
		"""Return value corresponding to given key.

		Raises KeyError when the key is not present in the mapping.

		Runs in O(1).
		"""
		return self._dict[key].value

	def __setitem__(self, key: KeyType, value: Any):
		"""Set item with given key to given value.

		If the key is already present in the mapping its order is unchanged,
		if it is not then it's added to the last place.

		Runs in O(1).
		"""
		if key in self._dict:
			index = self._dict[key].index
			self._list[index] = ListVal(key, value)
		else:
			index = len(self._list)
			self._list.append(ListVal(key, value))
		self._dict[key] = DictVal(index, value)

	def __delitem__(self, key: KeyType):
		"""Remove item with given key from the mapping.

		Runs in O(n), unless removing last item, then in O(1).
		"""
		index = self._dict.pop(key).index
		self._list.pop(index)
		self._fix_indices_after_delete(index)

	def __contains__(self, key):
		"""Check if a key is present in the mapping.

		Runs in O(1).
		"""
		return key in self._dict

	def __iter__(self):
		"""Return iterator over the keys of the mapping in order."""
		return (item.key for item in self._list)

	def _fix_indices_after_delete(self, starting_index: int = 0):
		for i, (k, v) in enumerate(self._list[starting_index:], starting_index):
			self._dict[k] = DictVal(i, v)
