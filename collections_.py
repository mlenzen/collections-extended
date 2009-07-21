#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#
""" collections_ - An extension of the built-in collections to include bags and setlists.

This module is an extension of the built-in collections module that contains
implementations of bags, AKA multisets, and setlists, AKA ordered sets or unique lists.
"""
_version = '0.3.0'

__all__ = ['setlist', 'frozensetlist', 'bag', 'frozenbag']

import heapq
import sys
from abc import ABCMeta, abstractmethod
from operator import itemgetter
from collections import *
import collections
__all__ += collections.__all__

#####################################################################
## setlists
#####################################################################

class _basesetlist(Sequence, Set):
	""" A setlist is an ordered Collection of unique elements.
	_basesetlist is the superclass of setlist and frozensetlist.  It is immutable
	and unhashable.
	"""

	def __init__(self, iterable : Iterable = None):
		self._list = list()
		self._dict = dict()
		if iterable:
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
		return self._list.__reversed__()

	def count(self, sub, start=0, end=-1):
		"""
		This runs in O(len(sub))

		>>> sl = setlist('abcdea')
		>>> sl.count('a')
		1
		>>> sl.count('f')
		0
		>>> sl.count('bc')
		1
		"""
		try:
			self.index(sub, start, end)
			return 1
		except ValueError:
			return 0

	def index(self, sub, start=0, end=-1):
		"""
		This runs in O(len(sub))

		>>> sl = setlist('abcdef')
		>>> sl.index('a')
		0
		>>> sl.index('ef')
		4
		>>> try:
		...   sl.index('cb')
		...   False
		... except ValueError:
		...   True
		True
		"""
		# First assume that sub is an element in self
		try:
			index = self._dict[sub]
			return index
		except KeyError:
			pass
		# If we didn't find it as an element, maybe it's a sublist to find
		if sub[0] in self:
			try:
				index = self._dict[sub[0]]
				for i in range(1, len(sub)):
					if sub[i] != self[index+i]:
						raise ValueError
				return index
			except TypeError:
				pass
		raise ValueError

	## Nothing needs to be done to implement Set

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
		del self._dict[self._dict[value]]
	
	def remove_all(self, elems_to_delete: Set):
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
		if value not in self:
			return
		del self._dict[self._dict[value]]

	def clear(self):
		self._dict = dict()
		self._list = list()

class frozensetlist(_basesetlist, Hashable):
	""" An immutable (hashable) setlist that inherits from _basesetlist. """

	def __hash__(self):
		return self._list.__hash__() + self._dict.__hash__() % sys.maxint

#####################################################################
## bags
#####################################################################

class _basebag(Sized, Iterable, Container):
	""" Base class for bag and frozenbag.	Is not mutable and not hashable, so there's 
	no reason to use this instead of either bag or frozenbag.
	"""
	## Basic object methods

	def __init__(self, iterable : Iterable = None):
		""" Create a new basebag.  If iterable isn't given, is None or is empty then the 
		bag starts empty.  Otherwise each element from iterable will be added to the bag 
		however many times it appears.

		This runs in O(len(iterable))

		>>> _basebag()                     # create empty bag
		_basebag()
		>>> _basebag('abracadabra')        # create from an Iterable
		_basebag(('a', 'a', 'a', 'a', 'a', 'r', 'r', 'b', 'b', 'c', 'd'))
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
	
	@classmethod
	def _from_iterable(cls, it):
		""" Construct an instance of the class from any iterable input.

		Must override this method if the class constructor signature
		does not accept an iterable for an input.
		"""
		return cls(it)

	def __repr__(self):
		""" The string representation is a call to the constructor given a tuple 
		containing all of the elements.
		
		This runs in whatever tuple(self) does, I'm assuming O(len(self))

		>>> ms = _basebag()
		>>> ms == eval(ms.__repr__())
		True
		>>> ms = _basebag('abracadabra')
		>>> ms == eval(ms.__repr__())
		True
		"""
		if self._size == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			format = '{class_name}({tuple!r})'
			return format.format(class_name=self.__class__.__name__, tuple=tuple(self))
	
	def __str__(self):
		""" The printable string appears just like a set, except that each element 
		is raised to the power of the multiplicity if it is greater than 1.

		This runs in O(self.num_unique_elements())

		>>> print(_basebag())
		bag()
		>>> print(_basebag('abracadabra'))
		{'a'^5, 'r'^2, 'b'^2, 'c', 'd'}
		>>> _basebag('abc').__str__() == set('abc').__str__()
		True
		"""
		if self._size == 0:
			return 'bag()'
		else:
			format_single = '{elem!r}'
			format_mult = '{elem!r}^{mult}'
			strings = []
			for elem, mult in self._dict.items():
				if mult > 1:
					strings.append(format_mult.format(elem=elem, mult=mult))
				else:
					strings.append(format_single.format(elem=elem))
			strings = tuple(strings)
			string = '{first}'.format(first=strings[0])
			for i in range(1,len(strings)):
				string = '{prev}, {next}'.format(prev=string, next=strings[i])
			string = '{{{0}}}'.format(string)
			return string

	## Internal methods

	def _set(self, elem, value):
		""" Set the multiplicity of elem to count. 
		
		This runs in O(1) time
		"""
		if value < 0:
			raise ValueError
		old_count = self.multiplicity(elem)
		if value == 0:
			if elem in self:
				del self._dict[elem]
		else:
			self._dict[elem] = value
		self._size += value - old_count

	def _inc(self, elem, count=1):
		""" Increment the multiplicity of value by count (if count <0 then decrement). """
		self._set(elem, self.multiplicity(elem) + count)

	## New public methods (not overriding/implementing anything)

	def num_unique_elements(self):
		""" Returns the number of unique elements. 
		
		This runs in O(1) time
		"""
		return len(self._dict)

	def unique_elements(self):
		""" Returns a view of unique elements in this bag. 
		
		This runs in O(1) time
		"""
		return set(self._dict.keys())

	def multiplicity(self, value):
		""" Return the multiplicity of value.  If value is not in the bag no Error is
		raised, instead 0 is returned. 
		
		This runs in O(1) time

		>>> ms = _basebag('abracadabra')

		>>> ms.multiplicity('a')
		5
		>>> ms.multiplicity('x')
		0
		"""
		try:
			return self._dict[value]
		except KeyError:
			return 0
	
	def nlargest(self, n=None):
		""" List the n most common elements and their counts from the most
		common to the least.  If n is None, the list all element counts.

		Run time should be O(m log m) where m is len(self)

		>>> _basebag('abracadabra').nlargest()
		[('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)]
		>>> _basebag('abracadabra').nlargest(2)
		[('a', 5), ('r', 2)]
		"""
		if n is None:
			return sorted(self._dict.items(), key=itemgetter(1), reverse=True)
		else:
			return heapq.nlargest(n, self._dict.items(), key=itemgetter(1))

	@classmethod
	def _from_map(cls, map):
		""" Creates a bag from a dict of elem->count.  Each key in the dict 
		is added if the value is > 0.

		This runs in O(len(map))
		
		>>> _basebag._from_map({'a': 1, 'b': 2})
		_basebag(('a', 'b', 'b'))
		"""
		out = cls()
		for elem, count in map.items():
			out._inc(elem, count)
		return out

	def copy(self):
		""" Create a shallow copy of self.

		This runs in O(len(self.num_unique_elements()))
		
		>>> _basebag().copy() == _basebag()
		True
		>>> abc = _basebag('abc')

		>>> abc.copy() == abc
		True
		"""
		return self._from_map(self._dict)

	## Alias methods - these methods are just names for other operations

	def cardinality(self): return len(self)
	def underlying_set(self): return self.unique_elements()
	
	## implementing Sized methods

	def __len__(self):
		""" Returns the cardinality of the bag. 

		This runs in O(1)
		
		>>> len(_basebag())
		0
		>>> len(_basebag('abc'))
		3
		>>> len(_basebag('aaba'))
		4
		"""
		return self._size

	## implementing Container methods

	def __contains__(self, value):
		""" Returns the multiplicity of the element. 

		This runs in O(1)
		
		>>> 'a' in _basebag('bbac')
		True
		>>> 'a' in _basebag()
		False
		>>> 'a' in _basebag('missing letter')
		False
		"""
		return self.multiplicity(value)
	
	## implementing Iterable methods

	def __iter__(self):
		""" Iterate through all elements, multiple copies will be returned if they exist. """
		for value, count in self._dict.items():
			for i in range(count):
				yield(value)

	## Comparison methods
	## A bag can be compared to any iterable
	
	def __le__(self, other: Iterable):
		""" Tests if self <= other where other is any Iterable

		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				l = 1
			else:
				l = len(other)

		>>> _basebag() <= _basebag()
		True
		>>> _basebag() <= _basebag('a')
		True
		>>> _basebag('abc') <= _basebag('aabbbc')
		True
		>>> _basebag('abbc') <= _basebag('abc')
		False
		>>> _basebag('abc') <= set('abc')
		True
		>>> _basebag('abbc') <= set('abc')
		False
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		if len(self) > len(other):
			return False
		for elem in self.unique_elements():
			if self.multiplicity(elem) > other.multiplicity(elem):
				return False
		return True

	def __lt__(self, other: Iterable):
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		return len(self) < len(other) and self <= other

	def __gt__(self, other: Iterable):
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		return other < self

	def __ge__(self, other: Iterable):
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		return other <= self

	def __eq__(self, other: Iterable):
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		return len(self) == len(other) and self <= other 

	def __ne__(self, other: Iterable):
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		return not (self == other)

	## Operations - &, |, +, -, ^, * and isdisjoint

	def __and__(self, other: Iterable):
		""" Intersection is the minimum of corresponding counts. 
		
		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				l = 1
			else:
				l = len(other)

		>>> bag('aabc') & bag('aacd') == bag('aac')
		True
		>>> bag() & bag('safgsd') == bag()
		True
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem in self._dict:
			values[elem] = min(other.multiplicity(elem), self.multiplicity(elem))
		return self._from_map(values)

	def isdisjoint(self, other: Iterable):
		""" This runs in O(len(other))

		TODO move isdisjoint somewhere more appropriate
		>>> bag().isdisjoint(bag())
		True
		>>> bag().isdisjoint(bag('abc'))
		True
		>>> bag('ab').isdisjoint(bag('ac'))
		False
		>>> bag('ab').isdisjoint(bag('cd'))
		True
		"""
		for value in other:
			if value in self:
				return False
		return True

	def __or__(self, other: Iterable):
		""" Union is the maximum of all elements. 
		
		This runs in O(m + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				m = other.num_unique_elements()
			else:
				m = len(other)

		>>> bag('abcc') | bag() == bag('abcc')
		True
		>>> bag('abcc') | bag('aabd') == bag('aabccd')
		True
		>>> bag('aabc') | set('abdd') == bag('aabcd')
		True
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem in self.unique_elements() | other.unique_elements():
			values[elem] = max(self.multiplicity(elem), other.multiplicity(elem))
		return self._from_map(values)

	def __add__(self, other: Iterable):
		"""
		other can be any iterable.
		self + other = self & other + self | other 

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		
		>>> bag('abcc') & bag() == bag()
		True
		>>> bag('abcc') & bag('aabd') == bag('ab')
		True
		>>> bag('aabc') & set('abdd') == bag('ab')
		True
		"""
		out = self.copy()
		for value in other:
			out._inc(value)
		return out
	
	def __sub__(self, other: Iterable):
		""" Difference between the sets.
		other can be any iterable.
		For normal sets this is all s.t. x in self and x not in other. 
		For bags this is multiplicity(x) = max(0, self.multiplicity(x)-other.multiplicity(x))

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)

		>>> bag('abc') - bag() == bag('abc')
		True
		>>> bag('abbc') - bag('bd') == bag('abc')
		True
		"""
		out = self.copy()
		for value in other:
			try:
				out._inc(value, -1)
			except ValueError:
				pass
		return out

	def __mul__(self, other: Iterable):
		""" Cartesian product of the two sets.
		other can be any iterable.
		Both self and other must contain elements that can be added together.

		This should run in O(m*n+l) where:
			m is the number of unique elements in self
			n is the number of unique elements in other
			if other is a bag:
				l is 0
			else:
				l is the len(other)
		The +l will only really matter when other is an iterable with MANY repeated elements
		For example: {'a'^2} * 'bbbbbbbbbbbbbbbbbbbbbbbbbb'
		The algorithm will be dominated by counting the 'b's

		>>> ms = _basebag('aab')

		>>> ms * set('a')
		_basebag(('aa', 'aa', 'ba'))
		>>> ms * set()
		_basebag()
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
		""" Symmetric difference between the sets. 
		other can be any iterable.

		This runs in O(m + n) where:
			m = len(self)
			n = len(other)

		>>> bag('abc') ^ bag() == bag('abc')
		True
		>>> bag('aabc') ^ bag('ab') == bag('ac')
		True
		>>> bag('aabcc') ^ bag('abcde') == bag('acde')
		True
		"""
		return (self - other) | (other - self)

	def multichoose(it: Iterable, k):
		""" Returns a set of all possible multisets of length k on unique elements from iterable.
		The number of sets returned is C(n+k-1, k) where:
			C is the binomial coefficient function
			n is the number of unique elements in iterable
			k is the cardinality of the resulting multisets

		The run time is O((n+k-1)!/((n-1)!*k!)) which is O((n+k)^min(k,n))
		DO NOT run this on big inputs.

		see http://en.wikipedia.org/wiki/Multiset#Multiset_coefficients

		>>> _basebag.multichoose((), 1)
		set()
		>>> _basebag.multichoose('a', 1)
		{frozenbag(('a',))}
		>>> _basebag.multichoose('a', 2)
		{frozenbag(('a', 'a'))}
		>>> result = _basebag.multichoose('ab', 3)
		>>> len(result) == 4 and \
			 	frozenbag(('a', 'a', 'a')) in result and \
			 	frozenbag(('a', 'a', 'b')) in result and \
			 	frozenbag(('a', 'b', 'b')) in result and \
			 	frozenbag(('b', 'b', 'b')) in result
		True
		"""
		# if iterable is empty there are no multisets
		if not it:
			return set()
		symbols = set(it)
		symbol = symbols.pop()
		result = set()
		if len(symbols) == 0:
			result.add(frozenbag._from_map({symbol : k}))
		else:
			for symbol_multiplicity in range(k+1):
				symbol_set = frozenbag._from_map({symbol : symbol_multiplicity})
				for others in _basebag.multichoose(symbols, k-symbol_multiplicity):
					result.add(symbol_set + others)
		return result

class bag(_basebag):
	""" bag is a MutableCollection _basebag, thus not hashable and unusable for dict keys or in
	other sets.
	"""

	def pop(self):
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

	## In-place operations

	def __ior__(self, other: Iterable):
		"""
		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))

		>>> b = bag()
		>>> b |= bag()
		>>> print(b)
		bag()
		>>> b = bag('aab')
		>>> b |= bag()
		>>> print(b)
		{'a'^2, 'b'}
		>>> b = bag('aab')
		>>> b |= bag('ac')
		>>> print(b)
		{'a'^2, 'c', 'b'}
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, other_count in other._dict.items():
			self_count = self.multiplicity(elem)
			self._set(elem, max(other_count, self_count))
		return self
	
	def __iand__(self, other: Iterable):
		"""
		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))

		>>> b = bag()
		>>> b &= bag()
		>>> print(b)
		bag()
		>>> b = bag('aab')
		>>> b &= bag()
		>>> print(b)
		bag()
		>>> b = bag('aab')
		>>> b &= bag('ac')
		>>> print(b)
		{'a'}
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, self_count in set(self._dict.items()):
			other_count = other.multiplicity(elem)
			self._set(elem, min(other_count, self_count))
		return self
	
	def __ixor__(self, other: Iterable):
		"""
		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))

		>>> b = bag('abbc')
		>>> b ^= bag('bg')
		>>> b == bag('abcg')
		True
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		other_minus_self = other - self
		self -= other
		self |= other_minus_self
		return self
	
	def __isub__(self, other: Iterable):
		"""
		if isinstance(it, _basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))

		>>> b = bag('aabbc')
		>>> b -= bag('bd')
		>>> b == bag('aabc')
		True
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, count in other._dict.items():
			try:
				self._inc(elem, -count)
			except ValueError:
				pass
		return self

	def __iadd__(self, other: Iterable):
		"""
		if isinstance(it, _basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))

		>>> b = bag('abc')
		>>> b += bag('cde')
		>>> b == bag('abccde')
		True
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, count in other._dict.items():
			self._inc(elem, count)
		return self
	

class frozenbag(_basebag, Hashable):
	""" frozenbag is a Hashable _basebag, thus it is immutable and usable for dict keys
	"""
	def __hash__(self):
		""" Use the hash funtion from Set,
		I'm not sure that it works for collections with multiple elements.

		>>> hash(frozenbag()) == hash(frozenbag((0,)))
		False
		>>> hash(frozenbag('a')) == hash(frozenbag(('aa')))
		False
		>>> hash(frozenbag('a')) == hash(frozenbag(('aaa')))
		False
		>>> hash(frozenbag('a')) == hash(frozenbag(('aaaa')))
		False
		>>> hash(frozenbag('a')) == hash(frozenbag(('aaaaa')))
		False
		>>> hash(frozenbag('ba')) == hash(frozenbag(('ab')))
		True
		>>> hash(frozenbag('badce')) == hash(frozenbag(('dbeac')))
		True
		"""
		return Set._hash(self)

