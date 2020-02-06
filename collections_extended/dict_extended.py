from collections.abc import MutableMapping
from typing import Any, Iterable

from .sentinel import NOT_SET

# * MultiDict
# * Ordered / Indexed
# * frozen
# * bijection

class DictExtended(MutableMapping):

	__slots__ = ('_data', )

	def __init__(self, iterable: Iterable, default: Any = NOT_SET, **kwargs):
		self._data = {}
		self.default = default
		self.update(iterable, **kwargs)

	def _default_value(self):
		try:
			return self.default()
		except TypeError:
			# default is not Callable
			return self.default

	def __len__(self):
		return len(self._data)

	def __getitem__(self, key):
		try:
			return self._data[key]
		except KeyError:
			if self.default is NOT_SET:
				raise
			else:
				return  elf._default_value()

	def __setitem__(self, key, value):
		self._data[key] = value

	def __delitem__(self, key):
		del self._data[key]

	def __contains__(self, key):
		return key in self._data

	def get(self, key, default=None):
		try:
			return self._data[key]
		except KeyError:
			return default

	def pop(self, key, default=NOT_SET):
		raise NotImplementedError

	def popitem(self):
		raise NotImplementedError

	def clear(self):
		self._data.clear()

	def update(self, other=None, /, **kwargs):
		raise NotImplementedError

	def setdefault(self, key, default=None):
		raise NotImplementedError

	def keys(self):
		return self._data.keys()
	
	def items(self):
		return self._data.items()

	def values(self):
		return self._data.values()

	def __eq__(self, other):
		raise NotImplementedError
