from abc import ABCMeta, abstractmethod
from typing import (
	Any,
	Callable,
	Collection,
	Iterable,
	Generic,
	Tuple,
	TypeVar,
)

from .store import Store

T = TypeVar('T')


class MulSetView:
	"""Base class for MulSet views."""

	__metaclass__ = ABCMeta
	__slots__ = ('mulset', )

	def __init__(self, mulset: 'MulSet'):
		self.mulset = mulset

	def __repr__(self):
		return '{0.__class__.__name__}({0.mulset!r})'.format(self)

	def __len__(self):
		return len(self.mulset)

	@abstractmethod
	def __iter__(self):
		raise NotImplementedError

	@abstractmethod
	def __contains__(self, elem):
		raise NotImplementedError


def mulset_factory(
		mutable: bool = True,
		orderable: bool = False,
		unique: bool = False,
):
	raise NotImplementedError


def mulset(iterable: Iterable[T] = None, **kwargs):
	cls = mulset_factory(**kwargs)
	return cls(iterable)


# class MulSet(Generic[T], Collection):
class MulSet(Collection[T]):
	"""

	"""

	def __init__(self, iterable: Iterable[T]):
		self.store = Store(iterable)

	@abstractmethod
	def copy(self) -> 'MulSet[T]':
		raise NotImplementedError


class MutableMulSet(MulSet):
	pass
