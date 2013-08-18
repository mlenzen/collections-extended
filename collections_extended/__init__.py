'''collections_extended contains a few extra basic data structures'''

__version__ = '0.1.2'

from abc import ABCMeta, abstractmethod
from collections import *
import collections

from .bags import bag, frozenbag
from .setlists import setlist, frozensetlist

__all__ = ['collection', 'Collection', 'MutableCollection', 'MutableSequence', 'Set', 'setlist', 'frozensetlist', 'bag', 'frozenbag'] + collections.__all__

def collection(it=(), mutable=True, ordered=False, unique=False):
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
Collection.register(bag)
Collection.register(frozenbag)

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

class Set(Set):
	""" Extended Set to efficiently count elements. """

	def count(self, elem):
		return elem in self

class MutableSequence(MutableSequence):
	""" Extended MutableSequence to fit Collection ABC """

	def add(self, value):
		return self.append(value)

