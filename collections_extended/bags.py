"""Bag class definitions."""
from abc import ABCMeta, abstractmethod
import heapq
from collections import defaultdict
from operator import itemgetter

from ._compat import (
	Collection,
	Hashable,
	MutableSet,
	Set,
	handle_rich_comp_not_implemented,
	)
from ._util import deprecated

__all__ = (
	'BagView',
	'CountsView',
	'UniqueElementsView',
	'bag',
	'frozenbag',
	)


class BagView(Collection):
	"""Base class for bag views."""

	__metaclass__ = ABCMeta
	__slots__ = ('bag', )

	def __init__(self, bag):
		self.bag = bag

	def __repr__(self):
		return '{0.__class__.__name__}({0.bag!r})'.format(self)

	def __len__(self):
		return self.bag.num_unique_elements()

	@abstractmethod
	def __iter__(self):
		raise NotImplementedError

	@abstractmethod
	def __contains__(self, elem):
		raise NotImplementedError


class UniqueElementsView(BagView):
	"""A view for the unique items and their counts in a bag.

	.. versionadded:: 1.0
	"""

	def __iter__(self):
		for elem in self.bag._dict:
			yield elem

	def __contains__(self, elem):
		return elem in self.bag


class CountsView(BagView):
	"""A view for the unique items and their counts in a bag.

	.. versionadded:: 1.0
	"""

	__slots__ = ('bag', )

	def __len__(self):
		return self.bag.num_unique_elements()

	def __iter__(self):
		for elem in self.bag.unique_elements():
			yield elem, self.bag.count(elem)

	def __contains__(self, item):
		elem, count = item
		return self.bag.count(elem) == count


class _basebag(Set):
	"""Base class for bag classes.

	Base class for bag and frozenbag. Is not mutable and not hashable, so there's
	no reason to use this instead of either bag or frozenbag.
	"""

	# Basic object methods

	def __init__(self, iterable=None):
		"""Create a new bag.

		If iterable isn't given, is None or is empty then the bag starts empty.
		Otherwise each element from iterable will be added to the bag
		however many times it appears.

		This runs in O(len(iterable))
		"""
		self._dict = dict()
		self._size = 0
		if iterable:
			if isinstance(iterable, _basebag):
				self._dict = iterable._dict.copy()
				self._size = iterable._size
			else:
				for value in iterable:
					self._increment_count(value)

	def _set_count(self, elem, count):
		if count < 0:
			raise ValueError
		self._size += count - self.count(elem)
		if count == 0:
			self._dict.pop(elem, None)
		else:
			self._dict[elem] = count

	def _increment_count(self, elem, count=1):
		self._set_count(elem, self.count(elem) + count)

	@classmethod
	def _from_iterable(cls, it):
		return cls(it)

	def copy(self):
		"""Create a shallow copy of self.

		This runs in O(len(self.num_unique_elements()))
		"""
		out = self._from_iterable(None)
		out._dict = self._dict.copy()
		out._size = self._size
		return out

	def __repr__(self):
		if self._size == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			repr_format = '{class_name}({values!r})'
			return repr_format.format(
				class_name=self.__class__.__name__,
				values=tuple(self),
				)

	def __str__(self):
		if self._size == 0:
			return '{class_name}()'.format(class_name=self.__class__.__name__)
		else:
			format_single = '{elem!r}'
			format_mult = '{elem!r}^{mult}'
			strings = []
			for elem, mult in self.counts():
				if mult > 1:
					strings.append(format_mult.format(elem=elem, mult=mult))
				else:
					strings.append(format_single.format(elem=elem))
			return '{%s}' % ', '.join(strings)

	# New public methods (not overriding/implementing anything)

	def num_unique_elements(self):
		"""Return the number of unique elements.

		This runs in O(1) time
		"""
		return len(self._dict)

	def unique_elements(self):
		"""Return a view of unique elements in this bag."""
		return UniqueElementsView(self)

	def count(self, value):
		"""Return the number of value present in this bag.

		If value is not in the bag no Error is raised, instead 0 is returned.

		This runs in O(1) time

		Args:
			value: The element of self to get the count of
		Returns:
			int: The count of value in self
		"""
		return self._dict.get(value, 0)

	@deprecated(
		"Use `heapq.nlargest(n, self.counts(), key=itemgetter(1))` instead or "
		"`sorted(self.counts(), reverse=True, key=itemgetter(1))` for `n=None`",
		'1.0',
		)
	def nlargest(self, n=None):
		"""List the n most common elements and their counts.

		List is from the most
		common to the least.  If n is None, the list all element counts.

		Run time should be O(m log m) where m is len(self)
		Args:
			n (int): The number of elements to return
		"""
		if n is None:
			return sorted(self.counts(), key=itemgetter(1), reverse=True)
		else:
			return heapq.nlargest(n, self.counts(), key=itemgetter(1))

	def counts(self):
		"""Return a view of the unique elements in self and their counts.

		.. versionadded:: 1.1
		"""
		return CountsView(self)

	@classmethod
	def from_mapping(cls, mapping):
		"""Create a bag from a dict of elem->count.

		Each key in the dict is added if the value is > 0.

		Raises:
			ValueError: If any count is < 0.
		"""
		out = cls()
		for elem, count in mapping.items():
			out._set_count(elem, count)
		return out

	# implementing Sized methods

	def __len__(self):
		"""Return the cardinality of the bag.

		This runs in O(1)
		"""
		return self._size

	# implementing Container methods

	def __contains__(self, value):
		"""Return the multiplicity of the element.

		This runs in O(1)
		"""
		return self.count(value)

	# implementing Iterable methods

	def __iter__(self):
		"""Iterate through all elements.

		Multiple copies will be returned if they exist.
		"""
		for value, count in self.counts():
			for _ in range(count):
				yield value

	# Comparison methods

	@deprecated('Renamed to issubset', '1.1')
	def is_subset(self, other):
		"""Check that every element in self has a count <= in other.

		Args:
			other (Set)
		"""
		return self.issubset(other)

	def issubset(self, other):
		"""Check that every element in self has a count <= in other.

		Args:
			other (Set)
		"""
		if isinstance(other, _basebag):
			for elem, count in self.counts():
				if not count <= other.count(elem):
					return False
		else:
			for elem in self:
				if self.count(elem) > 1 or elem not in other:
					return False
		return True

	@deprecated('Renamed to issuperset', '1.1')
	def is_superset(self, other):
		"""Check that every element in self has a count >= in other.

		Args:
			other (Set)
		"""
		return self.issuperset(other)

	def issuperset(self, other):
		"""Check that every element in self has a count >= in other.

		Args:
			other (Set)
		"""
		if isinstance(other, _basebag):
			for elem, count in other.counts():
				if not self.count(elem) >= count:
					return False
		else:
			for elem in other:
				if elem not in self:
					return False
		return True

	def __le__(self, other):
		if not isinstance(other, Set):
			return handle_rich_comp_not_implemented()
		return len(self) <= len(other) and self.is_subset(other)

	def __lt__(self, other):
		if not isinstance(other, Set):
			return handle_rich_comp_not_implemented()
		return len(self) < len(other) and self.is_subset(other)

	def __gt__(self, other):
		if not isinstance(other, Set):
			return handle_rich_comp_not_implemented()
		return len(self) > len(other) and self.is_superset(other)

	def __ge__(self, other):
		if not isinstance(other, Set):
			return handle_rich_comp_not_implemented()
		return len(self) >= len(other) and self.is_superset(other)

	def __eq__(self, other):
		if not isinstance(other, Set):
			return False
		if isinstance(other, _basebag):
			return self._dict == other._dict
		if not len(self) == len(other):
			return False
		for elem in other:
			if self.count(elem) != 1:
				return False
		return True

	def __ne__(self, other):
		return not (self == other)

	# Operations - &, |, +, -, ^, * and isdisjoint

	def _iadd(self, other):
		"""Add all of the elements of other to self.

		if isinstance(it, _basebag):
				This runs in O(it.num_unique_elements())
		else:
				This runs in O(len(it))
		"""
		if isinstance(other, _basebag):
			for elem, count in other.counts():
				self._increment_count(elem, count)
		else:
			for elem in other:
				self._increment_count(elem, 1)
		return self

	def _iand(self, other):
		"""Set multiplicity of each element to the minimum of the two collections.

		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		# TODO do we have to create a bag from the other first?
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, old_count in set(self.counts()):
			other_count = other.count(elem)
			new_count = min(other_count, old_count)
			self._set_count(elem, new_count)
		return self

	def _ior(self, other):
		"""Set multiplicity of each element to the maximum of the two collections.

		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		# TODO do we have to create a bag from the other first?
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, other_count in other.counts():
			old_count = self.count(elem)
			new_count = max(other_count, old_count)
			self._set_count(elem, new_count)
		return self

	def _ixor(self, other):
		"""Set self to the symmetric difference between the sets.

		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		if isinstance(other, _basebag):
			for elem, other_count in other.counts():
				count = abs(self.count(elem) - other_count)
				self._set_count(elem, count)
		else:
			# Let a = self.count(elem) and b = other.count(elem)
			# if a >= b then elem is removed from self b times leaving a - b
			# if a < b then elem is removed from self a times then added (b - a)
			# times leaving a - a + (b - a) = b - a
			for elem in other:
				try:
					self._increment_count(elem, -1)
				except ValueError:
					self._increment_count(elem, 1)
		return self

	def _isub(self, other):
		"""Discard the elements of other from self.

		if isinstance(it, _basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))
		"""
		if isinstance(other, _basebag):
			for elem, other_count in other.counts():
				try:
					self._increment_count(elem, -other_count)
				except ValueError:
					self._set_count(elem, 0)
		else:
			for elem in other:
				try:
					self._increment_count(elem, -1)
				except ValueError:
					pass
		return self

	def __and__(self, other):
		"""Intersection is the minimum of corresponding counts.

		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				l = 1
			else:
				l = len(other)
		"""
		return self.copy()._iand(other)

	def isdisjoint(self, other):
		"""Return if this bag is disjoint with the passed collection.

		This runs in O(len(other))
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
		return self.copy()._ior(other)

	def __add__(self, other):
		"""Return a new bag also containing all the elements of other.

		self + other = self & other + self | other

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		Args:
			other (Iterable): elements to add to self
		"""
		return self.copy()._iadd(other)

	def __sub__(self, other):
		"""Difference between the sets.

		For normal sets this is all x s.t. x in self and x not in other.
		For bags this is count(x) = max(0, self.count(x)-other.count(x))

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		Args:
			other (Iterable): elements to remove
		"""
		return self.copy()._isub(other)

	def __mul__(self, other):
		"""Cartesian product with other."""
		return self.product(other)

	def product(self, other, operator=None):
		"""Cartesian product of the two sets.

		Optionally, pass an operator to combine elements instead of creating a
		tuple.

		This should run in O(m*n+l) where:
			m is the number of unique elements in self
			n is the number of unique elements in other
			if other is a bag:
				l is 0
			else:
				l is the len(other)

		Args:
			other (Iterable): The iterable to take the product with.
			operator (Callable): A function that accepts an element from self
				and other and returns a combined value to include in the return
				value.
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = defaultdict(int)
		for elem, count in self.counts():
			for other_elem, other_count in other.counts():
				if operator:
					new_elem = operator(elem, other_elem)
				else:
					new_elem = (elem, other_elem)
				new_count = count * other_count
				values[new_elem] += new_count
		return self.from_mapping(values)

	def __xor__(self, other):
		"""Symmetric difference between the sets.

		other can be any iterable.

		This runs in O(m + n) where:
			m = len(self)
			n = len(other)
		"""
		return self.copy()._ixor(other)


class bag(_basebag, MutableSet):
	"""bag is a mutable unhashable bag.

	.. automethod:: __init__
	"""

	def pop(self):
		"""Remove and return an element of self."""
		# TODO can this be done more efficiently (no need to create an iterator)?
		it = iter(self)
		try:
			value = next(it)
		except StopIteration:
			raise KeyError('pop from an empty bag')
		self.remove(value)
		return value

	def add(self, elem):
		"""Add elem to self."""
		self._increment_count(elem)

	def discard(self, elem):
		"""Remove elem from this bag, silent if it isn't present."""
		try:
			self.remove(elem)
		except ValueError:
			pass

	def remove(self, elem):
		"""Remove elem from this bag, raising a ValueError if it isn't present.

		Args:
			elem: object to remove from self
		Raises:
			ValueError: if the elem isn't present
		"""
		self._increment_count(elem, -1)

	def discard_all(self, other):
		"""Discard all of the elems from other."""
		self._isub(other)

	def remove_all(self, other):
		"""Remove all of the elems from other.

		Raises a ValueError if the multiplicity of any elem in other is greater
		than in self.
		"""
		if not self.is_superset(other):
			raise ValueError('Passed collection is not a subset of this bag')
		self.discard_all(other)

	def clear(self):
		"""Remove all elements from this bag."""
		self._dict = dict()
		self._size = 0

	# In-place operations

	__ior__ = _basebag._ior
	__iand__ = _basebag._iand
	__ixor__ = _basebag._ixor
	__isub__ = _basebag._isub
	__iadd__ = _basebag._iadd


class frozenbag(_basebag, Hashable):
	"""frozenbag is an immutable, hashable bag.

	.. automethod:: __init__
	"""

	def __hash__(self):
		"""Compute the hash value of a frozenbag.

		This was copied directly from _collections_abc.Set._hash in Python3 which
		is identical to _abcoll.Set._hash
		We can't call it directly because Python2 raises a TypeError.
		"""
		if not hasattr(self, '_hash_value'):
			self._hash_value = self._hash()
		return self._hash_value
