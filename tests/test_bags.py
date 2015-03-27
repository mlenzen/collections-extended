
import pytest

from collections_extended.bags import _basebag, bag, frozenbag, _compat


def test_init():
	b = _basebag('abracadabra')
	assert b.count('a') == 5
	assert b.count('b') == 2
	assert b.count('r') == 2
	assert b.count('c') == 1
	assert b.count('d') == 1
	b2 = bag(b)
	assert b2 == b


def test_repr():
	ms = _basebag()
	assert ms == eval(ms.__repr__())
	ms = _basebag('abracadabra')
	assert ms == eval(ms.__repr__())


def compare_bag_string(b):
	s = str(b)
	return set(s.lstrip('{').rstrip('}').split(', '))


def test_str():
	assert str(_basebag()) == '_basebag()'
	assert "'a'^5" in str(_basebag('abracadabra'))
	assert "'b'^2" in str(_basebag('abracadabra'))
	assert "'c'" in str(_basebag('abracadabra'))
	abra_elems = set(("'a'^5", "'b'^2", "'r'^2", "'c'", "'d'"))
	assert compare_bag_string(bag('abracadabra')) == abra_elems
	if not _compat.is_py2:
		assert compare_bag_string(bag('abc')) == compare_bag_string(set('abc'))


def test_count():
	ms = _basebag('abracadabra')
	assert ms.count('a') == 5
	assert ms.count('x') == 0


def test_nlargest():
	abra = _basebag('abracadabra')
	sort_key = lambda e: (-e[1], e[0])
	abra_counts = [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1)]
	assert (sorted(abra.nlargest(), key=sort_key) == abra_counts)
	assert sorted(abra.nlargest(3), key=sort_key) == abra_counts[:3]
	assert _basebag('abcaba').nlargest(3) == [('a', 3), ('b', 2), ('c', 1)]


def test_from_map():
	assert _basebag._from_map({'a': 1, 'b': 2}) == _basebag('abb')


def test_copy():
	b = _basebag()
	assert b.copy() == b
	assert b.copy() is not b
	b = _basebag('abc')
	assert b.copy() == b
	assert b.copy() is not b


def test_len():
	assert len(_basebag()) == 0
	assert len(_basebag('abc')) == 3
	assert len(_basebag('aaba')) == 4


def test_contains():
	assert 'a' in _basebag('bbac')
	assert 'a' not in _basebag()
	assert 'a' not in _basebag('missing letter')


def test_le():
	assert _basebag() <= _basebag()
	assert _basebag() <= _basebag('a')
	assert _basebag('abc') <= _basebag('aabbbc')
	assert not _basebag('abbc') <= _basebag('abc')
	with pytest.raises(TypeError):
		bag('abc') < set('abc')
	assert not bag('aabc') < bag('abc')


def test_and():
	assert bag('aabc') & bag('aacd') == bag('aac')
	assert bag() & bag('safgsd') == bag()
	assert bag('abcc') & bag() == bag()
	assert bag('abcc') & bag('aabd') == bag('ab')
	assert bag('aabc') & set('abdd') == bag('ab')


def test_isdisjoint():
	assert bag().isdisjoint(bag())
	assert bag().isdisjoint(bag('abc'))
	assert not bag('ab').isdisjoint(bag('ac'))
	assert bag('ab').isdisjoint(bag('cd'))


def test_or():
	assert bag('abcc') | bag() == bag('abcc')
	assert bag('abcc') | bag('aabd') == bag('aabccd')
	assert bag('aabc') | set('abdd') == bag('aabcd')


def test_add_op():
	b1 = bag('abc')
	result = b1 + bag('ab')
	assert result == bag('aabbc')
	assert b1 == bag('abc')
	assert result is not b1


def test_add():
	b = bag('abc')
	b.add('a')
	assert b == bag('aabc')


def test_clear():
	b = bag('abc')
	b.clear()
	assert b == bag()


def test_discard():
	b = bag('abc')
	b.discard('a')
	assert b == bag('bc')
	b.discard('a')
	assert b == bag('bc')


def test_sub():
	assert bag('abc') - bag() == bag('abc')
	assert bag('abbc') - bag('bd') == bag('abc')


def test_mul():
	ms = _basebag('aab')
	assert ms * set('a') == _basebag(('aa', 'aa', 'ba'))
	assert ms * set() == _basebag()


def test_xor():
	assert bag('abc') ^ bag() == bag('abc')
	assert bag('aabc') ^ bag('ab') == bag('ac')
	assert bag('aabcc') ^ bag('abcde') == bag('acde')


def test_ior():
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
	b = bag('abbc')
	b ^= bag('bg')
	assert b == bag('abcg')
	b = bag('abbc')
	b ^= set('bg')
	assert b == bag('abcg')


def test_isub():
	b = bag('aabbc')
	b -= bag('bd')
	assert b == bag('aabc')
	b = bag('aabbc')
	b -= set('bd')
	assert b == bag('aabc')


def test_iadd():
	b = bag('abc')
	b += bag('cde')
	assert b == bag('abccde')
	b = bag('abc')
	b += 'cde'
	assert b == bag('abccde')


def test_hash():
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
	assert bag('abracadabra').num_unique_elements() == 5


def test_pop():
	b = bag('a')
	assert b.pop() == 'a'
	with pytest.raises(KeyError):
		b.pop()


def test_hashability():
	"""
	Since Multiset is mutable and FronzeMultiset is hashable, the second
	should be usable for dictionary keys and the second should raise a key
	or value error when used as a key or placed in a set.
	"""
	a = bag([1, 2, 3])  # Mutable multiset.
	b = frozenbag([1, 1, 2, 3])	 # prototypical frozen multiset.

	c = frozenbag([4, 4, 5, 5, b, b])  # make sure we can nest them
	d = frozenbag([4, frozenbag([1, 3, 2, 1]), 4, 5, b, 5])
	# c and d are the same; make sure nothing weird happes to hashes.
	assert c == d  # Make sure both constructions work.

	dic = {}
	dic[b] = 3
	dic[c] = 5
	dic[d] = 7
	assert len(dic) == 2  # Make sure no duplicates in dictionary.
	# Make sure TypeErrors are raised when using mutable bags for keys.
	with pytest.raises(TypeError):
		dic[a] = 4
	with pytest.raises(TypeError):
		set([a])
	with pytest.raises(TypeError):
		frozenbag([a, 1])
	with pytest.raises(TypeError):
		bag([a, 1])
	# test commutativity of multiset instantiation.
	assert bag([4, 4, 5, 5, c]) == bag([4, 5, d, 4, 5])
