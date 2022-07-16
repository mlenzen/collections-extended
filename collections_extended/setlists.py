"""Setlist class definitions."""
import random as random_
from typing import (
	overload,
	Hashable,
	MutableSequence,
	MutableSet,
	Sequence,
	Any,
	Callable,
	Dict,
	Generic,
	Iterable,
	List,
	Optional,
	Set,
	TypeVar,
	Union,
	)

from . import _util

__all__ = ('SetList', 'setlist', 'frozensetlist')

T = TypeVar('T', bound=Hashable)


class SetList(Sequence, Set, Generic[T]):
	"""A setlist is an ordered `Collection` of unique elements.

	`SetList` is the superclass of `setlist` and `frozensetlist`. It is
	immutable and unhashable.
	"""

	def __init__(
			self,
			iterable: Iterable[T] = None,
			raise_on_duplicate: bool = False,
			):
		"""Create a setlist, initializing from iterable if present.

		Args:
			iterable: Values to initialize the setlist with.
			raise_on_duplicate: Raise a ValueError if any duplicate values
				are present.
		"""
		self._list: List[T] = list()
		self._dict: Dict[T, int] = dict()
		if iterable:
			if isinstance(iterable, SetList):
				self._list = iterable._list.copy()
				self._dict = iterable._dict.copy()
			elif raise_on_duplicate:
				self._extend(iterable)
			else:
				self._update(iterable)

	def __repr__(self):
		if len(self) == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			repr_format = '{class_name}({values!r})'
			return repr_format.format(
				class_name=self.__class__.__name__,
				values=tuple(self),
				)

	# Convenience methods

	def _fix_neg_index(self, index: int) -> int:
		if index < 0:
			index += len(self)
		if index < 0:
			raise IndexError('index is out of range')
		return index

	def _fix_end_index(self, index: Optional[int]) -> int:
		if index is None:
			return len(self)
		else:
			return self._fix_neg_index(index)

	def _append(self, value: T):
		# Checking value in self will check that value is Hashable
		if value in self:
			raise ValueError('Value "%s" already present' % str(value))
		else:
			self._dict[value] = len(self)
			self._list.append(value)

	def _extend(self, values: Iterable[T]):
		new_values: Set[T] = set()
		for value in values:
			if value in new_values:
				raise ValueError('New values contain duplicates')
			elif value in self:
				raise ValueError('New values contain elements already present in self')
			else:
				new_values.add(value)
		for value in values:
			self._dict[value] = len(self)
			self._list.append(value)

	def _add(self, item: T):
		if item not in self:
			self._dict[item] = len(self)
			self._list.append(item)

	def _update(self, values: Iterable[T]):
		for value in values:
			if value not in self:
				self._dict[value] = len(self)
				self._list.append(value)

	@classmethod
	def _from_iterable(cls, it: Iterable[T], **kwargs):
		return cls(it, **kwargs)

	# Implement Container
	def __contains__(self, value):
		return value in self._dict

	# Iterable we get by inheriting from Sequence

	# Implement Sized
	def __len__(self) -> int:
		return len(self._list)

	# Implement Sequence
	def __getitem__(self, index):
		if isinstance(index, slice):
			return self._from_iterable(self._list[index])
		return self._list[index]

	def count(self, value: T) -> int:
		"""Return the number of occurrences of value in self.

		This runs in O(1)

		Args:
			value: The value to count
		Returns:
			1 if the value is in the setlist, otherwise 0
		"""
		if value in self:
			return 1
		else:
			return 0

	def index(self, value: T, start: int = 0, end: int = None) -> int:
		"""Return the index of value between start and end.

		By default, the entire setlist is searched.

		This runs in O(1)

		Args:
			value: The value to find the index of
			start: The index to start searching at (defaults to 0)
			end: The index to stop searching at (defaults to the end of the list)
		Returns:
			The index of the value
		Raises:
			ValueError: If the value is not in the list or outside of start - end
			IndexError: If start or end are out of range
		"""
		try:
			index = self._dict[value]
		except KeyError:
			raise ValueError
		else:
			start = self._fix_neg_index(start)
			end = self._fix_end_index(end)
			if start <= index < end:
				return index
			else:
				raise ValueError

	@classmethod
	def _check_type(cls, other: Any, operand_name: str):
		"""Check that other is an Iterable."""
		if not isinstance(other, SetList):
			message = (
				"unsupported operand type(s) for {operand_name}: "
				"'{self_type}' and '{other_type}'").format(
					operand_name=operand_name,
					self_type=cls,
					other_type=type(other),
					)
			raise TypeError(message)

	def __add__(self, other: Iterable[T]) -> 'SetList[T]':
		self._check_type(other, '+')
		out = self.copy()
		out._extend(other)
		return out

	# Implement Set

	def issubset(self, other):
		return self <= other

	def issuperset(self, other):
		return self >= other

	def union(self, other):
		"""Return the union of sets as a new set.

		(i.e. all elements that are in either set.)
		"""
		out = self.copy()
		out._update(other)
		return out

	def intersection(self, other):
		"""Return the intersection of two sets as a new set.

		(i.e. all elements that are in both sets.)
		"""
		# TODO why does using a set for other fail
		# other = set(other)
		other = setlist(other)
		return self._from_iterable(item for item in self if item in other)

	def difference(self, other):
		"""Return the difference of two or more sets as a new set.

		(i.e. all elements that are in this set but not the others.)
		"""
		# TODO why does using a set for other fail
		# other = set(other)
		other = setlist(other)
		return self._from_iterable(item for item in self if item not in other)

	def symmetric_difference(self, other):
		"""Return the symmetric difference (disjuntive union) of two sets.

		(i.e. all elements that are in one set but not both.)
		"""
		return self.union(other) - self.intersection(other)

	def __sub__(self, other):
		self._check_type(other, '-')
		return self.difference(other)

	def __and__(self, other):
		self._check_type(other, '&')
		return self.intersection(other)

	def __or__(self, other):
		self._check_type(other, '|')
		return self.union(other)

	def __xor__(self, other):
		self._check_type(other, '^')
		return self.symmetric_difference(other)

	# Comparison

	def __eq__(self, other: Any) -> bool:
		if not isinstance(other, SetList):
			return False
		if not len(self) == len(other):
			return False
		for self_elem, other_elem in zip(self, other):
			if self_elem != other_elem:
				return False
		return True

	def __ne__(self, other: Any) -> bool:
		return not (self == other)

	# New methods

	def sub_index(
			self,
			sub: Sequence[T],
			start: int = 0,
			end: int = None,
			) -> int:
		"""Return the index of a subsequence.

		This runs in O(len(sub))

		Args:
			sub: An sub-Sequence to search for
			start: The index at which to start the search
			end: The index at which to end the search
		Returns:
			The index of the first element of sub
		Raises:
			ValueError: If sub isn't a subsequence
			TypeError: If sub isn't iterable
			IndexError: If start or end are out of range
		"""
		start_index = self.index(sub[0], start, end)
		end = self._fix_end_index(end)
		if start_index + len(sub) > end:
			raise ValueError
		for i in range(1, len(sub)):
			if sub[i] != self[start_index + i]:
				raise ValueError
		return start_index

	def copy(self) -> 'SetList':
		"""Return a shallow copy of the setlist."""
		return self.__class__(self)


class setlist(SetList, MutableSequence, MutableSet):
	"""A mutable (unhashable) setlist.

	.. automethod:: __init__
	"""

	def __str__(self) -> str:
		return '{[%s}]' % ', '.join(repr(v) for v in self)

	# Helper methods
	def _delete_all(self, elems_to_delete: Iterable[T], raise_errors: bool):
		indices_to_delete: Set[int] = set()
		for elem in elems_to_delete:
			try:
				elem_index = self._dict[elem]
			except KeyError:
				if raise_errors:
					raise ValueError('Passed values contain elements not in self')
			else:
				if elem_index in indices_to_delete:
					if raise_errors:
						raise ValueError('Passed vales contain duplicates')
				indices_to_delete.add(elem_index)
		self._delete_values_by_index(indices_to_delete)

	def _delete_values_by_index(self, indices_to_delete: Set[int]):
		deleted_count = 0
		for i, elem in enumerate(self._list):
			if i in indices_to_delete:
				deleted_count += 1
				del self._dict[elem]
			else:
				new_index = i - deleted_count
				self._list[new_index] = elem
				self._dict[elem] = new_index
		# Now remove deleted_count items from the end of the list
		if deleted_count:
			self._list = self._list[:-deleted_count]

	# Set/Sequence agnostic
	def pop(self, index: int = -1) -> T:
		"""Remove and return the item at index."""
		value = self._list.pop(index)
		del self._dict[value]
		return value

	def clear(self):
		"""Remove all elements from self."""
		self._dict = dict()
		self._list = list()

	# Implement MutableSequence
	@overload
	def __setitem__(self, index: int, value: T): ...
	@overload
	def __setitem__(self, index: slice, value: Iterable[T]): ...
	def __setitem__(self, index, value):
		if isinstance(index, slice):
			old_values = self[index]
			for v in value:
				if v in self and v not in old_values:
					raise ValueError
			self._list[index] = value
			self._dict = {}
			for i, v in enumerate(self._list):
				self._dict[v] = i
		else:
			index = self._fix_neg_index(index)
			old_value = self._list[index]
			if value in self:
				if value == old_value:
					return
				else:
					raise ValueError
			del self._dict[old_value]
			self._list[index] = value
			self._dict[value] = index

	def __delitem__(self, index: Union[int, slice]):
		if isinstance(index, slice):
			indices_to_delete = set(self.index(e) for e in self._list[index])
			self._delete_values_by_index(indices_to_delete)
		else:
			index = self._fix_neg_index(index)
			value = self._list[index]
			del self._dict[value]
			for elem in self._list[index + 1:]:
				self._dict[elem] -= 1
			del self._list[index]

	def insert(self, index: int, value: T):
		"""Insert value at index.

		Args:
			index: Index to insert value at
			value: Value to insert
		Raises:
			ValueError: If value already in self
			IndexError: If start or end are out of range
		"""
		if value in self:
			raise ValueError
		index = self._fix_neg_index(index)
		self._dict[value] = index
		for elem in self._list[index:]:
			self._dict[elem] += 1
		self._list.insert(index, value)

	def append(self, value: T):
		"""Append value to the end.

		Args:
			value: Value to append
		Raises:
			ValueError: If value alread in self
			TypeError: If value isn't hashable
		"""
		self._append(value)

	def extend(self, values: Iterable[T]):
		"""Append all values to the end.

		If any of the values are present, ValueError will
		be raised and none of the values will be appended.

		Args:
			values: Values to append
		Raises:
			ValueError: If any values are already present or there are duplicates
				in the passed values.
			TypeError: If any of the values aren't hashable.
		"""
		self._extend(values)

	def __iadd__(self, values: Iterable[T]):
		"""Add all values to the end of self.

		Args:
			values: Values to append
		Raises:
			ValueError: If any values are already present
		"""
		self._check_type(values, '+=')
		self.extend(values)
		return self

	def remove(self, value: T):
		"""Remove value from self.

		Args:
			value: Element to remove from self
		Raises:
			ValueError: if element is already present
		"""
		try:
			index = self._dict[value]
		except KeyError:
			raise ValueError('Value "%s" is not present.')
		else:
			del self[index]

	def remove_all(self, elems_to_delete: Iterable[T]):
		"""Remove all elements from elems_to_delete, raises ValueErrors.

		See Also:
			discard_all
		Args:
			elems_to_delete: Elements to remove.
		Raises:
			ValueError: If the count of any element is greater in
				elems_to_delete than self.
			TypeError: If any of the values aren't hashable.
		"""
		self._delete_all(elems_to_delete, raise_errors=True)

	def reverse(self):
		"""Reverse the setlist in-place."""
		self._list.reverse()
		for index, item in enumerate(self._list):
			self._dict[item] = index

	# Implement MutableSet

	def add(self, item: T):
		"""Add an item.

		Note:
			This does not raise a ValueError for an already present value like
			append does. This is to match the behavior of set.add
		Args:
			item: Item to add
		Raises:
			TypeError: If item isn't hashable.
		"""
		self._add(item)

	def update(self, values):
		"""Add all values to the end.

		If any of the values are present, silently ignore
		them (as opposed to extend which raises an Error).

		See also:
			extend
		Args:
			values: Values to add
		Raises:
			TypeError: If any of the values are unhashable.
		"""
		self._update(values)

	def discard_all(self, elems_to_delete):
		"""Discard all the elements from elems_to_delete.

		This is much faster than removing them one by one.
		This runs in O(len(self) + len(elems_to_delete))

		See also:
			remove_all
		Args:
			elems_to_delete: Elements to discard.
		Raises:
			TypeError: If any of the values aren't hashable.
		"""
		self._delete_all(elems_to_delete, raise_errors=False)

	def discard(self, value: T):
		"""Discard an item.

		See also:
			remove
		Note:
			This does not raise a ValueError for a missing value like remove does.
			This matches the behavior of set.discard
		"""
		try:
			self.remove(value)
		except ValueError:
			pass

	def difference_update(self, other):
		"""Update self to include only the difference with other."""
		# TODO why does using a set for other fail
		# other = set(other)
		other = setlist(other)
		indices_to_delete = set()
		for i, elem in enumerate(self):
			if elem in other:
				indices_to_delete.add(i)
		if indices_to_delete:
			self._delete_values_by_index(indices_to_delete)

	def intersection_update(self, other):
		"""Update self to include only the intersection with other."""
		# TODO why does using a set for other fail
		# other = set(other)
		other = setlist(other)
		indices_to_delete = set()
		for i, elem in enumerate(self):
			if elem not in other:
				indices_to_delete.add(i)
		if indices_to_delete:
			self._delete_values_by_index(indices_to_delete)

	def symmetric_difference_update(self, other: Iterable[T]):
		"""Update self to include only the symmetric difference with other."""
		# TODO why does using a set for other fail
		# other = set(other)
		other = setlist(other)
		indices_to_delete = set()
		for i, item in enumerate(self):
			if item in other:
				indices_to_delete.add(i)
		for item in other:
			self.add(item)
		self._delete_values_by_index(indices_to_delete)

	def __isub__(self, other):
		self._check_type(other, '-=')
		self.difference_update(other)
		return self

	def __iand__(self, other):
		self._check_type(other, '&=')
		self.intersection_update(other)
		return self

	def __ior__(self, other):
		self._check_type(other, '|=')
		self.update(other)
		return self

	def __ixor__(self, other):
		self._check_type(other, '^=')
		self.symmetric_difference_update(other)
		return self

	# New methods
	def shuffle(self, random: Callable[[], float] = None):
		"""Shuffle all of the elements in self in place.

		Args:
			random: A function returning a random float in [0.0, 1.0). If none
				is passed, the default from `random.shuffle` will be used.
		"""
		random_.shuffle(self._list, random=random)
		for i, elem in enumerate(self._list):
			self._dict[elem] = i

	def sort(self, *, key: Callable[[T], Any] = None, reverse: bool = False):
		"""Sort this setlist in place."""
		self._list.sort(key=key, reverse=reverse)
		for index, value in enumerate(self._list):
			self._dict[value] = index

	def swap(self, i: int, j: int):
		"""Swap the values at indices i & j.

		.. versionadded:: 1.0.3
		"""
		i = self._fix_neg_index(i)
		j = self._fix_neg_index(j)
		self._list[i], self._list[j] = self._list[j], self._list[i]
		self._dict[self._list[i]] = i
		self._dict[self._list[j]] = j


class frozensetlist(SetList, Hashable):
	"""An immutable (hashable) setlist.

	.. automethod:: __init__
	"""

	def __hash__(self):
		if not hasattr(self, '_hash_value'):
			self._hash_value = _util.hash_iterable(self)
		return self._hash_value
