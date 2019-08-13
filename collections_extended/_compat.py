"""Python 2/3 compatibility helpers."""
import sys

is_py2 = sys.version_info[0] == 2

__all__ = ('Collection', )


if sys.version_info < (3, 6):

	def _check_methods(C, *methods):
		mro = C.__mro__
		for method in methods:
			for B in mro:
				if method in B.__dict__:
					if B.__dict__[method] is None:
						return NotImplemented
					break
			else:
				return NotImplemented
		return True

	class Collection(Sized, Iterable, Container):
		"""Backport from Python3.6."""

		__slots__ = tuple()

		@classmethod
		def __subclasshook__(cls, C):
			if cls is Collection:
				return _check_methods(C, "__len__", "__iter__", "__contains__")
			return NotImplemented

else:
	from collections.abc import Collection
