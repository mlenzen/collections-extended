"""table - read, write and manipulate tabluar data."""
from collections import (
	Sequence,
	Set,
	MutableSequence,
	MutableSet,
	Hashable,
	)


from .setlists import setlist


class _TableView():

	def __init__(self, row, col):
		assert self.row.table == self.col.table
		self.row = row
		self.col = col

	@property
	def value(self):
		return self.table


class ColumnView():
	"""A Column of a Table."""

	def __init__(self, table, index):
		self._table = table
		self._index = index

	@property
	def table(self):
		return self._table

	@property
	def index(self):
		return self._index

	@property
	def name(self):
		return self.table.col_names[self.index]


class _RowValuesView():

	def __init__(self, table, index):
		self.table = table
		self.index = index

	def get_index_value(self, index):
		return self.table._data[self.index][index]

	def get_key_value(self, key):
		index = self.table.col_names.index(key)
		return self.table._data[self.index][index]


class RowView():
	"""A row of a Table."""

	def __init__(self, table, index):
		self._table = table
		self._index = index

	@property
	def table(self):
		return self._table

	@property
	def index(self):
		return self._index

	def __getitem__(self):
		raise NotImplementedError

	@property
	def values(self):
		raise NotImplementedError

	@values.setter
	def values(self, new_values):
		self.table.set_row_values(new_values)


class _RowContainer():

	def __init__(self, table):
		self.table = table

	def __getitem__(self, key):
		if isinstance(key, int):
			return self.index[key]
		else:
			return self.key[key]


class Table():
	"""A table."""

	def __init__(
		self,
		data=None,
		col_names=None,
		width=None,
		pkey_cols=None,
		pkey_col_names=None,
		default_value=None,
		default_func=None,
		allow_empty=True,
		):
		"""Create a Table.

		Args:
			data: A Sequence of Sequences
			col_names: A Sequence of Hashable objects
			width (int): New cols are created this wide. Pass this only if not
				passing col_names. Unnecessary if allow_empty == False.
			pkey_cols: A list of column indices to use as the primary key.
			pkey_col_names: A list of column names to use as the primary key.
			default_func: If present, a function to generate the default initial
				value for a cell.
			default_value: If no default_func, use this value as the default
			 	initial value for a cell.
			allow_empty: Allow rows to be created with missing values (to be
				filled with the default value).
		"""
		self.col_names = setlist()
		if col_names:
			try:
				self.col_names.extend(col_names)
			except ValueError:
				raise ValueError('col_names contains duplicate values')
			if width is not None and width != len(self.col_names):
				raise ValueError('passed width does not match length of col_names')
			self._width = len(col_names)
		else:
			self._width = width
		if pkey_col_names:
			if pkey_cols:
				raise ValueError('Cannot pass both pkey_cols and pkey_col_names')
			self._pkey_cols = tuple(self.col_names.index(col) for col in pkey_col_names)
		else:
			self._pkey_cols = tuple(pkey_cols)
		if default_value and default_func:
			raise ValueError('Cannot pass both default_func and default_value')
		self._default_value = default_value
		self._default_func = default_func
		self.allow_empty = allow_empty
		self._data = []
		if data:
			for row in data:
				self.add_row(values=row)

	@classmethod
	def from_list_of_dicts(cls, data, col_names, ignore_extras=False, raise_on_missing=True, **kwargs):
		"""

		Args:
			data (list): A list of dicts.
			col_names: Required
			ignore_extras (bool): If false, an exception is raised when a row
				contains a key that is not in col_names, otherwise ignore.
			raise_on_missing (bool): If true, raise an error for a row missing
				a key from col names instead of setting the value to the default.
			kwargs: Passed to Table.__init__
		"""
		table = cls(col_names=col_names, **kwargs)
		for row in data:
			row_d = dict(row)
			if raise_on_missing:
				row_values = [row_d.pop(col) for col in col_names]
			else:
				row_values = [row_d.pop(col, table.default) for col in col_names]
			if not ignore_extras and row_d:
				raise ValueError('Row contains an unknown value')
			table._data.append(row_values)
		return table

	@property
	def width(self):
		return self._width

	@property
	def values(self):
		raise NotImplementedError

	@property
	def cols(self):
		raise NotImplementedError

	@property
	def rows(self):
		raise NotImplementedError

	@property
	def default(self):
		if self._default_func:
			return self._default_func()
		else:
			return self._default_value

	def get_value(self, row_index, col_index):
		return self._data[row_index][col_index]

	def set_value(self, row_index, col_index, value):
		self._data[row_index][col_index] = value

	def add_row(self, values=None, raise_on_missing=None):
		if raise_on_missing is None:
			raise_on_missing = not self.allow_empty
		if values:
			values_list = list(values)
		else:
			values_list = []
		if self.width is not None:
			if len(values_list) > self.width:
				raise ValueError('Too many values for row')
			elif len(values_list) < self.width:
				if raise_on_missing:
					raise ValueError('Too few values for row')
				else:
					while len(values_list) < self.width:
						values_list.append(self.default)
		elif values_list:
			self._width = len(values_list)
		self._data.append(values_list)

	def set_row_values(self, row_index, values):
		values_list = list(values)
		if len(values_list) != len(self._data[row_index]):
			raise ValueError('values is wrong length')
		self._data[row_index] = values_list

	def set_col_values(self, col_index, values):
		if len(values) != len(self._data):
			raise ValueError('values is wrong length')
		for value, row in zip(values, self._data):
			row[col_index] = value

	def to_html():
		raise NotImplementedError
