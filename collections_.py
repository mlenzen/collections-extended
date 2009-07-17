#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#

_version = '0.1.0'

import heapq
import sys
from abc import ABCMeta, abstractmethod
from collections import Sized, Iterable, Container, Set, Hashable, MutableSet, MutableSequence, Sequence
from operator import itemgetter

def collection(it: Iterable=None, mutable=False, ordered=False, unique=False):
	""" Return a Collection with the specified properties. """
	if unique:
		if ordered:
			if mutable:
				return setlist(it)
			else:
				return frozensetlist(it)
		else:
			if mutable:
				return set_(it)
			else:
				return frozenset_(it)
	else:
		if ordered:
			if mutable:
				return list(it)
			else:
				return tuple(it)
		else:
			if mutable:
				return bag(it)
			else:
				return frozenbag(it)

#####################################################################
## ABCs
#####################################################################

class Collection(Sized, Iterable, Container):
	@classmethod
	def _from_iterable(cls, it):
		""" Construct an instance of the class from any iterable input.

		Must override this method if the class constructor signature
		does not accept an iterable for an input.
		"""
		return cls(it)

	@abstractmethod
	def __getitem__(self, key):
		raise KeyError

Collection.register(list)
Collection.register(tuple)

class Mutable(metaclass=ABCMeta):
	@abstractmethod
	def __setitem__(self, key, value):
		raise KeyError

	@abstractmethod
	def __delitem__(self, key):
		raise KeyError

	@abstractmethod
	def pop(self):
		raise KeyError

Mutable.register(list)

#####################################################################
## Extending sets
#####################################################################

class set_(set, Collection, Mutable):
	""" set_ extends set and implements Collection and Mutable.
	set_[item]
		returns if the item is in the set_
	set_[item] = value
		sets whether or not item is in set_ based on what value evaluates to
	del set_[item]
		removes item from set_
	
	>>> s = set_('abc')
	>>> s['a']
	True
	>>> s['d']
	False
	>>> s['a'] = False
	>>> 'a' in s
	False
	>>> del s['b']
	>>> 'b' in s
	False
	"""
	def __getitem__(self, item):
		""" Equal to `item in self` """
		return item in self

	def __setitem__(self, elem, value):
		""" Set whether or not elem is in set_ based on what value evaluates to. """
		if value:
			self.add(elem)
		else:
			self.remove(elem)

	def __delitem__(self, item):
		self.remove(item)

class frozenset_(frozenset, Collection):
	""" frozenset_ extends frozenset and implements Collection """
	def __getitem__(self, item):
		return item in self

#####################################################################
## setlists
#####################################################################

class basesetlist(Collection, Sequence, Set):
	""" A setlist is an ordered Collection of unique elements.
	basesetlist is the superclass of setlist and frozensetlist.  It is immutable
	and unhashable.
	"""

	def __init__(self, iterable: Iterable):
		self._list = list()
		self._dict = dict()
		if iterable:
			for value in iterable:
				if value not in self:
					index = len(self)
					self._list.insert(index, value)
					self._dict[value] = index
	
	def __str__(self):
		return self._list.__str__()

	def __repr__(self):
		if len(self) == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			format = '{class_name}({tuple!r})'
			return format.format(class_name=self.__class__.__name__, tuple=tuple(self))
	
	## Implement Collection
	def __getitem__(self, index):
		return self._list.__getitem__(index)

	## Implement Container from Collection
	def __contains__(self, elem): 
		return self._dict.__contains__(elem)

	## Implement Iterable from Collection
	def __iter__(self):
		self._list.__iter__()

	## Implement Sized from Collection
	def __len__(self):
		return self._list.__len__()

	## Implement Sequence
	def __reversed__(self):
		return self._list.__reversed__()

	def count(sub, start=0, end=-1):
		"""
		This runs in O(len(sub))
		"""
		try:
			index(sub, start, end)
			return 1
		except ValueError:
			return 0

	def index(sub, start=0, end=-1):
		"""
		This runs in O(len(sub))
		"""
		index %= len(self)
		# First assume that sub is an element in self
		try:
			index = self._dict[sub]
			return index
		except KeyError:
			pass
		# If we didn't find it as an element, maybe it's a sublist to find
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

class setlist(basesetlist, Mutable, MutableSequence, MutableSet):
	""" A mutable (unhashable) setlist that inherits from basesetlist. """
	## Implement Mutable
	def __setitem__(self, index, value):
		index %= len(self)
		if index >= len(self):
			raise IndexError
		if value in self:
			return
		old_value = self._list[index]
		self._list[index] = value
		del self._dict[value]
		self._dict[value] = index

	def __delitem__(self, index):
		index %= len(self)
		if index >= len(self):
			raise IndexError
		old_value = self._list[index]
		del self._list[index]
		del self._dict[old_value]
	
	def pop(self, index=-1):
		index %= len(self)
		value = self._list.pop(index)
		del self._dict[value]
		return value

	## Implement MutableSequence
	def insert(self, index, value):
		index %= len(self)
		if index > len(self):
			raise IndexError
		if value in self:
			return
		index %= len(self)
		self._list.insert(index, value)
		self._dict[value] = index
	
	def append(self, value):
		insert(self, len(self), value)
	
	def extend(self, values):
		for value in values:
			self.append(value)

	def __iadd__(self, values):
		""" This will quietly not add values that are already present. """
		self.extend(values)
		return self

	def remove(self, value):
		del self[self._dict[value]]

	## Implement MutableSet
	def add(self, item):
		self.append(item)

	def discard(self, value):
		if value not in self:
			return
		index = self._dict[value]
		del self._list[index]
		del self._dict[value]

	def clear(self):
		self._dict = dict()
		self._list = list()

class frozensetlist(basesetlist, Hashable):
	""" An immutable (hashable) setlist that inherits from basesetlist. """

	def __hash__(self):
		return self._list.__hash__() + self._dict.__hash__() % sys.maxint

#####################################################################
## bags
#####################################################################

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
		self._dict = dict()
		self._size = 0
		if iterable:
			if isinstance(iterable, basebag):
				for elem, count in iterable._dict.items():
					self._inc(elem, count)
			else:
				for value in iterable:
					self._inc(value)
	
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
		if self._size == 0:
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
		if self._size == 0:
			return '{}'
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

	def __getitem__(self, value):
		return self._dict[value]

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
		return self._dict.keys()

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
			return self[value]
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
			return sorted(self._dict.items(), key=itemgetter(1), reverse=True)
		else:
			return heapq.nlargest(n, self._dict.items(), key=itemgetter(1))

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
			out._inc(elem, count)
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
		return self._from_map(self._dict)

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
		return self._size

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

		>>> basebag() <= basebag()
		True
		>>> basebag() <= basebag('a')
		True
		>>> basebag('abc') <= basebag('aabbbc')
		True
		>>> basebag('abbc') <= basebag('abc')
		False
		>>> basebag('abc') <= set('abc')
		True
		>>> basebag('abbc') <= set('abc')
		False
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

	def __and__(self, other: Iterable):
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
		for elem in self._dict:
			values[elem] = min(other.multiplicity(elem), self.multiplicity(elem))
		return self._from_map(values)

	def isdisjoint(self, other: Iterable):
		"""

		This runs in O(n) where:
			n is len(other)

		TODO write unit tests for isdisjoint
		TODO move isdisjoint somewhere more appropriate
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

		TODO write unit tests for or
		"""
		if not isinstance(other, basebag):
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
		
		TODO write unit tests for add
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

		TODO write tests for sub
		"""
		out = self.copy()
		for value in other:
			out._inc(value, -1)
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

		>>> ms = basebag('aab')

		>>> ms * set('a')
		basebag(('aa', 'aa', 'ba'))
		>>> ms * set()
		basebag()
		"""
		if not isinstance(other, basebag):
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

		This runs in < O(m+n) where:
			m = len(self)
			n = len(other)

		TODO write unit tests for xor
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

		>>> basebag.multichoose((), 1)
		set()
		>>> basebag.multichoose('a', 1)
		{frozenbag(('a',))}
		>>> basebag.multichoose('a', 2)
		{frozenbag(('a', 'a'))}
		>>> result = basebag.multichoose('ab', 3)
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
				for others in basebag.multichoose(symbols, k-symbol_multiplicity):
					result.add(symbol_set + others)
		return result

class bag(basebag, Mutable):
	""" bag is a Mutable basebag, thus not hashable and unusable for dict keys or in
	other sets.

	TODO write bag add, discard and clear unit tests
	"""

	def __setitem__(self, elem, value):
		""" This sets the number of times that value appears in the bag.

		>>> b = bag('abc')
		>>> b['a'] = 2
		>>> b['a']
		2
		>>> b['d'] = 5
		>>> b['d']
		5
		>>> b['d'] = 0
		>>> 'd' in b
		False
		"""
		self._set(elem, value)
	
	def __delitem__(self, elem):
		self.remove(elem)

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
		self._inc(elem, -1)

	def remove(self, value):
		if value not in self:
			raise KeyError(value)
		self.discard(value)

	def clear(self):
		self._dict = dict()
		self._size = 0

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
		for elem, other_count in other._dict.items():
			self_count = self.multiplicity(elem)
			self._set(elem, max(other_count, self_count))
		return self
	
	def __iand__(self, it: Iterable):
		"""
		This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			other = it
		else:
			other = self._from_iterable(it)
		for elem, other_count in other._dict.items():
			self_count = self.multiplicity(elem)
			self._set(elem, min(other_count, self_count))
		return self
	
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
		return self
	
	def __isub__(self, it: Iterable):
		"""
		if isinstance(it, basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			for elem, count in it._dict.items():
				self._inc(value, -count)
		else:
			for value in it:
				self._inc(value, -1)
		return self

	def __iadd__(self, it: Iterable):
		"""
		if isinstance(it, basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))

		TODO write test cases
		"""
		if isinstance(it, basebag):
			for elem, count in it._dict.items():
				self._inc(value, count)
		else:
			for value in it:
				self._inc(value, 1)
		return self
	

class frozenbag(basebag, Hashable):
	""" frozenbag is a Hashable basebag, thus it is immutable and usable for dict keys
	"""
	def __hash__(self):
		""" Use the hash funtion from Set,
		I'm not sure that it works for collections with multiple elements.

		XXX find out if Set._hash works for bags
		"""
		return Set._hash(self)

