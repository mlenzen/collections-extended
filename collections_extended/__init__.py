"""collections_extended contains a few extra basic data structures."""
from typing import Any, Optional, Iterable

from ._compat import Collection
from .bags import bag, frozenbag
from .bijection import bijection
from .indexed_dict import IndexedDict
from .range_map import RangeMap
from .setlists import frozensetlist, setlist

__all__ = (
	'Collection',
	'bag',
	'frozenbag',
	'bijection',
	'IndexedDict',
	'RangeMap',
	'frozensetlist',
	'setlist',
	)


def collection(
		iterable: Optional[Iterable[Any]] = None,
		mutable: bool = True,
		ordered: bool = False,
		unique: bool = False,
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
