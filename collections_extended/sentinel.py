"""Sentinel class."""

__all__ = ('Sentinel', 'NOT_SET')

from typing import Any, Dict, Tuple


class Sentinel:
	"""A class to create sentinel objects.

	The benefits vs. object() are a good repr it is picklable.

	Inspired by https://pypi.org/project/sentinels/
	"""

	_registry: Dict[str, 'Sentinel'] = {}

	def __getnewargs__(self) -> Tuple[str]:
		return self._name,

	def __new__(cls, _name: str):
		"""Find the Sentinel object with name or create a new one."""
		try:
			return cls._registry[_name]
		except KeyError:
			new = super(Sentinel, cls).__new__(cls)
			cls._registry[_name] = new
			return new

	def __init__(self, name: str):
		super(Sentinel, self).__init__()
		self._name = name

	def __repr__(self):
		return '<%s>' % self._name

	def __bool__(self):
		return False

	def __eq__(self, other: Any):
		if other.__class__ == self.__class__:
			return self._name == other._name
		return False


NOT_SET = Sentinel('not_set')
