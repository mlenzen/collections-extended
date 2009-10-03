#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
"""

__all__ = ['collection', 'Collection', 'MutableCollection', 'MutableSequence', 'setlist', 'frozensetlist', 'bag', 'frozenbag']

from abc import ABCMeta, abstractmethod
from collections import *
from bag import _basebag, bag, frozenbag
from setlist import _basesetlist, setlist, frozensetlist
import collections
__all__ += collections.__all__

def collection(it : Iterable = (), mutable=True, ordered=False, unique=False):
	""" Return a Collection with the specified properties. 
	
	>>> isinstance(collection(), bag)
	True
	>>> isinstance(collection(ordered=True), list)
	True
	>>> isinstance(collection(unique=True), set)
	True
	>>> isinstance(collection(unique=True, ordered=True), setlist)
	True
	>>> isinstance(collection(mutable=False), frozenbag)
	True
	>>> isinstance(collection(mutable=False, ordered=True), tuple)
	True
	>>> isinstance(collection(mutable=False, unique=True), frozenset)
	True
	>>> isinstance(collection(mutable=False, ordered=True, unique=True), frozensetlist)
	True
	"""
	if unique:
		if ordered:
			if mutable:
				return setlist(it)
			else:
				return frozensetlist(it)
		else:
			if mutable:
				return set(it)
			else:
				return frozenset(it)
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
	""" An ABC for all collections.
	>>> isinstance(list(), Collection)
	True
	>>> isinstance(set(), Collection)
	True
	>>> isinstance(bag(), Collection)
	True
	>>> isinstance(setlist(), Collection)
	True
	"""
	@classmethod
	def _from_iterable(cls, it):
		""" Construct an instance of the class from any iterable input.

		Must override this method if the class constructor signature
		does not accept an iterable for an input.
		"""
		return cls(it)

	def count(self, elem):
		count = 0
		for e in self:
			if e == elem:
				count += 1
		return count

Collection.register(Sequence)
Collection.register(Set)
Collection.register(_basebag)

class MutableCollection(Collection):
	""" A metaclass for all MutableCollection objects.
	
	>>> isinstance(list(), MutableCollection)
	True
	>>> isinstance(set(), MutableCollection)
	True
	>>> isinstance(bag(), MutableCollection)
	True
	>>> isinstance(setlist(), MutableCollection)
	True
	"""
	@abstractmethod
	def add(self, value):
		raise ValueError

	@abstractmethod
	def remove(self, value):
		raise ValueError

	@abstractmethod
	def pop(self):
		raise KeyError

MutableCollection.register(MutableSequence)
MutableCollection.register(MutableSet)
MutableCollection.register(bag)

#####################################################################
## Extending built-in classes
#####################################################################

class MutableSequence(MutableSequence):
	""" Extended MutableSequence to fit Collection ABC """

	def add(self, value):
		return self.append(value)
