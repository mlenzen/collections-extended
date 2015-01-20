import heapq
from operator import itemgetter
from collections import Sized, Iterable, Container, Hashable

from . import _compat


class _basebag(Sized, Iterable, Container):
	"""
	Base class for bag and frozenbag.	Is not mutable and not hashable, so there's
	no reason to use this instead of either bag or frozenbag.
	"""
	# Basic object methods

	def __init__(self, iterable=None):
		"""Create a new basebag.

		If iterable isn't given, is None or is empty then the bag starts empty.
		Otherwise each element from iterable will be added to the bag
		however many times it appears.

		This runs in O(len(iterable))
		"""
		self._dict = dict()
		self._size = 0
		if iterable:
			if isinstance(iterable, _basebag):
				for elem, count in iterable._dict.items():
					self._inc(elem, count)
			else:
				for value in iterable:
					self._inc(value)

	def __repr__(self):
		"""The string representation is a call to the constructor given a tuple
		containing all of the elements.

		This runs in whatever tuple(self) does, I'm assuming O(len(self))
		"""
		if self._size == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			format = '{class_name}({tuple!r})'
			return format.format(class_name=self.__class__.__name__, tuple=tuple(self))

	def __str__(self):
		"""The printable string appears just like a set, except that each element
		is raised to the power of the multiplicity if it is greater than 1.

		This runs in O(self.num_unique_elements())
		"""
		if self._size == 0:
			return '{class_name}()'.format(class_name=self.__class__.__name__)
		else:
			format_single = '{elem!r}'
			format_mult = '{elem!r}^{mult}'
			strings = []
			for elem, mult in self._dict.items():
				if mult > 1:
					strings.append(format_mult.format(elem=elem, mult=mult))
				else:
					strings.append(format_single.format(elem=elem))
			return '{%s}' % ', '.join(strings)

	# Internal methods

	def _set(self, elem, value):
		"""Set the multiplicity of elem to count.

		This runs in O(1) time
		"""
		if value < 0:
			raise ValueError
		old_count = self.count(elem)
		if value == 0:
			if elem in self:
				del self._dict[elem]
		else:
			self._dict[elem] = value
		self._size += value - old_count

	def _inc(self, elem, count=1):
		"""Increment the multiplicity of value by count.

		If count <0 then decrement.
		"""
		self._set(elem, self.count(elem) + count)

	# New public methods (not overriding/implementing anything)

	def num_unique_elements(self):
		"""Returns the number of unique elements.

		This runs in O(1) time
		"""
		return len(self._dict)

	def unique_elements(self):
		"""Returns a view of unique elements in this bag.

		This runs in O(1) time
		"""
		return _compat.keys_set(self._dict)

	def count(self, value):
		"""Return the multiplicity of value.  If value is not in the bag no Error is
		raised, instead 0 is returned.

		This runs in O(1) time
		"""
		return self._dict.get(value, 0)

	def nlargest(self, n=None):
		"""List the n most common elements and their counts from the most
		common to the least.  If n is None, the list all element counts.

		Run time should be O(m log m) where m is len(self)
		"""
		if n is None:
			return sorted(self._dict.items(), key=itemgetter(1), reverse=True)
		else:
			return heapq.nlargest(n, self._dict.items(), key=itemgetter(1))

	@classmethod
	def _from_iterable(cls, it):
		return cls(it)

	@classmethod
	def _from_map(cls, map):
		"""Creates a bag from a dict of elem->count.  Each key in the dict
		is added if the value is > 0.

		This runs in O(len(map))
		"""
		out = cls()
		for elem, count in map.items():
			out._inc(elem, count)
		return out

	def copy(self):
		"""Create a shallow copy of self.

		This runs in O(len(self.num_unique_elements()))
		"""
		return self._from_map(self._dict)

	# implementing Sized methods

	def __len__(self):
		"""Returns the cardinality of the bag.

		This runs in O(1)
		"""
		return self._size

	# implementing Container methods

	def __contains__(self, value):
		"""Returns the multiplicity of the element.

		This runs in O(1)
		"""
		return self.count(value)

	# implementing Iterable methods

	def __iter__(self):
		"""Iterate through all elements.

		Multiple copies will be returned if they exist.
		"""
		for value, count in self._dict.items():
			for i in range(count):
				yield(value)

	# Comparison methods

	def __le__(self, other):
		"""Tests if self <= other where other is another bag

		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				l = 1
			else:
				l = len(other)
		"""
		if not isinstance(other, _basebag):
			return NotImplemented
		if len(self) > len(other):
			return False
		for elem in self.unique_elements():
			if self.count(elem) > other.count(elem):
				return False
		return True

	def __lt__(self, other):
		return self <= other and len(self) < len(other)

	def __gt__(self, other):
		return other < self

	def __ge__(self, other):
		return other <= self

	def __eq__(self, other):
		if not isinstance(other, _basebag):
			return False
		return len(self) == len(other) and self <= other

	def __ne__(self, other):
		return not (self == other)

	# Operations - &, |, +, -, ^, * and isdisjoint

	def __and__(self, other):
		"""Intersection is the minimum of corresponding counts.

		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				l = 1
			else:
				l = len(other)
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem in self._dict:
			values[elem] = min(other.count(elem), self.count(elem))
		return self._from_map(values)

	def isdisjoint(self, other):
		"""This runs in O(len(other))

		TODO move isdisjoint somewhere more appropriate
		"""
		for value in other:
			if value in self:
				return False
		return True

	def __or__(self, other):
		"""Union is the maximum of all elements.

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				m = other.num_unique_elements()
			else:
				m = len(other)
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem in self.unique_elements() | other.unique_elements():
			values[elem] = max(self.count(elem), other.count(elem))
		return self._from_map(values)

	def __add__(self, other):
		"""
		other can be any iterable.
		self + other = self & other + self | other

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		"""
		out = self.copy()
		for value in other:
			out._inc(value)
		return out

	def __sub__(self, other):
		"""Difference between the sets.
		other can be any iterable.
		For normal sets this is all s.t. x in self and x not in other.
		For bags this is count(x) = max(0, self.count(x)-other.count(x))

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		"""
		out = self.copy()
		for value in other:
			try:
				out._inc(value, -1)
			except ValueError:
				pass
		return out

	def __mul__(self, other):
		"""Cartesian product of the two sets.
		other can be any iterable.
		Both self and other must contain elements that can be added together.

		This should run in O(m*n+l) where:
			m is the number of unique elements in self
			n is the number of unique elements in other
			if other is a bag:
				l is 0
			else:
				l is the len(other)
		The +l will only really matter when other is an iterable with MANY
		repeated elements.
		For example: {'a'^2} * 'bbbbbbbbbbbbbbbbbbbbbbbbbb'
		The algorithm will be dominated by counting the 'b's
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem, count in self._dict.items():
			for other_elem, other_count in other._dict.items():
				new_elem = elem + other_elem
				new_count = count * other_count
				values[new_elem] = new_count
		return self._from_map(values)

	def __xor__(self, other):
		"""Symmetric difference between the sets.
		other can be any iterable.

		This runs in O(m + n) where:
			m = len(self)
			n = len(other)
		"""
		return (self - other) | (other - self)


class bag(_basebag):
	"""bag is a mutable _basebag.

	Thus not hashable and unusable for dict keys or in other sets.
	"""

	def pop(self):
		# TODO can this be done more efficiently (no need to create an iterator)?
		it = iter(self)
		try:
			value = next(it)
		except StopIteration:
			raise KeyError
		self.discard(value)
		return value

	def add(self, elem):
		self._inc(elem, 1)

	def discard(self, elem):
		try:
			self.remove(elem)
		except ValueError:
			pass

	def remove(self, elem):
		self._inc(elem, -1)

	def clear(self):
		self._dict = dict()
		self._size = 0

	# In-place operations

	def __ior__(self, other):
		"""
		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, other_count in other._dict.items():
			self_count = self.count(elem)
			self._set(elem, max(other_count, self_count))
		return self

	def __iand__(self, other):
		"""
		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, self_count in set(self._dict.items()):
			other_count = other.count(elem)
			self._set(elem, min(other_count, self_count))
		return self

	def __ixor__(self, other):
		"""
		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		other_minus_self = other - self
		self -= other
		self |= other_minus_self
		return self

	def __isub__(self, other):
		"""
		if isinstance(it, _basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, count in other._dict.items():
			try:
				self._inc(elem, -count)
			except ValueError:
				pass
		return self

	def __iadd__(self, other):
		"""
		if isinstance(it, _basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, count in other._dict.items():
			self._inc(elem, count)
		return self


class frozenbag(_basebag, Hashable):
	"""frozenbag is an immutable _basebag.

	Thus it is Hashable and usable for dict keys
	"""
	def __hash__(self):
		"""Compute the hash value of a frozenbag.

		This was copied directly from _collections_abc.Set._hash in Python3 which
		is identical to _abcoll.Set._hash
		We can't call it directly because Python2 raises a TypeError.
		"""
		MAX = _compat.maxint
		MASK = 2 * MAX + 1
		n = len(self)
		h = 1927868237 * (n + 1)
		h &= MASK
		for x in self:
			hx = hash(x)
			h ^= (hx ^ (hx << 16) ^ 89869747) * 3644798167
			h &= MASK
		h = h * 69069 + 907133923
		h &= MASK
		if h > MAX:
			h -= MASK + 1
		if h == -1:
			h = 590923713
		return h
