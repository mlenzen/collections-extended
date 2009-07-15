#!/usr/bin/env python3.1
# -*- coding: utf-8 -*-
#
# Copyright © 2009 Michael Lenzen <m.lenzen@gmail.com>
#
""" bijection - a one-to-one onto mapping, a dict with unique values

TODO write long desc
"""

class bijection(dict, MutableMapping):
	"""

	TODO write unit tests for bijection
	"""
	def __init__(self, *args):
		dict.__init__(self, args)
		self.invr = dict()
	
	def clear(self):
		dict.clear(self)
		dict.clear(invr)

	def __setitem__(self, key, value):
		if key in self or value in self.invr:
			# TODO hand inserts that already exist
			pass
		dict.__setitem__(self, key, value)
		dict.__setitem__(invr, value, key)

	def __delitem__(self, key):
		value = self[key]
		dict.__delitem__(self, key)
		dict.__delitem__(invr, value)
	
	def values(self):
		return self.invr.keys()
