
import random as random_

from collections import (
	Sequence,
	Set,
	MutableSequence,
	MutableSet,
	Hashable,
	)


class _basesetlist(Sequence, Set):
	""" A setlist is an ordered Collection of unique elements.
	_basesetlist is the superclass of setlist and frozensetlist.  It is immutable
	and unhashable.
	"""

	def __init__(self, iterable=None):
		self._list = list()
		self._dict = dict()
		if iterable is not None:
			for value in iterable:
				if value not in self:
					index = len(self)
					self._list.insert(index, value)
					self._dict[value] = index

	def __str__(self):
		return self._list.__repr__()

	def __repr__(self):
		if len(self) == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			format = '{class_name}({tuple!r})'
			return format.format(class_name=self.__class__.__name__, tuple=tuple(self))

	## Convenience methods
	def _fix_neg_index(self, index):
		if index < 0:
			index += len(self)
		if index < 0:
			index = 0
		return index

	def _fix_end_index(self, index):
		if index is None:
			return len(self)
		else:
			return self._fix_neg_index(index)

	## Implement Container
	def __contains__(self, elem):
		return elem in self._dict

	## Iterable we get by inheriting from Sequence

	## Implement Sized
	def __len__(self):
		return len(self._list)

	## Implement Sequence
	def __getitem__(self, index):
		return self._list[index]

	def count(self, sub, start=0, end=-1):
		"""
		This runs in O(len(sub))
		"""
		try:
			self.index(sub, start, end)
			return 1
		except ValueError:
			return 0

	def index(self, sub, start=0, end=None):
		"""
		This runs in O(1)
		"""
		# TODO add more tests with start and end
		try:
			index = self._dict[sub]
		except KeyError:
			raise ValueError
		else:
			start = self._fix_neg_index(start)
			end = self._fix_end_index(end)
			if start <= index and index < end:
				return index
			else:
				raise ValueError

	## Nothing needs to be done to implement Set

	## Comparison

	def __le__(self, other):
		return NotImplemented

	def __lt__(self, other):
		return self <= other

	def __gt__(self, other):
		return other < self

	def __ge__(self, other):
		return other <= self

	def __eq__(self, other):
		if not isinstance(other, _basesetlist):
			return False
		if not len(self) == len(other):
			return False
		for i in range(len(self)):
			if self[i] != other[i]:
				return False
		return True

	def __ne__(self, other):
		return not (self == other)

	## New methods

	def sub_index(self, sub, start=0, end=None):
		"""
		Find the index of a subsequence

		This runs in O(len(sub))
		Raises ValueError if the subsequence doesn't exist.
		Raises TypeError if sub isn't a Sequence.
		"""
		start_index = self.index(sub[0], start, end)
		end = self._fix_end_index(end)
		if start_index + len(sub) > end:
			raise ValueError
		for i in range(1, len(sub)):
			try:
				if sub[i] != self[start_index+i]:
					raise ValueError
			except IndexError:
				raise ValueError
		return start_index


class setlist(_basesetlist, MutableSequence, MutableSet):
	""" A mutable (unhashable) setlist that inherits from _basesetlist.
	"""

	## Implement MutableCollection
	def __setitem__(self, index, value):
		index = self._fix_neg_index(index)
		if value in self:
			return
		old_value = self._list[index]
		del self._dict[old_value]
		self._list[index] = value
		self._dict[value] = index

	def __delitem__(self, index):
		index = self._fix_neg_index(index)
		del self._dict[self._list[index]]
		for elem in self._list[index+1:]:
			self._dict[elem] -= 1
		del self._list[index]

	def pop(self, index=-1):
		index = self._fix_neg_index(index)
		value = self[index]
		del self[index]
		return value

	## Implement MutableSequence
	def insert(self, index, value):
		if value in self:
			return
		index = self._fix_neg_index(index)
		self._dict[value] = index
		for elem in self._list[index:]:
			self._dict[elem] += 1
		self._list.insert(index, value)

	def append(self, value):
		self.insert(len(self), value)

	def extend(self, values):
		for value in values:
			self.append(value)

	def __iadd__(self, values):
		""" This will quietly not add values that are already present. """
		self.extend(values)
		return self

	def remove(self, value):
		if value not in self:
			raise ValueError
		del self[self._dict[value]]

	def remove_all(self, elems_to_delete):
		""" Remove all the elements from iterable.
		This is much faster than removing them one by one.
		This runs in O(len(self) + len(elems_to_delete))
		"""
		marked_to_delete = object()
		for elem in elems_to_delete:
			if elem in self:
				self._list[self._dict[elem]] = marked_to_delete
				del self._dict[elem]
		deleted_count = 0
		for i, elem in enumerate(self):
			if elem is marked_to_delete:
				deleted_count += 1
			else:
				new_index = i - deleted_count
				self._list[new_index] = elem
				self._dict[elem] = new_index
		## Now remove deleted_count items from the end of the list
		self._list = self._list[:-deleted_count]

	## Implement MutableSet
	def add(self, item):
		self.append(item)

	def discard(self, value):
		try:
			self.remove(value)
		except ValueError:
			pass

	def clear(self):
		self._dict = dict()
		self._list = list()

	## New methods
	def shuffle(self, random=None):
		random_.shuffle(self._list, random=random)
		for i, elem in enumerate(self._list):
			self._dict[elem] = i


class frozensetlist(_basesetlist, Hashable):
	""" An immutable (hashable) setlist that inherits from _basesetlist. """

	def __hash__(self):
		return self._list.__hash__() ^ self._dict.__hash__()
