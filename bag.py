#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#
""" multiset - Also known as a bag or unordered tuple.

This module provides three classes:
	basemultiset - The superclass of multiset and frozen multiset.  It is both immutable
		and unhashable.
	multiset - A mutable (unhashable) multiset.
	frozenmultiset - A hashable (immutable) multiset.
"""

_version = '0.2.0'

import heapq
from collections import MutableSet, Set, Hashable, Iterable
from operator import itemgetter

class basemultiset(Set):
	""" Base class for multiset and frozenmultiset.	Is not mutable and not hashable, so there's 
	no reason to use this instead of either multiset or frozenmultiset.
	"""
	## Basic object methods

	def __init__(self, iterable=None):
		""" Create a new basemultiset.  If iterable isn't given, is None or is empty then the 
		set starts empty.  If iterable is a map, then it is assumed to be a map from elements
		to the number of times they should appear in the multiset.  Otherwise each element 
		from iterable will be added to the multiset however many times it appears.

		This runs in O(len(iterable))

		>>> basemultiset()                     # create empty set
		basemultiset()
		>>> basemultiset('abracadabra')        # create from an Iterable
		basemultiset(('a', 'a', 'a', 'a', 'a', 'r', 'r', 'b', 'b', 'c', 'd'))
		"""
		self.__dict = dict()
		self.__size = 0
		if iterable:
			for elem in iterable:
				self.__inc(elem)
	
	def __repr__(self):
		""" The string representation is a call to the constructor given a tuple 
		containing all of the elements.
		
		This runs in whatever tuple(self) does, I'm assuming O(len(self))

		>>> ms = basemultiset()

		>>> ms == eval(ms.__repr__())
		True
		>>> ms = basemultiset('abracadabra')

		>>> ms == eval(ms.__repr__())
		True
		"""
		if self.__size == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			format = '{class_name}({tuple!r})'
			return format.format(class_name=self.__class__.__name__, tuple=tuple(self))
	
	def __str__(self):
		""" The printable string appears just like a set, except that each element 
		is raised to the power of the multiplicity if it is greater than 1.

		This runs in O(self.num_unique_elements())

		>>> print(basemultiset())
		{}
		>>> print(basemultiset('abracadabra'))
		{'a'^5, 'r'^2, 'b'^2, 'c', 'd'}
		>>> basemultiset('abc').__str__() == set('abc').__str__()
		True
		"""
		if self.__size == 0:
			return '{}'
		else:
			format_single = '{elem!r}'
			format_mult = '{elem!r}^{mult}'
			strings = []
			for elem, mult in self.__dict.items():
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

	def __inc(self, elem, count=1):
		""" Increment the multiplicity of elem by count (if count <0 then decrement). 
		
		This runs in O(1) time
		"""
		old_count = self.multiplicity(elem)
		new_count = max(0, old_count + count)
		if new_count == 0:
			try:
				del self.__dict[elem]
			except KeyError:
				pass
		else:
			self.__dict[elem] = new_count
		self.__size += new_count - old_count

	## New public methods (not overriding/implementing anything)

	def num_unique_elements(self):
		""" Returns the number of unique elements. 
		
		This runs in O(1) time
		"""
		return len(self.__dict)

	def unique_elements(self):
		""" Returns a view of unique elements in this multiset. 
		
		This runs in O(1) time
		"""
		return self.__dict.keys()

	def multiplicity(self, elem):
		""" Return the multiplicity of elem.  If elem is not in the set no Error is
		raised, instead 0 is returned. 
		
		This runs in O(1) time

		>>> ms = basemultiset('abracadabra')

		>>> ms.multiplicity('a')
		5
		>>> ms.multiplicity('x')
		0
		"""
		try:
			return self.__dict[elem]
		except KeyError:
			return 0
	
	def nlargest(self, n=None):
		""" List the n most common elements and their counts from the most
		common to the least.  If n is None, the list all element counts.

		Run time should be O(m log m) where m is len(self)

		>>> basemultiset('abracadabra').nlargest()
		[('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)]
		>>> basemultiset('abracadabra').nlargest(2)
		[('a', 5), ('r', 2)]
		"""
		if n is None:
			return sorted(self.__dict.items(), key=itemgetter(1), reverse=True)
		else:
			return heapq.nlargest(n, self.__dict.items(), key=itemgetter(1))

	@classmethod
	def _from_map(cls, map):
		""" Creates a multiset from a dict of elem->count.  Each key in the dict 
		is added if the value is > 0.

		This runs in O(len(map))
		
		>>> basemultiset._from_map({'a': 1, 'b': 2})
		basemultiset(('a', 'b', 'b'))
		"""
		out = cls()
		for elem, count in map.items():
			out.__inc(elem, count)
		return out

	def copy(self):
		""" Create a shallow copy of self.

		This runs in O(len(self.num_unique_elements()))
		
		>>> basemultiset().copy() == basemultiset()
		True
		>>> abc = basemultiset('abc')

		>>> abc.copy() == abc
		True
		"""
		return self._from_map(self.__dict)

	## Alias methods - these methods are just names for other operations

	def cardinality(self): return len(self)
	def underlying_set(self): return unique_elements()
	def cartesian_product(self, other): return self * other
	def join(self, other): return self + other
	def sum(self, other): return self + other
	def difference(self, other): return self - other
	def symmetric_difference(self, other): return self ^ other
	def xor(self, other): return self ^ other
	def intersect(self, other): return self & other
	def union(self, other): return self | other
	
	## implementing Sized (inherited from Set) methods

	def __len__(self):
		""" Returns the cardinality of the multiset. 

		This runs in O(1)
		
		>>> len(basemultiset())
		0
		>>> len(basemultiset('abc'))
		3
		>>> len(basemultiset('aaba'))
		4
		"""
		return self.__size

	## implementing Container (inherited from Set) methods

	def __contains__(self, elem):
		""" Returns the multiplicity of the element. 

		This runs in O(1)
		
		>>> 'a' in basemultiset('bbac')
		True
		>>> 'a' in basemultiset()
		False
		>>> 'a' in basemultiset('missing letter')
		False
		"""
		return self.multiplicity(elem)
	
	## implementing Iterable (inherited from Set) methods

	def __iter__(self):
		""" Iterate through all elements, multiple copies will be returned if they exist. """
		for elem, count in self.__dict.items():
			for i in range(count):
				yield(elem)

	## implementing/overriding Set methods
	##
	## Also included here is __add__ even though its not overriding a Set method.
	## I figured it would be better to keep it with the other set operations.

	def __le__(self, other):
		"""

		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a multiset:
				l = 1
			else:
				l = len(other)

		TODO write test cases for __le__
		"""
		if not isinstance(other, basemultiset):
			if not isinstance(other, Iterable):
				return NotImplemented
			other = self._from_iterable(other)
		if len(self) > len(other):
			return False
		for elem in self.unique_elements():
			if self.multiplicity(elem) > other.multiplicity(elem):
				return False
		return True

	def __and__(self, other):
		""" Intersection is the minimum of corresponding counts. 
		
		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a multiset:
				l = 1
			else:
				l = len(other)

		TODO write unit tests for and
		"""
		if not isinstance(other, basemultiset):
			if not isinstance(other, Iterable):
				return NotImplemented
			other = self._from_iterable(other)
		values = dict()
		for elem in self.__dict:
			values[elem] = min(other.multiplicity(elem), self.multiplicity(elem))
		return self._from_map(values)

	def isdisjoint(self, other):
		"""

		This runs in O(l + m*n) where:
			m is self.num_unique_elements()
			n is other.num_unique_elements()
			if other is a multiset:
				l = 1
			else:
				l = len(other)

		TODO write unit tests for isdisjoint
		"""
		if not isinstance(other, basemultiset):
			if not isinstance(other, Iterable):
				return NotImplemented
			other = self._from_iterable(other)
		return super.isdisjoint(self.unique_elements(), other.unique_elements())

	def __or__(self, other):
		""" Union is the maximum of all elements. 
		
		This runs in O(m + n) where:
			n is self.num_unique_elements()
			if other is a multiset:
				m = other.num_unique_elements()
			else:
				m = len(other)

		TODO write unit tests for or
		"""
		if not isinstance(other, basemultiset):
			if not isinstance(other, Iterable):
				return NotImplemented
			other = self._from_iterable(other)
		values = dict()
		for elem in self.unique_elements() | other.unique_elements():
			values[elem] = max(self.multiplicity(elem), other.multiplicity(elem))
		return self._from_map(values)

	def __add__(self, other):
		""" Sum of sets
		other can be any iterable.
		self + other = self & other + self | other 

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		
		TODO write unit tests for add
		"""
		if not isinstance(other, Iterable):
			return NotImplemented
		out = self.copy()
		for elem in other:
			out.__inc(elem)
		return out
	
	def __sub__(self, other):
		""" Difference between the sets.
		other can be any iterable.
		For normal sets this is all s.t. x in self and x not in other. 
		For multisets this is multiplicity(x) = max(0, self.multiplicity(x)-other.multiplicity(x))

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)

		TODO write tests for sub
		"""
		if not isinstance(other, Iterable):
			return NotImplemented
		out = self.copy()
		for elem in other:
			out.__inc(elem, -1)
		return out

	def __mul__(self, other):
		""" Cartesian product of the two sets.
		other can be any iterable.
		Both self and other must contain elements that can be added together.

		This should run in O(m*n+l) where:
			m is the number of unique elements in self
			n is the number of unique elements in other
			if other is a multiset:
				l is 0
			else:
				l is the len(other)
		The +l will only really matter when other is an iterable with MANY repeated elements
		For example: {'a'^2} * 'bbbbbbbbbbbbbbbbbbbbbbbbbb'
		The algorithm will be dominated by counting the 'b's

		>>> ms = basemultiset('aab')

		>>> ms * set('a')
		basemultiset(('aa', 'aa', 'ba'))
		>>> ms * set()
		basemultiset()
		"""
		if not isinstance(other, basemultiset):
			if not isinstance(other, Iterable):
				return NotImplemented
			other = self._from_iterable(other)
		values = dict()
		for elem, count in self.__dict.items():
			for other_elem, other_count in other.__dict.items():
				new_elem = elem + other_elem
				new_count = count * other_count
				values[new_elem] = new_count
		return self._from_map(values)

	def __xor__(self, other):
		""" Symmetric difference between the sets. 
		other can be any iterable.

		This runs in < O(m+n) where:
			m = len(self)
			n = len(other)

		TODO write unit tests for xor
		"""
		return (self - other) | (other - self)

class multiset(basemultiset, MutableSet):
	""" multiset is a Mutable basemultiset, thus not hashable and unusable for dict keys or in
	other sets.

	TODO write multiset add, discard and clear unit tests
	"""
	def add(self, elem):
		self.__inc(elem, 1)
	
	def discard(self, elem):
		self.__inc(elem, -1)

	def clear(self):
		self.__dict = dict()
		self.__size = 0

class frozenmultiset(basemultiset, Hashable):
	""" frozenmultiset is a Hashable basemultiset, thus it is immutable and usable for dict keys
	"""
	def __hash__(self):
		""" Use the hash funtion inherited from somewhere.  For now this is from Set,
		I'm not sure that it works for collections with multiple elements.

		TODO write unit tests for hash
		"""
		return self._hash()
	
def multichoose(iterable, k):
	""" Returns a set of all possible multisets of length k on unique elements from iterable.
	The number of sets returned is C(n+k-1, k) where:
		C is the binomial coefficient function
		n is the number of unique elements in iterable
		k is the cardinality of the resulting multisets

	The run time is O((n+k)!/(n!*k!)) which is O((n+k)^min(k,n))
	DO NOT run this on big inputs.

	see http://en.wikipedia.org/wiki/Multiset#Multiset_coefficients

	>>> multichoose((), 1)
	set()
	>>> multichoose('a', 1)
	{frozenmultiset(('a',))}
	>>> multichoose('a', 2)
	{frozenmultiset(('a', 'a'))}
	>>> result = multichoose('ab', 3)

	>>> len(result)
	4
	>>> frozenmultiset(('a', 'a', 'a')) in result
	True
	>>> frozenmultiset(('a', 'a', 'b')) in result
	True
	>>> frozenmultiset(('a', 'b', 'b')) in result
	True
	>>> frozenmultiset(('b', 'b', 'b')) in result
	True
	"""
	# if iterable is empty there are no multisets
	if not iterable:
		return set()

	symbols = set(iterable)
	
	symbol = symbols.pop()
	result = set()
	if len(symbols) == 0:
		result.add(frozenmultiset._from_map({symbol : k}))
	else:
		for symbol_multiplicity in range(k+1):
			symbol_set = frozenmultiset._from_map({symbol : symbol_multiplicity})
			for others in multichoose(symbols, k-symbol_multiplicity):
				result.add(symbol_set + others)
	return result

