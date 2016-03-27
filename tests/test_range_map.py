"""Tests for RangeMap class."""
import datetime

# from hypothesis import given
# from hypothesis.strategies import integers
import pytest

from collections_extended._compat import is_py2
from collections_extended.range_map import RangeMap


def test_simple_set():
	"""Test set."""
	rm = RangeMap()
	rm.set('a', start=1)
	print(rm._ordered_keys, rm._key_mapping)
	assert rm[1] == 'a'
	assert rm[2] == 'a'
	with pytest.raises(KeyError):
		rm[0]
	rm.set('b', start=2)
	assert rm[1] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'b'


def test_closed():
	"""Test a closed RangeMap."""
	rm = RangeMap()
	rm.set('a', start=1, stop=2)
	print(rm._ordered_keys, rm._key_mapping)
	assert rm[1] == 'a'
	assert rm[1.9] == 'a'
	with pytest.raises(KeyError):
		rm[2]
	with pytest.raises(KeyError):
		rm[0]


def test_from_mapping():
	"""Test creating a RangeMap from a mapping."""
	rm = RangeMap()
	rm.set('a', start=1)
	rm.set('b', start=2)
	assert rm == RangeMap({1: 'a', 2: 'b'})


def test_set_closed_interval_end():
	"""Test setting a closed range on the end."""
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('c', start=3, stop=4)
	assert rm[1] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'c'
	assert rm[4] == 'b'


def test_set_existing_interval():
	"""Test setting an exact existing range."""
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('c', start=1, stop=2)
	print(rm)
	assert rm[1] == 'c'
	assert rm[2] == 'b'
	assert rm[3] == 'b'
	assert rm == RangeMap({1: 'c', 2: 'b'})
	with pytest.raises(KeyError):
		rm[0]


def test_set_consecutive_before_eq():
	"""Test setting consecutive ranges to the same value."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c'})
	print(rm._ordered_keys, rm._key_mapping)
	rm.set('b', 1, 2)
	print(rm._ordered_keys, rm._key_mapping)
	assert rm == RangeMap({1: 'b', 3: 'c'})


def test_set_consecutive_after_eq():
	"""Test setting consecutive ranges to the same value."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c'})
	rm.set('a', 2, 3)
	assert rm == RangeMap({1: 'a', 3: 'c'})


def test_set_consecutive_between_eq():
	"""Test setting consecutive ranges to the same value."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'b'})
	rm.set('b', 3, 4)
	assert rm == RangeMap({1: 'a', 2: 'b'})


def test_break_up_existing_open_end_interval():
	"""Test breaking up an existing open interval at the end."""
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('d', start=2, stop=2.5)
	assert rm[1] == 'a'
	assert rm[2] == 'd'
	assert rm[2.5] == 'b'
	assert rm[3] == 'b'


def test_break_up_existing_internal_interval():
	"""Test breaking up an existing interval."""
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('d', start=1, stop=1.5)
	assert rm[1] == 'd'
	assert rm[1.5] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'b'


def test_overwrite_multiple_internal():
	"""Test overwriting multiple adjoining intervals."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm.set('z', start=2, stop=5)
	assert rm[1] == 'a'
	assert rm[2] == 'z'
	assert rm[3] == 'z'
	assert rm[4] == 'z'
	assert rm[5] == 'e'


def test_overwrite_all():
	"""Test overwriting the entire mapping."""
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('z', start=0)
	with pytest.raises(KeyError):
		rm[-1]
	assert rm[0] == 'z'
	assert rm[1] == 'z'
	assert rm[2] == 'z'
	assert rm[3] == 'z'


def test_default_value():
	"""Test setting just a default value."""
	rm = RangeMap(default_value=None)
	print(rm)
	assert rm[1] is None
	assert rm[-2] is None
	rm.set('a', start=1)
	print(rm)
	assert rm[0] is None
	assert rm[1] == 'a'
	assert rm[2] == 'a'


def test_whole_range():
	"""Test setting the whole range."""
	rm = RangeMap()
	rm.set('a')
	assert rm[1] == 'a'
	assert rm[-1] == 'a'


def test_set_beg():
	"""Test setting the beginning."""
	rm = RangeMap()
	rm.set('a', stop=4)
	with pytest.raises(KeyError):
		rm[4]
	assert rm[3] == 'a'


def test_alter_beg():
	"""Test altering the beginning."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm.set('z', stop=3)
	assert rm[0] == 'z'
	assert rm[1] == 'z'
	assert rm[2] == 'z'
	assert rm[3] == 'c'
	assert rm[4] == 'd'
	assert rm[5] == 'e'
	rm.set('y', stop=3)
	assert rm == RangeMap({3: 'c', 4: 'd', 5: 'e'}, default_value='y')


def test_dates():
	"""Test using dates."""
	rm = RangeMap()
	rm.set('b', datetime.date(1936, 12, 11))
	rm.set('a', datetime.date(1952, 2, 6))
	assert rm[datetime.date(1945, 1, 1)] == 'b'
	assert rm[datetime.date(1965, 4, 6)] == 'a'
	with pytest.raises(KeyError):
		rm[datetime.date(1900, 1, 1)]


def test_version_differences():
	"""Test python 2 and 3 differences."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	if is_py2:
		with pytest.raises(SyntaxError):
			rm[3:] = 'a'
		with pytest.raises(SyntaxError):
			del rm[4:5]
		with pytest.raises(SyntaxError):
			assert rm[2:] == RangeMap({2: 'b', 3: 'a'})
	else:
		rm[3:] = 'a'
		assert rm == RangeMap({1: 'a', 2: 'b', 3: 'a'})


def test_slice_errors():
	"""Test slicing errors."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	with pytest.raises(ValueError):
		rm[2:5:2]
	with pytest.raises(ValueError):
		rm[3] = 'z'
	with pytest.raises(ValueError):
		rm[3:5:2] = 'z'


def test_delete():
	"""Test deleting."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z')
	rm.delete(stop=1)
	assert rm == RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm.delete(start=2, stop=4)
	assert rm == RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	rm.delete(start=5)
	assert rm == RangeMap.from_iterable(((1, 2, 'a'), (4, 5, 'd')))


def test_delitem_beginning():
	"""Test RangeMap.__delitem__ at the beginning."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	if not is_py2:
		with pytest.raises(ValueError):
			del rm[2]
		with pytest.raises(ValueError):
			del rm[2:4:2]
	rm.delete(1, 2)
	assert rm == RangeMap({2: 'b', 3: 'c', 4: 'd', 5: 'e'})


def test_delitem_consecutive():
	"""Test deleting consecutive ranges."""
	rm = RangeMap({2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm.delete(3, 4)
	rm.delete(4, 5)
	assert rm == RangeMap.from_iterable(((2, 3, 'b'), (5, None, 'e')))


def test_str():
	"""Test __str__."""
	assert str(RangeMap()) == 'RangeMap()'
	rm = RangeMap(default_value='a')
	print(rm._ordered_keys, rm._key_mapping)
	assert str(rm) == "RangeMap((None, None): a)"
	assert str(RangeMap({1: 'b'})) == "RangeMap((1, None): b)"
	assert (
		str(RangeMap({1: 'b'}, default_value='a')) ==
		"RangeMap((None, 1): a, (1, None): b)"
		)


def test_repr():
	test_objects = [
		RangeMap(),
		RangeMap(default_value='a'),
		RangeMap({1: 'a'}),
		RangeMap([(1, 2, 'a'), (2, 3, 'b')]),
		RangeMap([(1, 2, 'a'), (3, 4, 'b')]),
		RangeMap([
			(datetime.date(2015, 1, 1), datetime.date(2015, 1, 2), 'a'),
			(datetime.date(2015, 1, 2), datetime.date(2015, 1, 3), 'b'),
			]),
		]
	for obj in test_objects:
		assert eval(repr(obj)) == obj


def test_eq():
	"""Test __eq__."""
	assert RangeMap() == RangeMap()
	assert RangeMap({1: 'a'}) == RangeMap({1: 'a'})
	assert (
		RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}) ==
		RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
		)
	assert RangeMap(default_value='z') == RangeMap(default_value='z')
	assert (
		RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z') ==
		RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z')
		)
	assert RangeMap() != RangeMap(default_value='z')
	assert RangeMap({1: 'a'}, default_value='z') != RangeMap({1: 'a'})
	assert RangeMap(default_value='z') != RangeMap(default_value='a')
	assert not RangeMap() == dict()


def test_contains():
	"""Test __contains__."""
	assert 1 not in RangeMap()
	assert 1 in RangeMap(default_value=1)
	assert 1 in RangeMap({1: 'a'})
	assert 2 in RangeMap({1: 'a'})
	assert 0 not in RangeMap({1: 'a'})


def test_get_range():
	"""Test get_range."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z')
	assert (
		rm.get_range(1, 3) ==
		RangeMap.from_iterable(((1, 2, 'a'), (2, 3, 'b')))
		)
	assert (
		rm.get_range(1.5, 3) ==
		RangeMap.from_iterable(((1.5, 2, 'a'), (2, 3, 'b')))
		)
	print(rm.get_range(start=3)._key_mapping, rm.get_range(start=3)._ordered_keys)
	assert rm.get_range(start=3) == RangeMap({3: 'c', 4: 'd', 5: 'e'})
	assert (
		rm.get_range(stop=3) ==
		RangeMap.from_iterable(((None, 1, 'z'), (1, 2, 'a'), (2, 3, 'b')))
		)
	if is_py2:
		with pytest.raises(SyntaxError):
			rm[2:3]
	else:
		assert rm[2:3] == rm.get_range(2, 3)
