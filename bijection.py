#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2010 Michael Lenzen <m.lenzen@gmail.com>
#
# This is part of the project at http://code.google.com/p/python-data-structures/
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
""" bijection - a one-to-one onto mapping, a dict with unique values

TODO write long desc

This implementation kinda sucks because it stores everything twice.
"""

from collections import MutableMapping

class bijection(MutableMapping):
	"""

	TODO write unit tests for bijection including dict methods like copy
	"""
	def __init__(self, *args):
		self.data = dict(args)
		self.invr = bijection()
		self.invr.invr = self
		for key, value in self.data.items():
			if value in self.invr.data:
				del self.data(self.invr.data[value])
			self.data[key] = value
	
	def __len__(self):
		return len(self.data)

	def __getitem__(self, key):
		return self.data[key]
	
	def __setitem__(self, key, value):
		if key in self:
			del self.invr.data[self[key]]
		if value in self.invr:
			del self.data[self.invr[value]]
		self.data[key] = value
		self.invr.data[value] = key

	def __delitem__(self, key):
		# if key is not is self then self[key] will raise a KeyError as expected
		del self.invr.data[self[key]]
		del self.data[key]
	
	def __contains__(self, key):
		return key in self.data

	def iter(self):
		return self.data.iter()
	
	def clear(self):
		""" This should be more efficient than MutableMapping.clear """
		self.data.clear()
		self.invr.data.clear()

	def copy(self):
		return bijection(self)
	
	@classmethod
	def fromkeys(cls, seq, value=None):
		""" Since only the last pair will be retained (as values must be unique) 
		we have a more optimal solution than dict's. """
		result = bijection()
		result[seq[-1]] = value
		return result

	def get(self, key, default=None):
		if key in self:
			return self[key]
		else:
			return default

	def items(self):
		return self.data.items()

	def keys(self):
		return self.data.keys()

	def values(self):
		return self.invr.keys()

	def __eq__(self, other):
		if not isinstance(other, bijection):
			return False
		return self.data == other.data

	def __ne__(self, other):
		return not self.__eq__(other)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

