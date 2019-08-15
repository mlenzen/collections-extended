"""collections_extended contains a few extra basic data structures."""
from typing import Any, Optional, Iterable

from ._compat import Collection
from .bags import bag, frozenbag, CountsView, UniqueElementsView
from .setlists import setlist, frozensetlist
from .bijection import bijection
from .range_map import RangeMap, MappedRange
from .indexed_dict import IndexedDict
from ._version import __version__

__all__ = (
	'collection',
	'setlist',
	'frozensetlist',
	'bag',
	'frozenbag',
	'CountsView',
	'UniqueElementsView',
	'bijection',
	'RangeMap',
	'MappedRange',
	'Collection',
	'IndexedDict',
	'__version__',
	)


def collection(
	iterable: Optional[Iterable[Any]] = ...,
	mutable: bool = ...,
	ordered: bool = ...,
	unique: bool = ...,
) -> Collection:
	"""Return a :class:`Collection` with the specified properties.

	Args:
		iterable: collection to instantiate new collection from.
		mutable: Whether or not the new collection is mutable.
		ordered: Whether or not the new collection is ordered.
		unique: Whether or not the new collection contains only unique values.
	"""
	if iterable is None:
		iterable = tuple()
	if unique:
		if ordered:
			if mutable:
				return setlist(iterable)
			else:
				return frozensetlist(iterable)
		else:
			if mutable:
				return set(iterable)
			else:
				return frozenset(iterable)
	else:
		if ordered:
			if mutable:
				return list(iterable)
			else:
				return tuple(iterable)
		else:
			if mutable:
				return bag(iterable)
			else:
				return frozenbag(iterable)
