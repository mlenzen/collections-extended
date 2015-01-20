
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

	# Convenience methods
	def _fix_neg_index(self, index):
		if index < 0:
			index += len(self)
		if index < 0:
			raise IndexError
		return index

	def _fix_end_index(self, index):
		if index is None:
			return len(self)
		else:
			return self._fix_neg_index(index)

	@classmethod
	def _from_iterable(cls, it):
		return cls(it)

	# Implement Container
	def __contains__(self, elem):
		return elem in self._dict

	# Iterable we get by inheriting from Sequence

	# Implement Sized
	def __len__(self):
		return len(self._list)

	# Implement Sequence
	def __getitem__(self, index):
		if isinstance(index, slice):
			return self._from_iterable(self._list[index])
		return self._list[index]

	def count(self, sub, start=0, end=None):
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

	# Nothing needs to be done to implement Set

	# Comparison

	def __eq__(self, other):
		if not isinstance(other, _basesetlist):
			return False
		if not len(self) == len(other):
			return False
		for self_elem, other_elem in zip(self, other):
			if self_elem != other_elem:
				return False
		return True

	def __ne__(self, other):
		return not (self == other)

	# New methods

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
			if sub[i] != self[start_index + i]:
				raise ValueError
		return start_index

	def copy(self):
		return self.__class__(self)


class setlist(_basesetlist, MutableSequence, MutableSet):
	""" A mutable (unhashable) setlist that inherits from _basesetlist.
	"""

	# Implement MutableSequence
	def __setitem__(self, index, value):
		if isinstance(index, slice):
			old_values = self[index]
			for v in value:
				if v in self and v not in old_values:
					raise ValueError
			else:
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

	def __delitem__(self, index):
		if isinstance(index, slice):
			values_to_remove = self._list[index]
			self.remove_all(values_to_remove)
		else:
			index = self._fix_neg_index(index)
			value = self._list[index]
			self.remove(value)

	def insert(self, index, value):
		if value in self:
			raise ValueError
		index = self._fix_neg_index(index)
		self._dict[value] = index
		for elem in self._list[index:]:
			self._dict[elem] += 1
		self._list.insert(index, value)

	def append(self, value):
		if value in self:
			raise ValueError
		else:
			# Do this first in case value isn't Hashable
			self._dict[value] = len(self) + 1
			self._list.append(value)

	def extend(self, values):
		if not self.isdisjoint(values):
			raise ValueError
		for value in values:
			self.append(value)

	def __iadd__(self, values):
		""" This will quietly not add values that are already present. """
		self.extend(values)
		return self

	def remove(self, value):
		try:
			index = self._dict[value]
		except KeyError:
			raise ValueError
		else:
			del self._dict[value]
			for elem in self._list[index + 1:]:
				self._dict[elem] -= 1
			del self._list[index]

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
		# Now remove deleted_count items from the end of the list
		self._list = self._list[:-deleted_count]

	# Implement MutableSet
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

	# New methods
	def shuffle(self, random=None):
		random_.shuffle(self._list, random=random)
		for i, elem in enumerate(self._list):
			self._dict[elem] = i


class frozensetlist(_basesetlist, Hashable):
	""" An immutable (hashable) setlist that inherits from _basesetlist. """

	def __hash__(self):
		return Set._hash(self)
