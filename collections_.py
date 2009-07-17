#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#

_version = '0.1.0'

from abc import abstractmethod
from collections import Sized, Iterable, Container

class Collection(Sized, Iterable, Container):
	@classmethod
	def _from_iterable(cls, it):
		"""Construct an instance of the class from any iterable input.

		Must override this method if the class constructor signature
		does not accept an iterable for an input.
		"""
		return cls(it)

	@abstractmethod
	def __getitem__(self, key):
		raise KeyError

class Mutable():
	@abstractmethod
	def __setitem__(self, key, value):
		raise KeyError

	@abstractmethod
	def __delitem__(self, key):
		raise KeyError

	def pop(self):
		"""Return the popped value.  Raise KeyError if empty."""
		it = iter(self)
		try:
			value = next(it)
		except StopIteration:
			raise KeyError
		self.discard(value)
		return value

class set_(set, Collection, Mutable):
	""" 
	TODO document set_
	TODO write unit tests for set_
	"""
	def __getitem__(self, item):
		""" Returns `item in self` """
		return item in self

	def __setitem__(self, elem1, elem2):
		""" Replaces elem1 with elem2.  
		If elem1 not in self raise KeyError.  
		If elem2 in self, raise ValueError.
		"""
		if elem2 in self:
			raise ValueError
		if elem1 not in self:
			raise KeyError
		self.discard(item)
		self.add(value)

	def __delitem__(self, item):
		""" Deletes item from self.  Raises KeyError if item is not in self. """
		self.delete(item)
