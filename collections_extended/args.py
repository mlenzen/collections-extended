from collections.abc import Collection
from functools import wraps
from typing import Any, Callable, Iterable, Mapping, Tuple, Union

from .indexed_dict import IndexedDict


class Args(Collection):
	"""Store the arguments of a function."""

	def __init__(self, args: Iterable[Any] = None, kwargs: Mapping[str, Any] = None):
		self.args: Tuple[Any] = tuple(args or [])
		self.kwargs: Mapping[str, Any] = IndexedDict(kwargs or {})

	# def __str__(self):
	# 	raise NotImplementedError

	def __contains__(self, item):
		return item in self.args or item in self.kwargs.values()

	def __iter__(self):
		yield from self.args
		yield from self.kwargs.values()

	def __len__(self):
		return len(self.args) + len(self.kwargs)

	def __getitem__(self, item: Union[int, str]):
		if isinstance(item, int):
			if item < 0:
				raise IndexError
			elif item < len(self.args):
				return self.args[item]
			else:
				kwarg_index = item - len(self.args)
				if kwarg_index >= len(self.kwargs):
					raise IndexError
				for i, val in enumerate(self.kwargs.values()):
					if i == kwarg_index:
						return val
				# This is logically unreachable
				raise RuntimeError
		elif isinstance(item, str):
			return self.kwargs[item]
		raise TypeError

	def __eq__(self, other):
		if not isinstance(other, Args):
			return False
		return (self.args, self.kwargs) == (other.args, other.kwargs)


def save_args(func: Callable) -> Callable:
	"""Introspect a function, adding the args as an attribute."""
	print('save_args')

	@wraps(func)
	def wrapper(*args, **kwargs):
		print('wrapper')
		func.args = Args(args, kwargs)
		return func(args, *args, **kwargs)

	return wrapper


class TestArgs:

	def test_init_empty(self):
		args = Args()
		assert len(args) == 0
		assert args.args == tuple()
		assert args.kwargs == {}

	def test_init_one_arg(self):
		args = Args('a')
		assert len(args) == 1
		assert args.args == ('a', )
		assert args.kwargs == {}

	def test_init_mult_args(self):
		args = Args('abc')
		assert len(args) == 3
		assert args.args == tuple('abc')
		assert args.kwargs == {}

	def test_init_one_kwarg(self):
		args = Args(None, {'kwarg1': 2})
		assert len(args) == 1
		assert args.args == tuple()
		assert args.kwargs == {'kwarg1': 2}

	def test_init_mult_kwargs(self):
		args = Args(kwargs={'kwarg0': 'a', 'kwarg1': 2})
		assert len(args) == 2
		assert args.args == tuple()
		assert args.kwargs == {'kwarg0': 'a', 'kwarg1': 2}

	def test_init_combo(self):
		args = Args('abc', {'kwarg3': 'd', 'kwarg4': 'e'})
		assert len(args) == 5
		assert args.args == tuple('abc')
		assert args.kwargs == {'kwarg3': 'd', 'kwarg4': 'e'}


def test_save_args_no_parens():

	@save_args
	def inner(args, arg0, kwarg1=None):
		print('inner')
		print(args)
		return args

	assert inner('a', kwarg1=2) == Args('a', {'kwargs1': 2})


def test_save_args_parens():

	@save_args()
	def inner(args, arg0, kwarg1=None):
		print('inner2')
		print(args)
		return args

	assert inner('a') == Args('a', {'kwargs1': None})
