"""SortedList class definition."""

import bisect

class SortedList(list):
	"""Extends list and keeps values in sorted order.

	A key can be specified like for sorted.

	All list methods are inherited but raise a ValueError if they result in
	inserting a value in the wrong order.

	SortedList cannot enforce correct ordering after mutable elements are
	added then modified.
	"""

	def __init__(self, *args, key=None, reverse=None, **kwargs):
		self.key = key
		self.reverse = reverse
		super().__init__(*args, **kwargs)

	def __setitem__(self, key, value):
		if key + 1 >= 0 and value < self[key - 1]:
			raise ValueError
		if key + 1 < len(self) and value > self[key + 1]:
			raise ValueError
		super().__setitem__(key, value)

	def add(self, object):
		# TODO optionally add left or right
		pass

	def count(self, value, start=0, end=None):
		pass

	def index(self, value, start=0, stop=None):
		pass

	def sort(self, key=None, reverse=False):
		super().sort(key=key, reverse=reverse)
		self.key = key
		self.reverse = reverse
