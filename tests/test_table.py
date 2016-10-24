"""Test collections_extended.Table."""
import pytest

from collections_extended.table import Table


def test_init():
	data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	t1 = Table(data, col_names=['a', 'b', 'c'], pkey_cols=[0])
	t2 = Table(data, col_names=['a', 'b', 'c'], pkey_col_names=['a'])
	assert t1 == t2


def test_cell_access():
	data = [['x', 2, 3], ['y', 5, 6], ['z', 8, 9]]
	t = Table(data, col_names=['a', 'b', 'c'], pkey_cols=[0])
	assert t[0][0] == 'x'
	assert t[2][1] == 8
	assert t['y'][1] == 5
	assert t[1]['c'] == 6
	assert t['z']['c'] == 9


def test_col_names():
	data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	t = Table(data, col_names=['a', 'b', 'c'])
	assert t.cols['a'] == [1, 4, 7]
	assert t.cols.name['b'] == [2, 5, 8]
	assert t.cols.n['c'] == [3, 6, 9]


def test_numbers_as_col_names():
	data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	t = Table(data, col_names=[1, 2, 3])
	assert t.cols[1] == [2, 5, 8]
	assert t.cols.n[1] == [1, 4, 7]
	assert t.cols.i[1] == [2, 5, 8]
	assert t.cols.name[3] == [3, 6, 9]
	assert t.cols.index[0] == [1, 4, 7]


def test_row_keys():
	data = [['a', 1, 2], ['b', 5, 10]]
	t = Table(data, pkey_cols=[0])
	assert t.rows['a'] == ['a', 1, 2]
	assert t.rows[0] == ['a', 1, 2]
	assert t.rows.key['b'] == ['b', 5, 10]
	assert t.rows.index[1] == ['b', 5, 10]


def test_ints_as_row_keys():
	data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	t = Table(data, pkey_cols=[0])
	assert t.rows[1] == [4, 5, 6]
	assert t.rows.k[1] == [1, 2, 3]
	assert t.rows.i[1] == [4, 5, 6]
	assert t.rows.key[3] == [7, 8, 9]
	assert t.rows.index[0] == [1, 2, 3]
	with pytest.raises(IndexError):
		t.i[3]
	with pytest.raises(IndexError):
		t[3]
	with pytest.raises(KeyError):
		t.key[0]
