
import pytest

from collections_extended.range_map import RangeMap


def test_simple_set():
	rm = RangeMap()
	rm[1:] = 'a'
	assert rm[1] == 'a'
	assert rm[2] == 'a'
	with pytest.raises(KeyError):
		rm[0]
	rm[2:] = 'b'
	assert rm[1] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'b'


def test_closed():
	rm = RangeMap()
	rm[1:2] = 'a'
	assert rm[1] == 'a'
	assert rm[1.9] == 'a'
	with pytest.raises(KeyError):
		rm[2]
	with pytest.raises(KeyError):
		rm[0]


def test_from_mapping():
	rm = RangeMap()
	rm[1:] = 'a'
	rm[2:] = 'b'
	assert rm == RangeMap({1: 'a', 2: 'b'})


def test_set_closed_interval_end():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm[3:4] = 'c'
	assert rm[1] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'c'
	assert rm[4] == 'b'


def test_set_existing_interval():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm[1:2] = 'c'
	assert rm[1] == 'c'
	assert rm[2] == 'b'
	assert rm[3] == 'b'
	with pytest.raises(KeyError):
		rm[0]


def test_break_up_existing_open_end_interval():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm[2:2.5] = 'd'
	assert rm[1] == 'a'
	assert rm[2] == 'd'
	assert rm[2.5] == 'b'
	assert rm[3] == 'b'


def test_break_up_existing_internal_interval():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm[1:1.5] = 'd'
	assert rm[1] == 'd'
	assert rm[1.5] == 'a'
	assert rm[2] == 'b'
	assert rm[3] == 'b'


def test_overwrite_multiple_internal():
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm[2:5] = 'z'
	assert rm[1] == 'a'
	assert rm[2] == 'z'
	assert rm[3] == 'z'
	assert rm[4] == 'z'
	assert rm[5] == 'e'


def test_overwrite_all():
	rm = RangeMap({1: 'a', 2: 'b'})
	rm[0:] = 'z'
	with pytest.raises(KeyError):
		rm[-1]
	assert rm[0] == 'z'
	assert rm[1] == 'z'
	assert rm[2] == 'z'
	assert rm[3] == 'z'


def test_default_value():
	rm = RangeMap(default_value=None)
	assert rm[1] is None
	assert rm[-2] is None
	rm[1:] = 'a'
	assert rm[0] is None
	assert rm[1] == 'a'
	assert rm[2] == 'a'


def test_whole_range():
	rm = RangeMap()
	rm[:] = 'a'
	assert rm[1] == 'a'
	assert rm[-1] == 'a'


def test_set_beg():
	rm = RangeMap()
	rm[:4] = 'a'
	with pytest.raises(KeyError):
		rm[4]
	assert rm[3] == 'a'


def test_alter_beg():
	rm = RangeMap({1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'})
	rm[:3] = 'z'
	assert rm[0] == 'z'
	assert rm[1] == 'z'
	assert rm[2] == 'z'
	assert rm[3] == 'c'
	assert rm[4] == 'd'
	assert rm[5] == 'e'
