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
It also assumes that dict only manipulates everything via __setitem__ and __delitem__
"""

class bijection(dict):
	"""

	TODO write unit tests for bijection including dict methods like copy
	"""
	def __init__(self, *args):
		dict.__init__(self, args)
		self.invr = bijection()
		self.invr.invr = self
		for key, value in self.items():
			if value in self.invr:
				dict.__delitem__(self, self.invr[value])
			dict.__setitem__(invr, value, key)
	
	def clear(self):
		dict.clear(self)
		dict.clear(invr)
	
	def __setitem__(self, key, value):
		if key in self:
			dict.__delitem__(invr, self[key])
		if value in self.invr:
			dict.__delitem__(self, self.invr[value])
		dict.__setitem__(self, key, value)
		dict.__setitem__(invr, value, key)

	def __delitem__(self, key):
		# if key is not is self then self[key] will raise a KeyError as expected
		dict.__delitem__(invr, self[key])
		dict.__delitem__(self, key)
	
	def values(self):
		return self.invr.keys()

	def __eq__(self, other):
		if not isinstance(other, bijection):
			return False
		return dict.__eq__(self, other)

	def __ne__(self, other):
		return not self.__eq__(other)

	@classmethod
	def fromkeys(cls, seq, value=None):
		""" Since only the last pair will be retained (as values must be unique) we have a more optimal solution than dict's. """
		result = bijection()
		result[seq[-1]] = value
		return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()

