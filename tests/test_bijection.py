"""Test bijection class."""
import pytest

from collections_extended.bijection import bijection


def test_bijection():
    """General tests for bijection."""
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


def test_init_from_pairs():
    assert bijection({'a': 1, 'b': 2}) == bijection((('a', 1), ('b', 2)))


def test_repr():
    """Test __repr__."""
    b = bijection()
    assert b == eval(b.__repr__())
    b = bijection({'a': 1, 'b': 2, 'c': 3})
    assert b == eval(b.__repr__())
    assert repr(bijection({'a': 1})) == "bijection({'a': 1})"


def test_setting_value():
    """Test that setting an existing value removes that key."""
    b = bijection()
    b['a'] = 1
    b['b'] = 1
    assert 'a' not in b
    assert 'b' in b
    assert 1 in b.values()


def test_iter():
    b = bijection({'a': 1, 'b': 2, 'c': 3})
    assert set(b) == {'a', 'b', 'c'}


def test_clear():
    b = bijection({'a': 1, 'b': 2, 'c': 3})
    assert b.keys()
    assert b.values()
    assert b
    b.clear()
    assert not b
    assert not b.keys()
    assert not b.values()
