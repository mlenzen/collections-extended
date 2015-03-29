
from datetime import date

import pytest

from collections_extended._compat import is_py2
from collections_extended.range_map import RangeMap


def test_simple_set():
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
	rm = RangeMap()
	rm.set('a', start=1)
	rm.set('b', start=2)
	assert rm == RangeMap({1: 'a', 2: 'b'})


def test_set_closed_interval_end():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('c', start=3, stop=4)
	assert rm[1] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'c'
	assert rm[4] == 'b'


def test_set_existing_interval():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('c', start=1, stop=2)
	print(rm)
	assert rm[1] == 'c'
	assert rm[2] == 'b'
	assert rm[3] == 'b'
	with pytest.raises(KeyError):
		rm[0]


def test_break_up_existing_open_end_interval():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('d', start=2, stop=2.5)
	assert rm[1] == 'a'
	assert rm[2] == 'd'
	assert rm[2.5] == 'b'
	assert rm[3] == 'b'


def test_break_up_existing_internal_interval():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('d', start=1, stop=1.5)
	assert rm[1] == 'd'
	assert rm[1.5] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'b'


def test_overwrite_multiple_internal():
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm.set('z', start=2, stop=5)
	assert rm[1] == 'a'
	assert rm[2] == 'z'
	assert rm[3] == 'z'
	assert rm[4] == 'z'
	assert rm[5] == 'e'


def test_overwrite_all():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm.set('z', start=0)
	with pytest.raises(KeyError):
		rm[-1]
	assert rm[0] == 'z'
	assert rm[1] == 'z'
	assert rm[2] == 'z'
	assert rm[3] == 'z'


def test_default_value():
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
	rm = RangeMap()
	rm.set('a')
	assert rm[1] == 'a'
	assert rm[-1] == 'a'


def test_set_beg():
	rm = RangeMap()
	rm.set('a', stop=4)
	with pytest.raises(KeyError):
		rm[4]
	assert rm[3] == 'a'


def test_alter_beg():
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
	rm = RangeMap()
	rm.set('b', date(1936, 12, 11))
	rm.set('a', date(1952, 2, 6))
	assert rm[date(1945, 1, 1)] == 'b'
	assert rm[date(1965, 4, 6)] == 'a'
	with pytest.raises(KeyError):
		rm[date(1900, 1, 1)]


def test_version_differences():
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
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	with pytest.raises(ValueError):
		rm[2:5:2]
	with pytest.raises(ValueError):
		rm[3] = 'z'
	with pytest.raises(ValueError):
		rm[3:5:2] = 'z'


def test_delete():
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z')
	rm.delete(stop=1)
	assert rm == RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm.delete(start=2, stop=4)
	assert rm == RangeMap.from_iterable(((1, 2, 'a'), (4, 5, 'd'), (5, None, 'e')))
	rm.delete(start=5)
	assert rm == RangeMap.from_iterable(((1, 2, 'a'), (4, 5, 'd')))


def test_str():
	assert str(RangeMap()) == 'RangeMap()'
	assert str(RangeMap(default_value='a')) == "RangeMap((None, None): 'a')"
	assert str(RangeMap({1: 'b'})) == "RangeMap((1, None): 'b')"
	assert str(RangeMap({1: 'b'}, default_value='a')) == "RangeMap((None, 1): 'a', (1, None): 'b')"


def test_eq():
	assert RangeMap() == RangeMap()
	assert RangeMap({1: 'a'}) == RangeMap({1: 'a'})
	assert RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}) == RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	assert RangeMap(default_value='z') == RangeMap(default_value='z')
	assert RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z') == RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}, default_value='z')
	assert RangeMap() != RangeMap(default_value='z')
	assert RangeMap({1: 'a'}, default_value='z') != RangeMap({1: 'a'})
	assert RangeMap(default_value='z') != RangeMap(default_value='a')


def test_contains():
	assert 1 not in RangeMap()
	assert 1 in RangeMap(default_value=1)
	assert 1 in RangeMap({1: 'a'})
	assert 2 in RangeMap({1: 'a'})
	assert 0 not in RangeMap({1: 'a'})