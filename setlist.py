#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#
""" setlist - an ordered collection of unique elements

TODO write long-desc
"""

_version = '0.1.1'

from collections import MutableSet, Set, Hashable, Iterable, Sequence, MutableSequence
import sys

from collection import Collection, Mutable

class basesetlist(Collection, Sequence, Set):
	"""
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
	"""
	"""
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
		del self._dict.pop(index)
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
	"""
	"""

	def __hash__(self):
		return self._list.__hash__() + self._dict.__hash__() % sys.maxint
