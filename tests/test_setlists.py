
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
	with pytest.raises(ValueError):
		sl.index('g')
	with pytest.raises(ValueError):
		sl.index('a', start=1)
	with pytest.raises(ValueError):
		sl.index('f', end=5)
	with pytest.raises(ValueError):
		sl.index('f', end=-1)


def test_sub_index():
	sl = setlist('abcdef')
	assert sl.sub_index('ef') == 4
	with pytest.raises(ValueError):
		sl.sub_index('cb')
	with pytest.raises(ValueError):
		sl.sub_index('efg')
	with pytest.raises(TypeError):
		sl.sub_index(1)
	with pytest.raises(ValueError):
		sl.sub_index('ef', end=5)
	with pytest.raises(ValueError):
		sl.sub_index('ab', start=1)


def test_setlist():
	sl = setlist('abcde')
	sl[0] = 5
	assert sl == setlist((5, 'b', 'c', 'd', 'e'))
	sl[-1] = 0
	assert sl == setlist((5, 'b', 'c', 'd', 0))
	with pytest.raises(ValueError):
		sl[1] = 'c'
	assert sl == setlist((5, 'b', 'c', 'd', 0))
	with pytest.raises(ValueError):
		sl.append('c')
	assert sl == setlist((5, 'b', 'c', 'd', 0))
	sl[2] == 'c'
	assert sl == setlist((5, 'b', 'c', 'd', 0))
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
	assert sl == setlist(('befg'))


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


def test_shuffle():
	sl = setlist(range(100))
	sl.shuffle()
	assert sl != setlist(range(100))


def test_del():
	sl = setlist('abcde')
	del sl[1]
	assert sl == setlist('acde')
	del sl[0]
	assert sl == setlist('cde')
	del sl[2]
	assert sl == setlist('cd')
	with pytest.raises(IndexError):
		del sl[2]
	with pytest.raises(IndexError):
		del sl[-3]
