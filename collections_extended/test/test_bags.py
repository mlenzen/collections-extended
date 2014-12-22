
from ..bags import _basebag, bag, frozenbag


def test_init():
	b =_basebag('abracadabra')
	assert b.count('a') == 5
	assert b.count('b') == 2
	assert b.count('r') == 2
	assert b.count('c') == 1
	assert b.count('d') == 1


def test_repr():
	ms = _basebag()
	assert ms == eval(ms.__repr__())
	ms = _basebag('abracadabra')
	assert ms == eval(ms.__repr__())


def test_str():
	assert str(_basebag()) == '_basebag()'
	assert "'a'^5" in str(_basebag('abracadabra'))
	assert "'b'^2" in str(_basebag('abracadabra'))
	assert "'c'" in str(_basebag('abracadabra'))
	assert str(_basebag('abc')) == str(set('abc'))


def test_count():
	ms = _basebag('abracadabra')
	assert ms.count('a') == 5
	assert ms.count('x') == 0


def test_nlargest():
	assert sorted(_basebag('abracadabra').nlargest(), key=lambda e: (-e[1], e[0])) == [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1)]
	assert sorted(_basebag('abracadabra').nlargest(3), key=lambda e: (-e[1], e[0])) == [('a', 5), ('b', 2), ('r', 2)]
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


def test_and():
	assert bag('aabc') & bag('aacd') == bag('aac')
	assert bag() & bag('safgsd') == bag()


def test_isdisjoint():
	assert bag().isdisjoint(bag())
	assert bag().isdisjoint(bag('abc'))
	assert not bag('ab').isdisjoint(bag('ac'))
	assert bag('ab').isdisjoint(bag('cd'))


def test_or():
	assert bag('abcc') | bag() == bag('abcc')
	assert bag('abcc') | bag('aabd') == bag('aabccd')
	assert bag('aabc') | set('abdd') == bag('aabcd')


def test_add():
	assert bag('abcc') & bag() == bag()
	assert bag('abcc') & bag('aabd') == bag('ab')
	assert bag('aabc') & set('abdd') == bag('ab')


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


def test_ixor():
	b = bag('abbc')
	b ^= bag('bg')
	assert b == bag('abcg')


def test_isub():
	b = bag('aabbc')
	b -= bag('bd')
	assert b == bag('aabc')


def test_iadd():
	b = bag('abc')
	b += bag('cde')
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
