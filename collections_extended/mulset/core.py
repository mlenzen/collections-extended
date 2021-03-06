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


# class MulSet(Generic[T], Collection):
class MulSet(Collection[T]):
	"""

	"""

	class __metaclass__:

		def __call__(
				self,
				iterable: Iterable[T] = None,
				mutable: bool = True,
				orderable: bool = False,
				unique: bool = False,
		) -> 'MulSet[T]':
			subclass = MulSet.factory(
				mutable=mutable,
				orderable=orderable,
				unique=unique,
			)
			return subclass(iterable)

	@classmethod
	def factory(
			cls,
			mutable: bool = True,
			orderable: bool = False,
			unique: bool = False,
	) -> 'MulSet[T]':
		# TODO implement if/then branching and/or subclasses
		pass

	@abstractmethod
	def __init__(self, iterable: Iterable[T]):
		pass

	@abstractmethod
	def copy(self) -> 'MulSet[T]':
		raise NotImplementedError


class TestMulSet:
	...


class MutableMulSet(MulSet):
	pass


class TestMutableMulSet:
	...
