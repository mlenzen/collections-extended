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

_version = '0.0.1'

from collections_ import *

_marked_to_delete = object()

class QuickList(MutableSequence):
	"""
	>>> ql = QuickList('0123456789abcdef')
	"""
	def __init__(self, iterable: Iterable = (), threshold=.5):
		self._list = list(iterable)
		self.threshold = threshold
		self._deleted_items = Deletree()
	
	def __eq__(self, other: Sequence):
		if len(self) != len(other):
			return False
		for i in range(len(self)):
			if self[i] != other[i]:
				return False
		return True
	
	def __repr__(self):
		"""
		>>> ql = QuickList()
		>>> ql == eval(ql.__repr__())
		True
		>>> ql = QuickList('abracadabra')
		>>> ql == eval(ql.__repr__())
		True
		"""
		if len(self) == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			format = '{class_name}({tuple!r})'
			return format.format(class_name=self.__class__.__name__, tuple=tuple(self))

	def __str__(self):
		string = ", ".join(self)
		return '[{}]'.format(string)

	def __getitem__(self, index):
		"""
		O(log(d)^2)
		"""
		return self._list[self._offset_index(index)]

	def __delitem__(self, index):
		"""
		amortized O(log(d)^2)
		"""
		index = self._offset_index(index)
		self._deleted_items.add(index)
		self._list[index] = _marked_to_delete
		if len(self._deleted_items) > self.threshold * len(self):
			self.clean()
	
	def __setitem__(self, index, value):
		"""
		O(log(d)^2)
		"""
		self._list[self._offset_index(index)] = value

	def __iter__(self):
		for i in range(len(self)):
			yield(self[i])
	
	def insert(self, index, value):
		"""
		O(n)
		"""
		# TODO insert as efficiently as delitem
		if len(self._deleted_items) > 0:
			self.clean()
		self._list.insert(index, value)
	
	def __len__(self):
		return len(self._list) - len(self._deleted_items)

	def clean(self):
		"""
		O(n)
		>>> ql = QuickList('abcdefgh', 1)
		>>> len(ql._list)
		8
		>>> ql.clean()
		>>> del ql[0]
		>>> del ql[0]
		>>> del ql[0]
		>>> len(ql)
		5
		>>> len(ql._list)
		8
		>>> ql.clean()
		>>> len(ql._list)
		5
		"""
		deleted_count = 0
		for i in range(len(self._list)):
			elem = self._list[i]
			if elem == _marked_to_delete:
				deleted_count += 1
			else:
				self._list[i - deleted_count] = elem
		for i in range(deleted_count):
			del self._list[len(self._list)-1]
		assert deleted_count == len(self._deleted_items)
		self._deleted_items.clear()
	
	def _offset_index(self, index):
		"""
		O(log(d)^2))
		>>> ql = QuickList('abcdefgh', 1)
		>>> ql._offset_index(5)
		5
		>>> del ql[0]
		>>> ql._offset_index(5)
		6
		>>> del ql[4]
		>>> ql._offset_index(5)
		7
		>>> ql._offset_index(0)
		1
		"""
		# do a heuristic binary search
		left_bound = index
		right_bound = index + len(self._deleted_items)
		while right_bound != left_bound:
			holes_left_of_left_bound = self._deleted_items.count_le(left_bound)
			holes_left_of_right_bound = self._deleted_items.count_le(right_bound)

			# get the density of holes between the bounds
			num_holes = holes_left_of_right_bound - holes_left_of_left_bound
			hole_density = num_holes / (right_bound - left_bound)

			guess = left_bound + int(holes_left_of_left_bound * (1 /(1 - hole_density)))
			holes_left_of_guess = self._deleted_items.count_le(guess)

			if holes_left_of_guess == guess - index:
				return guess
			elif holes_left_of_guess > guess - index:
				left_bound = guess
			else:
				right_bound = guess
		return left_bound

class Deletree(Container, Sized):
	"""
	>>> d = Deletree()
	>>> d.add(5)
	>>> d.add(3)
	>>> d.add(7)
	>>> d.add(0)
	>>> 3 in d
	True
	>>> 5 in d
	True
	>>> 7 in d
	True
	>>> 6 in d
	False
	>>> 0 in d
	True
	>>> len(d)
	4
	>>> d.count_le(8)
	4
	>>> d.count_le(5)
	3
	>>> d.count_le(2)
	1
	"""
	# TODO make tree self balancing
	def __init__(self):
		self.root = None
	
	def add(self, value):
		"""
		O(log(d))
		"""
		if self.root == None:
			self.root = Deletree.Node(value)
		else:
			self.root.addNode(value)
	
	def clear(self):
		self.root = None

	def __contains__(self, value):
		"""
		O(log(d))
		"""
		if self.root == None:
			return False
		else:
			return value in self.root

	def __len__(self):
		"""
		O(1)
		"""
		if self.root == None:
			return 0
		else:
			return len(self.root)

	def count_le(self, value):
		""" Return the count of values <= value 
		O(log(d))
		"""
		if self.root == None:
			return 0
		else:
			return self.root.count_le(value)

	class Node(Container, Sized):
		def __init__(self, value):
			self.value = value
			self.left = None
			self.right = None
			self.leftCount = 0
			self.rightCount = 0

		def __len__(self):
			return self.leftCount + 1 + self.rightCount

		def count_le(self, value):
			""" Return the count of values <= value
			"""
			if value == self.value:
				if self.left == None:
					return 1
				else:
					return self.leftCount + 1
			elif value < self.value:
				if self.left == None:
					return 0
				else:
					return self.left.count_le(value)
			else:
				if self.right == None:
					return 1 + self.leftCount
				else:
					return self.leftCount + 1 + self.right.count_le(value)

		def addNode(self, value):
			if value < self.value:
				if self.left == None:
					self.left = Deletree.Node(value)
				else:
					self.left.addNode(value)
				self.leftCount += 1
			elif value > self.value:
				if self.right == None:
					self.right = Deletree.Node(value)
				else:
					self.right.addNode(value)
				self.rightCount += 1
			else:
				raise ValueError

		def __contains__(self, value):
			if self.value == value:
				return True
			elif value < self.value:
				if self.left == None:
					return False
				else:
					return self.left.__contains__(value)
			else:
				if self.right == None:
					return False
				else:
					return self.right.__contains__(value)
