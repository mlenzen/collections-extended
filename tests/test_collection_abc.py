from collections_extended import (
	setlist,
	frozensetlist,
	bag,
	frozenbag,
	bijection,
	RangeMap,
	MappedRange,
	Collection,
	)


def test_subclass():
	"""Test that all appropriate collections are subclasses of Collection."""
	classes = (
		setlist,
		frozensetlist,
		bag,
		frozenbag,
		bijection,
		RangeMap,
		MappedRange,
		list,
		tuple,
		set,
		frozenset,
		dict,
		)
	for cls in classes:
		assert issubclass(cls, Collection)
