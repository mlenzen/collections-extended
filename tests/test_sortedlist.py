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
	sl.reverse = True
	assert sl[0] == 3
	assert sl[1] == 2
	assert sl[2] == 1
