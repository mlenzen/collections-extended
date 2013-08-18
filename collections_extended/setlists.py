from collections import Sequence, Set, Sized, Iterable, Container, MutableSequence, MutableSet, Hashable

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

	## Implement Container
	def __contains__(self, elem): 
		return elem in self._dict

	## Implement Iterable
	__iter__ = list.__iter__

	## Implement Sized
	def __len__(self):
		return len(self._list)

	## Implement Sequence
	def __getitem__(self, index):
		return self._list[index]

	def __reversed__(self):
		return self._from_iterable(self._list.__reversed__())

	def count(self, sub, start=0, end=-1):
		"""
		This runs in O(len(sub))

		>>> sl = setlist('abcdea')
		>>> sl.count('a')
		1
		>>> sl.count('f')
		0
		"""
		try:
			self.index(sub, start, end)
			return 1
		except ValueError:
			return 0

	def index(self, sub, start=0, end=None):
		"""
		This runs in O(1)

		>>> sl = setlist('abcdef')
		>>> sl.index('a')
		0
		>>> sl.index('f')
		5
		"""
		# TODO add more tests with start and end
		try:
			index = self._dict[sub]
		except KeyError:
			raise ValueError
		else:
			start = self._fix_neg_index(start)
			if end == None:
				end = len(self)
			else:
				end = self._fix_neg_index(end)
			if start <= index and index < end:
				return index
			else:
				raise ValueError

	def sub_index(self, sub, start=0, end=-1):
		"""
		Find the index of a subsequence

		This runs in O(len(sub))
		
		>>> sl = setlist('abcdef')
		>>> sl.sub_index('ef')
		4
		>>> try:
		...   sl.sub_index('cb')
		...   False
		... except ValueError:
		...   True
		True
		"""
		try:
			if sub[0] in self:
				index = self._dict[sub[0]]
				for i in range(1, len(sub)):
					if sub[i] != self[index+i]:
						raise ValueError
				return index
		except TypeError:
			pass

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


class setlist(_basesetlist, MutableSequence, MutableSet):
	""" A mutable (unhashable) setlist that inherits from _basesetlist. 
	
	>>> sl = setlist('abcde')
	>>> sl[0] = 5
	>>> sl
	setlist((5, 'b', 'c', 'd', 'e'))
	>>> sl[-1] = 0
	>>> sl
	setlist((5, 'b', 'c', 'd', 0))
	>>> sl[1] = 'c'
	>>> sl
	setlist((5, 'b', 'c', 'd', 0))
	>>> del sl[0]
	>>> sl
	setlist(('b', 'c', 'd', 0))
	>>> del sl[-1]
	>>> sl
	setlist(('b', 'c', 'd'))
	>>> sl.pop()
	'd'
	>>> sl.pop(0)
	'b'
	>>> sl
	setlist(('c',))
	>>> sl.insert(0, 'a')
	>>> sl
	setlist(('a', 'c'))
	>>> sl.insert(len(sl), 'e')
	>>> sl
	setlist(('a', 'c', 'e'))
	>>> sl.append('f')
	>>> sl
	setlist(('a', 'c', 'e', 'f'))
	>>> sl += ('g', 'h')
	>>> sl
	setlist(('a', 'c', 'e', 'f', 'g', 'h'))
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
		for i in range(index + 1, len(self._list)):
			elem = self._list[i]
			self._dict[elem] = self._dict[elem] - 1
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
		for i in range(index, len(self._list)):
			elem = self._list[i]
			self._dict[elem] = self._dict[elem] + 1
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
		This runs in O(len(self))

		>>> sl = setlist('abcdefgh')
		>>> sl.remove_all(set('acdh'))
		>>> sl
		setlist(('b', 'e', 'f', 'g'))
		"""
		## First go through and mark all of the items to delete, also remove them from the dict
		marked_to_delete = object()
		num_to_delete = 0
		for i in range(len(self)):
			elem = self[i]
			if elem in elems_to_delete:
				del self._dict[elem]
				self._list[i] = marked_to_delete
				num_to_delete += 1
		## Now go through and shift elements backwards
		deleted_count = 0
		for i in range(len(self._list)):
			elem = self._list[i]
			if elem == marked_to_delete:
				deleted_count += 1
			else:
				self._list[i - deleted_count] = elem
				self._dict[elem] = i - deleted_count
		## Now remove deleted_count items from the end of the list
		for i in range(deleted_count):
			del self._list[len(self._list)-1]

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

class frozensetlist(_basesetlist, Hashable):
	""" An immutable (hashable) setlist that inherits from _basesetlist. """

	def __hash__(self):
		return self._list.__hash__() ^ self._dict.__hash__()

