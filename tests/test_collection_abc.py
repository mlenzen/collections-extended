import pytest

from collections_extended import (
    setlist,
    frozensetlist,
    bag,
    frozenbag,
    bijection,
    RangeMap,
    Collection,
)


@pytest.mark.parametrize(
    "klass",
    [
        setlist,
        frozensetlist,
        bag,
        frozenbag,
        bijection,
        RangeMap,
        list,
        tuple,
        set,
        frozenset,
        dict,
    ],
)
def test_subclass(klass):
    """Test that all appropriate collections are subclasses of Collection."""
    assert issubclass(klass, Collection)
