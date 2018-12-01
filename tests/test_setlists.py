"""Test for setlist classes."""
import pytest

from collections_extended.setlists import setlist, frozensetlist


def test_init():
	"""Test __init__."""
	with pytest.raises(ValueError):
		setlist('aa', raise_on_duplicate=True)
	with pytest.raises(ValueError):
		setlist('aa', True)


def test_count():
	"""Test count."""
	sl = setlist('abcdea')
	assert sl.count('a') == 1
	assert sl.count('f') == 0
	assert sl.count('e') == 1


def test_index():
	"""Test index."""
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
	with pytest.raises(IndexError):
		sl.index('a', end=-10)


def test_sub_index():
	"""Test sub_index."""
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
	"""General setlist tests."""
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
	with pytest.raises(ValueError):
		sl.insert(1, 'e')
	sl.append('f')
	assert sl == setlist(('a', 'c', 'e', 'f'))


def test_operator_iadd():
	sl = setlist('abc')
	sl += setlist('de')
	assert sl == setlist('abcde')


def test_operator_add():
	assert setlist('abc') + setlist('def') == setlist('abcdef')
	with pytest.raises(TypeError):
		assert setlist('abc') + 'def' == setlist('abcdef')
	assert frozensetlist(range(2)) + frozensetlist([2]) == frozensetlist(range(3))
	assert setlist(range(2)) + frozensetlist([2]) == setlist(range(3))
	assert frozensetlist(range(2)) + setlist([2]) == frozensetlist(range(3))
	assert setlist(range(2)) + setlist([2]) == setlist(range(3))
	with pytest.raises(TypeError):
		setlist() + set()
	with pytest.raises(TypeError):
		setlist() + list()


def test_remove_all_works():
	sl = setlist('abcdefgh')
	sl.remove_all('acdh')
	assert sl == setlist(('befg'))


def test_remove_all_raises_on_all_missing():
	sl = setlist(range(5))
	with pytest.raises(ValueError):
		sl.remove_all([5, 6])


def test_remove_all_raises_on_some_missing():
	sl = setlist(range(5))
	with pytest.raises(ValueError):
		sl.remove_all([4, 5])
	assert sl == setlist(range(5))


def test_remove_all_raises_on_duplicates():
	sl = setlist(range(5))
	with pytest.raises(ValueError):
		sl.remove_all([4, 4])


def test_discard_all_works():
	sl = setlist(range(5))
	sl.discard_all([3, 4])
	assert sl == setlist(range(3))


def test_discard_all_ignores_some_missing_end():
	sl = setlist(range(5))
	sl.discard_all([4, 5])
	assert sl == setlist(range(4))


def test_discard_all_ignores_some_missing_beg():
	sl = setlist(range(5))
	sl.discard_all([-1, 0])
	assert sl == setlist([1, 2, 3, 4])


def test_discard_all_ignores_all_missing_end():
	sl = setlist(range(5))
	sl.discard_all([5, 6])
	assert sl == setlist(range(5))


def test_discard_all_ignores_all_missing_beg():
	sl = setlist(range(5))
	sl.discard_all([-2, -1])
	assert sl == setlist(range(5))


def test_discard_all_handles_duplicates():
	sl = setlist(range(5))
	sl.discard_all([3, 3])
	assert sl == setlist([0, 1, 2, 4])
	sl.discard_all([4, 4])
	assert sl == setlist([0, 1, 2])


def test_len():
	"""Test __len__."""
	assert len(setlist()) == 0
	assert len(setlist('a')) == 1
	assert len(setlist('ab')) == 2
	assert len(setlist('abc')) == 3


def test_shuffle():
	"""Test shuffle."""
	sl = setlist(range(100))
	sl.shuffle()
	assert sl != setlist(range(100))


def test_del():
	"""Test __delitem__."""
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


def test_getitem():
	"""Test __getitem__."""
	sl = setlist(range(10))
	assert sl[0] == 0
	assert sl[5] == 5
	assert sl[9] == 9
	with pytest.raises(IndexError):
		sl[10]
	assert sl[-1] == 9
	with pytest.raises(IndexError):
		sl[-11]
	assert sl[1:3] == setlist([1, 2])
	assert sl[1:6:2] == setlist([1, 3, 5])
	assert sl[6:1:-2] == setlist([6, 4, 2])


def test_setitem():
	"""Test __setitem__."""
	sl = setlist('abc')
	sl[0] = 'd'
	assert sl == setlist('dbc')
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
	sl = setlist(range(10))
	sl[0] = 'a'
	assert sl == setlist(['a'] + list(range(1, 10)))
	sl[9] = 'b'
	assert sl == setlist(['a'] + list(range(1, 9)) + ['b'])
	sl[-1] = 'c'
	assert sl == setlist(['a'] + list(range(1, 9)) + ['c'])
	with pytest.raises(IndexError):
		sl[-11] = 'd'
	assert sl == setlist(['a'] + list(range(1, 9)) + ['c'])
	with pytest.raises(IndexError):
		sl[10] = 'd'
	assert sl == setlist(['a'] + list(range(1, 9)) + ['c'])
	with pytest.raises(TypeError):
		sl[0:2] = 1
	sl = setlist(range(10))
	with pytest.raises(ValueError):
		sl[0:2] = [8, 9]
	with pytest.raises(ValueError):
		sl[-1:0:-2] = ['a', 'b']


@pytest.mark.parametrize('slice_, replacement', [
	(slice(0, 2), ['a', 'b']),
	(slice(2, 4), ['a', 'b']),
	(slice(7, 9), ['a', 'b']),
	(slice(2, -2), ['a', 'b']),
	(slice(2, 5, 2), ['a', 'b']),
	(slice(-1, None, -1), list(range(10))),
	])
def test_compare_set_slice_to_list(slice_, replacement):
	sl = setlist(range(10))
	sl[slice_] = replacement
	l = list(range(10))
	l[slice_] = replacement
	assert sl == setlist(l)


def test_delitem():
	"""Test __delitem__."""
	sl = setlist(range(10))
	del sl[9]
	assert sl == setlist(range(9))
	del sl[-1]
	assert sl == setlist(range(8))
	del sl[0]
	assert sl == setlist(range(1, 8))
	with pytest.raises(IndexError):
		del sl[10]


@pytest.mark.parametrize('slice_', [
	slice(0, 2),
	slice(6, 9),
	slice(3, 7),
	slice(7, 3, -1),
	slice(0, 7, 2),
	])
def test_compare_del_slice_to_list(slice_):
	sl = setlist(range(10))
	del sl[slice_]
	l = list(range(10))
	del l[slice_]
	assert sl == setlist(l)


def test_append_works():
	sl = setlist(range(2))
	sl.append(2)
	assert sl == setlist(range(3))


def test_append_unhashable_raises_type_error():
	sl = setlist()
	with pytest.raises(TypeError):
		sl.append(list())


def test_append_duplicate_raises_value_error():
	sl = setlist('a')
	with pytest.raises(ValueError):
		sl.append('a')


def test_extend_works():
	"""Test simple extend works."""
	sl = setlist(range(1))
	sl.extend([1, 2])
	assert sl == setlist(range(3))
	assert sl.index(0) == 0
	assert sl.index(1) == 1
	assert sl.index(2) == 2


def test_extend_fails_with_existing_values():
	"""Test extend with existing values fails."""
	sl = setlist(range(3))
	with pytest.raises(ValueError):
		sl.extend([1, 2])
	assert sl == setlist(range(3))


def test_extend_fails_with_some_existing_values():
	"""Test extend with some existing values fails and doesn't change the setlist."""
	sl = setlist(range(3))
	with pytest.raises(ValueError):
		sl.extend([4, 2])
	assert sl == setlist(range(3))


def test_extend_fails_with_duplicate_values():
	"""Test extend with duplicate values fails and doesn't change the setlist."""
	sl = setlist(range(3))
	with pytest.raises(ValueError):
		sl.extend([3, 3])
	assert sl == setlist(range(3))


def test_extend_fails_with_unhashable_value():
	sl = setlist()
	with pytest.raises(TypeError):
		sl.extend(['a', list()])
	assert sl == setlist()


def test_update():
	sl = setlist(range(3))
	sl.update([3])
	assert sl == setlist(range(4))


def test_update_with_duplicates():
	sl = setlist(range(3))
	sl.update([2, 3])
	assert sl == setlist(range(4))


def test_update_raises_type_error():
	sl = setlist()
	with pytest.raises(TypeError):
		sl.update([list()])


def test_hash():
	"""Test __hash__."""
	assert hash(frozensetlist('abc')) == hash(frozensetlist('abc'))
	assert hash(frozensetlist()) == hash(frozensetlist())


def test_hash_differs_with_order():
	assert hash(frozensetlist('abc')) != hash(frozensetlist('cab'))


def test_clear():
	"""Test clear."""
	sl = setlist(range(10))
	sl.clear()
	assert sl == setlist()


def test_discard():
	"""Test discard."""
	sl = setlist(range(10))
	sl.discard(9)
	assert sl == setlist(range(9))
	sl.discard(100)
	assert sl == setlist(range(9))


def test_add():
	"""Test add."""
	sl = setlist(range(10))
	sl.add(10)
	assert sl == setlist(range(11))
	sl.add(10)
	assert sl == setlist(range(11))


def test_remove():
	"""Test remove."""
	sl = setlist(range(10))
	sl.remove(9)
	assert sl == setlist(range(9))
	with pytest.raises(ValueError):
		sl.remove(100)


def test_eq():
	"""Test __eq__."""
	assert not setlist(range(10)) == list(range(10))
	assert not setlist(range(10)) == setlist(range(9))


def test_str():
	"""Test __str__."""
	assert str(setlist()) == '{[}]'
	assert str(setlist('abc')) == "{['a', 'b', 'c'}]"
	assert str(frozensetlist()) == 'frozensetlist()'
	assert str(frozensetlist('abc')) == "frozensetlist(('a', 'b', 'c'))"


def test_repr():
	"""Test __repr."""
	assert repr(setlist()) == 'setlist()'
	assert repr(setlist(range(4))) == 'setlist((0, 1, 2, 3))'
	assert repr(frozensetlist()) == 'frozensetlist()'
	assert repr(frozensetlist('abc')) == "frozensetlist(('a', 'b', 'c'))"


def test_copy():
	"""Test copy."""
	sl = setlist(range(10))
	copy = sl.copy()
	assert sl == copy
	assert sl is not copy
	sl = setlist(('1', (0, 1)))
	copy = sl.copy()
	assert sl == copy
	assert sl is not copy
	assert sl[1] is copy[1]


def test_is_subset():
	assert setlist('ab').issubset(setlist('abc'))
	assert setlist('abc').issubset(setlist('abc'))
	assert not setlist('abc').issubset(setlist('ab'))


def test_is_superset():
	assert not setlist('ab').issuperset(setlist('abc'))
	assert setlist('abc').issuperset(setlist('abc'))
	assert setlist('abc').issuperset(setlist('ab'))


def test_union():
	assert setlist('ab').union(setlist('bc')) == setlist('abc')
	assert setlist('ab').union('bc') == setlist('abc')
	assert setlist('ab') | setlist('bc') == setlist('abc')
	with pytest.raises(TypeError):
		assert setlist('ab') | 'bc' == setlist('abc')


def test_intersection():
	assert setlist('abd').intersection(setlist('bcd')) == setlist('bd')
	assert setlist('abd').intersection('bcd') == setlist('bd')
	assert setlist('abd') & setlist('bcd') == setlist('bd')
	with pytest.raises(TypeError):
		assert setlist('abd') & 'bcd' == setlist('bd')


def test_difference():
	assert setlist('abd').difference(setlist('bcd')) == setlist('a')
	assert setlist('abd').difference('bcd') == setlist('a')
	assert setlist('abd') - setlist('bcd') == setlist('a')
	with pytest.raises(TypeError):
		assert setlist('abd') - 'bcd' == setlist('a')


def test_symmetric_difference():
	assert setlist('abd').symmetric_difference(setlist('bcd')) == setlist('ac')
	assert setlist('abd').symmetric_difference('bcd') == setlist('ac')
	assert setlist('abd') ^ setlist('bcd') == setlist('ac')
	with pytest.raises(TypeError):
		assert setlist('abd') ^ 'bcd' == setlist('ac')


def test_intersection_update():
	sl = setlist('abd')
	sl.intersection_update(setlist('bcd'))
	assert sl == setlist('bd')
	sl = setlist('abd')
	sl.intersection_update('bcd')
	assert sl == setlist('bd')
	sl = setlist('abd')
	sl &= setlist('bcd')
	assert sl == setlist('bd')
	sl = setlist('abd')
	with pytest.raises(TypeError):
		sl &= 'bcd'


def test_difference_update():
	sl = setlist('abd')
	sl.difference_update(setlist('bcd'))
	assert sl == setlist('a')
	sl = setlist('abd')
	sl.difference_update('bcd')
	assert sl == setlist('a')
	sl = setlist('abd')
	sl -= setlist('bcd')
	assert sl == setlist('a')
	sl = setlist('abd')
	with pytest.raises(TypeError):
		sl -= 'bcd'


def test_symmetric_difference_update():
	sl = setlist('abd')
	sl.symmetric_difference_update(setlist('bcd'))
	assert sl == setlist('ac')
	sl = setlist('abd')
	sl.symmetric_difference_update('bcd')
	assert sl == setlist('ac')
	sl = setlist('abd')
	sl ^= setlist('bcd')
	assert sl == setlist('ac')
	sl = setlist('abd')
	with pytest.raises(TypeError):
		sl ^= 'bcd'


def test_union_update():
	sl = setlist('abd')
	sl |= setlist('bcd')
	assert sl == setlist('abdc')


def test_extend_update():
	sl = setlist('abd')
	sl += setlist('e')
	assert sl == setlist('abde')
	with pytest.raises(TypeError):
		sl += 'f'
	assert sl == setlist('abde')
	with pytest.raises(ValueError):
		sl += setlist('fe')
	assert sl == setlist('abde')


def test_sort():
	sl = setlist([4, 7, 1, 0])
	sl.sort()
	assert sl == setlist([0, 1, 4, 7])
	sl = setlist([])
	sl.sort()
	assert sl == setlist()
	sl = setlist(['a9', 'b7', 'c5'])
	sl.sort(key=lambda i: i[1])
	assert sl == setlist(['c5', 'b7', 'a9'])


def test_tuple_keys():
	# https://github.com/mlenzen/collections-extended/issues/83
	sl = setlist()
	sl.add((1, 2, 3))
	with pytest.raises(ValueError):
		sl.append((1, 2, 3))
	assert sl == setlist([(1, 2, 3)])


def assert_internal_structure(sl):
	print(sl._list)
	print(sl._dict)
	for i, elem in enumerate(sl):
		assert sl._dict[elem] == i
	assert len(sl._dict) == len(sl._list)


def test_swap():
	sl = setlist('abcdef')
	sl.swap(1, 2)
	assert_internal_structure(sl)
	assert sl == setlist('acbdef')
	sl.swap(-1, 1)
	assert_internal_structure(sl)
	assert sl == setlist('afbdec')
