"""Test for collections_extended factory."""

from collections_extended import (
	collection,
	bag,
	setlist,
	frozenbag,
	frozensetlist,
	)


def test_collection_factory():
	"""Test collection factory."""
	assert type(collection()) == bag
	assert type(collection(ordered=True)) == list
	assert type(collection(unique=True)) == set
	assert type(collection(unique=True, ordered=True)) == setlist
	assert type(collection(mutable=False)) == frozenbag
	assert type(collection(mutable=False, ordered=True)) == tuple
	assert type(collection(mutable=False, unique=True)) == frozenset
	assert (
		type(collection(mutable=False, unique=True, ordered=True)) ==
		frozensetlist
		)
