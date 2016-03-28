import pytest

from collections_extended import SortedList


def test_init():
	assert SortedList('cba') == SortedList('abc')


def test_key():
	sl = SortedList([1, 2, 3])
	sl.key = lambda i: -i
	assert sl[0] == 3
	assert sl[1] == 2
	assert sl[2] == 1


def test_reverse():
	sl = SortedList([1, 2, 3])
	sl.reversed = True
	assert sl[0] == 3
	assert sl[1] == 2
	assert sl[2] == 1


def test_str():
	assert str(SortedList()) == '[]'
	assert str(SortedList([1])) == '[1]'
	assert str(SortedList([1, 2])) == '[1, 2]'


def test_repr():
	for sl in [
		SortedList(),
		SortedList([1]),
		SortedList(range(10)),
		]:
		assert sl == eval(repr(sl))

def test_count():
	sl = SortedList([1, 2, 2, 3, 3, 4, 2])
	print(sl._keys)
	assert sl.count(1) == 1
	assert sl.count(2) == 3
	assert sl.count(3) == 2
	assert sl.count(4) == 1
	assert sl.count(5) == 0
	sl = SortedList([1, 2, 4, 2], key=lambda i: i % 2)
	assert sl.count(2) == 2
