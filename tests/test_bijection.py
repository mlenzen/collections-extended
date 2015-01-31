
import pytest

from collections_extended.bijection import bijection


def test_bijection():
	b = bijection()
	assert len(b) == 0
	b['a'] = 1
	assert len(b) == 1
	assert b['a'] == 1
	assert b.inverse[1] == 'a'
	assert 'a' in b
	assert 1 not in b
	assert 1 in b.inverse
	with pytest.raises(KeyError):
		del b['f']
	assert b == bijection(a=1)
	assert b.inverse.inverse is b
	assert b == b.copy()
	del b['a']
	assert b == bijection()
	assert bijection(a=1, b=2, c=3) == bijection({'a': 1, 'b': 2, 'c': 3})
	b['a'] = 1
	b.inverse[1] = 'b'
	assert 'b' in b
	assert b['b'] == 1
	assert 'a' not in b
