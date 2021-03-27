from typing import Collection, TypeVar, Iterable, Dict, List

T = TypeVar('T')


def list_set_value_count(l: List[T], val: T, count: int) -> int:
	"""Ensure there are exactly count of val in l.

	Returns:
		The count of values added (or removed).
	"""
	# TODO this is a naive implementation
	old_count = l.count(val)
	diff = count - old_count
	if diff > 0:
		for _ in range(diff):
			l.append(val)
	elif diff < 0:
		for _ in range(-diff):
			l.remove(val)


def dict_set_value_count(d: Dict[T, int], val: T, count: int) -> int:
	"""

	Raises:
		TypeError if val isn't hashable
	"""
	# This first lin will raise the TypeError we need when val isn't hashable
	old_count = d.get(val, 0)
	if count == 0:
		del d[val]
	else:
		d[val] = count
	return count - old_count


class Store(Collection[T]):

	def __init__(self, values: Iterable[T] = None):
		self._list: List[T] = []
		self._dict: Dict[T, int] = {}
		self._size = 0
		if values:
			for value in values:
				self.increment_count(value)

	# def __repr__(self):
	# 	return f'Store()'

	def set_count(self, value: T, count: int):
		if count < 0:
			raise ValueError
		try:
			diff = dict_set_value_count(self._dict, value, count)
		except TypeError:
			diff = list_set_value_count(self._list, value, count)
		self._size += diff
		return diff

	def increment_count(self, value: T, count: int = 1):
		# TODO this is implemented poorly (2x list lokups)
		self.set_count(value, self.count(value) + count)

	def count(self, value: T) -> int:
		try:
			return self._dict.get(value, 0)
		except TypeError:
			return self._list.count(value)

	def copy(self) -> 'Store':
		s = Store()
		s._list = self._list.copy()
		s._dict = self._dict.copy()
		s._size = self._size

	def __len__(self) -> int:
		"""Return the cardinality of the bag.

		This runs in O(1)
		"""
		return self._size

	# implementing Container methods

	def __contains__(self, value: T) -> bool:
		"""Return the multiplicity of the element.

		This runs in O(1)
		"""
		return self.count(value) > 0

	# implementing Iterable methods

	def __iter__(self):
		"""Iterate through all elements.

		Multiple copies will be returned if they exist.
		"""
		for value, count in self._dict.items():
			for _ in range(count):
				yield value
		yield from self._list

