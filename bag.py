#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#
""" bag - Also known as a bag or unordered tuple.

This module provides three classes:
	basebag - The superclass of bag and frozenbag.  It is both immutable
		and unhashable.
	bag - A mutable (unhashable) multiset.
	frozenbag - A hashable (immutable) multiset.
"""

_version = '0.3.0'

import heapq
from collections import Set, Hashable, Iterable
from collection import Collection, MutableCollection
from operator import itemgetter

class basebag(Collection):
	""" Base class for bag and frozenbag.	Is not mutable and not hashable, so there's 
	no reason to use this instead of either bag or frozenbag.
	"""
	## Basic object methods

	def __init__(self, iterable=None):
		""" Create a new basebag.  If iterable isn't given, is None or is empty then the 
		bag starts empty.  Otherwise each element from iterable will be added to the bag 
		however many times it appears.

		This runs in O(len(iterable))

		>>> basebag()                     # create empty bag
		basebag()
		>>> basebag('abracadabra')        # create from an Iterable
		basebag(('a', 'a', 'a', 'a', 'a', 'r', 'r', 'b', 'b', 'c', 'd'))
		"""
		self.__dict = dict()
		self.__size = 0
		if iterable:
			for value in iterable:
				self.__inc(value)
	
	def __repr__(self):
		""" The string representation is a call to the constructor given a tuple 
		containing all of the elements.
		
		This runs in whatever tuple(self) does, I'm assuming O(len(self))

		>>> ms = basebag()

		>>> ms == eval(ms.__repr__())
		True
		>>> ms = basebag('abracadabra')

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

		>>> print(basebag())
		{}
		>>> print(basebag('abracadabra'))
		{'a'^5, 'r'^2, 'b'^2, 'c', 'd'}
		>>> basebag('abc').__str__() == set('abc').__str__()
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

	def __getitem__(self, value):
		return self.multiplicity(value)

	## Internal methods

	def __inc(self, value, count=1):
		""" Increment the multiplicity of value by count (if count <0 then decrement). 
		
		This runs in O(1) time
		"""
		old_count = self.multiplicity(value)
		new_count = max(0, old_count + count)
		if new_count == 0:
			try:
				del self.__dict[value]
			except KeyError:
				pass
		else:
			self.__dict[value] = new_count
		self.__size += new_count - old_count

	## New public methods (not overriding/implementing anything)

	def num_unique_elements(self):
		""" Returns the number of unique elements. 
		
		This runs in O(1) time
		"""
		return len(self.__dict)

	def unique_elements(self):
		""" Returns a view of unique elements in this bag. 
		
		This runs in O(1) time
		"""
		return self.__dict.keys()

	def multiplicity(self, value):
		""" Return the multiplicity of value.  If value is not in the bag no Error is
		raised, instead 0 is returned. 
		
		This runs in O(1) time

		>>> ms = basebag('abracadabra')

		>>> ms.multiplicity('a')
		5
		>>> ms.multiplicity('x')
		0
		"""
		try:
			return self.__dict[value]
		except KeyError:
			return 0
	
	def nlargest(self, n=None):
		""" List the n most common elements and their counts from the most
		common to the least.  If n is None, the list all element counts.

		Run time should be O(m log m) where m is len(self)

		>>> basebag('abracadabra').nlargest()
		[('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)]
		>>> basebag('abracadabra').nlargest(2)
		[('a', 5), ('r', 2)]
		"""
		if n is None:
			return sorted(self.__dict.items(), key=itemgetter(1), reverse=True)
		else:
			return heapq.nlargest(n, self.__dict.items(), key=itemgetter(1))

	@classmethod
	def _from_map(cls, map):
		""" Creates a bag from a dict of elem->count.  Each key in the dict 
		is added if the value is > 0.

		This runs in O(len(map))
		
		>>> basebag._from_map({'a': 1, 'b': 2})
		basebag(('a', 'b', 'b'))
		"""
		out = cls()
		for elem, count in map.items():
			out.__inc(elem, count)
		return out

	def copy(self):
		""" Create a shallow copy of self.

		This runs in O(len(self.num_unique_elements()))
		
		>>> basebag().copy() == basebag()
		True
		>>> abc = basebag('abc')

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
	
	## implementing Sized methods

	def __len__(self):
		""" Returns the cardinality of the bag. 

		This runs in O(1)
		
		>>> len(basebag())
		0
		>>> len(basebag('abc'))
		3
		>>> len(basebag('aaba'))
		4
		"""
		return self.__size

	## implementing Container methods

	def __contains__(self, value):
		""" Returns the multiplicity of the element. 

		This runs in O(1)
		
		>>> 'a' in basebag('bbac')
		True
		>>> 'a' in basebag()
		False
		>>> 'a' in basebag('missing letter')
		False
		"""
		return self.multiplicity(value)
	
	## implementing Iterable methods

	def __iter__(self):
		""" Iterate through all elements, multiple copies will be returned if they exist. """
		for value, count in self.__dict.items():
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

		TODO write test cases for __le__
		"""
		if not isinstance(other, basebag):
			other = self._from_iterable(other)
		if len(self) > len(other):
			return False
		for elem in self.unique_elements():
			if self.multiplicity(elem) > other.multiplicity(elem):
				return False
		return True

	def __lt__(self, other: Iterable):
		if not isinstance(other, basebag):
			other = self._from_iterable(other)
		return len(self) < len(other) and self <= other

	def __gt__(self, other: Iterable):
		if not isinstance(other, basebag):
			other = self._from_iterable(other)
		return other < self

	def __ge__(self, other: Iterable):
		if not isinstance(other, basebag):
			other = self._from_iterable(other)
		return other <= self

	def __eq__(self, other: Iterable):
		if not isinstance(other, basebag):
			other = self._from_iterable(other)
		return len(self) == len(other) and self <= other 

	def __ne__(self, other: Iterable):
		if not isinstance(other, basebag):
			other = self._from_iterable(other)
		return not (self == other)

	## Operations - &, |, +, -, ^, * and isdisjoint

	def __and__(self, other):
		""" Intersection is the minimum of corresponding counts. 
		
		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				l = 1
			else:
				l = len(other)

		TODO write unit tests for and
		"""
		if not isinstance(other, basebag):
			if not isinstance(other, Iterable):
				return NotImplemented
			other = self._from_iterable(other)
		values = dict()
		for elem in self.__dict:
			values[elem] = min(other.multiplicity(elem), self.multiplicity(elem))
		return self._from_map(values)

	def isdisjoint(self, other):
		"""

		This runs in O(n) where:
			n is len(other)

		TODO write unit tests for isdisjoint
		TODO move isdisjoint somewhere more appropriate
		"""
		if not isinstance(other, Iterable):
			return NotImplemented
		for value in other:
			if value in self:
				return False
		return True

	def __or__(self, other):
		""" Union is the maximum of all elements. 
		
		This runs in O(m + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				m = other.num_unique_elements()
			else:
				m = len(other)

		TODO write unit tests for or
		"""
		if not isinstance(other, basebag):
			if not isinstance(other, Iterable):
				return NotImplemented
			other = self._from_iterable(other)
		values = dict()
		for elem in self.unique_elements() | other.unique_elements():
			values[elem] = max(self.multiplicity(elem), other.multiplicity(elem))
		return self._from_map(values)

	def __add__(self, other):
		"""
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
		for value in other:
			out.__inc(value)
		return out
	
	def __sub__(self, other):
		""" Difference between the sets.
		other can be any iterable.
		For normal sets this is all s.t. x in self and x not in other. 
		For bags this is multiplicity(x) = max(0, self.multiplicity(x)-other.multiplicity(x))

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)

		TODO write tests for sub
		"""
		if not isinstance(other, Iterable):
			return NotImplemented
		out = self.copy()
		for value in other:
			out.__inc(value, -1)
		return out

	def __mul__(self, other):
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

		>>> ms = basebag('aab')

		>>> ms * set('a')
		basebag(('aa', 'aa', 'ba'))
		>>> ms * set()
		basebag()
		"""
		if not isinstance(other, basebag):
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

class bag(basebag, MutableCollection):
	""" bag is a Mutable basebag, thus not hashable and unusable for dict keys or in
	other sets.

	TODO write bag add, discard and clear unit tests
	"""

	def __setitem__(self, elem, value=True):
		if value:
			add(elem)
	
	def __delitem__(self, value):
		self.remove(value)

	def add(self, value):
		self.__inc(value, 1)
	
	def discard(self, value):
		self.__inc(value, -1)

	def remove(self, value):
		if value not in self:
			raise KeyError(value)
		self.discard(value)

	def clear(self):
		self.__dict = dict()
		self.__size = 0

	def pop(self):
		it = iter(self)
		try:
			value = next(it)
		except StopIteration:
			raise KeyError
		self.discard(value)
		return value

	## In-place operations

	def __ior__(self, it: Iterable):
		"""
		This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			other = it
		else:
			other = self._from_iterable(it)
		for elem, other_count in other.__dict.items():
			self_count = self.multiplicity(elem)
			self.__inc(elem, max(other_count, self_count) - self_count)
	
	def __iand__(self, it: Iterable):
		"""
		This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			other = it
		else:
			other = self._from_iterable(it)
		for elem, other_count in other.__dict.items():
			self_count = self.multiplicity(elem)
			self.__inc(elem, min(other_count, self_count) - self_count)
	
	def __ixor__(self, it: Iterable):
		"""
		if isinstance(it, basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			other = it
		else:
			other = self._from_iterable(it)
		other_minus_self = other - self
		self -= other
		self |= other_minus_self
	
	def __isub__(self, it: Iterable):
		"""
		if isinstance(it, basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			for elem, count in it.__dict.items():
				self.__inc(value, -count)
		else:
			for value in it:
				self.__inc(value, -1)

	def __iadd__(self, it: Iterable):
		"""
		if isinstance(it, basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			for elem, count in it.__dict.items():
				self.__inc(value, count)
		else:
			for value in it:
				self.__inc(value, 1)
	

class frozenbag(basebag, Hashable):
	""" frozenbag is a Hashable basebag, thus it is immutable and usable for dict keys
	"""
	def __hash__(self):
		""" Use the hash funtion from Set,
		I'm not sure that it works for collections with multiple elements.

		TODO write unit tests for hash
		"""
		return Set._hash(self)
	
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
	{frozenbag(('a',))}
	>>> multichoose('a', 2)
	{frozenbag(('a', 'a'))}
	>>> result = multichoose('ab', 3)

	>>> len(result)
	4
	>>> frozenbag(('a', 'a', 'a')) in result
	True
	>>> frozenbag(('a', 'a', 'b')) in result
	True
	>>> frozenbag(('a', 'b', 'b')) in result
	True
	>>> frozenbag(('b', 'b', 'b')) in result
	True
	"""
	# if iterable is empty there are no multisets
	if not iterable:
		return set()

	symbols = set(iterable)
	
	symbol = symbols.pop()
	result = set()
	if len(symbols) == 0:
		result.add(frozenbag._from_map({symbol : k}))
	else:
		for symbol_multiplicity in range(k+1):
			symbol_set = frozenbag._from_map({symbol : symbol_multiplicity})
			for others in multichoose(symbols, k-symbol_multiplicity):
				result.add(symbol_set + others)
	return result

