
import pytest
import random

from collections_extended.setlists import _basesetlist, setlist, frozensetlist


def test_count():
	sl = setlist('abcdea')
	assert sl.count('a') == 1
	assert sl.count('f') == 0


def test_index():
	sl = setlist('abcdef')
	assert sl.index('a') == 0
	assert sl.index('f') == 5


def test_sub_index():
	sl = setlist('abcdef')
	assert sl.sub_index('ef') == 4
	with pytest.raises(ValueError):
		sl.sub_index('cb')


def test_setlist():
	sl = setlist('abcde')
	sl[0] = 5
	assert sl == setlist((5, 'b', 'c', 'd', 'e'))
	sl[-1] = 0
	assert sl == setlist((5, 'b', 'c', 'd', 0))
	sl[1] = 'c'
	assert sl == setlist((5, 'b', 'c', 'd', 0))
	del sl[0]
	assert sl == setlist(('b', 'c', 'd', 0))
	del sl[-1]
	assert sl == setlist(('b', 'c', 'd'))
	assert sl.pop() == 'd'
	assert sl.pop(0) == 'b'
	assert sl == setlist(('c',))
	sl.insert(0, 'a')
	assert sl == setlist(('a', 'c'))
	sl.insert(len(sl), 'e')
	assert sl == setlist(('a', 'c', 'e'))
	sl.append('f')
	assert sl == setlist(('a', 'c', 'e', 'f'))
	sl += ('g', 'h')
	assert sl == setlist(('a', 'c', 'e', 'f', 'g', 'h'))


def test_removeall():
	sl = setlist('abcdefgh')
	sl.remove_all(set('acdh'))
	assert sl == setlist(('b', 'e', 'f', 'g'))


def test_assignment():
	sl = setlist('abc')
	sl[0] = 'd'
	assert sl == setlist('dbc')
	sl[1] = 'e'
	assert sl == setlist('dec')
	sl[2] = 'f'
	assert sl == setlist('def')
	with pytest.raises(IndexError):
		sl[3] = 'g'
	sl[0], sl[1] = 'h', 'i'
	assert sl == setlist('hif')


def test_len():
	assert len(setlist()) == 0
	assert len(setlist('a')) == 1
	assert len(setlist('ab')) == 2
	assert len(setlist('abc')) == 3
