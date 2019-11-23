"""Test for bag classes."""
from operator import concat, mul
import warnings

import pytest

from collections_extended.bags import _basebag, bag, frozenbag


def test_init():
	"""Test __init__."""
	b = _basebag('abracadabra')
	assert b.count('a') == 5
	assert b.count('b') == 2
	assert b.count('r') == 2
	assert b.count('c') == 1
	assert b.count('d') == 1
	b2 = bag(b)
	assert b2 == b


def test_repr():
	"""Test __repr__."""
	ms = _basebag()
	assert ms == eval(ms.__repr__())
	ms = _basebag('abracadabra')
	assert ms == eval(ms.__repr__())
	assert repr(bag('a')) == "bag(('a',))"


def test_str():
	"""Test __str__."""
	def compare_bag_string(b):
		s = str(b)
		assert s.startswith('{')
		assert s.endswith('}')
		return set(s[1:-1].split(', '))
	assert str(_basebag()) == '_basebag()'
	assert "'a'^5" in str(_basebag('abracadabra'))
	assert "'b'^2" in str(_basebag('abracadabra'))
	assert "'c'" in str(_basebag('abracadabra'))
	abra_elems = set(("'a'^5", "'b'^2", "'r'^2", "'c'", "'d'"))
	assert compare_bag_string(bag('abracadabra')) == abra_elems


def test_count():
	"""Test count."""
	ms = _basebag('abracadabra')
	assert ms.count('a') == 5
	assert ms.count('x') == 0


def test_nlargest():
	"""Test nlargest."""
	abra = _basebag('abracadabra')
	sort_key = lambda e: (-e[1], e[0])
	abra_counts = [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1)]
	assert sorted(abra.nlargest(), key=sort_key) == abra_counts
	assert sorted(abra.nlargest(3), key=sort_key) == abra_counts[:3]
	assert _basebag('abcaba').nlargest(3) == [('a', 3), ('b', 2), ('c', 1)]


def test_nlargest_deprecated():
	"""Test that nlargest raises a DeprecationWarning."""
	b = bag()
	with pytest.deprecated_call():
		b.nlargest()


def test_from_map():
	"""Test from_mapping."""
	assert _basebag.from_mapping({'a': 1, 'b': 2}) == _basebag('abb')
	assert _basebag.from_mapping({'a': 1, 'b': 2, 'c': 0}) == _basebag('abb')


def test_copy():
	"""Test copy."""
	b = _basebag()
	assert b.copy() == b
	assert b.copy() is not b
	b = _basebag('abc')
	assert b.copy() == b
	assert b.copy() is not b


def test_len():
	"""Test __len__."""
	assert len(_basebag()) == 0
	assert len(_basebag('abc')) == 3
	assert len(_basebag('aaba')) == 4


def test_contains():
	"""Test __contains__."""
	assert 'a' in _basebag('bbac')
	assert 'a' not in _basebag()
	assert 'a' not in _basebag('missing letter')


@pytest.mark.parametrize("bag_data, set_data", [
	('', ''),
	('a', 'a'),
	('ab', 'ab'),
	])
def test_compare_eq_set(bag_data, set_data):
	"""Test comparisons to Sets that should be equal."""
	assert _basebag(bag_data) == set(set_data)


@pytest.mark.parametrize("bag_data, set_data", [
	('ab', 'a'),
	('a', 'ab'),
	('aa', 'a'),
	('aa', 'ab'),
	('ac', 'ab'),
	])
def test_compare_ne_set(bag_data, set_data):
	assert not _basebag(bag_data) == set(set_data)


def test_compare_unorderable():
	assert not _basebag('ac') <= set('ab')
	assert not _basebag('ac') >= set('ab')


def test_rich_comp_equal():
	"""Test rich comparisons for equal bags."""
	assert _basebag() <= _basebag()
	assert not _basebag() < _basebag()
	assert _basebag() >= _basebag()
	assert not _basebag() > _basebag()
	b1 = _basebag('aabc')
	b2 = _basebag('aabc')
	assert not b2 > b1
	assert b2 >= b1
	assert not b2 < b1
	assert b2 <= b1


def test_rich_comp_superset():
	"""Test rich comparisons for bags that are supersets of other bags."""
	b1 = _basebag('aabc')
	b2 = _basebag('abc')
	assert b1 > b2
	assert b1 >= b2
	assert not b1 < b2
	assert not b1 <= b2


def test_rich_comp_subset():
	"""Test rich comparisons for bags that are subsets of other bags."""
	b1 = _basebag('abc')
	b2 = _basebag('aabc')
	assert not b1 > b2
	assert not b1 >= b2
	assert b1 < b2
	assert b1 <= b2


def test_rich_comp_unorderable_eq_len():
	"""Test rich comparisons for bags of equal length but unorderable."""
	b1 = _basebag('abb')
	b2 = _basebag('abc')
	assert not b1 < b2
	assert not b1 <= b2
	assert not b1 > b2
	assert not b1 >= b2
	assert not b1 == b2
	assert b1 != b2


def test_rich_comp_unorderable_diff_len():
	"""Test rich comparisons for bags of unequal length and unorderable."""
	b1 = _basebag('abd')
	b2 = _basebag('aabc')
	assert not b1 > b2
	assert not b1 >= b2
	assert not b1 < b2
	assert not b1 <= b2
	assert not b2 > b1
	assert not b2 >= b1
	assert not b2 < b1
	assert not b2 <= b1
	assert not b1 == b2
	assert b1 != b2


def test_rich_comp_type_mismatch():
	"""Test rich comparisons for bags with type mismatches."""
	with pytest.raises(TypeError):
		bag('abc') < 'abc'
	with pytest.raises(TypeError):
		bag('abc') <= 'abc'
	with pytest.raises(TypeError):
		bag('abc') > 'abc'
	with pytest.raises(TypeError):
		bag('abc') >= 'abc'
	with pytest.raises(TypeError):
		'abc' < bag('abc')
	with pytest.raises(TypeError):
		'abc' <= bag('abc')
	with pytest.raises(TypeError):
		'abc' > bag('abc')
	with pytest.raises(TypeError):
		'abc' >= bag('abc')
	assert not bag('abc') == 'abc'
	assert not 'abc' == bag('abc')


def test_comparison_chaining():
	assert bag('a') < bag('aa') <= bag('aa')


def test_and():
	"""Test __and__."""
	assert bag('aabc') & bag('aacd') == bag('aac')
	assert bag() & bag('safgsd') == bag()
	assert bag('abcc') & bag() == bag()
	assert bag('abcc') & bag('aabd') == bag('ab')
	assert bag('aabc') & set('abdd') == bag('ab')


def test_isdisjoint():
	"""Test isdisjoint."""
	assert bag().isdisjoint(bag())
	assert bag().isdisjoint(bag('abc'))
	assert not bag('ab').isdisjoint(bag('ac'))
	assert bag('ab').isdisjoint(bag('cd'))


def test_or():
	"""Test __or__."""
	assert bag('abcc') | bag() == bag('abcc')
	assert bag('abcc') | bag('aabd') == bag('aabccd')
	assert bag('aabc') | set('abdd') == bag('aabcd')


def test_add_op():
	"""Test __iadd__."""
	b1 = bag('abc')
	result = b1 + bag('ab')
	assert result == bag('aabbc')
	assert b1 == bag('abc')
	assert result is not b1


def test_add():
	"""Test __add__."""
	b = bag('abc')
	b.add('a')
	assert b == bag('aabc')


def test_clear():
	"""Test clear."""
	b = bag('abc')
	b.clear()
	assert b == bag()


def test_discard():
	"""Test discard."""
	b = bag('aabc')
	b.discard('a')
	assert b == bag('abc')
	b.discard('a')
	assert b == bag('bc')
	b.discard('a')
	assert b == bag('bc')


def test_sub():
	"""Test __sub__."""
	assert bag('abc') - bag() == bag('abc')
	assert bag('abbc') - bag('bd') == bag('abc')


def test_mul():
	"""Test __mul__."""
	assert bag('aab') * set('a') == bag((('a', 'a'), ('a', 'a'), ('b', 'a')))


def test_mul_empty_set():
	"""Test __mul__ on an empty set."""
	assert bag('aab') * set() == bag()


def test_product():
	"""Test product"""
	assert bag('aab').product(set('a'), operator=concat) == bag(('aa', 'aa', 'ba'))


def test_product_commutative():
	"""Test product for a commutative operator."""
	assert bag((1, 2)).product([2, 1], operator=mul) == bag((2, 1, 4, 2))


def test_xor():
	"""Test __xor__."""
	assert bag('abc') ^ bag() == bag('abc')
	assert bag('aabc') ^ bag('ab') == bag('ac')
	assert bag('aabcc') ^ bag('abcde') == bag('acde')


def test_ior():
	"""Test __ior__."""
	b = bag()
	b |= bag()
	assert b == bag()
	b = bag('aab')
	b |= bag()
	assert b == bag('aab')
	b = bag('aab')
	b |= bag('ac')
	assert b == bag('aabc')
	b = bag('aab')
	b |= set('ac')
	assert b == bag('aabc')


def test_iand():
	"""Test __iand__."""
	b = bag()
	b &= bag()
	assert b == bag()
	b = bag('aab')
	b &= bag()
	assert b == bag()
	b = bag('aab')
	b &= bag('ac')
	assert b == bag('a')
	b = bag('aab')
	b &= set('ac')
	assert b == bag('a')


def test_ixor():
	"""Test __ixor__."""
	b = bag('abbbccd')
	b ^= bag('bbcdg')
	assert b == bag('abcg')
	b = bag('bbcdg')
	b ^= bag('abbbccd')
	assert b == bag('acbg')
	b = bag('abbc')
	b ^= set('bg')
	assert b == bag('abcg')


def test_isub():
	"""Test __isub__ and discard_all."""
	b = bag('aabbc')
	b -= bag('bd')
	assert b == bag('aabc')
	b = bag('aabc')
	b -= set('bd')
	assert b == bag('aac')


def test_remove_all():
	b = bag('abc')
	with pytest.raises(ValueError):
		b.remove_all('cd')
	assert b == bag('abc')
	b.remove_all('bc')
	assert b == bag('a')


def test_iadd():
	"""Test __iadd__."""
	b = bag('abc')
	b += bag('cde')
	assert b == bag('abccde')
	b = bag('abc')
	b += 'cde'
	assert b == bag('abccde')


def test_hash():
	"""Test __hash__ vs an empty bag."""
	bag_with_empty_tuple = frozenbag([()])
	assert not hash(frozenbag()) == hash(bag_with_empty_tuple)
	assert not hash(frozenbag()) == hash(frozenbag((0,)))
	assert not hash(frozenbag('a')) == hash(frozenbag(('aa')))
	assert not hash(frozenbag('a')) == hash(frozenbag(('aaa')))
	assert not hash(frozenbag('a')) == hash(frozenbag(('aaaa')))
	assert not hash(frozenbag('a')) == hash(frozenbag(('aaaaa')))
	assert hash(frozenbag('ba')) == hash(frozenbag(('ab')))
	assert hash(frozenbag('badce')) == hash(frozenbag(('dbeac')))


def test_num_unique_elems():
	"""Test _basebag.num_unique_elements."""
	assert bag('abracadabra').num_unique_elements() == 5


def test_pop():
	"""Test bag.pop."""
	b = bag('a')
	assert b.pop() == 'a'
	with pytest.raises(KeyError):
		b.pop()


def test_hashability():
	"""Test __hash__ for bags.

	Since bag is mutable and frozenbag is hashable, the second
	should be usable for dictionary keys and the second should raise a key
	or value error when used as a key or placed in a set.
	"""
	a = bag([1, 2, 3])  # Mutable multiset.
	b = frozenbag([1, 1, 2, 3])	 # prototypical frozen multiset.

	c = frozenbag([4, 4, 5, 5, b, b])  # make sure we can nest them
	d = frozenbag([4, frozenbag([1, 3, 2, 1]), 4, 5, b, 5])
	# c and d are the same; make sure nothing weird happens to hashes.
	assert c == d  # Make sure both constructions work.

	dic = {
		b: 3,
		d: 5,
		d: 7,
		}
	assert len(dic) == 2  # Make sure no duplicates in dictionary.
	# Make sure TypeErrors are raised when using mutable bags for keys.
	with pytest.raises(TypeError):
		dic[a] = 4
	with pytest.raises(TypeError):
		frozenbag([a, 1])
	with pytest.raises(TypeError):
		bag([a, 1])
	# test commutativity of bag instantiation.
	assert bag([4, 4, 5, 5, c]) == bag([4, 5, d, 4, 5])
