"""collections_extended contains a few extra basic data structures."""
from collections.abc import Iterable

from ._compat import Collection
from .bags import Bag, CountsView, UniqueElementsView, bag, frozenbag
from .bijection import bijection
from .indexed_dict import IndexedDict
from .range_map import MappedRange, RangeMap
from .setlists import SetList, frozensetlist, setlist

__all__ = (
	'Collection',
	'Bag',
	'bag',
	'frozenbag',
	'bijection',
	'IndexedDict',
	'RangeMap',
	'SetList',
	'frozensetlist',
	'setlist',
	)


def collection(
		iterable: Iterable = None,
		mutable=True,
		ordered=False,
		unique=False,
		) -> Collection:
	"""Return a :class:`Collection` with the specified properties.

	Args:
		iterable (Iterable): collection to instantiate new collection from.
		mutable (bool): Whether or not the new collection is mutable.
		ordered (bool): Whether or not the new collection is ordered.
		unique (bool): Whether or not the new collection contains only unique values.
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
