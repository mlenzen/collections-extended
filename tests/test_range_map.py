"""Tests for RangeMap class."""
import datetime

# from hypothesis import given
# from hypothesis.strategies import integers
import pytest

from collections_extended.range_map import RangeMap, MappedRange


def print_underlying(rm):
	print(rm._keys, rm._values)


def test_simple_set():
	"""Test set."""
	rm = RangeMap()
	rm.set('a', start=1)
	print_underlying(rm)
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
	print_underlying(rm)
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
	print_underlying(rm)
	assert rm[1] == 'c'
	assert rm[2] == 'b'
	assert rm[3] == 'b'
	assert rm == RangeMap({1: 'c', 2: 'b'})
	with pytest.raises(KeyError):
		rm[0]


def test_set_consecutive_before_eq():
	"""Test setting consecutive ranges to the same value."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c'})
	print_underlying(rm)
	rm.set('b', 1, 2)
	print_underlying(rm)
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
	rm[3:] = 'a'
	assert rm == RangeMap({1: 'a', 2: 'b', 3: 'a'})
	del rm[1:2]
	assert rm == RangeMap({2: 'b', 3: 'a'})


def test_slice_errors():
	"""Test slicing errors."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	with pytest.raises(ValueError):
		rm[2:5:2]
	with pytest.raises(TypeError):
		rm[3] = 'z'
	with pytest.raises(ValueError):
		rm[3:5:2] = 'z'


def test_bool():
	assert not bool(RangeMap())
	assert bool(RangeMap(default_value='a'))
	assert bool(RangeMap({1: 1}))
	assert bool(RangeMap([(1, 2, 3)]))


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

	rm = RangeMap({1: 'a', 2: 'b', 3: 'c'})
	rm.delete(2, 3)
	assert rm == RangeMap([(1, 2, 'a'), (3, None, 'c')])
	print(repr(rm))
	with pytest.raises(KeyError):
		rm.delete(2, 3)
	with pytest.raises(KeyError):
		rm.delete(0, 2)
	with pytest.raises(KeyError):
		rm.delete(2.5, 3.5)


def test_delitem_beginning():
	"""Test RangeMap.__delitem__ at the beginning."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
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
	print_underlying(rm)
	assert str(rm) == "RangeMap((None, None): a)"
	assert str(RangeMap({1: 'b'})) == "RangeMap((1, None): b)"
	assert (
		str(RangeMap({1: 'b'}, default_value='a')) ==
		"RangeMap((None, 1): a, (1, None): b)"
		)


def test_empty():
	"""Test RangeMap.empty."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd'})
	rm.empty(2, 3)
	rm.empty(2, 3)
	assert rm == RangeMap.from_iterable((
		(1, 2, 'a'),
		(3, 4, 'c'),
		(4, None, 'd'),
		))
	rm.empty(3.5, 4.5)
	assert rm == RangeMap.from_iterable((
		(1, 2, 'a'),
		(3, 3.5, 'c'),
		(4.5, None, 'd'),
		))


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
	rm = RangeMap([(1, 2, 'a'), (3, 4, 'b')])
	assert 0 not in rm
	assert 1 in rm
	assert 2 not in rm
	assert 3 in rm
	assert 4 not in rm


def test_get_range():
	"""Test get_range."""
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z')
	print_underlying(rm)
	print_underlying(rm.get_range(1, 3))
	print_underlying(RangeMap.from_iterable(((1, 2, 'a'), (2, 3, 'b'))))
	assert (
		rm.get_range(1, 3) ==
		RangeMap.from_iterable(((1, 2, 'a'), (2, 3, 'b')))
		)
	assert (
		rm.get_range(1.5, 3) ==
		RangeMap.from_iterable(((1.5, 2, 'a'), (2, 3, 'b')))
		)
	print_underlying(rm.get_range(start=3))
	assert rm.get_range(start=3) == RangeMap({3: 'c', 4: 'd', 5: 'e'})
	assert (
		rm.get_range(stop=3) ==
		RangeMap.from_iterable(((None, 1, 'z'), (1, 2, 'a'), (2, 3, 'b')))
		)
	assert rm[2:3] == rm.get_range(2, 3)


def test_start_gt_stop():
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z')
	with pytest.raises(ValueError):
		rm.set('a', start=3, stop=2)
	with pytest.raises(ValueError):
		rm.get_range(start=3, stop=2)


def test_init():
	assert RangeMap(iterable=[]) == RangeMap()
	rm = RangeMap(((1, 2, 'a'), (2, None, 'b')))
	assert RangeMap.from_mapping({1: 'a', 2: 'b'}) == rm
	with pytest.raises(TypeError):
		RangeMap(foo='bar')


def test_len():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert len(rm) == 3
	assert len(RangeMap(default_value='a')) == 1
	assert len(RangeMap()) == 0
	assert len(RangeMap(default_value=None)) == 1


def test_keys():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert rm.keys() == set((1, 4, 5))
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		))
	assert rm.keys() == set((1, 4))
	assert RangeMap().keys() == set()
	assert RangeMap(default_value='a').keys() == set((None,))
	assert RangeMap(default_value=None).keys() == set((None, ))


def test_values():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert list(rm.values()) == ['a', 'd', 'e']
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		))
	assert list(rm.values()) == ['a', 'd']
	assert list(RangeMap().values()) == []
	assert list(RangeMap(default_value='a').values()) == ['a']
	assert list(RangeMap(default_value=None).values()) == [None]


def test_items():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert rm.items() == set(((1, 'a'), (4, 'd'), (5, 'e')))
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		))
	assert rm.items() == set(((1, 'a'), (4, 'd')))
	assert RangeMap().items() == set()
	assert RangeMap(default_value='a').items() == set(((None, 'a'),))
	assert RangeMap(default_value=None).items() == set(((None, None), ))


def test_iter():
	assert list(RangeMap()) == []
	assert list(RangeMap(default_value='a')) == [None]
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert list(rm) == [1, 4, 5]
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		))
	assert list(rm) == [1, 4]


def test_key_view_contains():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert 1 in rm.keys()
	assert 2 not in rm.keys()
	assert 1.5 in rm.keys()


def test_items_view_contains():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert (1, 'a') in rm.items()
	assert (2, 'a') not in rm.items()


def test_values_view_contains():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert 'a' in rm.values()
	assert 'b' not in rm.values()


def test_get():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	assert rm.get(1) == 'a'
	assert rm.get(1.5) == 'a'
	assert rm.get(2) is None


def test_clear():
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'd'),
		(5, None, 'e'),
		))
	rm.clear()
	assert rm == RangeMap()


def test_start():
	assert RangeMap().start is None
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'b'),
		))
	assert rm.start == 1
	rm = RangeMap.from_iterable((
		(None, 2, 'a'),
		(4, 5, 'b'),
		))
	assert rm.start is None


def test_end():
	assert RangeMap().end is None
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, 5, 'b'),
		))
	assert rm.end == 5
	rm = RangeMap.from_iterable((
		(1, 2, 'a'),
		(4, None, 'b'),
		))
	assert rm.end is None


class TestMappedRange:

	def test_str(self):
		mr = MappedRange(0, 1, 'a')
		assert str(mr) == "[0, 1) -> 'a'"

	def test_repr(self):
		mr = MappedRange(0, 1, 'a')
		assert repr(mr) == "MappedRange(0, 1, 'a')"

	def test_unpack(self):
		mr = MappedRange(0, 1, 'a')
		v1, v2, v3 = mr
		assert v1 == 0
		assert v2 == 1
		assert v3 == 'a'

	def test_equality(self):
		assert MappedRange(0, 1, 'a') == MappedRange(0, 1, 'a')
		assert not MappedRange(0, 1, 'a') is MappedRange(0, 1, 'a')
		assert MappedRange(0, 1, 'a') != MappedRange(None, 1, 'a')
