"""Python version compatibility helpers."""
import sys

from ._util import Sentinel

__all__ = ('Collection', )

if sys.version_info < (3, 6):
	from abc import ABCMeta
	from collections.abc import Sized, Iterable, Container

	def _check_methods(klass, *methods):
		_missing = Sentinel('missing')
		for method in methods:
			for superclass in klass.__mro__:
				implementation = superclass.__dict__.get(method, _missing)
				if implementation is _missing:
					continue
				elif implementation is None:
					return NotImplemented
				else:
					break
		return True

	class Collection(Sized, Iterable, Container, metaclass=ABCMeta):
		"""Backport from Python3.6+."""

		__slots__ = tuple()

		@classmethod
		def __subclasshook__(cls, klass):
			if cls is not Collection:
				return NotImplemented
			return _check_methods(klass, "__len__", "__iter__", "__contains__")

else:
	from collections.abc import Collection
