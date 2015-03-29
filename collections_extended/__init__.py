'''collections_extended contains a few extra basic data structures'''

__version__ = '0.4.0'

from .bags import bag, frozenbag
from .setlists import setlist, frozensetlist
from .bijection import bijection
from .range_map import RangeMap, MappedRange

__all__ = ['collection', 'setlist', 'frozensetlist', 'bag', 'frozenbag', 'bijection', 'RangeMap', 'MappedRange']


def collection(it=(), mutable=True, ordered=False, unique=False):
	""" Return a Collection with the specified properties.

	"""
	if unique:
		if ordered:
			if mutable:
				return setlist(it)
			else:
				return frozensetlist(it)
		else:
			if mutable:
				return set(it)
			else:
				return frozenset(it)
	else:
		if ordered:
			if mutable:
				return list(it)
			else:
				return tuple(it)
		else:
			if mutable:
				return bag(it)
			else:
				return frozenbag(it)
